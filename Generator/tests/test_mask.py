"""The solder mask's split over the copper (kese/core/conformal.py, kese/s4_geometry/solder_mask.py):
where a pad's opening follows its edge, a grid step off or with other points along its curve, the
mask on the copper keeps only slivers, all of them left out (without_hairlines), while mask on the
copper wider than twice SolderMask.MASK_OVER_COPPER_HAIRLINE_MM is kept, a sliver ending in a wide
piece too, and so are the flat mask and the wall.

    python -m pytest tests/test_mask.py        (or:  python tests/test_mask.py)"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import shapely  # noqa: E402
from shapely import affinity  # noqa: E402
from shapely.geometry import Point, box  # noqa: E402

from kese.core import shapes2d as sh  # noqa: E402
from kese.core.conformal import conformal_regions, without_hairlines  # noqa: E402
from parameters import P  # noqa: E402

H = P.SolderMask.MASK_OVER_COPPER_HAIRLINE_MM


def mask_over(pads, openings):
    """(flat, top, wall) of a mask over the pads, 10 um thick, with the openings."""
    region = sh.diff(sh.snap(box(-3, -3, 6, 3)), sh.snap(sh.union(openings)))
    return conformal_regions(region, sh.snap(sh.union(pads)), 0.01, 4)


def test_a_pad_whose_opening_follows_its_edge_keeps_no_mask_on_its_copper():
    round_pad = Point(0, 0).buffer(0.5, quad_segs=16)
    other_points = affinity.rotate(round_pad, 360 / 64 / 2, origin=(0, 0))      # half a segment round
    square_pad = box(2, -0.5, 3, 0.5)
    step_off = box(2 + sh.grid(), -0.5, 3 + sh.grid(), 0.5)                       # a grid step to the right
    flat, top, wall = mask_over([round_pad, square_pad], [other_points, step_off])
    slivers = shapely.get_parts(top)
    assert len(slivers) > 32 and shapely.is_empty(shapely.buffer(slivers, -H)).all()
    kept, gone = without_hairlines(top, H)
    assert kept.is_empty and gone == len(slivers)
    assert flat.area > 50 and wall.area > 0.01                                     # the rest of the mask stays


def test_mask_on_copper_wider_than_twice_the_hairline_is_kept():
    trace = box(-2, -0.1, 4, 0.1)                                                  # under the mask but for its ends
    opening = [box(-2.5, -0.5, -1.5, 0.5), box(3.5, -0.5, 4.5, 0.5)]
    _, top, _ = mask_over([trace], opening)
    assert without_hairlines(top, H) == (top, 0) and abs(top.area - 5 * 0.2) < 1e-9
    wide, narrow = box(0, 0, 1, 3 * H), box(0, 1, 1, 1 + 1.5 * H)                  # 3 um and 1.5 um across
    tail = sh.union([box(0, 2, 1, 2 + H), box(1, 2, 1.01, 2.01)])                  # a sliver ending in a wide piece
    kept, gone = without_hairlines(sh.as_region([wide, narrow, *shapely.get_parts(tail)]), H)
    assert gone == 1 and abs(kept.area - wide.area - tail.area) < 1e-12
    assert without_hairlines(sh.EMPTY, H) == (sh.EMPTY, 0) and without_hairlines(narrow, 0) == (narrow, 0)


if __name__ == "__main__":
    test_a_pad_whose_opening_follows_its_edge_keeps_no_mask_on_its_copper()
    test_mask_on_copper_wider_than_twice_the_hairline_is_kept()
    print("ok")
