"""Solder mask, top and bottom, conformal over the copper: MASK_OVER_LAMINATE_MM thick on bare
laminate and MASK_OVER_COPPER_MM on top of copper, with a wall where it climbs over a trace.
Where the mask is comes from stage 3 (Regions.mask)."""
from kese.core import shapes2d as sh
from kese.s4_geometry.heights import mask_thicknesses
from parameters import P


def build(r, ps, mode):
    st, M = r.stackup, P.SolderMask
    t_lam, t_cu, src = mask_thicknesses(st)
    ps.notes.append(f"solder mask: {t_lam} mm over laminate, {t_cu} mm over copper ({src})")
    for side, layer, sign, tb in (("F", "F.Cu", 1, "Top"), ("B", "B.Cu", -1, "Bottom")):
        region = r.mask[side]
        if region.is_empty:
            continue
        cu = r.copper_all.get(layer, sh.EMPTY)
        cu_lo, cu_hi = st.band[layer]
        cu_t = cu_hi - cu_lo
        base = st.half                         # laminate face
        flat, top, wall = sh.conformal_regions(region, cu, t_lam, M.MASK_WALL_QUAD_SEGS)
        part = f"{tb} Solder Mask"
        over = f"{tb} Mask over Copper" if mode == "visual" else part
        props = {"side": side, "thickness_over_laminate_mm": t_lam, "thickness_over_copper_mm": t_cu}
        z = lambda v: sign * v
        ps.add(part, "mask", flat, z(base), z(base + t_lam), layer=f"{side}.Mask", props=props)
        ps.add(over, "mask_over_copper", top, z(base + cu_t), z(base + cu_t + t_cu), layer=f"{side}.Mask", props=props)
        ps.add(part, "mask", wall, z(base), z(base + cu_t + t_cu), layer=f"{side}.Mask", props=props)
