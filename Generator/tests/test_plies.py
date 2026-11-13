"""The plies of the laminate as the board file gives them (kese/s2_collect/plies.py, stackup.py):
every sub-layer of a dielectric is a ply with its own values, the frequency and model of the format
after KiCad 10, the mask's material on each side, what the parameters fill in, the plies given by
hand, a stack-up that cannot be used, the plies fused to one solid or built apart, and that the
plies of a gap add up to the gap.

    python -m pytest tests/test_plies.py           (or:  python tests/test_plies.py)"""
import math

from helpers import run_tests, settings
from kese.core.sexp import parse
from kese.s2_collect.stackup import read_stackup
from kese.s3_resolve.heights import dielectric_z, finished_bands, ply_z
from parameters import P

CU4 = ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"]
SEPARATE = {"Stackup.FUSION_BUILD": "PLIES_SEPARATE"}
TOP = '(layer "F.SilkS" (type "Top Silk Screen")) (layer "F.Mask" (type "Top Solder Mask") (color "Green") ' \
      '(thickness 0.01) (material "LPI") (epsilon_r 3.5) (loss_tangent 0.025)) (layer "F.Cu" (type "copper") (thickness 0.035))'
BOTTOM = '(layer "B.Cu" (type "copper") (thickness 0.035)) (layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01) ' \
         '(material "Dry film") (epsilon_r 3.8)) (layer "B.SilkS" (type "Bottom Silk Screen")) (copper_finish "ENIG")'
IN1, IN2 = ('(layer "In1.Cu" (type "copper") (thickness 0.0152))', '(layer "In2.Cu" (type "copper") (thickness 0.0152))')
P2116, P1080 = ('(thickness 0.124) (material "2116") (epsilon_r 4.16) (loss_tangent 0.02)',
                '(thickness 0.0764 locked) (material "1080") (epsilon_r 3.91) (loss_tangent 0.018)')
CORE = '(layer "dielectric 2" (type "core") (thickness 1.065) (material "FR4 core") (epsilon_r 4.6) (loss_tangent 0.02))'


def gap(n, kind, *plies):
    """A dielectric as KiCad writes it: its sub-layers in one (layer ...), the bare word addsublayer between them."""
    return f'(layer "dielectric {n}" (type "{kind}") ' + " addsublayer ".join(plies) + ")"


REAL = " ".join([TOP, gap(1, "prepreg", P2116, P1080), IN1, CORE, IN2, gap(3, "prepreg", P1080, P2116), BOTTOM])


def stack(text, layers=CU4, thickness=1.6, board="", said=None):
    """The Stackup of (setup (stackup <text>)); the warnings go to the list `said`."""
    setup = parse(f"(setup (stackup {text}))") if text else []
    return read_stackup(setup, list(layers), thickness, (said if said is not None else []).append, board)


def refused(make, said):
    try:
        make()
    except ValueError as e:
        assert said in str(e), f"{e}\n  does not say: {said}"
    else:
        raise AssertionError(f"taken, but should be refused: {said}")


def test_every_sub_layer_is_a_ply_with_its_own_values():
    st = stack(REAL)
    d1, d2, d3 = st.dielectrics
    assert [d.name for d in st.dielectrics] == ["dielectric 1", "dielectric 2", "dielectric 3"]
    assert [(p.name, p.kind, p.material, p.thickness, p.epsilon_r, p.loss_tangent, p.of, p.number, p.count) for p in d1.plies] \
        == [("dielectric 1 ply 1", "prepreg", "2116", 0.124, 4.16, 0.02, "dielectric 1", 1, 2),
            ("dielectric 1 ply 2", "prepreg", "1080", 0.0764, 3.91, 0.018, "dielectric 1", 2, 2)]
    assert [(p.name, p.kind, p.thickness, p.count) for p in d2.plies] == [("dielectric 2", "core", 1.065, 1)]
    assert [p.material for p in d3.plies] == ["1080", "2116"]
    # fused, a gap is one solid of its plies' thickness with its first ply's values
    assert math.isclose(d1.thickness, 0.2004) and (d1.material, d1.epsilon_r, d1.loss_tangent) == ("2116", 4.16, 0.02)
    assert (d3.material, d3.epsilon_r, d3.loss_tangent) == ("1080", 3.91, 0.018)
    assert (d1.above, d1.below, d3.above, d3.below) == ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")
    assert math.isclose(st.laminate_thickness, 1.4962) and st.copper_finish == "ENIG"
    assert not d1.solids                                                  # only built with the plies separate
    assert st.mask_materials == {"F.Mask": {"material": "LPI", "epsilon_r": 3.5, "loss_tangent": 0.025},
                                 "B.Mask": {"material": "Dry film", "epsilon_r": 3.8}}


