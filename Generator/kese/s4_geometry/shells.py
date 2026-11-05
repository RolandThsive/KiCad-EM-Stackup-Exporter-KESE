"""How a finish shell is laid in the air beside a copper region, metal by metal (finish_shells.py
says where the shells go), and the helpers the edge, the holes and the walls share."""
from itertools import accumulate

import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.conformal import grow
from kese.core.shape_copies import own
from kese.core.shapes2d import EMPTY, exactly, union
from kese.core.vertices import noded
from kese.s4_geometry.finish import drawn_thickness, exposed, mitre, props
from parameters import P


def reach(layers):
    """How far the shells reach out from the copper, with two grid steps to spare."""
    return sum(drawn_thickness(t) for _, t in layers) + 2 * sh.grid()


def named(prefix):
    """The part name for a metal (and a net, with FINISH_GROUPING = "net"): "<prefix> Finish Gold_GND"."""
    return lambda metal, net: f"{prefix} Finish {metal}" + (f"_{net}" if net is not None else "")


def bare_faces(r):
    """{"F": ..., "B": ...}: the outer copper that takes the finish on its face."""
    return {s: exposed(r, s, r.copper_all.get(l, EMPTY)) for s, l in (("F", "F.Cu"), ("B", "B.Cu"))}


def near_faces(face, d):
    """Where a shell wraps over the corner onto the finish on `face`: within d of it."""
    return grow(face, d, join_style="mitre")


def note(ps, what, layers, across):
    """report.txt's line on where the shells went, naming the metals drawn thicker than they are
    across a wall (`layers`: the finish's, or [] when no shell was made)."""
    drawn = [f"{metal} {t} mm drawn {drawn_thickness(t):.6g} mm thick" for metal, t in layers
             if abs(drawn_thickness(t) - t) > 1e-12]
    grid = f" ({'; '.join(drawn)} across the {across}, the snapping grid)" if drawn else ""
    ps.notes.append(f"finish: also {what}{grid}")


MARGIN = 4          # grid steps: how far past a band's part the solid beside it is taken (air_near)
TILE = 2000         # vertices: a bigger part of the solid is cut into tiles of about this many first
TILE_DEPTH = 16     # at most this many halvings of a part's box (64k tiles a side)


def tiles(part):
    """A polygon cut along halvings of its box into pieces of about TILE vertices or fewer, which
    fill it and do not overlap."""
    out, todo = [], [(part, 0)]
    while todo:
        p, depth = todo.pop()
        if shapely.get_num_coordinates(p) <= TILE or depth == TILE_DEPTH:
            out.append(p)
            continue
        x0, y0, x1, y1 = p.bounds
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        for box in ((x0, y0, xm, ym), (xm, y0, x1, ym), (x0, ym, xm, y1), (xm, ym, x1, y1)):
            todo += [(q, depth + 1) for q in shapely.get_parts(sh.polys_only(shapely.clip_by_rect(p, *box)))
                     if not q.is_empty]
    return out


def air_near(regions):
    """band -> the band less the union of `regions`, on the grid, worked out for each of the band's
    parts on its own: the solid within MARGIN grid steps of the part's box, joined and put on the
    grid, is cut from it.  So no union of the whole board is made (on a big board that took most of
    the holes' finish: 31 s of NE_Delta's, where its 1,911 bores take about 7 s this way).  A big
    part of the solid (the drilled board, a plane) is cut into tiles first, so that each bore clips
    only the tiles near it.  The air comes out as the whole union's but where an edge crossing rounds
    onto the grid another way: a sliver thinner than a grid step.  Called from threads: what it cuts
    is this thread's own copies (kese/core/shape_copies.py)."""
    parts = [t for g in regions if g is not None for p in shapely.get_parts(sh.polys_only(g)) if not p.is_empty
             for t in tiles(p)]
    parts = np.array(parts, dtype=object)
    tree = shapely.STRtree(parts) if len(parts) else None

    def air(band):
        pieces = shapely.get_parts(sh.polys_only(band))
        m = MARGIN * sh.grid()
        boxes = shapely.bounds(pieces) + (-m, -m, m, m)
        at, near = tree.query(shapely.box(*boxes.T), predicate="intersects") if tree is not None else ([], [])
        which, k = np.unique(near, return_inverse=True)
        mine = own(parts[which])
        found = [[] for _ in pieces]
        for i, j in zip(np.asarray(at).tolist(), np.asarray(k).tolist()):
            found[i].append(j)
        out = []
        for piece, box, js in zip(pieces, boxes, found):
            solid = union([sh.polys_only(shapely.clip_by_rect(mine[j], *box)) for j in js])
            out += [q for q in shapely.get_parts(sh.diff(piece, sh.snap(solid))) if not q.is_empty]
        return sh.as_region(out)
    return air


