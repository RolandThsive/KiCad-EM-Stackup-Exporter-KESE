"""Palace's input for a meshed board, running it, and each coil's Z, R, L and M read back.

Palace (AWS Labs, Apache-2.0) solves Maxwell's equations in the frequency domain with Nedelec finite elements: the
copper is a conducting domain, the air round it is meshed out to a boundary, and each coil is opened by a lumped
port, a sheet across the gap that opens it with a resistance across it. One port carries the drive (its incident
voltage behind its own resistance); a receiver's port has a resistance of 1 MOhm, so it is open to within a few
parts in a million, and its voltage is the EMF the driven coil induces in it.

Palace writes each port's voltage V (the field's line integral across the sheet, along the port's direction) and
the current in the port's own resistance, V / R. The current into the coil is what the source gives less that: at
the driven port, (2 V_inc - V) / R, with the source taken as 2 V_inc behind R; at an undriven one, -V / R. With one
column of V and I per driven port, Z = V I^-1 is the open-circuit impedance matrix between the ports, and with only
the TX driven, Z[k][TX] = V_k / I_TX to within the receivers' 1 MOhm. M = Im(Z[rx][TX]) / omega.

Palace also writes the field's magnetic energy, W = 1/2 Re(integral of H* . B) over the domain (J), with the fields
as complex amplitudes. With the TX alone carrying current, W = L |I|^2 / 2, so its L is also 2 W / |I|^2: the check
that the port's voltage and the field inside agree (energy_check). On E01 at 3.5 MHz the two agree to five digits.
"""
from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OPEN_OHM = 1e6                       # a receiver's port: open to within |Z| / 1 MOhm


def palace_exe():
    """$PALACE, else the branch's Solver_Palace/install/bin/palace, else palace on the PATH."""
    env = os.environ.get('PALACE')
    if env and Path(env).is_file():
        return Path(env)
    own = HERE.parent / 'Solver_Palace' / 'install' / 'bin' / 'palace'
    if own.is_file():
        return own
    found = shutil.which('palace')
    if found:
        return Path(found)
    raise FileNotFoundError('Palace not found: see Solver_Palace/README.md, or set PALACE to its launcher')


@dataclass
class Port:
    name: str
    attr: int                         # the port sheet's boundary tag in the mesh
    direction: object                 # along the sheet, from one electrode to the other: '+Z' or [x, y, z]
    R: float = OPEN_OHM               # ohm across the sheet
    excite: int = 0                   # 0: not driven; otherwise its excitation index (each one a solve)


@dataclass
class Case:
    mesh: Path                        # Gmsh 2.2 file, in mm
    conductors: list                  # the physical volumes that are copper
    air: list                         # the physical volumes that are air
    outer: list                       # the boundary tags of the domain's outside (PEC: tangential E = 0)
    ports: list                       # [Port]
    sigma: float = 5.8e7              # S/m
    order: int = 1
    solver: dict = field(default_factory=lambda: dict(Type='AMS', KSPType='GMRES', Tol=1e-8, MaxIts=2000,
                                                      MaxSize=200))


def config(case, freq_hz, out_dir):
    """Palace's JSON input for one frequency."""
    ports = []
    for k, p in enumerate(case.ports, start=1):
        d = p.direction if isinstance(p.direction, str) else [float(x) for x in np.asarray(p.direction) /
                                                              np.linalg.norm(p.direction)]
        entry = dict(Index=k, R=float(p.R), Elements=[dict(Attributes=[int(p.attr)], Direction=d)])
        if p.excite:
            entry['Excitation'] = int(p.excite)
        ports.append(entry)
    return {
        'Problem': {'Type': 'Driven', 'Verbose': 2, 'Output': str(out_dir)},
        'Model': {'Mesh': str(case.mesh), 'L0': 1e-3},
        'Domains': {'Materials': [
            {'Attributes': [int(a) for a in case.air], 'Permeability': 1.0, 'Permittivity': 1.0},
            {'Attributes': [int(a) for a in case.conductors], 'Permeability': 1.0, 'Permittivity': 1.0,
             'Conductivity': float(case.sigma)}]},
        'Boundaries': {'PEC': {'Attributes': [int(a) for a in case.outer]}, 'LumpedPort': ports},
        'Solver': {'Order': case.order, 'Device': 'CPU',
                   'Driven': {'Samples': [{'Type': 'Point', 'Freq': [freq_hz * 1e-9]}], 'Save': []},
                   'Linear': dict(case.solver)},
    }


