"""Boards 14 to 18: stack-ups, plated edges and castellated pads, a plated edge with a copper border,
solder mask and silkscreen, and gold edge fingers."""
import math

from common import OUTER, PLAIN, at, new_board
from footprints7 import footprint, pad, shape, text
from kicad7 import (arc, copper_names, core, gr_arc, gr_circle, gr_line, gr_poly, gr_rect, gr_text, prepreg,
                    segment, stackup, via, zone)

THT = ("*.Cu", "*.Mask")
SMD = ("F.Cu", "F.Paste", "F.Mask")
TTF = "DejaVu Sans"


def ref(s, y=-2.5, layer="F.SilkS"):
    return text("reference", s, (0, y), layer, size=1, thickness=0.15,
                justify=("mirror",) if layer.startswith("B") else ())


def tht(b, net, p, name, size=1.7, drill=1.0):
    return footprint(b, "Feature:OnePad", p, children=[
        ref(name, -1.8), pad("1", "thru_hole", "circle", (0, 0), (size, size), THT, drill=drill, net=net)])


def layer_tracks(b, x0, x1, y0, step):
    """One track per copper layer, each on its own net named after the layer."""
    for i, layer in enumerate(copper_names(b.copper)):
        b.add(segment(b, at(x0, y0 + step * i), at(x1, y0 + step * i), 0.3, layer, layer.split(".")[0].upper()))


def stackup_full():
    """A four-layer stack-up with everything KiCad 7 lets you set: coloured mask and silk, a mask
    material with its permittivity, copper of 35, 17.5, 17.5 and 70 um, a prepreg of two sublayers,
    a core and a prepreg of different materials, an ENIG finish and impedance-controlled dielectrics."""
    b = new_board("stackup_full", 4, (30, 20), stack=False)
    b.thickness = 1.58
    dielectrics = [[prepreg(0.1, 3.8, 0.015, "1080"), prepreg(0.12, 4.1, 0.017, "2116")],
                   core(1.0, 4.6, 0.018, "FR4 core"), prepreg(0.2, 4.2, 0.016, "2116")]
    stackup(b, dielectrics, [0.035, 0.0175, 0.0175, 0.07], mask_t=0.01, mask_color="Green",
            silk_color="White", finish="ENIG", mask=dict(material="Liquid Ink", er=3.3, tand=0.025),
            constraints=True)
    layer_tracks(b, 8, 25, 4, 4)
    b.add(tht(b, "GND", at(4, 10), "J1"), via(b, at(27, 10), 0.8, 0.4, "GND"),
          gr_text(b, "4 LAYERS 1.58", at(15, 18), "F.SilkS", size=1, thickness=0.15))
    return b


def stackup_none():
    """Four copper layers, no stack-up in the file (as older KiCad boards have), and a board
    thickness of 1.2 mm in the general section."""
    b = new_board("stackup_none", 4, (30, 20), stack=False)
    b.thickness = 1.2
    layer_tracks(b, 8, 25, 4, 4)
    b.add(tht(b, "GND", at(4, 10), "J1"), via(b, at(27, 10), 0.8, 0.4, "GND"))
    return b


def edge_plating_castellation():
    """Castellated pads (pad property castellated) on the right edge, with their holes on the edge,
    a plated board edge (edge_plating yes, castellated_pads yes) with GND tracks running along the
    left edge, a GND zone, and an immersion silver finish."""
    b = new_board("edge_plating_castellation", 2, (30, 20), stack=False)
    stackup(b, PLAIN[2], OUTER, finish="Immersion silver", extra=("(castellated_pads yes)", "(edge_plating yes)"))
    nets = ["C1", "C2", "C3", "C4", "GND"]
    pads = [pad(str(i + 1), "thru_hole", "oval", (0, y), (2.4, 1.6), THT, drill=0.8, net=n, prop="pad_prop_castellated")
            for i, (y, n) in enumerate(zip((-6, -3, 0, 3, 6), nets))]
    b.add(footprint(b, "Feature:Castellated", at(30, 10), children=[ref("J1", -8.5)] + pads))
    b.add(*[segment(b, at(30, 10 + y), at(25, 10 + y), 0.3, "F.Cu", n) for y, n in zip((-6, -3, 0, 3), nets)])
    b.add(segment(b, at(0.25, 0.5), at(0.25, 19.5), 0.5, "F.Cu", "GND"),
          segment(b, at(0.25, 0.5), at(0.25, 19.5), 0.5, "B.Cu", "GND"),
          tht(b, "GND", at(4, 10), "J2"),
          zone(b, "GND", ["F.Cu"], [at(0, 0), at(22, 0), at(22, 20), at(0, 20)]),
          zone(b, "GND", ["B.Cu"], [at(0, 0), at(22, 0), at(22, 20), at(0, 20)]))
    return b


