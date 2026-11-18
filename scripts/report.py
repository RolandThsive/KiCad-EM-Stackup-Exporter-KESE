"""Write the comparison pages from data/ (scripts/collect.py) and charts/ (scripts/charts.py); every number in them is
computed here.

    python scripts/report.py            write README.md and Comparisons/<board>.md, one per coil board
    python scripts/report.py --print    print README.md instead

README.md shows the S0d2 board's comparison (ROOT_BOARD) and links the others; Comparisons/<board>.md, named as the
board's folder in the integration branches, has each board's. The prose that no number can carry (how each solver
models the boards, the faults found on the way) is in scripts/notes.json. GPL-3.0.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import charts as C          # noqa: E402  (the same solver order, colours and board names as the charts)

ROOT = HERE.parent
PAGES = ROOT / 'Comparisons'
GAPS = (0.1, 0.5, 1.0, 1.5, 2.0)
REF = 'FastHenry'
ROOT_BOARD = 'S0d2_1x_OD23_2L_tiny_TX3top_Cut'
METHOD = {'Elmer': 'FEM (finite elements, the A-V eddy-current formulation)',
          'Palace': 'FEM (finite elements, the frequency-domain Maxwell solver)',
          'PyPEEC': 'PEEC (partial elements on voxels, FFT-accelerated)',
          'FastHenry': 'PEEC (partial elements on filaments, direct solve)'}
BRANCH = {'Elmer': 'Elmer_Integration', 'PyPEEC': 'PyPEEC_Integration', 'FastHenry': 'FastHenry_Integration',
          'Palace': 'Palace_Integration'}
SHORT = {'S0_1x_OD21_2L_tiny': 'S0', 'S0_1x_OD21_2L_tiny_TXtop': 'S0 TXtop', 'S0_1x_OD22_2L_tiny_TXtop': 'OD22 TXtop',
         'S0_1x_OD22_2L_tiny_TXtop_Cut': 'OD22 Cut', 'S0_1x_OD23_2L_tiny_TX3top_Cut': 'OD23 Cut',
         'S0d2_1x_OD23_2L_tiny_TX3top_Cut': 'S0d2'}
WHAT = {'S0_1x_OD21_2L_tiny': '21 mm across, one period per turn, the TX one turn on each layer, a half-ring rotor; SIN '
                              'and COS opened at a left-out via',
        'S0_1x_OD21_2L_tiny_TXtop': 'S0 with the TX two turns on the top layer (the generator narrows the RX band to '
                                    'fit them)',
        'S0_1x_OD22_2L_tiny_TXtop': "the TX two turns on the top layer around S0's own RX coils, the board grown to "
                                    "22.2 mm",
        'S0_1x_OD22_2L_tiny_TXtop_Cut': 'the 22 mm board with SIN and COS opened by a 0.2 mm cut in a top trace instead '
                                        'of a left-out via',
        'S0_1x_OD23_2L_tiny_TX3top_Cut': "the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by "
                                         "cuts",
        'S0d2_1x_OD23_2L_tiny_TX3top_Cut': 'the three-turn 23 mm board with two electrical periods per turn and a rotor '
                                           'of two sectors, so the curves repeat every 180°; solved at 16 angles over '
                                           'the whole turn'}


def num(v, d=2):
    """A number with a real minus sign, or a dash when there is none."""
    if v in ('', None):
        return '—'
    return f'{v:.{d}f}'.replace('-', '−')


def rel(v, d=1):
    """A ratio less one, in words: 4.9 % under, 1.2 % over."""
    return f'{num(abs(100 * v), d)} % ' + ('under' if v < 0 else 'over')


def span(v, d):
    """'lo to hi', or one number when they round alike, or a dash."""
    if not v:
        return '—'
    lo, hi = num(min(v), d), num(max(v), d)
    return lo if lo == hi else f'{lo} to {hi}'


def pct(v, d=1):
    return ('+' if v >= 0 else '') + num(100 * v, d)


def load():
    th = C.rows('theory.csv') if (C.DATA / 'theory.csv').exists() else []
    e01 = C.rows('theory_e01.csv') if (C.DATA / 'theory_e01.csv').exists() else []
    return (C.rows('summary.csv'), C.rows('solves.csv'), C.rows('proof.csv'), C.rows('generator.csv'), th,
            e01[0] if e01 else None)


def theory(th, b):
    r = [x for x in th if x['board'] == b]
    return r[0] if r else None


def bracket(t):
    return f"{num(t['L_hf_nH'], 1)} to {num(t['L_dc_nH'], 1)}"


def against_l(v, t):
    """Where a rotor-away L TX sits against the hand values: inside them, over the DC value (the most it can be) or
    under the high-frequency limit."""
    if v > t['L_dc_nH']:
        return f"{num(100 * (v / t['L_dc_nH'] - 1), 1)} % over the DC value, the most it can be"
    if v < t['L_hf_nH']:
        return f"{num(100 * (1 - v / t['L_hf_nH']), 1)} % under the high-frequency limit"
    return 'inside the hand values'


def row(summ, s, b, g):
    r = [x for x in summ if x['solver'] == s and x['board'] == b and x['gap_mm'] == g]
    return r[0] if r else None


def done_row(summ, s, b, g):
    r = row(summ, s, b, g)
    return r if r and C.complete(r) else None


def pairs(summ, s, board=None):
    """(solver row, FastHenry row) for every gap (of one board, or of all) both have finished."""
    base = {(r['board'], r['gap_mm']): r for r in summ if r['solver'] == REF and C.complete(r)}
    return [(r, base[(r['board'], r['gap_mm'])]) for r in summ
            if r['solver'] == s and C.complete(r) and (r['board'], r['gap_mm']) in base
            and (board is None or r['board'] == board)]


def stats(v):
    return (min(v), statistics.mean(v), max(v), len(v)) if v else None


def amp_ratios(summ, s, board=None):
    v = []
    for a, b in pairs(summ, s, board):
        v += [a['amp_SIN_nH'] / b['amp_SIN_nH'], a['amp_COS_nH'] / b['amp_COS_nH']]
    r = stats(v)
    return (r[0], r[1], r[2], r[3] // 2) if r else None


def ratios(summ, s, key, board=None):
    return stats([a[key] / b[key] for a, b in pairs(summ, s, board) if a[key] not in ('', None)
                  and b[key] not in ('', None)])


def status(summ):
    out = {}
    for s in C.SOLVERS:
        rs = [r for r in summ if r['solver'] == s]
        done = [r for r in rs if C.complete(r)]
        boards = sorted({r['board'] for r in done if all(done_row(summ, s, r['board'], g) for g in GAPS)})
        out[s] = dict(gaps=len(done), boards=boards, solves=int(sum(r['solves'] for r in rs)),
                      checks=int(sum(r['checks_ok'] for r in rs)))
    return out


def gap_label(g):
    return f'{g:g} mm'


# ---------------------------------------------------------------------------------------------------------------- pages

def board_page(b, summ, gen, notes, h, up, th=()):
    """One board's comparison: h is the heading level of its top heading, up the path from the page to the branch's
    root (charts/ and data/ are there), th the hand values (data/theory.csv)."""
    H = '#' * h
    H2 = '#' * (h + 1)
    T = theory(th, b)
    have = [s for s in C.SOLVERS if any(done_row(summ, s, b, g) for g in GAPS)]
    others = [s for s in have if s != REF]
    t = [f'{H} {b}', '', f'**{SHORT[b]}**: {WHAT[b]}.', '']

    # where each solver stands on this board
    t += ['| Solver | Gaps finished (of 5) | Solves | Passing their own checks |', '|---|---|---|---|']
    for s in C.SOLVERS:
        rs = [r for r in summ if r['solver'] == s and r['board'] == b]
        n_done = sum(1 for g in GAPS if done_row(summ, s, b, g))
        solves = int(sum(r['solves'] for r in rs))
        state = f'{n_done}' + ('' if n_done == 5 else ' (still solving)')
        t.append(f"| {s} | {state} | {solves} | {int(sum(r['checks_ok'] for r in rs))} |")
    if T:
        t.append('| Theory | worked out from the copper by hand formulas, nothing to solve | — | — |')
    t.append('')

    # the short answer for this board
    if REF in have:
        lines = []
        for s in others:
            a, l = amp_ratios(summ, s, b), ratios(summ, s, 'L_TX_mean_nH', b)
            d = [abs(x['angle_error_rms_deg'] - y['angle_error_rms_deg']) for x, y in pairs(summ, s, b)]
            if not a:
                continue
            lines.append(f"- **{s}** ({C.KIND[s]}): the coupling (SIN's and COS's amplitude) is {rel(a[1] - 1)} "
                         f"FastHenry's on average over the {a[3]} gaps both have finished ({pct(a[0] - 1)} to "
                         f"{pct(a[2] - 1)} %); L TX is {rel(l[1] - 1)} ({pct(l[0] - 1)} to {pct(l[2] - 1)} %); the rms "
                         f"angle error is within {num(max(d), 2)}° of FastHenry's (electrical degrees).")
        for s in C.SOLVERS:
            if s not in have and s != REF:
                lines.append(f'- **{s}** has not finished a gap of this board yet; it is still solving.')
        if lines:
            t += ['Against FastHenry, the yardstick (the closest to the reference on the proof boards):', ''] + lines + ['']
    if T:
        lines = []
        for s in C.SOLVERS:
            r = row(summ, s, b, 1.0)
            if not r or r['L_TX_away_nH'] in ('', None):
                continue
            lines.append(f"- **{s}**: L TX with the rotor away {num(r['L_TX_away_nH'], 1)} nH, "
                         f"{against_l(r['L_TX_away_nH'], T)}; R TX {num(r['R_TX_away_mohm'], 0)} mΩ, "
                         f"{rel(r['R_TX_away_mohm'] / T['R_dc_mohm'] - 1)} its DC value.")
        if lines:
            t += [f"Against the hand values (the Theory rows, worked out in [Formulas](#formulas)): with the rotor away, "
                  f"L TX has to lie between about {num(T['L_hf_nH'], 1)} nH (all the current at the copper's surface) "
                  f"and {num(T['L_dc_nH'], 1)} nH (its DC value, the most it can be at any frequency), and R TX can be "
                  f"no less than its DC resistance, {num(T['R_dc_mohm'], 1)} mΩ.", ''] + lines + ['']

    t += [f'![{SHORT[b]} against the air gap]({up}charts/{b}.webp)', '',
          "*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms "
          'angle error against the air gap, one line per solver.*', '']

    # at 1 mm
    t += [f'{H2} At 1 mm', '', f'![The curves at 1 mm]({up}charts/{b}_1mm.webp)', '',
          '| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | '
          'Angle error, rms (°) | Angle error, peak (°) | Solves |', '|---|---|---|---|---|---|---|---|---|']
    if T:
        t.append(f"| **Theory** | no hand formula | no hand formula | ≤ {num(T['L_dc_nH'], 1)} | {bracket(T)} | "
                 f"≥ {num(T['R_dc_mohm'], 1)} | 0 (ideal) | 0 (ideal) | — |")
    for s in C.SOLVERS:
        r = row(summ, s, b, 1.0)
        if not r:
            continue
        if not C.complete(r):
            t.append(f"| {s} | still solving | | | {num(r['L_TX_away_nH'], 1)} | | | | "
                     f"{int(r['solves'])} of {int(r['solves_wanted'])} |")
            continue
        t.append(f"| {s} | {num(r['amp_SIN_nH'], 3)} | {num(r['amp_COS_nH'], 3)} | {num(r['L_TX_mean_nH'], 1)} | "
                 f"{num(r['L_TX_away_nH'], 1)} | {num(r['R_TX_mean_mohm'], 0)} | {num(r['angle_error_rms_deg'], 3)} | "
                 f"{num(r['angle_error_peak_deg'], 3)} | {int(r['solves'])} |")
    t.append('')

    # every gap, quantity by quantity
    t += [f'{H2} Every air gap', '']
    if T:
        t += ['In the Theory column: L TX can be no more than its DC value and R TX no less than its DC resistance, at '
              "any gap; an ideal sensor's angle error is 0; and no hand formula gives the amplitudes (see "
              '[Formulas](#formulas)).', '']
    hand = {'amp_SIN_nH': '—', 'amp_COS_nH': '—', 'L_TX_mean_nH': f"≤ {num(T['L_dc_nH'], 1)}" if T else '',
            'R_TX_mean_mohm': f"≥ {num(T['R_dc_mohm'], 1)}" if T else '', 'angle_error_rms_deg': '0'}
    for key, lab, d in (('amp_SIN_nH', "SIN's amplitude (nH)", 3), ('amp_COS_nH', "COS's amplitude (nH)", 3),
                        ('L_TX_mean_nH', 'L TX, mean over the turn (nH)', 1),
                        ('R_TX_mean_mohm', 'R TX, mean over the turn (mΩ)', 0),
                        ('angle_error_rms_deg', 'Angle error, rms (electrical °)', 3)):
        cols = have + (['Theory'] if T else [])
        t += [f'**{lab}**', '', '| Air gap | ' + ' | '.join(cols) + ' |', '|---|' + '---|' * len(cols)]
        for g in GAPS:
            cells = []
            for s in have:
                r = done_row(summ, s, b, g)
                cells.append(num(r[key], d) if r else '—')
            if T:
                cells.append(hand[key])
            t.append(f'| {gap_label(g)} | ' + ' | '.join(cells) + ' |')
        t.append('')

    # against FastHenry, gap by gap
    if REF in have and others:
        t += [f'{H2} Against FastHenry, gap by gap', '',
              "Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX."
              + (" In the Theory column, in brackets, the most L TX can be (its DC value) over FastHenry's L TX; there "
                 'is no hand value for the amplitude.' if T else ''), '',
              '| Air gap | ' + ' | '.join(others + (['Theory'] if T else [])) + ' |',
              '|---|' + '---|' * (len(others) + bool(T))]
        for g in GAPS:
            f = done_row(summ, REF, b, g)
            cells = []
            for s in others:
                r = done_row(summ, s, b, g)
                cells.append(f"{num(r['amp_SIN_nH'] / f['amp_SIN_nH'], 3)} ({num(r['L_TX_mean_nH'] / f['L_TX_mean_nH'], 3)})"
                             if r and f else '—')
            if T:
                cells.append(f"— (≤ {num(T['L_dc_nH'] / f['L_TX_mean_nH'], 3)})" if f else '—')
            t.append(f'| {gap_label(g)} | ' + ' | '.join(cells) + ' |')
        t.append('')

    # the hand values and the generator's estimates
    g = [x for x in gen if x['board'] == b]
    g = g[0] if g else None
    if g or T:
        intro = []
        if T:
            intro.append('The Theory row is worked out from the TX copper alone (see [Formulas](#formulas)).')
        if g:
            intro.append(f"The generator's figures come from `Parameters.txt`, formulas rather than field solves: L TX "
                         f"{num(g['L_TX_away_nH'], 0)} nH with the rotor away and {num(g['L_TX_rotor_nH'], 0)} nH with "
                         f"it at 1 mm (which it calls an upper estimate of the drop, so the true value should be above "
                         f"it), and R TX {num(g['R_TX_dc_mohm'], 0)} mΩ at DC.")
        t += [f"{H2} The hand values and the generator's estimates", '', ' '.join(intro), '',
              '| | L TX, rotor away (nH) | Against the hand values | Over the generator\'s estimate | L TX at 0.1 mm (nH) '
              '| L TX at 1 mm (nH) | R TX, rotor away (mΩ) |', '|---|---|---|---|---|---|---|']
        if T:
            t.append(f"| **Theory** | {bracket(T)} | — | "
                     f"{pct(T['L_dc_nH'] / g['L_TX_away_nH'] - 1) + ' % (DC value)' if g else '—'} | "
                     f"≤ {num(T['L_dc_nH'], 1)} | ≤ {num(T['L_dc_nH'], 1)} | ≥ {num(T['R_dc_mohm'], 1)} |")
        if g:
            t.append(f"| Generator | {num(g['L_TX_away_nH'], 0)} | — | — | — | ≥ {num(g['L_TX_rotor_nH'], 0)} | "
                     f"{num(g['R_TX_dc_mohm'], 0)} (DC) |")
        for s in C.SOLVERS:
            r1 = row(summ, s, b, 1.0)
            r01 = done_row(summ, s, b, 0.1)
            aw = r1['L_TX_away_nH'] if r1 else None
            if aw in ('', None) and not r01:
                continue
            has = aw not in ('', None)
            over = pct(aw / g['L_TX_away_nH'] - 1) + ' %' if has and g else '—'
            t.append(f"| {s} | {num(aw, 1)} | {against_l(aw, T) if has and T else '—'} | {over} | "
                     f"{num(r01['L_TX_mean_nH'] if r01 else None, 1)} | "
                     f"{num(r1['L_TX_mean_nH'] if r1 and C.complete(r1) else None, 1)} | "
                     f"{num(r1['R_TX_away_mohm'] if r1 else None, 0)} |")
        t.append('')

    # time and memory on this board
    t += [f'{H2} Time and memory', '', notes['COST_INTRO'], '',
          '| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured '
          'it (GB) |', '|---|---|---|---|']
    for s in have:
        rs = [done_row(summ, s, b, g) for g in GAPS]
        rs = [r for r in rs if r and r.get('seconds_per_solve') not in ('', None)]
        if not rs:
            continue
        sec = [r['seconds_per_solve'] for r in rs]
        mem = [r['peak_memory_gb'] for r in rs if r.get('peak_memory_gb') not in ('', None)]
        t.append(f'| {s} | {num(statistics.median(sec), 0)} | {span(sec, 0)} | '
                 f"{span(mem, 1)} |")
    if T and T.get('seconds') not in ('', None):
        t.append(f"| Theory | {num(T['seconds'], 0)} (once for the board: both of Neumann's sums) | — | "
                 f"{num(T['peak_memory_gb'], 1)} |")
    t.append('')

    turned = sorted({(r['solver'], n) for r in summ if r['board'] == b for n in ('SIN', 'COS')
                     if r.get(f'sign_turned_{n}') == 1})
    if turned:
        t += ['A receiver whose plus terminal sits on the other side in one branch comes out turned over; here '
              + ', '.join(f'{s} {n}' for s, n in turned) + ' is turned back to match FastHenry. Amplitudes and angle '
              'errors are the same either way.', '']
    return t


def formulas(b, T, g, summ, e01, H, whose="this board's"):
    """How each Theory value of board b is worked out, with the board's own numbers. H is the heading's #s."""
    if not T:
        return []
    um = T['copper_mm'] * 1000
    t = [f'{H} Formulas', '',
         f"How each Theory value is worked out, with {whose} numbers. `scripts/theory.py` does the sums; its inputs "
         "are the TX copper in the board's `Boards/Stator.kicad_pcb` and the stack-up KESE exported with it "
         "(`3D_Geometry/Stator/materials.json`), read from the FastHenry branch (every branch has the same boards).", '',
         "**1. L TX with the rotor away: Neumann's formula, with the geometric mean distance.**", '',
         '```math', r"L = \frac{\mu_0}{4\pi} \oint \oint \frac{d\mathbf{l} \cdot d\mathbf{l}'}{r}", '```', '',
         f"over the TX copper's centre line, {num(T['length_mm'], 1)} mm of {num(T['width_mm'], 1)} mm × "
         f"{num(um, 0)} µm trace from one terminal end to the other, with the via that joins the layers (the two ends "
         'sit stacked at the terminal, and the port closes the loop there at no length, as in E01). Along one stretch '
         'of trace (points less than 2 mm apart along the copper), r becomes √(r² + g²), where g is the geometric mean distance (GMD) of the trace\'s cross-section: '
         "a conductor's self-inductance is the mutual inductance of two thin filaments g apart (Rosa; Grover, "
         '*Inductance Calculations*). Between separate stretches of copper (neighbouring turns, and the two layers '
         f"{num(T['layer_gap_mm'], 3)} mm apart), 1/r is averaged over both cross-sections, to second order. The sum "
         'runs over pieces of 0.05 mm with four Gauss points each.', '',
         f"- **DC**, the current spread evenly: g = 0.2235 (w + t) = {num(T['gmd_dc_mm'], 4)} mm (Grover), so "
         f"**L = {num(T['L_dc_nH'], 1)} nH**.",
         f"- **High-frequency limit**, the current all at the copper's surface: g is then the rectangle's logarithmic "
         f"capacity, {num(T['gmd_hf_mm'], 4)} mm (from a boundary-element solve of the cross-section, which gives the "
         f"known 0.25 w for a thin strip and 0.590 a for a square of side a), so **L = {num(T['L_hf_nH'], 1)} nH**.", '']
    if e01:
        t += [f"The same code on E01's loop gives {num(e01['L_dc_nH'], 3)} nH against the textbook "
              f"{num(e01['ref_dc_nH'], 3)} nH ({pct(e01['dc_off_pct'] / 100, 2)} %).", '']
    t += ['**2. Why these bound the solvers.** With no magnetic material near, a coil\'s inductance can only fall, and '
          'its resistance only rise, as the frequency goes up; and copper brought near it (the rotor) only lowers L '
          f"and adds loss. So at 3.5 MHz and at every air gap, L TX ≤ {num(T['L_dc_nH'], 1)} nH and "
          f"R TX ≥ {num(T['R_dc_mohm'], 1)} mΩ; with the rotor away, L TX lies between about "
          f"{num(T['L_hf_nH'], 1)} and {num(T['L_dc_nH'], 1)} nH. The skin depth at 3.5 MHz,", '',
          '```math', r"\delta = \frac{1}{\sqrt{\pi f \mu_0 \sigma}} = " + f"{num(T['skin_depth_um'], 1)}" +
          r"\ \mu\mathrm{m},", '```', '',
          "is the copper's own thickness, so the true value lies inside that range, not at either end. The lower end "
          'counts each trace on its own; the turns pushing each other\'s current about at high frequency would lower '
          'it by well under 1 %.', '',
          '**3. R TX at DC.**', '',
          '```math', r"R = \frac{\ell}{\sigma w t} = \frac{" + f"{num(T['length_mm'], 1)}" +
          r"\ \mathrm{mm}}{58\ \mathrm{MS/m} \times " + f"{num(T['width_mm'], 1)}" + r"\ \mathrm{mm} \times " +
          f"{num(um, 0)}" + r"\ \mu\mathrm{m}} = " + f"{num(T['R_dc_mohm'], 1)}" + r"\ \mathrm{m}\Omega", '```', '',
          'The via adds well under 1 mΩ.', '',
          "**4. Angle error 0.** The receivers are drawn so that SIN and COS follow the sine and cosine of the rotor "
          "angle exactly, and an ideal sensor's angle error is zero. It is the design's target, not a bound: a "
          "solver's error is the real board's departure from it plus the solver's own.", '',
          '**5. No hand value for the amplitudes.** How much of the TX field reaches SIN and COS depends on the eddy '
          "currents in the rotor's copper, and no closed formula gives those: only a field solve does."]
    f1, f2 = done_row(summ, REF, b, 0.1), done_row(summ, REF, b, 2.0)
    if T.get('period_mm') not in ('', None) and f1 and f2:
        import math
        guess = math.exp(-2 * math.pi * 1.9 / T['period_mm'])
        t[-1] += (f" The generator's note that the signal falls about as exp(−2π gap / period), with a period of "
                  f"{num(T['period_mm'], 1)} mm here, would keep SIN's amplitude at 2 mm at {num(100 * guess, 0)} % of "
                  f"its value at 0.1 mm; FastHenry finds {num(100 * f2['amp_SIN_nH'] / f1['amp_SIN_nH'], 0)} %. It is a "
                  'rule of thumb, and is not used here.')
    t.append('')
    if g:
        above = [s for s in C.SOLVERS if done_row(summ, s, b, 1.0)]
        ok = all(done_row(summ, s, b, 1.0)['L_TX_mean_nH'] >= g['L_TX_rotor_nH'] for s in above)
        t += [f"**6. The generator's estimates.** L TX {num(g['L_TX_away_nH'], 0)} nH with the rotor away, from its own "
              f"formula (the DC value above is {rel(T['L_dc_nH'] / g['L_TX_away_nH'] - 1)} it); "
              f"{num(g['L_TX_rotor_nH'], 0)} nH with the rotor at 1 mm, which it calls an upper estimate of the drop, so "
              'the true value should be above it' + (' (every solver\'s is)' if ok and above else '') + '; and R TX '
              f"{num(g['R_TX_dc_mohm'], 0)} mΩ at DC, rounded (the copper's {num(T['length_mm'], 1)} mm give "
              f"{num(T['R_dc_mohm'], 1)} mΩ).", '']
    return t


