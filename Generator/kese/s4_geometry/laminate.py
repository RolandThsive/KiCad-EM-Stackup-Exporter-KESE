"""The laminate: one prism per dielectric layer (core / prepreg), drilled where holes pass, with
pockets where inner copper sits (filled by resin, i.e. by the neighbouring prepreg).  Where a
counterbore or countersink (KiCad 10) cuts a dielectric or the resin beside inner copper part of
the way through, the laminate near it is cut in stretches between the heights where the cut changes."""
from kese.core import shapes2d as sh
from kese.core.shapes2d import union
from kese.s3_resolve.heights import dielectric_z
from kese.s3_resolve.holes import stretches
from parameters import P


def cut_slab(region, lo, hi, cuts):
    """[(region, z0, z1)]: a dielectric less the cuts [(z0, z1, disk)] between their heights: the
    dielectric less every disk over its whole height, and the dielectric under the disks stretch by
    stretch, less the disks that cut that stretch; neighbouring stretches cut alike are one."""
    if not cuts:
        return [(region, lo, hi)]
    under = union([d for *_, d in cuts])
    out = [(sh.diff(region, under), lo, hi)] + stretches(sh.inter(region, under), lo, hi, cuts)
    return [(g, a, b) for g, a, b in out if not g.is_empty]


def build(r, ps):
    """r: Regions.  ps: PrismSet to add to."""
    st, B = r.stackup, P.Board
    merged = B.DIELECTRIC_GROUPING == "merged"

    def add(d, region, lo, hi, cuts, **more):     # dielectric d's laminate from lo to hi
        props = {"kind": d.kind, "material": d.material, "thickness_mm": round(hi - lo, 6),
                 "epsilon_r": d.epsilon_r, "loss_tangent": d.loss_tangent, **more}
        for g, z0, z1 in cut_slab(region, lo, hi, cuts):
            ps.add("Board" if merged else f"Board_{d.name}", "board", g, z0, z1, layer=d.name, props=props)
    for i, d in enumerate(st.dielectrics):
        lo, hi = dielectric_z(st, i)
        add(d, r.slab[i], lo, hi, r.slab_cuts.get(i, []), between=[d.above, d.below])
    if not B.RESIN_FILL_BETWEEN_INNER_COPPER:
        ps.notes.append("inner copper pockets left empty (RESIN_FILL_BETWEEN_INNER_COPPER = False)")
        return
    # laminate beside each inner copper layer: resin from the adjacent prepreg (else the dielectric above)
    for k, l in enumerate(st.copper_layers[1:-1], start=1):
        above, below = st.dielectrics[k - 1], st.dielectrics[k]
        d = below if below.kind == "prepreg" and above.kind != "prepreg" else above
        add(d, r.band_laminate.get(l), *st.band[l], r.band_cuts.get(l, []), resin_fill_beside=l)
