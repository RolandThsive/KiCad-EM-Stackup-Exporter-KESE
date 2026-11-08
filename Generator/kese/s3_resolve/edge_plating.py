"""Edge plating: a copper band inside the outline when the board edge is plated
(Copper.EDGE_PLATING), belonging to one net."""
import math
from collections import Counter, defaultdict

import shapely

from kese.core import shapes2d as sh
from kese.core.shapes2d import EMPTY, union
from kese.s3_resolve.holes import drills
from parameters import P

INF = math.inf


def edge_plating(r, items, log):
    """Set r.edge_band (board frame) and r.edge_net, move other nets' copper out of the band, and
    let the band take the laminate's place at the edge.  A hole through the whole board interrupts
    the band; one that is not (a blind or buried hole, a backdrill, a counterbore or countersink)
    cuts it only between its own heights (r.edge_cuts)."""
    C = P.Copper
    plated = {"file": items.stackup.edge_plating, "yes": True, "no": False}[C.EDGE_PLATING]
    r.edge_band, r.edge_net = None, None
    if not plated:
        return
    last = len(r.layers) - 1
    ring = sh.snap(sh.diff(r.outline, r.outline.buffer(-C.EDGE_PLATING_WALL_MM)))
    r.edge_cuts = edge_cuts(r, ring)
    through = (lambda h: h.kind == "drill" and h.i == 0 and h.j == last) if r.edge_cuts else (lambda h: True)
    band = sh.diff(ring, r.to_board_T(drills(r, through)))
    if C.EDGE_PLATING_NET == "auto":
        touching = defaultdict(float)
        for l in r.layers:
            for net, g in r.copper[l].items():
                a = g.intersection(band).area
                if a > 0:
                    touching[net] += a
        named = {n: a for n, a in touching.items() if n != C.NO_NET_NAME}
        net = max(named, key=named.get) if named else C.NO_NET_NAME
    else:
        net = C.EDGE_PLATING_NET
    moved = Counter()
    for l in r.layers:
        cu = r.copper[l]
        for other, g in list(cu.items()):
            if other != net and g.intersects(band):
                inside = sh.inter(g, band)
                if inside.area > 0:
                    moved[other] += 1
                    cu[other] = sh.diff(g, band)
                    if cu[other].is_empty:
                        del cu[other]
                    cu[net] = sh.snap(union([cu.get(net, EMPTY), inside]))
    for other, n in moved.items():
        log(f"edge plating: copper of net {other!r} inside the edge band moved to net {net!r} on {n} layer(s)")
    r.edge_band, r.edge_net = band, net
    items.found["edge plating band (net " + net + ")"] += 1
    # the band takes the laminate's place at the edge (like a barrel in its drill hole); on the
    # outer layers it is part of the edge net's copper, which caps it like an annular ring
    r.slab = [sh.diff(s, band) for s in r.slab]
    for k in (0, last):
        on = sh.diff(band, r.to_board_T(drills(r, lambda h, k=k: h.i <= k <= h.j))) if r.edge_cuts else band
        r.copper[r.layers[k]][net] = sh.snap(union([r.copper[r.layers[k]].get(net, EMPTY), on]))
    # the band runs through the inner layers' copper bands, as a barrel through its drill: the
    # inner copper stops at the band and touches it
    for l in r.layers[1:-1]:
        if net in r.copper[l]:
            r.copper[l][net] = sh.diff(r.copper[l][net], band)
            if r.copper[l][net].is_empty:
                del r.copper[l][net]


def edge_cuts(r, ring):
    """[(z0, z1, disk)], board frame: what cuts the plated edge between two heights only, where it
    meets the ring the edge plating takes: post machining and backdrills (r.barrel_cuts), and blind
    and buried holes."""
    st, layers, last = r.stackup, r.layers, len(r.layers) - 1
    cuts = [cut for cuts in r.barrel_cuts.values() for cut in cuts]
    cuts += [(-INF if h.j == last else st.band[layers[h.j]][0], INF if h.i == 0 else st.band[layers[h.i]][1], h.drill)
             for h in r.items.holes if h.kind == "drill" and not (h.i == 0 and h.j == last)]
    disks = [r.to_board_T(d) for *_, d in cuts]
    shapely.prepare(ring)
    meet = shapely.intersects(ring, disks) if disks else []
    return [(z0, z1, d) for (z0, z1, _), d, m in zip(cuts, disks, meet) if m and sh.inter(d, ring).area > 0]
