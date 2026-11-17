"""Set up a coil set from the Sinusoidal Coil Generator for Elmer: one command from the generator's output folder to
a folder here that simulation.py runs as it is.

    python new_coil.py <generator output folder> <name>
    python new_coil.py ".../Output/Coil_2_10.5_1_1_1_Series_SteppedDiagonal" S0_1x_OD21_2L_tiny
    python new_coil.py <folder> <name> --angles 16 --level 1.0 --no-estimate

<folder> is what the generator's Single Coil Set Generator wrote (Stator.kicad_pcb, Rotor.kicad_pcb, Parameters.txt
and the two SVG pictures). <name> is the new folder beside this file, laid out as S0_1x_OD21_2L_tiny is:

    README.md            the board, its terminals, the generator's warnings, the memory a solve needs and how to run it
    Boards/              straight from the generator: the boards, Parameters.txt (the local path in it replaced by
                         <your checkout>), the pictures, and parameter_files/ with the generator's parameter files,
                         taken from Parameters.txt
    Elmer Simulation/
      test_spec.json     every board fact simulation.py needs, read from Parameters.txt and Stator.kicad_pcb: the
                         nets, the frequency, the air gap, the air box (3 x the board's radius), the rotor's period,
                         the sweep's angles, and where each coil is opened (the TX at its stacked ends, each RX coil
                         at the layer-change via nearest the generator's suggested cut, or farthest from the TX copper
                         where it found no cut spot)
      simulation.py, angle_error.py, make_charts.py, rig_picture.py, angle_setup.py
                         S0_1x_OD21_2L_tiny's, unchanged: they read everything from test_spec.json
    3D_Geometry/         KESE's export of each board (STL solids, materials.json, STEP, KESE's report), written by
                         the first run and reused while the board is unchanged
    Results/
      expected_results.json   the generator's estimates (the TX's inductance and resistance); the runs add
                         SINCOS_Results.md here, and their results and charts in a folder per air gap
                         (1mm_AirGap, 0d5mm_AirGap)

Unless --no-estimate is given, it builds the mesh at one angle and says its size and the memory a direct solve
needs, at roughly 200 kB a node (S0 at level 0.25: 13 to 17 GB at 80,000 to 95,000 nodes; it grows faster than the
nodes). Single-set boards only: a dual board (DualCoil_...) has two coil sets.
This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / 'S0_1x_OD21_2L_tiny' / 'Elmer Simulation' / 'simulation.py'
SCRIPTS = ('simulation.py', 'angle_error.py', 'make_charts.py', 'rig_picture.py', 'angle_setup.py')  # from TEMPLATE's folder
KB_PER_NODE = 200.0                        # a direct solve's memory a node, roughly: S0 at level 0.25 took 13 to 17 GB
                                           # (in memory and swap) at 80,000 to 95,000 nodes, and more per node on
                                           # bigger meshes (about 40 to 55 GB at 204,000); the iterative solve 57 kB
AXIS = (100.0, 100.0)                      # the generator puts the sensor's axis at KiCad (100, 100)


def grab(pattern, text, cast=str, default=None):
    m = re.search(pattern, text, re.M)
    return cast(m.group(1)) if m else default


def parameters(text):
    """The values the generator lists under PARAMETER VALUES USED, as {name: python value}."""
    part = text.split('PARAMETER VALUES USED', 1)[-1].split('PARAMETER FILES', 1)[0]
    out = {}
    for name, value in re.findall(r'^\s+([A-Z][A-Z0-9_]+)\s+=\s+(.+?)(?:\s{3}\(.*\))?\s*$', part, re.M):
        try:
            out[name] = json.loads(value.replace("'", '"').replace('None', 'null').replace('True', 'true')
                                   .replace('False', 'false').replace('(', '[').replace(')', ']'))
        except ValueError:
            out[name] = value.strip("'\"")
    return out


def parameter_files(text):
    """The generator's parameter files, as {file name: text}, from the verbatim copies at the end of Parameters.txt."""
    part = text.split('PARAMETER FILES (verbatim copies)', 1)[-1]
    out = {}
    end = r'(?=^#{10} \w+\.py #+\n|^[A-Z][A-Z ()]+\n-{5,}\n|\Z)'     # the next file, or a section of the record
    for m in re.finditer(r'^#{10} (\w+\.py) #+\n(.*?)' + end, part, re.M | re.S):
        out[m.group(1)] = m.group(2).rstrip('\n') + '\n'
    return out


