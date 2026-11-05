"""The finish shells' air (kese/s4_geometry/shells.py, finish_shells.py) cut bore by bore, each by
the solid near it alone (air_near), a span's bores worked on in groups, and an inner layer whose
copper comes nowhere near the board edge left without air at once: every part's finish comes out,
height by height, as the cut by the whole board's union makes it, but for slivers thinner than a
grid step where an edge crossing rounds onto the grid another way.  A big part of the solid is cut
into tiles that fill it and do not overlap, and bores whose shells could meet are put in one group.
Takes about half a minute.

    python -m pytest tests/test_finish_shells.py    (or:  python tests/test_finish_shells.py)"""
import sys
from pathlib import Path

import numpy as np
import shapely
from shapely.geometry import Point, box

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core import shapes2d as sh  # noqa: E402
from kese.core.shapes2d import union  # noqa: E402
from kese.job import start  # noqa: E402
from kese.model.prisms import PrismSet  # noqa: E402
from kese.s1_read import read  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s3_resolve import resolve  # noqa: E402
from kese.s4_geometry import finish_shells, geometry, shells  # noqa: E402

FEATURES = ROOT.parent / "featureTest"
BOARDS = ["03_vias_through", "04_vias_blind_buried", "11_zones", "16_edge_plating_castellation",
          "16b_edge_plating_border", "18c_finish_before_mask", "22_hdi_module"]


def test_a_big_part_is_cut_into_tiles_that_fill_it_and_do_not_overlap():
    plane = box(0, 0, 40, 30).difference(union([Point(x, y).buffer(0.3, quad_segs=16)
                                                for x in np.arange(1, 40, 1.5) for y in np.arange(1, 30, 1.5)]))
    parts = shells.tiles(plane)
    assert len(parts) > 4 and all(shapely.get_num_coordinates(p) <= shells.TILE for p in parts)
    assert abs(sum(p.area for p in parts) - plane.area) < 1e-9
    assert shapely.symmetric_difference(union(parts), plane).area < 1e-9
    assert shells.tiles(box(0, 0, 1, 1)) == [box(0, 0, 1, 1)]


def test_bores_whose_shells_could_meet_share_a_group():
    saved = finish_shells.BORES_AT_A_TIME
    finish_shells.BORES_AT_A_TIME = 5
    try:
        rings = [Point(x, y).buffer(0.3).difference(Point(x, y).buffer(0.2)) for x in range(6) for y in range(4)]
        rings.append(Point(0.62, 0).buffer(0.3).difference(Point(0.62, 0).buffer(0.2)))   # 0.02 mm from the first
        found = finish_shells.bore_groups(rings, 0.01)
        assert sorted(k for g in found for k in g) == list(range(len(rings))) and all(g == sorted(g) for g in found)
        assert len(found) >= 4 and any(0 in g and 24 in g for g in found)
    finally:
        finish_shells.BORES_AT_A_TIME = saved
    assert finish_shells.bore_groups(rings[:3], 0.01) == [[0, 1, 2]]


def test_an_inner_band_inside_the_outline_has_no_air_and_joins_nothing():
    outline, copper = box(0, 0, 10, 10), box(1, 1, 2, 2)
    saved = finish_shells.union
    finish_shells.union = lambda regions: (_ for _ in ()).throw(AssertionError("joined"))
    try:
        assert finish_shells.air_beside([copper, outline], False)(box(0.5, 0.5, 3, 3)).is_empty
    finally:
        finish_shells.union = saved
    edge = finish_shells.air_beside([copper, outline], False)(box(9, 4, 11, 6))      # past the edge
    assert abs(edge.area - 2) < 1e-9
    outer = finish_shells.air_beside([copper], True)(box(0.5, 0.5, 3, 3))           # an outer layer
    assert abs(outer.area - (2.5 ** 2 - 1)) < 1e-9


def finish_prisms(r, near):
    """The finish prisms of a resolved board: the air cut bore by bore, the bores in groups of seven
    (near), or by the whole union, each span at once (as before)."""
    saved = finish_shells.air_near, finish_shells.air_beside, finish_shells.BORES_AT_A_TIME
    finish_shells.BORES_AT_A_TIME = 7 if near else 10 ** 9
    if not near:
        def whole(regions):
            joined = sh.snap(union(list(regions)))
            return lambda band: sh.diff(band, joined)
        finish_shells.air_near = whole
        finish_shells.air_beside = lambda solid, outer: lambda band: sh.diff(band, sh.snap(union(solid)))
    try:
        ps = PrismSet(regions=r)
        finish_shells.build(r, ps)
    finally:
        finish_shells.air_near, finish_shells.air_beside, finish_shells.BORES_AT_A_TIME = saved
    return [p for p in ps.prisms if p.role == "finish"]


def test_the_air_cut_bore_by_bore_is_the_whole_union_s_but_for_slivers():
    for name in BOARDS:
        job = start("simulation", ["glb"], None, (), False, lambda s: None)
        r = resolve.run(collect.run(read.run(str(FEATURES / f"{name}.kicad_pcb"), job), job), job)
        job.status.stop()
        geometry.geometry(r, "simulation")            # the copper bands the shells stand on
        a, b = by_place(finish_prisms(r, near=False)), by_place(finish_prisms(r, near=True))
        assert a and a.keys() == b.keys(), name
        for key, p in a.items():
            d = shapely.symmetric_difference(p, b[key])
            assert shapely.buffer(d, -0.5 * sh.grid(), join_style="mitre").is_empty, (name, key, d.area)
            assert abs(p.area - b[key].area) <= 1e-3 * max(p.area, 1e-6), (name, key)


def by_place(prisms):
    """{(part, z0, z1, layer, net): the prisms' region there, joined}: the bores' groups make a
    prism each where a whole span made one."""
    out = {}
    for p in prisms:
        out.setdefault((p.part, p.z0, p.z1, p.layer, p.net), []).append(p.region)
    return {key: union(regions) for key, regions in out.items()}


if __name__ == "__main__":
    test_a_big_part_is_cut_into_tiles_that_fill_it_and_do_not_overlap()
    test_bores_whose_shells_could_meet_share_a_group()
    test_an_inner_band_inside_the_outline_has_no_air_and_joins_nothing()
    test_the_air_cut_bore_by_bore_is_the_whole_union_s_but_for_slivers()
    print("ok")