def test_fused_plies_in_series():
    with settings({"Board.FUSED_PROPERTIES": "series"}):
        d1, d2, _ = stack(REAL).dielectrics
    assert d1.epsilon_r == 4.06101 and d1.material == "2116 + 1080"        # h / er = sum(h_p / er_p)
    # the same from the plies as capacitors in series, each with the complex er (1 - j tan d)
    whole = 0.2004 / (0.124 / (4.16 * (1 - 0.02j)) + 0.0764 / (3.91 * (1 - 0.018j)))
    assert abs(d1.epsilon_r - whole.real) < 1e-4 and abs(d1.loss_tangent - -whole.imag / whole.real) < 1e-6
    assert 0.018 < d1.loss_tangent < 0.02
    assert (d2.epsilon_r, d2.loss_tangent, d2.material) == (4.6, 0.02, "FR4 core")      # one ply: its own


def test_the_frequency_and_the_model_of_a_ply():
    plies = ['(thickness 0.1) (material "A") (epsilon_r 4) (loss_tangent 0.02) (spec_frequency 1e+10) (dielectric_model djordjevic_sarkar)',
             '(thickness 0.1) (material "B") (epsilon_r 4) (loss_tangent 0.02) (spec_frequency 5000000000) (dielectric_model constant)',
             '(thickness 0.1) (material "C") (epsilon_r 4) (loss_tangent 0.02) (spec_frequency 0) (dielectric_model debye)',
             '(thickness 0.1) (material "D") (epsilon_r 4) (loss_tangent 0.02)',
             '(thickness 0.1) (material "E") (epsilon_r 4) (loss_tangent 0.02) (spec_frequency 100) (dielectric_model djordjevic_sarkar)']
    text = " ".join([TOP, gap(1, "prepreg", *plies), BOTTOM])
    said = []
    got = [(p.frequency_hz, p.model) for p in stack(text, ["F.Cu", "B.Cu"], said=said).dielectrics[0].plies]
    assert got == [(1e10, "djordjevic_sarkar"), (5e9, "constant"), (1e9, "constant"), (1e9, "constant"), (100.0, "constant")], got
    assert said == ["warning: stackup layer dielectric 1 ply 3: KESE does not know the dielectric_model 'debye' (it knows "
                    "constant, djordjevic_sarkar): Board.DIELECTRIC_MODEL is used",
                    "warning: dielectric 1 ply 5: the Djordjevic-Sarkar model needs its spec frequency (100 Hz) between "
                    "Board.DS_LOW_FREQUENCY_HZ (1000) and Board.DS_HIGH_FREQUENCY_HZ (1e+12): written with constant values"], said
    with settings({"Board.DIELECTRIC_MODEL": "djordjevic_sarkar", "Board.DEFAULT_SPEC_FREQUENCY_HZ": 2e9}):
        got = [(p.frequency_hz, p.model) for p in stack(text, ["F.Cu", "B.Cu"]).dielectrics[0].plies]
        assert got[2:4] == [(2e9, "djordjevic_sarkar")] * 2, got            # what the file leaves out, or gives wrong
        assert got[:2] == [(1e10, "djordjevic_sarkar"), (5e9, "constant")]  # what it gives stays
    with settings({"Board.USE_STACKUP_SPEC_FREQUENCY": False, "Board.USE_STACKUP_DIELECTRIC_MODEL": False}):
        d = stack(text, ["F.Cu", "B.Cu"]).dielectrics[0]
        assert {(p.frequency_hz, p.model) for p in d.plies} == {(1e9, "constant")} and d.model == "constant"
    d = stack(text, ["F.Cu", "B.Cu"]).dielectrics[0]
    assert (d.frequency_hz, d.model) == (1e10, "djordjevic_sarkar")         # fused: the first ply's


