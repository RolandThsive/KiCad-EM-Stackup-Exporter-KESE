"""A coil set from the Sinusoidal Coil Generator in FastHenry: the SIN and COS curves against the rotor's angle, at
any air gap. Everything that belongs to the board is in test_spec.json beside this file, so the same script runs
every single-set board that new_coil.py sets up; the board's README, one folder up, says what this board is. A board
folder holds Boards/ (straight from the generator), 3D_Geometry/ (KESE's export of the two boards, for the copper
layers' heights), FastHenry Simulation/ (this script, test_spec.json, angle_error.py and the runs under case/) and
Results/ (what the runs give, and what was expected).

    python simulation.py                          the rotor away, then every angle in test_spec.json
    python simulation.py --gap 0.5                the same at a 0.5 mm air gap (copper to copper)
    python simulation.py --angles 0 90 --no-away  the rotor at 0 and 90 degrees only
    python simulation.py --step 10                every 10 degrees over the whole turn
    python simulation.py --jobs 3                 three solves at once (FastHenry uses one core for each)
    python simulation.py --plot                   only redraw the curves from the results already written
    python simulation.py --angles 0 --model-only  build one angle's filaments and say how many, to judge the memory
    python simulation.py --nwinc 5                5 filaments across each track instead of the default (a trial,
                                                  kept in case/; more memory and time)
    python simulation.py --gap 0.5 --merge a.json b.json
                                                  add the solves in results files from other machines (each one
                                                  ran some angles of this gap) to this gap's results, and redraw

The TX carries 1 A; SIN and COS are open, so their voltages are the EMFs the TX induces in them, given as mutual
inductances (EMF = 2 pi f M x 1 A: 1 nH is 22 mV at 3.5 MHz). The rotor repeats itself every 360 / sectors degrees,
so the curves are drawn over that span: a full turn on a one-sector rotor.

The conductors come from the board files themselves: every track of the three coils is a FastHenry segment along its
centre line, as wide as the track and as thick as its layer's copper, split into filaments across its width so the
current can crowd to its edges; a via is a vertical bar. The rotor's copper is a grid of bars turned to each angle,
graded finer towards its edges. KESE's export in ../3D_Geometry gives the heights and thicknesses of the copper
layers. The space round the copper needs no mesh, and FastHenry's dense direct solve (LU) gives the exact answer of
that model, so a solve has no convergence to judge: its impedance matrix comes out symmetric to the last digit, and
the results check it (reciprocity: M from the TX to a receiver equals M from the receiver to the TX).

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
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent              # <board>/FastHenry Simulation
BOARD = HERE.parent                                 # <board>: README.md, Boards/, FastHenry Simulation/, Results/
RESULTS = BOARD / 'Results'
GEOMETRY = BOARD / '3D_Geometry'                     # KESE's export of each board, kept in the repo
sys.path.insert(0, str(HERE.parents[3]))
sys.path.insert(0, str(HERE))
from angle_error import METHOD, angle_error, gap_folder, results_files, sine_fit   # noqa: E402
import make_charts as charts   # noqa: E402
from bridge import fasthenry_case as C, kicad as K, stackup as S   # noqa: E402

SPEC = json.loads((HERE / 'test_spec.json').read_text())
EXPECTED = (json.loads((RESULTS / 'expected_results.json').read_text())
            if (RESULTS / 'expected_results.json').exists() else {})
AXIS_KICAD = tuple(SPEC['coordinates'].get('kicad_axis_xy', (100.0, 100.0)))
AXIS = (AXIS_KICAD[0], -AXIS_KICAD[1])               # the same in model coordinates, y up


def model_xy(xy_kicad):
    """KiCad (x, y) to model (x, y), y up."""
    return float(xy_kicad[0]), -float(xy_kicad[1])


SET = SPEC['sets'][0]
SIN_NET, COS_NET = str(SET['sin']), str(SET['cos'])
AGREE = charts.AGREE   # how far M to and from the TX may differ for a solve to be read (make_charts.readable)
SETTINGS = dict(
    stator=SPEC['files']['stator'],    # paths from the board folder
    rotor=SPEC['files']['rotor'],
    names={str(k): v for k, v in SPEC['nets'].items()},   # the board's net -> the coil's name
    sigma=5.8e7,                       # S/m, copper
    freq_hz=SET['f_Hz'],
    air_gap_mm=SPEC['air_gap_mm'],     # stator F.Cu top to rotor copper face; --gap sets another
    angles_deg=SET['sweep_angles_mech_deg'],
    period_deg=SET.get('rotor_period_mech_deg', 360.0),   # the rotor repeats itself after this
    tx_end=model_xy(SPEC['terminals']['TX']['ends_xy_kicad']),
    tx_end_radius_mm=SPEC['terminals']['TX'].get('end_radius_mm', 0.1),     # how near the two ends must reach it
    rx_vias={'SIN': model_xy(SPEC['terminals'][SIN_NET]['via_xy_kicad']),
             'COS': model_xy(SPEC['terminals'][COS_NET]['via_xy_kicad'])},
    rx_cuts={name: dict(xy=model_xy(c['xy_kicad']), along=(c['along_kicad'][0], -c['along_kicad'][1]),
                        gap_mm=c['gap_mm'], half_width_mm=c['half_width_mm'], layer=c.get('layer', 'F.Cu'))
             for name, net in (('SIN', SIN_NET), ('COS', COS_NET))
             if (c := SPEC['terminals'][net].get('cut'))},    # with rx_port 'cut': where each top trace is cut
    nwinc=3,                           # filaments across each track's width ...
    rw=2.0,                            # ... each edge filament this much narrower than the next one in
    nhinc=1,                           # filaments through each track's copper thickness
    max_arc_deg=5.0,                   # an arc track as chords of at most 5 degrees (and 0.5 mm)
    rotor_edge_mm=0.05,                # the rotor's grid: bars this wide at its edges ...
    rotor_max_mm=0.3,                  # ... growing to this in its middle
    via_plating_mm=0.025,              # a via is a bar with the copper section of a barrel plated this thick
    options=['-s', 'ludecomp', '-m', 'direct', '-a', 'off'],   # FastHenry's dense direct solve, exact for the
                                       # model; no splitting of segments for multipole cubes, which a direct solve
                                       # has no use for (it changes no digit at 1 mm, and the split pieces upset its
                                       # exact formula for parallel filaments at 0.1 mm)
    jobs=1,                            # solves at once (--jobs)
)


def stack(board_file):
    """A board's copper layers, {layer: (z_bottom, z_top)} in KESE's coordinates, from KESE's export of it (made
    again only when the board file changes)."""
    return S.copper_layers(S.kese_geometry(BOARD / board_file, GEOMETRY, log=lambda *_: None))


def stator_layers():
    """The stator's copper layers in model coordinates: its F.Cu top face at z = 0."""
    zs = stack(SETTINGS['stator'])
    top = zs['F.Cu'][1]
    return {k: (a - top, b - top) for k, (a, b) in zs.items()}


