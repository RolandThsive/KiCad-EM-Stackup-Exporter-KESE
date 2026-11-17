"""The PyPEEC input for a set of voxels, running PyPEEC, and its answer read back.

PyPEEC (github.com/otvam/pypeec, MPL-2.0) solves the magneto-quasi-static field of conductors drawn as voxels with
the PEEC method: the copper alone carries unknowns, the air needs no mesh, and the couplings between voxels are
products with FFTs on the grid. Each conductor is a domain with copper's resistivity (scaled per copper sheet, see
voxels.py). Each coil has two terminals (ports.py): a current source drives its current into the first and a 0 V
source takes it out of the second, so the coil's voltage is the first terminal's. A receiver is driven with 0 A, so
its voltage is the open-circuit EMF the driven coil induces in it. A conductor with no terminals (a rotor, a shield)
carries eddy currents only; PyPEEC needs a source on every piece of copper, so one of its voxels is held at 0 V, which
lets no current in or out (it is the piece's only connection).

PyPEEC runs in a process of its own for each solve (run), as the Elmer branch runs ElmerSolver, so that its peak
memory is measured and given back after every solve.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .voxels import flat

HERE = Path(__file__).resolve().parent
TOLERANCE = HERE / 'tolerance.yaml'       # PyPEEC's own default tolerances, with the changes listed at its top


@dataclass
class Coil:
    """A conductor opened at two terminals. body: its voxels' body name. t1, t2: the terminals' voxel indices
    (ports.terminals). current: the fixed current in A driven from t1 through the copper to t2 (0 for a receiver)."""
    name: str
    body: str
    t1: np.ndarray
    t2: np.ndarray
    current: complex = 1.0


@dataclass
class Case:
    grid: object                      # voxels.Grid
    vox: dict                         # body -> {'sheet k' | 'between': indices}, the terminals already taken out
    coils: list
    sigma: dict = field(default_factory=dict)   # body -> S/m (copper's 5.8e7 where missing)
    floating: list = field(default_factory=list)   # bodies with no terminals: one voxel each held at 0 V
    tolerance: dict = field(default_factory=dict)  # changes to tolerance.yaml for this case (nested keys)


def _rho(case, body, key):
    """The resistivity of a body's voxels in one sheet (scaled to keep the sheet resistance) or between sheets."""
    rho = 1.0 / case.sigma.get(body, 5.8e7)
    if key.startswith('sheet '):
        rho *= case.grid.sheets[int(key.split()[1])]['scale']
    return rho


def _sheet_key(case, idx):
    """The sheet most of a terminal's voxels lie in ('between' if none)."""
    _, _, iz = case.grid.ijk(idx)
    s = case.grid.sheet_of_layer[iz]
    s = s[s >= 0]
    return f'sheet {np.bincount(s).argmax()}' if len(s) else 'between'


def inputs(case, freq_hz):
    """PyPEEC's geometry (voxel mesher) and problem as dicts, and a description of the domains."""
    g = case.grid
    dom, mats = {}, {}
    groups, insulated = {}, []

    def add(name, idx, body, key):
        dom[name] = np.asarray(idx, int).tolist()
        mats.setdefault((body, key), []).append(name)
    srcs = {}
    for c in case.coils:
        names = []
        for k, idx in case.vox[c.body].items():
            if len(idx):
                add(f'{c.body}|{k}', idx, c.body, k)
                names.append(f'{c.body}|{k}')
        for t, idx in (('T1', c.t1), ('T2', c.t2)):
            add(f'{c.name}_{t}', idx, c.body, _sheet_key(case, idx))
        srcs[f'{c.name}_T1'] = dict(kind='current', value=complex(c.current))
        srcs[f'{c.name}_T2'] = dict(kind='voltage', value=0j)
        groups[c.name] = {'domain_group': [names, [f'{c.name}_T1'], [f'{c.name}_T2']], 'connected': True}
        insulated.append([f'{c.name}_T1'])               # one domain per conductor: PyPEEC's check pairs the groups'
                                                          # domains one to one, so groups of unequal size break it
    for b in case.floating:
        allv = flat(case.vox[b])
        if not len(allv):
            continue
        ref = allv[:1]
        names = []
        for k, idx in case.vox[b].items():
            idx = np.setdiff1d(idx, ref)
            if len(idx):
                add(f'{b}|{k}', idx, b, k)
                names.append(f'{b}|{k}')
        add(f'{b}_REF', ref, b, _sheet_key(case, ref))
        srcs[f'{b}_REF'] = dict(kind='voltage', value=0j)
        insulated.append([f'{b}_REF'])
    if len(insulated) > 1:
        groups['insulation'] = {'domain_group': insulated, 'connected': False}
    geometry = {
        'mesh_type': 'voxel',
        'data_voxelize': {'param': {'n': [g.nx, g.ny, g.nz], 'd': [g.d * 1e-3, g.d * 1e-3, g.dz * 1e-3],
                                    'c': [float(g.x0 + g.nx * g.d / 2) * 1e-3, float(g.y0 + g.ny * g.d / 2) * 1e-3,
                                          float(g.z_layer.mean()) * 1e-3]},
                          'domain_index': dom},
        'data_point': {'check_cloud': False, 'filter_cloud': False, 'pts_cloud': []},
        'data_resampling': {'use_reduce': False, 'use_resample': False, 'resampling_factor': [1, 1, 1]},
        'data_conflict': {'resolve_rules': False, 'resolve_random': False, 'conflict_rules': []},
        'data_integrity': {'check_integrity': True, 'domain_connected': groups, 'domain_adjacent': {}},
    }
    mat_def, mat_val = {}, {}
    for n, ((body, key), names) in enumerate(sorted(mats.items())):
        tag = f'm{n}_{body}|{key}'
        mat_def[tag] = {'domain_list': names, 'material_type': 'electric', 'orientation_type': 'isotropic',
                        'var_type': 'lumped'}
        mat_val[tag] = {'rho_re': _rho(case, body, key), 'rho_im': 0.0}
    src_def, src_val = {}, {}
    for name, s in srcs.items():
        src_def[name] = {'domain_list': [name], 'source_type': s['kind'], 'var_type': 'lumped'}
        v = s['value']
        src_val[name] = ({'I_re': v.real, 'I_im': v.imag, 'Y_re': 0.0, 'Y_im': 0.0} if s['kind'] == 'current' else
                         {'V_re': v.real, 'V_im': v.imag, 'Z_re': 0.0, 'Z_im': 0.0})
    problem = {'material_def': mat_def, 'source_def': src_def,
               'sweep_solver': {'ac': {'init': None, 'param': {'freq': float(freq_hz), 'material_val': mat_val,
                                                               'source_val': src_val}}}}
    return geometry, problem