def test_what_the_file_leaves_out_comes_from_the_parameters():
    text = " ".join([TOP, gap(1, "core", '(thickness 0.5) (material "Rogers") (loss_tangent 0.003)', "(thickness 0.5)",
                                  '(thickness 0.51) (material "X") (epsilon_r 3.0)'), BOTTOM])
    with settings({"Board.DEFAULT_EPSILON_R": 4.4, "Board.DEFAULT_LOSS_TANGENT": 0.019, "Board.DEFAULT_DIELECTRIC_MATERIAL": "FR4"}):
        a, b, c = stack(text, ["F.Cu", "B.Cu"]).dielectrics[0].plies
        assert (a.material, a.epsilon_r, a.loss_tangent) == ("Rogers", 4.4, 0.003)
        assert (b.material, b.epsilon_r, b.loss_tangent) == ("FR4", 4.4, 0.019)
        assert (c.material, c.epsilon_r, c.loss_tangent) == ("X", 3.0, 0.019)
        with settings({"Board.USE_STACKUP_EPSILON_R": False, "Board.USE_STACKUP_LOSS_TANGENT": False}):
            assert {(p.epsilon_r, p.loss_tangent) for p in stack(text, ["F.Cu", "B.Cu"]).dielectrics[0].plies} == {(4.4, 0.019)}
    with settings({"Copper.USE_STACKUP_COPPER_THICKNESS": False, "Copper.DEFAULT_TOP_FOIL_MM": 0.07,
                   "Copper.DEFAULT_INNER_FOIL_MM": 0.0175, "Copper.DEFAULT_BOTTOM_FOIL_MM": 0.018}):
        assert stack(REAL).copper_thickness == {"F.Cu": 0.07, "In1.Cu": 0.0175, "In2.Cu": 0.0175, "B.Cu": 0.018}
    with settings({"SolderMask.USE_STACKUP_MASK_THICKNESS": False}):
        assert stack(REAL).mask_thickness is None
    assert stack(REAL).mask_thickness == 0.01


