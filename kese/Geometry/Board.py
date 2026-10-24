"""Board.py - the laminate: one prism per dielectric layer (core / prepreg), drilled where holes
pass, with pockets where inner copper sits (filled by resin, i.e. by the neighbouring prepreg)."""
from parameters import P


def build(b, ps):
    """b: Breakdown (resolved).  ps: PrismSet to add to."""
    st, R, B = b.stackup, P.Run, P.Board
    merged = R.DIELECTRIC_GROUPING == "merged"
    for i, d in enumerate(st.dielectrics):
        lo, hi = st.dielectric_z(i)
        part = "Board" if merged else f"Board_{d.name}"
        props = {"kind": d.kind, "material": d.material, "thickness_mm": round(hi - lo, 6),
                 "epsilon_r": d.epsilon_r, "loss_tangent": d.loss_tangent,
                 "between": [d.above, d.below]}
        ps.add(part, "board", b.slab[i], lo, hi, layer=d.name, props=props)
    if not B.RESIN_FILL_BETWEEN_INNER_COPPER:
        ps.notes.append("inner copper pockets left empty (RESIN_FILL_BETWEEN_INNER_COPPER = False)")
        return
    # laminate beside each inner copper layer: resin from the adjacent prepreg (else the dielectric above)
    for k, l in enumerate(st.inner(), start=1):
        above, below = st.dielectrics[k - 1], st.dielectrics[k]
        d, i = (below, k) if below.kind == "prepreg" and above.kind != "prepreg" else (above, k - 1)
        part = "Board" if merged else f"Board_{d.name}"
        lo, hi = st.band[l]
        props = {"kind": d.kind, "material": d.material, "thickness_mm": round(hi - lo, 6),
                 "epsilon_r": d.epsilon_r, "loss_tangent": d.loss_tangent, "resin_fill_beside": l}
        ps.add(part, "board", b.band_laminate.get(l), lo, hi, layer=d.name, props=props)
