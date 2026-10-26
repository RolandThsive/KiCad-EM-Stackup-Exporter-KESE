"""Which runs of a ring's vertices a STEP file writes as true circular arcs: those that lie on one
circle (math2d.arcs_in_ring), a whole circle on the board's exact circle when it is one
(step_curves.Circles), and only where the arc cannot cross anything (_clear).  In board mm."""
import math

import numpy as np
import shapely

from kese.core import math2d as geo
from parameters import P

# An edge that leaves an arc's end and cuts into its circle by less than this only touches the arc,
# as a line that leaves it along its tangent does.  OpenCascade takes two curves that come within
# about 2e-7 of the file's unit for touching, and in mm, the stricter unit, that is 2e-7 mm.
TANGENT_MM = 5e-8


def ring_arcs(polys, circles):
    """The rings of the polygons, [exterior, holes...] per polygon, each as (vertices, arcs) for
    step_curves.wire, an arc being (start, end, centre, radius, counter_clockwise).  With
    STEP_EXACT_ARCS the vertex runs that lie on one circle (faceted vias, pads, round outlines,
    track ends, arc tracks) are arcs, and a ring that is a whole circle is one."""
    R = P.Run
    rings = [list(ring.coords)[:-1] for p in polys for ring in (p.exterior, *p.interiors)]
    fits = [_fit(pts, circles) for pts in rings] if R.STEP_EXACT_ARCS else [(pts, []) for pts in rings]
    fits = _clear(fits, P.Geometry.SNAP_GRID_MM)
    out, k = [], 0
    for p in polys:
        out.append(fits[k:k + 1 + len(p.interiors)])
        k += 1 + len(p.interiors)
    return out


def _fit(pts, circles):
    """One ring's arcs, the ring restarted where its first arc ends so that the ring's start does
    not split an arc: (vertices, arcs)."""
    R = P.Run
    find = lambda q: geo.arcs_in_ring(q, R.STEP_ARC_FIT_TOLERANCE_MM, R.STEP_ARC_MIN_POINTS)
    arcs, n = find(pts), len(pts)
    if arcs and arcs[0][1] - arcs[0][0] < n:     # an arc found at index 0 may continue from the ring's end:
        s = arcs[0][1] % n                       # restart the ring where it ends and look again
        pts = pts[s:] + pts[:s]
        arcs = find(pts)
    if arcs and arcs[0][1] - arcs[0][0] == n:    # a whole circle
        i, j, c, r, ccw = arcs[0]
        arcs = [(i, j, *circles.match(c, r), ccw)]
    return pts, arcs


def _clear(fits, margin):
    """The fits with only the arcs that cannot cross anything.  An arc bulges out from the chords
    it replaces, up to 5 µm on a circle KiCad faceted; where another outline passes closer than
    that, as along a sliver between two pads, the curve would cross it and the face would be
    invalid.  So no edge of the rings may enter an arc's strip (_strip), but for the two edges at
    its ends, which may run along the curve there (where an outline doubles back or goes on along
    the tangent) but not cut into its circle (_meets); and no two arcs' strips may overlap.
    Otherwise the vertices stay straight."""
    owner, strips, rows = [], [], []
    for g, (pts, arcs) in enumerate(fits):
        n = len(pts)
        for i, j, c, r, ccw in arcs:
            cv = curve(pts, i, j, c, r, ccw)
            owner.append((g, i, j - i, n))
            strips.append(_strip(pts, i, j, cv, margin))
            rows.append((*cv[0], *cv[1:]) if cv else (math.nan,) * 5)
    if not strips:
        return fits
    owner, strips, rows = np.array(owner), np.array(strips, dtype=object), np.array(rows, dtype=float)
    bad = ~shapely.is_valid(strips)
    # every edge of every ring, with the ring it is on and its place there
    ring = np.concatenate([np.full(len(pts), g) for g, (pts, _) in enumerate(fits)])
    place = np.concatenate([np.arange(len(pts)) for pts, _ in fits])
    xy = [np.asarray(pts, dtype=float) for pts, _ in fits]
    ends = np.concatenate([np.stack([x, np.roll(x, -1, axis=0)], axis=1) for x in xy])
    edges = shapely.linestrings(ends)
    s, e = shapely.STRtree(edges).query(strips, predicate="intersects")
    ok = ~bad[s]                            # (an arc without a valid strip is dropped already)
    s, e = s[ok], e[ok]
    g, i, span, n = owner[s].T
    at = np.where(ring[e] == g, (place[e] - i) % n, -1)     # the edge's place on the arc's ring, from the arc's start
    after, before = at == span, (at == n - 1) & (at > span)    # the edges from its last vertex and to its first
    beside = (after | before) & (span < n - 1)              # (one edge that joins both cannot cross it; a circle has none)
    other = (at < 0) | ((at > span) & (at < n - 1))         # (its own chords are neither)
    bad[s[other][shapely.relate_pattern(strips[s[other]], edges[e[other]], "T********")]] = True   # into, not just onto
    bad[s[beside][_meets(rows[s[beside]], ends[e[beside]], after[beside], TANGENT_MM)]] = True
    keep = np.flatnonzero(~bad)             # two arcs whose strips overlap may cross: neither is kept
    a, b = shapely.STRtree(strips[keep]).query(strips[keep], predicate="intersects")
    a, b = keep[a[a < b]], keep[b[a < b]]
    hit = shapely.relate_pattern(strips[a], strips[b], "T********")
    bad[a[hit]] = True
    bad[b[hit]] = True
    out, k = [], 0
    for pts, arcs in fits:
        out.append((pts, [arc for m, arc in enumerate(arcs) if not bad[k + m]]))
        k += len(arcs)
    return out


