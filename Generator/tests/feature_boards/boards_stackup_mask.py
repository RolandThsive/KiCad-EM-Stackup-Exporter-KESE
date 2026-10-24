"""Boards 14 to 18: stack-ups, plated edges and castellated pads, solder mask and silkscreen, and
gold edge fingers."""
from common import OUTER, PLAIN, at, new_board
from footprints7 import footprint, pad, shape, text
from kicad7 import (copper_names, core, gr_circle, gr_line, gr_poly, gr_rect, gr_text, prepreg, segment,
                    stackup, via, zone)

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


BOARDS = [stackup_full, stackup_none, edge_plating_castellation, mask_silk, finishes]
