"""Boards 7 to 10: pad shapes, copper drawings, copper text and tracks."""
from common import at, new_board
from footprints7 import footprint, pad, prim_circle, prim_line, prim_poly, prim_rect, shape, text
from kicad7 import (arc, gr_arc, gr_circle, gr_curve, gr_line, gr_poly, gr_rect, gr_text, gr_text_box, q,
                    segment, stroke, xy)

SMD = ("F.Cu", "F.Paste", "F.Mask")
SMD_B = ("B.Cu", "B.Paste", "B.Mask")
TTF = "DejaVu Sans"


def ref(s, y=-2.5, layer="F.SilkS"):
    return text("reference", s, (0, y), layer, size=1, thickness=0.15,
                justify=("mirror",) if layer.startswith("B") else ())


def chamfered(num, at_, net, ratio, corners, rratio=0.0, size=(2.4, 1.4), layers=SMD, angle=0):
    return pad(num, "smd", "roundrect", at_, size, layers, angle=angle, net=net, rratio=rratio,
               chamfer=(ratio, corners))


def pad_shapes():
    """Every pad shape: circle, rect, oval, rounded rect, trapezoid, chamfered, chamfered and
    rounded, custom pads on a circle and a rect anchor; rotated pads, a footprint at 45 degrees and
    one on the back; mask-only and paste-only aperture pads, an edge-connector pad and a pad with
    no net."""
    b = new_board("pad_shapes", 2, (44, 30))
    arrow = prim_poly([(0, -0.6), (1.4, -0.6), (1.4, -1.1), (2.0, 0), (1.4, 1.1), (1.4, 0.6), (0, 0.6)])
    arc_prim = "(gr_arc (start -1.2 0) (mid 0 -1.2) (end 1.2 0) (width 0.3))"
    curve = "(gr_curve (pts (xy -1.2 0.4) (xy -0.4 1.6) (xy 0.4 -0.2) (xy 1.2 0.9)) (width 0.2))"
    pads = [pad("1", "smd", "circle", (0, 0), (1.6, 1.6), SMD, net="P_CIRCLE"),
            pad("2", "smd", "rect", (4, 0), (2.0, 1.2), SMD, net="P_RECT"),
            pad("3", "smd", "oval", (8, 0), (2.4, 1.2), SMD, net="P_OVAL"),
            pad("4", "smd", "oval", (12, 0), (1.2, 2.4), SMD, net="P_OVAL_V"),
            pad("5", "smd", "roundrect", (16, 0), (2.4, 1.4), SMD, net="P_RRECT", rratio=0.25),
            pad("6", "smd", "roundrect", (20, 0), (2.4, 1.4), SMD, net="P_RRECT50", rratio=0.5),
            pad("7", "smd", "trapezoid", (24, 0), (2.0, 1.4), SMD, net="P_TRAP_X", delta=(0.6, 0)),
            pad("8", "smd", "trapezoid", (28, 0), (2.0, 1.4), SMD, net="P_TRAP_Y", delta=(0, 0.6)),
            chamfered("9", (32, 0), "P_CHAMF", 0.25, ("top_left", "bottom_right")),
            chamfered("10", (0, 5), "P_CHAMF_RR", 0.3, ("top_right",), rratio=0.2),
            chamfered("11", (4, 5), "P_OCTAGON", 0.29, ("top_left", "top_right", "bottom_left", "bottom_right"),
                      size=(2.0, 2.0)),
            pad("12", "smd", "custom", (8, 5), (1.0, 1.0), SMD, net="P_CUSTOM_C", anchor="circle",
                primitives=[arrow]),
            pad("13", "smd", "custom", (13, 5), (1.0, 1.0), SMD, net="P_CUSTOM_R", anchor="rect",
                primitives=[prim_circle((1.0, 0), 0.5), prim_line((-1.4, 0), (-0.5, 0.8), 0.4),
                            prim_rect((-0.3, -1.3), (0.3, -0.5))]),
            pad("14", "smd", "custom", (18, 5), (0.6, 0.6), SMD, net="P_CUSTOM_ARC", anchor="circle",
                primitives=[arc_prim, curve]),
            pad("15", "smd", "rect", (22, 5), (2.0, 1.2), SMD, angle=30, net="P_ROT30"),
            pad("16", "smd", "oval", (26, 5), (2.4, 1.2), SMD, angle=90, net="P_ROT90"),
            pad("17", "smd", "roundrect", (30, 5), (2.4, 1.4), SMD, angle=45, net="P_ROT45", rratio=0.25),
            pad("18", "smd", "trapezoid", (34, 5), (2.0, 1.4), SMD, angle=15, net="P_TRAP_ROT", delta=(0.6, 0)),
            pad("A1", "smd", "rect", (0, 10), (2.0, 1.2), ("F.Mask",)),
            pad("A2", "smd", "rect", (4, 10), (2.0, 1.2), ("F.Paste",)),
            pad("C1", "connect", "rect", (8, 10), (2.0, 1.2), ("F.Cu", "F.Mask"), net="P_CONNECT"),
            pad("N1", "smd", "rect", (12, 10), (2.0, 1.2), SMD),
            pad("19", "smd", "rect", (16, 10), (2.0, 1.2), SMD_B, net="P_BACK_IN_FRONT_FP")]
    b.add(footprint(b, "Feature:PadShapes", at(4, 5), children=[ref("U1")] + pads))
    b.add(footprint(b, "Feature:Pads45", at(8, 23), angle=45, children=[
        ref("U2"), pad("1", "smd", "rect", (-3, 0), (2.0, 1.2), SMD, net="P45_RECT"),
        pad("2", "smd", "roundrect", (0, 0), (2.4, 1.4), SMD, net="P45_RRECT", rratio=0.25),
        pad("3", "smd", "trapezoid", (3, 0), (2.0, 1.4), SMD, net="P45_TRAP", delta=(0.6, 0)),
        pad("4", "smd", "custom", (6.5, 0), (1.0, 1.0), SMD, net="P45_CUSTOM", anchor="rect",
            primitives=[prim_circle((0.9, 0), 0.5)])]))
    b.add(footprint(b, "Feature:PadsBack", at(30, 23), angle=30, side="B", children=[
        ref("U3", layer="B.SilkS"), pad("1", "smd", "rect", (-5, 0), (2.0, 1.2), SMD_B, net="PB_RECT"),
        pad("2", "smd", "trapezoid", (-1.5, 0), (2.0, 1.4), SMD_B, net="PB_TRAP", delta=(0.6, 0)),
        pad("3", "smd", "custom", (2, 0), (1.0, 1.0), SMD_B, net="PB_CUSTOM", anchor="circle",
            primitives=[arrow]),
        chamfered("4", (6, 0), "PB_CHAMF", 0.25, ("top_left",), layers=SMD_B)]))
    return b


