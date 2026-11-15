"""Output units and orientation, and the clean-up every mesh gets before it is written."""
import numpy as np
from kese.core.graph import connected_components
from kese.core.mesh import Mesh
from kese.core.mesh_math import unitize
from parameters import P


def output_transform():
    """4x4: board frame (mm, Y up, F.Cu toward +Z) -> output units and orientation."""
    R = P.Run
    scale = 1.0 if R.UNITS == "mm" else 0.001
    if R.ORIENTATION == "flat":      # board in XZ, F.Cu toward +Y
        rot = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], dtype=float)
    else:
        rot = np.eye(4)
    return np.diag([scale, scale, scale, 1.0]) @ rot


def finish_mesh(mesh, mat):
    """The mesh in output units and orientation, shaded smooth; the faces that collapsed onto a
    repeated vertex go (zero-area triangles with three distinct vertices stay).  None for no mesh."""
    if mesh is None:
        return None
    f = mesh.faces
    mesh.update_faces((f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2]))
    mesh.remove_unreferenced_vertices()
    if not len(mesh.faces):
        return None
    mesh.apply_transform(mat)
    v, f, normals = smooth_shaded(mesh, np.radians(P.Mesh.SMOOTH_SHADE_ANGLE_DEG))
    # a fresh mesh with only its normals: what the shading left cached on the old one is three
    # times the mesh itself
    return Mesh(v, f, vertex_normals=normals)


def smooth_shaded(mesh, angle):
    """(vertices, faces, vertex normals) shaded as trimesh's smooth_shade(): faces grouped across edges
    flatter than angle (big flat facets on their own), each group's vertices copied and given the
    angle-weighted mean normal of its faces, or [0, 0, 1]."""
    faces, normals = mesh.faces, mesh.face_normals
    pairs, turn = mesh.face_adjacency, mesh.face_adjacency_angles
    smooth = pairs[turn < angle]
    big = np.zeros(len(faces), dtype=bool)
    if len(pairs):
        # flat as trimesh.graph.facets() has it: (radius / span) ** 2 > Geometry.FLAT_FACET_THRESHOLD, with
        # radius = span / (2 sin(turn)) and infinite below a turn of 0.01 degrees (it also takes two
        # faces of no area as flat, but they never make a facet big)
        flat = (turn <= np.radians(0.01)) | (2 * np.abs(np.sin(turn)) < 1 / np.sqrt(P.Geometry.FLAT_FACET_THRESHOLD))
        facet = connected_components(len(faces), *pairs[flat].T)[1]
        least = mesh.area / P.Geometry.SMOOTH_FACET_AREA_DIVISOR
        big = ((np.bincount(facet) > 1) & (np.bincount(facet, weights=mesh.area_faces) > least))[facet]
        smooth = smooth[~big[smooth].any(axis=1)]
    group = connected_components(len(faces), *smooth.T)[1].astype(np.int64)
    if big.any():
        group = np.where(big, group.max() + 1 + facet, group)
    n = len(mesh.vertices)
    key, corner = np.unique(group[:, None] * n + faces, return_inverse=True)
    corner = corner.reshape(-1, 3)
    ok = (normals ** 2).sum(axis=1) > 0.5                # faces of no area have no normal
    at, w = corner[ok].ravel(), mesh.face_angles[ok].ravel()
    summed = np.stack([np.bincount(at, weights=w * np.repeat(normals[ok, k], 3), minlength=len(key))
                       for k in range(3)], axis=1)
    out = unitize(summed)
    out[np.linalg.norm(out, axis=1) < 0.5] = [0.0, 0.0, 1.0]
    return mesh.vertices[key % n], corner, out
