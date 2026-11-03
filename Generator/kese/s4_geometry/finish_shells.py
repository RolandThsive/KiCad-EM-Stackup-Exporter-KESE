"""The finish everywhere but the faces of the outer copper: a shell per metal in the air beside the
copper's walls, inside the open plated holes, on the plated board edge and in the castellations,
wrapping over the corner onto the face's finish (finish.py)."""
from kese.core import shapes2d as sh
from kese.core.shapes2d import EMPTY, union
from kese.s3_resolve.holes import drilled, drills
from kese.s4_geometry.finish import drawn as on_grid, exposed, finish_layers, props
from parameters import P


def build(r, ps):
    layers, _ = finish_layers(r.stackup)
    if not layers:
        return
    zones = [edge(r, ps, layers)]
    zones.append(bores(r, ps, layers, zones[0]))
    walls(r, ps, layers, union([z for z in zones if z is not None]))


def _edge_copper(r):
    """[(region, net)] of the edge copper that takes the finish, board frame: the plated edge band
    and the castellations' part-barrels inside the outline; -> (that list, what it holds in words)."""
    T = r.to_board_T
    edge = [(r.edge_band, r.edge_net)] if r.edge_band is not None else []
    cast = []
    for h in r.items.holes:
        if h.castellated:
            ring = sh.inter(T(h.drill.difference(h.drill.buffer(-h.wall))), r.outline)
            if not ring.is_empty:
                cast.append((ring, h.net))
    what = " and ".join(w for w, on in (("plated edge", edge), ("castellations", cast)) if on)
    return edge + cast, what


def _shells(ps, layers, M, groups, solid, body, caps, part, layer, side):
    """Per finish metal, a shell in the air beside copper region M (board frame), outside `solid`:
    from body = (z_lo, z_hi), wrapping over the copper's face for each cap (near, z, sign): at height
    z, going up (sign 1) or down (-1), within `near` (None: everywhere).

    The metals are laid outward from the copper in order, as the top finish is laid upward: metal k
    fills the air between offsets o_(k-1) and o_k from the copper over the body; past the face it
    fills everything within o_k between z + h_(k-1) and z + h_k, where the face's finish is (h: the
    real thicknesses summed; o: the drawn ones).  So the shells, the finish on the face and the copper
    meet with no gap and no overlap.  groups:
    [(net, the area its shells may take)], the first net keeping an area two nets share, or
    [(None, None)] for one part per metal.  -> the notes on metals drawn thicker than they are."""
    g, drawn_note, o_prev, h_prev, inner = sh.grid(), [], 0.0, 0.0, M
    for metal, t in layers:
        o, h = o_prev + on_grid(t, g), h_prev + t
        if abs(o - o_prev - t) > 1e-12:
            drawn_note.append(f"{metal} {t} mm drawn {o - o_prev:.6g} mm thick")
        outer = sh.snap(M.buffer(o, join_style="mitre", mitre_limit=2.0))
        ring = sh.diff(sh.diff(outer, inner), solid)                 # beside the copper: this metal's shell
        cover = sh.diff(outer, solid)                                # past the face, over the shells below
        pieces = [(ring, *body)]
        for near, z, sign in caps:
            clip = (lambda a: a) if near is None else (lambda a, n=near: sh.inter(a, n))
            pieces += [(clip(ring), z, z + sign * h_prev), (clip(cover), z + sign * h_prev, z + sign * h)]
        meta = props(side, metal, t, drawn_thickness_mm=round(o - o_prev, 9))
        taken = EMPTY
        for net, own in groups:
            name = part(metal, net)
            for region, z0, z1 in pieces:
                if own is not None:
                    region = sh.diff(sh.inter(region, own), taken)
                ps.add(name, "finish", region, z0, z1, layer=layer, net=net, props=dict(meta))
            if own is not None:
                taken = union([taken, own])
        o_prev, h_prev, inner = o, h, outer
    return drawn_note