def groups(pairs, d):
    """[(net, its copper grown by d)] for FINISH_GROUPING = "net", else [(None, None)]."""
    if P.Finish.FINISH_GROUPING != "net":
        return [(None, None)]
    nets = {}
    for m, net in pairs:
        nets[net] = union([nets.get(net, EMPTY), m])
    return [(net, m.buffer(d, join_style="mitre")) for net, m in nets.items()]


def within(region, area):
    """The part of `region` inside `area`, both on the grid (see exactly()), as a prism's region:
    noded the way stage 6 nodes every slice (vertices.noded).  Where a band one grid step wide comes
    out thinner than that between two slanted edges, noding closes it; closed here already, the
    prisms hold the same volume as the solids built from them."""
    return noded(exactly(shapely.intersection(sh.polys_only(region), sh.polys_only(area))))


def shells(layers, M, nets, air_of, body, caps, part, layer, side):
    """Per finish metal, a shell in the air beside copper region M (board frame), from body =
    (z_lo, z_hi); air_of(band) is the air in a band round M (the band less the solid beside M, on the
    grid: air_near()).  caps: [(near, z, sign)], where the shell wraps over
    the copper's face at height z, going up (sign 1) or down (-1), within `near`.

    The metals are laid outward from the copper in order, as the face's finish is laid upward. With
    o_k the drawn thicknesses summed and h_k the real ones, metal k fills the air between o_(k-1) and
    o_k from the copper over the body, and, past the face, everything within o_k of the copper
    between z + h_(k-1) and z + h_k, where the face's finish is.  So the shells, the finish on the
    face and the copper meet with no gap and no overlap.

    The air the finish fills (air_of the band within o_K of the copper) is cut once, on the grid, and
    split between the metals along their outer sides (each grown from the copper and put on the grid
    on its own) in floating point: two metals side by side share the same edges, vertex for vertex.

    nets: [(net, the area its shells may take)], the first net keeping an area two nets share, or
    [(None, None)] for one part per metal.  -> [(part, region, z0, z1, layer, net, props)], to add
    in this order (add_all)."""
    drawn = [drawn_thickness(t) for _, t in layers]
    joins = mitre()
    outers = [grow(M, o, **joins) for o in accumulate(drawn)]
    # each metal's own area: inside its outer side, outside the one below (the first: inside its own)
    bands = [outers[0]] + [exactly(shapely.difference(outer, inner)) for inner, outer in zip(outers, outers[1:])]
    air = air_of(outers[-1])
    near = [sh.polys_only(shapely.intersection(air, sh.polys_only(n))) for n, _, _ in caps]
    adds, h_prev = [], 0.0
    for (metal, t), d, band, outer in zip(layers, drawn, bands, outers):
        h = h_prev + t
        pieces = [(within(air, band), *body)]
        for (_, z, sign), cap in zip(caps, near):
            pieces += [(within(cap, band), z, z + sign * h_prev), (within(cap, outer), z + sign * h_prev, z + sign * h)]
        meta = props(side, metal, t, drawn_thickness_mm=round(d, 9))
        taken = EMPTY
        for net, area in nets:
            for region, z0, z1 in pieces:
                if area is not None:
                    region = noded(exactly(shapely.difference(shapely.intersection(region, area), taken)))
                adds.append((part(metal, net), region, z0, z1, layer, net, dict(meta)))
            if area is not None:
                taken = union([taken, area])
        h_prev = h
    return adds


def add_all(ps, adds):
    """Add the shells' prisms (from shells()) to the PrismSet, in order."""
    for name, region, z0, z1, layer, net, meta in adds:
        ps.add(name, "finish", region, z0, z1, layer=layer, net=net, props=meta)
