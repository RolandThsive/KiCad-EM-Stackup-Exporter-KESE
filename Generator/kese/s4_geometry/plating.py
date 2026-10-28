"""Plating: the barrel of every plated hole (and the plated board edge), between the copper
layers it joins."""
from kese.s4_geometry.copper import part_name
from parameters import P


def build(r, ps):
    st, R, C = r.stackup, P.Run, P.Copper
    last = len(r.layers) - 1
    for ring, i, j, net in r.barrels:
        # the barrel runs between the copper layers it joins; within a copper layer's own band the
        # ring area belongs to that layer's copper (it caps the barrel), so the solids only touch
        # outer layers cap the barrel (their copper covers the ring area); inner layers are
        # drilled through, so the barrel continues through their band
        hi = st.band[r.layers[i]][0] if i == 0 else st.band[r.layers[i]][1]
        lo = st.band[r.layers[j]][1] if j == last else st.band[r.layers[j]][0]
        props = {"layer": f"{r.layers[i]}-{r.layers[j]}", "net": net,
                 "conductivity_S_per_m": C.COPPER_CONDUCTIVITY_S_PER_M}
        ps.add(part_name(R.COPPER_GROUPING, net, f"{r.layers[i]}-{r.layers[j]}", plating=True),
               "plating", ring, lo, hi, layer=f"{r.layers[i]}-{r.layers[j]}", net=net, props=props)
