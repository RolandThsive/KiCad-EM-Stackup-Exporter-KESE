"""A coil set from the Sinusoidal Coil Generator in PyPEEC: the SIN and COS curves against the rotor's angle, at any
air gap. Everything that belongs to the board is in test_spec.json beside this file, so the same script runs every
single-set board that new_coil.py sets up; the board's README, one folder up, says what this board is. A board folder
holds Boards/ (straight from the generator), PyPEEC Simulation/ (this script, test_spec.json, angle_error.py and the
runs under case/) and Results/ (what the runs give, and what was expected).

    python simulation.py                          the rotor away, then every angle in test_spec.json
    python simulation.py --gap 0.5                the same at a 0.5 mm air gap (copper to copper)
    python simulation.py --angles 0 90 --no-away  the rotor at 0 and 90 degrees only
    python simulation.py --step 10                every 10 degrees over one turn of the rotor's pattern
    python simulation.py --plot                   only redraw the curves from the results already written
    python simulation.py --angles 0 --voxels-only draw one angle's voxels and say how many, to judge the memory
    python simulation.py --voxel 0.035            voxels of 35 um in the board's plane instead of 50 um (a trial,
                                                  kept in case/; more memory and time)
    python simulation.py --gap 0.5 --merge a.json b.json
                                                  add the solves in results files from other machines (each one
                                                  ran some angles of this gap) to this gap's results, and redraw

The TX carries 1 A; SIN and COS carry none, so their voltages are the EMFs the TX induces in them, given as mutual
inductances (EMF = 2 pi f M x 1 A: 1 nH is 22 mV at 3.5 MHz). The rotor repeats itself every 360 / sectors degrees,
so the curves are drawn over that span: a full turn on a one-sector rotor.

Every angle gets its own voxels, the rotor's copper at that angle drawn onto the grid, which stays where the stator
is. The rotor's edges then fall on the voxels a little differently at each angle, which shows as small noise on the
curves; the fit written with the results says how much.

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
import sys
import time
from pathlib import Path

import numpy as np
from shapely.geometry import Point, Polygon

HERE = Path(__file__).resolve().parent              # <board>/PyPEEC Simulation
BOARD = HERE.parent                                 # <board>: README.md, Boards/, PyPEEC Simulation/, Results/
RESULTS = BOARD / 'Results'
GEOMETRY = BOARD / '3D_Geometry'                     # KESE's export of each board, kept in the repo
sys.path.insert(0, str(HERE.parents[3]))
sys.path.insert(0, str(HERE))
from angle_error import METHOD, angle_error, gap_folder, results_files, sine_fit   # noqa: E402
import make_charts as charts   # noqa: E402
from bridge import geometry as G, layers as L, ports as P, pypeec_case as C, study as S, voxels as V   # noqa: E402

SPEC = json.loads((HERE / 'test_spec.json').read_text())
EXPECTED = (json.loads((RESULTS / 'expected_results.json').read_text())
            if (RESULTS / 'expected_results.json').exists() else {})
AXIS = (100.0, -100.0)                 # KiCad (100, 100) in model coordinates, y up


def model_xy(xy_kicad):
    """KiCad (x, y) to model (x, y), y up."""
    return float(xy_kicad[0]), -float(xy_kicad[1])


SET = SPEC['sets'][0]
SIN_NET, COS_NET = str(SET['sin']), str(SET['cos'])
AGREE = charts.AGREE   # how far the TX's L and R from its voltage may be from the field energy's and the
                       # losses' for a solve to be read (make_charts.readable)
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
    tx_end=model_xy(SPEC['terminals']['TX']['ends_xy_kicad']),
    tx_end_radius_mm=SPEC['terminals']['TX'].get('end_radius_mm', 0.1),     # the trace ends' round caps
    rx_vias={'SIN': model_xy(SPEC['terminals'][SIN_NET]['via_xy_kicad']),
             'COS': model_xy(SPEC['terminals'][COS_NET]['via_xy_kicad'])},
    via_void_radius_mm=SPEC['terminals'][SIN_NET].get('void_radius_mm', 0.3),   # the barrel left out inside this
    rx_cuts={name: dict(xy=model_xy(c['xy_kicad']), along=(c['along_kicad'][0], -c['along_kicad'][1]),
                        gap_mm=c['gap_mm'], half_width_mm=c['half_width_mm'])
             for name, net in (('SIN', SIN_NET), ('COS', COS_NET))
             if (c := SPEC['terminals'][net].get('cut'))},    # with rx_port 'cut': where each top trace is cut
    voxel_mm=SPEC.get('voxel_mm', 0.05),   # the voxels' size in the board's plane: a 0.2 mm trace is 4 voxels across
    n_cu=1,                            # voxel layers through each copper sheet (dz follows, about the copper's 35 um)
    threads=4,
    tolerance={},                      # changes to the bridge's tolerance.yaml (PyPEEC's iterative solver)
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


def build(stator_export, rotor_export, angle, gap, d, log=print):
    """The voxels with the rotor at `angle` (degrees, KiCad's sense), or away (None), each coil opened at its port,
    as a case for PyPEEC."""
    stator = stator_parts(stator_export)
    parts = list(stator)
    if angle is not None:
        parts += rotor_parts(rotor_export, angle, gap)
    lay = L.Layout(parts).build(log=log, insulators=SETTINGS['insulators'])
    grid, vox = V.build(lay, d, copper_mm=SPEC['stator']['copper_thickness_mm'], n_cu=SETTINGS['n_cu'], log=log)
    top = next(s_ for s_ in grid.sheets if abs(s_['z1']) < 1e-6)      # the stator's F.Cu: its top face at z = 0
    bottom = grid.sheets[0]                                           # its B.Cu
    f0, f1 = top['z0'], top['z1']
    coils = []
    for name in ('TX', 'SIN', 'COS'):
        if name == 'TX':                    # the TX's two ends, stacked on the two layers: the gap is between them
            hole = Point(SETTINGS['tx_end']).buffer(SETTINGS['tx_end_radius_mm'], 32)
            t1, t2 = P.terminals(grid, vox, name, hole, bottom['z1'], f0)
        elif RX_PORT == 'cut':              # a gap cut across the top trace
            box = cut_box(name)
            n = P.cut(grid, vox, name, box, f0, f1)
            t1, t2 = P.terminals(grid, vox, name, box, f0, f1)
            log(f'{name}: cut {n} voxels')
        else:                               # a via's barrel left out: the gap is between its two pads
            hole = Point(SETTINGS['rx_vias'][name]).buffer(SETTINGS['via_void_radius_mm'], 64)
            n = P.cut(grid, vox, name, hole, bottom['z1'], f0)
            t1, t2 = P.terminals(grid, vox, name, hole, bottom['z1'], f0)
            log(f'{name}: via left out, {n} voxels')
        log(f'{name}: terminals of {len(t1)} and {len(t2)} voxels')
        coils.append(C.Coil(name, name, t1, t2, 1.0 if name == 'TX' else 0.0))
    case = C.Case(grid=grid, vox=vox, coils=coils, sigma={b: SETTINGS['sigma'] for b in vox},
                  floating=['ROTOR'] if angle is not None and 'ROTOR' in vox else [],
                  tolerance=SETTINGS['tolerance'])
    return case


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
            how = ('' if max(ang) - min(ang) >= 0.75 * per else ', drawn only between the solved angles while few '
                   'are in')
            sec += [f'![SIN and COS against the rotor angle at a {gap:g} mm air gap]({png})', '',
                    f"*Figure {i}. SIN (blue) and COS (orange) at a {gap:g} mm air gap: the mutual inductance from "
                    f"the TX against the rotor's angle, {len(ang)} of {planned} angles solved. Each dot is one PyPEEC "
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
        flagged = [r for r in runs if not r['solve'].get('pypeec', {}).get('status', True)]
        if flagged:
            sec += [f"PyPEEC flagged {len(flagged)} of {len(runs)} solves ("
                    f"{', '.join(format(r['rotor_deg'], 'g') + '°' for r in flagged)}): its own check of the solver or "
                    f"of the matrices' condition did not pass. Their L and R checks are in the table.", '']
        loose = [r for r in runs if not charts.readable(r['solve'])]
        if loose:
            sec += [f"**Not converged enough to read:** {len(loose)} of {len(runs)} solves "
                    f"({', '.join(format(r['rotor_deg'], 'g') + '°' for r in loose)}) give the TX a negative "
                    f"resistance, or an L or R from its voltage more than {AGREE * 100:g} % away from the L from the field "
                    f"energy or the R from the losses. Read this gap's curve with that in mind.",
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
    boards += [f"*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In PyPEEC, SIN is "
               f"opened {opened}at {xy(rs)} and COS at {xy(rc)}, the TX at its ends at {xy(tx)} (KiCad mm). The "
               f"[README](../README.md) has the board and how it was made.*", '']
    if (BOARD / f'{BOARD.name}_pypeec_setup.webp').exists():
        boards += [f'![how the stator and rotor are set up in PyPEEC](../{BOARD.name}_pypeec_setup.webp)',
                   '', "*How the boards are set up in PyPEEC, drawn by "
                   "[`rig_picture.py`](../PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves "
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
                  f"{tx_exp['L_rotor_gen_H'] * 1e9:.0f} nH with it (its drop with the rotor is an upper estimate). PyPEEC "
                  "gives "
                  + ', and '.join(got) + '. The expected values are in '
                  '[expected_results.json](expected_results.json).', '']
    method = ['## How the angle error is worked out', '', METHOD, '']
    text = '\n'.join([
        f'# {BOARD.name}: SIN and COS over the rotor\'s turn in PyPEEC', '',
        f"A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-"
        f"Encoders-Coil-Generator): {2 * st['bore_and_outer_radius_mm'][1]:g} mm across, {len(st['layers'])} copper "
        f"layers, {'one electrical period' if n_per == 1 else f'{n_per} electrical periods'} per turn and {rotor}. The TX carries 1 A at "
        f"{SETTINGS['freq_hz'] / 1e6:g} MHz; the curves are the mutual inductance from the TX to SIN and to COS "
        f"(1 nH is {w:.0f} mV of EMF). Each angle is one PyPEEC solve with its own voxels, checked by working the TX's L "
        f"and R out two ways: from its voltage, and from the stored energy and the losses (the L and R checks in "
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
    """How a solve went, for the tables: the iterative solver's iterations and the residual it stopped at."""
    return f"{s['iterations']} iterations, {s['residual']:.1e}"


def checks_cell(s):
    """How far the TX's L and R from its voltage are from L from the stored energy and R from the losses, in %."""
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
    """What makes two solves alike: the voxels (their size in the plane and through the copper) and the changes to
    the solver's tolerances."""
    d = result.get('solver') or {}
    return (d.get('voxel_mm'), d.get('n_cu'), json.dumps(d.get('tolerance', {}), sort_keys=True))


def merge(res_file, others, log=print):
    """Add the solves of other results files of the same gap (say, one angle each from machines run in parallel) to
    res_file, then redraw. An angle already in res_file keeps its solve; a file with another gap, voxel size or
    solver setting is refused, so that only like solves share a curve."""
    result = json.loads(res_file.read_text()) if res_file.exists() else None
    same = ('gap_mm', 'rx_port')
    for f in others:
        other = json.loads(f.read_text())
        if result is None:
            result = dict(other, runs=[])
        dflt = dict(rx_port='via')                       # results from before rx_port was recorded
        bad = [k for k in same if other.get(k, dflt.get(k)) != result.get(k, dflt.get(k))]
        if bad or solver_key(other) != solver_key(result):
            log(f'{f.name}: not merged, its ' + (', '.join(bad) or 'solver setting') + ' differs')
            continue
        if other.get('versions', {}).get('pypeec') != result.get('versions', {}).get('pypeec'):
            log(f"{f.name}: PyPEEC {other.get('versions', {}).get('pypeec')} against "
                f"{result.get('versions', {}).get('pypeec')} here; merged, but say so")
        have = {r['rotor_deg'] for r in result['runs']}
        new = [r for r in other['runs'] if r['rotor_deg'] not in have]
        result['runs'] += new
        log(f'{f.name}: added ' + (', '.join(str(r['rotor_deg']) for r in new) or 'nothing new'))
    if result is None:
        return
    v = result.setdefault('versions', {})
    if str(v.get('kese', 'unknown')).startswith('unknown'):  # solved where KESE was not installed: the export's own
        v['kese'] = S.versions([GEOMETRY / Path(SETTINGS[k]).stem for k in ('stator', 'rotor')])['kese']
    result['runs'].sort(key=lambda r: -1 if r['rotor_deg'] == 'away' else r['rotor_deg'])
    res_file.parent.mkdir(parents=True, exist_ok=True)
    res_file.write_text(json.dumps(result, indent=1))
    plot(res_file, log)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--angles', type=float, nargs='*', default=None)
    ap.add_argument('--step', type=float, default=None, help="every STEP degrees over the rotor's period")
    ap.add_argument('--gap', type=float, default=SETTINGS['air_gap_mm'], help='air gap, copper to copper (mm)')
    ap.add_argument('--no-away', action='store_true', help='skip the run with the rotor away')
    ap.add_argument('--voxel', type=float, default=SETTINGS['voxel_mm'], help="the voxels' size in the plane (mm)")
    ap.add_argument('--n-cu', type=int, default=SETTINGS['n_cu'], help='voxel layers through each copper sheet')
    ap.add_argument('--threads', type=int, default=SETTINGS['threads'])
    ap.add_argument('--trial', default='', help='a name for a trial setting: its results stay in case/')
    ap.add_argument('--voxels-only', action='store_true', help='draw the voxels and say how many, solve nothing')
    ap.add_argument('--plot', action='store_true', help='only redraw the table and the curves')
    ap.add_argument('--merge', nargs='+', metavar='JSON', default=None,
                    help="other machines' results files of this gap: their solves are added to this gap's results")
    ap.add_argument('--out', default=str(HERE / 'case'))
    a = ap.parse_args()
    tagg = (f'gap{a.gap:g}mm' + ('' if a.voxel == SETTINGS['voxel_mm'] else f'_voxel{a.voxel * 1e3:g}um')
            + ('' if a.n_cu == SETTINGS['n_cu'] else f'_cu{a.n_cu}') + (f'_{a.trial}' if a.trial else ''))
    trial = tagg != f'gap{a.gap:g}mm'                   # another voxel size or setting: a trial, kept in case/
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
        angles = [float(x) for x in np.arange(0.0, SETTINGS['period_deg'] - 1e-9, a.step)]
    else:
        angles = [float(x) for x in SETTINGS['angles_deg']]
    SETTINGS['n_cu'] = a.n_cu
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
        board=BOARD.name, gap_mm=a.gap, voxel_mm=a.voxel, rx_port=RX_PORT, settings=SETTINGS, expected=EXPECTED,
        solver=dict(kind='PyPEEC, FFT-accelerated PEEC, GMRES with its own preconditioner', voxel_mm=a.voxel,
                    n_cu=a.n_cu, tolerance=SETTINGS['tolerance'], tolerance_file=in_repo(C.TOLERANCE)),
        versions=S.versions((se, re_)), runs=[])
    done = {r['rotor_deg'] for r in result['runs']}
    runs = ([] if a.no_away else [None]) + angles
    for angle in runs:
        key = 'away' if angle is None else angle
        if key in done and not a.voxels_only:
            log(f'{key}: already in {res_file.name}, skipped')
            continue
        tag = 'away' if angle is None else f'rotor{angle:g}'
        t0 = time.time()
        case = build(se, re_, angle, a.gap, a.voxel, log)
        g = case.grid
        voxels = dict(seconds=round(time.time() - t0, 1), **g.summary(),
                      copper_voxels={b: int(sum(len(v) for v in kv.values())) for b, kv in case.vox.items()},
                      terminal_voxels={c.name: [len(c.t1), len(c.t2)] for c in case.coils})
        log(f'{tag}: voxels {voxels}')
        if a.voxels_only:
            continue
        folder = out / f'{tagg}_{tag}'
        rows = S.solve(case, [SETTINGS['freq_hz']], folder, threads=a.threads, log=log, tag=tag)
        result['runs'] = [r for r in result['runs'] if r['rotor_deg'] != key]
        result['runs'].append(dict(rotor_deg=key, voxels=voxels, solve=rows[0]))
        result['runs'].sort(key=lambda r: -1 if r['rotor_deg'] == 'away' else r['rotor_deg'])
        res_file.write_text(json.dumps(result, indent=1))
        c = rows[0]['coils']
        log(f"{tag}: L_TX {c['TX']['L'] * 1e9:.3f} nH, R_TX {c['TX']['R'] * 1e3:.2f} mOhm, "
            f"M_SIN {c['SIN']['M'] * 1e9:.4f} nH, M_COS {c['COS']['M'] * 1e9:.4f} nH, {rows[0]['iterations']} it, "
            f"res {rows[0]['residual']:.1e}, {rows[0]['peak_memory_gb']} GB, {rows[0]['seconds']} s")
        plot(res_file, log)
    if not a.voxels_only:
        log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
