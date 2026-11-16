"""The charts of the results, as lossless WebP: each air gap's beside its results in ../Results/<gap>_AirGap, the
chart of every gap together in ../Results. simulation.py calls it after every solve; run on its own
it redraws every chart from the results already there and rewrites SINCOS_Results.md.

    python make_charts.py

    results_gap<gap>mm.webp   SIN and COS against the rotor's angle at one air gap: a dot for each Elmer solve, a
                              solid line joining them, and a dotted line for the ideal sine and cosine (each
                              channel's best sine fit, what the angle error is measured against)
    SINCOS_gaps.webp          every air gap on one chart, once two are solved
    results_gap<gap>mm_SIN.webp, results_gap<gap>mm_COS.webp
                              one channel alone at one air gap, on its own scale, and below it each solve's
                              distance from the ideal curve; a ring marks a solve that did not converge
    SINCOS_gaps_SIN.webp, SINCOS_gaps_COS.webp
                              one channel at every air gap, the same way

The one-channel charts are for judging the solves closely; SINCOS_Results.md shows only the first two kinds.

This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BOARD = HERE.parent
RESULTS = BOARD / 'Results'
sys.path.insert(0, str(HERE))
from angle_error import results_files, sine_fit   # noqa: E402

SPEC = json.loads((HERE / 'test_spec.json').read_text())
PERIOD = SPEC['sets'][0].get('rotor_period_mech_deg', 360.0)
FREQ = SPEC['sets'][0]['f_Hz']
INK, INK2, GRID, SURFACE = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
COLOURS = {'SIN': (0x2a, 0x78, 0xd6), 'COS': (0xeb, 0x68, 0x34)}    # categorical slots 1 and 2 of the house palette
DOTS = (0, (1, 2.2))                  # the ideal curves: dotted, so they never read as solves
LOOSE = 5e-4      # a solve that stopped above this residual, or gives the TX a negative resistance, is not converged
          # enough to read (every 1 mm solve stopped below it); simulation.py uses it too


def tint(rgb, k):
    """The colour mixed with the chart's surface: k = 1 is the colour itself."""
    return '#' + ''.join(f'{round(c * k + s * (1 - k)):02x}' for c, s in zip(rgb, (0xfc, 0xfc, 0xfb), strict=True))


def curves_of(res_file):
    """The solved angles and the two curves (nH) of a results file."""
    res = json.loads(Path(res_file).read_text())
    runs = sorted((r for r in res['runs'] if r['rotor_deg'] != 'away'), key=lambda r: r['rotor_deg'])
    ang = [r['rotor_deg'] for r in runs]
    return (res, ang, [r['solve']['coils']['SIN']['M'] * 1e9 for r in runs],
            [r['solve']['coils']['COS']['M'] * 1e9 for r in runs])


def _axes(title, subtitle):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    _style(ax, matplotlib, title, subtitle)
    ax.set_xlabel('rotor angle (degrees)', color=INK2)
    return plt, fig, ax


def _style(ax, matplotlib, title=None, subtitle=None):
    ax.set_facecolor(SURFACE)
    ax.axhline(0, color=INK2, lw=0.8, zorder=1)
    ax.set_xlim(0, PERIOD)
    ax.set_xticks(np.linspace(0, PERIOD, 9))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g'))
    ax.set_ylabel('M from the TX (nH)', color=INK2)
    if title:
        ax.set_title(title, color=INK, fontsize=11, loc='left', pad=20)
        ax.text(0, 1.015, subtitle, transform=ax.transAxes, fontsize=8, color=INK2, va='bottom')
    ax.grid(True, color=GRID, lw=0.6)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=INK2, labelsize=8)


