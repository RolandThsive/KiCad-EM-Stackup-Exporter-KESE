"""The tops and bottoms of prisms: polygons cut into triangles.  As in KiCad's 3D viewer, earcut cuts
them, and a big polygon strip by strip, as KiCad cuts big polygons into 1 cm cells first: earcut's
time grows with the points times the holes.  Earcut is not always right (it runs two holes whose
edges lie on one line into one, through a slit of no width), so every cut is checked, and a
polygon or a strip whose triangles do not close exactly on its edges is cut again by Manifold's
triangulator."""
from collections import defaultdict

import manifold3d as mf
import mapbox_earcut
import numpy as np
import shapely

from kese.core.cells import cell_lines, crossed
from kese.core.shapes2d import polys_only
from parameters import P


def caps(polys, cut):
    """The polygons' tops cut into triangles by cut(points, ring ends): (xy, nxt, poly, tri, bad),
    with xy, nxt and poly as rings_of() gives them, tri counter-clockwise, and bad marking the
    polygons whose triangles fold over or do not close exactly on their edges, and those with a
    point twice (rings that touch there: the slow way, extrude_cdt(), takes them)."""
    xy, nxt, poly, spans, bad = rings_of(polys)
    tri = [cut(xy[a:b], ends) + a for (a, b, ends), skip in zip(spans, bad.tolist()) if not skip]
    tri = np.concatenate(tri).astype(np.int64) if tri else np.empty((0, 3), dtype=np.int64)
    of = poly[tri[:, 0]]
    twice = twice_area(xy, tri)
    turn = (np.bincount(of, weights=twice, minlength=len(polys)) < 0)[of]
    tri[turn], twice[turn] = tri[turn][:, ::-1], -twice[turn]
    size = (np.diff(xy[tri], axis=1) ** 2).sum(axis=(1, 2))
    bad[of[twice < -1e-9 * size]] = True                 # a triangle folded over
    bad[open_edges(tri, nxt, poly)] = True
    return xy, nxt, poly, tri, bad


def rings_of(polys):
    """The points of the polygons' rings, outer rings counter-clockwise and holes clockwise, without
    the closing points: (xy, the next point along the ring of every point, the polygon of every
    point, [(first point, end, ring ends from the first point)] of every polygon, polygons with a
    point twice)."""
    rings, ring_poly = shapely.get_rings(polys, return_index=True)
    xy, ring = shapely.get_coordinates(rings, return_index=True)
    keep = np.r_[ring[1:] == ring[:-1], False]           # every ring ends on its first point again
    xy, ring = xy[keep], ring[keep]
    n = len(xy)
    start = np.r_[0, np.flatnonzero(np.diff(ring)) + 1]
    end = np.r_[start[1:], n]
    nxt = np.arange(1, n + 1)
    nxt[end - 1] = start
    twice = np.bincount(ring, weights=xy[:, 0] * xy[nxt, 1] - xy[nxt, 0] * xy[:, 1], minlength=len(start))
    outer = np.r_[True, ring_poly[1:] != ring_poly[:-1]]
    turn = ((twice > 0) != outer)[ring]
    idx = np.arange(n)
    idx[turn] = (start + end - 1)[ring[turn]] - idx[turn]
    xy = xy[idx]
    poly = ring_poly[ring]
    order = np.lexsort((xy[:, 1], xy[:, 0], poly))
    same = (np.diff(xy[order], axis=0) == 0).all(axis=1) & (np.diff(poly[order]) == 0)
    repeated = np.zeros(len(polys), dtype=bool)
    repeated[poly[order[1:][same]]] = True
    first = np.flatnonzero(outer)
    span = zip(start[first].tolist(), np.r_[start[first[1:]], n].tolist(),
               first.tolist(), np.r_[first[1:], len(start)].tolist())
    return xy, nxt, poly, [(a, b, end[r0:r1] - a) for a, b, r0, r1 in span], repeated


def twice_area(xy, tri):
    """Twice the signed area of every triangle, positive when it runs counter-clockwise."""
    a, b, c = xy[tri[:, 0]], xy[tri[:, 1]], xy[tri[:, 2]]
    return (b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0])


