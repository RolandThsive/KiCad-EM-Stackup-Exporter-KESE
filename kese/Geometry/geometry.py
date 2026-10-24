"""geometry.py - the plain mathematics every other module builds on: distances, circles through
points, arcs, Bezier curves, rotations, and recognising circular arcs in a polyline.

Nothing here reads parameters or knows about boards; every function takes numbers and returns
numbers (or lists of points)."""
import math

import numpy as np

TAU = 2 * math.pi


def distance(a, b):
    """Euclidean distance between two points."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def rotation(origin, angle_deg):
    """Point transform for a KiCad footprint: local (x, y) -> board (x, y).
    KiCad rotates counter-clockwise on screen, whose Y axis points down."""
    fx, fy = origin
    rad = math.radians(angle_deg)
    c, s = math.cos(rad), math.sin(rad)
    return lambda p: (fx + p[0] * c + p[1] * s, fy - p[0] * s + p[1] * c)


def circle_through(p1, p2, p3):
    """Centre (cx, cy) and radius of the circle through three points, or None if collinear."""
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-12:
        return None
    s1, s2, s3 = x1 * x1 + y1 * y1, x2 * x2 + y2 * y2, x3 * x3 + y3 * y3
    cx = (s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2)) / d
    cy = (s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1)) / d
    return (cx, cy), math.hypot(x1 - cx, y1 - cy)


def angle(c, p):
    """Angle of point p seen from centre c, in radians."""
    return math.atan2(p[1] - c[1], p[0] - c[0])


def arc_sweep(c, p1, p2, p3):
    """Start angle and signed sweep (radians) of the arc p1 -> p2 -> p3 about centre c."""
    a1, a2, a3 = angle(c, p1), angle(c, p2), angle(c, p3)
    ccw = (a2 - a1) % TAU <= (a3 - a1) % TAU
    return a1, (a3 - a1) % TAU if ccw else -((a1 - a3) % TAU)


def arc_points(c, r, a0, sweep, n):
    """n + 1 points along the arc of radius r about c from angle a0 over `sweep` radians."""
    return [(c[0] + r * math.cos(a0 + sweep * i / n), c[1] + r * math.sin(a0 + sweep * i / n)) for i in range(n + 1)]


def bezier_points(p, n):
    """n + 1 points along the cubic Bezier with control points p[0..3]."""
    t = np.linspace(0, 1, n + 1)[:, None]
    p = np.asarray(p, dtype=float)
    pts = (1 - t) ** 3 * p[0] + 3 * (1 - t) ** 2 * t * p[1] + 3 * (1 - t) * t ** 2 * p[2] + t ** 3 * p[3]
    return [tuple(q) for q in pts]


def fit_circle(points):
    """Least-squares circle (Kasa fit) through points: (cx, cy), r, largest radial deviation."""
    q = np.asarray(points, dtype=float)
    x, y = q[:, 0], q[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(q))]
    sol, *_ = np.linalg.lstsq(A, x * x + y * y, rcond=None)
    cx, cy = sol[0], sol[1]
    r = math.sqrt(max(sol[2] + cx * cx + cy * cy, 0.0))
    dev = np.abs(np.hypot(x - cx, y - cy) - r).max()
    return (cx, cy), r, dev


def arcs_in_ring(coords, tol, min_points=5, min_sweep_deg=10.0):
    """Find runs of consecutive vertices of a closed ring that lie on one circle.

    coords: ring vertices without the repeated closing point.
    Returns a list of (start index, end index, centre, radius, counter_clockwise): the arc runs
    from coords[start] through coords[end] (indices mod n, end may wrap past n).  A run is accepted
    when every vertex is within `tol` of the fitted circle, it has at least min_points vertices and
    spans at least min_sweep_deg.  Runs share at most their end points.  A full circle is returned
    with end = start + n."""
    pts = [tuple(map(float, p)) for p in coords]
    n = len(pts)
    if n < min_points:
        return []
    used = [False] * n
    arcs = []
    i = 0
    while i < n:
        j, fit = i + 2, None
        best = None
        while j - i < n:
            run = [pts[k % n] for k in range(i, j + 1)]
            if any(used[k % n] for k in range(i + 1, j + 1)):
                break
            c, r, dev = fit_circle(run)
            if dev > tol or r <= 0:
                break
            # a faceted arc turns by the same angle at every vertex (its first and last chord may
            # be shorter where a boolean cut it); turns keep one sense and stay below a half-turn
            a = [angle(c, p) for p in run]
            turns = [((a[k + 1] - a[k] + math.pi) % TAU) - math.pi for k in range(len(a) - 1)]
            size = sorted(abs(t) for t in turns)
            med = size[len(size) // 2]
            if any(abs(t) > math.pi / 2 for t in turns) or (max(turns) > 0 and min(turns) < 0) \
                    or size[-1] > 1.3 * med or any(abs(t) < 0.7 * med for t in turns[1:-1]):
                break
            best, fit = j, (c, r, turns[0] > 0, abs(sum(turns)))
            if j - i + 1 == n:               # all vertices: a full circle if the closing chord fits too
                closing = ((a[0] - a[-1] + math.pi) % TAU) - math.pi
                if abs(closing) <= 1.3 * med and (closing > 0) == (turns[0] > 0):
                    best = i + n
            j += 1
        if best is not None and best - i + 1 >= min_points and math.degrees(fit[3]) >= min_sweep_deg:
            c, r, ccw, _ = fit
            arcs.append((i, best, c, r, ccw))
            for k in range(i, best + 1):
                used[k % n] = True
            i = best
        else:
            i += 1
    return arcs