def test_a_stack_up_that_cannot_be_used_is_split_evenly():
    def even(st, n, laminate):
        each = (laminate - sum(st.copper_thickness[l] for l in st.copper_layers[1:-1])) / (n - 1)
        assert len(st.dielectrics) == n - 1 and all(math.isclose(d.thickness, each) for d in st.dielectrics), st.dielectrics
        assert all(len(d.plies) == 1 and d.plies[0].name == d.name == f"dielectric {k + 1}" for k, d in enumerate(st.dielectrics))
        assert math.isclose(st.laminate_thickness, laminate)
    cu8 = ["F.Cu", *[f"In{i}.Cu" for i in range(1, 7)], "B.Cu"]
    with settings({"Copper.DEFAULT_TOP_FOIL_MM": 0.035, "Copper.DEFAULT_INNER_FOIL_MM": 0.035, "Copper.DEFAULT_BOTTOM_FOIL_MM": 0.035}):
        mask = P.SolderMask.MASK_OVER_COPPER_MM
        even(stack("", ["F.Cu", "B.Cu"], 1.6), 2, 1.6 - 0.07 - 2 * mask)                 # no stack-up in the file
        even(stack("", cu8, 2.4), 8, 2.4 - 0.07 - 2 * mask)
        even(stack("", CU4, None), 4, P.Board.DEFAULT_BOARD_THICKNESS_MM - 0.07 - 2 * mask)
    # a gap with no dielectric, and one whose plies have no thickness: the file's total is used
    no_gap = " ".join([TOP, gap(1, "prepreg", P2116), IN1, IN2, gap(3, "prepreg", P2116), BOTTOM])
    even(stack(no_gap), 4, 1.6 - 0.07 - 0.02)
    no_thickness = " ".join([TOP, gap(1, "prepreg", '(material "2116") (epsilon_r 4.16)'), IN1, CORE, IN2, gap(3, "prepreg", P2116), BOTTOM])
    even(stack(no_thickness), 4, 1.6 - 0.07 - 0.02)
    # a ply with no thickness beside one that has it: the gap is that ply's, and built apart the empty one is joined to it
    said = []
    with settings(SEPARATE):
        d = stack(" ".join([TOP, gap(1, "core", '(thickness 1.5) (material "A")', '(material "B")', "(thickness -1)"), BOTTOM]),
                  ["F.Cu", "B.Cu"], said=said).dielectrics[0]
    assert math.isclose(d.thickness, 1.5) and [p.thickness for p in d.plies] == [1.5, 0.0, 0.0]
    assert [(p.name, p.thickness) for p in d.solids] == [("dielectric 1", 1.5)]
    assert said[0] == "warning: stackup layer dielectric 1 ply 3: thickness -1.0 mm is less than 0: read as not given", said
    assert all("joined to dielectric 1 ply 1" in s for s in said[1:]) and len(said) == 3, said


def test_a_ply_that_cannot_be_used_as_given():
    # er 0 cannot be put in series: the gap keeps its first ply's values, with a warning
    zero = '(thickness 0.1) (material "X") (epsilon_r 0) (loss_tangent 0.01)'
    text = " ".join([TOP, gap(1, "prepreg", P2116, zero), IN1, CORE, IN2, gap(3, "prepreg", P1080, P2116), BOTTOM])
    with settings({"Board.FUSED_PROPERTIES": "series"}):
        said = []
        d1, _, d3 = stack(text, said=said).dielectrics
    assert (d1.material, d1.epsilon_r, d1.loss_tangent) == ("2116", 4.16, 0.02) and d3.material == "1080 + 2116"
    assert (d1.fused_properties, d3.fused_properties) == ("first", "series")       # as materials.json then says
    assert said == ["warning: dielectric 1: a ply with er 0 or less cannot be put in series (Board.FUSED_PROPERTIES): "
                    "the gap keeps its first ply's values"], said
    # the model "table" with no table: constant values, with a warning; with a table it stays
    table = REAL.replace('(material "1080")', '(material "1080") (dielectric_model table)', 1)
    said = []
    assert [p.model for p in stack(table, said=said).dielectrics[0].plies] == ["constant", "constant"]
    assert said == ['warning: dielectric 1 ply 2: its dielectric model is "table" but Board.DIELECTRIC_TABLE is empty: '
                    "written with constant values"], said
    with settings({"Board.DIELECTRIC_TABLE": ((1e9, 4.5, 0.02),)}):
        said = []
        assert [p.model for p in stack(table, said=said).dielectrics[0].plies] == ["constant", "table"] and not said
    # a model KESE does not know, in any case of letters, and one left empty: the parameters' model
    for given, model, warned in (("Djordjevic_Sarkar", "djordjevic_sarkar", 0), ("debye", "constant", 1), ("", "constant", 0)):
        said = []
        text = REAL.replace('(material "1080")', f'(material "1080") (dielectric_model {given})', 1)
        assert stack(text, said=said).dielectrics[0].plies[1].model == model, given
        assert said == ["warning: stackup layer dielectric 1 ply 2: KESE does not know the dielectric_model 'debye' (it knows "
                        "constant, djordjevic_sarkar): Board.DIELECTRIC_MODEL is used"][:warned], said
    # a value left empty is as one left out; a number left empty is refused as KiCad refuses it
    empty = REAL.replace('(material "1080")', "(material)", 1).replace('(type "prepreg")', "(type)", 1).replace('(color "Green")', "(color)")
    d1 = stack(empty).dielectrics[0]
    assert (d1.kind, d1.plies[1].material) == (P.Board.DEFAULT_DIELECTRIC_TYPE, P.Board.DEFAULT_DIELECTRIC_MATERIAL)
    for full, bare in (("(epsilon_r 4.16)", "(epsilon_r)"), ("(thickness 0.035)", "(thickness)"),      # a ply, the top copper
                       ("(thickness 0.01)", "(thickness)")):                                         # and the top mask
        try:
            stack(REAL.replace(full, bare, 1))
        except ValueError as e:
            assert str(e).startswith(f"nothing where a number belongs, in {bare[:-1]} ...)"), e
        else:
            raise AssertionError(f"{bare} with nothing in it was taken")
    # a ply of no thickness is joined to its neighbour whatever Board.PLY_MIN_THICKNESS_MM is
    none = '(thickness 0) (material "Film") (epsilon_r 3.2) (loss_tangent 0.02)'
    text = " ".join([TOP, gap(1, "prepreg", P2116, none), IN1, CORE, IN2, gap(3, "prepreg", P1080, P2116), BOTTOM])
    with settings({**SEPARATE, "Board.PLY_MIN_THICKNESS_MM": 0}):
        said = []
        d1 = stack(text, said=said).dielectrics[0]
    assert [(p.name, p.thickness, p.holds) for p in d1.solids] == [("dielectric 1", 0.124, ["dielectric 1 ply 1", "dielectric 1 ply 2"])]
    assert said == ["warning: dielectric 1 ply 2 has no thickness: joined to dielectric 1 ply 1"], said


