"""Pads: copper on the pad's layers, its drill (plated or not) and its solder mask openings."""
from shapely import affinity
from shapely.geometry import LineString

from kese.core.sexp import atoms, child, num, numbers
from kese.core.shapes2d import EMPTY, disk, thicken
from kese.model.items import Hole
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
    layers = ctx.expand(child(pad, "layers")[1:])
    margin = num(pad, "solder_mask_margin")
    margin = margin if margin is not None else (fp_margin if fp_margin is not None else items.mask_clearance)
    last = len(ctx.layers) - 1
    if ptype == "np_thru_hole":
        if not hole.is_empty and P.Board.INCLUDE_NON_PLATED_HOLES:
            items.holes.append(Hole(hole, 0, last, False, "", 0.0, pos if round_r else None, round_r))
        items.found["non-plated holes"] += 1
    else:
        for l in layers:
            if l in ctx.layers:
                items.copper_items[l].append((shape, net))
        if ptype == "thru_hole" and not hole.is_empty:
            items.holes.append(Hole(hole, 0, last, True, net, C.PTH_WALL_MM, pos if round_r else None, round_r))
        items.found["pads"] += 1
    for side in ("F", "B"):
        if f"{side}.Mask" in layers:
            items.mask_open_items[side].append(shape.buffer(margin) if margin else shape)
            items.found[f"pad mask openings on {side}.Mask"] += 1
