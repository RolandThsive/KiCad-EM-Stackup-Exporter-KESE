"""Stage 6's boundary of a part (kese/core/boundary.py, flat_faces.py, pinches.py, vertices.py): the
vertices a part has twice are found for many parts at once, the same as part by part; the flat
faces are found again only at the heights next to a slice that changed, the same as all of them
again; faces are cut only where two slices differ, group by group, and come out as a cut of the
whole slices does (no face where the rings are the same, whatever point they start at); slices
spanned by the same regions are made once; two regions have the same vertices whatever point
their rings start at; and a part whose slices meet at T-junctions comes out with every vertex
shared (no vertex of one face or slice lies on the edge of another at its height without being
one of its vertices too) and a closed, consistently wound mesh, as does a band one grid step wide
that ends in two needle tips a hair apart (a board's gold, where faces cut on the grid left it open),
and a piece of a board's mask whose needle tips traded vertices for ever, once cut open there;
and a cut that snap rounding refuses on the grid is made with both regions put on the grid first.

    python -m pytest tests/test_boundary.py        (or:  python tests/test_boundary.py)"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
import shapely  # noqa: E402
from shapely.geometry import MultiPolygon, Point, Polygon, box  # noqa: E402

from kese.core import boundary  # noqa: E402
from kese.core import shapes2d as sh  # noqa: E402
from kese.core.boundary import boundary_of, heights_of, slices_of, wall_segments  # noqa: E402
from kese.core.boundary_mesh import mesh_of_boundary  # noqa: E402
from kese.core.flat_faces import faces_between, flat_faces  # noqa: E402
from kese.core.pinches import cut_open_at, repeated_vertices  # noqa: E402
from kese.core.vertices import grid_keys, near_edge, noded, ring_points, same_vertices  # noqa: E402
from kese.model.prisms import Prism  # noqa: E402
from parameters import P  # noqa: E402


def repeated_one_by_one(parts, check):
    """The vertices each part in `check` has twice, found part by part (how KESE 2.3 did it)."""
    out = {}
    for k in check:
        if parts[k].is_empty:
            continue
        xy, ring = shapely.get_coordinates(shapely.get_rings(shapely.get_parts(parts[k])), return_index=True)
        keep = np.r_[ring[1:] == ring[:-1], False]
        keys, xy = grid_keys(xy[keep]), xy[keep]
        _, idx, count = np.unique(keys, return_index=True, return_counts=True)
        if (count > 1).any():
            out[k] = [tuple(p) for p in xy[idx[count > 1]]]
    return out


def test_the_vertices_parts_have_twice_are_found_for_all_parts_at_once():
    shell = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 5)]
    touching_hole = Polygon(shell, [[(0, 5), (3, 6), (3, 4)]])               # a hole touching the outer ring
    two_holes = Polygon(shell, [[(0, 5), (3, 6), (3, 4)], [(5, 5), (7, 4), (7, 6)], [(5, 5), (6, 8), (4, 8)]])
    corners = MultiPolygon([box(20, 0, 22, 2), box(22, 2, 24, 4)])           # two pieces touching at a corner
    parts = [touching_hole, box(0, 0, 1, 1), corners, Polygon(), two_holes, touching_hole]
    found = repeated_vertices(parts, [0, 2, 3, 4])                          # part 5 is not asked about
    assert found == {0: [(0.0, 5.0)], 2: [(22.0, 2.0)], 4: [(0.0, 5.0), (5.0, 5.0)]}
    assert list(found) == [0, 2, 4] and found == repeated_one_by_one(parts, [0, 2, 3, 4])
    assert repeated_vertices(parts, []) == {} and repeated_vertices([Polygon()], [0]) == {}
    rng = np.random.default_rng(3)                                          # and on many random parts
    many = [shapely.make_valid(Polygon(rng.integers(0, 6, size=(7, 2)) * 0.5)) for _ in range(300)]
    many = [shapely.get_parts(g)[0] if g.geom_type == "GeometryCollection" else g for g in many]
    many = [g if g.geom_type in ("Polygon", "MultiPolygon") else Polygon() for g in many]
    check = list(range(0, 300, 2))
    assert repeated_vertices(many, check) == repeated_one_by_one(many, check)
    assert sum(map(len, repeated_one_by_one(many, check).values())) > 10   # (the test does test something)


def test_flat_faces_found_again_only_next_to_a_changed_slice_are_all_of_them_found_again():
    levels = [0.0, 1.0, 2.0, 3.0]
    slices = [box(0, 0, 4, 4), box(1, 1, 3, 3), box(0, 0, 4, 4)]
    before = flat_faces(slices, levels)
    slices[1] = box(1, 1, 3.5, 3)                                           # slice 1 changes: heights 1 and 2
    again = flat_faces(slices, levels, before, {1, 2})
    whole = flat_faces(slices, levels)
    assert [(z, up) for z, _, up in again] == [(z, up) for z, _, up in whole]
    assert all(shapely.to_wkb(a) == shapely.to_wkb(b) for (_, a, _), (_, b, _) in zip(again, whole))
    every = flat_faces(slices, levels, before, range(4))                    # every height asked: all again
    assert all(shapely.to_wkb(a) == shapely.to_wkb(b) for (_, a, _), (_, b, _) in zip(every, whole)) and len(every) == len(whole)
    stale = flat_faces(slices, levels, before, {0, 3})                      # (heights 1 and 2 kept as they were)
    assert any(shapely.to_wkb(a) != shapely.to_wkb(b) for (_, a, _), (_, b, _) in zip(stale, whole))


def via_with_pads_and_a_trace():
    """One net's copper: a bottom pad, a barrel through the board, a top pad with a trace leaving it
    and a second, square pad that the trace's end lands on: slices that meet at T-junctions."""
    drill = Point(5, 5).buffer(0.3, quad_segs=8)
    barrel = Point(5, 5).buffer(0.32, quad_segs=8).difference(drill)
    top = shapely.union_all([Point(5, 5).buffer(1.0, quad_segs=8), box(5, 4.9, 9, 5.1), box(8.5, 4.4, 9.5, 5.6)]).difference(drill)
    bottom = Point(5, 5).buffer(0.8, quad_segs=6).difference(drill)
    return [Prism("Copper_GND", "copper", bottom, -0.035, 0.0), Prism("Copper_GND", "plating", barrel, 0.0, 1.0),
            Prism("Copper_GND", "copper", top, 1.0, 1.035), Prism("Copper_GND", "copper", box(8.5, 4.4, 9.5, 5.6), 1.0, 1.07)]