def root_page(summ, proof, gen, notes, st, th=(), e01=None):
    t = ['# Solvers comparison: the KESE inductive-coil examples', '',
         "KESE exports a KiCad board's copper and stackup for electromagnetic solvers. Four free, open-source solvers were "
         'run on the same six inductive position-sensor boards (a TX coil that drives the rotor, and SIN and COS '
         'receivers that read it), each on its own branch, with the same boards, the same air gaps (0.1, 0.5, 1, 1.5 '
         'and 2 mm), the same rotor angles and the same frequency (3.5 MHz, copper at 58 MS/m). This branch reads '
         'their results and compares them. It solves nothing itself.', '',
         '| Solver | Method | Branch | Coil boards finished (of 6) | Solves | Passing their own checks |',
         '|---|---|---|---|---|---|']
    for s in C.SOLVERS:
        x = st[s]
        bd = f"{len(x['boards'])}" + ('' if len(x['boards']) == 6 else f" (still solving; {x['gaps']} of 30 gaps)")
        t.append(f"| {s} | {METHOD[s]} | `{BRANCH[s]}` | {bd} | {x['solves']} | {x['checks']} |")
    if th:
        t.append(f"| Theory | hand formulas: Neumann's integral over the TX copper, its DC resistance "
                 f"([Formulas](#formulas)) | this one (`scripts/theory.py`) | {len(th)} | — | — |")
    t += ['', notes['INTRO_AFTER_STATUS'], '',
          f'This page shows one board, {ROOT_BOARD}. Every board has its own page in [`Comparisons/`](Comparisons/), '
          'named as its folder in the integration branches:', '',
          '| Board | What it is | SIN amplitude at 1 mm: ' + ', '.join(C.SOLVERS) + ' (nH) | L TX with the rotor away, '
          'Theory (nH) |', '|---|---|---|---|']
    for b in C.LABEL:
        amps = []
        for s in C.SOLVERS:
            r = done_row(summ, s, b, 1.0)
            amps.append(num(r['amp_SIN_nH'], 2) if r else '—')
        T = theory(th, b)
        t.append(f'| [{b}](Comparisons/{b}.md) | {SHORT[b]}: {WHAT[b]} | ' + ' / '.join(amps) +
                 f" | {bracket(T) if T else '—'} |")
    t += ['', 'There is no hand formula for the SIN amplitude; the Theory column gives the range L TX must lie in with '
          'the rotor away (see [Formulas](#formulas)).', '']
    t += board_page(ROOT_BOARD, summ, gen, notes, 2, '', th)
    t += proof_section(proof, notes, e01) + why_section(notes) + data_section(bool(th))
    t += formulas(ROOT_BOARD, theory(th, ROOT_BOARD), next((x for x in gen if x['board'] == ROOT_BOARD), None), summ,
                  e01, '##', f"{SHORT[ROOT_BOARD]}'s")
    t += proof_formulas(e01) + tail()
    return t


