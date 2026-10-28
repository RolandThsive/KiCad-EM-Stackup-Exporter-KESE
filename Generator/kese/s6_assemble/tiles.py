"""The visible skin of a big board is joined in tiles, one after another, as KiCad cuts big polygons
into a grid of cells before it triangulates them: one union of a whole dense board would need many
GB at once.  The tile edges lie halfway between two points of the snap grid, where no outline
vertex is, and every outline edge that crosses one gets its crossing point first, the same point
for every region that has the edge (kese/core/cells.py); so the tiles meet in exactly the same
vertices, and the faces that only close a tile are left out."""
from collections import defaultdict

import manifold3d as mf
import numpy as np
import shapely

from kese.core.extrude import extrude
from kese.core.shapes2d import grid, polys_only
from parameters import P


def tile_edges(prisms):
    """The x and y of the tile edges inside the board, each halfway between two grid points: as
    many tiles as Geometry.SKIN_TILE_POINTS asks for, about square."""
    count = sum(shapely.get_num_coordinates(p.region) for p in prisms)
    tiles = int(np.ceil(count / P.Geometry.SKIN_TILE_POINTS))
    if tiles <= 1:
        return np.empty(0), np.empty(0)
    b = np.array([p.region.bounds for p in prisms])
    x0, y0, x1, y1 = b[:, 0].min(), b[:, 1].min(), b[:, 2].max(), b[:, 3].max()
    nx = max(1, int(round(np.sqrt(tiles * (x1 - x0) / max(y1 - y0, 1e-9)))))
    ny = max(1, int(np.ceil(tiles / nx)))
    g = grid()

    def edges(lo, hi, k):
        return np.unique((np.floor((lo + (hi - lo) * np.arange(1, k) / k) / g) + 0.5) * g)
    return edges(x0, x1, nx), edges(y0, y1, ny)


def tile_surface(prisms, regions, box, index, loose):
    """The surface of the union of the prisms inside one tile, less the faces that only close the
    tile: (vertices, faces, part index of every face).  Pieces that are not closed solids go to
    loose as they are."""
    x0, y0, x1, y1 = box
    clip = np.isfinite(box).any()
    solids, owner = [], {}
    for p, r in zip(prisms, regions):
        if clip:
            r = polys_only(shapely.clip_by_rect(r, *np.clip(box, -1e9, 1e9)))
        m = extrude(r, p.z0, p.z1)
        if m is None or not len(m.faces):
            continue
        s = mf.Manifold(mesh=mf.Mesh64(vert_properties=np.asarray(m.vertices, dtype=np.float64),
                                       tri_verts=np.asarray(m.faces, dtype=np.uint32)))
        if s.status() != mf.Error.NoError:
            loose.append((p.part, m))          # not a closed solid: only its hidden faces go
            continue
        s = s.as_original()
        owner[s.original_id()] = index[p.part]
        solids.append(s)
    if not solids:
        return np.empty((0, 3)), np.empty((0, 3), dtype=np.int64), np.empty(0, dtype=np.int64)
    out = mf.Manifold.batch_boolean(solids, mf.OpType.Add).to_mesh64()
    del solids
    v, f = np.array(out.vert_properties)[:, :3], np.array(out.tri_verts, dtype=np.int64)
    runs = np.diff(np.asarray(out.run_index)) // 3
    who = np.repeat([owner[o] for o in np.asarray(out.run_original_id).tolist()], runs)
    corners = v[f]
    cut = np.zeros(len(f), dtype=bool)
    for axis, edge in ((0, x0), (0, x1), (1, y0), (1, y1)):
        if np.isfinite(edge):
            cut |= (corners[:, :, axis] == edge).all(axis=1)
    return v, f[~cut], who[~cut]


def joined_tiles(v, f, owner, xs, ys):
    """The tiles' surfaces as one: a vertex on a tile edge is the same vertex in every tile, and
    where one tile has a vertex along a line on the cut that its neighbour joined away (two faces
    in one plane made one), the neighbour's edge is split at it."""
    on = np.isin(v[:, 0], xs) | np.isin(v[:, 1], ys)
    if not on.any():
        return v, f, owner
    at = np.flatnonzero(on)
    _, first, inverse = np.unique(v[at], axis=0, return_index=True, return_inverse=True)
    same = np.arange(len(v))
    same[at] = at[first][inverse.ravel()]
    f = same[f]
    for _ in range(4):
        f, owner, split = split_open_edges(v, f, owner)
        if not split:
            break
    return v, f, owner


def split_open_edges(v, f, owner):
    """Faces whose edge is used only once and passes through other open edges' vertices, split at
    them.  On a cut every such edge runs along x, y or z."""
    e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    face = np.tile(np.arange(len(f)), 3)
    opposite = np.concatenate([f[:, 2], f[:, 0], f[:, 1]])
    _, idx, count = np.unique(np.sort(e, axis=1), axis=0, return_inverse=True, return_counts=True)
    lone = np.flatnonzero(count[idx.ravel()] == 1)
    if not len(lone):
        return f, owner, 0
    ends = np.unique(e[lone])
    lines = {}
    for axis in range(3):                      # the vertices on each line along this axis
        other = [k for k in range(3) if k != axis]
        key = v[ends][:, other]
        order = np.lexsort((v[ends, axis], key[:, 1], key[:, 0]))
        lines[axis] = (key[order], v[ends[order], axis], ends[order])
    extra = defaultdict(list)                  # face -> [(edge start, edge end, vertices inside)]
    for k in lone.tolist():
        a, b = e[k]
        same = v[a] == v[b]
        if same.sum() != 2:
            continue
        axis = int(np.flatnonzero(~same)[0])
        keys, pos, ids = lines[axis]
        other = [i for i in range(3) if i != axis]
        target = v[a][other]
        lo = np.searchsorted(keys[:, 0], target[0], "left")
        hi = np.searchsorted(keys[:, 0], target[0], "right")
        sub = np.flatnonzero(keys[lo:hi, 1] == target[1]) + lo
        t0, t1 = v[a, axis], v[b, axis]
        inside = sub[(pos[sub] > min(t0, t1)) & (pos[sub] < max(t0, t1))]
        if len(inside):
            inside = inside[np.argsort(pos[inside] * (1 if t1 > t0 else -1))]
            extra[face[k]].append((a, b, ids[inside].tolist(), opposite[k]))
    if not extra:
        return f, owner, 0
    keep = np.ones(len(f), dtype=bool)
    new_f, new_o = [], []
    for fi, splits in extra.items():
        if len(splits) > 1:                    # two split edges on one face: one now, the other next round
            splits = splits[:1]
        a, b, mids, o = splits[0]
        chain = [a, *mids, b]
        keep[fi] = False
        new_f += [[chain[i], chain[i + 1], o] for i in range(len(chain) - 1)]
        new_o += [owner[fi]] * (len(chain) - 1)
    return np.concatenate([f[keep], np.array(new_f, dtype=np.int64)]), \
        np.concatenate([owner[keep], np.array(new_o, dtype=owner.dtype)]), len(extra)
