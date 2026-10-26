"""The true arcs of STEP files (kese/s7_write/step_arcs.py): a run of vertices on one circle is
written as an arc only where the arc cannot cross anything.  The arc bulges out from its vertices'
chords, up to 5 µm on a circle KiCad faceted; an edge closer to the chords than that, of the same
ring (as on PC110, where it made a dielectric invalid), of a hole or of another polygon, or another
arc bulging towards it, keeps the vertices straight; an edge that leaves the arc along its tangent
does not.  Needs shapely; with cadquery it also checks the faces and solids OpenCascade makes.
Takes a few seconds.

    python -m pytest tests/test_step_arcs.py        (or:  python tests/test_step_arcs.py)"""
import math
import sys
from pathlib import Path

import shapely
from shapely import affinity

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.s7_write.step_arcs import _fit, curve, ring_arcs  # noqa: E402
from kese.s7_write.step_curves import Circles, wire  # noqa: E402

try:
    import cadquery as cq
except ImportError:
    cq = None

ERR = 0.005                                       # mm: the chords' largest distance from the circle


def facets(c, r, a0, a1):
    """Vertices on the circle (c, r) from angle a0 to a1 (degrees), with chords ERR inside it."""
    k = math.ceil(abs(math.radians(a1 - a0)) / (2 * math.acos(1 - ERR / r)))
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / k)),
             c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / k))) for i in range(k + 1)]


def bite(gap, through):
    """A 4 x 2 mm plate with a semicircular bite (centre (2, 0), r 0.5) out of its bottom edge and
    a slot 40 µm wide pointing at the bite: the slot's end runs parallel to one chord, `gap` mm
    from it, inside the arc when gap < ERR.  through: the slot comes in from the plate's right
    edge (one ring with the bite, as on PC110), else it is a hole in the plate."""
    arc = facets((2.0, 0.0), 0.5, 180.0, 0.0)
    (x0, y0), (x1, y1) = arc[-3], arc[-2]                             # the chord from 30 to 15 degrees
    m, length = ((x0 + x1) / 2, (y0 + y1) / 2), math.hypot(x1 - x0, y1 - y0)
    u = ((m[0] - 2.0) / math.hypot(m[0] - 2.0, m[1]), m[1] / math.hypot(m[0] - 2.0, m[1]))
    t = (-u[1], u[0])
    end = [(m[0] + gap * u[0] + s * 0.02 * t[0], m[1] + gap * u[1] + s * 0.02 * t[1]) for s in (-1, 1)]
    assert length > 0.04
    if through:                                   # out to the right edge, x = 4
        far = [(4.0, p[1] + (4.0 - p[0]) / u[0] * u[1]) for p in end]
        ring = [(0, 0), *arc, (4, 0), far[0], end[0], end[1], far[1], (4, 2), (0, 2)]
        return shapely.Polygon(ring)
    far = [(p[0] + 0.3 * u[0], p[1] + 0.3 * u[1]) for p in end]
    return shapely.Polygon([(0, 0), *arc, (4, 0), (4, 2), (0, 2)], [[end[0], far[0], far[1], end[1]]])


def kept(polys):
    """For each ring of the polygons, the sweeps of the arcs written (degrees, rounded)."""
    out = []
    for rings in ring_arcs(polys, Circles([])):
        for pts, arcs in rings:
            out.append(sorted(round(abs(math.degrees(curve(pts, *arc)[3]))) for arc in arcs))
    return out


def test_an_arc_that_would_cross_its_own_ring_stays_straight():
    for through in (True, False):
        near, far = bite(ERR / 2, through), bite(4 * ERR, through)
        assert near.is_valid and far.is_valid
        assert kept([far])[0] == [180], kept([far])          # the bite is one arc of 180 degrees
        assert kept([near])[0] == [], kept([near])           # unless the slot ends inside its bulge


def notch(bend):
    """A 1 x 1 mm plate whose top is a semicircular notch as wide as the plate (centre (1, 1),
    r 0.5), as on TheMainBoard: its sides run up along the circle's tangents and the outline turns
    back down along the arc.  bend: the right side's top edge comes in from that far inside, and
    its line cuts into the circle by 25 bend² (0.0225 nm for 30 nm, 0.225 µm for 3 µm)."""
    arc = facets((1.0, 1.0), 0.5, 180.0, 360.0)[::-1]                 # (1.5, 1) down to (1, 0.5), up to (0.5, 1)
    return shapely.Polygon([(0.5, 0.0), (1.5, 0.0), (1.5 - bend, 0.9), *arc])


