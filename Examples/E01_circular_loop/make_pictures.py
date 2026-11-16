"""E01's and E02's pictures for the wiki, from Elmer's own output: nothing here is drawn by hand.

    python make_pictures.py [--out DIR]

Reads results.json (and results_grade.json, results_grade2.json, results_domain120.json when present) beside this
file, ../E02_coaxial_loops/results.json (and its results_grade.json), and the residual histories in residuals.json. residuals.json is collected
from the ElmerSolver logs under case/ when they are there (they are not committed), so the chart can be drawn again
without them. Writes lossless WebP files into DIR (default pictures/), laid out as the wiki keeps them:

    elmerresults_1_against_reference.webp                     L (E01) and M (E02) against their references
    E01_circular_loop/elmerresults_2_residual.webp            the linear solver's residual against its iterations
    E01_circular_loop/elmerresults_3_fields.webp              |B| round the loop and |J| across the trace, level 0.75
    E01_circular_loop/elmeraccuracy_1_air_mesh.webp           the mesh round the trace, two air gradings (Accuracy page)

The mesh picture needs the meshes under case/ and case_grade/, the fields picture the VTU files that
`simulation.py --levels 0.75 --max-iter 1500 --fields --out case_fields --results results_fields.json` writes; neither is committed, and
each picture is skipped without them.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E02 = HERE.parent / 'E02_coaxial_loops'

INK, INK2, GRID, SURFACE = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
BLUE, ORANGE, AQUA, VIOLET = '#2a78d6', '#eb6834', '#1baf7a', '#8a5cd1'


def style(ax, xlabel, ylabel):
    ax.set_facecolor(SURFACE)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_xlabel(xlabel, color=INK2, fontsize=10)
    ax.set_ylabel(ylabel, color=INK2, fontsize=10)


def save(fig, path):
    fig.savefig(path, format='webp', dpi=200, facecolor=SURFACE, pil_kwargs=dict(lossless=True))
    print('wrote', path)


def solve(run, f):
    return next((s for s in run['solves'] if s['frequency_hz'] == f), None)


EDGES = {504: [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)],                       # Elmer's tetrahedron
         706: [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3), (1, 4), (2, 5)]}  # and wedge


def read_elmer_mesh(folder):
    """Node coordinates (mm, indexed by node number) and {element type: (bodies, node numbers)} of an Elmer mesh."""
    nodes = np.loadtxt(folder / 'mesh.nodes')
    xyz = np.zeros((int(nodes[:, 0].max()) + 1, 3))
    xyz[nodes[:, 0].astype(int)] = nodes[:, 2:5]
    els = {}
    for line in open(folder / 'mesh.elements'):
        f = line.split()
        b, c = els.setdefault(int(f[2]), ([], []))
        b.append(int(f[1]))
        c.append([int(v) for v in f[3:]])
    return xyz, {t: (np.array(b), np.array(c)) for t, (b, c) in els.items()}


def slice_x(xyz, els, x0, ywin, zwin):
    """The polygons (in y and z) where the plane x = x0 cuts each element near the window, and their bodies."""
    polys, bodies = [], []
    for t, (body, conn) in els.items():
        if t not in EDGES:
            continue
        p = xyz[conn]
        d, y, z = p[..., 0] - x0, p[..., 1], p[..., 2]
        near = (d.min(1) < 0) & (d.max(1) > 0) & (y.max(1) > ywin[0]) & (y.min(1) < ywin[1]) & \
               (z.max(1) > zwin[0]) & (z.min(1) < zwin[1])
        for i in np.where(near)[0]:
            pts = np.array([p[i, a, 1:] + d[i, a] / (d[i, a] - d[i, b]) * (p[i, b, 1:] - p[i, a, 1:])
                            for a, b in EDGES[t] if (d[i, a] < 0) != (d[i, b] < 0)])
            if len(pts) >= 3:                    # a cut through a convex element is a convex polygon
                c = pts.mean(0)
                polys.append(pts[np.argsort(np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0]))])
                bodies.append(body[i])
    return polys, np.array(bodies)


def read_vtu(path):
    """Every array of one of ElmerSolver's VTU files (appended raw binary, 32-bit headers), by name."""
    raw = Path(path).read_bytes()
    head, _, rest = raw.partition(b'<AppendedData encoding="raw">')
    data = rest[rest.index(b'_') + 1:]
    out = {}
    for tag in re.findall(rb'<DataArray [^>]*format="appended"[^>]*/>', head):
        att = dict(re.findall(rb'(\w+)="([^"]*)"', tag))
        off, nc = int(att[b'offset']), int(att.get(b'NumberOfComponents', b'1'))
        n = int(np.frombuffer(data[off:off + 4], '<u4')[0])
        a = np.frombuffer(data[off + 4:off + 4 + n], {b'Float64': '<f8', b'Int32': '<i4'}[att[b'type']])
        out[att.get(b'Name', b'points').decode()] = a.reshape(-1, nc) if nc > 1 else a
    return out