def _peak_gb(text):
    """The peak memory of all the ranks together, GB, from Palace's log ('Estimated peak per-node memory usage
    is: ... Total 738.2M')."""
    m = re.findall(r'Estimated peak per-node memory usage is:.*Total ([\d.]+)([KMGT])', text)
    if not m:
        return None
    v, u = m[-1]
    return round(float(v) * {'K': 1e-6, 'M': 1e-3, 'G': 1.0, 'T': 1e3}[u], 3)


def _iterations(text):
    """Each linear solve's iterations, its residual at the end relative to its start (the last 'KSP residual norm'
    over the first) and whether it converged, from Palace's log; empty for a direct solve, which logs none."""
    its, res, ok = [], [], []
    first = None
    for line in text.splitlines():
        m = re.match(r'\s*(\d+) \(restart \d+\) KSP residual norm ([0-9.eE+-]+)', line)
        if m:
            if m.group(1) == '0' and first is None:
                first = float(m.group(2))
            last = float(m.group(2))
            continue
        m = re.search(r'(did NOT converge|converged) in (\d+) iteration', line)
        if m and first is not None:
            its.append(int(m.group(2)))
            res.append(last / first if first else None)
            ok.append(m.group(1) == 'converged')
            first = None
    return its, res, ok


def run(case, freq_hz, folder, np_=4, log=print):
    """Write config.json in folder, run Palace on np_ MPI ranks, and return what it gave: the port matrices and
    the energy, with time, memory and the linear solves' iterations."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    out = folder / 'out'
    cfg = config(case, freq_hz, out)
    (folder / 'config.json').write_text(json.dumps(cfg, indent=1))
    env = dict(os.environ, OMPI_ALLOW_RUN_AS_ROOT='1', OMPI_ALLOW_RUN_AS_ROOT_CONFIRM='1',
               OMPI_MCA_rmaps_base_oversubscribe='1')
    t0 = time.time()
    with open(folder / 'palace.log', 'w') as f:      # written as Palace runs, so a long solve can be watched
        r = subprocess.run([str(palace_exe()), '-np', str(np_), 'config.json'], cwd=folder, stdout=f,
                           stderr=subprocess.STDOUT, text=True, env=env)
    secs = time.time() - t0
    text = (folder / 'palace.log').read_text()
    if r.returncode or not (out / 'port-V.csv').exists():
        raise RuntimeError(f'Palace failed in {folder} (exit {r.returncode}):\n{text[-3000:]}')
    its, res, ok = _iterations(text)
    got = read(case, out, freq_hz)
    got.update(seconds=round(secs, 1), peak_memory_gb=_peak_gb(text), iterations=its, residuals=res,
               converged=all(ok), ranks=np_)
    return got


def _table(path):
    """A Palace CSV as {column name: values}."""
    lines = [ln for ln in Path(path).read_text().splitlines() if ln.strip()]
    heads = [h.strip() for h in lines[0].split(',')]
    rows = [[float(x) for x in ln.split(',')] for ln in lines[1:]]
    return {h: [row[i] for row in rows] for i, h in enumerate(heads)}


def read(case, out, freq_hz):
    """Z (the open-circuit impedance matrix between the ports, from every driven column there is), each port's V
    and I per excitation, and the magnetic energy per excitation."""
    v = _table(out / 'port-V.csv')
    n = len(case.ports)
    exc = sorted({p.excite for p in case.ports if p.excite})
    lab = (lambda e: '') if len(exc) == 1 else (lambda e: f'[{e}]')
    V = np.zeros((n, len(exc)), complex)
    I = np.zeros((n, len(exc)), complex)
    for j, e in enumerate(exc):
        for k, p in enumerate(case.ports, start=1):
            V[k - 1, j] = v[f'Re{{V[{k}]{lab(e)}}} (V)'][-1] + 1j * v[f'Im{{V[{k}]{lab(e)}}} (V)'][-1]
            if p.excite == e:
                vinc = v[f'V_inc[{k}]{lab(e)} (V)'][-1]
                I[k - 1, j] = (2 * vinc - V[k - 1, j]) / p.R
            else:
                I[k - 1, j] = -V[k - 1, j] / p.R
    driven = [next(k for k, p in enumerate(case.ports) if p.excite == e) for e in exc]
    if len(exc) == n:                                  # every port driven once: the whole matrix
        Z = V @ np.linalg.inv(I)
    else:                                              # the driven columns, the others open to 1 MOhm
        Z = np.full((n, n), np.nan + 0j)
        for j, k in enumerate(driven):
            Z[:, k] = V[:, j] / I[k, j]
    energy = {}
    ef = out / 'domain-E.csv'
    if ef.exists():
        d = _table(ef)
        for e in exc:
            key = f'E_mag{lab(e)} (J)'
            if key in d:
                energy[e] = d[key][-1]
    return dict(frequency_hz=freq_hz, Z=Z, V=V, I=I, driven=driven, energy_j=energy)


def coil_rows(case, got, driven_name):
    """The driven coil's Z, R and L, and for each other coil its mutual impedance from the driven one, its M, the
    reverse M (from the receiver's own drive, where it was driven) and its own L (where it was driven). Complex
    values as [re, im], as JSON keeps them."""
    w = 2 * math.pi * got['frequency_hz']
    names = [p.name for p in case.ports]
    k = names.index(driven_name)
    Z = got['Z']
    out = {}
    for i, name in enumerate(names):
        if i == k:
            z = Z[k, k]
            out[name] = dict(Z=[z.real, z.imag], R=z.real, L=z.imag / w)
            continue
        zm, zr = Z[i, k], Z[k, i]
        row = dict(Z_mutual=[zm.real, zm.imag], M=zm.imag / w)
        if not np.isnan(zr):
            row.update(M_reverse=zr.imag / w)
        if not np.isnan(Z[i, i]):
            row.update(L_self=Z[i, i].imag / w, R_self=Z[i, i].real)
        out[name] = row
    return out


def energy_check(case, got, driven_name):
    """The driven coil's L from the field's magnetic energy, 2 W / |I|^2, while it alone carries current (its
    excitation); None where Palace wrote no energy."""
    names = [p.name for p in case.ports]
    k = names.index(driven_name)
    e = case.ports[k].excite
    if not e or e not in got['energy_j']:
        return None
    j = sorted({p.excite for p in case.ports if p.excite}).index(e)
    return 2 * got['energy_j'][e] / abs(got['I'][k, j]) ** 2


def version():
    """Palace's version, as the program prints it ('v0.19.0-dirty': the release with this branch's patch)."""
    try:
        r = subprocess.run([str(palace_exe()), '--version'], capture_output=True, text=True, timeout=60,
                           env=dict(os.environ, OMPI_ALLOW_RUN_AS_ROOT='1', OMPI_ALLOW_RUN_AS_ROOT_CONFIRM='1'))
        m = re.search(r'Palace version: v?(\S+)', r.stdout + r.stderr)
        return m.group(1) if m else (r.stdout + r.stderr).strip()[:80]
    except Exception as e:              # noqa: BLE001
        return f'unknown ({e})'
