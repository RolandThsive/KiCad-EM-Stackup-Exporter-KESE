"""Heights: the z range of every copper layer, dielectric and ply, in mm from the laminate's mid-plane
(F side positive).  Set in stage 3, where post machining and via fills are placed in them."""
from parameters import P


def finished_bands(st):
    """Fill st.band: z range of every copper layer.  The top and the bottom copper sit on the
    laminate faces, as finished (foil + Copper.TOP_ / BOTTOM_PLATING_ADDED_MM); inner copper lies inside."""
    st.half = st.laminate_thickness / 2
    outer = {"F.Cu": st.copper_thickness["F.Cu"] + P.Copper.TOP_PLATING_ADDED_MM,
             "B.Cu": st.copper_thickness["B.Cu"] + P.Copper.BOTTOM_PLATING_ADDED_MM}
    band = {"F.Cu": (st.half, st.half + outer["F.Cu"]), "B.Cu": (-st.half - outer["B.Cu"], -st.half)}
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


def ply_z(st, i):
    """[(ply, z_lo, z_hi)] of dielectric i's plies as built with the plies separate, top to bottom:
    stacked down from the dielectric's top, the last one ending at its bottom."""
    lo, z = dielectric_z(st, i)
    solids, out = st.dielectrics[i].solids, []
    for n, ply in enumerate(solids):
        bottom = lo if n == len(solids) - 1 else z - ply.thickness
        out.append((ply, bottom, z))
        z = bottom
    return out
