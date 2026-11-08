"""Cutting polygons along straight lines: a point wherever an edge crosses a line, worked out the
same way for every polygon that has the edge, so pieces cut apart meet in the same points."""
import numpy as np
import shapely

from kese.core.shapes2d import grid
from parameters import P


def cell_lines(lo, hi):
    """The x of the strip edges strictly between lo and hi: one every Geometry.TRIANGULATE_CELL_MM,
    a quarter of a grid step off the grid, so that no point on the grid lies on one, and no point
    on the edge of a grid point's hot pixel (GEOS's snap rounding: halfway between two grid points)."""
    w, g = P.Geometry.TRIANGULATE_CELL_MM, grid()
    k = np.arange(np.floor(lo / w), np.ceil(hi / w) + 1)
    xs = (np.round(k * w / g) + 0.25) * g
    return xs[(xs > lo) & (xs < hi)]


def crossed(polys, xs, ys):
    """The polygons (an array) with a point wherever an edge crosses x = xs or y = ys, worked out from
    the edge's lower end (an edge that only ends on a line gets none)."""
    if not len(polys) or not (len(xs) or len(ys)):
        return polys
    rings, of_poly = shapely.get_rings(polys, return_index=True)
    xy, of_ring = shapely.get_coordinates(rings, return_index=True)
    edge = np.flatnonzero(of_ring[1:] == of_ring[:-1])            # edge k runs from xy[k] to xy[k + 1]
    a, b = xy[edge], xy[edge + 1]
    keys, points = [edge.astype(float)], [a]
    for axis, lines in ((0, xs), (1, ys)):
        if not len(lines):
            continue
        ia, ib = np.searchsorted(lines, a[:, axis]), np.searchsorted(lines, b[:, axis])
        n = np.abs(ib - ia)
        e = np.repeat(np.arange(len(a)), n)
        if not len(e):
            continue
        line = lines[np.repeat(np.minimum(ia, ib), n) + np.arange(len(e)) - np.repeat(np.cumsum(n) - n, n)]
        p, q = a[e], b[e]
        t = (line - p[:, axis]) / (q[:, axis] - p[:, axis])
        inside = (t > 0) & (t < 1)
        e, line, p, q, t = e[inside], line[inside], p[inside], q[inside], t[inside]
        low = (p[:, axis] < q[:, axis])[:, None]
        lo, hi = np.where(low, p, q), np.where(low, q, p)
        cross = np.empty((len(e), 2))
        cross[:, axis] = line
        s = (line - lo[:, axis]) / (hi[:, axis] - lo[:, axis])
        cross[:, 1 - axis] = lo[:, 1 - axis] + s * (hi[:, 1 - axis] - lo[:, 1 - axis])
        keys.append(edge[e] + t)
        points.append(cross)
    if sum(len(k) for k in keys[1:]) == 0:
        return polys
    key = np.concatenate(keys)
    order = np.argsort(key, kind="stable")
    pts, ring = np.concatenate(points)[order], of_ring[np.floor(key[order]).astype(np.int64)]
    first = np.r_[0, np.flatnonzero(np.diff(ring)) + 1]
    closed = np.insert(pts, np.r_[first[1:], len(pts)], pts[first], axis=0)
    ring_of = np.insert(ring, np.r_[first[1:], len(ring)], ring[first])
    return shapely.polygons(shapely.linearrings(closed, indices=ring_of), indices=of_poly)
