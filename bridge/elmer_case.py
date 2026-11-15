"""The Elmer case for a mesh from mesh25d: the sif, its circuits and the run.

Every coil is a massive conductor of Elmer's circuit module, opened at its terminals: two faces of its copper
(the two ends of a cut trace, or the two pads of a left-out via) are its electrodes. WPotentialSolver puts a
potential W from 0 on one to 1 on the other through the coil's copper, and the coil's voltage drives the current
along grad W. A circuit fixes the current through each coil: 1 A for the driven coil, 0 A for a receiver, whose
circuit voltage is then its open-circuit EMF. L, R and M follow from V / I.

Why open coils: Elmer's massive coils in 3D always take their direction from the nodal W potential's gradient
(CircuitsAndDynamics.F90, Add_massive), so a closed massive coil, whose potential would jump across a cut, cannot
be driven; "Coil Use W Vector" and CoilSolver's closed coils serve stranded coils only.

What makes the voltage unique: with electrodes inside the domain, a gradient added to A (curl free, so no field
energy) can carry the coil voltage instead of the circuit's V, and the system is singular. Elmer's own examples
avoid it by putting the electrodes on the outer boundary, where n x A = 0. The bridge does the same in small: a
port sheet, a few faces across the gap from one electrode to the other with n x A = 0 on them (the lumped port
of a circuit model), pins it. The coil's scalar potential is on (Activate Constraint) and held at 0 on both
electrodes, as Elmer's automatic electrode condition does on outer electrodes.

What the voltage holds: then the circuit voltage is I R plus j omega times the line integral of A round the
whole loop, the copper and the sheet (where A along it is 0): the loop's EMF, gap included. The sheet forces
the field's normal component through itself to 0; it is a fraction of a square millimetre and the error is
in the third decimal.

Conductors that are not coils (a rotor's copper, a plate) are ordinary conducting bodies: eddy currents flow in
them, with their scalar potential, and nothing drives them.
"""
from __future__ import annotations

import math
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

ELMER_BIN = Path(__file__).resolve().parent.parent / 'Solver_Elmer' / 'install' / 'bin'
MU0 = 1.25663706212e-6
EPS0 = 8.8541878128e-12


@dataclass
class Coil:
    """A massive coil opened at two electrodes. body: its mesh body. current: the circuit's fixed current in A
    (0 for a receiver). t_low, t_high: the electrodes, the mesh boundaries where W = 0 and W = 1. sheet: the
    port sheet's boundary (n x A = 0), the faces across the gap joining the two electrodes."""
    name: str
    body: str
    t_low: str
    t_high: str
    sheet: str
    current: complex = 1.0


@dataclass
class Material:
    name: str
    sigma: float = 0.0
    mu_r: float = 1.0
    eps_r: float = 1.0


@dataclass
class Case:
    mesh_dir: Path
    bodies: dict                      # mesh body name -> Material, every body of the mesh
    coils: list
    outer: str = 'OUTER'              # the domain's outside: n x A = 0
    order: int = 1                    # 1: Whitney edge elements, 2: second order (Quadratic Approximation)
    solver: str = 'iterative'         # 'iterative' (BiCGStabL or GCR, circuit preconditioner) or 'mumps'
    method: str = 'BiCGStabL'         # BiCGStabL needs little memory; GCR keeps `restart` vectors
    bicg_degree: int = 4
    restart: int = 50
    tol: float = 1e-9
    max_iter: int = 6000
    save_fields: bool = False         # write the VTU (big); the scalars are always saved
    extra_calc: list = field(default_factory=list)


def _vec(v):
    return ' '.join(repr(float(x)) for x in v)


