"""Boards for the KiCad 10 features that cut or fill holes, and for hatched drawings: backdrills,
counterbores and countersinks, the protection of vias (IPC-4761) and hatched fills."""
from boards_later import SMD, THT, new_board, ref, stub
from common import OUTER, PLAIN, X0, Y0, at
from footprints7 import pad, shape, text
from footprints_later import footprint
from kicad7 import copper_names, f, q, stackup, xy
from kicad_later import K10, gr_circle, gr_line, gr_poly, gr_rect, gr_text, segment, via

NPTH = ("*.Cu", "*.Mask")


def backdrills():
    """KiCad 10's backdrills on six layers: from the back down to each inner layer and from the front
    (tertiary drills), both on one via, through the whole board, as wide as the pad, narrower than
    the hole, starting and ending on the same layer, on a blind via and through a track that leaves
    the drilled-out layer; plated pads with a backdrill and a tertiary drill, a non-plated hole
    stepped by one, and drills KESE leaves out as KiCad does: on an SMD pad, with no size, and to a
    layer the board does not have."""
    b = new_board("backdrills", K10, 6, (52, 32))
    F, I1, I2, I3, I4, B = copper_names(6)
    rows = [
        [("BD_B_IN4", dict(backdrill=(0.6, B, I4)), I3), ("BD_B_IN3", dict(backdrill=(0.6, B, I3)), I2),
         ("BD_B_IN2", dict(backdrill=(0.6, B, I2)), I1), ("BD_B_IN1", dict(backdrill=(0.6, B, I1)), F),
         ("TD_F_IN1", dict(tertiary=(0.6, F, I1)), I2), ("TD_F_IN4", dict(tertiary=(0.6, F, I4)), B)],
        [("BD_BOTH", dict(backdrill=(0.6, B, I4), tertiary=(0.6, F, I1)), I2),
         ("BD_TRACK_CUT", dict(backdrill=(0.6, B, I3)), I4), ("BD_PAD_WIDE", dict(backdrill=(0.8, B, I3)), F),
         ("BD_NARROW", dict(backdrill=(0.3, B, I3)), F), ("BD_THROUGH", dict(backdrill=(0.6, F, B)), F),
         ("BD_SAME_LAYER", dict(backdrill=(0.6, B, B)), F)],
        [("BD_NO_SIZE", dict(backdrill=(0, B, I3)), F), ("BD_NO_LAYER", dict(backdrill=(0.6, B, "In7.Cu")), F)]]
    for j, row in enumerate(rows):
        for i, (net, opts, layer) in enumerate(row):
            p = at(4 + 8 * i, 4 + 6 * j)
            b.add(via(b, p, 0.8, 0.4, net, **opts), stub(b, p, layer, net))
            if net in ("BD_B_IN4", "BD_BOTH"):          # the far end of the signal
                b.add(stub(b, p, I3 if net == "BD_BOTH" else F, net, -2.0))
    p = at(20, 16)
    b.add(via(b, p, 0.8, 0.4, "BD_BLIND", (F, I2), "blind", tertiary=(0.6, F, I1)), stub(b, p, I2, "BD_BLIND"))
    b.add(footprint(b, "Feature:BackdrillPad", at(5, 26), children=[
        ref("J1", -2), pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="P_BACKDRILL",
                           backdrill=(1.3, B, I3))]))
    b.add(segment(b, at(5, 26), at(9, 26), 0.3, I2, "P_BACKDRILL"))
    b.add(footprint(b, "Feature:TertiaryPad", at(15, 26), children=[
        ref("J2", -2), pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="P_TERTIARY",
                           tertiary=(1.3, F, I2))]))
    b.add(segment(b, at(15, 26), at(19, 26), 0.3, I3, "P_TERTIARY"))
    b.add(footprint(b, "Feature:SteppedHole", at(27, 26), children=[
        ref("H1", -3), pad("", "np_thru_hole", "circle", (0, 0), (2.2, 2.2), NPTH, drill=2.2,
                           backdrill=(3.0, B, I3))]))
    b.add(footprint(b, "Feature:SmdBackdrill", at(38, 26), children=[
        ref("U1", -2), pad("1", "smd", "rect", (0, 0), (1.5, 1.5), SMD, net="P_SMD", backdrill=(0.6, B, I3))]))
    return b


