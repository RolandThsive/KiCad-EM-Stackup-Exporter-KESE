"""Which runs of an outline's vertices a STEP file writes as true circular arcs (Step.STEP_EXACT_ARCS):
those that lie on one circle within STEP_ARC_FIT_TOLERANCE_MM, turning the same way by the same
angle at every vertex as a faceted circle does (find_arcs).  Every arc is written on the circle
through its two end vertices and the fitted circle's point halfway between them, so that its ends
lie on it exactly.  In board mm."""
import math
from typing import NamedTuple

import numpy as np

TAU = 2 * math.pi


class Fit(NamedTuple):
    """What a run of vertices must do to be an arc (from Step.STEP_ARC_*)."""
    tol: float            # mm: every vertex this close to one circle
    points: int           # at least this many vertices
    sweep: float          # radians: turning at least this far in all
    turn: float           # radians: and at most this far at any one vertex (a faceted circle turns little)
    max_sweep: float      # radians: a longer arc is cut in pieces
    uneven_max: float     # no chord spans more than this many times the median chord's angle
    uneven_min: float     # and none but the first and last less than this many times


def fit_of(S):
    """The Fit of the Step settings S (P.Step)."""
    return Fit(S.STEP_ARC_FIT_TOLERANCE_MM, S.STEP_ARC_MIN_POINTS, math.radians(S.STEP_ARC_MIN_SWEEP_DEG),
               math.radians(S.STEP_ARC_MAX_TURN_DEG), math.radians(S.STEP_ARC_MAX_SWEEP_DEG),
               S.STEP_ARC_TURN_RATIO_MAX, S.STEP_ARC_TURN_RATIO_MIN)


def fit_circle(q):
    """Least-squares circle (Kasa fit) through points (rows): (centre, radius, largest deviation).
    In plain floats: the runs are short (six points, typically), and tens of thousands of them cost
    numpy more in calls than in sums."""
    xs, ys = q[:, 0].tolist(), q[:, 1].tolist()
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    x, y = [v - mx for v in xs], [v - my for v in ys]
    sxx = sxy = syy = sxz = syz = sz = 0.0
    for u, v in zip(x, y):
        z = u * u + v * v
        sxx, sxy, syy, sxz, syz, sz = sxx + u * u, sxy + u * v, syy + v * v, sxz + u * z, syz + v * z, sz + z
    det = sxx * syy - sxy * sxy
    if det <= 0:
        return np.array([mx, my]), 0.0, math.inf
    a, b = 0.5 * (syy * sxz - sxy * syz) / det, 0.5 * (sxx * syz - sxy * sxz) / det
    r = math.sqrt(a * a + b * b + sz / n)
    return np.array([mx + a, my + b]), r, max(abs(math.hypot(u - a, v - b) - r) for u, v in zip(x, y))


