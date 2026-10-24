"""Heights: the z range of every copper layer and dielectric, in mm from the laminate's
mid-plane (F side positive), and the thickness of the solder mask."""
from parameters import P


def copper_bands(st, outer_copper_t):
    """Fill st.band: z range of every copper layer.  Outer copper sits on the laminate faces
    (outer_copper_t = {"F.Cu": finished thickness, "B.Cu": ...}); inner copper lies inside."""
    st.half = st.laminate_thickness / 2
    band = {"F.Cu": (st.half, st.half + outer_copper_t["F.Cu"]),
            "B.Cu": (-st.half - outer_copper_t["B.Cu"], -st.half)}
    z = st.half
    for i, d in enumerate(st.dielectrics):
        z -= d.thickness
        if i < len(st.dielectrics) - 1:
            l = d.below
            band[l] = (z - st.copper_thickness[l], z)
            z -= st.copper_thickness[l]
    st.band = band
    return band


def dielectric_z(st, i):
    """(z_lo, z_hi) of dielectric i."""
    d = st.dielectrics[i]
    hi = st.half if i == 0 else st.band[d.above][0]
    lo = -st.half if i == len(st.dielectrics) - 1 else st.band[d.below][1]
    return lo, hi


def mask_thicknesses(st):
    """(over laminate, over copper, where the values come from), mm."""
    M = P.SolderMask
    if M.USE_STACKUP_MASK_THICKNESS and st.mask_thickness:
        return st.mask_thickness, st.mask_thickness, "stackup"
    return M.MASK_OVER_LAMINATE_MM, M.MASK_OVER_COPPER_MM, "parameters/solder_mask.py"
