"""Solder mask: the openings (the pads' openings from the file, plus the vias that are not
tented, SolderMask.VIA_TENTING), and the region the mask covers."""
import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.graph import connected_components, pairs_within
from kese.core.parallel import in_parallel
from kese.core.shape_copies import own
from kese.core.shapes2d import union
from parameters import P


def via_openings(items):
    """Mask openings over the vias that are not tented, KiCad frame."""
    M = P.SolderMask
    out = {"F": [], "B": []}
    for pad, span, tent in items.via_tenting:
        for side, layer in (("F", "F.Cu"), ("B", "B.Cu")):
            tented = {"file": tent[side], "tented": True, "open": False}[M.VIA_TENTING]
            if layer in span and not tented:
                out[side].append(pad.buffer(items.mask_clearance) if items.mask_clearance else pad)
    return out


def mask_openings(r, items, outline_k):
    """r.mask_open per side, board frame; returns the openings in KiCad's frame, for the silk."""
    vo = via_openings(items)
    openings = {}
    for side in ("F", "B"):
        openings[side] = without_specks(min_width_joined(items, union(items.mask_open_items[side] + vo[side]), side),
                                        items, side)
        r.mask_open[side] = r.to_board_T(openings[side].intersection(outline_k))
    return openings


def without_specks(openings, items, side):
    """The openings without those narrower than twice SolderMask.MASK_OPENING_HAIRLINE_MM everywhere."""
    h = P.SolderMask.MASK_OPENING_HAIRLINE_MM
    parts = shapely.get_parts(sh.polys_only(openings))
    if h <= 0 or not len(parts):
        return openings
    maybe = np.flatnonzero(shapely.area(parts) <= h * shapely.length(parts))   # only those can be that thin
    speck = maybe[shapely.is_empty(shapely.buffer(parts[maybe], -h))]
    if not len(speck):
        return openings
    items.found[f"mask openings narrower than {2 * h:g} mm left out on {side}.Mask"] += len(speck)
    return sh.as_region(list(np.delete(parts, speck)))


def min_width_joined(items, openings, side):
    """The openings with every mask web narrower than the board's solder_mask_min_width taken out,
    as KiCad plots the mask (plot_board_layers.cpp, GenerateLayerPoly): every opening grown by half
    the width less 1 nm, joined, shrunk back (corners chamfered), and the exact openings added back.
    Done group by group (web_groups), Parallel.WORKERS groups at a time in threads: the same webs
    as the whole layer at once, with the same vertices, in about half the time on CIAA ACC."""
    w = items.mask_min_width
    if w <= 0 or openings.is_empty:
        return openings
    grow = w / 2 - 1e-6
    webs = [p for found in in_parallel(lambda group: webs_of(own(group), grow), web_groups(openings, w))
            for p in found]
    if not webs:
        return openings
    items.found[f"mask webs under the min width ({w} mm) removed on {side}.Mask"] += len(webs)
    return union([openings] + webs)


def web_groups(openings, w):
    """The openings in groups: two openings within w of each other are in one group, and so are
    chains of them.  A web narrower than w closes only between openings of one group (or in one
    opening's own notch), since two openings grown by less than w/2 meet only when they are less
    than w apart."""
    parts = shapely.get_parts(sh.polys_only(openings))
    a, b = pairs_within(parts, w)
    label = connected_components(len(parts), a, b)[1]
    order = np.argsort(label, kind="stable")
    return [sh.as_region(list(parts[g])) for g in np.split(order, np.flatnonzero(np.diff(label[order])) + 1)]


def webs_of(openings, grow):
    """The webs the min width fills among a group of openings: grown by `grow`, joined, shrunk back,
    less the openings.  Only the webs: the hairlines where the grown and shrunk curves miss the exact
    ones are not openings KiCad makes (it adds the exact shapes back for that), and would only add
    slivers."""
    joined = openings.buffer(grow, join_style="bevel").buffer(-grow, join_style="bevel")
    return [p for p in shapely.get_parts(sh.diff(joined, openings))
            if p.geom_type == "Polygon" and not p.buffer(-P.SolderMask.MASK_WEB_HAIRLINE_MM).is_empty]


def mask_regions(r):
    """r.mask per side, board frame: KiCad's mask layers are negative, so the mask is the outline
    minus the open bores and the openings, pulled back from the edge by MASK_EDGE_PULLBACK_MM.  A
    covered via (KiCad 10) has mask over its bore even in an opening, which the opening then leaves."""
    M = P.SolderMask
    for side in ("F", "B"):
        region = sh.diff(sh.diff(r.outline, r.bores_side[side]), r.mask_open[side])
        cover = r.covered.get(side, sh.EMPTY)
        if not cover.is_empty:
            region = sh.polys_only(shapely.union_all([region, sh.snap(cover)], grid_size=sh.grid()))
            r.mask_open[side] = sh.diff(r.mask_open[side], cover)
        if M.MASK_EDGE_PULLBACK_MM > 0:
            region = sh.inter(region, pulled_back(r))
        r.mask[side] = region


def pulled_back(r):
    """The outline shrunk by MASK_EDGE_PULLBACK_MM: how close mask and silk come to the edge."""
    M = P.SolderMask
    return sh.snap(r.outline.buffer(-M.MASK_EDGE_PULLBACK_MM, quad_segs=M.MASK_WALL_QUAD_SEGS * 2))
