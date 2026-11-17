"""How the board is set up in PyPEEC, as one lossless WebP drawn from the same voxels simulation.py solves: the
stator's coils seen from above with the rotor over them, a section through the voxels of the stack, and close-ups,
voxel by voxel, of where a receiver and the TX are opened and of their two terminals.

    python rig_picture.py                 the rotor at 0 degrees and the spec's air gap
    python rig_picture.py --gap 0.5 --angle 45

Writes <board>_pypeec_setup.webp beside the board's README. Nothing here is solved: it reads KESE's export in
../3D_Geometry, builds the voxels and the terminals as simulation.py does (its build), and draws them.
This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import shapely
from shapely.geometry import Point

import simulation as sim
from make_charts import COLOURS, INK, INK2, SURFACE, tint

L, S, V = sim.L, sim.S, sim.V
HERE = Path(__file__).resolve().parent
ROTOR = '#8a8984'
QUIET = lambda *_: None   # noqa: E731


def exports():
    se = S.kese_geometry(sim.BOARD / sim.SETTINGS['stator'], sim.GEOMETRY, log=QUIET)
    re_ = S.kese_geometry(sim.BOARD / sim.SETTINGS['rotor'], sim.GEOMETRY, log=QUIET)
    return se, re_


def model_layout(gap, angle):
    """The parts as simulation.py places them (insulators left out, as in the solve), sectioned in every slab."""
    se, re_ = exports()
    parts = sim.stator_parts(se) + sim.rotor_parts(re_, angle, gap)
    return L.Layout(parts).build(log=QUIET, insulators=sim.SETTINGS['insulators'])


def model_case(gap, angle, d):
    """The voxels and terminals simulation.py solves with the rotor at `angle`."""
    se, re_ = exports()
    return sim.build(se, re_, angle, gap, d, log=QUIET)


def body_geom(lay, body, k):
    """The section body `body` holds in slab k."""
    g = [p.polys[k] for p in lay.parts if p.body == body and k in p.polys]
    return shapely.unary_union(g) if g else None


def slab_of(lay, body, which):
    """The slab index of a coil's top copper ('top') or bottom copper ('bottom')."""
    ks = sorted(k for p in lay.parts if p.body == body for k in p.polys)
    return ks[-1] if which == 'top' else ks[0]


def fill(ax, g, **kw):
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path as MPath
    for p in shapely.get_parts(g):
        if p.geom_type != 'Polygon' or p.is_empty:
            continue
        verts, codes = [], []
        for ring in [p.exterior, *p.interiors]:
            c = np.asarray(ring.coords)
            verts += c.tolist()
            codes += [MPath.MOVETO] + [MPath.LINETO] * (len(c) - 2) + [MPath.CLOSEPOLY]
        ax.add_patch(PathPatch(MPath(verts, codes), **kw))


COIL = {'TX': INK2, 'SIN': tint(COLOURS['SIN'], 1.0), 'COS': tint(COLOURS['COS'], 1.0)}
# what a voxel is, in the close-ups and the section: its code is its place in this list
KINDS = [('air', SURFACE), ('TX', COIL['TX']), ('SIN', COIL['SIN']), ('COS', COIL['COS']), ('ROTOR', ROTOR),
         ('terminal 1: the current goes in', '#008300'), ('terminal 2: held at 0 V', '#6250d6'),
         ('the gap that opens the coil', '#e4e3df')]
T1, T2, GAP = 5, 6, 7


def _rgb(hexcol):
    return tuple(int(hexcol[i:i + 2], 16) for i in (1, 3, 5))


def kicad_axes(ax):
    """Tick labels in KiCad's coordinates: the model's y is KiCad's y with its sign turned."""
    import matplotlib.ticker
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{-v:g}'))


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=INK2, labelsize=7.5)


def voxel_codes(case):
    """Every voxel of the grid as its code in KINDS, as an array [iz, iy, ix]."""
    g = case.grid
    a = np.zeros(g.size, np.int8)
    names = [k for k, _ in KINDS]
    for b, kv in case.vox.items():
        if b in names:
            a[V.flat(kv)] = names.index(b)
    for c in case.coils:
        a[c.t1], a[c.t2] = T1, T2
    return a.reshape(g.nz, g.ny, g.nx)