def _panels(title, subtitle):
    """Two panels over the same angles: a channel's curve above, each solve's distance from its ideal curve below."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    fig, (ax, dx) = plt.subplots(2, 1, figsize=(8, 6.6), dpi=200, sharex=True, layout='constrained',
                                 gridspec_kw=dict(height_ratios=[3, 1.3]))
    fig.patch.set_facecolor(SURFACE)
    _style(ax, matplotlib, title, subtitle)
    _style(dx, matplotlib)
    dx.set_ylabel('solve minus ideal (nH)', color=INK2)
    dx.set_xlabel('rotor angle (degrees)', color=INK2)
    ax.margins(y=0.08)
    dx.margins(y=0.2)                                   # room for the rings round the farthest solves
    return plt, fig, ax, dx


def _save(plt, fig, ax, path, ncol):
    ax.legend(frameon=False, fontsize=8, labelcolor=INK, loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=ncol)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE, pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    return path


def _draw(ax, ang, y, name, col, whole, ideal=True, label=None, end_label=None):
    """One channel: the ideal curve dotted (its best sine), the solves joined by a solid line, a dot for each."""
    tt = np.linspace(0, PERIOD, 721)
    if ideal and len(y) >= 3:
        f = sine_fit(ang, y, PERIOD)
        keep = np.ones_like(tt, bool) if whole else (tt >= min(ang)) & (tt <= max(ang))
        yy = f['offset'] + f['amplitude'] * np.sin(np.radians(tt[keep] * 360.0 / PERIOD + f['phase_deg']))
        ax.plot(tt[keep], yy, color=col, lw=1.3, ls=DOTS, alpha=0.75, zorder=2)
    xs, ys = list(ang), list(y)                      # round to the start of the period once the turn is covered
    if whole and min(ang) == 0:
        xs, ys = xs + [PERIOD], ys + [y[0]]
    ax.plot(xs, ys, color=col, lw=1.6, zorder=3)
    ax.plot(ang, y, ls='none', color=col, marker='o', ms=6.5, mec=SURFACE, mew=1.4, zorder=4)
    ax.plot([], [], color=col, lw=1.6, marker='o', ms=6, mec=SURFACE, label=label or name)
    return (xs[-1], ys[-1], end_label, col) if whole and end_label else None


def _end_labels(ax, labels):
    """Each curve's name just right of its end, spread apart so that no two overlap: the names keep their order
    from bottom to top, stay at least one line apart, and sit as near their ends as that allows; a thin line in
    the curve's colour joins each name to its curve's end."""
    labels = [x for x in labels if x]
    if not labels:
        return
    lo, hi = ax.get_ylim()
    line = 0.06 * (hi - lo)                              # one line of 8.5 pt text on these 4.6 in tall charts
    labels.sort(key=lambda x: x[1])
    ys = [y for _, y, _, _ in labels]
    placed = list(ys)
    for i in range(1, len(placed)):                      # push each name up clear of the one below it
        placed[i] = max(placed[i], placed[i - 1] + line)
    shift = (sum(placed) - sum(ys)) / len(ys)            # then move the block back so that, on average, the names
    placed = [y - shift for y in placed]                 # sit on their ends
    over, under = placed[-1] - (hi - 0.02 * (hi - lo)), (lo + 0.02 * (hi - lo)) - placed[0]
    placed = [y - over for y in placed] if over > 0 else [y + under for y in placed] if under > 0 else placed
    dx = 0.035 * PERIOD
    for (x, y, text, col), yt in zip(labels, placed, strict=True):
        ax.annotate(text, (x, y), xytext=(x + dx, yt), textcoords='data', va='center', ha='left', color=INK,
                    fontsize=8.5, annotation_clip=False,
                    arrowprops=dict(arrowstyle='-', color=col, lw=0.7, shrinkA=0, shrinkB=2))


def gap_chart(res_file):
    """results_gap<gap>mm.webp beside the results file; None while fewer than one angle is solved."""
    res, ang, ms, mc = curves_of(res_file)
    if not ang:
        return None
    whole = len(ang) >= 3 and max(ang) - min(ang) >= 0.75 * PERIOD
    gap, level = res['gap_mm'], res['level']
    plt, fig, ax = _axes(f'{res["board"]}: SIN and COS against the rotor angle, {gap:g} mm air gap',
                         f'1 A at {FREQ / 1e6:g} MHz in the TX; solid: the solves joined; dotted: the ideal curves, '
                         f'each channel\'s best sine{"" if whole else ", between the solved angles for now"}; '
                         f'mesh level {level:g}')
    _end_labels(ax, [_draw(ax, ang, y, name, tint(COLOURS[name], 1.0), whole, label=f'{name}: one Elmer solve per dot',
                           end_label=name) for name, y in (('SIN', ms), ('COS', mc))])
    if len(ang) >= 3:
        ax.plot([], [], color=INK2, lw=1.3, ls=DOTS, label='ideal sine and cosine (best fit)')
    for name in ('SIN', 'COS'):
        channel_chart(res_file, name)
    return _save(plt, fig, ax, Path(res_file).with_suffix('.webp'), 3)


def gaps_chart(results):
    """SINCOS_gaps.webp: every air gap's solves on one chart, the smallest gap in full colour and the larger ones
    lighter; `results` is a list of results files. None with fewer than two gaps of three angles or more."""
    data = []
    for f in results:
        res, ang, ms, mc = curves_of(f)
        if len(ang) >= 3:
            data.append((res['gap_mm'], ang, ms, mc))
    if len(data) < 2:
        return None
    data.sort(key=lambda d: d[0])
    plt, fig, ax = _axes(f'{BOARD.name}: SIN and COS at each air gap',
                         f'1 A at {FREQ / 1e6:g} MHz in the TX; a dot for each solve, joined; dotted: each gap\'s '
                         'ideal curves; the smallest gap in full colour')
    ends = []
    for j, (gap, ang, ms, mc) in enumerate(data):
        k = 1.0 - 0.5 * j / (len(data) - 1)
        whole = max(ang) - min(ang) >= 0.75 * PERIOD
        for name, y in (('SIN', ms), ('COS', mc)):
            ends.append(_draw(ax, ang, y, name, tint(COLOURS[name], k), whole, label=f'{name}, {gap:g} mm',
                              end_label=f'{name} {gap:g} mm'))
    _end_labels(ax, ends)
    ax.plot([], [], color=INK2, lw=1.3, ls=DOTS, label='ideal sine and cosine (best fit)')
    for name in ('SIN', 'COS'):
        channel_gaps_chart(results, name)
    return _save(plt, fig, ax, RESULTS / 'SINCOS_gaps.webp', min(2 * len(data) + 1, 4))   # at most 4 a row


def _loose(res):
    """The rotor angles of a results file whose solves are not converged enough to read (see LOOSE)."""
    return {r['rotor_deg'] for r in res['runs'] if r['rotor_deg'] != 'away'
            and (r['solve']['residual'] > LOOSE or r['solve']['coils']['TX']['R'] < 0)}


def _ideal(ang, y):
    """The best sine through the solves, at the solved angles, and the fit itself."""
    f = sine_fit(ang, y, PERIOD)
    return f['offset'] + f['amplitude'] * np.sin(np.radians(np.asarray(ang) * 360.0 / PERIOD + f['phase_deg'])), f


def _rings(axes, ang, ys, loose):
    """A ring round every solve that is not converged, on each of the axes (ys: the values on each)."""
    for ax, y in zip(axes, ys, strict=True):
        pts = [(a, v) for a, v in zip(ang, y, strict=True) if a in loose]
        if pts:
            ax.plot(*zip(*pts), ls='none', marker='o', ms=12, mfc='none', mec=INK, mew=1.0, zorder=5, clip_on=False)


def _save2(plt, fig, ax, dx, path, ncol):
    h, lab = ax.get_legend_handles_labels()
    fig.legend(h, lab, frameon=False, fontsize=8, labelcolor=INK, loc='outside lower center', ncol=ncol)
    fig.savefig(path, facecolor=SURFACE, pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    return path


def channel_chart(res_file, name):
    """results_gap<gap>mm_<name>.webp beside the results file: SIN or COS alone at one air gap, on its own scale,
    and below it each solve's distance from the ideal curve. None with fewer than four angles (a sine passes
    through any three)."""
    res, ang, ms, mc = curves_of(res_file)
    if len(ang) < 4:
        return None
    y = np.asarray(ms if name == 'SIN' else mc)
    whole = max(ang) - min(ang) >= 0.75 * PERIOD
    gap, loose = res['gap_mm'], _loose(res)
    ideal, f = _ideal(ang, y)
    rms = f['rms_left']
    plt, fig, ax, dx = _panels(f'{res["board"]}: {name} against the rotor angle, {gap:g} mm air gap',
                               f'1 A at {FREQ / 1e6:g} MHz; ideal {f["offset"]:.3f} + {f["amplitude"]:.3f} sin(θ '
                               f'{"+" if f["phase_deg"] >= 0 else "−"} {abs(f["phase_deg"]):.1f}°) nH; the solves stray '
                               f'{rms:.3f} nH rms from it ({100 * rms / f["amplitude"]:.1f} % of the amplitude)')
    col = tint(COLOURS[name], 1.0)
    _draw(ax, ang, y, name, col, whole, label=f'{name}: one Elmer solve per dot')
    dx.plot(ang, y - ideal, color=col, lw=1.3, marker='o', ms=5.5, mec=SURFACE, mew=1.2, zorder=3)
    _rings((ax, dx), ang, (y, y - ideal), loose)
    ax.plot([], [], color=INK2, lw=1.3, ls=DOTS, label='ideal (best sine fit)')
    if loose:
        ax.plot([], [], ls='none', marker='o', ms=10, mfc='none', mec=INK, mew=1.0,
                label=f'not converged (residual above {LOOSE:.0e} or R_TX below 0)')
    return _save2(plt, fig, ax, dx, Path(res_file).with_name(f'results_gap{gap:g}mm_{name}.webp'), 3)


def channel_gaps_chart(results, name):
    """SINCOS_gaps_<name>.webp: SIN or COS at every air gap, the smallest gap in full colour, and below it each
    solve's distance from its own gap's ideal curve. None with fewer than two gaps of four angles or more."""
    data = []
    for f in results:
        res, ang, ms, mc = curves_of(f)
        if len(ang) >= 4:
            data.append((res['gap_mm'], ang, np.asarray(ms if name == 'SIN' else mc), _loose(res)))
    if len(data) < 2:
        return None
    data.sort(key=lambda d: d[0])
    plt, fig, ax, dx = _panels(f'{BOARD.name}: {name} at each air gap',
                               f'1 A at {FREQ / 1e6:g} MHz in the TX; a dot for each solve, joined; dotted: each gap\'s '
                               'ideal curve; the smallest gap in full colour')
    ends, any_loose = [], False
    for j, (gap, ang, y, loose) in enumerate(data):
        col = tint(COLOURS[name], 1.0 - 0.5 * j / (len(data) - 1))
        whole = max(ang) - min(ang) >= 0.75 * PERIOD
        ideal, _ = _ideal(ang, y)
        ends.append(_draw(ax, ang, y, name, col, whole, label=f'{name}, {gap:g} mm', end_label=f'{gap:g} mm'))
        dx.plot(ang, y - ideal, color=col, lw=1.3, marker='o', ms=5.5, mec=SURFACE, mew=1.2, zorder=3)
        _rings((ax, dx), ang, (y, y - ideal), loose)
        any_loose |= bool(loose)
    _end_labels(ax, ends)
    ax.plot([], [], color=INK2, lw=1.3, ls=DOTS, label='ideal (best sine fit)')
    if any_loose:
        ax.plot([], [], ls='none', marker='o', ms=10, mfc='none', mec=INK, mew=1.0,
                label=f'not converged (residual above {LOOSE:.0e} or R_TX below 0)')
    return _save2(plt, fig, ax, dx, RESULTS / f'SINCOS_gaps_{name}.webp', 3)


def all_results():
    """The results files of the default mesh and solver, one per air gap, the largest gap first."""
    return [p for _, p in results_files(RESULTS)]


def main():
    files = all_results()
    for f in files:
        print('wrote', gap_chart(f))
    g = gaps_chart(files)
    if g:
        print('wrote', g)
    import simulation                                   # the page is simulation.py's
    simulation.report()


if __name__ == '__main__':
    main()
