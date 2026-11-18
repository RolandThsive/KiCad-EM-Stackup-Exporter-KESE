"""The board outline from Edge.Cuts: closed shapes as they are, open lines and arcs joined into
faces.  An outline inside another one is a cut-out, and an outline inside a cut-out a board again."""
from kese.core.outlines import faces, nested
from kese.core.shapes2d import union
from parameters import P


def outline_from(items, log):
    """The outline in KiCad's frame."""
    B = P.Board
    rings = list(items.edge_closed)
    if items.edge_open:
        closed, gap = faces(items.edge_open, B.OUTLINE_LINE_SNAP_MM)
        if gap:
            log(f"note: Edge.Cuts line ends up to {gap:.6f} mm apart joined "
                f"(Board.OUTLINE_LINE_SNAP_MM = {B.OUTLINE_LINE_SNAP_MM} mm)")
        rings += closed
        if not closed:
            log("warning: Edge.Cuts lines/arcs do not form a closed outline")
    uniq = []
    for r in rings:
        if r.is_valid and r.area > B.OUTLINE_MIN_AREA_MM2 and not any(r.symmetric_difference(u).area < B.OUTLINE_DUPLICATE_AREA_MM2 for u in uniq):
            uniq.append(r)
    if not uniq:
        if B.OUTLINE_FALLBACK == "error":
            raise ValueError("no Edge.Cuts outline and OUTLINE_FALLBACK is 'error'")
        log(f"warning: no Edge.Cuts outline; using the copper's convex hull + {B.OUTLINE_FALLBACK_MARGIN_MM} mm")
        allcu = union([g for gs in items.copper_items.values() for g, _ in gs])
        return allcu.convex_hull.buffer(B.OUTLINE_FALLBACK_MARGIN_MM)
    # as KiCad does: a cut-out is taken out of the outline one level up that holds it, so an outline
    # inside a cut-out is a board again
    return nested(uniq)