def rotor_layers(gap):
    """The rotor's copper layers in model coordinates: the board turned copper side down (z -> -z, its pattern not
    mirrored) with its copper's outer face `gap` above z = 0."""
    zr = stack(SETTINGS['rotor'])
    face = max(b for _, b in zr.values())
    return {k: (gap + face - b, gap + face - a) for k, (a, b) in zr.items()}


RX_PORT = SPEC.get('rx_port', 'via')   # how SIN and COS are opened: 'via' (a via left out) or 'cut' (a gap cut
                                       # across a top trace, at test_spec.json's 'cut' of each)
assert RX_PORT == 'via' or len(SETTINGS['rx_cuts']) == 2, "rx_port 'cut' needs a 'cut' for SIN and COS in test_spec.json"


def boards():
    """The stator and rotor board files read (their tracks, vias and copper polygons)."""
    return K.read(BOARD / SETTINGS['stator']), K.read(BOARD / SETTINGS['rotor'])


def build(stator, rotor, angle, gap, s=SETTINGS, log=print):
    """The FastHenry model with the rotor at `angle` (degrees, KiCad's sense, about the axis), or away (None), each
    coil opened at its port. Returns the model and what it is made of."""
    t0 = time.time()
    inv = {coil: net for net, coil in s['names'].items()}
    m = C.Model(title=f'{BOARD.name}: rotor ' + ('away' if angle is None else f'at {angle:g} deg') + f', gap {gap:g} mm')
    cuts = ([dict(net=inv[n], **s['rx_cuts'][n]) for n in ('SIN', 'COS')] if RX_PORT == 'cut' else [])
    open_vias = [] if RX_PORT == 'cut' else [s['rx_vias'][n] for n in ('SIN', 'COS')]
    rw = s['rw'] if s['nwinc'] > 1 else None
    zst = stator_layers()
    ends = C.add_board(m, stator, zst, s['names'], nwinc=s['nwinc'], nhinc=s['nhinc'], rw=rw, open_vias=open_vias,
                       cuts=cuts, max_deg=s['max_arc_deg'], plating_mm=s['via_plating_mm'])
    within = max(0.3, s['tx_end_radius_mm'])
    m.port('TX', *C.via_nodes(m, inv['TX'], *s['tx_end'], within=within))      # between its two stacked ends
    for i, name in enumerate(('SIN', 'COS')):
        if RX_PORT == 'cut':                # between the two faces of the cut
            m.port(name, *C.cut_nodes(m, cuts[i]['net'], cuts[i]['layer'], ends[i]))
        else:                               # between the left-out via's two ends, on F.Cu and B.Cu
            m.port(name, *C.via_nodes(m, inv[name], *s['rx_vias'][name]))
    n_stator = len(m.segs)
    bars = 0
    if angle is not None:
        zr = rotor_layers(gap)
        for layer, _net, pts in rotor.polygons:
            if layer in zr:
                z0, z1 = zr[layer]
                bars += C.add_polygon(m, 'ROTOR', pts, AXIS_KICAD, angle, (z0 + z1) / 2, z1 - z0,
                                      h_edge=s['rotor_edge_mm'], h_max=s['rotor_max_mm'])
    info = dict(seconds=round(time.time() - t0, 2), nodes=len(m.nodes), segments=len(m.segs),
                filaments=m.filaments, stator_segments=n_stator, rotor_bars=bars,
                ports={name: [m.xyz(a), m.xyz(b)] for name, a, b in m.ports})
    return m, info


