"""Pinch points: where two pieces of a region, or two rings of one piece, touch at a single
point, the solid built on it is pinched to a line there and could not close on its own; and
where a vertex of one ring lies within a grid step of another ring's edge, the vertex sharing
(kese/core/vertices.py) would bend the edge onto it and make such a pinch.  So a disc around
every such point is cut out of the smaller piece, and the cut is tried again with twice the
radius until the pieces are clear of each other: two tangent circles leave each other so slowly
that a cut of a grid step can end on the other's edge again.

The same happens between two heights: where a piece of the material below a height and a piece
of the material above it meet along an edge with the material on opposite sides, the solid is
pinched to that edge, with four faces on it (the two walls, a face looking up, one looking down).
A strip along the edge is cut out of the smaller piece then (open_pinches_between)."""
import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.vertices import grid_keys, near_edge, noded, pairs_in, vertex_keys
from parameters import P

CUT_ROUNDS = 10          # the radius doubles each round: up to 512 times Geometry.PINCH_POINT_OPENING_MM


def open_pinches(region, log=None):
    """The region with a gap at every pinch point (see above); the region itself when it has none."""
    region = sh.polys_only(region)
    if region.is_empty:
        return region
    parts = list(shapely.get_parts(region))
    check = range(len(parts))                              # the parts whose rings are checked this round
    cut_any = False
    for round_ in range(CUT_ROUNDS):
        cuts = pieces_too_close(parts)
        for k in check:
            for p in repeated_vertices(parts[k]):
                cuts.setdefault(k, []).append(p)
        if not cuts:
            break
        r = P.Geometry.PINCH_POINT_OPENING_MM * 2 ** round_
        for k, pts in cuts.items():
            discs = shapely.union_all([shapely.Point(p).buffer(r, quad_segs=2) for p in pts])
            parts[k] = noded(parts[k].difference(discs, grid_size=sh.grid()))
        check, cut_any = sorted(cuts), True
    else:
        if log:
            log(f"pinch points left after {CUT_ROUNDS} rounds of cutting")
    if not cut_any:
        return region
    return sh.as_region([q for p in parts for q in shapely.get_parts(p) if q.area > 1e-10])


def pieces_too_close(parts):
    """{index of the smaller piece: [points]} for every two pieces that touch at a point or come
    within near_edge() of each other: the touching points, or the middle of the shortest line
    between them."""
    cuts = {}
    if len(parts) < 2:
        return cuts
    i, j = shapely.STRtree(parts).query(parts, predicate="dwithin", distance=near_edge())
    for a, b in zip(i.tolist(), j.tolist()):
        if a < b:
            k = b if parts[b].area <= parts[a].area else a
            pts = points_of(parts[a].intersection(parts[b]))
            if not pts:
                pts = [tuple(np.asarray(shapely.shortest_line(parts[a], parts[b]).coords).mean(axis=0))]
            cuts.setdefault(k, []).extend(pts)
    return cuts


def points_of(g):
    """The points of a geometry that are points (where two pieces touch at a point)."""
    return [tuple(p.coords[0]) for p in shapely.get_parts(g) if p.geom_type == "Point"]


def repeated_vertices(polygon):
    """The vertices a polygon has twice (where its rings touch each other or themselves), as xy."""
    keys, ring, xy = vertex_keys(polygon)
    ring_end = np.flatnonzero(np.r_[ring[1:] != ring[:-1], True])    # a ring's closing point repeats its first
    keys, xy = np.delete(keys, ring_end), np.delete(xy, ring_end, axis=0)
    _, idx, count = np.unique(keys, return_index=True, return_counts=True)
    return [tuple(p) for p in xy[idx[count > 1]]]


def open_pinches_between(below, above, log=None):
    """The material below a height and the material above it, with a gap cut wherever a piece of
    one meets a piece of the other along an edge with the material on opposite sides (see
    above): a strip along the edge, out of the smaller piece, twice as wide each round as for
    open_pinches().  -> (below, above, whether anything was cut)."""
    parts = [list(shapely.get_parts(sh.polys_only(below))), list(shapely.get_parts(sh.polys_only(above)))]
    cut_any = False
    for round_ in range(CUT_ROUNDS):
        cuts = edges_against_each_other(*parts)
        if not cuts:
            break
        r = P.Geometry.PINCH_POINT_OPENING_MM * 2 ** round_
        for (side, k), edges in cuts.items():
            strips = shapely.union_all([shapely.LineString(e).buffer(r, quad_segs=2) for e in edges])
            parts[side][k] = noded(parts[side][k].difference(strips, grid_size=sh.grid()))
        cut_any = True
    else:
        if log:
            log(f"pinch edges between two heights left after {CUT_ROUNDS} rounds of cutting")
    if not cut_any:
        return below, above, False
    below, above = (sh.as_region([q for p in side for q in shapely.get_parts(p) if q.area > 1e-10]) for side in parts)
    return below, above, True


def edges_against_each_other(below, above):
    """{(side, index of the smaller piece): [edges as ((x, y), (x, y))]} for every edge that a
    piece of `below` (side 0) and a piece of `above` (side 1) have the other way round."""
    cuts = {}
    if not below or not above:
        return cuts
    lo, hi = ring_edges(below), ring_edges(above)
    against = np.flatnonzero(pairs_in(lo[0], lo[1], hi[1], hi[0]))
    piece_above = dict(zip(zip(hi[1].tolist(), hi[0].tolist()), hi[2].tolist()))
    for i in against.tolist():
        j, k = int(lo[2][i]), piece_above[(int(lo[0][i]), int(lo[1][i]))]
        side = 0 if below[j].area <= above[k].area else 1
        cuts.setdefault((side, j if side == 0 else k), []).append((tuple(lo[3][i]), tuple(lo[4][i])))
    return cuts


def ring_edges(parts):
    """Every edge of the parts' rings: (grid key of its start, of its end, the part it is on, its
    start xy, its end xy), each an array over the edges."""
    rings, of_part = shapely.get_rings(np.array(parts, dtype=object), return_index=True)
    xy, ring = shapely.get_coordinates(rings, return_index=True)
    key = grid_keys(xy)
    e = np.flatnonzero(ring[1:] == ring[:-1])                          # the edge from point e to e + 1
    return key[e], key[e + 1], of_part[ring[e]], xy[e], xy[e + 1]