def rounded_rect(x0, y0, x1, y1, r):
    """The sides of a rectangle with corners rounded to radius r, in turn from the top: ("line", a, c)
    and ("arc", start, mid, end), points given from the board's top-left corner."""
    k = r * (1 - math.sqrt(0.5))
    return [("line", (x0 + r, y0), (x1 - r, y0)), ("arc", (x1 - r, y0), (x1 - k, y0 + k), (x1, y0 + r)),
            ("line", (x1, y0 + r), (x1, y1 - r)), ("arc", (x1, y1 - r), (x1 - k, y1 - k), (x1 - r, y1)),
            ("line", (x1 - r, y1), (x0 + r, y1)), ("arc", (x0 + r, y1), (x0 + k, y1 - k), (x0, y1 - r)),
            ("line", (x0, y1 - r), (x0, y0 + r)), ("arc", (x0, y0 + r), (x0 + k, y0 + k), (x0 + r, y0))]


def drawn(b, sides, layer, width):
    """The sides as graphic lines and arcs on a layer."""
    return [gr_line(b, at(*s[1]), at(*s[2]), layer, width) if s[0] == "line" else
            gr_arc(b, at(*s[1]), at(*s[2]), at(*s[3]), layer, width) for s in sides]


def tracked(b, sides, layer, width, net):
    """The sides as tracks and arc tracks of a net."""
    return [segment(b, at(*s[1]), at(*s[2]), width, layer, net) if s[0] == "line" else
            arc(b, at(*s[1]), at(*s[2]), at(*s[3]), width, layer, net) for s in sides]


def along(sides, step):
    """Points about step apart along the straight sides, both ends included."""
    out = []
    for s in sides:
        if s[0] == "line":
            (ax, ay), (cx, cy) = s[1], s[2]
            n = max(1, round(math.dist(s[1], s[2]) / step))
            out += [(ax + (cx - ax) * i / n, ay + (cy - ay) * i / n) for i in range(n + 1)]
    return out


