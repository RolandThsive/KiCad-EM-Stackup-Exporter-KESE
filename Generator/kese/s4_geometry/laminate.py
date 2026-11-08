"""The laminate: one prism per dielectric layer (core / prepreg), drilled where holes pass, with
pockets where inner copper sits (filled by resin, i.e. by the neighbouring prepreg).  Where a
counterbore or countersink (KiCad 10) cuts a dielectric or the resin beside inner copper part of
the way through, the laminate near it is cut in stretches between the heights where the cut changes."""
from kese.core import shapes2d as sh
from kese.core.shapes2d import union
from kese.s3_resolve.heights import dielectric_z
from parameters import P


def cut_slab(region, lo, hi, cuts):
    """[(region, z0, z1)]: a dielectric less the cuts [(z0, z1, disk)] between their heights: the
    dielectric less every disk over its whole height, and the dielectric under the disks stretch by
    stretch, less the disks that cut that stretch; neighbouring stretches cut alike are one."""
    if not cuts:
        return [(region, lo, hi)]
    under = union([d for *_, d in cuts])
    out = [(sh.diff(region, under), lo, hi)]
    near = sh.inter(region, under)
    levels = sorted({lo, hi} | {z for c in cuts for z in c[:2] if lo < z < hi})
    last_key = None
    for a, b in zip(levels, levels[1:]):
        active = tuple(k for k, (z0, z1, _) in enumerate(cuts) if z0 <= a + 1e-9 and z1 >= b - 1e-9)
        if active == last_key:
            out[-1] = (out[-1][0], out[-1][1], b)
            continue
        out.append((sh.diff(near, union([cuts[k][2] for k in active])) if active else near, a, b))
        last_key = active
    return [(g, a, b) for g, a, b in out if not g.is_empty]


def build(r, ps):
    """r: Regions.  ps: PrismSet to add to."""
    st, B = r.stackup, P.Board
    merged = B.DIELECTRIC_GROUPING == "merged"
    for i, d in enumerate(st.dielectrics):
        lo, hi = dielectric_z(st, i)
        part = "Board" if merged else f"Board_{d.name}"
        props = {"kind": d.kind, "material": d.material, "thickness_mm": round(hi - lo, 6),
                 "epsilon_r": d.epsilon_r, "loss_tangent": d.loss_tangent,
                 "between": [d.above, d.below]}
        for g, z0, z1 in cut_slab(r.slab[i], lo, hi, r.slab_cuts.get(i, [])):
            ps.add(part, "board", g, z0, z1, layer=d.name, props=props)
    if not B.RESIN_FILL_BETWEEN_INNER_COPPER:
        ps.notes.append("inner copper pockets left empty (RESIN_FILL_BETWEEN_INNER_COPPER = False)")
        return
    # laminate beside each inner copper layer: resin from the adjacent prepreg (else the dielectric above)
    for k, l in enumerate(st.copper_layers[1:-1], start=1):
        above, below = st.dielectrics[k - 1], st.dielectrics[k]
        d = below if below.kind == "prepreg" and above.kind != "prepreg" else above
        part = "Board" if merged else f"Board_{d.name}"
        lo, hi = st.band[l]
        props = {"kind": d.kind, "material": d.material, "thickness_mm": round(hi - lo, 6),
                 "epsilon_r": d.epsilon_r, "loss_tangent": d.loss_tangent, "resin_fill_beside": l}
        for g, z0, z1 in cut_slab(r.band_laminate.get(l), lo, hi, r.band_cuts.get(l, [])):
            ps.add(part, "board", g, z0, z1, layer=d.name, props=props)