def tolerance(case):
    """tolerance.yaml with the case's changes."""
    import scisave
    tol = scisave.load_config(str(TOLERANCE))

    def deep(d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                deep(d.setdefault(k, {}), v)
            else:
                d[k] = v
    deep(tol, case.tolerance)
    return tol


def _peak_kb(pid):
    try:
        with open(f'/proc/{pid}/status') as f:
            for line in f:
                if line.startswith('VmHWM:'):
                    return int(line.split()[1])
    except OSError:
        pass
    return 0


DRIVER = ('import sys, pypeec\n'
          'f = sys.argv[1:]\n'
          'pypeec.run_mesher_file(file_geometry=f[0], file_voxel=f[1])\n'
          'pypeec.run_solver_file(file_voxel=f[1], file_problem=f[2], file_tolerance=f[3], file_solution=f[4])\n')


def run(case, freq_hz, folder, name, threads=4, log=print, timeout=None, keep=False):
    """Write the input, run PyPEEC's mesher and solver in a process of their own, and read the solution. Returns
    (solution dict, seconds, peak memory in GB, the voxel summary). The large voxel and solution files are removed
    after reading unless keep."""
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    geometry, problem = inputs(case, freq_hz)
    files = [folder / f'{name}_{k}' for k in ('geometry.json', 'voxel.mpk', 'problem.json', 'tolerance.json',
                                              'solution.mpk')]
    files[0].write_text(json.dumps(geometry))
    files[2].write_text(json.dumps(problem, indent=1))
    files[3].write_text(json.dumps(tolerance(case), indent=1))
    env = dict(os.environ)
    for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[k] = str(threads)
    logf = folder / f'{name}.log'
    t0 = time.time()
    peak = 0
    with open(logf, 'w') as fh:
        p = subprocess.Popen([sys.executable, '-c', DRIVER, *map(str, files)], cwd=folder, stdout=fh,
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
    if p.returncode or not files[4].exists():
        err = [l for l in logf.read_text(errors='replace').splitlines() if 'Error' in l or 'error' in l]
        raise RuntimeError(f'PyPEEC failed ({p.returncode}) on {name}: ' + '; '.join(err[-3:]))
    import scisave
    sol = scisave.load_data(str(files[4]))
    sol = sol.get('data', sol)                            # the file holds 'meta' and 'data'
    if not keep:
        for f in (files[0], files[1], files[4]):
            f.unlink(missing_ok=True)
    log(f'PyPEEC {name}: {dt:.0f} s, peak memory {peak / 1048576:.2f} GB')
    return sol, dt, peak / 1048576


def coil_results(sol, coils, freq_hz):
    """V, I and Z of each coil from the solution: V across its terminals, I driven into its first. Next to one
    driven coil, an undriven coil's open-circuit voltage over the driving current is the mutual impedance, and its
    imaginary part over omega the mutual inductance (positive when both coils run the same way from t1 to t2)."""
    omega = 2 * math.pi * freq_hz
    sv = sol['data_sweep']['ac']['source_values']
    out = {}
    for c in coils:
        v = complex(sv[f'{c.name}_T1']['V']) - complex(sv[f'{c.name}_T2']['V'])
        i = complex(sv[f'{c.name}_T1']['I'])
        z = v / i if abs(i) > 1e-12 else None
        out[c.name] = dict(V=v, I=i, Z=z, R=z.real if z else None, L=z.imag / omega if z else None)
    driven = [c for c in coils if abs(complex(c.current)) > 0]
    if len(driven) == 1:
        i_d = out[driven[0].name]['I']
        for c in coils:
            r = out[c.name]
            if c is not driven[0] and i_d:
                zm = r['V'] / i_d
                r.update(Zm=zm, M=zm.imag / omega, Rm=zm.real, driven_by=driven[0].name)
    return out
