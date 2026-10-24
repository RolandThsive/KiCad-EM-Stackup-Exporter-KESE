"""Copper: on every layer, the items of each net joined, cut by the holes and clipped to the
outline.  Where two nets overlap, the first keeps the shared area."""
from collections import defaultdict

from kese.core import shapes2d as sh
from kese.core.shapes2d import EMPTY, union
from kese.s3_resolve.holes import bores, drills
from parameters import P


def copper_layers(r, items, outline_k):
    """r.copper {layer: {net: region}} and r.copper_all {layer: region}."""
    T, last = r.to_board_T, len(items.layers) - 1
    for k, l in enumerate(items.layers):
        if k in (0, last):
            cut = bores(items, lambda h, k=k: h.i <= k <= h.j)         # outer copper caps the barrel
        else:
            cut = drills(items, lambda h, k=k: h.i <= k <= h.j)        # inner copper stops at the drill wall
        per_net = defaultdict(list)
        for g, net in items.copper_items.get(l, []):
            per_net[net].append(g)
        regions = {}
        for net, gs in per_net.items():
            cu = union(gs).intersection(outline_k).difference(cut)
            if P.Geometry.SIMPLIFY_TOLERANCE_MM > 0:
                cu = cu.simplify(P.Geometry.SIMPLIFY_TOLERANCE_MM)
            cu = T(cu)
            if not cu.is_empty:
                regions[net] = cu
        # copper of different nets never overlaps on a real board; if the file has overlaps, the
        # first net keeps the shared area so the solids stay disjoint
        taken = EMPTY
        for net in list(regions):
            if not taken.is_empty:
                regions[net] = sh.diff(regions[net], taken)
            taken = union([taken, regions[net]])
        r.copper[l] = {n: g for n, g in regions.items() if not g.is_empty}
        r.copper_all[l] = sh.snap(union(list(r.copper[l].values())))


def join_nets(r):
    """r.copper_all once more, after edge plating has changed the copper."""
    for l in r.layers:
        r.copper_all[l] = sh.snap(union(list(r.copper[l].values())))
