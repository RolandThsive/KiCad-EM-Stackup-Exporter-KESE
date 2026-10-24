"""The board frame: KiCad's (x, y down) becomes (x - cx, -(y - cy)), Y up with F.Cu toward +Z,
with the origin per Run.ORIGIN.  Every shape that passes through it is snapped to the grid."""
from shapely import affinity

from kese.core import shapes2d as sh
from kese.core.shapes2d import EMPTY
from parameters import P


def place(r, outline_k):
    """Set r.to_board, r.transform_note, r.to_board_T and r.outline from the KiCad-frame outline."""
    R = P.Run
    minx, miny, maxx, maxy = outline_k.bounds
    if R.ORIGIN == "center":
        cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
        r.transform_note = f"origin: outline centre ({cx:.4f}, {cy:.4f}) in KiCad coordinates"
    else:
        cx, cy = 0.0, 0.0
        r.transform_note = "origin: KiCad page origin"
    r.to_board = (cx, cy)
    # KiCad (x, y down) -> board (x - cx, -(y - cy)): Y up, F.Cu toward +Z
    T = lambda g: sh.snap(affinity.affine_transform(sh.polys_only(g), [1, 0, 0, -1, -cx, cy])) \
        if g is not None and not g.is_empty else EMPTY
    r.to_board_T = T
    r.outline = T(outline_k)
