"""Stage 3's union of a net's items on one layer (kese/s3_resolve/copper.py, net_union): joined in
floating point, then rounded to the grid as a whole.  Two zone fills whose shared edge agrees only to
within floating point join with no crack, a crack narrower than the grid closes, items that do not
meet stay apart, every vertex ends on the grid, the area is within a grid step of the exact union's
(closer than a union on the grid comes), the result is on no grid, so the clip to the outline that
follows leaves no burr past the board edge, and when GEOS cannot join the items in floating point the
union on the grid is used.

    python -m pytest tests/test_copper_union.py     (or:  python tests/test_copper_union.py)"""
import numpy as np
import shapely
import shapely.errors
from shapely.geometry import LineString, Point, Polygon, box

import kese.s3_resolve.copper as copper
from helpers import run_tests
from kese.core import shapes2d as sh
from kese.s3_resolve.copper import net_union


def on_grid(g):
    k = shapely.get_coordinates(g) / sh.grid()
    return bool(np.abs(k - np.round(k)).max() < 1e-6)


def test_fills_that_meet_only_to_within_floating_point_join_with_no_crack():
    left = Polygon([(0, 0), (5.0000000000001, 0), (5.0000000000001, 10), (0, 10)])
    right = Polygon([(4.9999999999999, 0), (10, 0), (10, 10), (4.9999999999999, 10)])
    apart = [box(0, 0, 5, 10), box(5 + 1e-12, 0, 10, 10)]
    crack = [box(0, 0, 5, 10), box(5 + 3e-5, 0, 10, 10), box(4, 4, 6, 6)]     # narrower than the grid
    for gs in ([left, right], apart, crack):
        g = net_union(gs)
        assert g.geom_type == "Polygon" and not g.interiors and on_grid(g) and g.is_valid
        assert abs(g.area - 100) < 1e-6


def test_items_that_do_not_meet_stay_apart_and_the_area_is_within_a_grid_step_of_the_exact_union():
    assert len(shapely.get_parts(net_union([box(0, 0, 1, 1), box(2, 0, 3, 1)]))) == 2
    rng = np.random.default_rng(5)
    tracks = [LineString(rng.uniform(0, 20, size=(2, 2))).buffer(0.1234567, quad_segs=6) for _ in range(150)]
    pads = [Point(rng.uniform(0, 20, size=2)).buffer(0.4567891, quad_segs=8) for _ in range(60)]
    g, grid = net_union(tracks + pads), shapely.union_all(tracks + pads, grid_size=sh.grid())
    exact = shapely.union_all(tracks + pads)
    assert g.is_valid and on_grid(g)
    # each edge moves by less than a grid step: the area by less than the perimeter times a step,
    # and by less than a union on the grid moves it (that rounds every item's vertices, not just
    # the union's: 2.3e-3 mm2 here, against 3e-4 mm2)
    assert abs(g.area - exact.area) <= g.length * sh.grid()
    assert abs(g.area - exact.area) < abs(grid.area - exact.area)
    assert len(shapely.get_parts(g)) == len(shapely.get_parts(grid))
    assert sum(len(p.interiors) for p in shapely.get_parts(g)) == sum(len(p.interiors) for p in shapely.get_parts(grid))


def test_the_union_is_on_no_grid_so_the_clip_to_the_outline_leaves_no_burr_past_the_edge():
    # an outline edge with ends off the grid (a chord of an arc), and a zone fill with a vertex 0.09 um
    # past it (KiCad's fill follows chords of its own): clipped on the grid, the edge would be bent
    # through that vertex, 0.08 um past the board edge once rounded (seen on 16b_edge_plating_border)
    outline = Polygon([(125.101168, 122.994869), (125.151428, 122.988468), (125.16, 123.1), (125.09, 123.1)])
    fill = Polygon([(125.0523, 122.9985), (125.10451, 122.994351), (125.156407, 122.987519), (125.16, 123.05),
                    (125.06, 123.05)])
    g = net_union([fill, box(125.11, 123.0, 125.12, 123.01)])
    assert shapely.get_precision(g) == 0 and on_grid(g)
    assert outline.buffer(1e-9).contains(g.intersection(outline))


def test_a_union_geos_cannot_do_in_floating_point_is_done_on_the_grid():
    real = shapely.union_all

    def refusing(geoms, grid_size=None, **kw):
        if grid_size is None:
            raise shapely.errors.GEOSException("TopologyException: found non-noded intersection")
        return real(geoms, grid_size=grid_size, **kw)
    copper.shapely.union_all = refusing
    try:
        g = net_union([box(0, 0, 1.00001234, 1), box(1, 0, 2, 1)])
    finally:
        copper.shapely.union_all = real
    assert g.geom_type == "Polygon" and on_grid(g) and abs(g.area - 2) < 1e-6


if __name__ == "__main__":
    run_tests(__file__)
