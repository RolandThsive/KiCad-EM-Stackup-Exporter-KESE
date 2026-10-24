"""Extrusion: a 2D region between two heights as a closed triangle mesh (trimesh), and the
union of such meshes into one solid."""
import numpy as np
import shapely
import trimesh

from kese.core.shapes2d import polygons, polys_only
from parameters import P


# ---- extrusion -------------------------------------------------------------------------------------
def extrude(geom, z0, z1, _retry=True):
    """A closed triangle mesh of the polygon(s) between z0 and z1, or None."""
    geom = polys_only(geom)
    if geom.is_empty or abs(z1 - z0) < 1e-12:
        return None
    z0, z1 = min(z0, z1), max(z0, z1)
    meshes = []
    for p in polygons(geom):
        if p.area <= 1e-10:
            continue
        m = trimesh.creation.extrude_polygon(p, height=z1 - z0)
        m.apply_translation([0, 0, z0])
        if not m.is_watertight:          # earcut trips on holes touching the outer ring
            m = extrude_cdt(p, z0, z1)
        if not m.is_watertight and _retry:   # rings pinch at a point: part them slightly
            opened = polys_only(shapely.set_precision(p, 0).buffer(-P.Geometry.PINCH_POINT_OPENING_MM, quad_segs=1))
            pieces = [q for q in (extrude(x, z0, z1, _retry=False) for x in polygons(opened)) if q is not None]
            if pieces and all(q.is_watertight for q in pieces):
                m = trimesh.util.concatenate(pieces)
        meshes.append(m)
    return trimesh.util.concatenate(meshes) if meshes else None


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
    meshes = [m for m in meshes if m is not None and len(m.faces)]
    if not meshes:
        return None
    if len(meshes) == 1:
        return meshes[0]
    try:
        return trimesh.boolean.union(meshes, engine="manifold")
    except Exception as exc:
        if log is not None:
            log(f"note: boolean union unavailable ({exc}); pieces left touching")
        return trimesh.util.concatenate(meshes)
