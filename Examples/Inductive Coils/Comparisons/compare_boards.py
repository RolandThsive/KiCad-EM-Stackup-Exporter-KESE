"""The S0 boards side by side, from each board's own results (../<board>/Results).

    python compare_boards.py     prints two Markdown tables: S0 against the two boards with the TX on the top layer,
                                 gap by gap; and every board's SIN amplitude from 0.1 to 2 mm

In the first table the amplitude is each board's best sine through all its solves, as on its own results page. In
the second it goes through the readable solves alone where at least five are readable, and is marked with ? where
fewer are. A solve is readable when the TX's L and R from its voltage agree with L from the field energy and R from
the eddy power and R is positive (readable() in the boards' make_charts.py).
Nothing here is solved. This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARDS = HERE.parent
FREQ = 3.5e6
GAPS = (2.0, 1.5, 1.0, 0.5, 0.1)
TX_ON_TOP = (('S0_1x_OD21_2L_tiny', 'S0 (21 mm, TX one turn on each layer)'),
             ('S0_1x_OD21_2L_tiny_TXtop', '21 mm, 2 TX turns on top'),
             ('S0_1x_OD22_2L_tiny_TXtop', "22 mm, 2 TX turns on top, S0's RX"))
ALL = (('S0_1x_OD21_2L_tiny', 'S0'), ('S0_1x_OD21_2L_tiny_TXtop', '21 mm, 2 TX turns on top'),
       ('S0_1x_OD22_2L_tiny_TXtop', '22 mm, 2 TX turns on top'),
       ('S0_1x_OD22_2L_tiny_TXtop_Cut', '22 mm, 2 TX turns on top, opened by cuts'),
       ('S0_1x_OD23_2L_tiny_TX3top_Cut', '23 mm, 3 TX turns on top, opened by cuts'))


sys.path.insert(0, str(BOARDS / 'S0_1x_OD21_2L_tiny' / 'Elmer Simulation'))   # the boards' own check
from make_charts import readable


def load(board, gap):
    f = BOARDS / board / 'Results' / f'{gap:g}mm_AirGap'.replace('.', 'd') / f'results_gap{gap:g}mm.json'
    return json.loads(f.read_text()) if f.exists() else None


def runs_of(res):
    return [r for r in res['runs'] if r['rotor_deg'] != 'away']


def loose(r):
    return not readable(r['solve'])


def checks(runs):
    """The worst disagreement of L (voltage against field energy) and R (voltage against eddy power) over the solves."""
    worst = 0.0
    for r in runs:
        s, tx = r['solve'], r['solve']['coils']['TX']
        if s.get('L_from_energy_h') is None or s.get('R_from_power_ohm') is None:
            return 'not checked'
        worst = max(worst, abs(s['L_from_energy_h'] - tx['L']) / tx['L'], abs(s['R_from_power_ohm'] - tx['R']) / abs(tx['R']))
    return f'within {worst * 100:.3f} %'


def mv(nh):
    return 2 * math.pi * FREQ * nh * 1e-9 * 1e3


def sine_amplitude(ang, y):
    """The amplitude of the best sine of one period per turn through (ang, y), by least squares."""
    import numpy as np
    t = np.radians(np.asarray(ang, float))
    a = np.column_stack([np.ones_like(t), np.sin(t), np.cos(t)])
    c = np.linalg.lstsq(a, np.asarray(y, float), rcond=None)[0]
    return float(math.hypot(c[1], c[2]))


def tx_on_top_table():
    rows = ['| Air gap | Board | Angles | Amplitude SIN / COS | Angle error | SIN to COS | L TX over the turn | '
            'L and R checks | Not readable |', '|---|---|---|---|---|---|---|---|---|']
    for gap in GAPS:
        for board, label in TX_ON_TOP:
            r = load(board, gap)
            if not r:
                continue
            runs = runs_of(r)
            fs, fc = r['fit_nH']['SIN']['amplitude'], r['fit_nH']['COS']['amplitude']
            ae = r['angle_error_deg']
            L = [x['solve']['coils']['TX']['L'] * 1e9 for x in runs]
            rows.append(f"| {gap:g} mm | {label} | {len(runs)} of 8 | {fs:.2f} / {fc:.2f} nH ({mv(fs):.0f} / {mv(fc):.0f} mV) "
                        f"| {ae['rms']:.1f}° rms, {ae['peak']:.1f}° peak | {ae['sin_to_cos_deg']:.1f}° | "
                        f"{min(L):.1f} to {max(L):.1f} nH | {checks(runs)} | "
                        f"{sum(loose(x) for x in runs)} of {len(runs)} |")
    return '\n'.join(rows)


def signal_table(gaps=(0.1, 0.5, 1.0, 1.5, 2.0)):
    rows = ['| Board | ' + ' | '.join(f'SIN at {g:g} mm' for g in gaps) + ' |', '|---|' + '---|' * len(gaps)]
    for board, label in ALL:
        cells = []
        for g in gaps:
            r = load(board, g)
            if not r:
                cells.append('not solved')
                continue
            runs = runs_of(r)
            ok = [x for x in runs if not loose(x)]
            use = ok if len(ok) >= 5 else runs
            a = sine_amplitude([x['rotor_deg'] for x in use], [x['solve']['coils']['SIN']['M'] * 1e9 for x in use])
            cells.append(f'{a:.2f} nH' + ('' if len(ok) >= 5 else ' ?')
                         + (f' ({len(runs) - len(ok)} of {len(runs)} not readable)' if len(ok) < len(runs) else ''))
        rows.append(f'| [{label}](../{board}/) | ' + ' | '.join(cells) + ' |')
    return '\n'.join(rows)


def main():
    print(tx_on_top_table())
    print()
    print(signal_table())


if __name__ == '__main__':
    main()
