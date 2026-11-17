"""A coil set from the Sinusoidal Coil Generator in Elmer: the SIN and COS curves against the rotor's angle, at any
air gap. Everything that belongs to the board is in test_spec.json beside this file, so the same script runs every
single-set board that new_coil.py sets up; the board's README, one folder up, says what this board is. A board folder
holds Boards/ (straight from the generator), Elmer Simulation/ (this script, test_spec.json, angle_error.py and the
runs under case/) and Results/ (what the runs give, and what was expected).

    python simulation.py                          the rotor away, then every angle in test_spec.json
    python simulation.py --gap 0.5                the same at a 0.5 mm air gap (copper to copper)
    python simulation.py --angles 0 90 --no-away  the rotor at 0 and 90 degrees only
    python simulation.py --step 10                every 10 degrees over the whole turn
    python simulation.py --plot                   only redraw the curves from the results already written
    python simulation.py --angles 0 --mesh-only   build one mesh and say its size, to judge the memory
    python simulation.py --solver iterative       the iterative solve (GCR) instead of the direct one: less memory,
                                                  but on the S0 boards at 3.5 MHz it converges too slowly to read M
    python simulation.py --gap 0.5 --merge a.json b.json
                                                  add the solves in results files from other machines (each one
                                                  ran some angles of this gap) to this gap's results, and redraw

The TX carries 1 A; SIN and COS carry none, so their voltages are the EMFs the TX induces in them, given as mutual
inductances (EMF = 2 pi f M x 1 A: 1 nH is 22 mV at 3.5 MHz). The rotor repeats itself every 360 / sectors degrees,
so the curves are drawn over that span: a full turn on a one-sector rotor.

Every angle gets its own mesh, the rotor's copper at that angle drawn into it. The stator's mesh then differs a
little between angles, which shows as small noise on the curves; the fit written with the results says how much.

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
import time
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Point, Polygon

HERE = Path(__file__).resolve().parent              # <board>/Elmer Simulation
BOARD = HERE.parent                                 # <board>: README.md, Boards/, Elmer Simulation/, Results/
RESULTS = BOARD / 'Results'
GEOMETRY = BOARD / '3D_Geometry'                     # KESE's export of each board, kept in the repo
sys.path.insert(0, str(HERE.parents[3]))
sys.path.insert(0, str(HERE))
from angle_error import METHOD, angle_error, gap_folder, results_files, sine_fit   # noqa: E402
import make_charts as charts   # noqa: E402
from bridge import elmer_case as E, geometry as G, mesh25d as M, ports as P, study as S   # noqa: E402

SPEC = json.loads((HERE / 'test_spec.json').read_text())
EXPECTED = (json.loads((RESULTS / 'expected_results.json').read_text())
            if (RESULTS / 'expected_results.json').exists() else {})
AXIS = (100.0, -100.0)                 # KiCad (100, 100) in model coordinates, y up


def model_xy(xy_kicad):
    """KiCad (x, y) to model (x, y), on the mesher's 0.5 um grid so that a sheet's line lands on mesh edges."""
    return round(xy_kicad[0] * 2000) / 2000, round(-xy_kicad[1] * 2000) / 2000


SET = SPEC['sets'][0]
SIN_NET, COS_NET = str(SET['sin']), str(SET['cos'])
AGREE = charts.AGREE   # how far the TX's L and R from its voltage may be from the field energy's and the eddy
                       # power's for a solve to be read (make_charts.readable)
SETTINGS = dict(
    stator=SPEC['files']['stator'],    # paths from the board folder
    rotor=SPEC['files']['rotor'],
    names={str(k): v for k, v in SPEC['nets'].items()},   # KESE's copper part per net -> the coil's name
    sigma=5.8e7,
    freq_hz=SET['f_Hz'],
    air_gap_mm=SPEC['air_gap_mm'],     # stator F.Cu top to rotor copper face; --gap sets another
    insulators=False,                  # FR-4 and mask are air to the magneto-quasi-static solve
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
    sheet_half_mm=0.8 * SPEC['terminals']['TX'].get('end_radius_mm', 0.1),    # half a TX sheet's line
    rx_sheet_half_mm=0.25 / 0.3 * SPEC['terminals'][SIN_NET].get('void_radius_mm', 0.3),   # half an RX sheet's
    level=SPEC.get('mesh_level', 0.25),   # the copper's mesh sizes divided by this (S2's checks used 1.0)
    mesh=dict(h_edge=0.1, h_in=0.2, h_max=6.0, grade=0.5, dz_copper=0.018, dz_max=0.4,
              tet_max=8.0, tet_grade=0.7),
    threads=4,
    tol=1e-7,
    max_iter=1500,
    solver='mumps',                    # a direct solve (serial MUMPS), exact: 2 to 5 min and 13 to 25 GB a solve at level
                                       # 0.25 (more at wider gaps; past about 13 GB a swap file); 'iterative' (GCR) needs
                                       # less memory but converges too slowly on these boards at 3.5 MHz to read M
    method='GCR',                      # GCR(50) falls slowly but steadily; BiCGStabL wanders on these boards
    ilu_order=1,                       # ILU(1) of the field under the circuit preconditioner; None leaves every
                                       # field row bare (the circuit preconditioner alone), ten times slower here
    ilu_factor=0.1,                    # the ILU factors the matrix with its diagonal times 1.1: the air's curl-curl
                                       # block is singular, and an unshifted ILU of it breaks down on tiny pivots
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


def cut_box(name):
    """The cut across SIN's or COS's top trace (model coordinates): gap_mm along the trace, wider than it."""
    c = SETTINGS['rx_cuts'][name]
    d = np.asarray(c['along'], float) / np.linalg.norm(c['along'])
    n = np.array([-d[1], d[0]])
    o, hl, hw = np.asarray(c['xy']), c['gap_mm'] / 2, c['half_width_mm']
    return Polygon([o - hl * d - hw * n, o + hl * d - hw * n, o + hl * d + hw * n, o - hl * d + hw * n])


def top_copper(stator, name):
    """The z span of a coil's top copper (F.Cu)."""
    lo, hi = next(p.zrange for p in stator if p.body == name)
    lv = sorted({z for p in stator if p.body == name for z in p.levels()})
    return max(z for z in lv if lo < z < hi), hi


