"""Edge plating: a copper band inside the outline when the board edge is plated
(Copper.EDGE_PLATING), belonging to one net."""
from collections import Counter, defaultdict

from kese.core import shapes2d as sh
from kese.core.shapes2d import EMPTY, union
from kese.s3_resolve.holes import drills
from parameters import P


def edge_plating(r, items, log):
    """Set r.edge_band (board frame) and r.edge_net, move other nets' copper out of the band, and
    let the band take the laminate's place at the edge."""
    C = P.Copper
    plated = {"file": items.stackup.edge_plating, "yes": True, "no": False}[C.EDGE_PLATING]
    r.edge_band, r.edge_net = None, None
    if not plated:
        return
    band = sh.snap(sh.diff(r.outline, r.outline.buffer(-C.EDGE_PLATING_WALL_MM)))
    hole = r.to_board_T(drills(r, lambda h: True))       # every hole that reaches the edge interrupts the plating
    band = sh.diff(band, hole)
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
        for other in list(r.copper[l]):
            if other != net and r.copper[l][other].intersects(band):
                inside = sh.inter(r.copper[l][other], band)
                if inside.area > 0:
                    moved[other] += 1
                    r.copper[l][other] = sh.diff(r.copper[l][other], band)
                    if r.copper[l][other].is_empty:
                        del r.copper[l][other]
                    r.copper[l][net] = sh.snap(union([r.copper[l].get(net, EMPTY), inside]))
    for other, n in moved.items():
        log(f"edge plating: copper of net {other!r} inside the edge band moved to net {net!r} on {n} layer(s)")
    r.edge_band, r.edge_net = band, net
    items.found["edge plating band (net " + net + ")"] += 1
    # the band takes the laminate's place at the edge (like a barrel in its drill hole); on the
    # outer layers it is part of the edge net's copper, which caps it like an annular ring
    r.slab = [sh.diff(s, band) for s in r.slab]
    for l in (r.layers[0], r.layers[-1]):
        r.copper[l][net] = sh.snap(union([r.copper[l].get(net, EMPTY), band]))