def circuit_lines(coils):
    """One circuit per coil: a current source in series with the coil. Unknowns i_src, i_coil, v_src, v_coil, u.
    The source's row fixes i_src = I_n_Source; Kirchhoff's current law makes the coil's current the same."""
    out = [f'$ Circuits = {len(coils)}']
    for n, c in enumerate(coils, 1):
        C = f'C.{n}'
        out += [f'! circuit {n}: {c.name}, a fixed current through the coil',
                f'$ {C}.variables = 5',
                f'$ {C}.perm = zeros({C}.variables)',
                f'$ {C}.A = zeros({C}.variables,{C}.variables)',
                f'$ {C}.B = zeros({C}.variables,{C}.variables)',
                f'$ {C}.name.1 = "i_I{n}"',
                f'$ {C}.name.2 = "i_component({n})"',
                f'$ {C}.name.3 = "v_I{n}"',
                f'$ {C}.name.4 = "v_component({n})"',
                f'$ {C}.name.5 = "u_{n}_circuit_{n}"',
                f'$ {C}.source.5 = "I{n}_Source"',
                f'$ {C}.B(0,0) = -1', f'$ {C}.B(0,1) = 1',
                f'$ {C}.B(1,2) = 1', f'$ {C}.B(1,4) = -1',
                f'$ {C}.B(2,3) = -1', f'$ {C}.B(2,4) = 1',
                f'$ {C}.B(4,0) = 1', '']
    return out


