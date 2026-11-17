"""E02: two coaxial circular traces, TX on F.Cu and RX on B.Cu of a 1.6 mm board, each E01's loop: their mutual
inductance from PyPEEC, against Maxwell's formula for coaxial circles averaged over both traces' widths.

    python simulation.py                      the voxel ladder at both frequencies
    python simulation.py --voxels 0.05        one voxel size only
    python simulation.py --voxels-only        draw the voxels and print how many, solve nothing

TX carries 1 A; RX carries none, so its voltage is the EMF the TX induces in it and M = Im(V_RX / I_TX) / omega.
Writes results.json beside this file and the runs under case/ (not committed). Every setting is in SETTINGS.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import shapely
from shapely.geometry import box

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from bridge import geometry as G, layers as L, ports as P, pypeec_case as C, study as S, voxels as V   # noqa: E402

MU0 = 1.25663706212e-6
SETTINGS = dict(
    board='E02_coaxial_loops.kicad_pcb',
    centre=(100.0, -100.0),        # the loops' centre in model coordinates (KiCad (100, 100), y up)
    radius_mm=10.0,                # each trace's centre line
    width_mm=0.5,
    gap_mm=0.2,
    copper_mm=0.035,
    gap_box=(109.75, -100.35, 110.25, -99.65),   # holds both loops' 0.2 mm gaps, one above the other
    sigma=5.8e7,                   # copper, S/m
    freqs_hz=[1e4, 3.5e6],
    voxels_mm=[0.1, 0.05],         # the voxel ladder: the voxels' size in the board's plane (0.025: 30 M voxels, 9 GB)
    n_cu=1,                        # voxel layers through each copper sheet
    threads=4,
)


def build(export, d, n_cu, log=print):
    mats = json.loads((export / 'materials.json').read_text())
    parts, _ = G.load_parts(export, z_shift=-G.copper_top(mats))
    lay = L.Layout(parts).build(log=log, insulators=False)
    grid, vox = V.build(lay, d, copper_mm=SETTINGS['copper_mm'], n_cu=n_cu, log=log)
    coils = []
    for name in ('TX', 'RX'):
        cu = shapely.unary_union([g for p in lay.parts if p.body == name for g in p.polys.values()])
        gap = box(*SETTINGS['gap_box']).difference(cu)
        z0, z1 = zrange(lay, name)
        t1, t2 = P.terminals(grid, vox, name, gap, z0, z1)
        log(f'{name}: terminals of {len(t1)} and {len(t2)} voxels')
        coils.append(C.Coil(name, name, t1, t2, 1.0 if name == 'TX' else 0.0))
    return C.Case(grid=grid, vox=vox, coils=coils, sigma={b: SETTINGS['sigma'] for b in vox}), lay


def zrange(lay, body):
    zs = [z for p in lay.parts if p.body == body for z in p.zrange]
    return min(zs), max(zs)


def maxwell_mutual(r1, r2, d):
    """Maxwell's mutual inductance of two coaxial circular filaments of radii r1, r2 (m), d (m) apart."""
    from scipy.special import ellipe, ellipk
    k2 = 4 * r1 * r2 / ((r1 + r2) ** 2 + d * d)
    k = math.sqrt(k2)
    return MU0 * math.sqrt(r1 * r2) * ((2 / k - k) * ellipk(k2) - 2 / k * ellipe(k2))


def references(dz_mm):
    """M of the two closed loops, filaments and averaged over both widths (uniform current, 41 x 41 filaments),
    then scaled by the share of the circle the TX's current runs round (theta / 2 pi): by symmetry each piece of
    the TX's arc links the RX's closed path (its copper plus its gap) equally."""
    r, w = SETTINGS['radius_mm'] * 1e-3, SETTINGS['width_mm'] * 1e-3
    d = dz_mm * 1e-3
    m_fil = maxwell_mutual(r, r, d)
    xs = r + np.linspace(-w / 2, w / 2, 41)
    m_avg = float(np.mean([[maxwell_mutual(a, b, d) for b in xs] for a in xs]))
    half_gap = math.asin((SETTINGS['gap_mm'] + SETTINGS['width_mm']) / 2 / SETTINGS['radius_mm'])
    share = (2 * math.pi - 2 * half_gap) / (2 * math.pi)
    return dict(dz_mm=dz_mm, M_filament_h=m_fil, M_closed_h=m_avg, arc_share=share, M_open_h=m_avg * share)


