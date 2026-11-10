"""Triangles of zero area, which earcut makes where a ring has a point on a straight run, flipped
away (kese/core/triangulate.py), and those GEOS makes split away (flats_split_away);
the signed area every triangle check uses; and triangles that GEOS gives by their corners found
among a polygon's points."""
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


def flat_any(xy, tri):
    """Whether any triangle has no area (three points on one line), or runs clockwise."""
    twice = twice_area(xy, tri)
    return bool(len(tri) and (twice <= 1e-12 * (np.diff(xy[tri], axis=1) ** 2).sum(axis=(1, 2))).any())



def flats_split_away(xy, nxt, tri):
    """The triangles (counter-clockwise, into the rings' points xy; nxt: each point's next on its
    ring) without those of no area, the triangles beside them split at the points the flat ones
    had on their edges, so every edge inside is met once each way again; `tri` itself if that
    does not close (GEOS has given flat triangles on points of different rings that happen to lie
    on one line, stacked two deep, which no edge flip undoes)."""
    twice = twice_area(xy, tri)
    flat = twice <= 1e-12 * (np.diff(xy[tri], axis=1) ** 2).sum(axis=(1, 2))
    pts = np.unique(tri[flat])
    ring = set(zip(range(len(nxt)), nxt.tolist()))
    todo = [tuple(t) for t in tri[~flat].tolist()]
    have = {(t[i], t[(i + 1) % 3]) for t in todo for i in range(3)}
    out = []
    while todo:
        t = todo.pop()
        for i in range(3):
            u, v, w = t[i], t[(i + 1) % 3], t[(i + 2) % 3]
            if (v, u) in have or (u, v) in ring:
                continue
            on = [p for p in pts.tolist() if p not in t and on_segment(xy[u], xy[v], xy[p])]
            if on:
                on.sort(key=lambda p: np.dot(xy[p] - xy[u], xy[v] - xy[u]))
                chain = [u, *on, v]
                fan = [(a, b, w) for a, b in zip(chain[:-1], chain[1:])]
                have |= {(a, b) for a, b, _ in fan} | {(b, w) for _, b, _ in fan} | {(w, a) for a, _, _ in fan}
                todo += fan
                break
        else:
            out.append(t)
    done = np.array(out, dtype=np.int64).reshape(-1, 3)
    e = {(t[i], t[(i + 1) % 3]) for t in out for i in range(3)}
    closes = all((v, u) in e or (u, v) in ring for u, v in e) and ring <= e
    return done if closes and not flat_any(xy, done) else tri


def on_segment(a, b, p):
    """Whether p lies on the segment a b, strictly between its ends (three points on one line)."""
    d = b - a
    cross = d[0] * (p[1] - a[1]) - d[1] * (p[0] - a[0])
    t = np.dot(p - a, d)
    return abs(cross) <= 1e-12 * np.dot(d, d) and 0 < t < np.dot(d, d)