def solve(model, folder, s=SETTINGS, log=print):
    """One FastHenry solve at the set's frequency: each coil's numbers (make_charts and the tables read them) and
    the solve's own."""
    names, Z, secs, gb, text = C.run(model, s['freq_hz'], folder, s['options'], sigma=s['sigma'])
    coils = C.coil_rows(names, Z, s['freq_hz'], driven='TX')
    scale = max(abs(coils[n]['M']) for n in ('SIN', 'COS')) or 1e-30
    recip = {n: abs(coils[n]['M'] - coils[n]['M_reverse']) / scale for n in ('SIN', 'COS')}
    return dict(frequency_hz=s['freq_hz'], seconds=round(secs, 1), peak_memory_gb=round(gb, 3),
                coils=coils, reciprocity=recip, fasthenry=dict(size=C.size_of(text), options=list(s['options'])),
                Z_ohm={'ports': names, 're': Z.real.tolist(), 'im': Z.imag.tolist()})


def fit(angles, values):
    """The best sine over the rotor's period (angle_error.sine_fit): offset, amplitude, phase and the rms left."""
    return sine_fit(angles, values, SETTINGS['period_deg'])


def model_label(res):
    """What the model is, in a few words, for the charts' subtitles."""
    d = res.get('solver', {})
    return (f"{d.get('nwinc', '?')} filaments across each track, rotor bars "
            f"{d.get('rotor_edge_mm', 0) * 1e3:g} to {d.get('rotor_max_mm', 0) * 1e3:g} µm")


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
                    f"FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, "
                    f"each channel's best sine fit{how}, which is what the angle error is measured against. SIN swings "
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
        rows = ['| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | '
                'Memory | Time |', '|---|---|---|---|---|---|---|---|---|---|']
        for r in away + runs:
            s, c = r['solve'], r['solve']['coils']
            e = err['per_angle'].get(float(r['rotor_deg'])) if err and r['rotor_deg'] != 'away' else None
            rows.append(f"| {'away' if r['rotor_deg'] == 'away' else format(r['rotor_deg'], 'g') + '°'} | "
                        f"{c['SIN']['M'] * 1e9:.4f} | {c['COS']['M'] * 1e9:.4f} | "
                        f"{'' if e is None else f'{e:+.2f}°'} | {c['TX']['L'] * 1e9:.3f} | "
                        f"{c['TX']['R'] * 1e3:.2f} | {r['model']['filaments']:,} | {reciprocity_cell(s)} | "
                        f"{s['peak_memory_gb']:.1f} GB | {time_cell(s['seconds'])} |")
        if len(rows) > 2:
            sec += rows + ['']
        loose = [r for r in runs if not charts.readable(r['solve'])]
        if loose:
            sec += [f"**Not readable:** {len(loose)} of {len(runs)} solves "
                    f"({', '.join(format(r['rotor_deg'], 'g') + '°' for r in loose)}) give the TX a negative "
                    f"resistance, or an M from the TX more than {AGREE * 100:g} % away from the M back to it. Read "
                    "this gap's curve with that in mind.", '']
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
    boards += [f"*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In FastHenry, SIN "
               f"is opened {opened}at {xy(rs)} and COS at {xy(rc)}, the TX at its ends at {xy(tx)} (KiCad mm). The "
               f"[README](../README.md) has the board and how it was made.*", '']
    if (BOARD / f'{BOARD.name}_fasthenry_setup.webp').exists():
        boards += [f'![how the stator and rotor are set up in FastHenry](../{BOARD.name}_fasthenry_setup.webp)',
                   '', "*How the boards are set up in FastHenry, drawn by "
                   "[`rig_picture.py`](../FastHenry%20Simulation/rig_picture.py) from the model simulation.py solves: "
                   "the stator's tracks as segments split into filaments, the rotor copper side down over the stator "
                   "as a grid of bars, each receiver opened "
                   + ("by a cut across a top trace (the port is between the two cut faces, and the receiver is open "
                      "there, so the voltage across the cut is the open-circuit EMF)" if RX_PORT == 'cut' else
                      "at a left-out via (the port is between where its tracks reach the via on the two layers, and "
                      "the receiver is open there, so the voltage across it is the open-circuit EMF)")
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
                  f"{tx_exp['L_rotor_gen_H'] * 1e9:.0f} nH with it (its drop with the rotor is an upper estimate). "
                  "FastHenry gives " + ', and '.join(got) + '. The expected values are in '
                  '[expected_results.json](expected_results.json).', '']
    method = ['## How the angle error is worked out', '', METHOD, '']
    text = '\n'.join([
        f'# {BOARD.name}: SIN and COS over the rotor\'s turn in FastHenry', '',
        f"A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-"
        f"Encoders-Coil-Generator): {2 * st['bore_and_outer_radius_mm'][1]:g} mm across, {len(st['layers'])} copper "
        f"layers, {'one electrical period' if n_per == 1 else f'{n_per} electrical periods'} per turn and {rotor}. The "
        f"TX carries 1 A at {SETTINGS['freq_hz'] / 1e6:g} MHz; the curves are the mutual inductance from the TX to SIN "
        f"and to COS (1 nH is {w:.0f} mV of EMF). Each angle is one FastHenry solve: the stator's tracks as filaments "
        f"and the rotor's copper as a grid of bars turned to that angle, solved directly, so each solve is the exact "
        f"answer of its model. Each is checked by reciprocity: the M from the TX to a receiver and the M from the "
        f"receiver back to the TX must agree (the Reciprocity column gives how far apart they are, as a part of the "
        f"larger receiver's M; a solve is read when it is within {AGREE * 100:g} %). This page is rewritten by "
        f"`simulation.py` after every solve.", '',
        '| Air gap | Angles solved | Amplitude SIN / COS | Angle error |', '|---|---|---|---|', *summary, '',
        *sections, *gaps_section(curves, [p for _, p in gaps], len(sections) + 1), *expect, *method, *boards])
    (RESULTS / 'SINCOS_Results.md').write_text(text)
    log('wrote SINCOS_Results.md')