def _groups(pairs, reach):
    """[(net, its copper grown by reach)] for FINISH_GROUPING = "net", else [(None, None)]."""
    if P.Finish.FINISH_GROUPING != "net":
        return [(None, None)]
    nets = {}
    for m, net in pairs:
        nets[net] = union([nets.get(net, EMPTY), m])
    return [(net, m.buffer(reach, join_style="mitre")) for net, m in nets.items()]


def edge(r, ps, layers):
    """The finish on the plated board edge and in the castellations: per metal, a shell in the air
    beside the edge copper, from the bottom of B.Cu to the top of F.Cu, wrapping over the corner
    where the top or bottom copper at the edge takes the finish too (_shells).  -> the area within
    reach of the edge copper, which the finish on the copper walls leaves to it, or None."""
    st, g = r.stackup, sh.grid()
    copper, what = _edge_copper(r)
    if not copper:
        return None
    M = sh.snap(union([m for m, _ in copper]))
    zt, zb = st.band["F.Cu"][1], st.band["B.Cu"][0]
    # the top / bottom finish: the shell wraps over the corner only next to it (next to all the
    # outer copper when the finish goes on before the mask)
    caps = {s: exposed(r, s, r.copper_all.get(l, EMPTY)) for s, l in (("F", "F.Cu"), ("B", "B.Cu"))}
    # what is solid beside the edge copper: the drilled board, the barrels, the edge copper, every
    # layer's copper and the top / bottom finish (on the grid these can stand a hair past the outline)
    solid = sh.snap(union([drilled(r, lambda h: True), M] + [ring for ring, *_ in r.barrels]
                          + list(r.copper_all.values()) + list(caps.values())))
    reach = sum(on_grid(t, g) for _, t in layers) + 2 * g          # beyond the outermost shell
    wrap = [(caps[s].buffer(reach, join_style="mitre"), z, sign)
            for s, z, sign in (("F", zt, 1), ("B", zb, -1)) if not caps[s].is_empty]
    drawn = _shells(ps, layers, M, _groups(copper, reach), solid, (zb, zt), wrap,
                    lambda metal, net: f"Edge Finish {metal}" + (f"_{net}" if net is not None else ""),
                    "Edge.Finish", "Edge")
    ps.notes.append(f"finish: also on the {what}"
                    + (f" ({'; '.join(drawn)} across the edge, the snapping grid)" if drawn else ""))
    return M.buffer(reach, join_style="mitre")


def bores(r, ps, layers, edge_zone):
    """The finish inside the open bores of the plated holes: the baths run
    through every hole that is open at a face, so the barrel's inside takes the finish over its whole
    length, and wraps onto the finish on the annular ring.  Per (top layer, bottom layer, open ends)
    of the barrels, a shell inside the bore (_shells), part "Hole Finish <metal>".  A hole closed at
    both faces (buried, or a via tented on both) takes none, nor do the castellations (the edge
    finish's).  -> the area within reach of the
    barrels, or None."""
    st, g, last = r.stackup, sh.grid(), len(r.layers) - 1
    T = r.to_board_T
    before = P.Finish.FINISH_BEFORE_SOLDER_MASK
    spans = {}
    for h in r.items.holes:
        if not (h.plated and h.wall > 0) or h.castellated:
            continue
        d = T(h.drill)
        # an end is open at a face it reaches, unless the mask closes it (a tented via); with the
        # finish before the mask, every end reaching a face is open
        ends = tuple(reach_ and (before or d.intersects(r.mask_open[s]))
                     for s, reach_ in (("F", h.i == 0), ("B", h.j == last)))
        if any(ends):
            spans.setdefault((h.i, h.j, ends), []).append((T(h.drill.difference(h.drill.buffer(-h.wall))), h.net))
    if not spans:
        return None
    caps = {s: exposed(r, s, r.copper_all.get(l, EMPTY)) for s, l in (("F", "F.Cu"), ("B", "B.Cu"))}
    solid = sh.snap(union([drilled(r, lambda h: True)] + [ring for ring, *_ in r.barrels]
                          + list(r.copper_all.values()) + list(caps.values())
                          + ([edge_zone] if edge_zone is not None else [])))
    reach = sum(on_grid(t, g) for _, t in layers) + 2 * g
    zone, drawn = [], []
    for (i, j, (open_f, open_b)), rings in spans.items():
        M = sh.snap(union([m for m, _ in rings]))
        lo = st.band["B.Cu"][0] if j == last else st.band[r.layers[j]][1]     # an open end at a face, or the
        hi = st.band["F.Cu"][1] if i == 0 else st.band[r.layers[i]][0]        # copper that closes the bore
        wrap = [(caps[s].buffer(reach, join_style="mitre"), z, sign)
                for s, z, sign, open_ in (("F", hi, 1, open_f), ("B", lo, -1, open_b))
                if open_ and not caps[s].is_empty]
        drawn = _shells(ps, layers, M, _groups(rings, reach), solid, (lo, hi), wrap,
                        lambda metal, net: f"Hole Finish {metal}" + (f"_{net}" if net is not None else ""),
                        "Hole.Finish", "Hole") or drawn
        zone.append(M.buffer(reach, join_style="mitre"))
    ps.notes.append("finish: also inside the plated holes"
                    + (f" ({'; '.join(drawn)} across the wall, the snapping grid)" if drawn else ""))
    return union(zone)


