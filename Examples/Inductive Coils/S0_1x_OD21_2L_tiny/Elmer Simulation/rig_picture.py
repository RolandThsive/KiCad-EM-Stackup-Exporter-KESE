"""How the board is set up in Elmer, as one lossless WebP drawn from the same geometry simulation.py meshes: the
stator's coils seen from above with the rotor over them, a section through the stack, and close-ups of where a
receiver and the TX are opened for their terminals.

    python rig_picture.py                 the rotor at 0 degrees and the spec's air gap
    python rig_picture.py --gap 0.5 --angle 45

Writes <board>_elmer_setup.webp beside the board's README. Nothing here is solved: it reads KESE's export in
../3D_Geometry (what simulation.py meshes) and the terminals in test_spec.json, and draws them.
This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import shapely
from shapely.geometry import LineString, Point

import simulation as sim
from make_charts import COLOURS, INK, INK2, SURFACE, tint

M, S = sim.M, sim.S
HERE = Path(__file__).resolve().parent
ROTOR = '#8a8984'


def model_layout(gap, angle):
    """The parts as simulation.py places them (insulators left out, as in the solve), sectioned in every slab."""
    se = S.kese_geometry(sim.BOARD / sim.SETTINGS['stator'], sim.GEOMETRY, log=lambda *_: None)
    re_ = S.kese_geometry(sim.BOARD / sim.SETTINGS['rotor'], sim.GEOMETRY, log=lambda *_: None)
    stator = sim.stator_parts(se)
    rot = sim.rotor_parts(re_, angle, gap)
    lay = M.Layout(stator + sim.voids(stator) + rot, M.disc(sim.AXIS, 30.0, n=64), (-5, 5))
    return lay.build(log=lambda *_: None, insulators=sim.SETTINGS['insulators'])


def body_geom(lay, body, k):
    """The geometry body `body` holds in slab k: its parts' sections less any void (air that wins over copper)."""
    g = [p.polys[k] for p in lay.parts if p.body == body and k in p.polys]
    if not g:
        return None
    v = [p.polys[k] for p in lay.parts if p.role == 'void' and k in p.polys]
    out = shapely.unary_union(g)
    return out.difference(shapely.unary_union(v)) if v else out


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


def section_rects(lay, line, bodies):
    """Where the vertical plane through `line` cuts each body: [(body, s0, s1, z0, z1)], s along the line."""
    out = []
    a = np.asarray(line.coords[0])
    for body in bodies:
        for k, (z0, z1) in enumerate(lay.slabs):
            g = body_geom(lay, body, k)
            if g is None:
                continue
            cut = line.intersection(g)
            for seg in shapely.get_parts(cut):
                if seg.geom_type != 'LineString' or seg.length < 1e-6:
                    continue
                s = sorted(float(np.linalg.norm(np.asarray(c) - a)) for c in seg.coords)
                out.append((body, s[0], s[-1], z0, z1))
    return out


COIL = {'TX': INK2, 'SIN': tint(COLOURS['SIN'], 1.0), 'COS': tint(COLOURS['COS'], 1.0)}


def kicad_axes(ax):
    """Tick labels in KiCad's coordinates: the model's y is KiCad's y with its sign turned."""
    import matplotlib.ticker
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{-v:g}'))


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=INK2, labelsize=7.5)


def top_view(ax, lay, angle, gap):
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
        labels.append((xy, f'{name} port: one via\nleft out',
                       (cx - R + 0.1, xy[1] + (4.4 if xy[1] > cy else -4.6))))
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
    ax.set_title('Seen from above', color=INK, fontsize=10, loc='left')
    from matplotlib.patches import Patch
    hs = [Patch(fc=COIL[n], label=f'{n}, F.Cu') for n in ('TX', 'SIN', 'COS')]
    hs += [Patch(fc=tint(_rgb(COIL[n]), 0.35), label=f'{n}, B.Cu') for n in ('TX', 'SIN', 'COS')]
    hs.append(Patch(fc=ROTOR, alpha=0.22, ec=INK, ls=(0, (4, 2)), label='rotor copper'))
    ax.legend(handles=hs, frameon=False, fontsize=7.5, ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.09),
              labelcolor=INK)


def _rgb(hexcol):
    return tuple(int(hexcol[i:i + 2], 16) for i in (1, 3, 5))