def edge_plating_border():
    """A plated board edge (edge_plating yes) as RF boards have it: a GND border 1.2 mm wide on every
    copper layer along the rounded outline and 1.0 mm wide around a rounded cut-out, the solder mask
    open over it on both sides, a fence of GND vias in the border, GND planes on F.Cu, In1.Cu and
    B.Cu, a +3V3 plane on In2.Cu, plated mounting holes, and a few parts.  Green mask, white silk,
    ENIG."""
    b = new_board("edge_plating_border", 4, None, stack=False)
    stackup(b, PLAIN[4], [OUTER, 0.0175, 0.0175, OUTER], mask_color="Green", silk_color="White", finish="ENIG",
            extra=("(edge_plating yes)",))
    W, H, R = 40.0, 28.0, 2.0                                   # outline, corner radius
    CUT, RC = (14.0, 18.0, 26.0, 23.0), 1.0                      # cut-out, corner radius
    RIM, RIM_CUT = 1.2, 1.0                                      # border widths
    outer = rounded_rect(0, 0, W, H, R)
    cut = rounded_rect(*CUT, RC)
    rim = rounded_rect(RIM / 2, RIM / 2, W - RIM / 2, H - RIM / 2, R - RIM / 2)
    x0, y0, x1, y1 = CUT
    h = RIM_CUT / 2
    rim_cut = rounded_rect(x0 - h, y0 - h, x1 + h, y1 + h, RC + h)
    b.add(*drawn(b, outer, "Edge.Cuts", 0.1), *drawn(b, cut, "Edge.Cuts", 0.1))
    for layer in copper_names(4):
        b.add(*tracked(b, rim, layer, RIM, "GND"), *tracked(b, rim_cut, layer, RIM_CUT, "GND"))
    for layer in ("F.Mask", "B.Mask"):                           # the mask open over the border
        b.add(*drawn(b, rim, layer, RIM + 0.1), *drawn(b, rim_cut, layer, RIM_CUT + 0.1))
    b.add(*[via(b, at(*p), 0.6, 0.3, "GND") for p in along(rim, 2.0) + along(rim_cut, 1.5)])
    full = [at(0, 0), at(W, 0), at(W, H), at(0, H)]
    b.add(zone(b, "GND", ["F.Cu"], full), zone(b, "GND", ["In1.Cu"], full),
          zone(b, "+3V3", ["In2.Cu"], full, clearance=0.5), zone(b, "GND", ["B.Cu"], full))
    for i, (x, y) in enumerate(((4, 4), (W - 4, 4), (4, H - 4), (W - 4, H - 4))):
        b.add(footprint(b, "Feature:MountingHole", at(x, y), children=[
            text("reference", f"H{i + 1}", (0, -2.6), "F.SilkS", hide=True, size=1, thickness=0.15),
            pad("1", "thru_hole", "circle", (0, 0), (3.6, 3.6), THT, drill=2.2, net="GND")]))
    qfn = [pad(str(i + 1), "smd", "rect", p, sz, SMD, net=n) for i, (p, sz, n) in enumerate(
        [((-1.9, -0.8 + 0.8 * k), (0.8, 0.4), ("GND", "RF_IN", "GND")[k]) for k in range(3)]
        + [((1.9, -0.8 + 0.8 * k), (0.8, 0.4), ("GND", "RF_OUT", "GND")[k]) for k in range(3)]
        + [((-0.8 + 0.8 * k, -1.9), (0.4, 0.8), ("+3V3", "+3V3", "GND")[k]) for k in range(3)]
        + [((-0.8 + 0.8 * k, 1.9), (0.4, 0.8), "GND") for k in range(3)])]
    b.add(footprint(b, "Feature:QFN12", at(20, 9), children=[
        ref("U1", -3.4), *qfn, pad("13", "smd", "rect", (0, 0), (2.0, 2.0), SMD, net="GND"),
        shape("rect", "F.SilkS", 0.15, a=(-2.6, -2.6), c=(2.6, 2.6))]))
    for name, x, net in (("J1", 6.5, "RF_IN"), ("J2", 33.5, "RF_OUT")):
        b.add(footprint(b, "Feature:RFLaunch", at(x, 9), children=[
            ref(name, -2.6), pad("1", "smd", "rect", (0, 0), (1.5, 1.0), SMD, net=net),
            pad("2", "smd", "rect", (0, -1.6), (1.5, 1.2), SMD, net="GND"),
            pad("3", "smd", "rect", (0, 1.6), (1.5, 1.2), SMD, net="GND")]))
    b.add(footprint(b, "Feature:C0603", at(20, 4), children=[
        ref("C1", -1.6), pad("1", "smd", "rect", (-0.8, 0), (0.9, 0.9), SMD, net="+3V3"),
        pad("2", "smd", "rect", (0.8, 0), (0.9, 0.9), SMD, net="GND")]))
    b.add(segment(b, at(7.25, 9), at(17.7, 9), 0.5, "F.Cu", "RF_IN"),
          segment(b, at(22.3, 9), at(32.75, 9), 0.5, "F.Cu", "RF_OUT"),
          segment(b, at(19.2, 6.7), at(19.2, 4), 0.3, "F.Cu", "+3V3"),
          segment(b, at(19.2, 7.1), at(20, 7.1), 0.3, "F.Cu", "+3V3"),
          segment(b, at(19.2, 4), at(17, 4), 0.3, "F.Cu", "+3V3"),
          via(b, at(17, 4), 0.6, 0.3, "+3V3"),
          *[via(b, at(20 + dx, 9 + dy), 0.6, 0.3, "GND") for dx in (-0.5, 0.5) for dy in (-0.5, 0.5)])
    b.add(gr_text(b, "KESE", at(9, 15.2), "F.SilkS", size=2, thickness=0.3),
          gr_text(b, "PLATED EDGE", at(31, 15.2), "F.SilkS", size=1, thickness=0.15),
          gr_text(b, "EDGE PLATING", at(20, 25.6), "B.SilkS", size=1, thickness=0.15, justify=("mirror",)))
    return b


