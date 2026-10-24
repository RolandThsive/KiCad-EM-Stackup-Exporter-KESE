"""Boards in a later KiCad format than 7: the via, padstack and copper drawing features of KiCad 10,
and one small board saved in each format from KiCad 6 to 10."""
from common import OUTER, PLAIN, X0, Y0, at, kicad7, kicad7_filled
from footprints7 import pad, shape, text
from footprints_later import footprint
from kicad7 import copper_names, stackup
from kicad_later import (K6, K7, K8, K9, K10, Board, arc, gr_arc, gr_circle, gr_line, gr_poly, gr_rect, gr_text,
                         outline, segment, via, zone)

THT = ("*.Cu", "*.Mask")
SMD = ("F.Cu", "F.Paste", "F.Mask")


def ref(s, y=-2.5, layer="F.SilkS"):
    return text("reference", s, (0, y), layer, size=1, thickness=0.15,
                justify=("mirror",) if layer.startswith("B") else ())


def new_board(name, version, copper, size):
    b = Board(name, version, copper)
    stackup(b, PLAIN[copper], [OUTER] + [0.0175] * (copper - 2) + [OUTER])
    if size:
        b.add(outline(b, X0, Y0, X0 + size[0], Y0 + size[1]))
    return b


def stub(b, p, layer, net, dx=2.0):
    """A short track from a via, so that the via joins copper on that layer."""
    return segment(b, p, (p[0] + dx, p[1]), 0.25, layer, net)


def vias_k10():
    """KiCad 10's via options on four layers: tented on both sides, on the front only, open, and
    left to the board's setting on one side; covered, plugged, capped and filled vias; a backdrill
    from the bottom and one from the top, a counterbore and a countersink; blind, buried and micro
    vias; vias that keep only their start and end rings or drop unused rings; and a plated pad with
    a backdrill and mounting holes with a counterbore and a countersink."""
    b = new_board("vias_k10", K10, 4, (40, 30))
    F, I1, I2, B = copper_names(4)
    rows = [
        [("V_TENT_DEFAULT", {}), ("V_TENT_FRONT", dict(tenting=(True, False))),
         ("V_OPEN", dict(tenting=(False, False))), ("V_TENT_MIXED", dict(tenting=(False, None)))],
        [("V_COVERED", dict(covering=(True, True))), ("V_PLUGGED", dict(plugging=(True, False))),
         ("V_CAPPED", dict(capping=True, filling=True)), ("V_FILLED", dict(filling=True))],
        [("V_BACKDRILL", dict(backdrill=(0.6, B, I2))), ("V_TOPDRILL", dict(tertiary=(0.6, F, I1))),
         ("V_COUNTERBORE", dict(front_pm=("counterbore", 1.2, 0.3, None))),
         ("V_COUNTERSINK", dict(back_pm=("countersink", 1.2, None, 90)))]]
    for j, row in enumerate(rows):
        for i, (net, opts) in enumerate(row):
            p = at(4 + 9 * i, 4 + 5 * j)
            b.add(via(b, p, 0.8, 0.4, net, **opts), stub(b, p, I2 if net == "V_TOPDRILL" else F, net))
    kinds = [("V_BLIND", (F, I1), "blind", {}), ("V_BURIED", (I1, I2), "buried", {}),
             ("V_MICRO", (F, I1), "micro", {}), ("V_START_END", (F, B), "", dict(start_end_only=True)),
             ("V_RM", (F, B), "", dict(remove_unused=True)),
             ("V_RM_KEEP", (F, B), "", dict(remove_unused=True, keep_end=True))]
    for i, (net, ends, kind, opts) in enumerate(kinds):
        p = at(4 + 6 * i, 19)
        size, drill = (0.3, 0.1) if kind == "micro" else (0.6, 0.3)
        b.add(via(b, p, size, drill, net, ends, kind, **opts), stub(b, p, ends[0], net, 1.5))
    b.add(footprint(b, "Feature:BackdrillPad", at(5, 25), children=[
        ref("J1", -2), pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="P_BACKDRILL",
                           backdrill=(1.3, B, I2))]))
    b.add(footprint(b, "Feature:Counterbore", at(17, 25), children=[
        ref("H1", -4), pad("", "np_thru_hole", "circle", (0, 0), (3.2, 3.2), THT, drill=3.2,
                           front_pm=("counterbore", 6.0, 1.0, None))]))
    b.add(footprint(b, "Feature:Countersink", at(29, 25), children=[
        ref("H2", -4), pad("", "np_thru_hole", "circle", (0, 0), (3.2, 3.2), THT, drill=3.2,
                           front_pm=("countersink", 6.3, None, 90))]))
    return b


