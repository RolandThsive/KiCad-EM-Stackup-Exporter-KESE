"""Solder mask: the openings (the pads' openings from the file, plus the vias that are not
tented, Copper.VIA_TENTING), and the region the mask covers."""
import shapely

from kese.core import shapes2d as sh
from kese.core.shapes2d import union
from parameters import P


WEB_HAIRLINE_MM = 1e-3     # a piece narrower than twice this between grown and exact openings is no web


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
        openings[side] = min_width_joined(items, union(items.mask_open_items[side] + vo[side]), side)
        r.mask_open[side] = r.to_board_T(openings[side].intersection(outline_k))
    return openings


def min_width_joined(items, openings, side):
    """The openings with every mask web narrower than the board's solder_mask_min_width taken out,
    as KiCad plots the mask (plot_board_layers.cpp, GenerateLayerPoly): every opening grown by half
    the width less 1 nm, joined, shrunk back (corners chamfered), and the exact openings added back."""
    w = items.mask_min_width
    if not w or w <= 0 or openings.is_empty:
        return openings
    grow = w / 2 - 1e-6
    joined = openings.buffer(grow, join_style="bevel").buffer(-grow, join_style="bevel")
    # only the webs: the hairlines where the grown and shrunk curves miss the exact ones are not
    # openings KiCad makes (it adds the exact shapes back for that), and would only add slivers
    webs = [p for p in shapely.get_parts(sh.diff(joined, openings))
            if p.geom_type == "Polygon" and not p.buffer(-WEB_HAIRLINE_MM).is_empty]
    if not webs:
        return openings
    items.found[f"mask webs under the min width ({w} mm) removed on {side}.Mask"] += len(webs)
    return union([openings] + webs)


def mask_regions(r):
    """r.mask per side, board frame: KiCad's mask layers are negative, so the mask is the outline
    minus the open bores and the openings, pulled back from the edge by MASK_EDGE_PULLBACK_MM."""
    M = P.SolderMask
    for side in ("F", "B"):
        region = sh.diff(sh.diff(r.outline, r.bores_side[side]), r.mask_open[side])
        if M.MASK_EDGE_PULLBACK_MM > 0:
            inset = sh.snap(r.outline.buffer(-M.MASK_EDGE_PULLBACK_MM, quad_segs=M.MASK_WALL_QUAD_SEGS * 2))
            region = sh.inter(region, inset)
        r.mask[side] = region