def test_several_dielectrics_in_one_gap_are_one():
    text = " ".join([TOP, '(layer "dielectric 1" (type "prepreg") (thickness 0.1) (material "A") (epsilon_r 4.0))',
                     '(layer "dielectric 2" (type "core") (thickness 0.3) (material "B") (epsilon_r 4.5) addsublayer (thickness 0.2) (material "C"))',
                     BOTTOM])
    d, = stack(text, ["F.Cu", "B.Cu"]).dielectrics
    assert d.name == "dielectric 1 + dielectric 2" and math.isclose(d.thickness, 0.6) and (d.kind, d.material) == ("prepreg", "A")
    assert [(p.name, p.kind, p.of, p.number, p.count) for p in d.plies] == [
        ("dielectric 1", "prepreg", "dielectric 1", 1, 3), ("dielectric 2 ply 1", "core", "dielectric 2", 2, 3),
        ("dielectric 2 ply 2", "core", "dielectric 2", 3, 3)]


def test_plies_given_by_hand():
    hand = {("F.Cu", "In1.Cu"): [
        {"type": "prepreg", "thickness_mm": 0.06, "material": "106", "epsilon_r": 3.7, "loss_tangent": 0.021},
        {"type": "prepreg", "thickness_mm": 0.11, "material": "3313", "epsilon_r": 4.1, "loss_tangent": 0.019,
         "frequency_hz": 2e9, "model": "djordjevic_sarkar"}]}
    with settings({"Board.PLIES_BY_HAND": {"mine": hand}}):
        d1, d2, d3 = stack(REAL, board="mine").dielectrics
        assert [(p.name, p.material, p.thickness, p.frequency_hz, p.model) for p in d1.plies] == [
            ("dielectric 1 ply 1", "106", 0.06, 1e9, "constant"), ("dielectric 1 ply 2", "3313", 0.11, 2e9, "djordjevic_sarkar")]
        assert math.isclose(d1.thickness, 0.17) and [p.material for p in d3.plies] == ["1080", "2116"]   # the others: the file's
        assert math.isclose(d2.thickness, 1.065)
        assert [p.material for p in stack(REAL, board="another").dielectrics[0].plies] == ["2116", "1080"]
        # a board with no stack-up: the gap by hand keeps its plies, the others share the rest
        st = stack("", CU4, 1.6, board="mine")
        rest = (st.laminate_thickness - sum(st.copper_thickness[l] for l in CU4[1:-1]) - 0.17) / 2
        assert [p.material for p in st.dielectrics[0].plies] == ["106", "3313"]
        assert all(math.isclose(d.thickness, rest) and len(d.plies) == 1 for d in st.dielectrics[1:])
    good = hand[("F.Cu", "In1.Cu")][0]
    where = "Board.PLIES_BY_HAND['mine'][('F.Cu', 'In1.Cu')]"
    for wrong, said in (
            ({("F.Cu", "In2.Cu"): [good]}, "('F.Cu', 'In2.Cu') is not two neighbouring copper layers of this board, the upper one "
                                           "first; its gaps are ('F.Cu', 'In1.Cu'), ('In1.Cu', 'In2.Cu'), ('In2.Cu', 'B.Cu')"),
            ({("In1.Cu", "F.Cu"): [good]}, "is not two neighbouring copper layers"),
            ({("F.Cu", "In1.Cu"): []}, f"{where} must be a list of plies, top to bottom, not []"),
            ({("F.Cu", "In1.Cu"): good}, f"{where} must be a list of plies"),
            ({("F.Cu", "In1.Cu"): ["2116"]}, f"{where}[0] must be a ply, as"),
            ({("F.Cu", "In1.Cu"): [{k: v for k, v in good.items() if k != "epsilon_r"}]}, f"{where}[0] has no 'epsilon_r': a ply takes"),
            ({("F.Cu", "In1.Cu"): [{**good, "thicknes": 1}]}, f"{where}[0] has 'thicknes', which a ply does not take"),
            ({("F.Cu", "In1.Cu"): [{**good, "thickness_mm": "0.1"}]}, f"{where}[0]: 'thickness_mm' must be a number, not '0.1'"),
            ({("F.Cu", "In1.Cu"): [{**good, "material": 2116}]}, f"{where}[0]: 'material' must be text, in quotes, not 2116"),
            ({("F.Cu", "In1.Cu"): [good, {**good, "thickness_mm": 0}]}, f"{where}[1]: 'thickness_mm' must be more than 0"),
            ({("F.Cu", "In1.Cu"): [{**good, "type": "resin"}]}, f"{where}[0]: 'type' must be 'core' or 'prepreg'"),
            ({("F.Cu", "In1.Cu"): [{**good, "epsilon_r": 0.5}]}, f"{where}[0]: 'epsilon_r' must be 1 or more"),
            ({("F.Cu", "In1.Cu"): [{**good, "loss_tangent": -0.1}]}, f"{where}[0]: 'loss_tangent' must be 0 or more"),
            ({("F.Cu", "In1.Cu"): [{**good, "frequency_hz": 0}]}, f"{where}[0]: 'frequency_hz' must be more than 0"),
            ({("F.Cu", "In1.Cu"): [{**good, "model": "debye"}]}, f"{where}[0]: 'model' must be one of 'constant', 'djordjevic_sarkar', 'table'"),
            ({("F.Cu", "In1.Cu"): [{**good, "model": "table"}]}, f"{where}[0]: 'model' may be 'table' only when Board.DIELECTRIC_TABLE has rows"),
            ([good], "Board.PLIES_BY_HAND['mine'] must be {(copper above, copper below): [plies]}")):
        with settings({"Board.PLIES_BY_HAND": {"mine": wrong}}):
            refused(lambda: stack(REAL, board="mine"), said)


