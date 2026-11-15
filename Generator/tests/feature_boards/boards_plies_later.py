"""Boards 29b and 29c: KiCad 10's machining cut into a laminate of plies, and the frequency and
model that the format after KiCad 10 gives every dielectric."""
from boards_later import SMD, THT, ref, stub
from boards_plies import REAL, REAL_COPPER, REAL_THICKNESS
from common import X0, Y0, at
from footprints7 import pad
from footprints_later import footprint
from kicad7 import copper_names, core, prepreg, stackup
from kicad_later import AFTER_K10, K10, Board, gr_text, outline, segment, via

NPTH = ("*.Cu", "*.Mask")


def plies_board(name, version, size, dielectrics=REAL, **more):
    """A four-layer board with the build of boards_plies.REAL (or other dielectrics of its thicknesses)."""
    b = Board(name, version, 4, REAL_THICKNESS)
    stackup(b, dielectrics, REAL_COPPER, **more)
    b.add(outline(b, X0, Y0, X0 + size[0], Y0 + size[1]))
    return b


def stackup_plies_machined():
    """KiCad 10's machining in a laminate of plies (four layers, a 2116 and a 1080 ply on each side of
    one core).  Counterbores from the front, their depth from the top of F.Cu: to a floor inside the
    first ply (0.1 mm), exactly between the two plies (0.159 mm), inside the second ply (0.2 mm),
    inside In1.Cu and the resin beside it (0.243 mm) and inside the core (0.5 mm); the same from the
    back into the outer ply and to the join of the plies; a countersink from each side; vias with a
    backdrill and a tertiary drill through both plies, a counterbored via, blind vias through the
    plies and a buried via through the core, and a counterbored plated pad."""
    b = plies_board("stackup_plies_machined", K10, (60, 30))
    F, I1, I2, B = copper_names(4)
    holes = [("CB_PLY1", dict(front_pm=("counterbore", 6.0, 0.1, None))),
             ("CB_JOIN", dict(front_pm=("counterbore", 6.0, 0.159, None))),
             ("CB_PLY2", dict(front_pm=("counterbore", 6.0, 0.2, None))),
             ("CB_RESIN", dict(front_pm=("counterbore", 6.0, 0.243, None))),
             ("CB_CORE", dict(front_pm=("counterbore", 6.0, 0.5, None))),
             ("CS_FRONT", dict(front_pm=("countersink", 6.3, None, 90))),
             ("CB_BACK_PLY", dict(back_pm=("counterbore", 6.0, 0.1, None))),
             ("CB_BACK_JOIN", dict(back_pm=("counterbore", 6.0, 0.159, None))),
             ("CS_BACK", dict(back_pm=("countersink", 6.3, None, 90)))]
    for k, (name, opts) in enumerate(holes):
        p = at(6 + 10 * (k % 6), 6 + 10 * (k // 6))
        b.add(footprint(b, f"Feature:{name}", p, children=[
            ref(f"H{k + 1}", -4), pad("", "np_thru_hole", "circle", (0, 0), (3.2, 3.2), NPTH, drill=3.2, **opts)]))
    vias = [("V_THROUGH", (F, B), "", {}, (F, B)), ("V_BACKDRILL", (F, B), "", dict(backdrill=(0.6, B, I2)), (F, I1)),
            ("V_TOPDRILL", (F, B), "", dict(tertiary=(0.6, F, I1)), (I2, B)),
            ("V_COUNTERBORE", (F, B), "", dict(front_pm=("counterbore", 1.2, 0.159, None)), (I1, B)),
            ("V_BLIND_TOP", (F, I1), "blind", {}, (F, I1)), ("V_BURIED", (I1, I2), "buried", {}, (I1, I2)),
            ("V_BLIND_BOT", (I2, B), "blind", {}, (I2, B))]
    for i, (net, ends, kind, opts, joined) in enumerate(vias):
        p = at(38 + 6 * (i % 4), 14 + 5 * (i // 4))
        b.add(via(b, p, 0.8, 0.4, net, ends, kind, **opts), stub(b, p, joined[0], net), stub(b, p, joined[1], net, -2.0))
    b.add(footprint(b, "Feature:MachinedPad", at(6, 26), children=[
        ref("J1", -2.5), pad("1", "thru_hole", "circle", (0, 0), (2.5, 2.5), THT, drill=1.3, net="P_MACHINED",
                             front_pm=("counterbore", 2.2, 0.1, None), back_pm=("counterbore", 2.2, 0.2, None))]))
    b.add(segment(b, at(6, 26), at(12, 26), 0.3, I1, "P_MACHINED"), segment(b, at(6, 26), at(12, 27.5), 0.3, I2, "P_MACHINED"))
    for i, layer in enumerate((F, I1, I2, B)):
        b.add(segment(b, at(16, 24 + 1.5 * i), at(34, 24 + 1.5 * i), 0.4, layer, layer.split(".")[0].upper()))
    return b


def stackup_frequency():
    """What the format after KiCad 10 adds to every ply of a dielectric (file format 20260511): the
    frequency its er and loss tangent hold at (spec_frequency, in Hz) and how they change with
    frequency (dielectric_model constant or djordjevic_sarkar).  Four layers: a 2116 ply with the
    Djordjevic-Sarkar model at 1 GHz on a 1080 ply with constant values, a core with the model at
    10 GHz, a 1080 ply with the model at 5 GHz on a 2116 ply with constant values at 2.5 GHz, and a
    solder mask of another material on each side."""
    ds = "djordjevic_sarkar"
    dielectrics = [[prepreg(0.124, 4.16, 0.02, "2116", f=1e9, model=ds), prepreg(0.0764, 3.91, 0.02, "1080", f=1e9)],
                   core(1.065, 4.6, 0.02, "FR4 core", f=1e10, model=ds),
                   [prepreg(0.0764, 3.91, 0.02, "1080", f=5e9, model=ds), prepreg(0.124, 4.16, 0.02, "2116", f=2.5e9)]]
    b = plies_board("stackup_frequency", AFTER_K10, (30, 20), dielectrics, mask_color="Green", silk_color="White",
                    finish="ENIG", constraints=True,
                    mask=(dict(material="LPI gloss", er=3.5, tand=0.025), dict(material="LPI matt", er=3.8, tand=0.03)))
    F, I1, I2, B = copper_names(4)
    for i, layer in enumerate((F, I1, I2, B)):
        b.add(segment(b, at(8, 4 + 4 * i), at(25, 4 + 4 * i), 0.3, layer, layer.split(".")[0].upper()))
    b.add(footprint(b, "Feature:OnePad", at(4, 10), children=[
        ref("J1", -1.8), pad("1", "thru_hole", "circle", (0, 0), (1.7, 1.7), THT, drill=1.0, net="GND")]))
    b.add(footprint(b, "Feature:Smd", at(4, 16), children=[
        ref("U1", -1.8), pad("1", "smd", "rect", (0, 0), (1.5, 1.5), SMD, net="GND")]))
    b.add(via(b, at(27, 10), 0.8, 0.4, "GND"), stub(b, at(27, 10), F, "GND", -2.0),
          gr_text(b, "DS AND CONSTANT", at(15, 18.5), "F.SilkS", size=1, thickness=0.15))
    return b