def proof_section(proof, notes, e01=None):
    t = ['## The proof boards', '', '![The proof boards](charts/proof.webp)', '', notes['PROOF_INTRO'], '',
         '| Solver | E01, L, 10 kHz | E01, L, 3.5 MHz | E02, M, 10 kHz | E02, M, 3.5 MHz | Run |', '|---|---|---|---|---|---|']
    cases = [('E01_circular_loop', 1e4), ('E01_circular_loop', 3.5e6), ('E02_coaxial_loops', 1e4),
             ('E02_coaxial_loops', 3.5e6)]
    for s in C.SOLVERS:
        files = sorted({r['file'] for r in proof if r['solver'] == s}, key=lambda f: (f != 'results.json', f))
        for f in files:
            cells = []
            for b, fr in cases:
                mine = [x for x in proof if x['solver'] == s and x['file'] == f and x['board'] == b]
                r = [x for x in mine if x['frequency_hz'] == fr]
                tag = ''
                if not r and fr == 1e4:             # a run whose low frequency is 100 kHz (same L and M, see notes)
                    r, tag = [x for x in mine if x['frequency_hz'] == 1e5], ' at 100 kHz'
                cells.append(f"{num(r[0]['value_nH'], 3)} nH ({pct(r[0]['error_pct'] / 100, 2)} %){tag}" if r else '—')
            run = 'as each branch solves it' if f == 'results.json' else f'`{f}` (a finer mesh, kept by the branch)'
            t.append(f'| {s} | ' + ' | '.join(cells) + f' | {run} |')
        if not files:
            t.append(f'| {s} | still to solve | | | | |')
    refs = {(r['board'], r['frequency_hz']): r['reference_nH'] for r in proof}
    if refs:
        e01_hf = (f"{num(e01['L_hf_nH'], 2)} to {num(e01['ref_dc_nH'], 2)} nH (the branches use "
                  f"{num(refs.get(('E01_circular_loop', 3.5e6)), 3)})" if e01 else
                  f"{num(refs.get(('E01_circular_loop', 3.5e6)), 3)} nH")
        t.append(f"| **Theory** | {num(refs.get(('E01_circular_loop', 1e4)), 3)} nH | {e01_hf} | "
                 f"{num(refs.get(('E02_coaxial_loops', 1e4)), 3)} nH | {num(refs.get(('E02_coaxial_loops', 3.5e6)), 3)} nH "
                 '| the references, by Neumann\'s integral ([Formulas](#the-proof-boards-references)) |')
    ref = sorted({(r['board'], r['frequency_hz'], r['reference_nH']) for r in proof})
    if refs:
        return t + [''] + [x for k in notes.get('PROOF_AFTER', []) for x in ('- ' + k,)] + (
            [''] if notes.get('PROOF_AFTER') else [])
    t += ['', 'The references: ' + '; '.join(f"{b.split('_')[0]} at {fr / 1e6:g} MHz {num(v, 3)} nH" if fr >= 1e6 else
                                           f"{b.split('_')[0]} at {fr / 1e3:g} kHz {num(v, 3)} nH" for b, fr, v in ref) + '.',
          '']
    return t


