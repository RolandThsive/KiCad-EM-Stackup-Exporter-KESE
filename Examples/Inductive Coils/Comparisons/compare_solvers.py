"""PyPEEC against Elmer on every coil board, from each branch's own results: the SIN and COS amplitudes, L TX over the
turn and with the rotor away, and the angle error, gap by gap.

    python compare_solvers.py                      the Elmer results from git (the branch origin/Elmer_Integration)
    python compare_solvers.py --elmer <checkout>   the Elmer results from a checkout of the Elmer_Integration branch
    python compare_solvers.py --chart              also draws SINCOS_PyPEEC_vs_Elmer.webp here: SIN's amplitude
                                                   against the gap on every board, by both solvers

The two branches solve the same boards from the same KESE export, at the same angles and gaps, with the same ports;
Elmer with finite elements in a meshed air box (level 0.25), PyPEEC with 50 um voxels and no air. Each amplitude is
the best sine through a gap's solves, as on the boards' own results pages, and the angle error is worked out the
same way (angle_error.py). Nothing here is solved. This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARDS = HERE.parent
ROOT = BOARDS.parents[1]
GAPS = (2.0, 1.5, 1.0, 0.5, 0.1)
ALL = (('S0_1x_OD21_2L_tiny', 'S0'), ('S0_1x_OD21_2L_tiny_TXtop', '21 mm, 2 TX turns on top'),
       ('S0_1x_OD22_2L_tiny_TXtop', '22 mm, 2 TX turns on top'),
       ('S0_1x_OD22_2L_tiny_TXtop_Cut', '22 mm, 2 TX turns on top, cuts'),
       ('S0_1x_OD23_2L_tiny_TX3top_Cut', '23 mm, 3 TX turns on top, cuts'),
       ('S0d2_1x_OD23_2L_tiny_TX3top_Cut', '23 mm, 3 TX turns, cuts, 2 periods'))
sys.path.insert(0, str(BOARDS / 'S0_1x_OD21_2L_tiny' / 'PyPEEC Simulation'))   # the boards' own chart style
from make_charts import COLOURS, INK, INK2, SURFACE, _style, tint  # noqa: E402


def rel(board, gap):
    folder = f'{gap:g}mm_AirGap'.replace('.', 'd')
    return f'Examples/Inductive Coils/{board}/Results/{folder}/results_gap{gap:g}mm.json'


def pypeec(board, gap):
    f = ROOT / rel(board, gap)
    return json.loads(f.read_text()) if f.exists() else None


def elmer(board, gap, checkout=None):
    if checkout:
        f = Path(checkout) / rel(board, gap)
        return json.loads(f.read_text()) if f.exists() else None
    r = subprocess.run(['git', '-C', str(ROOT), 'show', f'origin/Elmer_Integration:{rel(board, gap)}'],
                       capture_output=True, text=True, check=False)
    return json.loads(r.stdout) if r.returncode == 0 else None


def summary(res):
    """Amplitude of SIN and COS (nH), angle error (rms, peak), mean L TX over the turn (nH), and L TX with the rotor
    away if this file has it."""
    if not res or 'fit_nH' not in res or not (res.get('angle_error_deg') or {}).get('rms'):
        return None                                # not solved, or too few angles yet for a fit
    runs = [r for r in res['runs'] if r['rotor_deg'] != 'away']
    away = [r['solve']['coils']['TX']['L'] * 1e9 for r in res['runs'] if r['rotor_deg'] == 'away']
    ae = res.get('angle_error_deg') or {}
    lt = [r['solve']['coils']['TX']['L'] * 1e9 for r in runs]
    return dict(n=len(runs), sin=res['fit_nH']['SIN']['amplitude'], cos=res['fit_nH']['COS']['amplitude'],
                rms=ae.get('rms'), peak=ae.get('peak'), lt=sum(lt) / len(lt) if lt else None,
                away=away[0] if away else None)


def pct(a, b):
    return f'{100 * (a - b) / b:+.1f} %'


def table(checkout=None):
    rows = ['| Board | Air gap | Angles PyPEEC / Elmer | SIN amplitude PyPEEC / Elmer | COS amplitude PyPEEC / Elmer | '
            'Angle error rms PyPEEC / Elmer | L TX over the turn PyPEEC / Elmer |', '|---|---|---|---|---|---|---|']
    away = ['| Board | L TX, rotor away: PyPEEC | Elmer | PyPEEC against Elmer | The generator\'s estimate |',
            '|---|---|---|---|---|']
    data = {}
    for board, label in ALL:
        a_p = a_e = None
        for gap in GAPS:
            p, e = summary(pypeec(board, gap)), summary(elmer(board, gap, checkout))
            a_p = a_p or (p or {}).get('away')
            a_e = a_e or (e or {}).get('away')
            if not p or not e:
                continue
            data.setdefault(board, []).append((gap, p, e))
            rows.append(f"| [{label}](../{board}/) | {gap:g} mm | {p['n']} / {e['n']} | {p['sin']:.2f} / {e['sin']:.2f} nH "
                        f"({pct(p['sin'], e['sin'])}) | {p['cos']:.2f} / {e['cos']:.2f} nH ({pct(p['cos'], e['cos'])}) | "
                        f"{p['rms']:.1f}° / {e['rms']:.1f}° | {p['lt']:.1f} / {e['lt']:.1f} nH ({pct(p['lt'], e['lt'])}) |")
        exp = BOARDS / board / 'Results' / 'expected_results.json'
        gen = json.loads(exp.read_text()).get('tx', {}).get('L_away_gen_H') if exp.exists() else None
        if a_p and a_e:
            away.append(f"| [{label}](../{board}/) | {a_p:.1f} nH | {a_e:.1f} nH | {pct(a_p, a_e)} | "
                        + (f'{gen * 1e9:.0f} nH |' if gen else ' |'))
    return '\n'.join(rows), '\n'.join(away), data


def chart(data, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    boards = [b for b, _ in ALL if b in data]
    n = len(boards)
    if not n:
        return None
    cols = min(3, n)
    fig, axes = plt.subplots((n + cols - 1) // cols, cols, figsize=(4.2 * cols, 3.3 * ((n + cols - 1) // cols)),
                             dpi=200, squeeze=False)
    fig.patch.set_facecolor(SURFACE)
    blue = tint(COLOURS['SIN'], 1.0)
    for ax in axes.flat[n:]:
        ax.set_visible(False)
    for ax, board in zip(axes.flat, boards, strict=False):
        _style(ax, matplotlib)
        rows = sorted(data[board])
        g = [r[0] for r in rows]
        ax.set_xlim(0, max(g) + 0.1)                   # air gaps along x, not the angles _style sets
        ax.set_xticks(g)
        ax.plot(g, [r[1]['sin'] for r in rows], '-o', color=blue, lw=2, ms=6, label='PyPEEC', zorder=3)
        ax.plot(g, [r[2]['sin'] for r in rows], '--s', color=INK2, lw=1.5, ms=5, mfc=SURFACE, label='Elmer', zorder=2)
        ax.set_title(dict(ALL)[board], color=INK, fontsize=9, loc='left')
        ax.set_xlabel('air gap (mm)', color=INK2, fontsize=8)
        ax.set_ylabel('SIN amplitude (nH)', color=INK2, fontsize=8)
        ax.set_ylim(bottom=0)
    axes.flat[0].legend(frameon=False, fontsize=8, labelcolor=INK)
    fig.suptitle('SIN amplitude against the air gap: PyPEEC (voxels) and Elmer (finite elements)', x=0.02, ha='left',
                 color=INK, fontsize=11)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE, pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--elmer', default=None, help='a checkout of the Elmer_Integration branch (default: read it from git)')
    ap.add_argument('--chart', action='store_true', help='also draw SINCOS_PyPEEC_vs_Elmer.webp')
    a = ap.parse_args()
    t, away, data = table(a.elmer)
    print(t)
    print()
    print(away)
    if a.chart:
        print('wrote', chart(data, HERE / 'SINCOS_PyPEEC_vs_Elmer.webp'))


if __name__ == '__main__':
    main()
