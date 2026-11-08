"""The finish everywhere but the faces of the outer copper (those are finish.py): a shell per metal
in the air beside the copper's walls, inside the open plated holes (finish_bores.py), on the plated
board edge and in the castellations, wrapping over the corner onto the finish on the face.  How a
shell is laid is in shells.py; the copper layers are worked on Parallel.WORKERS at a time, in
threads, each on its own copies of the shapes it uses (kese/core/shape_copies.py)."""
from kese.core import shapes2d as sh
from kese.core.parallel import in_parallel
from kese.core.shape_copies import own
from kese.core.shapes2d import EMPTY, union
from kese.s3_resolve.holes import drilled, drills, full_height
from kese.s4_geometry.finish import exposed, finish_layers
from kese.s4_geometry.finish_bores import bores
from kese.s4_geometry.shells import add_all, air_near, bare_faces, groups, named, near_faces, note, reach, shells
from parameters import P


def build(r, ps):
    layers, _ = finish_layers(r.stackup)
    if not layers:
        return
    # the edge and the holes have their own finish: the walls leave their surroundings to them
    edge_zone = edge(r, ps, layers)
    hole_zone = bores(r, ps, layers, edge_zone)          # finish_bores.py
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
    air = air_near([drilled(r, full_height), M] + [ring for ring, *_ in r.barrels]
                   + list(r.copper_all.values()) + list(faces.values()))
    caps = [(near_faces(faces[s], d), z, sign)
            for s, z, sign in (("F", top, 1), ("B", bottom, -1)) if not faces[s].is_empty]
    add_all(ps, shells(layers, M, groups(copper, d), air, (bottom, top), caps, named("Edge"), "Edge.Finish", "Edge"))
    note(ps, f"on the {what}", layers, "edge")
    return near_faces(M, d)


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
        nets = [(net, cu) for net, cu in r.copper[layer].items() if not cu.is_empty]
        per_net = list(zip(own([cu for _, cu in nets]), [net for net, _ in nets]))
        if not per_net:
            return []
        C = own(r.copper_all[layer])
        bottom, top = st.band[layer]
        if k in (0, last):
            side, sign, prefix = ("F", 1, "Top") if k == 0 else ("B", -1, "Bottom")
            # solid beside the copper: the ink, and the mask unless the finish went on before it
            solid = [C, own(r.silk.get(side, EMPTY))]
            if not P.Finish.FINISH_BEFORE_SOLDER_MASK:
                solid.append(own(r.mask[side]))
            face = exposed(r, side, C, take=own)
            caps = [(near_faces(face, d), top if sign > 0 else bottom, sign)] if not face.is_empty else []
            where = f"{side}.Finish"
        else:
            # inside the board the copper lies in the laminate: only the board edge leaves it bare
            side, prefix, solid, caps, where = "Edge", "Edge", [C, own(r.outline)], [], "Edge.Finish"
        # an open bore has its own finish (in `zone`), a closed one (a tented via) none
        solid.append(own(plated_bores))
        if zone is not None and not zone.is_empty:
            solid.append(own(zone))
        return shells(layers, C, groups(per_net, d), air_beside(solid, k in (0, last)), (bottom, top), caps,
                      named(prefix), where, side)

    done = in_parallel(layer_walls, range(len(r.layers)))
    for adds in done:
        add_all(ps, adds)
    note(ps, "on the copper's walls where they meet the air", layers if any(done) else [], "wall")


def air_beside(solid, outer):
    """band -> the band less the solid beside a layer's copper (`solid`: [copper, ...], the outline
    second on an inner layer), joined only when needed: an inner layer's band that lies inside the
    outline (no copper within the shells' reach of the board edge, as on most boards) has no air."""
    def air(band):
        if not outer and sh.diff(band, solid[1]).is_empty:
            return EMPTY
        return sh.diff(band, sh.snap(union(solid)))
    return air
