"""The finish inside the plated holes open at a face (finish_shells.py does the rest of the finish
beside the copper): a shell per metal over the bore and onto the ring's finish on the face, the
hole spans' bores in groups, Parallel.WORKERS at a time, in threads, each on its own copies of the
shapes it uses (kese/core/shape_copies.py).  KiCad 10's via protection and post machining close
some bores and cut others back."""
import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.graph import connected_components, pairs_within
from kese.core.parallel import in_parallel
from kese.core.shape_copies import own
from kese.core.shapes2d import union
from kese.s3_resolve.holes import drilled, full_height
from kese.s4_geometry.shells import add_all, air_near, bare_faces, groups, named, near_faces, note, reach, shells
from kese.s4_geometry.via_fill import plug_ranges
from parameters import P


def closed_end(h, side, before):
    """Whether a via's protection (KiCad 10) closes its end on `side` before the finish goes on: a
    cap or a plug there, or a covering when the finish comes after the mask."""
    p = h.protect
    return p is not None and not p.opened[side] and (p.capped or p.plugged[side] or (p.covered[side] and not before))


def open_stretches(bottom, top, cuts, plugs):
    """[(z0, z1, open below, open above)]: the stretches of a bore from bottom to top that hold air,
    between the plugs [(z0, z1)] and the cuts of post machining and backdrills [(z0, z1)] (whose ring is
    gone there), with whether each end opens onto a cut (air)."""
    gaps = sorted([(max(a, bottom), min(b, top), True) for a, b in cuts if min(b, top) > max(a, bottom)]
                  + [(max(a, bottom), min(b, top), False) for a, b in plugs if min(b, top) > max(a, bottom)])
    out, z, open_below = [], bottom, False
    for a, b, air in gaps:
        if a > z + 1e-9:
            out.append((z, a, open_below, air))
        if b > z:
            z, open_below = b, air
    if top > z + 1e-9:
        out.append((z, top, open_below, False))
    return out


