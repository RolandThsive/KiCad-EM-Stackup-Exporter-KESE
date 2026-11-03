"""The finish everywhere but the faces of the outer copper (those are finish.py): a shell per metal
in the air beside the copper's walls, inside the open plated holes, on the plated board edge and in
the castellations, wrapping over the corner onto the finish on the face."""
from kese.core import shapes2d as sh
from kese.core.shapes2d import EMPTY, union
from kese.s3_resolve.holes import drilled, drills
from kese.s4_geometry.finish import exposed, finish_layers, on_grid, props
from parameters import P


def build(r, ps):
    layers, _ = finish_layers(r.stackup)
    if not layers:
        return
    # the edge and the holes have their own finish: the walls leave their surroundings to them
    edge_zone = edge(r, ps, layers)
    hole_zone = bores(r, ps, layers, edge_zone)
    walls(r, ps, layers, union([z for z in (edge_zone, hole_zone) if z is not None]))


def _reach(layers):
    """How far the shells reach out from the copper, with two grid steps to spare."""
    return sum(on_grid(t, sh.grid()) for _, t in layers) + 2 * sh.grid()


def _named(prefix):
    """The part name for a metal (and a net, with FINISH_GROUPING = "net"): "<prefix> Finish Gold_GND"."""
    return lambda metal, net: f"{prefix} Finish {metal}" + (f"_{net}" if net is not None else "")


def _bare_faces(r):
    """{"F": ..., "B": ...}: the outer copper that takes the finish on its face."""
    return {s: exposed(r, s, r.copper_all.get(l, EMPTY)) for s, l in (("F", "F.Cu"), ("B", "B.Cu"))}


def _note(ps, what, drawn, across):
    grid = f" ({'; '.join(drawn)} across the {across}, the snapping grid)" if drawn else ""
    ps.notes.append(f"finish: also {what}{grid}")


def _groups(pairs, reach):
    """[(net, its copper grown by reach)] for FINISH_GROUPING = "net", else [(None, None)]."""
    if P.Finish.FINISH_GROUPING != "net":
        return [(None, None)]
    nets = {}
    for m, net in pairs:
        nets[net] = union([nets.get(net, EMPTY), m])
    return [(net, m.buffer(reach, join_style="mitre")) for net, m in nets.items()]


def _shells(ps, layers, M, groups, solid, body, caps, part, layer, side):
    """Per finish metal, a shell in the air beside copper region M (board frame), outside `solid`,
    from body = (z_lo, z_hi).  caps: [(near, z, sign)], where the shell wraps over the copper's face
    at height z, going up (sign 1) or down (-1), within `near`.

    The metals are laid outward from the copper in order, as the face's finish is laid upward. With
    o_k the drawn thicknesses summed and h_k the real ones, metal k fills the air between o_(k-1) and
    o_k from the copper over the body, and, past the face, everything within o_k of the copper
    between z + h_(k-1) and z + h_k, where the face's finish is.  So the shells, the finish on the
    face and the copper meet with no gap and no overlap.

    groups: [(net, the area its shells may take)], the first net keeping an area two nets share, or
    [(None, None)] for one part per metal.  -> notes on the metals drawn thicker than they are."""
    g, notes = sh.grid(), []
    o_prev, h_prev, inner = 0.0, 0.0, M
    for metal, t in layers:
        o, h = o_prev + on_grid(t, g), h_prev + t
        if abs(o - o_prev - t) > 1e-12:
            notes.append(f"{metal} {t} mm drawn {o - o_prev:.6g} mm thick")
        outer = sh.snap(M.buffer(o, join_style="mitre", mitre_limit=2.0))
        ring = sh.diff(sh.diff(outer, inner), solid)        # this metal's shell beside the copper
        cover = sh.diff(outer, solid)                       # past the face: over the shells below too
        pieces = [(ring, *body)]
        for near, z, sign in caps:
            pieces += [(sh.inter(ring, near), z, z + sign * h_prev),
                       (sh.inter(cover, near), z + sign * h_prev, z + sign * h)]
        meta = props(side, metal, t, drawn_thickness_mm=round(o - o_prev, 9))
        taken = EMPTY
        for net, own in groups:
            for region, z0, z1 in pieces:
                if own is not None:
                    region = sh.diff(sh.inter(region, own), taken)
                ps.add(part(metal, net), "finish", region, z0, z1, layer=layer, net=net, props=dict(meta))
            if own is not None:
                taken = union([taken, own])
        o_prev, h_prev, inner = o, h, outer
    return notes


def _edge_copper(r):
    """[(region, net)] of the edge copper, board frame: the plated edge band and the castellations'
    part-barrels inside the outline; -> (that list, what it holds in words)."""
    edge = [(r.edge_band, r.edge_net)] if r.edge_band is not None else []
    cast = []
    for h in r.items.holes:
        if h.castellated:
            ring = sh.inter(r.to_board_T(h.drill.difference(h.drill.buffer(-h.wall))), r.outline)
            if not ring.is_empty:
                cast.append((ring, h.net))
    what = " and ".join(w for w, on in (("plated edge", edge), ("castellations", cast)) if on)
    return edge + cast, what


