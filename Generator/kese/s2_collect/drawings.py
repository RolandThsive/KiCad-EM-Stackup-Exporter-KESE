"""Drawings: gr_* / fp_* lines, arcs, circles, rectangles, polygons and Bezier curves.  On
Edge.Cuts they make the outline; on any other layer they cover their stroke, and their inside too
when filled."""
import math

import shapely
from shapely.geometry import LineString, Polygon

from kese.core.sexp import child, num, pt
from kese.core.shapes2d import (EMPTY, G, arc3, arc_pts, bezier, circle_quads, disk, polys_only, rounded_rect, thicken,
                                 union)
from kese.s1_read.parse_kicad_version import is_filled, layer_and_mask, legacy_arc, stroke_width
from kese.s2_collect.nets import net_name

GRAPHICS = {"gr_line", "gr_arc", "gr_circle", "gr_rect", "gr_poly", "gr_curve", "gr_bezier",
            "fp_line", "fp_arc", "fp_circle", "fp_rect", "fp_poly", "fp_curve",
            "gr_ellipse", "gr_ellipse_arc", "fp_ellipse", "fp_ellipse_arc"}     # ellipses: KiCad after 10


def graphic(node, T):
    """A gr_*/fp_* drawing -> (centre-line geometry, closed?, stroke width, filled?)."""
    kind = node[0].split("_", 1)[1]
    w = stroke_width(node)
    filled = is_filled(node, kind, w)
    if kind == "line":
        return LineString([T(pt(child(node, "start"))), T(pt(child(node, "end")))]), False, w, False
    if kind == "arc":
        legacy = legacy_arc(node, T)
        if legacy is None:
            pts = arc3(T(pt(child(node, "start"))), T(pt(child(node, "mid"))), T(pt(child(node, "end"))))
        else:
            c, r, a0, sweep, p0 = legacy
            pts = arc_pts(c, r, a0, sweep, first=p0)
        return LineString(pts), False, w, False
    if kind == "circle":
        c, e = T(pt(child(node, "center"))), T(pt(child(node, "end")))
        return disk(c, math.hypot(e[0] - c[0], e[1] - c[1])), True, w, filled
    if kind == "rect":
        (x1, y1), (x2, y2) = pt(child(node, "start")), pt(child(node, "end"))
        r = num(node, "radius", 0.0)                        # rounded corners
        corners = rounded_rect(x1, y1, x2, y2, r).exterior.coords[:-1] if r > 0 else \
            ((x1, y1), (x2, y1), (x2, y2), (x1, y2))
        return Polygon([T(p) for p in corners]), True, w, filled
    if kind == "poly":
        pts = []
        for p in child(node, "pts")[1:]:
            if p[0] == "xy":
                pts.append(T(pt(p)))
            elif p[0] == "arc":
                pts.extend(arc3(T(pt(child(p, "start"))), T(pt(child(p, "mid"))), T(pt(child(p, "end"))))[1:])
        # make_valid, not buffer(0): a self-crossing (bow-tie) polygon keeps every lobe, as KiCad fills it
        return (polys_only(shapely.make_valid(Polygon(pts))) if len(pts) >= 3 else EMPTY), True, w, filled
    if kind in ("ellipse", "ellipse_arc"):
        pts = [T(p) for p in ellipse_pts(node, kind == "ellipse_arc")]
        if kind == "ellipse":
            return Polygon(pts), True, w, filled
        return LineString(pts), False, w, False
    if kind in ("curve", "bezier"):
        pts = [T(pt(p)) for p in child(node, "pts")[1:] if p[0] == "xy"]
        return LineString(bezier(pts)), False, w, False
    return None, False, 0.0, False


def ellipse_pts(node, arc):
    """An ellipse or elliptical arc (KiCad after 10): centre + R(rotation) (a cos t, b sin t) from
    start_angle to end_angle, in KiCad's frame (libs/kimath/src/geometry/shape_ellipse.cpp)."""
    cx, cy = pt(child(node, "center"))
    a, b = num(node, "major_radius", 0.0), num(node, "minor_radius", 0.0)
    rot = math.radians(num(node, "rotation_angle", 0.0))
    t0, t1 = (math.radians(num(node, "start_angle", 0.0)), math.radians(num(node, "end_angle", 0.0))) if arc \
        else (0.0, 2 * math.pi)
    while t1 <= t0:
        t1 += 2 * math.pi
    n = max(8, math.ceil(math.degrees(t1 - t0) / G().ARC_STEP_DEG))
    cr, sr = math.cos(rot), math.sin(rot)
    out = []
    for k in range(n + (1 if arc else 0)):
        t = t0 + (t1 - t0) * k / n
        x, y = a * math.cos(t), b * math.sin(t)
        out.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
    return out


def painted(geom, closed, w, filled):
    """What a drawing covers on a non-outline layer."""
    if geom is None or geom.is_empty:
        return EMPTY
    parts = [geom] if closed and filled else []
    parts.append(thicken(geom.boundary if closed else geom, w))   # boundary: a self-crossing poly is a MultiPolygon
    return union(parts)


def add_drawing(ctx, node, T, in_footprint=False):
    layer, bare = layer_and_mask(node)
    geom, closed, w, filled = graphic(node, T)
    if geom is None or geom.is_empty:
        return
    if layer == "Edge.Cuts":
        if closed:      # a self-crossing poly is a MultiPolygon: one outline per face
            ctx.items.edge_closed.extend(getattr(geom, "geoms", [geom]))
        else:
            ctx.items.edge_open.append(geom)
        ctx.items.found["outline shapes on Edge.Cuts"] += 1
    else:
        kind = "footprint graphic" if in_footprint else "graphic"
        # a copper shape can carry a net; without one it stays on NO_NET_NAME
        ctx.add(layer, painted(geom, closed, w, filled), kind + "s", net_name(ctx.items, node))
        if bare:
            m = ctx.bare_margin(node, w, solid=closed and filled)
            # KiCad (EDA_SHAPE::TransformShapeToPolygon): a filled circle or rounded rectangle is grown by
            # w/2 + margin, so a negative margin shrinks its opening; a filled polygon or square-cornered
            # rectangle keeps its whole inside
            curved = node[0].endswith("circle") or (node[0].endswith("rect") and num(node, "radius", 0.0) > 0)
            if closed and filled and curved and w / 2 + m < 0:
                opening = geom.buffer(w / 2 + m, quad_segs=circle_quads(abs(w / 2 + m)))
            else:
                opening = painted(geom, closed, w + 2 * m, filled)
            ctx.add(f"{bare}.Mask", opening, kind + " mask openings")
