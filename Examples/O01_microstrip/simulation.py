"""O01: a straight 50 ohm class microstrip, 2.9 mm on a 1.53 mm FR-4 core (eps_r 4.4) over a solid ground: its
characteristic impedance and effective permittivity from openEMS, against Hammerstad and Jensen's formulas with
the strip's thickness, and Kirschning and Jansen's dispersion of eps_eff.

    python simulation.py                 the run (a few minutes on 4 cores)
    python simulation.py --h-edge 0.1    a finer mesh at the strip's edges

Each port measures its line's impedance and propagation constant from its own probes, so the line is checked
without any reference impedance. Port 1 is excited; S11 and S21 are the one column that run gives.
Writes results.json beside this file and the run under case/ (not committed). Every setting is in SETTINGS.
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
from bridge import fdtd as F   # noqa: E402

SETTINGS = dict(
    board='O01_microstrip.kicad_pcb',
    length_mm=50.0, width_mm=2.9, centre_kicad=(100.0, 100.0),
    f0_hz=3e9, fc_hz=2e9,                # Gaussian pulse: 1 to 5 GHz, with almost no DC (see the README)
    f_report_hz=[1e9, 2e9, 3e9, 4e9],
    port_len_mm=10.0, feed_shift_mm=0.0, meas_shift_mm=6.0, feed_r_ohm=50.0,
    mesh=dict(f_max=5e9, res_div=30, h_edge=0.2, dielectric_cells=6, copper_cells=1, ratio=1.4,
              air_mm=(15.0, 15.0, 15.0)),
    boundaries=['MUR'] * 6,           # a quarter wavelength of air at 5 GHz all round the board
    end_criteria=1e-4,                   # -40 dB of the peak energy
    max_steps=80000,
    threads=4,
    engine='cpu',                        # openEMS's CPU engine; None for the default engine of an older build
)


def hammerstad_jensen(w, h, t, er):
    """Z0 (ohm) and eps_eff of a microstrip, w, h, t in any one unit: Hammerstad and Jensen (1980), with their
    correction for the strip's thickness."""
    eta0 = 376.730313668

    def z01(u):
        f = 6 + (2 * math.pi - 6) * math.exp(-(30.666 / u) ** 0.7528)
        return eta0 / (2 * math.pi) * math.log(f / u + math.sqrt(1 + 4 / u ** 2))

    def ee(u):
        a = 1 + math.log((u ** 4 + (u / 52) ** 2) / (u ** 4 + 0.432)) / 49 + math.log(1 + (u / 18.1) ** 3) / 18.7
        b = 0.564 * ((er - 0.9) / (er + 3)) ** 0.053
        return (er + 1) / 2 + (er - 1) / 2 * (1 + 10 / u) ** (-a * b)
    u, tn = w / h, t / h
    du1 = tn / math.pi * math.log(1 + 4 * math.e / (tn / math.tanh(math.sqrt(6.517 * u)) ** 2))
    dur = 0.5 * (1 + 1 / math.cosh(math.sqrt(er - 1))) * du1
    u1, ur = u + du1, u + dur
    eps = ee(ur) * (z01(u1) / z01(ur)) ** 2
    z0 = z01(ur) / math.sqrt(ee(ur))
    return z0, eps


