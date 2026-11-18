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
    return C.rows('summary.csv'), C.rows('solves.csv'), C.rows('proof.csv'), C.rows('generator.csv')


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

def board_page(b, summ, gen, notes, h, up):
    """One board's comparison: h is the heading level of its top heading, up the path from the page to the branch's
    root (charts/ and data/ are there)."""
    H = '#' * h
    H2 = '#' * (h + 1)
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

    t += [f'![{SHORT[b]} against the air gap]({up}charts/{b}.webp)', '',
          "*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms "
          'angle error against the air gap, one line per solver.*', '']

    # at 1 mm
    t += [f'{H2} At 1 mm', '', f'![The curves at 1 mm]({up}charts/{b}_1mm.webp)', '',
          '| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | '
          'Angle error, rms (°) | Angle error, peak (°) | Solves |', '|---|---|---|---|---|---|---|---|---|']
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
    for key, lab, d in (('amp_SIN_nH', "SIN's amplitude (nH)", 3), ('amp_COS_nH', "COS's amplitude (nH)", 3),
                        ('L_TX_mean_nH', 'L TX, mean over the turn (nH)', 1),
                        ('R_TX_mean_mohm', 'R TX, mean over the turn (mΩ)', 0),
                        ('angle_error_rms_deg', 'Angle error, rms (electrical °)', 3)):
        t += [f'**{lab}**', '', '| Air gap | ' + ' | '.join(have) + ' |', '|---|' + '---|' * len(have)]
        for g in GAPS:
            cells = []
            for s in have:
                r = done_row(summ, s, b, g)
                cells.append(num(r[key], d) if r else '—')
            t.append(f'| {gap_label(g)} | ' + ' | '.join(cells) + ' |')
        t.append('')

    # against FastHenry, gap by gap
    if REF in have and others:
        t += [f'{H2} Against FastHenry, gap by gap', '',
              "Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX.", '',
              '| Air gap | ' + ' | '.join(others) + ' |', '|---|' + '---|' * len(others)]
        for g in GAPS:
            f = done_row(summ, REF, b, g)
            cells = []
            for s in others:
                r = done_row(summ, s, b, g)
                cells.append(f"{num(r['amp_SIN_nH'] / f['amp_SIN_nH'], 3)} ({num(r['L_TX_mean_nH'] / f['L_TX_mean_nH'], 3)})"
                             if r and f else '—')
            t.append(f'| {gap_label(g)} | ' + ' | '.join(cells) + ' |')
        t.append('')

    # the generator's estimates
    g = [x for x in gen if x['board'] == b]
    if g:
        g = g[0]
        t += [f"{H2} The generator's estimates", '',
              f"The generator's own figures from `Parameters.txt`, formulas rather than field solves: L TX "
              f"{num(g['L_TX_away_nH'], 0)} nH with the rotor away and {num(g['L_TX_rotor_nH'], 0)} nH with it (which "
              f"it calls an upper estimate of the drop), and R TX {num(g['R_TX_dc_mohm'], 0)} mΩ at DC.", '',
              '| Solver | L TX, rotor away (nH) | Over the estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) |',
              '|---|---|---|---|---|']
        for s in C.SOLVERS:
            r1 = row(summ, s, b, 1.0)
            r01 = done_row(summ, s, b, 0.1)
            aw = r1['L_TX_away_nH'] if r1 else None
            if aw in ('', None) and not r01:
                continue
            over = pct(aw / g['L_TX_away_nH'] - 1) + ' %' if aw not in ('', None) else '—'
            t.append(f"| {s} | {num(aw, 1)} | {over} | {num(r01['L_TX_mean_nH'] if r01 else None, 1)} | "
                     f"{num(r1['L_TX_mean_nH'] if r1 and C.complete(r1) else None, 1)} |")
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
    t.append('')

    turned = sorted({(r['solver'], n) for r in summ if r['board'] == b for n in ('SIN', 'COS')
                     if r.get(f'sign_turned_{n}') == 1})
    if turned:
        t += ['A receiver whose plus terminal sits on the other side in one branch comes out turned over; here '
              + ', '.join(f'{s} {n}' for s, n in turned) + ' is turned back to match FastHenry. Amplitudes and angle '
              'errors are the same either way.', '']
    return t


