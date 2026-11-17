"""The 22 mm board opened by a cut in a top trace (../S0_1x_OD22_2L_tiny_TXtop_Cut) against the same board opened
at a left-out via (../S0_1x_OD22_2L_tiny_TXtop), solve by solve at every air gap both have.

    python compare_ports.py      prints the comparison as a Markdown table and draws SINCOS_cut_vs_via.webp here

Which cut face counts as plus is a convention, and the cut's is the other way round from the via's for SIN: the via
board's SIN is shown with its sign turned, which moves its curve by half a turn and changes nothing else.
Nothing here is solved. This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BOARDS = HERE.parent
CUT = BOARDS / 'S0_1x_OD22_2L_tiny_TXtop_Cut' / 'Results'
VIA = BOARDS / 'S0_1x_OD22_2L_tiny_TXtop' / 'Results'
sys.path.insert(0, str(CUT.parent / 'FastHenry Simulation'))         # the boards' own fit and chart style
from angle_error import sine_fit  # noqa: E402
from make_charts import COLOURS, FREQ, INK, INK2, PERIOD, SURFACE, _style, readable, tint  # noqa: E402
GAPS = (2.0, 1.5, 1.0, 0.5, 0.1)


def load(results, gap):
    f = results / f'{gap:g}mm_AirGap'.replace('.', 'd') / f'results_gap{gap:g}mm.json'
    return json.loads(f.read_text()) if f.exists() else None


def solves(res, flip_sin=False):
    """{angle: (M_SIN nH, M_COS nH, L_TX nH, R_TX ohm, readable)} for the solved angles (the rotor away left out)."""
    out = {}
    for r in res['runs']:
        if r['rotor_deg'] == 'away':
            continue
        c, s = r['solve']['coils'], r['solve']
        out[r['rotor_deg']] = ((-1 if flip_sin else 1) * c['SIN']['M'] * 1e9, c['COS']['M'] * 1e9, c['TX']['L'] * 1e9,
                               c['TX']['R'], readable(s))
    return out


def loose(v):
    return not v[4]


def summary(res, s):
    ang = sorted(s)
    ok = [a for a in ang if not loose(s[a])]
    fit = {n: sine_fit(ang, [s[a][i] for a in ang], PERIOD) for i, n in enumerate(('SIN', 'COS'))}
    fit_ok = ({n: sine_fit(ok, [s[a][i] for a in ok], PERIOD) for i, n in enumerate(('SIN', 'COS'))}
              if len(ok) >= 5 else None)
    ae = res.get('angle_error_deg') or {}
    L = [s[a][2] for a in ang]
    return dict(n=len(ang), loose=len(ang) - len(ok), fit=fit, fit_ok=fit_ok, rms=ae.get('rms'), peak=ae.get('peak'),
                q=ae.get('sin_to_cos_deg'), L=(min(L), max(L)))


def mv(nh):
    return 2 * math.pi * FREQ * nh * 1e-9 * 1e3


def table():
    rows = ['| Air gap | Port | Amplitude SIN / COS, all solves | The same, readable solves only | Angle error | SIN to '
            'COS | L TX over the turn | Not readable | Cut against via, where both are readable |',
            '|---|---|---|---|---|---|---|---|---|']
    for gap in GAPS:
        rc, rv = load(CUT, gap), load(VIA, gap)
        if not rc or not rv:
            continue
        sc, sv = solves(rc), solves(rv, flip_sin=True)
        both = [a for a in sorted(sc) if a in sv and not loose(sc[a]) and not loose(sv[a])]
        d = []
        for i, n in enumerate(('SIN', 'COS')):
            if both:
                amp = summary(rv, sv)['fit'][n]['amplitude']
                d.append(f'{n} {np.mean([abs(sc[a][i] - sv[a][i]) for a in both]) / amp * 100:.1f} %')
        cmp = (f'{len(both)} angle{"s" if len(both) > 1 else ""}; mean difference {", ".join(d)} of the amplitude' if both else 'no angle')
        for port, res, s in (('via (left out)', rv, sv), ('cut', rc, sc)):
            m = summary(res, s)
            a = m['fit']
            ok = m['fit_ok']
            okt = (f"{ok['SIN']['amplitude']:.2f} / {ok['COS']['amplitude']:.2f} nH ({m['n'] - m['loose']} solves)"
                   if ok else 'fewer than 5 readable')
            rows.append(f"| {gap:g} mm | {port} | {a['SIN']['amplitude']:.2f} / {a['COS']['amplitude']:.2f} nH "
                        f"({mv(a['SIN']['amplitude']):.0f} / {mv(a['COS']['amplitude']):.0f} mV) | {okt} | "
                        f"{m['rms']:.1f}° rms, {m['peak']:.1f}° peak | {m['q']:.1f}° | {m['L'][0]:.1f} to {m['L'][1]:.1f} nH "
                        f"| {m['loose']} of {m['n']} | {cmp if port.startswith('cut') else ''} |")
    return '\n'.join(rows)


def chart(path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    gaps = [g for g in GAPS if load(CUT, g) and load(VIA, g)]
    fig, axes = plt.subplots(len(gaps), 1, figsize=(8, 2.9 * len(gaps) + 1.3), dpi=200, sharex=True,
                             layout='constrained')
    fig.patch.set_facecolor(SURFACE)
    axes = np.atleast_1d(axes)
    for k, (ax, gap) in enumerate(zip(axes, gaps)):
        _style(ax, matplotlib)
        ax.set_ylabel('M (nH)', color=INK2)
        sc, sv = solves(load(CUT, gap)), solves(load(VIA, gap), flip_sin=True)
        for i, n in enumerate(('SIN', 'COS')):
            col = tint(COLOURS[n], 1.0)
            for s, ls, fill, z in ((sv, (0, (4, 2)), SURFACE, 3), (sc, '-', col, 4)):
                ang = sorted(s)
                x, y = ang + [PERIOD], [s[a][i] for a in ang] + [s[ang[0]][i]]
                ax.plot(x, y, color=col, lw=1.6 if ls == '-' else 1.2, ls=ls, zorder=z)
                ax.plot(ang, [s[a][i] for a in ang], ls='none', marker='o', ms=6.5, mfc=fill, mec=col, mew=1.4,
                        zorder=z + 2)
                lp = [(a, s[a][i]) for a in ang if loose(s[a])]
                if lp:
                    ax.plot(*zip(*lp), ls='none', marker='o', ms=13, mfc='none', mec=INK2, mew=0.8, zorder=z + 1)
        nc = sum(loose(v) for v in sc.values())
        nv = sum(loose(v) for v in sv.values())
        ax.set_title(f'{gap:g} mm air gap', color=INK, fontsize=10, loc='left')
        ax.text(1, 1.02, f'not readable: cut {nc} of {len(sc)}, via {nv} of {len(sv)}', transform=ax.transAxes,
                ha='right', va='bottom', fontsize=8, color=INK2)
        ax.margins(y=0.12)
    axes[-1].set_xlabel('rotor angle (degrees)', color=INK2)
    fig.suptitle('Cut against via: the same board, the receivers opened two ways', x=0.02, ha='left', color=INK,
                 fontsize=12)
    hs = [Line2D([], [], color=tint(COLOURS['SIN'], 1.0), lw=1.6, marker='o', mfc=tint(COLOURS['SIN'], 1.0),
                 label='SIN, cut'),
          Line2D([], [], color=tint(COLOURS['SIN'], 1.0), lw=1.2, ls=(0, (4, 2)), marker='o', mfc=SURFACE,
                 label='SIN, via (sign turned)'),
          Line2D([], [], color=tint(COLOURS['COS'], 1.0), lw=1.6, marker='o', mfc=tint(COLOURS['COS'], 1.0),
                 label='COS, cut'),
          Line2D([], [], color=tint(COLOURS['COS'], 1.0), lw=1.2, ls=(0, (4, 2)), marker='o', mfc=SURFACE,
                 label='COS, via'),
          Line2D([], [], ls='none', marker='o', ms=11, mfc='none', mec=INK2, label='not readable')]
    fig.legend(handles=hs, frameon=False, fontsize=8, labelcolor=INK, loc='outside lower center', ncol=5)
    fig.savefig(path, facecolor=SURFACE, pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    return path


def main():
    print(table())
    print('wrote', chart(HERE / 'SINCOS_cut_vs_via.webp'))


if __name__ == '__main__':
    main()
