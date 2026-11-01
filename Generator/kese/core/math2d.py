"""The plain mathematics every other module builds on: distances, circles through points, arcs,
Bezier curves and rotations.  Nothing here reads parameters or knows about boards."""
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
