"""Pads: copper on the pad's layers, its drill (plated or not) and its solder mask openings."""
from shapely import affinity
from shapely.geometry import LineString

from kese.core.sexp import atoms, child, numbers
from kese.core.shapes2d import EMPTY, disk, thicken
from kese.model.items import Hole
from kese.s1_read.parse_kicad_version import flag, mask_margin, padstack_entries, zone_layer_connections
from kese.s2_collect.left_out import count
from kese.s2_collect.nets import net_name
from kese.s2_collect.pad_shapes import pad_shape
from parameters import P


def add_pad(ctx, pad, T, fp_margin):
    items, C = ctx.items, P.Copper
    ptype = pad[2]
    count(items, pad, "pads")
    vals = numbers(child(pad, "at"))
    pos = T((vals[0], vals[1]))
    ang = vals[2] if len(vals) > 2 else 0.0            # pad angles are stored absolute
    size = child(pad, "size")
    w, h = float(size[1]), float(size[2])
    drill = child(pad, "drill")
    net = net_name(items, pad)

    def place(g, offset=(0.0, 0.0)):
        g = affinity.translate(g, *offset)
        return affinity.translate(affinity.rotate(g, -ang, origin=(0, 0)), *pos)

    offset, hole, round_r = (0.0, 0.0), EMPTY, 0.0
    if drill is not None:
        off = child(drill, "offset")
        offset = (float(off[1]), float(off[2])) if off else (0.0, 0.0)
        a = atoms(drill)
        if a and a[0] == "oval":
            dw, dh = float(a[1]), float(a[2]) if len(a) > 2 else float(a[1])
            d = abs(dw - dh) / 2
            hole = disk((0, 0), dw / 2) if d < 1e-9 else thicken(
                LineString([(-d, 0), (d, 0)] if dw > dh else [(0, -d), (0, d)]), min(dw, dh))
            round_r = dw / 2 if d < 1e-9 else 0.0
        elif a:
            hole = disk((0, 0), float(a[0]) / 2)
            round_r = float(a[0]) / 2
        hole = place(hole)
    shape = place(pad_shape(items, pad, w, h), offset if drill is not None else (0.0, 0.0))
    stack, made = padstack_layers(pad, ctx.layers), {}

    def shape_on(l):
        """The pad's shape on copper layer l: the front shape, or its padstack's shape there."""
        node = stack.get(l)
        if node is None:
            return shape
        if id(node) not in made:
            sz = child(node, "size")
            off = child(node, "offset")
            made[id(node)] = place(pad_shape(items, node, float(sz[1]), float(sz[2] if len(sz) > 2 else sz[1])),
                                   (float(off[1]), float(off[2])) if off else offset if drill is not None else (0.0, 0.0))
        return made[id(node)]

    layers = ctx.expand(child(pad, "layers")[1:])
    margin = mask_margin(pad, items.raw.dialect)
    margin = margin if margin is not None else (fp_margin if fp_margin is not None else items.mask_clearance)
    if not any(l in ctx.layers for l in layers):
        margin = 0.0        # a pad on no copper layer opens the mask as drawn (PAD::GetSolderMaskExpansion)
    elif margin < 0:        # a negative margin shrinks the opening at most to nothing, as KiCad keeps it
        margin = max(margin, -min(w, h) / 2)
    last = len(ctx.layers) - 1
    if ptype == "np_thru_hole":
        if not hole.is_empty and P.Board.INCLUDE_NON_PLATED_HOLES:
            items.holes.append(Hole(hole, 0, last, False, "", 0.0, pos if round_r else None, round_r))
        items.found["non-plated holes"] += 1
        if npth_has_copper(pad, w, h, offset, drill):     # a copper ring round the bare hole
            for l in layers:
                if l in ctx.layers:
                    items.copper_items[l].append((shape_on(l), net))
            items.found["copper rings on non-plated holes"] += 1
    else:
        # KiCad's "remove unused layers" on a through-hole pad: a ring stays only where copper meets it,
        # but on the outer layers when keep_end_layers says so (as for vias, s2_collect/vias.py)
        prune = ptype == "thru_hole" and C.HONOUR_REMOVE_UNUSED_LAYERS and flag(pad, "remove_unused_layers")
        keep = ("F.Cu", "B.Cu") if flag(pad, "keep_end_layers") else ()
        forced, zones_count = zone_layer_connections(pad)
        for l in layers:
            if l in ctx.layers:
                if prune and l not in keep and l not in forced:
                    ctx.conditional_pads.append((l, shape_on(l), net, zones_count))
                else:
                    items.copper_items[l].append((shape_on(l), net))
        if ptype == "thru_hole" and not hole.is_empty:
            items.holes.append(Hole(hole, 0, last, True, net, C.PTH_WALL_MM, pos if round_r else None, round_r))
        items.found["pads"] += 1
    for side in ("F", "B"):
        if f"{side}.Mask" in layers:
            opening = shape_on(f"{side}.Cu")              # the back opening follows the back shape
            items.mask_open_items[side].append(opening.buffer(margin) if margin else opening)
            items.found[f"pad mask openings on {side}.Mask"] += 1


def npth_has_copper(pad, w, h, offset, drill):
    """Whether a non-plated hole's pad puts copper on its copper layers, as KiCad decides
    (pad.cpp, PAD::FlashLayer): not when a round pad on a round drill, or an oval pad on an oval
    drill, is no bigger than the drill and not offset; any other pad shape does."""
    shape, a = str(pad[3]), atoms(drill) if drill is not None else []
    if not a or offset != (0.0, 0.0):
        return bool(a)
    oval = a[0] == "oval"
    dw = float(a[1] if oval else a[0])
    dh = float(a[2]) if oval and len(a) > 2 else dw
    if shape == "circle" and not oval:
        return dw < w
    if shape == "oval" and oval:
        return dw < w or dh < h
    return True


# what describes a pad's shape: a padstack layer gives its own, never the front one's
SHAPE_KEYS = {"size", "offset", "rect_delta", "roundrect_rratio", "chamfer_ratio", "chamfer", "options", "primitives"}


def padstack_layers(pad, copper):
    """{copper layer: a pad node with that layer's shape, size and options in front of the pad's
    own}, for the layers whose padstack shape is not the front one."""
    out = {}
    for layers, entry in padstack_entries(pad, copper):
        body = [c for c in entry[2:] if isinstance(c, list)]
        sh = child(entry, "shape")
        rest = [c for c in pad[4:] if not (isinstance(c, list) and c and c[0] in SHAPE_KEYS)]
        if child(entry, "size") is None:
            body.append(child(pad, "size"))
        node = ["pad", pad[1], pad[2], str(sh[1]) if sh else pad[3], *body, *rest]
        out.update((l, node) for l in layers)
    return out
