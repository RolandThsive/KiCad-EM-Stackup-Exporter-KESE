"""A coil's port in the 2.5D mesh: the sheet across the gap that opens it, and the copper faces either side.

The gap is a region of the model with no copper of the coil in it (the space between two trace ends, or a
via's barrel once the via is left out). The electrodes are the coil's copper faces that border the gap; they
fall into two separate groups, one each side, and finding exactly two proves the gap opens the coil into one
conductor. The sheet is a set of faces inside the gap that joins the two electrodes: Palace's lumped port, a
surface with a resistance across it whose voltage, along the sheet from one electrode to the other, is the coil's
(see palace_case.py).
"""
from __future__ import annotations

import numpy as np
import shapely

from . import mesh25d as M


def _groups(faces_list):
    """Split faces (lists of node-index arrays) into groups that share nodes. Returns a label per face."""
    n = len(faces_list)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    owner = {}
    for i, f in enumerate(faces_list):
        for v in f:
            v = int(v)
            if v in owner:
                a, b = find(i), find(owner[v])
                if a != b:
                    parent[a] = b
            else:
                owner[v] = i
    roots = [find(i) for i in range(n)]
    uniq = {r: k for k, r in enumerate(dict.fromkeys(roots))}
    return np.array([uniq[r] for r in roots], int)


def electrodes(m, body, gap, z0, z1, tol=1e-3):
    """The two electrodes of coil `body` (its index in m['names']) at a gap: the faces of its copper whose centre
    lies within tol (mm) of the gap region (a shapely polygon in xy) and between z0 and z1. Returns
    [(tris, tri parents, quads, quad parents), ...] for the two groups, ordered by the mean of (x, y, z)."""
    near = gap.buffer(tol)

    def sel(x, y, z):
        return shapely.contains_xy(near, x, y) & (z > z0 - tol) & (z < z1 + tol)
    (t, tp), (q, qp) = M.body_faces(m, [body], sel)
    faces = list(t) + list(q)
    if not faces:
        raise ValueError(f'no copper faces of {m["names"][body]} border the gap')
    lab = _groups(faces)
    nt = len(t)
    groups = sorted(set(lab.tolist()))
    if len(groups) != 2:
        raise ValueError(f'the copper of {m["names"][body]} borders the gap in {len(groups)} places, not 2: '
                         'the gap does not cut the coil into one open conductor')
    out = []
    for g in groups:
        kt = np.flatnonzero(lab[:nt] == g)
        kq = np.flatnonzero(lab[nt:] == g)
        out.append((t[kt], tp[kt], q[kq], qp[kq]))
    cen = [m['nodes'][np.vstack([f.reshape(-1, 1) for f in (e[0], e[2]) if len(f)]).ravel()].mean(axis=0)
           for e in out]
    order = sorted(range(2), key=lambda i: tuple(np.round(cen[i], 6)))
    return [out[i] for i in order]


def sheet_at_level(m, gap, z):
    """The port sheet as the horizontal faces at height z whose triangle centre lies in the gap region."""
    return M.level_faces(m, z, lambda x, y: shapely.contains_xy(gap, x, y))


def sheet_vertical(m, line, z0, z1):
    """The port sheet as the vertical faces between z0 and z1 along `line`, a shapely LineString that must be
    embedded in the triangle mesh (give it to build_mesh in extra_lines)."""
    return M.vertical_faces(m, z0, z1, line)


def facing_vertices(copper, region, axis=1, grid=0.0005, simplify=0.0005, tol=1e-6):
    """The port's line across a gap between two round trace ends: of the copper outline's vertices inside region
    (a shapely polygon), the pair on opposite sides of the region's middle that share their coordinate across
    `axis` (0: x, 1: y; the line runs along it) and lie closest together. A sheet along that line touches the
    copper exactly at both ends, which Palace's lumped port needs (its sheet must be a rectangle with its two ends
    on the conductors). The outline is taken as the mesher draws it (mesh25d.build_mesh: simplified by
    Settings.simplify and snapped to Settings.grid), so the two vertices are nodes of the mesh. Returns a shapely
    LineString."""
    from shapely.geometry import LineString
    geoms = getattr(copper, 'geoms', [copper])
    rings = [r.simplify(simplify) for g in geoms for r in [g.exterior, *g.interiors]]
    pts = np.round(np.vstack([np.asarray(r.coords) for r in rings]) / grid) * grid
    inside = shapely.contains_xy(region.buffer(tol), pts[:, 0], pts[:, 1])
    pts = np.unique(np.round(pts[inside], 7), axis=0)
    mid = region.centroid.coords[0][axis]
    lo, hi = pts[pts[:, axis] < mid], pts[pts[:, axis] > mid]
    best = None
    for p in lo:
        same = hi[np.abs(hi[:, 1 - axis] - p[1 - axis]) < tol]
        for q in same:
            d = q[axis] - p[axis]
            if best is None or d < best[0]:
                best = (d, p, q)
    if best is None:
        raise ValueError('no two copper vertices face each other across the gap')
    return LineString([tuple(best[1]), tuple(best[2])])
