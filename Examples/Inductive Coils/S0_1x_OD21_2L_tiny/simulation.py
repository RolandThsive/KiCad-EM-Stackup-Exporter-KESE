"""A coil set from the Sinusoidal Coil Generator in Elmer: the SIN and COS curves against the rotor's angle, at any
air gap. Everything that belongs to the board is in test_spec.json beside this file, so the same script runs every
single-set board that new_coil.py (one folder up) sets up; this folder's README says what this board is.

    python simulation.py                          the rotor away, then every angle in test_spec.json
    python simulation.py --gap 0.5                the same at a 0.5 mm air gap (copper to copper)
    python simulation.py --angles 0 90 --no-away  the rotor at 0 and 90 degrees only
    python simulation.py --step 10                every 10 degrees over one turn of the rotor's pattern
    python simulation.py --plot                   only redraw the curves from the results already written
    python simulation.py --angles 0 --mesh-only   build one mesh and say its size, to judge the memory

The TX carries 1 A; SIN and COS carry none, so their voltages are the EMFs the TX induces in them, given as mutual
inductances (EMF = 2 pi f M x 1 A: 1 nH is 22 mV at 3.5 MHz). The rotor repeats itself every 360 / sectors degrees,
so the curves are drawn over that span: a full turn on a one-sector rotor.

Every angle gets its own mesh, the rotor's copper at that angle drawn into it. The stator's mesh then differs a
little between angles, which shows as small noise on the curves; the fit written with the results says how much.

Writes results_gap<gap>mm.json, a table (.csv) and the curves (.png) beside this file, and SINCOS_Results.md: every
gap's curves with a caption, the fit, the angle error and every solve, and SINCOS_gaps.png with all the gaps on one
chart once two are solved. The runs go under case/ (not committed). This script is GPL-3.0 as the bridge; the boards beside it keep their own licence (see
../LICENSE.md).
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


SET = SPEC['sets'][0]
SIN_NET, COS_NET = str(SET['sin']), str(SET['cos'])
SETTINGS = dict(
    stator='Stator.kicad_pcb',
    rotor='Rotor.kicad_pcb',
    names={str(k): v for k, v in SPEC['nets'].items()},   # KESE's copper part per net -> the coil's name
    sigma=5.8e7,
    freq_hz=SET['f_Hz'],
    air_gap_mm=SPEC['air_gap_mm'],     # stator F.Cu top to rotor copper face; --gap sets another
    insulators=False,                  # FR-4 and mask are air to the magneto-quasi-static solve
    angles_deg=SET['sweep_angles_mech_deg'],
    period_deg=SET.get('rotor_period_mech_deg', 360.0),   # the rotor repeats itself after this
    domain_radius_mm=SPEC['air_box']['radius_or_half_width_mm'],
    domain_margin_mm=SPEC['air_box']['radius_or_half_width_mm'],   # air above the rotor and below the stator
    tx_end=model_xy(SPEC['terminals']['TX']['ends_xy_kicad']),
    tx_end_radius_mm=SPEC['terminals']['TX'].get('end_radius_mm', 0.1),     # the trace ends' round caps
    rx_vias={'SIN': model_xy(SPEC['terminals'][SIN_NET]['via_xy_kicad']),
             'COS': model_xy(SPEC['terminals'][COS_NET]['via_xy_kicad'])},
    via_void_radius_mm=SPEC['terminals'][SIN_NET].get('void_radius_mm', 0.3),   # the barrel left out inside this
    sheet_half_mm=0.8 * SPEC['terminals']['TX'].get('end_radius_mm', 0.1),    # half a TX sheet's line
    rx_sheet_half_mm=0.25 / 0.3 * SPEC['terminals'][SIN_NET].get('void_radius_mm', 0.3),   # half an RX sheet's
    level=SPEC.get('mesh_level', 0.75),   # the copper's mesh sizes divided by this (S2's checks used 1.0)
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
        h2 = SETTINGS['rx_sheet_half_mm']
        sheets[name] = LineString([(xy[0] - h2, xy[1]), (xy[0] + h2, xy[1])])
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
    """The best fit a + b sin(t) + c cos(t), t the angle over the rotor's period as a full circle: offset, amplitude,
    phase (degrees) and the rms of what is left."""
    t = np.radians(np.asarray(angles, float) * 360.0 / SETTINGS['period_deg'])
    y = np.asarray(values, float)
    A = np.c_[np.ones_like(t), np.sin(t), np.cos(t)]
    (a, b, c), *_ = np.linalg.lstsq(A, y, rcond=None)
    rest = y - A @ np.array([a, b, c])
    return dict(offset=a, amplitude=math.hypot(b, c), phase_deg=math.degrees(math.atan2(c, b)),
                rms_left=float(np.sqrt(np.mean(rest ** 2))) if len(y) > 3 else None)


def through_points(angles, values, tt):
    """The smooth periodic curve through every point: with the angles evenly spread over the rotor's period, the
    trigonometric interpolation (the lowest harmonics that pass through every point exactly); otherwise the best
    sine fit."""
    a = np.asarray(angles, float)
    y = np.asarray(values, float)
    n = len(a)
    per = SETTINGS['period_deg']
    if n >= 3 and np.allclose(a, np.arange(n) * per / n):
        c = np.fft.rfft(y) / n
        t = np.radians(np.asarray(tt) * 360.0 / per)
        out = np.full_like(t, c[0].real)
        for k in range(1, len(c)):
            w = 1.0 if (n % 2 == 0 and k == n // 2) else 2.0
            out += w * (c[k] * np.exp(1j * k * t)).real
        return out, 'interpolated through the points'
    f = fit(angles, values)
    t = np.radians(np.asarray(tt) * 360.0 / per)
    return f['offset'] + f['amplitude'] * np.sin(t + np.radians(f['phase_deg'])), 'best sine fit'


def angle_error(ang, msin, mcos):
    """What a decoder would read from SIN and COS once the offset and gain of each are calibrated out (each from its
    best sine fit), less the true angle: rms and peak in electrical degrees, its mean taken off (a fixed offset only
    moves where zero is). Also the phase between the two fits, 90 degrees for perfect quadrature."""
    if len(ang) < 5:
        return None
    fs, fc = fit(ang, msin), fit(ang, mcos)
    u = np.radians(np.asarray(ang, float) * 360.0 / SETTINGS['period_deg'] + fs['phase_deg'])
    s = (np.asarray(msin, float) - fs['offset']) / fs['amplitude']          # sin(u)
    c = (np.asarray(mcos, float) - fc['offset']) / fc['amplitude']          # sin(u + d), d near +90 or -90
    d = math.radians(fc['phase_deg'] - fs['phase_deg'])
    e = np.angle(np.exp(1j * (np.arctan2(s, math.copysign(1.0, math.sin(d)) * c) - u)))
    e = np.degrees(np.angle(np.exp(1j * (e - np.angle(np.mean(np.exp(1j * e)))))))
    return dict(rms=float(np.sqrt(np.mean(e ** 2))), peak=float(np.abs(e).max()),
                sin_to_cos_deg=abs((math.degrees(d) + 180) % 360 - 180), points=len(e))


def report(log=print):
    """SINCOS_Results.md beside this file: for every air gap solved, the curves with a caption, the fit, the angle
    error and every solve; then the boards. Rewritten after every solve, so it is as current as the results."""
    import re
    gaps = sorted(((float(m.group(1)), p) for p in HERE.glob('results_gap*mm.json')
                   if (m := re.fullmatch(r'results_gap([0-9.]+)mm\.json', p.name))), key=lambda x: -x[0])
    if not gaps:
        return
    w = 2 * math.pi * SETTINGS['freq_hz'] * 1e-6                     # mV of EMF per nH at 1 A
    per = SETTINGS['period_deg']
    deg = (', the same as mechanical degrees here' if per == 360 and SET['loops'] == 1
           else f' ({per / 360:g} of a mechanical degree each)')
    st, ring, n_per = SPEC['stator'], SPEC['rotor']['rings'][0], SET['loops']
    rotor = ('a half-ring rotor' if ring['sectors'] == 1 and abs(ring['duty'] - 0.5) < 1e-6
             else f"a rotor of {ring['sectors']} copper sectors")
    summary, sections, curves = [], [], []
    for i, (gap, path) in enumerate(gaps, 1):
        res = json.loads(path.read_text())
        runs = sorted((r for r in res['runs'] if r['rotor_deg'] != 'away'), key=lambda r: r['rotor_deg'])
        away = [r for r in res['runs'] if r['rotor_deg'] == 'away']
        ang = [r['rotor_deg'] for r in runs]
        ms = [r['solve']['coils']['SIN']['M'] * 1e9 for r in runs]
        mc = [r['solve']['coils']['COS']['M'] * 1e9 for r in runs]
        lt = [r['solve']['coils']['TX']['L'] * 1e9 for r in runs]
        planned = max(len(SETTINGS['angles_deg']), len(ang))
        full = len(ang) >= planned
        fs, fc = (fit(ang, ms), fit(ang, mc)) if len(ang) >= 3 else (None, None)
        err = angle_error(ang, ms, mc)
        if fs:
            curves.append((gap, ang, ms, mc, fs, fc))
        so_far = '' if full else ' so far'
        summary.append(f"| {gap:g} mm | {len(ang)} of {planned} | "
                       + (f"{fs['amplitude']:.2f} / {fc['amplitude']:.2f} nH ({w * fs['amplitude']:.0f} / "
                          f"{w * fc['amplitude']:.0f} mV) |" if fs else '| ')
                       + (f" {err['rms']:.1f}° rms, {err['peak']:.1f}° peak{so_far} |" if err else ' |'))
        sec = [f'## {gap:g} mm air gap', '']
        png = path.with_suffix('.png').name
        if (HERE / png).exists() and fs:
            how = ('interpolated through them' if through_points(ang, ms, [0.0])[1] != 'best sine fit'
                   else 'a sine fit, drawn only between the solved angles while few are in')
            sec += [f'![SIN and COS against the rotor angle at a {gap:g} mm air gap]({png})', '',
                    f"*Figure {i}. SIN (blue) and COS (orange) at a {gap:g} mm air gap: the mutual inductance from "
                    f"the TX against the rotor's angle, {len(ang)} of {planned} angles solved. Each dot is one Elmer "
                    f"solve; the dashes are {how}. SIN swings ±{fs['amplitude']:.2f} nH and COS ±{fc['amplitude']:.2f} nH, that is "
                    f"±{w * fs['amplitude']:.0f} and ±{w * fc['amplitude']:.0f} mV of EMF.*", '']
            line = (f"Best sine fit: SIN amplitude {fs['amplitude']:.3f} nH, offset {fs['offset']:.3f} nH, phase "
                    f"{fs['phase_deg']:.1f}°; COS amplitude {fc['amplitude']:.3f} nH, offset {fc['offset']:.3f} nH, "
                    f"phase {fc['phase_deg']:.1f}°.")
            if err:
                line += (f" Angle error{so_far}, with the offset and gain of each channel calibrated out: "
                         f"{err['rms']:.1f}° rms and {err['peak']:.1f}° at worst, in electrical degrees{deg}. SIN and "
                         f"COS are {err['sin_to_cos_deg']:.1f}° apart, against 90° for perfect quadrature.")
            sec += [line, '']
        elif not runs:
            sec += ['The first angle is solving; the curves appear here as the angles finish.', '']
        rows = ['| Rotor | M SIN (nH) | M COS (nH) | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |',
                '|---|---|---|---|---|---|---|---|---|']
        for r in away + runs:
            s, c = r['solve'], r['solve']['coils']
            rows.append(f"| {'away' if r['rotor_deg'] == 'away' else format(r['rotor_deg'], 'g') + '°'} | "
                        f"{c['SIN']['M'] * 1e9:.4f} | {c['COS']['M'] * 1e9:.4f} | {c['TX']['L'] * 1e9:.3f} | "
                        f"{c['TX']['R'] * 1e3:.2f} | {s['iterations']} | {s['residual']:.1e} | "
                        f"{s['peak_memory_gb']:.1f} GB | {s['seconds'] / 60:.0f} min |")
        if len(rows) > 2:
            sec += rows + ['']
        capped = [r for r in runs if r['solve']['iterations'] >= SETTINGS['max_iter']]
        if capped and len(lt) >= 2:
            res_ = [r['solve']['residual'] for r in capped]
            sec += [f"{len(capped)} of {len(runs)} solves stopped at the {SETTINGS['max_iter']}-iteration cap, with "
                    f"the residual between {min(res_):.1e} and {max(res_):.1e} rather than the {SETTINGS['tol']:.0e} "
                    f"asked for. The TX is round, so turning the rotor should not change its inductance: its spread "
                    f"here, {min(lt):.1f} to {max(lt):.1f} nH, is a measure of what the solver leaves.", '']
        sections.append('\n'.join(sec))
    pic = next((p.name for p in [HERE / f'{HERE.name}_stator_and_rotor.png'] if p.exists()),
               next((p.name for p in sorted(HERE.glob('*_Representative.svg'))), None))
    tx, rs, rc = (SPEC['terminals'][k] for k in ('TX', SIN_NET, COS_NET))
    xy = lambda t: '({:g}, {:g})'.format(*(round(v, 2) for v in t.get('via_xy_kicad') or t.get('ends_xy_kicad')))
    boards = ['## The boards', '']
    if pic:
        boards += [f'![stator and rotor]({pic})', '']
    boards += [f"*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is "
               f"opened at {xy(rs)} and COS at {xy(rc)}, the TX at its ends at {xy(tx)} (KiCad mm). The "
               f"[README](README.md) has the board and how it was made.*", '']
    text = '\n'.join([
        f'# {HERE.name}: SIN and COS over the rotor\'s turn in Elmer', '',
        f"A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-"
        f"Encoders-Coil-Generator): {2 * st['bore_and_outer_radius_mm'][1]:g} mm across, {len(st['layers'])} copper "
        f"layers, {'one electrical period' if n_per == 1 else f'{n_per} electrical periods'} per turn and {rotor}. The TX carries 1 A at "
        f"{SETTINGS['freq_hz'] / 1e6:g} MHz; the curves are the mutual inductance from the TX to SIN and to COS "
        f"(1 nH is {w:.0f} mV of EMF). Each angle is one Elmer solve with its own mesh. This page is rewritten by "
        f"`simulation.py` after every solve.", '',
        '| Air gap | Angles solved | Amplitude SIN / COS | Angle error |', '|---|---|---|---|', *summary, '',
        *sections, *gaps_figure(curves, len(sections) + 1), *boards])
    (HERE / 'SINCOS_Results.md').write_text(text)
    log('wrote SINCOS_Results.md')


def gaps_figure(curves, number):
    """With two air gaps or more solved, SINCOS_gaps.png: every gap's SIN and COS on one chart, the smallest gap in
    full colour and the larger ones lighter; returns its section for SINCOS_Results.md."""
    if len(curves) < 2:
        return []
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    ink, ink2, surface = '#0b0b0b', '#52514e', '#fcfcfb'
    base = {'SIN': (0x2a, 0x78, 0xd6), 'COS': (0xeb, 0x68, 0x34)}
    tint = lambda rgb, k: '#' + ''.join(f'{round(c * k + s * (1 - k)):02x}' for c, s in zip(rgb, (0xfc, 0xfc, 0xfb), strict=True))
    per = SETTINGS['period_deg']
    tt = np.linspace(0, per, 721)
    curves = sorted(curves, key=lambda c: c[0])
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=200)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    for j, (gap, ang, ms, mc, _, _) in enumerate(curves):
        k = 1.0 - 0.5 * j / (len(curves) - 1)
        for name, y in (('SIN', ms), ('COS', mc)):
            col = tint(base[name], k)
            yy, how = through_points(ang, y, tt)
            keep = (np.ones_like(tt, bool) if how != 'best sine fit' or max(ang) - min(ang) >= 0.75 * per
                    else (tt >= min(ang)) & (tt <= max(ang)))
            ax.plot(tt[keep], yy[keep], color=col, lw=1.6, ls=(0, (5, 3)), zorder=2)
            ax.plot(ang, y, ls='none', color=col, marker='o', ms=6, mec=surface, mew=1.2, zorder=3,
                    label=f'{name}, {gap:g} mm')
            if keep[-1]:
                ax.annotate(f'{name} {gap:g} mm', (tt[-1], yy[-1]), xytext=(6, 0), textcoords='offset points',
                            va='center', color=ink, fontsize=8, annotation_clip=False)
    ax.axhline(0, color=ink2, lw=0.8, zorder=1)
    ax.set_xlim(0, per)
    ax.set_xticks(np.linspace(0, per, 9))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g'))
    ax.set_xlabel('rotor angle (degrees)', color=ink2)
    ax.set_ylabel('M from the TX (nH)', color=ink2)
    ax.set_title(f'{HERE.name}: SIN and COS at each air gap', color=ink, fontsize=11, loc='left', pad=20)
    ax.text(0, 1.015, f'1 A at {SETTINGS["freq_hz"] / 1e6:g} MHz in the TX; dots: one solve each; the smallest gap '
            'in full colour', transform=ax.transAxes, fontsize=8, color=ink2, va='bottom')
    ax.grid(True, color='#e4e3df', lw=0.6)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=ink2, labelsize=8)
    ax.legend(frameon=False, fontsize=8, labelcolor=ink, loc='upper center', bbox_to_anchor=(0.5, -0.14),
              ncol=2 * len(curves))
    fig.tight_layout()
    fig.savefig(HERE / 'SINCOS_gaps.png', facecolor=surface)
    plt.close(fig)
    (g0, *_, fs0, fc0), (g1, *_, fs1, fc1) = curves[0], curves[-1]
    return ['## The air gaps together', '', '![SIN and COS at each air gap](SINCOS_gaps.png)', '',
            f"*Figure {number}. Every air gap on one chart, the {g0:g} mm gap in full colour. Going from {g1:g} to "
            f"{g0:g} mm makes SIN {fs0['amplitude'] / fs1['amplitude']:.2f} times and COS "
            f"{fc0['amplitude'] / fc1['amplitude']:.2f} times larger.*", '']


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
        for a, s, c, lt in zip(ang, msin, mcos, ltx, strict=True):
            f.write(f'{a:g},{s:.5f},{c:.5f},{lt:.5f},{w * s * 1e-6:.4f},{w * c * 1e-6:.4f}\n')
    fits = {'SIN': fit(ang, msin), 'COS': fit(ang, mcos)}
    result['fit_nH'] = fits
    result['angle_error_deg'] = angle_error(ang, msin, mcos)
    res_file.write_text(json.dumps(result, indent=1))

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    ink, ink2, grid, surface = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
    blue, orange = '#2a78d6', '#eb6834'                  # categorical slots 1 and 2 of the house palette
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=200)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    per = SETTINGS['period_deg']
    tt = np.linspace(0, per, 721)
    how = None
    for name, y, col in (('SIN', msin, blue), ('COS', mcos, orange)):
        if len(y) >= 3:
            yy, how = through_points(ang, y, tt)
            whole = how != 'best sine fit' or max(ang) - min(ang) >= 0.75 * per
            if not whole:                                # no guessing past the solved angles while few are in
                keep = (tt >= min(ang)) & (tt <= max(ang))
                tt_, yy = tt[keep], yy[keep]
                how = 'a sine fit, only between the solved angles for now'
            else:
                tt_ = tt
            ax.plot(tt_, yy, color=col, lw=1.6, ls=(0, (5, 3)), zorder=2)
            if whole:
                ax.annotate(name, (tt_[-1], yy[-1]), xytext=(6, 0), textcoords='offset points', va='center',
                            color=ink, fontsize=9, annotation_clip=False)
        ax.plot(ang, y, ls='none', color=col, marker='o', ms=7, mec=surface, mew=1.5, label=f'{name}, one Elmer solve',
                zorder=3)
    ax.axhline(0, color=ink2, lw=0.8, zorder=1)
    ax.set_xlim(0, per)
    ax.set_xticks(np.linspace(0, per, 9))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g'))
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
    report(log)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--angles', type=float, nargs='*', default=None)
    ap.add_argument('--step', type=float, default=None, help="every STEP degrees over the rotor's period")
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
        angles = [float(x) for x in np.arange(0.0, SETTINGS['period_deg'] - 1e-9, a.step)]
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
