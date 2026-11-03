"""How a finish shell is laid in the air beside a copper region, metal by metal (finish_shells.py
says where the shells go), and the helpers the edge, the holes and the walls share."""
from itertools import accumulate

import shapely

from kese.core import shapes2d as sh
from kese.core.conformal import grow
from kese.core.shapes2d import EMPTY, union
from kese.core.vertices import noded
from kese.s4_geometry.finish import drawn_thickness, exposed, props
from parameters import P

MITRE = {"join_style": "mitre", "mitre_limit": 2.0}   # how a shell's outer side follows the copper's corners


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


def groups(pairs, d):
    """[(net, its copper grown by d)] for FINISH_GROUPING = "net", else [(None, None)]."""
    if P.Finish.FINISH_GROUPING != "net":
        return [(None, None)]
    nets = {}
    for m, net in pairs:
        nets[net] = union([nets.get(net, EMPTY), m])
    return [(net, m.buffer(d, join_style="mitre")) for net, m in nets.items()]


def exactly(g):
    """g, the result of a set operation done in floating point on regions on the grid, back on the
    grid with as little change as possible: only the new vertices, where two outlines cross, are
    rounded onto it (a part this leaves invalid is snapped as a whole).  So two regions cut along the
    same outline keep the same vertices there and still meet with no gap and no overlap, where
    snapping each on its own could round their shared edge two ways."""
    parts = shapely.get_parts(sh.polys_only(g))
    if not len(parts):
        return EMPTY
    off = ~sh.on_grid(parts)
    if not off.any():
        return sh.polys_only(g)
    rounded = shapely.set_precision(parts[off], sh.grid(), mode="pointwise")
    bad = ~shapely.is_valid(rounded) | shapely.is_empty(rounded)
    rounded[bad] = shapely.set_precision(parts[off][bad], sh.grid())
    parts[off] = rounded
    pieces = [p for q in parts for p in shapely.get_parts(sh.polys_only(q)) if not p.is_empty]
    out = shapely.MultiPolygon(pieces)
    return out if out.is_valid else sh.joined(pieces)


def within(region, area):
    """The part of `region` inside `area`, both on the grid (see exactly()), as a prism's region:
    noded the way stage 6 nodes every slice (vertices.noded).  Where a band one grid step wide comes
    out thinner than that between two slanted edges, noding closes it; closed here already, the
    prisms hold the same volume as the solids built from them."""
    return noded(exactly(shapely.intersection(sh.polys_only(region), sh.polys_only(area))))


def shells(layers, M, nets, solid, body, caps, part, layer, side):
    """Per finish metal, a shell in the air beside copper region M (board frame), outside `solid`
    (which holds M), from body = (z_lo, z_hi).  caps: [(near, z, sign)], where the shell wraps over
    the copper's face at height z, going up (sign 1) or down (-1), within `near`.

    The metals are laid outward from the copper in order, as the face's finish is laid upward. With
    o_k the drawn thicknesses summed and h_k the real ones, metal k fills the air between o_(k-1) and
    o_k from the copper over the body, and, past the face, everything within o_k of the copper
    between z + h_(k-1) and z + h_k, where the face's finish is.  So the shells, the finish on the
    face and the copper meet with no gap and no overlap.

    The air the finish fills (within o_K of the copper, less `solid`) is cut once, on the grid, and
    split between the metals along their outer sides (each grown from the copper and put on the grid
    on its own) in floating point: two metals side by side share the same edges, vertex for vertex.

    nets: [(net, the area its shells may take)], the first net keeping an area two nets share, or
    [(None, None)] for one part per metal.  -> [(part, region, z0, z1, layer, net, props)], to add
    in this order (add_all)."""
    drawn = [drawn_thickness(t) for _, t in layers]
    outers = [grow(M, o, **MITRE) for o in accumulate(drawn)]
    # each metal's own area: inside its outer side, outside the one below (the first: inside its own)
    bands = [outers[0]] + [exactly(shapely.difference(outer, inner)) for inner, outer in zip(outers, outers[1:])]
    air = sh.diff(outers[-1], solid)
    near = [sh.polys_only(shapely.intersection(air, sh.polys_only(n))) for n, _, _ in caps]
    adds, h_prev = [], 0.0
    for (metal, t), d, band, outer in zip(layers, drawn, bands, outers):
        h = h_prev + t
        pieces = [(within(air, band), *body)]
        for (_, z, sign), cap in zip(caps, near):
            pieces += [(within(cap, band), z, z + sign * h_prev), (within(cap, outer), z + sign * h_prev, z + sign * h)]
        meta = props(side, metal, t, drawn_thickness_mm=round(d, 9))
        taken = EMPTY
        for net, own in nets:
            for region, z0, z1 in pieces:
                if own is not None:
                    region = noded(exactly(shapely.difference(shapely.intersection(region, own), taken)))
                adds.append((part(metal, net), region, z0, z1, layer, net, dict(meta)))
            if own is not None:
                taken = union([taken, own])
        h_prev = h
    return adds


def add_all(ps, adds):
    """Add the shells' prisms (from shells()) to the PrismSet, in order."""
    for name, region, z0, z1, layer, net, meta in adds:
        ps.add(name, "finish", region, z0, z1, layer=layer, net=net, props=meta)
