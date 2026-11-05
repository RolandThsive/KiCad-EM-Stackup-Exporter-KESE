"""2D shape helpers (shapely): circles, strokes and set operations on the snapping grid.  All
tolerances come from parameters/geometry.py; nothing numeric is defined here."""
import math

import numpy as np
import shapely
from shapely.geometry import GeometryCollection, LineString, Point, box

from kese.core import math2d as geo
from kese.core.graph import connected_components, pairs_within
from kese.core.shape_copies import own
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
    n = math.pi / math.acos(1 - min(g.CIRCLE_CHORD_TOLERANCE_MM / r, 1.0))
    return int(min(g.CIRCLE_MAX_QUAD_SEGS, max(g.CIRCLE_MIN_QUAD_SEGS, math.ceil(n / 4))))


def disk(c, r):
    return Point(c).buffer(r, quad_segs=circle_quads(r)) if r > 0 else EMPTY


def thicken(line, w):
    if w <= 0:
        return EMPTY
    return line.buffer(w / 2, quad_segs=max(G().TRACK_END_MIN_QUAD_SEGS, circle_quads(w / 2) // 2))


def rounded_rect(x1, y1, x2, y2, r):
    """The rectangle between two opposite corners, its corners rounded to radius r (at most half its
    shorter side)."""
    (x1, x2), (y1, y2) = sorted((x1, x2)), sorted((y1, y2))
    r = min(r, (x2 - x1) / 2, (y2 - y1) / 2)
    if r <= 0:
        return box(x1, y1, x2, y2)
    core = box(x1 + r, y1 + r, x2 - r, y2 - r) if r < min(x2 - x1, y2 - y1) / 2 else \
        LineString([(x1 + r, y1 + r), (x2 - r, y2 - r)])
    return core.buffer(r, quad_segs=circle_quads(r))


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
    """Snap a shape to the grid (makes touching layers share identical vertices).  Every part is
    rounded on its own (a part already on the grid is kept as it is) and only parts that then
    meet are joined again: rounding a whole layer at once costs minutes on a big board."""
    parts = shapely.get_parts(polys_only(g))
    if not len(parts):
        return EMPTY
    off = ~on_grid(parts)
    parts[off] = shapely.set_precision(parts[off], grid())
    return side_by_side(parts)


def on_grid(parts):
    """For each polygon: True when it is valid and all its vertices lie on the grid already."""
    xy, which = shapely.get_coordinates(parts, return_index=True)
    k = xy / grid()
    off = np.abs(k - np.round(k)).max(axis=1) > 1e-6 if len(xy) else np.zeros(0, bool)
    return (np.bincount(which[off], minlength=len(parts)) == 0) & shapely.is_valid(parts)


def side_by_side(regions):
    """The union of regions that mostly do not touch (the nets of one copper layer), as joined()."""
    return joined([p for x in regions for p in shapely.get_parts(polys_only(x)) if not p.is_empty])


def meeting(parts):
    """The parts in groups (lists of indices): parts within a grid step of each other share a group."""
    if not len(parts):
        return []
    a, b = pairs_within(parts, grid())
    label = connected_components(len(parts), a, b)[1]
    order = np.argsort(label, kind="stable")
    return [g.tolist() for g in np.split(order, np.flatnonzero(np.diff(label[order])) + 1)]


def joined(parts):
    """Polygons on the grid as one region: a part that meets no other stays as it is and only the
    groups that meet are joined (on the grid), as KiCad joins only what meets."""
    if len(parts) < 2:
        return parts[0] if len(parts) else EMPTY
    out = []
    for idx in meeting(parts):
        out += [parts[idx[0]]] if len(idx) == 1 else \
            list(shapely.get_parts(polys_only(shapely.union_all([parts[i] for i in idx], grid_size=grid()))))
    return as_region(out)


def as_region(polys):
    """Polygons that do not overlap as one region."""
    return shapely.MultiPolygon(polys) if len(polys) > 1 else polys[0] if polys else EMPTY


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
            out += [x for x in polygons(q) if x.area > G().SLIVER_AREA_MM2]
        else:
            out.append(p)
    return shapely.MultiPolygon(out) if out else EMPTY


def diff(a, b):
    return _overlay(shapely.difference, a, b)


def inter(a, b):
    return _overlay(shapely.intersection, a, b)


def _overlay(op, a, b):
    """op(a, b) on the grid.  Where GEOS refuses (an input whose part crosses itself, as snap rounding
    once left one on a KiCad 8 board), it is made valid and the op tried again."""
    a, b = polys_only(a), polys_only(b)
    try:
        return polys_only(op(a, b, grid_size=grid()))
    except shapely.errors.GEOSException:          # copies made valid: b may be shared by threads (shape_copies.py)
        return polys_only(op(*(polys_only(shapely.make_valid(own(g))) for g in (a, b)), grid_size=grid()))


def exactly(g):
    """g, the result of a set operation done in floating point on regions on the grid, back on the
    grid with as little change as possible: only the new vertices, where two outlines cross, are
    rounded onto it (a part this leaves invalid is snapped as a whole).  So two regions cut along the
    same outline keep the same vertices there and still meet with no gap and no overlap, where
    snapping each on its own could round their shared edge two ways."""
    parts = shapely.get_parts(polys_only(g))
    if not len(parts):
        return EMPTY
    off = ~on_grid(parts)
    if not off.any():
        return polys_only(g)
    rounded = shapely.set_precision(parts[off], grid(), mode="pointwise")
    bad = ~shapely.is_valid(rounded) | shapely.is_empty(rounded)
    rounded[bad] = shapely.set_precision(parts[off][bad], grid())
    parts[off] = rounded
    pieces = [p for q in parts for p in shapely.get_parts(polys_only(q)) if not p.is_empty]
    out = shapely.MultiPolygon(pieces)
    return out if out.is_valid else joined(pieces)


def exact_diff(a, b):
    """a less b for regions on the grid: cut in floating point, then only the new vertices rounded
    onto the grid (exactly()).  Where a cut on the grid would drop a sliver thinner than a grid step
    (two needle tips a hair apart), this keeps it whenever its corners on the grid still make a
    polygon.  Where GEOS refuses, the cut on the grid (diff)."""
    try:
        return exactly(shapely.difference(polys_only(a), polys_only(b)))
    except shapely.errors.GEOSException:
        return diff(a, b)


def polygons(g):
    """The polygons of a region, as built into 3D, those that touch at a point or along a line pulled
    apart by PINCH_POINT_OPENING_MM (the last step before extrusion: a grid operation would rejoin them)."""
    g = polys_only(g)
    if g.is_empty:
        return []
    if g.geom_type != "MultiPolygon":
        return [g]
    return list(part_touching(g).geoms)


# ---- footprint placement -------------------------------------------------------------------------
def make_transform(at_numbers):
    """Footprint local -> board coordinates."""
    if not at_numbers:
        return lambda p: p
    return geo.rotation((at_numbers[0], at_numbers[1]), at_numbers[2] if len(at_numbers) > 2 else 0.0)
