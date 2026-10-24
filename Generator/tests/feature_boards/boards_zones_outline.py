"""Boards 11 to 13: copper zones and board outlines."""
import math

from common import X0, Y0, at, new_board
from footprints7 import footprint, pad, shape, text
from kicad7 import gr_arc, gr_circle, gr_curve, gr_line, gr_poly, gr_rect, segment, via, zone

THT = ("*.Cu", "*.Mask")
SMD = ("F.Cu", "F.Paste", "F.Mask")
EDGE = "Edge.Cuts"


def rect(x0, y0, x1, y1):
    return [at(x0, y0), at(x1, y0), at(x1, y1), at(x0, y1)]


def ref(s, y=-2.5):
    return text("reference", s, (0, y), "F.SilkS", size=1, thickness=0.15)


def tie(b, net, p, name):
    """A one-pad footprint that connects a zone: KiCad counts zone copper reached only by vias and
    tracks as isolated, and keeps it whatever the island setting."""
    return footprint(b, "Feature:ZoneTie", p, children=[
        ref(name, -1.6), pad("1", "thru_hole", "circle", (0, 0), (1.4, 1.4), THT, drill=0.7, net=net)])


def zones():
    """Four layers of zones: thermal reliefs and a solid connection to the same pads, pads that
    override the zone's connection, a pad of another net inside a zone, hatched fills at 0 and 45
    degrees, a zone split in two by a track with its island kept on In1 and removed on In2, a zone
    on two layers with a cut-out, zones of two priorities overlapping, a zone left unfilled, and a
    keepout area that a zone flows around."""
    b = new_board("zones", 4, (40, 31))
    F, I1, I2, B = "F.Cu", "In1.Cu", "In2.Cu", "B.Cu"
    b.add(footprint(b, "Feature:ZonePads", at(5, 6), children=[
        ref("J1"), pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="GND"),
        pad("2", "smd", "rect", (4, 0), (1.5, 1.5), SMD, net="GND"),
        pad("3", "smd", "rect", (8, 0), (1.5, 1.5), SMD, net="SIG"),
        pad("4", "thru_hole", "circle", (0, 5), (1.7, 1.7), THT, drill=1.0, net="GND", zone_connect=2),
        pad("5", "thru_hole", "circle", (4, 5), (1.7, 1.7), THT, drill=1.0, net="GND", zone_connect=0),
        pad("6", "thru_hole", "rect", (8, 5), (1.7, 1.7), THT, drill=1.0, net="GND")]))
    b.add(segment(b, at(13, 6), at(17.5, 6), 0.3, F, "SIG"), segment(b, at(17.5, 6), at(17.5, 12.5), 0.3, F, "SIG"),
          via(b, at(16, 3), 0.8, 0.4, "GND"))
    b.add(zone(b, "GND", [F], rect(1, 1, 19, 14)),
          zone(b, "GND", [B], rect(1, 1, 19, 14), connect="yes"))
    hatch = dict(thickness=0.5, gap=1.0)
    b.add(zone(b, "HATCH", [F], rect(21, 1, 39, 14), hatch=hatch),
          zone(b, "HATCH", [B], rect(21, 1, 39, 14), hatch=dict(hatch, orientation=45)),
          tie(b, "HATCH", at(36, 4), "TP1"))
    b.add(zone(b, "PWR", [I1], rect(21, 1, 39, 14), islands=(1, 10)),
          zone(b, "PWR", [I2], rect(21, 1, 39, 14)),
          tie(b, "PWR", at(24, 7), "TP2"),
          segment(b, at(30, 0.6), at(30, 14.4), 0.5, I1, "SPLIT"),
          segment(b, at(30, 0.6), at(30, 14.4), 0.5, I2, "SPLIT"))
    b.add(zone(b, "MULTI", [I1, I2], rect(1, 16, 19, 29), holes=[rect(6, 20, 12, 25)]),
          tie(b, "MULTI", at(3, 18.5), "TP3"))
    b.add(zone(b, "LOW", [F], rect(1, 16, 14, 29), priority=0), tie(b, "LOW", at(4, 22), "TP4"),
          zone(b, "HIGH", [F], rect(8, 16, 19, 29), priority=1), tie(b, "HIGH", at(16, 22), "TP5"))
    b.add(zone(b, "UNF", [F], rect(21, 16, 29, 22), name="UNFILLED", unfilled=True),
          tie(b, "UNF", at(25, 19), "TP6"))
    b.add(zone(b, None, [F, B], rect(31, 16, 39, 22), name="KEEPOUT",
               keepout=dict(tracks="not_allowed", vias="not_allowed", pads="not_allowed",
                            copperpour="not_allowed", footprints="allowed")),
          zone(b, "KGND", [B], rect(21, 16, 39, 29)), tie(b, "KGND", at(25, 26), "TP7"))
    return b