def post_machining():
    """KiCad 10's counterbores and countersinks on four layers.  Mounting holes counterbored from the
    front and from the back, deeper than the board and to a floor inside an inner copper layer;
    countersunk at 82, 90, 100 and 120 degrees, from the back, to a depth short of the cone's tip, and
    smaller than the hole (nothing to cut).  A plated pad counterbored on the front and countersunk on
    the back, a pad whose counterbore is centred on the pad off its offset drill, vias counterbored
    and countersunk, and what KESE leaves out as KiCad does: a counterbore with no depth, a countersink
    with no angle, and one on an SMD pad."""
    b = new_board("post_machining", K10, 4, (60, 36))
    F, I1, I2, B = copper_names(4)
    holes = [("CB_FRONT", dict(front_pm=("counterbore", 6.0, 1.0, None))),
             ("CB_BACK", dict(back_pm=("counterbore", 6.0, 0.5, None))),
             ("CB_DEEP", dict(front_pm=("counterbore", 5.0, 2.0, None))),
             ("CB_IN_IN1", dict(front_pm=("counterbore", 5.0, 0.245, None))),
             ("CS_82", dict(front_pm=("countersink", 6.3, None, 82))),
             ("CS_90", dict(front_pm=("countersink", 6.3, None, 90))),
             ("CS_100", dict(front_pm=("countersink", 6.3, None, 100))),
             ("CS_120", dict(front_pm=("countersink", 6.3, None, 120))),
             ("CS_DEPTH", dict(front_pm=("countersink", 6.0, 0.8, 90))),
             ("CS_BACK", dict(back_pm=("countersink", 6.3, None, 90))),
             ("CS_INSIDE", dict(front_pm=("countersink", 2.0, None, 90))),
             ("CB_NO_DEPTH", dict(front_pm=("counterbore", 5.0, None, None)))]
    for k, (name, opts) in enumerate(holes):
        p = at(6 + 10 * (k % 6), 6 + 10 * (k // 6))
        b.add(footprint(b, f"Feature:{name}", p, children=[
            ref(f"H{k + 1}", -4), pad("", "np_thru_hole", "circle", (0, 0), (3.2, 3.2), NPTH, drill=3.2, **opts)]))
    b.add(footprint(b, "Feature:MachinedPad", at(6, 28), children=[
        ref("J1", -2.5), pad("1", "thru_hole", "circle", (0, 0), (2.5, 2.5), THT, drill=1.3, net="P_MACHINED",
                             front_pm=("counterbore", 2.2, 0.5, None), back_pm=("countersink", 2.4, None, 90))]))
    b.add(segment(b, at(6, 28), at(10, 28), 0.3, I1, "P_MACHINED"))
    b.add(footprint(b, "Feature:OffsetPad", at(16, 28), children=[
        ref("J2", -2.5), pad("1", "thru_hole", "oval", (0, 0), (3.0, 2.0), THT, drill=1.0, net="P_OFFSET",
                             offset=(0.5, 0), front_pm=("counterbore", 1.6, 0.4, None))]))
    b.add(via(b, at(24, 28), 0.8, 0.4, "V_COUNTERBORE", back_pm=("counterbore", 0.9, 0.3, None)),
          stub(b, at(24, 28), F, "V_COUNTERBORE"))
    b.add(via(b, at(30, 28), 0.8, 0.4, "V_COUNTERSINK", front_pm=("countersink", 1.0, None, 90)),
          stub(b, at(30, 28), B, "V_COUNTERSINK"))
    b.add(via(b, at(36, 28), 0.8, 0.4, "V_NO_ANGLE", front_pm=("countersink", 1.0, None, None)),
          stub(b, at(36, 28), B, "V_NO_ANGLE"))
    b.add(footprint(b, "Feature:SmdCounterbore", at(46, 28), children=[
        ref("U1", -2), pad("1", "smd", "rect", (0, 0), (1.5, 1.5), SMD, net="P_SMD",
                           front_pm=("counterbore", 1.2, 0.2, None))]))
    return b


def via_protection():
    """KiCad 10's via protection (IPC-4761) on four layers: Types I to VII on the front, then on both
    faces (tented, tented and covered, plugged, plugged and covered, filled, filled and covered,
    filled and capped); a via left to the board's setting (plugged on the back), covered but not
    tented, capped with no fill, filled and backdrilled, plugged and counterbored on the same face,
    a filled blind via, a filled and capped buried via (a cap needs an outer end) and a blind via
    covered at its inner end (no effect)."""
    b = new_board("via_protection", K10, 4, (60, 24))
    b.vias.update(plugging=(False, True))                 # the board's setting: plugged on the back
    F, I1, I2, B = copper_names(4)
    no_plug = dict(plugging=(False, False))
    rows = [
        [("T1_TENTED", dict(tenting=(True, False), **no_plug)),
         ("T2_TENT_COVER", dict(tenting=(True, False), covering=(True, False), **no_plug)),
         ("T3_PLUG", dict(plugging=(True, False))),
         ("T4_PLUG_COVER", dict(plugging=(True, False), covering=(True, False))),
         ("T5_FILL", dict(filling=True, **no_plug)),
         ("T6_FILL_COVER", dict(filling=True, covering=(True, False), **no_plug)),
         ("T7_FILL_CAP", dict(filling=True, capping=True, **no_plug))],
        [("T1B_TENTED", dict(tenting=(True, True), **no_plug)),
         ("T2B_TENT_COVER", dict(tenting=(True, True), covering=(True, True), **no_plug)),
         ("T3B_PLUG", dict(plugging=(True, True))),
         ("T4B_PLUG_COVER", dict(plugging=(True, True), covering=(True, True))),
         ("T5B_FILL_OPEN", dict(filling=True, tenting=(False, False), **no_plug)),
         ("T6B_FILL_COVER", dict(filling=True, covering=(True, True), **no_plug)),
         ("T7B_FILL_CAP_COVER", dict(filling=True, capping=True, covering=(True, True), **no_plug))],
        [("INHERIT", dict(covering=(None, None))),
         ("COVER_UNTENTED", dict(tenting=(False, False), covering=(True, True), **no_plug)),
         ("CAP_ONLY", dict(capping=True, **no_plug)),
         ("FILL_BACKDRILL", dict(filling=True, backdrill=(0.6, B, I2), **no_plug)),
         ("PLUG_COUNTERBORE", dict(plugging=(True, False), front_pm=("counterbore", 1.2, 0.3, None)))]]
    for j, row in enumerate(rows):
        for i, (net, opts) in enumerate(row):
            p = at(4 + 8 * i, 4 + 6 * j)
            b.add(via(b, p, 0.8, 0.4, net, **opts), stub(b, p, I1 if net == "FILL_BACKDRILL" else F, net))
    special = [("BLIND_FILLED", (F, I1), "blind", dict(filling=True, **no_plug)),
               ("BURIED_CAPPED", (I1, I2), "buried", dict(filling=True, capping=True, **no_plug)),
               ("BLIND_COVER_INNER", (I1, B), "blind", dict(covering=(True, True), plugging=(False, False)))]
    for i, (net, ends, kind, opts) in enumerate(special):
        p = at(44 + 6 * i, 16)
        b.add(via(b, p, 0.6, 0.3, net, ends, kind, **opts), stub(b, p, ends[0], net, 1.5))
    return b


def text_box(b, s, a, c, layer, width=0.1):
    """A board text box (gr_text_box) as KiCad 10 writes it, with a border."""
    return (f"(gr_text_box {q(s)} (start {xy(a)}) (end {xy(c)}) (margins 0.5 0.5 0.5 0.5) (layer {q(layer)}) "
            f"{b.ts()} (effects (font (size 1 1) (thickness 0.15)) (justify left top)) (border yes) "
            f"(stroke (width {f(width)}) (type solid)) (knockout no))")


def hatched_fills():
    """KiCad 10's hatched fills on two layers.  Hatched, reverse-hatched and cross-hatched rectangles,
    a rectangle with rounded corners, circles and polygons on copper (with a net), silkscreen and the
    solder mask, at pen widths from 0.1 to 0.5 mm; copper left bare by the mask under a hatch; the
    hatch cut back around board text, a line, an overlapping hatched shape, a text box and another
    footprint's reference, but not around a footprint's own reference or another footprint's other
    text; a turned footprint with hatched drawings; a hatch too fine for its size, held to about 100
    lines; a hatch drawn with no pen (nothing), a hatched custom pad shape (solid) and a hatched board
    outline (the outline only)."""
    b = new_board("hatched_fills", K10, 2, None)
    b.add(gr_rect(b, (X0, Y0), (X0 + 64, Y0 + 44), "Edge.Cuts", 0.1, "hatch"))
    b.add(gr_rect(b, at(3, 3), at(11, 9), "F.Cu", 0.1, "hatch", net="HATCH"),
          gr_rect(b, at(14, 3), at(22, 9), "F.Cu", 0.15, "reverse_hatch", radius=1.5, net="REVERSE"),
          gr_circle(b, at(28, 6), 3, "F.Cu", 0.2, "cross_hatch", net="CROSS"),
          gr_poly(b, [at(34, 3), at(42, 3), at(42, 9), at(36, 9)], "F.Cu", 0.25, "hatch", net="POLY"),
          gr_rect(b, at(45, 3), at(61, 9), "B.Cu", 0.5, "cross_hatch", net="WIDE"))
    b.add(gr_circle(b, at(6, 15), 3, "F.SilkS", 0.15, "hatch"),
          gr_rect(b, at(11, 12), at(19, 18), "F.SilkS", 0.12, "cross_hatch"),
          gr_rect(b, at(22, 12), at(30, 18), "F.Mask", 0.2, "reverse_hatch"),
          gr_poly(b, [at(33, 12), at(41, 12), at(37, 18)], "B.Mask", 0.2, "cross_hatch"),
          gr_rect(b, at(44, 12), at(52, 18), "F.Cu", 0.2, "hatch", net="BARE", layers=("F.Cu", "F.Mask")),
          gr_rect(b, at(55, 12), at(61, 18), "F.Cu", 0, "hatch", net="NO_PEN"))
    b.add(gr_rect(b, at(3, 21), at(13, 28), "F.Cu", 0.1, "hatch", net="KO_TEXT"),
          gr_text(b, "KO", at(8, 24.5), "F.Cu", size=2, thickness=0.3),
          gr_rect(b, at(16, 21), at(26, 28), "F.Cu", 0.1, "reverse_hatch", net="KO_LINE"),
          gr_line(b, at(16, 28), at(26, 21), "F.Cu", 0.3),
          gr_rect(b, at(29, 21), at(37, 27), "F.Cu", 0.1, "hatch", net="KO_A"),
          gr_rect(b, at(33, 23), at(41, 28), "F.Cu", 0.1, "cross_hatch", net="KO_B"),
          gr_rect(b, at(44, 21), at(61, 28), "F.Cu", 0.1, "hatch", net="KO_BOX"),
          text_box(b, "BOX", at(48, 22.5), at(57, 26.5), "F.Cu"))
    b.add(footprint(b, "Feature:HatchedTurned", at(8, 36), angle=30, children=[
        ref("U1", 0), shape("rect", "F.SilkS", 0.12, "hatch", a=(-4, -3), c=(4, 3)),
        shape("circle", "F.Cu", 0.15, "cross_hatch", c=(0, 0), r=1.5)]))
    b.add(gr_rect(b, at(17, 31), at(31, 41), "F.SilkS", 0.12, "hatch"))
    b.add(footprint(b, "Feature:Fields", at(24, 36), children=[
        ref("U2", -2), text("user", "USER", (0, 2.5), "F.SilkS", size=1, thickness=0.15)]))
    b.add(gr_rect(b, at(34, 31), at(62, 35), "B.Cu", 0.02, "hatch", net="FINE"))
    star = "(gr_poly (pts (xy -1 -1) (xy 1 -1) (xy 1 1) (xy -1 1)) (width 0.1) (fill hatch))"
    b.add(footprint(b, "Feature:HatchedPad", at(40, 39), children=[
        ref("J1", -2.5), pad("1", "smd", "custom", (0, 0), (0.6, 0.6), SMD, net="P_HATCH", primitives=[star])]))
    return b


def plated_edge_machining():
    """KiCad 10's post machining, backdrills and blind vias at a plated board edge (edge_plating
    yes) on four layers: a counterbore from the front and a countersink from the back that cross the
    edge while their holes stay inside, a via backdrilled from the back and a plated pad drilled from
    the front (a tertiary drill) wider than their rings, both crossing the edge, and blind vias from
    the front that reach into the plating; GND tracks along the left edge give the plating its net.
    Each cuts the plating only between its own heights."""
    b = new_board("plated_edge_machining", K10, 4, (40, 24))
    stackup(b, PLAIN[4], [OUTER, 0.0175, 0.0175, OUTER], extra=("(edge_plating yes)",))
    F, I1, I2, B = copper_names(4)
    b.add(*[segment(b, at(0.25, 0.5), at(0.25, 23.5), 0.5, layer, "GND") for layer in (F, B)])
    b.add(footprint(b, "Feature:CounterboreAtEdge", at(8, 2), children=[
        ref("H1", 4.2), pad("", "np_thru_hole", "circle", (0, 0), (3.2, 3.2), NPTH, drill=3.2,
                          front_pm=("counterbore", 6.0, 0.5, None))]))
    b.add(footprint(b, "Feature:CountersinkAtEdge", at(8, 22.2), children=[
        ref("H2", -3.5), pad("", "np_thru_hole", "circle", (0, 0), (3.2, 3.2), NPTH, drill=3.2,
                             back_pm=("countersink", 5.0, None, 90))]))
    p = at(20, 0.5)
    b.add(via(b, p, 0.8, 0.4, "BD_EDGE", backdrill=(1.2, B, I2)), segment(b, p, at(20, 4), 0.25, F, "BD_EDGE"))
    b.add(footprint(b, "Feature:TertiaryAtEdge", at(30, 1), children=[
        ref("J1", 2.5), pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="P_EDGE",
                            tertiary=(2.4, F, I1))]))
    b.add(segment(b, at(30, 1), at(30, 5), 0.3, I2, "P_EDGE"))
    for x in (16, 22):
        p = at(x, 23.84)
        b.add(via(b, p, 0.6, 0.3, "GND", (F, I1), "blind"), segment(b, p, at(x, 20), 0.25, I1, "GND"))
    return b


BOARDS = [backdrills, post_machining, via_protection, hatched_fills, plated_edge_machining]
