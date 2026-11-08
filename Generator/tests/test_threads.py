"""Threads (kese/core/parallel.py in_parallel) and their own copies of shapes
(kese/core/shape_copies.py): a thread's own copies are the same shapes, made only where GEOS needs
them (and on no grid where the grid is not used: a join of shared regions is the same join);
threads share one prepared copy of a slice's material and one set of joined holes, cut faces only
by the pieces of material that meet them (a face wholly against material at once, the covers test
answering as shapely.covers does), share a slow slice's probes, finish the skin's meshes the
biggest first and no more faces at once than the biggest holds, and find the solder mask's webs
group by group as the whole layer gives them; they hand back the memory they freed (unless
Parallel.GIVE_BACK_MEMORY is off).

    python -m pytest tests/test_threads.py          (or:  python tests/test_threads.py)"""
import platform
import sys
import threading
import time
from types import SimpleNamespace

import numpy as np
import shapely

from helpers import run_tests, settings
from kese.core import memory, shape_copies
from kese.core.parallel import in_parallel
from kese.core.shape_copies import _owned, own
from kese.s3_resolve.holes import made_once
from kese.s6_assemble import skin_faces
from kese.s6_assemble.assemble import finished_skin
from kese.s6_assemble.skin_faces import cut_away, lies_against_material
from kese.s6_assemble.skin_mesh import looks_at_material, probe_shares
from parameters import P


def collections_of_grids():
    """Collections on no grid of parts on one, as as_region builds them: GEOS grows each part on its own."""
    part = shapely.set_precision(shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5)), 1e-4)
    two = shapely.MultiPolygon([part, shapely.box(2, 0, 3, 1)])
    return [two, shapely.set_srid(shapely.GeometryCollection([two, part, shapely.Point(1, 2)]), 4326)]


def grids(shape):
    """The grid of a shape and, in a collection, those of its parts (at any depth)."""
    if shapely.get_type_id(shape) < 4 or shape.is_empty:
        return float(shapely.get_precision(shape))
    return float(shapely.get_precision(shape)), [grids(p) for p in shapely.get_parts(shape)]


def test_a_thread_s_own_copies_are_the_same_shapes_on_factories_of_their_own():
    square = shapely.set_precision(shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5)), 1e-4)
    shapes = [square, shapely.box(0, 0, 1, 1), shapely.set_precision(shapely.Polygon(), 1e-4),
              shapely.set_precision(shapely.LinearRing([(0, 0), (1, 0), (1, 1)]), 1e-4),
              shapely.set_srid(shapely.set_precision(shapely.Point(1, 2), 1e-4), 4326), *collections_of_grids()]
    copies = _owned({"list": shapes, "tuple": (shapes[0], "net"), "array": np.array(shapes, dtype=object), "n": 3})
    assert copies["n"] == 3 and copies["tuple"][1] == "net" and isinstance(copies["tuple"], tuple)
    for got in (copies["list"], list(copies["array"]), [copies["tuple"][0]]):
        for a, b in zip(shapes, got):
            assert a is not b and type(a) is type(b) and shapely.to_wkb(a) == shapely.to_wkb(b)
            assert grids(a) == grids(b) and shapely.get_srid(a) == shapely.get_srid(b)
            assert shapely.to_wkb(a.buffer(0.01)) == shapely.to_wkb(b.buffer(0.01))     # on the same grids


def test_copies_only_where_geos_needs_them():
    # GEOS 3.15 counts a factory's shapes atomically: there threads may share shapes, and own() is x itself
    assert shape_copies.SHARED_SAFELY == (shapely.geos_version >= (3, 15, 0))
    shapes = [shapely.set_precision(shapely.box(0, 0, 1, 1), 1e-4)]
    saved = shape_copies.SHARED_SAFELY
    try:
        shape_copies.SHARED_SAFELY = True
        assert own(shapes) is shapes
        shape_copies.SHARED_SAFELY = False
        assert own(shapes)[0] is not shapes[0]
    finally:
        shape_copies.SHARED_SAFELY = saved


