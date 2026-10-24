"""Tracks: straight segments and arcs, each the stroke of its width on one copper layer."""
from shapely.geometry import LineString

from kese.core.sexp import child, layer_of, num, pt
from kese.core.shapes2d import arc3, thicken
from kese.s2_collect.nets import net_name


def add_track(ctx, node):
    """(segment ...) or (arc ...) -> copper of its net."""
    if node[0] == "segment":
        line = LineString([pt(child(node, "start")), pt(child(node, "end"))])
    else:
        line = LineString(arc3(pt(child(node, "start")), pt(child(node, "mid")), pt(child(node, "end"))))
    ctx.add(layer_of(node), thicken(line, num(node, "width", 0.0)),
            "tracks" if node[0] == "segment" else "arc tracks", net_name(ctx.items, node))
