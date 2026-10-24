"""Vias: a ring on every copper layer they span, a plated hole, and whether each end is tented."""
from kese.core.sexp import atoms, child, flag, num, pt, yes
from kese.core.shapes2d import disk, union
from kese.model.items import Hole
from kese.s2_collect.nets import net_name
from parameters import P


def add_via(ctx, node):
    items, C = ctx.items, P.Copper
    x, y = pt(child(node, "at"))
    size, drill = num(node, "size"), num(node, "drill")
    ends = [str(l) for l in child(node, "layers")[1:]]
    span = ctx.span(ends[0], ends[-1]) if len(ends) >= 2 else ctx.layers
    net = net_name(items, node)
    pad = disk((x, y), size / 2)
    prune = C.HONOUR_REMOVE_UNUSED_LAYERS and flag(node, "remove_unused_layers")
    keep_ends = flag(node, "keep_end_layers")
    for l in span:
        if prune and not (keep_ends and l in (span[0], span[-1])):
            ctx.conditional_pads.append((l, pad, net))
        else:
            items.copper_items[l].append((pad, net))
    i, j = ctx.layers.index(span[0]), ctx.layers.index(span[-1])
    items.holes.append(Hole(disk((x, y), drill / 2), i, j, True, net, C.VIA_WALL_MM, (x, y), drill / 2))
    items.via_pads.append(((x, y), size / 2))
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


def drop_unconnected_rings(ctx):
    """Via rings that remove_unused_layers makes conditional stay only where other copper meets them."""
    items = ctx.items
    if ctx.conditional_pads:
        existing = {l: union([g for g, _ in gs]) for l, gs in items.copper_items.items()}
        kept = 0
        for l, pad, net in ctx.conditional_pads:
            if l in existing and existing[l].intersects(pad):
                items.copper_items[l].append((pad, net))
                kept += 1
        items.found["via rings removed on unconnected layers"] += len(ctx.conditional_pads) - kept