def padstacks():
    """KiCad 10's padstacks on four layers: a plated pad and a via with one shape on the front,
    another on the inner layers and a third on the back; a pad and a via with their own shape on
    every copper layer; a normal pad and via beside them, and inner tracks to the inner rings."""
    b = new_board("padstacks", K10, 4, (34, 20))
    F, I1, I2, B = copper_names(4)
    fib = ("front_inner_back", {"Inner": dict(shape="circle", size=(1.0, 1.0)),
                                "B.Cu": dict(shape="rect", size=(1.8, 1.8))})
    custom = ("custom", {I1: dict(shape="circle", size=(1.0, 1.0)), I2: dict(shape="oval", size=(1.6, 1.0)),
                         B: dict(shape="roundrect", size=(2.0, 1.4), rratio=0.25)})
    b.add(footprint(b, "Feature:Padstacks", at(5, 6), children=[
        ref("U1", -2.5),
        pad("1", "thru_hole", "circle", (0, 0), (1.6, 1.6), THT, drill=0.8, net="PS_FIB", padstack=fib),
        pad("2", "thru_hole", "roundrect", (5, 0), (2.0, 1.4), THT, drill=0.8, net="PS_CUSTOM", rratio=0.25,
            padstack=custom),
        pad("3", "thru_hole", "circle", (10, 0), (1.6, 1.6), THT, drill=0.8, net="PS_NORMAL"),
        pad("4", "smd", "rect", (15, 0), (1.5, 1.5), SMD, net="PS_SMD")]))
    b.add(segment(b, at(5, 6), at(5, 11), 0.3, I1, "PS_FIB"), segment(b, at(10, 6), at(10, 11), 0.3, I2, "PS_CUSTOM"),
          segment(b, at(15, 6), at(15, 11), 0.3, B, "PS_NORMAL"))
    b.add(via(b, at(5, 15), 0.9, 0.4, "V_FIB", padstack=("front_inner_back", {"Inner": 0.6, "B.Cu": 1.2})),
          via(b, at(12, 15), 0.8, 0.4, "V_CUSTOM", padstack=("custom", {I1: 0.5, I2: 0.7, B: 1.0})),
          via(b, at(19, 15), 0.8, 0.4, "V_NORMAL"))
    b.add(stub(b, at(5, 15), I1, "V_FIB"), stub(b, at(12, 15), I2, "V_CUSTOM"), stub(b, at(19, 15), B, "V_NORMAL"))
    return b


def copper_graphics_nets():
    """KiCad 10's copper drawings: shapes that belong to a net, copper left bare by the solder mask
    (a rectangle, a track and an arc track, with and without a mask margin), rectangles with
    rounded corners, hatched, reverse-hatched and cross-hatched fills, and a board outline drawn
    as one rectangle with rounded corners."""
    b = new_board("copper_graphics_nets", K10, 2, None)
    b.add(outline(b, X0, Y0, X0 + 36, Y0 + 24, radius=2))
    b.add(gr_rect(b, at(3, 3), at(9, 7), "F.Cu", 0.1, True, net="NET_RECT"),
          gr_circle(b, at(14, 5), 2, "F.Cu", 0.1, True, net="NET_CIRCLE"),
          gr_poly(b, [at(19, 3), at(25, 3), at(22, 7)], "B.Cu", 0.1, True, net="NET_POLY"),
          gr_line(b, at(28, 3), at(33, 7), "F.Cu", 0.5, net="NET_LINE"),
          gr_arc(b, at(28, 10), at(30.5, 8.5), at(33, 10), "B.Cu", 0.5, net="NET_ARC"))
    b.add(gr_rect(b, at(3, 10), at(9, 14), "F.Cu", 0.1, True, net="BARE_RECT", layers=("F.Cu", "F.Mask"),
                  mask_margin=0.1),
          segment(b, at(11, 12), at(19, 12), 0.6, "F.Cu", "BARE_TRACK", bare_margin=0.05),
          arc(b, at(21, 13), at(23, 11), at(25, 13), 0.6, "B.Cu", "BARE_ARC", bare_margin=0))
    b.add(gr_rect(b, at(3, 17), at(9, 21), "F.Cu", 0.1, True, radius=1, net="ROUND_RECT"),
          gr_rect(b, at(11, 17), at(16, 21), "F.SilkS", 0.15, radius=0.8),
          gr_rect(b, at(18, 17), at(23, 21), "F.Cu", 0.1, "hatch", net="HATCH_RECT"),
          gr_circle(b, at(27, 19), 2, "B.Cu", 0.1, "cross_hatch", net="CROSS_CIRCLE"),
          gr_poly(b, [at(30, 17), at(34, 17), at(34, 21)], "F.SilkS", 0.1, "reverse_hatch"))
    return b