def stack_view(ax, lay, gap):
    """A section along KiCad's y through the axis, heights stretched so the 35 um copper shows."""
    from matplotlib.patches import Rectangle
    style(ax)
    cx, cy = sim.AXIS
    R = sim.SPEC['stator']['bore_and_outer_radius_mm'][1] + 1.0
    line = LineString([(cx, cy + R), (cx, cy - R)])       # KiCad y from -cy - R to -cy + R
    y0 = -cy - R
    for body, s0, s1, z0, z1 in section_rects(lay, line, ('TX', 'SIN', 'COS', 'ROTOR')):
        ax.add_patch(Rectangle((y0 + s0, z0), s1 - s0, z1 - z0, fc=COIL.get(body, ROTOR), ec='none', zorder=3))
    zs = sorted({z for z0, z1 in lay.slabs for z in (z0, z1)})
    st_top, st_bot = 0.0, min(zs)
    rot_face = min(z for p in lay.parts if p.body == 'ROTOR' for z in p.zrange)
    for z0, z1, text in ((st_bot, st_top, 'stator: FR-4 and mask are air to this solve'),):
        ax.axhspan(z0, z1, color=INK2, alpha=0.06, lw=0, zorder=1)
        ax.text(y0 + 0.2, (z0 + z1) / 2, text, fontsize=7.5, color=INK2, va='center')
    xd = y0 + 2 * R - 0.6
    ax.annotate('', (xd, st_top), (xd, rot_face), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
    ax.text(xd - 0.25, (st_top + rot_face) / 2, f'air gap {gap:g} mm\n(copper to copper)', ha='right',
            va='center', fontsize=7.5, color=INK)
    ax.text(y0 + 2 * R - 0.2, rot_face + 0.12, 'rotor copper, a half ring (its FR-4 above is air too)',
            fontsize=7.5, color=INK2, va='bottom', ha='right')
    ax.set_xlim(y0, y0 + 2 * R)
    ax.set_ylim(st_bot - 0.25, rot_face + 0.45)
    ax.set_xlabel(f'KiCad y (mm), along x = {cx:g} through the axis', color=INK2, fontsize=8)
    ax.set_ylabel('z (mm)', color=INK2, fontsize=8)
    box_r = sim.SETTINGS['domain_radius_mm']
    ax.set_title(f'Section through the stack, heights stretched; air all round out to {box_r:g} mm from the axis '
                 f'and {sim.SETTINGS["domain_margin_mm"]:g} mm above and below',
                 color=INK, fontsize=8.5, loc='left')


def port_view(ax, lay, name, xy, half, hole_r, title, note):
    """A true-scale section along KiCad's x through a port: the copper there, the electrodes, the sheet."""
    from matplotlib.patches import Rectangle
    style(ax)
    w = 1.3
    line = LineString([(xy[0] - w, xy[1]), (xy[0] + w, xy[1])])
    rects = section_rects(lay, line, (name,))
    for _, s0, s1, z0, z1 in rects:
        ax.add_patch(Rectangle((xy[0] - w + s0, z0), s1 - s0, z1 - z0, fc=COIL[name], ec='none', zorder=3))
    lv = sorted({z for p in lay.parts if p.body == name for z in p.levels()})
    lo, hi = lv[0], lv[-1]
    inner = [z for z in lv if lo < z < hi]
    b0, b1 = min(inner), max(inner)
    ax.add_patch(Rectangle((xy[0] - half, b0), 2 * half, b1 - b0, fc='none', ec=INK, lw=0, hatch='////',
                           alpha=0.55, zorder=2))
    hole = Point(xy).buffer(hole_r, 64)
    for z in (b0, b1):                                     # the electrodes: copper faces bordering the gap
        k = next(i for i, (z0, z1) in enumerate(lay.slabs) if (abs(z1 - z) < 1e-6 if z == b0 else abs(z0 - z) < 1e-6))
        g = body_geom(lay, name, k)
        cut = line.intersection(g.intersection(hole)) if g is not None else None
        for seg in shapely.get_parts(cut) if cut is not None else []:
            c = np.asarray(seg.coords)
            if len(c) >= 2:
                ax.plot([c[:, 0].min(), c[:, 0].max()], [z, z], color=INK, lw=3.2, solid_capstyle='butt', zorder=5)
    ax.text(xy[0] + hole_r + 0.06, b1 - 0.03, 'electrode', fontsize=7.5, color=INK, va='top')
    ax.text(xy[0] + hole_r + 0.06, b0 + 0.03, 'electrode', fontsize=7.5, color=INK, va='bottom')
    ax.text(xy[0] - half - 0.06, (b0 + b1) / 2, 'port sheet\n(hatched)', fontsize=7.5, color=INK, ha='right',
            va='center', zorder=6)
    ax.text(xy[0] - w + 0.05, lo - 0.08, note, fontsize=7.5, color=INK2, va='top')
    ax.set_xlim(xy[0] - w, xy[0] + w)
    ax.set_ylim(lo - 0.42, hi + 0.12)
    ax.set_aspect('equal')
    ax.set_xlabel(f'KiCad x (mm), along y = {-xy[1]:g}', color=INK2, fontsize=8)
    ax.set_ylabel('z (mm)', color=INK2, fontsize=8)
    ax.set_title(title, color=INK, fontsize=9, loc='left')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--gap', type=float, default=sim.SETTINGS['air_gap_mm'])
    ap.add_argument('--angle', type=float, default=0.0)
    ap.add_argument('--out', default=str(sim.BOARD / f'{sim.BOARD.name}_elmer_setup.webp'))
    a = ap.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    lay = model_layout(a.gap, a.angle)
    fig = plt.figure(figsize=(13, 6.9), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 1.25], height_ratios=[0.8, 1.0], wspace=0.14, hspace=0.42)
    top_view(fig.add_subplot(gs[:, 0]), lay, a.angle, a.gap)
    stack_view(fig.add_subplot(gs[0, 1]), lay, a.gap)
    sub = gs[1, 1].subgridspec(1, 2, wspace=0.22)
    s = sim.SETTINGS
    rx = 'SIN'
    port_view(fig.add_subplot(sub[0, 0]), lay, rx, s['rx_vias'][rx], s['rx_sheet_half_mm'], s['via_void_radius_mm'],
              f'{rx} port (COS the same): the via left out',
              f'0 A is forced through {rx}, so the voltage\nacross the sheet is its open-circuit EMF')
    port_view(fig.add_subplot(sub[0, 1]), lay, 'TX', s['tx_end'], s['sheet_half_mm'], s['tx_end_radius_mm'],
              'TX port: between its two stacked ends', '1 A is driven through the TX across\nthis gap, at '
              f'{s["freq_hz"] / 1e6:g} MHz')
    fig.suptitle(f'{sim.BOARD.name}: how the stator and rotor are set up in Elmer', x=0.06, ha='left', y=0.985,
                 color=INK, fontsize=12)
    fig.savefig(a.out, facecolor=SURFACE, bbox_inches='tight', pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    print('wrote', a.out)


if __name__ == '__main__':
    main()
