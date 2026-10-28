"""Footprints in KiCad 7's format.  Pads and footprint text are given in the footprint's own frame
with angles relative to it; footprint() writes them the way KiCad 7 stores them (positions local,
angles absolute)."""
from kicad7 import effects, f, fill, pts, q, stroke, xy


def pad(num, kind, shape, at, size, layers, angle=0, drill=None, net=None, **opt):
    """kind: thru_hole, np_thru_hole, smd or connect.  drill: a diameter, ("oval", w, h), and
    opt["offset"] = (x, y) for an offset drill.  Other opt: rratio, chamfer=(ratio, corners),
    delta=(dx, dy), prop, remove_unused, keep_end, mask_margin, anchor, primitives, zone_connect."""
    return dict(kind="pad", num=num, type=kind, shape=shape, at=at, size=size, layers=layers,
                angle=angle, drill=drill, net=net, opt=opt)


def text(kind, s, at, layer, angle=0, hide=False, **fx):
    """kind: reference, value or user."""
    return dict(kind="text", type=kind, s=s, at=at, layer=layer, angle=angle, hide=hide, fx=fx)


def shape(kind, layer, width=0.12, filled=False, **geo):
    """kind: line (a, c), rect (a, c), circle (c, r), arc (start, mid, end) or poly (points)."""
    return dict(kind="shape", type=kind, layer=layer, width=width, filled=filled, geo=geo)


def footprint(b, lib, at, angle=0, side="F", children=(), mask_margin=None, attr=None, model=None):
    """A footprint.  Without a value text it gets the empty one KiCad would add, so that its
    timestamp does not change from one run to the next."""
    if not any(c["kind"] == "text" and c["type"] == "value" for c in children):
        children = [*children, text("value", "", (0, 0), "F.SilkS", size=1.27, thickness=0.15)]
    s = f"(footprint {q(lib)} (layer {q(side + '.Cu')}) {b.ts()} (at {xy(at)}{' ' + f(angle) if angle else ''})"
    if mask_margin is not None:
        s += f" (solder_mask_margin {f(mask_margin)})"
    if attr:
        s += f" (attr {attr})"
    for c in children:
        s += "\n    " + (_pad(b, c, angle) if c["kind"] == "pad" else
                         _text(b, c, angle) if c["kind"] == "text" else _shape(b, c))
    if model:
        s += (f"\n    (model {q(model)} (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))")
    return s + ")"


def _angle(local, fp_angle):
    a = (local + fp_angle) % 360
    return f" {f(a)}" if a else ""


def _text(b, t, fp_angle):
    return (f"(fp_text {t['type']} {q(t['s'])} (at {xy(t['at'])}{_angle(t['angle'], fp_angle)}) "
            f"(layer {q(t['layer'])}){' hide' if t['hide'] else ''} {effects(**t['fx'])} {b.ts()})")


def _shape(b, c):
    g, lay = c["geo"], f"(layer {q(c['layer'])})"
    body = {"line": lambda: f"(fp_line (start {xy(g['a'])}) (end {xy(g['c'])}) {stroke(c['width'])}",
            "rect": lambda: f"(fp_rect (start {xy(g['a'])}) (end {xy(g['c'])}) {stroke(c['width'])} {fill(c['filled'])}",
            "circle": lambda: (f"(fp_circle (center {xy(g['c'])}) (end {xy((g['c'][0] + g['r'], g['c'][1]))}) "
                               f"{stroke(c['width'])} {fill(c['filled'])}"),
            "arc": lambda: f"(fp_arc (start {xy(g['start'])}) (mid {xy(g['mid'])}) (end {xy(g['end'])}) {stroke(c['width'])}",
            "poly": lambda: f"(fp_poly {pts(g['points'])} {stroke(c['width'])} {fill(c['filled'])}"}[c["type"]]()
    return f"{body} {lay} {b.ts()})"


def _pad(b, p, fp_angle):
    o = p["opt"]
    s = f"(pad {q(p['num'])} {p['type']} {p['shape']} (at {xy(p['at'])}{_angle(p['angle'], fp_angle)})"
    s += f" (size {xy(p['size'])})"
    if "delta" in o:
        s += f" (rect_delta {xy(o['delta'])})"
    d = p["drill"]
    if d is not None:
        hole = f"oval {f(d[1])} {f(d[2])}" if isinstance(d, tuple) else f(d)
        off = f" (offset {xy(o['offset'])})" if "offset" in o else ""
        s += f" (drill {hole}{off})"
    if "prop" in o:
        s += f" (property {o['prop']})"
    s += " (layers " + " ".join(q(l) for l in p["layers"]) + ")"
    s += " (remove_unused_layers)" * bool(o.get("remove_unused")) + " (keep_end_layers)" * bool(o.get("keep_end"))
    if "rratio" in o:
        s += f" (roundrect_rratio {f(o['rratio'])})"
    if "chamfer" in o:
        s += f" (chamfer_ratio {f(o['chamfer'][0])}) (chamfer {' '.join(o['chamfer'][1])})"
    if p["net"]:
        s += f" (net {b.n(p['net'])} {q(p['net'])})"
    if "mask_margin" in o:
        s += f" (solder_mask_margin {f(o['mask_margin'])})"
    if "zone_connect" in o:
        s += f" (zone_connect {o['zone_connect']})"
    if "primitives" in o:
        s += f" (options (clearance outline) (anchor {o.get('anchor', 'circle')}))"
        s += " (primitives " + " ".join(o["primitives"]) + ")"
    return s + f" {b.ts()})"


def prim_poly(points, width=0):
    return f"(gr_poly {pts(points)} (width {f(width)}) (fill yes))"


def prim_circle(c, r, width=0):
    return f"(gr_circle (center {xy(c)}) (end {xy((c[0] + r, c[1]))}) (width {f(width)}) (fill yes))"


def prim_line(a, c, width):
    return f"(gr_line (start {xy(a)}) (end {xy(c)}) (width {f(width)}))"


def prim_rect(a, c, width=0):
    return f"(gr_rect (start {xy(a)}) (end {xy(c)}) (width {f(width)}) (fill yes))"
