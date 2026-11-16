"""E01's and E02's pictures for the wiki, from Elmer's own output: nothing here is drawn by hand.

    python make_pictures.py [--out DIR]

Reads results.json (and results_grade.json, results_domain120.json, results_fields.json when present) beside this
file, ../E02_coaxial_loops/results.json, and the residual histories in residuals.json. residuals.json is collected
from the ElmerSolver logs under case/ when they are there (they are not committed), so the chart can be drawn again
without them. Writes lossless WebP files into DIR (default pictures/), laid out as the wiki keeps them:

    elmerresults_1_against_reference.webp                     L (E01) and M (E02) against their references
    E01_circular_loop/elmerresults_2_residual.webp            the linear solver's residual against its iterations
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E02 = HERE.parent / 'E02_coaxial_loops'

INK, INK2, GRID, SURFACE = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
BLUE, ORANGE, AQUA, VIOLET = '#2a78d6', '#eb6834', '#1baf7a', '#8a5cd1'


def style(ax, xlabel, ylabel):
    ax.set_facecolor(SURFACE)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_xlabel(xlabel, color=INK2, fontsize=10)
    ax.set_ylabel(ylabel, color=INK2, fontsize=10)


def save(fig, path):
    fig.savefig(path, format='webp', dpi=200, facecolor=SURFACE, pil_kwargs=dict(lossless=True))
    print('wrote', path)


def solve(run, f):
    return next((s for s in run['solves'] if s['frequency_hz'] == f), None)


def collect_residuals():
    """{label: [[iteration, residual], ...]} from the logs under case/, merged into residuals.json."""
    path = HERE / 'residuals.json'
    data = json.loads(path.read_text()) if path.exists() else {}
    for level in ('0.75', '1', '1.3'):
        for f, tag in ((1e4, 'f10000'), (3.5e6, 'f3.5e06')):
            log = HERE / 'case' / f'order1_level{level}' / f'{tag}.log'
            if not log.exists():
                continue
            part = log.read_text(errors='replace').split('WhitneyAVHarmonicSolver: Solving', 1)[-1]
            rows = [[int(a), float(b)] for a, b in re.findall(r'^\s*(\d+)\s+([0-9.]+E[+-]\d+)\s*$', part, re.M)]
            if rows:
                data[f'level {level}, {f / 1e3:g} kHz' if f < 1e6 else f'level {level}, {f / 1e6:g} MHz'] = rows
    path.write_text(json.dumps(data, indent=0))
    return data


def chart_reference(out, plt):
    r1 = json.loads((HERE / 'results.json').read_text())
    r2 = json.loads((E02 / 'results.json').read_text())
    l_ref, m_ref = r1['references']['L_open_dc_h'], r2['references']['M_open_h']
    e01 = sorted((run['nodes'], solve(run, 1e4)['coils']['LOOP']['L']) for run in r1['runs'] if solve(run, 1e4))
    e02 = sorted((run['nodes'], solve(run, 1e4)['coils']['RX']['M']) for run in r2['runs'] if solve(run, 1e4))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    fig.patch.set_facecolor(SURFACE)
    ax.axhline(0, color=INK2, lw=2, ls='--', label='the reference')
    n, v = zip(*e01)
    ax.plot(np.array(n) / 1e3, (np.array(v) / l_ref - 1) * 100, color=BLUE, lw=2, marker='o', ms=8,
            markeredgecolor=SURFACE, markeredgewidth=2, label="E01: L, against Grover's ring formula")
    n, v = zip(*e02)
    ax.plot(np.array(n) / 1e3, (np.array(v) / m_ref - 1) * 100, color=ORANGE, lw=2, marker='s', ms=8,
            markeredgecolor=SURFACE, markeredgewidth=2, label="E02: M, against Maxwell's formula")
    for name, color, marker, label in (('results_grade.json', AQUA, 'D', 'E01: L, the air graded twice as finely'),
                                       ('results_domain120.json', VIOLET, '^', 'E01: L, the air domain twice as big')):
        p = HERE / name
        if p.exists():
            for run in json.loads(p.read_text())['runs']:
                s = solve(run, 1e4)
                if s:
                    ax.plot(run['nodes'] / 1e3, (s['coils']['LOOP']['L'] / l_ref - 1) * 100, lw=0, color=color,
                            marker=marker, ms=9, markeredgecolor=SURFACE, markeredgewidth=2, label=label)
    style(ax, 'mesh nodes (thousands)', 'difference from the reference (%)')
    lo = min(-4.5, ax.get_ylim()[0])
    ax.set_ylim(lo, 0.8)
    ax.set_title('Elmer against the closed forms at 10 kHz, as the mesh is refined', color=INK, fontsize=10.5,
                 loc='left')
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc='lower right')
    fig.tight_layout()
    save(fig, out / 'elmerresults_1_against_reference.webp')
    plt.close(fig)


def chart_residual(out, plt, data):
    styles = {'level 0.75, 10 kHz': (BLUE, '-'), 'level 1, 10 kHz': (ORANGE, '-'), 'level 1.3, 10 kHz': (AQUA, '-'),
              'level 1, 3.5 MHz': (INK2, '--')}
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    fig.patch.set_facecolor(SURFACE)
    for label, (color, ls) in styles.items():
        if label in data:
            it, res = zip(*data[label])
            ax.semilogy(it, res, color=color, lw=2, ls=ls, label=label)
    ax.axhline(1e-7, color=INK2, lw=1, ls=':')
    ax.text(3000, 1.15e-7, 'tolerance 1e-7', color=INK2, fontsize=8, ha='right', va='bottom')
    style(ax, 'iteration', 'relative residual')
    ax.set_title('E01: the linear solve stalls at 10 kHz and converges at 3.5 MHz', color=INK, fontsize=10.5,
                 loc='left')
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc='upper right')
    fig.tight_layout()
    (out / 'E01_circular_loop').mkdir(parents=True, exist_ok=True)
    save(fig, out / 'E01_circular_loop' / 'elmerresults_2_residual.webp')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=str(HERE / 'pictures'))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    data = collect_residuals()
    chart_reference(out, plt)
    chart_residual(out, plt, data)


if __name__ == '__main__':
    main()
