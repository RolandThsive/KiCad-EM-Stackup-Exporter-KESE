"""Triangles of zero area, which earcut makes where a ring has a point on a straight run, flipped
away (kese/core/triangulate.py); the signed area every triangle check uses; and triangles that GEOS
gives by their corners found among a polygon's points."""
import numpy as np


def flip_flat(xy, tri, twice, size):
    """The triangles with every flat one (three points on one line, as earcut makes) taken out by
    flipping the edge it lies on; the area and the ring edges stay as they are."""
    flat = np.flatnonzero(np.abs(twice) <= 1e-12 * size)
    if not len(flat):
        return tri, twice
    tri = tri.copy()
    for k in flat.tolist():
        t = tri[k]
        p = xy[t]
        long = [np.sum((p[(i + 2) % 3] - p[(i + 1) % 3]) ** 2) for i in range(3)]     # the edge facing each point
        i = int(np.argmax(long))
        b, z, x = int(t[i]), int(t[(i + 1) % 3]), int(t[(i + 2) % 3])          # runs x, b, z: long edge z -> x
        e0, e1, e2 = tri[:, 0], tri[:, 1], tri[:, 2]
        hit = np.flatnonzero(((e0 == x) & (e1 == z)) | ((e1 == x) & (e2 == z)) | ((e2 == x) & (e0 == z)))
        hit = [h for h in hit.tolist() if h != k]
        if len(hit) != 1 or long[i] == 0:
            continue
        h = hit[0]
        d = int(next(v for v in tri[h].tolist() if v not in (x, z)))
        new = np.array([[x, b, d], [b, z, d]])
        area = twice_area(xy, new)
        if (area <= 0).any():
            continue
        tri[h], tri[k] = new
        twice[h], twice[k] = area
    return tri, twice


def twice_area(xy, tri):
    """Twice the signed area of every triangle, positive when it runs counter-clockwise."""
    a, b, c = xy[tri[:, 0]], xy[tri[:, 1]], xy[tri[:, 2]]
    return (b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0])


def on_points(xy, corners):
    """Triangles given by their corners (k, 3, 2) as counter-clockwise triangles into xy; none when
    there are none, or a corner is not one of xy's points."""
    at = lookup(xy, corners.reshape(-1, 2)) if len(corners) else None
    if at is None:
        return np.empty((0, 3), dtype=np.int64)
    tri = at.reshape(-1, 3)
    turn = twice_area(xy, tri) < 0
    tri[turn] = tri[turn][:, ::-1]
    return tri


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
