"""Building blocks for boards in KiCad 7's file format (version 20221018).  Every helper returns the
s-expression of one item; Board collects them with the nets and the layer table.  Coordinates are
KiCad's: millimetres, y down."""
import uuid

VERSION = 20221018
NAMESPACE = uuid.UUID("6b1e0c7e-5e7a-4c55-9f37-0d1c2a6f4e10")     # fixed, so tstamps never change
NON_COPPER = [(32, "B.Adhes", "B.Adhesive"), (33, "F.Adhes", "F.Adhesive"), (34, "B.Paste", None),
              (35, "F.Paste", None), (36, "B.SilkS", "B.Silkscreen"), (37, "F.SilkS", "F.Silkscreen"),
              (38, "B.Mask", None), (39, "F.Mask", None), (40, "Dwgs.User", "User.Drawings"),
              (41, "Cmts.User", "User.Comments"), (42, "Eco1.User", "User.Eco1"),
              (43, "Eco2.User", "User.Eco2"), (44, "Edge.Cuts", None), (45, "Margin", None),
              (46, "B.CrtYd", "B.Courtyard"), (47, "F.CrtYd", "F.Courtyard"), (48, "B.Fab", None),
              (49, "F.Fab", None)]


def f(v):
    """A number as KiCad writes it: at most 6 decimals, no trailing zeros."""
    s = f"{v:.6f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def xy(p):
    return f"{f(p[0])} {f(p[1])}"


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def pts(points):
    return "(pts " + " ".join(f"(xy {xy(p)})" for p in points) + ")"


def copper_names(n):
    return ["F.Cu"] + [f"In{i}.Cu" for i in range(1, n - 1)] + ["B.Cu"]


class Board:
    """One board: its copper layer count, nets, setup and items, written out by text()."""

    def __init__(self, name, copper=2, thickness=1.6):
        self.name, self.copper, self.thickness = name, copper, thickness
        self.nets, self.items, self.setup, self.stackup = [""], [], [], None
        self.unfilled = set()            # names of zones KiCad must leave unfilled
        self._count = 0

    def n(self, name):
        """The net number of a net, declared on first use."""
        if name not in self.nets:
            self.nets.append(name)
        return self.nets.index(name)

    def ts(self):
        self._count += 1
        return f"(tstamp {uuid.uuid5(NAMESPACE, f'{self.name}/{self._count}')})"

    def add(self, *items):
        self.items += items

    def text(self):
        ids = {"F.Cu": 0, "B.Cu": 31, **{f"In{i}.Cu": i for i in range(1, 31)}}
        layers = [f"({ids[l]} {q(l)} signal)" for l in copper_names(self.copper)]
        layers += [f"({i} {q(n)} user{' ' + q(u) if u else ''})" for i, n, u in NON_COPPER]
        setup = ([self.stackup] if self.stackup else []) + self.setup
        return "\n".join([
            f"(kicad_pcb (version {VERSION}) (generator pcbnew)",
            f"  (general (thickness {f(self.thickness)}))",
            '  (paper "A4")',
            "  (layers\n    " + "\n    ".join(layers) + ")",
            "  (setup " + " ".join(setup or ["(pad_to_mask_clearance 0)"]) + ")",
            *[f"  (net {i} {q(n)})" for i, n in enumerate(self.nets)],
            *["  " + it for it in self.items],
            ")", ""])