def root_page(summ, proof, gen, notes, st):
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
    t += ['', notes['INTRO_AFTER_STATUS'], '',
          f'This page shows one board, {ROOT_BOARD}. Every board has its own page in [`Comparisons/`](Comparisons/), '
          'named as its folder in the integration branches:', '',
          '| Board | What it is | SIN amplitude at 1 mm: ' + ', '.join(C.SOLVERS) + ' (nH) |', '|---|---|---|']
    for b in C.LABEL:
        amps = []
        for s in C.SOLVERS:
            r = done_row(summ, s, b, 1.0)
            amps.append(num(r['amp_SIN_nH'], 2) if r else '—')
        t.append(f'| [{b}](Comparisons/{b}.md) | {SHORT[b]}: {WHAT[b]} | ' + ' / '.join(amps) + ' |')
    t.append('')
    t += board_page(ROOT_BOARD, summ, gen, notes, 2, '')
    t += proof_section(proof, notes) + why_section(notes) + data_section() + tail()
    return t


def proof_section(proof, notes):
    t = ['## The proof boards', '', '![The proof boards](charts/proof.webp)', '', notes['PROOF_INTRO'], '',
         '| Solver | E01, L, 10 kHz | E01, L, 3.5 MHz | E02, M, 10 kHz | E02, M, 3.5 MHz | Run |', '|---|---|---|---|---|---|']
    cases = [('E01_circular_loop', 1e4), ('E01_circular_loop', 3.5e6), ('E02_coaxial_loops', 1e4),
             ('E02_coaxial_loops', 3.5e6)]
    for s in C.SOLVERS:
        files = sorted({r['file'] for r in proof if r['solver'] == s}, key=lambda f: (f != 'results.json', f))
        for f in files:
            cells = []
            for b, fr in cases:
                r = [x for x in proof if x['solver'] == s and x['file'] == f and x['board'] == b and x['frequency_hz'] == fr]
                cells.append(f"{num(r[0]['value_nH'], 3)} nH ({pct(r[0]['error_pct'] / 100, 2)} %)" if r else '—')
            run = 'as each branch solves it' if f == 'results.json' else f'`{f}` (a finer mesh, kept by the branch)'
            t.append(f'| {s} | ' + ' | '.join(cells) + f' | {run} |')
        if not files:
            t.append(f'| {s} | still to solve | | | | |')
    ref = sorted({(r['board'], r['frequency_hz'], r['reference_nH']) for r in proof})
    t += ['', 'The references: ' + '; '.join(f"{b.split('_')[0]} at {fr / 1e6:g} MHz {num(v, 3)} nH" if fr >= 1e6 else
                                           f"{b.split('_')[0]} at {fr / 1e3:g} kHz {num(v, 3)} nH" for b, fr, v in ref) + '.',
          '']
    return t


def why_section(notes):
    return ['## Why they differ', ''] + [x for k in notes['WHY'] for x in (k, '')]


def data_section():
    return ['## The data', '',
            '| File | One row per | Columns |', '|---|---|---|',
            '| [data/solves.csv](data/solves.csv) | solve | solver, board, gap, rotor angle, M SIN and M COS (nH), L TX (nH), '
            "R TX (mΩ), whether it passed its branch's checks, seconds, peak memory |",
            '| [data/summary.csv](data/summary.csv) | solver, board and gap | the best sine through SIN and COS (amplitude, '
            'offset, phase), the angle error (rms and peak, electrical degrees), L TX over the turn (mean, lowest, '
            'highest), R TX, L and R with the rotor away, seconds per solve, peak memory |',
            '| [data/proof.csv](data/proof.csv) | proof-board value | solver, board, results file, frequency, value, '
            "reference, error (%), the run's settings |",
            "| [data/generator.csv](data/generator.csv) | board | the generator's estimates of L TX (rotor away, with the "
            'rotor) and of R TX at DC |', '',
            "A port's plus side is each branch's own convention, so a receiver can come out with the opposite sign. "
            "Where a solver's curve is more than 90° from FastHenry's, its sign is turned (the `sign_turned_SIN` and "
            '`sign_turned_COS` columns say so); amplitudes and angle errors do not depend on it.', '']


def tail():
    return ['## Running it again', '', '```',
            'git fetch origin Elmer_Integration PyPEEC_Integration FastHenry_Integration Palace_Integration',
            'python scripts/collect.py          # reads every branch into data/',
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
    summ, solves, proof, gen = load()
    notes = json.loads((HERE / 'notes.json').read_text())
    st = status(summ)
    pages = {ROOT / 'README.md': finish(root_page(summ, proof, gen, notes, st))}
    for b in C.LABEL:
        lines = board_page(b, summ, gen, notes, 1, '../')
        lines[0] = f'# {b}: the solvers compared'
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
