"""S0_1x_OD21_2L_tiny in Elmer: the SIN and COS curves over a full turn of the rotor, at any air gap.

    python simulation.py                          the rotor away, then every angle in SETTINGS['angles_deg']
    python simulation.py --gap 0.5                the same at a 0.5 mm air gap (copper to copper)
    python simulation.py --angles 0 90 --no-away  the rotor at 0 and 90 degrees only
    python simulation.py --step 10                every 10 degrees from 0 to 350 instead of every 45
    python simulation.py --plot                   only redraw the curves from the results already written

The board is one electrical period per turn, so a full turn of the rotor gives one period of each curve: SIN
follows the sine of the rotor's angle and COS its cosine. The TX carries 1 A at 3.5 MHz; SIN and COS carry none,
so their voltages are the EMFs the TX induces in them, given here as mutual inductances (EMF = 2 pi f M x 1 A:
1 nH is 22 mV at 3.5 MHz).

The rotor is a half ring, so its outline turns with it and every angle gets its own mesh (S2 draws its four
sectors' few positions into one mesh instead). The stator's mesh then differs a little between angles, which
shows as small noise on the curves; the fit printed at the end says how much.

Writes results_gap<gap>mm.json, a table (.csv) and the curves (.png) beside this file, and the runs under case/
(not committed). Every setting is in SETTINGS. This script is GPL-3.0 as the bridge; the boards beside it keep
their own licence (see ../LICENSE.md).
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
import time
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Point

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from bridge import elmer_case as E, geometry as G, mesh25d as M, ports as P, study as S   # noqa: E402

SPEC = json.loads((HERE / 'test_spec.json').read_text())
AXIS = (100.0, -100.0)                 # KiCad (100, 100) in model coordinates, y up


def model_xy(xy_kicad):
    """KiCad (x, y) to model (x, y), on the mesher's 0.5 um grid so that a sheet's line lands on mesh edges."""
    return round(xy_kicad[0] * 2000) / 2000, round(-xy_kicad[1] * 2000) / 2000


SETTINGS = dict(
    stator='Stator.kicad_pcb',
    rotor='Rotor.kicad_pcb',
    names={'TX': 'TX', '1': 'COS', '2': 'SIN'},    # KESE's copper part per net -> the coil's name
    sigma=5.8e7,
    freq_hz=SPEC['sets'][0]['f_Hz'],
    air_gap_mm=SPEC['air_gap_mm'],     # stator F.Cu top to rotor copper face; --gap sets another
    insulators=False,                  # FR-4 and mask are air to the magneto-quasi-static solve
    angles_deg=SPEC['sets'][0]['sweep_angles_mech_deg'],
    domain_radius_mm=SPEC['air_box']['radius_or_half_width_mm'],
    domain_margin_mm=SPEC['air_box']['radius_or_half_width_mm'],   # air above the rotor and below the stator
    tx_end=model_xy(SPEC['terminals']['TX']['ends_xy_kicad']),
    tx_end_radius_mm=0.1,              # the trace ends' round caps (0.2 mm traces)
    rx_vias={'SIN': model_xy(SPEC['terminals']['2']['via_xy_kicad']),
             'COS': model_xy(SPEC['terminals']['1']['via_xy_kicad'])},
    via_void_radius_mm=0.3,            # the barrel (drill 0.4 mm) is left out inside this radius; the pad is 0.4
    sheet_half_mm=0.08,                # half the length of a TX sheet's line; an RX sheet's is 0.25
    level=0.75,                        # 0.75: about 12 GB a solve; 1.0 (S2's) about 16 GB
    mesh=dict(h_edge=0.1, h_in=0.2, h_max=6.0, grade=0.5, dz_copper=0.018, dz_max=0.4,
              tet_max=8.0, tet_grade=0.7),
    threads=4,
    tol=1e-7,
    max_iter=1500,
    ilu_order=None,                    # None: the circuit preconditioner alone, as in Elmer's tests; 0: with ILU0
)


def stator_parts(export):
    mats = json.loads((export / 'materials.json').read_text())
    top = G.copper_top(mats)
    names = SETTINGS['names']

    def body_of(name, info):
        if info['role'] == 'copper':
            return names.get(str(info.get('net')), 'COPPER_' + str(info.get('net')))
        return 'MASK' if info['role'] == 'mask' else 'FR4'
    parts, _ = G.load_parts(export, z_shift=-top, body_of=body_of)
    return parts


def rotor_parts(export, angle_deg, gap, body='ROTOR'):
    """The rotor as drawn, turned copper side down without mirroring, its copper face `gap` above z = 0, turned
    by angle_deg about the axis in KiCad's sense."""
    mats = json.loads((export / 'materials.json').read_text())
    cu = [i for i in mats['parts'].values() if i['role'] == 'copper']
    face = max(i['z_range_mm'][1] for i in cu)            # the copper's outer face, which turns to face down
    parts, _ = G.load_parts(export, z_shift=gap + face, flip=True, rotate_deg=angle_deg, axis=AXIS, prefix='R_',
                            body_of=lambda n, i: body if i['role'] == 'copper' else 'R_' + i['role'].upper())
    return parts


