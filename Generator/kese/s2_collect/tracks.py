"""Tracks: straight segments and arcs, each the stroke of its width on one copper layer."""
from shapely.geometry import LineString

from kese.core.sexp import child, num, pt
from kese.s1_read.parse_kicad_version import layer_and_mask
from kese.core.shapes2d import arc3, thicken
from kese.s2_collect.nets import net_name


def add_track(ctx, node):
    """(segment ...) or (arc ...) -> copper of its net, and its opening in the mask when the mask
    leaves it bare."""
    if node[0] == "segment":
        line = LineString([pt(child(node, "start")), pt(child(node, "end"))])
    else:
        line = LineString(arc3(pt(child(node, "start")), pt(child(node, "mid")), pt(child(node, "end"))))
    kind = "track" if node[0] == "segment" else "arc track"
    w = num(node, "width", 0.0)
    layer, bare = layer_and_mask(node)
    ctx.add(layer, thicken(line, w), kind + "s", net_name(ctx.items, node))
    if bare:
        ctx.add(f"{bare}.Mask", thicken(line, w + 2 * ctx.bare_margin(node, w)), kind + " mask openings")