def no_vertex_on_another_edge(boundary):
    """[(z, the vertex)] of every vertex at a height that lies on an edge of a face or slice there
    without being one of its vertices."""
    bad = []
    for k, z in enumerate(boundary.levels):
        regions = [s for (z0, z1, s) in boundary.slices if z in (z0, z1) and not s.is_empty]
        regions += [r for h, r, _ in boundary.flats if h == z]
        points = np.unique(np.concatenate([shapely.get_coordinates(r) for r in regions]), axis=0)
        for r in regions:
            seg = wall_segments(r)
            own = set(grid_keys(seg[:, 0]).tolist())
            near, _ = shapely.STRtree(shapely.linestrings(seg)).query(shapely.points(points), predicate="dwithin", distance=near_edge())
            for i in set(near.tolist()):
                if grid_keys(points[i:i + 1])[0] not in own:
                    bad.append((z, tuple(points[i])))
    return bad


def closed_and_wound(mesh):
    """Whether every edge of the mesh is used once each way (closed, consistently wound)."""
    f = mesh.faces
    e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    n = len(mesh.vertices)
    there, back = np.unique(e[:, 0] * n + e[:, 1], return_counts=True), e[:, 1] * n + e[:, 0]
    return bool((there[1] == 1).all() and np.isin(back, there[0]).all())


def test_a_part_meeting_at_t_junctions_shares_its_vertices_and_closes():
    b = boundary_of("Copper_GND", via_with_pads_and_a_trace())
    assert b.levels == [-0.035, 0.0, 1.0, 1.035, 1.07]
    assert no_vertex_on_another_edge(b) == []
    assert closed_and_wound(mesh_of_boundary(b))
    assert abs(b.volume() - b.volume_of_slices()) <= 1e-9 * b.volume_of_slices()


def test_a_band_ending_in_two_needle_tips_a_hair_apart_closes():
    """The gold on a slanted copper edge of a KiCad 4 board (r0891 of the corpus): its band one grid
    step wide along the wall ends in a needle, and above it the band on the face, cut short by the
    face's edge, in a needle whose tip lies 0.8 and 0.9 grid steps off the first one's edges (just
    past what counts as on an edge).  Cut on the grid, the faces between them lost the sliver between
    the two tips while both slices' walls kept their tips: four edges used once.  Cut exactly, the
    part closes and holds the volume of its slices."""
    band = shapely.from_wkt("POLYGON ((12.1925 40.556, 12.2696 40.5705, 12.2789 40.5765, 12.3364 40.6135, 12.2789 40.5764, "
                            "12.2696 40.5704, 12.193 40.556, 12.1925 40.556))")
    tip = shapely.from_wkt("POLYGON ((12.2789 40.5764, 12.2789 40.5765, 12.3305 40.6098, 12.2789 40.5764))")
    b = boundary_of("Top Finish Gold", [Prism("Top Finish Gold", "finish", band, 0.755, 0.79),
                                        Prism("Top Finish Gold", "finish", tip, 0.79, 0.795)])
    assert closed_and_wound(mesh_of_boundary(b)) and no_vertex_on_another_edge(b) == []
    assert abs(b.volume() - b.volume_of_slices()) <= 1e-9 * b.volume_of_slices()


