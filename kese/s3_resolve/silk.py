"""Silkscreen: the ink clipped to the outline and off the open bores, and off the mask openings
too unless Silkscreen.SILKSCREEN_OVER_COPPER."""
from kese.core.shapes2d import union
from kese.s3_resolve.holes import bores
from parameters import P


def clip_silk(r, items, outline_k, openings):
    """r.silk per side, board frame; `openings` are the mask openings in KiCad's frame."""
    last = len(items.layers) - 1
    for side in ("F", "B"):
        silk = union(items.silk_items[side]).intersection(outline_k).difference(
            bores(items, lambda h: h.i == 0) if side == "F" else bores(items, lambda h: h.j == last))
        if not P.Silkscreen.SILKSCREEN_OVER_COPPER:      # no ink where there is no mask (openings, bare copper)
            silk = silk.difference(openings[side])
        r.silk[side] = r.to_board_T(silk)
