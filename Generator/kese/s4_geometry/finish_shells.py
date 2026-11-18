"""The finish everywhere but the faces of the outer copper (those are finish.py): a shell per metal
in the air beside the copper's walls, inside the open plated holes (finish_bores.py), on the plated
board edge and in the castellations, wrapping over the corner onto the finish on the face.  The
board's outline is routed after the finish goes on, so a copper face the router cuts (the outer
and inner copper at the board edge, a castellation's cut ends) stays bare; a plated edge is routed
before its plating, and takes the finish.  How a shell is laid is in shells.py; the copper layers
are worked on Parallel.WORKERS at a time, in threads, each on its own copies of the shapes it uses
(kese/core/shape_copies.py)."""
from kese.core import shapes2d as sh
from kese.core.parallel import in_parallel
from kese.core.shape_copies import own
from kese.core.shapes2d import EMPTY, union
from kese.s3_resolve.holes import cut_back, drilled, drills, full_height, ring_of
from kese.s4_geometry.finish import exposed, finish_layers, named
from kese.s4_geometry.finish_bores import bores
from kese.s4_geometry.shells import add_all, air_near, bare_faces, groups, near_faces, note, reach, shells
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
            ring = sh.inter(r.to_board_T(ring_of(h)), r.outline)
            if not ring.is_empty:
                cast.append((ring, h.net))
    what = " and ".join(w for w, on in (("plated edge", edge), ("castellations", cast)) if on)
    return edge + cast, what


def edge(r, ps, layers):
    """The finish on the plated edge and in the castellations, from B.Cu's bottom to F.Cu's top, over
    the corner where the copper beside it is bare ("Edge Finish <metal>"); where post machining, a
    backdrill or a blind or buried hole cuts the plated edge (r.edge_cuts), on what is left of it,
    stretch by stretch, as on a cut barrel (finish_bores.py).  A castellation is a plated hole when
    the finish goes on and is cut by the router after: its part-barrel has the finish on its bore
    side, and its cut ends none but where the edge is plated; -> the zone, or None."""
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
    bores = [sh.inter(r.to_board_T(h.drill), r.outline) for h in r.items.holes if h.castellated]
    if bores:           # the castellations' bores inside the board, and anywhere near the plated edge
        reached = sh.snap(union(bores + ([near_faces(r.edge_band, d)] if r.edge_band is not None else [])))
        air = inside(air, reached)
    caps = [(near_faces(faces[s], d), z, sign)
            for s, z, sign in (("F", top, 1), ("B", bottom, -1)) if not faces[s].is_empty]
    spans = [(copper, bottom, top)]
    if r.edge_cuts:                     # copper[0] is the plated edge, the rest the castellations
        spans = [([(g, r.edge_net)] + copper[1:], z0, z1)
                 for g, z0, z1 in cut_back(r.edge_band, bottom, top, r.edge_cuts)]
    for parts, z0, z1 in spans:
        ends = [cap for cap in caps if (z1 == top if cap[2] > 0 else z0 == bottom)]
        add_all(ps, shells(layers, sh.snap(union([m for m, _ in parts])), groups(parts, d), air, (z0, z1), ends,
                           named("Edge"), "Edge.Finish", "Edge"))
    note(ps, f"on the {what}", layers, "edge")
    return near_faces(M, d)


def walls(r, ps, layers, zone):
    """The finish on the outer copper's side walls wherever they meet the air inside the board: the
    walls of the pads and traces in the mask openings, wrapping over the top corner as part of that
    side's finish ("Top Finish Nickel").  Where the mask covers a wall there is none (with the finish
    before the mask, the mask wraps round it instead).  The copper the board edge cuts is bare where
    cut, on the outer layers and the inner ones, which meet the air nowhere else.  `zone` (the edge
    and the holes, which have their own finish) is left out."""
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
        side, sign, prefix = ("F", 1, "Top") if k == 0 else ("B", -1, "Bottom")
        # solid beside the copper: the ink, and the mask unless the finish went on before it
        solid = [C, own(r.silk.get(side, EMPTY))]
        if not P.Finish.FINISH_BEFORE_SOLDER_MASK:
            solid.append(own(r.mask[side]))
        face = exposed(r, side, C, take=own)
        caps = [(near_faces(face, d), top if sign > 0 else bottom, sign)] if not face.is_empty else []
        # an open bore has its own finish (in `zone`), a closed one (a tented via) none
        solid.append(own(plated_bores))
        if zone is not None and not zone.is_empty:
            solid.append(own(zone))
        return shells(layers, C, groups(per_net, d), inside(air_beside(solid), own(r.outline)), (bottom, top),
                      caps, named(prefix), f"{side}.Finish", side)

    done = in_parallel(layer_walls, (0, last))                # the inner copper meets no air inside the board
    for adds in done:
        add_all(ps, adds)
    note(ps, "on the copper's walls where they meet the air", layers if any(done) else [], "wall")


def air_beside(solid):
    """band -> the band less the solid beside an outer layer's copper (`solid`: [copper, ...])."""
    def air(band):
        return sh.diff(band, sh.snap(union(solid)))
    return air


def inside(air_of, area):
    """band -> the air air_of(band) finds, within `area` (on the grid): the board, or for the
    castellations their bores."""
    def air(band):
        return sh.inter(air_of(band), area)
    return air
