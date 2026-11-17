"""E01: one circular trace, 20 mm across, opened by a 0.2 mm gap: its inductance and resistance from PyPEEC, against
Grover's ring formula and the resistance of an annular sector.

    python simulation.py                      the voxel ladder at both frequencies (a few minutes on 4 cores)
    python simulation.py --voxels 0.05        one voxel size only
    python simulation.py --voxels 0.025 --n-cu 2 --results results_cu2.json
                                              two voxel layers through the copper (17.5 um each) instead of one,
                                              to its own results file
    python simulation.py --voxels-only        draw the voxels and print how many, solve nothing

Writes results.json beside this file and the runs under case/ (not committed). Every setting is in SETTINGS.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import shapely
from shapely.geometry import box

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
sys.path.insert(0, str(HERE.parent))                  # Examples/references.py
from bridge import geometry as G, layers as L, ports as P, pypeec_case as C, study as S, voxels as V   # noqa: E402
from references import ring_inductance   # noqa: E402

SETTINGS = dict(
    board='E01_circular_loop.kicad_pcb',
    centre=(100.0, -100.0),        # the loop's centre in model coordinates (KiCad (100, 100), y up)
    radius_mm=10.0,                # the trace's centre line
    width_mm=0.5,
    gap_mm=0.2,
    copper_mm=0.035,
    gap_box=(109.75, -100.35, 110.25, -99.65),   # holds the 0.2 mm gap between the two round ends
    sigma=5.8e7,                   # copper, S/m
    freqs_hz=[1e4, 3.5e6],         # uniform current (10 kHz, skin depth 0.66 mm) and the coils' frequency
    voxels_mm=[0.1, 0.05, 0.025, 0.0125],   # the voxel ladder: the voxels' size in the board's plane
    n_cu=1,                        # voxel layers through the copper (dz = 35 um / n_cu)
    threads=4,
)


def build(export, d, n_cu, log=print):
    mats = json.loads((export / 'materials.json').read_text())
    parts, _ = G.load_parts(export, z_shift=-G.copper_top(mats))
    lay = L.Layout(parts).build(log=log, insulators=False)
    grid, vox = V.build(lay, d, copper_mm=SETTINGS['copper_mm'], n_cu=n_cu, log=log)
    cu = shapely.unary_union([g for p in lay.parts if p.body == 'LOOP' for g in p.polys.values()])
    gap = box(*SETTINGS['gap_box']).difference(cu)
    t1, t2 = P.terminals(grid, vox, 'LOOP', gap, -SETTINGS['copper_mm'], 0.0)
    log(f'terminals of {len(t1)} and {len(t2)} voxels')
    return C.Case(grid=grid, vox=vox, coils=[C.Coil('LOOP', 'LOOP', t1, t2, 1.0)], sigma={'LOOP': SETTINGS['sigma']})


def references():
    """Grover's ring formula for the closed ring, at DC (the rectangle's GMD) and with the current crowded to the
    strip's edges (w / 4), then scaled by the share of the circle the current runs round: the loop is open, and by
    symmetry each piece of its arc links the closed path (copper plus the gap) alike, so to first order
    L_open = L_ring theta / 2 pi. R_dc is the annular sector's resistance between its two ends."""
    r, w, t = SETTINGS['radius_mm'], SETTINGS['width_mm'], SETTINGS['copper_mm']
    g_dc = 0.2235 * (w + t)                            # GMD of a w x t rectangle (Grover)
    g_hf = w / 4                                        # GMD of a thin strip with its edge-crowded current
    half_gap = math.asin((SETTINGS['gap_mm'] + w) / 2 / r)   # the round ends' centres sit (gap + w) apart
    theta = 2 * math.pi - 2 * half_gap
    share = theta / (2 * math.pi)
    r_dc = theta / (SETTINGS['sigma'] * t * 1e-3 * math.log((r + w / 2) / (r - w / 2)))
    l_dc, l_hf = ring_inductance(r, g_dc), ring_inductance(r, g_hf)
    return dict(L_ring_dc_h=l_dc, L_ring_hf_h=l_hf, arc_share=share, L_open_dc_h=l_dc * share,
                L_open_hf_h=l_hf * share, R_dc_ohm=r_dc, gmd_dc_mm=g_dc, gmd_hf_mm=g_hf)


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
    ref = references()
    result = dict(board=SETTINGS['board'], settings=SETTINGS, references=ref, versions=S.versions(), runs=[])
    res_file = Path(a.results) if a.results else HERE / 'results.json'
    if res_file.exists():                  # keep the runs already there (merge_run replaces a rerun)
        result['runs'] = json.loads(res_file.read_text()).get('runs', [])
    for d in a.voxels:
        t0 = time.time()
        case = build(export, d, a.n_cu, log)
        vox_s = time.time() - t0
        if a.voxels_only:
            continue
        rows = S.solve(case, a.freqs, out / f'voxel{d * 1e3:g}um_cu{a.n_cu}', threads=SETTINGS['threads'], log=log)
        merge_run(result, dict(voxel_mm=d, n_cu=a.n_cu, voxel_seconds=round(vox_s, 1), grid=case.grid.summary(),
                               copper_voxels=int(sum(len(v) for v in case.vox['LOOP'].values()))
                               + len(case.coils[0].t1) + len(case.coils[0].t2), solves=rows))
        res_file.write_text(json.dumps(result, indent=1))
        for r in rows:
            c = r['coils']['LOOP']
            log(f"voxel {d * 1e3:g} um f {r['frequency_hz']:.4g} Hz: L {c['L'] * 1e9:.3f} nH (energy "
                f"{r['L_from_energy_h'] * 1e9:.3f}), R {c['R'] * 1e3:.3f} mOhm (losses "
                f"{r['R_from_power_ohm'] * 1e3:.3f}), {r['iterations']} it, res {r['residual']:.1e}, "
                f"{r['seconds']} s, {r['peak_memory_gb']} GB")
    if not a.voxels_only:
        log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
