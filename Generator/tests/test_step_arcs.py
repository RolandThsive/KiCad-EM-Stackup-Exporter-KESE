"""The true arcs of STEP files (Run.STEP_EXACT_ARCS; kese/s7_write/step_arcs.py, step_curved.py): a
run of vertices on one circle is written as an arc edge, and the walls on it as a cylinder, only
where the arc cannot cross anything.  The arc bulges out from its vertices' chords, up to 5 µm on
the circles below; an edge closer to the chords than that, of the same ring, of a hole or of another
polygon, or another arc bulging towards it, keeps the vertices straight; an edge that leaves the
arc along its tangent does not.  With OCP (cadquery-ocp) every file is also read back: valid solids,
no free edge, the volume of the true shape.  Takes a few seconds.

    python -m pytest tests/test_step_arcs.py        (or:  python tests/test_step_arcs.py)"""
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
import shapely
from shapely import affinity

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from kese.core.boundary import Boundary  # noqa: E402
from kese.s7_write import step_arcs as sa  # noqa: E402
from kese.s7_write.step import write_part  # noqa: E402
from kese.s7_write.step_curved import with_arcs  # noqa: E402
from kese.s7_write.step_topology import topology_of  # noqa: E402
from kese.s7_write.step_writer import StepWriter  # noqa: E402
from parameters import P  # noqa: E402
from test_step_native import STEPControl_Reader, read_back  # noqa: E402

ERR = 0.005                                       # mm: the chords' largest distance from the circle


def facets(c, r, a0, a1):
    """Vertices on the circle (c, r) from angle a0 to a1 (degrees), with chords ERR inside it."""
    k = math.ceil(abs(math.radians(a1 - a0)) / (2 * math.acos(1 - ERR / r)))
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / k)),
             c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / k))) for i in range(k + 1)]


def snapped(geom):
    """The geometry on KESE's snapping grid, as every region stage 6 builds is."""
    return shapely.set_precision(geom, P.Geometry.SNAP_GRID_MM)


def slab(region, levels=(0.0, 0.1)):
    """A Boundary of the region between the heights (one slice per pair)."""
    region = snapped(region)
    slices = [(z0, z1, region) for z0, z1 in zip(levels[:-1], levels[1:])]
    return Boundary("part", list(levels), slices, [(levels[0], region, False), (levels[-1], region, True)])


def arcs(region, levels=(0.0, 0.1)):
    """The sweeps (degrees, rounded) of the arc edges at the lowest height, sorted; [] when none."""
    topo = with_arcs(topology_of(slab(region, levels)))
    if topo.edge_circle is None:
        return []
    out = []
    for e in np.flatnonzero(topo.edge_circle >= 0):
        a, b = topo.xyz[topo.edge_start[e]], topo.xyz[topo.edge_end[e]]
        if a[2] != levels[0]:
            continue
        c = topo.circle_xy[topo.edge_circle[e]]
        out.append(round(abs(math.degrees(sa.sweep_of(c, a[:2], b[:2], topo.edge_ccw[e])[1]))))
    return sorted(out)


def written(region, levels=(0.0, 0.1), arcs_on=True, M=None):
    """The region written as a STEP part and read back: [(valid, faces, free edges, volume)] per
    solid, and the file's size; None for the read-back without OCP."""
    saved = P.Run.STEP_EXACT_ARCS
    P.override("Run.STEP_EXACT_ARCS", arcs_on)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "part.step"
            w = StepWriter(path, "part", "mm")
            solids = write_part(w, "part", slab(region, levels), np.eye(4) if M is None else M, lambda s: None)
            w.add_part("part", (200, 120, 60), solids)
            w.close()
            return (read_back(path) if STEPControl_Reader else None), path.stat().st_size
    finally:
        P.override("Run.STEP_EXACT_ARCS", saved)


def bite(gap, through):
    """A 4 x 2 mm plate with a semicircular bite (centre (2, 0), r 0.5) out of its bottom edge and
    a slot 40 µm wide pointing at the bite: the slot's end runs parallel to one chord, `gap` mm
    from it, inside the arc when gap < ERR.  through: the slot comes in from the plate's right
    edge (one ring with the bite), else it is a hole in the plate."""
    arc = facets((2.0, 0.0), 0.5, 180.0, 0.0)
    (x0, y0), (x1, y1) = arc[-3], arc[-2]                             # the chord from 30 to 15 degrees
    m = ((x0 + x1) / 2, (y0 + y1) / 2)
    u = ((m[0] - 2.0) / math.hypot(m[0] - 2.0, m[1]), m[1] / math.hypot(m[0] - 2.0, m[1]))
    t = (-u[1], u[0])
    end = [(m[0] + gap * u[0] + s * 0.02 * t[0], m[1] + gap * u[1] + s * 0.02 * t[1]) for s in (-1, 1)]
    if through:                                   # out to the right edge, x = 4
        far = [(4.0, p[1] + (4.0 - p[0]) / u[0] * u[1]) for p in end]
        return shapely.Polygon([(0, 0), *arc, (4, 0), far[0], end[0], end[1], far[1], (4, 2), (0, 2)])
    far = [(p[0] + 0.3 * u[0], p[1] + 0.3 * u[1]) for p in end]
    return shapely.Polygon([(0, 0), *arc, (4, 0), (4, 2), (0, 2)], [[end[0], far[0], far[1], end[1]]])


