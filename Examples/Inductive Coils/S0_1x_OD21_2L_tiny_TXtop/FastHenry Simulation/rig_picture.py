"""How the board is set up in FastHenry, as one lossless WebP drawn from the same model simulation.py solves: the
stator's coils seen from above with the rotor's grid of bars over them, a section through the stack showing each
track's filaments, and close-ups, in three dimensions, of where a receiver and the TX are opened and of the two nodes
of each port.

    python rig_picture.py                 the rotor at 0 degrees and the spec's air gap
    python rig_picture.py --gap 0.5 --angle 45

Writes <board>_fasthenry_setup.webp beside the board's README. Nothing here is solved: it reads the board files and
KESE's export in ../3D_Geometry, builds the model as simulation.py does (its build), and draws it.
This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import shapely
from shapely.geometry import LineString, Polygon

import simulation as sim
from make_charts import COLOURS, INK, INK2, SURFACE, tint

HERE = Path(__file__).resolve().parent
ROTOR = '#8a8984'
QUIET = lambda *_: None   # noqa: E731
COIL = {'TX': INK2, 'SIN': tint(COLOURS['SIN'], 1.0), 'COS': tint(COLOURS['COS'], 1.0)}
NODE1, NODE2 = '#008300', '#6250d6'
GRIDC = '#c9c8c4'


def _rgb(hexcol):
    return tuple(int(hexcol[i:i + 2], 16) for i in (1, 3, 5))


def light(name, k=0.38):
    """A coil's colour as its bottom layer is drawn, under the top one."""
    return tint(_rgb(COIL[name]), k)


def model_of(gap, angle):
    """The model simulation.py solves with the rotor at `angle` (None: away), and what it is made of."""
    stator, rotor = sim.boards()
    model, info = sim.build(stator, rotor, angle, gap, log=QUIET)
    return model, info, rotor


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


def coil_geoms(model):
    """Each coil's copper seen from above, {(coil, 'top' or 'bottom'): shape}, from the model's segments: a track is
    its centre line widened to its width; a via is left to the vias' own marks."""
    zs = sorted({round(p0[2], 6) for b, k, p0, p1, w, h in model.geometry if k == 'track'})
    top = max(zs)
    parts = {}
    for body, kind, p0, p1, w, h in model.geometry:
        if kind != 'track':
            continue
        side = 'top' if abs(p0[2] - top) < 1e-6 else 'bottom'
        parts.setdefault((body, side), []).append(LineString([p0[:2], p1[:2]]).buffer(w / 2, quad_segs=6))
    return {k: shapely.unary_union(v) for k, v in parts.items()}


def rotor_geom(rotor, angle):
    """The rotor's copper seen from above in model coordinates, turned by angle about the axis in KiCad's sense."""
    cx, cy = sim.AXIS_KICAD
    t = math.radians(angle)
    out = []
    for _layer, _net, pts in rotor.polygons:
        p = np.asarray(pts, float) - (cx, cy)
        x = cx + p[:, 0] * math.cos(t) - p[:, 1] * math.sin(t)
        y = cy + p[:, 0] * math.sin(t) + p[:, 1] * math.cos(t)
        out.append(Polygon(np.c_[x, -y]).buffer(0))
    return shapely.unary_union(out)


def rotor_bars(model):
    """The rotor's bars as line pieces (x0, y0), (x1, y1) for a LineCollection."""
    return [(p0[:2], p1[:2]) for b, k, p0, p1, w, h in model.geometry if k == 'rotor']


def vias(model):
    return [(b, p0, p1, w) for b, k, p0, p1, w, h in model.geometry if k == 'via']


def kicad_axes(ax):
    """Tick labels in KiCad's coordinates: the model's y is KiCad's y with its sign turned."""
    import matplotlib.ticker
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{-v:g}'))


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=INK2, labelsize=7.5)


