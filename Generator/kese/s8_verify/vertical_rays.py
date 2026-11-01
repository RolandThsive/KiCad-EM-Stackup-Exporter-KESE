"""Vertical rays through a triangle mesh, in numpy: which triangles a ray straight down crosses, and
at what height.  The Verifier's visual check casts only vertical rays, so a point-in-triangle test
in the plane does it; the rays are binned on a grid so each triangle meets only the rays near it."""
import numpy as np

TRIANGLES_AT_A_TIME = 200_000


def vertical_hits(vertices, faces, xy):
    """(ray index, z, triangle index) of every crossing of the rays through the points xy, going
    straight down, with the triangles (vertices[faces]).  A ray on an edge or vertex counts on each
    triangle it touches there."""
    xy = np.asarray(xy, dtype=float)
    tri = np.asarray(vertices, dtype=float)[np.asarray(faces)]
    lo, hi = xy.min(axis=0), xy.max(axis=0)
    cells = max(1, int(np.sqrt(len(xy))))
    size = np.maximum((hi - lo) / cells, 1e-12)
    cell = np.minimum(((xy - lo) / size).astype(np.int64), cells - 1)
    key = cell[:, 0] * cells + cell[:, 1]
    order = np.argsort(key, kind="stable")
    start = np.searchsorted(key[order], np.arange(cells * cells + 1))
    out = [], [], []
    for a in range(0, len(tri), TRIANGLES_AT_A_TIME):
        t = tri[a:a + TRIANGLES_AT_A_TIME]
        c0 = np.clip(((t[:, :, :2].min(axis=1) - lo) / size).astype(np.int64), 0, cells - 1)
        c1 = np.clip(((t[:, :, :2].max(axis=1) - lo) / size).astype(np.int64), 0, cells - 1)
        ok = (t[:, :, :2].max(axis=1) >= lo).all(axis=1) & (t[:, :, :2].min(axis=1) <= hi).all(axis=1)
        nx, ny = c1[:, 0] - c0[:, 0] + 1, c1[:, 1] - c0[:, 1] + 1
        n = np.where(ok, nx * ny, 0)
        which = np.repeat(np.arange(len(t)), n)                       # one row per (triangle, cell)
        k = np.arange(n.sum()) - np.repeat(np.cumsum(n) - n, n)
        cx = c0[which, 0] + k // ny[which]
        cy = c0[which, 1] + k % ny[which]
        ck = cx * cells + cy
        m = start[ck + 1] - start[ck]
        tri_i = np.repeat(which, m)                                   # one row per (triangle, ray)
        j = np.arange(m.sum()) - np.repeat(np.cumsum(m) - m, m)
        ray = order[np.repeat(start[ck], m) + j]
        p, q = xy[ray], t[tri_i]
        a_, b_, c_ = q[:, 0], q[:, 1], q[:, 2]
        d = (b_[:, 0] - a_[:, 0]) * (c_[:, 1] - a_[:, 1]) - (b_[:, 1] - a_[:, 1]) * (c_[:, 0] - a_[:, 0])
        good = d != 0
        with np.errstate(divide="ignore", invalid="ignore"):
            u = ((b_[:, 0] - p[:, 0]) * (c_[:, 1] - p[:, 1]) - (b_[:, 1] - p[:, 1]) * (c_[:, 0] - p[:, 0])) / d
            v = ((c_[:, 0] - p[:, 0]) * (a_[:, 1] - p[:, 1]) - (c_[:, 1] - p[:, 1]) * (a_[:, 0] - p[:, 0])) / d
        w = 1 - u - v
        inside = good & (u >= 0) & (v >= 0) & (w >= 0)
        z = u * a_[:, 2] + v * b_[:, 2] + w * c_[:, 2]
        out[0].append(ray[inside])
        out[1].append(z[inside])
        out[2].append(tri_i[inside] + a)
    kinds = (np.int64, float, np.int64)
    return tuple(np.concatenate(o).astype(k) if o else np.zeros(0, k) for o, k in zip(out, kinds))
