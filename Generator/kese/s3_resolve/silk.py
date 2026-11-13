"""Silkscreen: the ink clipped to the outline and off the open bores, off the mask openings too
unless SilkScreen.SILKSCREEN_OVER_COPPER, and kept as far from the edge as the mask."""
from kese.core import shapes2d as sh
from kese.core.shapes2d import union
from kese.s3_resolve.holes import bores
from kese.s3_resolve.mask import pulled_back
from parameters import P


def clip_silk(r, items, outline_k, openings):
    """r.silk per side, board frame; `openings` are the mask openings in KiCad's frame."""
    last = len(items.layers) - 1
    for side in ("F", "B"):
        silk = union(items.silk_items[side]).intersection(outline_k).difference(
            bores(r, lambda h: h.i == 0) if side == "F" else bores(r, lambda h: h.j == last))
        if not P.SilkScreen.SILKSCREEN_OVER_COPPER:      # no ink where there is no mask (openings, bare copper)
            silk = silk.difference(openings[side])
        silk = r.to_board_T(silk)
        if P.SolderMask.MASK_EDGE_PULLBACK_MM > 0 and not silk.is_empty:   # the same edge clearance as the mask
            silk = sh.inter(silk, pulled_back(r))
        r.silk[side] = silk