def test_plies_built_apart_thin_ones_and_equal_ones_joined():
    names = lambda d: [(p.name, round(p.thickness, 6)) for p in d.solids]
    equal = '(thickness 0.1) (material "7628") (epsilon_r 4.4) (loss_tangent 0.017)'
    thin = '(thickness 0.0005) (material "Film") (epsilon_r 3.2) (loss_tangent 0.02)'
    text = " ".join([TOP, gap(1, "prepreg", equal, equal, P2116, equal), IN1, gap(2, "core", '(thickness 0.3) (material "Core")', thin),
                     IN2, gap(3, "prepreg", equal, equal, equal), BOTTOM])
    with settings(SEPARATE):
        said = []
        d1, d2, d3 = stack(text, said=said).dielectrics
        assert names(d1) == [("dielectric 1 ply 1", 0.1), ("dielectric 1 ply 2", 0.1), ("dielectric 1 ply 3", 0.124), ("dielectric 1 ply 4", 0.1)]
        assert names(d2) == [("dielectric 2", 0.3005)] and d2.solids[0].material == "Core"       # the thin ply is in its neighbour
        assert said == ["warning: dielectric 2 ply 2 is 0.0005 mm thick, less than Board.PLY_MIN_THICKNESS_MM (0.001 mm): "
                        "joined to dielectric 2 ply 1"], said
        assert [p.thickness for p in d2.plies] == [0.3, 0.0005]                                   # the file's plies stay as read
        with settings({"Board.PLY_MIN_THICKNESS_MM": 0}):
            assert names(stack(text).dielectrics[1]) == [("dielectric 2 ply 1", 0.3), ("dielectric 2 ply 2", 0.0005)]
        with settings({"Board.PLY_MIN_THICKNESS_MM": 0.11}):       # the thinnest first, each to its thicker neighbour
            said = []
            d1, _, d3 = stack(text, said=said).dielectrics
            assert names(d1) == [("dielectric 1 ply 1-2", 0.2), ("dielectric 1 ply 3-4", 0.224)]
            assert [p.holds for p in d1.solids] == [["dielectric 1 ply 1", "dielectric 1 ply 2"], ["dielectric 1 ply 3", "dielectric 1 ply 4"]]
            assert d1.solids[1].material == "2116" and names(d3) == [("dielectric 3", 0.3)]      # the thicker ply's values
            assert len(said) == 2 + 1 + 2, said
        with settings({"Board.JOIN_EQUAL_PLIES": True}):
            d1, _, d3 = stack(text).dielectrics
            assert names(d1) == [("dielectric 1 ply 1-2", 0.2), ("dielectric 1 ply 3", 0.124), ("dielectric 1 ply 4", 0.1)]
            assert names(d3) == [("dielectric 3", 0.3)]
    with settings({"Board.JOIN_EQUAL_PLIES": True}):
        assert not stack(text).dielectrics[0].solids                 # fused: nothing is built ply by ply


