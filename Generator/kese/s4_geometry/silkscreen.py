"""Silkscreen: legend ink printed on the solder mask surface; the two sides at once, in threads."""
from kese.core import shapes2d as sh
from kese.core.conformal import conformal_regions, grow, near
from kese.core.parallel import in_parallel
from kese.core.shape_copies import own
from kese.s4_geometry.finish import under_mask_copper, under_mask_mm
from kese.s4_geometry.heights import mask_thicknesses
from parameters import P


def build(r, ps):
    sides = (("F", "F.Cu", 1, "Top"), ("B", "B.Cu", -1, "Bottom"))
    for (side, _, sign, tb), pieces in zip(sides, in_parallel(lambda s: ink(r, *s[:2]), sides)):   # both at once
        props = {"side": side, "thickness_mm": P.Silkscreen.SILK_THICKNESS_MM}
        for region, z0, z1 in pieces:
            ps.add(f"{tb} Silkscreen", "silk", region, sign * z0, sign * z1, layer=f"{side}.SilkS", props=props)


def ink(r, side, layer):
    """[(region, z0, z1)] of one side's ink, heights from the board's middle outward.  In a thread: the
    ink, the copper and the mask are this thread's own copies (kese/core/shape_copies.py)."""
    st, M = r.stackup, P.SolderMask
    t_silk = P.Silkscreen.SILK_THICKNESS_MM
    t_lam, t_cu, _ = mask_thicknesses(st)
    lift = under_mask_mm(st)                    # finish applied before the mask: on the copper, under the mask
    silk = own(r.silk.get(side, sh.EMPTY))
    if silk.is_empty:
        return []
    mask = own(r.mask[side])
    # only the copper the ink can reach matters: what lies farther than t_lam + t_silk is left out
    reach = t_lam + t_silk + sh.G().REACH_MARGIN_STEPS * sh.grid()
    cu = under_mask_copper(st, near(own(r.copper_all.get(layer, sh.EMPTY)), silk, reach))
    cu_t = st.band[layer][1] - st.band[layer][0] + lift
    base = st.half
    out = []

    def add(region, z0, z1):
        out.append((region, z0, z1))
    # the mask's surface is flat on laminate and raised over copper and the mask's own wall beside it
    raised = grow(cu, t_lam, quad_segs=M.MASK_WALL_QUAD_SEGS) if not cu.is_empty else cu
    # where the ink leaves the mask (openings that keep their silk) it steps down the mask edge,
    # from the mask's surface beside it down to the copper or the laminate under it
    off_mask, on_mask, step = conformal_regions(silk, mask, t_silk, M.MASK_WALL_QUAD_SEGS, around="region")
    step_cu, step_off = sh.inter(step, cu), sh.diff(step, cu)
    step_raised, step_flat = sh.inter(step_off, raised), sh.diff(step_off, raised)
    add(step_cu, base + cu_t, base + cu_t + t_cu + t_silk)
    add(step_raised, base, base + cu_t + t_cu + t_silk)
    add(step_flat, base, base + t_lam + t_silk)
    # on the mask: the ink climbs the mask's raised surface with a wall of its own, t_silk wide
    flat, top, wall = conformal_regions(on_mask, raised, t_silk, M.MASK_WALL_QUAD_SEGS, around="region")
    add(flat, base + t_lam, base + t_lam + t_silk)
    add(top, base + cu_t + t_cu, base + cu_t + t_cu + t_silk)
    add(wall, base + t_lam, base + cu_t + t_cu + t_silk)
    # off the mask (openings, when the file keeps silk there): directly on laminate / copper
    if not off_mask.is_empty:
        add(sh.diff(off_mask, cu), base, base + t_silk)
        add(sh.inter(off_mask, cu), base + cu_t, base + cu_t + t_silk)
    return out
