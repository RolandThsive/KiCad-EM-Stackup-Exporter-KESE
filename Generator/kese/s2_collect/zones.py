"""Zones: the filled polygons KiCad stores for a copper zone.  An unfilled zone stores none."""
from shapely.geometry import Polygon

from kese.core.sexp import child, children, layer_of, pt
from kese.s2_collect.nets import net_name

UNFILLED = "zones with no fill (unfilled - press B in KiCad and save)"


def add_zone(ctx, node):
    zone_layer = layer_of(node)
    fills = children(node, "filled_polygon")
    net = net_name(ctx.items, node)
    for fp in fills:
        pts = [pt(p) for p in child(fp, "pts")[1:] if p[0] == "xy"]
        if len(pts) >= 3:
            ctx.add(layer_of(fp) or zone_layer, Polygon(pts).buffer(0), "zone fills", net)
    if not fills:
        if child(node, "keepout"):
            ctx.items.skipped["keepout / rule areas (no copper by design)"] += 1
        else:
            ctx.items.skipped[UNFILLED] += 1
