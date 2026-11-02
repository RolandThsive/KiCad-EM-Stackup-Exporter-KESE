"""Surface finish (ENIG, HASL, ...) on the copper the solder mask leaves bare: the top and bottom
copper, and the plated board edge and castellations."""
from kese.core import shapes2d as sh
from kese.core.shapes2d import EMPTY, union
from kese.s3_resolve.holes import drilled
from parameters import P


def finish_type(st):
    F = P.Finish
    if F.FINISH_TYPE != "file":
        return F.FINISH_TYPE
    fold = lambda s: s.lower().replace(" ", "").replace("-", "").replace("_", "")
    name = fold(st.copper_finish or "")
    if name == "none":
        return None                                      # the board says: no finish
    for key in list(F.FINISH_TYPES) + list(F.FINISH_NAME_ALIASES):
        if fold(key) == name:
            return F.FINISH_NAME_ALIASES.get(key, key)
    return F.FINISH_DEFAULT_TYPE


def _exposed(r, side, cu):
    """The part of `cu` (copper on side's outer layer) the finish lands on: in a mask opening and
    not under ink kept in the opening (SILKSCREEN_OVER_COPPER: printed before the finish)."""
    exposed = sh.inter(cu, r.mask_open[side])
    if P.Silkscreen.SILKSCREEN_OVER_COPPER:
        inked = r.silk.get(side, EMPTY)
        if not inked.is_empty:
            exposed = sh.diff(exposed, inked)
    return exposed


def _props(side, metal, t, **kw):
    return {"side": side, "metal": metal, "thickness_mm": t,
            "conductivity_S_per_m": P.Finish.FINISH_CONDUCTIVITY_S_PER_M.get(metal, 0.0), **kw}


def build(r, ps):
    F, st = P.Finish, r.stackup
    if not F.FINISH_ENABLED:
        return
    kind = finish_type(st)
    if kind is None:
        ps.notes.append("finish: the board's stackup says None, nothing applied")
        return
    layers = F.FINISH_TYPES.get(kind)
    if not layers:
        ps.notes.append(f"finish: unknown type {kind!r}, none applied")
        return
    ps.notes.append(f"finish: {kind} " + " + ".join(f"{m} {t} mm" for m, t in layers))
    for side, layer, sign, tb in (("F", "F.Cu", 1, "Top"), ("B", "B.Cu", -1, "Bottom")):
        # one part per metal and side, or per metal and net (FINISH_GROUPING = "net")
        groups = r.copper[layer].items() if F.FINISH_GROUPING == "net" else [(None, r.copper_all.get(layer, EMPTY))]
        for net, cu in groups:
            exposed = _exposed(r, side, cu)
            if exposed.is_empty:
                continue
            z = abs(st.band[layer][1] if sign > 0 else st.band[layer][0])
            for metal, t in layers:
                part = f"{tb} Finish {metal}" + (f"_{net}" if net is not None else "")
                ps.add(part, "finish", exposed, sign * z, sign * (z + t), layer=f"{side}.Finish", net=net,
                       props=_props(side, metal, t))
                z += t
    edge(r, ps, layers)


def _edge_copper(r):
    """[(region, net)] of the edge copper that takes the finish, board frame: the plated edge band
    (FINISH_ON_EDGE_PLATING) and the castellations' part-barrels inside the outline
    (FINISH_ON_CASTELLATIONS); -> (that list, what it holds in words)."""
    F, T = P.Finish, r.to_board_T
    edge = [(r.edge_band, r.edge_net)] if F.FINISH_ON_EDGE_PLATING and r.edge_band is not None else []
    cast = []
    if F.FINISH_ON_CASTELLATIONS:
        for h in r.items.holes:
            if h.castellated:
                ring = sh.inter(T(h.drill.difference(h.drill.buffer(-h.wall))), r.outline)
                if not ring.is_empty:
                    cast.append((ring, h.net))
    what = " and ".join(w for w, on in (("plated edge", edge), ("castellations", cast)) if on)
    return edge + cast, what


