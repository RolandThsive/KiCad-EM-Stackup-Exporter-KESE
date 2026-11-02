"""Surface finish (ENIG, HASL, ...) on the copper the solder mask leaves bare: the top and bottom
copper, and the plated board edge and castellations."""
from kese.core import shapes2d as sh
from kese.core.shapes2d import EMPTY, union
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


def _castellations(r):
    """[(plating ring, net)] of the plated holes the board edge cuts, board frame: the part-barrel
    inside the outline, as stage 3 plates it (Copper.CASTELLATION)."""
    T, out = r.to_board_T, []
    for h in r.items.holes:
        if not (h.plated and h.wall > 0):
            continue
        d = T(h.drill)
        if d.within(r.outline) or not d.intersects(r.outline):
            continue
        ring = sh.inter(sh.diff(d, T(h.drill.buffer(-h.wall))), r.outline)
        if not ring.is_empty:
            out.append((ring, h.net))
    return out


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
    F, st = P.Finish, r.stackup
    metal_at = []                                        # [(edge copper region, net)]
    if F.FINISH_ON_EDGE_PLATING and r.edge_band is not None:
        metal_at.append((r.edge_band, r.edge_net))
    if F.FINISH_ON_CASTELLATIONS:
        metal_at += _castellations(r)
    if not metal_at:
        return
    from kese.s3_resolve.holes import drilled
    g = sh.grid()
    M = sh.snap(union([m for m, _ in metal_at]))
    zt, zb = st.band["F.Cu"][1], st.band[r.layers[-1]][0]
    # the shell wraps over the corner only where the top / bottom copper beside it takes the finish
    caps = {s: _exposed(r, s, r.copper_all.get(l, EMPTY)) for s, l in (("F", "F.Cu"), ("B", r.layers[-1]))}
    # what is solid beside the edge copper: the drilled board, every plating barrel, the edge copper,
    # every layer's copper and the top and bottom finish (on the grid they can stand a hair past the
    # outline, and the shells must not overlap them)
    solid = sh.snap(union([drilled(r, lambda h: True), M] + [ring for ring, *_ in r.barrels]
                          + list(r.copper_all.values()) + list(caps.values())))
    total = sum(_drawn(t, g) for _, t in layers)
    near = {s: e.buffer(total + 2 * g, join_style="mitre") if not e.is_empty else EMPTY for s, e in caps.items()}
    nets = {}                                            # net -> its edge copper, for FINISH_GROUPING = "net"
    for m, net in metal_at:
        nets[net] = union([nets.get(net, EMPTY), m])
    grow = lambda o: sh.snap(M.buffer(o, join_style="mitre", mitre_limit=2.0)) if o > 0 else M
    drawn_note, o_prev = [], 0.0
    for metal, t in layers:
        o = o_prev + _drawn(t, g)
        if abs(o - o_prev - t) > 1e-12:
            drawn_note.append(f"{metal} {t} mm drawn {o - o_prev:.6g} mm thick across the edge")
        ring = sh.diff(sh.diff(grow(o), grow(o_prev)), solid)          # beside the copper, k-th shell
        cover = sh.diff(grow(o), solid)                                  # over the copper and the shells below
        pieces = [(ring, zb, zt)]
        for s, sign, z0 in (("F", 1, zt), ("B", -1, zb)):
            if near[s].is_empty:
                continue
            pieces.append((sh.inter(ring, near[s]), z0, z0 + sign * o_prev))
            pieces.append((sh.inter(cover, near[s]), z0 + sign * o_prev, z0 + sign * o))
        groups = [(None, None)] if F.FINISH_GROUPING != "net" else list(nets.items())
        taken = EMPTY
        for net, own in groups:
            for region, z0, z1 in pieces:
                if own is not None:      # each net's shells round its own copper; the first net keeps a meeting
                    region = sh.diff(sh.inter(region, own.buffer(o + 2 * g, join_style="mitre")), taken)
                part = f"Edge Finish {metal}" + (f"_{net}" if net is not None else "")
                ps.add(part, "finish", region, z0, z1, layer="Edge.Finish", net=net,
                       props=_props("Edge", metal, t, drawn_thickness_mm=round(o - o_prev, 9)))
            if own is not None:
                taken = union([taken, own.buffer(o + 2 * g, join_style="mitre")])
        o_prev = o
    on_edge = F.FINISH_ON_EDGE_PLATING and r.edge_band is not None
    what = " and ".join(w for w, on in (("plated edge", on_edge), ("castellations", len(metal_at) > on_edge)) if on)
    ps.notes.append(f"finish: also on the {what}" + (" (" + "; ".join(drawn_note) + ", the snapping grid)"
                                                       if drawn_note else ""))