def stackup(b, dielectrics, copper_t=0.035, mask_t=0.01, mask_color=None, silk_color=None,
            finish="None", mask=None, constraints=False, extra=()):
    """(stackup ...) for b's copper layers.  dielectrics[i] lies between copper i and i + 1: a dict
    (kind, t, material, er, tand) or a list of them for sublayers.  copper_t: one value or a list.
    mask: a dict (material, er, tand) for the solder mask.  extra: more fields at the end, such as
    "(castellated_pads yes)"."""
    cu = copper_names(b.copper)
    cu_t = copper_t if isinstance(copper_t, (list, tuple)) else [copper_t] * len(cu)
    color = lambda c: f" (color {q(c)})" if c else ""
    mask_s = f"(thickness {f(mask_t)})" if not mask else dielectric(dict(mask, t=mask_t))
    out = [f'(layer "F.SilkS" (type "Top Silk Screen"){color(silk_color)})',
           '(layer "F.Paste" (type "Top Solder Paste"))',
           f'(layer "F.Mask" (type "Top Solder Mask"){color(mask_color)} {mask_s})']
    for i, name in enumerate(cu):
        out.append(f'(layer {q(name)} (type "copper") (thickness {f(cu_t[i])}))')
        if i < len(cu) - 1:
            subs = dielectrics[i] if isinstance(dielectrics[i], (list, tuple)) else [dielectrics[i]]
            first, rest = subs[0], subs[1:]
            body = " ".join(dielectric(d) for d in [first])
            body += "".join(" addsublayer " + dielectric(d) for d in rest)
            out.append(f'(layer "dielectric {i + 1}" (type {q(first.get("kind", "core"))}) {body})')
    out += [f'(layer "B.Mask" (type "Bottom Solder Mask"){color(mask_color)} {mask_s})',
            '(layer "B.Paste" (type "Bottom Solder Paste"))',
            f'(layer "B.SilkS" (type "Bottom Silk Screen"){color(silk_color)})',
            f"(copper_finish {q(finish)})", f"(dielectric_constraints {'yes' if constraints else 'no'})", *extra]
    b.stackup = "(stackup\n      " + "\n      ".join(out) + ")"


def dielectric(d):
    s = f"(thickness {f(d['t'])})"
    if "material" in d:
        s += f" (material {q(d['material'])})"
    if "er" in d:
        s += f" (epsilon_r {f(d['er'])})"
    if "tand" in d:
        s += f" (loss_tangent {f(d['tand'])})"
    return s


def core(t, er=4.5, tand=0.02, material="FR4"):
    return {"kind": "core", "t": t, "material": material, "er": er, "tand": tand}


def prepreg(t, er=4.5, tand=0.02, material="FR4"):
    return {"kind": "prepreg", "t": t, "material": material, "er": er, "tand": tand}


# ---- drawings -------------------------------------------------------------------------------------
def stroke(width):
    return f"(stroke (width {f(width)}) (type solid))"


def fill(on):
    return f"(fill {'solid' if on else 'none'})"


def gr_line(b, a, c, layer, width=0.1):
    return f"(gr_line (start {xy(a)}) (end {xy(c)}) {stroke(width)} (layer {q(layer)}) {b.ts()})"


def gr_rect(b, a, c, layer, width=0.1, filled=False):
    return f"(gr_rect (start {xy(a)}) (end {xy(c)}) {stroke(width)} {fill(filled)} (layer {q(layer)}) {b.ts()})"


def gr_circle(b, c, r, layer, width=0.1, filled=False):
    return (f"(gr_circle (center {xy(c)}) (end {xy((c[0] + r, c[1]))}) {stroke(width)} {fill(filled)} "
            f"(layer {q(layer)}) {b.ts()})")


def gr_arc(b, start, mid, end, layer, width=0.1):
    return f"(gr_arc (start {xy(start)}) (mid {xy(mid)}) (end {xy(end)}) {stroke(width)} (layer {q(layer)}) {b.ts()})"


def gr_poly(b, points, layer, width=0.1, filled=True):
    return f"(gr_poly {pts(points)} {stroke(width)} {fill(filled)} (layer {q(layer)}) {b.ts()})"


def gr_curve(b, p0, c0, c1, p1, layer, width=0.1):
    return f"(gr_curve {pts([p0, c0, c1, p1])} {stroke(width)} (layer {q(layer)}) {b.ts()})"


def outline(b, x0, y0, x1, y1):
    """A rectangular Edge.Cuts outline."""
    return gr_rect(b, (x0, y0), (x1, y1), "Edge.Cuts", 0.1)