def merged(points, values, keep):
    """The points inside `keep`, each place once (Elmer writes a node once for each body it touches), values averaged."""
    q, inv = np.unique(np.round(points[keep], 6), axis=0, return_inverse=True)
    inv = inv.ravel()
    cnt = np.bincount(inv, minlength=len(q))
    v = values[keep]
    return q, np.stack([(np.bincount(inv, v[:, k].real, len(q)) + 1j * np.bincount(inv, v[:, k].imag, len(q))) / cnt
                        for k in range(v.shape[1])], axis=1)


def collect_residuals():
    """{label: [[iteration, residual], ...]} from the logs under case/, merged into residuals.json."""
    path = HERE / 'residuals.json'
    data = json.loads(path.read_text()) if path.exists() else {}
    for level in ('0.75', '1', '1.3'):
        for f, tag in ((1e4, 'f10000'), (3.5e6, 'f3.5e06')):
            log = HERE / 'case' / f'order1_level{level}' / f'{tag}.log'
            if not log.exists():
                continue
            part = log.read_text(errors='replace').split('WhitneyAVHarmonicSolver: Solving', 1)[-1]
            rows = [[int(a), float(b)] for a, b in re.findall(r'^\s*(\d+)\s+([0-9.]+E[+-]\d+)\s*$', part, re.M)]
            if rows:
                data[f'level {level}, {f / 1e3:g} kHz' if f < 1e6 else f'level {level}, {f / 1e6:g} MHz'] = rows
    path.write_text(json.dumps(data, indent=0))
    return data


def chart_reference(out, plt):
    r1 = json.loads((HERE / 'results.json').read_text())
    r2 = json.loads((E02 / 'results.json').read_text())
    l_ref, m_ref = r1['references']['L_open_dc_h'], r2['references']['M_open_h']
    e01 = sorted((run['nodes'], solve(run, 1e4)['coils']['LOOP']['L']) for run in r1['runs'] if solve(run, 1e4))
    e02 = sorted((run['nodes'], solve(run, 1e4)['coils']['RX']['M']) for run in r2['runs'] if solve(run, 1e4))
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    fig.patch.set_facecolor(SURFACE)
    ax.axhline(0, color=INK2, lw=1.5, ls=':', label='the reference')
    n, v = zip(*e01)
    ax.plot(np.array(n) / 1e3, (np.array(v) / l_ref - 1) * 100, color=BLUE, lw=2, marker='o', ms=8,
            markeredgecolor=SURFACE, markeredgewidth=2, label="E01: L against Grover's ring formula, the ladder")
    n, v = zip(*e02)
    ax.plot(np.array(n) / 1e3, (np.array(v) / m_ref - 1) * 100, color=ORANGE, lw=2, marker='s', ms=8,
            markeredgecolor=SURFACE, markeredgewidth=2, label="E02: M against Maxwell's formula, the ladder")
    finer = []                             # the air graded 2x and 4x as finely, E01
    for name in ('results_grade.json', 'results_grade2.json'):
        p = HERE / name
        if p.exists():
            finer += [(run['nodes'], solve(run, 1e4)['coils']['LOOP']['L']) for run in json.loads(p.read_text())['runs']
                      if solve(run, 1e4)]
    if finer:
        n, v = zip(*sorted(finer))
        ax.plot(np.array(n) / 1e3, (np.array(v) / l_ref - 1) * 100, color=BLUE, lw=2, ls='--', marker='D', ms=8,
                markeredgecolor=SURFACE, markeredgewidth=2,
                label='E01: L, the air graded ' + ('2x and 4x' if len(finer) > 1 else 'twice') + ' as finely')
    for path, coil, ref, color, marker, label in (
            (E02 / 'results_grade.json', ('RX', 'M'), m_ref, ORANGE, 'D', 'E02: M, the air graded twice as finely'),
            (HERE / 'results_domain120.json', ('LOOP', 'L'), l_ref, BLUE, '^', 'E01: L, the air domain twice as big')):
        if path.exists():
            for run in json.loads(path.read_text())['runs']:
                s = solve(run, 1e4)
                if s:
                    ax.plot(run['nodes'] / 1e3, (s['coils'][coil[0]][coil[1]] / ref - 1) * 100, lw=0, color=color,
                            marker=marker, ms=9, markeredgecolor=SURFACE, markeredgewidth=2, label=label)
                    label = None
    style(ax, 'mesh nodes (thousands)', 'difference from the reference (%)')
    lo = min(-4.5, ax.get_ylim()[0])
    ax.set_ylim(lo, 0.8)
    ax.set_title('Elmer against the closed forms at 10 kHz, as the mesh is refined', color=INK, fontsize=10.5,
                 loc='left')
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=2)
    fig.tight_layout()
    save(fig, out / 'elmerresults_1_against_reference.webp')
    plt.close(fig)


