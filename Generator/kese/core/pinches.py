"""Pinch points: where two pieces or rings touch at a point, or a vertex lies within a grid step
of another ring, a disc is cut out of the smaller piece (doubled until clear); where pieces below
and above a height meet along an edge, a strip is cut (open_pinches_between)."""
import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.vertices import grid_keys, near_edge, noded, pairs_in
from parameters import P


def open_pinches(region, log=None):
    """The region with a gap at every pinch point (see above); the region itself when it has none."""
    region = sh.polys_only(region)
    if region.is_empty:
        return region
    parts = list(shapely.get_parts(region))
    check = range(len(parts))                              # the parts whose rings are checked this round
    cut_any = False
    for round_ in range(sh.G().PINCH_CUT_ROUNDS):
        cuts = pieces_too_close(parts)
        for k, pts in repeated_vertices(parts, check).items():
            cuts.setdefault(k, []).extend(pts)
        if not cuts:
            break
        r = P.Geometry.PINCH_POINT_OPENING_MM * 2 ** round_
        for k, pts in cuts.items():
            discs = shapely.union_all([cut_disc(p, r) for p in pts])
            parts[k] = noded(parts[k].difference(discs, grid_size=sh.grid()))
        check, cut_any = sorted(cuts), True
    else:
        if log:
            log(f"pinch points left after {sh.G().PINCH_CUT_ROUNDS} rounds of cutting")
    if not cut_any:
        return region
    return sh.as_region([q for p in parts for q in shapely.get_parts(p) if q.area > sh.G().SLIVER_AREA_MM2])


def cut_disc(p, r):
    """The disc cut out around a pinch point: an octagon turned by Geometry.PINCH_DISC_TURN_DEG, so no
    corner lies on KiCad's horizontal, vertical or 45-degree lines through the point."""
    a = np.radians(sh.G().PINCH_DISC_TURN_DEG + 45.0 * np.arange(8))
    return shapely.Polygon(np.c_[p[0] + r * np.cos(a), p[1] + r * np.sin(a)])


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


def repeated_vertices(parts, check):
    """{k: the vertices part k has twice (where its rings touch each other or themselves), as xy}
    for the parts k in `check` that have any, in check's order and each part's in the order of
    their grid keys.  All the parts at once: there can be thousands, most with none."""
    check = [k for k in check if not parts[k].is_empty]       # (a piece the cuts took away entirely)
    if not check:
        return {}
    pieces, of = shapely.get_parts(np.array([parts[k] for k in check], dtype=object), return_index=True)
    rings, of_piece = shapely.get_rings(pieces, return_index=True)
    xy, ring = shapely.get_coordinates(rings, return_index=True)
    keep = np.r_[ring[1:] == ring[:-1], False]                 # a ring's closing point repeats its first
    xy, owner = xy[keep], of[of_piece[ring[keep]]]
    key = grid_keys(xy)
    order = np.lexsort((key, owner))                            # stable: the first of equal points first
    start = np.r_[True, (owner[order][1:] != owner[order][:-1]) | (key[order][1:] != key[order][:-1])]
    first, count = order[start], np.diff(np.r_[np.flatnonzero(start), len(order)])
    twice = first[count > 1]
    out = {}
    for i, p in zip(owner[twice].tolist(), xy[twice]):
        out.setdefault(check[i], []).append(tuple(p))
    return out


def open_pinches_between(below, above, log, first):
    """The material below and above a height, with a strip cut out of the smaller piece wherever
    two meet along an edge with the material on opposite sides, wider from round `first` on.
    -> (below, above, whether anything was cut)."""
    parts = [list(shapely.get_parts(sh.polys_only(below))), list(shapely.get_parts(sh.polys_only(above)))]
    cut_any = False
    for round_ in range(first, first + sh.G().PINCH_CUT_ROUNDS):
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
            log(f"pinch edges between two heights left after {sh.G().PINCH_CUT_ROUNDS} rounds of cutting")
    if not cut_any:
        return below, above, False
    below, above = (sh.as_region([q for p in side for q in shapely.get_parts(p) if q.area > sh.G().SLIVER_AREA_MM2]) for side in parts)
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
