"""Copper: every copper layer, per net, optionally with the etch-factor slope on its walls."""
from kese.core import shapes2d as sh
from kese.s3_resolve.holes import drills
from parameters import P


def part_name(grouping, net, layer, plating=False):
    if grouping == "net":
        return f"Copper_{net}"
    if grouping == "layer":
        return "Plating" if plating else f"Copper_{layer}"
    return "Copper"


def _slices(region, z0, z1, foot_at_bottom, unetched, factor):
    """Etch-factor trapezoid as stacked slices: inset grows from the foot toward the free face.
    Copper edges on `unetched` (the hole walls and the board edge, board frame) are plated or cut,
    not etched: there the copper keeps its full outline, so it still meets the barrel."""
    C = P.Copper
    t = z1 - z0
    n = max(1, int(C.ETCH_STEPS))
    out = []
    for s in range(n):
        f = (s + 0.5) / n if foot_at_bottom else 1 - (s + 0.5) / n
        inset = factor * t * f
        g = region
        if inset > 0:
            g = region.buffer(-inset, join_style="mitre")
            if not unetched.is_empty:
                near = sh.inter(region, unetched.buffer(inset * C.ETCH_UNETCHED_REACH, join_style="mitre"))
                g = sh.union([g, near])
            g = sh.snap(g)
        out.append((g, z0 + t * s / n, z0 + t * (s + 1) / n))
    return out


def _unetched(r, k):
    """The edges copper layer k is not etched along, board frame: the drill walls of the holes
    through it and the outside of the board outline (edge plating, castellations)."""
    walls = r.to_board_T(drills(r, lambda h, k=k: h.i <= k <= h.j))
    return sh.union([walls, r.outline.boundary.buffer(1e-6)])


def position(k, last):
    """'top', 'inner' or 'bottom' for copper layer k of last + 1: its section of Copper.py."""
    return "top" if k == 0 else "bottom" if k == last else "inner"


def roughness():
    """The copper's surface roughness for the solver (materials.json): the model and its values for
    the treated face of a layer, pressed into the dielectric it was laminated on, and for the other."""
    C = P.Copper
    if C.COPPER_ROUGHNESS_MODEL == "hammerstad":
        return {"model": "hammerstad", "rms_treated_um": C.COPPER_ROUGHNESS_RMS_TREATED_UM,
                "rms_other_um": C.COPPER_ROUGHNESS_RMS_OTHER_UM}
    if C.COPPER_ROUGHNESS_MODEL == "huray":
        return {"model": "huray", "radius_treated_um": C.COPPER_HURAY_RADIUS_TREATED_UM,
                "radius_other_um": C.COPPER_HURAY_RADIUS_OTHER_UM,
                "surface_ratio_treated": C.COPPER_HURAY_SURFACE_RATIO_TREATED,
                "surface_ratio_other": C.COPPER_HURAY_SURFACE_RATIO_OTHER}
    return {"model": "none"}


def build(r, ps):
    st, C = r.stackup, P.Copper
    last = len(r.layers) - 1
    plating = {"top": C.TOP_PLATING_ADDED_MM, "inner": 0.0, "bottom": C.BOTTOM_PLATING_ADDED_MM}
    etch = {"top": C.TOP_ETCH_FACTOR, "inner": C.INNER_ETCH_FACTOR, "bottom": C.BOTTOM_ETCH_FACTOR}
    for k, l in enumerate(r.layers):
        lo, hi = st.band[l]
        where = position(k, last)
        etched = etch[where] > 0
        foot_at_bottom = (k == 0) or (where == "inner" and k <= last / 2)   # foot on the laminate / toward the centre
        unetched = _unetched(r, k) if etched else None
        # the layer's own values: a net's part lists them for every layer it lies on (s6_assemble props_of)
        own = {"layer": l, "position": where, "thickness_mm": round(hi - lo, 6), "foil_mm": st.copper_thickness[l],
               "plating_added_mm": plating[where], "etch_factor": etch[where],
               "treated_face": "lower" if foot_at_bottom else "upper"}       # the face on the laminate: the foot's
        for net, region in r.copper[l].items():
            props = {"layer": l, "net": net, "thickness_mm": round(hi - lo, 6),
                     "conductivity_S_per_m": C.COPPER_CONDUCTIVITY_S_PER_M,
                     "surface_roughness_um": C.COPPER_ROUGHNESS_RMS_TREATED_UM,
                     "foil_mm": st.copper_thickness[l],
                     "plating_added_mm": plating[where],
                     "material": C.COPPER_MATERIAL, "roughness": roughness(), "layers": [own]}
            pieces = _slices(region, lo, hi, foot_at_bottom, unetched, etch[where]) if etched else [(region, lo, hi)]
            for g, z0, z1 in pieces:
                ps.add(part_name(C.COPPER_GROUPING, net, l), "copper", g, z0, z1, layer=l, net=net, props=props)