def outline_shapes():
    """An outline of lines, rounded corners (arcs), a Bezier edge and a notch; cut-outs drawn as a
    circle, a rectangle, a polygon, a slot of two lines and two arcs, a rectangle of four lines whose
    ends miss by 3 nm, and a circle and a rectangle on Edge.Cuts inside a footprint at 30 degrees;
    zones on both sides that KiCad fills up to the outline and around the cut-outs."""
    b = new_board("outline_shapes", 2, None)
    E = lambda a, c: gr_line(b, at(*a), at(*c), EDGE)
    A = lambda s, m, e: gr_arc(b, at(*s), at(*m), at(*e), EDGE)
    r = 3 - 3 / math.sqrt(2)                                      # corner arc mid-point offset
    b.add(E((3, 0), (15, 0)), gr_curve(b, at(15, 0), at(18, 3), at(22, -3), at(25, 0), EDGE),
          E((25, 0), (37, 0)), A((37, 0), (40 - r, r), (40, 3)), E((40, 3), (40, 27)),
          A((40, 27), (40 - r, 30 - r), (37, 30)), E((37, 30), (24, 30)), E((24, 30), (24, 27)),
          E((24, 27), (20, 27)), E((20, 27), (20, 30)), E((20, 30), (3, 30)),
          A((3, 30), (r, 30 - r), (0, 27)), E((0, 27), (0, 3)), A((0, 3), (r, r), (3, 0)))
    hexagon = [at(21 + 2.2 * math.cos(math.radians(a)), 8 + 2.2 * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    b.add(gr_circle(b, at(6, 8), 2, EDGE), gr_rect(b, at(11, 6), at(15, 10), EDGE),
          gr_poly(b, hexagon, EDGE, filled=False),
          E((26, 7), (32, 7)), A((32, 7), (33, 8), (32, 9)), E((32, 9), (26, 9)), A((26, 9), (25, 8), (26, 7)))
    gap = (X0 + 6.000004, Y0 + 14)                                 # 3 nm short of the first line's start
    b.add(gr_line(b, (X0 + 6.000007, Y0 + 14), at(12, 14), EDGE), E((12, 14), (12, 18)), E((12, 18), (6, 18)),
          gr_line(b, at(6, 18), gap, EDGE))
    b.add(footprint(b, "Feature:EdgeFp", at(20, 18), angle=30, children=[
        ref("H1", -3), shape("circle", EDGE, 0.1, c=(0, 0), r=1.5),
        shape("rect", EDGE, 0.1, a=(3, -1), c=(6, 1))]))
    b.add(footprint(b, "Feature:GndPad", at(34, 20), children=[
        ref("J1"), pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="GND")]))
    whole = rect(-2, -4, 42, 32)
    b.add(zone(b, "GND", ["F.Cu"], whole), zone(b, "GND", ["B.Cu"], whole),
          segment(b, at(3, 13), at(3, 24), 0.3, "F.Cu", "SIG"))
    return b


def outline_none():
    """No Edge.Cuts at all: two plated pads joined by a track, and a via."""
    b = new_board("outline_none", 2, None)
    b.add(footprint(b, "Feature:TwoPads", at(5, 5), children=[
        ref("J1"), pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="A"),
        pad("2", "thru_hole", "circle", (10, 0), (1.7, 1.7), THT, drill=1.0, net="A")]))
    b.add(segment(b, at(5, 5), at(15, 5), 0.5, "F.Cu", "A"), via(b, at(10, 9), 0.8, 0.4, "B"))
    return b


def outline_two():
    """Two separate boards in one file, one of them with a square hole that has a third, small
    board inside it."""
    b = new_board("outline_two", 2, None)
    b.add(gr_rect(b, at(0, 0), at(20, 20), EDGE), gr_rect(b, at(5, 5), at(15, 15), EDGE),
          gr_rect(b, at(8, 8), at(12, 12), EDGE), gr_rect(b, at(24, 0), at(40, 20), EDGE))
    b.add(segment(b, at(2, 2), at(18, 2), 0.5, "F.Cu", "A_NET"),
          segment(b, at(9, 10), at(11, 10), 0.5, "F.Cu", "ISLAND"),
          zone(b, "B_GND", ["B.Cu"], rect(24, 0, 40, 20)), tie(b, "B_GND", at(32, 10), "TP1"))
    return b


BOARDS = [zones, outline_shapes, outline_none, outline_two]