def voids(stator):
    """Air parts (priority over copper) that open SIN and COS: each RX via's barrel left out through the dielectric,
    or with RX_PORT 'cut', a gap cut through the top copper of each."""
    out = []
    if RX_PORT == 'cut':
        for name in ('SIN', 'COS'):
            out.append(M.Part(name=f'{name}_cut', body='AIR', role='void', priority=4,
                              fixed={top_copper(stator, name): cut_box(name)}))
        return out
    for name, xy in SETTINGS['rx_vias'].items():
        lo, hi = next(p.zrange for p in stator if p.body == name)
        lv = sorted({z for p in stator if p.body == name for z in p.levels()})
        inner = [z for z in lv if lo < z < hi]           # the dielectric's span between the two coppers
        disc = Point(xy).buffer(SETTINGS['via_void_radius_mm'], 64)
        out.append(M.Part(name=f'{name}_via_void', body='AIR', role='void', priority=4,
                          fixed={(min(inner), max(inner)): disc}))
    return out


def coil_zrange(lay, body):
    zs = [z for p in lay.parts if p.body == body for z in p.zrange]
    return min(zs), max(zs)


def build(stator_export, rotor_export, angle, gap, level, log=print):
    """The mesh with the rotor at `angle` (degrees, KiCad's sense), or away (None: its copper made air), and the
    terminals' boundaries."""
    st = SETTINGS['mesh']
    stator = stator_parts(stator_export)
    rot = rotor_parts(rotor_export, 0.0 if angle is None else angle, gap, body='AIR' if angle is None else 'ROTOR')
    top = max(z for p in rot for z in p.zrange)
    bottom = min(z for p in stator for z in p.zrange)
    zbox = (bottom - SETTINGS['domain_margin_mm'], top + SETTINGS['domain_margin_mm'])
    lay = M.Layout(stator + voids(stator) + rot, M.disc(AXIS, SETTINGS['domain_radius_mm'], h=st['h_max']),
                   zbox).build(log=log, insulators=SETTINGS['insulators'])
    sheets = {}
    tx = SETTINGS['tx_end']
    h = SETTINGS['sheet_half_mm']
    sheets['TX'] = LineString([(tx[0] - h, tx[1]), (tx[0] + h, tx[1])])
    for name, xy in SETTINGS['rx_vias'].items():
        h2 = SETTINGS['rx_sheet_half_mm']
        if RX_PORT == 'via':
            sheets[name] = LineString([(xy[0] - h2, xy[1]), (xy[0] + h2, xy[1])])
    s = dict(st)
    for k in ('h_edge', 'h_in', 'dz_copper'):
        s[k] = st[k] / level
    cuts = ([LineString(cut_box(n).exterior.coords) for n in ('SIN', 'COS')] if RX_PORT == 'cut' else [])
    m = M.build_mesh(lay, M.Settings(**s), extra_lines=list(sheets.values()) + cuts, log=log)   # cuts: drawn in
    t, tp, q, qp = M.outer_faces(m)
    bnds = [('OUTER', t, tp, q, qp)]
    for name in ('TX', 'SIN', 'COS'):
        k = m['names'].index(name)
        if name != 'TX' and RX_PORT == 'cut':           # E01's port: the two cut faces, the sheet across the gap's floor
            box = cut_box(name)
            f0, f1 = top_copper([p for p in lay.parts if p.role != 'void'], name)
            e1, e2 = P.electrodes(m, k, box, f0, f1)
            ts, tsp = P.sheet_at_level(m, box, f0)
            bnds += [(f'{name}_T1', *e1), (f'{name}_T2', *e2), (f'{name}_SHEET', ts, tsp, q[:0], qp[:0])]
            log(f'{name}: cut electrodes {len(e1[0]) + len(e1[2])} and {len(e2[0]) + len(e2[2])} faces, sheet '
                f'{len(ts)} faces at z {f0:.4f}')
            continue
        if name == 'TX':
            hole = Point(tx).buffer(SETTINGS['tx_end_radius_mm'], 32)
        else:
            hole = Point(SETTINGS['rx_vias'][name]).buffer(SETTINGS['via_void_radius_mm'], 64)
        lo, hi = coil_zrange(lay, name)
        lv = sorted({z for p in lay.parts if p.body == name for z in p.levels()})
        inner = [z for z in lv if lo < z < hi]
        b0, b1 = min(inner), max(inner)                   # the faces of the copper toward the dielectric
        e1, e2 = P.electrodes(m, k, hole, b0, b1)
        qs, qsp = M.vertical_faces(m, b0, b1, sheets[name], tol=1e-4)
        bnds += [(f'{name}_T1', *e1), (f'{name}_T2', *e2), (f'{name}_SHEET', t[:0], tp[:0], qs, qsp)]
        log(f'{name}: electrodes {len(e1[0]) + len(e1[2])} and {len(e2[0]) + len(e2[2])} faces, sheet {len(qs)} '
            f'faces, z {b0:.4f} to {b1:.4f}')
    return m, bnds