def notch(bend):
    """A 1 x 1 mm plate whose top is a semicircular notch as wide as the plate (centre (1, 1),
    r 0.5): its sides run up along the circle's tangents and the outline turns back down along the
    arc.  bend: the right side's top comes in from that far inside, its line cutting into the
    circle by about 25 bend²."""
    arc = facets((1.0, 1.0), 0.5, 180.0, 360.0)[::-1]                 # (1.5, 1) down to (1, 0.5), up to (0.5, 1)
    return shapely.Polygon([(0.5, 0.0), (1.5, 0.0), (1.5 - bend, 0.9), *arc])


def s_bend():
    """Two arcs of 60 degrees that bend opposite ways, joined by one grid step of straight line, as
    in a zone outline: an S, from (-0.87, 0.5) through (0, 0) to (0.87, -0.5)."""
    return facets((0.0, 1.0), 1.0, -150.0, -90.0) + facets((0.0001, -1.0), 1.0, 90.0, 30.0)


def pad(c, r=0.3):
    return shapely.Polygon(facets(c, r, 0.0, 360.0)[:-1])


def pad_and_block():
    """A pad (r 0.3) and a block whose edge passes ERR / 2 (2.5 µm) outside one of its chords; and
    k, the number of the pad's chords."""
    k = math.ceil(math.pi / math.acos(1 - ERR / 0.3))
    x = 0.3 * math.cos(math.pi / k) + ERR / 2
    return pad((0.0, 0.0)), affinity.rotate(shapely.box(x, -0.02, x + 0.5, 0.02), 180.0 / k, origin=(0, 0)), k


def test_circles_and_round_ends_become_arcs():
    ring = pad((0.0, 0.0), 1.0).difference(pad((0.0, 0.0), 0.4))
    assert arcs(ring) == [180, 180, 180, 180]                       # two whole circles, in halves
    track = shapely.LineString([(0, 0), (3, 0)]).buffer(0.25, 32)    # a track with round ends
    assert arcs(track) == [180, 180]
    assert arcs(shapely.box(0, 0, 2, 1)) == []                      # nothing round, nothing changes
    assert arcs(shapely.box(0, 0, 20, 20)) == []                    # a square's corners are on one circle, but it is a square
    octagon = shapely.Polygon([(math.cos(a), math.sin(a)) for a in np.radians(np.arange(8) * 45 + 22.5)])
    assert arcs(octagon) == [] and arcs(octagon.buffer(-0.1, join_style="mitre")) == []   # an octagonal pad stays one
    big = pad((0.0, 0.0), 1.0).union(shapely.box(0.0, -0.2, 3.0, 0.2))   # a round pad with a track out of it
    assert sum(arcs(big)) == 326 and max(arcs(big)) <= 181          # 326 degrees, in pieces of half a turn at most


def test_the_two_arcs_of_an_s_bend_share_only_the_vertex_between_them():
    """Each arc may take one vertex past the run that turns its way: both arcs of an S could take
    the straight step in its middle, and each removed the other's end vertex, so that the arc edges
    ran to the wrong vertices (NE_Delta's Copper_D5 came out invalid)."""
    R = P.Run
    fit = sa.Fit(R.STEP_ARC_FIT_TOLERANCE_MM, R.STEP_ARC_MIN_POINTS, math.radians(R.STEP_ARC_MIN_SWEEP_DEG),
                 math.radians(R.STEP_ARC_MAX_TURN_DEG))
    _, found, _ = sa.find_arcs(np.array(s_bend()), False, fit)
    assert len(found) == 2 and found[0][4] != found[1][4], found     # one arc each way
    assert found[0][1] <= found[1][0], found


def test_an_arc_that_would_cross_its_own_ring_stays_straight():
    for through in (True, False):
        near, far = bite(ERR / 2, through), bite(4 * ERR, through)
        assert arcs(far) == [180], arcs(far)                         # the bite is one arc of 180 degrees
        assert arcs(near) == [], arcs(near)                          # unless the slot ends inside its bulge