def port_points():
    """Where each port is seen from above (model coordinates), and how it is opened, for the labels."""
    s = sim.SETTINGS
    out = [('TX', s['tx_end'], 'TX port: between its two ends,\nstacked on F.Cu and B.Cu')]
    for name in ('SIN', 'COS'):
        if sim.RX_PORT == 'cut':
            c = s['rx_cuts'][name]
            out.append((name, c['xy'], f'{name} port: a {c["gap_mm"]:g} mm cut\nacross the top trace'))
        else:
            out.append((name, s['rx_vias'][name], f'{name} port: one via\nleft out'))
    return out


def top_view(ax, model, info, rotor, angle, gap):
    from matplotlib.collections import LineCollection
    from matplotlib.patches import Circle, Patch, Rectangle
    style(ax)
    geoms = coil_geoms(model)
    for name in ('TX', 'SIN', 'COS'):
        if (name, 'bottom') in geoms:
            fill(ax, geoms[(name, 'bottom')], fc=light(name, 0.35), ec='none', zorder=2)
    for name in ('TX', 'SIN', 'COS'):
        if (name, 'top') in geoms:
            fill(ax, geoms[(name, 'top')], fc=COIL[name], ec='none', zorder=3)
    for body, p0, p1, w in vias(model):
        ax.add_patch(Rectangle((p0[0] - 0.09, p0[1] - 0.09), 0.18, 0.18, fc=SURFACE, ec=COIL[body], lw=0.9,
                               zorder=4))
    rot = rotor_geom(rotor, angle)
    fill(ax, rot, fc=ROTOR, alpha=0.16, ec='none', zorder=4)
    ax.add_collection(LineCollection(rotor_bars(model), colors=ROTOR, linewidths=0.25, alpha=0.9, zorder=5))
    fill(ax, rot, fc='none', ec=INK, lw=0.9, ls=(0, (4, 2)), zorder=5)
    cx, cy = sim.AXIS
    piece = rot if rot.geom_type == 'Polygon' else min(rot.geoms, key=lambda g: g.centroid.y)
    rc = piece.centroid                                     # an arrow the way a positive angle turns the rotor
    r = max(math.hypot(x - cx, y - cy) for x, y in piece.exterior.coords) + 0.7
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
            f'grey: the rotor at {angle:g}°, {gap:g} mm above, copper face down,\nas a grid of bars finer at its edges',
            ha='center', va='center', fontsize=8, color=INK, zorder=7)
    ax.plot(cx, cy, marker='+', color=INK, ms=9, mew=1.2, zorder=6)
    R = sim.SPEC['stator']['bore_and_outer_radius_mm'][1] + 1.2
    for name, xy, text in port_points():
        at = ((xy[0] - 1.6, xy[1] - 2.6) if name == 'TX'
              else (cx - R + 0.1, xy[1] + (4.4 if xy[1] > cy else -4.6)))
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
    s = sim.SETTINGS
    ax.set_title(f"Seen from above: {info['filaments']:,} filaments in all, the stator's\n"
                 f"{info['stator_segments']:,} track segments {s['nwinc']} across each and the rotor's "
                 f"{info['rotor_bars']:,} bars", color=INK, fontsize=10, loc='left')
    hs = [Patch(fc=COIL[n], label=f'{n}, F.Cu') for n in ('TX', 'SIN', 'COS')]
    hs += [Patch(fc=light(n, 0.35), label=f'{n}, B.Cu') for n in ('TX', 'SIN', 'COS')]
    hs.append(Patch(fc=ROTOR, alpha=0.3, ec=INK, ls=(0, (4, 2)), label='rotor copper (its bars)'))
    ax.legend(handles=hs, frameon=False, fontsize=7.5, ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.09),
              labelcolor=INK)


def filament_widths(n, r):
    """FastHenry's split of a width into n filaments, each next one in r times wider, as parts of the width."""
    if n <= 1:
        return np.array([1.0])
    k = n // 2
    half = [r ** i for i in range(k)]
    w = np.array(half + ([r ** k] if n % 2 else []) + half[::-1])
    return w / w.sum()