def fit(angles, values):
    """The best sine over the rotor's period (angle_error.sine_fit): offset, amplitude, phase and the rms left."""
    return sine_fit(angles, values, SETTINGS['period_deg'])


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
                    f"the TX against the rotor's angle, {len(ang)} of {planned} angles solved. Each dot is one Elmer "
                    f"solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each "
                    f"channel's best sine fit{how}, which is what the angle error is measured against. SIN swings "
                    f"±{fs['amplitude']:.2f} nH and COS ±{fc['amplitude']:.2f} nH, that is "
                    f"±{w * fs['amplitude']:.0f} and ±{w * fc['amplitude']:.0f} mV of EMF.*", '']
            line = (f"Best sine fit: SIN amplitude {fs['amplitude']:.3f} nH, offset {fs['offset']:.3f} nH, phase "
                    f"{fs['phase_deg']:.1f}°; COS amplitude {fc['amplitude']:.3f} nH, offset {fc['offset']:.3f} nH, "
                    f"phase {fc['phase_deg']:.1f}°.")
            if err:
                line += (f" Angle error{so_far}, with the offset and gain of each channel calibrated out (worked out as below): "
                         f"{err['rms']:.1f}° rms and {err['peak']:.1f}° at worst, in electrical degrees{deg}. SIN and "
                         f"COS are {err['sin_to_cos_deg']:.1f}° apart, against 90° for perfect quadrature.")
            sec += [line, '']
        elif not runs:
            sec += ['The first angle is solving; the curves appear here as the angles finish.', '']
        rows = ['| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | '
                'Memory | Time |', '|---|---|---|---|---|---|---|---|---|---|']
        for r in away + runs:
            s, c = r['solve'], r['solve']['coils']
            e = err['per_angle'].get(float(r['rotor_deg'])) if err and r['rotor_deg'] != 'away' else None
            rows.append(f"| {'away' if r['rotor_deg'] == 'away' else format(r['rotor_deg'], 'g') + '°'} | "
                        f"{c['SIN']['M'] * 1e9:.4f} | {c['COS']['M'] * 1e9:.4f} | "
                        f"{'' if e is None else f'{e:+.2f}°'} | {c['TX']['L'] * 1e9:.3f} | "
                        f"{c['TX']['R'] * 1e3:.2f} | {solve_cell(s)} | {checks_cell(s)} | "
                        f"{s['peak_memory_gb']:.1f} GB | {s['seconds'] / 60:.0f} min |")
        if len(rows) > 2:
            sec += rows + ['']
        capped = [r for r in runs if (r['solve']['iterations'] or 0) >= SETTINGS['max_iter']]
        if capped and len(lt) >= 2:
            res_ = [r['solve']['residual'] for r in capped]
            sec += [f"{len(capped)} of {len(runs)} solves stopped at the {SETTINGS['max_iter']}-iteration cap, with "
                    f"the residual between {min(res_):.1e} and {max(res_):.1e} rather than the {SETTINGS['tol']:.0e} "
                    f"asked for. The TX is round, so turning the rotor should not change its inductance: its spread "
                    f"here, {min(lt):.1f} to {max(lt):.1f} nH, is a measure of what the solver leaves.", '']
        loose = [r for r in runs if not charts.readable(r['solve'])]
        if loose:
            sec += [f"**Not converged enough to read:** {len(loose)} of {len(runs)} solves "
                    f"({', '.join(format(r['rotor_deg'], 'g') + '°' for r in loose)}) give the TX a negative "
                    f"resistance, or an L or R from its voltage more than {AGREE * 100:g} % away from the L from the field "
                    f"energy or the R from the eddy power (solves from before those checks: a residual above "
                    f"{charts.LOOSE:.0e}). Read this gap's curve with that in mind.",
                    '']
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
    boards += [f"*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is "
               f"opened {opened}at {xy(rs)} and COS at {xy(rc)}, the TX at its ends at {xy(tx)} (KiCad mm). The "
               f"[README](../README.md) has the board and how it was made.*", '']
    if (BOARD / f'{BOARD.name}_elmer_setup.webp').exists():
        boards += [f'![how the stator and rotor are set up in Elmer](../{BOARD.name}_elmer_setup.webp)',
                   '', "*How the boards are set up in Elmer, drawn by "
                   "[`rig_picture.py`](../Elmer%20Simulation/rig_picture.py) from the geometry the mesh is built "
                   "from: the rotor copper side down over the stator, each receiver opened "
                   + ("by a 0.2 mm cut across a top trace (the two cut faces are the terminal, held at 0 A, so the "
                      "voltage across the cut is the open-circuit EMF)" if RX_PORT == 'cut' else
                      "at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so "
                      "the voltage across it is the open-circuit EMF)")
                   + ", and the TX opened between its two stacked ends, where 1 A is driven.*", '']
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
                  f"{tx_exp['L_rotor_gen_H'] * 1e9:.0f} nH with it (its drop with the rotor is an upper estimate). Elmer "
                  "gives "
                  + ', and '.join(got) + '. The expected values are in '
                  '[expected_results.json](expected_results.json).', '']
    method = ['## How the angle error is worked out', '', METHOD, '']
    text = '\n'.join([
        f'# {BOARD.name}: SIN and COS over the rotor\'s turn in Elmer', '',
        f"A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-"
        f"Encoders-Coil-Generator): {2 * st['bore_and_outer_radius_mm'][1]:g} mm across, {len(st['layers'])} copper "
        f"layers, {'one electrical period' if n_per == 1 else f'{n_per} electrical periods'} per turn and {rotor}. The TX carries 1 A at "
        f"{SETTINGS['freq_hz'] / 1e6:g} MHz; the curves are the mutual inductance from the TX to SIN and to COS "
        f"(1 nH is {w:.0f} mV of EMF). Each angle is one Elmer solve with its own mesh, checked by working the TX's L "
        f"and R out two ways: from its voltage, and from the field energy and the eddy power (the L and R checks in "
        f"each table give how far apart they are; a solve is read when both are within {AGREE * 100:g} %). This page is "
        f"rewritten by `simulation.py` after every solve.", '',
        '| Air gap | Angles solved | Amplitude SIN / COS | Angle error |', '|---|---|---|---|', *summary, '',
        *sections, *gaps_section(curves, [p for _, p in gaps], len(sections) + 1), *expect, *method, *boards])
    (RESULTS / 'SINCOS_Results.md').write_text(text)
    log('wrote SINCOS_Results.md')


