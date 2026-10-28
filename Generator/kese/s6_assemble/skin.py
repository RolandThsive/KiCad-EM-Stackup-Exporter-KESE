"""The "visual" mode: the board's visible surface only.

Every prism is extruded on its own and all of them are joined in one exact boolean union (Manifold,
in double precision; on a big board tile by tile, see tiles.py): where two prisms meet their faces
cancel, and what is left is the surface between material and air.  Every triangle keeps the prism
it came from, so the surface is still split into named parts.  Two kinds of faces go as well: the
walls of a hollow sealed inside the board (the open bore of a buried via), which no one can see,
and a face that looks at another prism across less than Geometry.SKIN_BURIED_TEST_OFFSET_MM (two
pieces that meet but for rounding).  What is left is one outer surface, closed but for the mouths
of such hairline slits, so layers only microns apart no longer fight for the same pixels in web
viewers."""
from collections import defaultdict

import numpy as np
import shapely
import trimesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from kese.core.cells import split_at
from kese.s6_assemble.tiles import joined_tiles, tile_edges, tile_surface
from parameters import P

POINTS_PER_QUERY = 200_000


def skin_meshes(ps):
    """PrismSet -> {part name: trimesh of its visible faces} (mm, board frame)."""
    prisms = [p for p in ps.prisms if not p.region.is_empty]
    for p in prisms:
        shapely.prepare(p.region)
    parts = sorted({p.part for p in prisms})
    index = {part: i for i, part in enumerate(parts)}
    xs, ys = tile_edges(prisms)
    regions = [split_at(p.region, xs, ys) for p in prisms] if len(xs) or len(ys) else [p.region for p in prisms]
    boxes = np.array([r.bounds for r in regions])
    vs, fs, owners, loose, n = [], [], [], [], 0
    for x0, x1 in zip(np.r_[-np.inf, xs], np.r_[xs, np.inf]):
        for y0, y1 in zip(np.r_[-np.inf, ys], np.r_[ys, np.inf]):
            meet = np.flatnonzero((boxes[:, 0] < x1) & (boxes[:, 2] > x0) & (boxes[:, 1] < y1) & (boxes[:, 3] > y0))
            v, f, owner = tile_surface([prisms[i] for i in meet], [regions[i] for i in meet], (x0, y0, x1, y1),
                                       index, loose)
            vs.append(v)
            fs.append(f + n)
            owners.append(owner)
            n += len(v)
    v, f, owner = joined_tiles(np.concatenate(vs), np.concatenate(fs), np.concatenate(owners), xs, ys)
    seen = ~sealed(v, f)
    f, owner = f[seen], owner[seen]
    by = np.argsort(owner, kind="stable")
    cuts = np.flatnonzero(np.diff(owner[by])) + 1
    pieces = []
    for fi in np.split(by, cuts) if len(by) else []:
        used, faces = np.unique(f[fi], return_inverse=True)
        pieces.append((parts[owner[fi[0]]], trimesh.Trimesh(v[used], faces.reshape(-1, 3), process=False)))
    meshes = defaultdict(list)
    for part, m in pieces + loose:
        keep = ~buried(prisms, m.triangles_center + m.face_normals * P.Geometry.SKIN_BURIED_TEST_OFFSET_MM)
        if keep.any():
            m.update_faces(keep)
            m.remove_unreferenced_vertices()
            meshes[part].append(m)
    return {part: ms[0] if len(ms) == 1 else trimesh.util.concatenate(ms) for part, ms in meshes.items()}


def sealed(v, f):
    """Which faces belong to a closed shell that faces inward: the wall of a hollow inside the
    material, out of sight from every side."""
    if not len(f):
        return np.zeros(0, dtype=bool)
    edges = np.concatenate([f[:, :2], f[:, 1:]])
    graph = coo_matrix((np.ones(len(edges), dtype=bool), (edges[:, 0], edges[:, 1])), shape=(len(v), len(v)))
    _, shell = connected_components(graph, directed=False)
    shell = shell[f[:, 0]]
    o = (v.min(axis=0) + v.max(axis=0)) / 2
    a, b, c = v[f[:, 0]] - o, v[f[:, 1]] - o, v[f[:, 2]] - o
    volume = np.bincount(shell, weights=np.einsum("ij,ij->i", a, np.cross(b, c)))
    return volume[shell] < 0


def buried(prisms, points):
    """Which points lie inside a prism (strictly between its heights).  The prisms are taken in
    groups of equal heights, and a point is tested only against the prisms of its height whose
    box holds it."""
    hit = np.zeros(len(points), dtype=bool)
    order = np.argsort(points[:, 2], kind="stable")
    zs = points[order, 2]
    groups = defaultdict(list)
    for p in prisms:
        groups[(p.z0, p.z1)].append(p.region)
    for (z0, z1), regions in groups.items():
        span = order[np.searchsorted(zs, z0, "right"):np.searchsorted(zs, z1, "left")]
        tree = None
        for start in range(0, len(span), POINTS_PER_QUERY):
            idx = span[start:start + POINTS_PER_QUERY]
            idx = idx[~hit[idx]]
            if not len(idx):
                continue
            if tree is None:
                tree = shapely.STRtree(regions)
            pt, rg = tree.query(shapely.points(points[idx, :2]))
            if not len(pt):
                continue
            by = np.argsort(rg, kind="stable")
            pt, rg = pt[by], rg[by]
            cuts = np.flatnonzero(np.diff(rg)) + 1
            for sel, r in zip(np.split(pt, cuts), rg[np.r_[0, cuts]].tolist()):
                inside = shapely.contains_xy(regions[r], points[idx[sel], 0], points[idx[sel], 1])
                hit[idx[sel[inside]]] = True
    return hit
