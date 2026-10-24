"""Solder mask openings: the pads' openings from the file, plus the vias that are not tented
(Copper.VIA_TENTING)."""
from kese.core.shapes2d import union
from parameters import P


def via_openings(items):
    """Mask openings over the vias that are not tented, KiCad frame."""
    C = P.Copper
    out = {"F": [], "B": []}
    for pad, span, tent in items.via_tenting:
        for side, layer in (("F", "F.Cu"), ("B", "B.Cu")):
            tented = {"file": tent[side], "tented": True, "open": False}[C.VIA_TENTING]
            if layer in span and not tented:
                out[side].append(pad.buffer(items.mask_clearance) if items.mask_clearance else pad)
    return out


def mask_openings(r, items, outline_k):
    """r.mask_open per side, board frame; returns the openings in KiCad's frame, for the silk."""
    vo = via_openings(items)
    openings = {}
    for side in ("F", "B"):
        openings[side] = union(items.mask_open_items[side] + vo[side])
        r.mask_open[side] = r.to_board_T(openings[side].intersection(outline_k))
    return openings
