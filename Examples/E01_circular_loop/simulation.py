"""E01: one circular trace, 20 mm across, opened by a 0.2 mm gap: its inductance and resistance from Palace, against
Neumann's integral over the open arc and the resistance of an annular sector.

    python simulation.py                      the mesh ladder at both frequencies
    python simulation.py --levels 0.5         one mesh only
    python simulation.py --mesh-only          build the meshes and print their size, solve nothing
    python simulation.py --levels 0.75 --mesh grade=0.125 --mesh tet_grade=0.175 --mesh dz_max=0.2 \
        --results results_grade.json --out case_grade      the air graded as the coil boards' is
    python simulation.py --levels 0.75 --domain-mm 120 --results results_domain120.json --out case_domain120

The trace is meshed from KESE's export as the coil boards are: a 2.5D mesh of wedges through the copper and the
air beside it, tetrahedra above and below out to a disc 60 mm round. The port is a lumped port on the sheet across
the gap's floor, between the two round ends. Writes results.json beside this file and the runs under case/ (not
committed). Every setting is in SETTINGS.
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
from bridge import geometry as G, mesh25d as M, palace_case as C, ports as P, study as S   # noqa: E402
from references import arc_inductance, ring_inductance   # noqa: E402

SETTINGS = dict(
    board='E01_circular_loop.kicad_pcb',
    centre=(100.0, -100.0),        # the loop's centre in model coordinates (KiCad (100, 100), y up)
    radius_mm=10.0,                # the trace's centre line
    width_mm=0.5,
    gap_mm=0.2,
    gap_box=(109.75, -100.35, 110.25, -99.65),   # holds the 0.2 mm gap between the two round ends
    port_direction='+Y',           # across the gap, from one round end to the other
    sigma=5.8e7,                   # copper, S/m
    domain_radius_mm=60.0,         # 6 loop radii; the outside is a perfect conductor (tangential E = 0)
    domain_half_height_mm=60.0,
    freqs_hz=[1e4, 3.5e6],         # uniform current (10 kHz, skin depth 0.66 mm) and the coils' frequency
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


def build(export, level, st, log=print, domain=None):
    mats = json.loads((export / 'materials.json').read_text())
    parts, _ = G.load_parts(export, z_shift=-G.copper_top(mats))
    c = SETTINGS['centre']
    R = domain or SETTINGS['domain_radius_mm']
    H = domain or SETTINGS['domain_half_height_mm']
    lay = M.Layout(parts, M.disc(c, R, h=st['h_max']), (-H, H)).build(log=log, insulators=False)
    s = dict(st)
    for k in ('h_edge', 'h_in', 'dz_copper'):
        s[k] = st[k] / level
    cu = shapely.unary_union([g for p in lay.parts if p.body == 'LOOP' for g in p.polys.values()])
    gap = box(*SETTINGS['gap_box']).difference(cu)
    line = P.facing_vertices(cu, box(*SETTINGS['gap_box']), axis=1)   # from one round end's tip to the other's
    m = M.build_mesh(lay, M.Settings(**s), extra_lines=[line], log=log)
    loop = m['names'].index('LOOP')
    zs = [z for p in lay.parts if p.body == 'LOOP' for z in p.zrange]
    z0, z1 = min(zs), max(zs)
    P.electrodes(m, loop, gap, z0, z1)                 # exactly two faces either side: the gap opens the loop
    qs, qsp = M.vertical_faces(m, z0, z1, line, tol=1e-6)   # the port: a rectangle across the gap, through the copper
    t, tp, q, qp = M.outer_faces(m)
    return m, [('OUTER', t, tp, q, qp), ('PORT', t[:0], tp[:0], qs, qsp)], line.length


def references(t):
    """The open loop as Palace sees it: its copper runs on round its round ends to the gap's two faces, 0.2 mm
    apart, and the port's sheet closes it across the gap. Neumann's double integral over the arc with the GMD
    (references.arc_inductance) brackets that: the arc between the round ends' centres (356.0 degrees) and the arc
    to the gap's faces (358.9 degrees), at DC (the rectangle's GMD) and with the current crowded to the strip's
    edges (w / 4). Grover's ring formula for the closed ring is given beside them. R_dc is the annular sector's
    resistance between the round ends' centres, which the half-discs past them add a little to."""
    r, w = SETTINGS['radius_mm'], SETTINGS['width_mm']
    g_dc = 0.2235 * (w + t)
    g_hf = w / 4
    th_c = 2 * math.pi - 2 * math.asin((SETTINGS['gap_mm'] + w) / 2 / r)
    th_f = 2 * math.pi - 2 * math.asin(SETTINGS['gap_mm'] / 2 / r)
    r_dc = th_c / (SETTINGS['sigma'] * t * 1e-3 * math.log((r + w / 2) / (r - w / 2)))
    return dict(L_arc_centres_dc_h=arc_inductance(r, th_c, g_dc), L_arc_faces_dc_h=arc_inductance(r, th_f, g_dc),
                L_arc_centres_hf_h=arc_inductance(r, th_c, g_hf), L_arc_faces_hf_h=arc_inductance(r, th_f, g_hf),
                L_ring_dc_h=ring_inductance(r, g_dc), R_dc_ohm=r_dc, theta_centres_rad=th_c, theta_faces_rad=th_f,
                gmd_dc_mm=g_dc, gmd_hf_mm=g_hf)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--levels', type=float, nargs='+', default=SETTINGS['levels'])
    ap.add_argument('--freqs', type=float, nargs='+', default=SETTINGS['freqs_hz'])
    ap.add_argument('--solver', choices=sorted(SETTINGS['solvers']), default='ams')
    ap.add_argument('--ranks', type=int, default=SETTINGS['ranks'])
    ap.add_argument('--mesh-only', action='store_true', help='build and write the meshes, solve nothing')
    ap.add_argument('--mesh', action='append', default=[], metavar='KEY=VALUE',
                    help='change one of SETTINGS["mesh"], e.g. grade=0.125 (the air near the copper graded finer)')
    ap.add_argument('--domain-mm', type=float, help='the domain\'s radius and half height, in place of 60 mm')
    ap.add_argument('--results', default='results.json', help='the results file, beside this script')
    ap.add_argument('--out', default=str(HERE / 'case'))
    a = ap.parse_args()
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
    mats = json.loads((export / 'materials.json').read_text())
    t = next(i['z_range_mm'][1] - i['z_range_mm'][0] for i in mats['parts'].values() if i['role'] == 'copper')
    res_file = HERE / a.results
    old = json.loads(res_file.read_text()).get('runs', []) if res_file.exists() else []
    settings = dict(SETTINGS, mesh=mesh)
    if a.domain_mm:
        settings.update(domain_radius_mm=a.domain_mm, domain_half_height_mm=a.domain_mm)
    result = dict(board=SETTINGS['board'], settings=settings, copper_mm=t, references=references(t),
                  versions=S.versions([export]), runs=old)
    for level in a.levels:
        t0 = time.time()
        m, bnds, port_mm = build(export, level, mesh, log, domain=a.domain_mm)
        folder = out / f'level{level:g}_{a.solver}'
        tags = M.write_gmsh(m, folder / 'mesh.msh', bnds, log=log)
        mesh_s = time.time() - t0
        size = dict(nodes=len(m['nodes']), wedges=len(m['wedges']), tetrahedra=len(m['tets']), port_mm=port_mm)
        if a.mesh_only:
            log(f"level {level:g}: {size}")
            continue
        case = C.Case(mesh=folder / 'mesh.msh', conductors=[tags['LOOP']],
                      air=[tags[n] for n in m['names'] if n != 'LOOP'], outer=[tags['OUTER']],
                      ports=[C.Port('LOOP', tags['PORT'], SETTINGS['port_direction'], R=50.0, excite=1)],
                      order=SETTINGS['order'], solver=SETTINGS['solvers'][a.solver])
        solves = []
        for f in a.freqs:
            case.solver = dict(SETTINGS['solvers'][a.solver], **(SETTINGS['low_frequency'] if f < 1e5 else {}))
            got = C.run(case, f, folder / f'f{f:g}', np_=a.ranks, log=log)
            row = C.coil_rows(case, got, 'LOOP')['LOOP']
            le = C.energy_check(case, got, 'LOOP')
            solves.append(dict(frequency_hz=f, L_h=row['L'], R_ohm=row['R'], L_from_energy_h=le,
                               seconds=got['seconds'], peak_memory_gb=got['peak_memory_gb'],
                               iterations=got['iterations'], residuals=got['residuals'], converged=got['converged'],
                               ranks=got['ranks']))
            log(f"level {level:g}, {a.solver}, f {f:.4g} Hz: L {row['L'] * 1e9:.3f} nH (energy "
                f"{(le or float('nan')) * 1e9:.3f}), R {row['R'] * 1e3:.3f} mOhm, {size['nodes']:,} nodes, "
                f"{got['seconds']:.0f} s, {got['peak_memory_gb']} GB, iterations {got['iterations']}")
        run = dict(level=level, solver=a.solver, order=SETTINGS['order'], mesh_seconds=round(mesh_s, 1), **size,
                   solves=solves)
        result['runs'] = [r for r in result['runs'] if (r['level'], r['solver']) != (level, a.solver)] + [run]
        result['runs'].sort(key=lambda r: (r['solver'], r['level']))
        res_file.write_text(json.dumps(result, indent=1))
    if not a.mesh_only:
        log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