def test_floating_copies_keep_the_coordinates_on_no_grid():
    # where the grid is not used: polygons through WKB alone (GEOS's default factory, shared safely),
    # anything else an own() copy, each part on its grid
    square = shapely.set_precision(shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5)), 1e-4)
    shapes = [square, shapely.MultiPolygon([square, shapely.set_precision(shapely.box(2, 0, 3, 1), 1e-4)]),
              shapely.Polygon(), *collections_of_grids()]
    saved = shape_copies.SHARED_SAFELY
    try:
        shape_copies.SHARED_SAFELY = False
        got = shape_copies.floating(shapes)
    finally:
        shape_copies.SHARED_SAFELY = saved
    for a, b in zip(shapes, got):
        assert a is not b and type(a) is type(b) and shapely.to_wkb(a) == shapely.to_wkb(b)
        if shapely.get_type_id(a) in shape_copies.POLYGONAL:
            assert not shapely.get_precision([b, *shapely.get_parts(b)]).any(), a.geom_type
        else:
            assert grids(b) == grids(a), a.geom_type


def test_a_join_of_shared_regions_is_the_same_join():
    from kese.core.boundary import joined_regions
    on_grid = [shapely.set_precision(shapely.box(*b), 1e-4) for b in ((0, 0, 1, 1), (1, 0, 2, 1), (0.5, 0.5, 1.5, 2))]
    for regions in (on_grid[:2], on_grid):              # a coverage union, and a union of overlapping ones
        for exact in (True, False):
            a, b = joined_regions(regions, exact, shared=True), joined_regions(_owned(regions), exact)
            assert shapely.to_wkb(a) == shapely.to_wkb(b) and grids(a) == grids(b), (len(regions), exact)


def make_and_drop(square, n=3000):
    """In a thread: shapes made from `square` (they share its GEOS factory) and dropped, n times."""
    for _ in range(n):
        a = square.buffer(0.01)
        shapely.get_parts(a)
        a.intersection(shapely.box(1, 1, 5, 5))
    return True


def test_threads_on_their_own_copies_of_one_shape():
    # one shape on a grid, used by every thread: each works on its own copy (with the shared shape
    # itself, GEOS 3.14 can lose its factory's count of shapes and crash)
    shared = shapely.set_precision(shapely.box(0, 0, 10, 10).difference(shapely.box(2, 2, 3, 3)), 1e-4)
    parts = shapely.MultiPolygon([shared, shapely.set_precision(shapely.box(20, 0, 30, 10), 1e-4)])
    with settings({"Parallel.WORKERS": 4}):
        assert in_parallel(lambda k: make_and_drop(own((shared, parts)[k % 2])), range(4)) == [True] * 4


def test_threads_share_one_prepared_copy_of_a_slice():
    # a prepared copy for each thread would grow with the number of threads: one per slice, in turns
    material = shapely.set_precision(shapely.box(0, 0, 10, 10).difference(shapely.box(2, 2, 3, 3)), 1e-4)
    slice_ = (None, None, None, material, {"turn": threading.Lock()})
    regions = [shapely.box(k % 9, 4, k % 9 + 1, 5) for k in range(8)] + [shapely.box(1, 1, 4, 4)]
    with settings({"Parallel.WORKERS": 8}):
        got = in_parallel(lambda r: lies_against_material(r, slice_), regions)
    assert got == [True] * 8 + [False]
    assert set(slice_[4]) == {"turn", "copy"} and shapely.is_prepared(slice_[4]["copy"])
    assert not shapely.is_prepared(material)


def test_the_covers_test_answers_as_shapely_covers_does():
    # the pattern ******FF* asked of RelateNG, and covers where GEOS has no RelateNG: the same answers
    # on regions that share edges with the material's outline and its hole, or touch it at a point
    material = shapely.box(0, 0, 10, 10).difference(shapely.box(4, 4, 6, 6))
    regions = [shapely.box(1, 1, 2, 2), shapely.box(3, 4, 4, 6), shapely.box(0, 0, 10, 4), material,
               shapely.box(3, 3, 7, 7).difference(shapely.box(4, 4, 6, 6)), shapely.box(4, 4, 6, 6),
               shapely.box(3, 3, 5, 5), shapely.box(9, 9, 11, 11), shapely.box(10, 10, 11, 11),
               shapely.MultiPolygon([shapely.box(1, 1, 2, 2), shapely.box(12, 1, 13, 2)]),
               shapely.Polygon([(4, 4), (4, 6), (3, 5)]), shapely.box(5, 5, 6, 6)]
    want = [True, True, True, True, True, False, False, False, False, False, True, False]
    assert [bool(shapely.covers(material, r)) for r in regions] == want
    for by_pattern in (True, False):
        flag, skin_faces.COVERS_BY_PATTERN = skin_faces.COVERS_BY_PATTERN, by_pattern
        try:
            slice_ = (None, None, None, material, {"turn": threading.Lock()})
            assert [lies_against_material(r, slice_) for r in regions] == want
            assert not lies_against_material(shapely.Polygon(), slice_)
        finally:
            skin_faces.COVERS_BY_PATTERN = flag