def z_edges(g):
    """The voxel layers' edges in the model's real z: halfway between the heights the layers stand for."""
    z = g.z_layer
    return np.concatenate([[z[0] - g.dz / 2], 0.5 * (z[1:] + z[:-1]), [z[-1] + g.dz / 2]])


def mesh(ax, x_edges, y_edges, codes):
    from matplotlib.colors import BoundaryNorm, ListedColormap
    cmap = ListedColormap([c for _, c in KINDS])
    norm = BoundaryNorm(np.arange(len(KINDS) + 1) - 0.5, len(KINDS))
    ax.pcolormesh(x_edges, y_edges, np.ma.masked_equal(codes, 0), cmap=cmap, norm=norm, shading='flat',
                  rasterized=True, zorder=2)                 # air left clear


def top_view(ax, lay, angle, gap, grid):
    from matplotlib.patches import Circle
    style(ax)
    for name in ('TX', 'SIN', 'COS'):
        fill(ax, body_geom(lay, name, slab_of(lay, name, 'bottom')), fc=tint(_rgb(COIL[name]), 0.35), ec='none',
             zorder=2)
    for name in ('TX', 'SIN', 'COS'):
        fill(ax, body_geom(lay, name, slab_of(lay, name, 'top')), fc=COIL[name], ec='none', zorder=3)
    kr = slab_of(lay, 'ROTOR', 'top')
    fill(ax, body_geom(lay, 'ROTOR', kr), fc=ROTOR, alpha=0.22, ec=INK, lw=0.9, ls=(0, (4, 2)), zorder=4)
    cx, cy = sim.AXIS
    rot = body_geom(lay, 'ROTOR', kr)
    rc = rot.centroid                                       # an arrow the way a positive angle turns the rotor
    r = max(math.hypot(x - cx, y - cy) for x, y in rot.exterior.coords) + 0.7 if rot.geom_type == 'Polygon' else 9.0
    a0 = math.atan2(rc.y - cy, rc.x - cx)
    a1 = a0 - math.radians(20)                              # simulation.py's KiCad sense: -angle with y up
    t = np.linspace(a0 + math.radians(20), a1, 40)
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), color=INK, lw=1.1, zorder=6)
    ax.annotate('', (cx + r * math.cos(a1), cy + r * math.sin(a1)),
                (cx + r * math.cos(t[-3]), cy + r * math.sin(t[-3])),
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.1), zorder=6)
    ax.text(cx + (r + 0.5) * math.cos(a1), cy + (r + 0.5) * math.sin(a1), '+ angle', fontsize=7.5, color=INK,
            ha='right' if math.cos(a1) < 0 else 'left', va='center', zorder=7)
    ax.text(cx, cy - (r + 1.6) if rc.y < cy else cy + r + 1.6,
            f'grey: the rotor at {angle:g}°, {gap:g} mm above, copper face down', ha='center', va='center',
            fontsize=8, color=INK, zorder=7)
    ax.plot(cx, cy, marker='+', color=INK, ms=9, mew=1.2, zorder=6)
    tx = sim.SETTINGS['tx_end']
    R = sim.SPEC['stator']['bore_and_outer_radius_mm'][1] + 1.2
    labels = [(tx, 'TX port: its two ends,\nstacked on F.Cu and B.Cu', (tx[0] - 1.6, tx[1] - 2.6))]
    for name, xy in sim.SETTINGS['rx_vias'].items():
        if sim.RX_PORT == 'cut':                            # the cut, not the via, is the port
            xy = sim.SETTINGS['rx_cuts'][name]['xy']
        text = (f'{name} port: a {sim.SETTINGS["rx_cuts"][name]["gap_mm"]:g} mm cut\nacross the top trace'
                if sim.RX_PORT == 'cut' else f'{name} port: one via\nleft out')
        labels.append((xy, text, (cx - R + 0.1, xy[1] + (4.4 if xy[1] > cy else -4.6))))
    for xy, text, at in labels:
        ax.add_patch(Circle(xy, 0.55, fc='none', ec=INK, lw=1.4, zorder=8))
        ax.annotate(text, xy, xytext=at, textcoords='data', fontsize=8, color=INK, zorder=8, va='center',
                    arrowprops=dict(arrowstyle='-', color=INK, lw=0.8, shrinkA=2, shrinkB=9),
                    bbox=dict(boxstyle='round,pad=0.25', fc=SURFACE, ec='none', alpha=0.9))
    ax.set_xlim(cx - R, cx + R)
    ax.set_ylim(cy - R, cy + R)
    ax.set_aspect('equal')
    kicad_axes(ax)
    ax.set_xlabel('KiCad x (mm)', color=INK2, fontsize=8)
    ax.set_ylabel('KiCad y (mm)', color=INK2, fontsize=8)
    ax.set_title(f'Seen from above; every part is drawn in {grid.d * 1e3:g} µm voxels\n'
                 f'(a grid of {grid.nx} x {grid.ny} x {grid.nz}, {grid.size / 1e6:.1f} million, copper or not)',
                 color=INK, fontsize=10, loc='left')
    from matplotlib.patches import Patch
    hs = [Patch(fc=COIL[n], label=f'{n}, F.Cu') for n in ('TX', 'SIN', 'COS')]
    hs += [Patch(fc=tint(_rgb(COIL[n]), 0.35), label=f'{n}, B.Cu') for n in ('TX', 'SIN', 'COS')]
    hs.append(Patch(fc=ROTOR, alpha=0.22, ec=INK, ls=(0, (4, 2)), label='rotor copper'))
    ax.legend(handles=hs, frameon=False, fontsize=7.5, ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.09),
              labelcolor=INK)


