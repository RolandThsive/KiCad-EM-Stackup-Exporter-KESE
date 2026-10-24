"""2D shape helpers (shapely): circles, strokes, set operations on the snapping grid, and the
split of a coating over raised copper.  All tolerances come from parameters/geometry.py; nothing
numeric is defined here."""
import math

import shapely
from shapely.geometry import GeometryCollection, Point

from kese.core import math2d as geo
from parameters import P

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
    pts = geo.arc_points(c, r, a0, sweep, max(2, math.ceil(abs(math.degrees(sweep)) / G().ARC_STEP_DEG)))
    if first is not None:
        pts[0] = first
    if last is not None:
        pts[-1] = last
    return pts


def arc3(p1, p2, p3):
    """Points along the arc from p1 through p2 to p3."""
    circle = geo.circle_through(p1, p2, p3)
    if circle is None:
        return [p1, p3]
    c, r = circle
    a0, sweep = geo.arc_sweep(c, p1, p2, p3)
    return arc_pts(c, r, a0, sweep, p1, p3)


def bezier(p):
    return geo.bezier_points(p, G().BEZIER_SEGMENTS)


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
    apart by Geometry.PINCH_POINT_OPENING_MM so every solid is manifold on its own."""
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
    """Footprint local -> board coordinates."""
    if not at_numbers:
        return lambda p: p
    return geo.rotation((at_numbers[0], at_numbers[1]), at_numbers[2] if len(at_numbers) > 2 else 0.0)


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