def reciprocity_cell(s):
    """How far M from the TX and M back to it are apart, as a part of the larger receiver's M."""
    worst = max(s['reciprocity'].values())
    return 'exact' if worst < 1e-9 else f'{100 * worst:.2g} %'


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


SOLVER_KEYS = ('nwinc', 'rw', 'nhinc', 'max_arc_deg', 'rotor_edge_mm', 'rotor_max_mm', 'via_plating_mm', 'options')


def solver_key(result):
    """What makes two solves alike: the filaments, the rotor's grid, the vias and FastHenry's options."""
    d = result.get('solver') or {}
    return json.dumps({k: d.get(k) for k in SOLVER_KEYS}, sort_keys=True)


def merge(res_file, others, log=print):
    """Add the solves of other results files of the same gap (say, some angles each from machines run in parallel)
    to res_file, then redraw. An angle already in res_file keeps its solve; a file with another gap, port or solver
    setting is refused, so that only like solves share a curve."""
    result = json.loads(res_file.read_text()) if res_file.exists() else None
    same = ('gap_mm', 'rx_port')
    for f in others:
        other = json.loads(f.read_text())
        if result is None:
            result = dict(other, runs=[])
        bad = [k for k in same if other.get(k) != result.get(k)]
        if bad or solver_key(other) != solver_key(result):
            log(f'{f.name}: not merged, its ' + (', '.join(bad) or 'solver setting') + ' differs')
            continue
        if other.get('versions', {}).get('fasthenry') != result.get('versions', {}).get('fasthenry'):
            log(f"{f.name}: FastHenry {other.get('versions', {}).get('fasthenry')} against "
                f"{result.get('versions', {}).get('fasthenry')} here; merged, but say so")
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
    ap.add_argument('--step', type=float, default=None, help='every STEP degrees over the whole turn')
    ap.add_argument('--gap', type=float, default=SETTINGS['air_gap_mm'], help='air gap, copper to copper (mm)')
    ap.add_argument('--no-away', action='store_true', help='skip the run with the rotor away')
    ap.add_argument('--nwinc', type=int, default=SETTINGS['nwinc'], help="filaments across each track's width")
    ap.add_argument('--nhinc', type=int, default=SETTINGS['nhinc'], help="filaments through each track's copper")
    ap.add_argument('--rotor-edge', type=float, default=SETTINGS['rotor_edge_mm'],
                    help="the rotor grid's bars at its edges (mm)")
    ap.add_argument('--rotor-max', type=float, default=SETTINGS['rotor_max_mm'],
                    help="the rotor grid's bars in its middle (mm)")
    ap.add_argument('--jobs', type=int, default=SETTINGS['jobs'], help='solves at once (one core each)')
    ap.add_argument('--trial', default='', help='a name for a trial setting: its results stay in case/')
    ap.add_argument('--model-only', action='store_true', help='build the filaments and say how many, solve nothing')
    ap.add_argument('--plot', action='store_true', help='only redraw the table and the curves')
    ap.add_argument('--merge', nargs='+', metavar='JSON', default=None,
                    help="other machines' results files of this gap: their solves are added to this gap's results")
    ap.add_argument('--out', default=str(HERE / 'case'))
    a = ap.parse_args()
    changed = {k: v for k, v in (('nwinc', a.nwinc), ('nhinc', a.nhinc), ('rotor_edge_mm', a.rotor_edge),
                                 ('rotor_max_mm', a.rotor_max)) if v != SETTINGS[k]}
    tagg = (f'gap{a.gap:g}mm' + ''.join(f'_{k.split("_")[0]}{v:g}' for k, v in changed.items())
            + (f'_{a.trial}' if a.trial else ''))
    trial = tagg != f'gap{a.gap:g}mm'                   # another discretisation or setting: a trial, kept in case/
    SETTINGS.update(changed)
    res_file = (Path(a.out) if trial else RESULTS / gap_folder(a.gap)) / f'results_{tagg}.json'
    if not (a.model_only or a.plot):
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
    lock = threading.Lock()

    def log(msg):
        with lock:
            print(msg, flush=True)
            logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
            logf.flush()
    se = S.kese_geometry(BOARD / SETTINGS['stator'], GEOMETRY, log=log)   # exported again only if the board changed
    re_ = S.kese_geometry(BOARD / SETTINGS['rotor'], GEOMETRY, log=log)
    stator, rotor = boards()
    result = json.loads(res_file.read_text()) if res_file.exists() else dict(
        board=BOARD.name, gap_mm=a.gap, rx_port=RX_PORT, settings=SETTINGS, expected=EXPECTED,
        solver=dict(kind='FastHenry: filaments (partial inductances), dense direct solve (LU)',
                    **{k: SETTINGS[k] for k in SOLVER_KEYS}),
        stackup=dict(stator=stator_layers(), rotor_at_gap=rotor_layers(a.gap)),
        versions=S.versions((se, re_)), runs=[])
    result['model'] = dict(label=model_label(result))
    done = {r['rotor_deg'] for r in result['runs']}
    todo = []
    for angle in ([] if a.no_away else [None]) + angles:
        key = 'away' if angle is None else angle
        if key in done and not a.model_only:
            log(f'{key}: already in {res_file.name}, skipped')
            continue
        todo.append(angle)

    def one(angle):
        tag = 'away' if angle is None else f'rotor{angle:g}'
        model, info = build(stator, rotor, angle, a.gap, log=log)
        log(f"{tag}: {info['filaments']:,} filaments ({info['stator_segments']:,} stator segments, "
            f"{info['rotor_bars']:,} rotor bars), {info['nodes']:,} nodes")
        if a.model_only:
            return angle, info, None
        return angle, info, solve(model, out / f'{tagg}_{tag}', log=log)

    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as pool:
        for fut in as_completed([pool.submit(one, angle) for angle in todo]):
            angle, info, row = fut.result()
            if row is None:
                continue
            key = 'away' if angle is None else angle
            tag = 'away' if angle is None else f'rotor{angle:g}'
            result['runs'] = [r for r in result['runs'] if r['rotor_deg'] != key]
            result['runs'].append(dict(rotor_deg=key, model=info, solve=row))
            result['runs'].sort(key=lambda r: -1 if r['rotor_deg'] == 'away' else r['rotor_deg'])
            res_file.write_text(json.dumps(result, indent=1))
            c = row['coils']
            log(f"{tag}: L_TX {c['TX']['L'] * 1e9:.3f} nH, R_TX {c['TX']['R'] * 1e3:.2f} mOhm, "
                f"M_SIN {c['SIN']['M'] * 1e9:.4f} nH, M_COS {c['COS']['M'] * 1e9:.4f} nH, reciprocity "
                f"{max(row['reciprocity'].values()):.1e}, {row['peak_memory_gb']} GB, {row['seconds']} s")
            plot(res_file, log)
    if not a.model_only:
        log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
