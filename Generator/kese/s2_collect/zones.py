"""Zones: the filled polygons KiCad stores for a copper zone.  An unfilled zone stores none."""
from shapely.geometry import Polygon

from kese.core.sexp import child, children, layer_of, num, pt
from kese.s2_collect.nets import net_name

STROKED_FILL_UNTIL = 20250210     # KiCad's format version from which no zone fill is stroked
UNFILLED = "zones with no fill (unfilled - press B in KiCad and save)"


def add_zone(ctx, node):
    zone_layer = layer_of(node)
    fills = children(node, "filled_polygon")
    net = net_name(ctx.items, node)
    pen = stroked_fill_pen(node, ctx.items.raw.version)
    for fp in fills:
        pts = [pt(p) for p in child(fp, "pts")[1:] if p[0] == "xy"]
        if len(pts) >= 3:
            fill = Polygon(pts).buffer(0)
            if pen > 0:
                fill = fill.buffer(pen / 2, quad_segs=16)
            ctx.add(layer_of(fp) or zone_layer, fill, "zone fills", net)
            ctx.zone_fills.add(id(fill))
    if not fills:
        if child(node, "keepout"):
            ctx.items.skipped["keepout / rule areas (no copper by design)"] += 1
        else:
            ctx.items.skipped[UNFILLED] += 1


def stroked_fill_pen(node, version):
    """The pen a zone's stored fill is drawn with, 0 for none.  KiCad 5 and older stored a fill shrunk by
    half the zone's min_thickness and drew its outline with a pen of min_thickness; KiCad 6 to 8 write
    (filled_areas_thickness no) on a zone they filled, and files from format 20250210 on are never
    stroked.  As KiCad does on reading such a file, a stroked fill grows by half the min_thickness,
    round at the corners (pcb_io_kicad_sexpr_parser.cpp, parseZONE: isStrokedFill and
    InflateWithLinkedHoles)."""
    flag = child(node, "filled_areas_thickness")
    stroked = version < STROKED_FILL_UNTIL
    if flag and len(flag) > 1 and str(flag[1]) in ("no", "false"):
        stroked = False
    if not stroked or child(node, "keepout"):
        return 0.0
    return num(node, "min_thickness", 0.0)