def copper_graphics():
    """Lines, rectangles, circles (open and filled), an arc, polygons (filled, open, and one with an
    arc edge) and a Bezier curve drawn on F.Cu and B.Cu with no net, as KiCad 7 has them; the same
    shapes in a footprint at 30 degrees and in one on the back; a track that ends on a drawing."""
    b = new_board("copper_graphics", 2, (30, 24))
    F, B = "F.Cu", "B.Cu"
    poly_arc = (f"(gr_poly (pts (xy {xy(at(25, 8))}) (arc (start {xy(at(28, 8))}) (mid {xy(at(29.5, 9.5))}) "
                f"(end {xy(at(28, 11))})) (xy {xy(at(25, 11))})) {stroke(0.1)} (fill solid) (layer {q(F)}) {b.ts()})")
    b.add(gr_line(b, at(3, 3), at(10, 3), F, 0.3),
          gr_rect(b, at(12, 2), at(16, 5), F, 0.2),
          gr_rect(b, at(18, 2), at(22, 5), F, 0.1, filled=True),
          gr_circle(b, at(26, 3.5), 1.5, F, 0.25),
          gr_circle(b, at(4, 9.5), 1.5, F, 0.1, filled=True),
          gr_arc(b, at(8, 10), at(10, 8), at(12, 10), F, 0.3),
          gr_poly(b, [at(14, 8), at(18, 8), at(16, 11)], F),
          gr_poly(b, [at(19, 8), at(23, 8), at(23, 11), at(19, 11)], F, 0.2, filled=False),
          poly_arc,
          gr_curve(b, at(3, 15), at(5, 12.5), at(7, 17.5), at(9, 15), F, 0.3),
          gr_rect(b, at(12, 13), at(16, 16), B, 0.1, filled=True),
          gr_circle(b, at(20, 14.5), 1.2, B, 0.3))
    b.add(segment(b, at(10, 3), at(10, 6), 0.3, F, "TOUCHES_LINE"))
    b.add(footprint(b, "Feature:CopperShapes", at(7, 20), angle=30, children=[
        ref("G1", -3),
        shape("line", F, 0.25, a=(-3, 0), c=(3, 0)),
        shape("rect", F, 0.1, filled=True, a=(-2, 1), c=(2, 2.2)),
        shape("circle", B, 0.2, c=(4, 1), r=0.8),
        shape("arc", F, 0.2, start=(-4, 1.2), mid=(-3, 2.2), end=(-2.4, 1.2)),
        shape("poly", F, 0.1, filled=True, points=[(4.5, -1.5), (6, -1.5), (5.2, -0.4)])]))
    b.add(footprint(b, "Feature:CopperShapesBack", at(24, 20), side="B", children=[
        ref("G2", -2.2, "B.SilkS"),
        shape("rect", B, 0.1, filled=True, a=(-2, -1), c=(0, 1)),
        shape("poly", B, 0.1, filled=True, points=[(1, -1), (3, 0), (1, 1)])]))
    return b


