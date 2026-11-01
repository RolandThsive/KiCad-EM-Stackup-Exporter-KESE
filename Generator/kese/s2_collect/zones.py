"""Zones: the filled polygons KiCad stores for a copper zone.  An unfilled zone stores none."""
from shapely.geometry import LineString, Polygon

from kese.core.sexp import child, children, layer_of, num, pt
from kese.core.shapes2d import circle_quads, thicken, union
from kese.s1_read.parse_kicad_version import legacy_fill_segments, stroked_fill_pen
from kese.s2_collect.nets import net_name

UNFILLED = "zones with no fill (unfilled - press B in KiCad and save)"


def add_zone(ctx, node):
    zone_layer = layer_of(node)
    fills = children(node, "filled_polygon")
    net = net_name(ctx.items, node)
    pen = stroked_fill_pen(node, ctx.items.raw.dialect)
    for fp in fills:
        pts = [pt(p) for p in child(fp, "pts")[1:] if p[0] == "xy"]
        if len(pts) >= 3:
            fill = Polygon(pts).buffer(0)
            if pen > 0:
                fill = fill.buffer(pen / 2, quad_segs=circle_quads(pen / 2))
            ctx.add(layer_of(fp) or zone_layer, fill, "zone fills", net)
            ctx.zone_fills.add(id(fill))
    segments = legacy_fill_segments(node)
    if segments:
        w = num(node, "min_thickness", 0.0)
        fill = union([thicken(LineString(s), w) for s in segments])
        ctx.add(zone_layer, fill, "zone fills (segment fill)", net)
        ctx.zone_fills.add(id(fill))
    elif not fills:
        if child(node, "keepout"):
            ctx.items.skipped["keepout / rule areas (no copper by design)"] += 1
        else:
            ctx.items.skipped[UNFILLED] += 1