def proof_formulas(e01):
    """The proof boards' references, as formulas."""
    t = ["### The proof boards' references", '',
         'E01 is one open circular loop, its trace 0.5 mm wide on a 10 mm radius, open by 0.2 mm; E02 is two such loops, '
         'one on each side of a board, 1.565 mm apart (copper centre to copper centre). Both references are Neumann\'s '
         'double integral over the open arcs, each over θ = 356.0°, between its round ends\' centres:', '',
         '```math', r"M_{12} = \frac{\mu_0 r_1 r_2}{4\pi} \int_0^{\theta}\!\int_0^{\theta} "
         r"\frac{\cos(\varphi_1 - \varphi_2)\, d\varphi_1\, d\varphi_2}"
         r"{\sqrt{r_1^2 + r_2^2 - 2 r_1 r_2 \cos(\varphi_1 - \varphi_2) + d^2}}", '```', '',
         "- E01's L is the loop's M with itself at d = g, the trace's GMD (the same method as the coils' L): "
         'g = 0.2235 (w + t) at DC gives 55.590 nH. At 3.5 MHz the branches use g = w / 4 = 0.125 mm, the GMD of a '
         'strip of no thickness with its current crowded to the edges, which gives 55.039 nH.']
    if e01:
        t[-1] += (f" With the copper's 35 µm thickness counted, the high-frequency limit's GMD is "
                  f"{num(e01['gmd_hf_mm'], 4)} mm and L {num(e01['L_hf_nH'], 2)} nH; since the skin depth at 3.5 MHz "
                  f"equals the thickness, the true value lies between that and the DC value, {num(e01['L_hf_nH'], 2)} to "
                  f"{num(e01['ref_dc_nH'], 2)} nH, and 55.039 nH is one point inside that range rather than an exact "
                  'answer.')
    t += ["- E02's M is the two loops' M at d = 1.565 mm, averaged over both traces' widths with the current spread "
          'evenly (21 × 21 radii): 23.886 nH, used at both frequencies.', '']
    return t


