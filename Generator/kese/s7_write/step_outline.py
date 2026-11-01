"""The plan view of a part's Topology for its arcs (step_curved): its points, the segments between
them, the heights of each, the chains of points an arc can run through, and the arcs found on them.
In board mm."""
import math

import numpy as np

from kese.core.vertices import grid_keys
from kese.s7_write import step_arcs as sa
from parameters import P


class Outline:
    """The plan view of a Topology: its points, the segments between them (a horizontal edge at any
    height), the heights each segment is at, and the chains of points an arc can run through."""


def outline_of(topo):
    """Topology -> its Outline, or None when no point of it can be inside an arc."""
    o = Outline()
    xy = topo.xyz[:, :2]
    _, first, o.pt = np.unique(grid_keys(xy), return_index=True, return_inverse=True)
    o.xy = xy[first]
    o.levels, o.lev = np.unique(topo.xyz[:, 2], return_inverse=True)
    h = np.flatnonzero(~topo.vertical)
    a, b = o.pt[topo.edge_start[h]], o.pt[topo.edge_end[h]]
    lo, hi = np.minimum(a, b), np.maximum(a, b)
    _, sf, seg_of_h = np.unique(lo * len(o.xy) + hi, return_index=True, return_inverse=True)
    o.seg_a, o.seg_b = lo[sf], hi[sf]
    o.edge_seg = np.full(len(topo.edge_start), -1)
    o.edge_seg[h] = seg_of_h
    # the heights of every segment, as bits
    words = (len(o.levels) + 63) // 64
    o.mask = np.zeros((len(o.seg_a), words), dtype=np.uint64)
    lv = o.lev[topo.edge_start[h]]
    np.bitwise_or.at(o.mask, (seg_of_h, lv // 64), np.left_shift(np.uint64(1), (lv % 64).astype(np.uint64)))
    # a point an arc can pass: two neighbours in plan, and every vertex on it with two horizontal edges
    n = len(o.xy)
    degree = np.bincount(o.seg_a, minlength=n) + np.bincount(o.seg_b, minlength=n)
    hdeg = np.bincount(topo.edge_start[h], minlength=len(o.pt)) + np.bincount(topo.edge_end[h], minlength=len(o.pt))
    o.through = degree == 2
    o.through[o.pt[hdeg != 2]] = False
    if not o.through.any():
        return None
    o.chains = chains(o)
    return o


def chains(o):
    """The chains of segments through the points an arc can pass: [(points, segments, closed)],
    an open chain from one other point to another, a closed one (all its points passable) from one
    of its points around to it again (the point repeated at the end).  Chains of fewer points than an arc needs are left out."""
    n, seg_a, seg_b = len(o.xy), o.seg_a.tolist(), o.seg_b.tolist()
    ends = np.concatenate([o.seg_a, o.seg_b])
    order = np.argsort(ends, kind="stable")
    seg_at = (order % len(seg_a)).tolist()
    start = np.r_[0, np.cumsum(np.bincount(ends, minlength=n))].tolist()
    through = o.through.tolist()
    shortest = P.Run.STEP_ARC_MIN_POINTS
    seen = bytearray(len(seg_a))
    chains = []

    def walk(p, s):
        """From point p along segment s, on through passable points: (points, segments)."""
        pts, segs = [p], []
        while True:
            seen[s] = 1
            segs.append(s)
            p = seg_a[s] + seg_b[s] - p
            pts.append(p)
            if not through[p] or p == pts[0]:
                return pts, segs
            s0, s1 = seg_at[start[p]], seg_at[start[p] + 1]
            s = s1 if s0 == s else s0

    for p in np.flatnonzero(~o.through).tolist():
        for k in range(start[p], start[p + 1]):
            s = seg_at[k]
            q = seg_a[s] + seg_b[s] - p
            if seen[s] or not through[q]:
                continue
            pts, segs = walk(p, s)
            if len(pts) >= shortest:
                chains.append((pts, segs, False))
    for p in np.flatnonzero(o.through).tolist():
        s = seg_at[start[p]]
        if seen[s]:
            continue
        pts, segs = walk(p, s)
        if len(pts) >= shortest:
            chains.append((pts, segs, True))
    return chains


def arcs_of(o):
    """The arcs of every chain: [(chain, i, j, circle, ccw)], circles in o.circles as (centre,
    radius); the two halves of a whole circle share one."""
    R = P.Run
    fit = sa.Fit(R.STEP_ARC_FIT_TOLERANCE_MM, R.STEP_ARC_MIN_POINTS, math.radians(R.STEP_ARC_MIN_SWEEP_DEG),
                 math.radians(R.STEP_ARC_MAX_TURN_DEG))
    o.circles, pieces = [], []
    for k, (pts, segs, closed) in enumerate(o.chains):
        s, arcs, whole = sa.find_arcs(o.xy[pts], closed, fit)
        if s:                                                   # a closed chain restarted at another point
            pts, segs = pts[s:-1] + pts[:s + 1], segs[s:] + segs[:s]
            o.chains[k] = (pts, segs, closed)
        q2 = o.xy[pts]
        if whole:
            i, j, c, r, ccw = arcs[0]
            circle = sa.written_circle(q2[i], q2[j], c, r, ccw)
            if circle is None:
                continue
            o.circles.append(circle)
            pieces += [(k, i, j, len(o.circles) - 1, ccw), (k, j, arcs[1][1], len(o.circles) - 1, ccw)]
            continue
        for i, j, c, r, ccw in arcs:
            circle = sa.written_circle(q2[i], q2[j], c, r, ccw)
            if circle is not None:
                o.circles.append(circle)
                pieces.append((k, i, j, len(o.circles) - 1, ccw))
    return pieces
