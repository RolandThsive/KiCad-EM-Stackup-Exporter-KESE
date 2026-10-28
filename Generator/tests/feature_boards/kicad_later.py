"""Building blocks for boards in the file formats of KiCad 6, 8, 9 and 10, which KiCad 7 cannot write.
Every item has the tokens, in the order, that the matching KiCad writes (pcb_plugin.cpp for 6,
pcb_io_kicad_sexpr.cpp for 8, 9 and 10), and KiCad 8 and later lay the file out with their Prettify,
ported below.  Names and arguments follow kicad7.py and footprints7.py (pads, text and shapes of a
footprint are the dicts footprints7 makes), so a board can be described once for any version."""
import uuid

from kicad7 import NAMESPACE, NON_COPPER, copper_names, f, pts, q, xy

K6, K7, K8, K9, K10 = 20211014, 20221018, 20240108, 20241229, 20260206
GENERATOR = {K8: "8.0", K9: "9.0", K10: "10.0"}
OLD_IDS = {"F.Cu": 0, "B.Cu": 31, **{f"In{i}.Cu": i for i in range(1, 31)}, **{n: i for i, n, _ in NON_COPPER}}
NEW_IDS = {"F.Cu": 0, "B.Cu": 2, **{f"In{i}.Cu": 2 * i + 2 for i in range(1, 31)},
           "F.Mask": 1, "B.Mask": 3, "F.SilkS": 5, "B.SilkS": 7, "F.Adhes": 9, "B.Adhes": 11, "F.Paste": 13,
           "B.Paste": 15, "Dwgs.User": 17, "Cmts.User": 19, "Eco1.User": 21, "Eco2.User": 23, "Edge.Cuts": 25,
           "Margin": 27, "B.CrtYd": 29, "F.CrtYd": 31, "B.Fab": 33, "F.Fab": 35}
UI_ORDER = ["F.Adhes", "B.Adhes", "F.Paste", "B.Paste", "F.SilkS", "B.SilkS", "F.Mask", "B.Mask", "Dwgs.User",
            "Cmts.User", "Eco1.User", "Eco2.User", "Edge.Cuts", "Margin", "F.CrtYd", "B.CrtYd", "F.Fab", "B.Fab"]
USER_NAMES = {n: u for _, n, u in NON_COPPER if u}
WILDCARDS = ["*.Cu", "*.Adhes", "*.Paste", "*.SilkS", "*.Mask", "*.CrtYd", "*.Fab"]


def prettify(src):
    """KiCad's Prettify (common/io/kicad/kicad_io_utils.cpp, KiCad 10): tabs, one list per line,
    runs of (xy ...) kept on a line up to column 99, long lists of atoms wrapped after column 72."""
    out, depth, last, column = [], 0, "", 0
    in_quote = spaced = multi = in_xy = False
    backslashes = 0
    n = len(src)
    i = 0
    while i < n:
        c = src[i]
        j = i
        while j < n and src[j] in " \t\r\n":
            j += 1
        nxt = src[j] if j < n else ""
        if c in " \t\r\n" and not in_quote:
            if not spaced and depth > 0 and last != "(" and nxt not in (")", "("):
                if in_xy or column < 72:
                    out.append(" ")
                    column += 1
                else:
                    out.append("\n" + "\t" * depth)
                    column, multi = depth, True
                spaced = True
        else:
            spaced = False
            if c == "(" and not in_quote:
                cur_xy = src[i + 1:i + 4] == "xy "
                if not out:
                    out.append("(")
                    column += 1
                elif in_xy and cur_xy and column < 99:
                    out.append(" (")
                    column += 2
                else:
                    out.append("\n" + "\t" * depth + "(")
                    column = depth + 1
                in_xy = cur_xy
                depth += 1
            elif c == ")" and not in_quote:
                depth = max(depth - 1, 0)
                if last == ")" or multi:
                    out.append("\n" + "\t" * depth + ")")
                    column, multi = depth + 1, False
                else:
                    out.append(")")
                    column += 1
            else:
                if c == "\\":
                    backslashes += 1
                elif c == '"' and backslashes % 2 == 0:
                    in_quote = not in_quote
                if c != "\\":
                    backslashes = 0
                out.append(c)
                column += 1
            last = c
        i += 1
    return "".join(out) + "\n"


