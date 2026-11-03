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
from kese.core.mesh import Mesh
from kese.core.parallel import workers_wanted
from parameters import P


def skin_meshes_from_faces(levels, pieces, faces):
    """-> {part: mesh of its visible faces} (mm, board frame)."""
    at = {z: k for k, z in enumerate(levels)}
    made, owners, parts = [], [], []
    for part, (flats, walls) in faces.items():
        mine = [flat_face_triangles(region, at[z], up) for z, region, up in flats]
        mine += [wall_triangles(segments, at[z0], at[z1]) for z0, z1, segments in walls]
        mine = [piece for piece in mine if len(piece[2])]
        made += mine
        owners += [np.full(len(tri), len(parts)) for _, _, tri in mine]
        parts.append(part)
    if not made:
        return {}
    v, f = mesh_with_shared_vertices(made, levels)
    owner = np.concatenate(owners)
    keep = ~looks_at_material(v, f, levels, pieces)
    f, owner = f[keep], owner[keep]
    keep = ~sealed(v, f)
    return meshes_per_part(v, f[keep], owner[keep], parts)


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


PROBES_AT_A_TIME = 2_000_000     # triangles: their probe points and normals take a quarter of a gigabyte


def looks_at_material(v, f, levels, pieces):
    """Which triangles have material just in front of them: a point SKIN_BURIED_TEST_OFFSET_MM out along
    the normal lies in some part's material.  Slices Run.WORKERS at a time, PROBES_AT_A_TIME probes."""
    inside = np.zeros(len(f), dtype=bool)
    with ThreadPoolExecutor(workers_wanted()) as pool:
        for start in range(0, len(f), PROBES_AT_A_TIME):
            these = slice(start, start + PROBES_AT_A_TIME)
            probe = probes_of(v, f[these])
            at = np.searchsorted(levels, probe[:, 2], "right") - 1        # the slice each probe's height falls in
            with_material = [k for k in np.unique(at).tolist() if 0 <= k < len(pieces) and not pieces[k][3].is_empty]
            list(pool.map(partial(place_in_slice, pieces, at, probe, inside[these]), with_material))
    return inside


def probes_of(v, f):
    """A point SKIN_BURIED_TEST_OFFSET_MM out from the centre of each triangle, along its normal."""
    a, b, c = v[f[:, 0]], v[f[:, 1]], v[f[:, 2]]
    normal = np.cross(b - a, c - a)
    normal /= np.maximum(np.linalg.norm(normal, axis=1, keepdims=True), 1e-300)
    return (a + b + c) / 3 + normal * P.Geometry.SKIN_BURIED_TEST_OFFSET_MM


def place_in_slice(pieces, at, probe, inside, k):
    """inside[...] = whether each probe that falls in slice k lies in the slice's material."""
    joined = pieces[k][3]
    shapely.prepare(joined)
    rows = np.flatnonzero(at == k)
    inside[rows] = shapely.contains_xy(joined, probe[rows, 0], probe[rows, 1])


def sealed(v, f):
    """Which faces belong to a closed shell that faces inward: the wall of a hollow inside the
    material, out of sight from every side."""
    if not len(f):
        return np.zeros(0, dtype=bool)
    edges = np.concatenate([f[:, :2], f[:, 1:]])
    _, shell = connected_components(len(v), edges[:, 0], edges[:, 1])
    shell = shell[f[:, 0]]
    o = (v.min(axis=0) + v.max(axis=0)) / 2
    a, b, c = v[f[:, 0]] - o, v[f[:, 1]] - o, v[f[:, 2]] - o
    volume = np.bincount(shell, weights=np.einsum("ij,ij->i", a, np.cross(b, c)))
    return volume[shell] < 0