def test_the_report_lists_the_laminate_as_it_is_built():
    from kese.s9_report.report import laminate_lines
    thin = '(thickness 0.0006) (material "Film") (epsilon_r 3.2) (loss_tangent 0.02)'
    text = " ".join([TOP, gap(1, "prepreg", P2116, P1080), IN1, gap(2, "core", '(thickness 1.066) (material "FR4 core")', thin),
                     IN2, gap(3, "prepreg", P1080, P2116), BOTTOM])
    st = stack(text)
    finished_bands(st)
    assert laminate_lines(st) == [
        "  dielectric 1             prepreg  2116       0.2004 mm  er 4.16  tan d 0.02   z +0.5485 .. +0.7489",
        "    fused from dielectric 1 ply 1: prepreg 2116 0.1240 mm  er 4.16  tan d 0.02",
        "    fused from dielectric 1 ply 2: prepreg 1080 0.0764 mm  er 3.91  tan d 0.018",
        "  dielectric 2             core     FR4 core   1.0666 mm  er 4.5  tan d 0.02   z -0.5333 .. +0.5333",
        "    fused from dielectric 2 ply 1: core FR4 core 1.0660 mm  er 4.5  tan d 0.02",
        "    fused from dielectric 2 ply 2: core Film 0.0006 mm  er 3.2  tan d 0.02",
        "  dielectric 3             prepreg  1080       0.2004 mm  er 3.91  tan d 0.018   z -0.7489 .. -0.5485",
        "    fused from dielectric 3 ply 1: prepreg 1080 0.0764 mm  er 3.91  tan d 0.018",
        "    fused from dielectric 3 ply 2: prepreg 2116 0.1240 mm  er 4.16  tan d 0.02"], laminate_lines(st)
    with settings(SEPARATE):
        st = stack(text)
        finished_bands(st)
        lines = laminate_lines(st)
    assert lines == [
        "  dielectric 1 ply 1       prepreg  2116       0.1240 mm  er 4.16  tan d 0.02   z +0.6249 .. +0.7489",
        "  dielectric 1 ply 2       prepreg  1080       0.0764 mm  er 3.91  tan d 0.018   z +0.5485 .. +0.6249",
        "  resin In1.Cu             resin    resin      0.0152 mm  er 3.5  tan d 0.02   z +0.5333 .. +0.5485   (flowed from dielectric 1 ply 2)",
        "  dielectric 2             core     FR4 core   1.0666 mm  er 4.5  tan d 0.02   z -0.5333 .. +0.5333"
        "   (holds dielectric 2 ply 1, dielectric 2 ply 2)",
        "  resin In2.Cu             resin    resin      0.0152 mm  er 3.5  tan d 0.02   z -0.5485 .. -0.5333   (flowed from dielectric 3 ply 1)",
        "  dielectric 3 ply 1       prepreg  1080       0.0764 mm  er 3.91  tan d 0.018   z -0.6249 .. -0.5485",
        "  dielectric 3 ply 2       prepreg  2116       0.1240 mm  er 4.16  tan d 0.02   z -0.7489 .. -0.6249"], lines


