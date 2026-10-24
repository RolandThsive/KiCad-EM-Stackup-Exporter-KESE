"""The board outline from Edge.Cuts: closed shapes as they are, open lines and arcs joined into
faces.  An outline inside another one is a cut-out."""
import math

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
        digits = max(0, round(-math.log10(B.OUTLINE_LINE_SNAP_MM)))
        noded = shapely.union_all([LineString(np.round(np.asarray(g.coords), digits)) for g in items.edge_open])
        faces = list(polygonize(noded))
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
    solid = union([s for s, d in zip(uniq, depth) if d % 2 == 0])
    cut = union([s for s, d in zip(uniq, depth) if d % 2 == 1])
    return solid.difference(cut)