def board(path):
    """Nets {number: name}, vias [(x, y, net)], and the copper of each net as segments [(x1, y1, x2, y2, net, layer)]
    (arcs as two chords), from a KiCad board file."""
    t = Path(path).read_text()
    nets = {int(n): name for n, name in re.findall(r'^\s*\(net (\d+) "([^"]*)"\)', t, re.M)}
    vias = [(float(x), float(y), int(n)) for x, y, n in
            re.findall(r'\(via \(at ([-\d.]+) ([-\d.]+)\)[^\n]*?\(net (\d+)\)', t)]
    segs = [(float(a), float(b), float(c), float(d), int(n), lay) for a, b, c, d, lay, n in
            re.findall(r'\(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\)[^\n]*?'
                       r'\(layer "([^"]+)"\)[^\n]*?\(net (\d+)\)', t)]
    for a, b, mx, my, c, d, lay, n in re.findall(r'\(arc \(start ([-\d.]+) ([-\d.]+)\) \(mid ([-\d.]+) ([-\d.]+)\) '
                                                 r'\(end ([-\d.]+) ([-\d.]+)\)[^\n]*?\(layer "([^"]+)"\)[^\n]*?'
                                                 r'\(net (\d+)\)', t):
        a, b, mx, my, c, d, n = float(a), float(b), float(mx), float(my), float(c), float(d), int(n)
        segs += [(a, b, mx, my, n, lay), (mx, my, c, d, n, lay)]
    return nets, vias, segs


def tx_ends(segs, vias, tx_net):
    """Where the TX coil's two ends lie: the free ends of its copper (an end that no other piece of the same layer
    and no via meets), when they sit stacked at one point on two layers, as the generator draws them."""
    count = {}
    for s in segs:
        if s[4] == tx_net:
            for p in ((s[0], s[1]), (s[2], s[3])):
                k = (round(p[0], 3), round(p[1], 3), s[5])
                count[k] = count.get(k, 0) + 1
    on_via = {(round(x, 3), round(y, 3)) for x, y, n in vias if n == tx_net}
    free = [(x, y, lay) for (x, y, lay), c in count.items() if c == 1 and (x, y) not in on_via]
    if len(free) == 2 and math.hypot(free[0][0] - free[1][0], free[0][1] - free[1][1]) < 0.01 \
            and free[0][2] != free[1][2]:
        return free[0][0], free[0][1]
    return None


def seg_dist(p, s):
    (x, y), (a, b, c, d) = p, s[:4]
    dx, dy = c - a, d - b
    t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((x - a) * dx + (y - b) * dy) / (dx * dx + dy * dy)))
    return math.hypot(x - a - t * dx, y - b - t * dy)


def rx_via(vias, segs, net, tx_net, tx_end, cut=None):
    """Where an RX coil is opened: one of its layer-change vias (simulation.py leaves it out). Where the generator
    suggests a cut for the leads, the via nearest that cut; where it found no spot, the via farthest from the TX
    copper, and of those within 0.01 mm of the farthest, the one farthest from the TX's ends.
    Returns (x, y, distance to the TX copper)."""
    tx = [s for s in segs if s[4] == tx_net]
    cands = [(min(seg_dist((x, y), s) for s in tx), math.hypot(x - tx_end[0], y - tx_end[1]), x, y)
             for x, y, n in vias if n == net]
    if not cands:
        raise SystemExit(f'no via on net {net}: this script opens each RX coil at one of its layer-change vias')
    if cut:
        best = min(cands, key=lambda c: math.hypot(c[2] - cut[0], c[3] - cut[1]))
    else:
        far = max(c[0] for c in cands)
        best = max((c for c in cands if c[0] > far - 0.01), key=lambda c: c[1])
    return best[2], best[3], best[0]


def rx_cut(text, net):
    """The generator's suggested cut of an RX coil, (x, y), from the lead-cutting suggestion; None if it found none."""
    m = re.search(rf'^\s+\w+ \({re.escape(net)}\): cut the \w+ trace at \(([-\d.]+), ([-\d.]+)\)', text, re.M)
    return (float(m.group(1)), float(m.group(2))) if m else None