def voids(stator):
    """Air parts that leave the two RX vias' barrels out (priority over copper), through the dielectric."""
    out = []
    for name, xy in SETTINGS['rx_vias'].items():
        lo, hi = next(p.zrange for p in stator if p.body == name)
        lv = sorted({z for p in stator if p.body == name for z in p.levels()})
        inner = [z for z in lv if lo < z < hi]           # the dielectric's span between the two coppers
        disc = Point(xy).buffer(SETTINGS['via_void_radius_mm'], 64)
        out.append(M.Part(name=f'{name}_via_void', body='AIR', role='void', priority=4,
                          fixed={(min(inner), max(inner)): disc}))
    return out


def coil_zrange(lay, body):
    zs = [z for p in lay.parts if p.body == body for z in p.zrange]
    return min(zs), max(zs)


def build(stator_export, rotor_export, angle, gap, level, log=print):
    """The mesh with the rotor at `angle` (degrees, KiCad's sense), or away (None: its copper made air), and the
    terminals' boundaries."""
    st = SETTINGS['mesh']
    stator = stator_parts(stator_export)
    rot = rotor_parts(rotor_export, 0.0 if angle is None else angle, gap, body='AIR' if angle is None else 'ROTOR')
    top = max(z for p in rot for z in p.zrange)
    bottom = min(z for p in stator for z in p.zrange)
    zbox = (bottom - SETTINGS['domain_margin_mm'], top + SETTINGS['domain_margin_mm'])
    lay = M.Layout(stator + voids(stator) + rot, M.disc(AXIS, SETTINGS['domain_radius_mm'], h=st['h_max']),
                   zbox).build(log=log, insulators=SETTINGS['insulators'])
    sheets = {}
    tx = SETTINGS['tx_end']
    h = SETTINGS['sheet_half_mm']
    sheets['TX'] = LineString([(tx[0] - h, tx[1]), (tx[0] + h, tx[1])])
    for name, xy in SETTINGS['rx_vias'].items():
        sheets[name] = LineString([(xy[0] - 0.25, xy[1]), (xy[0] + 0.25, xy[1])])
    s = dict(st)
    for k in ('h_edge', 'h_in', 'dz_copper'):
        s[k] = st[k] / level
    m = M.build_mesh(lay, M.Settings(**s), extra_lines=list(sheets.values()), log=log)
    t, tp, q, qp = M.outer_faces(m)
    bnds = [('OUTER', t, tp, q, qp)]
    for name in ('TX', 'SIN', 'COS'):
        k = m['names'].index(name)
        if name == 'TX':
            hole = Point(tx).buffer(SETTINGS['tx_end_radius_mm'], 32)
        else:
            hole = Point(SETTINGS['rx_vias'][name]).buffer(SETTINGS['via_void_radius_mm'], 64)
        lo, hi = coil_zrange(lay, name)
        lv = sorted({z for p in lay.parts if p.body == name for z in p.levels()})
        inner = [z for z in lv if lo < z < hi]
        b0, b1 = min(inner), max(inner)                   # the faces of the copper toward the dielectric
        e1, e2 = P.electrodes(m, k, hole, b0, b1)
        qs, qsp = M.vertical_faces(m, b0, b1, sheets[name], tol=1e-4)
        bnds += [(f'{name}_T1', *e1), (f'{name}_T2', *e2), (f'{name}_SHEET', t[:0], tp[:0], qs, qsp)]
        log(f'{name}: electrodes {len(e1[0]) + len(e1[2])} and {len(e2[0]) + len(e2[2])} faces, sheet {len(qs)} '
            f'faces, z {b0:.4f} to {b1:.4f}')
    return m, bnds


def fit(angles, values):
    """The best fit a + b sin(t) + c cos(t): offset, amplitude, phase (degrees) and the rms of what is left."""
    t = np.radians(np.asarray(angles, float))
    y = np.asarray(values, float)
    A = np.c_[np.ones_like(t), np.sin(t), np.cos(t)]
    (a, b, c), *_ = np.linalg.lstsq(A, y, rcond=None)
    rest = y - A @ np.array([a, b, c])
    return dict(offset=a, amplitude=math.hypot(b, c), phase_deg=math.degrees(math.atan2(c, b)),
                rms_left=float(np.sqrt(np.mean(rest ** 2))) if len(y) > 3 else None)