def test_threads_cut_faces_by_the_pieces_that_meet_them_alone():
    # a ring round the face meets its box but not the face, a square over its corner meets both: in
    # every thread the face loses that corner alone, and no shape is left prepared
    grid = 1e-4
    ring = shapely.set_precision(shapely.box(-5, -5, 15, 15).difference(shapely.box(-1, -1, 11, 11)), grid)
    polys = np.array([ring, shapely.set_precision(shapely.box(8, 8, 12, 12), grid)], dtype=object)
    material = (polys, np.array(["a", "b"], dtype=object), shapely.STRtree(polys), shapely.union_all(polys, grid_size=grid),
                {"turn": threading.Lock()})
    faces = [shapely.set_precision(shapely.box(0, 0, 10, 10), grid) for _ in range(16)]
    with settings({"Parallel.WORKERS": 8}):
        got = in_parallel(lambda face: cut_away(face, material), faces)
    want = shapely.box(0, 0, 10, 10).difference(shapely.box(8, 8, 10, 10))
    assert all(g.equals(want) for g in got)
    assert not shapely.is_prepared(faces).any() and not shapely.is_prepared(polys).any()
    inside = shapely.set_precision(shapely.box(9, 9, 11, 11), grid)                 # wholly against material
    assert cut_away(inside, material).is_empty and cut_away(shapely.box(20, 20, 21, 21), material).equals(shapely.box(20, 20, 21, 21))


def test_the_probe_test_lets_go_of_its_prepared_slices():
    # one triangle standing in the material: the point just in front of it is inside; then the
    # slice's prepared index is freed, not kept for as long as the slices are
    material = shapely.box(0, 0, 1, 1)
    v = np.array([[0.5, 0.2, 0.4], [0.5, 0.8, 0.4], [0.5, 0.5, 0.6]])
    pieces = [(None, None, None, material, {})]
    assert looks_at_material(v, np.array([[0, 1, 2]]), np.array([0.0, 1.0]), pieces).tolist() == [True]
    assert not shapely.is_prepared(material)


def test_a_slow_slice_s_probes_are_shared_among_the_threads():
    # a slice of many probes is shared among up to Parallel.WORKERS threads, each share of at least
    # Parallel.SKIN_PROBES_PER_SHARE, the slice itself prepared by one share alone (the others take
    # copies), the biggest shares first; a slice without material, or none, is not probed
    full, empty = (None, None, None, shapely.box(0, 0, 1, 1), {}), (None, None, None, shapely.Polygon(), {})
    at = np.array([0] * 9 + [1] * 25 + [2] * 3 + [-1, 3])
    with settings({"Parallel.WORKERS": 4, "Parallel.SKIN_PROBES_PER_SHARE": 5}):
        shares = probe_shares([full, full, empty], at, 4)
    assert [(k, len(rows), first) for k, rows, first in shares] == [
        (0, 9, True), (1, 7, True), (1, 6, False), (1, 6, False), (1, 6, False)]
    assert sorted(np.concatenate([rows for _, rows, _ in shares]).tolist()) == list(range(34))


def test_the_skin_s_meshes_are_finished_in_threads_the_biggest_first_and_no_more_at_once():
    # the meshes finished at once never hold more faces in all than the biggest one, and each raw
    # mesh is let go as soon as it is finished
    sizes = [50, 7, 30, 20, 5, 5, 5, 40, 1, 25]
    skin = {f"part {k}": SimpleNamespace(faces=range(n)) for k, n in enumerate(sizes)}
    held, most, lock = [0], [0], threading.Lock()

    def finish(mesh):
        with lock:
            held[0] += len(mesh.faces)
            most[0] = max(most[0], held[0])
        time.sleep(0.01)
        with lock:
            held[0] -= len(mesh.faces)
        return len(mesh.faces) * 10
    with settings({"Parallel.WORKERS": 4}):
        got = list(finished_skin(skin, finish))
    order = sorted(range(len(sizes)), key=lambda k: -sizes[k])
    assert got == [(f"part {k}", sizes[k] * 10) for k in order] and not skin
    assert most[0] == max(sizes)
    assert list(finished_skin({}, finish)) == []


