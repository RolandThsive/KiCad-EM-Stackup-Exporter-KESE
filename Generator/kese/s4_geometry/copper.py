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


def _slices(region, z0, z1, foot_at_bottom, unetched):
    """Etch-factor trapezoid as stacked slices: inset grows from the foot toward the free face.
    Copper edges on `unetched` (the hole walls and the board edge, board frame) are plated or cut,
    not etched: there the copper keeps its full outline, so it still meets the barrel."""
    C = P.Copper
    t = z1 - z0
    n = max(1, int(C.ETCH_STEPS))
    out = []
    for s in range(n):
        f = (s + 0.5) / n if foot_at_bottom else 1 - (s + 0.5) / n
        inset = C.ETCH_FACTOR * t * f
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


def build(r, ps):
    st, C = r.stackup, P.Copper
    last = len(r.layers) - 1
    for k, l in enumerate(r.layers):
        lo, hi = st.band[l]
        outer = k in (0, last)
        etched = C.ETCH_FACTOR > 0 and (outer or C.ETCH_APPLY_TO_INNER_LAYERS)
        foot_at_bottom = (k == 0) or (not outer and k <= last / 2)   # foot on the laminate / toward the centre
        unetched = _unetched(r, k) if etched else None
        for net, region in r.copper[l].items():
            props = {"layer": l, "net": net, "thickness_mm": round(hi - lo, 6),
                     "conductivity_S_per_m": C.COPPER_CONDUCTIVITY_S_PER_M,
                     "surface_roughness_um": C.COPPER_SURFACE_ROUGHNESS_UM,
                     "foil_mm": st.copper_thickness[l],
                     "plating_added_mm": C.OUTER_PLATING_ADDED_MM if outer else 0.0}
            pieces = _slices(region, lo, hi, foot_at_bottom, unetched) if etched else [(region, lo, hi)]
            for g, z0, z1 in pieces:
                ps.add(part_name(C.COPPER_GROUPING, net, l), "copper", g, z0, z1, layer=l, net=net, props=props)
