"""Walls joined across the heights only a counterbore, a countersink or a via's plug brings
(kese/core/tall_walls.py): a wall segment the same in two slices one above the other is one taller
wall, unless a face or another wall has a vertex at that height on one of its upright edges (a crack
otherwise), and such a stop spreads along the ring of walls it is on; walls of different owners do
not join.

    python -m pytest tests/test_tall_walls.py       (or:  python tests/test_tall_walls.py)"""
import sys
from pathlib import Path

import numpy as np
from shapely.geometry import box

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core.tall_walls import tall_walls  # noqa: E402

LEVELS = [0.0, 1.0, 2.0, 3.0]
SQUARE = np.array([[(0, 0), (4, 0)], [(4, 0), (4, 4)], [(4, 4), (0, 4)], [(0, 4), (0, 0)]], dtype=float)


def slices(segs=SQUARE):
    return [(LEVELS[k], LEVELS[k + 1], segs.copy()) for k in range(3)]


def spans(out):
    return sorted({(z0, z1) for z0, z1, s, *_ in out for _ in s})


def test_a_wall_runs_on_across_free_heights():
    out = tall_walls(slices(), [], LEVELS, {1.0, 2.0})
    assert spans(out) == [(0.0, 3.0)] and sum(len(s) for *_, s in out) == 4
    out = tall_walls(slices(), [], LEVELS, {1.0})                 # 2.0 is a layer's own height: a stop
    assert spans(out) == [(0.0, 2.0), (2.0, 3.0)]


def test_a_vertex_on_an_edge_stops_the_wall_and_the_stop_spreads_round_the_ring():
    flats = [(1.0, box(4, 0, 6, 2), True)]                        # a face at 1.0 with a corner at (4, 0)
    out = tall_walls(slices(), flats, LEVELS, {1.0, 2.0})
    for z0, z1, s in out:
        assert (z0, z1) in ((0.0, 1.0), (1.0, 3.0)), (z0, z1)     # every wall of the ring stops at 1.0
    assert sum(len(s) for z0, z1, s in out if (z0, z1) == (0.0, 1.0)) == 4


def test_walls_of_other_owners_do_not_join():
    """One wall changes owner at 1.0: it stops there, and so (the stop spreading) does its ring."""
    walls = slices()
    owners = [np.array([0, 0, 0, 0]), np.array([0, 0, 0, 1]), np.array([0, 0, 0, 1])]
    out = tall_walls(walls, [], LEVELS, {1.0, 2.0}, owners)
    got = sorted((z0, z1, int(o)) for z0, z1, s, own in out for o in own)
    assert got == [(0.0, 1.0, 0)] * 4 + [(1.0, 3.0, 0)] * 3 + [(1.0, 3.0, 1)]
    apart = [np.array([0, 1, 2, 3])] * 3                         # owners that keep to their walls join
    assert spans(tall_walls(walls, [], LEVELS, {1.0, 2.0}, apart)) == [(0.0, 3.0)]


def test_no_free_heights_leaves_the_walls_as_they_are():
    walls = slices()
    assert [(a, b, len(s)) for a, b, s in tall_walls(walls, [], LEVELS, set())] == [(a, b, 4) for a, b, _ in walls]
    assert tall_walls([], [], LEVELS, {1.0}) == []


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