def why_section(notes):
    return ['## Why they differ', ''] + [x for k in notes['WHY'] for x in (k, '')]


def data_section(hand=False):
    t = ['## The data', '',
            '| File | One row per | Columns |', '|---|---|---|',
            '| [data/solves.csv](data/solves.csv) | solve | solver, board, gap, rotor angle, M SIN and M COS (nH), L TX (nH), '
            "R TX (mΩ), whether it passed its branch's checks, seconds, peak memory |",
            '| [data/summary.csv](data/summary.csv) | solver, board and gap | the best sine through SIN and COS (amplitude, '
            'offset, phase), the angle error (rms and peak, electrical degrees), L TX over the turn (mean, lowest, '
            'highest), R TX, L and R with the rotor away, seconds per solve, peak memory |',
            '| [data/proof.csv](data/proof.csv) | proof-board value | solver, board, results file, frequency, value, '
            "reference, error (%), the run's settings |",
            "| [data/generator.csv](data/generator.csv) | board | the generator's estimates of L TX (rotor away, with the "
            'rotor) and of R TX at DC |']
    if hand:
        t += ['| [data/theory.csv](data/theory.csv) | board | the hand values: L TX at DC and in the high-frequency '
              "limit, R TX at DC, and their inputs (the copper's length, width and thickness, the GMDs, the layers' "
              'spacing, the skin depth) |',
              "| [data/theory_e01.csv](data/theory_e01.csv) | — | the same code on E01's loop, against its reference |"]
    return t + ['',
            "A port's plus side is each branch's own convention, so a receiver can come out with the opposite sign. "
            "Where a solver's curve is more than 90° from FastHenry's, its sign is turned (the `sign_turned_SIN` and "
            '`sign_turned_COS` columns say so); amplitudes and angle errors do not depend on it.', '']