def copper_text():
    """Text on copper: the stroke font plain, bold, italic, rotated, on two lines and justified;
    TrueType text (DejaVu Sans) on F.Cu and mirrored on B.Cu, bold and italic; knockout text; a
    text box; footprint text with a hidden value and a ${REFERENCE} variable."""
    b = new_board("copper_text", 2, (44, 40))
    F, B = "F.Cu", "B.Cu"
    b.add(gr_text(b, "STROKE", at(10, 3), F, size=1.5, thickness=0.3),
          gr_text(b, "BOLD", at(30, 3), F, size=1.5, thickness=0.3, bold=True),
          gr_text(b, "ITALIC", at(10, 7), F, size=1.5, thickness=0.25, italic=True),
          gr_text(b, "ROT30", at(30, 7.5), F, angle=30, size=1.5, thickness=0.25),
          gr_text(b, "LINE ONE\nLINE TWO", at(10, 12), F, size=1.2, thickness=0.2),
          gr_text(b, "LEFT", at(22, 11), F, size=1.2, thickness=0.2, justify=("left",)),
          gr_text(b, "RIGHT", at(42, 13.5), F, size=1.2, thickness=0.2, justify=("right",)),
          gr_text(b, "TTF Sans", at(11, 18), F, size=2.0, thickness=0.2, face=TTF),
          gr_text(b, "TTF Bold", at(32, 18), F, size=2.0, thickness=0.4, face=TTF, bold=True, italic=True),
          gr_text(b, "KNOCKOUT", at(11, 23), F, knockout=True, size=1.5, thickness=0.25),
          gr_text(b, "MIRROR", at(32, 23), B, size=1.5, thickness=0.25, justify=("mirror",)),
          gr_text(b, "TTF Back", at(11, 28), B, size=2.0, thickness=0.2, face=TTF, justify=("mirror",)),
          gr_text_box(b, "BOX TEXT", at(23, 26), at(41, 29.5), F, 0.15, size=1.2, thickness=0.2,
                      justify=("left", "top")))
    b.add(footprint(b, "Feature:TextFp", at(6, 34.5), angle=90, children=[
        text("reference", "U7", (0, -2.5), "F.SilkS", size=1, thickness=0.15),
        text("value", "HIDDEN", (0, 0), F, hide=True, size=1, thickness=0.15),
        text("user", "${REFERENCE}", (0, 2.5), F, size=1, thickness=0.15),
        text("user", "FP TTF", (0, 6), F, size=1.2, thickness=0.15, face=TTF)]))
    return b


def tracks_arcs():
    """Tracks 0.1 to 2 mm wide, arc tracks of 90 and 180 degrees and an almost straight one, a
    segment-arc-segment chain, a zero-length track, two nets that cross (a short), overlapping
    tracks of one net, a 1 um track, a T and an acute junction, tracks and an arc on B.Cu.  The
    crossing tracks end on pads of their own nets: without them KiCad gives both the same net."""
    b = new_board("tracks_arcs", 2, (44, 24))
    F, B = "F.Cu", "B.Cu"
    for x, w in zip((3, 6, 9, 12, 15, 18, 22, 27), (0.1, 0.15, 0.2, 0.25, 0.3, 0.5, 1.0, 2.0)):
        b.add(segment(b, at(x, 2), at(x, 8), w, F, f"W{round(w * 100):03d}"))
    b.add(arc(b, at(32, 2), at(34.12132, 2.87868), at(35, 5), 0.3, F, "ARC90"),
          arc(b, at(38, 5), at(40, 3), at(42, 5), 0.3, F, "ARC180"),
          segment(b, at(3, 12), at(8, 12), 0.3, F, "CHAIN"),
          arc(b, at(8, 12), at(9.414214, 12.585786), at(10, 14), 0.3, F, "CHAIN"),
          segment(b, at(10, 14), at(10, 18), 0.3, F, "CHAIN"),
          segment(b, at(14, 12), at(14, 12), 0.8, F, "DOT"),
          segment(b, at(16, 13), at(22, 13), 0.3, F, "SHORT_A"),
          segment(b, at(19, 11), at(19, 15), 0.3, F, "SHORT_B"),
          footprint(b, "Feature:ShortPads", at(16, 13), children=[
              ref("J1", -3.5), pad("1", "smd", "rect", (0, 0), (0.8, 0.8), SMD, net="SHORT_A"),
              pad("2", "smd", "rect", (3, -2), (0.8, 0.8), SMD, net="SHORT_B")]),
          segment(b, at(24, 12), at(30, 12), 0.3, F, "OVERLAP"),
          segment(b, at(27, 12), at(33, 12), 0.3, F, "OVERLAP"),
          segment(b, at(35, 12), at(35.001, 12), 0.25, F, "TINY"),
          arc(b, at(24, 16), at(29, 16.01), at(34, 16), 0.3, F, "FLAT"),
          segment(b, at(36, 15), at(42, 15), 0.3, F, "TEE"),
          segment(b, at(39, 15), at(39, 19), 0.3, F, "TEE"),
          segment(b, at(36, 21), at(42, 21), 0.3, F, "ACUTE"),
          segment(b, at(36, 21), at(42, 22.5), 0.3, F, "ACUTE"),
          segment(b, at(3, 20), at(20, 20), 0.5, B, "B_TRACK"),
          arc(b, at(24, 20), at(26, 18), at(28, 20), 0.4, B, "B_ARC"))
    return b


BOARDS = [pad_shapes, copper_graphics, copper_text, tracks_arcs]
