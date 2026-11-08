"""KiCad 10's post machining and backdrills in the board's heights.  A counterbore or countersink
knocks out the copper of every layer it reaches (a hole of kind "knockout" on that one layer, which
the copper, the mask and the silk then take like any hole) and cuts the laminate, beside the inner
copper too, between two heights: a counterbore as one cylinder, a countersink as a stack of
cylinders that keep within Board.COUNTERSINK_STEP_TOLERANCE_MM of its cone.  A backdrill is a hole
already (stage 2); here it and the post machining are also told to the barrel they cut back
(Regions.barrel_cuts)."""
import math

from kese.core.shapes2d import disk
from kese.model.items import Hole
from kese.s3_resolve.heights import dielectric_z
from parameters import P

INF = math.inf


def post_machining_steps(pm, band, layers, tolerance):
    """A counterbore's or countersink's cut, board heights (mm, F up): ([(z0, z1, radius)] from its
    face to its floor, [(k, radius)] the copper layers it knocks out), as KiCad 10 cuts it
    (exporter_step.cpp, create_layer_items.cpp):
      - its depth counts from the copper's outer face; a countersink of depth 0, or deeper than its
        cone, goes to the cone's tip;
      - it knocks out the copper of every layer it reaches, by KiCad's own rule for the copper
        (PAD/PCB_VIA::GetPostMachiningKnockout, BOARD_STACKUP::GetLayerDistance): a layer is
        reached when its distance from the face is less than the depth, the distance to an inner
        layer counting to its middle, to the outer layer on the far side through all of it (0 to
        the one on its own side); a counterbore knocks out its whole size, a countersink the cone's
        size at that distance, a layer where the cone has come to its tip not at all;
      - the laminate it cuts to its floor, even a floor inside a copper layer's band, as KiCad's
        3D board does (exporter_step.cpp: AddCounterbore, AddCountersink);
      - KESE: a countersink is a stack of cylinders, each at the cone's radius halfway up it, so
        within `tolerance` of the cone, with a step at every copper face."""
    front = pm.side == "F"
    face = band[layers[0]][1] if front else band[layers[-1]][0]
    far = band[layers[-1]][0] if front else band[layers[0]][1]
    big = pm.size / 2
    tan_h = math.tan(math.radians(pm.angle / 2)) if pm.mode == "countersink" else 0.0
    if pm.mode == "countersink":
        tip = big / tan_h
        depth = min(pm.depth, tip) if pm.depth > 0 else tip
    else:
        depth = pm.depth

    def radius_at(z):                         # the cut's radius at height z
        return big - abs(face - z) * tan_h

    floor = max(face - depth, far) if front else min(face + depth, far)
    top, bottom = (face, floor) if front else (floor, face)
    knocked, last = {}, len(layers) - 1
    for k, l in enumerate(layers):
        if k in (0, last):
            dist = 0.0 if (k == 0) == front else abs(face - far)
        else:
            dist = abs(face - sum(band[l]) / 2)
        r = big - dist * tan_h
        if dist < depth - 1e-7 and r > 0:
            knocked[k] = r
    cuts = sorted({top, bottom} | {z for l in layers for z in band[l] if bottom < z < top}, reverse=front)
    steps = []
    for a, b in zip(cuts, cuts[1:]):
        z0, z1 = min(a, b), max(a, b)
        if not tan_h:
            steps.append((z0, z1, big))
            continue
        h = 2 * tolerance / tan_h
        n = max(1, math.ceil((z1 - z0) / h - 1e-9))
        for s in range(n):
            lo = z0 + (z1 - z0) * s / n
            hi = z0 + (z1 - z0) * (s + 1) / n
            r = radius_at((lo + hi) / 2)
            if r > 0:
                steps.append((lo, hi, r))
    return steps, sorted(knocked.items())


def machine(r, items):
    """The knockouts of every post machining as holes (items.holes, kind "knockout"), the laminate
    cuts (r.slab_cuts {dielectric index: [(z0, z1, disk)]} and beside the inner copper r.band_cuts
    {layer: [(z0, z1, disk)]}, board frame) and the barrel cuts (r.barrel_cuts {hole index:
    [(z0, z1, disk)]}, KiCad frame) of post machining and backdrills.  Once per Items: a second call
    finds the knockouts in."""
    st, layers = r.stackup, items.layers
    spans = [(r.slab_cuts, i, dielectric_z(st, i)) for i in range(len(st.dielectrics))]
    spans += [(r.band_cuts, l, st.band[l]) for l in layers[1:-1]]
    last = len(layers) - 1
    known = any(h.kind == "knockout" for h in items.holes)
    for pm in items.post_machining:
        steps, knocked = post_machining_steps(pm, st.band, layers, P.Board.COUNTERSINK_STEP_TOLERANCE_MM)
        if not known:
            for k, rad in knocked:
                items.holes.append(Hole(disk(pm.center, rad), k, k, False, "", 0.0, kind="knockout", of=pm.of))
        drill = items.holes[pm.of].drill
        for z0, z1, rad in steps:
            d = disk(pm.center, rad)
            if drill.buffer(1e-6).contains(d):        # inside the hole: nothing left there to cut
                continue
            r.barrel_cuts.setdefault(pm.of, []).append((z0, z1, d))
            for into, key, (lo, hi) in spans:
                if min(z1, hi) - max(z0, lo) > 1e-9:
                    into.setdefault(key, []).append((max(z0, lo), min(z1, hi), r.to_board_T(d)))
    for h in items.holes:
        if h.kind == "backdrill" and h.of >= 0:
            z1 = INF if h.i == 0 else st.band[layers[h.i]][1]
            z0 = -INF if h.j == last else st.band[layers[h.j]][0]
            r.barrel_cuts.setdefault(h.of, []).append((z0, z1, h.drill))