def tail():
    return ['## Running it again', '', '```',
            'git fetch origin Elmer_Integration PyPEEC_Integration FastHenry_Integration Palace_Integration',
            'python scripts/collect.py          # reads every branch into data/',
            'python scripts/theory.py --check   # works out the hand values into data/ (a few minutes)',
            'python scripts/charts.py           # draws charts/',
            'python scripts/report.py           # writes this README and Comparisons/', '```', '',
            'It needs Python 3 with numpy and matplotlib (and Pillow for WebP). `collect.py --dir SOLVER=FOLDER` reads '
            'one solver from a checkout instead of git.', '',
            '## Licence', '',
            "The scripts are GPL-3.0 ([LICENSE](LICENSE)). The boards are the Sinusoidal Coil Generator's, and the "
            'data, charts and these pages describe them, so they keep its non-commercial terms: see '
            '[LICENSE.md](LICENSE.md).', '']


def page_tail():
    return ['---', '',
            "The proof boards, why the solvers differ, the data files and how to run it again are in the "
            "[branch's README](../README.md). The boards are the Sinusoidal Coil Generator's, for non-commercial use: "
            'see [LICENSE.md](../LICENSE.md).', '']


def finish(lines):
    text = '\n'.join(lines).rstrip() + '\n'
    if 'TODO' in text:
        raise SystemExit('a TODO is left in the text')
    return text


def build():
    summ, solves, proof, gen, th, e01 = load()
    notes = json.loads((HERE / 'notes.json').read_text())
    st = status(summ)
    pages = {ROOT / 'README.md': finish(root_page(summ, proof, gen, notes, st, th, e01))}
    for b in C.LABEL:
        lines = board_page(b, summ, gen, notes, 1, '../', th)
        lines[0] = f'# {b}: the solvers compared'
        lines += formulas(b, theory(th, b), next((x for x in gen if x['board'] == b), None), summ, e01, '##')
        pages[PAGES / f'{b}.md'] = finish(['[Solvers comparison](../README.md) › ' + SHORT[b], ''] + lines + page_tail())
    return pages


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--print', action='store_true')
    a = ap.parse_args()
    pages = build()
    if a.print:
        print(pages[ROOT / 'README.md'])
        return
    PAGES.mkdir(exist_ok=True)
    for p, text in pages.items():
        p.write_text(text)
        print('wrote', p.relative_to(ROOT))


if __name__ == '__main__':
    main()
