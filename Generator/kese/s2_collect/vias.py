"""Vias: a ring on every copper layer they span, a plated hole, and whether each end is tented."""
from kese.core.sexp import atoms, child, num, pt, yes
from kese.core.shapes2d import disk, union
from kese.model.items import Hole
from kese.s1_read.parse_kicad_version import (net_class_vias, padstack_entries, via_size, via_tenting,
                                              zone_layer_connections)
from kese.s2_collect.left_out import count_padstack
from kese.s2_collect.machining import machine
from kese.s2_collect.nets import net_name
from parameters import P

OFF_BOARD = "vias on a copper layer the board does not have"     # a damaged file
# which rings "remove unused layers" leaves (PADSTACK::UNCONNECTED_LAYER_MODE)
KEEP_ALL, REMOVE_ALL, KEEP_ENDS, ENDS_ONLY = "keep all", "remove all", "keep ends", "ends only"
# word -> (the mode it sets when on, the mode it sets on a pad when off); off, a via's word changes nothing
RING_TOKENS = {"remove_unused_layers": (REMOVE_ALL, KEEP_ALL), "keep_end_layers": (KEEP_ENDS, REMOVE_ALL),
               "start_end_only": (ENDS_ONLY, None)}


def add_via(ctx, node):
    items, C = ctx.items, P.Copper
    ends = [str(l) for l in child(node, "layers")[1:]]
    if len(ends) >= 2 and not {ends[0], ends[-1]} <= set(ctx.layers):
        items.skipped[OFF_BOARD] += 1
        return
    x, y = pt(child(node, "at"))
    net = net_name(items, node)
    size, drill = via_size(node)
    if size is None or drill is None:      # left at its net class's
        dsize, ddrill = net_class_via(items, net, "micro" in atoms(node))
        size, drill = size if size is not None else dsize, drill if drill is not None else ddrill
    span = ctx.span(ends[0], ends[-1]) if len(ends) >= 2 else ctx.layers
    pad = disk((x, y), size / 2)
    sizes = padstack_sizes(node, ctx.layers)
    mode = ring_mode(node, via=True) if C.HONOUR_REMOVE_UNUSED_LAYERS else KEEP_ALL
    forced, zones_count = zone_layer_connections(node)
    for l in span:
        ring = disk((x, y), sizes[l] / 2) if l in sizes else pad
        tip = l in (span[0], span[-1])
        if mode == ENDS_ONLY and not tip:
            items.found["via rings removed on unconnected layers"] += 1
        elif (mode == REMOVE_ALL or (mode == KEEP_ENDS and not tip)) and l not in forced:
            ctx.conditional_pads.append((l, ring, net, zones_count))
        else:
            items.copper_items[l].append((ring, net))
    i, j = ctx.layers.index(span[0]), ctx.layers.index(span[-1])
    items.holes.append(Hole(disk((x, y), drill / 2), i, j, True, net, C.VIA_WALL_MM))
    through = i == 0 and j == len(ctx.layers) - 1
    items.found["through vias" if through else "blind/buried vias"] += 1
    items.via_tenting.append((pad, span, via_tenting(node, items.tent_default)))
    count_padstack(items, node, "vias")
    machine(ctx, node, len(items.holes) - 1, (x, y), "vias")


def ring_mode(node, via):
    """Which rings of a via or through-hole pad "remove unused layers" leaves, as KiCad's parser sets it
    token by token, in the file's order: for a via each of remove_unused_layers, keep_end_layers and
    start_end_only that is on sets its mode, so keep_end_layers alone keeps the ends and makes the
    rest conditional (PCB_VIA::SetKeepStartEnd); for a pad remove_unused_layers sets "remove all" or
    "keep all" and keep_end_layers "keep ends" or "remove all" (PAD::SetRemoveUnconnected,
    SetKeepTopBottom).  A bare token, (token) and (token yes) are on, as KiCad reads them."""
    mode = KEEP_ALL
    for c in node[1:]:
        name = str(c[0] if isinstance(c, list) and c else c)
        if name not in RING_TOKENS or (name == "start_end_only" and not via):
            continue
        on_mode, pad_off = RING_TOKENS[name]
        if not isinstance(c, list) or len(c) < 2 or yes(c[1]):
            mode = on_mode
        elif not via:
            mode = pad_off
    return mode


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
                                     if net in (no_net, n) and (zones or id(g) not in ctx.zone_fills)])
            return joined[key]

        # all tested before any is added, so one conditional ring does not keep another
        kept = [(l, pad, net) for l, pad, net, zones in ctx.conditional_pads if copper(l, net, zones).intersects(pad)]
        for l, pad, net in kept:
            items.copper_items[l].append((pad, net))
        items.found["via rings removed on unconnected layers"] += len(ctx.conditional_pads) - len(kept)


def net_class_via(items, net, micro):
    """The size and drill of a via that gives none, from its net's class."""
    if items.via_classes is None:
        items.via_classes = net_class_vias(items.raw.tree, items.raw.dialect)
    default, classes = items.via_classes
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
