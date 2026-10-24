"""Drawings: gr_* / fp_* lines, arcs, circles, rectangles, polygons and Bezier curves.  On
Edge.Cuts they make the outline; on any other layer they cover their stroke, and their inside too
when filled."""
import math

from shapely.geometry import LineString, Polygon

from kese.core.sexp import child, layer_of, num, pt, yes
from kese.core.shapes2d import EMPTY, arc3, arc_pts, bezier, disk, thicken, union
from kese.s2_collect.nets import net_name

GRAPHICS = {"gr_line", "gr_arc", "gr_circle", "gr_rect", "gr_poly", "gr_curve", "gr_bezier",
            "fp_line", "fp_arc", "fp_circle", "fp_rect", "fp_poly", "fp_curve"}


def graphic(node, T):
    """A gr_*/fp_* drawing -> (centre-line geometry, closed?, stroke width, filled?)."""
    kind = node[0].split("_", 1)[1]
    w = num(node, "width")
    if w is None:
        stroke = child(node, "stroke")
        w = num(stroke, "width", 0.0) if stroke else 0.0
    fill = child(node, "fill")
    filled = yes(fill[1]) if fill and len(fill) > 1 else kind == "poly"
    if kind == "line":
        return LineString([T(pt(child(node, "start"))), T(pt(child(node, "end")))]), False, w, False
    if kind == "arc":
        if child(node, "mid"):
            pts = arc3(T(pt(child(node, "start"))), T(pt(child(node, "mid"))), T(pt(child(node, "end"))))
        else:  # KiCad 5: (start centre) (end arc-start) (angle deg)
            c, p0 = T(pt(child(node, "start"))), T(pt(child(node, "end")))
            r = math.hypot(p0[0] - c[0], p0[1] - c[1])
            a0 = math.atan2(p0[1] - c[1], p0[0] - c[0])
            pts = arc_pts(c, r, a0, math.radians(num(node, "angle", 0.0)), first=p0)
        return LineString(pts), False, w, False
    if kind == "circle":
        c, e = T(pt(child(node, "center"))), T(pt(child(node, "end")))
        return disk(c, math.hypot(e[0] - c[0], e[1] - c[1])), True, w, filled
    if kind == "rect":
        (x1, y1), (x2, y2) = pt(child(node, "start")), pt(child(node, "end"))
        return Polygon([T(p) for p in ((x1, y1), (x2, y1), (x2, y2), (x1, y2))]), True, w, filled
    if kind == "poly":
        pts = []
        for p in child(node, "pts")[1:]:
            if p[0] == "xy":
                pts.append(T(pt(p)))
            elif p[0] == "arc":
                pts.extend(arc3(T(pt(child(p, "start"))), T(pt(child(p, "mid"))), T(pt(child(p, "end"))))[1:])
        return (Polygon(pts).buffer(0) if len(pts) >= 3 else EMPTY), True, w, filled
    if kind in ("curve", "bezier"):
        pts = [T(pt(p)) for p in child(node, "pts")[1:] if p[0] == "xy"]
        return LineString(bezier(pts)), False, w, False
    return None, False, 0.0, False


def painted(geom, closed, w, filled):
    """What a drawing covers on a non-outline layer."""
    if geom is None or geom.is_empty:
        return EMPTY
    parts = [geom] if closed and filled else []
    parts.append(thicken(geom.exterior if closed else geom, w))
    return union(parts)


def add_drawing(ctx, node, T, in_footprint=False):
    layer = layer_of(node)
    geom, closed, w, filled = graphic(node, T)
    if geom is None or geom.is_empty:
        return
    if layer == "Edge.Cuts":
        (ctx.items.edge_closed if closed else ctx.items.edge_open).append(geom)
        ctx.items.found["outline shapes on Edge.Cuts"] += 1
    else:
        # copper shapes can carry a net (KiCad 8+); without one they stay on NO_NET_NAME
        ctx.add(layer, painted(geom, closed, w, filled), "footprint graphics" if in_footprint else "graphics",
                net_name(ctx.items, node))
