"""2D shape helpers (shapely) and the prism extrusion (trimesh).  All tolerances come from
Geometry_Parameters; nothing numeric is defined here."""
import math

import numpy as np
import shapely
import trimesh
from shapely.geometry import GeometryCollection, LineString, Point, Polygon

from Parameters import P

EMPTY = GeometryCollection()


# ---- parameters as short names ----------------------------------------------------------------
def G():
    return P.Geometry


def grid():
    return G().SNAP_GRID_MM


# ---- circles, arcs, strokes ---------------------------------------------------------------------
def circle_quads(r):
    g = G()
    if r <= 0:
        return g.CIRCLE_MIN_QUAD_SEGS
    n = math.pi / math.acos(max(-1.0, 1 - min(g.CIRCLE_CHORD_TOLERANCE_MM / r, 1.0)))
    return int(min(g.CIRCLE_MAX_QUAD_SEGS, max(g.CIRCLE_MIN_QUAD_SEGS, math.ceil(n / 4))))


def disk(c, r):
    return Point(c).buffer(r, quad_segs=circle_quads(r)) if r > 0 else EMPTY


def thicken(line, w):
    if w <= 0:
        return EMPTY
    return line.buffer(w / 2, quad_segs=max(G().TRACK_END_MIN_QUAD_SEGS, circle_quads(w / 2) // 2))


def arc_pts(c, r, a0, sweep, first=None, last=None):
    n = max(2, math.ceil(abs(math.degrees(sweep)) / G().ARC_STEP_DEG))
    pts = [(c[0] + r * math.cos(a0 + sweep * i / n), c[1] + r * math.sin(a0 + sweep * i / n))
           for i in range(n + 1)]
    if first is not None:
        pts[0] = first
    if last is not None:
        pts[-1] = last
    return pts


def arc3(p1, p2, p3):
    """Points along the arc from p1 through p2 to p3."""
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-12:
        return [p1, p3]
    s1, s2, s3 = x1 * x1 + y1 * y1, x2 * x2 + y2 * y2, x3 * x3 + y3 * y3
    ux = (s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2)) / d
    uy = (s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1)) / d
    r = math.hypot(x1 - ux, y1 - uy)
    a1, a2, a3 = (math.atan2(y - uy, x - ux) for x, y in (p1, p2, p3))
    tau = 2 * math.pi
    sweep = (a3 - a1) % tau if (a2 - a1) % tau <= (a3 - a1) % tau else -((a1 - a3) % tau)
    return arc_pts((ux, uy), r, a1, sweep, p1, p3)


def bezier(p):
    t = np.linspace(0, 1, G().BEZIER_SEGMENTS + 1)[:, None]
    p = np.array(p)
    return list(map(tuple, (1 - t) ** 3 * p[0] + 3 * (1 - t) ** 2 * t * p[1]
                    + 3 * (1 - t) * t ** 2 * p[2] + t ** 3 * p[3]))


# ---- set operations -------------------------------------------------------------------------------
def union(geoms):
    geoms = [g for g in geoms if g is not None and not g.is_empty]
    return shapely.union_all(geoms) if geoms else EMPTY


def polys_only(g):
    if g is None or g.is_empty:
        return EMPTY
    if g.geom_type in ("Polygon", "MultiPolygon"):
        return g
    return union([p for p in getattr(g, "geoms", []) if p.geom_type in ("Polygon", "MultiPolygon")])


def snap(g):
    """Snap a shape to the grid (makes touching layers share identical vertices).  Snapping can
    leave two parts of a multipolygon sharing an edge, so the result is unioned once more."""
    g = polys_only(shapely.set_precision(polys_only(g), grid()))
    if g.geom_type == "MultiPolygon":
        g = polys_only(shapely.union_all(g, grid_size=grid()))
    return g


def part_touching(g):
    """Parts of a multipolygon that touch each other at a point (or along a line) are pulled
    apart by Geometry_Parameters.PINCH_POINT_OPENING_MM so every solid is manifold on its own."""
    parts = list(g.geoms)
    tree = shapely.STRtree(parts)
    pairs = tree.query(parts, predicate="touches")
    touching = set(pairs[0].tolist()) | set(pairs[1].tolist())
    if not touching:
        return g
    eps = G().PINCH_POINT_OPENING_MM / 2
    out = []
    for i, p in enumerate(parts):
        if i in touching:
            q = shapely.set_precision(p, 0).buffer(-eps, join_style="mitre")
            out += [x for x in polygons(q) if x.area > 1e-10]
        else:
            out.append(p)
    return shapely.MultiPolygon(out) if len(out) > 1 else shapely.MultiPolygon([out[0]]) if out else EMPTY


def diff(a, b):
    return polys_only(polys_only(a).difference(polys_only(b), grid_size=grid()))


def inter(a, b):
    return polys_only(polys_only(a).intersection(polys_only(b), grid_size=grid()))


def polygons(g, part=True):
    """The polygons of a region, as built into 3D.  Parts that touch at a point or along a line
    are pulled apart by PINCH_POINT_OPENING_MM here, at the last step before extrusion (any
    earlier grid operation would snap them back together)."""
    g = polys_only(g)
    if g.is_empty:
        return []
    if g.geom_type != "MultiPolygon":
        return [g]
    return list(part_touching(g).geoms) if part else list(g.geoms)


# ---- footprint placement -------------------------------------------------------------------------
def make_transform(at_numbers):
    """Footprint local -> board coordinates.  KiCad angles are CCW on screen (Y down)."""
    if not at_numbers:
        return lambda p: p
    fx, fy = at_numbers[0], at_numbers[1]
    rot = math.radians(at_numbers[2]) if len(at_numbers) > 2 else 0.0
    c, s = math.cos(rot), math.sin(rot)
    return lambda p: (fx + p[0] * c + p[1] * s, fy - p[0] * s + p[1] * c)


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
            opened = polys_only(shapely.set_precision(p, 0).buffer(-G().PINCH_POINT_OPENING_MM, quad_segs=1))
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


def conformal_regions(region, raised, t, wall_quad_segs):
    """Split a coating of thickness t laid over `raised` (copper) into
    (flat on the base, on top of the raised copper, wall beside the copper)."""
    region, raised = snap(region), snap(raised)
    if region.is_empty:
        return EMPTY, EMPTY, EMPTY
    if raised.is_empty:
        return region, EMPTY, EMPTY
    grown = snap(raised.buffer(t, quad_segs=wall_quad_segs))
    flat = diff(region, grown)
    top = inter(region, raised)
    wall = inter(region, diff(grown, raised))
    return flat, top, wall