def test_the_plies_of_a_gap_add_up_to_the_gap():
    equal = '(thickness 0.1) (material "7628") (epsilon_r 4.4) (loss_tangent 0.017)'
    third = '(thickness 0.033333) (material "106") (epsilon_r 3.7)'
    text = " ".join([TOP, gap(1, "prepreg", third, third, third, P1080), IN1, CORE, IN2, gap(3, "prepreg", equal, P2116, equal), BOTTOM])
    for changes in ({}, {"Board.BOARD_THICKNESS_MM": 1.0}, {"Board.JOIN_EQUAL_PLIES": True},
                    {"Copper.TOP_PLATING_ADDED_MM": 0.02, "Copper.BOTTOM_PLATING_ADDED_MM": 0.01}):
        with settings({**SEPARATE, **changes}):
            st = stack(text)
            finished_bands(st)
            z = st.half
            for i, d in enumerate(st.dielectrics):
                lo, hi = dielectric_z(st, i)
                built = ply_z(st, i)
                assert built[0][2] == hi == z and built[-1][1] == lo, changes          # exactly the gap's faces
                assert all(a[1] == b[2] for a, b in zip(built, built[1:]))                # each ply on the next
                assert all(math.isclose(top - bottom, ply.thickness, abs_tol=1e-12) for ply, bottom, top in built)
                assert math.isclose(sum(ply.thickness for ply in d.solids), d.thickness)
                assert math.isclose(sum(ply.thickness for ply in d.plies), d.thickness)
                z = lo - (st.copper_thickness[d.below] if i < len(st.dielectrics) - 1 else 0)
            assert math.isclose(z, -st.half) and math.isclose(2 * st.half, changes.get("Board.BOARD_THICKNESS_MM", st.laminate_thickness))


if __name__ == "__main__":
    run_tests(__file__)
