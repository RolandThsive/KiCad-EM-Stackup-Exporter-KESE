"""Heights: the z range of every copper layer and dielectric, in mm from the laminate's mid-plane
(F side positive).  Set in stage 3, where post machining and via fills are placed in them."""
from parameters import P


def finished_bands(st):
    """st.band with the outer copper as finished: foil + Copper.OUTER_PLATING_ADDED_MM."""
    copper_bands(st, {l: st.copper_thickness[l] + P.Copper.OUTER_PLATING_ADDED_MM for l in ("F.Cu", "B.Cu")})


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


def dielectric_z(st, i):
    """(z_lo, z_hi) of dielectric i."""
    d = st.dielectrics[i]
    hi = st.half if i == 0 else st.band[d.above][0]
    lo = -st.half if i == len(st.dielectrics) - 1 else st.band[d.below][1]
    return lo, hi
