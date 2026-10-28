"""Pad shapes, centred on the pad's origin: circle, rect, oval, roundrect, trapezoid and custom."""
from shapely.geometry import LineString, Polygon, box

from kese.core import shapes2d as sh
from kese.core.sexp import child, num
from kese.core.shapes2d import EMPTY, disk, thicken, union
from kese.s2_collect.drawings import GRAPHICS, graphic, painted


def pad_shape(items, pad, w, h):
    shape = pad[3]
    if shape == "circle":
        return disk((0, 0), w / 2)
    if shape == "rect":
        return box(-w / 2, -h / 2, w / 2, h / 2)
    if shape == "oval":
        if abs(w - h) < 1e-9:
            return disk((0, 0), w / 2)
        d = abs(w - h) / 2
        return thicken(LineString([(-d, 0), (d, 0)] if w > h else [(0, -d), (0, d)]), min(w, h))
    if shape == "roundrect":
        return sh.rounded_rect(-w / 2, -h / 2, w / 2, h / 2, num(pad, "roundrect_rratio", 0.25) * min(w, h))
    if shape == "trapezoid":
        rd = child(pad, "rect_delta")
        dx, dy = (float(rd[1]) / 2, float(rd[2]) / 2) if rd else (0.0, 0.0)
        return Polygon([(-w / 2 - dy, h / 2 + dx), (w / 2 + dy, h / 2 - dx),
                        (w / 2 - dy, -h / 2 + dx), (-w / 2 + dy, -h / 2 - dx)])
    if shape == "custom":
        opts = child(pad, "options")
        anchor = child(opts, "anchor")[1] if opts and child(opts, "anchor") else "circle"
        parts = [disk((0, 0), w / 2) if anchor == "circle" else box(-w / 2, -h / 2, w / 2, h / 2)]
        for prim in (child(pad, "primitives") or [])[1:]:
            if isinstance(prim, list) and prim[0] in GRAPHICS:
                geom, closed, pw, filled = graphic(prim, lambda p: p)
                parts.append(painted(geom, closed, pw, filled))
        return union(parts)
    items.skipped[f"pads of shape {shape}"] += 1
    return EMPTY