def test_an_outline_may_touch_an_arc_where_it_joins_it_but_not_cross_it():
    assert notch(0.0).is_valid and notch(0.003).is_valid
    assert kept([notch(0.0)]) == [[180]]                    # the sides only touch the arc at its ends
    assert kept([notch(0.00003)]) == [[180]]                # it meets the arc again 0.3 µm down, but 0.02 nm in: a touch
    assert kept([notch(0.0001)]) == [[]]                    # 0.25 nm in, which OpenCascade takes for a crossing in mm
    assert kept([notch(0.003)]) == [[]]                     # the arc would cross the bent side 30 µm down
    half = shapely.Polygon(facets((0.0, 0.0), 0.5, 0.0, 180.0))       # a half round: one edge joins the arc's ends
    assert kept([half]) == [[180]]


def test_arcs_of_two_polygons_that_would_overlap_stay_straight():
    pad = lambda c: shapely.Polygon(facets(c, 0.3, 0.0, 360.0)[:-1])
    k = math.ceil(math.pi / math.acos(1 - ERR / 0.3))                 # the pad's chords turn 360 / k degrees
    # two round pads with a chord facing the other's: with the circles 1 µm apart both are kept,
    # with the circles 1 µm into each other neither (the pads themselves are still 8 µm apart)
    for d, expect in ((0.6 + 0.001, [[360], [360]]), (0.6 - 0.001, [[], []])):
        a = affinity.rotate(pad((0.0, 0.0)), 180.0 / k, origin=(0, 0))
        b = affinity.translate(a, d)
        assert a.distance(b) > 0.008
        assert kept([a, b]) == expect, (d, kept([a, b]))
    # a pad and a block whose edge passes 2.5 µm outside one of the pad's chords
    a = pad((0.0, 0.0))
    x = 0.3 * math.cos(math.pi / k) + ERR / 2
    block = shapely.box(x, -0.02, x + 0.5, 0.02)
    assert not a.intersects(affinity.rotate(block, 180.0 / k, origin=(0, 0)))
    assert kept([a, affinity.rotate(block, 180.0 / k, origin=(0, 0))]) == [[], []]


def test_opencascade_takes_the_faces():
    if cq is None:
        return                                    # cadquery is not installed
    import numpy as np
    from OCP.BRepCheck import BRepCheck_Analyzer

    def valid(rings):
        """OpenCascade's checks on the face and on the solid made from it as step.py makes a part:
        extruded, then fused with the band above it."""
        wires = [wire(*r, 0.0, cq, np.eye(4)) for r in rings]
        face = cq.Face.makeFromWires(wires[0], wires[1:])
        solid = cq.Solid.extrudeLinear(face, cq.Vector(0, 0, 0.1))
        fused = solid.fuse(cq.Solid.makeBox(4, 2, 0.1, cq.Vector(0, 0, 0.1)), glue=True).clean()
        return BRepCheck_Analyzer(face.wrapped).IsValid() and BRepCheck_Analyzer(fused.wrapped).IsValid()

    every = lambda poly: [_fit(list(r.coords)[:-1], Circles([])) for r in (poly.exterior, *poly.interiors)]
    for through in (True, False):
        near, far = bite(ERR / 2, through), bite(4 * ERR, through)
        assert not valid(every(near))             # every arc written: the bite's crosses the slot
        assert valid(ring_arcs([near], Circles([]))[0])
        assert valid(ring_arcs([far], Circles([]))[0])
    assert not valid(every(notch(0.003)))
    assert valid(ring_arcs([notch(0.003)], Circles([]))[0])
    assert valid(ring_arcs([notch(0.0)], Circles([]))[0])
    assert valid(every(notch(0.00003)))                   # the arc kept where a side cuts 0.02 nm into its circle
    assert not valid(every(notch(0.0001)))                # and the one left straight where it cuts 0.25 nm in
    assert valid(ring_arcs([notch(0.0001)], Circles([]))[0])


if __name__ == "__main__":
    test_an_arc_that_would_cross_its_own_ring_stays_straight()
    test_an_outline_may_touch_an_arc_where_it_joins_it_but_not_cross_it()
    test_arcs_of_two_polygons_that_would_overlap_stay_straight()
    test_opencascade_takes_the_faces()
    print("ok" if cq is not None else "ok (cadquery not installed: the faces were not built)")
