"""E01: one circular trace, 20 mm across, opened by a 0.2 mm gap: its inductance and resistance from Elmer, against
Grover's ring formula and the resistance of an annular sector.

    python simulation.py                 the mesh ladder at every frequency (about 40 minutes on 4 cores)
    python simulation.py --levels 1      one mesh only
    python simulation.py --order 2       second-order edge elements

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
from bridge import elmer_case as E, geometry as G, mesh25d as M, ports as P, study as S   # noqa: E402

SETTINGS = dict(
    board='E01_circular_loop.kicad_pcb',
    centre=(100.0, -100.0),        # the loop's centre in model coordinates (KiCad (100, 100), y up)
    radius_mm=10.0,                # the trace's centre line
    width_mm=0.5,
    gap_mm=0.2,
    copper_mm=0.035,
    gap_box=(109.75, -100.35, 110.25, -99.65),   # holds the 0.2 mm gap between the two round ends
    sigma=5.8e7,                   # copper, S/m
    domain_radius_mm=60.0,         # 6 loop radii: the outside is n x A = 0
    domain_half_height_mm=60.0,
    freqs_hz=[1e4, 3.5e6],         # uniform current (10 kHz, skin depth 0.66 mm) and the coils' frequency
    order=1,
    levels=[1.0, 1.5, 2.0],        # the mesh ladder: each level divides the copper's mesh sizes by this
    mesh=dict(h_edge=0.09, h_in=0.18, h_max=6.0, grade=0.5, dz_copper=0.018, dz_max=0.4,
              tet_max=8.0, tet_grade=0.7),
    threads=4,
    tol=1e-7,
    max_iter=3000,
)


def build(export, level, st, log=print):
    mats = json.loads((export / 'materials.json').read_text())
    parts, _ = G.load_parts(export, z_shift=-G.copper_top(mats))
    c = SETTINGS['centre']
    R = SETTINGS['domain_radius_mm']
    h = st['h_max']
    lay = M.Layout(parts, M.disc(c, R, h=h), (-SETTINGS['domain_half_height_mm'],
                                              SETTINGS['domain_half_height_mm'])).build(log=log)
    s = dict(st)
    for k in ('h_edge', 'h_in', 'dz_copper'):
        s[k] = st[k] / level
    m = M.build_mesh(lay, M.Settings(**s), log=log)
    loop = m['names'].index('LOOP')
    cu = shapely.unary_union([g for p in lay.parts if p.body == 'LOOP' for g in p.polys.values()])
    gap = box(*SETTINGS['gap_box']).difference(cu)
    t_cu = SETTINGS['copper_mm']
    e1, e2 = P.electrodes(m, loop, gap, -t_cu, 0.0)
    ts, tsp = P.sheet_at_level(m, gap, -t_cu)
    t, tp, q, qp = M.outer_faces(m)
    return m, lay, [('OUTER', t, tp, q, qp), ('T1', *e1), ('T2', *e2), ('SHEET', ts, tsp, q[:0], qp[:0])]


def references():
    """Grover's ring formula for the closed ring, at DC (the rectangle's GMD) and with the current crowded to the
    strip's edges (w / 4), then scaled by the share of the circle the current runs round: the loop is open, and by
    symmetry each piece of its arc links the closed path (copper plus the sheet across the gap) alike, so to
    first order L_open = L_ring theta / 2 pi. R_dc is the annular sector's resistance between its two ends."""
    r, w, t = SETTINGS['radius_mm'], SETTINGS['width_mm'], SETTINGS['copper_mm']
    g_dc = 0.2235 * (w + t)                            # GMD of a w x t rectangle (Grover)
    g_hf = w / 4                                        # GMD of a thin strip with its edge-crowded current
    half_gap = math.asin((SETTINGS['gap_mm'] + w) / 2 / r)   # the round ends' centres sit (gap + w) apart
    theta = 2 * math.pi - 2 * half_gap
    share = theta / (2 * math.pi)
    r_dc = theta / (SETTINGS['sigma'] * t * 1e-3 * math.log((r + w / 2) / (r - w / 2)))
    l_dc, l_hf = S.ring_inductance(r, g_dc), S.ring_inductance(r, g_hf)
    return dict(L_ring_dc_h=l_dc, L_ring_hf_h=l_hf, arc_share=share, L_open_dc_h=l_dc * share,
                L_open_hf_h=l_hf * share, R_dc_ohm=r_dc, gmd_dc_mm=g_dc, gmd_hf_mm=g_hf)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--levels', type=float, nargs='+', default=SETTINGS['levels'])
    ap.add_argument('--freqs', type=float, nargs='+', default=SETTINGS['freqs_hz'])
    ap.add_argument('--order', type=int, default=SETTINGS['order'])
    ap.add_argument('--out', default=str(HERE / 'case'))
    ap.add_argument('--max-iter', type=int, default=SETTINGS['max_iter'],
                    help='the linear solver\'s iteration cap (the iteration check runs at half and full)')
    ap.add_argument('--results', default=None, help='the results file (default results.json beside this file)')
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / 'run.log', 'a')

    def log(msg):
        print(msg)
        logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
        logf.flush()
    export = S.kese_export(HERE / SETTINGS['board'], out / 'kese', log=log)
    ref = references()
    result = dict(board=SETTINGS['board'], settings=SETTINGS, references=ref, versions=S.versions(), runs=[])
    res_file = Path(a.results) if a.results else HERE / ('results.json' if a.order == 1 else
                                                       f'results_order{a.order}.json')
    if res_file.exists():                  # keep the runs already there (S.merge_run replaces a rerun)
        result['runs'] = json.loads(res_file.read_text()).get('runs', [])
    for level in a.levels:
        t0 = time.time()
        m, lay, bnds = build(export, level, SETTINGS['mesh'], log)
        folder = out / f'order{a.order}_level{level:g}'
        M.write_elmer(m, folder / 'mesh_files', bnds, log=log)
        mesh_s = time.time() - t0
        cu = E.Material('Copper', sigma=SETTINGS['sigma'])
        bodies = {n: (cu if n == 'LOOP' else E.Material('Air' if n == 'AIR' else n.title())) for n in m['names']}
        case = E.Case(mesh_dir=folder / 'mesh_files', bodies=bodies, order=a.order, tol=SETTINGS['tol'],
                      max_iter=a.max_iter,
                      coils=[E.Coil('LOOP', 'LOOP', 'T1', 'T2', 'SHEET', 1.0)])
        rows = S.solve(case, a.freqs, folder, threads=SETTINGS['threads'], log=log)
        S.merge_run(result, dict(level=level, order=a.order, max_iter=a.max_iter, mesh_seconds=round(mesh_s, 1),
                                   nodes=len(m['nodes']), wedges=len(m['wedges']), tetrahedra=len(m['tets']),
                                   solves=rows))
        res_file.write_text(json.dumps(result, indent=1))
        for r in rows:
            c = r['coils']['LOOP']
            log(f"level {level:g} f {r['frequency_hz']:.4g} Hz: L {c['L'] * 1e9:.3f} nH (energy "
                f"{r.get('L_from_energy_h', float('nan')) * 1e9:.3f}), R {c['R'] * 1e3:.3f} mOhm, R_dc "
                f"{r['dc_resistance_ohm']['LOOP'] * 1e3:.3f} mOhm, {r['iterations']} it, res {r['residual']}")
    log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
