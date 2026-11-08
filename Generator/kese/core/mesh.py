"""A triangle mesh: vertices (n, 3) float, faces (m, 3) int, and what the stages ask of it, done
as trimesh did it (kese/core/mesh_math.py), face normals kept until the mesh changes."""
import numpy as np

from kese.core import mesh_math as mm
from parameters import P


class Mesh:
    def __init__(self, vertices, faces, vertex_normals=None):
        self.vertices = np.asarray(vertices, dtype=np.float64, order="C").reshape((-1, 3))
        self.faces = np.asarray(faces, dtype=np.int64, order="C").reshape((-1, 3))
        self.vertex_normals = None if vertex_normals is None else np.ascontiguousarray(vertex_normals, dtype=np.float64)
        self._normals = None

    # ---- the face normals, kept until the mesh changes -------------------------------------------
    @property
    def face_normals(self):
        if not len(self.faces):
            return np.zeros((0, 3))
        if self._normals is None:
            t = self.triangles
            self._normals = mm.face_normals(t, mm.crosses(t))
        return self._normals

    # ---- what is worked out of it ---------------------------------------------------------------
    @property
    def triangles(self):
        return self.vertices[self.faces]

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

    def copy(self):
        """The vertices and faces only (as trimesh's copy() leaves its cache behind)."""
        return Mesh(self.vertices.copy(), self.faces.copy())

    # ---- changes: a mesh given vertex normals is only read (kese/s6_assemble/transform.py) ----------
    def update_faces(self, mask):
        mask = np.asanyarray(mask)
        if not len(self.faces) or (mask.dtype == bool and mask.all()):
            return
        self.faces, self._normals = self.faces[mask], None

    def _update_vertices(self, mask, inverse):
        if not len(self.faces) or not len(mask) or (mask.dtype == bool and mask.all()):
            return
        self.faces = inverse[self.faces.reshape(-1)].reshape((-1, 3))
        self.vertices, self._normals = self.vertices[mask], None

    def remove_unreferenced_vertices(self):
        referenced = np.zeros(len(self.vertices), dtype=bool)
        referenced[self.faces] = True
        inverse = np.zeros(len(self.vertices), dtype=np.int64)
        inverse[referenced] = np.arange(referenced.sum())
        self._update_vertices(referenced, inverse)

    def merge_vertices(self, digits_vertex):
        """Vertices that round to the same point at 10^-digits_vertex made one, the first of them
        kept where it was in the order (vertex normals are not compared)."""
        if not len(self.vertices):
            return
        if len(self.faces):
            referenced = np.zeros(len(self.vertices), dtype=bool)
            referenced[self.faces] = True
        else:
            referenced = np.ones(len(self.vertices), dtype=bool)
        rows = np.ascontiguousarray((self.vertices * (10 ** digits_vertex)).round().astype(np.int64)[referenced])
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
        turned = not mm.nearly_equal(matrix[:3, :3], np.eye(3), 1e-6)
        if turned and np.linalg.det(matrix[:3, :3]) < 0.0:
            self.faces = np.ascontiguousarray(np.fliplr(self.faces))
        self.vertices, self._normals = mm.transform_points(self.vertices, matrix), None
        return self
