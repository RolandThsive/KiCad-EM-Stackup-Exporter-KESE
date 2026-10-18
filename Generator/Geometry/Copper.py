"""Copper.py - every copper layer (per net) and the plating of every hole."""
from Generator.Common import shapes as sh
from Parameters import P


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
        r = sh.snap(region.buffer(-inset, join_style="mitre")) if inset > 0 else region
        out.append((r, z0 + t * s / n, z0 + t * (s + 1) / n))
    return out


def build(b, ps):
    st, R, C = b.stackup, P.Run, P.Copper
    last = len(b.layers) - 1
    for k, l in enumerate(b.layers):
        lo, hi = st.band[l]
        outer = k in (0, last)
        etched = C.ETCH_FACTOR > 0 and (outer or C.ETCH_APPLY_TO_INNER_LAYERS)
        foot_at_bottom = (k == 0) or (not outer and k <= last / 2)   # foot on the laminate / toward the centre
        for net, region in b.copper[l].items():
            props = {"layer": l, "net": net, "thickness_mm": round(hi - lo, 6),
                     "conductivity_S_per_m": C.COPPER_CONDUCTIVITY_S_PER_M,
                     "surface_roughness_um": C.COPPER_SURFACE_ROUGHNESS_UM,
                     "foil_mm": st.copper_thickness[l],
                     "plating_added_mm": C.OUTER_PLATING_ADDED_MM if outer else 0.0}
            pieces = _slices(region, lo, hi, foot_at_bottom) if etched else [(region, lo, hi)]
            for r, z0, z1 in pieces:
                ps.add(part_name(R.COPPER_GROUPING, net, l), "copper", r, z0, z1, layer=l, net=net, props=props)
    for ring, i, j, net in b.barrels:
        # the barrel runs between the copper layers it joins; within a copper layer's own band the
        # ring area belongs to that layer's copper (it caps the barrel), so the solids only touch
        # outer layers cap the barrel (their copper covers the ring area); inner layers are
        # drilled through, so the barrel continues through their band
        hi = st.band[b.layers[i]][0] if i == 0 else st.band[b.layers[i]][1]
        lo = st.band[b.layers[j]][1] if j == last else st.band[b.layers[j]][0]
        props = {"layer": f"{b.layers[i]}-{b.layers[j]}", "net": net,
                 "conductivity_S_per_m": C.COPPER_CONDUCTIVITY_S_PER_M}
        ps.add(part_name(R.COPPER_GROUPING, net, f"{b.layers[i]}-{b.layers[j]}", plating=True),
               "plating", ring, lo, hi, layer=f"{b.layers[i]}-{b.layers[j]}", net=net, props=props)
