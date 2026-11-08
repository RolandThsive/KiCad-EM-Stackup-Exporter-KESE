"""Holes: plated holes cut by the board edge, the laminate drilled where holes pass, and the
plating barrels.  Every distinct set of holes is joined only once (Regions.holes_made) and reused
wherever the same holes pass."""
from collections import defaultdict
from threading import RLock

from kese.core import shapes2d as sh
from kese.core.shapes2d import union
from parameters import P

_MAKING = RLock()        # made_once(): reentrant, as drilled() makes drills() inside it


def hole_shapes(holes, pred, bore=False, take=lambda g: g):
    """The holes for which pred(hole) holds, one shape each, KiCad frame: the drilled outline, or
    with bore=True the open bore inside the plating.  take(drills): the drills as used (own, in a thread)."""
    picked = [h for h in holes if pred(h)]
    return [d.buffer(-h.wall) if bore and h.wall > 0 else d for h, d in zip(picked, take([h.drill for h in picked]))]


def made_once(r, kind, pred, make):
    """make(), or what it made before for the same kind and the same holes: made once even when
    threads ask at the same time (one makes it, the others wait for it).  A thread that makes new
    shapes from what it returns takes an own() copy of it (kese/core/shape_copies.py)."""
    holes = r.items.holes
    picked = tuple(i for i, h in enumerate(holes) if pred(h))
    key = (kind, picked, tuple(holes[i].wall for i in picked))
    with _MAKING:
        if key not in r.holes_made:
            r.holes_made[key] = make()
        return r.holes_made[key]


def drills(r, pred):
    """The drilled outlines of the holes for which pred(hole) holds, joined, KiCad frame."""
    return made_once(r, "drills", pred, lambda: union(hole_shapes(r.items.holes, pred)))


def bores(r, pred):
    """The open bores (inside the plating) of the holes for which pred(hole) holds, joined, KiCad frame."""
    return made_once(r, "bores", pred, lambda: union(hole_shapes(r.items.holes, pred, bore=True)))


def drilled(r, pred):
    """The outline drilled by the holes for which pred(hole) holds, board frame."""
    return made_once(r, "drilled", pred, lambda: sh.diff(r.outline, r.to_board_T(drills(r, pred))))


def castellate(items, outline_k):
    """Plated holes the outline cuts through: plated or left bare per Copper.CASTELLATION."""
    C = P.Copper
    plate = C.CASTELLATION == "auto" or (C.CASTELLATION == "file" and items.stackup.castellated_pads)
    for h in items.holes:
        if h.plated and not outline_k.contains(h.drill) and h.drill.intersects(outline_k):
            items.found["castellated holes (plated holes cut by the board edge)"] += 1
            if plate:
                h.wall, h.castellated = C.CASTELLATION_WALL_MM, True
            else:
                h.plated, h.wall = False, 0.0
                items.skipped["castellation plating (CASTELLATION is 'off')"] += 1
    if C.CASTELLATION == "file" and not items.stackup.castellated_pads and \
            items.found["castellated holes (plated holes cut by the board edge)"]:
        items.notes.append("plated holes cross the board edge but the stackup has no (castellated_pads yes); "
                           "set Copper.CASTELLATION = 'auto' to plate them")


def full_height(h):
    """Whether hole h is drilled the board's whole height where it passes: not a backdrill, nor a
    counterbore's or countersink's knockout, which leave the laminate between their heights."""
    return h.kind == "drill"


def at_face(h, side, last):
    """Whether hole h ends at the face `side`."""
    return h.i == 0 if side == "F" else h.j == last


def shut(h, side):
    """Whether a via's protection shuts its end on `side` (filled, capped, plugged or covered there)."""
    return h.protect is not None and h.protect.shut(side)


def covered(h, side):
    """Whether a via's end on `side` is covered: the solder mask spans its bore."""
    return h.protect is not None and h.protect.covered[side] and not h.protect.opened[side]