def section_cells(model, x0):
    """The model cut by the plane x = x0 (model coordinates) along KiCad's y: each filament crossing it as a
    rectangle (KiCad y, z, width, height, colour, which), a track's filaments as FastHenry splits it, a rotor bar as
    the cell it stands for."""
    s = sim.SETTINGS
    fw = filament_widths(s['nwinc'], s['rw'])
    out = []
    for body, kind, p0, p1, w, h in model.geometry:
        if kind not in ('track', 'rotor') or (p0[0] - x0) * (p1[0] - x0) > 0 or abs(p1[0] - p0[0]) < 1e-9:
            continue
        t = (x0 - p0[0]) / (p1[0] - p0[0])
        y = -(p0[1] + t * (p1[1] - p0[1]))                    # KiCad's y where it crosses
        sin_a = abs(p1[0] - p0[0]) / math.hypot(p1[0] - p0[0], p1[1] - p0[1])   # its slant to the plane
        if sin_a < (0.5 if kind == 'rotor' else 0.2):
            continue
        cut = w / sin_a
        if kind == 'rotor':
            out.append((y - cut / 2, p0[2] - h / 2, cut, h, tint(_rgb(ROTOR), 0.7), 'rotor'))
            continue
        edges = y - cut / 2 + cut * np.concatenate([[0], np.cumsum(fw)])
        nh = s['nhinc']
        for i in range(len(fw)):
            for j in range(nh):
                out.append((edges[i], p0[2] - h / 2 + j * h / nh, edges[i + 1] - edges[i], h / nh, COIL[body], body))
    return out


