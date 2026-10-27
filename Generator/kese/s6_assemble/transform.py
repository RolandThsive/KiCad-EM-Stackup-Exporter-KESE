"""Output units and orientation, and the clean-up every mesh gets before it is written."""
import numpy as np
import trimesh
from trimesh import tol
from trimesh.graph import connected_component_labels

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


def finish_mesh(mesh, mat, merged=False):
    """The mesh in output units and orientation, shaded smooth.  Vertices within two decades of
    the snap grid of each other are merged first, unless `merged` says the mesh has every vertex
    once already (one built from faces that share their vertices, kese/core/boundary_mesh.py);
    then only the faces that collapsed onto a repeated vertex go (zero-area triangles with three
    distinct vertices stay: the union needs them)."""
    if not merged:
        mesh.merge_vertices(digits_vertex=int(round(-np.log10(P.Geometry.SNAP_GRID_MM))) + 2)
    f = mesh.faces
    mesh.update_faces((f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2]))
    mesh.remove_unreferenced_vertices()
    if not len(mesh.faces):
        return None
    mesh.apply_transform(mat)
    v, f, normals = smooth_shaded(mesh, np.radians(P.Run.SMOOTH_SHADE_ANGLE_DEG))
    # a fresh mesh with only its normals: what the shading left cached on the old one is three
    # times the mesh itself
    return trimesh.Trimesh(v, f, vertex_normals=normals, process=False)


def smooth_shaded(mesh, angle):
    """(vertices, faces, vertex normals) of the mesh shaded as trimesh.graph.smooth_shade() shades
    it, without its loop over every group of faces.  The faces fall into groups joined across the
    edges flatter than angle, a flat facet of more than a tenth of the mesh's area being a group of
    its own (trimesh's facets); every group gets its own copy of its vertices, and every vertex the
    angle-weighted mean normal of its group's faces around it, or [0, 0, 1] where they have none."""
    faces, normals = mesh.faces, mesh.face_normals
    pairs, turn = mesh.face_adjacency, mesh.face_adjacency_angles
    smooth = pairs[turn < angle]
    big = np.zeros(len(faces), dtype=bool)
    if len(pairs):
        # flat as trimesh.graph.facets() has it: (radius / span) ** 2 > tol.facet_threshold, with
        # radius = span / (2 sin(turn)) and infinite below a turn of 0.01 degrees (it also takes two
        # faces of no area as flat, but they never make a facet big)
        flat =(turn <= np.radians(0.01)) | (2 * np.abs(np.sin(turn)) < 1 / np.sqrt(tol.facet_threshold))
        facet = connected_component_labels(pairs[flat], node_count=len(faces))
        big = ((np.bincount(facet) > 1) & (np.bincount(facet, weights=mesh.area_faces) > mesh.area / 10))[facet]
        smooth = smooth[~big[smooth].any(axis=1)]
    group = connected_component_labels(smooth, node_count=len(faces)).astype(np.int64)
    if big.any():
        group = np.where(big, group.max() + 1 + facet, group)
    n = len(mesh.vertices)
    key, corner = np.unique(group[:, None] * n + faces, return_inverse=True)
    corner = corner.reshape(-1, 3)
    ok = (normals ** 2).sum(axis=1) > 0.5                # faces of no area have no normal
    at, w = corner[ok].ravel(), mesh.face_angles[ok].ravel()
    summed = np.stack([np.bincount(at, weights=w * np.repeat(normals[ok, k], 3), minlength=len(key))
                       for k in range(3)], axis=1)
    out = trimesh.util.unitize(summed)
    out[np.linalg.norm(out, axis=1) < 0.5] = [0.0, 0.0, 1.0]
    return mesh.vertices[key % n], corner, out
