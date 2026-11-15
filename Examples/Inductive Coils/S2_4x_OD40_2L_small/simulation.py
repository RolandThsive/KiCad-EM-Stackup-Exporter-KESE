"""S2_4x_OD40_2L_small in Elmer: the TX's inductance and resistance with the rotor away and present, and the TX to
SIN and COS coupling against the rotor's angle (checks C1, C2, C3, C4, C10 of this folder's README).

    python simulation.py                         rotor away, then every angle in SETTINGS['angles_deg']
    python simulation.py --angles 0              rotor away and the rotor at 0 degrees only
    python simulation.py --angles 0 --no-away    the rotor at 0 degrees only
    python simulation.py --level 0.8             a coarser mesh (the copper's mesh sizes divided by 0.8)

One mesh serves every run: the rotor's outline at every angle is drawn into it, and each run only relabels which
wedges are rotor copper, so the differences between runs carry no remeshing noise. The TX carries 1 A at 3.5 MHz;
SIN and COS carry none, so their voltages are the EMFs the TX induces in them.

Writes results.json beside this file and the runs under case/ (not committed). Every setting is in SETTINGS.
This script is GPL-3.0 as the bridge; the boards beside it keep their own licence (see ../LICENSE.md).
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import shapely
from shapely import affinity
from shapely.geometry import LineString, Point

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from bridge import elmer_case as E, geometry as G, mesh25d as M, ports as P, study as S   # noqa: E402

SPEC = json.loads((HERE / 'test_spec.json').read_text())
AXIS = (100.0, -100.0)                 # KiCad (100, 100) in model coordinates, y up


def model_xy(xy_kicad):
    """KiCad (x, y) to model (x, y), on the mesher's 0.5 um grid so that a sheet's line lands on mesh edges."""
    return round(xy_kicad[0] * 2000) / 2000, round(-xy_kicad[1] * 2000) / 2000


SETTINGS = dict(
    stator='Stator.kicad_pcb',
    rotor='Rotor.kicad_pcb',
    names={'TX': 'TX', '1': 'COS', '2': 'SIN'},    # KESE's copper part per net -> the coil's name
    sigma=5.8e7,
    freq_hz=SPEC['sets'][0]['f_Hz'],
    air_gap_mm=SPEC['air_gap_mm'],     # stator F.Cu top to rotor copper face
    insulators=False,                  # FR-4 and mask are air to the magneto-quasi-static solve
    angles_deg=SPEC['sets'][0]['c4_angles_mech_deg'],
    domain_radius_mm=SPEC['air_box']['radius_or_half_width_mm'],
    domain_z_mm=SPEC['air_box']['z_range_mm'],
    tx_end=model_xy(SPEC['terminals']['TX']['ends_xy_kicad']),
    tx_end_radius_mm=0.1,              # the trace ends' round caps (0.2 mm traces)
    rx_vias={'SIN': model_xy(SPEC['terminals']['2']['via_xy_kicad']),
             'COS': model_xy(SPEC['terminals']['1']['via_xy_kicad'])},
    via_void_radius_mm=0.3,            # the barrel (drill 0.4 mm) is left out inside this radius; the pad is 0.4
    sheet_half_mm=0.08,                # half the length of a TX sheet's line; an RX sheet's is 0.25
    level=1.0,
    mesh=dict(h_edge=0.1, h_in=0.2, h_max=6.0, grade=0.5, dz_copper=0.018, dz_max=0.4,
              tet_max=8.0, tet_grade=0.7),
    threads=4,
    tol=1e-7,
    max_iter=1500,
)


def stator_parts(export):
    mats = json.loads((export / 'materials.json').read_text())
    top = G.copper_top(mats)
    names = SETTINGS['names']

    def body_of(name, info):
        if info['role'] == 'copper':
            return names.get(str(info.get('net')), 'COPPER_' + str(info.get('net')))
        return 'MASK' if info['role'] == 'mask' else 'FR4'
    parts, _ = G.load_parts(export, z_shift=-top, body_of=body_of)
    return parts


def rotor_parts(export, angle_deg, body='ROTOR'):
    """The rotor as drawn, turned copper side down without mirroring, its copper face air_gap above z = 0, turned
    by angle_deg about the axis in KiCad's sense."""
    mats = json.loads((export / 'materials.json').read_text())
    cu = [i for i in mats['parts'].values() if i['role'] == 'copper']
    face = max(i['z_range_mm'][1] for i in cu)            # the copper's outer face, which turns to face down
    shift = SETTINGS['air_gap_mm'] + face                 # after z -> -z it lies at -face
    parts, _ = G.load_parts(export, z_shift=shift, flip=True, rotate_deg=angle_deg, axis=AXIS, prefix='R_',
                            body_of=lambda n, i: body if i['role'] == 'copper' else 'R_' + i['role'].upper())
    return parts


