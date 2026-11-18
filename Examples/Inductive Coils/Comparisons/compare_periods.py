"""The two-period board (../S0d2_1x_OD23_2L_tiny_TX3top_Cut) against the one-period board with the same TX
(../S0_1x_OD23_2L_tiny_TX3top_Cut): three TX turns on the top layer, 23.4 mm across, opened by cuts, at every air
gap both have.

    python compare_periods.py    prints the comparison as a Markdown table and draws SINCOS_1_vs_2_periods.webp here

The signal is each channel's amplitude, the best sine through the solves over the turn, with the rotor's period (360
degrees for one period per turn, 180 for two). Where at least five solves of a gap are readable
(make_charts.readable: the solve converged, the TX's L from its port and from the field's energy agree within 1 %, R
TX is positive, and M is reciprocal within 1 % where it was checked), the fit goes through those alone; with fewer,
through all of them. The angle error is each board's own (angle_error.py), in electrical degrees, and in mechanical
degrees: the same for one period, half for two. L TX is the mean over the turn. Nothing here is solved. This script
is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BOARDS = HERE.parent
ONE = BOARDS / 'S0_1x_OD23_2L_tiny_TX3top_Cut' / 'Results'
TWO = BOARDS / 'S0d2_1x_OD23_2L_tiny_TX3top_Cut' / 'Results'
sys.path.insert(0, str(ONE.parent / 'Palace Simulation'))         # the boards' own fit and chart style
from angle_error import sine_fit  # noqa: E402
from make_charts import COLOURS, FREQ, INK, INK2, SURFACE, _style, readable, tint  # noqa: E402
GAPS = (0.1, 0.5, 1.0, 1.5, 2.0)


def load(results, gap):
    f = results / f'{gap:g}mm_AirGap'.replace('.', 'd') / f'results_gap{gap:g}mm.json'
    return json.loads(f.read_text()) if f.exists() else None


def summary(res):
    """The amplitudes (readable solves alone where five or more are), the angle error, L TX and the count."""
    ae = res.get('angle_error_deg') or {}
    mech = ae.get('mechanical_per_electrical', 1.0)
    period = 360.0 * mech
    runs = sorted((r for r in res['runs'] if r['rotor_deg'] != 'away'), key=lambda r: r['rotor_deg'])
    ok = [r for r in runs if readable(r['solve'])]
    use = ok if len(ok) >= 5 else runs
    ang = [r['rotor_deg'] for r in use]
    amp = {n: sine_fit(ang, [r['solve']['coils'][n]['M'] * 1e9 for r in use], period)['amplitude']
           for n in ('SIN', 'COS')}
    L = [r['solve']['coils']['TX']['L'] * 1e9 for r in runs]
    return dict(n=len(runs), loose=len(runs) - len(ok), readable=len(ok) >= 5, amp=amp, L=float(np.mean(L)),
                Lr=(min(L), max(L)), rms=ae.get('rms'), peak=ae.get('peak'), mech=mech)


def mv(nh):
    return 2 * math.pi * FREQ * nh * 1e-9 * 1e3


def rows():
    out = []
    for gap in GAPS:
        r1, r2 = load(ONE, gap), load(TWO, gap)
        if r1 and r2:
            out.append((gap, summary(r1), summary(r2)))
    return out


def table():
    head = ('| Air gap | Periods per turn | Amplitude SIN / COS | Angle error, electrical | Angle error, mechanical | '
            'L TX over the turn | Not readable |')
    lines = [head, '|---|---|---|---|---|---|---|']
    for gap, s1, s2 in sorted(rows(), key=lambda x: -x[0]):
        for per, s in (('1', s1), ('2', s2)):
            a = s['amp']
            lines.append(f"| {gap:g} mm | {per} | {a['SIN']:.2f} / {a['COS']:.2f} nH ({mv(a['SIN']):.0f} / "
                         f"{mv(a['COS']):.0f} mV) | {s['rms']:.1f}° rms, {s['peak']:.1f}° peak | "
                         f"{s['rms'] * s['mech']:.2f}° rms, {s['peak'] * s['mech']:.2f}° peak | "
                         f"{s['Lr'][0]:.1f} to {s['Lr'][1]:.1f} nH | {s['loose']} of {s['n']} |")
    return '\n'.join(lines)


def ratios():
    """Two periods over one, per gap where both are readable: SIN, mechanical angle error and L TX."""
    return [(gap, s2['amp']['SIN'] / s1['amp']['SIN'], (s2['rms'] * s2['mech']) / (s1['rms'] * s1['mech']),
             s2['L'] / s1['L']) for gap, s1, s2 in rows() if s1['readable'] and s2['readable']]


def chart(path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    data = rows()
    fig, (ax, ex) = plt.subplots(2, 1, figsize=(8, 7.2), dpi=200, sharex=True, layout='constrained',
                                 gridspec_kw=dict(height_ratios=[3, 1.8]))
    fig.patch.set_facecolor(SURFACE)
    _style(ax, matplotlib)
    _style(ex, matplotlib)
    ax.set_ylabel('amplitude of M (nH)', color=INK2)
    ex.set_ylabel('angle error, mechanical\n(degrees rms)', color=INK2)
    ex.set_xlabel('air gap (mm)', color=INK2)
    g = [d[0] for d in data]
    for k, (per, ls, z) in enumerate((('1', (0, (4, 2)), 3), ('2', '-', 4))):
        for n in ('SIN', 'COS'):
            col = tint(COLOURS[n], 1.0)
            y = [d[1 + k]['amp'][n] for d in data]
            ax.plot(g, y, color=col, lw=1.6 if ls == '-' else 1.2, ls=ls, marker='o', ms=6.5,
                    mfc=col if ls == '-' else SURFACE, mec=col, mew=1.4, zorder=z)
        col = INK if per == '2' else INK2
        e = [d[1 + k]['rms'] * d[1 + k]['mech'] for d in data]
        ex.plot(g, e, color=col, lw=1.6 if ls == '-' else 1.2, ls=ls, marker='o', ms=6,
                mfc=col if ls == '-' else SURFACE, mec=col, mew=1.3, zorder=z)
        ex.text(g[-1] + 0.05, e[-1], f"{per} period{'s' if per == '2' else ''}", color=INK, fontsize=8.5,
                va='center', ha='left')
    ax.set_xlim(0, max(g) + 0.45)
    ex.set_xticks(g)                                   # the gaps solved, not the angles _style sets
    ax.set_ylim(bottom=0)
    ex.set_ylim(0, max(d[k]['rms'] * d[k]['mech'] for d in data for k in (1, 2)) * 1.2)
    fig.suptitle('One period per turn against two: the signal and the mechanical angle error at each air gap',
                 x=0.02, ha='left', color=INK, fontsize=12)
    hs = [Line2D([], [], color=tint(COLOURS['SIN'], 1.0), lw=1.6, marker='o', mfc=tint(COLOURS['SIN'], 1.0),
                 label='SIN, 2 periods'),
          Line2D([], [], color=tint(COLOURS['SIN'], 1.0), lw=1.2, ls=(0, (4, 2)), marker='o', mfc=SURFACE,
                 label='SIN, 1 period'),
          Line2D([], [], color=tint(COLOURS['COS'], 1.0), lw=1.6, marker='o', mfc=tint(COLOURS['COS'], 1.0),
                 label='COS, 2 periods'),
          Line2D([], [], color=tint(COLOURS['COS'], 1.0), lw=1.2, ls=(0, (4, 2)), marker='o', mfc=SURFACE,
                 label='COS, 1 period')]
    fig.legend(handles=hs, frameon=False, fontsize=8, labelcolor=INK, loc='outside lower center', ncol=4)
    fig.savefig(path, facecolor=SURFACE, pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    return path


def main():
    print(table())
    print()
    for gap, s, e, L in ratios():
        print(f'{gap:g} mm: two periods over one, SIN {s:.2f}, mechanical angle error {e:.2f}, L TX {L:.2f}')
    print('wrote', chart(HERE / 'SINCOS_1_vs_2_periods.webp'))


if __name__ == '__main__':
    main()