def needle_tips_of_a_mask():
    """A 20 by 20 um piece of a board's solder mask (NE_Delta, KiCad 10) where an opening's edge runs a
    grid step or two from a pad's: the flat mask, the mask on the copper (a needle 0.2 um wide at
    most) and the wall beside it (its tip on the needle's), in grid steps from (10, 10).  The
    slices traded vertices round after round, some 400 rounds, and the part kept three T-junctions."""
    flat = [[(164, 179), (129, 198), (103, 200), (200, 200), (200, 149)],
            [(52, 190), (22, 164), (4, 129), (1, 89), (13, 52), (43, 0), (0, 0), (0, 200), (87, 200)]]
    top = [(100, 102), (200, 19), (200, 17), (183, 31), (101, 100)]
    wall = [(100, 102), (99, 102), (158, 0), (43, 0), (13, 52), (1, 89), (4, 129), (22, 164), (52, 190), (87, 200),
            (103, 200), (129, 198), (164, 179), (200, 149), (200, 19)]
    at = lambda ring: Polygon([(round(10 + x * 1e-4, 4), round(10 + y * 1e-4, 4)) for x, y in ring])
    return [Prism("Top Solder Mask", "mask", MultiPolygon([at(r) for r in flat]), 0.755, 0.765),
            Prism("Top Solder Mask", "mask_over_copper", at(top), 0.79, 0.8),
            Prism("Top Solder Mask", "mask", at(wall), 0.755, 0.8)]


def test_slices_whose_needle_tips_trade_vertices_for_ever_are_cut_open_there_and_close():
    prisms, notes = needle_tips_of_a_mask(), []
    b = boundary_of("Top Solder Mask", prisms, notes.append)
    rounds = P.Geometry.VERTEX_SHARING_ROUNDS
    assert len(notes) == 1 and notes[0].startswith(f"slices still sharing new vertices after {rounds} rounds: cut open at")
    assert closed_and_wound(mesh_of_boundary(b)) and no_vertex_on_another_edge(b) == []
    whole = sum((p.z1 - p.z0) * p.region.area for p in prisms)
    assert abs(b.volume() - b.volume_of_slices()) <= 1e-9 * whole and 0.99 * whole < b.volume() < whole
    boundary.cut_open_at = lambda slices, pts, n: (set(), 0.0)                       # never cut open
    try:
        notes = []
        b = boundary_of("Top Solder Mask", prisms, notes.append)
    finally:
        boundary.cut_open_at = cut_open_at
    assert notes[-1] == f"faces and walls still changing after {rounds} rounds"
    assert no_vertex_on_another_edge(b) != []


def test_a_cut_snap_rounding_refuses_is_made_with_both_regions_on_the_grid():
    """A face of the visual skin of the same board (r0891 of the corpus) less the slice above it,
    joined in floating point: a sliver hole of the slice, thinner than a grid step, ends on the face's
    corner, and GEOS refuses the cut on the grid ("Ring edge missing"), the regions made valid or not;
    the run stopped there.  With both put on the grid first, the cut comes out on the grid, valid,
    and within a grid step of the cut in floating point."""
    face = shapely.from_wkt("POLYGON ((12.6735 26.6841, 12.6735 26.6842, 12.6771 26.6985, 12.6811 26.7097, 12.6837 26.7091, "
                            "12.6714 26.6485, 12.6689 26.649, 12.6695 26.66, 12.6717 26.6754, 12.6718 26.6758, "
                            "12.6723 26.6794, 12.6735 26.6841))")
    above = Polygon([(12.676618497109827, 26.6738), (12.671471428571428, 26.6738), (12.67165, 26.67505),
                     (12.671396640537514, 26.6738), (12.663400000000001, 26.6738), (12.663400000000001, 26.693800000000003),
                     (12.67545039193729, 26.693800000000003), (12.673523559457298, 26.68429358339982),
                     (12.675916783216783, 26.693800000000003), (12.680664739884394, 26.693800000000003)],
                    [[(12.6735, 26.6841), (12.6735, 26.684177348066303), (12.671993670886065, 26.676745569620206)]])
    cut = sh.diff(face, above)
    assert cut.is_valid and sh.on_grid(shapely.get_parts(cut)).all()
    exact = shapely.difference(face, above)
    assert shapely.symmetric_difference(cut, exact).area <= sh.grid() * exact.length


