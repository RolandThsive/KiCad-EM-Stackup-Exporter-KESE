"""The split of a coating laid over raised copper: flat on the base, on top of the copper, and the
wall beside it.  As KiCad builds every piece of copper on its own, each piece is grown and cut on
its own against only the coating near it; one boolean operation over the whole board gives the
same regions, to a fraction of a micron, in many times the time."""
import numpy as np
import shapely
from shapely.geometry import Polygon

from kese.core.shapes2d import EMPTY, as_region, diff, grid, inter, joined, meeting, polys_only, snap


def grow(g, t, quad_segs):
    """The region grown by t, every part on its own, on the grid."""
    parts = shapely.get_parts(polys_only(g))
    grown = shapely.set_precision(shapely.buffer(parts, t, quad_segs=quad_segs), grid())
    return joined([p for q in grown for p in shapely.get_parts(polys_only(q)) if not p.is_empty])


def near(g, other, d):
    """The parts of g within d of other."""
    parts = shapely.get_parts(polys_only(g))
    if not len(parts) or polys_only(other).is_empty:
        return EMPTY
    hits = shapely.STRtree(parts).query(shapely.get_parts(polys_only(other)), predicate="dwithin", distance=d)[1]
    return as_region(list(parts[np.unique(hits)]))


def cutter(region):
    """x -> the polygons of x inside region, for a small x: only the parts of the region that x
    meets, and only their holes near x, take part."""
    parts = list(shapely.get_parts(polys_only(region)))
    shells = [Polygon(p.exterior) for p in parts]
    holes = [(k, Polygon(ring)) for k, p in enumerate(parts) for ring in p.interiors]
    shell_tree = shapely.STRtree(shells)
    hole_tree = shapely.STRtree([h for _, h in holes]) if holes else None
    shapely.prepare(shells)

    def cut(x):
        x = polys_only(x)
        out = []
        if x.is_empty:
            return out
        for k in shell_tree.query(x, predicate="intersects").tolist():
            y = x if shells[k].contains(x) else inter(x, shells[k])
            if hole_tree is not None and not y.is_empty:
                inside = [holes[h][1] for h in hole_tree.query(y, predicate="intersects").tolist() if holes[h][0] == k]
                if inside:
                    y = diff(y, as_region(inside))
            out += [p for p in shapely.get_parts(y) if not p.is_empty]
        return out
    return cut


def conformal_regions(region, raised, t, wall_quad_segs, around="raised"):
    """Split a coating of thickness t laid over `raised` into (flat on the base, on top of the raised
    copper, wall beside the copper).  around="raised" when the raised copper is the one in many
    small pieces (the solder mask over the copper), "region" when the coating is (silk on the mask)."""
    region, raised = snap(region), snap(raised)
    if region.is_empty:
        return EMPTY, EMPTY, EMPTY
    if raised.is_empty:
        return region, EMPTY, EMPTY
    return (around_region if around == "region" else around_raised)(region, raised, t, wall_quad_segs)


def around_raised(region, raised, t, quad_segs):
    """Every group of copper that meets once grown is grown, and cut by the coating near it, on its
    own; the flat coating is the region less all the grown copper."""
    parts = shapely.get_parts(raised)
    grown = shapely.set_precision(shapely.buffer(parts, t, quad_segs=quad_segs), grid())
    cut = cutter(region)
    rings, tops, walls = [], [], []
    for idx in meeting(list(grown)):
        g = grown[idx[0]] if len(idx) == 1 else polys_only(shapely.union_all(list(grown[idx]), grid_size=grid()))
        cu = parts[idx[0]] if len(idx) == 1 else shapely.MultiPolygon(list(parts[idx]))
        rings += [p for p in shapely.get_parts(polys_only(g)) if not p.is_empty]
        tops += cut(cu)
        walls += cut(diff(g, cu))
    return diff(region, as_region(rings)), as_region(tops), as_region(walls)


def around_region(region, raised, t, quad_segs):
    """Every piece of the coating split on its own, against the raised copper inside a box around
    it wide enough that what the box cuts off cannot reach the piece once grown."""
    cut = cutter(raised)
    m = 2 * t + 8 * grid()
    flats, tops, walls = [], [], []
    for s in shapely.get_parts(region):
        x0, y0, x1, y1 = s.bounds
        local = as_region(cut(shapely.box(x0 - m, y0 - m, x1 + m, y1 + m)))
        if local.is_empty:
            flats.append(s)
            continue
        g = grow(local, t, quad_segs)
        for out, piece in ((flats, diff(s, g)), (tops, inter(s, local)), (walls, inter(s, diff(g, local)))):
            out += [p for p in shapely.get_parts(piece) if not p.is_empty]
    return as_region(flats), as_region(tops), as_region(walls)