def kirschning_jansen_eps(eps0, w, h, er, f_hz):
    """eps_eff at f from its quasi-static value: Kirschning and Jansen (1982), h in mm."""
    u = w / h
    fn = f_hz * 1e-9 * h                 # GHz mm
    p1 = 0.27488 + (0.6315 + 0.525 / (1 + 0.0157 * fn) ** 20) * u - 0.065683 * math.exp(-8.7513 * u)
    p2 = 0.33622 * (1 - math.exp(-0.03442 * er))
    p3 = 0.0363 * math.exp(-4.6 * u) * (1 - math.exp(-(fn / 38.7) ** 4.97))
    p4 = 1 + 2.751 * (1 - math.exp(-(er / 15.916) ** 8))
    p = p1 * p2 * ((0.1844 + p3 * p4) * fn) ** 1.5763
    return er - (er - eps0) / (1 + p)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--h-edge', type=float, default=SETTINGS['mesh']['h_edge'])
    ap.add_argument('--out', default=str(HERE / 'case'))
    ap.add_argument('--reuse', action='store_true', help='read the last run again instead of running openEMS')
    ap.add_argument('--engine', default=SETTINGS['engine'] or 'default',
                    help="openEMS engine: cpu, multithreaded, basic, or default (openEMS's own choice)")
    a = ap.parse_args()
    engine = None if a.engine == 'default' else a.engine
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / 'run.log', 'a')

    def log(msg):
        print(msg, flush=True)
        logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
        logf.flush()
    export = F.kese_export(HERE / SETTINGS['board'], out / 'kese', log=log)
    parts, mats = F.load(export)
    trace = next(p for p in parts if p.net == 'RF')
    gnd = next(p for p in parts if p.role == 'copper' and p.net != 'RF')
    board = next(p for p in parts if p.role == 'board')
    h = board.z[1] - board.z[0]
    t = trace.z[1] - trace.z[0]
    er = board.props['epsilon_r']
    w, L = SETTINGS['width_mm'], SETTINGS['length_mm']
    cx, cy = F.kicad_to_model(*SETTINGS['centre_kicad'])
    x0, x1 = cx - L / 2, cx + L / 2
    z_strip, z_ref = board.z[1], gnd.z[1]           # the strip's underside and the ground's top
    pl, fs, ms = SETTINGS['port_len_mm'], SETTINGS['feed_shift_mm'], SETTINGS['meas_shift_mm']
    fr = SETTINGS['feed_r_ohm']
    top, pad = trace.z[1], a.h_edge         # the current probes enclose the whole 35 um strip (fdtd.py)
    ports = [F.MSLPortSpec(1, 'RF', gnd.net, (x0, cy - w / 2, z_strip), (x0 + pl, cy + w / 2, z_ref), 'x', 1.0,
                           fs, ms, fr, top, pad),
             F.MSLPortSpec(2, 'RF', gnd.net, (x1, cy - w / 2, z_strip), (x1 - pl, cy + w / 2, z_ref), 'x', 0.0,
                           fs, ms, fr, top, pad)]
    spec = F.MeshSpec(**{**SETTINGS['mesh'], 'h_edge': a.h_edge})
    spec.extra = {0: [x0, x1, x0 + ms, x1 - ms]}
    lines, info = F.make_mesh(parts, spec)
    checks = F.preflight(lines, parts, ports, spec, info, log=log)
    FDTD, CSX, pobj = F.build(parts, lines, ports, SETTINGS['f0_hz'], SETTINGS['fc_hz'], SETTINGS['boundaries'],
                              end_criteria=SETTINGS['end_criteria'], max_steps=SETTINGS['max_steps'])
    tag = f'h{a.h_edge:g}' + ('' if a.engine == (SETTINGS['engine'] or 'default') else f'_{a.engine}')
    sim = out / tag
    if a.reuse and (sim / 'port_ut_1B').exists():
        seconds = json.loads((HERE / 'results.json').read_text()).get('seconds', 0.0) if (HERE / 'results.json').exists() else 0.0
        log(f'reusing the run in {sim}')
    else:
        seconds = F.run(FDTD, sim, threads=SETTINGS['threads'], engine=engine, log=log)
    freqs = np.linspace(1e9, 5e9, 41)
    res = F.port_results(pobj, sim, freqs, excited=1)

    # eps_eff a second way: from S21's phase over the line between the two measurement planes (S is referred to
    # each port's own line impedance, so S21 is the line's transmission between the planes)
    planes = [res['lines'][k]['meas_plane_mm'] for k in ('1', '2')]
    l_planes = abs(planes[1] - planes[0]) * 1e-3
    s21 = np.array([complex(*v) for v in res['S']['S21']])
    phase = -np.unwrap(np.angle(s21))
    phase += 2 * np.pi * np.round((2 * np.pi * freqs[0] * l_planes * np.sqrt(3.3) / F.C0 - phase[0]) / (2 * np.pi))
    eps_s21 = (phase * F.C0 / (2 * np.pi * freqs * l_planes)) ** 2
    res['eps_eff_from_S21'] = [float(v) for v in eps_s21]
    res['line_between_planes_mm'] = l_planes * 1e3
    z0_hj, eps_hj = hammerstad_jensen(w, h, t, er)
    ref = dict(h_mm=h, t_mm=t, eps_r=er, Z0_ohm=z0_hj, eps_eff_static=eps_hj,
               eps_eff=[kirschning_jansen_eps(eps_hj, w, h, er, f) for f in freqs])
    report = []
    for f in SETTINGS['f_report_hz']:
        k = int(np.argmin(abs(freqs - f)))
        zl = res['lines']['1'].get('Z_line_ohm')
        ee = res['lines']['1'].get('eps_eff')
        report.append(dict(f_hz=float(freqs[k]), Z0_ohm=zl[k][0] if zl else None, eps_eff=ee[k] if ee else None,
                           eps_eff_from_S21=float(eps_s21[k]),
                           Z0_ref_ohm=z0_hj, eps_eff_ref=ref['eps_eff'][k],
                           S21_db=20 * math.log10(abs(complex(*res['S']['S21'][k]))),
                           S11_db=20 * math.log10(max(abs(complex(*res['S']['S11'][k])), 1e-12))))
        r = report[-1]
        log(f"{r['f_hz'] / 1e9:.2f} GHz: Z0 {r['Z0_ohm']:.2f} ohm (ref {z0_hj:.2f}), eps_eff {r['eps_eff']:.4f} from "
            f"the port, {r['eps_eff_from_S21']:.4f} from S21 (ref {r['eps_eff_ref']:.4f}), S21 {r['S21_db']:.3f} dB, "
            f"S11 {r['S11_db']:.1f} dB")
    result = dict(board=SETTINGS['board'], settings=SETTINGS, h_edge_mm=a.h_edge, engine=a.engine, versions=F.versions(),
                  code=F.code_hashes(__file__), preflight=[dict(check=c, ok=bool(o), detail=d) for c, o, d in checks],
                  mesh=dict(cells={n: len(lines[i]) - 1 for i, n in enumerate('xyz')}, **{k: v for k, v in info.items()
                                                                                         if k != 'box'}),
                  seconds=round(seconds, 1), references=ref, report=report, data=res)
    name = 'results.json' if tag == f"h{SETTINGS['mesh']['h_edge']:g}" else f'results_{tag}.json'
    (HERE / name).write_text(json.dumps(result, indent=1))
    log(f'wrote {HERE / name}')


if __name__ == '__main__':
    main()
