"""A Boundary as a closed triangle mesh: every flat face cut into triangles, every wall segment
two triangles, and every vertex once.  The faces are cut one after another, each on its own
points; then the points are numbered by (height, grid point), so that the faces that share a
vertex in the Boundary share it in the mesh too, and the mesh closes as the Boundary does."""
import numpy as np
import shapely
import trimesh

from kese.core import shapes2d as sh
from kese.core.triangulate import (
    caps,
    cells_cut,
    lookup,
    manifold_cut,
    rings_of,
    twice_area,
)
from kese.core.vertices import grid_keys, vertices_in_order


def mesh_of_boundary(boundary):
    """Boundary -> trimesh (mm, board frame), or None when it has no faces."""
    at = {z: k for k, z in enumerate(boundary.levels)}
    pieces = [flat_face_triangles(region, at[z], up) for z, region, up in boundary.flats]
    pieces += [wall_triangles(segments, at[z0], at[z1]) for z0, z1, segments in boundary.walls()]
    xyz, tri = mesh_with_shared_vertices(pieces, boundary.levels)
    return trimesh.Trimesh(xyz, tri, process=False) if len(tri) else None


def mesh_with_shared_vertices(pieces, heights):
    """Pieces of mesh (xy, the height index of every point, triangles into the points) -> (xyz,
    triangles), with one vertex per distinct (height, grid point)."""
    pieces = [(xy, level, tri) for xy, level, tri in pieces if len(tri)]
    if not pieces:
        return np.empty((0, 3)), np.empty((0, 3), dtype=np.int64)
    offsets = np.cumsum([0] + [len(xy) for xy, _, _ in pieces[:-1]])
    xy = np.concatenate([xy for xy, _, _ in pieces])
    level = np.concatenate([level for _, level, _ in pieces])
    tri = np.concatenate([tri + n for (_, _, tri), n in zip(pieces, offsets)])
    vertex, first = vertices_in_order(level, grid_keys(xy))
    xyz = np.c_[xy[first], np.asarray(heights, dtype=float)[level[first]]]
    return xyz, vertex[tri]


def flat_face_triangles(region, level, up):
    """A flat face at the height of index `level` as (xy (n, 2), level (n,), triangles (m, 3)
    into xy), wound to look up or down."""
    polys = np.array([p for p in shapely.get_parts(sh.polys_only(region)) if p.area > 1e-10], dtype=object)
    xy, tri = polygon_triangles(polys)
    if not up:
        tri = tri[:, ::-1]
    return xy, np.full(len(xy), level), tri


def wall_triangles(segments, lower, upper):
    """The wall on every segment (a, b), the material on its left, between the heights of index
    `lower` and `upper`: (xy (4n, 2), level (4n,), triangles (2n, 3) into xy).  The corners are
    a, b at the lower height and b, a at the upper; the triangles a0 b0 b1 and a0 b1 a1 face away
    from the material."""
    a, b = segments[:, 0], segments[:, 1]
    n = len(a)
    xy = np.concatenate([a, b, b, a])
    level = np.repeat([lower, lower, upper, upper], n)
    i = np.arange(n)
    tri = np.concatenate([np.c_[i, i + n, i + 2 * n], np.c_[i, i + 2 * n, i + 3 * n]])
    return xy, level, tri


def polygon_triangles(polys):
    """The polygons cut into counter-clockwise triangles on their own vertices: (xy, triangles into
    xy).  Earcut first (kese/core/triangulate.py), Manifold's triangulator for the polygons it
    gets wrong, and constrained Delaunay triangles for what neither closes (rings that touch)."""
    xys, tris, n = [], [], 0
    left = polys
    for cut in (cells_cut, manifold_cut):
        if len(left):
            xy, _, poly, tri, bad = caps(left, cut)
            xys.append(xy)
            tris.append(tri[~bad[poly[tri[:, 0]]]] + n)
            n += len(xy)
            left = left[bad]
    for p in left:
        xy, tri = delaunay_triangles(p)
        xys.append(xy)
        tris.append(tri + n)
        n += len(xy)
    if not xys:
        return np.empty((0, 2)), np.empty((0, 3), dtype=np.int64)
    return np.concatenate(xys), np.concatenate(tris)


def delaunay_triangles(polygon):
    """One polygon cut by GEOS's constrained Delaunay triangulation, which keeps to the polygon's
    own vertices and copes with rings that touch: (xy, counter-clockwise triangles into xy)."""
    xy, _, _, _, _ = rings_of(np.array([polygon], dtype=object))
    corners = np.array([np.asarray(t.exterior.coords)[:3] for t in shapely.constrained_delaunay_triangles(polygon).geoms])
    if not len(corners):
        return xy, np.empty((0, 3), dtype=np.int64)
    tri = lookup(xy, corners.reshape(-1, 2))
    if tri is None:
        return xy, np.empty((0, 3), dtype=np.int64)
    tri = tri.reshape(-1, 3)
    turn = twice_area(xy, tri) < 0
    tri[turn] = tri[turn][:, ::-1]
    return xy, tri