def _drawn(t, g):
    """A finish metal's thickness across the edge, on the snapping grid: the nearest whole number of
    grid steps, at least one (a film thinner than the grid is drawn one step thick)."""
    return max(1, round(t / g)) * g


def edge(r, ps, layers):
    """The finish on the plated board edge and in the castellations: per metal, a shell in the air
    beside the edge copper, from the bottom of B.Cu to the top of F.Cu, wrapping over the corner
    where the top or bottom copper at the edge takes the finish too.

    The metals are laid outward from the copper in order, like the top finish is laid upward: metal
    k fills the air between offsets o_(k-1) and o_k from the edge copper over the copper's height;
    above the top copper (and below the bottom copper) it fills everything up to o_k between heights
    zt + o_(k-1) and zt + o_k, where the top finish is.  So the shells, the top and bottom finish and
    the copper tile the corner with no gap and no overlap."""
    F, st, g = P.Finish, r.stackup, sh.grid()
    copper, what = _edge_copper(r)
    if not copper:
        return
    M = sh.snap(union([m for m, _ in copper]))
    zt, zb = st.band["F.Cu"][1], st.band["B.Cu"][0]
    # the top / bottom finish: the shell wraps over the corner only next to it
    caps = {s: _exposed(r, s, r.copper_all.get(l, EMPTY)) for s, l in (("F", "F.Cu"), ("B", "B.Cu"))}
    # what is solid beside the edge copper: the drilled board, the barrels, the edge copper, every
    # layer's copper and the top / bottom finish (on the grid these can stand a hair past the outline)
    solid = sh.snap(union([drilled(r, lambda h: True), M] + [ring for ring, *_ in r.barrels]
                          + list(r.copper_all.values()) + list(caps.values())))
    reach = sum(_drawn(t, g) for _, t in layers) + 2 * g          # beyond the outermost shell
    near = {s: e.buffer(reach, join_style="mitre") for s, e in caps.items() if not e.is_empty}
    # one part per metal, or per metal and net: each net's shells lie round its own edge copper, and
    # where two nets' shells meet the first net keeps the shared area
    if F.FINISH_GROUPING == "net":
        nets = {}
        for m, net in copper:
            nets[net] = union([nets.get(net, EMPTY), m])
        groups = [(net, m.buffer(reach, join_style="mitre")) for net, m in nets.items()]
    else:
        groups = [(None, None)]
    drawn_note, o_prev, inner = [], 0.0, M
    for metal, t in layers:
        o = o_prev + _drawn(t, g)
        if abs(o - o_prev - t) > 1e-12:
            drawn_note.append(f"{metal} {t} mm drawn {o - o_prev:.6g} mm thick across the edge")
        outer = sh.snap(M.buffer(o, join_style="mitre", mitre_limit=2.0))
        ring = sh.diff(sh.diff(outer, inner), solid)                 # beside the copper: this metal's shell
        cover = sh.diff(outer, solid)                                # over the copper and the shells below
        pieces = [(ring, zb, zt)]
        for s, sign, z0 in (("F", 1, zt), ("B", -1, zb)):
            if s in near:
                pieces += [(sh.inter(ring, near[s]), z0, z0 + sign * o_prev),
                           (sh.inter(cover, near[s]), z0 + sign * o_prev, z0 + sign * o)]
        props = _props("Edge", metal, t, drawn_thickness_mm=round(o - o_prev, 9))
        taken = EMPTY
        for net, own in groups:
            part = f"Edge Finish {metal}" + (f"_{net}" if net is not None else "")
            for region, z0, z1 in pieces:
                if own is not None:
                    region = sh.diff(sh.inter(region, own), taken)
                ps.add(part, "finish", region, z0, z1, layer="Edge.Finish", net=net, props=dict(props))
            if own is not None:
                taken = union([taken, own])
        o_prev, inner = o, outer
    ps.notes.append(f"finish: also on the {what}"
                    + (f" ({'; '.join(drawn_note)}, the snapping grid)" if drawn_note else ""))
