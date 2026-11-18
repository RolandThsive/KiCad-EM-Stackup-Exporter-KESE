"""Draw the comparison charts from data/ (scripts/collect.py writes it) into charts/, as lossless WebP.

    python scripts/charts.py

For each board: <board>.webp (SIN's amplitude, L TX and the angle error against the air gap, one line per solver)
and <board>_1mm.webp (SIN and COS against the rotor angle at 1 mm). For all boards: ratio_to_fasthenry.webp (each
solver's SIN amplitude and L TX over FastHenry's, gap by gap) and proof.webp (the proof boards against their
references). GPL-3.0.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA, CHARTS = ROOT / 'data', ROOT / 'charts'
INK, INK2, GRID, SURFACE = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
# one colour per solver, categorical slots 1 to 4 of the house palette in this fixed order (checked with the palette
# validator: every neighbouring pair clears the colour-blind and normal-vision floors; aqua and yellow are under 3:1
# against the surface, so every line also carries its solver's name or marker, and the README has the tables)
SOLVERS = ('Elmer', 'PyPEEC', 'FastHenry', 'Palace')
COLOUR = {'Elmer': '#2a78d6', 'PyPEEC': '#eb6834', 'FastHenry': '#1baf7a', 'Palace': '#eda100'}
MARKER = {'Elmer': 's', 'Palace': 'D', 'PyPEEC': 'o', 'FastHenry': '^'}     # FEM square and diamond, PEEC round and triangle
KIND = {'Elmer': 'FEM', 'Palace': 'FEM', 'PyPEEC': 'PEEC', 'FastHenry': 'PEEC'}
LABEL = {'S0_1x_OD21_2L_tiny': 'S0 (21 mm, TX one turn on each layer)',
         'S0_1x_OD21_2L_tiny_TXtop': '21 mm, 2 TX turns on top',
         'S0_1x_OD22_2L_tiny_TXtop': '22 mm, 2 TX turns on top',
         'S0_1x_OD22_2L_tiny_TXtop_Cut': '22 mm, 2 TX turns on top, opened by cuts',
         'S0_1x_OD23_2L_tiny_TX3top_Cut': '23 mm, 3 TX turns on top, opened by cuts',
         'S0d2_1x_OD23_2L_tiny_TX3top_Cut': '23 mm, 3 TX turns on top, cuts, 2 periods per turn'}


def rows(name):
    with open(DATA / name) as f:
        out = []
        for r in csv.DictReader(f):
            for k, v in r.items():
                try:
                    r[k] = float(v)
                except (TypeError, ValueError):
                    pass
            out.append(r)
        return out


def complete(s):
    return s['solves'] >= s['solves_wanted'] and s['amp_SIN_nH'] not in ('', None)


def style(ax, matplotlib):
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.margins(y=0.08)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    for sp in ('left', 'bottom'):
        ax.spines[sp].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=8)


def save(fig, path, plt):
    fig.savefig(path, facecolor=SURFACE, pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    return path


def spread(ax, items, x, dx_pt=6, sep_pt=10.5):
    """Write each (y, text) of items at x, offset dx_pt to the right, pushed apart vertically so that no two labels
    are closer than sep_pt (the order is kept and the group stays centred on where the points are)."""
    if not items:
        return
    from matplotlib.transforms import blended_transform_factory, offset_copy
    y0, y1 = ax.get_ylim()
    h_pt = ax.get_window_extent().height * 72 / ax.figure.dpi
    sep = sep_pt / max(h_pt, 1.0)
    items = sorted(((y - y0) / (y1 - y0), s) for y, s in items)
    want = [f for f, _ in items]
    pos = list(want)
    for i in range(1, len(pos)):
        pos[i] = max(pos[i], pos[i - 1] + sep)
    shift = np.mean(np.subtract(want, pos))
    pos = [p + shift for p in pos]
    for i in range(1, len(pos)):             # the shift may have pushed the lowest label under its neighbour's floor
        pos[i] = max(pos[i], pos[i - 1] + sep)
    if pos[0] < sep / 2:                     # keep the group inside the axes, clear of the axis line
        pos = [p + sep / 2 - pos[0] for p in pos]
    elif pos[-1] > 1 - sep / 2:
        pos = [p - (pos[-1] - 1 + sep / 2) for p in pos]
    tr = offset_copy(blended_transform_factory(ax.transData, ax.transAxes), fig=ax.figure, x=dx_pt, y=0, units='points')
    for f, (_, s) in zip(pos, items):
        ax.text(x, f, s, transform=tr, va='center', ha='left', fontsize=8, color=INK, clip_on=False)


def present(rows_, board):
    """The solvers with a finished gap on this board, and those with something solved but no finished gap yet."""
    done = [s for s in SOLVERS if any(r['solver'] == s and r['board'] == board and complete(r) for r in rows_)]
    part = [s for s in SOLVERS if s not in done and any(r['solver'] == s and r['board'] == board and
            (r['solves'] or r.get('L_TX_away_nH') not in ('', None)) for r in rows_)]
    return done, part


def legend(fig, done, part):
    from matplotlib.lines import Line2D
    hs = [Line2D([], [], color=COLOUR[s], lw=2, marker=MARKER[s], ls='-' if KIND[s] == 'PEEC' else (0, (5, 2)),
                 label=f'{s} ({KIND[s]})' + ('' if s in done else ', still solving')) for s in SOLVERS
          if s in done or s in part]
    fig.legend(handles=hs, frameon=False, fontsize=8, labelcolor=INK, loc='outside lower center', ncol=4)


AWAY = 2.5          # where the rotor-away points stand on the gap axis


def board_chart(board, summ, matplotlib, plt):
    fig, axes = plt.subplots(3, 1, figsize=(8, 9.2), dpi=200, sharex=True, layout='constrained')
    fig.patch.set_facecolor(SURFACE)
    panels = (('amp_SIN_nH', "SIN's amplitude (nH)"), ('L_TX_mean_nH', 'L TX, mean over the turn (nH)'),
              ('angle_error_rms_deg', 'angle error, rms (electrical °)'))
    labels = {}
    for ax, (key, lab) in zip(axes, panels):
        style(ax, matplotlib)
        ax.set_ylabel(lab, color=INK2, fontsize=9)
        ends, away = [], []
        for s in SOLVERS:
            pts = sorted((r['gap_mm'], r[key]) for r in summ if r['solver'] == s and r['board'] == board and complete(r))
            if pts:
                x, y = zip(*pts)
                ax.plot(x, y, color=COLOUR[s], lw=2, marker=MARKER[s], ms=6.5, mec=SURFACE, mew=1.2, zorder=3,
                        ls='-' if KIND[s] == 'PEEC' else (0, (5, 2)))
                ends.append((x[-1], y[-1], s))
            if key == 'L_TX_mean_nH':
                aw = [r['L_TX_away_nH'] for r in summ if r['solver'] == s and r['board'] == board
                      and r['L_TX_away_nH'] not in ('', None)]
                if aw:
                    ax.plot([AWAY], [aw[0]], ls='none', marker=MARKER[s], ms=6.5, mfc=SURFACE, mec=COLOUR[s],
                            mew=1.6, zorder=3)
                    away.append((aw[0], s))
        labels[ax] = (ends, away)
        if key == 'L_TX_mean_nH':
            ax.axvline((2.0 + AWAY) / 2, color=GRID, lw=1.2, ls=(0, (2, 2)), zorder=1)
    axes[-1].set_xlabel('air gap (mm)', color=INK2)
    axes[-1].set_xticks([0.1, 0.5, 1.0, 1.5, 2.0, AWAY])
    axes[-1].set_xticklabels(['0.1', '0.5', '1.0', '1.5', '2.0', 'rotor\naway'])
    axes[-1].set_xlim(0, AWAY + 0.55)
    fig.suptitle(LABEL[board], x=0.02, ha='left', color=INK, fontsize=12)
    done, part = present(summ, board)
    legend(fig, done, part)
    fig.canvas.draw()                        # settle the layout, so that the label spacing is measured on the real axes
    for ax, (ends, away) in labels.items():
        by_x = defaultdict(list)
        for x, y, s in ends:
            by_x[x].append((y, s))
        for x, items in by_x.items():
            spread(ax, items, x)
        spread(ax, away, AWAY)
    return save(fig, CHARTS / f'{board}.webp', plt)


def curves_chart(board, solves, matplotlib, plt, gap=1.0):
    fig, axes = plt.subplots(2, 1, figsize=(7.5, 6.6), dpi=200, sharex=True, layout='constrained')
    fig.patch.set_facecolor(SURFACE)
    ends_by_ax = {}
    for ax, n in zip(axes, ('SIN', 'COS')):
        style(ax, matplotlib)
        ax.axhline(0, color=INK2, lw=0.8, zorder=1)
        ax.set_ylabel(f'M from the TX to {n} (nH)', color=INK2, fontsize=9)
        ends = []
        for s in SOLVERS:
            pts = sorted((r['rotor_deg'], r[f'M_{n}_nH']) for r in solves
                         if r['solver'] == s and r['board'] == board and r['gap_mm'] == gap)
            if not pts:
                continue
            x, y = zip(*pts)
            ax.plot(list(x) + [360.0], list(y) + [y[0]], color=COLOUR[s], lw=1.6, marker=MARKER[s], ms=5.5,
                    mec=SURFACE, mew=1.0, ls='-' if KIND[s] == 'PEEC' else (0, (5, 2)), zorder=3,
                    markevery=list(range(len(x))))
            ends.append((y[0], s))
        ends_by_ax[ax] = ends
        ax.set_xlim(0, 410)
        ax.set_xticks(np.linspace(0, 360, 9))
    axes[-1].set_xlabel('rotor angle (degrees)', color=INK2)
    fig.suptitle(f'{LABEL[board]}: the curves at {gap:g} mm', x=0.02, ha='left', color=INK, fontsize=12)
    here = [r for r in solves if r['gap_mm'] == gap]
    legend(fig, [s for s in SOLVERS if any(r['solver'] == s and r['board'] == board for r in here)], [])
    fig.canvas.draw()
    for ax, ends in ends_by_ax.items():
        spread(ax, ends, 360.0)
    return save(fig, CHARTS / f'{board}_{gap:g}mm.webp', plt)


def ratio_chart(summ, matplotlib, plt, ref='FastHenry'):
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.4), dpi=200, sharex=True, layout='constrained')
    fig.patch.set_facecolor(SURFACE)
    base = {(r['board'], r['gap_mm']): r for r in summ if r['solver'] == ref and complete(r)}
    ends = {ax: [] for ax in axes}
    for ax, (key, lab) in zip(axes, (('amp_SIN_nH', "SIN's amplitude over FastHenry's"),
                                     ('L_TX_mean_nH', "L TX over FastHenry's"))):
        style(ax, matplotlib)
        ax.axhline(1, color=INK2, lw=0.8, zorder=1)
        ax.set_title(lab, color=INK, fontsize=10, loc='left')
        for k, s in enumerate(s for s in SOLVERS if s != ref):
            by_gap = defaultdict(list)
            for r in summ:
                b = base.get((r['board'], r['gap_mm']))
                if r['solver'] == s and b and complete(r):
                    by_gap[r['gap_mm']].append(r[key] / b[key])
            if not by_gap:
                continue
            g = sorted(by_gap)
            mean = [np.mean(by_gap[x]) for x in g]
            lo = [min(by_gap[x]) for x in g]
            hi = [max(by_gap[x]) for x in g]
            dx = (k - 1) * 0.04
            ax.errorbar([x + dx for x in g], mean, yerr=[np.subtract(mean, lo), np.subtract(hi, mean)],
                        color=COLOUR[s], lw=1.8, marker=MARKER[s], ms=6.5, mec=SURFACE, mew=1.2, capsize=3,
                        ls='-' if KIND[s] == 'PEEC' else (0, (5, 2)), zorder=3, label=f'{s} ({KIND[s]})')
            ends[ax].append((g[-1] + dx, mean[-1], s))
        ax.set_xlabel('air gap (mm)', color=INK2)
        ax.set_xticks([0.1, 0.5, 1.0, 1.5, 2.0])
        ax.set_xlim(0, 2.45)
    fig.suptitle('Each solver against FastHenry: the mean over the boards solved, and the range', x=0.02, ha='left',
                 color=INK, fontsize=12)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=8, labelcolor=INK, loc='outside lower center', ncol=3)
    fig.canvas.draw()
    for ax, e in ends.items():
        if e:
            spread(ax, [(y, s) for _, y, s in e], max(x for x, _, _ in e))
    return save(fig, CHARTS / 'ratio_to_fasthenry.webp', plt)


def proof_chart(proof, matplotlib, plt):
    cases = [('E01_circular_loop', 1e4, 'E01, L, 10 kHz'), ('E01_circular_loop', 3.5e6, 'E01, L, 3.5 MHz'),
             ('E02_coaxial_loops', 1e4, 'E02, M, 10 kHz'), ('E02_coaxial_loops', 3.5e6, 'E02, M, 3.5 MHz')]
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200, layout='constrained')
    fig.patch.set_facecolor(SURFACE)
    style(ax, matplotlib)
    ax.axvline(0, color=INK2, lw=0.8)
    for i, (b, f, lab) in enumerate(cases):
        for k, s in enumerate(SOLVERS):
            pts = [r for r in proof if r['solver'] == s and r['board'] == b and r['frequency_hz'] == f
                   and r['file'] == 'results.json' and r['error_pct'] not in ('', None)]
            for r in pts:
                y = i + (k - 1.5) * 0.17
                ax.plot([r['error_pct']], [y], ls='none', marker=MARKER[s], ms=7, color=COLOUR[s], mec=SURFACE,
                        mew=1.0, zorder=3)
                ax.annotate(f"{s} {r['error_pct']:+.2f} %", (r['error_pct'], y), xytext=(7, 0),
                            textcoords='offset points', va='center', fontsize=7, color=INK)
    ax.set_yticks(range(len(cases)))
    ax.set_yticklabels([c[2] for c in cases], color=INK)
    ax.invert_yaxis()
    ax.set_xlabel('error against the reference (%)', color=INK2)
    fig.suptitle('The proof boards: each solver against the same reference', x=0.02, ha='left', color=INK, fontsize=12)
    return save(fig, CHARTS / 'proof.webp', plt)


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    CHARTS.mkdir(exist_ok=True)
    summ, solves, proof = rows('summary.csv'), rows('solves.csv'), rows('proof.csv')
    for b in LABEL:
        print('wrote', board_chart(b, summ, matplotlib, plt).name)
        print('wrote', curves_chart(b, solves, matplotlib, plt).name)
    print('wrote', ratio_chart(summ, matplotlib, plt).name)
    print('wrote', proof_chart(proof, matplotlib, plt).name)


if __name__ == '__main__':
    main()
