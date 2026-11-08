"""What KiCad 10's via protection (IPC-4761) puts inside a via: a fill through the whole bore
(Copper.VIA_FILL: copper, joined to the via's own copper, or resin) and plugs of resin from the
faces it is plugged on (Copper.VIA_PLUG_DEPTH_FRACTION of the bore each).  A fill or plug follows
what is left of the barrel: a backdrill or post machining leaves its cavity empty.  The caps and the
covering are elsewhere: a cap is the face's copper left whole over the bore (s3_resolve/copper.py),
a covering the solder mask over it (s3_resolve/mask.py)."""
from collections import defaultdict

from kese.core import shapes2d as sh
from kese.core.shapes2d import union
from kese.s3_resolve.holes import barrel_span, cut_back
from kese.s4_geometry.copper import part_name
from parameters import P

RESIN_PART = "Via Resin"


def fill_span(st, layers, h):
    """(bottom, top): the heights a fill of hole h reaches.  At a face whose copper the bore cuts,
    flush with the copper's outer face; where copper shuts the bore (a cap, a copper fill), up to that
    copper; at an end inside the board, the barrel's end."""
    last, fill = len(layers) - 1, P.Copper.VIA_FILL
    lo, hi = barrel_span(st, layers, h.i, h.j)
    top = st.band[layers[0]][1] if h.i == 0 and not h.protect.copper_shut("F", fill) else hi
    bottom = st.band[layers[-1]][0] if h.j == last and not h.protect.copper_shut("B", fill) else lo
    return bottom, top


def plug_ranges(st, layers, h):
    """[(z0, z1)]: the heights the plugs of hole h fill, from each face it is plugged on (an end a
    backdrill or post machining opens takes none), Copper.VIA_PLUG_DEPTH_FRACTION of the bore deep;
    plugs that meet are one.  [] when the hole has no protection or is filled (a fill fills the whole
    bore)."""
    p = h.protect
    if p is None or p.filled:
        return []
    bottom, top = fill_span(st, layers, h)
    deep = P.Copper.VIA_PLUG_DEPTH_FRACTION * (top - bottom)
    out = []
    if p.plugged["F"] and not p.opened["F"]:
        out.append((max(top - deep, bottom), top))
    if p.plugged["B"] and not p.opened["B"]:
        out.append((bottom, min(bottom + deep, top)))
    if len(out) == 2 and out[0][0] <= out[1][1]:
        out = [(bottom, top)]
    return out


def build(r, ps):
    st, C, layers = r.stackup, P.Copper, r.layers
    groups = defaultdict(list)          # (part, role, z0, z1, span, net) -> [region]
    for n, h in enumerate(r.items.holes):
        p = h.protect
        if p is None or not h.plated or h.wall <= 0:
            continue
        bore = h.drill.buffer(-h.wall)
        span = f"{layers[h.i]}-{layers[h.j]}"
        cuts = r.barrel_cuts.get(n, [])
        if p.filled:
            copper = C.VIA_FILL == "copper"
            part = part_name(C.COPPER_GROUPING, h.net, span, plating=True) if copper else RESIN_PART
            role = "plating" if copper else "via_resin"
            ranges = [fill_span(st, layers, h)]
        else:
            part, role, ranges = RESIN_PART, "via_resin", plug_ranges(st, layers, h)
        for z0, z1 in ranges:
            for g, a, b in cut_back(bore, z0, z1, cuts):
                groups[(part, role, round(a, 9), round(b, 9), span, h.net if role == "plating" else "")].append(g)
    for (part, role, z0, z1, span, net), regions in groups.items():
        region = sh.snap(sh.inter(r.to_board_T(union(regions)), r.outline))
        if role == "plating":
            props = {"layer": span, "net": net, "conductivity_S_per_m": C.COPPER_CONDUCTIVITY_S_PER_M}
            ps.add(part, role, region, z0, z1, layer=span, net=net, props=props)
        else:
            props = {"material": "via resin", "epsilon_r": C.VIA_RESIN_EPSILON_R,
                     "loss_tangent": C.VIA_RESIN_LOSS_TANGENT, "layer": span}
            ps.add(part, role, region, z0, z1, layer=span, props=props)
