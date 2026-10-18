"""SolderMask.py - top and bottom solder mask, conformal over the copper.

KiCad's mask layers are negative: the mask is  outline - openings - open bores,  pulled back
from the board edge.  It is MASK_OVER_LAMINATE_MM thick on bare laminate and
MASK_OVER_COPPER_MM thick on top of copper, with a wall where it climbs over a trace."""
from Generator.Common import shapes as sh
from Parameters import P


def thicknesses(st):
    M = P.SolderMask
    if M.USE_STACKUP_MASK_THICKNESS and st.mask_thickness:
        return st.mask_thickness, st.mask_thickness, "stackup"
    return M.MASK_OVER_LAMINATE_MM, M.MASK_OVER_COPPER_MM, "SolderMask_Parameters"


def mask_region(b, side):
    M = P.SolderMask
    region = sh.diff(sh.diff(b.outline, b.bores_side[side]), b.mask_open[side])
    if M.MASK_EDGE_PULLBACK_MM > 0:
        inset = sh.snap(b.outline.buffer(-M.MASK_EDGE_PULLBACK_MM, quad_segs=M.MASK_WALL_QUAD_SEGS * 2))
        region = sh.inter(region, inset)
    return region


def build(b, ps, mode):
    st, M = b.stackup, P.SolderMask
    t_lam, t_cu, src = thicknesses(st)
    ps.notes.append(f"solder mask: {t_lam} mm over laminate, {t_cu} mm over copper ({src})")
    for side, layer, sign, tb in (("F", "F.Cu", 1, "Top"), ("B", "B.Cu", -1, "Bottom")):
        region = mask_region(b, side)
        if region.is_empty:
            continue
        cu = b.copper_all.get(layer, sh.EMPTY)
        cu_lo, cu_hi = st.band[layer]
        cu_t = cu_hi - cu_lo
        base = st.half                         # laminate face
        flat, top, wall = sh.conformal_regions(region, cu, t_lam, M.MASK_WALL_QUAD_SEGS)
        part = f"{tb} Solder Mask"
        over = f"{tb} Mask over Copper" if mode == "pretty" else part
        props = {"side": side, "thickness_over_laminate_mm": t_lam, "thickness_over_copper_mm": t_cu}
        z = lambda v: sign * v
        ps.add(part, "mask", flat, z(base), z(base + t_lam), layer=f"{side}.Mask", props=props)
        ps.add(over, "mask_over_copper", top, z(base + cu_t), z(base + cu_t + t_cu), layer=f"{side}.Mask", props=props)
        ps.add(part, "mask", wall, z(base), z(base + cu_t + t_cu), layer=f"{side}.Mask", props=props)