def formats(version, fills=()):
    """The same small board in KiCad 6, 7, 8, 9 and 10's format: a plated pad and a rounded SMD pad
    in a footprint, a pad on the back of a turned footprint, a track, a via and an arc track, a GND
    zone on the back, and silkscreen and copper text."""
    n = {K6: 6, K7: 7, K8: 8, K9: 9, K10: 10}[version]
    b = new_board(f"format_kicad{n}", version, 2, (24, 16))
    b.add(footprint(b, "Feature:Formats", at(5, 8), children=[
        ref("J1"), text("value", "CONN", (0, 2.5), "F.Fab", hide=True),
        shape("line", "F.SilkS", 0.12, a=(-1.5, 1.5), c=(5.5, 1.5)),
        pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="GND"),
        pad("2", "smd", "roundrect", (4, 0), (1.5, 1.0), SMD, net="SIG", rratio=0.25)]))
    b.add(footprint(b, "Feature:FormatsBack", at(19, 4), angle=90, side="B", children=[
        ref("U1", -2, "B.SilkS"), pad("1", "smd", "rect", (0, 0), (1.2, 1.2), ("B.Cu", "B.Paste", "B.Mask"),
                                      net="SIG2")]))
    b.add(segment(b, at(9, 8), at(13, 8), 0.3, "F.Cu", "SIG"), via(b, at(13, 8), 0.8, 0.4, "SIG"),
          arc(b, at(13, 8), at(13.87868, 10.12132), at(16, 11), 0.3, "B.Cu", "SIG"))
    b.add(zone(b, "GND", "B.Cu", [at(1, 1), at(23, 1), at(23, 15), at(1, 15)], name="GND_FILL", connect="yes",
               fills=fills))
    b.add(gr_text(b, f"KICAD {n}", at(12, 14), "F.SilkS", size=1, thickness=0.15),
          gr_text(b, "CU", at(20, 9), "F.Cu", size=1.5, thickness=0.3),
          gr_circle(b, at(21, 13), 1, "F.SilkS", 0.12))
    return b


def kicad7_fills(board, zone_name):
    """The filled polygons KiCad 7 gives a zone of a board in its format, [(points, is_island)], or
    none without KiCad 7."""
    pcbnew = kicad7()
    if not pcbnew:
        return ()
    filled = kicad7_filled(pcbnew, board.text())
    out = []
    for z in filled.Zones():
        if z.GetZoneName() == zone_name:
            for layer in z.GetLayerSet().Seq():
                polys = z.GetFilledPolysList(layer)
                for i in range(polys.OutlineCount()):
                    chain = polys.COutline(i)
                    points = [(chain.CPoint(j).x / 1e6, chain.CPoint(j).y / 1e6) for j in range(chain.PointCount())]
                    out.append((points, z.IsIsland(layer, i)))
    return out


def in_format(version):
    def build():
        return formats(version, () if version == K7 else kicad7_fills(formats(K7), "GND_FILL"))
    build.__doc__ = formats.__doc__
    return build


VERSIONS = [(c, in_format(v)) for c, v in zip("abcde", (K6, K7, K8, K9, K10))]
BOARDS = [vias_k10, padstacks, copper_graphics_nets, *[fn for _, fn in VERSIONS]]
