"""Extrusion: a 2D region between two heights as a closed triangle mesh (trimesh), and the
union of such meshes into one solid."""
import manifold3d as mf
import numpy as np
import shapely
import trimesh

from kese.core.shapes2d import polygons, polys_only
from kese.core.triangulate import caps, cells_cut, manifold_cut
from parameters import P


# ---- extrusion -------------------------------------------------------------------------------------
def extrude(geom, z0, z1, _retry=True):
    """A closed triangle mesh of the polygon(s) between z0 and z1, or None.  The top and bottom of
    every polygon are cut into triangles (kese/core/triangulate.py) and its walls stand on its own
    edges, all polygons of the region at once; a polygon neither triangulator closes goes through
    extrude_cdt(), and is parted where its rings pinch."""
    geom = polys_only(geom)
    if geom.is_empty or abs(z1 - z0) < 1e-12:
        return None
    z0, z1 = min(z0, z1), max(z0, z1)
    left = np.array(polygons(geom), dtype=object)
    left = left[shapely.area(left) > 1e-10]
    if not len(left):
        return None
    meshes = []
    for cut in (cells_cut, manifold_cut):
        if len(left):
            m, bad = prism_mesh(left, z0, z1, cut)
            meshes.append(m)
            left = left[bad]
    meshes += [slow_prism(p, z0, z1, _retry) for p in left]
    meshes = [m for m in meshes if m is not None]
    return meshes[0] if len(meshes) == 1 else trimesh.util.concatenate(meshes) if meshes else None


def prism_mesh(polys, z0, z1, cut):
    """The polygons between z0 and z1 as one mesh, their tops and bottoms cut into triangles by
    cut (caps()), and the indices of the polygons whose triangles do not close exactly on their
    edges, which are left out of it."""
    xy, nxt, poly, tri, bad = caps(polys, cut)
    keep = ~bad[poly]
    m = int(keep.sum())
    if not m:
        return None, np.flatnonzero(bad)
    new = np.cumsum(keep) - 1
    t = new[tri[~bad[poly[tri[:, 0]]]]]
    i, j = new[keep], new[nxt[keep]]
    v = np.concatenate([np.c_[xy[keep], np.full(m, z0)], np.c_[xy[keep], np.full(m, z1)]])
    # the bottom facing down, the top facing up, and on every ring edge a wall of two triangles
    f = np.concatenate([t[:, ::-1], t + m, np.c_[i, j, j + m], np.c_[i, j + m, i + m]])
    return trimesh.Trimesh(v, f, process=False), np.flatnonzero(bad)


def slow_prism(p, z0, z1, retry):
    """A polygon neither triangulator closes (rings that touch): GEOS's constrained Delaunay
    triangles, and if they do not close either, the polygon parted slightly where its rings pinch."""
    m = extrude_cdt(p, z0, z1)
    if not m.is_watertight and retry:
        opened = polys_only(shapely.set_precision(p, 0).buffer(-P.Geometry.PINCH_POINT_OPENING_MM, quad_segs=1))
        pieces = [q for q in (extrude(x, z0, z1, _retry=False) for x in polygons(opened)) if q is not None]
        if pieces and all(q.is_watertight for q in pieces):
            m = trimesh.util.concatenate(pieces)
    return m


def extrude_cdt(p, z0, z1):
    """Extrusion with GEOS constrained-Delaunay caps; robust when rings touch."""
    from shapely.geometry.polygon import orient
    p = orient(p, 1.0)
    tris = [np.asarray(t.exterior.coords)[:3] for t in shapely.constrained_delaunay_triangles(p).geoms]
    verts, faces = [], []

    def tri(a, b, c):
        n = len(verts)
        verts.extend([a, b, c])
        faces.append([n, n + 1, n + 2])

    for t in tris:
        if (t[1][0] - t[0][0]) * (t[2][1] - t[0][1]) - (t[1][1] - t[0][1]) * (t[2][0] - t[0][0]) < 0:
            t = t[::-1]
        a, b, c = t
        tri((*a, z1), (*b, z1), (*c, z1))
        tri((*a, z0), (*c, z0), (*b, z0))
    for ring in [p.exterior, *p.interiors]:
        c = np.asarray(ring.coords)
        for (ax, ay), (bx, by) in zip(c[:-1], c[1:]):
            tri((ax, ay, z0), (bx, by, z0), (bx, by, z1))
            tri((ax, ay, z0), (bx, by, z1), (ax, ay, z1))
    m = trimesh.Trimesh(np.array(verts), np.array(faces), process=True)
    m.merge_vertices()
    return m


def solid_union(meshes, log=None):
    """One solid of the meshes, joined by Manifold in double precision.  trimesh's own call to
    Manifold rounds every vertex to float32 (in steps of 7.6 nm at 100 mm, a thirteenth of the snap
    grid), and prisms that met exactly could come back as two vertices at one place: an open solid
    once merged."""
    meshes = [m for m in meshes if m is not None and len(m.faces)]
    if not meshes:
        return None
    if len(meshes) == 1:
        return meshes[0]
    try:
        solids = [mf.Manifold(mesh=mf.Mesh64(vert_properties=np.asarray(m.vertices, dtype=np.float64),
                                             tri_verts=np.asarray(m.faces, dtype=np.uint32))) for m in meshes]
        bad = [s.status() for s in solids if s.status() != mf.Error.NoError]
        if bad:
            raise ValueError(f"{len(bad)} of {len(solids)} pieces are not closed ({bad[0]})")
        out = mf.Manifold.batch_boolean(solids, mf.OpType.Add).to_mesh64()
        # copies, so Manifold's own arrays are freed with it
        return trimesh.Trimesh(np.array(out.vert_properties)[:, :3], np.array(out.tri_verts, dtype=np.int64), process=False)
    except Exception as exc:
        if log is not None:
            log(f"note: boolean union unavailable ({exc}); pieces left touching")
        return trimesh.util.concatenate(meshes)