def section_view(ax, model, gap, y_range):
    """The section through the axis along KiCad's y, between y_range (KiCad's y), true to scale, with one TX track
    magnified to show its filaments."""
    from matplotlib.patches import Rectangle
    style(ax)
    s = sim.SETTINGS
    x0 = sim.AXIS[0]
    cells = section_cells(model, x0)
    if not any(c[5] == 'rotor' and y_range[0] < c[0] < y_range[1] for c in cells):
        x0 += 0.3                                          # a rotor edge on the axis's line: cut just beside it
        cells = section_cells(model, x0)
    for y, z, w, h, col, _ in cells:
        ax.add_patch(Rectangle((y, z), w, h, fc=col, ec=SURFACE, lw=0.4, zorder=3))
    zst = sim.stator_layers()
    zr = sim.rotor_layers(gap)
    bot = min(a for a, _ in zst.values())
    rtop = max(b for _, b in zr.values())
    face = min(a for a, _ in zr.values())
    ax.axhspan(bot, 0, color=INK2, alpha=0.05, lw=0, zorder=1)
    ax.text(y_range[0] + 0.05, bot / 2, 'stator: FR-4 and mask are air to FastHenry,\nwhich models only the copper',
            fontsize=7.5, color=INK2, va='center')
    xd = y_range[1] - 0.12
    ax.annotate('', (xd, 0), (xd, face), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
    ax.text(xd - 0.06, 0.06 * face, f'air gap {gap:g} mm\n(copper to copper)', ha='right', va='bottom', fontsize=7.5,
            color=INK)
    ax.text(y_range[0] + 0.05, rtop + 0.04, "the rotor's bars where they cross this plane, one filament each",
            fontsize=7.5, color=INK2, va='bottom')
    ax.set_xlim(*y_range)
    ax.set_ylim(bot - 0.08, rtop + 0.22)
    ax.set_xlabel(f'KiCad y (mm), along x = {x0:g}' + (' through the axis' if x0 == sim.AXIS[0] else
                  f', {x0 - sim.AXIS[0]:g} mm beside the axis'), color=INK2, fontsize=8)
    ax.set_ylabel('z (mm)', color=INK2, fontsize=8)
    ax.set_title("A section through the stack, true to scale; the air needs no mesh, so nothing bounds it",
                 color=INK, fontsize=8.5, loc='left')
    tx = [c for c in cells if c[5] == 'TX' and c[1] + c[3] > -1e-6 and y_range[0] < c[0] < y_range[1]]
    if not tx:
        return
    tx.sort(key=lambda c: c[0])
    track = [tx[-1]]                                       # the outermost TX track: its filaments side by side
    for c in reversed(tx[:-1]):
        if track[-1][0] - (c[0] + c[2]) > 0.02:
            break
        track.append(c)
    tx = track
    yc = sum(c[0] + c[2] / 2 for c in tx) / len(tx)
    wd = max(c[0] + c[2] for c in tx) - min(c[0] for c in tx)
    ins = ax.inset_axes([0.2, 0.36, 0.36, 0.34])
    style(ins)
    for y, z, w, h, col, which in cells:
        if which == 'TX' and abs(y + w / 2 - yc) < wd:
            ins.add_patch(Rectangle((y, z), w, h, fc=col, ec=SURFACE, lw=1.2))
    ins.set_xlim(yc - 0.75 * wd, yc + 0.75 * wd)
    h = tx[0][3] * s['nhinc']
    ins.set_ylim(-h * 1.6, h * 0.6)
    ins.set_aspect('equal')
    ins.set_xticks([])
    ins.set_yticks([])
    for sp in ins.spines.values():
        sp.set_visible(True)
        sp.set_color(GRIDC)
    ins.set_title(f"a TX track magnified: {s['nwinc']} filaments across, the edge ones {s['rw']:g} times\nnarrower, "
                  f"and {s['nhinc']} through its {h * 1e3:.0f} µm of copper", fontsize=7, color=INK, loc='left')
    ax.annotate('', (yc, 0.0), (yc, 0.33), arrowprops=dict(arrowstyle='-', color=INK2, lw=0.6))


def port_close_up(ax, model, name, title, note, w=0.9, zs=4.0):
    """The coil's segments round its port in three dimensions (heights stretched zs times), the via bars, and the
    port's two nodes, between which FastHenry drives or reads it."""
    port = next(p for p in model.ports if p[0] == name)
    a, b = model.xyz(port[1]), model.xyz(port[2])
    cx_, cy_ = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    zt = max(p0[2] for _, k, p0, *_ in model.geometry if k == 'track')
    box = shapely.box(cx_ - w, cy_ - w, cx_ + w, cy_ + w)
    for body, kind, p0, p1, wd, h in model.geometry:
        if body != name or kind not in ('track', 'via'):
            continue
        seg = LineString([p0[:2], p1[:2]]) if kind == 'track' else None
        if kind == 'track':
            c = seg.intersection(box)
            if c.is_empty or c.geom_type != 'LineString':
                continue
            (x0, y0), (x1, y1) = c.coords[0], c.coords[-1]
            col = COIL[name] if abs(p0[2] - zt) < 1e-6 else light(name, 0.5)
            ax.plot([x0, x1], [y0, y1], [p0[2] * zs] * 2, color=col, lw=4.5, solid_capstyle='butt', zorder=2)
        elif box.contains(shapely.Point(p0[:2])):
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2] * zs, p1[2] * zs], color=COIL[name], lw=2.2, zorder=2)
    for xyz, col in ((a, NODE1), (b, NODE2)):
        ax.scatter([xyz[0]], [xyz[1]], [xyz[2] * zs], s=36, color=col, edgecolor=SURFACE, linewidth=0.8, zorder=5,
                   depthshade=False)
    ax.plot([a[0], b[0]], [a[1], b[1]], [a[2] * zs, b[2] * zs], color=INK, lw=1.0, ls=(0, (2, 1.5)), zorder=4)
    ax.set_xlim(cx_ - w, cx_ + w)
    ax.set_ylim(cy_ - w, cy_ + w)
    zl = sorted(z for z0z1 in sim.stator_layers().values() for z in z0z1)
    ax.set_zlim(zl[0] * zs - 0.3, 0.3)
    ax.set_box_aspect((1, 1, 0.75))
    ax.view_init(elev=24, azim=-58)
    ax.set_facecolor(SURFACE)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((0.99, 0.99, 0.985, 1.0))
        axis.line.set_color(INK2)
        axis._axinfo['grid']['color'] = (0.89, 0.89, 0.87, 1.0)
    ax.tick_params(colors=INK2, labelsize=6.5, pad=0)
    for axis, lo in ((ax.xaxis, cx_), (ax.yaxis, cy_)):
        axis.set_ticks([lo - 0.6 * w, lo, lo + 0.6 * w])
    ax.zaxis.set_ticks([zl[0] * zs, 0])
    ax.yaxis.set_major_formatter(__import__('matplotlib').ticker.FuncFormatter(lambda v, _: f'{-v:.2f}'))
    ax.xaxis.set_major_formatter(__import__('matplotlib').ticker.FuncFormatter(lambda v, _: f'{v:.2f}'))
    ax.zaxis.set_major_formatter(__import__('matplotlib').ticker.FuncFormatter(lambda v, _: f'{v / zs:.2g}'))
    ax.set_xlabel('KiCad x', color=INK2, fontsize=7, labelpad=-4)
    ax.set_ylabel('KiCad y', color=INK2, fontsize=7, labelpad=-4)
    ax.set_zlabel('z (mm)', color=INK2, fontsize=7, labelpad=-6)
    ax.set_title(title, color=INK, fontsize=9, loc='left', pad=2)
    ax.text2D(0.0, -0.08, note, transform=ax.transAxes, fontsize=7.5, color=INK2, va='top')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--gap', type=float, default=sim.SETTINGS['air_gap_mm'])
    ap.add_argument('--angle', type=float, default=0.0)
    ap.add_argument('--out', default=str(sim.BOARD / f'{sim.BOARD.name}_fasthenry_setup.webp'))
    a = ap.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    model, info, rotor = model_of(a.gap, a.angle)
    fig = plt.figure(figsize=(13, 7.3), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 1.25], height_ratios=[0.8, 1.0], wspace=0.3, hspace=0.42)
    top_view(fig.add_subplot(gs[:, 0]), model, info, rotor, a.angle, a.gap)
    r_out = sim.SPEC['stator']['bore_and_outer_radius_mm'][1]
    section_view(fig.add_subplot(gs[0, 1]), model, a.gap,
                 (sim.AXIS_KICAD[1] + r_out - 6.0, sim.AXIS_KICAD[1] + r_out - 1.6))
    sub = gs[1, 1].subgridspec(1, 2, wspace=0.12)
    rx = 'SIN'
    if sim.RX_PORT == 'cut':
        port_close_up(fig.add_subplot(sub[0, 0], projection='3d'), model, rx,
                      f'{rx} port (COS the same):\nthe cut in its top trace',
                      f'{rx} is open here, so the voltage between the\ntwo cut faces is its open-circuit EMF')
    else:
        port_close_up(fig.add_subplot(sub[0, 0], projection='3d'), model, rx,
                      f'{rx} port (COS the same):\nthe via left out',
                      f'{rx} is open here, so the voltage between where\nits tracks reach the via on the two layers '
                      'is\nits open-circuit EMF')
    port_close_up(fig.add_subplot(sub[0, 1], projection='3d'), model, 'TX', 'TX port:\nbetween its two stacked ends',
                  f'1 A is driven through the TX between\nthese two nodes, at {sim.SETTINGS["freq_hz"] / 1e6:g} MHz')
    hs = [Line2D([], [], ls='none', marker='o', ms=6, color=NODE1, label="the port's first node"),
          Line2D([], [], ls='none', marker='o', ms=6, color=NODE2, label='its second node'),
          Line2D([], [], color=INK, lw=1.0, ls=(0, (2, 1.5)), label='the port between them'),
          Line2D([], [], color=INK2, lw=4, label='the coil, F.Cu (B.Cu lighter); heights stretched 4 times')]
    fig.legend(handles=hs, frameon=False, fontsize=7.5, ncol=2, loc='upper center', labelcolor=INK,
               bbox_to_anchor=(0.72, 0.06), handlelength=1.6, columnspacing=1.2)
    fig.suptitle(f'{sim.BOARD.name}: how the stator and rotor are set up in FastHenry', x=0.06, ha='left', y=0.985,
                 color=INK, fontsize=12)
    fig.savefig(a.out, facecolor=SURFACE, bbox_inches='tight', pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    print('wrote', a.out)


if __name__ == '__main__':
    main()
