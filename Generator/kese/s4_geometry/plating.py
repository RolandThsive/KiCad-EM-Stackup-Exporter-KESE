"""Plating: the barrel of every plated hole (and the plated board edge), between the copper
layers it joins."""
from kese.s4_geometry.copper import part_name
from parameters import P


def build(r, ps):
    st, C = r.stackup, P.Copper
    last = len(r.layers) - 1
    for ring, i, j, net in r.barrels:
        # outer layers cap the barrel (their copper covers the ring area), so it stops at their face;
        # inner layers are drilled through, so the barrel continues through their band
        hi = st.band[r.layers[i]][0] if i == 0 else st.band[r.layers[i]][1]
        lo = st.band[r.layers[j]][1] if j == last else st.band[r.layers[j]][0]
        span = f"{r.layers[i]}-{r.layers[j]}"
        props = {"layer": span, "net": net, "conductivity_S_per_m": C.COPPER_CONDUCTIVITY_S_PER_M}
        ps.add(part_name(C.COPPER_GROUPING, net, span, plating=True), "plating", ring, lo, hi,
               layer=span, net=net, props=props)