class Board:
    """One board in one KiCad version: its copper layers, nets, setup and items, written by text()."""

    def __init__(self, name, version, copper=2, thickness=1.6):
        self.name, self.version, self.copper, self.thickness = name, version, copper, thickness
        self.nets, self.items, self.setup, self.stackup = [""], [], [], None
        self.unfilled = set()
        self.vias = dict(tenting=(True, True), covering=(False, False), plugging=(False, False),
                         capping=False, filling=False)          # board defaults (KiCad 9 and 10)
        self._count = 0

    def ts(self):
        self._count += 1
        u = uuid.uuid5(NAMESPACE, f"{self.name}/{self._count}")
        return f"(tstamp {u})" if self.version < K8 else f'(uuid "{u}")'

    def n(self, name):
        if name not in self.nets:
            self.nets.append(name)
        return self.nets.index(name)

    def net(self, name):
        """The net of a track, via or drawing."""
        return f"(net {q(name or '')})" if self.version >= K10 else f"(net {self.n(name or '')})"

    def pad_net(self, name):
        return f"(net {q(name)})" if self.version >= K10 else f"(net {self.n(name)} {q(name)})"

    def zone_net(self, name):
        if self.version >= K10:
            return f"(net {q(name)}) " if name else ""
        return f"(net {self.n(name) if name else 0}) (net_name {q(name or '')}) "

    def flag(self, key, on=True):
        """A boolean: a bare (key) before KiCad 8, (key yes|no) from then on."""
        if self.version < K8:
            return f"({key})" if on else ""
        return f"({key} {'yes' if on else 'no'})"

    def add(self, *items):
        self.items += items

    def _via_setup(self):
        v, d = self.version, self.vias
        yn = lambda x: "yes" if x else "no"
        fb = lambda key, pair: f"({key} (front {yn(pair[0])}) (back {yn(pair[1])}))"
        if v >= K10:
            return ["(allow_soldermask_bridges_in_footprints no)", fb("tenting", d["tenting"]),
                    fb("covering", d["covering"]), fb("plugging", d["plugging"]),
                    f"(capping {yn(d['capping'])})", f"(filling {yn(d['filling'])})"]
        if v >= K9:
            sides = " ".join(s for s, on in zip(("front", "back"), d["tenting"]) if on) or "none"
            return ["(allow_soldermask_bridges_in_footprints no)", f"(tenting {sides})"]
        return []

    def text(self):
        v = self.version
        ids = NEW_IDS if v >= K9 else OLD_IDS
        layers = [f"({ids[l]} {q(l)} signal)" for l in copper_names(self.copper)]
        tech = UI_ORDER if v >= K9 else [n for _, n, _ in NON_COPPER]
        layers += [f"({ids[n]} {q(n)} user{' ' + q(USER_NAMES[n]) if n in USER_NAMES else ''})" for n in tech]
        if v < K8:
            head = [f"(kicad_pcb (version {v}) (generator pcbnew)", f"(general (thickness {f(self.thickness)}))"]
        else:
            head = [f'(kicad_pcb (version {v}) (generator "pcbnew") (generator_version "{GENERATOR[v]}")',
                    f"(general (thickness {f(self.thickness)}) (legacy_teardrops no))"]
        setup = ([self.stackup] if self.stackup else []) + ["(pad_to_mask_clearance 0)"] + self._via_setup() + self.setup
        nets = [] if v >= K10 else [f"(net {i} {q(n)})" for i, n in enumerate(self.nets)]
        body = head + ['(paper "A4")', "(layers " + " ".join(layers) + ")", "(setup " + " ".join(setup) + ")",
                       *nets, *self.items, *(["(embedded_fonts no)"] if v >= K9 else [])]
        if v < K8:
            return "\n  ".join(body) + "\n)\n"
        return prettify(" ".join(body) + ")")


def layer_list(b, layers, quoted_wildcards=True):
    """(layers ...) of a pad: wildcards first, then single layers in the order of their layer ids."""
    ids = NEW_IDS if b.version >= K9 else OLD_IDS
    wild = [w for w in WILDCARDS if w in layers]
    single = sorted((l for l in layers if l not in wild), key=lambda l: ids[l])
    words = [q(w) if quoted_wildcards else w for w in wild] + [q(l) for l in single]
    return "(layers " + " ".join(words) + ")"