def chart_residual(out, plt, data):
    styles = {'level 0.75, 10 kHz': (BLUE, '-'), 'level 1, 10 kHz': (ORANGE, '-'), 'level 1.3, 10 kHz': (AQUA, '-'),
              'level 1, 3.5 MHz': (INK2, '--')}
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    fig.patch.set_facecolor(SURFACE)
    for label, (color, ls) in styles.items():
        if label in data:
            it, res = zip(*data[label])
            ax.semilogy(it, res, color=color, lw=2, ls=ls, label=label)
    ax.axhline(1e-7, color=INK2, lw=1, ls=':')
    ax.text(3000, 1.15e-7, 'tolerance 1e-7', color=INK2, fontsize=8, ha='right', va='bottom')
    style(ax, 'iteration', 'relative residual')
    ax.set_title('E01: the linear solve stalls at 10 kHz and converges at 3.5 MHz', color=INK, fontsize=10.5,
                 loc='left')
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc='upper right')
    fig.tight_layout()
    (out / 'E01_circular_loop').mkdir(parents=True, exist_ok=True)
    save(fig, out / 'E01_circular_loop' / 'elmerresults_2_residual.webp')
    plt.close(fig)


def chart_air_mesh(out, plt):
    """The mesh round the trace, cut through the loop's axis, with the examples' air grading and twice as fine."""
    from matplotlib.collections import PolyCollection
    cases = []
    for folder, results, name in ((HERE / 'case', HERE / 'results.json', "the examples' grading"),
                                  (HERE / 'case_grade', HERE / 'results_grade.json', 'twice as fine')):
        mesh = folder / 'order1_level0.75' / 'mesh_files'
        if not (mesh.exists() and results.exists()):
            return
        r = json.loads(results.read_text())
        run = next(run for run in r['runs'] if run['level'] == 0.75)
        err = (solve(run, 1e4)['coils']['LOOP']['L'] / r['references']['L_open_dc_h'] - 1) * 100
        g = r['settings']['mesh']
        cases.append((mesh, f"{name}: grade {g['grade']:g}, tet_grade {g['tet_grade']:g}\n"
                            f"{run['nodes']:,} nodes, L {-err:.{1 if err < -2 else 2}f} % low"))
    cy = r['settings']['centre'][1] + r['settings']['radius_mm']     # where the trace crosses x = centre
    yw, zw = (cy - 2, cy + 2), (-2, 2)
    fig, axs = plt.subplots(1, 2, figsize=(7.6, 4.6), sharey=True, layout='constrained')
    fig.patch.set_facecolor(SURFACE)
    for ax, (mesh, title) in zip(axs, cases):
        xyz, els = read_elmer_mesh(mesh)
        polys, bodies = slice_x(xyz, els, r['settings']['centre'][0] + 1e-4, (yw[0] - 1, yw[1] + 1), (-3, 3))
        face = np.where(bodies == 3, ORANGE, np.where(bodies == 2, '#cfeee2', SURFACE))   # copper, mask, air
        ax.add_collection(PolyCollection(polys, facecolors=face, edgecolors=INK2, linewidths=0.35))
        ax.set_xlim(*yw)
        ax.set_ylim(*zw)
        ax.set_aspect('equal')
        style(ax, 'y (mm)', 'z (mm)' if ax is axs[0] else '')
        ax.grid(False)
        ax.set_title(title, color=INK, fontsize=9.5, loc='left')
    fig.suptitle("E01's mesh at level 0.75 round the trace (orange), cut through the loop's axis",
                 color=INK, fontsize=10.5, x=0.01, ha='left')
    (out / 'E01_circular_loop').mkdir(parents=True, exist_ok=True)
    save(fig, out / 'E01_circular_loop' / 'elmeraccuracy_1_air_mesh.webp')
    plt.close(fig)