def spec_from(src, name, text, n_angles, level):
    P = parameters(text)
    made = grab(r'^name\s+(\S+)', text, default=src.name)
    if not made.startswith('Coil_'):
        raise SystemExit(f'{made}: not a Single Coil Set Generator board (Coil_...); dual boards have two sets')
    loops = grab(r'Stator: (\d+) loop', text, int)
    sectors = grab(r'Rotor \([^)]*\): (\d+) sector', text, int)
    duty = grab(r'sector\(s\), metal fraction ([\d.]+)', text, float)
    r_in, r_out = (grab(r'board edge: bore r = ([\d.]+) mm', text, float),
                   grab(r'board edge: bore r = [\d.]+ mm, outer r = ([\d.]+) mm', text, float))
    band = re.search(r'RX band r = ([\d.]+) \.\.\. ([\d.]+) mm', text)
    tx_ring = re.search(r'TX ring r = ([\d.]+) \.\.\. ([\d.]+) mm', text)
    rotor_cu = re.search(r'copper r = ([\d.]+) \.\.\. ([\d.]+) mm on', text)
    nets, vias, segs = board(src / 'Stator.kicad_pcb')
    by_name = {v: k for k, v in nets.items()}
    tx_name = str(P.get('TX_NET', 'TX'))
    tx_end = tx_ends(segs, vias, by_name[tx_name])
    tail = grab(r'TX ring r = [\d.]+ \.\.\. [\d.]+ mm \(tail end ([\d.]+) mm\)', text, float)
    if tx_end is None and tail and 'TX terminal sits at 0 deg' in text:
        tx_end = (AXIS[0] + tail, AXIS[1])                # the generator turns the board to put them at 0 degrees
    if tx_end is None:
        raise SystemExit("found no TX ends: neither two free ends stacked on two layers in Stator.kicad_pcb, nor "
                         "the tail end at 0 degrees in Parameters.txt")
    tx_end = (round(tx_end[0], 6), round(tx_end[1], 6))
    used = {s[5] for s in segs}
    layers = ['F.Cu'] + sorted((x for x in used if x.startswith('In')), key=lambda x: int(re.sub(r'\D', '', x))) \
        + ['B.Cu']
    sin_name, cos_name = str(P.get('RX_NET_PHASE_0_2', '2')), str(P.get('RX_NET_PHASE_1_3', '1'))
    sin_cut, cos_cut = rx_cut(text, sin_name), rx_cut(text, cos_name)
    sin_xy = rx_via(vias, segs, by_name[sin_name], by_name[tx_name], tx_end, sin_cut)
    cos_xy = rx_via(vias, segs, by_name[cos_name], by_name[tx_name], tx_end, cos_cut)

    def rx_source(xy, cut):
        if cut:
            return (f"the generator suggests cutting the coil at ({cut[0]:g}, {cut[1]:g}) for its leads; "
                    f"simulation.py opens coils at vias, so the layer-change via nearest that cut "
                    f"({math.hypot(xy[0] - cut[0], xy[1] - cut[1]):.2f} mm from it)")
        return (f"the generator found no cut spot; the layer-change via farthest from the TX copper "
                f"({xy[2]:.2f} mm), of those the farthest from the TX ends")
    drill, size = float(P.get('VIA_DRILL_MM', 0.4)), float(P.get('VIA_DIAMETER_MM', 0.8))
    void = round((drill + size) / 4, 4)                   # between the barrel's radius and the pad's
    period = 360.0 / sectors
    gap = float(P.get('AIR_GAP_MM', 1.0))
    thick = float(P.get('PCB_THICKNESS_MM', 1.6))
    est = {k: grab(p, text, float) for k, p in (('L_away_gen_uH', r'L = ([\d.]+) uH with the rotor away'),
                                                 ('L_rotor_gen_uH', r'L = ([\d.]+) uH with the rotor at'),
                                                 ('R_dc_ohm', r'R = ([\d.]+) ohm DC'))}
    rx_how = 'leave this via out (opens the loop); the terminal goes between its two pads'
    return dict(
        board=name, generator='Single', made_from=made,
        purpose='the SIN and COS curves against the rotor angle, at any air gap',
        units='mm, H, Hz, ohm, degrees',
        files={'stator': 'Boards/Stator.kicad_pcb', 'rotor': 'Boards/Rotor.kicad_pcb',
               'parameters': 'Boards/Parameters.txt', 'expected': 'Results/expected_results.json',
               'note': 'paths from the board folder'},
        coordinates={'kicad_axis_xy': list(AXIS),
                     'model_origin': "the rotation axis, at the top face of the stator's F.Cu copper",
                     'z': f'z up, from the stator towards the rotor. Stator F.Cu top face at z = 0, B.Cu at z = -{thick:g}'},
        stator={'layers': layers, 'board_thickness_mm': thick,
                'copper_thickness_mm': float(P.get('COPPER_THICKNESS_UM', 35)) / 1000,
                'bore_and_outer_radius_mm': [r_in, r_out],
                'rx_band_mm': [float(band.group(1)), float(band.group(2))] if band else None,
                'tx_ring_mm': [float(tx_ring.group(1)), float(tx_ring.group(2))] if tx_ring else None},
        rotor={'placement': 'copper side towards the stator, not mirrored, its copper face at z = +air_gap',
               'rings': [{'r_in': float(rotor_cu.group(1)) if rotor_cu else None,
                          'r_out': float(rotor_cu.group(2)) if rotor_cu else None,
                          'sectors': sectors, 'duty': duty}]},
        air_gap_mm=gap,
        air_gap_definition='stator F.Cu top face to rotor copper face (copper to copper)',
        air_box={'radius_or_half_width_mm': round(3 * r_out, 3),
                 'note': '3 x the board radius, as on the other boards; its height follows the gap'},
        nets={sin_name: 'SIN', cos_name: 'COS', tx_name: 'TX'},
        terminals={
            'TX': {'kind': 'TX ends', 'source': "the two free ends of the TX copper in Stator.kicad_pcb, stacked at "
                                                "one point (as Parameters.txt's lead-cutting suggestion)",
                   'ends_xy_kicad': list(tx_end), 'end_radius_mm': float(P.get('TX_TRACE_WIDTH_MM', 0.2)) / 2,
                   'how': 'the two coil ends lie stacked at this point on the two layers; the terminal goes between them'},
            sin_name: {'kind': 'RX via', 'source': rx_source(sin_xy, sin_cut), 'generator_cut_xy_kicad': sin_cut,
                       'via_xy_kicad': [sin_xy[0], sin_xy[1]], 'void_radius_mm': void, 'how': rx_how},
            cos_name: {'kind': 'RX via', 'source': rx_source(cos_xy, cos_cut), 'generator_cut_xy_kicad': cos_cut,
                       'via_xy_kicad': [cos_xy[0], cos_xy[1]], 'void_radius_mm': void, 'how': rx_how}},
        sets=[{'set': 1, 'tx': tx_name, 'sin': sin_name, 'cos': cos_name,
               'f_Hz': float(P.get('EXCITATION_FREQ_HZ', 3.5e6)), 'loops': loops,
               'electrical_period_mech_deg': round(360.0 / loops, 6), 'rotor_period_mech_deg': round(period, 6),
               'sweep_angles_mech_deg': [round(k * period / n_angles, 6) for k in range(n_angles)]}],
        mesh_level=level,
        expected={'tx': {'L_away_gen_H': est['L_away_gen_uH'] * 1e-6 if est['L_away_gen_uH'] else None,
                         'L_rotor_gen_H': est['L_rotor_gen_uH'] * 1e-6 if est['L_rotor_gen_uH'] else None,
                         'R_dc_ohm': est['R_dc_ohm'],
                         'note': "the generator's estimate; its drop with the rotor is an upper estimate"},
                  'coupling': f'SIN and COS follow the sine and cosine of {loops} x the rotor angle, 90 degrees apart'},
    )