def open_edges(tri, nxt, poly):
    """The polygons whose triangles (counter-clockwise) do not close exactly on their rings: with
    every ring edge taken backwards (as its wall meets it), every edge must be met once each way."""
    n = len(nxt)
    e = np.concatenate([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]])
    key, count = np.unique(np.concatenate([e[:, 0] * n + e[:, 1], nxt * n + np.arange(n)]), return_counts=True)
    back = key % n * n + key // n
    at = np.minimum(np.searchsorted(key, back), len(key) - 1)
    return np.unique(poly[key[(count > 1) | (key[at] != back)] // n])


def earcut_cut(xy, ends):
    """One polygon (its points, and where each ring ends) cut by earcut: triangles of its points."""
    try:
        return mapbox_earcut.triangulate_float64(xy, ends.astype(np.uint32)).reshape(-1, 3)
    except Exception:
        return np.empty((0, 3), dtype=np.int64)       # no triangles: the polygon fails the check


def manifold_cut(xy, ends):
    """earcut_cut by Manifold's triangulator: slower, but it keeps to the edges it is given."""
    try:
        return np.asarray(mf.triangulate(np.split(xy, ends[:-1]))).reshape(-1, 3)
    except Exception:
        return np.empty((0, 3), dtype=np.int64)


def cells_cut(xy, ends):
    """earcut_cut, and a polygon of more than Geometry.TRIANGULATE_CELL_POINTS points strip by strip:
    the polygon gets a point wherever an edge crosses a strip edge (kese/core/cells.py), every strip
    is cut on its own (a strip earcut gets wrong by Manifold's triangulator), and the points the
    strips added are taken out again (without()), so the walls keep exactly the polygon's own
    edges.  No triangles when that fails: the polygon is then cut whole."""
    xs = cell_lines(xy[:, 0].min(), xy[:, 0].max()) if len(xy) > P.Geometry.TRIANGULATE_CELL_POINTS else []
    if not len(xs):
        return earcut_cut(xy, ends)
    nothing = np.empty((0, 3), dtype=np.int64)
    rings = np.split(xy, ends[:-1])
    whole = crossed(np.array([shapely.Polygon(rings[0], rings[1:])], dtype=object), xs, [])
    wxy, nxt, _, _, repeated = rings_of(whole)
    if repeated.any():
        return nothing
    y0, y1 = xy[:, 1].min() - 1, xy[:, 1].max() + 1
    strips = np.array([p for a, b in zip(np.r_[xy[:, 0].min() - 1, xs], np.r_[xs, xy[:, 0].max() + 1])
                       for p in shapely.get_parts(polys_only(shapely.clip_by_rect(whole[0], a, y0, b, y1)))], dtype=object)
    out = []
    for cut in (earcut_cut, manifold_cut):
        if len(strips):
            sxy, _, poly, tri, bad = caps(strips, cut)
            at = lookup(wxy, sxy)
            if at is None:
                return nothing
            out.append(at[tri[~bad[poly[tri[:, 0]]]]])
            strips = strips[np.flatnonzero(bad)]
    at = lookup(xy, wxy, missing=True)
    tri = without(np.concatenate(out), wxy, nxt, np.flatnonzero(at < 0)) if not len(strips) else None
    return nothing if tri is None else at[tri]


def lookup(xy, pts, missing=False):
    """The index in xy of every point of pts; None if one is not there (or -1 with missing=True)."""
    key = xy[:, 0] + 1j * xy[:, 1]
    order = np.argsort(key)
    k = pts[:, 0] + 1j * pts[:, 1]
    at = order[np.minimum(np.searchsorted(key[order], k), len(key) - 1)]
    found = key[at] == k
    if missing:
        return np.where(found, at, -1)
    return at if found.all() else None


def without(tri, xy, nxt, extra):
    """The triangles (counter-clockwise, of a polygon whose rings run along nxt) with the points extra
    taken out: every such point lies on an edge of the polygon, between its ring neighbours a and b,
    so the fan of triangles around it is the polygon a, b and the points around it, cut anew.  None
    when a fan is not whole."""
    prv = np.empty_like(nxt)
    prv[nxt] = np.arange(len(nxt))
    nxt = nxt.copy()
    is_extra = np.zeros(len(xy), dtype=bool)
    is_extra[extra] = True
    live, at = {}, defaultdict(set)              # the triangles at an extra point, by number
    for k in np.flatnonzero(is_extra[tri].any(axis=1)).tolist():
        live[k] = tri[k].tolist()
        for v in live[k]:
            if is_extra[v]:
                at[v].add(k)
    keep, count = np.ones(len(tri), dtype=bool), len(tri)
    for c in extra.tolist():
        fan = {}
        for k in at.pop(c, ()):
            u, v, w = live.pop(k)
            p, q = (v, w) if u == c else (w, u) if v == c else (u, v)     # the triangle c, p, q
            fan[p] = q
            for x in (u, v, w):
                if x != c and is_extra[x]:
                    at[x].discard(k)
            if k < len(tri):
                keep[k] = False
        a, b = int(prv[c]), int(nxt[c])
        ring = [a, b]
        while ring[-1] != a and ring[-1] in fan:
            ring.append(fan.pop(ring[-1]))
        if ring.pop() != a or fan:
            return None
        pts = xy[ring]                           # a, b and the points around c; only a, b if its fan is the flat a, c, b
        new = earcut_cut(pts, np.array([len(ring)])) if len(ring) > 2 else np.empty((0, 3), dtype=np.int64)
        if len(new) != len(ring) - 2:
            return None
        if twice_area(pts, new).sum() < 0:
            new = new[:, ::-1]
        for t in np.asarray(ring)[new].tolist():
            live[count] = t
            for x in t:
                if is_extra[x]:
                    at[x].add(count)
            count += 1
        nxt[a], prv[b] = b, a
    rest = [t for k, t in live.items() if k >= len(tri)]
    return np.concatenate([tri[keep], np.array(rest, dtype=np.int64).reshape(-1, 3)])
