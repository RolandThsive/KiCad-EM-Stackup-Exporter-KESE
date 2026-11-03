"""The finish everywhere but the faces of the outer copper (those are finish.py): a shell per metal
in the air beside the copper's walls, inside the open plated holes, on the plated board edge and in
the castellations, wrapping over the corner onto the finish on the face.  How a shell is laid is in
shells.py; the hole spans and the copper layers are worked on Run.WORKERS at a time."""
from kese.core import shapes2d as sh
from kese.core.parallel import in_parallel
from kese.core.shapes2d import EMPTY, union
from kese.s3_resolve.holes import drilled, drills
from kese.s4_geometry.finish import exposed, finish_layers
from kese.s4_geometry.shells import add_all, bare_faces, groups, named, near_faces, note, reach, shells
from parameters import P


def build(r, ps):
    layers, _ = finish_layers(r.stackup)
    if not layers:
        return
    # the edge and the holes have their own finish: the walls leave their surroundings to them
    edge_zone = edge(r, ps, layers)
    hole_zone = bores(r, ps, layers, edge_zone)
    walls(r, ps, layers, union([z for z in (edge_zone, hole_zone) if z is not None]))


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
    st, d, faces = r.stackup, reach(layers), bare_faces(r)
    M = sh.snap(union([m for m, _ in copper]))
    top, bottom = st.band["F.Cu"][1], st.band["B.Cu"][0]
    # solid beside the edge copper: the drilled board, the barrels, the edge copper, every layer's
    # copper and the face's finish (on the grid these can stand a hair past the outline)
    solid = sh.snap(union([drilled(r, lambda h: True), M] + [ring for ring, *_ in r.barrels]
                          + list(r.copper_all.values()) + list(faces.values())))
    caps = [(near_faces(faces[s], d), z, sign)
            for s, z, sign in (("F", top, 1), ("B", bottom, -1)) if not faces[s].is_empty]
    adds, drawn = shells(layers, M, groups(copper, d), solid, (bottom, top), caps, named("Edge"), "Edge.Finish", "Edge")
    add_all(ps, adds)
    note(ps, f"on the {what}", drawn, "edge")
    return near_faces(M, d)


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
    d, faces = reach(layers), bare_faces(r)
    copper = {key: sh.snap(union([m for m, _ in rings])) for key, rings in spans.items()}
    # solid beside the bores: the drilled board, the barrels, every layer's copper, the face's finish,
    # the edge's finish and the rings themselves (so that each span's copper lies in it)
    solid = sh.snap(union([drilled(r, lambda h: True)] + [ring for ring, *_ in r.barrels]
                          + list(r.copper_all.values()) + list(faces.values()) + list(copper.values())
                          + ([edge_zone] if edge_zone is not None else [])))

    def span(key):
        (i, j, (open_f, open_b)), M = key, copper[key]
        # from an open end at a face, or from the inner copper that closes the bore
        bottom = st.band["B.Cu"][0] if j == last else st.band[r.layers[j]][1]
        top = st.band["F.Cu"][1] if i == 0 else st.band[r.layers[i]][0]
        caps = [(near_faces(faces[s], d), z, sign)
                for s, z, sign, is_open in (("F", top, 1, open_f), ("B", bottom, -1, open_b))
                if is_open and not faces[s].is_empty]
        adds, drawn = shells(layers, M, groups(spans[key], d), solid, (bottom, top), caps, named("Hole"), "Hole.Finish", "Hole")
        return adds, drawn, near_faces(M, d)

    done = in_parallel(span, list(spans))
    for adds, _, _ in done:
        add_all(ps, adds)
    note(ps, "inside the plated holes", next((drawn for _, drawn, _ in reversed(done) if drawn), []), "wall")
    return union([zone for *_, zone in done])


def walls(r, ps, layers, zone):
    """The finish on the copper's side walls wherever they meet the air: on the outer layers the
    walls of the pads and traces in the mask openings and of the copper the board edge cuts, wrapping
    over the top corner as part of that side's finish ("Top Finish Nickel"); on the inner layers the
    copper the board edge cuts ("Edge Finish Nickel").  Where the mask covers a wall there is none
    (with the finish before the mask, the mask wraps round it instead).  `zone` (the edge and the
    holes, which have their own finish) is left out."""
    st, d, last = r.stackup, reach(layers), len(r.layers) - 1
    plated_bores = r.to_board_T(drills(r, lambda h: h.plated))

    def layer_walls(k):
        layer = r.layers[k]
        per_net = [(cu, net) for net, cu in r.copper[layer].items() if not cu.is_empty]
        if not per_net:
            return [], []
        C = r.copper_all[layer]
        bottom, top = st.band[layer]
        if k in (0, last):
            side, sign, prefix = ("F", 1, "Top") if k == 0 else ("B", -1, "Bottom")
            # solid beside the copper: the ink, and the mask unless the finish went on before it
            solid = [C, r.silk.get(side, EMPTY)]
            if not P.Finish.FINISH_BEFORE_SOLDER_MASK:
                solid.append(r.mask[side])
            face = exposed(r, side, C)
            caps = [(near_faces(face, d), top if sign > 0 else bottom, sign)] if not face.is_empty else []
            where = f"{side}.Finish"
        else:
            # inside the board the copper lies in the laminate: only the board edge leaves it bare
            side, prefix, solid, caps, where = "Edge", "Edge", [C, r.outline], [], "Edge.Finish"
        # an open bore has its own finish (in `zone`), a closed one (a tented via) none
        solid.append(plated_bores)
        if zone is not None and not zone.is_empty:
            solid.append(zone)
        return shells(layers, C, groups(per_net, d), sh.snap(union(solid)), (bottom, top), caps,
                      named(prefix), where, side)

    done = in_parallel(layer_walls, range(len(r.layers)))
    for adds, _ in done:
        add_all(ps, adds)
    note(ps, "on the copper's walls where they meet the air", next((drawn for _, drawn in reversed(done) if drawn), []), "wall")
