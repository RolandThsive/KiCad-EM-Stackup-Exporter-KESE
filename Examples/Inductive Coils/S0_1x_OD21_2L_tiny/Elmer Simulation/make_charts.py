"""The charts of the results, as lossless WebP: each air gap's beside its results in ../Results/<gap>_AirGap, the
chart of every gap together in ../Results. simulation.py calls it after every solve; run on its own
it redraws every chart from the results already there and rewrites SINCOS_Results.md.

    python make_charts.py

    results_gap<gap>mm.webp   SIN and COS against the rotor's angle at one air gap: a dot for each Elmer solve, a
                              solid line joining them, and dashes for the ideal sine and cosine (each channel's best
                              sine fit, what the angle error is measured against)
    SINCOS_gaps.webp          every air gap on one chart, once two are solved

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
DASH = (0, (5, 3))


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
    ax.set_facecolor(SURFACE)
    ax.axhline(0, color=INK2, lw=0.8, zorder=1)
    ax.set_xlim(0, PERIOD)
    ax.set_xticks(np.linspace(0, PERIOD, 9))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g'))
    ax.set_xlabel('rotor angle (degrees)', color=INK2)
    ax.set_ylabel('M from the TX (nH)', color=INK2)
    ax.set_title(title, color=INK, fontsize=11, loc='left', pad=20)
    ax.text(0, 1.015, subtitle, transform=ax.transAxes, fontsize=8, color=INK2, va='bottom')
    ax.grid(True, color=GRID, lw=0.6)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=INK2, labelsize=8)
    return plt, fig, ax


def _save(plt, fig, ax, path, ncol):
    ax.legend(frameon=False, fontsize=8, labelcolor=INK, loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=ncol)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE, pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    return path


def _draw(ax, ang, y, name, col, whole, ideal=True, label=None, end_label=None):
    """One channel: the ideal curve dashed (its best sine), the solves joined by a solid line, a dot for each."""
    tt = np.linspace(0, PERIOD, 721)
    if ideal and len(y) >= 3:
        f = sine_fit(ang, y, PERIOD)
        keep = np.ones_like(tt, bool) if whole else (tt >= min(ang)) & (tt <= max(ang))
        yy = f['offset'] + f['amplitude'] * np.sin(np.radians(tt[keep] * 360.0 / PERIOD + f['phase_deg']))
        ax.plot(tt[keep], yy, color=col, lw=1.3, ls=DASH, alpha=0.75, zorder=2)
    xs, ys = list(ang), list(y)                      # round to the start of the period once the turn is covered
    if whole and min(ang) == 0:
        xs, ys = xs + [PERIOD], ys + [y[0]]
    ax.plot(xs, ys, color=col, lw=1.6, zorder=3)
    ax.plot(ang, y, ls='none', color=col, marker='o', ms=6.5, mec=SURFACE, mew=1.4, zorder=4)
    ax.plot([], [], color=col, lw=1.6, marker='o', ms=6, mec=SURFACE, label=label or name)
    if whole and end_label:
        ax.annotate(end_label, (xs[-1], ys[-1]), xytext=(6, 0), textcoords='offset points', va='center',
                    color=INK, fontsize=8.5, annotation_clip=False)


def gap_chart(res_file):
    """results_gap<gap>mm.webp beside the results file; None while fewer than one angle is solved."""
    res, ang, ms, mc = curves_of(res_file)
    if not ang:
        return None
    whole = len(ang) >= 3 and max(ang) - min(ang) >= 0.75 * PERIOD
    gap, level = res['gap_mm'], res['level']
    plt, fig, ax = _axes(f'{res["board"]}: SIN and COS against the rotor angle, {gap:g} mm air gap',
                         f'1 A at {FREQ / 1e6:g} MHz in the TX; solid: the solves joined; dashes: the ideal curves, '
                         f'each channel\'s best sine{"" if whole else ", between the solved angles for now"}; '
                         f'mesh level {level:g}')
    for name, y in (('SIN', ms), ('COS', mc)):
        _draw(ax, ang, y, name, tint(COLOURS[name], 1.0), whole, label=f'{name}: one Elmer solve per dot',
              end_label=name)
    if len(ang) >= 3:
        ax.plot([], [], color=INK2, lw=1.3, ls=DASH, label='ideal sine and cosine (best fit)')
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
                         f'1 A at {FREQ / 1e6:g} MHz in the TX; a dot for each solve, joined; the smallest gap in '
                         'full colour')
    for j, (gap, ang, ms, mc) in enumerate(data):
        k = 1.0 - 0.5 * j / (len(data) - 1)
        whole = max(ang) - min(ang) >= 0.75 * PERIOD
        for name, y in (('SIN', ms), ('COS', mc)):
            _draw(ax, ang, y, name, tint(COLOURS[name], k), whole, ideal=False, label=f'{name}, {gap:g} mm',
                  end_label=f'{name} {gap:g} mm')
    return _save(plt, fig, ax, RESULTS / 'SINCOS_gaps.webp', 2 * len(data))


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