def vertex_set(g):
    return set(map(tuple, np.round(ring_points(g) / sh.grid()).astype(np.int64).tolist()))


def test_faces_are_cut_only_where_the_slices_differ_and_come_out_as_a_whole_cut_does():
    holes = [Point(x, y).buffer(0.3, quad_segs=8) for x in range(1, 10, 2) for y in range(1, 10, 2)]
    walls = [h.buffer(0.05, quad_segs=8).difference(h) for h in holes]               # a hole finish: one ring per hole
    same = noded(sh.as_region(walls))                                                 # slices are noded
    turned = sh.as_region([Polygon(np.roll(np.asarray(w.exterior.coords)[:-1], 7, axis=0)[::-1],
                                   [np.asarray(w.interiors[0].coords)[::-1]]) for w in shapely.get_parts(same)])  # other start, other way round
    assert faces_between(same, turned) == (sh.EMPTY, sh.EMPTY)                        # the same rings: no face at all
    caps = noded(sh.as_region([h.buffer(0.2, quad_segs=8).difference(h) for h in holes[:7]]))   # caps on seven of the holes
    up, down = faces_between(caps, same)
    whole_up, whole_down = sh.exact_diff(caps, same), sh.exact_diff(same, caps)
    for got, want in ((up, whole_up), (down, whole_down)):
        assert got.is_valid and abs(got.area - want.area) < 1e-12 and vertex_set(got) == vertex_set(want)
    assert len(shapely.get_parts(down)) == len(shapely.get_parts(whole_down)) == len(walls) - 7   # (the capped walls face nothing)
    alone = box(50, 50, 51, 51)                                                       # nothing above it: a face as it is
    up, down = faces_between(sh.as_region([alone, *shapely.get_parts(caps)]), same)
    assert same_vertices(alone, noded(alone))                                         # (it is noded)
    assert any(p.equals_exact(alone, 0) for p in shapely.get_parts(up))
    assert faces_between(sh.EMPTY, same) == (sh.EMPTY, same) and faces_between(same, sh.EMPTY) == (same, sh.EMPTY)


def test_slices_spanned_by_the_same_regions_are_made_once():
    ring = Point(0, 0).buffer(1.0, quad_segs=8).difference(Point(0, 0).buffer(0.9, quad_segs=8))
    copy = shapely.from_wkb(shapely.to_wkb(ring))                                    # the same shape, another object
    prisms = [Prism("Hole Finish Gold", "finish", ring, 0.0, 1.0), Prism("Hole Finish Gold", "finish", copy, 1.0, 2.0),
              Prism("Hole Finish Gold", "finish", box(-2, -2, 2, 2).difference(Point(0, 0).buffer(0.9)), 2.0, 2.1)]
    slices = slices_of(prisms, heights_of(prisms))
    assert slices[0] is slices[1] and slices[2] is not slices[0]
    assert shapely.to_wkb(slices[0]) == shapely.to_wkb(noded(ring))


def test_two_regions_have_the_same_vertices_whatever_point_their_rings_start_at():
    a = Polygon([(0, 0), (4, 0), (4, 3), (0, 3)], [[(1, 1), (2, 1), (2, 2)]])
    b = Polygon([(4, 3), (0, 3), (0, 0), (4, 0)], [[(2, 2), (1, 1), (2, 1)]])
    assert same_vertices(a, b) and same_vertices(sh.EMPTY, sh.EMPTY)
    assert not same_vertices(a, Polygon([(0, 0), (4, 0), (4, 3.0001), (0, 3)], [[(1, 1), (2, 1), (2, 2)]]))
    assert not same_vertices(a, box(0, 0, 4, 3)) and not same_vertices(a, sh.EMPTY)

if __name__ == "__main__":
    test_the_vertices_parts_have_twice_are_found_for_all_parts_at_once()
    test_flat_faces_found_again_only_next_to_a_changed_slice_are_all_of_them_found_again()
    test_a_part_meeting_at_t_junctions_shares_its_vertices_and_closes()
    test_a_band_ending_in_two_needle_tips_a_hair_apart_closes()
    test_slices_whose_needle_tips_trade_vertices_for_ever_are_cut_open_there_and_close()
    test_a_cut_snap_rounding_refuses_is_made_with_both_regions_on_the_grid()
    test_faces_are_cut_only_where_the_slices_differ_and_come_out_as_a_whole_cut_does()
    test_slices_spanned_by_the_same_regions_are_made_once()
    test_two_regions_have_the_same_vertices_whatever_point_their_rings_start_at()
    print("ok")
