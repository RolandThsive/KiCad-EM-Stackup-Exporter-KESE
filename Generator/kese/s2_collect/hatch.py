"""Hatched fills of drawings (KiCad 10, (fill hatch|reverse_hatch|cross_hatch)): the copper, mask
opening or ink KiCad draws inside a hatched circle, rectangle or polygon besides its outline
(EDA_SHAPE::UpdateHatching in eda_shape.cpp), cut back from the drawings and text near it on its
layer (PCB_SHAPE::getHatchingKnockouts in pcb_shape.cpp).  The knockouts need every item of the
layer, so the hatches are worked out once the whole board is collected (finish)."""
import math
from dataclasses import dataclass

import numpy as np
import shapely
from shapely import affinity
from shapely.geometry import LineString, Polygon, box

from kese.core.sexp import child
from kese.core.shapes2d import EMPTY, polys_only, union

HATCHES = ("hatch", "reverse_hatch", "cross_hatch")
NM = 1_000_000                       # KiCad's internal unit: 1 nm, coordinates are whole numbers of it
SLOPES = {"hatch": -1.0, "reverse_hatch": 1.0}   # in KiCad's frame (Y down)
MAX_LINES = 100                      # a hatch has at most about this many lines across its larger side
LINE_SPACING = 10                    # the lines' pitch, in line widths (EDA_SHAPE::GetHatchLineSpacing)
ARC_LOW_DEF_MM = 0.02                # the error KiCad builds the knockouts with (ERROR_OUTSIDE)
MIN_SEGMENTS = 8                     # at least this many to a circle (MIN_SEGCOUNT_FOR_CIRCLE)
COS45 = math.cos(math.radians(45))


@dataclass
class Hatched:
    """A hatched drawing waiting for its hatch: its filled shape and pen, KiCad frame."""
    layer: str
    shape: object
    width: float
    mode: str
    footprint: object                # the footprint it belongs to (an id), or None
    net: str
    bounds: tuple                    # of the drawing with its outline's pen
    key: int                         # the drawing's id(), so that it does not knock out its own hatch


@dataclass
class Knockout:
    """A drawing or text that cuts back the hatch of another drawing of its layer."""
    layer: str
    footprint: object
    kind: str                        # "shape", "text", "field" (a footprint's reference, value, ...) or "textbox"
    bounds: tuple
    make: object                     # margin (mm) -> the shape it knocks out
    key: int = 0


def hatch_of(node):
    """A drawing's hatched fill ((fill hatch|reverse_hatch|cross_hatch)), or None."""
    fill = child(node, "fill")
    word = str(fill[1]) if fill is not None and len(fill) > 1 and not isinstance(fill[1], list) else ""
    return word if word in HATCHES else None


def spacing_nm(width, bounds):
    """The lines' pitch, nm: ten line widths, or the larger side over 100 for a big drawing."""
    spacing = LINE_SPACING * round(width * NM)
    major = max(round((bounds[2] - bounds[0]) * NM), round((bounds[3] - bounds[1]) * NM))
    return major // MAX_LINES if major // spacing > MAX_LINES else spacing


def hatch(shape, width, mode, knockouts=EMPTY):
    """The hatch KiCad draws inside `shape` (KiCad frame, mm) for a pen `width`, less `knockouts`:
    lines `width` wide at 45 degrees (hatch: rising to the right on screen, reverse_hatch: falling),
    or for cross_hatch the shape less a grid of square holes turned 45 degrees."""
    w = round(width * NM)
    if w <= 0 or shape is None or shape.is_empty:
        return EMPTY
    spacing = spacing_nm(width, shape.bounds)
    if spacing <= 0:
        return EMPTY
    if not knockouts.is_empty:
        shape = polys_only(shape.difference(knockouts))
        if shape.is_empty:
            return EMPTY
    if mode == "cross_hatch":
        return cross_hatch(shape, w, spacing, knockouts)
    return union([oval(a, b, w) for a, b in hatch_segments(shape, SLOPES[mode], spacing)])


def hatch_segments(shape, slope, spacing):
    """The pieces of the lines y = slope x + k spacing (nm, every whole k) inside the shape, as
    SHAPE_POLY_SET::GenerateHatchLines finds them: [(start, end)] in mm.  As there, the last line
    (through the far corner of the shape's box) is not drawn, nor a piece shorter than 1 nm."""
    x0, y0, x1, y1 = (round(v * NM) for v in shape.bounds)
    if slope > 0:
        lo, hi = y0 - slope * x1, y1 - slope * x0
    else:
        lo, hi = y0 - slope * x0, y1 - slope * x1
    ks = np.arange(math.ceil(lo / spacing), math.ceil(hi / spacing))
    if not len(ks):
        return []
    xa, xb = x0 - 1e3, x1 + 1e3
    lines = [LineString([(xa / NM, (slope * xa + k * spacing) / NM), (xb / NM, (slope * xb + k * spacing) / NM)])
             for k in ks]
    out = []
    for g in shapely.intersection(np.array(lines, dtype=object), shape):
        for part in shapely.get_parts(g):
            if part.geom_type == "LineString" and part.length * NM >= 1:
                c = list(part.coords)
                out.append((c[0], c[-1]))
    return out