def walls(r, ps, layers, zone):
    """The finish on the side walls of the copper, wherever the wall meets the air: the baths coat
    every bare copper face.  On the outer layers that is the
    pads' and traces' walls in the mask openings and the copper the board edge cuts; on the inner
    layers, the copper the board edge cuts (beside a castellation, say).  Per layer and metal, a shell
    in the air beside the copper, over the copper's height (_shells); on an outer layer it wraps over
    the top corner onto the finish on the face and is part of that side's finish ("Top Finish
    Nickel"), on an inner layer it is part "Edge Finish <metal>".  Where the mask covers the wall
    there is none (with the finish before the mask, the mask wraps round it instead); `zone` (the
    plated edge, the castellations and the holes, which have their own finish) is left out."""
    F, st, g = P.Finish, r.stackup, sh.grid()
    reach = sum(on_grid(t, g) for _, t in layers) + 2 * g
    last, drawn = len(r.layers) - 1, []
    plated_bores = r.to_board_T(drills(r, lambda h: h.plated))
    for k, layer in enumerate(r.layers):
        per_net = [(cu, net) for net, cu in r.copper[layer].items() if not cu.is_empty]
        if not per_net:
            continue
        C = r.copper_all[layer]
        lo, hi = st.band[layer]
        outer = k in (0, last)
        if outer:
            side, sign, tb = ("F", 1, "Top") if k == 0 else ("B", -1, "Bottom")
            # beside the copper: the ink, and the mask unless the finish went on before it
            solid = [C, r.silk.get(side, EMPTY)] + ([] if F.FINISH_BEFORE_SOLDER_MASK else [r.mask[side]])
            face = exposed(r, side, C)
            wrap = [(face.buffer(reach, join_style="mitre"), hi if sign > 0 else lo, sign)] if not face.is_empty else []
            name = lambda metal, net, tb=tb: f"{tb} Finish {metal}" + (f"_{net}" if net is not None else "")
            where = f"{side}.Finish"
        else:
            # inside the board the copper lies in the laminate: only the board edge leaves it bare
            solid, wrap, side = [C, r.outline], [], "Edge"
            name = lambda metal, net: f"Edge Finish {metal}" + (f"_{net}" if net is not None else "")
            where = "Edge.Finish"
        # and the bores of the plated holes: an open bore has its own finish (in `zone`), a closed
        # one (a tented via) none
        solid.append(plated_bores)
        if zone is not None and not zone.is_empty:
            solid.append(zone)
        drawn = _shells(ps, layers, C, _groups(per_net, reach), sh.snap(union(solid)), (lo, hi), wrap,
                        name, where, side) or drawn
    ps.notes.append("finish: also on the copper's walls where they meet the air"
                    + (f" ({'; '.join(drawn)} across the wall, the snapping grid)" if drawn else ""))
