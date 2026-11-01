"""Vias: a ring on every copper layer they span, a plated hole, and whether each end is tented."""
from kese.core.sexp import atoms, child, num, pt
from kese.core.shapes2d import disk, union
from kese.model.items import Hole
from kese.s1_read.parse_kicad_version import (flag, kicad_unescape, net_class_vias, overbar_markup, padstack_entries,
                                              via_size, via_tenting, zone_layer_connections)
from kese.s2_collect.left_out import count
from kese.s2_collect.nets import net_name
from parameters import P


def add_via(ctx, node):
    items, C = ctx.items, P.Copper
    x, y = pt(child(node, "at"))
    size, drill = via_size(node)
    if size is None or drill is None:      # left at its net class's
        dsize, ddrill = net_class_via(items, net_name(items, node), "micro" in atoms(node))
        size, drill = size if size is not None else dsize, drill if drill is not None else ddrill
    ends = [str(l) for l in child(node, "layers")[1:]]
    span = ctx.span(ends[0], ends[-1]) if len(ends) >= 2 else ctx.layers
    net = net_name(items, node)
    pad = disk((x, y), size / 2)
    sizes = padstack_sizes(node, ctx.layers)
    prune = C.HONOUR_REMOVE_UNUSED_LAYERS and flag(node, "remove_unused_layers")
    keep_ends = flag(node, "keep_end_layers")
    ends_only = C.HONOUR_REMOVE_UNUSED_LAYERS and flag(node, "start_end_only")
    forced, zones_count = zone_layer_connections(node)
    for l in span:
        ring = disk((x, y), sizes[l] / 2) if l in sizes else pad
        if ends_only and l not in (span[0], span[-1]):
            items.found["via rings removed on unconnected layers"] += 1
        elif prune and not (keep_ends and l in (span[0], span[-1])) and l not in forced:
            ctx.conditional_pads.append((l, ring, net, zones_count))
        else:
            items.copper_items[l].append((ring, net))
    i, j = ctx.layers.index(span[0]), ctx.layers.index(span[-1])
    items.holes.append(Hole(disk((x, y), drill / 2), i, j, True, net, C.VIA_WALL_MM, (x, y), drill / 2))
    through = i == 0 and j == len(ctx.layers) - 1
    items.found["through vias" if through else "blind/buried vias"] += 1
    items.via_tenting.append((pad, span, via_tenting(node, items.tent_default)))
    count(items, node, "vias")


def drop_unconnected_rings(ctx):
    """Pad and via rings that remove_unused_layers makes conditional stay only where copper of
    their net meets them (any copper, for a ring with no net)."""
    items, no_net = ctx.items, P.Copper.NO_NET_NAME
    if ctx.conditional_pads:
        joined = {}

        def copper(l, net, zones):
            key = (l, net, zones)
            if key not in joined:
                joined[key] = union([g for g, n in items.copper_items.get(l, [])
                                     if (net == no_net or n == net) and (zones or id(g) not in ctx.zone_fills)])
            return joined[key]

        # all tested before any is added, so one conditional ring does not keep another
        kept = [(l, pad, net) for l, pad, net, zones in ctx.conditional_pads if copper(l, net, zones).intersects(pad)]
        for l, pad, net in kept:
            items.copper_items[l].append((pad, net))
        items.found["via rings removed on unconnected layers"] += len(ctx.conditional_pads) - len(kept)


def net_class_via(items, net, micro):
    """The size and drill of a via that gives none, from its net's class."""
    if not hasattr(items, "_via_classes"):
        d = items.raw.dialect
        items._via_classes = net_class_vias(items.raw.tree, lambda s: kicad_unescape(overbar_markup(s, d)))
    default, classes = items._via_classes
    v = classes.get(net, default)
    return (v[2], v[3]) if micro else (v[0], v[1])


def padstack_sizes(node, copper):
    """{copper layer: ring diameter} where a via's padstack gives a size other than its own."""
    out = {}
    for layers, entry in padstack_entries(node, copper):
        d = num(entry, "size")
        if d is not None:
            out.update((l, d) for l in layers)
    return out
