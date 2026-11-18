"""Write README.md from data/ (scripts/collect.py) and charts/ (scripts/charts.py): every number in it is computed here.

    python scripts/report.py            write README.md
    python scripts/report.py --print    print it instead

The prose that no number can carry (how each solver models the boards, the faults found on the way) is in
scripts/notes.json. GPL-3.0.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import charts as C          # noqa: E402  (the same solver order, colours and board names as the charts)

ROOT = HERE.parent
GAPS = (0.1, 0.5, 1.0, 1.5, 2.0)
REF = 'FastHenry'
METHOD = {'Elmer': 'FEM (finite elements, the A-V eddy-current formulation)',
          'Palace': 'FEM (finite elements, the frequency-domain Maxwell solver)',
          'PyPEEC': 'PEEC (partial elements on voxels, FFT-accelerated)',
          'FastHenry': 'PEEC (partial elements on filaments, direct solve)'}
BRANCH = {'Elmer': 'Elmer_Integration', 'PyPEEC': 'PyPEEC_Integration', 'FastHenry': 'FastHenry_Integration',
          'Palace': 'Palace_Integration'}
SHORT = {'S0_1x_OD21_2L_tiny': 'S0', 'S0_1x_OD21_2L_tiny_TXtop': 'S0 TXtop', 'S0_1x_OD22_2L_tiny_TXtop': 'OD22 TXtop',
         'S0_1x_OD22_2L_tiny_TXtop_Cut': 'OD22 Cut', 'S0_1x_OD23_2L_tiny_TX3top_Cut': 'OD23 Cut',
         'S0d2_1x_OD23_2L_tiny_TX3top_Cut': 'S0d2'}


def num(v, d=2):
    """A number with a real minus sign, or a dash when there is none."""
    if v in ('', None):
        return '—'
    return f'{v:.{d}f}'.replace('-', '−')


def rel(v, d=1):
    """A ratio less one, in words: 4.9 % under, 1.2 % over."""
    return f'{num(abs(100 * v), d)} % ' + ('under' if v < 0 else 'over')


def pct(v, d=1, sign=True):
    return num(100 * v, d) if not sign else (('+' if v >= 0 else '') + num(100 * v, d))


def load():
    return C.rows('summary.csv'), C.rows('solves.csv'), C.rows('proof.csv'), C.rows('generator.csv')


def pairs(summ, s, ref=REF):
    """(solver row, reference row) for every board and gap both have finished."""
    base = {(r['board'], r['gap_mm']): r for r in summ if r['solver'] == ref and C.complete(r)}
    return [(r, base[(r['board'], r['gap_mm'])]) for r in summ
            if r['solver'] == s and C.complete(r) and (r['board'], r['gap_mm']) in base]


def ratios(summ, s, key):
    v = [a[key] / b[key] for a, b in pairs(summ, s) if a[key] not in ('', None) and b[key] not in ('', None)]
    return (min(v), statistics.mean(v), max(v), len(v)) if v else None


def amp_ratios(summ, s):
    v = []
    for a, b in pairs(summ, s):
        v += [a['amp_SIN_nH'] / b['amp_SIN_nH'], a['amp_COS_nH'] / b['amp_COS_nH']]
    return (min(v), statistics.mean(v), max(v), len(v) // 2) if v else None


def status(summ):
    out = {}
    for s in C.SOLVERS:
        rs = [r for r in summ if r['solver'] == s]
        done = [r for r in rs if C.complete(r)]
        boards = sorted({r['board'] for r in done if all(any(x['board'] == r['board'] and x['gap_mm'] == g and
                         C.complete(x) for x in done) for g in GAPS)})
        out[s] = dict(gaps=len(done), boards=boards, solves=int(sum(r['solves'] for r in rs)),
                      checks=int(sum(r['checks_ok'] for r in rs)))
    return out


def intro(st, notes):
    t = ['# Solvers comparison: the KESE inductive-coil examples', '',
         'KESE exports a KiCad board\'s copper and stackup for electromagnetic solvers. Four free, open-source solvers were '
         'run on the same six inductive position-sensor boards (a TX coil that drives the rotor, and SIN and COS '
         'receivers that read it), each on its own branch, with the same boards, the same air gaps (0.1, 0.5, 1, 1.5 '
         'and 2 mm), the same rotor angles and the same frequency (3.5 MHz, copper at 58 MS/m). This branch reads '
         'their results and compares them. It solves nothing itself.', '',
         '| Solver | Method | Branch | Coil boards finished (of 6) | Solves | Passing their own checks |',
         '|---|---|---|---|---|---|']
    for s in C.SOLVERS:
        x = st[s]
        b = f"{len(x['boards'])}" + ('' if len(x['boards']) == 6 else f" (still solving; {x['gaps']} of 30 gaps)")
        t.append(f"| {s} | {METHOD[s]} | `{BRANCH[s]}` | {b} | {x['solves']} | {x['checks']} |")
    t += ['', notes['INTRO_AFTER_STATUS'], '']
    return t


def short_answer(summ, proof, gen, notes):
    t = ['## The short answer', '']
    fh_proof = {(r['board'], r['frequency_hz']): r['error_pct'] for r in proof
                if r['solver'] == REF and r['file'] == 'results.json'}
    worst = max(abs(v) for k, v in fh_proof.items() if k[1] == 1e4) if fh_proof else None
    if worst is not None:
        t.append(f'- **FastHenry is the yardstick.** On the two proof boards it lands within {num(worst, 2)} % of the '
                 'reference at 10 kHz, the closest of the four (the table under "The proof boards"). Every ratio below '
                 'is against FastHenry, board by board and gap by gap.')
    lines = []
    for s in C.SOLVERS:
        if s == REF:
            continue
        a, l, aw, an = amp_ratios(summ, s), ratios(summ, s, 'L_TX_mean_nH'), ratios(summ, s, 'L_TX_away_nH'), pairs(summ, s)
        if not a:
            lines.append(f'- **{s}** has no finished gap yet; it is still solving.')
            continue
        d = [abs(x['angle_error_rms_deg'] - y['angle_error_rms_deg']) for x, y in an]
        lines.append(f'- **{s}** ({C.KIND[s]}): the coupling (the amplitude of SIN and COS) is {rel(a[1] - 1)} '
                     f'FastHenry\'s on average ({pct(a[0] - 1)} to {pct(a[2] - 1)} % over the {a[3]} board-gaps both '
                     f'have finished); L TX is {rel(l[1] - 1)} ({pct(l[0] - 1)} to {pct(l[2] - 1)} %); the rms angle '
                     f'error is within {num(max(d), 2)}° of FastHenry\'s, {num(statistics.median(d), 2)}° typically '
                     '(electrical degrees).')
    t += lines
    t += ['', notes['SHORT_AFTER'], '']
    rows = []
    for g in gen:
        fh = [r for r in summ if r['solver'] == REF and r['board'] == g['board'] and r['gap_mm'] == 1.0 and C.complete(r)]
        if fh and fh[0]['L_TX_away_nH'] not in ('', None):
            rows.append((g, fh[0]))
    if rows:
        t += ['The generator\'s own estimates of L TX (from each board\'s `Parameters.txt`) against FastHenry:', '',
              '| Board | Generator, rotor away (nH) | FastHenry, rotor away (nH) | Generator, with the rotor (nH) | '
              'FastHenry, rotor at 1 mm (nH) |', '|---|---|---|---|---|']
        for g, f in rows:
            t.append(f"| {SHORT[g['board']]} | {num(g['L_TX_away_nH'], 0)} | {num(f['L_TX_away_nH'], 1)} | "
                     f"{num(g['L_TX_rotor_nH'], 0)} | {num(f['L_TX_mean_nH'], 1)} |")
        t += ['', notes['GENERATOR'], '']
    return t


def all_boards(summ):
    t = ['## How close the solvers are, all boards together', '',
         '![Each solver over FastHenry](charts/ratio_to_fasthenry.webp)', '',
         'Each solver\'s value over FastHenry\'s on the same board and gap: the mean over the boards both have finished, '
         'and in brackets the lowest and the highest.', '']
    others = [s for s in C.SOLVERS if s != REF and pairs(summ, s)]
    if not others:
        return t
    for key, lab in (('amp_SIN_nH', 'SIN\'s amplitude'), ('L_TX_mean_nH', 'L TX, mean over the turn'),
                     ('R_TX_mean_mohm', 'R TX, mean over the turn')):
        t += [f'**{lab}**', '', '| Air gap | ' + ' | '.join(others) + ' |', '|---|' + '---|' * len(others)]
        for g in GAPS:
            cells = []
            for s in others:
                v = [a[key] / b[key] for a, b in pairs(summ, s) if a['gap_mm'] == g]
                cells.append(f'{num(statistics.mean(v), 3)} ({num(min(v), 3)} to {num(max(v), 3)})' if v else '—')
            t.append(f'| {g:g} mm | ' + ' | '.join(cells) + ' |')
        t.append('')
    return t


def board_section(b, summ, gen):
    desc = C.LABEL[b].split('(', 1)[1].rstrip(')') if C.LABEL[b].startswith(SHORT[b] + ' (') else C.LABEL[b]
    t = [f'### {SHORT[b]}: {desc}', '', f'![{SHORT[b]} against the air gap](charts/{b}.webp)', '',
         f'At 1 mm (the curves: [charts/{b}_1mm.webp](charts/{b}_1mm.webp)):', '',
         '| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | '
         'Angle error, rms (°) | Angle error, peak (°) | Solves |', '|---|---|---|---|---|---|---|---|---|']
    for s in C.SOLVERS:
        r = [x for x in summ if x['solver'] == s and x['board'] == b and x['gap_mm'] == 1.0]
        if not r:
            continue
        r = r[0]
        if not C.complete(r):
            t.append(f"| {s} | still solving | | | {num(r['L_TX_away_nH'], 1)} | | | | "
                     f"{int(r['solves'])} of {int(r['solves_wanted'])} |")
            continue
        t.append(f"| {s} | {num(r['amp_SIN_nH'], 3)} | {num(r['amp_COS_nH'], 3)} | {num(r['L_TX_mean_nH'], 1)} | "
                 f"{num(r['L_TX_away_nH'], 1)} | {num(r['R_TX_mean_mohm'], 0)} | {num(r['angle_error_rms_deg'], 3)} | "
                 f"{num(r['angle_error_peak_deg'], 3)} | {int(r['solves'])} |")
    have = [s for s in C.SOLVERS if any(x['solver'] == s and x['board'] == b and C.complete(x) for x in summ)]
    t += ['', 'SIN\'s amplitude (nH) at every gap:', '', '| Air gap | ' + ' | '.join(have) + ' |',
          '|---|' + '---|' * len(have)]
    for g in GAPS:
        cells = []
        for s in have:
            r = [x for x in summ if x['solver'] == s and x['board'] == b and x['gap_mm'] == g and C.complete(x)]
            cells.append(num(r[0]['amp_SIN_nH'], 3) if r else '—')
        t.append(f'| {g:g} mm | ' + ' | '.join(cells) + ' |')
    return t + ['']


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
    if not any(r['solver'] == 'Palace' for r in proof):
        t.append('| Palace | still to solve | | | | |')
    ref = sorted({(r['board'], r['frequency_hz'], r['reference_nH']) for r in proof})
    t += ['', 'The references: ' + '; '.join(f"{b.split('_')[0]} at {fr / 1e6:g} MHz {num(v, 3)} nH" if fr >= 1e6 else
                                           f"{b.split('_')[0]} at {fr / 1e3:g} kHz {num(v, 3)} nH" for b, fr, v in ref) + '.',
          '']
    return t


def cost_section(summ, notes):
    t = ['## Time and memory', '', notes['COST_INTRO'], '',
         '| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |', '|---|---|---|---|']
    for s in C.SOLVERS:
        rs = [r for r in summ if r['solver'] == s and C.complete(r) and r.get('seconds_per_solve') not in ('', None)]
        if not rs:
            t.append(f'| {s} | still solving | | |')
            continue
        sec = [r['seconds_per_solve'] for r in rs]
        mem = [r['peak_memory_gb'] for r in rs if r.get('peak_memory_gb') not in ('', None)]
        t.append(f'| {s} | {num(statistics.median(sec), 0)} | {num(min(sec), 0)} to {num(max(sec), 0)} | '
                 f'{num(min(mem), 1)} to {num(max(mem), 1)} |')
    return t + ['']


def why_section(notes):
    return ['## Why they differ', ''] + [x for k in notes['WHY'] for x in (k, '')]


def data_section(summ):
    turned = sorted({(r['solver'], n) for r in summ for n in ('SIN', 'COS') if r.get(f'sign_turned_{n}') == 1})
    t = ['## The data', '',
         '| File | One row per | Columns |', '|---|---|---|',
         '| [data/solves.csv](data/solves.csv) | solve | solver, board, gap, rotor angle, M SIN and M COS (nH), L TX (nH), '
         'R TX (mΩ), whether it passed its branch\'s checks, seconds, peak memory |',
         '| [data/summary.csv](data/summary.csv) | solver, board and gap | the best sine through SIN and COS (amplitude, '
         'offset, phase), the angle error (rms and peak, electrical degrees), L TX over the turn (mean, lowest, '
         'highest), R TX, L and R with the rotor away, seconds per solve, peak memory |',
         '| [data/proof.csv](data/proof.csv) | proof-board value | solver, board, results file, frequency, value, '
         'reference, error (%), the run\'s settings |',
         '| [data/generator.csv](data/generator.csv) | board | the generator\'s estimates of L TX (rotor away, with the '
         'rotor) and of R TX at DC |', '']
    note = ('A port\'s plus side is each branch\'s own convention, so a receiver can come out with the opposite sign. '
            'Where a solver\'s curve is more than 90° from FastHenry\'s, its sign is turned (the `sign_turned_SIN` and '
            '`sign_turned_COS` columns say so); amplitudes and angle errors do not depend on it.')
    if turned:
        note += ' Turned here: ' + ', '.join(f'{s} {n}' for s, n in turned) + '.'
    return t + [note, '']


def tail():
    return ['## Running it again', '', '```',
            'git fetch origin Elmer_Integration PyPEEC_Integration FastHenry_Integration Palace_Integration',
            'python scripts/collect.py          # reads every branch into data/',
            'python scripts/charts.py           # draws charts/',
            'python scripts/report.py           # writes this README', '```', '',
            'It needs Python 3 with numpy and matplotlib (and Pillow for WebP). `collect.py --dir SOLVER=FOLDER` reads '
            'one solver from a checkout instead of git.', '',
            '## Licence', '',
            'The scripts are GPL-3.0 ([LICENSE](LICENSE)). The boards are the Sinusoidal Coil Generator\'s, and the '
            'data, charts and this README describe them, so they keep its non-commercial terms: see '
            '[LICENSE.md](LICENSE.md).', '']


def build():
    summ, solves, proof, gen = load()
    notes = json.loads((HERE / 'notes.json').read_text())
    st = status(summ)
    t = intro(st, notes) + short_answer(summ, proof, gen, notes) + all_boards(summ)
    t += ['## Board by board', '', notes['BOARD_INTRO'], '']
    for b in C.LABEL:
        t += board_section(b, summ, gen)
    t += proof_section(proof, notes) + why_section(notes) + cost_section(summ, notes) + data_section(summ) + tail()
    text = '\n'.join(t).rstrip() + '\n'
    if 'TODO' in text:
        raise SystemExit('a TODO is left in the text')
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--print', action='store_true')
    a = ap.parse_args()
    text = build()
    if a.print:
        print(text)
    else:
        (ROOT / 'README.md').write_text(text)
        print('wrote README.md')


if __name__ == '__main__':
    main()
