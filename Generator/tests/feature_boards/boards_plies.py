"""Boards 29 and 29d: gaps between copper layers that are laid up of plies (KiCad's sub-layers of a
dielectric), and one fabricator's four-layer build as it is pressed."""
from boards_stackup_mask import SMD, THT, layer_tracks, ref, tht
from common import at, new_board
from footprints7 import footprint, pad
from kicad7 import core, gr_text, prepreg, segment, stackup, via, zone

# JLCPCB's JLC04161H-2116C, a 1.6 mm four-layer build: one core, and on each side of it a 1080 ply
# against the inner copper and a 2116 ply under the outer copper (thickness and er from JLCPCB's
# impedance calculator; the loss tangent is a generic FR4 value)
REAL = [[prepreg(0.124, 4.16, 0.02, "2116"), prepreg(0.0764, 3.91, 0.02, "1080")],
        core(1.065, 4.6, 0.02, "FR4 core"),
        [prepreg(0.0764, 3.91, 0.02, "1080"), prepreg(0.124, 4.16, 0.02, "2116")]]
REAL_COPPER = [0.035, 0.0152, 0.0152, 0.035]
REAL_THICKNESS = 1.5862                    # the laminate (1.4962), the outer copper and two masks of 0.01


def stackup_plies():
    """Six layers whose gaps are laid up of plies, as KiCad's stack-up editor writes them (the
    sub-layers of a dielectric): a 1080 ply on a 2116 ply under F.Cu and the same mirrored over B.Cu,
    a core of one ply, three equal 7628 plies between In2.Cu and In3.Cu, and a core with a bond film
    of half a micrometre, thinner than KESE builds on its own.  A through via, a blind via from each
    side, a buried via through the three equal plies and one through both cores, a plated and a
    non-plated hole, a track on every layer and GND planes on In2.Cu and In3.Cu."""
    b = new_board("stackup_plies", 6, (36, 22), stack=False)
    b.thickness = 1.4605
    film = dict(kind="core", t=0.0005, material="Bond film", er=3.2, tand=0.02)
    dielectrics = [[prepreg(0.08, 3.9, 0.018, "1080"), prepreg(0.12, 4.2, 0.016, "2116")],
                   core(0.3, 4.6, 0.018, "FR4 core"),
                   [prepreg(0.1, 4.4, 0.017, "7628")] * 3,
                   [core(0.3, 4.6, 0.018, "FR4 core"), film],
                   [prepreg(0.12, 4.2, 0.016, "2116"), prepreg(0.08, 3.9, 0.018, "1080")]]
    stackup(b, dielectrics, [0.035, 0.0175, 0.0175, 0.0175, 0.0175, 0.035], finish="ENIG")
    layer_tracks(b, 8, 24, 3, 3)
    vias = [((28, 4), ("F.Cu", "B.Cu"), "GND", ""), ((28, 8), ("F.Cu", "In1.Cu"), "BLIND_TOP", "blind"),
            ((28, 12), ("In2.Cu", "In3.Cu"), "BURIED", "blind"), ((28, 16), ("In4.Cu", "B.Cu"), "BLIND_BOT", "blind"),
            ((28, 20), ("In1.Cu", "In4.Cu"), "BURIED_WIDE", "blind")]
    for p, ends, net, kind in vias:
        p = at(*p)
        b.add(via(b, p, 0.6, 0.3, net, ends, kind))
        if net != "GND":
            b.add(segment(b, p, (p[0] + 3, p[1]), 0.25, ends[0], net),
                  segment(b, p, (p[0] + 3, p[1] - 1.5), 0.25, ends[1], net))
    full = [at(0, 0), at(36, 0), at(36, 22), at(0, 22)]
    b.add(tht(b, "GND", at(4, 8), "J1"),
          footprint(b, "Feature:Hole", at(4, 16), children=[
              ref("H1", -2.6), pad("", "np_thru_hole", "circle", (0, 0), (2.2, 2.2), THT, drill=2.2)]),
          zone(b, "GND", ["In2.Cu", "In3.Cu"], full),
          gr_text(b, "PLIES", at(14, 20.5), "F.SilkS", size=1, thickness=0.15))
    return b


def stackup_real():
    """A fabricator's four-layer build as it is pressed (JLCPCB's JLC04161H-2116C, 1.6 mm): under each
    outer copper a 2116 ply of 0.124 mm (er 4.16) and a 1080 ply of 0.0764 mm (er 3.91), a core of
    1.065 mm, inner copper of 15.2 um and outer copper of 35 um.  A microstrip between two launch
    pads over a GND plane on In1.Cu, GND copper beside it with a fence of vias, a +3V3 plane on
    In2.Cu fed through a via, a decoupling capacitor, a header, and tracks on the back.  Green mask,
    white silk, ENIG."""
    b = new_board("stackup_real", 4, (40, 24), stack=False)
    b.thickness = REAL_THICKNESS
    stackup(b, REAL, REAL_COPPER, mask_color="Green", silk_color="White", finish="ENIG", constraints=True)
    for name, x in (("J1", 4), ("J2", 36)):
        b.add(footprint(b, "Feature:RFLaunch", at(x, 12), children=[
            ref(name, -3.4), pad("1", "smd", "rect", (0, 0), (1.5, 1.0), SMD, net="RF"),
            pad("2", "smd", "rect", (0, -1.8), (1.5, 1.2), SMD, net="GND"),
            pad("3", "smd", "rect", (0, 1.8), (1.5, 1.2), SMD, net="GND")]))
    b.add(segment(b, at(4, 12), at(36, 12), 0.36, "F.Cu", "RF"))
    b.add(*[via(b, at(x, 12 + dy), 0.6, 0.3, "GND") for x in range(8, 33, 3) for dy in (-1.5, 1.5)])
    b.add(footprint(b, "Feature:C0603", at(20, 5), children=[
        ref("C1", -1.6), pad("1", "smd", "rect", (-0.8, 0), (0.9, 0.9), SMD, net="+3V3"),
        pad("2", "smd", "rect", (0.8, 0), (0.9, 0.9), SMD, net="GND")]))
    b.add(footprint(b, "Feature:Header", at(8, 20), children=[
        ref("J3", -2), pad("1", "thru_hole", "rect", (0, 0), (1.7, 1.7), THT, drill=1.0, net="+3V3"),
        pad("2", "thru_hole", "circle", (2.54, 0), (1.7, 1.7), THT, drill=1.0, net="GND")]))
    b.add(segment(b, at(19.2, 5), at(16, 5), 0.3, "F.Cu", "+3V3"), via(b, at(16, 5), 0.6, 0.3, "+3V3"),
          *[segment(b, at(*a), at(*c), 0.4, "B.Cu", "+3V3") for a, c in (((16, 5), (16, 22)), ((16, 22), (8, 22)),
                                                                           ((8, 22), (8, 20)))],
          segment(b, at(24, 18), at(34, 18), 0.25, "B.Cu", "CTRL"), segment(b, at(24, 20), at(34, 20), 0.25, "B.Cu", "CTRL2"))
    full = [at(0, 0), at(40, 0), at(40, 24), at(0, 24)]
    b.add(zone(b, "GND", ["F.Cu"], full, clearance=0.4), zone(b, "GND", ["In1.Cu"], full),
          zone(b, "+3V3", ["In2.Cu"], full, clearance=0.4), zone(b, "GND", ["B.Cu"], full),
          gr_text(b, "2116 + 1080", at(30, 4), "F.SilkS", size=1, thickness=0.15))
    return b
