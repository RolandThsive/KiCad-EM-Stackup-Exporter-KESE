"""Which arcs a STEP file can write without their curve crossing another edge (step_curved): an
arc bulges out from the chords it replaces, and where another edge at one of its heights passes
closer than that it stays straight.  In board mm."""
import math

import numpy as np
import shapely

from kese.s7_write import step_arcs as sa
from parameters import P

# An edge that leaves an arc's end and cuts into its circle by less than this only touches the arc,
# as a line that leaves it along its tangent does (OpenCascade takes two curves that come within
# about 2e-7 of the file's unit for touching; in mm, the stricter unit, that is 2e-7 mm)
TANGENT_MM = 5e-8


def clear(o, pieces, margin):
    """The arcs of `pieces` (step_outline.arcs_of) that cannot cross anything.  The bulge is up to
    Geometry.CIRCLE_CHORD_TOLERANCE_MM on a circle KESE faceted, so an edge passing closer, as
    along a sliver between two pads, would make the face invalid.  No segment at the arc's heights
    may enter its strip (strip), except those that leave its end vertices: they may run along the
    curve there (an outline that doubles back, or goes on along the tangent) but not cut into its
    circle (meets).  No two arcs' strips at one height may overlap.  An arc whose vertices do not
    follow its written circle in order, or that is not at the same heights all along, is dropped."""
    rows, strips, u, w, ok, mask = [], [], [], [], [], []
    seg_piece = np.full(len(o.seg_a), -1)
    near = 3 * P.Run.STEP_ARC_FIT_TOLERANCE_MM
    for m, (k, i, j, ci, ccw) in enumerate(pieces):
        pts, segs, _ = o.chains[k]
        c, r = o.circles[ci]
        q = o.xy[pts[i:j + 1]].tolist()            # (plain floats: an arc has a few vertices, and there are many arcs)
        cx, cy = float(c[0]), float(c[1])
        a0, sweep = sa.sweep_of((cx, cy), q[0], q[-1], ccw)
        d = [math.hypot(x - cx, y - cy) for x, y in q]
        rows.append((cx, cy, r, a0, sweep))
        strips.append(strip(q, d, (cx, cy), r, a0, sweep, margin))
        u.append(pts[i])
        w.append(pts[j])
        chords = segs[i:j]
        seg_piece[chords] = m
        mask.append(o.mask[chords[0]])
        # the vertices follow the written circle, in order along the arc, at the same heights all along
        sign = math.copysign(1, sweep)
        t = [0.0] + [(math.atan2(y - cy, x - cx) - a0) * sign % sa.TAU for x, y in q[1:-1]] + [abs(sweep)]
        ok.append(bool((o.mask[chords] == o.mask[chords[0]]).all())
                  and max(abs(di - r) for di in d) <= near and all(t1 > t0 for t0, t1 in zip(t, t[1:])))
    rows, strips, u, w = np.array(rows), np.array(strips, dtype=object), np.array(u), np.array(w)
    mask = np.array(mask)
    bad = ~shapely.is_valid(strips) | ~np.array(ok)
    lines = shapely.linestrings(np.stack([o.xy[o.seg_a], o.xy[o.seg_b]], axis=1))
    s, e = shapely.STRtree(lines).query(strips, predicate="intersects")
    keep = (seg_piece[e] != s) & (mask[s] & o.mask[e]).any(axis=1) & ~bad[s]
    s, e = s[keep], e[keep]
    at_u = (o.seg_a[e] == u[s]) | (o.seg_b[e] == u[s])
    at_w = (o.seg_a[e] == w[s]) | (o.seg_b[e] == w[s])
    beside = at_u ^ at_w                     # (a segment joining both ends cannot cross the arc)
    other = ~at_u & ~at_w
    hit = shapely.relate_pattern(strips[s[other]], lines[e[other]], "T********")   # into, not just onto
    bad[s[other][hit]] = True
    sb, eb = s[beside], e[beside]
    v = np.where(at_u[beside], u[sb], w[sb])
    far = o.seg_a[eb] + o.seg_b[eb] - v
    bad[sb[meets(rows[sb], o.xy[v], o.xy[far])]] = True
    good = np.flatnonzero(~bad)              # two arcs whose strips overlap at a height may cross: neither is kept
    a, b = shapely.STRtree(strips[good]).query(strips[good], predicate="intersects")
    a, b = good[a[a < b]], good[b[a < b]]
    same_height = (mask[a] & mask[b]).any(axis=1)
    a, b = a[same_height], b[same_height]
    hit = shapely.relate_pattern(strips[a], strips[b], "T********")
    bad[a[hit]] = True
    bad[b[hit]] = True
    return [p for p, x in zip(pieces, bad.tolist()) if not x]


def strip(q, d, c, r, a0, sweep, margin):
    """What an arc through the vertices q (a list of (x, y), d their distances from the centre c)
    adds to its face or cuts off it, between their chords and the curve, and `margin` on both sides
    of the curve: a shapely polygon.  From the inner vertices, those closer than `margin` inside the
    curve moved there, out to `margin` outside the curve or to the furthest vertex, closed at the end
    vertices."""
    cx, cy = c
    k = math.ceil(abs(sweep) / min(math.pi / 4, math.sqrt(margin / r)))
    step = sweep / k
    ro = max(r + margin, max(d)) / math.cos(step / 2)            # the corners of a polyline outside the curve
    outer = [(cx + ro * math.cos(a), cy + ro * math.sin(a)) for a in (a0 + step * (n + 0.5) for n in range(k))]
    inner = [(cx + (x - cx) * f, cy + (y - cy) * f) for (x, y), di in zip(q[1:-1], d[1:-1]) for f in (min(di, r - margin) / di,)]
    return shapely.Polygon([q[0], *outer, q[-1], *inner[::-1]])


def meets(arc, v, o):
    """Whether edges that leave an arc's end vertex v for o cross the arc's curve: the edge's line
    meets the circle a second time, on the edge and on the arc, and cuts into the circle by more
    than TANGENT_MM (by less it only touches the arc, as a line along its tangent does).  arc: rows
    of (centre x, y, radius, start angle, signed sweep)."""
    d = o - v
    c, dd = v - arc[:, 0:2], np.einsum("ij,ij->i", d, d)
    t = -2 * np.einsum("ij,ij->i", c, d) / dd                    # the edge's line meets the circle there too
    x = c + t[:, None] * d
    turn = (np.arctan2(x[:, 1], x[:, 0]) - arc[:, 3]) * np.sign(arc[:, 4]) % sa.TAU
    deep = arc[:, 2] - np.abs(c[:, 0] * d[:, 1] - c[:, 1] * d[:, 0]) / np.sqrt(dd)
    return (t > 0) & (t <= 1) & (turn <= np.abs(arc[:, 4])) & (deep > TANGENT_MM)