def chart_fields(out, plt):
    """|B| in the plane through the loop's axis at 3.5 MHz, and |J| across the trace at 10 kHz and 3.5 MHz."""
    from matplotlib.colors import LogNorm
    from scipy.interpolate import LinearNDInterpolator, griddata
    folder = HERE / 'case_fields' / 'order1_level0.75'
    vtu = {f: folder / f'res_{f}' / f'{f}_t0001.vtu' for f in ('f10000', 'f3.5e06')}
    if not all(p.exists() for p in vtu.values()):
        return
    st = json.loads((HERE / 'results_fields.json').read_text())['settings']
    cx, cy = st['centre']
    r, w = st['radius_mm'], st['width_mm']
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.6, 3.9), width_ratios=[1.9, 1], layout='constrained')
    fig.patch.set_facecolor(SURFACE)

    d = read_vtu(vtu['f3.5e06'])
    pts = d['points'] * 1e3                                   # Elmer writes metres
    b = d['magnetic flux density re e'] + 1j * d['magnetic flux density im e']
    keep = (np.abs(pts[:, 0] - cx) < 6) & (np.abs(pts[:, 1] - cy) < r + 12) & (np.abs(pts[:, 2]) < 14)
    q, bq = merged(pts, b, keep)
    y, z = np.linspace(cy - r - 5, cy + r + 5, 301), np.linspace(-7, 7, 141)
    yy, zz = np.meshgrid(y, z)
    bg = LinearNDInterpolator(q, bq)(np.full(yy.size, cx), yy.ravel(), zz.ravel()).reshape(yy.shape + (3,))
    mag = np.sqrt((np.abs(bg) ** 2).sum(-1)) * 1e6
    pc = ax.pcolormesh(yy, zz, mag, norm=LogNorm(10, 1000), cmap='Blues', shading='auto', rasterized=True)
    ax.streamplot(y, z, np.nan_to_num(bg[..., 1].real), np.nan_to_num(bg[..., 2].real), color=INK2, linewidth=0.6,
                  density=1.3, arrowsize=0.6)
    ax.plot([cy - r, cy + r], [-0.0175, -0.0175], ls='none', marker='s', ms=4, color=ORANGE)
    ax.set_xlim(y[0], y[-1])
    ax.set_ylim(z[0], z[-1])
    ax.set_aspect('equal')
    style(ax, 'y (mm)', 'z (mm)')
    ax.grid(False)
    cb = fig.colorbar(pc, ax=ax, shrink=0.8, pad=0.01)
    cb.set_label('|B| (µT)', color=INK2, fontsize=9)
    cb.ax.tick_params(colors=INK2, labelsize=8)
    centre = mag[np.argmin(np.abs(z)), np.argmin(np.abs(y - cy))]
    ax.set_title(f'|B| at 3.5 MHz for 1 A, cut through the axis; {centre:.0f} µT at the centre', color=INK,
                 fontsize=9.5, loc='left')

    yc = cy + r                                               # the trace crosses x = cx here, inner edge first
    across = np.linspace(yc - w / 2 + 0.002, yc + w / 2 - 0.002, 81)
    for f, color, label in (('f10000', BLUE, '10 kHz'), ('f3.5e06', ORANGE, '3.5 MHz')):
        d = read_vtu(vtu[f])
        pts = d['points'] * 1e3
        start = np.r_[0, d['offsets'][:-1]]
        cu = np.where((d['GeometryIds'] == 3) & (d['types'] == 13))[0]          # the copper's wedges
        idx = np.unique(np.concatenate([d['connectivity'][start[i]:d['offsets'][i]] for i in cu]))
        pc_, j = pts[idx], (d['current density re e'] + 1j * d['current density im e'])[idx]
        zs = np.unique(np.round(pc_[:, 2], 6))
        mid = zs[np.argmin(np.abs(zs - zs.mean()))]
        m = (np.abs(pc_[:, 2] - mid) < 1e-6) & (np.abs(pc_[:, 0] - cx) < 1.5) & (np.abs(pc_[:, 1] - yc) < w)
        jm = np.sqrt((np.abs(j[m]) ** 2).sum(1)) / 1e6        # A/mm²
        g = griddata(pc_[m][:, :2], jm, np.c_[np.full(across.size, cx), across], method='linear')
        bx.plot(across - (yc - w / 2), g, color=color, lw=2, label=label)
    bx.axhline(1 / (w * st['copper_mm']), color=INK2, lw=1, ls=':', label='1 A spread evenly')
    style(bx, "distance from the trace's inner edge (mm)", '|J| (A/mm²)')
    bx.set_xlim(0, w)
    bx.set_ylim(0, None)
    bx.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc='upper center')
    bx.set_title('|J| across the trace, mid-copper', color=INK, fontsize=9.5, loc='left')
    (out / 'E01_circular_loop').mkdir(parents=True, exist_ok=True)
    save(fig, out / 'E01_circular_loop' / 'elmerresults_3_fields.webp')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=str(HERE / 'pictures'))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    data = collect_residuals()
    chart_reference(out, plt)
    chart_residual(out, plt, data)
    chart_air_mesh(out, plt)
    chart_fields(out, plt)


if __name__ == '__main__':
    main()
