"""Plating: the barrel of every plated hole (and the plated board edge), between the copper
layers it joins (s3_resolve/holes.py barrel_span), less what post machining and backdrills cut."""
from kese.s3_resolve.holes import barrel_span
from kese.s4_geometry.copper import part_name
from parameters import P


def build(r, ps):
    C = P.Copper
    pieces = [(ring, *barrel_span(r.stackup, r.layers, i, j), i, j, net) for ring, i, j, net in r.barrels]
    for ring, lo, hi, i, j, net in pieces + r.barrel_pieces:
        span = f"{r.layers[i]}-{r.layers[j]}"
        props = {"layer": span, "net": net, "conductivity_S_per_m": C.COPPER_CONDUCTIVITY_S_PER_M,
                 "material": C.COPPER_MATERIAL}
        ps.add(part_name(C.COPPER_GROUPING, net, span, plating=True), "plating", ring, lo, hi,
               layer=span, net=net, props=props)