def in_repo(path):
    """A path inside the repository relative to its root, so the results name no machine's folders."""
    p, root = Path(path).resolve(), HERE.parents[3]
    return str(p.relative_to(root)) if p.is_relative_to(root) else str(path)


def solve_cell(s):
    """How a solve was done, for the tables: direct, or the iterations and the residual it stopped at."""
    if s['iterations'] is None:
        return 'direct'
    return f"{s['iterations']} iterations" + ('' if s['residual'] is None else f", {s['residual']:.1e}")


def checks_cell(s):
    """How far the TX's L and R from its voltage are from L from the field energy and R from the eddy power, in %."""
    tx, lw, rp = s['coils']['TX'], s.get('L_from_energy_h'), s.get('R_from_power_ohm')
    if lw is None or rp is None:
        return 'not checked'
    dl, dr = (round(100 * (x - y) / y, 3) + 0.0 for x, y in ((tx['L'], lw), (tx['R'], rp)))   # + 0.0: no -0.000
    return f"L {dl:+.3f} %, R {dr:+.3f} %"


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
    """What makes two solves alike: iterative or direct, the Krylov method and its settings and any extra solver
    lines (not where Elmer is installed)."""
    d = result.get('solver') or {}
    return (d.get('kind', 'iterative'), d.get('method', 'BiCGStabL'), d.get('degree', 4),   # older files: iterative,
            d.get('restart', 50),                                                            # BiCGStabL
            d.get('max_iter', SETTINGS['max_iter']), tuple(d.get('lines', [])))


