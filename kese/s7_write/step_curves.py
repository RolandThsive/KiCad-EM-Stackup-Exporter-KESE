"""Exact edges for STEP: one polygon ring -> a closed wire of straight edges, circular arcs and
whole circles, in output coordinates."""
import math

import numpy as np

from kese.core import math2d as geo
from parameters import P


def xf(M, x, y, z):
    v = M @ np.array([x, y, z, 1.0])
    return float(v[0]), float(v[1]), float(v[2])


class Circles:
    """The board's exact circles (Model.circles: drill walls, plated bores, via pads), looked up by
    a ring's fitted circle.  A ring that closes on one of them is written with that circle, so every
    part that meets a hole uses the very same curve; fitting each part's polygon separately gives
    circles a few nm apart, and fusing those leaves sliver faces that CAD importers reject."""

    CELL = 0.01   # mm

    def __init__(self, circles):
        self.tol = 2 * P.Geometry.CIRCLE_CHORD_TOLERANCE_MM
        self.grid = {}
        for c, r in circles:
            self.grid.setdefault(self._key(c), []).append((c, r))

    def _key(self, c):
        return round(c[0] / self.CELL), round(c[1] / self.CELL)

    def match(self, c, r):
        """The exact circle nearest the fit (c, r) within tolerance, else the fit itself."""
        kx, ky = self._key(c)
        best, err = (c, r), self.tol
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for c2, r2 in self.grid.get((kx + dx, ky + dy), ()):
                    e = max(math.hypot(c2[0] - c[0], c2[1] - c[1]), abs(r2 - r))
                    if e <= err:
                        best, err = (c2, r2), e
        return best


def wire(ring, z, cq, M, circles):
    """Closed wire of one polygon ring in output coordinates.  With STEP_EXACT_ARCS the vertex
    runs that lie on one circle (faceted vias, pads, round outlines, track ends, arc tracks)
    become true circular arcs; everything else stays a straight edge.  A ring that is a whole
    circle becomes one circle edge, on the board's exact circle when it is one (see Circles)."""
    R = P.Run
    pts = list(ring.coords)[:-1]
    V = lambda p: cq.Vector(*xf(M, p[0], p[1], z))
    arcs = geo.arcs_in_ring(pts, R.STEP_ARC_FIT_TOLERANCE_MM, R.STEP_ARC_MIN_POINTS) if R.STEP_EXACT_ARCS else []
    if not arcs:
        return cq.Wire.makePolygon([V(p) for p in pts], close=True)
    n = len(pts)
    if arcs[0][1] - arcs[0][0] < n:          # an arc found at index 0 may continue from the ring's end:
        s = arcs[0][1] % n                   # restart the ring where it ends and look again
        pts = pts[s:] + pts[:s]
        arcs = geo.arcs_in_ring(pts, R.STEP_ARC_FIT_TOLERANCE_MM, R.STEP_ARC_MIN_POINTS)
    if arcs[0][1] - arcs[0][0] == n:         # a full circle: one closed edge, seam at a fixed angle
        c, r = circles.match(arcs[0][2], arcs[0][3])
        normal = M[:3, :3] @ np.array([0.0, 0.0, 1.0])
        scale = float(np.linalg.norm(normal))
        return cq.Wire.assembleEdges([cq.Edge.makeCircle(r * scale, V(c), cq.Vector(*map(float, normal / scale)))])
    on = lambda c, r, a: (c[0] + r * math.cos(a), c[1] + r * math.sin(a))
    edges, k = [], arcs[0][0]                # walk once around the ring from the first arc
    for i, j, c, r, ccw in arcs:
        for m in range(k, i):                # straight edges up to the arc
            edges.append(cq.Edge.makeLine(V(pts[m % n]), V(pts[(m + 1) % n])))
        a0, a1 = geo.angle(c, pts[i % n]), geo.angle(c, pts[j % n])
        sweep = (a1 - a0) % geo.TAU if ccw else -((a0 - a1) % geo.TAU)
        edges.append(cq.Edge.makeThreePointArc(V(pts[i % n]), V(on(c, r, a0 + sweep / 2)), V(pts[j % n])))
        k = j
    for m in range(k, arcs[0][0] + n):       # straight edges back to the start
        edges.append(cq.Edge.makeLine(V(pts[m % n]), V(pts[(m + 1) % n])))
    return cq.Wire.assembleEdges(edges)
