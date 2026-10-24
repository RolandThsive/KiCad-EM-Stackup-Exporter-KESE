"""Copper: every copper layer, per net, optionally with the etch-factor slope on its walls."""
from kese.core import shapes2d as sh
from parameters import P


def part_name(grouping, net, layer, plating=False):
    if grouping == "net":
        return f"Copper_{net}"
    if grouping == "layer":
        return "Plating" if plating else f"Copper_{layer}"
    return "Copper"


def _slices(region, z0, z1, foot_at_bottom):
    """Etch-factor trapezoid as stacked slices: inset grows from the foot toward the free face."""
    C = P.Copper
    t = z1 - z0
    n = max(1, int(C.ETCH_STEPS)) if C.ETCH_FACTOR > 0 else 1
    out = []
    for s in range(n):
        f = (s + 0.5) / n if foot_at_bottom else 1 - (s + 0.5) / n
        inset = C.ETCH_FACTOR * t * f
        g = sh.snap(region.buffer(-inset, join_style="mitre")) if inset > 0 else region
        out.append((g, z0 + t * s / n, z0 + t * (s + 1) / n))
    return out


def build(r, ps):
    st, R, C = r.stackup, P.Run, P.Copper
    last = len(r.layers) - 1
    for k, l in enumerate(r.layers):
        lo, hi = st.band[l]
        outer = k in (0, last)
        etched = C.ETCH_FACTOR > 0 and (outer or C.ETCH_APPLY_TO_INNER_LAYERS)
        foot_at_bottom = (k == 0) or (not outer and k <= last / 2)   # foot on the laminate / toward the centre
        for net, region in r.copper[l].items():
            props = {"layer": l, "net": net, "thickness_mm": round(hi - lo, 6),
                     "conductivity_S_per_m": C.COPPER_CONDUCTIVITY_S_PER_M,
                     "surface_roughness_um": C.COPPER_SURFACE_ROUGHNESS_UM,
                     "foil_mm": st.copper_thickness[l],
                     "plating_added_mm": C.OUTER_PLATING_ADDED_MM if outer else 0.0}
            pieces = _slices(region, lo, hi, foot_at_bottom) if etched else [(region, lo, hi)]
            for g, z0, z1 in pieces:
                ps.add(part_name(R.COPPER_GROUPING, net, l), "copper", g, z0, z1, layer=l, net=net, props=props)
