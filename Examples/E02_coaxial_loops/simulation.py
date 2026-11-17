"""E02: two coaxial circular traces, TX on F.Cu and RX on B.Cu of a 1.6 mm board, each E01's loop: their mutual
inductance from FastHenry, against Neumann's formula for the two open arcs averaged over both traces' widths.

    python simulation.py                      the filament ladder at both frequencies
    python simulation.py --nwinc 9            9 filaments across each trace only

TX carries 1 A; RX is open, so its voltage is the EMF the TX induces in it and M = Im(Z[RX][TX]) / omega. FastHenry
gives the reverse too, Z[TX][RX], which its direct solve makes equal (reciprocity). Writes results.json beside this
file and the runs under case/ (not committed). Every setting is in SETTINGS.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
sys.path.insert(0, str(HERE.parent))                  # Examples/references.py
from bridge import fasthenry_case as C, kicad as K, stackup as S   # noqa: E402
from references import arc_mutual   # noqa: E402

SETTINGS = dict(
    board='E02_coaxial_loops.kicad_pcb',
    radius_mm=10.0,                # each trace's centre line
    width_mm=0.5,
    gap_mm=0.2,
    ends_mm=((109.993873, -100.35), (109.993873, -99.65)),   # each loop's two trace ends at its gap, model coordinates
    layers={'TX': 'F.Cu', 'RX': 'B.Cu'},
    sigma=5.8e7,                   # copper, S/m
    freqs_hz=[1e4, 3.5e6],
    ladder=[(1, 1), (3, 1), (5, 1), (9, 1), (9, 3)],   # (filaments across, filaments through)
    rw=2.0,                        # each edge filament this much narrower than the next one in
    chord_deg=5.0,                 # the arcs as chords of at most this many degrees (and 0.5 mm)
    options=['-s', 'ludecomp', '-m', 'direct', '-a', 'off'],   # FastHenry's dense direct solve
)


def build(board, zl, nwinc, nhinc):
    m = C.Model(title=f'E02 coaxial loops, {nwinc} x {nhinc} filaments')
    C.add_board(m, board, zl, {'TX': 'TX', 'RX': 'RX'}, nwinc=nwinc, nhinc=nhinc,
                rw=SETTINGS['rw'] if nwinc > 1 else None, rh=SETTINGS['rw'] if nhinc > 1 else None,
                max_deg=SETTINGS['chord_deg'])
    (x0, y0), (x1, y1) = SETTINGS['ends_mm']
    for name in ('TX', 'RX'):
        lay = SETTINGS['layers'][name]
        m.port(name, C.nearest_node(m, name, lay, x0, y0, 0.01), C.nearest_node(m, name, lay, x1, y1, 0.01))
    return m


def references(dz_mm, n=21):
    """M of the two open arcs (each over theta, between its round ends' centres, the two gaps one above the other),
    by Neumann's double integral (references.arc_mutual), averaged over both widths with the current uniform across
    them (n x n radii), and the same for the closed rings (Maxwell's formula), for scale."""
    r, w = SETTINGS['radius_mm'], SETTINGS['width_mm']
    half_gap = math.asin((SETTINGS['gap_mm'] + w) / 2 / r)
    theta = 2 * math.pi - 2 * half_gap
    xs = r + np.linspace(-w / 2, w / 2, n)
    m_open = float(np.mean([[arc_mutual(a, b, dz_mm, theta) for b in xs] for a in xs]))
    m_ring = float(np.mean([[arc_mutual(a, b, dz_mm, 2 * math.pi) for b in xs] for a in xs]))
    return dict(dz_mm=dz_mm, theta_rad=theta, M_open_h=m_open, M_closed_h=m_ring,
                M_filament_open_h=arc_mutual(r, r, dz_mm, theta))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--nwinc', type=int, nargs='+', default=None, help='filaments across (with --nhinc)')
    ap.add_argument('--nhinc', type=int, default=1)
    ap.add_argument('--freqs', type=float, nargs='+', default=SETTINGS['freqs_hz'])
    ap.add_argument('--out', default=str(HERE / 'case'))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / 'run.log', 'a')

    def log(msg):
        print(msg, flush=True)
        logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
        logf.flush()
    export = S.kese_geometry(HERE / SETTINGS['board'], HERE / '3D_Geometry', log=log)
    zs = S.copper_layers(export)
    top = zs['F.Cu'][1]
    zl = {k: (z0 - top, z1 - top) for k, (z0, z1) in zs.items()}
    mid = {k: (z0 + z1) / 2 for k, (z0, z1) in zl.items()}
    dz = mid[SETTINGS['layers']['TX']] - mid[SETTINGS['layers']['RX']]
    board = K.read(HERE / SETTINGS['board'])
    res_file = HERE / 'results.json'
    old = json.loads(res_file.read_text()) if res_file.exists() else {}
    ref = old.get('references') if old.get('references', {}).get('dz_mm') == dz else references(dz)
    log(f"reference: M {ref['M_open_h'] * 1e9:.4f} nH for the open arcs {dz:g} mm apart")
    result = dict(board=SETTINGS['board'], settings=SETTINGS, stackup=zl, references=ref,
                  versions=S.versions([export]), runs=old.get('runs', []))
    ladder = [(n, a.nhinc) for n in a.nwinc] if a.nwinc else SETTINGS['ladder']
    for nw, nh in ladder:
        m = build(board, zl, nw, nh)
        solves = []
        for f in a.freqs:
            names, Z, secs, gb, text = C.run(m, f, out / f'w{nw}h{nh}_f{f:g}', SETTINGS['options'],
                                             sigma=SETTINGS['sigma'])
            rows = C.coil_rows(names, Z, f, driven='TX')
            tx, rx = rows['TX'], rows['RX']
            solves.append(dict(frequency_hz=f, M_h=rx['M'], M_reverse_h=rx['M_reverse'], L_TX_h=tx['L'],
                               R_TX_ohm=tx['R'], L_RX_h=rx['L_self'], R_RX_ohm=rx['Z_self'][0], seconds=round(secs, 2),
                               peak_memory_gb=round(gb, 3), size=C.size_of(text)))
            log(f"{nw} x {nh} filaments, f {f:.4g} Hz: M {rx['M'] * 1e9:.4f} nH (reverse {rx['M_reverse'] * 1e9:.4f}), "
                f"L_TX {tx['L'] * 1e9:.3f} nH, R_TX {tx['R'] * 1e3:.3f} mOhm, {m.filaments} filaments, {secs:.1f} s")
        result['runs'] = [r for r in result['runs'] if (r['nwinc'], r['nhinc']) != (nw, nh)]
        result['runs'].append(dict(nwinc=nw, nhinc=nh, segments=len(m.segs), filaments=m.filaments, solves=solves))
        result['runs'].sort(key=lambda r: (r['nhinc'], r['nwinc']))
        res_file.write_text(json.dumps(result, indent=1))
    log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