def bores(r, ps, layers, edge_zone):
    """The finish inside the plated holes open at a face, over the whole bore and onto the ring's
    finish ("Hole Finish <metal>"): the baths run through them.  A hole closed at both faces (buried,
    or tented on both) gets none; castellations have the edge's.  KiCad 10: a filled via gets none, a
    plugged one only where its bore is open, a backdrilled or post machined one only on what is left
    of its barrel, open onto the cavity.  -> the bores' zone, or None."""
    st, last = r.stackup, len(r.layers) - 1
    before = P.Finish.FINISH_BEFORE_SOLDER_MASK
    spans = {}                      # (top layer, bottom layer, (open at F, open at B), z0, z1) -> [(ring, net)]
    for n, h in enumerate(r.items.holes):
        if not (h.plated and h.wall > 0) or h.castellated or (h.protect is not None and h.protect.filled):
            continue
        drill = r.to_board_T(h.drill)
        # an end at a face is open unless the mask closes it (a tented via); with the finish before
        # the mask, every end at a face is open
        ends = tuple(at_face and not closed_end(h, s, before) and (before or drill.intersects(r.mask_open[s]))
                     for s, at_face in (("F", h.i == 0), ("B", h.j == last)))
        ring_k = h.drill.difference(h.drill.buffer(-h.wall))
        cuts = [(z0, z1) for z0, z1, d in r.barrel_cuts.get(n, []) if sh.inter(ring_k, d).area > 0]
        if not any(ends) and not cuts:
            continue
        # from an open end at a face, or from the copper that closes the bore: an inner layer's, or a
        # face's that a cap or a copper fill leaves whole over it
        shut = {s: h.protect is not None and h.protect.copper_shut(s, P.Copper.VIA_FILL) for s in ("F", "B")}
        bottom = st.band["B.Cu"][0 if not shut["B"] else 1] if h.j == last else st.band[r.layers[h.j]][1]
        top = st.band["F.Cu"][1 if not shut["F"] else 0] if h.i == 0 else st.band[r.layers[h.i]][0]
        ring = r.to_board_T(ring_k)
        for z0, z1, air_below, air_above in open_stretches(bottom, top, cuts, plug_ranges(st, r.layers, h)):
            at = (ends[0] and z1 == top, ends[1] and z0 == bottom)
            if any(at) or air_below or air_above:
                spans.setdefault((h.i, h.j, at, z0, z1), []).append((ring, h.net))
    if not spans:
        return None
    d, faces = reach(layers), bare_faces(r)
    copper = {key: sh.snap(union([m for m, _ in rings])) for key, rings in spans.items()}
    # solid beside the bores: the drilled board, the barrels, every layer's copper, the face's finish,
    # the edge's finish and the rings themselves (so that each span's copper lies in it); each bore
    # is cut by what lies near it alone
    # (the holes through the whole board: a backdrill or post machining is not air at every height)
    air = air_near([drilled(r, full_height)] + [ring for ring, *_ in r.barrels]
                   + list(r.copper_all.values()) + list(faces.values()) + list(copper.values()) + [edge_zone])
    near = {s: near_faces(faces[s], d) for s in ("F", "B") if not faces[s].is_empty}

    def bores_of(job):
        (i, j, (open_f, open_b), bottom, top), group = job
        rings = own([spans[job[0]][k] for k in group])
        caps = [(own(near[s]), z, sign) for s, z, sign, is_open in (("F", top, 1, open_f), ("B", bottom, -1, open_b))
                if is_open and s in near]
        first = {}                  # each net where it first comes in the span: who keeps an area two share
        for k, (_, net) in enumerate(spans[job[0]]):
            first.setdefault(net, k)
        nets = sorted(groups(rings, d), key=lambda g: first.get(g[0], -1))
        return shells(layers, sh.snap(union([m for m, _ in rings])), nets, air, (bottom, top), caps, named("Hole"),
                      "Hole.Finish", "Hole")

    jobs = [(key, group) for key, rings in spans.items() for group in bore_groups([m for m, _ in rings], d)]
    for adds in in_parallel(bores_of, jobs):
        add_all(ps, adds)
    note(ps, "inside the plated holes", layers, "wall")
    return union([near_faces(M, d) for M in copper.values()])


def bore_groups(rings, d):
    """A span's rings (their indices, in order) in groups of about Geometry.FINISH_BORES_AT_A_TIME, worked
    on each in a thread of its own: rings within 2 d (and Geometry.AIR_NEAR_MARGIN_STEPS grid steps) of
    each other, whose shells could meet, in one group, and the groups' rings near each other (Z order of
    the board), so that each group cuts and clips a small corner of the board.  The groups do not
    depend on the number of threads, so neither do the files."""
    most = sh.G().FINISH_BORES_AT_A_TIME
    if len(rings) <= most:
        return [list(range(len(rings)))]
    a, b = pairs_within(rings, 2 * d + sh.G().AIR_NEAR_MARGIN_STEPS * sh.grid())
    _, label = connected_components(len(rings), a, b)
    centre = shapely.centroid(np.asarray(rings, dtype=object))
    xy, there = np.zeros((len(rings), 2)), ~shapely.is_empty(centre)        # an empty ring (no drill): at 0, 0
    xy[there] = shapely.get_coordinates(centre[there])
    cell = np.floor((xy - xy.min(axis=0)) / max(float(np.ptp(xy, axis=0).max()), 1e-9) * 1023.999).astype(np.int64)
    z = sum(((cell[:, 0] >> bit & 1) << 2 * bit) | ((cell[:, 1] >> bit & 1) << 2 * bit + 1) for bit in range(10))
    order = np.argsort(label, kind="stable")
    members = np.split(order, np.flatnonzero(np.diff(label[order])) + 1)    # each cluster's rings, in order
    out, group = [], []
    for c in sorted(range(len(members)), key=lambda c: (z[members[c][0]], members[c][0])):   # at its first ring
        group += members[c].tolist()
        if len(group) >= most:
            out.append(sorted(group))
            group = []
    return out + ([sorted(group)] if group else [])
