"""Closed areas from outline drawings, as KiCad chains them (ConvertOutlineToPolygon): the board
outline from Edge.Cuts (s3_resolve/outline.py) and a footprint's courtyard (s2_collect/courtyards.py)."""
import numpy as np
import shapely
from shapely.geometry import LineString, Polygon
from shapely.ops import polygonize

from kese.core.shapes2d import union


def faces(lines, d):
    """The faces the open lines and arcs close, their loose ends within d joined (joined_ends), each
    as its outer ring.  -> (faces, the widest gap joined)."""
    joined, gap = joined_ends(lines, d)
    return [Polygon(f.exterior) for f in polygonize(shapely.union_all(joined))], gap


def nested(rings):
    """The area of closed outlines, an outline inside another a hole in it and an outline inside a
    hole an area again: each is taken out of the one a level up that holds it."""
    depth = [sum(1 for j, o in enumerate(rings) if j != i and o.contains(s)) for i, s in enumerate(rings)]
    return union([s.difference(union([h for h, e in zip(rings, depth) if e == d + 1 and s.contains(h)]))
                  for s, d in zip(rings, depth) if d % 2 == 0])


def joined_ends(lines, d):
    """The open lines (rounded to 1 nm), every loose end moved onto the nearest other loose end within
    d, closest pairs first, as KiCad chains Edge.Cuts.  -> (lines, the widest gap joined)."""
    coords = [np.round(np.asarray(g.coords, dtype=float), 6) for g in lines]
    ends = np.array([c[k] for c in coords for k in (0, -1)])
    pts, count = np.unique(ends, axis=0, return_counts=True)
    pts = pts[count % 2 == 1]
    move, gap = {}, 0.0
    if len(pts) > 1:
        i, j = shapely.STRtree(shapely.points(pts)).query(shapely.points(pts), predicate="dwithin", distance=d)
        i, j = i[i < j], j[i < j]
        dist = np.linalg.norm(pts[i] - pts[j], axis=1)
        used = np.zeros(len(pts), bool)
        for k in np.argsort(dist, kind="stable"):
            if not used[i[k]] and not used[j[k]]:
                used[i[k]] = used[j[k]] = True
                move[tuple(pts[j[k]])] = pts[i[k]]
                gap = max(gap, float(dist[k]))
    for c in coords:
        for k in (0, -1):
            c[k] = move.get(tuple(c[k]), c[k])
    return [LineString(c) for c in coords], gap