def _meets(arc, seg, after, tangent):
    """Whether edges that join arcs at an end cross the arcs' curves: the edge's line meets the
    circle a second time, on the edge and on the arc, and cuts into the circle by more than
    `tangent` (by less it only touches the arc, as a line along its tangent does, however far it
    runs along it).  arc: rows of (centre x, y, radius, start angle, sweep); seg: the edges' two
    ends; after: the edge starts at the arc's last vertex, else it ends at its first."""
    v = np.where(after[:, None], seg[:, 0], seg[:, 1])     # the vertex the edge shares with the arc
    d = np.where(after[:, None], seg[:, 1], seg[:, 0]) - v
    c, dd = v - arc[:, 0:2], np.einsum("ij,ij->i", d, d)   # (from the centre)
    t = -2 * np.einsum("ij,ij->i", c, d) / dd               # the edge's line meets the circle there too
    x = c + t[:, None] * d
    turn = (np.arctan2(x[:, 1], x[:, 0]) - arc[:, 3]) * np.sign(arc[:, 4]) % geo.TAU
    deep = arc[:, 2] - np.abs(c[:, 0] * d[:, 1] - c[:, 1] * d[:, 0]) / np.sqrt(dd)   # how far the line cuts into the circle
    return (t > 0) & (t <= 1) & (turn <= np.abs(arc[:, 4])) & (deep > tangent)


def curve(pts, i, j, c, r, ccw):
    """The circle an arc is written on, and where: (centre, radius, start angle, signed sweep).  A
    whole circle is its own; a partial arc's passes through its end vertices and mid(), as
    step_curves.wire writes it.  None when those three points are on one line."""
    n = len(pts)
    if j - i == n:
        return c, r, 0.0, geo.TAU
    circle = geo.circle_through(pts[i % n], mid(pts, i, j, c, r, ccw), pts[j % n])
    if circle is None:
        return None
    return (*circle, *_sweep(circle[0], pts[i % n], pts[j % n], ccw))


def _strip(pts, i, j, cv, margin):
    """What an arc adds to its face or cuts off it, between its vertices' chords and its curve,
    and `margin` on both sides of the curve: a shapely polygon (None without a curve).  For a
    partial arc, from its inner vertices, those closer than `margin` inside the curve moved there,
    out to `margin` outside the curve or to its furthest vertex, closed at its end vertices.  For a
    whole circle, the ring from its nearest chord or `margin` inside it out to `margin` outside it
    or its furthest vertex (the board's exact circle may lie a little off the vertices)."""
    if cv is None:
        return None
    c, r, a0, sweep = cv
    n = len(pts)
    q = np.array([pts[m % n] for m in range(i, j + 1)], dtype=float)
    d = np.hypot(*(q - c).T)
    outer = _around(c, max(r + margin, d.max()), a0, sweep, margin)
    if j - i == n:
        a, b = q[:-1], q[1:]
        t = np.clip(np.einsum("ij,ij->i", c - a, b - a) / np.einsum("ij,ij->i", b - a, b - a), 0, 1)
        inner = min(r - margin, np.hypot(*(a + t[:, None] * (b - a) - c).T).min())
        return shapely.Polygon(outer, [_around(c, inner, 0.0, geo.TAU, margin, out=False)] if inner > 0 else [])
    inner = c + (q[1:-1] - c) * (np.minimum(d[1:-1], r - margin) / d[1:-1])[:, None]
    return shapely.Polygon([q[0], *outer, q[-1], *inner[::-1]])


def _around(c, r, a0, sweep, margin, out=True):
    """Points of a polyline that follows the circle (c, r) from angle a0 over `sweep` to within
    margin / 8: with out, the corners of one whose edges touch the circle, so that it is nowhere
    inside it; else points on the circle, for one nowhere outside it."""
    k = math.ceil(abs(sweep) / min(math.pi / 4, math.sqrt(margin / r)))
    step = sweep / k
    a = a0 + step * (np.arange(k) + 0.5 * out)
    r = r / math.cos(step / 2) if out else r
    return np.c_[c[0] + r * np.cos(a), c[1] + r * np.sin(a)]


def _sweep(c, p, q, ccw):
    """Start angle and signed sweep about c of the arc from p to q, counter-clockwise or not."""
    a0, a1 = geo.angle(c, p), geo.angle(c, q)
    return a0, (a1 - a0) % geo.TAU if ccw else -((a0 - a1) % geo.TAU)


def mid(pts, i, j, c, r, ccw):
    """The point of the fitted circle halfway along an arc, which it is written through."""
    n = len(pts)
    a0, sweep = _sweep(c, pts[i % n], pts[j % n], ccw)
    return c[0] + r * math.cos(a0 + sweep / 2), c[1] + r * math.sin(a0 + sweep / 2)