def edge(r, ps, layers):
    """The finish on the plated edge and in the castellations, from B.Cu's bottom to F.Cu's top, over
    the corner where the copper beside it is bare ("Edge Finish <metal>"); -> its zone, or None."""
    copper, what = _edge_copper(r)
    if not copper:
        return None
    st, reach, faces = r.stackup, _reach(layers), _bare_faces(r)
    M = sh.snap(union([m for m, _ in copper]))
    top, bottom = st.band["F.Cu"][1], st.band["B.Cu"][0]
    # solid beside the edge copper: the drilled board, the barrels, the edge copper, every layer's
    # copper and the face's finish (on the grid these can stand a hair past the outline)
    solid = sh.snap(union([drilled(r, lambda h: True), M] + [ring for ring, *_ in r.barrels]
                          + list(r.copper_all.values()) + list(faces.values())))
    caps = [(faces[s].buffer(reach, join_style="mitre"), z, sign)
            for s, z, sign in (("F", top, 1), ("B", bottom, -1)) if not faces[s].is_empty]
    drawn = _shells(ps, layers, M, _groups(copper, reach), solid, (bottom, top), caps,
                    _named("Edge"), "Edge.Finish", "Edge")
    _note(ps, f"on the {what}", drawn, "edge")
    return M.buffer(reach, join_style="mitre")


def bores(r, ps, layers, edge_zone):
    """The finish inside the plated holes open at a face, over the whole bore and onto the ring's
    finish ("Hole Finish <metal>"): the baths run through them.  A hole closed at both faces (buried,
    or tented on both) gets none; castellations have the edge's.  -> the bores' zone, or None."""
    st, last = r.stackup, len(r.layers) - 1
    before = P.Finish.FINISH_BEFORE_SOLDER_MASK
    spans = {}                      # (top layer, bottom layer, (open at F, open at B)) -> [(ring, net)]
    for h in r.items.holes:
        if not (h.plated and h.wall > 0) or h.castellated:
            continue
        drill = r.to_board_T(h.drill)
        # an end at a face is open unless the mask closes it (a tented via); with the finish before
        # the mask, every end at a face is open
        ends = tuple(at_face and (before or drill.intersects(r.mask_open[s]))
                     for s, at_face in (("F", h.i == 0), ("B", h.j == last)))
        if any(ends):
            ring = r.to_board_T(h.drill.difference(h.drill.buffer(-h.wall)))
            spans.setdefault((h.i, h.j, ends), []).append((ring, h.net))
    if not spans:
        return None
    reach, faces = _reach(layers), _bare_faces(r)
    solid = sh.snap(union([drilled(r, lambda h: True)] + [ring for ring, *_ in r.barrels]
                          + list(r.copper_all.values()) + list(faces.values())
                          + ([edge_zone] if edge_zone is not None else [])))
    zones, drawn = [], []
    for (i, j, (open_f, open_b)), rings in spans.items():
        M = sh.snap(union([m for m, _ in rings]))
        # from an open end at a face, or from the inner copper that closes the bore
        bottom = st.band["B.Cu"][0] if j == last else st.band[r.layers[j]][1]
        top = st.band["F.Cu"][1] if i == 0 else st.band[r.layers[i]][0]
        caps = [(faces[s].buffer(reach, join_style="mitre"), z, sign)
                for s, z, sign, is_open in (("F", top, 1, open_f), ("B", bottom, -1, open_b))
                if is_open and not faces[s].is_empty]
        drawn = _shells(ps, layers, M, _groups(rings, reach), solid, (bottom, top), caps,
                        _named("Hole"), "Hole.Finish", "Hole") or drawn
        zones.append(M.buffer(reach, join_style="mitre"))
    _note(ps, "inside the plated holes", drawn, "wall")
    return union(zones)


def walls(r, ps, layers, zone):
    """The finish on the copper's side walls wherever they meet the air: on the outer layers the
    walls of the pads and traces in the mask openings and of the copper the board edge cuts, wrapping
    over the top corner as part of that side's finish ("Top Finish Nickel"); on the inner layers the
    copper the board edge cuts ("Edge Finish Nickel").  Where the mask covers a wall there is none
    (with the finish before the mask, the mask wraps round it instead).  `zone` (the edge and the
    holes, which have their own finish) is left out."""
    st, reach, last = r.stackup, _reach(layers), len(r.layers) - 1
    plated_bores = r.to_board_T(drills(r, lambda h: h.plated))
    drawn = []
    for k, layer in enumerate(r.layers):
        per_net = [(cu, net) for net, cu in r.copper[layer].items() if not cu.is_empty]
        if not per_net:
            continue
        C = r.copper_all[layer]
        bottom, top = st.band[layer]
        if k in (0, last):
            side, sign, prefix = ("F", 1, "Top") if k == 0 else ("B", -1, "Bottom")
            # solid beside the copper: the ink, and the mask unless the finish went on before it
            solid = [C, r.silk.get(side, EMPTY)]
            if not P.Finish.FINISH_BEFORE_SOLDER_MASK:
                solid.append(r.mask[side])
            face = exposed(r, side, C)
            z = top if sign > 0 else bottom
            caps = [(face.buffer(reach, join_style="mitre"), z, sign)] if not face.is_empty else []
            where = f"{side}.Finish"
        else:
            # inside the board the copper lies in the laminate: only the board edge leaves it bare
            side, prefix, solid, caps, where = "Edge", "Edge", [C, r.outline], [], "Edge.Finish"
        # an open bore has its own finish (in `zone`), a closed one (a tented via) none
        solid.append(plated_bores)
        if zone is not None and not zone.is_empty:
            solid.append(zone)
        drawn = _shells(ps, layers, C, _groups(per_net, reach), sh.snap(union(solid)), (bottom, top), caps,
                        _named(prefix), where, side) or drawn
    _note(ps, "on the copper's walls where they meet the air", drawn, "wall")