def merge_run(result, run):
    """Add a run (a dict with voxel_mm, n_cu and solves) to result['runs']. A run of the same voxels already there
    keeps its solves at other frequencies; a solve at the same frequency is replaced."""
    for old in result['runs']:
        if (old['voxel_mm'], old['n_cu']) == (run['voxel_mm'], run['n_cu']):
            freqs = {s['frequency_hz'] for s in run['solves']}
            solves = [s for s in old['solves'] if s['frequency_hz'] not in freqs] + run['solves']
            old.update({k: v for k, v in run.items() if k != 'solves'})
            old['solves'] = sorted(solves, key=lambda s: s['frequency_hz'])
            return result
    result['runs'].append(run)
    result['runs'].sort(key=lambda r: (r['n_cu'], -r['voxel_mm']))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--voxels', type=float, nargs='+', default=SETTINGS['voxels_mm'])
    ap.add_argument('--freqs', type=float, nargs='+', default=SETTINGS['freqs_hz'])
    ap.add_argument('--n-cu', type=int, default=SETTINGS['n_cu'])
    ap.add_argument('--out', default=str(HERE / 'case'))
    ap.add_argument('--results', default=None, help='the results file (default results.json beside this file)')
    ap.add_argument('--voxels-only', action='store_true', help='draw the voxels, solve nothing')
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / 'run.log', 'a')

    def log(msg):
        print(msg, flush=True)
        logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
        logf.flush()
    export = S.kese_export(HERE / SETTINGS['board'], out / 'kese', log=log)
    result = dict(board=SETTINGS['board'], settings=SETTINGS, versions=S.versions(), runs=[])
    res_file = Path(a.results) if a.results else HERE / 'results.json'
    if res_file.exists():                  # keep the runs already there (merge_run replaces a rerun)
        result['runs'] = json.loads(res_file.read_text()).get('runs', [])
    for d in a.voxels:
        t0 = time.time()
        case, lay = build(export, d, a.n_cu, log)
        if 'references' not in result:
            (tx0, tx1), (rx0, rx1) = zrange(lay, 'TX'), zrange(lay, 'RX')
            result['references'] = references(0.5 * (tx0 + tx1) - 0.5 * (rx0 + rx1))
            log(f"reference: M {result['references']['M_open_h'] * 1e9:.3f} nH")
        vox_s = time.time() - t0
        if a.voxels_only:
            continue
        rows = S.solve(case, a.freqs, out / f'voxel{d * 1e3:g}um_cu{a.n_cu}', threads=SETTINGS['threads'], log=log)
        merge_run(result, dict(voxel_mm=d, n_cu=a.n_cu, voxel_seconds=round(vox_s, 1), grid=case.grid.summary(),
                               solves=rows))
        res_file.write_text(json.dumps(result, indent=1))
        for r in rows:
            tx, rx = r['coils']['TX'], r['coils']['RX']
            log(f"voxel {d * 1e3:g} um f {r['frequency_hz']:.4g} Hz: M {rx['M'] * 1e9:.3f} nH, L_TX {tx['L'] * 1e9:.3f} "
                f"nH (energy {r['L_from_energy_h'] * 1e9:.3f}), R_TX {tx['R'] * 1e3:.3f} mOhm, {r['iterations']} it, "
                f"res {r['residual']:.1e}, {r['seconds']} s, {r['peak_memory_gb']} GB")
    if not a.voxels_only:
        log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