def stack_view(ax, case, codes, gap):
    """The voxels in the plane x = the axis, along KiCad's y, heights stretched so the copper's layer shows."""
    style(ax)
    g = case.grid
    cx, cy = sim.AXIS
    R = sim.SPEC['stator']['bore_and_outer_radius_mm'][1] + 1.0
    ix = int(np.clip(np.floor((cx - g.x0) / g.d), 0, g.nx - 1))
    ye = g.y0 + np.arange(g.ny + 1) * g.d                  # the model's y; KiCad's is its negative
    mesh(ax, -ye[::-1], z_edges(g), codes[:, ::-1, ix])
    y0 = -cy - R
    stator = [s for s in g.sheets if s['z1'] < 1e-6]
    st_bot, st_top = stator[0]['z0'], 0.0
    rot_face = g.sheets[-1]['z0']
    ax.axhspan(st_bot, st_top, color=INK2, alpha=0.06, lw=0, zorder=1)
    ax.text(y0 + 0.2, (st_bot + st_top) / 2, 'stator: FR-4 and mask are air to this solve,\nso they get no voxels',
            fontsize=7.5, color=INK2, va='center')
    xd = y0 + 2 * R - 0.6
    ax.annotate('', (xd, st_top), (xd, rot_face), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
    ax.text(xd - 0.25, (st_top + rot_face) / 2, f'air gap {gap:g} mm\n(copper to copper)', ha='right',
            va='center', fontsize=7.5, color=INK)
    ax.text(y0 + 2 * R - 0.2, g.sheets[-1]['z1'] + 0.08, 'rotor copper, a half ring (its FR-4 above is air too)',
            fontsize=7.5, color=INK2, va='bottom', ha='right')
    ax.set_xlim(y0, y0 + 2 * R)
    ax.set_ylim(st_bot - 0.25, rot_face + 0.45)
    ax.set_xlabel(f'KiCad y (mm), along x = {cx:g} through the axis', color=INK2, fontsize=8)
    ax.set_ylabel('z (mm), stretched', color=INK2, fontsize=8)
    ax.set_title(f'The voxels through the stack: {g.d * 1e3:g} µm across, {g.dz * 1e3:.1f} µm high, one layer through '
                 f'each copper sheet\nand a via a column of them; the air needs no voxels, so nothing bounds it',
                 color=INK, fontsize=8.5, loc='left')


def _note_cells(ax, xs, ys, sel, text, at, ha):
    """A label pointing at the middle of the cells `sel` (a mask over the drawn plane)."""
    if not sel.any():
        return
    j, i = np.nonzero(sel)
    ax.annotate(text, (xs[i].mean(), ys[j].mean()), xytext=at, textcoords='data', fontsize=7.5, color=INK, ha=ha,
                va='center', zorder=7, arrowprops=dict(arrowstyle='-', color=INK, lw=0.7, shrinkB=3))


def port_section(ax, case, codes, name, xy, region, z0, z1, title, note, w=1.3):
    """The voxels in the vertical plane along KiCad's x through a port, true to scale: the coil's copper there, its
    two terminals, and the gap between them."""
    style(ax)
    g = case.grid
    iy = int(np.clip(np.floor((xy[1] - g.y0) / g.d), 0, g.ny - 1))
    i0 = max(0, int(np.floor((xy[0] - w - g.x0) / g.d)))
    i1 = min(g.nx, int(np.ceil((xy[0] + w - g.x0) / g.d)))
    stator = [s for s in g.sheets if s['z1'] < 1e-6]
    k0, k1 = max(0, stator[0]['layers'][0] - 4), min(g.nz, stator[-1]['layers'][1] + 5)
    c = codes[k0:k1, iy, i0:i1].copy()
    xc = g.x0 + (np.arange(i0, i1) + 0.5) * g.d
    zc = g.z_layer[k0:k1]
    X, Z = np.meshgrid(xc, zc)
    yc = g.y0 + (iy + 0.5) * g.d
    gap = (c == 0) & shapely.contains_xy(region, X, np.full_like(X, yc)) & (Z > z0 - 1e-6) & (Z < z1 + 1e-6)
    c[gap] = GAP
    keep = (c == KINDS.index((name, COIL[name]))) | (c == T1) | (c == T2) | (c == GAP)
    c[~keep] = 0                                           # only this coil (another's copper may pass behind)
    mesh(ax, g.x0 + np.arange(i0, i1 + 1) * g.d, z_edges(g)[k0:k1 + 1], c)
    lo, hi = zc[0], zc[-1]
    for code, text in ((T1, 'terminal 1'), (T2, 'terminal 2')):
        sel = c == code
        if sel.any():
            zm = zc[np.nonzero(sel)[0]].mean()
            _note_cells(ax, xc, zc, sel, text, (xy[0] + 0.4, zm), 'left')
    _note_cells(ax, xc, zc, gap, 'the gap', (xy[0] - w * 0.55, (z0 + z1) / 2), 'right')
    ax.annotate(note, (0, 0), xycoords='axes fraction', xytext=(0, -36), textcoords='offset points', fontsize=7.5,
                color=INK2, va='top')
    ax.set_xlim(xy[0] - w, xy[0] + w)
    ax.set_ylim(lo - 0.12, hi + 0.12)
    ax.set_aspect('equal')
    ax.set_xlabel(f'KiCad x (mm), along y = {-yc:.3g}', color=INK2, fontsize=8)
    ax.set_ylabel('z (mm)', color=INK2, fontsize=8)
    ax.set_title(title, color=INK, fontsize=9, loc='left')


def cut_plan(ax, case, codes, name, title, note, w=0.45):
    """The top copper's voxels round a cut, seen from above and true to scale: the trace either side, the voxels
    cut out, and the two terminals on the cut's faces."""
    style(ax)
    g = case.grid
    top = next(s for s in g.sheets if abs(s['z1']) < 1e-6)
    iz = top['layers'][0]
    cx_, cy_ = sim.SETTINGS['rx_cuts'][name]['xy']
    i0, i1 = max(0, int((cx_ - w - g.x0) / g.d)), min(g.nx, int(math.ceil((cx_ + w - g.x0) / g.d)))
    j0, j1 = max(0, int((cy_ - w - g.y0) / g.d)), min(g.ny, int(math.ceil((cy_ + w - g.y0) / g.d)))
    c = codes[iz, j0:j1, i0:i1].copy()
    xc = g.x0 + (np.arange(i0, i1) + 0.5) * g.d
    yc = g.y0 + (np.arange(j0, j1) + 0.5) * g.d
    X, Y = np.meshgrid(xc, yc)
    box = sim.cut_box(name)
    gap = (c == 0) & shapely.contains_xy(box, X, Y)
    c[gap] = GAP
    keep = (c == KINDS.index((name, COIL[name]))) | (c == T1) | (c == T2) | (c == GAP)
    c[~keep] = 0
    mesh(ax, g.x0 + np.arange(i0, i1 + 1) * g.d, g.y0 + np.arange(j0, j1 + 1) * g.d, c)
    bx, by = box.exterior.xy
    ax.plot(bx, by, color=INK, lw=0.9, ls=(0, (3, 2)), zorder=4)
    for code, text, dy in ((T1, 'terminal 1', 0.3), (T2, 'terminal 2', -0.3)):
        _note_cells(ax, xc, yc, c == code, text, (cx_ + 0.12, cy_ + dy), 'left')
    ax.annotate(note, (0, 0), xycoords='axes fraction', xytext=(0, -36), textcoords='offset points', fontsize=7.5,
                color=INK2, va='top')
    ax.set_xlim(cx_ - w, cx_ + w)
    ax.set_ylim(cy_ - w, cy_ + w)
    ax.set_anchor('E')
    ax.set_aspect('equal')
    kicad_axes(ax)
    ax.set_xlabel('KiCad x (mm)', color=INK2, fontsize=8)
    ax.set_ylabel('KiCad y (mm)', color=INK2, fontsize=8)
    ax.set_title(title, color=INK, fontsize=9, loc='left')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--gap', type=float, default=sim.SETTINGS['air_gap_mm'])
    ap.add_argument('--angle', type=float, default=0.0)
    ap.add_argument('--voxel', type=float, default=sim.SETTINGS['voxel_mm'])
    ap.add_argument('--out', default=str(sim.BOARD / f'{sim.BOARD.name}_pypeec_setup.webp'))
    a = ap.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    lay = model_layout(a.gap, a.angle)
    case = model_case(a.gap, a.angle, a.voxel)
    codes = voxel_codes(case)
    g = case.grid
    fig = plt.figure(figsize=(13, 7.3), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 1.25], height_ratios=[0.8, 1.0], wspace=0.3, hspace=0.42)
    top_view(fig.add_subplot(gs[:, 0]), lay, a.angle, a.gap, g)
    stack_view(fig.add_subplot(gs[0, 1]), case, codes, a.gap)
    sub = gs[1, 1].subgridspec(1, 2, wspace=0.28)
    s = sim.SETTINGS
    stator = [x for x in g.sheets if x['z1'] < 1e-6]
    bottom, top = stator[0], stator[-1]
    rx = 'SIN'
    if sim.RX_PORT == 'cut':
        cut_plan(fig.add_subplot(sub[0, 0]), case, codes, rx, f'{rx} port (COS the same): the cut in its top trace',
                 f'0 A is forced through {rx}, so the voltage\nacross the cut is its open-circuit EMF')
    else:
        hole = Point(s['rx_vias'][rx]).buffer(s['via_void_radius_mm'], 64)
        port_section(fig.add_subplot(sub[0, 0]), case, codes, rx, s['rx_vias'][rx], hole, bottom['z1'], top['z0'],
                     f'{rx} port (COS the same): the via left out',
                     f'0 A is forced through {rx}, so the voltage\nbetween its terminals is its open-circuit EMF')
    hole = Point(s['tx_end']).buffer(s['tx_end_radius_mm'], 32)
    ax = fig.add_subplot(sub[0, 1])
    port_section(ax, case, codes, 'TX', s['tx_end'], hole, bottom['z1'], top['z0'],
                 'TX port: between its two stacked ends', '1 A is driven through the TX across\nthis gap, at '
                 f'{s["freq_hz"] / 1e6:g} MHz')
    hs = [Patch(fc=c, label=k) for k, c in KINDS[5:]]
    fig.legend(handles=hs, frameon=False, fontsize=7.5, ncol=3, loc='upper center', labelcolor=INK,
               bbox_to_anchor=(0.72, 0.045), handlelength=1.2, columnspacing=1.0)
    fig.suptitle(f'{sim.BOARD.name}: how the stator and rotor are set up in PyPEEC', x=0.06, ha='left', y=0.985,
                 color=INK, fontsize=12)
    fig.savefig(a.out, facecolor=SURFACE, bbox_inches='tight', pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    print('wrote', a.out)


if __name__ == '__main__':
    main()