# ---- drawings and text ----------------------------------------------------------------------------
def _shape(b, kind, geo, layer, width, filled=None, net=None, radius=None, layers=None, mask_margin=None,
           prefix="gr"):
    """A gr_*/fp_* drawing.  filled: None (lines, arcs), True/False, or a KiCad 10 hatch name.
    layers: a layer set such as ("F.Cu", "F.Mask") for copper left bare by the mask (KiCad 9+)."""
    v = b.version
    head = f"({prefix}_{kind} {geo}" + (f" (radius {f(radius)})" if radius else "")
    lay = layer_list(b, layers) if layers else f"(layer {q(layer)})"
    if filled is None:
        fil = ""
    elif isinstance(filled, str):
        fil = f"(fill {filled})"
    elif v >= K9:
        fil = f"(fill {'yes' if filled else 'no'})"
    else:
        fil = f"(fill {'solid' if filled else 'none'})"
    if v < K7:
        parts = [head, lay, f"(width {f(width)})", fil]
    else:
        parts = [head, f"(stroke (width {f(width)}) (type solid))", fil, lay]
        parts += [f"(solder_mask_margin {f(mask_margin)})"] if mask_margin is not None else []
        parts += [b.net(net)] if net else []
    return " ".join(p for p in parts + [b.ts()] if p) + ")"


def gr_line(b, a, c, layer, width=0.1, **kw):
    return _shape(b, "line", f"(start {xy(a)}) (end {xy(c)})", layer, width, **kw)


def gr_rect(b, a, c, layer, width=0.1, filled=False, **kw):
    return _shape(b, "rect", f"(start {xy(a)}) (end {xy(c)})", layer, width, filled, **kw)


def gr_circle(b, c, r, layer, width=0.1, filled=False, **kw):
    return _shape(b, "circle", f"(center {xy(c)}) (end {xy((c[0] + r, c[1]))})", layer, width, filled, **kw)


def gr_arc(b, start, mid, end, layer, width=0.1, **kw):
    return _shape(b, "arc", f"(start {xy(start)}) (mid {xy(mid)}) (end {xy(end)})", layer, width, **kw)


def gr_poly(b, points, layer, width=0.1, filled=True, **kw):
    return _shape(b, "poly", "(pts " + " ".join(f"(xy {xy(p)})" for p in points) + ")", layer, width, filled, **kw)


def outline(b, x0, y0, x1, y1, radius=None):
    return gr_rect(b, (x0, y0), (x1, y1), "Edge.Cuts", 0.1, radius=radius)


def effects(b, size=1.0, thickness=0.15, bold=False, italic=False, justify=()):
    style = (" (bold yes)" * bold + " (italic yes)" * italic) if b.version >= K8 else (" bold" * bold + " italic" * italic)
    just = f" (justify {' '.join(justify)})" if justify else ""
    return f"(effects (font (size {f(size)} {f(size)}) (thickness {f(thickness)}){style}){just})"


def gr_text(b, s, at, layer, angle=0, knockout=False, **fx):
    if b.version < K8:
        a = f" {f(angle)}" if angle else ""
        return f"(gr_text {q(s)} (at {xy(at)}{a}) (layer {q(layer)}) {b.ts()} {effects(b, **fx)})"
    ko = " knockout" if knockout else ""
    return f"(gr_text {q(s)} (at {xy(at)} {f(angle)}) (layer {q(layer)}{ko}) {b.ts()} {effects(b, **fx)})"


# ---- tracks, vias, zones --------------------------------------------------------------------------
def _bare(b, layer, mask_margin):
    """The layer of a track: (layers "F.Cu" "F.Mask") when the mask leaves it bare (KiCad 9 and later)."""
    if mask_margin is None:
        return f"(layer {q(layer)})"
    margin = f" (solder_mask_margin {f(mask_margin)})" if mask_margin else ""
    return layer_list(b, (layer, layer[0] + ".Mask")) + margin


def segment(b, a, c, width, layer, net, bare_margin=None):
    """bare_margin: None, or the mask opening's margin for a track left bare by the mask (0 for none)."""
    return (f"(segment (start {xy(a)}) (end {xy(c)}) (width {f(width)}) {_bare(b, layer, bare_margin)} "
            f"{b.net(net)} {b.ts()})")


def arc(b, start, mid, end, width, layer, net, bare_margin=None):
    return (f"(arc (start {xy(start)}) (mid {xy(mid)}) (end {xy(end)}) (width {f(width)}) "
            f"{_bare(b, layer, bare_margin)} {b.net(net)} {b.ts()})")


def yn(on):
    return "yes" if on else "no"


def front_back(key, pair):
    """KiCad 10's (key (front yes|no|none) (back ...)); None leaves a side to the board's setting."""
    word = lambda v: "none" if v is None else yn(v)
    return f"({key} (front {word(pair[0])}) (back {word(pair[1])}))"


