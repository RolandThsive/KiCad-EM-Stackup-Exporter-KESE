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


def slabs(r, items):
    """r.slab: the laminate between copper k and k+1, drilled by every hole through it;
    r.bores_side: the open bores on each face."""
    T, last = r.to_board_T, len(items.layers) - 1
    r.slab = [drilled(r, lambda h, k=k: h.i <= k and h.j >= k + 1) for k in range(last)]
    r.bores_side = {"F": T(bores(r, lambda h: h.i == 0)), "B": T(bores(r, lambda h: h.j == last))}


def band_laminate(r, items):
    """r.band_laminate: on each inner copper layer, the laminate beside the copper, drilled."""
    last = len(items.layers) - 1
    for k, l in enumerate(items.layers):
        if 0 < k < last:
            lam = sh.diff(drilled(r, lambda h, k=k: h.i <= k <= h.j), r.copper_all[l])
            r.band_laminate[l] = sh.diff(lam, r.edge_band) if r.edge_band is not None else lam


def barrels(r, items, outline_k):
    """r.barrels: the plating ring of the plated holes, one region per (top layer, bottom layer,
    net), plus the plated board edge."""
    spans = defaultdict(list)
    for h in items.holes:
        if h.plated:
            spans[(h.i, h.j, h.net)].append(h.drill.difference(h.drill.buffer(-h.wall)).intersection(outline_k))
    r.barrels = [(r.to_board_T(union(rings)), i, j, net) for (i, j, net), rings in spans.items()]
    if r.edge_band is not None:
        r.barrels.append((r.edge_band, 0, len(items.layers) - 1, r.edge_net))