def merge(res_file, others, log=print):
    """Add the solves of other results files of the same gap (say, one angle each from machines run in parallel) to
    res_file, then redraw. An angle already in res_file keeps its solve; a file with another gap, mesh level or
    solver setting is refused, so that only like solves share a curve."""
    result = json.loads(res_file.read_text()) if res_file.exists() else None
    same = ('gap_mm', 'level', 'ilu_order', 'rx_port')
    for f in others:
        other = json.loads(f.read_text())
        if result is None:
            result = dict(other, runs=[])
        dflt = dict(rx_port='via')                       # results from before rx_port was recorded
        bad = [k for k in same if other.get(k, dflt.get(k)) != result.get(k, dflt.get(k))]
        if bad or solver_key(other) != solver_key(result):
            log(f'{f.name}: not merged, its ' + (', '.join(bad) or 'solver setting') + ' differs')
            continue
        if other.get('versions', {}).get('elmer') != result.get('versions', {}).get('elmer'):
            log(f"{f.name}: Elmer {other.get('versions', {}).get('elmer')} against "
                f"{result.get('versions', {}).get('elmer')} here; merged, but say so")
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
    ap.add_argument('--level', type=float, default=SETTINGS['level'])
    ap.add_argument('--ilu', type=int, default=SETTINGS['ilu_order'], help='ILU order for the preconditioner')
    ap.add_argument('--ilu-factor', type=float, default=SETTINGS['ilu_factor'],
                    help="the ILU's diagonal shift (Linear System ILU Factor)")
    ap.add_argument('--solver', default=SETTINGS['solver'], choices=('iterative', 'mumps'),
                    help='iterative (the Krylov method below) or mumps (a direct solve: exact, but needs the memory)')
    ap.add_argument('--method', default=SETTINGS['method'], choices=('BiCGStabL', 'GCR'), help='the Krylov method')
    ap.add_argument('--degree', type=int, default=4, help="BiCGStabL's polynomial degree")
    ap.add_argument('--restart', type=int, default=50, help="GCR's restart (it keeps twice this many vectors)")
    ap.add_argument('--max-iter', type=int, default=SETTINGS['max_iter'])
    ap.add_argument('--tree-gauge', action='store_true', help='gauge A with a spanning tree (Use Tree Gauge)')
    ap.add_argument('--sif', action='append', default=[], metavar='LINE',
                    help="another 'Keyword = value' line for the A-V solver (with --trial); repeat for more")
    ap.add_argument('--trial', default='', help='a name for a trial setting: its results stay in case/')
    ap.add_argument('--mesh-only', action='store_true', help='build and write the meshes, solve nothing')
    ap.add_argument('--plot', action='store_true', help='only redraw the table and the curves')
    ap.add_argument('--merge', nargs='+', metavar='JSON', default=None,
                    help="other machines' results files of this gap: their solves are added to this gap's results")
    ap.add_argument('--out', default=str(HERE / 'case'))
    a = ap.parse_args()
    tagg = (f'gap{a.gap:g}mm' + ('' if a.level == SETTINGS['level'] else f'_level{a.level:g}')
            + ('' if a.solver == SETTINGS['solver'] else f'_{a.solver}')
            + ('' if a.ilu == SETTINGS['ilu_order'] else f'_ilu{a.ilu}')
            + ('' if a.ilu_factor == SETTINGS['ilu_factor'] else f'_iluf{a.ilu_factor:g}')
            + ('' if a.method == SETTINGS['method'] else f'_{a.method.lower()}{a.restart}')
            + ('' if a.degree == 4 or a.method != 'BiCGStabL' else f'_deg{a.degree}')
            + ('' if a.max_iter == SETTINGS['max_iter'] else f'_it{a.max_iter}')
            + ('_tg' if a.tree_gauge else '') + (f'_{a.trial}' if a.trial else ''))
    if a.sif and not a.trial:
        ap.error('--sif needs --trial NAME, so its results are kept apart')
    lines = (['Use Tree Gauge = Logical True'] if a.tree_gauge else []) + a.sif
    trial = tagg != f'gap{a.gap:g}mm'                   # another level or solver setting: a trial, kept in case/
    res_file = (Path(a.out) if trial else RESULTS / gap_folder(a.gap)) / f'results_{tagg}.json'
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

    def log(msg):
        print(msg, flush=True)
        logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
        logf.flush()
    se = S.kese_geometry(BOARD / SETTINGS['stator'], GEOMETRY, log=log)   # exported again only if the board changed
    re_ = S.kese_geometry(BOARD / SETTINGS['rotor'], GEOMETRY, log=log)
    result = json.loads(res_file.read_text()) if res_file.exists() else dict(
        board=BOARD.name, gap_mm=a.gap, level=a.level, ilu_order=a.ilu, ilu_factor=a.ilu_factor, rx_port=RX_PORT,
        settings=SETTINGS, expected=EXPECTED,
        solver=dict(kind=a.solver, method=a.method, degree=a.degree, restart=a.restart, max_iter=a.max_iter,
                    lines=lines,
                    elmer_bin=in_repo(E.ELMER_BIN)),
        versions=S.versions(), runs=[])
    done = {r['rotor_deg'] for r in result['runs']}
    runs = ([] if a.no_away else [None]) + angles
    for angle in runs:
        key = 'away' if angle is None else angle
        if key in done and not a.mesh_only:
            log(f'{key}: already in {res_file.name}, skipped')
            continue
        tag = 'away' if angle is None else f'rotor{angle:g}'
        t0 = time.time()
        m, bnds = build(se, re_, angle, a.gap, a.level, log)
        mesh = dict(seconds=round(time.time() - t0, 1), nodes=len(m['nodes']), wedges=len(m['wedges']),
                    tetrahedra=len(m['tets']), triangles=int(m['nt']), layers=int(m['nk']))
        log(f'{tag}: mesh {mesh}')
        folder = out / f'{tagg}_{tag}'
        M.write_elmer(m, folder / 'mesh_files', bnds, log=log)
        if a.mesh_only:
            continue
        cu = E.Material('Copper', sigma=SETTINGS['sigma'])
        bodies = {n: (cu if n in ('TX', 'SIN', 'COS', 'ROTOR') else E.Material('Air' if n == 'AIR' else n.title()))
                  for n in m['names']}
        case = E.Case(mesh_dir=folder / 'mesh_files', bodies=bodies, order=1, tol=SETTINGS['tol'], solver=a.solver,
                      max_iter=a.max_iter, ilu_order=a.ilu, ilu_factor=a.ilu_factor, method=a.method,
                      bicg_degree=a.degree,
                      restart=a.restart, solver_lines=lines,
                      coils=[E.Coil('TX', 'TX', 'TX_T1', 'TX_T2', 'TX_SHEET', 1.0),
                             E.Coil('SIN', 'SIN', 'SIN_T1', 'SIN_T2', 'SIN_SHEET', 0.0),
                             E.Coil('COS', 'COS', 'COS_T1', 'COS_T2', 'COS_SHEET', 0.0)])
        rows = S.solve(case, [SETTINGS['freq_hz']], folder, threads=SETTINGS['threads'], log=log, tag=tag)
        result['runs'] = [r for r in result['runs'] if r['rotor_deg'] != key]
        result['runs'].append(dict(rotor_deg=key, mesh=mesh, solve=rows[0]))
        result['runs'].sort(key=lambda r: -1 if r['rotor_deg'] == 'away' else r['rotor_deg'])
        res_file.write_text(json.dumps(result, indent=1))
        c = rows[0]['coils']
        log(f"{tag}: L_TX {c['TX']['L'] * 1e9:.3f} nH, R_TX {c['TX']['R'] * 1e3:.2f} mOhm, "
            f"M_SIN {c['SIN']['M'] * 1e9:.4f} nH, M_COS {c['COS']['M'] * 1e9:.4f} nH, {rows[0]['iterations']} it, "
            f"res {rows[0]['residual']}, {rows[0]['peak_memory_gb']} GB, {rows[0]['seconds']} s")
        shutil.rmtree(folder / 'mesh_files', ignore_errors=True)       # the mesh is large; the results stay
        plot(res_file, log)
    if not a.mesh_only:
        log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
