"""E02: two coaxial circular traces, TX on F.Cu and RX on B.Cu of a 1.6 mm board, each E01's loop: their mutual
inductance from Elmer, against Maxwell's formula for coaxial circles averaged over both traces' widths.

    python simulation.py                 the mesh ladder at every frequency
    python simulation.py --levels 1      one mesh only
    python simulation.py --order 2       second-order edge elements

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
from bridge import elmer_case as E, geometry as G, mesh25d as M, ports as P, study as S   # noqa: E402

SETTINGS = dict(
    board='E02_coaxial_loops.kicad_pcb',
    centre=(100.0, -100.0),        # the loops' centre in model coordinates (KiCad (100, 100), y up)
    radius_mm=10.0,                # each trace's centre line
    width_mm=0.5,
    gap_mm=0.2,
    gap_box=(109.75, -100.35, 110.25, -99.65),   # holds both loops' 0.2 mm gaps, one above the other
    sigma=5.8e7,                   # copper, S/m
    insulators=False,              # FR-4 and mask are air to the magneto-quasi-static solve (mu_r 1, no eps)
    domain_radius_mm=60.0,
    domain_half_height_mm=60.0,
    freqs_hz=[1e4, 3.5e6],
    order=1,
    levels=[0.75, 1.0],            # level 1.5 does not fit in 15 GB (level 1 took 6.7 GB)
    mesh=dict(h_edge=0.09, h_in=0.18, h_max=6.0, grade=0.5, dz_copper=0.018, dz_max=0.4,
              tet_max=8.0, tet_grade=0.7),
    threads=4,
    tol=1e-7,
    max_iter=1500,
)


def zrange(lay, body):
    zs = [z for p in lay.parts if p.body == body for z in p.zrange]
    return min(zs), max(zs)


def build(export, level, st, log=print):
    mats = json.loads((export / 'materials.json').read_text())
    parts, _ = G.load_parts(export, z_shift=-G.copper_top(mats))
    c = SETTINGS['centre']
    lay = M.Layout(parts, M.disc(c, SETTINGS['domain_radius_mm'], h=st['h_max']),
                   (-SETTINGS['domain_half_height_mm'], SETTINGS['domain_half_height_mm'])
                   ).build(log=log, insulators=SETTINGS['insulators'])
    s = dict(st)
    for k in ('h_edge', 'h_in', 'dz_copper'):
        s[k] = st[k] / level
    m = M.build_mesh(lay, M.Settings(**s), log=log)
    t, tp, q, qp = M.outer_faces(m)
    bnds = [('OUTER', t, tp, q, qp)]
    for name in ('TX', 'RX'):
        k = m['names'].index(name)
        cu = shapely.unary_union([g for p in lay.parts if p.body == name for g in p.polys.values()])
        gap = box(*SETTINGS['gap_box']).difference(cu)
        z0, z1 = zrange(lay, name)
        e1, e2 = P.electrodes(m, k, gap, z0, z1)
        # the sheet on the copper's face toward the board's middle (any level of the copper's span would do)
        ts, tsp = P.sheet_at_level(m, gap, z0 if name == 'TX' else z1)
        bnds += [(f'{name}_T1', *e1), (f'{name}_T2', *e2), (f'{name}_SHEET', ts, tsp, q[:0], qp[:0])]
    return m, lay, bnds


def maxwell_mutual(r1, r2, d):
    """Maxwell's mutual inductance of two coaxial circular filaments of radii r1, r2 (m), d (m) apart."""
    from scipy.special import ellipe, ellipk
    k2 = 4 * r1 * r2 / ((r1 + r2) ** 2 + d * d)
    k = math.sqrt(k2)
    return E.MU0 * math.sqrt(r1 * r2) * ((2 / k - k) * ellipk(k2) - 2 / k * ellipe(k2))


def references(dz_mm):
    """M of the two closed loops, filaments and averaged over both widths (uniform current, 41 x 41 filaments),
    then scaled by the share of the circle the TX's current runs round (theta / 2 pi): by symmetry each piece of
    the TX's arc links the RX's closed path (its copper plus the sheet across its gap) equally."""
    r, w = SETTINGS['radius_mm'] * 1e-3, SETTINGS['width_mm'] * 1e-3
    d = dz_mm * 1e-3
    m_fil = maxwell_mutual(r, r, d)
    xs = r + np.linspace(-w / 2, w / 2, 41)
    m_avg = float(np.mean([[maxwell_mutual(a, b, d) for b in xs] for a in xs]))
    half_gap = math.asin((SETTINGS['gap_mm'] + SETTINGS['width_mm']) / 2 / SETTINGS['radius_mm'])
    share = (2 * math.pi - 2 * half_gap) / (2 * math.pi)
    return dict(dz_mm=dz_mm, M_filament_h=m_fil, M_closed_h=m_avg, arc_share=share, M_open_h=m_avg * share)


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
    result = dict(board=SETTINGS['board'], settings=SETTINGS, versions=S.versions(), runs=[])
    res_file = Path(a.results) if a.results else HERE / ('results.json' if a.order == 1 else
                                                       f'results_order{a.order}.json')
    if res_file.exists():                  # keep the runs already there (S.merge_run replaces a rerun)
        result['runs'] = json.loads(res_file.read_text()).get('runs', [])
    for level in a.levels:
        t0 = time.time()
        m, lay, bnds = build(export, level, SETTINGS['mesh'], log)
        if 'references' not in result:
            (tx0, tx1), (rx0, rx1) = zrange(lay, 'TX'), zrange(lay, 'RX')
            result['references'] = references(0.5 * (tx0 + tx1) - 0.5 * (rx0 + rx1))
            log(f"reference: M {result['references']['M_open_h'] * 1e9:.3f} nH")
        folder = out / f'order{a.order}_level{level:g}'
        M.write_elmer(m, folder / 'mesh_files', bnds, log=log)
        mesh_s = time.time() - t0
        cu = E.Material('Copper', sigma=SETTINGS['sigma'])
        bodies = {n: (cu if n in ('TX', 'RX') else E.Material('Air' if n == 'AIR' else n.title()))
                  for n in m['names']}
        case = E.Case(mesh_dir=folder / 'mesh_files', bodies=bodies, order=a.order, tol=SETTINGS['tol'],
                      max_iter=a.max_iter,
                      coils=[E.Coil('TX', 'TX', 'TX_T1', 'TX_T2', 'TX_SHEET', 1.0),
                             E.Coil('RX', 'RX', 'RX_T1', 'RX_T2', 'RX_SHEET', 0.0)])
        rows = S.solve(case, a.freqs, folder, threads=SETTINGS['threads'], log=log)
        S.merge_run(result, dict(level=level, order=a.order, max_iter=a.max_iter, mesh_seconds=round(mesh_s, 1),
                                   nodes=len(m['nodes']), wedges=len(m['wedges']), tetrahedra=len(m['tets']),
                                   solves=rows))
        res_file.write_text(json.dumps(result, indent=1))
        for r in rows:
            tx, rx = r['coils']['TX'], r['coils']['RX']
            log(f"level {level:g} f {r['frequency_hz']:.4g} Hz: M {rx['M'] * 1e9:.3f} nH, L_TX {tx['L'] * 1e9:.3f} nH, "
                f"R_TX {tx['R'] * 1e3:.3f} mOhm, {r['iterations']} it, res {r['residual']}")
    log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
