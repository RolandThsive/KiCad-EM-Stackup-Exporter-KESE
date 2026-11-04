"""Stage 6's boundary of a part (kese/core/boundary.py, pinches.py): the vertices a part has twice
are found for many parts at once, the same as part by part; the flat faces are found again only
at the heights next to a slice that changed, the same as all of them again; and a part whose
slices meet at T-junctions comes out with every vertex shared (no vertex of one face or slice lies
on the edge of another at its height without being one of its vertices too) and a closed,
consistently wound mesh.

    python -m pytest tests/test_boundary.py        (or:  python tests/test_boundary.py)"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
import shapely  # noqa: E402
from shapely.geometry import MultiPolygon, Point, Polygon, box  # noqa: E402

from kese.core.boundary import boundary_of, flat_faces, wall_segments  # noqa: E402
from kese.core.boundary_mesh import mesh_of_boundary  # noqa: E402
from kese.core.pinches import repeated_vertices  # noqa: E402
from kese.core.vertices import grid_keys, near_edge  # noqa: E402
from kese.model.prisms import Prism  # noqa: E402


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


if __name__ == "__main__":
    test_the_vertices_parts_have_twice_are_found_for_all_parts_at_once()
    test_flat_faces_found_again_only_next_to_a_changed_slice_are_all_of_them_found_again()
    test_a_part_meeting_at_t_junctions_shares_its_vertices_and_closes()
    print("ok")
