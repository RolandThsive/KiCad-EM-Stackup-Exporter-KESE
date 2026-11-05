"""Solder mask, top and bottom, conformal over the copper: MASK_OVER_LAMINATE_MM thick on bare
laminate and MASK_OVER_COPPER_MM on top of copper (on top of the finish, when the finish goes on
before the mask), with a wall where it climbs over a trace.  Where the mask is comes from stage 3
(Regions.mask).  The two sides are built at once, in threads.  Where an opening's outline follows the
copper's (a pad with no mask margin) with other points along its curves, or a grid step off, the
mask on the copper keeps slivers far thinner than a micrometre between the two: those narrower
than twice MASK_OVER_COPPER_HAIRLINE_MM are left out."""
from kese.core import shapes2d as sh
from kese.core.conformal import conformal_regions, without_hairlines
from kese.core.parallel import in_parallel
from kese.core.shape_copies import own
from kese.s4_geometry.finish import under_mask_copper, under_mask_mm
from kese.s4_geometry.heights import mask_thicknesses
from parameters import P


def build(r, ps, mode):
    st, M = r.stackup, P.SolderMask
    t_lam, t_cu, src = mask_thicknesses(st)
    lift = under_mask_mm(st)                   # finish applied before the mask lies under it, on the copper
    ps.notes.append(f"solder mask: {t_lam} mm over laminate, {t_cu} mm over copper ({src})"
                    + (f", on the finish ({lift:.6g} mm) over copper" if lift else ""))
    sides = (("F", "F.Cu", 1, "Top"), ("B", "B.Cu", -1, "Bottom"))

    def split(side):                           # (flat, top, slivers left out, wall) of one side, or None; in a
        region = own(r.mask[side[0]])          # thread, on its own copies (the two sides' shapes come from the same ones)
        if region.is_empty:
            return None
        cu = under_mask_copper(st, own(r.copper_all.get(side[1], sh.EMPTY)))
        flat, top, wall = conformal_regions(region, cu, t_lam, M.MASK_WALL_QUAD_SEGS)
        return flat, *without_hairlines(top, M.MASK_OVER_COPPER_HAIRLINE_MM), wall
    for (side, layer, sign, tb), pieces in zip(sides, in_parallel(split, sides)):   # both sides at once
        if pieces is None:
            continue
        flat, top, slivers, wall = pieces
        if slivers:
            ps.notes.append(f"solder mask: {slivers} slivers on the copper narrower than "
                            f"{2 * M.MASK_OVER_COPPER_HAIRLINE_MM:g} mm left out ({side}.Mask)")
        cu_t = st.band[layer][1] - st.band[layer][0] + lift
        base = st.half                         # laminate face
        part = f"{tb} Solder Mask"
        over = f"{tb} Mask over Copper" if mode == "visual" else part
        props = {"side": side, "thickness_over_laminate_mm": t_lam, "thickness_over_copper_mm": t_cu}
        z = lambda v: sign * v
        ps.add(part, "mask", flat, z(base), z(base + t_lam), layer=f"{side}.Mask", props=props)
        ps.add(over, "mask_over_copper", top, z(base + cu_t), z(base + cu_t + t_cu), layer=f"{side}.Mask", props=props)
        ps.add(part, "mask", wall, z(base), z(base + cu_t + t_cu), layer=f"{side}.Mask", props=props)
