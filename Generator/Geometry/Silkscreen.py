"""Silkscreen.py - legend ink printed on the solder mask surface."""
from Generator.Common import shapes as sh
from Generator.Geometry.SolderMask import mask_region, thicknesses
from Parameters import P


def build(b, ps):
    st, S, M = b.stackup, P.Silkscreen, P.SolderMask
    t_silk = S.SILK_THICKNESS_MM
    t_lam, t_cu, _ = thicknesses(st)
    for side, layer, sign, tb in (("F", "F.Cu", 1, "Top"), ("B", "B.Cu", -1, "Bottom")):
        silk = b.silk.get(side, sh.EMPTY)
        if M.MASK_EDGE_PULLBACK_MM > 0 and not silk.is_empty:   # silk keeps the same edge clearance as the mask
            silk = sh.inter(silk, sh.snap(b.outline.buffer(-M.MASK_EDGE_PULLBACK_MM, quad_segs=M.MASK_WALL_QUAD_SEGS * 2)))
        if silk.is_empty:
            continue
        cu = b.copper_all.get(layer, sh.EMPTY)
        cu_t = st.band[layer][1] - st.band[layer][0]
        base = st.half
        part = f"{tb} Silkscreen"
        props = {"side": side, "thickness_mm": t_silk}
        z = lambda v: sign * v
        masked = mask_region(b, side)
        # where the ink leaves the mask (openings that keep their silk) it steps down the mask edge
        off_mask, on_mask, step = sh.conformal_regions(silk, masked, t_silk, M.MASK_WALL_QUAD_SEGS)
        ps.add(part, "silk", step, z(base), z(base + t_lam + t_silk), layer=f"{side}.SilkS", props=props)
        # on the mask: the mask's surface is flat on laminate and raised over copper and the mask's
        # own wall beside it; the ink climbs that step with a wall of its own, t_silk wide
        raised = sh.snap(cu.buffer(t_lam, quad_segs=M.MASK_WALL_QUAD_SEGS)) if not cu.is_empty else cu
        flat, top, wall = sh.conformal_regions(on_mask, raised, t_silk, M.MASK_WALL_QUAD_SEGS)
        ps.add(part, "silk", flat, z(base + t_lam), z(base + t_lam + t_silk), layer=f"{side}.SilkS", props=props)
        ps.add(part, "silk", top, z(base + cu_t + t_cu), z(base + cu_t + t_cu + t_silk), layer=f"{side}.SilkS", props=props)
        ps.add(part, "silk", wall, z(base + t_lam), z(base + cu_t + t_cu + t_silk), layer=f"{side}.SilkS", props=props)
        # off the mask (openings, when the file keeps silk there): directly on laminate / copper
        if not off_mask.is_empty:
            on_cu, on_lam = sh.inter(off_mask, cu), sh.diff(off_mask, cu)
            ps.add(part, "silk", on_lam, z(base), z(base + t_silk), layer=f"{side}.SilkS", props=props)
            ps.add(part, "silk", on_cu, z(base + cu_t), z(base + cu_t + t_silk), layer=f"{side}.SilkS", props=props)
