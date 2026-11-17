"""E01: one circular trace, 20 mm across, opened by a 0.2 mm gap: its inductance and resistance from FastHenry,
against Grover's ring formula and the resistance of an annular sector.

    python simulation.py                      the filament ladder at both frequencies (a few minutes)
    python simulation.py --nwinc 9            9 filaments across the trace only
    python simulation.py --chord-deg 1        the arcs cut into chords of 1 degree instead of 5

The trace is two arcs on F.Cu; FastHenry gets them as straight segments (chords), each as wide as the trace and as
thick as its copper, split into nwinc filaments across and nhinc through. The port is between the two trace ends at
the gap. Writes results.json beside this file and the runs under case/ (not committed). Every setting is in
SETTINGS.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
sys.path.insert(0, str(HERE.parent))                  # Examples/references.py
from bridge import fasthenry_case as C, kicad as K, stackup as S   # noqa: E402
from references import arc_inductance, ring_inductance   # noqa: E402

SETTINGS = dict(
    board='E01_circular_loop.kicad_pcb',
    radius_mm=10.0,                # the trace's centre line
    width_mm=0.5,
    gap_mm=0.2,
    ends_mm=((109.993873, -100.35), (109.993873, -99.65)),   # the two trace ends at the gap, model coordinates
    sigma=5.8e7,                   # copper, S/m
    freqs_hz=[1e4, 3.5e6],         # uniform current (10 kHz, skin depth 0.66 mm) and the coils' frequency
    ladder=[(1, 1), (3, 1), (5, 1), (9, 1), (9, 3), (15, 3)],   # (filaments across, filaments through)
    rw=2.0,                        # each edge filament this much narrower than the next one in
    chord_deg=5.0,                 # the arcs as chords of at most this many degrees (and 0.5 mm)
    options=['-s', 'ludecomp', '-m', 'direct', '-a', 'off'],   # FastHenry's dense direct solve
)


def build(board, zl, nwinc, nhinc, chord_deg):
    m = C.Model(title=f'E01 circular loop, {nwinc} x {nhinc} filaments')
    C.add_board(m, board, zl, {'LOOP': 'LOOP'}, nwinc=nwinc, nhinc=nhinc, rw=SETTINGS['rw'] if nwinc > 1 else None,
                rh=SETTINGS['rw'] if nhinc > 1 else None, max_deg=chord_deg)
    (x0, y0), (x1, y1) = SETTINGS['ends_mm']
    a = C.nearest_node(m, 'LOOP', 'F.Cu', x0, y0, 0.01)
    b = C.nearest_node(m, 'LOOP', 'F.Cu', x1, y1, 0.01)
    m.port('LOOP', a, b)
    return m


def references(t):
    """The open loop is an arc of theta, between the centres of its two round ends. Its inductance as FastHenry sees
    it, with the port closing the loop at no length, is the arc's partial inductance: Neumann's double integral over
    the arc with the GMD (references.arc_inductance), at DC (the rectangle's GMD) and with the current crowded to
    the strip's edges (w / 4). Grover's ring formula for the closed ring, and that scaled by the share of the
    circle the arc covers, are given beside it: the scaling misses the ends' effect and reads 0.7 % high. R_dc is
    the annular sector's resistance between the arc's two ends. t: the copper's thickness (mm), from KESE's
    stack-up."""
    r, w = SETTINGS['radius_mm'], SETTINGS['width_mm']
    g_dc = 0.2235 * (w + t)                            # GMD of a w x t rectangle (Grover)
    g_hf = w / 4                                        # GMD of a thin strip with its edge-crowded current
    half_gap = math.asin((SETTINGS['gap_mm'] + w) / 2 / r)   # the round ends' centres sit (gap + w) apart
    theta = 2 * math.pi - 2 * half_gap
    share = theta / (2 * math.pi)
    r_dc = theta / (SETTINGS['sigma'] * t * 1e-3 * math.log((r + w / 2) / (r - w / 2)))
    l_dc, l_hf = ring_inductance(r, g_dc), ring_inductance(r, g_hf)
    return dict(L_arc_dc_h=arc_inductance(r, theta, g_dc), L_arc_hf_h=arc_inductance(r, theta, g_hf),
                L_ring_dc_h=l_dc, L_ring_hf_h=l_hf, arc_share=share, L_ring_share_dc_h=l_dc * share,
                L_ring_share_hf_h=l_hf * share, R_dc_ohm=r_dc, theta_rad=theta, gmd_dc_mm=g_dc, gmd_hf_mm=g_hf)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--nwinc', type=int, nargs='+', default=None, help='filaments across (with --nhinc)')
    ap.add_argument('--nhinc', type=int, default=1)
    ap.add_argument('--chord-deg', type=float, default=SETTINGS['chord_deg'])
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
    t = zl['F.Cu'][1] - zl['F.Cu'][0]
    board = K.read(HERE / SETTINGS['board'])
    res_file = HERE / 'results.json'
    old = json.loads(res_file.read_text()).get('runs', []) if res_file.exists() else []
    result = dict(board=SETTINGS['board'], settings=SETTINGS, copper_mm=t, references=references(t),
                  versions=S.versions([export]), runs=old)
    ladder = [(n, a.nhinc) for n in a.nwinc] if a.nwinc else SETTINGS['ladder']
    for nw, nh in ladder:
        m = build(board, zl, nw, nh, a.chord_deg)
        solves = []
        for f in a.freqs:
            names, Z, secs, gb, text = C.run(m, f, out / f'w{nw}h{nh}_chord{a.chord_deg:g}_f{f:g}',
                                             SETTINGS['options'], sigma=SETTINGS['sigma'])
            row = C.coil_rows(names, Z, f, driven='LOOP')['LOOP']
            solves.append(dict(frequency_hz=f, L_h=row['L'], R_ohm=row['R'], seconds=round(secs, 2),
                               peak_memory_gb=round(gb, 3), size=C.size_of(text)))
            log(f"{nw} x {nh} filaments, chords of {a.chord_deg:g} deg, f {f:.4g} Hz: L {row['L'] * 1e9:.3f} nH, "
                f"R {row['R'] * 1e3:.3f} mOhm, {m.filaments} filaments, {secs:.1f} s")
        run = dict(nwinc=nw, nhinc=nh, chord_deg=a.chord_deg, segments=len(m.segs), filaments=m.filaments,
                   solves=solves)
        result['runs'] = [r for r in result['runs'] if (r['nwinc'], r['nhinc'], r['chord_deg']) != (nw, nh, a.chord_deg)]
        result['runs'].append(run)
        result['runs'].sort(key=lambda r: (r['chord_deg'] != SETTINGS['chord_deg'], -r['chord_deg'], r['nhinc'],
                                           r['nwinc']))
        res_file.write_text(json.dumps(result, indent=1))
    log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
