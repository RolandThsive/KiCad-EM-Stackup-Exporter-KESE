"""Boards 1 to 5: slotted and round holes, through, blind, buried and micro vias."""
from common import at, new_board
from footprints7 import footprint, pad, text
from kicad7 import copper_names, segment, via

THT = ("*.Cu", "*.Mask")


def ref(s, y=-2.5):
    return text("reference", s, (0, y), "F.SilkS", size=1, thickness=0.15)


def holes_slotted():
    """Plated and non-plated slots: horizontal, vertical, rotated pad, rotated and flipped
    footprint, rectangular pad, long slot, a slot as wide as it is long, an offset slot."""
    b = new_board("holes_slotted", 2, (40, 26))
    oval = ("oval", 1.8, 0.8)
    pads = [pad("1", "thru_hole", "oval", (0, 0), (2.6, 1.6), THT, drill=oval, net="SLOT_H"),
            pad("2", "thru_hole", "oval", (5, 0), (1.6, 2.6), THT, drill=("oval", 0.8, 1.8), net="SLOT_V"),
            pad("3", "thru_hole", "oval", (10, 0), (2.6, 1.6), THT, angle=30, drill=oval, net="SLOT_ROT"),
            pad("4", "thru_hole", "rect", (15, 0), (3.0, 1.6), THT, drill=("oval", 2.2, 0.8), net="SLOT_RECT"),
            pad("5", "thru_hole", "roundrect", (21, 0), (5.0, 1.8), THT, drill=("oval", 4.0, 0.8),
                net="SLOT_LONG", rratio=0.25),
            pad("6", "thru_hole", "oval", (27, 0), (2.0, 2.0), THT, drill=("oval", 1.0, 1.0), net="SLOT_ROUND"),
            pad("7", "thru_hole", "oval", (0, 6), (2.6, 1.6), THT, drill=oval, net="SLOT_OFFSET",
                offset=(0.3, 0)),
            pad("8", "np_thru_hole", "oval", (5, 6), (2.0, 1.0), THT, drill=("oval", 2.0, 1.0)),
            pad("9", "np_thru_hole", "oval", (10, 6), (2.0, 1.0), THT, angle=60, drill=("oval", 2.0, 1.0)),
            pad("10", "thru_hole", "oval", (15, 6), (1.2, 0.8), THT, drill=("oval", 0.7, 0.35), net="SLOT_SMALL"),
            pad("11", "thru_hole", "oval", (21, 6), (2.6, 1.6), THT, drill=oval, net="SLOT_H")]
    b.add(footprint(b, "Feature:Slots", at(5, 5), children=[ref("J1")] + pads))
    route = [at(5, 5), at(5, 8), at(26, 8), at(26, 11)]              # clear of every other pad
    b.add(*[segment(b, a, c, 0.5, "B.Cu", "SLOT_H") for a, c in zip(route, route[1:])])
    b.add(footprint(b, "Feature:Slots45", at(8, 19), angle=45, children=[
        ref("J2"), pad("1", "thru_hole", "oval", (-2, 0), (2.6, 1.6), THT, drill=oval, net="SLOT_FP45"),
        pad("2", "thru_hole", "oval", (2, 0), (2.6, 1.6), THT, drill=oval, net="SLOT_FP45")]))
    b.add(segment(b, (106.585786, 117.585786), (109.414214, 120.414214), 0.5, "F.Cu", "SLOT_FP45"))
    b.add(footprint(b, "Feature:SlotBack", at(24, 19), side="B", children=[
        text("reference", "J3", (0, -2.5), "B.SilkS", justify=("mirror",)),
        pad("1", "thru_hole", "oval", (0, 0), (2.6, 1.6), THT, angle=90, drill=oval, net="SLOT_BACK")]))
    return b


def holes_round():
    """Round plated holes of several sizes and pad shapes, an offset drill, non-plated holes with
    and without a copper ring, and a plated hole in a footprint on the back."""
    b = new_board("holes_round", 2, (34, 20))
    pads = [pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="PTH_A"),
            pad("2", "thru_hole", "rect", (4, 0), (1.7, 1.7), THT, drill=1.0, net="PTH_A"),
            pad("3", "thru_hole", "circle", (9, 0), (6.0, 6.0), THT, drill=3.2, net="PTH_BIG"),
            pad("4", "thru_hole", "circle", (14, 0), (0.6, 0.6), THT, drill=0.3, net="PTH_TINY"),
            pad("5", "thru_hole", "circle", (18, 0), (2.0, 2.0), THT, drill=0.8, net="PTH_OFFSET",
                offset=(0.4, 0)),
            pad("6", "thru_hole", "roundrect", (23, 0), (2.5, 1.5), THT, drill=1.0, net="PTH_RR", rratio=0.25),
            pad("7", "np_thru_hole", "circle", (0, 8), (3.2, 3.2), THT, drill=3.2),
            pad("8", "np_thru_hole", "circle", (6, 8), (3.0, 3.0), THT, drill=2.0),
            pad("9", "np_thru_hole", "circle", (11, 8), (1.0, 1.0), THT, drill=1.0)]
    b.add(footprint(b, "Feature:Holes", at(5, 5), children=[ref("H1", -4)] + pads))
    b.add(segment(b, at(5, 5), at(9, 5), 0.6, "F.Cu", "PTH_A"))
    b.add(footprint(b, "Feature:HoleBack", at(26, 14), side="B", children=[
        text("reference", "H2", (0, -2.5), "B.SilkS", justify=("mirror",)),
        pad("1", "thru_hole", "circle", (0, 0), (1.8, 1.8), THT, drill=1.0, net="PTH_BACK")]))
    return b


