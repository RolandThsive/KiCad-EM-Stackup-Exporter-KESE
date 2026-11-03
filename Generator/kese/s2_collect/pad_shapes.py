"""Pad shapes, centred on the pad's origin: circle, rect, oval, roundrect, trapezoid and custom."""
from shapely.geometry import LineString, Polygon, box

from kese.core import shapes2d as sh
from kese.core.sexp import child, num
from kese.core.shapes2d import EMPTY, disk, thicken, union
from kese.s1_read.parse_kicad_version import roundrect_ratio
from kese.s2_collect.drawings import GRAPHICS, graphic, painted


def pad_shape(items, pad, w, h):
    shape = pad[3]
    if shape == "circle":
        return disk((0, 0), w / 2)
    if shape == "rect":
        return box(-w / 2, -h / 2, w / 2, h / 2)
    if shape == "oval":
        return oval(w, h)
    if shape == "roundrect":
        rounded = sh.rounded_rect(-w / 2, -h / 2, w / 2, h / 2, roundrect_ratio(pad) * min(w, h))
        return chamfered(pad, rounded, w, h)
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


def oval(w, h):
    """A w x h stadium centred on the origin (a circle when w == h): an oval pad or drill."""
    if abs(w - h) < 1e-9:
        return disk((0, 0), w / 2)
    d = abs(w - h) / 2
    return thicken(LineString([(-d, 0), (d, 0)] if w > h else [(0, -d), (0, d)]), min(w, h))


CORNERS = {"top_left": (-1, -1), "top_right": (1, -1), "bottom_right": (1, 1), "bottom_left": (-1, 1)}


def chamfered(pad, rounded, w, h):
    """A rounded rectangle pad with the corners its (chamfer ...) lists cut straight, the cut's legs
    chamfer_ratio x the shorter side, and those corners not rounded (KiCad's chamfered rectangle,
    TransformRoundChamferedRectToPolygon).  KiCad's frame: top is -y."""
    c = child(pad, "chamfer")
    cut = num(pad, "chamfer_ratio", 0.0) * min(w, h)
    corners = [CORNERS[str(a)] for a in (c[1:] if c else []) if str(a) in CORNERS]
    if not corners:
        return rounded
    sharp = [box(min(0, sx * w / 2), min(0, sy * h / 2), max(0, sx * w / 2), max(0, sy * h / 2)) for sx, sy in corners]
    shape = union([rounded, *sharp])           # the listed corners square again (radius 0)
    if cut > 0:
        tris = [Polygon([(sx * w / 2, sy * h / 2), (sx * (w / 2 - cut), sy * h / 2), (sx * w / 2, sy * (h / 2 - cut))])
                for sx, sy in corners]
        shape = shape.difference(union(tris))
    return shape