def test_the_mask_webs_found_group_by_group_are_the_whole_layer_s():
    # openings near each other (webs between them), far apart (none between them) and one with a
    # narrow notch (a web in itself): the webs found group by group, in threads, close the same
    # region as the whole layer at once, with the same vertices, however many threads
    from collections import Counter

    from kese.core import shapes2d as sh
    from kese.s3_resolve import mask
    pads = [shapely.box(x, y, x + 0.5, y + 0.3) for x in (0, 0.6, 1.2) for y in (0, 0.4)]   # 0.1 mm apart
    far = [shapely.box(5, 5, 5.5, 5.3), shapely.box(6, 5, 6.5, 5.3)]                          # 0.5 mm apart
    notched = shapely.box(10, 0, 11, 1).difference(shapely.box(10.45, 0.2, 10.55, 1))          # a 0.1 mm notch
    openings, w = sh.union(pads + far + [notched]), 0.25
    grow = w / 2 - 1e-6
    joined = openings.buffer(grow, join_style="bevel").buffer(-grow, join_style="bevel")
    whole = [p for p in shapely.get_parts(sh.diff(joined, openings))
             if not p.buffer(-P.SolderMask.MASK_WEB_HAIRLINE_MM).is_empty]
    assert len(whole) == 2 and len(mask.web_groups(openings, w)) == 4      # one among the pads, one in the notch
    done = {}
    for workers in (1, 3):
        with settings({"Parallel.WORKERS": workers}):
            items = SimpleNamespace(mask_min_width=w, found=Counter())
            done[workers] = mask.min_width_joined(items, openings, "F")
        assert list(items.found.values()) == [len(whole)]
    assert shapely.to_wkb(done[1]) == shapely.to_wkb(done[3])
    assert shapely.symmetric_difference(done[1], sh.union([openings] + whole)).area == 0
    stray = shapely.GeometryCollection([*shapely.get_parts(openings), shapely.LineString([(20, 0), (21, 1)])])
    assert len(mask.web_groups(stray, w)) == 4                                # a stray line is no opening
    found = [p for g in mask.web_groups(openings, w) for p in mask.webs_of(g, grow)]
    assert sorted(shapely.to_wkb(shapely.normalize(np.array(found, dtype=object)))) == \
        sorted(shapely.to_wkb(shapely.normalize(np.array(whole, dtype=object))))


def test_joined_holes_are_made_once_when_threads_ask_at_once():
    made = []

    def make():
        time.sleep(0.05)                    # long enough for every thread to ask before it is made
        made.append(1)
        return shapely.box(0, 0, 1, 1)
    r = SimpleNamespace(items=SimpleNamespace(holes=[SimpleNamespace(wall=0.02)] * 3), holes_made={})
    with settings({"Parallel.WORKERS": 8}):
        got = in_parallel(lambda _: made_once(r, "drills", lambda h: True, make), range(8))
    assert len(made) == 1 and all(g is got[0] for g in got)


def test_memory_freed_by_threads_is_handed_back():
    # glibc keeps what threads free in a pool per thread: on NE_Delta a gigabyte more at 16 threads
    if sys.platform.startswith("linux") and platform.libc_ver()[0] == "glibc":
        assert memory._MALLOC_TRIM is not None
    calls, saved = [], memory._MALLOC_TRIM
    memory._MALLOC_TRIM = calls.append
    try:
        with settings({"Parallel.WORKERS": 3}):
            assert in_parallel(lambda k: k * k, range(4)) == [0, 1, 4, 9]
    finally:
        memory._MALLOC_TRIM = saved
    assert calls == [0]
    memory.give_back_memory()                           # and on this system, it runs


def test_memory_is_kept_with_give_back_memory_off():
    calls, saved = [], memory._MALLOC_TRIM
    memory._MALLOC_TRIM = calls.append
    try:
        with settings({"Parallel.WORKERS": 3, "Parallel.GIVE_BACK_MEMORY": False}):
            assert in_parallel(lambda k: k * k, range(4)) == [0, 1, 4, 9]
            memory.done_then_given_back(abs, -1)
    finally:
        memory._MALLOC_TRIM = saved
    assert calls == []


if __name__ == "__main__":
    run_tests(__file__)
