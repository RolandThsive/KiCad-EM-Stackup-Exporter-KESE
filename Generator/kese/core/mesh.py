"""A triangle mesh: vertices (n, 3) float, faces (m, 3) int, and what the stages ask of it.

It does what trimesh's Trimesh did for KESE, the same way (kese/core/mesh_math.py has the
formulas), so the files come out byte for byte as before.  One habit of trimesh's is kept on
purpose: the face normals, once worked out, are kept while the vertices and faces stay the same
(by content), kept through update_faces(), and turned with the mesh by apply_transform() instead
of being worked out again."""
import numpy as np

from kese.core import mesh_math as mm
from parameters import P


class Mesh:
    def __init__(self, vertices, faces, vertex_normals=None, face_normals=None, merge=False):
        """merge: vertices that round to the same point at Geometry.MESH_MERGE_DIGITS made one."""
        self.vertices = np.asarray(vertices, dtype=np.float64, order="C").reshape((-1, 3))
        self.faces = np.asarray(faces, dtype=np.int64, order="C").reshape((-1, 3))
        self.vertex_normals = None
        if vertex_normals is not None:
            vn = np.asarray(vertex_normals, dtype=np.float64)
            self.vertex_normals = np.ascontiguousarray(vn) if vn.shape == self.vertices.shape else None
        self._normals, self._key = None, None
        if face_normals is not None:
            self._keep_normals(face_normals)
        if merge:
            self.merge_vertices()

    # ---- the face normals, kept while the mesh stays the same ----------------------------------
    def _content(self):
        return (self.vertices.shape, self.faces.shape, hash(self.vertices.tobytes()), hash(self.faces.tobytes()))

    def _cached_normals(self):
        return self._normals if self._normals is not None and self._key == self._content() else None

    def _keep_normals(self, values):
        values = np.asarray(values, dtype=np.float64)
        if not len(values) or values.shape != self.faces.shape:
            return
        spread = np.ptp(values)
        if not np.isfinite(spread) or spread < 10.0 ** -P.Geometry.MESH_MERGE_DIGITS:
            return
        t = self.vertices[self.faces[:20]]
        check = mm.face_normals(t, mm.crosses(t))
        if np.allclose(check, values[:20]):
            self._normals, self._key = np.ascontiguousarray(values), self._content()

    @property
    def face_normals(self):
        if not len(self.faces):
            return np.zeros((0, 3))
        kept = self._cached_normals()
        if kept is None:
            t = self.triangles
            kept = mm.face_normals(t, mm.crosses(t))
            self._normals, self._key = kept, self._content()
        return kept

    # ---- what is worked out of it ---------------------------------------------------------------
    @property
    def triangles(self):
        return self.vertices[self.faces]

    @property
    def triangles_center(self):
        return self.triangles.mean(axis=1)

    @property
    def area_faces(self):
        c = mm.crosses(self.triangles)
        return np.sqrt((c ** 2).sum(axis=1)) / 2.0

    @property
    def area(self):
        return self.area_faces.sum()

    @property
    def face_angles(self):
        return mm.angles(self.triangles, 10.0 ** -P.Geometry.MESH_MERGE_DIGITS)

    @property
    def face_adjacency(self):
        """(k, 2): the faces that share an edge, the lower first."""
        e, face = mm.edges(self.faces)
        pairs = face[mm.edge_pairs(np.sort(e, axis=1))]
        pairs = pairs[pairs[:, 0] != pairs[:, 1]]
        pairs.sort(axis=1)
        return pairs

    @property
    def face_adjacency_angles(self):
        n = self.face_normals[self.face_adjacency]
        return np.abs(np.arccos(np.clip(mm.diagonal_dot(n[:, 0], n[:, 1]), -1.0, 1.0)))

    def _closed(self):
        """(every edge in exactly two faces, every shared edge run opposite ways by its two faces)."""
        e = mm.edges(self.faces)[0]
        pairs = mm.edge_pairs(np.sort(e, axis=1))
        opposing = e[pairs].reshape((-1, 4))[:, 1:3].T
        return bool(len(pairs) * 2 == len(e)), bool(np.equal(*opposing).all())

    @property
    def is_watertight(self):
        return len(self.faces) > 0 and self._closed()[0]

    @property
    def is_winding_consistent(self):
        return len(self.faces) > 0 and self._closed()[1]

    @property
    def volume(self):
        t = self.triangles
        return mm.volume(t, mm.crosses(t))

    @property
    def bounds(self):
        used = self.vertices[np.unique(self.faces)] if len(self.faces) else self.vertices[:0]
        return np.array([used.min(axis=0), used.max(axis=0)]) if len(used) else None

    def copy(self):
        """The vertices and faces only (as trimesh's copy() leaves its cache behind)."""
        return Mesh(self.vertices.copy(), self.faces.copy())

    # ---- changes ---------------------------------------------------------------------------------
    def update_faces(self, mask):
        mask = np.asanyarray(mask)
        if not len(self.faces) or (mask.dtype == bool and mask.all()):
            return
        kept = self._cached_normals()
        self.faces = self.faces[mask]
        if kept is not None:
            self._keep_normals(kept[mask])

    def _update_vertices(self, mask, inverse):
        if not len(self.faces) or not len(mask) or (mask.dtype == bool and mask.all()):
            return
        self.faces = inverse[self.faces.reshape(-1)].reshape((-1, 3))
        self.vertices = self.vertices[mask]
        if self.vertex_normals is not None:
            self.vertex_normals = self.vertex_normals[mask]

    def remove_unreferenced_vertices(self):
        referenced = np.zeros(len(self.vertices), dtype=bool)
        referenced[self.faces] = True
        inverse = np.zeros(len(self.vertices), dtype=np.int64)
        inverse[referenced] = np.arange(referenced.sum())
        self._update_vertices(referenced, inverse)

    def merge_vertices(self, digits_vertex=None):
        """Vertices that round to the same point at 10^-digits made one, the first of them kept
        where it was in the order (vertex normals are not compared)."""
        if not len(self.vertices):
            return
        digits = P.Geometry.MESH_MERGE_DIGITS if digits_vertex is None else digits_vertex
        if len(self.faces):
            referenced = np.zeros(len(self.vertices), dtype=bool)
            referenced[self.faces] = True
        else:
            referenced = np.ones(len(self.vertices), dtype=bool)
        rows = np.ascontiguousarray((self.vertices * (10 ** digits)).round().astype(np.int64)[referenced])
        _, index, inverse = np.unique(rows.view(np.dtype((np.void, 24))).reshape(-1),
                                      return_index=True, return_inverse=True)
        order = index.argsort()
        full = np.zeros(len(self.vertices), dtype=np.int64)
        full[referenced] = order.argsort()[inverse.reshape(-1)]
        self._update_vertices(np.nonzero(referenced)[0][index[order]], full)

    def apply_transform(self, matrix):
        matrix = np.asanyarray(matrix, order="C", dtype=np.float64)
        if mm.nearly_equal(matrix, np.eye(4), 1e-8):
            return self
        new = mm.transform_points(self.vertices, matrix)
        turned = not mm.nearly_equal(matrix[:3, :3], np.eye(3), 1e-6)
        kept = self._cached_normals()
        if turned and kept is not None:
            kept = mm.unitize(mm.transform_points(kept, matrix, translate=False))
        if turned and self.vertex_normals is not None:
            self.vertex_normals = mm.unitize(mm.transform_points(self.vertex_normals, matrix, translate=False))
        if turned and np.linalg.det(matrix[:3, :3]) < 0.0:
            self.faces = np.ascontiguousarray(np.fliplr(self.faces))
        self.vertices = new
        if kept is not None:
            self._normals, self._key = kept, self._content()
        return self


def concatenate(meshes):
    """One mesh of them all, the vertices and faces in their order (the face normals carried
    when any of them has its own kept)."""
    if len(meshes) == 1:
        return meshes[0].copy()
    offset = np.append(0, np.cumsum([len(m.vertices) for m in meshes])[:-1])
    vertices = np.vstack([m.vertices for m in meshes])
    faces = np.vstack([m.faces + o for m, o in zip(meshes, offset) if len(m.faces)] or [np.zeros((0, 3), np.int64)])
    normals = None
    if any(m._cached_normals() is not None for m in meshes):
        normals = np.vstack([m.face_normals for m in meshes])
    return Mesh(vertices, faces, face_normals=normals)
