"""The visible faces of every part as meshes, vertices shared across parts; then the triangles that
look at material within Geometry.SKIN_BURIED_TEST_OFFSET_MM, and those of hollows sealed inside
the board, go."""
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import numpy as np
import shapely

from kese.core.boundary_mesh import (
    flat_face_triangles,
    mesh_with_shared_vertices,
    wall_triangles,
)
from kese.core.graph import connected_components
from kese.core.tall_walls import tall_walls
from kese.core.mesh import Mesh
from kese.core.memory import give_back_memory
from kese.core.parallel import workers_wanted
from kese.core.shape_copies import floating
from parameters import P


def skin_meshes_from_faces(levels, pieces, faces, free):
    """-> {part: mesh of its visible faces} (mm, board frame); across the heights in `free`
    (PrismSet.free_levels) a wall that goes on unchanged is one taller wall (kese/core/tall_walls.py)."""
    at = {z: k for k, z in enumerate(levels)}
    names = list(faces)
    walls_of = {part: faces[part][1] for part in names}
    if free:
        every = [(z0, z1, s) for part in names for z0, z1, s in faces[part][1]]
        owner = [np.full(len(s), n) for n, part in enumerate(names) for *_, s in faces[part][1]]
        flats = [f for part in names for f in faces[part][0]]
        walls_of = {part: [] for part in names}
        for z0, z1, s, o in tall_walls(every, flats, levels, free, owner):
            for n in np.unique(o):
                walls_of[names[n]].append((z0, z1, s[o == n]))
    made, owners = [], []
    for n, part in enumerate(names):
        mine = [flat_face_triangles(region, at[z], up) for z, region, up in faces[part][0]]
        mine += [wall_triangles(segments, at[z0], at[z1]) for z0, z1, segments in walls_of[part]]
        mine = [piece for piece in mine if len(piece[2])]
        made += mine
        owners += [np.full(len(tri), n) for _, _, tri in mine]
    if not made:
        return {}
    v, f = mesh_with_shared_vertices(made, levels)
    owner = np.concatenate(owners)
    keep = ~looks_at_material(v, f, levels, pieces)
    f, owner = f[keep], owner[keep]
    keep = ~sealed(v, f)
    return meshes_per_part(v, f[keep], owner[keep], names)


def meshes_per_part(v, f, owner, parts):
    """{part: a mesh of the triangles it owns}: the triangles sorted by owner once, in their
    order, not searched through once per part."""
    order = np.argsort(owner, kind="stable")
    first = np.searchsorted(owner[order], np.arange(len(parts) + 1))
    out = {}
    for k, part in enumerate(parts):
        mine = f[order[first[k]:first[k + 1]]]
        if len(mine):
            used, faces_of = np.unique(mine, return_inverse=True)
            out[part] = Mesh(v[used], faces_of.reshape(-1, 3))
    return out


def looks_at_material(v, f, levels, pieces):
    """Which triangles have material just in front of them: a point SKIN_BURIED_TEST_OFFSET_MM out along
    the normal lies in some part's material.  Parallel.SKIN_PROBES_AT_A_TIME probes at a time, each
    slice's in shares of at least Parallel.SKIN_PROBES_PER_SHARE, Parallel.WORKERS shares at a time."""
    inside = np.zeros(len(f), dtype=bool)
    workers = workers_wanted()
    with ThreadPoolExecutor(workers) as pool:
        step = P.Parallel.SKIN_PROBES_AT_A_TIME
        for start in range(0, len(f), step):
            these = slice(start, start + step)
            probe = probes_of(v, f[these])
            at = np.searchsorted(levels, probe[:, 2], "right") - 1        # the slice each probe's height falls in
            list(pool.map(partial(place_in_slice, pieces, probe, inside[these]), probe_shares(pieces, at, workers)))
    for *_, joined, _ in pieces:
        shapely.destroy_prepared(joined)        # the indexes place_in_slice built: not needed after this
    give_back_memory()
    return inside


def probe_shares(pieces, at, workers):
    """(slice, rows, whether the slice's first share) for the probes that fall in a slice with material:
    each slice's rows in up to `workers` shares of at least Parallel.SKIN_PROBES_PER_SHARE, the biggest
    shares first.  A slice can take far longer a probe than the others (on NE_Delta, the core with
    every via hole in it: 20 times as long, 11 of the 13 s on one thread while the rest were done)."""
    shares = []
    for k in np.unique(at).tolist():
        if 0 <= k < len(pieces) and not pieces[k][3].is_empty:
            rows = np.flatnonzero(at == k)
            n = max(1, min(workers, len(rows) // P.Parallel.SKIN_PROBES_PER_SHARE))
            shares += [(k, part, i == 0) for i, part in enumerate(np.array_split(rows, n))]
    return sorted(shares, key=lambda share: -len(share[1]))


def probes_of(v, f):
    """A point SKIN_BURIED_TEST_OFFSET_MM out from the centre of each triangle, along its normal."""
    a, b, c = v[f[:, 0]], v[f[:, 1]], v[f[:, 2]]
    normal = np.cross(b - a, c - a)
    normal /= np.maximum(np.linalg.norm(normal, axis=1, keepdims=True), 1e-300)
    return (a + b + c) / 3 + normal * P.Geometry.SKIN_BURIED_TEST_OFFSET_MM


def place_in_slice(pieces, probe, inside, share):
    """inside[rows] = whether each probe of a share (slice k, rows, first) lies in the slice's material.
    A prepared shape serves one thread at a time: the slice's first share prepares the slice itself,
    kept prepared for the next batch of probes, and every other share a copy of its own."""
    k, rows, first = share
    joined = pieces[k][3] if first else floating([pieces[k][3]])[0]
    shapely.prepare(joined)
    inside[rows] = shapely.contains_xy(joined, probe[rows, 0], probe[rows, 1])


def sealed(v, f):
    """Which faces are out of sight from every side: those of a closed shell that faces inward (the
    wall of a hollow inside the material), and those of a piece that lies flat at one height, with no
    wall.  Such a piece is the top or the bottom of a gap thinner than vertices.near_edge() inside the
    material: where stage 6 moved a slice's edge onto a vertex of the slice above or below (the
    vertex lay that near it), the walls of the gap are hidden (walls_split_at_vertices takes the
    vertex as on the edge beside it), and its faces were left on their own."""
    if not len(f):
        return np.zeros(0, dtype=bool)
    edges = np.concatenate([f[:, :2], f[:, 1:]])
    _, shell = connected_components(len(v), edges[:, 0], edges[:, 1])
    shell = shell[f[:, 0]]
    o = (v.min(axis=0) + v.max(axis=0)) / 2
    a, b, c = v[f[:, 0]] - o, v[f[:, 1]] - o, v[f[:, 2]] - o
    volume = np.bincount(shell, weights=np.einsum("ij,ij->i", a, np.cross(b, c)))
    z = v[f, 2]
    low, high = np.full(len(volume), np.inf), np.full(len(volume), -np.inf)
    np.minimum.at(low, shell, z.min(axis=1))
    np.maximum.at(high, shell, z.max(axis=1))
    return (volume[shell] < 0) | (low[shell] == high[shell])