def drills(o):
    """KiCad 10's extra drills of a pad or via: backdrill=(size, start, end) from the bottom,
    tertiary=(size, start, end) from the top, and front_pm/back_pm=(mode, size, depth, angle) for a
    counterbore or countersink."""
    s = ""
    for key, token in (("backdrill", "backdrill"), ("tertiary", "tertiary_drill")):
        if key in o:
            size, start, end = o[key]
            s += f" ({token} (size {f(size)}) (layers {q(start)} {q(end)}))"
    for key, token in (("front_pm", "front_post_machining"), ("back_pm", "back_post_machining")):
        if key in o:
            mode, size, depth, angle = o[key]
            s += f" ({token} {mode} (size {f(size)})" + (f" (depth {f(depth)})" if depth else "")
            s += (f" (angle {f(angle)})" if angle else "") + ")"
    return s


def via(b, at, size, drill, net, layers=("F.Cu", "B.Cu"), kind="", remove_unused=False, keep_end=False,
        free=False, **o):
    """A via.  kind: "", blind, buried (blind before KiCad 10) or micro.  KiCad 10 also takes
    start_end_only, tenting/covering/plugging=(front, back) with True, False or None (the board's
    setting), capping, filling, the drills of drills() and padstack=(mode, {layer: size}), mode
    front_inner_back (layers "Inner" and "B.Cu") or custom (every copper layer but F.Cu).  KiCad 9
    takes tenting, written as the list of tented sides."""
    v = b.version
    kind = "blind" if kind == "buried" and v < K10 else kind
    s = f"(via{' ' + kind if kind else ''} (at {xy(at)}) (size {f(size)}) (drill {f(drill)})"
    s += drills(o) if v >= K10 else ""
    s += f" (layers {q(layers[0])} {q(layers[1])})"
    if o.get("start_end_only"):
        s += " (start_end_only yes)"
    elif remove_unused:
        s += " " + b.flag("remove_unused_layers") + (" " + b.flag("keep_end_layers", keep_end) if keep_end or v >= K8 else "")
    s += " " + b.flag("free") if free else ""
    if v >= K8 and (remove_unused or o.get("start_end_only")):
        s += " (zone_layer_connections)"
    tent = o.get("tenting")
    if tent and v >= K10:
        s += " " + front_back("tenting", tent)
    elif tent and v >= K9:
        s += " (tenting " + (" ".join(side for side, on in zip(("front", "back"), tent) if on) or "none") + ")"
    if v >= K10:
        s += f" (capping {yn(o['capping'])})" if "capping" in o else ""
        s += "".join(" " + front_back(k, o[k]) for k in ("covering", "plugging") if k in o)
        s += f" (filling {yn(o['filling'])})" if "filling" in o else ""
        if "padstack" in o:
            mode, sizes = o["padstack"]
            s += f" (padstack (mode {mode})" + "".join(f" (layer {q(l)} (size {f(d)}))" for l, d in sizes.items()) + ")"
    return s + f" {b.net(net)} {b.ts()})"


def zone(b, net, layer, points, name=None, priority=None, clearance=0.3, min_thickness=0.25, connect=None,
         thermal_gap=0.5, thermal_width=0.5, islands=None, fills=()):
    """A copper zone on one layer.  connect and islands=(mode, min area) as in kicad7.zone; fills: its
    filled polygons [(points, is_island)], since nothing fills a hand-written board."""
    v = b.version
    s = f"(zone {b.zone_net(net)}(layer {q(layer)}) {b.ts()}" + (f" (name {q(name)})" if name else "")
    s += " (hatch edge 0.5)" + (f" (priority {priority})" if priority else "")
    s += f" (connect_pads{' ' + connect if connect else ''} (clearance {f(clearance)}))"
    s += f" (min_thickness {f(min_thickness)})" + (" (filled_areas_thickness no)" if v < K10 else "")
    s += " (fill" + " yes" * bool(fills) + f" (thermal_gap {f(thermal_gap)}) (thermal_bridge_width {f(thermal_width)})"
    mode, area = islands or (0, 10)
    if v >= K10 or mode:
        s += f" (island_removal_mode {mode})" + (f" (island_area_min {f(area)})" if mode == 2 or v < K10 else "")
    s += f") (polygon {pts(points)})"
    island = "(island yes)" if v >= K10 else "(island)"
    for poly, is_island in fills:
        s += f" (filled_polygon (layer {q(layer)}){' ' + island if is_island else ''} {pts(poly)})"
    return s + ")"
