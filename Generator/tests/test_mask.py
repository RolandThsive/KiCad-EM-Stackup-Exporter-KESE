"""The solder mask's split over the copper (kese/core/conformal.py, kese/s4_geometry/solder_mask.py):
where a pad's opening follows its edge, a grid step off or with other points along its curve, the
mask on the copper keeps only slivers, all of them left out (without_hairlines), while mask on the
copper wider than twice SolderMask.MASK_OVER_COPPER_HAIRLINE_MM is kept, a sliver ending in a wide
piece too, and so are the flat mask and the wall.  The slivers left out are added to the openings,
so the finish covers them (kese/s4_geometry/finish.py), each net's finish only its own, and on a
board the finish and the mask leave no copper face bare.

    python -m pytest tests/test_mask.py        (or:  python tests/test_mask.py)"""
from types import SimpleNamespace

import shapely
from shapely import affinity
from shapely.geometry import Point, box

from helpers import FEATURES, run_stages, run_tests, settings
from kese.core import shapes2d as sh
from kese.core.conformal import conformal_regions, without_hairlines
from kese.s3_resolve import resolve
from kese.s4_geometry import geometry
from kese.s4_geometry.finish import exposed
from parameters import P

H = P.SolderMask.MASK_OVER_COPPER_HAIRLINE_MM


def mask_over(pads, openings):
    """(flat, top, wall) of a mask over the pads, 10 um thick, with the openings."""
    region = sh.diff(sh.snap(box(-3, -3, 6, 3)), sh.snap(sh.union(openings)))
    return conformal_regions(region, sh.snap(sh.union(pads)), 0.01, 4)


def pads_and_openings():
    """A round pad whose opening has other points along its curve, and a square pad whose opening is
    a grid step off."""
    round_pad = Point(0, 0).buffer(0.5, quad_segs=16)
    other_points = affinity.rotate(round_pad, 360 / 64 / 2, origin=(0, 0))      # half a segment round
    square_pad = box(2, -0.5, 3, 0.5)
    step_off = box(2 + sh.grid(), -0.5, 3 + sh.grid(), 0.5)                       # a grid step to the right
    return [round_pad, square_pad], [other_points, step_off]


def test_a_pad_whose_opening_follows_its_edge_keeps_no_mask_on_its_copper():
    flat, top, wall = mask_over(*pads_and_openings())
    slivers = shapely.get_parts(top)
    assert len(slivers) > 32 and shapely.is_empty(shapely.buffer(slivers, -H)).all()
    kept, gone = without_hairlines(top, H)
    assert kept.is_empty and len(gone) == len(slivers)
    assert flat.area > 50 and wall.area > 0.01                                     # the rest of the mask stays


def test_the_finish_covers_the_slivers_the_mask_leaves_out_each_net_its_own():
    pads, openings = pads_and_openings()
    _, gone = without_hairlines(mask_over(pads, openings)[1], H)
    cu, opened = sh.snap(sh.union(pads)), sh.snap(sh.union(openings))
    r = SimpleNamespace(mask_open={"F": opened}, silk={})
    assert cu.area - exposed(r, "F", cu).area > 5e-4                               # bare copper without them
    r.mask_open["F"] = sh.joined(list(shapely.get_parts(opened)) + gone)            # as solder_mask.build adds them
    bare = exposed(r, "F", cu)
    assert sh.diff(bare, cu).is_empty and cu.area - bare.area < 1e-5 and bare_only_where_rounded(cu, bare)
    for pad in map(sh.snap, pads):                                                 # FINISH_GROUPING = "net"
        mine = exposed(r, "F", pad)
        assert sh.diff(mine, pad).is_empty and pad.area - mine.area < 1e-5 and bare_only_where_rounded(pad, mine)


def bare_only_where_rounded(cu, finish):
    """Whether the copper the finish leaves bare is no more than a grid step across anywhere: the
    triangles where the grid rounds two outlines that cross apart (as it does without the slivers)."""
    left = shapely.get_parts(sh.diff(cu, finish))
    return bool(shapely.is_empty(shapely.buffer(left, -sh.grid() / 2)).all())


def test_on_a_board_the_finish_and_the_mask_leave_no_copper_face_bare():
    """07_pad_shapes, the mask on: three of its pads' openings follow their edges with other points."""
    with settings({"Stackup.solder_mask": True}):
        r, _ = run_stages(FEATURES / "07_pad_shapes.kicad_pcb", resolve)
        ps = geometry.geometry(r, "simulation")
    assert "solder mask: 3 slivers on the copper narrower than 0.002 mm left out (F.Mask)" in ps.notes
    for layer, up in (("F.Cu", True), ("B.Cu", False)):
        face = max(abs(z) for z in r.stackup.band[layer])             # the copper's outer face
        on_it = [p.region for p in ps.prisms if p.role in ("finish", "mask_over_copper") and (p.z0 > 0) == up
                 and abs(min(abs(p.z0), abs(p.z1)) - face) < 1e-9]
        assert on_it and bare_only_where_rounded(r.copper_all[layer], sh.union(on_it)), layer


def test_mask_on_copper_wider_than_twice_the_hairline_is_kept():
    trace = box(-2, -0.1, 4, 0.1)                                                  # under the mask but for its ends
    opening = [box(-2.5, -0.5, -1.5, 0.5), box(3.5, -0.5, 4.5, 0.5)]
    _, top, _ = mask_over([trace], opening)
    assert without_hairlines(top, H) == (top, []) and abs(top.area - 5 * 0.2) < 1e-9
    wide, narrow = box(0, 0, 1, 3 * H), box(0, 1, 1, 1 + 1.5 * H)                  # 3 um and 1.5 um across
    tail = sh.union([box(0, 2, 1, 2 + H), box(1, 2, 1.01, 2.01)])                  # a sliver ending in a wide piece
    kept, gone = without_hairlines(sh.as_region([wide, narrow, *shapely.get_parts(tail)]), H)
    assert len(gone) == 1 and gone[0].equals(narrow) and abs(kept.area - wide.area - tail.area) < 1e-12
    assert without_hairlines(sh.EMPTY, H) == (sh.EMPTY, []) and without_hairlines(narrow, 0) == (narrow, [])


if __name__ == "__main__":
    run_tests(__file__)