def slabs(r, items):
    """r.slab: the laminate between copper k and k+1, drilled by every hole through it;
    r.bores_side: the open bores on each face; r.closed_bores and r.covered: the bores a via's
    protection shuts on each face, and those of them covered."""
    T, last = r.to_board_T, len(items.layers) - 1
    r.slab = [drilled(r, lambda h, k=k: h.i <= k and h.j >= k + 1) for k in range(last)]
    for s in ("F", "B"):
        r.bores_side[s] = T(bores(r, lambda h, s=s: at_face(h, s, last) and not shut(h, s)))
        r.closed_bores[s] = T(bores(r, lambda h, s=s: at_face(h, s, last) and shut(h, s)))
        r.covered[s] = T(bores(r, lambda h, s=s: at_face(h, s, last) and covered(h, s)))


def band_laminate(r, items):
    """r.band_laminate: on each inner copper layer, the laminate beside the copper, drilled (a
    counterbore's or countersink's knockout takes the copper only: the laminate is cut back between
    its heights, r.band_cuts)."""
    last = len(items.layers) - 1
    for k, l in enumerate(items.layers):
        if 0 < k < last:
            lam = sh.diff(drilled(r, lambda h, k=k: h.i <= k <= h.j and h.kind != "knockout"), r.copper_all[l])
            r.band_laminate[l] = sh.diff(lam, r.edge_band) if r.edge_band is not None else lam


def barrel_span(st, layers, i, j):
    """(lo, hi): the heights of the barrel of a hole from copper i to j.  Outer layers cap the barrel
    (their copper covers the ring area), so it stops at their face; inner layers are drilled through,
    so it goes on through their band."""
    last = len(layers) - 1
    hi = st.band[layers[i]][0] if i == 0 else st.band[layers[i]][1]
    lo = st.band[layers[j]][1] if j == last else st.band[layers[j]][0]
    return lo, hi


def barrels(r, items, outline_k):
    """r.barrels: the plating ring of the plated holes, one region per (top layer, bottom layer,
    net), plus the plated board edge; r.barrel_pieces: the rings that post machining or a backdrill
    cuts back, hole by hole, between the heights where the cuts change."""
    spans = defaultdict(list)
    for n, h in enumerate(items.holes):
        if not h.plated:
            continue
        ring = h.drill.difference(h.drill.buffer(-h.wall)).intersection(outline_k)
        if n in r.barrel_cuts:
            lo, hi = barrel_span(r.stackup, items.layers, h.i, h.j)
            for g, z0, z1 in cut_back(ring, lo, hi, r.barrel_cuts[n]):
                r.barrel_pieces.append((r.to_board_T(g), z0, z1, h.i, h.j, h.net))
        else:
            spans[(h.i, h.j, h.net)].append(ring)
    r.barrels = [(r.to_board_T(union(rings)), i, j, net) for (i, j, net), rings in spans.items()]
    if r.edge_band is not None:
        r.barrels.append((r.edge_band, 0, len(items.layers) - 1, r.edge_net))


def cut_back(ring, lo, hi, cuts):
    """[(what is left of `ring`, z0, z1)] between lo and hi, where cuts [(z0, z1, disk)] take the
    disk out between their heights; neighbouring stretches cut alike are one."""
    levels = sorted({lo, hi} | {z for c in cuts for z in c[:2] if lo < z < hi})
    out, last_key = [], None
    for a, b in zip(levels, levels[1:]):
        active = tuple(k for k, (z0, z1, _) in enumerate(cuts) if z0 <= a + 1e-9 and z1 >= b - 1e-9)
        if out and active == last_key:
            out[-1] = (out[-1][0], out[-1][1], b)
            continue
        out.append(((sh.diff(ring, union([cuts[k][2] for k in active])) if active else ring), a, b))
        last_key = active
    return [(g, a, b) for g, a, b in out if not g.is_empty]