def vias_through():
    """Through vias from 0.3 to 2 mm, a chain of vias on one net, vias in pads, a via on the
    board edge, a free via; vias left open in the mask (viasonmask true)."""
    b = new_board("vias_through", 2, (32, 20))
    b.setup.append("(pad_to_mask_clearance 0) (pcbplotparams (viasonmask true))")
    for x, (size, drill, net) in zip((4, 8, 12, 17, 24), ((0.3, 0.15, "V03"), (0.6, 0.3, "V06"),
                                                          (0.8, 0.4, "V08"), (1.2, 0.6, "V12"),
                                                          (2.0, 1.0, "V20"))):
        b.add(via(b, at(x, 4), size, drill, net))
    chain = [at(4, 9), at(9, 9), at(14, 9)]
    b.add(*[via(b, p, 0.8, 0.4, "GND") for p in chain])
    b.add(segment(b, chain[0], chain[1], 0.4, "F.Cu", "GND"), segment(b, chain[1], chain[2], 0.4, "B.Cu", "GND"))
    smd = ("F.Cu", "F.Paste", "F.Mask")
    b.add(footprint(b, "Feature:ViaInPad", at(8, 15), children=[
        ref("U1", -2), pad("1", "smd", "rect", (-2, 0), (1.6, 1.6), smd, net="VIP"),
        pad("2", "smd", "rect", (2, 0), (1.6, 1.6), smd, net="VIP_OFF")]))
    b.add(via(b, at(6, 15), 0.6, 0.3, "VIP"), via(b, at(10.4, 15.3), 0.6, 0.3, "VIP_OFF"))
    b.add(via(b, at(32, 12), 0.8, 0.4, "EDGE_VIA"), segment(b, at(28, 12), at(32, 12), 0.4, "F.Cu", "EDGE_VIA"))
    b.add(via(b, at(22, 15), 0.8, 0.4, "FREE", free=True))
    return b


def vias_blind_buried():
    """Six layers: a through via, blind vias from each side, a buried via, and through vias and a
    plated pad that drop their unused rings."""
    b = new_board("vias_blind_buried", 6, (32, 20))
    cu = copper_names(6)
    for x, ends, net, kind in ((4, ("F.Cu", "B.Cu"), "THRU", ""), (10, ("F.Cu", "In1.Cu"), "BLIND_TOP", "blind"),
                               (16, ("In4.Cu", "B.Cu"), "BLIND_BOT", "blind"),
                               (22, ("In1.Cu", "In4.Cu"), "BURIED", "blind")):
        p = at(x, 5)
        b.add(via(b, p, 0.6, 0.3, net, ends, kind))
        b.add(segment(b, p, (p[0] + 3, p[1]), 0.25, ends[0], net), segment(b, p, (p[0], p[1] + 3), 0.25, ends[1], net))
    rm = at(4, 14)
    b.add(via(b, rm, 0.6, 0.3, "UNUSED_RM", remove_unused=True),
          segment(b, rm, (rm[0] + 3, rm[1]), 0.25, "F.Cu", "UNUSED_RM"),
          segment(b, rm, (rm[0], rm[1] + 3), 0.25, "In2.Cu", "UNUSED_RM"))
    keep = at(11, 14)
    b.add(via(b, keep, 0.6, 0.3, "UNUSED_KEEP", remove_unused=True, keep_end=True),
          segment(b, keep, (keep[0] + 3, keep[1]), 0.25, "In3.Cu", "UNUSED_KEEP"))
    b.add(footprint(b, "Feature:PadUnused", at(20, 14), children=[
        ref("J1", -2), pad("1", "thru_hole", "circle", (0, 0), (1.6, 1.6), THT, drill=0.8, net="PAD_RM",
                           remove_unused=True)]))
    b.add(segment(b, at(20, 14), at(25, 14), 0.25, cu[1], "PAD_RM"))
    return b


def vias_micro():
    """Eight layers: microvias on each side, a stack of microvias over a buried via, and the same
    levels staggered."""
    b = new_board("vias_micro", 8, (30, 16))
    cu = copper_names(8)
    top, bottom = at(4, 5), at(9, 5)
    b.add(via(b, top, 0.3, 0.1, "MICRO_TOP", (cu[0], cu[1]), "micro"),
          segment(b, top, (top[0], top[1] + 3), 0.2, cu[1], "MICRO_TOP"))
    b.add(via(b, bottom, 0.3, 0.1, "MICRO_BOT", (cu[6], cu[7]), "micro"),
          segment(b, bottom, (bottom[0], bottom[1] + 3), 0.2, cu[6], "MICRO_BOT"))
    levels = [((cu[0], cu[1]), "micro"), ((cu[1], cu[2]), "micro"), ((cu[2], cu[5]), "blind"),
              ((cu[5], cu[6]), "micro"), ((cu[6], cu[7]), "micro")]
    stack = at(15, 5)
    b.add(*[via(b, stack, 0.6 if k == "blind" else 0.3, 0.3 if k == "blind" else 0.1, "STACK", ends, k)
            for ends, k in levels])
    p = at(21, 4)
    for i, (ends, k) in enumerate(levels):
        q_ = (p[0] + 1.0 * i, p[1] + 0.8 * i)
        b.add(via(b, q_, 0.6 if k == "blind" else 0.3, 0.3 if k == "blind" else 0.1, "STAGGER", ends, k))
        if i:
            b.add(segment(b, (p[0] + 1.0 * (i - 1), p[1] + 0.8 * (i - 1)), q_, 0.2, ends[0], "STAGGER"))
    return b


BOARDS = [holes_slotted, holes_round, vias_through, vias_blind_buried, vias_micro]
