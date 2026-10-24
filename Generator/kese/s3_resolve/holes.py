"""Holes: plated holes cut by the board edge, the laminate drilled where holes pass, the plating
barrels, and the exact circle of every round hole."""
from collections import defaultdict

from kese.core import shapes2d as sh
from kese.core.shapes2d import union
from parameters import P


def drills(items, pred):
    """The drilled outlines of the holes for which pred(hole) holds, KiCad frame."""
    return union([h.drill for h in items.holes if pred(h)])


def bores(items, pred):
    """The open bores (inside the plating) of the holes for which pred(hole) holds, KiCad frame."""
    return union([h.drill.buffer(-h.wall) if h.wall > 0 else h.drill for h in items.holes if pred(h)])


def castellate(items, outline_k):
    """Plated holes the outline cuts through: plated or left bare per Copper.CASTELLATION."""
    C = P.Copper
    plate = C.CASTELLATION == "auto" or (C.CASTELLATION == "file" and items.stackup.castellated_pads)
    for h in items.holes:
        if h.plated and not outline_k.contains(h.drill) and h.drill.intersects(outline_k):
            items.found["castellated holes (plated holes cut by the board edge)"] += 1
            if plate:
                h.wall = C.CASTELLATION_WALL_MM
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
    r.slab = [sh.diff(r.outline, T(drills(items, lambda h, k=k: h.i <= k and h.j >= k + 1))) for k in range(last)]
    r.bores_side = {"F": T(bores(items, lambda h: h.i == 0)), "B": T(bores(items, lambda h: h.j == last))}


def band_laminate(r, items):
    """r.band_laminate: on each inner copper layer, the laminate beside the copper, drilled."""
    T, last = r.to_board_T, len(items.layers) - 1
    for k, l in enumerate(items.layers):
        if 0 < k < last:
            hole = T(drills(items, lambda h, k=k: h.i <= k <= h.j))
            lam = sh.diff(sh.diff(r.outline, hole), r.copper_all[l])
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


def exact_circles(r, items):
    """r.circles: the true circles of every round hole (drill wall and plated bore) and via pad,
    board frame.  The STEP writer builds those rings from these, so the copper's hole and the
    barrel's wall are one identical circle instead of two fits to slightly different polygons."""
    cx, cy = r.to_board
    circles = list(items.via_pads)
    for h in items.holes:
        if h.centre is not None:
            circles.append((h.centre, h.radius))
            if h.wall > 0:
                circles.append((h.centre, h.radius - h.wall))
    r.circles = [((x - cx, -(y - cy)), rad) for (x, y), rad in circles if rad > 0]