def through_points(angles, values, tt):
    """The smooth periodic curve through every point: with the angles evenly spread over a turn, the trigonometric
    interpolation (the lowest harmonics that pass through every point exactly); otherwise the best sine fit."""
    a = np.asarray(angles, float)
    y = np.asarray(values, float)
    n = len(a)
    if n >= 3 and np.allclose(a, np.arange(n) * 360.0 / n):
        c = np.fft.rfft(y) / n
        t = np.radians(tt)
        out = np.full_like(t, c[0].real)
        for k in range(1, len(c)):
            w = 1.0 if (n % 2 == 0 and k == n // 2) else 2.0
            out += w * (c[k] * np.exp(1j * k * t)).real
        return out, 'interpolated through the points'
    f = fit(angles, values)
    return f['offset'] + f['amplitude'] * np.sin(np.radians(tt) + np.radians(f['phase_deg'])), 'best sine fit'


def plot(res_file, log=print):
    """The table and the curves of one results file: M of SIN and COS (nH) against the rotor's angle."""
    result = json.loads(res_file.read_text())
    runs = sorted((r for r in result['runs'] if r['rotor_deg'] != 'away'), key=lambda r: r['rotor_deg'])
    if not runs:
        return
    ang = [r['rotor_deg'] for r in runs]
    msin = [r['solve']['coils']['SIN']['M'] * 1e9 for r in runs]
    mcos = [r['solve']['coils']['COS']['M'] * 1e9 for r in runs]
    ltx = [r['solve']['coils']['TX']['L'] * 1e9 for r in runs]
    stem = res_file.with_suffix('')
    with open(f'{stem}.csv', 'w') as f:
        f.write('rotor_deg,M_SIN_nH,M_COS_nH,L_TX_nH,EMF_SIN_mV,EMF_COS_mV\n')
        w = 2 * math.pi * SETTINGS['freq_hz']
        for a, s, c, lt in zip(ang, msin, mcos, ltx):
            f.write(f'{a:g},{s:.5f},{c:.5f},{lt:.5f},{w * s * 1e-6:.4f},{w * c * 1e-6:.4f}\n')
    fits = {'SIN': fit(ang, msin), 'COS': fit(ang, mcos)}
    result['fit_nH'] = fits
    res_file.write_text(json.dumps(result, indent=1))

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    ink, ink2, grid, surface = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
    blue, orange = '#2a78d6', '#eb6834'                  # categorical slots 1 and 2 of the house palette
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=200)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    tt = np.linspace(0, 360, 721)
    how = None
    for name, y, col in (('SIN', msin, blue), ('COS', mcos, orange)):
        if len(y) >= 3:
            yy, how = through_points(ang, y, tt)
            ax.plot(tt, yy, color=col, lw=1.6, ls=(0, (5, 3)), zorder=2)
            ax.annotate(name, (360, yy[-1]), xytext=(6, 0), textcoords='offset points', va='center', color=ink,
                        fontsize=9, annotation_clip=False)
        ax.plot(ang, y, ls='none', color=col, marker='o', ms=7, mec=surface, mew=1.5, label=f'{name}, one Elmer solve',
                zorder=3)
    ax.axhline(0, color=ink2, lw=0.8, zorder=1)
    ax.set_xlim(0, 360)
    ax.set_xticks(range(0, 361, 45))
    ax.set_xlabel('rotor angle (degrees)', color=ink2)
    ax.set_ylabel('M from the TX (nH)', color=ink2)
    gap, level = result['gap_mm'], result['level']
    ax.set_title(f'{result["board"]}: SIN and COS against the rotor angle, {gap:g} mm air gap', color=ink,
                 fontsize=11, loc='left', pad=20)
    ax.text(0, 1.015, f'1 A at {SETTINGS["freq_hz"] / 1e6:g} MHz in the TX; dots: one solve each; dashes: '
            f'{how or "drawn once three angles are solved"}; mesh level {level:g}', transform=ax.transAxes,
            fontsize=8, color=ink2, va='bottom')
    ax.grid(True, color=grid, lw=0.6)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=ink2, labelsize=8)
    ax.legend(frameon=False, fontsize=8, labelcolor=ink, loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=2)
    fig.tight_layout()
    fig.savefig(f'{stem}.png', facecolor=surface)
    plt.close(fig)
    log(f'wrote {stem}.csv and {stem}.png; fit (nH): ' + '; '.join(
        f"{k} amplitude {v['amplitude']:.3f}, offset {v['offset']:.3f}, phase {v['phase_deg']:.1f} deg"
        + (f", rms left {v['rms_left']:.4f}" if v['rms_left'] is not None else '') for k, v in fits.items()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--angles', type=float, nargs='*', default=None)
    ap.add_argument('--step', type=float, default=None, help='every STEP degrees from 0 to below 360')
    ap.add_argument('--gap', type=float, default=SETTINGS['air_gap_mm'], help='air gap, copper to copper (mm)')
    ap.add_argument('--no-away', action='store_true', help='skip the run with the rotor away')
    ap.add_argument('--level', type=float, default=SETTINGS['level'])
    ap.add_argument('--ilu', type=int, default=SETTINGS['ilu_order'], help='ILU order for the preconditioner')
    ap.add_argument('--mesh-only', action='store_true', help='build and write the meshes, solve nothing')
    ap.add_argument('--plot', action='store_true', help='only redraw the table and the curves')
    ap.add_argument('--out', default=str(HERE / 'case'))
    a = ap.parse_args()
    tagg = (f'gap{a.gap:g}mm' + ('' if a.level == SETTINGS['level'] else f'_level{a.level:g}')
            + ('' if a.ilu == SETTINGS['ilu_order'] else f'_ilu{a.ilu}'))
    res_file = HERE / f'results_{tagg}.json'
    if a.plot:
        plot(res_file)
        return
    if a.angles is not None:
        angles = list(a.angles)
    elif a.step:
        angles = [float(x) for x in np.arange(0.0, 360.0 - 1e-9, a.step)]
    else:
        angles = [float(x) for x in SETTINGS['angles_deg']]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / 'run.log', 'a')

    def log(msg):
        print(msg, flush=True)
        logf.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
        logf.flush()
    se = S.kese_export(HERE / SETTINGS['stator'], out / 'kese', log=log)
    re_ = S.kese_export(HERE / SETTINGS['rotor'], out / 'kese', log=log)
    result = json.loads(res_file.read_text()) if res_file.exists() else dict(
        board=HERE.name, gap_mm=a.gap, level=a.level, ilu_order=a.ilu, settings=SETTINGS, expected=SPEC['expected'],
        versions=S.versions(), runs=[])
    done = {r['rotor_deg'] for r in result['runs']}
    runs = ([] if a.no_away else [None]) + angles
    for angle in runs:
        key = 'away' if angle is None else angle
        if key in done and not a.mesh_only:
            log(f'{key}: already in {res_file.name}, skipped')
            continue
        tag = 'away' if angle is None else f'rotor{angle:g}'
        t0 = time.time()
        m, bnds = build(se, re_, angle, a.gap, a.level, log)
        mesh = dict(seconds=round(time.time() - t0, 1), nodes=len(m['nodes']), wedges=len(m['wedges']),
                    tetrahedra=len(m['tets']), triangles=int(m['nt']), layers=int(m['nk']))
        log(f'{tag}: mesh {mesh}')
        folder = out / f'{tagg}_{tag}'
        M.write_elmer(m, folder / 'mesh_files', bnds, log=log)
        if a.mesh_only:
            continue
        cu = E.Material('Copper', sigma=SETTINGS['sigma'])
        bodies = {n: (cu if n in ('TX', 'SIN', 'COS', 'ROTOR') else E.Material('Air' if n == 'AIR' else n.title()))
                  for n in m['names']}
        case = E.Case(mesh_dir=folder / 'mesh_files', bodies=bodies, order=1, tol=SETTINGS['tol'],
                      max_iter=SETTINGS['max_iter'], ilu_order=a.ilu,
                      coils=[E.Coil('TX', 'TX', 'TX_T1', 'TX_T2', 'TX_SHEET', 1.0),
                             E.Coil('SIN', 'SIN', 'SIN_T1', 'SIN_T2', 'SIN_SHEET', 0.0),
                             E.Coil('COS', 'COS', 'COS_T1', 'COS_T2', 'COS_SHEET', 0.0)])
        rows = S.solve(case, [SETTINGS['freq_hz']], folder, threads=SETTINGS['threads'], log=log, tag=tag)
        result['runs'] = [r for r in result['runs'] if r['rotor_deg'] != key]
        result['runs'].append(dict(rotor_deg=key, mesh=mesh, solve=rows[0]))
        result['runs'].sort(key=lambda r: -1 if r['rotor_deg'] == 'away' else r['rotor_deg'])
        res_file.write_text(json.dumps(result, indent=1))
        c = rows[0]['coils']
        log(f"{tag}: L_TX {c['TX']['L'] * 1e9:.3f} nH, R_TX {c['TX']['R'] * 1e3:.2f} mOhm, "
            f"M_SIN {c['SIN']['M'] * 1e9:.4f} nH, M_COS {c['COS']['M'] * 1e9:.4f} nH, {rows[0]['iterations']} it, "
            f"res {rows[0]['residual']}, {rows[0]['peak_memory_gb']} GB, {rows[0]['seconds']} s")
        shutil.rmtree(folder / 'mesh_files', ignore_errors=True)       # the mesh is large; the results stay
        plot(res_file, log)
    if not a.mesh_only:
        log(f'wrote {res_file}')


if __name__ == '__main__':
    main()
