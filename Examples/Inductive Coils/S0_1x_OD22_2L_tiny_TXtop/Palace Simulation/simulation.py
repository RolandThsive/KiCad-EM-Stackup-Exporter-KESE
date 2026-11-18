"""A coil set from the Sinusoidal Coil Generator in Palace: the SIN and COS curves against the rotor's angle, at any
air gap. Everything that belongs to the board is in test_spec.json beside this file, so the same script runs every
single-set board that new_coil.py sets up; the board's README, one folder up, says what this board is. A board folder
holds Boards/ (straight from the generator), 3D_Geometry/ (KESE's export of the two boards), Palace Simulation/ (this
script, test_spec.json, angle_error.py and the runs under case/) and Results/ (what the runs give, and what was
expected).

    python simulation.py                          the rotor away, then every angle in test_spec.json
    python simulation.py --gap 0.5                the same at a 0.5 mm air gap (copper to copper)
    python simulation.py --angles 0 90 --no-away  the rotor at 0 and 90 degrees only
    python simulation.py --step 10                every 10 degrees over the whole turn
    python simulation.py --jobs 2 --ranks 2       two solves at once, each on two MPI ranks
    python simulation.py --plot                   only redraw the curves from the results already written
    python simulation.py --angles 0 --mesh-only   build one mesh and say its size, to judge the memory
    python simulation.py --level 0.5              a finer mesh than test_spec.json's (a trial, kept in case/)
    python simulation.py --mesh grade=0.25        the air beside the copper meshed finer (a trial, kept in case/)
    python simulation.py --gap 0.5 --merge a.json b.json
                                                  add the solves in results files from other machines (each one
                                                  ran some angles of this gap) to this gap's results, and redraw

The TX is driven through a lumped port; SIN and COS are opened by lumped ports of 1 MOhm, so their voltages are the
EMFs the TX induces in them, given as mutual inductances (EMF = 2 pi f M x 1 A: 1 nH is 22 mV at 3.5 MHz). The rotor
repeats itself every 360 / sectors degrees, so the curves are drawn over that span: a full turn on a one-sector rotor.

Every angle gets its own mesh, the rotor's copper at that angle drawn into it: wedges through the boards' copper and
the air between them, tetrahedra out to a cylinder three board radii round. The stator's mesh then differs a little
between angles, which shows as small noise on the curves; the fit written with the results says how much. Each solve
is checked two ways: the TX's L from its port's voltage against L from the magnetic energy in the whole field, and at
the first angle of each gap, reciprocity (SIN and COS are driven too, and the M from each back to the TX must equal
the M from the TX to it).

Writes into ../Results/<gap>_AirGap (1mm_AirGap, 0d5mm_AirGap): results_gap<gap>mm.json, a table (.csv) and the
chart (.webp, by make_charts.py beside this file); and into ../Results, SINCOS_Results.md: every
gap's curves with a caption, the fit, the angle error at each angle (angle_error.py beside this file) and every
solve, and SINCOS_gaps.webp with all the gaps on one chart once two are solved. The runs go under case/ here (not
committed). This script is GPL-3.0 as the bridge; the boards keep their own licence (see ../../LICENSE.md).
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Point, Polygon

HERE = Path(__file__).resolve().parent              # <board>/Palace Simulation
BOARD = HERE.parent                                 # <board>: README.md, Boards/, Palace Simulation/, Results/
RESULTS = BOARD / 'Results'
GEOMETRY = BOARD / '3D_Geometry'                     # KESE's export of each board, kept in the repo
sys.path.insert(0, str(HERE.parents[3]))
sys.path.insert(0, str(HERE))
from angle_error import METHOD, angle_error, gap_folder, results_files, sine_fit   # noqa: E402
import make_charts as charts   # noqa: E402
from bridge import geometry as G, mesh25d as M, palace_case as C, ports as P, study as S   # noqa: E402

SPEC = json.loads((HERE / 'test_spec.json').read_text())
EXPECTED = (json.loads((RESULTS / 'expected_results.json').read_text())
            if (RESULTS / 'expected_results.json').exists() else {})
AXIS = (100.0, -100.0)                 # KiCad (100, 100) in model coordinates, y up
GRID = 0.0005                          # mm, the mesher's snap grid


def snap(xy):
    """A point on the mesher's grid, so that a port's line lands exactly on mesh edges."""
    return round(xy[0] / GRID) * GRID, round(xy[1] / GRID) * GRID


def model_xy(xy_kicad):
    """KiCad (x, y) to model (x, y), on the mesher's grid."""
    return snap((xy_kicad[0], -xy_kicad[1]))


SET = SPEC['sets'][0]
SIN_NET, COS_NET = str(SET['sin']), str(SET['cos'])
AGREE = charts.AGREE   # how far the TX's L from its port may be from L from the field energy, and M from the TX
                       # from M back to it, for a solve to be read (make_charts.readable)
