"""The laminate, drilled where holes pass, with pockets where inner copper sits (filled by resin).
With the plies fused (Stackup.FUSION_BUILD) it is one solid per gap between two copper layers, the
resin beside the inner copper a part of the neighbouring prepreg's solid; with the plies separate,
one solid per ply and per core, and the resin beside each inner copper layer a solid of its own.
Where a counterbore or countersink (KiCad 10) cuts a dielectric or the resin beside inner copper
part of the way through, the laminate near it is cut in stretches between the heights where the cut
changes."""
from kese.core import shapes2d as sh
from kese.core.dielectric import model_props
from kese.core.shapes2d import union
from kese.s3_resolve.heights import dielectric_z, ply_z
from kese.s3_resolve.holes import stretches
from kese.s4_geometry.switches import built
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


def values(x, lo, hi, **more):
    """The properties of a laminate solid from lo to hi with the values of x, a Dielectric or a Ply."""
    return {"kind": x.kind, "material": x.material, "thickness_mm": round(hi - lo, 6),
            "epsilon_r": x.epsilon_r, "loss_tangent": x.loss_tangent, **more}


def model_of(x, epsilon_r=None, loss_tangent=None):
    """The frequency the values of x are given at, and how they change with it (materials.json)."""
    model = model_props(x.model, x.epsilon_r if epsilon_r is None else epsilon_r,
                        x.loss_tangent if loss_tangent is None else loss_tangent, x.frequency_hz)
    return {"spec_frequency_hz": x.frequency_hz, "dielectric_model": model}


def build(r, ps):
    """r: Regions.  ps: PrismSet to add to."""
    st, B = r.stackup, P.Board
    merged = B.DIELECTRIC_GROUPING == "merged"
    separate = P.Stackup.FUSION_BUILD == "PLIES_SEPARATE"
    resin = built("resin_between_traces")

    def add(name, layer, region, lo, hi, cuts, props):    # a laminate solid from lo to hi, less the cuts that reach it
        cuts = [c for c in cuts if min(c[1], hi) - max(c[0], lo) > 1e-9]
        for g, z0, z1 in cut_slab(region, lo, hi, cuts):
            ps.add("Board" if merged else f"Board_{name}", "board", g, z0, z1, layer=layer, props=props)
    for i, d in enumerate(st.dielectrics):
        between = [d.above, d.below]
        for ply, lo, hi in ply_z(st, i) if separate else ():
            add(ply.name, ply.of, r.slab[i], lo, hi, r.slab_cuts.get(i, []),
                values(ply, lo, hi, **model_of(ply), between=between, ply=ply.number, plies_in_gap=ply.count,
                       **({"joined_plies": ply.holds} if len(ply.holds) > 1 else {})))
        if not separate:
            lo, hi = dielectric_z(st, i)
            add(d.name, d.name, r.slab[i], lo, hi, r.slab_cuts.get(i, []),
                values(d, lo, hi, fused_properties=B.FUSED_PROPERTIES, **model_of(d), between=between,
                       plies=[{"name": ply.name, **values(ply, 0.0, ply.thickness), **model_of(ply)} for ply in d.plies]))
    if not resin:
        ps.notes.append('inner copper pockets left empty ("resin_between_traces" is False)')
        return
    # laminate beside each inner copper layer: resin from the adjacent prepreg (else the dielectric above)
    for k, l in enumerate(st.copper_layers[1:-1], start=1):
        above, below = st.dielectrics[k - 1], st.dielectrics[k]
        if not separate:        # a part of that dielectric's solid, with its values
            d = below if below.kind == "prepreg" and above.kind != "prepreg" else above
            add(d.name, d.name, r.band_laminate.get(l), *st.band[l], r.band_cuts.get(l, []),
                values(d, *st.band[l], resin_fill_beside=l))
            continue
        ply, er, tand = resin_values(st, k)
        flowed = model_of(ply, er, tand) if ply.model != "table" else {"spec_frequency_hz": ply.frequency_hz,
                                                                      "dielectric_model": {"model": "constant"}}
        props = {"kind": "resin", "material": B.RESIN_MATERIAL, "thickness_mm": round(st.band[l][1] - st.band[l][0], 6),
                 "epsilon_r": er, "loss_tangent": tand, **flowed, "resin_fill_beside": l, "flowed_from": ply.name}
        add(f"resin {l}", l, r.band_laminate.get(l), *st.band[l], r.band_cuts.get(l, []), props)


def resin_values(st, k):
    """(the ply it flowed from, er, tan d) of the resin beside inner copper layer k with the plies
    separate: the resin of the prepreg ply that touches the layer (of the one above it where both
    or neither are prepreg), with the values of Board.py or, where those are None, that ply's."""
    B = P.Board
    over, under = st.dielectrics[k - 1].solids[-1], st.dielectrics[k].solids[0]
    ply = under if under.kind == "prepreg" and over.kind != "prepreg" else over
    return (ply, ply.epsilon_r if B.RESIN_EPSILON_R is None else B.RESIN_EPSILON_R,
            ply.loss_tangent if B.RESIN_LOSS_TANGENT is None else B.RESIN_LOSS_TANGENT)