def coil_zrange(lay, body):
    zs = [z for p in lay.parts if p.body == body for z in p.zrange]
    return min(zs), max(zs)


def voids(stator):
    """Air parts that leave the two RX vias' barrels out (priority over copper), through the dielectric."""
    out = []
    for name, xy in SETTINGS['rx_vias'].items():
        z0, z1 = None, None
        for p in stator:
            if p.body == name:
                lo, hi = p.zrange
                z0, z1 = lo, hi
        lv = sorted({z for p in stator if p.body == name for z in p.levels()})
        # the dielectric's span: between the bottom copper's top and the top copper's bottom
        inner = [z for z in lv if z0 < z < z1]
        b0, b1 = min(inner), max(inner)
        disc = Point(xy).buffer(SETTINGS['via_void_radius_mm'], 64)
        out.append(M.Part(name=f'{name}_via_void', body='AIR', role='void', priority=4, fixed={(b0, b1): disc}))
    return out


def rotor_outlines(rotor_export, angles):
    """The rotor copper's outline (one slab's section) at each angle, as polygons in model coordinates."""
    base = rotor_parts(rotor_export, 0.0)
    lay = M.Layout(base, M.disc(AXIS, SETTINGS['domain_radius_mm'], n=64), (-70, 70)).build(
        log=lambda *_: None, insulators=False)
    g = shapely.unary_union([geo for p in lay.parts if p.body == 'ROTOR' for geo in p.polys.values()])
    return {a: affinity.rotate(g, -a, origin=AXIS) for a in angles}


def build(stator_export, rotor_export, angles, level, log=print):
    st = SETTINGS['mesh']
    stator = stator_parts(stator_export)
    parts = stator + voids(stator) + rotor_parts(rotor_export, angles[0] if angles else 0.0)
    z0, z1 = SETTINGS['domain_z_mm']
    lay = M.Layout(parts, M.disc(AXIS, SETTINGS['domain_radius_mm'], h=st['h_max']), (z0, z1)).build(
        log=log, insulators=SETTINGS['insulators'])
    outl = rotor_outlines(rotor_export, angles)
    lines = [LineString(r.coords) for g in outl.values() for r in M._rings(g)]
    sheets = {}
    tx = SETTINGS['tx_end']
    h = SETTINGS['sheet_half_mm']
    sheets['TX'] = LineString([(tx[0] - h, tx[1]), (tx[0] + h, tx[1])])
    for name, xy in SETTINGS['rx_vias'].items():
        sheets[name] = LineString([(xy[0] - 0.25, xy[1]), (xy[0] + 0.25, xy[1])])
    s = dict(st)
    for k in ('h_edge', 'h_in', 'dz_copper'):
        s[k] = st[k] / level
    m = M.build_mesh(lay, M.Settings(**s), extra_lines=lines + list(sheets.values()), extra_fine=list(outl.values()),
                     log=log)
    t, tp, q, qp = M.outer_faces(m)
    bnds = [('OUTER', t, tp, q, qp)]
    for name in ('TX', 'SIN', 'COS'):
        k = m['names'].index(name)
        if name == 'TX':
            gap = Point(tx).buffer(SETTINGS['tx_end_radius_mm'], 32)
        else:
            gap = Point(SETTINGS['rx_vias'][name]).buffer(SETTINGS['via_void_radius_mm'], 64)
        lo, hi = coil_zrange(lay, name)
        lv = sorted({z for p in lay.parts if p.body == name for z in p.levels()})
        inner = [z for z in lv if lo < z < hi]
        b0, b1 = min(inner), max(inner)                   # the faces of the copper toward the dielectric
        e1, e2 = P.electrodes(m, k, gap, b0, b1)
        qs, qsp = M.vertical_faces(m, b0, b1, sheets[name], tol=1e-4)
        bnds += [(f'{name}_T1', *e1), (f'{name}_T2', *e2), (f'{name}_SHEET', t[:0], tp[:0], qs, qsp)]
        log(f'{name}: electrodes {len(e1[0]) + len(e1[2])} and {len(e2[0]) + len(e2[2])} faces, sheet {len(qs)} '
            f'faces, z {b0:.4f} to {b1:.4f}')
    return m, lay, bnds


