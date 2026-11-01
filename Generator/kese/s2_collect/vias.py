"""Vias: a ring on every copper layer they span, a plated hole, and whether each end is tented."""
from kese.core.sexp import atoms, child, children, flag, num, pt, yes
from kese.core.shapes2d import disk, union
from kese.model.items import Hole
from kese.s2_collect.left_out import count
from kese.s2_collect.nets import kicad_unescape, net_name
from parameters import P


def add_via(ctx, node):
    items, C = ctx.items, P.Copper
    x, y = pt(child(node, "at"))
    size, drill = num(node, "size"), num(node, "drill")
    if size is None or drill is None:      # KiCad 4/5: a via left at its net class's size says none
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
    items.via_pads += [((x, y), d / 2) for d in sorted({size, *(sizes[l] for l in span if l in sizes)})]
    through = i == 0 and j == len(ctx.layers) - 1
    items.found["through vias" if through else "blind/buried vias"] += 1
    tent = dict(items.tent_default)
    vt = child(node, "tenting")
    if vt is not None:
        words = atoms(vt)
        for side, key in (("F", "front"), ("B", "back")):
            c = child(vt, key)
            if c is not None:                       # KiCad 10: (tenting (front yes) (back no))
                tent[side] = yes(c[1])
            elif words:                             # KiCad 9: (tenting front back) / (tenting none): complete list
                tent[side] = key in words
    items.via_tenting.append((pad, span, tent))
    count(items, node, "vias")


def zone_layer_connections(node):
    """(layers where a zone keeps the ring, whether zones count when the ring is tested).  KiCad 7+
    writes (zone_layer_connections "In1.Cu" ...) on a pad or via with remove_unused_layers: the zone
    filler's verdict, the layers where a zone connects to it.  KiCad then flashes the ring there and,
    on the other layers, only where a track, arc, via or pad of its net meets it, not a zone
    (pad.cpp / pcb_track.cpp FlashLayer, ZLO_FORCE_FLASHED).  An older file has no such list and
    any copper counts."""
    z = child(node, "zone_layer_connections")
    if z is None:
        return set(), True
    return {str(l) for l in z[1:] if not isinstance(l, list)}, False


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


KICAD_DEFAULT_VIA = (0.6, 0.3, 0.3, 0.1)       # via size, drill, micro via size, drill (KiCad's netclass.cpp)


def net_class_via(items, net, micro):
    """The size and drill of a via that gives none: its net's class in the file (KiCad 4/5 kept net
    classes in the board), else the board setup's via_size / via_drill, else KiCad's defaults
    (PCB_VIA::GetDrillValue takes the net class's when the via has none)."""
    if not hasattr(items, "_via_classes"):
        tree = items.raw.tree
        setup = child(tree, "setup") or []
        d = KICAD_DEFAULT_VIA
        board = (num(setup, "via_size", d[0]), num(setup, "via_drill", d[1]),
                 num(setup, "uvia_size", d[2]), num(setup, "uvia_drill", d[3]))
        classes, default = {}, board
        for nc in children(tree, "net_class"):
            vals = (num(nc, "via_dia", board[0]), num(nc, "via_drill", board[1]),
                    num(nc, "uvia_dia", board[2]), num(nc, "uvia_drill", board[3]))
            for a in children(nc, "add_net"):
                classes[kicad_unescape(str(a[1]))] = vals
            if len(nc) > 1 and str(nc[1]) == "Default":     # a net in no class is in Default
                default = vals
        items._via_classes = (default, classes)
    board, classes = items._via_classes
    v = classes.get(net, board)
    return (v[2], v[3]) if micro else (v[0], v[1])


def padstack_sizes(node, copper):
    """KiCad 9+ (padstack (mode front_inner_back | custom) (layer "Inner" | "B.Cu" | "In1.Cu" (size d))):
    {copper layer: ring diameter} where it is not the via's (front) size; "Inner" is every inner layer."""
    ps = child(node, "padstack")
    out = {}
    for entry in children(ps, "layer") if ps is not None else []:
        name, d = str(entry[1]), num(entry, "size")
        if d is None:
            continue
        for l in (copper[1:-1] if name == "Inner" else [name]):
            if l in copper and l != "F.Cu":
                out[l] = d
    return out
