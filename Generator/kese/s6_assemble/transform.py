"""Output units and orientation, and the clean-up every mesh gets before it is written."""
import numpy as np
import trimesh

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
    # merge vertices two decades below the snap grid, then drop only faces that collapsed onto a
    # repeated vertex (zero-area triangles with three distinct vertices stay: the union needs them)
    digits = int(round(-np.log10(P.Geometry.SNAP_GRID_MM))) + 2
    mesh.merge_vertices(digits_vertex=digits)
    f = mesh.faces
    mesh.update_faces((f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2]))
    mesh.remove_unreferenced_vertices()
    if not len(mesh.faces):
        return None
    mesh.apply_transform(mat)
    mesh = trimesh.graph.smooth_shade(mesh, angle=np.radians(P.Run.SMOOTH_SHADE_ANGLE_DEG))
    normals = np.array(mesh.vertex_normals)
    bad = np.linalg.norm(normals, axis=1) < 0.5
    if bad.any():
        normals[bad] = [0.0, 0.0, 1.0]
        mesh.vertex_normals = normals
    return mesh