def warnings(text):
    """The generator's warnings: the WARNINGS OF THIS RUN section and every line that starts with WARNING."""
    part = text.split('WARNINGS OF THIS RUN', 1)[-1].split('\n\n', 1)[0] if 'WARNINGS OF THIS RUN' in text else ''
    lines = [ln.strip() for ln in part.splitlines() if ln.strip() and not set(ln.strip()) <= {'-'}]
    lines += [ln.strip() for ln in text.splitlines() if ln.strip().startswith('WARNING ')]
    return list(dict.fromkeys(ln.removeprefix('WARNING ').strip() for ln in lines))


def readme(spec, src, warns, mesh, pics, expected=None):
    s, t, r = spec['stator'], spec['terminals'], spec['rotor']['rings'][0]
    st = spec['sets'][0]
    sin, cos = st['sin'], st['cos']
    picture = f'![stator and rotor](Boards/{pics[0]})\n\n*Drawn by the generator.*\n\n' if pics else ''
    mem = ''
    if mesh:
        gb = mesh['nodes'] * KB_PER_NODE / 1e6
        mem = (f"| Mesh level | Nodes | Memory a solve |\n|---|---|---|\n| {spec['mesh_level']:g} | {mesh['nodes']:,} | "
               f"about {gb:.1f} GB for the direct solve (at roughly {KB_PER_NODE:g} kB a node) |\n\n"
               "Past what the machine has, add a swap file (13.3 GB in memory and the rest in swap ran every S0 "
               "board); if it is far more, `--level` below the one above makes the mesh coarser and the solve "
               "smaller. `--solver iterative` (GCR) needs about 57 kB a node, but on the S0 boards at 3.5 MHz it "
               "converges too slowly to read M.\n\n")
    w = ''.join(f'* {x}\n' for x in warns) or '* none\n'
    tx = (expected or {}).get('tx', {})
    est = ''
    if tx.get('L_away_gen_H') and tx.get('L_rotor_gen_H') and tx.get('R_dc_ohm') is not None:
        est = (f"The generator's estimate for the TX: {tx['L_away_gen_H'] * 1e6:.2f} µH with the rotor away and "
               f"{tx['L_rotor_gen_H'] * 1e6:.2f} µH with it, {tx['R_dc_ohm']:g} Ω DC. Its warnings for this board:")
    else:
        est = "The generator's warnings for this board:"
    n, k = st['loops'], r['sectors']
    per = f"{n} electrical period{'s' if n != 1 else ''} per turn; the rotor has {k} sector{'s' if k != 1 else ''}"
    angles = ', '.join(f'{a:g}' for a in st['sweep_angles_mech_deg'])
    return f"""# {spec['board']}

A coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) (`{spec['made_from']}`), set up for Elmer by [`../new_coil.py`](../new_coil.py). The steps that made it are in [S0's README](../S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

## The board

Bore and outer radius {s['bore_and_outer_radius_mm'][0]:g} and {s['bore_and_outer_radius_mm'][1]:g} mm, {len(s['layers'])} copper layers, board {s['board_thickness_mm']:g} mm, air gap {spec['air_gap_mm']:g} mm by default (any other with `--gap`). {per} and repeats itself every {st['rotor_period_mech_deg']:g}°.

{picture}| Coil | Net | Opened at (KiCad mm) | How |
|---|---|---|---|
| TX | `{st['tx']}` | ({t['TX']['ends_xy_kicad'][0]:g}, {t['TX']['ends_xy_kicad'][1]:g}), F.Cu and B.Cu | its two stacked ends |
| SIN | `{sin}` | via at ({t[sin]['via_xy_kicad'][0]:.3f}, {t[sin]['via_xy_kicad'][1]:.3f}) | {t[sin]['source']}; the via is left out |
| COS | `{cos}` | via at ({t[cos]['via_xy_kicad'][0]:.3f}, {t[cos]['via_xy_kicad'][1]:.3f}) | {t[cos]['source']}; the via is left out |

{est}

{w}
## Results at each air gap

Not solved yet. After `python simulation.py` (and `--gap` for each other air gap), this section gets the table of each gap from [`Results/SINCOS_Results.md`](Results/SINCOS_Results.md): the amplitude of SIN and COS, the angle error, the solves passing both checks (the TX's L and R from its voltage against those from the field energy and the eddy power) and L TX over the turn, then the chart of SIN at every gap, `Results/SINCOS_gaps_SIN.webp`.

## The folder

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again |
| [`Elmer Simulation/`](Elmer%20Simulation/) | `test_spec.json` (every board fact the simulation needs), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` (S0's, unchanged), `RotorStator_AngleSetup/` (the rotor over the stator at each angle), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`1mm_AirGap`, `0d5mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

## Running it

{mem}    cd "Elmer Simulation"
    python simulation.py                   # the rotor away, then {angles} degrees
    python simulation.py --gap 0.5         # the same at a 0.5 mm air gap
    python simulation.py --plot            # redraw the table, the curves and SINCOS_Results.md
    python angle_error.py                  # print the angle error at each angle, and rewrite SINCOS_Results.md
    python make_charts.py                  # redraw every chart (WebP) and rewrite SINCOS_Results.md
    python rig_picture.py                  # redraw how the boards sit in Elmer
    python angle_setup.py                  # redraw the rotor at each angle

`SINCOS_Results.md` is rewritten after every solve: each gap's graph with a caption, the fit, the angle error at each angle and every solve.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [../LICENSE.md](../LICENSE.md); this branch's GPL-3.0 covers `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` only.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source', help="the generator's output folder (Stator.kicad_pcb, Rotor.kicad_pcb, Parameters.txt)")
    ap.add_argument('name', help='the new folder, beside this script')
    ap.add_argument('--angles', type=int, default=8, help="angles over one period of the rotor (default 8)")
    ap.add_argument('--level', type=float, default=0.25, help="the mesh level written into test_spec.json")
    ap.add_argument('--no-estimate', action='store_true', help='skip building the mesh to estimate the memory')
    ap.add_argument('--force', action='store_true', help='write into a folder that exists')
    a = ap.parse_args()
    src = Path(a.source).resolve()
    dst = HERE / a.name
    for f in ('Stator.kicad_pcb', 'Rotor.kicad_pcb', 'Parameters.txt'):
        if not (src / f).exists():
            raise SystemExit(f'{src / f} is missing')
    if dst.exists() and not a.force:
        raise SystemExit(f'{dst} exists (--force writes into it)')
    boards, sim, results = dst / 'Boards', dst / 'Elmer Simulation', dst / 'Results'
    for d in (boards, sim, results):
        d.mkdir(parents=True, exist_ok=True)
    text = (src / 'Parameters.txt').read_text()
    spec = spec_from(src, a.name, text, a.angles, a.level)
    expected = spec.pop('expected')
    for f in ('Stator.kicad_pcb', 'Stator.kicad_pro', 'Rotor.kicad_pcb', 'Rotor.kicad_pro'):
        if (src / f).exists():
            shutil.copy2(src / f, boards / f)
    pics = sorted(p.name for p in src.glob('*_Representative.svg')) + sorted(p.name for p in src.glob('*_Actual.svg'))
    for p in pics:
        shutil.copy2(src / p, boards / p)
    (boards / 'Parameters.txt').write_text(re.sub(r'^(folder\s+).*?(/Output/)',
                                                  r'\1<your checkout>/Generators/Single Coil Set Generator\2', text,
                                                  count=1, flags=re.M))
    files = parameter_files(text)
    if files:
        (boards / 'parameter_files').mkdir(exist_ok=True)
        for fname, body in files.items():
            (boards / 'parameter_files' / fname).write_text(body)
    (sim / 'test_spec.json').write_text(json.dumps(spec, indent=1) + '\n')
    (results / 'expected_results.json').write_text(json.dumps(
        dict(board=a.name, source="the generator's estimates, from Parameters.txt (Boards/Parameters.txt)",
             units='H, ohm', **expected), indent=1) + '\n')
    if TEMPLATE.parent.resolve() != sim.resolve():
        for f in SCRIPTS:
            shutil.copy2(TEMPLATE.parent / f, sim / f)
    print(f'wrote {dst}: Boards/ (the boards, Parameters.txt, {len(files)} parameter files, {len(pics)} pictures), '
          f'Elmer Simulation/ (test_spec.json, {", ".join(SCRIPTS)}), Results/ (expected_results.json)')
    mesh = None
    if not a.no_estimate:
        out = sim / 'case' / 'estimate'
        r = subprocess.run([sys.executable, str(sim / 'simulation.py'), '--angles', '0', '--no-away', '--mesh-only',
                            '--out', str(out)], capture_output=True, text=True, cwd=sim, check=False)
        m = re.search(r"mesh (\{.*\})", r.stdout)
        if m:
            mesh = json.loads(m.group(1).replace("'", '"'))
            print(f"one angle's mesh: {mesh['nodes']:,} nodes, about {mesh['nodes'] * KB_PER_NODE / 1e6:.1f} GB a direct "
                  "solve")
        else:
            print('the mesh estimate failed:\n' + (r.stdout + r.stderr)[-2000:])
        shutil.rmtree(out, ignore_errors=True)
    if not (dst / 'README.md').exists() or (a.force and TEMPLATE.parent.parent != dst):
        (dst / 'README.md').write_text(readme(spec, src, warnings(text), mesh, pics[:1], expected))
        print(f'wrote {dst / "README.md"}')


if __name__ == '__main__':
    main()
