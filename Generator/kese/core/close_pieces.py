"""Pieces of one region that lie side by side less than a grid step apart along an edge, as two
coatings' walls grown from two groups of copper and put on the grid each on its own leave them: such
a crack is no gap the material has, and cutting it open as a pinch point (pinches.py) chops the
thinner piece again and again, each cut on the grid moving its edge a little, until the edge has
walked a few grid steps from where it was (the mask's wall into the copper beside it).  The two are
joined instead, where joining makes one clean polygon and adds no more than the crack."""
import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.graph import pairs_within
from kese.core.vertices import near_edge, noded


def joined_where_close(parts):
    """The parts (a list), every two that run side by side within near_edge() of each other along an
    edge joined into one, and every hole narrower than 2 near_edge() everywhere (such a crack inside
    one piece, a needle whose tip a pinch cut only moves along it) filled; and whether any were."""
    d = near_edge()
    parts, joined_any = cracks_filled(list(parts), d)
    if len(parts) < 2:
        return parts, joined_any
    i, j = pairs_within(parts, d)
    for a, b in zip(i.tolist(), j.tolist()):
        if parts[a].is_empty or parts[b].is_empty or not side_by_side(parts[a], parts[b], d):
            continue
        one = joined(parts[a], parts[b], d)
        if one is not None:
            parts[a], parts[b], joined_any = one, sh.EMPTY, True
    return [p for p in parts if not p.is_empty], joined_any


def side_by_side(p, q, d):
    """Whether p and q come within d of each other along a stretch longer than a few grid steps, not
    only at a point (two pieces that touch at a corner are a pinch point, which pinches.py opens)."""
    near = shapely.intersection(p.boundary, q.buffer(d, quad_segs=1))
    return near.length > 4 * sh.grid()


def joined(p, q, d):
    """p and q as one polygon on the grid: q's vertices within 1.5 grid steps of p's (a grid point's
    diagonal neighbour) snapped onto them first, so that what fills the crack is no wider than it.
    None where that is not one polygon, or adds more than a strip d wide along the shorter outline."""
    one = noded(shapely.union(p, shapely.snap(q, p, 1.5 * sh.grid()), grid_size=sh.grid()))
    if one.geom_type != "Polygon" or not one.is_valid:
        return None
    if one.area - p.area - q.area > d * min(p.length, q.length) or one.area < max(p.area, q.area):
        return None
    return one


def cracks_filled(parts, d):
    """The parts with their holes narrower than 2 d everywhere (those a buffer of -d empties) filled,
    and whether any were."""
    filled = False
    for k in np.flatnonzero(shapely.get_num_interior_rings(parts) > 0).tolist() if parts else []:
        holes = [shapely.Polygon(r) for r in parts[k].interiors]
        crack = [h.area <= d * h.length and h.buffer(-d).is_empty for h in holes]
        if any(crack):
            parts[k] = shapely.Polygon(parts[k].exterior, [h.exterior for h, c in zip(holes, crack) if not c])
            filled = True
    return parts, filled
