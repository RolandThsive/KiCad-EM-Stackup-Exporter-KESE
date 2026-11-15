"""Running a study: KESE's export (cached), one Elmer solve per frequency, and the numbers read back."""
from __future__ import annotations

import hashlib
import json
import math
import re
import time
from pathlib import Path

from . import elmer_case as E
from . import geometry as G


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def kese_export(board, cache_root, mask=True, log=print):
    """KESE's export of a board, reused while the board file is unchanged. Returns the folder with materials.json."""
    board = Path(board)
    out = Path(cache_root) / f'{board.stem}_{file_hash(board)}'
    found = sorted(out.glob(f'{board.stem}/simulation_*/materials.json'))
    if found:
        log(f'KESE export reused: {found[-1].parent}')
        return found[-1].parent
    return G.run_kese(board, out, mask=mask, log=log)


def iterations(logfile):
    """The last linear solve of the A-V system in an ElmerSolver log: (iterations, relative residual)."""
    text = Path(logfile).read_text(errors='replace')
    part = text.split('WhitneyAVHarmonicSolver: Solving', 1)[-1]
    rows = re.findall(r'^\s*(\d+)\s+([0-9.]+E[+-]\d+)\s*$', part, re.M)
    if not rows:
        return None, None
    return int(rows[-1][0]), float(rows[-1][1])


def solve(case, freqs, folder, threads=4, log=print, tag='f'):
    """One Elmer solve per frequency. Returns a list of dicts: frequency, seconds, the linear solver's iterations
    and residual, the field energy and each coil's V, I, Z (complex as [re, im]), R and L."""
    folder = Path(folder)
    rows = []
    for f in freqs:
        name = f'{tag}{f:.6g}'.replace('+', '')
        sif = E.write_sif(case, folder, f, name)
        t0 = time.time()
        E.run(sif, threads=threads, log=log)
        dt = time.time() - t0
        sc = E.read_scalars(folder, name)
        coils = E.coil_results(sc, case.coils, f)
        it, res = iterations(sif.with_suffix('.log'))
        energy = next((v for k, v in sc.items() if 'field energy' in k), None)
        row = dict(frequency_hz=f, seconds=round(dt, 1), iterations=it, residual=res, field_energy_j=energy,
                   dc_resistance_ohm={c.name: sc.get(f'res: r_component({n})') for n, c in enumerate(case.coils, 1)},
                   coils={})
        for c in case.coils:
            r = coils[c.name]
            row['coils'][c.name] = {k: ([v.real, v.imag] if isinstance(v, complex) else v) for k, v in r.items()}
        driven = [c for c in case.coils if abs(complex(c.current)) > 0]
        if energy is not None and len(driven) == 1:
            i = abs(complex(driven[0].current))
            row['L_from_energy_h'] = 2 * energy / i ** 2
        rows.append(row)
        log(json.dumps({k: row[k] for k in ('frequency_hz', 'seconds', 'iterations', 'residual')}))
    return rows


def versions():
    """The versions a result depends on."""
    import platform
    out = {'python': platform.python_version(), 'kese': G.kese_version()}
    try:
        import gmsh
        out['gmsh'] = gmsh.__version__
    except Exception:                    # noqa: BLE001
        pass
    for mod in ('numpy', 'scipy', 'shapely', 'trimesh'):
        try:
            out[mod] = __import__(mod).__version__
        except Exception:                # noqa: BLE001
            pass
    try:
        import subprocess
        r = subprocess.run([str(E.ELMER_BIN / 'ElmerSolver'), '-v'], capture_output=True, text=True, timeout=60)
        m = re.search(r'Version:\s*(\S+).*?Rev:\s*(\S+)', r.stdout + r.stderr, re.S)
        out['elmer'] = f'{m.group(1)} ({m.group(2)})' if m else 'unknown'
    except Exception:                    # noqa: BLE001
        out['elmer'] = 'unknown'
    return out


def mu0():
    return E.MU0


def ring_inductance(radius_mm, gmd_mm):
    """A circular loop's inductance from the geometric mean distance of its cross-section (Grover):
    mu0 R (ln(8R / g) - 2)."""
    return mu0() * radius_mm * 1e-3 * (math.log(8 * radius_mm / gmd_mm) - 2)