def on_one_circle(q, fit):
    """Whether the points q (rows, in order) are a faceted arc: within fit.tol of one circle, every
    chord turning the same way by at most fit.turn, and by about the same angle (fit.uneven_max and
    fit.uneven_min times the median; the first and last chord may be shorter, where a boolean cut
    the arc).  -> (centre, radius, counter-clockwise,
    sweep in radians) or None."""
    c, r, dev = fit_circle(q)
    if dev > fit.tol or r <= 0:
        return None
    cx, cy = float(c[0]), float(c[1])
    a = [math.atan2(y - cy, x - cx) for x, y in q.tolist()]
    turn = [(a1 - a0 + math.pi) % TAU - math.pi for a0, a1 in zip(a, a[1:])]
    size = [abs(t) for t in turn]
    med, biggest = sorted(size)[len(size) // 2], max(size)          # (the upper median)
    if med <= 0 or biggest > fit.turn or (max(turn) > 0 and min(turn) < 0) or biggest > fit.uneven_max * med \
            or (len(size) > 2 and min(size[1:-1]) < fit.uneven_min * med):
        return None
    return c, r, turn[0] > 0, float(sum(size))


def find_arcs(q, closed, fit):
    """The arcs of one chain of vertices q (rows; for a closed chain the last row repeats the
    first): [(i, j, centre, radius, ccw)], the arc running from vertex i to vertex j, arcs sharing
    at most their ends, each turning at most fit.max_sweep.  A closed chain may be restarted at
    another vertex s so that its start does not split an arc: -> (s, arcs, whole), the arcs'
    vertices counted from s, whole when the chain is a whole circle in two halves, on one circle
    (with fit.max_sweep under 180 degrees, more pieces, each on a circle of its own)."""
    n = len(q) - 1
    if n + (not closed) < fit.points:               # (a closed chain's last vertex is its first)
        return 0, [], False
    if closed:
        whole = on_one_circle(q, fit)
        if whole is not None and abs(whole[3] - TAU) < 1e-6:
            k = max(2, math.ceil(TAU / fit.max_sweep - 1e-9))
            if k == 2:
                return 0, [(0, n // 2, *whole[:3]), (n // 2, n, *whole[:3])], True
            cuts = [m * n // k for m in range(k + 1)]
            return 0, [(i, j, *whole[:3]) for i, j in zip(cuts[:-1], cuts[1:]) if j - i >= 2], False
    arcs, s = _runs(q, fit), 0
    if closed and arcs and arcs[0][1] < n:          # restart where the first arc ends and look again
        s = arcs[0][1]
        q = np.concatenate([q[s:-1], q[:s + 1]])
        arcs = _runs(q, fit)
    return s, [piece for arc in arcs for piece in _pieces(q, *arc, fit.max_sweep)], False


def _runs(q, fit):
    """The arcs of an open chain, each as long as it goes from where the last one ended.  Only
    vertices where the chain turns one way by at most fit.turn can be inside an arc, so the
    search runs on the stretches of those (each arc grown by doubling, then halving)."""
    d = np.diff(q, axis=0)
    h = np.arctan2(d[:, 1], d[:, 0])
    turn = (np.diff(h) + math.pi) % TAU - math.pi            # at vertices 1 .. n-1
    ok = (np.abs(turn) <= fit.turn) & (turn != 0)
    sign = np.where(ok, np.sign(turn), 0)
    arcs = []
    # stretches of inner vertices turning one way: the arc can run one vertex further at each end
    brk = np.flatnonzero(np.r_[True, sign[1:] != sign[:-1], True])
    for a, b in zip(brk[:-1].tolist(), brk[1:].tolist()):
        if sign[a] == 0 or b - a + 2 < fit.points:
            continue
        lo, hi = a, b + 1                                     # vertices lo .. hi
        i = max(lo, arcs[-1][1]) if arcs else lo              # not back into the arc before (an S-bend)
        while hi - i + 1 >= fit.points:
            j = i + fit.points - 1
            got = on_one_circle(q[i:j + 1], fit)
            if got is None:
                i += 1
                continue
            step, bad = 1, None
            while j < hi:                                     # gallop: double the step until it fails
                k = min(j + step, hi)
                f = on_one_circle(q[i:k + 1], fit)
                if f is None:
                    bad = k
                    break
                j, got, step = k, f, step * 2
            while bad is not None and bad - j > 1:            # then halve between the last pass and the fail
                k = (j + bad) // 2
                f = on_one_circle(q[i:k + 1], fit)
                if f is None:
                    bad = k
                else:
                    j, got = k, f
            if got[3] >= fit.sweep:
                arcs.append((i, j, *got[:3]))
                i = j
            else:
                i += 1
    return arcs


def _pieces(q, i, j, c, r, ccw, max_sweep):
    """An arc cut into pieces that turn at most max_sweep, at vertices spread evenly."""
    _, sweep = sweep_of(c, q[i], q[j], ccw)
    k = max(1, math.ceil(abs(sweep) / max_sweep - 1e-9))
    cuts = [i + round(m * (j - i) / k) for m in range(k + 1)]
    return [(s, e, c, r, ccw) for s, e in zip(cuts[:-1], cuts[1:]) if e - s >= 2]


def sweep_of(c, p, q, ccw):
    """Start angle and signed sweep about c of the arc from p to q, counter-clockwise or not."""
    a0 = math.atan2(p[1] - c[1], p[0] - c[0])
    a1 = math.atan2(q[1] - c[1], q[0] - c[0])
    return a0, (a1 - a0) % TAU if ccw else -((a0 - a1) % TAU)


def written_circle(p, q, c, r, ccw):
    """The circle an arc from p to q on the fitted circle (c, r) is written on: through p, q and
    the fitted circle's point halfway between them.  -> (centre, radius) or None (on one line)."""
    a0, sweep = sweep_of(c, p, q, ccw)
    m = (c[0] + r * math.cos(a0 + sweep / 2), c[1] + r * math.sin(a0 + sweep / 2))
    (x1, y1), (x2, y2), (x3, y3) = p, m, q
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-18:
        return None
    s1, s2, s3 = x1 * x1 + y1 * y1, x2 * x2 + y2 * y2, x3 * x3 + y3 * y3
    cx = (s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2)) / d
    cy = (s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1)) / d
    return np.array([cx, cy]), math.hypot(x1 - cx, y1 - cy)
