"""Running a study: KESE's export (cached), one PyPEEC solve per frequency, and the numbers read back."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from . import geometry as G
from . import pypeec_case as C


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


def kese_geometry(board, folder, mask=True, log=print):
    """KESE's export of a board kept in folder/<board name>: materials.json, the STL solids, the STEP and KESE's
    report and parameters, meant to be committed beside the board. source.json there records the board file's hash,
    KESE's version and the settings; the board is exported again only when its file changes. Returns that folder."""
    import shutil
    import tempfile
    board = Path(board)
    dst = Path(folder) / board.stem
    rec = dst / 'source.json'
    h = file_hash(board)
    if rec.exists() and (dst / 'materials.json').exists() and json.loads(rec.read_text()).get('board_hash') == h:
        log(f'KESE geometry reused: {dst}')
        return dst
    with tempfile.TemporaryDirectory() as tmp:
        src = G.run_kese(board, Path(tmp), mask=mask, log=log)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    write_source(dst, board, mask)
    return dst


def write_source(dst, board, mask=True):
    """source.json in a kept KESE export: which board file (by its hash), KESE's version and the settings used."""
    Path(dst, 'source.json').write_text(json.dumps(dict(
        board=Path(board).name, board_hash=file_hash(board), hash='the first 16 hex digits of the file\'s SHA-256',
        kese=G.kese_version(), preset='elmer', formats=['step', 'stl'],
        settings=G.MASK_SETTINGS if mask else []), indent=1) + '\n')


def solve(case, freqs, folder, threads=4, log=print, tag='f'):
    """One PyPEEC solve per frequency. Returns a list of dicts: frequency, seconds, peak memory, the iterative
    solver's iterations and residual, the stored magnetic energy and the losses, each coil's V, I, Z (complex as
    [re, im]), R and L, and PyPEEC's own checks. With one coil driven, L from the energy (4 W / |I|^2) and R from the
    losses (2 P / |I|^2) are given beside the coil's own, as the Elmer branch gives them (PyPEEC's phasors are peak
    values: W is the time-averaged energy and P the average loss)."""
    folder = Path(folder)
    rows = []
    for f in freqs:
        name = f'{tag}{f:.6g}'.replace('+', '')
        sol, dt, peak_gb = C.run(case, f, folder, name, threads=threads, log=log)
        sw = sol['data_sweep']['ac']
        st, cond, tot = sw['solver_status'], sw['condition_status'], sw['integral_total']
        coils = C.coil_results(sol, case.coils, f)
        row = dict(frequency_hz=f, seconds=round(dt, 1), peak_memory_gb=round(peak_gb, 2),
                   iterations=int(st['n_iter']), residual=float(st['residuum_val']),
                   field_energy_j=float(tot['W_total']), loss_power_w=float(tot['P_total']),
                   pypeec=dict(status=bool(sol['status']), solver_ok=bool(sw['solver_ok']),
                               condition_ok=bool(sw['condition_ok']), solution_ok=bool(sw['solution_ok']),
                               residual_threshold=float(st['residuum_thr']), n_dof=int(st['n_dof_total']),
                               cond_electric=float(cond['cond_electric'])),
                   coils={})
        for c in case.coils:
            r = coils[c.name]
            row['coils'][c.name] = {k: ([v.real, v.imag] if isinstance(v, complex) else v) for k, v in r.items()}
        driven = [c for c in case.coils if abs(complex(c.current)) > 0]
        if len(driven) == 1:
            i = abs(complex(driven[0].current))
            row['L_from_energy_h'] = 4 * row['field_energy_j'] / i ** 2
            row['R_from_power_ohm'] = 2 * row['loss_power_w'] / i ** 2
        rows.append(row)
        log(json.dumps({k: row[k] for k in ('frequency_hz', 'seconds', 'peak_memory_gb', 'iterations', 'residual')}
                       | {'pypeec_status': row['pypeec']['status']}))
    return rows


def versions(exports=()):
    """The versions a result depends on. Where KESE is not installed (a board whose export is committed needs it
    not), KESE's version is the one that made the exports, from their source.json."""
    import platform
    out = {'python': platform.python_version(), 'kese': G.kese_version()}
    made = sorted({json.loads(Path(e, 'source.json').read_text()).get('kese', '') for e in exports
                   if Path(e, 'source.json').exists()} - {''})
    if made and out['kese'].startswith('unknown'):
        out['kese'] = ', '.join(made) + ' (made the export; not installed where this ran)'
    for mod in ('pypeec', 'scisave', 'numpy', 'scipy', 'shapely', 'trimesh'):
        try:
            out[mod] = __import__(mod).__version__
        except Exception:                # noqa: BLE001
            pass
    return out