def relabelled(m, stator_export, rotor_export, angle, log=print):
    """The mesh with the rotor at `angle` (degrees, KiCad's sense), or away (None: its copper made air)."""
    stator = stator_parts(stator_export)
    rot = rotor_parts(rotor_export, 0.0 if angle is None else angle, body='AIR' if angle is None else 'ROTOR')
    lay = M.Layout(stator + voids(stator) + rot, m['layout'].region, m['layout'].zbox).build(
        log=lambda *_: None, insulators=SETTINGS['insulators'])
    return M.relabel(m, lay, log=log)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--angles', type=float, nargs='*', default=SETTINGS['angles_deg'])
    ap.add_argument('--no-away', action='store_true', help='skip the run with the rotor away')
    ap.add_argument('--level', type=float, default=SETTINGS['level'])
    ap.add_argument('--mesh-only', action='store_true', help='build and write the mesh, solve nothing')
    ap.add_argument('--out', default=str(HERE / 'case'))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / 'run.log', 'a')

    def log(msg):
        print(msg, flush=True)
        logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
        logf.flush()
    se = S.kese_export(HERE / SETTINGS['stator'], out / 'kese', log=log)
    re_ = S.kese_export(HERE / SETTINGS['rotor'], out / 'kese', log=log)
    angles = list(a.angles)
    t0 = time.time()
    m, lay, bnds = build(se, re_, angles or [0.0], a.level, log)
    mesh_s = time.time() - t0
    res_file = HERE / ('results.json' if a.level == 1.0 else f'results_level{a.level:g}.json')
    result = json.loads(res_file.read_text()) if res_file.exists() else dict(
        board=HERE.name, settings=SETTINGS, expected=SPEC['expected'], versions=S.versions(), runs=[])
    result['mesh'] = dict(level=a.level, seconds=round(mesh_s, 1), nodes=len(m['nodes']), wedges=len(m['wedges']),
                          tetrahedra=len(m['tets']), triangles=int(m['nt']), layers=int(m['nk']))
    if a.mesh_only:
        log(f"mesh: {result['mesh']}")
    runs = ([] if a.no_away else [None]) + angles
    for angle in runs:
        tag = 'away' if angle is None else f'rotor{angle:g}'
        mm = relabelled(m, se, re_, angle, log)
        folder = out / f'level{a.level:g}_{tag}'
        M.write_elmer(mm, folder / 'mesh_files', bnds, log=log)
        if a.mesh_only:
            continue
        cu = E.Material('Copper', sigma=SETTINGS['sigma'])
        bodies = {n: (cu if n in ('TX', 'SIN', 'COS', 'ROTOR') else E.Material('Air' if n == 'AIR' else n.title()))
                  for n in mm['names']}
        case = E.Case(mesh_dir=folder / 'mesh_files', bodies=bodies, order=1, tol=SETTINGS['tol'],
                      max_iter=SETTINGS['max_iter'],
                      coils=[E.Coil('TX', 'TX', 'TX_T1', 'TX_T2', 'TX_SHEET', 1.0),
                             E.Coil('SIN', 'SIN', 'SIN_T1', 'SIN_T2', 'SIN_SHEET', 0.0),
                             E.Coil('COS', 'COS', 'COS_T1', 'COS_T2', 'COS_SHEET', 0.0)])
        rows = S.solve(case, [SETTINGS['freq_hz']], folder, threads=SETTINGS['threads'], log=log, tag=tag)
        result['runs'] = [r for r in result['runs'] if r.get('rotor_deg', 'away') != (angle if angle is not None
                                                                                       else 'away')]
        result['runs'].append(dict(rotor_deg=angle if angle is not None else 'away', level=a.level, solve=rows[0]))
        res_file.write_text(json.dumps(result, indent=1))
        c = rows[0]['coils']
        log(f"{tag}: L_TX {c['TX']['L'] * 1e6:.4f} uH, R_TX {c['TX']['R']:.4f} Ohm, M_SIN {c['SIN']['M'] * 1e9:.3f} nH, "
            f"M_COS {c['COS']['M'] * 1e9:.3f} nH, {rows[0]['iterations']} it, res {rows[0]['residual']}")
        shutil.rmtree(folder / 'mesh_files', ignore_errors=True)       # the mesh is large; the results stay
    if not a.mesh_only:
        log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
