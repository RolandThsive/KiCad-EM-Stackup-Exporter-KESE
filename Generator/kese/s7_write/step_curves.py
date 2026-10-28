"""Exact edges for STEP: one polygon ring -> a closed wire of straight edges, circular arcs and
whole circles, in output coordinates."""
import math

import numpy as np

from kese.s7_write.step_arcs import mid
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


def wire(pts, arcs, z, cq, M):
    """Closed wire of one ring (vertices and arcs from step_arcs.ring_arcs) in output coordinates:
    every arc a true circular arc, a whole circle one circle edge, every other edge straight."""
    V = lambda p: cq.Vector(*xf(M, p[0], p[1], z))
    if not arcs:
        return cq.Wire.makePolygon([V(p) for p in pts], close=True)
    n = len(pts)
    if arcs[0][1] - arcs[0][0] == n:         # a full circle: one closed edge, seam at a fixed angle
        c, r = arcs[0][2], arcs[0][3]
        normal = M[:3, :3] @ np.array([0.0, 0.0, 1.0])
        scale = float(np.linalg.norm(normal))
        return cq.Wire.assembleEdges([cq.Edge.makeCircle(r * scale, V(c), cq.Vector(*map(float, normal / scale)))])
    edges, k = [], arcs[0][0]                # walk once around the ring from the first arc
    for i, j, c, r, ccw in arcs:
        for m in range(k, i):                # straight edges up to the arc
            edges.append(cq.Edge.makeLine(V(pts[m % n]), V(pts[(m + 1) % n])))
        edges.append(cq.Edge.makeThreePointArc(V(pts[i % n]), V(mid(pts, i, j, c, r, ccw)), V(pts[j % n])))
        k = j
    for m in range(k, arcs[0][0] + n):       # straight edges back to the start
        edges.append(cq.Edge.makeLine(V(pts[m % n]), V(pts[(m + 1) % n])))
    return cq.Wire.assembleEdges(edges)
