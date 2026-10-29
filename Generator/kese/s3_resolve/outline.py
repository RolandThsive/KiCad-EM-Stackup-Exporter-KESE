"""The board outline from Edge.Cuts: closed shapes as they are, open lines and arcs joined into
faces.  An outline inside another one is a cut-out, and an outline inside a cut-out a board again."""
import numpy as np
import shapely
from shapely.geometry import LineString, Polygon
from shapely.ops import polygonize

from kese.core.shapes2d import union
from parameters import P


def outline_from(items, log):
    """The outline in KiCad's frame."""
    B = P.Board
    rings = list(items.edge_closed)
    if items.edge_open:
        lines, gap = joined_ends(items.edge_open, B.OUTLINE_LINE_SNAP_MM)
        if gap:
            log(f"note: Edge.Cuts line ends up to {gap:.6f} mm apart joined "
                f"(Board.OUTLINE_LINE_SNAP_MM = {B.OUTLINE_LINE_SNAP_MM} mm)")
        faces = list(polygonize(shapely.union_all(lines)))
        rings += [Polygon(f.exterior) for f in faces]
        if not faces:
            log("warning: Edge.Cuts lines/arcs do not form a closed outline")
    uniq = []
    for r in rings:
        if r.is_valid and r.area > 1e-9 and not any(r.symmetric_difference(u).area < 1e-6 for u in uniq):
            uniq.append(r)
    if not uniq:
        if B.OUTLINE_FALLBACK == "error":
            raise ValueError("no Edge.Cuts outline and OUTLINE_FALLBACK is 'error'")
        log(f"warning: no Edge.Cuts outline; using the copper's convex hull + {B.OUTLINE_FALLBACK_MARGIN_MM} mm")
        allcu = union([g for gs in items.copper_items.values() for g, _ in gs])
        return allcu.convex_hull.buffer(B.OUTLINE_FALLBACK_MARGIN_MM)
    depth = [sum(1 for j, o in enumerate(uniq) if j != i and o.contains(s)) for i, s in enumerate(uniq)]
    # as KiCad does: a cut-out is taken out of the outline one level up that holds it, so an outline
    # inside a cut-out is a board again
    return union([s.difference(union([h for h, e in zip(uniq, depth) if e == d + 1 and s.contains(h)]))
                  for s, d in zip(uniq, depth) if d % 2 == 0])


def joined_ends(lines, d):
    """The open lines (rounded to KiCad's 1 nm), with every loose end moved onto the nearest other
    loose end within d, the closest pairs first, as KiCad chains the Edge.Cuts shapes of an outline.
    Ends that already meet are left as they are, so a run of tiny segments never folds up.  Returns
    the lines and the widest gap joined (0 if none)."""
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