def write_sif(case: Case, folder, freq_hz, name='case'):
    """Write <folder>/<name>.sif for one frequency, the mesh linked in as <folder>/mesh. Returns its path."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    mesh = Path(case.mesh_dir).resolve()
    link = folder / 'mesh'
    if link.is_symlink():
        link.unlink()
    elif link.exists():
        shutil.rmtree(link)
    os.symlink(mesh, link)
    omega = 2 * math.pi * freq_hz
    coil_of = {c.body: n for n, c in enumerate(case.coils, 1)}
    mats = []
    for m in case.bodies.values():
        if m not in mats:
            mats.append(m)
    L = ['Header', '  CHECK KEYWORDS Warn', '  Mesh DB "." "mesh"', f'  Results Directory "res_{name}"', 'End', '',
         'Simulation', '  Max Output Level = 5', '  Coordinate System = "Cartesian"',
         '  Coordinate Scaling = 0.001', '  Simulation Type = "Steady"', f'  Angular Frequency = {omega!r}',
         '  Steady State Max Iterations = 1', '  Output Intervals(1) = 1', '  Use Mesh Names = True', 'End', '',
         'Constants', f'  Permittivity of Vacuum = {EPS0!r}', f'  Permeability of Vacuum = {MU0!r}', 'End', '']
    for i, (bname, m) in enumerate(case.bodies.items(), 1):
        L += [f'Body {i}', f'  Name = "{bname}"', f'  Equation = {2 if bname in coil_of else 1}',
              f'  Material = {mats.index(m) + 1}']
        if bname in coil_of:
            L.append(f'  Body Force = {coil_of[bname]}')
        L += ['End', '']
    for i, m in enumerate(mats, 1):
        L += [f'Material {i}', f'  Name = "{m.name}"', f'  Electric Conductivity = {m.sigma!r}',
              f'  Relative Permeability = {m.mu_r!r}', f'  Relative Permittivity = {m.eps_r!r}', 'End', '']
    L += circuit_lines(case.coils)
    for n, c in enumerate(case.coils, 1):
        cur = complex(c.current)
        L += [f'Component {n}', f'  Name = "{c.name}"', f'  Master Bodies Name = {c.body}',
              '  Coil Type = "Massive"', '  Activate Constraint = Logical True', 'End', '',
              f'Body Force {n}', f'  I{n}_Source re = Real {cur.real!r}', f'  I{n}_Source im = Real {cur.imag!r}',
              'End', '']
    bcs = [(case.outer, ['  A re {e} = Real 0', '  A im {e} = Real 0'])]
    for c in case.coils:
        bcs += [(c.t_low, ['  W = Real 0', '  A re = Real 0', '  A im = Real 0']),
                (c.t_high, ['  W = Real 1', '  A re = Real 0', '  A im = Real 0']),
                (c.sheet, ['  A re {e} = Real 0', '  A im {e} = Real 0'])]
    for i, (bname, lines) in enumerate(bcs, 1):
        L += [f'Boundary Condition {i}', f'  Name = "{bname}"'] + lines + ['End', '']
    e1 = [2, 3, 4, 5] + ([7] if case.save_fields else [])
    e2 = [1] + e1
    L += ['Equation 1', f'  Active Solvers({len(e1)}) = ' + ' '.join(map(str, e1)), 'End', '',
          'Equation 2', f'  Active Solvers({len(e2)}) = ' + ' '.join(map(str, e2)), 'End', '']
    L += ['Solver 1', '  Exec Solver = Before All', '  Equation = "W potential"',
          '  Procedure = "WPotentialSolver" "Wsolve"', '  Variable = W',
          '  Linear System Solver = Iterative', '  Linear System Iterative Method = CG',
          '  Linear System Preconditioning = ILU0', '  Linear System Max Iterations = 10000',
          '  Linear System Convergence Tolerance = 1.0e-12', '  Linear System Abort Not Converged = True',
          '  Linear System Residual Output = 1000', 'End', '',
          'Solver 2', '  Exec Solver = Always', '  Equation = Circuits', '  Variable = X',
          '  No Matrix = Logical True', '  Procedure = "CircuitsAndDynamics" "CircuitsAndDynamicsHarmonic"',
          'End', '',
          'Solver 3', '  Equation = "MGDynamics"', '  Variable = "A[A re:1 A im:1]"',
          '  Procedure = "MagnetoDynamics" "WhitneyAVHarmonicSolver"', f'  Angular Frequency = {omega!r}',
          '  Export Lagrange Multiplier = Logical True']
    if case.order == 2:
        L.append('  Quadratic Approximation = Logical True')
    if case.solver == 'mumps':
        L += ['  Linear System Solver = Direct', '  Linear System Direct Method = MUMPS']
    else:
        L += ['  Linear System Symmetric = Logical True', '  Linear System Complex = Logical True',
              '  Linear System Solver = Iterative', f'  Linear System Iterative Method = {case.method}',
              f'  BiCGstabL Polynomial Degree = {case.bicg_degree}', f'  Linear System GCR Restart = {case.restart}',
              '  Linear System Preconditioning = Circuit', f'  Linear System Convergence Tolerance = {case.tol!r}',
              f'  Linear System Max Iterations = {case.max_iter}', '  Linear System Residual Output = 50',
              '  Linear System Abort Not Converged = False']
    L += ['  Steady State Convergence Tolerance = 1e-6', 'End', '',
          'Solver 4', '  Equation = "MGDynamicsCalc"', '  Procedure = "MagnetoDynamics" "MagnetoDynamicsCalcFields"',
          '  Potential Variable = String "A"', '  Calculate Current Density = Logical True',
          '  Calculate Magnetic Vector Potential = Logical True', '  Calculate Elemental Fields = Logical True',
          '  Calculate Nodal Fields = Logical False', '  Discontinuous Bodies = Logical True',
          '  Steady State Convergence Tolerance = 0', '  Linear System Solver = "Iterative"',
          '  Linear System Iterative Method = CG', '  Linear System Preconditioning = None',
          '  Linear System Max Iterations = 5000', '  Linear System Convergence Tolerance = 1.0e-9']
    L += [f'  {x}' for x in case.extra_calc]
    L += ['End', '',
          'Solver 5', '  Exec Solver = Always', '  Equation = Circuits Output',
          '  Procedure = "CircuitsAndDynamics" "CircuitsOutput"', 'End', '',
          'Solver 6', '  Exec Solver = After All', '  Equation = "sv"', '  Procedure = "SaveData" "SaveScalars"',
          f'  Filename = scalars_{name}.dat', 'End', '']
    if case.save_fields:
        L += ['Solver 7', '  Exec Solver = After All', '  Equation = "vtu"',
              '  Procedure = "ResultOutputSolve" "ResultOutputSolver"', f'  Output File Name = "{name}"',
              '  Vtu Format = Logical True', '  Binary Output = Logical True', '  Discontinuous Bodies = Logical True',
              '  Save Geometry Ids = Logical True', 'End', '']
    sif = folder / f'{name}.sif'
    sif.write_text('\n'.join(L) + '\n')
    return sif


def _peak_kb(pid):
    """The peak resident memory of a running process, in kB (Linux), or 0 where /proc has no answer."""
    try:
        for line in open(f'/proc/{pid}/status'):
            if line.startswith('VmHWM:'):
                return int(line.split()[1])
    except OSError:
        pass
    return 0


def run(sif, threads=4, log=print, timeout=None):
    """Run ElmerSolver on a sif in its folder. Returns (seconds, log path, peak memory in GB)."""
    import time
    sif = Path(sif)
    env = dict(os.environ)
    env['PATH'] = f'{ELMER_BIN}:{env.get("PATH", "")}'
    env['OMP_NUM_THREADS'] = str(threads)
    logf = sif.with_suffix('.log')
    t0 = time.time()
    peak = 0
    with open(logf, 'w') as fh:
        p = subprocess.Popen([str(ELMER_BIN / 'ElmerSolver'), sif.name], cwd=sif.parent, stdout=fh,
                             stderr=subprocess.STDOUT, env=env)
        while True:
            try:
                p.wait(timeout=1.0)
                break
            except subprocess.TimeoutExpired:
                peak = max(peak, _peak_kb(p.pid))
                if timeout and time.time() - t0 > timeout:
                    p.kill()
                    raise
    dt = time.time() - t0
    text = logf.read_text(errors='replace')
    if p.returncode or 'ERROR' in text:
        err = [l for l in text.splitlines() if 'ERROR' in l or 'Fatal' in l]
        raise RuntimeError(f'ElmerSolver failed ({p.returncode}) on {sif}: ' + '; '.join(err[-3:]))
    log(f'ElmerSolver {sif.name}: {dt:.0f} s, peak memory {peak / 1048576:.2f} GB')
    return dt, logf, peak / 1048576


def read_scalars(folder, name='case'):
    """The saved scalars as {name: value}, from scalars_<name>.dat and its .names file."""
    folder = Path(folder)
    dat = next(iter(sorted(folder.glob(f'res_{name}/scalars_{name}.dat'))), None) or folder / f'scalars_{name}.dat'
    names = Path(str(dat) + '.names').read_text().splitlines()
    cols = []
    for line in names:
        m = re.match(r'\s*(\d+):\s*(.*)$', line)
        if m:
            cols.append(m.group(2).strip())
    vals = [float(x) for x in dat.read_text().split()]
    vals = vals[-len(cols):]
    return dict(zip(cols, vals))


def coil_results(scalars, coils, freq_hz):
    """V, I and Z of each coil from the circuit outputs."""
    omega = 2 * math.pi * freq_hz
    out = {}
    for n, c in enumerate(coils, 1):
        def get(kind):
            re_ = next((v for k, v in scalars.items() if k.endswith(f'{kind}_component({n}) re')), None)
            im_ = next((v for k, v in scalars.items() if k.endswith(f'{kind}_component({n}) im')), None)
            return None if re_ is None else complex(re_, im_ or 0.0)
        v, i = get('v'), get('i')
        z = v / i if (v is not None and i and abs(i) > 1e-12) else None
        out[c.name] = dict(V=v, I=i, Z=z, R=z.real if z else None, L=z.imag / omega if z else None)
    # an undriven coil (0 A) next to one driven coil: its open-circuit voltage over the driving current is the
    # mutual impedance, and its imaginary part over omega the mutual inductance (positive when both coils run
    # the same way from t_low to t_high)
    driven = [c for c in coils if abs(complex(c.current)) > 0]
    if len(driven) == 1:
        i_d = out[driven[0].name]['I']
        for c in coils:
            r = out[c.name]
            if c is not driven[0] and r['V'] is not None and i_d:
                zm = r['V'] / i_d
                r.update(Zm=zm, M=zm.imag / omega, Rm=zm.real, driven_by=driven[0].name)
    return out