def mask_silk():
    """Solder mask openings from the board's pad-to-mask clearance, a footprint's margin, a pad's own
    margin and a negative one; plated pads; openings drawn on F.Mask and B.Mask (a rectangle over
    a track, a circle, a polygon, text); a tented via; silkscreen lines, shapes and text on both
    sides, TrueType silk text, and a silk outline drawn across pads.  Red mask, black silk, HASL."""
    b = new_board("mask_silk", 2, (40, 30), stack=False)
    stackup(b, PLAIN[2], OUTER, mask_color="Red", silk_color="Black", finish="HAL lead-free")
    b.setup.append("(pad_to_mask_clearance 0.05) (solder_mask_min_width 0.1)")
    smd = lambda n, x, net, **o: pad(n, "smd", "rect", (x, 0), (1.2, 1.2), SMD, net=net, **o)
    b.add(footprint(b, "Feature:MaskBoard", at(5, 5), children=[
        ref("U1"), smd("1", 0, "M1"), smd("2", 3, "M2"), smd("3", 6, "M3"),
        shape("rect", "F.SilkS", 0.15, a=(-1, -0.3), c=(7, 0.3))]))
    b.add(footprint(b, "Feature:MaskFootprint", at(5, 11), mask_margin=0.15, children=[
        ref("U2"), smd("1", 0, "M4"), smd("2", 3, "M5")]))
    b.add(footprint(b, "Feature:MaskPad", at(5, 17), children=[
        ref("U3"), smd("1", 0, "M6", mask_margin=0.2), smd("2", 3, "M7", mask_margin=-0.1)]))
    b.add(footprint(b, "Feature:MaskTHT", at(18, 5), children=[
        ref("J1"), pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="M8"),
        pad("2", "thru_hole", "rect", (3, 0), (1.7, 1.7), THT, drill=1.0, net="M8")]))
    b.add(segment(b, at(23, 5), at(33, 5), 0.5, "F.Cu", "EXPOSED"),
          gr_rect(b, at(26, 3.5), at(30, 6.5), "F.Mask", 0.1, filled=True),
          gr_circle(b, at(28, 12), 2, "B.Mask", 0.1, filled=True),
          gr_poly(b, [at(18, 10), at(22, 10), at(20, 13)], "F.Mask"),
          gr_text(b, "MASK TEXT", at(30, 16), "F.Mask", size=1.5, thickness=0.3),
          via(b, at(36, 5), 0.8, 0.4, "V_TENTED"))
    b.add(gr_text(b, "SILK", at(8, 23), "F.SilkS", size=1.5, thickness=0.25),
          gr_text(b, "BACK SILK", at(28, 23), "B.SilkS", size=1.5, thickness=0.25, justify=("mirror",)),
          gr_text(b, "TTF SILK", at(12, 27), "F.SilkS", size=1.5, thickness=0.15, face=TTF),
          gr_line(b, at(2, 20), at(38, 20), "F.SilkS", 0.15),
          gr_rect(b, at(20, 25), at(26, 28), "F.SilkS", 0.15),
          gr_circle(b, at(32, 27), 1.5, "B.SilkS", 0.15),
          gr_poly(b, [at(35, 24), at(38, 24), at(36.5, 26.5)], "F.SilkS"))
    return b


def finishes():
    """Gold edge fingers: edge-connector pads on both sides running to a bevelled card edge
    (edge_connector bevelled), with a hard gold finish."""
    b = new_board("finishes", 2, (30, 16), stack=False)
    stackup(b, PLAIN[2], OUTER, finish="Hard gold", extra=("(edge_connector bevelled)",))
    fingers = []
    for i in range(6):
        x = -6.25 + 2.5 * i
        fingers += [pad(f"A{i + 1}", "connect", "rect", (x, 0), (1.5, 5), ("F.Cu", "F.Mask"), net=f"G{i + 1}"),
                    pad(f"B{i + 1}", "connect", "rect", (x, 0), (1.5, 5), ("B.Cu", "B.Mask"), net=f"G{i + 1}")]
    b.add(footprint(b, "Feature:EdgeFingers", at(15, 13.4), children=[ref("J1", -4)] + fingers))
    b.add(*[segment(b, at(15 - 6.25 + 2.5 * i, 10.9), at(15 - 6.25 + 2.5 * i, 6), 0.4, side, f"G{i + 1}")
            for i in range(6) for side in ("F.Cu", "B.Cu")])
    b.add(*[via(b, at(15 - 6.25 + 2.5 * i, 6), 0.8, 0.4, f"G{i + 1}") for i in range(6)])
    return b


BOARDS = [stackup_full, stackup_none, edge_plating_castellation, edge_plating_border, mask_silk, finishes]
