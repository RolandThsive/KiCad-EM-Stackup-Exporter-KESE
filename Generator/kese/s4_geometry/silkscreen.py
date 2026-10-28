"""Silkscreen: legend ink printed on the solder mask surface."""
from kese.core import shapes2d as sh
from kese.core.conformal import conformal_regions, grow, near
from kese.s4_geometry.heights import mask_thicknesses
from parameters import P


def build(r, ps):
    st, S, M = r.stackup, P.Silkscreen, P.SolderMask
    t_silk = S.SILK_THICKNESS_MM
    t_lam, t_cu, _ = mask_thicknesses(st)
    for side, layer, sign, tb in (("F", "F.Cu", 1, "Top"), ("B", "B.Cu", -1, "Bottom")):
        silk = r.silk.get(side, sh.EMPTY)
        if silk.is_empty:
            continue
        # only the copper the ink can reach matters: what lies farther than t_lam + t_silk is left out
        cu = near(r.copper_all.get(layer, sh.EMPTY), silk, t_lam + t_silk + 8 * sh.grid())
        cu_t = st.band[layer][1] - st.band[layer][0]
        base = st.half
        part = f"{tb} Silkscreen"
        props = {"side": side, "thickness_mm": t_silk}
        z = lambda v: sign * v
        masked = r.mask[side]
        # the mask's surface is flat on laminate and raised over copper and the mask's own wall beside it
        raised = grow(cu, t_lam, M.MASK_WALL_QUAD_SEGS) if not cu.is_empty else cu
        # where the ink leaves the mask (openings that keep their silk) it steps down the mask edge,
        # from the mask's surface beside it down to the copper or the laminate under it
        off_mask, on_mask, step = conformal_regions(silk, masked, t_silk, M.MASK_WALL_QUAD_SEGS, around="region")
        step_cu, step_off = sh.inter(step, cu), sh.diff(step, cu)
        step_raised, step_flat = sh.inter(step_off, raised), sh.diff(step_off, raised)
        ps.add(part, "silk", step_cu, z(base + cu_t), z(base + cu_t + t_cu + t_silk), layer=f"{side}.SilkS", props=props)
        ps.add(part, "silk", step_raised, z(base), z(base + cu_t + t_cu + t_silk), layer=f"{side}.SilkS", props=props)
        ps.add(part, "silk", step_flat, z(base), z(base + t_lam + t_silk), layer=f"{side}.SilkS", props=props)
        # on the mask: the ink climbs the mask's raised surface with a wall of its own, t_silk wide
        flat, top, wall = conformal_regions(on_mask, raised, t_silk, M.MASK_WALL_QUAD_SEGS, around="region")
        ps.add(part, "silk", flat, z(base + t_lam), z(base + t_lam + t_silk), layer=f"{side}.SilkS", props=props)
        ps.add(part, "silk", top, z(base + cu_t + t_cu), z(base + cu_t + t_cu + t_silk), layer=f"{side}.SilkS", props=props)
        ps.add(part, "silk", wall, z(base + t_lam), z(base + cu_t + t_cu + t_silk), layer=f"{side}.SilkS", props=props)
        # off the mask (openings, when the file keeps silk there): directly on laminate / copper
        if not off_mask.is_empty:
            on_cu, on_lam = sh.inter(off_mask, cu), sh.diff(off_mask, cu)
            ps.add(part, "silk", on_lam, z(base), z(base + t_silk), layer=f"{side}.SilkS", props=props)
            ps.add(part, "silk", on_cu, z(base + cu_t), z(base + cu_t + t_silk), layer=f"{side}.SilkS", props=props)
