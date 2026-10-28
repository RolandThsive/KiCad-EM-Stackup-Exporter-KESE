"""The topology of a Boundary for STEP: every vertex, every edge and every face once, so that the
faces that meet share their edges and the edges their vertices (what makes a B-rep closed), and
the faces grouped into shells.  Everything is in board mm; nothing is written here.

A loop is a ring of a face: a run of "uses", each a step along one edge, forwards (from the
edge's start vertex to its end) or backwards.  The vertices of a flat face are those of its rings
at the face's height; a wall on the segment a -> b of a slice has the loop a, b at the lower
height, then b, a at the upper one."""
from dataclasses import dataclass

import numpy as np
import shapely
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from kese.core import shapes2d as sh
from kese.core.triangulate import rings_of
from kese.core.vertices import grid_keys, vertices_in_order


@dataclass
class Topology:
    xyz: np.ndarray                # (vertices, 3)
    edge_start: np.ndarray         # per edge: its first vertex, the one at the lower height for a vertical edge
    edge_end: np.ndarray
    vertical: np.ndarray           # per edge: whether it stands on one point of the board
    use_edge: np.ndarray           # per use: its edge
    use_forward: np.ndarray        # per use: along the edge from its start to its end
    loop_start: np.ndarray         # per loop: its first use; its uses follow in order
    loop_count: np.ndarray
    face_loop_start: np.ndarray    # per face: its first loop, the outer one; its holes follow
    face_loop_count: np.ndarray
    face_plane: np.ndarray         # per face: its plane
    face_same_sense: np.ndarray    # per face: its normal is the plane's axis (else the opposite)
    plane_origin: np.ndarray       # (planes, 3)
    plane_axis: np.ndarray         # (planes, 3): the plane's normal
    plane_ref: np.ndarray          # (planes, 3): the plane's x direction
    plane_origin_vertex: np.ndarray  # per plane: the vertex at its origin, or -1
    face_shell: np.ndarray         # per face: its shell
    shells: int
    edges_not_used_twice: int      # zero when the boundary is closed


def topology_of(boundary):
    """Boundary -> Topology.  Every list below collects one array per flat face or per slice of
    walls, joined at the end: a part can have millions of walls."""
    at = {z: i for i, z in enumerate(boundary.levels)}
    heights = np.array(boundary.levels, dtype=float)
    xy, level, loop_count, face_loop_count, face_plane, same_sense = [], [], [], [], [], []
    plane_origin, plane_axis, plane_ref, plane_origin_use = [], [], [], []   # per plane; the origin as a use, or -1
    uses = planes = 0
    for z, region, up in boundary.flats:
        polys = np.array([p for p in shapely.get_parts(sh.polys_only(region)) if p.area > 1e-10], dtype=object)
        if not len(polys):
            continue
        ring_xy, _, _, spans, _ = rings_of(polys)
        for a, b, ends in spans:                                # one polygon: its rings, outer first
            e0 = 0
            for e in ends.tolist():
                xy.append(ring_xy[a + e0:a + e] if up else ring_xy[a + e0:a + e][::-1])
                e0 = e
            loop_count.append(np.diff(np.r_[0, ends]))
            face_loop_count.append([len(ends)])
        level.append(np.full(b, at[z]))
        face_plane.append(np.full(len(spans), planes))
        same_sense.append(np.full(len(spans), up))
        plane_origin.append([[0.0, 0.0, z]])
        plane_axis.append([[0.0, 0.0, 1.0]])
        plane_ref.append([[1.0, 0.0, 0.0]])
        plane_origin_use.append([-1])
        uses += b
        planes += 1
    for z0, z1, segments in boundary.walls():
        a, b = segments[:, 0], segments[:, 1]
        n = len(a)
        if not n:
            continue
        xy.append(np.stack([a, b, b, a], axis=1).reshape(-1, 2))          # a, b at z0; b, a at z1
        level.append(np.tile([at[z0], at[z0], at[z1], at[z1]], n))
        loop_count.append(np.full(n, 4))
        face_loop_count.append(np.full(n, 1))
        face_plane.append(planes + np.arange(n))
        same_sense.append(np.full(n, True))
        d = b - a
        length = np.hypot(d[:, 0], d[:, 1])[:, None]
        plane_origin.append(np.c_[a, np.full(n, z0)])
        plane_axis.append(np.c_[d[:, 1], -d[:, 0], np.zeros(n)] / length)
        plane_ref.append(np.c_[d, np.zeros(n)] / length)
        plane_origin_use.append(uses + 4 * np.arange(n))
        uses += 4 * n
        planes += n
    xy, level = np.concatenate(xy), np.concatenate(level)
    loop_count, face_loop_count = np.concatenate(loop_count), np.concatenate(face_loop_count)
    key = grid_keys(xy)
    vertex, first = vertices_in_order(level, key)
    xyz = np.c_[xy[first], heights[level[first]]]
    loop_start = np.cumsum(np.r_[0, loop_count[:-1]])
    nxt = np.arange(1, len(vertex) + 1)
    nxt[loop_start + loop_count - 1] = loop_start                          # a loop closes on its first use
    va, vb = vertex, vertex[nxt]
    lo, hi = np.minimum(va, vb), np.maximum(va, vb)
    _, first_use, use_edge = np.unique(lo * len(xyz) + hi, return_index=True, return_inverse=True)
    edge_start, edge_end = lo[first_use], hi[first_use]
    plane_origin_use = np.concatenate(plane_origin_use)
    plane_origin_vertex = np.where(plane_origin_use >= 0, vertex[plane_origin_use], -1)
    face_loop_start = np.cumsum(np.r_[0, face_loop_count[:-1]])
    face_shell, shells, loose = shells_of(use_edge, np.repeat(np.arange(len(loop_count)), loop_count),
                                          np.repeat(np.arange(len(face_loop_count)), face_loop_count))
    return Topology(xyz, edge_start, edge_end, key[first][edge_start] == key[first][edge_end], use_edge, va == lo,
                    loop_start, loop_count, face_loop_start, face_loop_count, np.concatenate(face_plane),
                    np.concatenate(same_sense), np.concatenate(plane_origin), np.concatenate(plane_axis),
                    np.concatenate(plane_ref), plane_origin_vertex, face_shell, shells, loose)


def shells_of(use_edge, use_loop, loop_face):
    """The faces grouped into shells, two faces being in one shell when they share an edge:
    (the shell of every face, how many shells, how many edges are not used by exactly two faces)."""
    use_face = loop_face[use_loop]
    order = np.argsort(use_edge, kind="stable")
    count = np.bincount(use_edge)
    first = np.r_[0, np.cumsum(count)[:-1]][count == 2]                # where the uses of every edge used twice start
    f1, f2 = use_face[order[first]], use_face[order[first + 1]]
    faces = int(loop_face.max()) + 1 if len(loop_face) else 0
    graph = coo_matrix((np.ones(len(f1), dtype=bool), (f1, f2)), shape=(faces, faces))
    shells, face_shell = connected_components(graph, directed=False)
    return face_shell, shells, int((count != 2).sum())