def oval(a, b, w):
    """TransformOvalToPolygon(a, b, w, max error w, ERROR_INSIDE) as KiCad draws a hatch line: a
    stadium w nm wide whose round ends have eight sides to the circle, their corners on it."""
    r = (w // 2) / NM
    (ax, ay), (bx, by) = a, b
    length = math.hypot(bx - ax, by - ay)
    pts = [(length, r)]
    for deg in (22.5, 67.5, 112.5, 157.5):
        t = math.radians(deg)
        pts.append((length + r * math.sin(t), r * math.cos(t)))
    pts += [(length, -r), (0.0, -r)]
    for deg in (22.5, 67.5, 112.5, 157.5):
        t = math.radians(deg)
        pts.append((-r * math.sin(t), -r * math.cos(t)))
    pts.append((0.0, r))
    g = Polygon(pts)
    g = affinity.rotate(g, math.atan2(by - ay, bx - ax), origin=(0, 0), use_radians=True)
    return affinity.translate(g, ax, ay)


def turn(g, sign):
    """KiCad's SHAPE_POLY_SET::Rotate by sign x 45 degrees about the origin, to whole nm (RotatePoint:
    x' = x cos + y sin, y' = y cos - x sin)."""
    s = sign * COS45

    def f(xy):
        x, y = xy[:, 0] * NM, xy[:, 1] * NM
        return np.column_stack((np.round(x * COS45 + y * s), np.round(y * COS45 - x * s))) / NM
    return shapely.transform(g, f)


def cpp_mod(a, b):
    """C++'s a % b for whole numbers: the sign of a."""
    return int(math.fmod(a, b))


def cross_hatch(shape, w, grid, knockouts):
    """The cross hatch: the shape turned -45 degrees, less square holes (grid - w) on a grid of
    pitch `grid` (nm) from KiCad's own origin, turned back, less the knockouts again."""
    turned = turn(shape, -1)
    bx0, by0, bx1, by1 = (round(v * NM) for v in turned.bounds)
    hole = grid - w
    xs = range(bx0 - cpp_mod(bx0, grid) - grid, bx1 + 1, grid)
    ys = range(by0 - cpp_mod(by0, grid) - grid, by1 + 1, grid)
    holes = [box(x / NM, y / NM, (x + hole) / NM, (y + hole) / NM) for x in xs for y in ys]
    web = polys_only(turned.difference(shapely.coverage_union_all(np.array(holes, dtype=object)))) if holes else turned
    web = turn(web, 1)
    return polys_only(web.difference(knockouts)) if not knockouts.is_empty else web


def knocks(pending, k):
    """Whether knockout k cuts the hatch of `pending`: same layer, boxes that meet, and not text
    boxes or plain text of a footprint, nor the hatched drawing's own footprint's items."""
    if k.layer != pending.layer or k.key == pending.key:
        return False
    a, b = pending.bounds, k.bounds
    if a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1]:
        return False
    if k.footprint is None:                          # board items: drawings, text and text boxes
        return True
    return k.footprint != pending.footprint and k.kind in ("shape", "field")


def pen_growth(pen):
    """How far KiCad's knockout of a stroke-font text reaches past its letters' pen (mm): the strokes
    are ovals of ARC_LOW_DEF accuracy with all the error outside (TransformOvalToPolygon, ERROR_OUTSIDE),
    whose straight sides lie that far out."""
    r = round(pen * NM) // 2
    if r <= 0:
        return 0.0
    rel = ARC_LOW_DEF_MM * NM / r
    step = math.degrees(math.acos(1.0 - rel)) * 2 if rel < 2 else 360.0
    n = max(math.floor(360.0 / min(360.0 / MIN_SEGMENTS, step) + 0.5), 2)        # KiROUND
    n = (n + 7) // 8 * 8
    return round(abs(r * (1 - 1 / math.cos(math.pi / n)))) / NM


def text_hull(geom, pos, angle, margin):
    """A text's knockout (PCB_TEXT::TransformShapeToPolygon): the box of its letters, square to the
    text, grown by `margin` (the hatch's margin and the pen's pen_growth)."""
    upright = affinity.rotate(geom, angle, origin=pos)
    x0, y0, x1, y1 = upright.bounds
    m = margin
    return affinity.rotate(box(x0 - m, y0 - m, x1 + m, y1 + m), -angle, origin=pos)


def finish(ctx):
    """Every hatch of the board, now that every item is collected, filed with its drawing."""
    for p in ctx.hatched:
        margin = LINE_SPACING * round(p.width * NM) / 2 / NM     # half of GetHatchLineSpacing, unadjusted
        cuts = [k.make(0.0 if k.kind == "textbox" else margin) for k in ctx.knockouts if knocks(p, k)]
        region = hatch(p.shape, p.width, p.mode, union([c for c in cuts if c is not None and not c.is_empty]))
        ctx.add_more(p.layer, region, p.net)