SETTINGS = dict(
    stator=SPEC['files']['stator'],    # paths from the board folder
    rotor=SPEC['files']['rotor'],
    names={str(k): v for k, v in SPEC['nets'].items()},   # KESE's copper part per net -> the coil's name
    sigma=5.8e7,
    freq_hz=SET['f_Hz'],
    air_gap_mm=SPEC['air_gap_mm'],     # stator F.Cu top to rotor copper face; --gap sets another
    insulators=False,                  # FR-4 and mask are air here: at 3.5 MHz their permittivity changes nothing
    angles_deg=SET['sweep_angles_mech_deg'],
    period_deg=SET.get('rotor_period_mech_deg', 360.0),   # the rotor repeats itself after this
    domain_radius_mm=SPEC['air_box']['radius_or_half_width_mm'],
    domain_margin_mm=SPEC['air_box']['radius_or_half_width_mm'],   # air above the rotor and below the stator
    tx_end=model_xy(SPEC['terminals']['TX']['ends_xy_kicad']),
    tx_end_radius_mm=SPEC['terminals']['TX'].get('end_radius_mm', 0.1),     # the trace ends' round caps
    rx_vias={'SIN': model_xy(SPEC['terminals'][SIN_NET]['via_xy_kicad']),
             'COS': model_xy(SPEC['terminals'][COS_NET]['via_xy_kicad'])},
    via_void_radius_mm=SPEC['terminals'][SIN_NET].get('void_radius_mm', 0.3),   # the barrel left out inside this
    rx_cuts={name: dict(xy=model_xy(c['xy_kicad']), along=(c['along_kicad'][0], -c['along_kicad'][1]),
                        gap_mm=c['gap_mm'], half_width_mm=c['half_width_mm'])
             for name, net in (('SIN', SIN_NET), ('COS', COS_NET))
             if (c := SPEC['terminals'][net].get('cut'))},    # with rx_port 'cut': where each top trace is cut
    sheet_half_mm=0.8 * SPEC['terminals']['TX'].get('end_radius_mm', 0.1),    # half the TX port's width
    rx_sheet_half_mm=0.25 / 0.3 * SPEC['terminals'][SIN_NET].get('void_radius_mm', 0.3),   # half an RX via port's
    level=SPEC.get('mesh_level', 0.25),   # the copper's mesh sizes divided by this
    port_segment_mm=None,              # each port line drawn into the mesh in pieces at most this long (None: as it falls)
    mesh=dict(h_edge=0.1, h_in=0.2, h_max=6.0, grade=0.125, dz_copper=0.018, dz_max=0.2,
              tet_max=8.0, tet_grade=0.175),
                                       # the air graded four times as finely as the bridge's default (0.5 and 0.7)
                                       # and wedge layers half as thick (0.4): the mesh study in the README
    order=1,                           # Nedelec elements of the first order
    tx_ohm=50.0,                       # the TX port's resistance (its source's); the receivers' are C.OPEN_OHM
    ranks=2,                           # MPI ranks per solve (--ranks)
    jobs=1,                            # solves at once (--jobs), each on `ranks` ranks
    solver='ams',
    solvers={'ams': dict(Type='AMS', KSPType='GMRES', Tol=1e-8, MaxIts=2000, MaxSize=300, EstimatorTol=1e-2),
             'ams_1e-10': dict(Type='AMS', KSPType='GMRES', Tol=1e-10, MaxIts=2000, MaxSize=300, EstimatorTol=1e-2),
             'ams_1e-6': dict(Type='AMS', KSPType='GMRES', Tol=1e-6, MaxIts=2000, MaxSize=300, EstimatorTol=1e-2)},
                                       # GMRES with hypre's AMS, to a residual of 1e-8 of where it starts (1e-10 and
                                       # 1e-6 are the trials it was chosen by); EstimatorTol only loosens Palace's
                                       # error estimate, which nothing here reads
    reciprocity='first',               # drive SIN and COS too: at the 'first' angle of each gap, at 'all', or 'none'
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


def rotor_parts(export, angle_deg, gap, body='ROTOR'):
    """The rotor as drawn, turned copper side down without mirroring, its copper face `gap` above z = 0, turned
    by angle_deg about the axis in KiCad's sense."""
    mats = json.loads((export / 'materials.json').read_text())
    cu = [i for i in mats['parts'].values() if i['role'] == 'copper']
    face = max(i['z_range_mm'][1] for i in cu)            # the copper's outer face, which turns to face down
    parts, _ = G.load_parts(export, z_shift=gap + face, flip=True, rotate_deg=angle_deg, axis=AXIS, prefix='R_',
                            body_of=lambda n, i: body if i['role'] == 'copper' else 'R_' + i['role'].upper())
    return parts


RX_PORT = SPEC.get('rx_port', 'via')   # how SIN and COS are opened: 'via' (a via left out) or 'cut' (a gap cut
                                       # across a top trace, at test_spec.json's 'cut' of each)
assert RX_PORT == 'via' or len(SETTINGS['rx_cuts']) == 2, "rx_port 'cut' needs a 'cut' for SIN and COS in test_spec.json"


def cut_geometry(name):
    """The cut across SIN's or COS's top trace (model coordinates): the region left out (gap_mm along the trace,
    wider than it), and the port's line across it, from the middle of one cut face to the middle of the other, along
    the trace. The line's two ends are on the grid and are corners of the region too, so that the port's sheet is an
    exact rectangle with its two ends on the cut faces, as Palace asks of a lumped port."""
    c = SETTINGS['rx_cuts'][name]
    d = np.asarray(c['along'], float) / np.linalg.norm(c['along'])
    n = np.array([-d[1], d[0]])
    o, hl, hw = np.asarray(c['xy']), c['gap_mm'] / 2, c['half_width_mm']
    p1, p2 = np.array(snap(o - hl * d)), np.array(snap(o + hl * d))
    box = Polygon([snap(p1 - hw * n), tuple(p1), snap(p1 + hw * n), snap(p2 + hw * n), tuple(p2), snap(p2 - hw * n)])
    return box, LineString([tuple(p1), tuple(p2)])


def top_copper(stator, name):
    """The z span of a coil's top copper (F.Cu)."""
    lo, hi = next(p.zrange for p in stator if p.body == name)
    lv = sorted({z for p in stator if p.body == name for z in p.levels()})
    return max(z for z in lv if lo < z < hi), hi


def voids(stator):
    """The parts that open SIN and COS. With RX_PORT 'via': each RX via's barrel left out through the dielectric (air
    with priority over copper), and its two pads filled over the drill hole (copper of the coil), since a via that is
    left out is not drilled; the port sheet then stands between copper over its whole width. With RX_PORT 'cut': a
    gap cut through the top copper of each."""
    out = []
    if RX_PORT == 'cut':
        for name in ('SIN', 'COS'):
            out.append(M.Part(name=f'{name}_cut', body='AIR', role='void', priority=4,
                              fixed={top_copper(stator, name): cut_geometry(name)[0]}))
        return out
    for name, xy in SETTINGS['rx_vias'].items():
        lo, hi = next(p.zrange for p in stator if p.body == name)
        lv = sorted({z for p in stator if p.body == name for z in p.levels()})
        inner = [z for z in lv if lo < z < hi]           # the dielectric's span between the two coppers
        disc = Point(xy).buffer(SETTINGS['via_void_radius_mm'], 64)
        out.append(M.Part(name=f'{name}_via_void', body='AIR', role='void', priority=4,
                          fixed={(min(inner), max(inner)): disc}))
        out.append(M.Part(name=f'{name}_pad_fill', body=name, role='bridge', priority=4,
                          fixed={(lo, min(inner)): disc, (max(inner), hi): disc}))
    return out


def coil_zrange(lay, body):
    zs = [z for p in lay.parts if p.body == body for z in p.zrange]
    return min(zs), max(zs)


def build(stator_export, rotor_export, angle, gap, level, log=print):
    """The mesh with the rotor at `angle` (degrees, KiCad's sense), or away (None: its copper made air), its
    boundaries (the outside and each coil's port sheet) and each port's direction."""
    st = SETTINGS['mesh']
    stator = stator_parts(stator_export)
    rot = rotor_parts(rotor_export, 0.0 if angle is None else angle, gap, body='AIR' if angle is None else 'ROTOR')
    top = max(z for p in rot for z in p.zrange)
    bottom = min(z for p in stator for z in p.zrange)
    zbox = (bottom - SETTINGS['domain_margin_mm'], top + SETTINGS['domain_margin_mm'])
    lay = M.Layout(stator + voids(stator) + rot, M.disc(AXIS, SETTINGS['domain_radius_mm'], h=st['h_max']),
                   zbox).build(log=log, insulators=SETTINGS['insulators'])
    sheets, extra = {}, []
    tx = SETTINGS['tx_end']
    h = SETTINGS['sheet_half_mm']
    sheets['TX'] = LineString([(tx[0] - h, tx[1]), (tx[0] + h, tx[1])])
    for name, xy in SETTINGS['rx_vias'].items():
        h2 = SETTINGS['rx_sheet_half_mm']
        if RX_PORT == 'via':
            sheets[name] = LineString([(xy[0] - h2, xy[1]), (xy[0] + h2, xy[1])])
        else:
            box, sheets[name] = cut_geometry(name)
            extra.append(LineString(box.exterior.coords))            # the cut's outline, drawn in
    if SETTINGS['port_segment_mm']:
        import shapely
        sheets = {k: shapely.segmentize(v, SETTINGS['port_segment_mm']) for k, v in sheets.items()}
    s = dict(st)
    for k in ('h_edge', 'h_in', 'dz_copper'):
        s[k] = st[k] / level
    m = M.build_mesh(lay, M.Settings(**s), extra_lines=list(sheets.values()) + extra, log=log)
    t, tp, q, qp = M.outer_faces(m)
    bnds, directions = [('OUTER', t, tp, q, qp)], {}
    solid = [p for p in lay.parts if p.role != 'void']
    for name in ('TX', 'SIN', 'COS'):
        k = m['names'].index(name)
        if name != 'TX' and RX_PORT == 'cut':
            # the port: a rectangle across the gap, through the top copper's thickness, from one cut face to the other
            box, line = cut_geometry(name)
            f0, f1 = top_copper(solid, name)
            P.electrodes(m, k, box, f0, f1)             # exactly two faces either side: the cut opens the coil
            qs, qsp = M.vertical_faces(m, f0, f1, line, tol=1e-6)
            (x0, y0), (x1, y1) = line.coords
            directions[name] = [(x1 - x0) / line.length, (y1 - y0) / line.length, 0.0]
            log(f'{name}: port across the cut, {len(qs)} faces, {line.length:.4f} mm by {f1 - f0:.4f} mm at z '
                f'{f0:.4f}')
        else:
            # the port: a rectangle standing between the coil's two copper layers, across the dielectric, where the
            # coil is opened (the TX's two stacked ends, or a receiver's left-out via)
            hole = (Point(tx).buffer(SETTINGS['tx_end_radius_mm'], 32) if name == 'TX'
                    else Point(SETTINGS['rx_vias'][name]).buffer(SETTINGS['via_void_radius_mm'], 64))
            lo, hi = coil_zrange(lay, name)
            lv = sorted({z for p in lay.parts if p.body == name for z in p.levels()})
            inner = [z for z in lv if lo < z < hi]
            b0, b1 = min(inner), max(inner)               # the faces of the copper toward the dielectric
            P.electrodes(m, k, hole, b0, b1)              # the coil's copper meets the opening in two places
            qs, qsp = M.vertical_faces(m, b0, b1, sheets[name], tol=1e-6)
            directions[name] = '+Z'
            log(f'{name}: port between the layers, {len(qs)} faces, {sheets[name].length:.4f} mm by '
                f'{b1 - b0:.4f} mm, z {b0:.4f} to {b1:.4f}')
        if not len(qs):
            raise ValueError(f'{name}: no mesh faces on the port line')
        bnds.append((f'{name}_PORT', t[:0], tp[:0], qs, qsp))
    return m, bnds, directions


def solve(m, bnds, directions, folder, solver, ranks, recip, log=print, tag=''):
    """One Palace solve at the set's frequency (with recip, one for each coil driven in turn): each coil's numbers
    (make_charts and the tables read them) and the solve's own."""
    tags = M.write_gmsh(m, folder / 'mesh.msh', bnds, log=log)
    cu = [tags[n] for n in m['names'] if n in ('TX', 'SIN', 'COS', 'ROTOR')]
    ports = [C.Port('TX', tags['TX_PORT'], directions['TX'], R=SETTINGS['tx_ohm'], excite=1)]
    ports += [C.Port(n, tags[f'{n}_PORT'], directions[n], R=C.OPEN_OHM, excite=(k if recip else 0))
              for k, n in ((2, 'SIN'), (3, 'COS'))]
    case = C.Case(mesh=folder / 'mesh.msh', conductors=cu, air=[tags[n] for n in m['names'] if tags[n] not in cu],
                  outer=[tags['OUTER']], ports=ports, sigma=SETTINGS['sigma'], order=SETTINGS['order'],
                  solver=SETTINGS['solvers'][solver])
    got = C.run(case, SETTINGS['freq_hz'], folder, np_=ranks, log=log)
    coils = C.coil_rows(case, got, 'TX')
    le = C.energy_check(case, got, 'TX')
    row = dict(frequency_hz=SETTINGS['freq_hz'], seconds=got['seconds'], peak_memory_gb=got['peak_memory_gb'],
               coils=coils, L_from_energy_h=le, iterations=got['iterations'], residuals=got['residuals'],
               converged=got['converged'], ranks=ranks, excitations=3 if recip else 1,
               Z_ohm={'ports': [p.name for p in ports], 're': np.nan_to_num(got['Z'].real, nan=0.0).tolist(),
                      'im': np.nan_to_num(got['Z'].imag, nan=0.0).tolist(), 'columns': got['driven']})
    if recip:
        scale = max(abs(coils[n]['M']) for n in ('SIN', 'COS')) or 1e-30
        row['reciprocity'] = {n: abs(coils[n]['M'] - coils[n]['M_reverse']) / scale for n in ('SIN', 'COS')}
    (folder / 'mesh.msh').unlink(missing_ok=True)                    # the mesh is large; the results stay
    shutil.rmtree(folder / 'out' / 'paraview', ignore_errors=True)
    return row


def fit(angles, values):
    """The best sine over the rotor's period (angle_error.sine_fit): offset, amplitude, phase and the rms left."""
    return sine_fit(angles, values, SETTINGS['period_deg'])


def model_label(res):
    """What the model is, in a few words, for the charts' subtitles."""
    d = res.get('solver', {})
    return f"mesh level {res.get('level', '?'):g}, {d.get('kind', 'AMS')}"


def report(log=print):
    """../Results/SINCOS_Results.md: for every air gap solved, the curves with a caption, the fit, the angle
    error and every solve; then the boards. Rewritten after every solve, so it is as current as the results."""
    gaps = results_files(RESULTS)
    if not gaps:
        return
    w = 2 * math.pi * SETTINGS['freq_hz'] * 1e-6                     # mV of EMF per nH at 1 A
    per = SETTINGS['period_deg']
    deg = (', the same as mechanical degrees here' if per == 360 and SET['loops'] == 1
           else f' ({per / 360:g} of a mechanical degree each)')
    st, ring, n_per = SPEC['stator'], SPEC['rotor']['rings'][0], SET['loops']
    rotor = ('a half-ring rotor' if ring['sectors'] == 1 and abs(ring['duty'] - 0.5) < 1e-6
             else f"a rotor of {ring['sectors']} copper sectors")
    summary, sections, curves, lt_all = [], [], [], []
    for i, (gap, path) in enumerate(gaps, 1):
        res = json.loads(path.read_text())
        runs = sorted((r for r in res['runs'] if r['rotor_deg'] != 'away'), key=lambda r: r['rotor_deg'])
        away = [r for r in res['runs'] if r['rotor_deg'] == 'away']
        ang = [r['rotor_deg'] for r in runs]
        ms = [r['solve']['coils']['SIN']['M'] * 1e9 for r in runs]
        mc = [r['solve']['coils']['COS']['M'] * 1e9 for r in runs]
        lt = [r['solve']['coils']['TX']['L'] * 1e9 for r in runs]
        planned = max(len(SETTINGS['angles_deg']), len(ang))
        full = len(ang) >= planned
        fs, fc = (fit(ang, ms), fit(ang, mc)) if len(ang) >= 3 else (None, None)
        err = angle_error(ang, ms, mc, per)
        if fs:
            curves.append((gap, ang, ms, mc, fs, fc))
        so_far = '' if full else ' so far'
        summary.append(f"| {gap:g} mm | {len(ang)} of {planned} | "
                       + (f"{fs['amplitude']:.2f} / {fc['amplitude']:.2f} nH ({w * fs['amplitude']:.0f} / "
                          f"{w * fc['amplitude']:.0f} mV) |" if fs else '| ')
                       + (f" {err['rms']:.1f}° rms, {err['peak']:.1f}° peak{so_far} |" if err else ' |'))
        sec = [f'## {gap:g} mm air gap', '']
        png = f'{path.parent.name}/{path.with_suffix(".webp").name}'
        if path.with_suffix('.webp').exists() and fs:
            how = ('' if max(ang) - min(ang) >= 270 else ', drawn only between the solved angles while few '
                   'are in')
            sec += [f'![SIN and COS against the rotor angle at a {gap:g} mm air gap]({png})', '',
                    f"*Figure {i}. SIN (blue) and COS (orange) at a {gap:g} mm air gap: the mutual inductance from "
                    f"the TX against the rotor's angle, {len(ang)} of {planned} angles solved. Each dot is one "
                    f"Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each "
                    f"channel's best sine fit{how}, which is what the angle error is measured against. SIN swings "
                    f"±{fs['amplitude']:.2f} nH and COS ±{fc['amplitude']:.2f} nH, that is "
                    f"±{w * fs['amplitude']:.0f} and ±{w * fc['amplitude']:.0f} mV of EMF.*", '']
            line = (f"Best sine fit: SIN amplitude {fs['amplitude']:.3f} nH, offset {fs['offset']:.3f} nH, phase "
                    f"{fs['phase_deg']:.1f}°; COS amplitude {fc['amplitude']:.3f} nH, offset {fc['offset']:.3f} nH, "
                    f"phase {fc['phase_deg']:.1f}°.")
            if err:
                line += (f" Angle error{so_far}, with the offset and gain of each channel calibrated out (worked out "
                         f"as below): {err['rms']:.1f}° rms and {err['peak']:.1f}° at worst, in electrical "
                         f"degrees{deg}. SIN and COS are {err['sin_to_cos_deg']:.1f}° apart, against 90° for perfect "
                         "quadrature.")
            sec += [line, '']
        elif not runs:
            sec += ['The first angle is solving; the curves appear here as the angles finish.', '']
        rows = ['| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | '
                'Memory | Time |', '|---|---|---|---|---|---|---|---|---|---|']
        for r in away + runs:
            s, c = r['solve'], r['solve']['coils']
            e = err['per_angle'].get(float(r['rotor_deg'])) if err and r['rotor_deg'] != 'away' else None
            rows.append(f"| {'away' if r['rotor_deg'] == 'away' else format(r['rotor_deg'], 'g') + '°'} | "
                        f"{c['SIN']['M'] * 1e9:.4f} | {c['COS']['M'] * 1e9:.4f} | "
                        f"{'' if e is None else f'{e:+.2f}°'} | {c['TX']['L'] * 1e9:.3f} | "
                        f"{c['TX']['R'] * 1e3:.2f} | {solve_cell(s)} | {checks_cell(s)} | "
                        f"{s['peak_memory_gb']:.1f} GB | {time_cell(s['seconds'])} |")
        if len(rows) > 2:
            sec += rows + ['']
        loose = [r for r in runs if not charts.readable(r['solve'])]
        if loose:
            sec += [f"**Not readable:** {len(loose)} of {len(runs)} solves "
                    f"({', '.join(format(r['rotor_deg'], 'g') + '°' for r in loose)}) did not converge, give the TX "
                    f"a negative resistance, or an L from its port more than {AGREE * 100:g} % away from the L in the "
                    "field's energy (or, where SIN and COS were driven too, an M from the TX more than "
                    f"{AGREE * 100:g} % away from the M back to it). Read this gap's curve with that in mind.", '']
        sections.append('\n'.join(sec))
        lt_all.append((gap, lt, [r['solve']['coils']['TX']['L'] * 1e9 for r in away]))
    boards_dir = BOARD / 'Boards'
    pic = next((p.name for p in [BOARD / f'{BOARD.name}_stator_and_rotor.webp'] if p.exists()), None)  # beside README
    if not pic:                                                                   # else the generator's own picture
        pic = next(('Boards/' + p.name for p in sorted(boards_dir.glob('*_Representative.svg'))), None)
    tx, rs, rc = (SPEC['terminals'][k] for k in ('TX', SIN_NET, COS_NET))
    xy = lambda t: '({:g}, {:g})'.format(*(round(v, 2) for v in (t['cut']['xy_kicad'] if RX_PORT == 'cut' and 'cut' in t
                                                                 else t.get('via_xy_kicad') or t.get('ends_xy_kicad'))))
    opened = 'by a cut in its top trace ' if RX_PORT == 'cut' else ''
    boards = ['## The boards', '']
    if pic:
        boards += [f'![stator and rotor](../{pic})', '']
    boards += [f"*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Palace, SIN is "
               f"opened {opened}at {xy(rs)} and COS at {xy(rc)}, the TX at its ends at {xy(tx)} (KiCad mm). The "
               f"[README](../README.md) has the board and how it was made.*", '']
    if (BOARD / f'{BOARD.name}_palace_setup.webp').exists():
        boards += [f'![how the stator and rotor are set up in Palace](../{BOARD.name}_palace_setup.webp)',
                   '', "*How the boards are set up in Palace, drawn by "
                   "[`rig_picture.py`](../Palace%20Simulation/rig_picture.py) from the geometry the mesh is built "
                   "from: the rotor copper side down over the stator, each receiver opened "
                   + ("by a 0.2 mm cut across a top trace (its lumped port, a sheet across the cut from one cut face "
                      "to the other, has 1 MΩ across it, so the voltage across the cut is the open-circuit EMF)"
                      if RX_PORT == 'cut' else
                      "at a left-out via (its lumped port, a sheet standing between the via's two pads, has 1 MΩ "
                      "across it, so the voltage across it is the open-circuit EMF)")
                   + ", and the TX opened between its two stacked ends, where its port drives it.*", '']
    expect = []
    tx_exp = EXPECTED.get('tx', {})
    if tx_exp.get('L_away_gen_H') and lt_all:
        got = []
        aw = next((a[0] for _, _, a in lt_all if a), None)
        if aw:
            got.append(f'{aw:.1f} nH with the rotor away')
        for gap, lt, _ in lt_all:
            if lt:
                got.append(f'{min(lt):.1f} to {max(lt):.1f} nH with the rotor at {gap:g} mm')
        expect = ['## Against the expectation', '',
                  f"The generator estimates the TX at {tx_exp['L_away_gen_H'] * 1e9:.0f} nH with the rotor away and "
                  f"{tx_exp['L_rotor_gen_H'] * 1e9:.0f} nH with it (its drop with the rotor is an upper estimate). "
                  "Palace gives " + ', and '.join(got) + '. The expected values are in '
                  '[expected_results.json](expected_results.json).', '']
    method = ['## How the angle error is worked out', '', METHOD, '']
    text = '\n'.join([
        f'# {BOARD.name}: SIN and COS over the rotor\'s turn in Palace', '',
        f"A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-"
        f"Encoders-Coil-Generator): {2 * st['bore_and_outer_radius_mm'][1]:g} mm across, {len(st['layers'])} copper "
        f"layers, {'one electrical period' if n_per == 1 else f'{n_per} electrical periods'} per turn and {rotor}. The "
        f"TX is driven at {SETTINGS['freq_hz'] / 1e6:g} MHz; the curves are the mutual inductance from the TX to SIN "
        f"and to COS (1 nH is {w:.0f} mV of EMF for 1 A in the TX). Each angle is one Palace solve with its own mesh, "
        f"checked by working the TX's L out two ways: from its port's voltage, and from the magnetic energy in the "
        f"whole field (the Checks column gives how far apart they are; a solve is read when the linear solve "
        f"converged and the two are within {AGREE * 100:g} %). At the first angle of each gap SIN and COS are driven "
        f"too, and the M from each back to the TX is checked against the M from the TX to it (reciprocity, in the "
        f"same column). This page is rewritten by `simulation.py` after every solve.", '',
        '| Air gap | Angles solved | Amplitude SIN / COS | Angle error |', '|---|---|---|---|', *summary, '',
        *sections, *gaps_section(curves, [p for _, p in gaps], len(sections) + 1), *expect, *method, *boards])
    (RESULTS / 'SINCOS_Results.md').write_text(text)
    log('wrote SINCOS_Results.md')


def solve_cell(s):
    """How a solve was done, for the tables: the iterations (of each excitation) and the residual it stopped at."""
    its = s.get('iterations') or []
    if not its:
        return 'direct'
    res = max((r for r in s.get('residuals') or [] if r is not None), default=None)
    out = ' + '.join(str(i) for i in its) + ' iterations' + ('' if res is None else f', {res:.0e}')
    return out if s.get('converged', True) else out + ', **not converged**'


def checks_cell(s):
    """How far the TX's L from its port is from L from the field energy, and where SIN and COS were driven too, how
    far the M from the TX is from the M back to it (as a part of the larger receiver's M)."""
    tx, lw = s['coils']['TX'], s.get('L_from_energy_h')
    out = 'not checked' if lw is None else f"L {round(100 * (tx['L'] - lw) / lw, 3) + 0.0:+.3f} %"
    if s.get('reciprocity'):
        worst = max(s['reciprocity'].values())
        out += f', reciprocity {100 * worst:.2g} %'
    return out


def time_cell(secs):
    return f'{secs:.0f} s' if secs < 120 else f'{secs / 60:.0f} min'


def gaps_section(curves, files, number):
    """With two air gaps or more solved, SINCOS_gaps.webp (make_charts.py) and its section for SINCOS_Results.md."""
    if len(curves) < 2 or not charts.gaps_chart(files):
        return []
    curves = sorted(curves, key=lambda c: c[0])
    (g0, *_, fs0, fc0), (g1, *_, fs1, fc1) = curves[0], curves[-1]
    return ['## The air gaps together', '', '![SIN and COS at each air gap](SINCOS_gaps.webp)', '',
            f"*Figure {number}. Every air gap on one chart, the {g0:g} mm gap in full colour, the solves of each joined "
            f"by a solid line, and each gap's ideal sine and cosine dotted. Going from {g1:g} to {g0:g} mm makes "
            f"SIN {fs0['amplitude'] / fs1['amplitude']:.2f} "
            f"times and COS {fc0['amplitude'] / fc1['amplitude']:.2f} times larger.*", '']


def plot(res_file, log=print):
    """The table, the fit and the angle error of one results file, its chart (make_charts.py) and the page."""
    result = json.loads(res_file.read_text())
    runs = sorted((r for r in result['runs'] if r['rotor_deg'] != 'away'), key=lambda r: r['rotor_deg'])
    if not runs:
        return
    ang = [r['rotor_deg'] for r in runs]
    msin = [r['solve']['coils']['SIN']['M'] * 1e9 for r in runs]
    mcos = [r['solve']['coils']['COS']['M'] * 1e9 for r in runs]
    ltx = [r['solve']['coils']['TX']['L'] * 1e9 for r in runs]
    stem = res_file.with_suffix('')
    with open(f'{stem}.csv', 'w') as f:
        f.write('rotor_deg,M_SIN_nH,M_COS_nH,L_TX_nH,EMF_SIN_mV,EMF_COS_mV\n')
        w = 2 * math.pi * SETTINGS['freq_hz']
        for a, s, c, lt in zip(ang, msin, mcos, ltx, strict=True):
            f.write(f'{a:g},{s:.5f},{c:.5f},{lt:.5f},{w * s * 1e-6:.4f},{w * c * 1e-6:.4f}\n')
    fits = {'SIN': fit(ang, msin), 'COS': fit(ang, mcos)}
    result['fit_nH'] = fits
    result['angle_error_deg'] = angle_error(ang, msin, mcos, SETTINGS['period_deg'])
    res_file.write_text(json.dumps(result, indent=1))
    charts.gap_chart(res_file)
    log(f'wrote {stem.name}.csv and {stem.name}.webp; fit (nH): ' + '; '.join(
        f"{k} amplitude {v['amplitude']:.3f}, offset {v['offset']:.3f}, phase {v['phase_deg']:.1f} deg"
        + (f", rms left {v['rms_left']:.4f}" if v['rms_left'] is not None else '') for k, v in fits.items()))
    report(log)


def solver_key(result):
    """What makes two solves alike: the mesh level, the element order and the linear solver's settings."""
    d = result.get('solver') or {}
    return json.dumps(dict(level=result.get('level'), order=d.get('order'), linear=d.get('linear')), sort_keys=True)


def merge(res_file, others, log=print):
    """Add the solves of other results files of the same gap (say, some angles each from machines run in parallel)
    to res_file, then redraw. An angle already in res_file keeps its solve; a file with another gap, port, mesh or
    solver setting is refused, so that only like solves share a curve."""
    result = json.loads(res_file.read_text()) if res_file.exists() else None
    same = ('gap_mm', 'rx_port')
    for f in others:
        other = json.loads(f.read_text())
        if result is None:
            result = dict(other, runs=[])
        bad = [k for k in same if other.get(k) != result.get(k)]
        if bad or solver_key(other) != solver_key(result):
            log(f'{f.name}: not merged, its ' + (', '.join(bad) or 'mesh or solver setting') + ' differs')
            continue
        if other.get('versions', {}).get('palace') != result.get('versions', {}).get('palace'):
            log(f"{f.name}: Palace {other.get('versions', {}).get('palace')} against "
                f"{result.get('versions', {}).get('palace')} here; merged, but say so")
        have = {r['rotor_deg'] for r in result['runs']}
        new = [r for r in other['runs'] if r['rotor_deg'] not in have]
        result['runs'] += new
        log(f'{f.name}: added ' + (', '.join(str(r['rotor_deg']) for r in new) or 'nothing new'))
    if result is None:
        return
    result['runs'].sort(key=lambda r: -1 if r['rotor_deg'] == 'away' else r['rotor_deg'])
    res_file.parent.mkdir(parents=True, exist_ok=True)
    res_file.write_text(json.dumps(result, indent=1))
    plot(res_file, log)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--angles', type=float, nargs='*', default=None)
    ap.add_argument('--step', type=float, default=None, help='every STEP degrees over the whole turn')
    ap.add_argument('--gap', type=float, default=SETTINGS['air_gap_mm'], help='air gap, copper to copper (mm)')
    ap.add_argument('--no-away', action='store_true', help='skip the run with the rotor away')
    ap.add_argument('--level', type=float, default=SETTINGS['level'], help="divides the copper's mesh sizes")
    ap.add_argument('--solver', default=SETTINGS['solver'], choices=sorted(SETTINGS['solvers']),
                    help="the linear solver's settings, by name in SETTINGS['solvers']")
    ap.add_argument('--reciprocity', default=SETTINGS['reciprocity'], choices=('first', 'all', 'none'),
                    help='where SIN and COS are driven too, to check reciprocity (three solves in one)')
    ap.add_argument('--ranks', type=int, default=SETTINGS['ranks'], help='MPI ranks per solve')
    ap.add_argument('--jobs', type=int, default=SETTINGS['jobs'], help='solves at once, each on RANKS ranks')
    ap.add_argument('--mesh', action='append', default=[], metavar='KEY=VALUE',
                    help="change one of SETTINGS['mesh'] (a trial, kept in case/), e.g. grade=0.25")
    ap.add_argument('--port-segment', type=float, default=None,
                    help='draw each port line into the mesh in pieces at most this long (mm)')
    ap.add_argument('--trial', default='', help='a name for a trial setting: its results stay in case/')
    ap.add_argument('--mesh-only', action='store_true', help='build the meshes and say their size, solve nothing')
    ap.add_argument('--plot', action='store_true', help='only redraw the table and the curves')
    ap.add_argument('--merge', nargs='+', metavar='JSON', default=None,
                    help="other machines' results files of this gap: their solves are added to this gap's results")
    ap.add_argument('--out', default=str(HERE / 'case'))
    a = ap.parse_args()
    changed = ''
    for kv in a.mesh:
        k, v = kv.split('=')
        if k not in SETTINGS['mesh']:
            ap.error(f"--mesh {k}: not one of {sorted(SETTINGS['mesh'])}")
        SETTINGS['mesh'][k] = float(v)
        changed += f'_{k}{float(v):g}'
    if a.port_segment:
        SETTINGS['port_segment_mm'] = a.port_segment
        changed += f'_portseg{a.port_segment:g}'
    tagg = (f'gap{a.gap:g}mm' + ('' if a.level == SETTINGS['level'] else f'_level{a.level:g}') + changed
            + ('' if a.solver == SETTINGS['solver'] else f'_{a.solver}') + (f'_{a.trial}' if a.trial else ''))
    trial = tagg != f'gap{a.gap:g}mm'                   # another mesh or solver setting: a trial, kept in case/
    res_file = (Path(a.out) if trial else RESULTS / gap_folder(a.gap)) / f'results_{tagg}.json'
    if not (a.mesh_only or a.plot):
        res_file.parent.mkdir(parents=True, exist_ok=True)
    if a.merge:
        merge(res_file, [Path(f) for f in a.merge])
        return
    if a.plot:
        plot(res_file)
        return
    if a.angles is not None:
        angles = list(a.angles)
    elif a.step:
        angles = [float(x) for x in np.arange(0.0, 360.0 - 1e-9, a.step)]
    else:
        angles = [float(x) for x in SETTINGS['angles_deg']]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / 'run.log', 'a')
    lock, mesh_lock = threading.Lock(), threading.Lock()

    def log(msg):
        with lock:
            print(msg, flush=True)
            logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
            logf.flush()
    se = S.kese_geometry(BOARD / SETTINGS['stator'], GEOMETRY, log=log)   # exported again only if the board changed
    re_ = S.kese_geometry(BOARD / SETTINGS['rotor'], GEOMETRY, log=log)
    result = json.loads(res_file.read_text()) if res_file.exists() else dict(
        board=BOARD.name, gap_mm=a.gap, level=a.level, rx_port=RX_PORT, settings=SETTINGS, expected=EXPECTED,
        solver=dict(kind=a.solver.upper(), order=SETTINGS['order'],
                    linear=SETTINGS['solvers'][a.solver], palace_bin=in_repo(C.palace_exe())),
        versions=S.versions((se, re_)), runs=[])
    result['model'] = dict(label=model_label(result))
    done = {r['rotor_deg'] for r in result['runs']}
    checked = any(r['solve'].get('reciprocity') for r in result['runs'])
    todo = []
    for angle in ([] if a.no_away else [None]) + angles:
        key = 'away' if angle is None else angle
        if key in done and not a.mesh_only:
            log(f'{key}: already in {res_file.name}, skipped')
            continue
        recip = a.reciprocity == 'all' or (a.reciprocity == 'first' and angle is not None and not checked)
        checked = checked or recip
        todo.append((angle, recip))

    def one(angle, recip):
        tag = 'away' if angle is None else f'rotor{angle:g}'
        t0 = time.time()
        with mesh_lock:                                  # gmsh, which the mesher calls, runs one mesh at a time
            m, bnds, directions = build(se, re_, angle, a.gap, a.level, log)
        mesh = dict(seconds=round(time.time() - t0, 1), nodes=len(m['nodes']), wedges=len(m['wedges']),
                    tetrahedra=len(m['tets']), triangles=int(m['nt']), layers=int(m['nk']))
        log(f'{tag}: mesh {mesh}')
        folder = out / f'{tagg}_{tag}'
        if a.mesh_only:
            return angle, mesh, None
        return angle, mesh, solve(m, bnds, directions, folder, a.solver, a.ranks, recip, log=log, tag=tag)

    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as pool:
        for fut in as_completed([pool.submit(one, angle, recip) for angle, recip in todo]):
            angle, mesh, row = fut.result()
            if row is None:
                continue
            key = 'away' if angle is None else angle
            tag = 'away' if angle is None else f'rotor{angle:g}'
            result['runs'] = [r for r in result['runs'] if r['rotor_deg'] != key]
            result['runs'].append(dict(rotor_deg=key, mesh=mesh, solve=row))
            result['runs'].sort(key=lambda r: -1 if r['rotor_deg'] == 'away' else r['rotor_deg'])
            res_file.write_text(json.dumps(result, indent=1))
            c = row['coils']
            log(f"{tag}: L_TX {c['TX']['L'] * 1e9:.3f} nH (energy {(row['L_from_energy_h'] or math.nan) * 1e9:.3f}), "
                f"R_TX {c['TX']['R'] * 1e3:.2f} mOhm, M_SIN {c['SIN']['M'] * 1e9:.4f} nH, M_COS "
                f"{c['COS']['M'] * 1e9:.4f} nH, iterations {row['iterations']}, converged {row['converged']}, "
                + (f"reciprocity {max(row['reciprocity'].values()):.1e}, " if row.get('reciprocity') else '')
                + f"{row['peak_memory_gb']} GB, {row['seconds']} s")
            plot(res_file, log)
    if not a.mesh_only:
        log(f'wrote {res_file}')


def in_repo(path):
    """A path inside the repository relative to its root, so the results name no machine's folders."""
    p, root = Path(path).resolve(), HERE.parents[3]
    return str(p.relative_to(root)) if p.is_relative_to(root) else str(path)


if __name__ == '__main__':
    main()
