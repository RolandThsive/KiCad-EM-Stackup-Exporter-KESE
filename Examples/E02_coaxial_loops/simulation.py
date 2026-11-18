"""E02: two coaxial circular traces, TX on F.Cu and RX on B.Cu of a 1.6 mm board, each E01's loop: their mutual
inductance from Palace, against Maxwell's formula for coaxial rings averaged over both traces' widths, and the check
that M from the TX to the RX equals M from the RX to the TX.

    python simulation.py                      the mesh ladder at both frequencies
    python simulation.py --levels 0.5         one mesh only
    python simulation.py --mesh-only          build the meshes and print their size, solve nothing
    python simulation.py --levels 0.75 --freqs 1e5 3.5e6 --mesh grade=0.125 --mesh tet_grade=0.175 \
        --mesh dz_max=0.2 --results results_grade.json --out case_grade --restart 100
                                              the air graded as the coil boards' is: GMRES restarts every 100
                                              iterations, so its vectors fit in 15 GB, and the low frequency is
                                              100 kHz, since at 10 kHz it does not converge on this mesh
    python simulation.py --levels 0.75 --freqs 1e5 --results results_100k.json --out case_100k
                                              M at 100 kHz on the default mesh, to set beside 10 kHz

Each loop is opened by its 0.2 mm gap, the two gaps one above the other, and each gap holds a lumped port: a sheet
across it, through the copper, from one round end to the other. Both ports are driven in turn (two solves in one), so
Palace gives the whole impedance matrix between them: Z[RX][TX] / (j omega) is M from the TX to the RX, Z[TX][RX] /
(j omega) is M back, and Z[TX][TX] is the TX alone with the RX open. The board is meshed from KESE's export as E01's
is. Writes results.json beside this file and the runs under case/ (not committed). Every setting is in SETTINGS.
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
sys.path.insert(0, str(HERE.parent))                  # Examples/references.py
from bridge import geometry as G, mesh25d as M, palace_case as C, ports as P, study as S   # noqa: E402
from references import arc_mutual   # noqa: E402

SETTINGS = dict(
    board='E02_coaxial_loops.kicad_pcb',
    centre=(100.0, -100.0),        # the loops' centre in model coordinates (KiCad (100, 100), y up)
    radius_mm=10.0,                # each trace's centre line
    width_mm=0.5,
    gap_mm=0.2,
    gap_box=(109.75, -100.35, 110.25, -99.65),   # holds both loops' 0.2 mm gaps, one above the other
    port_direction='+Y',           # across each gap, from one round end to the other
    port_ohm=50.0,                 # each port's resistance: both are driven in turn, and Z = V I^-1 from the two
    sigma=5.8e7,                   # copper, S/m
    domain_radius_mm=60.0,         # 6 loop radii; the outside is a perfect conductor (tangential E = 0)
    domain_half_height_mm=60.0,
    freqs_hz=[1e4, 3.5e6],         # uniform current (10 kHz) and the coils' frequency
    order=1,
    levels=[0.25, 0.5, 0.75, 1.0],   # the mesh ladder: each level divides the copper's mesh sizes by this
    mesh=dict(h_edge=0.09, h_in=0.18, h_max=6.0, grade=0.5, dz_copper=0.018, dz_max=0.4,
              tet_max=8.0, tet_grade=0.7),
    ranks=4,
    # GMRES with hypre's AMS, as on the coil boards (a residual of 1e-8 of where it starts). Below 100 kHz the operator
    # AMS works on is all but singular in the air (the electric field's gradients there cost almost nothing): AMS is
    # told so (low_frequency), or GMRES diverges, and it then converges slowly, so it may stop at MaxIts
    solvers={'ams': dict(Type='AMS', KSPType='GMRES', Tol=1e-8, MaxIts=2000, MaxSize=300, EstimatorTol=1e-2)},
    low_frequency=dict(AMSSingularOperator=True, MaxIts=3000),
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
                   ).build(log=log, insulators=False)
    s = dict(st)
    for k in ('h_edge', 'h_in', 'dz_copper'):
        s[k] = st[k] / level
    region = box(*SETTINGS['gap_box'])
    lines = {}
    for name in ('TX', 'RX'):
        cu = shapely.unary_union([g for p in lay.parts if p.body == name for g in p.polys.values()])
        lines[name] = P.facing_vertices(cu, region, axis=1)   # from one round end's tip to the other's
    m = M.build_mesh(lay, M.Settings(**s), extra_lines=list({l.wkt: l for l in lines.values()}.values()), log=log)
    t, tp, q, qp = M.outer_faces(m)
    bnds = [('OUTER', t, tp, q, qp)]
    for name in ('TX', 'RX'):
        k = m['names'].index(name)
        cu = shapely.unary_union([g for p in lay.parts if p.body == name for g in p.polys.values()])
        z0, z1 = zrange(lay, name)
        P.electrodes(m, k, region.difference(cu), z0, z1)    # exactly two faces either side: the gap opens it
        qs, qsp = M.vertical_faces(m, z0, z1, lines[name], tol=1e-6)
        bnds.append((f'{name}_PORT', t[:0], tp[:0], qs, qsp))
        log(f'{name}: port {len(qs)} faces, {lines[name].length:.4f} mm by {z1 - z0:.4f} mm at z {z0:.4f}')
    return m, lay, bnds


def references(dz_mm, n=21):
    """M of the two loops as Palace has them: each closed by its port's sheet across its gap, the TX's current running
    through its sheet and the RX's EMF the line integral round its copper and across its sheet, so in effect two
    closed coaxial rings, whose M is Maxwell's formula (references.arc_mutual over the whole circle), averaged over
    both widths with the current uniform across them (n x n radii). The open arcs between the round ends' centres
    (Neumann's double integral over 356 degrees each) are given for scale: they are what M would be if no current
    crossed the TX's gap and the RX's EMF were taken only along its copper."""
    r, w = SETTINGS['radius_mm'], SETTINGS['width_mm']
    half_gap = math.asin((SETTINGS['gap_mm'] + w) / 2 / r)
    theta = 2 * math.pi - 2 * half_gap
    xs = r + np.linspace(-w / 2, w / 2, n)
    m_ring = float(np.mean([[arc_mutual(a, b, dz_mm, 2 * math.pi) for b in xs] for a in xs]))
    m_open = float(np.mean([[arc_mutual(a, b, dz_mm, theta) for b in xs] for a in xs]))
    return dict(dz_mm=dz_mm, M_closed_h=m_ring, M_open_h=m_open, theta_open_rad=theta,
                M_filament_closed_h=arc_mutual(r, r, dz_mm, 2 * math.pi))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--levels', type=float, nargs='+', default=SETTINGS['levels'])
    ap.add_argument('--freqs', type=float, nargs='+', default=SETTINGS['freqs_hz'])
    ap.add_argument('--solver', choices=sorted(SETTINGS['solvers']), default='ams')
    ap.add_argument('--ranks', type=int, default=SETTINGS['ranks'])
    ap.add_argument('--mesh-only', action='store_true', help='build and write the meshes, solve nothing')
    ap.add_argument('--mesh', action='append', default=[], metavar='KEY=VALUE',
                    help='change one of SETTINGS["mesh"], e.g. grade=0.125 (the air near the copper graded finer)')
    ap.add_argument('--results', default='results.json', help='the results file, beside this script')
    ap.add_argument('--out', default=str(HERE / 'case'))
    ap.add_argument('--restart', type=int, help="GMRES's restart (MaxSize) in place of SETTINGS': fewer vectors "
                    'held, for a mesh whose solve would not fit in memory')
    a = ap.parse_args()
    solver = dict(SETTINGS['solvers'][a.solver], **({'MaxSize': a.restart} if a.restart else {}))
    mesh = dict(SETTINGS['mesh'])
    for kv in a.mesh:
        k, v = kv.split('=')
        if k not in mesh:
            ap.error(f'--mesh {k}: not one of {sorted(mesh)}')
        mesh[k] = float(v)
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / 'run.log', 'a')

    def log(msg):
        print(msg, flush=True)
        logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
        logf.flush()
    export = S.kese_geometry(HERE / SETTINGS['board'], HERE / '3D_Geometry', log=log)
    res_file = HERE / a.results
    old = json.loads(res_file.read_text()) if res_file.exists() else {}
    result = dict(board=SETTINGS['board'], settings=dict(SETTINGS, mesh=mesh, solvers=dict(SETTINGS['solvers'], **{a.solver: solver})), versions=S.versions([export]),
                  references=old.get('references'), runs=old.get('runs', []))
    for level in a.levels:
        t0 = time.time()
        m, lay, bnds = build(export, level, mesh, log)
        if not result['references']:
            (tx0, tx1), (rx0, rx1) = zrange(lay, 'TX'), zrange(lay, 'RX')
            result['references'] = references(0.5 * (tx0 + tx1) - 0.5 * (rx0 + rx1))
            log(f"reference: M {result['references']['M_closed_h'] * 1e9:.4f} nH for the closed rings "
                f"{result['references']['dz_mm']:.4f} mm apart (open arcs {result['references']['M_open_h'] * 1e9:.4f})")
        folder = out / f'level{level:g}_{a.solver}'
        tags = M.write_gmsh(m, folder / 'mesh.msh', bnds, log=log)
        mesh_s = time.time() - t0
        size = dict(nodes=len(m['nodes']), wedges=len(m['wedges']), tetrahedra=len(m['tets']))
        if a.mesh_only:
            log(f"level {level:g}: {size}")
            continue
        case = C.Case(mesh=folder / 'mesh.msh', conductors=[tags['TX'], tags['RX']],
                      air=[tags[n] for n in m['names'] if n not in ('TX', 'RX')], outer=[tags['OUTER']],
                      ports=[C.Port('TX', tags['TX_PORT'], SETTINGS['port_direction'], R=SETTINGS['port_ohm'],
                                    excite=1),
                             C.Port('RX', tags['RX_PORT'], SETTINGS['port_direction'], R=SETTINGS['port_ohm'],
                                    excite=2)],
                      sigma=SETTINGS['sigma'], order=SETTINGS['order'], solver=solver)
        solves = []
        for f in a.freqs:
            case.solver = dict(solver, **(SETTINGS['low_frequency'] if f < 1e5 else {}))
            got = C.run(case, f, folder / f'f{f:g}', np_=a.ranks, log=log)
            rows = C.coil_rows(case, got, 'TX')
            tx, rx = rows['TX'], rows['RX']
            le = C.energy_check(case, got, 'TX')
            solves.append(dict(frequency_hz=f, M_h=rx['M'], M_reverse_h=rx['M_reverse'], L_tx_h=tx['L'],
                               R_tx_ohm=tx['R'], L_rx_h=rx['L_self'], R_rx_ohm=rx['R_self'], L_from_energy_h=le,
                               Z_ohm={'re': got['Z'].real.tolist(), 'im': got['Z'].imag.tolist()},
                               seconds=got['seconds'], peak_memory_gb=got['peak_memory_gb'],
                               iterations=got['iterations'], residuals=got['residuals'],
                               converged=got['converged'], ranks=got['ranks']))
            log(f"level {level:g}, f {f:.4g} Hz: M {rx['M'] * 1e9:.4f} nH (back {rx['M_reverse'] * 1e9:.4f}), L_TX "
                f"{tx['L'] * 1e9:.3f} nH, R_TX {tx['R'] * 1e3:.3f} mOhm, L_RX {rx['L_self'] * 1e9:.3f} nH, "
                f"{size['nodes']:,} nodes, {got['seconds']:.0f} s, {got['peak_memory_gb']} GB, iterations "
                f"{got['iterations']}")
        run = dict(level=level, solver=a.solver, order=SETTINGS['order'], gmres_restart=solver['MaxSize'],
                   mesh_seconds=round(mesh_s, 1), **size,
                   solves=solves)
        result['runs'] = [r for r in result['runs'] if (r['level'], r['solver']) != (level, a.solver)] + [run]
        result['runs'].sort(key=lambda r: (r['solver'], r['level']))
        res_file.write_text(json.dumps(result, indent=1))
        (folder / 'mesh.msh').unlink(missing_ok=True)
    if not a.mesh_only:
        log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
