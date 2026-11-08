"""The pairs of shapes within a distance of each other (kese/core/graph.py, pairs_within), which
shapes2d.meeting and the copper's hairline gaps group by: the very pairs an STRtree's dwithin query of
the shapes against themselves finds, with a zone fill of many points among small pads, pieces exactly
the distance apart and pieces a hair further; no shape is left prepared, and a shape prepared before
stays prepared.  And an index built before threads share it (shared_tree) finds what an STRtree
finds, from eight threads at once.

    python -m pytest tests/test_pairs.py     (or:  python tests/test_pairs.py)"""
import numpy as np
import shapely
from shapely.geometry import Point, box

from helpers import run_tests, settings
from kese.core import shapes2d as sh
from kese.core.graph import pairs_within, shared_tree
from kese.core.parallel import in_parallel


def by_query(parts, d):
    i, j = shapely.STRtree(parts).query(parts, predicate="dwithin", distance=d)
    return {(min(a, b), max(a, b)) for a, b in zip(i.tolist(), j.tolist()) if a != b}


def shapes():
    g = sh.grid()
    rng = np.random.default_rng(7)
    fill = Point(10, 10).buffer(9, quad_segs=400).difference(Point(10, 10).buffer(2, quad_segs=200))   # many points
    pads = [box(x, y, x + 0.3, y + 0.2) for x, y in np.round(rng.uniform(0, 20, size=(400, 2)), 4)]
    edge = [box(30, 0, 31, 1), box(31 + g, 0, 32, 1), box(32 + g * 1.0001, 0, 33, 1),     # one step apart, a hair more
            box(40, 0, 41, 1), box(41.00005, 0.5, 42, 2)]
    return np.array([fill] + pads + edge, dtype=object)


def test_the_pairs_are_those_the_query_finds():
    parts = shapes()
    for d in (sh.grid(), 2 * sh.grid(), 0.05):
        i, j = pairs_within(parts, d)
        assert (i < j).all()
        assert set(zip(i.tolist(), j.tolist())) == by_query(parts, d)
    near = set(zip(*(x.tolist() for x in pairs_within(parts, sh.grid()))))
    n = len(parts)
    assert (n - 5, n - 4) in near and (n - 4, n - 3) not in near and (n - 2, n - 1) in near


def test_no_shape_is_left_prepared_and_one_prepared_before_stays_so():
    parts = shapes()
    shapely.prepare(parts[0])
    pairs_within(parts, sh.grid())
    assert shapely.is_prepared(parts[0]) and not shapely.is_prepared(parts[1:]).any()
    shapely.destroy_prepared(parts[0])
    pairs_within(parts, sh.grid())
    assert not shapely.is_prepared(parts).any()


def test_a_shared_tree_finds_what_an_strtree_finds_from_many_threads():
    parts = shapes()
    probes = [shapely.box(x, y, x + 1.5, y + 1.5) for x in range(0, 20, 2) for y in range(0, 20, 2)]
    want = [shapely.STRtree(parts).query(p, predicate="intersects").tolist() for p in probes]
    with settings({"Parallel.WORKERS": 8}):
        for _ in range(5):          # a fresh tree each time, queried first from the threads
            tree = shared_tree(parts)
            assert in_parallel(lambda p, tree=tree: tree.query(p, predicate="intersects").tolist(), probes) == want
    assert len(shared_tree([]).query(probes[0])) == 0


if __name__ == "__main__":
    run_tests(__file__)
