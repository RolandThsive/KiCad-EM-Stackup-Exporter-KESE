"""Footprints in the file formats of KiCad 6 to 10, from the pad, text and shape dicts of
footprints7.  Pads take KiCad 10's options too: backdrill, tertiary, front_pm and back_pm (see
kicad_later.drills), tenting=(front, back), and padstack=(mode, {layer: dict(shape, size, ...)}),
mode front_inner_back (layers "Inner" and "B.Cu") or custom (every copper layer but F.Cu)."""
from footprints7 import text
from kicad7 import f, pts, q, xy
from kicad_later import K7, K8, K9, K10, _shape, drills, effects, front_back, layer_list

FIELDS = {"reference": "Reference", "value": "Value"}


def footprint(b, lib, at, angle=0, side="F", children=(), mask_margin=None, attr=None, model=None):
    """A footprint; without a value text it gets the empty one KiCad 7 adds (see footprints7)."""
    v = b.version
    if not any(c["kind"] == "text" and c["type"] == "value" for c in children):
        children = [*children, text("value", "", (0, 0), "F.SilkS", size=1.27, thickness=0.15)]
    s = f"(footprint {q(lib)} (layer {q(side + '.Cu')})" + (" (tedit 0)" if v < K7 else "")
    s += f" {b.ts()} (at {xy(at)}{' ' + f(angle) if angle else ''})"
    fields = [c for c in children if c["kind"] == "text" and c["type"] in FIELDS]
    if v >= K8:                                   # fields come first from KiCad 8 on
        s += "".join(" " + _text(b, t, angle) for t in fields)
    s += f" (solder_mask_margin {f(mask_margin)})" if mask_margin is not None else ""
    s += f" (attr {attr})" if attr else ""
    s += " (duplicate_pad_numbers_are_jumpers no)" if v >= K10 else ""
    if v < K8:
        s += "".join(" " + _text(b, t, angle) for t in fields)
    rest = [c for c in children if c not in fields]
    s += "".join(" " + (_text(b, c, angle) if c["kind"] == "text" else _fp_shape(b, c))
                 for c in rest if c["kind"] != "pad")
    s += "".join(" " + _pad(b, c, angle) for c in rest if c["kind"] == "pad")
    s += " (embedded_fonts no)" if v >= K9 else ""
    if model:
        s += f" (model {q(model)} (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))"
    return s + ")"


def _text(b, t, fp_angle):
    """Footprint text: angles are written absolute, positions in the footprint's frame."""
    v, angle = b.version, (t["angle"] + fp_angle) % 360
    fx = effects(b, **t["fx"])
    if v < K8:
        a = f" {f(angle)}" if angle else ""
        return (f"(fp_text {t['type']} {q(t['s'])} (at {xy(t['at'])}{a}) (layer {q(t['layer'])})"
                f"{' hide' if t['hide'] else ''} {fx} {b.ts()})")
    field = t["type"] in FIELDS
    head = f"(property {q(FIELDS[t['type']])} {q(t['s'])}" if field else f"(fp_text user {q(t['s'])}"
    hide = " (hide yes)" if t["hide"] and (field or v < K9) else ""
    return f"{head} (at {xy(t['at'])} {f(angle)}) (layer {q(t['layer'])}){hide} {b.ts()} {fx})"


def _fp_shape(b, c):
    g = c["geo"]
    geo = {"line": lambda: f"(start {xy(g['a'])}) (end {xy(g['c'])})",
           "rect": lambda: f"(start {xy(g['a'])}) (end {xy(g['c'])})",
           "circle": lambda: f"(center {xy(g['c'])}) (end {xy((g['c'][0] + g['r'], g['c'][1]))})",
           "arc": lambda: f"(start {xy(g['start'])}) (mid {xy(g['mid'])}) (end {xy(g['end'])})",
           "poly": lambda: pts(g["points"])}[c["type"]]()
    filled = c["filled"] if c["type"] in ("rect", "circle", "poly") else None
    return _shape(b, c["type"], geo, c["layer"], c["width"], filled, prefix="fp")


def _corners(o, shape):
    s = f" (roundrect_rratio {f(o.get('rratio', 0))})" if shape == "roundrect" else ""
    if "chamfer" in o:
        s += f" (chamfer_ratio {f(o['chamfer'][0])}) (chamfer {' '.join(o['chamfer'][1])})"
    return s


def _pad(b, p, fp_angle):
    v, o = b.version, p["opt"]
    angle = (p["angle"] + fp_angle) % 360
    s = f"(pad {q(p['num'])} {p['type']} {p['shape']} (at {xy(p['at'])}{' ' + f(angle) if angle else ''})"
    s += f" (size {xy(p['size'])})" + (f" (rect_delta {xy(o['delta'])})" if "delta" in o else "")
    d = p["drill"]
    if d is not None:
        hole = f"oval {f(d[1])} {f(d[2])}" if isinstance(d, tuple) else f(d)
        s += f" (drill {hole}" + (f" (offset {xy(o['offset'])})" if "offset" in o else "") + ")"
    s += drills(o) if v >= K10 else ""
    s += f" (property {o['prop']})" if "prop" in o else ""
    s += " " + layer_list(b, p["layers"], quoted_wildcards=v >= K7)
    if p["type"] == "thru_hole" and (v >= K8 or o.get("remove_unused")):
        s += " " + b.flag("remove_unused_layers", o.get("remove_unused", False))
        if o.get("remove_unused"):
            s += (" " + b.flag("keep_end_layers", o.get("keep_end", False))) * (v >= K8 or o.get("keep_end", False))
            s += " (zone_layer_connections)" * (v >= K8)
    s += _corners(o, p["shape"])
    s += " " + b.pad_net(p["net"]) if p["net"] else ""
    s += f" (solder_mask_margin {f(o['mask_margin'])})" if "mask_margin" in o else ""
    s += f" (zone_connect {o['zone_connect']})" if "zone_connect" in o else ""
    if "primitives" in o:
        s += f" (options (clearance outline) (anchor {o.get('anchor', 'circle')}))"
        s += " (primitives " + " ".join(o["primitives"]) + ")"
    if "tenting" in o and v >= K10:
        s += " " + front_back("tenting", o["tenting"])
    s += " " + b.ts()
    if "padstack" in o and v >= K10:
        mode, layers = o["padstack"]
        s += f" (padstack (mode {mode})"
        for name, l in layers.items():
            s += f" (layer {q(name)} (shape {l['shape']}) (size {xy(l['size'])})" + _corners(l, l["shape"]) + ")"
        s += ")"
    return s + ")"

