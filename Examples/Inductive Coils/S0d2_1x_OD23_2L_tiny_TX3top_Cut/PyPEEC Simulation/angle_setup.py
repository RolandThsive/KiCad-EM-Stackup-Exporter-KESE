"""The rotor over the stator at every angle of the sweep, seen from above, as lossless WebP pictures in
RotorStator_AngleSetup/ beside this file: one picture per angle, so that each angle in the results can be matched
to where the rotor's copper sat over the coils.

    python angle_setup.py                 every angle in test_spec.json's sweep
    python angle_setup.py --angles 0 45   only these

Drawn from the same geometry simulation.py draws its voxels from (rig_picture.model_layout: KESE's export in
../3D_Geometry, the rotor turned copper side down without mirroring and turned about the axis in KiCad's sense), so
a picture shows where the copper sat when PyPEEC solved that angle. Nothing here is solved.
This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
from matplotlib.patches import Circle, Patch

import rig_picture as rig
import simulation as sim
from make_charts import INK, INK2, SURFACE, tint

HERE = Path(__file__).resolve().parent
OUT = HERE / 'RotorStator_AngleSetup'
ROTOR_FILL, ROTOR_EDGE = '#8a8984', '#3d3c39'


def rotor_bearing(lay):
    """The direction (radians, model frame, y up) from the axis to the rotor copper's centroid, and its reach."""
    g = rig.body_geom(lay, 'ROTOR', rig.slab_of(lay, 'ROTOR', 'top'))
    cx, cy = sim.AXIS
    c = g.centroid
    reach = max(math.hypot(x - cx, y - cy) for p in getattr(g, 'geoms', [g]) for x, y in p.exterior.coords)
    return math.atan2(c.y - cy, c.x - cx), reach, g


def picture(angle, a_zero, gap, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    lay = rig.model_layout(gap, angle)
    bearing, reach, rot = rotor_bearing(lay)
    cx, cy = sim.AXIS
    bore, outer = sim.SPEC['stator']['bore_and_outer_radius_mm']
    R = outer + 2.3
    fig, ax = plt.subplots(figsize=(6.4, 7.0), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    rig.style(ax)
    ax.set_xticks([])
    ax.set_yticks([])
    for name in ('TX', 'SIN', 'COS'):                     # B.Cu lighter under F.Cu, as the coils lie
        rig.fill(ax, rig.body_geom(lay, name, rig.slab_of(lay, name, 'bottom')),
                 fc=tint(rig._rgb(rig.COIL[name]), 0.4), ec='none', zorder=2)
    for name in ('TX', 'SIN', 'COS'):
        rig.fill(ax, rig.body_geom(lay, name, rig.slab_of(lay, name, 'top')), fc=rig.COIL[name], ec='none', zorder=3)
    for r in (bore, outer):                               # the stator board's edges
        ax.add_patch(Circle((cx, cy), r, fc='none', ec=INK, lw=1.3, zorder=1))
    rig.fill(ax, rot, fc=ROTOR_FILL, alpha=0.38, ec='none', zorder=4)
    rig.fill(ax, rot, fc='none', ec=ROTOR_EDGE, lw=1.0, zorder=5)
    # the turn from 0 degrees, read on the bore as on a dial: a dotted ray where the rotor's middle sits at 0, a
    # solid one where it sits now, an arrow between them the way the rotor turned, and the angle in the middle
    r_ray = reach + 0.45                                  # just past the rotor copper, short of the ports
    for b, ls, lw in ((a_zero, (0, (1, 2)), 1.0), (bearing, '-', 1.4)):
        ax.plot([cx + bore * math.cos(b), cx + r_ray * math.cos(b)],
                [cy + bore * math.sin(b), cy + r_ray * math.sin(b)], color=INK, ls=ls, lw=lw, zorder=6)
    turn = -math.radians(angle)                           # simulation.py's KiCad sense: a positive angle is -angle, y up
    ra = 0.72 * bore
    if angle % 360:
        t = np.linspace(a_zero, a_zero + turn, 120)
        ax.plot(cx + ra * np.cos(t), cy + ra * np.sin(t), color=INK, lw=1.1, zorder=6)
        ax.annotate('', (cx + ra * math.cos(t[-1]), cy + ra * math.sin(t[-1])),
                    (cx + ra * math.cos(t[-6]), cy + ra * math.sin(t[-6])),
                    arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.1, mutation_scale=9), zorder=6)
    ax.text(cx, cy, f'{angle:g}°', fontsize=10, color=INK, ha='center', va='center', zorder=8, fontweight='bold')
    ax.text(cx + (r_ray + 0.55) * math.cos(a_zero), cy + (r_ray + 0.55) * math.sin(a_zero), '0°', fontsize=8.5,
            color=INK2, ha='center', va='center', zorder=8)
    # the three ports, ringed, named outside the board so that no rotor position covers a name
    ports = [('TX', sim.SETTINGS['tx_end'])] + list(sim.SETTINGS['rx_vias'].items())
    if sim.RX_PORT == 'cut':                              # SIN and COS are opened by a cut in a top trace instead
        ports = ports[:1] + [(n, c['xy']) for n, c in sim.SETTINGS['rx_cuts'].items()]
    for name, xy in ports:
        ax.add_patch(Circle(xy, 0.5, fc='none', ec=INK, lw=1.1, zorder=8))
        d = math.atan2(xy[1] - cy, xy[0] - cx)
        rt = outer + 1.25
        at = (cx + rt * math.cos(d), cy + rt * math.sin(d))
        ax.annotate(f'{name} port' + ('\n(cut)' if name != 'TX' and sim.RX_PORT == 'cut' else ''), xy, xytext=at, textcoords='data', fontsize=7.5, color=INK, zorder=8,
                    ha='center', va='center', arrowprops=dict(arrowstyle='-', color=INK, lw=0.7, shrinkA=1,
                                                              shrinkB=7))
    ax.set_xlim(cx - R, cx + R)
    ax.set_ylim(cy - R, cy + R)
    ax.set_aspect('equal')
    ax.set_title(f'Rotor at {angle:g}°', color=INK, fontsize=13, loc='left', pad=22)
    ax.text(0, 1.012, f'{sim.BOARD.name}, seen from above as PyPEEC solves it: the rotor copper face down '
            'over the stator, the same at every air gap', transform=ax.transAxes, fontsize=7.5, color=INK2, va='bottom')
    hs = [Patch(fc=rig.COIL[n], label=f'{n}, F.Cu') for n in ('TX', 'SIN', 'COS')]
    hs += [Patch(fc=tint(rig._rgb(rig.COIL[n]), 0.4), label=f'{n}, B.Cu') for n in ('TX', 'SIN', 'COS')]
    hs.append(Patch(fc=ROTOR_FILL, alpha=0.38, ec=ROTOR_EDGE, label='rotor copper'))
    ax.legend(handles=hs, frameon=False, fontsize=7.5, ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.01),
              labelcolor=INK, handlelength=1.4, columnspacing=1.2)
    fig.savefig(path, facecolor=SURFACE, bbox_inches='tight', pad_inches=0.15,
                pil_kwargs={'lossless': True, 'method': 6})
    plt.close(fig)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--angles', type=float, nargs='*', default=sim.SETTINGS['angles_deg'])
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    gap = sim.SETTINGS['air_gap_mm']                      # seen from above, the gap changes nothing
    a_zero = rotor_bearing(rig.model_layout(gap, 0.0))[0]
    for angle in a.angles:
        print('wrote', picture(angle, a_zero, gap, OUT / f'rotor_{angle:03.0f}deg.webp'))


if __name__ == '__main__':
    main()
