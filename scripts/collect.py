"""Gather every solver's results for the coil boards and the proof boards into data/, from each solver's branch.

    python scripts/collect.py                      reads each branch as git has it (origin/<branch>; git fetch first)
    python scripts/collect.py --dir Palace=../Palace_Integration
                                                   reads one solver from a folder instead (a checkout of its branch)

Writes data/solves.csv (one row per solve: solver, board, air gap, rotor angle, M SIN, M COS, L TX, R TX, whether the
solve passed its solver's checks, its time and memory), data/summary.csv (one row per solver, board and gap: the fitted
amplitudes, the angle error, L TX over the turn, L TX with the rotor away, the time and memory of a solve),
data/proof.csv (the proof boards E01 and E02 against their references) and data/generator.csv (the generator's own
estimates for each board). Each branch is read as it is; nothing is solved here. GPL-3.0.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / 'data'
SOLVERS = {'Elmer': 'Elmer_Integration', 'PyPEEC': 'PyPEEC_Integration', 'FastHenry': 'FastHenry_Integration',
           'Palace': 'Palace_Integration'}
BOARDS = ('S0_1x_OD21_2L_tiny', 'S0_1x_OD21_2L_tiny_TXtop', 'S0_1x_OD22_2L_tiny_TXtop', 'S0_1x_OD22_2L_tiny_TXtop_Cut',
          'S0_1x_OD23_2L_tiny_TX3top_Cut', 'S0d2_1x_OD23_2L_tiny_TX3top_Cut')
GAPS = (0.1, 0.5, 1.0, 1.5, 2.0)
AGREE = 0.01        # the 1 % every branch's readable() allows
REF = 'FastHenry'   # whose curves set the sign of SIN and COS (a port's plus side is each bridge's own convention)


class Source:
    """One solver's branch: read through git (a ref) or from a folder."""

    def __init__(self, solver, folder=None, ref=None, repo=None):
        self.solver, self.folder, self.ref, self.repo = solver, folder, ref, repo

    def read(self, path):
        if self.folder:
            f = Path(self.folder) / path
            return f.read_text() if f.exists() else None
        r = subprocess.run(['git', '-C', str(self.repo), 'show', f'{self.ref}:{path}'], capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None

    def json(self, path):
        t = self.read(path)
        return json.loads(t) if t else None


def gap_folder(g):
    return f'{g:g}mm_AirGap'.replace('.', 'd')


def checks_ok(solver, s):
    """Whether a solve passes its own branch's checks (each branch's readable(), at 1 %)."""
    c = s['coils']
    tx = c['TX']
    if tx['R'] <= 0:
        return False
    if solver in ('Elmer', 'Palace', 'PyPEEC'):
        lw = s.get('L_from_energy_h')
        if lw is None or abs(lw - tx['L']) > AGREE * tx['L'] or s.get('converged', True) is False:
            return False
        if solver == 'PyPEEC':
            rp = s.get('R_from_power_ohm')
            if rp is not None and abs(rp - tx['R']) > AGREE * tx['R']:
                return False
        if solver == 'Elmer':
            rp = s.get('R_from_power_ohm')
            if rp is not None and abs(rp - tx['R']) > AGREE * tx['R']:
                return False
        return all(v <= AGREE for v in (s.get('reciprocity') or {}).values())
    scale = max(abs(c[n]['M']) for n in ('SIN', 'COS')) or 1e-30          # FastHenry: reciprocity in every solve
    return all(abs(c[n]['M'] - c[n].get('M_reverse', c[n]['M'])) <= AGREE * scale for n in ('SIN', 'COS'))


def fit(ang, y, period):
    """The best sine through (ang, y) over the period: offset, amplitude, phase (degrees)."""
    import numpy as np
    t = np.radians(np.asarray(ang, float) * 360.0 / period)
    a = np.column_stack([np.ones_like(t), np.sin(t), np.cos(t)])
    c = np.linalg.lstsq(a, np.asarray(y, float), rcond=None)[0]
    return float(c[0]), float(math.hypot(c[1], c[2])), float(math.degrees(math.atan2(c[2], c[1])))


def coils(sources):
    rows, summary = [], []
    for solver, src in sources.items():
        for b in BOARDS:
            away = None
            per_gap = {}
            for g in GAPS:
                r = src.json(f'Examples/Inductive Coils/{b}/Results/{gap_folder(g)}/results_gap{g:g}mm.json')
                if not r:
                    continue
                per_gap[g] = r
                for x in r['runs']:
                    if x['rotor_deg'] == 'away':
                        away = x['solve']['coils']['TX']
            for g, r in per_gap.items():
                ae = r.get('angle_error_deg') or {}
                period = 360.0 * ae.get('mechanical_per_electrical', 1.0)
                runs = sorted((x for x in r['runs'] if x['rotor_deg'] != 'away'), key=lambda x: x['rotor_deg'])
                for x in runs:
                    s, c = x['solve'], x['solve']['coils']
                    rows.append(dict(solver=solver, board=b, gap_mm=g, rotor_deg=x['rotor_deg'],
                                     M_SIN_nH=c['SIN']['M'] * 1e9, M_COS_nH=c['COS']['M'] * 1e9,
                                     L_TX_nH=c['TX']['L'] * 1e9, R_TX_mohm=c['TX']['R'] * 1e3,
                                     checks_ok=int(checks_ok(solver, s)), seconds=s.get('seconds'),
                                     peak_memory_gb=s.get('peak_memory_gb')))
                L = [x['solve']['coils']['TX']['L'] * 1e9 for x in runs]
                ang = [x['rotor_deg'] for x in runs]
                fs = fit(ang, [x['solve']['coils']['SIN']['M'] * 1e9 for x in runs], period) if len(runs) >= 3 else None
                fc = fit(ang, [x['solve']['coils']['COS']['M'] * 1e9 for x in runs], period) if len(runs) >= 3 else None
                summary.append(dict(
                    solver=solver, board=b, gap_mm=g, solves=len(runs),
                    solves_wanted=len(r.get('settings', {}).get('angles_deg') or []) or (16 if b.startswith('S0d2') else 8),
                    checks_ok=sum(checks_ok(solver, x['solve']) for x in runs),
                    amp_SIN_nH=fs[1] if fs else None, amp_COS_nH=fc[1] if fc else None,
                    offset_SIN_nH=fs[0] if fs else None, offset_COS_nH=fc[0] if fc else None,
                    phase_SIN_deg=fs[2] if fs else None, phase_COS_deg=fc[2] if fc else None,
                    angle_error_rms_deg=ae.get('rms'), angle_error_peak_deg=ae.get('peak'),
                    mech_per_elec=ae.get('mechanical_per_electrical', 1.0),
                    L_TX_mean_nH=sum(L) / len(L) if L else None, L_TX_min_nH=min(L) if L else None,
                    L_TX_max_nH=max(L) if L else None,
                    R_TX_mean_mohm=(sum(x['solve']['coils']['TX']['R'] for x in runs) / len(runs) * 1e3) if runs else None,
                    L_TX_away_nH=away['L'] * 1e9 if away else None,
                    R_TX_away_mohm=away['R'] * 1e3 if away else None,
                    seconds_per_solve=(sum(x['solve'].get('seconds') or 0 for x in runs) / len(runs)) if runs else None,
                    peak_memory_gb=max((x['solve'].get('peak_memory_gb') or 0 for x in runs), default=None)))
    return rows, summary


def generator(sources):
    """The generator's own estimates for each board (Parameters.txt, as every branch copies them into its results)."""
    out = []
    for b in BOARDS:
        for solver in (REF,) + tuple(s for s in sources if s != REF):
            e = None
            for g in GAPS:
                r = sources[solver].json(f'Examples/Inductive Coils/{b}/Results/{gap_folder(g)}/results_gap{g:g}mm.json')
                if r and r.get('expected'):
                    e = r['expected'].get('tx') or {}
                    break
            if e:
                out.append(dict(board=b, L_TX_away_nH=e.get('L_away_gen_H', 0) * 1e9 or None,
                                L_TX_rotor_nH=e.get('L_rotor_gen_H', 0) * 1e9 or None,
                                R_TX_dc_mohm=e.get('R_dc_ohm', 0) * 1e3 or None, source='Boards/Parameters.txt'))
                break
    return out


def align_signs(rows, summary):
    """Turn a solver's SIN or COS over where its best sine is more than 90 degrees from FastHenry's at the same board
    and gap: which side of a port is plus is each bridge's own convention, and turning it moves the curve by half a
    period and changes nothing else. The rows say which were turned."""
    ref = {(s['board'], s['gap_mm']): s for s in summary if s['solver'] == REF}
    turned = {}
    for s in summary:
        r = ref.get((s['board'], s['gap_mm']))
        for n in ('SIN', 'COS'):
            if r and s['solver'] != REF and s[f'phase_{n}_deg'] is not None and r[f'phase_{n}_deg'] is not None:
                d = abs((s[f'phase_{n}_deg'] - r[f'phase_{n}_deg'] + 180) % 360 - 180)
                if d > 90:
                    turned[(s['solver'], s['board'], s['gap_mm'], n)] = True
                    s[f'offset_{n}_nH'] *= -1
                    s[f'phase_{n}_deg'] = (s[f'phase_{n}_deg'] + 360) % 360 - 180
            s[f'sign_turned_{n}'] = int(turned.get((s['solver'], s['board'], s['gap_mm'], n), False))
    for x in rows:
        for n in ('SIN', 'COS'):
            t = turned.get((x['solver'], x['board'], x['gap_mm'], n), False)
            if t:
                x[f'M_{n}_nH'] *= -1
            x[f'sign_turned_{n}'] = int(t)


# The proof boards' references, the same for every solver: Neumann's double integral over the open arcs (each 356°,
# between its round ends' centres), averaged over filaments across the traces' widths, as the branches' references.py
# work it out (arc_inductance, arc_mutual). E01's at 3.5 MHz takes the thin strip's high-frequency geometric mean
# distance (w / 4) and is an estimate: the skin depth equals the copper's thickness there.
REFERENCES = {('E01_circular_loop', 'dc'): 55.590, ('E01_circular_loop', 'hf'): 55.039,
              ('E02_coaxial_loops', 'dc'): 23.886, ('E02_coaxial_loops', 'hf'): 23.886}
EXTRA = {'Elmer': {'E01_circular_loop': ['results_grade2.json'], 'E02_coaxial_loops': ['results_grade.json']}}


def proof(sources):
    """E01 (one loop: L) and E02 (two coaxial loops: M): each solver's finest run of its ladder at each frequency, and
    the diagnostic runs that refine further, against REFERENCES."""
    out = []
    for solver, src in sources.items():
        for e in ('E01_circular_loop', 'E02_coaxial_loops'):
            for name in ['results.json'] + EXTRA.get(solver, {}).get(e, []):
                r = src.json(f'Examples/{e}/{name}')
                if not r:
                    continue
                for run in r.get('runs', [])[-1:]:
                    for s in run.get('solves', []):
                        f = s['frequency_hz']
                        c = s.get('coils') or {}
                        if e.startswith('E01'):
                            v = s.get('L_h') or next((x.get('L') for x in c.values() if 'L' in x), None)
                            q = 'L of the loop'
                        else:
                            v = s.get('M_h') or next((x.get('M') for x in c.values() if 'M' in x), None)
                            q = 'M between the loops'
                        rv = REFERENCES[(e, 'hf' if f > 1e6 else 'dc')]
                        desc = {k: run[k] for k in run if k != 'solves' and not isinstance(run[k], (dict, list))}
                        out.append(dict(solver=solver, board=e, file=name, frequency_hz=f, quantity=q,
                                        value_nH=v * 1e9 if v else None, reference_nH=rv,
                                        error_pct=(v * 1e9 / rv - 1) * 100 if v else None, run=json.dumps(desc)))
    return out


def write(path, rows):
    if not rows:
        return
    keys = list(rows[0])
    for r in rows[1:]:
        keys += [k for k in r if k not in keys]
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f'{v:.6g}' if isinstance(v, float) else v) for k, v in r.items()})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo', default=str(ROOT), help='the git repository the branches are read from')
    ap.add_argument('--remote', default='origin')
    ap.add_argument('--dir', action='append', default=[], metavar='SOLVER=FOLDER',
                    help='read this solver from a folder (a checkout of its branch) instead of git')
    a = ap.parse_args()
    dirs = dict(kv.split('=', 1) for kv in a.dir)
    sources = {s: Source(s, folder=dirs.get(s), ref=f'{a.remote}/{b}', repo=a.repo) for s, b in SOLVERS.items()}
    rows, summary = coils(sources)
    align_signs(rows, summary)
    DATA.mkdir(exist_ok=True)
    write(DATA / 'solves.csv', rows)
    write(DATA / 'summary.csv', summary)
    write(DATA / 'proof.csv', proof(sources))
    write(DATA / 'generator.csv', generator(sources))
    for s in SOLVERS:
        n = sum(1 for r in rows if r['solver'] == s)
        print(f'{s}: {n} solves', '(from ' + (dirs[s] if s in dirs else f'{a.remote}/{SOLVERS[s]}') + ')')


if __name__ == '__main__':
    main()