def effects(size=1.0, thickness=0.15, bold=False, italic=False, face=None, justify=()):
    font = (f"(face {q(face)}) " if face else "") + f"(size {f(size)} {f(size)}) (thickness {f(thickness)})"
    font += " bold" * bold + " italic" * italic
    just = f" (justify {' '.join(justify)})" if justify else ""
    return f"(effects (font {font}){just})"


def gr_text(b, s, at, layer, angle=0, knockout=False, **fx):
    a = f" {f(angle)}" if angle else ""
    return (f"(gr_text {q(s)} (at {xy(at)}{a}) (layer {q(layer)}{' knockout' if knockout else ''}) {b.ts()} "
            f"{effects(**fx)})")


def gr_text_box(b, s, a, c, layer, width=0.1, **fx):
    return (f"(gr_text_box {q(s)} (start {xy(a)}) (end {xy(c)}) (layer {q(layer)}) {b.ts()} "
            f"{effects(**fx)} {stroke(width)})")


# ---- tracks, vias, zones --------------------------------------------------------------------------
def segment(b, a, c, width, layer, net):
    return f"(segment (start {xy(a)}) (end {xy(c)}) (width {f(width)}) (layer {q(layer)}) (net {b.n(net)}) {b.ts()})"


def arc(b, start, mid, end, width, layer, net):
    return (f"(arc (start {xy(start)}) (mid {xy(mid)}) (end {xy(end)}) (width {f(width)}) (layer {q(layer)}) "
            f"(net {b.n(net)}) {b.ts()})")


def via(b, at, size, drill, net, layers=("F.Cu", "B.Cu"), kind="", remove_unused=False, keep_end=False,
        free=False):
    opts = " (remove_unused_layers)" * remove_unused + " (keep_end_layers)" * keep_end + " (free)" * free
    return (f"(via{' ' + kind if kind else ''} (at {xy(at)}) (size {f(size)}) (drill {f(drill)}) "
            f"(layers {q(layers[0])} {q(layers[1])}){opts} (net {b.n(net)}) {b.ts()})")


def zone(b, net, layers, points, name=None, priority=None, clearance=0.3, min_thickness=0.25,
         connect=None, thermal_gap=0.5, thermal_width=0.5, hatch=None, islands=None, keepout=None,
         unfilled=False, holes=()):
    """A copper zone (or a rule area with keepout=dict).  connect: None (thermal reliefs), "yes",
    "no" or "thru_hole_only".  hatch: dict(thickness, gap, orientation) for a hatched fill.  islands:
    (mode, min area).  holes: point lists cut out of the outline.  KiCad fills the zone when the
    board is saved, unless unfilled (then name is required)."""
    if unfilled:
        b.unfilled.add(name)
    lay = f"(layer {q(layers[0])})" if len(layers) == 1 else "(layers " + " ".join(q(l) for l in layers) + ")"
    netno = b.n(net) if net else 0
    s = f"(zone (net {netno}) (net_name {q(net or '')}) {lay} {b.ts()}"
    s += f" (name {q(name)})" if name else ""
    s += " (hatch edge 0.5)"
    s += f" (priority {priority})" if priority is not None else ""
    s += f" (connect_pads{' ' + connect if connect else ''} (clearance {f(clearance)}))"
    s += f" (min_thickness {f(min_thickness)}) (filled_areas_thickness no)"
    if keepout:
        s += " (keepout " + " ".join(f"({k} {v})" for k, v in keepout.items()) + ")"
    s += " (fill" + (" yes" if not keepout else "")
    s += " (mode hatch)" if hatch else ""
    s += f" (thermal_gap {f(thermal_gap)}) (thermal_bridge_width {f(thermal_width)})"
    if islands:
        s += f" (island_removal_mode {islands[0]}) (island_area_min {f(islands[1])})"
    if hatch:
        s += (f" (hatch_thickness {f(hatch['thickness'])}) (hatch_gap {f(hatch['gap'])}) "
              f"(hatch_orientation {f(hatch.get('orientation', 0))}) (hatch_border_algorithm hatch_thickness) "
              f"(hatch_min_hole_area 0.3)")
    return s + ") " + " ".join(f"(polygon {pts(p)})" for p in [points, *holes]) + ")"
