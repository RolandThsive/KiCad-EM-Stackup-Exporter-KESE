"""A small writer of KiCad 7 board files (format 20221018), for the examples' make_board.py scripts.

Coordinates are KiCad's: millimetres, y pointing down.  Every board opens in KiCad 7 and later,
KiCad 10 included.  Only what the examples need is here: copper tracks and arcs, vias, a board
outline, filled copper polygons and a stack-up."""
import math
import uuid

VERSION = 20221018
_NS = uuid.UUID("2f6c3c4e-8f1a-4d0e-9a51-6c0b7e0d5a11")      # fixed, so the files never change


def num(v):
    """A number as KiCad writes it: at most 6 decimals, no trailing zeros."""
    s = f"{v:.6f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def xy(p):
    return f"{num(p[0])} {num(p[1])}"


def copper_names(n):
    return ["F.Cu"] + [f"In{i}.Cu" for i in range(1, n - 1)] + ["B.Cu"]


class Board:
    """One board: copper layers, a stack-up, nets and items; text() writes the file."""

    def __init__(self, name, copper=2, thickness=1.6, copper_t=0.035, er=4.4, tand=0.02, cores=None):
        self.name, self.copper, self.thickness, self.copper_t = name, copper, thickness, copper_t
        self.er, self.tand = er, tand
        # dielectric thicknesses between copper layers; by default equal shares of what the copper leaves
        n_d = copper - 1
        self.cores = cores or [round((thickness - copper * copper_t) / n_d, 6)] * n_d
        self.nets, self.items, self._count = [""], [], 0

    def net(self, name):
        if name not in self.nets:
            self.nets.append(name)
        return self.nets.index(name)

    def _ts(self):
        self._count += 1
        return f"(tstamp {uuid.uuid5(_NS, f'{self.name}/{self._count}')})"

    def segment(self, a, c, width, layer, net):
        self.items.append(f"(segment (start {xy(a)}) (end {xy(c)}) (width {num(width)}) (layer \"{layer}\") "
                          f"(net {self.net(net)}) {self._ts()})")

    def arc(self, start, mid, end, width, layer, net):
        self.items.append(f"(arc (start {xy(start)}) (mid {xy(mid)}) (end {xy(end)}) (width {num(width)}) "
                          f"(layer \"{layer}\") (net {self.net(net)}) {self._ts()})")

    def arc_centre(self, centre, radius, a0_deg, a1_deg, width, layer, net):
        """A track arc about centre from angle a0 to a1 (degrees, counter-clockwise on screen is negative
        in KiCad's y-down frame; here angles are taken in KiCad's own frame)."""
        def p(a):
            return (centre[0] + radius * math.cos(math.radians(a)), centre[1] + radius * math.sin(math.radians(a)))
        self.arc(p(a0_deg), p((a0_deg + a1_deg) / 2), p(a1_deg), width, layer, net)

    def via(self, at, size, drill, net, layers=("F.Cu", "B.Cu")):
        self.items.append(f"(via (at {xy(at)}) (size {num(size)}) (drill {num(drill)}) "
                          f"(layers \"{layers[0]}\" \"{layers[1]}\") (net {self.net(net)}) {self._ts()})")

    def poly(self, points, layer):
        """A filled graphic polygon on a layer: on a copper layer it is copper with no net (a ground plane)."""
        pts = " ".join(f"(xy {xy(p)})" for p in points)
        self.items.append(f"(gr_poly (pts {pts}) (stroke (width 0) (type solid)) (fill solid) (layer \"{layer}\") "
                          f"{self._ts()})")

    def outline_rect(self, x0, y0, x1, y1, width=0.1):
        self.items.append(f"(gr_rect (start {xy((x0, y0))}) (end {xy((x1, y1))}) (stroke (width {num(width)}) "
                          f"(type solid)) (fill none) (layer \"Edge.Cuts\") {self._ts()})")

    def outline_circle(self, centre, r, width=0.1):
        self.items.append(f"(gr_circle (center {xy(centre)}) (end {xy((centre[0] + r, centre[1]))}) (stroke (width "
                          f"{num(width)}) (type solid)) (fill none) (layer \"Edge.Cuts\") {self._ts()})")

    def _stackup(self):
        names = copper_names(self.copper)
        rows = ['(layer "F.SilkS" (type "Top Silk Screen"))', '(layer "F.Paste" (type "Top Solder Paste"))',
                '(layer "F.Mask" (type "Top Solder Mask") (thickness 0.01))']
        for i, cu in enumerate(names):
            rows.append(f'(layer "{cu}" (type "copper") (thickness {num(self.copper_t)}))')
            if i < len(self.cores):
                kind = "core" if i % 2 == 0 else "prepreg"
                rows.append(f'(layer "dielectric {i + 1}" (type "{kind}") (thickness {num(self.cores[i])}) '
                            f'(material "FR4") (epsilon_r {num(self.er)}) (loss_tangent {num(self.tand)}))')
        rows += ['(layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01))',
                 '(layer "B.Paste" (type "Bottom Solder Paste"))', '(layer "B.SilkS" (type "Bottom Silk Screen"))']
        return "(stackup " + " ".join(rows) + " (copper_finish \"None\") (dielectric_constraints no))"

    def text(self):
        ids = {"F.Cu": 0, "B.Cu": 31, **{f"In{i}.Cu": i for i in range(1, 31)}}
        layers = [f'({ids[l]} "{l}" signal)' for l in copper_names(self.copper)]
        layers += ['(32 "B.Adhes" user "B.Adhesive")', '(33 "F.Adhes" user "F.Adhesive")', '(34 "B.Paste" user)',
                   '(35 "F.Paste" user)', '(36 "B.SilkS" user "B.Silkscreen")', '(37 "F.SilkS" user "F.Silkscreen")',
                   '(38 "B.Mask" user)', '(39 "F.Mask" user)', '(44 "Edge.Cuts" user)', '(45 "Margin" user)',
                   '(46 "B.CrtYd" user "B.Courtyard")', '(47 "F.CrtYd" user "F.Courtyard")', '(48 "B.Fab" user)',
                   '(49 "F.Fab" user)']
        return "\n".join([
            f"(kicad_pcb (version {VERSION}) (generator pcbnew)",
            f"  (general (thickness {num(self.thickness)}))",
            '  (paper "A4")',
            "  (layers\n    " + "\n    ".join(layers) + ")",
            f"  (setup {self._stackup()} (pad_to_mask_clearance 0))",
            *[f'  (net {i} "{n}")' for i, n in enumerate(self.nets)],
            *["  " + it for it in self.items],
            ")", ""])

    def write(self, path):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(self.text())