def test_an_outline_may_touch_an_arc_where_it_joins_it_but_not_cross_it():
    assert arcs(notch(0.0)) == [180]                                 # the sides only touch the arc at its ends
    assert arcs(notch(0.003)) == []                                  # the arc would cross the bent side
    half = shapely.Polygon(facets((0.0, 0.0), 0.5, 0.0, 180.0))       # a half round: one edge joins the arc's ends
    assert arcs(half) == [180]


def test_arcs_of_two_polygons_that_would_overlap_stay_straight():
    a, block, k = pad_and_block()                                     # the pad's chords turn 360 / k degrees
    # circles 1 µm apart, or 1 µm into each other: then only the far halves are arcs
    for d, expect in ((0.6 + 0.001, [180] * 4), (0.6 - 0.001, [180, 180])):
        turned = affinity.rotate(a, 180.0 / k, origin=(0, 0))
        b = affinity.translate(turned, d)
        assert turned.distance(b) > 0.008
        assert arcs(shapely.MultiPolygon([turned, b])) == expect, d
    assert not a.intersects(block)
    assert arcs(shapely.MultiPolygon([a, block])) == [180]          # the half away from the block


def test_an_arc_is_kept_where_the_edge_near_it_is_at_another_height():
    """A pad on the lower slice and a block on the upper one, 2.5 µm off the pad's chord: in plan
    they come closer than the bulge, but they never share a height."""
    a, block, _ = pad_and_block()
    lower, upper = snapped(a), snapped(block)
    b = Boundary("part", [0.0, 0.1, 0.2, 0.3], [(0.0, 0.1, lower), (0.2, 0.3, upper)],
                 [(0.0, lower, False), (0.1, lower, True), (0.2, upper, False), (0.3, upper, True)])
    topo = with_arcs(topology_of(b))
    assert topo.edge_circle is not None and (topo.edge_circle >= 0).sum() == 4   # two halves, top and bottom


def test_written_files_read_back_as_valid_solids():
    if STEPControl_Reader is None:
        return                                    # OCP is not installed
    cases = [pad((0.0, 0.0), 1.0).difference(pad((0.0, 0.0), 0.4)),
             shapely.LineString([(0, 0), (3, 0), (3, 2)]).buffer(0.25, 32),
             bite(ERR / 2, True), bite(4 * ERR, False), notch(0.0), notch(0.003),
             pad((0.0, 0.0), 1.0).union(shapely.box(0.0, -0.2, 3.0, 0.2))]
    for region in cases:
        for levels in ((0.0, 0.1), (0.0, 0.035, 0.1)):              # one slice, or two stacked
            (faceted, small), (curved, smaller) = written(region, levels, False), written(region, levels, True)
            assert all(v and free == 0 for v, _, free, _ in curved), curved
            assert len(curved) == len(faceted) and smaller <= small
            for (_, _, _, a), (_, _, _, b) in zip(faceted, curved):  # the true shape differs by the bulges only
                assert abs(a - b) <= 0.01 * a, (a, b)
    # in metres and turned on its side ("flat" orientation): the arcs turn with the board
    M = np.diag([0.001, 0.001, 0.001, 1.0]) @ np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], float)
    r, _ = written(cases[1], (0.0, 0.1), True, M)
    assert r == [(True, 9, 0, 0.0)]                                  # (a volume of 3e-10 rounds to 0)
    M = np.diag([1.0, -1.0, 1.0, 1.0])                               # and mirrored
    r, _ = written(cases[1], (0.0, 0.1), True, M)
    assert r == [(True, 9, 0, 0.268294)]


def test_a_failure_in_the_arcs_writes_the_part_faceted():
    import kese.s7_write.step as step

    def broken(topo):
        raise AssertionError("broken on purpose")
    saved, notes = step.with_arcs, []
    step.with_arcs = broken
    P.override("Run.STEP_EXACT_ARCS", True)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            w = StepWriter(Path(tmp) / "part.step", "part", "mm")
            assert len(write_part(w, "Copper_X", slab(pad((0.0, 0.0))), np.eye(4), notes.append)) == 1
            w.discard()
    finally:
        step.with_arcs = saved
        P.override("Run.STEP_EXACT_ARCS", False)
    assert notes == ["step: Copper_X: written without arcs (AssertionError: broken on purpose)"]


if __name__ == "__main__":
    test_circles_and_round_ends_become_arcs()
    test_an_arc_that_would_cross_its_own_ring_stays_straight()
    test_an_outline_may_touch_an_arc_where_it_joins_it_but_not_cross_it()
    test_arcs_of_two_polygons_that_would_overlap_stay_straight()
    test_an_arc_is_kept_where_the_edge_near_it_is_at_another_height()
    test_written_files_read_back_as_valid_solids()
    test_a_failure_in_the_arcs_writes_the_part_faceted()
    print("ok" if STEPControl_Reader is not None else "ok (OCP not installed: the files were not read back)")
