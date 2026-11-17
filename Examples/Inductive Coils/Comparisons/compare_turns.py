"""The board with three TX turns on the top layer (../S0_1x_OD23_2L_tiny_TX3top_Cut) against the two-turn board it
grew from (../S0_1x_OD22_2L_tiny_TXtop_Cut), both opened by the same cuts, at every air gap both have.

    python compare_turns.py      prints the comparison as a Markdown table and draws SINCOS_2_vs_3_turns.webp here

The signal is each channel's amplitude, the best sine through the solves. Where at least five solves of a gap
are readable (make_charts.readable: M from the TX to each receiver and back agree within 1 %, and R TX is
positive), the fit goes through those alone; with fewer, through all of them, and the chart draws that point hollow
and ringed, as one not to read. L TX is the mean over the turn. Nothing here is solved. This script is GPL-3.0 as
the bridge.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BOARDS = HERE.parent
THREE = BOARDS / 'S0_1x_OD23_2L_tiny_TX3top_Cut' / 'Results'
TWO = BOARDS / 'S0_1x_OD22_2L_tiny_TXtop_Cut' / 'Results'
sys.path.insert(0, str(THREE.parent / 'FastHenry Simulation'))       # the boards' own fit and chart style
from angle_error import sine_fit  # noqa: E402
from make_charts import COLOURS, FREQ, INK, INK2, PERIOD, SURFACE, _style, readable, tint  # noqa: E402
GAPS = (0.1, 0.5, 1.0, 1.5, 2.0)


def load(results, gap):
    f = results / f'{gap:g}mm_AirGap'.replace('.', 'd') / f'results_gap{gap:g}mm.json'
    return json.loads(f.read_text()) if f.exists() else None


def loose(r):
    return not readable(r['solve'])


def summary(res):
    """The amplitudes (readable solves alone where five or more are), the angle error, L TX and the count."""
    runs = sorted((r for r in res['runs'] if r['rotor_deg'] != 'away'), key=lambda r: r['rotor_deg'])
    ok = [r for r in runs if not loose(r)]
    use = ok if len(ok) >= 5 else runs
    ang = [r['rotor_deg'] for r in use]
    amp = {n: sine_fit(ang, [r['solve']['coils'][n]['M'] * 1e9 for r in use], PERIOD)['amplitude']
           for n in ('SIN', 'COS')}
    L = [r['solve']['coils']['TX']['L'] * 1e9 for r in runs]
    ae = res.get('angle_error_deg') or {}
    away = [r for r in res['runs'] if r['rotor_deg'] == 'away']
    return dict(n=len(runs), loose=len(runs) - len(ok), readable=len(ok) >= 5, amp=amp, L=float(np.mean(L)),
                Lr=(min(L), max(L)), rms=ae.get('rms'), peak=ae.get('peak'),
                away=away[0]['solve']['coils']['TX']['L'] * 1e9 if away else None)


def mv(nh):
    return 2 * math.pi * FREQ * nh * 1e-9 * 1e3


def rows():
    out = []
    for gap in GAPS:
        r2, r3 = load(TWO, gap), load(THREE, gap)
        if r2 and r3:
            out.append((gap, summary(r2), summary(r3)))
    return out


def table():
    lines = ['| Air gap | TX | Amplitude SIN / COS | Fitted through | Angle error | L TX over the turn | Not readable |',
             '|---|---|---|---|---|---|---|']
    for gap, s2, s3 in sorted(rows(), key=lambda x: -x[0]):
        for turns, s in (('2 turns', s2), ('3 turns', s3)):
            a = s['amp']
            lines.append(f"| {gap:g} mm | {turns} | {a['SIN']:.2f} / {a['COS']:.2f} nH ({mv(a['SIN']):.0f} / "
                         f"{mv(a['COS']):.0f} mV) | {'the readable solves' if s['readable'] else 'all solves (fewer than 5 readable)'} | "
                         f"{s['rms']:.1f}° rms, {s['peak']:.1f}° peak | {s['Lr'][0]:.1f} to {s['Lr'][1]:.1f} nH | "
                         f"{s['loose']} of {s['n']} |")
    return '\n'.join(lines)


def ratios():
    """Three turns over two, per gap where both are readable: SIN, COS and L TX."""
    return [(gap, s3['amp']['SIN'] / s2['amp']['SIN'], s3['amp']['COS'] / s2['amp']['COS'], s3['L'] / s2['L'])
            for gap, s2, s3 in rows() if s2['readable'] and s3['readable']]


def chart(path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    data = rows()
    fig, (ax, lx) = plt.subplots(2, 1, figsize=(8, 7.2), dpi=200, sharex=True, layout='constrained',
                                 gridspec_kw=dict(height_ratios=[3, 1.6]))
    fig.patch.set_facecolor(SURFACE)
    _style(ax, matplotlib)
    _style(lx, matplotlib)
    ax.set_ylabel('amplitude of M (nH)', color=INK2)
    lx.set_ylabel('L TX (nH)', color=INK2)
    lx.set_xlabel('air gap (mm)', color=INK2)
    g = [d[0] for d in data]
    for k, (turns, ls, z) in enumerate((('2', (0, (4, 2)), 3), ('3', '-', 4))):
        for n in ('SIN', 'COS'):
            col = tint(COLOURS[n], 1.0)
            y = [d[1 + k]['amp'][n] for d in data]
            ok = [d[1 + k]['readable'] for d in data]
            ax.plot(g, y, color=col, lw=1.6 if ls == '-' else 1.2, ls=ls, zorder=z)
            ax.plot([a for a, o in zip(g, ok) if o], [b for b, o in zip(y, ok) if o], ls='none', marker='o', ms=6.5,
                    mfc=col if ls == '-' else SURFACE, mec=col, mew=1.4, zorder=z + 2)
            bad = [(a, b) for a, b, o in zip(g, y, ok) if not o]
            if bad:
                ax.plot(*zip(*bad), ls='none', marker='o', ms=6.5, mfc=SURFACE, mec=col, mew=1.4, zorder=z + 2)
                ax.plot(*zip(*bad), ls='none', marker='o', ms=13, mfc='none', mec=INK2, mew=0.8, zorder=z + 1)
        col = INK2 if turns == '2' else INK
        lx.plot(g, [d[1 + k]['L'] for d in data], color=col, lw=1.6 if ls == '-' else 1.2, ls=ls, marker='o', ms=6,
                mfc=col if ls == '-' else SURFACE, mec=col, mew=1.3, zorder=z)
        lx.text(g[-1] + 0.05, data[-1][1 + k]['L'], f'{turns} turns', color=INK, fontsize=8.5, va='center',
                ha='left')
    for d in data:
        for k in (1, 2):
            if d[k]['away'] is not None:
                lx.plot([d[0]], [d[k]['away']], ls='none', marker='D', ms=5.5, mfc='none', mec=INK2, mew=1.0,
                        zorder=6)
    ax.set_xlim(0, max(g) + 0.35)
    lx.set_xticks(g)                                   # the gaps solved, not the angles _style sets
    ax.set_ylim(bottom=0)
    lx.set_ylim(0, max(max(d[1]['L'], d[2]['L'], d[1]['away'] or 0, d[2]['away'] or 0) for d in data) * 1.25)
    fig.suptitle('Two TX turns against three: the signal and the TX inductance at each air gap', x=0.02, ha='left',
                 color=INK, fontsize=12)
    hs = [Line2D([], [], color=tint(COLOURS['SIN'], 1.0), lw=1.6, marker='o', mfc=tint(COLOURS['SIN'], 1.0),
                 label='SIN, 3 turns'),
          Line2D([], [], color=tint(COLOURS['SIN'], 1.0), lw=1.2, ls=(0, (4, 2)), marker='o', mfc=SURFACE,
                 label='SIN, 2 turns'),
          Line2D([], [], color=tint(COLOURS['COS'], 1.0), lw=1.6, marker='o', mfc=tint(COLOURS['COS'], 1.0),
                 label='COS, 3 turns'),
          Line2D([], [], color=tint(COLOURS['COS'], 1.0), lw=1.2, ls=(0, (4, 2)), marker='o', mfc=SURFACE,
                 label='COS, 2 turns'),
          Line2D([], [], ls='none', marker='o', ms=11, mfc='none', mec=INK2, label='fewer than 5 solves readable'),
          Line2D([], [], ls='none', marker='D', ms=5.5, mfc='none', mec=INK2, label='L TX, rotor away')]
    fig.legend(handles=hs, frameon=False, fontsize=8, labelcolor=INK, loc='outside lower center', ncol=3)
    fig.savefig(path, facecolor=SURFACE, pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    return path


def main():
    print(table())
    print()
    for gap, s, c, L in ratios():
        print(f'{gap:g} mm: three turns over two, SIN {s:.2f}, COS {c:.2f}, L TX {L:.2f}')
    print('wrote', chart(HERE / 'SINCOS_2_vs_3_turns.webp'))


if __name__ == '__main__':
    main()
