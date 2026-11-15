"""Colours (kese/s5_materials/materials.py): every part takes its colour from the Color section of
its element's file in parameters/PCB_elements/.  A colour name of KiCad's Board Setup is looked up in
the tables of SolderMask.py and SilkScreen.py, a user-defined colour (#RRGGBBAA, or #RRGGBB) is used
as it is with the opacity of the part's colour setting, lightened toward white for the mask over
copper in visual mode, and anything else keeps the file's colour with a warning.  Takes a moment.

    python -m pytest tests/test_colors.py           (or:  python tests/test_colors.py)"""
from types import SimpleNamespace

from helpers import run_tests, settings
from kese.s5_materials.materials import looks, material_for, unknown_colors
from parameters import P

STACKUP = SimpleNamespace(colors={"F.Mask": "#1B5E20D4", "B.Mask": "Green", "F.SilkS": "#aabbcc",
                                  "B.SilkS": "Teal", "dielectric 1": "FR4 natural"})
M, S = P.SolderMask, P.SilkScreen


def look(part, role, mode, props=None):
    m = material_for(part, role, props or {}, STACKUP, mode)
    return m["color"], m["alpha"]


def test_user_defined_colours():
    with settings({"SolderMask.USE_STACKUP_MASK_COLOR": True, "SilkScreen.USE_STACKUP_SILK_COLOR": True,
                   "SolderMask.VISUAL_MASK_OPAQUE": True, "SolderMask.USER_MASK_OVER_COPPER_LIGHTEN": 0.15}):
        alpha = M.TOP_MASK_COLOR["alpha"]
        assert look("Top Solder Mask", "mask", "simulation") == ("#1B5E20", alpha)     # the file's AA is not used
        assert look("Top Solder Mask", "mask", "visual") == ("#1B5E20", 1.0)
        # 15 % toward white: 0x1B + 0.15 * (255 - 0x1B) = 61.2 -> 0x3D, 0x5E -> 0x76, 0x20 -> 0x41
        assert look("Top Mask over Copper", "mask_over_copper", "visual") == ("#3D7641", 1.0)
        assert look("Top Silkscreen", "silk", "simulation") == ("#AABBCC", S.TOP_SILK_COLOR["alpha"])


def test_colour_names_and_unknown_values():
    with settings({"SolderMask.USE_STACKUP_MASK_COLOR": True, "SilkScreen.USE_STACKUP_SILK_COLOR": True}):
        assert look("Bottom Solder Mask", "mask", "simulation")[0] == M.STACKUP_MASK_COLORS["green"]
        assert look("Bottom Mask over Copper", "mask_over_copper", "visual")[0] == M.STACKUP_MASK_OVER_COPPER_COLORS["green"]
        assert look("Bottom Silkscreen", "silk", "simulation")[0] == S.BOTTOM_SILK_COLOR["color"]
        assert unknown_colors(STACKUP) == [("B.SilkS", "Teal")]


def test_stackup_colours_off():
    # the mask's and the ink's stack-up colours are honoured apart (one setting, Color.USE_STACKUP_COLORS, before)
    with settings({"SolderMask.USE_STACKUP_MASK_COLOR": False}):
        assert look("Top Solder Mask", "mask", "simulation")[0] == M.TOP_MASK_COLOR["color"]
        assert look("Top Silkscreen", "silk", "simulation")[0] == "#AABBCC"
        assert unknown_colors(STACKUP) == [("B.SilkS", "Teal")]
    with settings({"SilkScreen.USE_STACKUP_SILK_COLOR": False}):
        assert look("Top Silkscreen", "silk", "simulation")[0] == S.TOP_SILK_COLOR["color"]
        assert look("Top Solder Mask", "mask", "simulation")[0] == "#1B5E20"
        assert unknown_colors(STACKUP) == []
    with settings({"SolderMask.USE_STACKUP_MASK_COLOR": True, "SilkScreen.USE_STACKUP_SILK_COLOR": True}):
        P.override("Color.USE_STACKUP_COLORS", False)                   # the old name sets both
        assert not M.USE_STACKUP_MASK_COLOR and not S.USE_STACKUP_SILK_COLOR


def test_every_part_takes_the_colour_of_its_file():
    B, C = P.Board, P.Copper
    for part, role, mode, props, setting in (
            ("Board_dielectric 1", "board", "simulation", {"kind": "core"}, B.CORE_COLOR),
            ("Board_dielectric 2", "board", "simulation", {"kind": "prepreg"}, B.PREPREG_COLOR),
            ("Board_resin In1.Cu", "board", "simulation", {"kind": "resin"}, B.RESIN_COLOR),
            ("Board", "board", "simulation", {}, B.BOARD_COLOR),
            ("Copper_GND", "copper", "simulation", {}, C.COPPER_COLOR),
            ("Plating", "plating", "simulation", {}, C.PLATING_COLOR),
            ("Copper_GND", "copper", "visual", {}, C.EXPOSED_COPPER_COLOR),
            ("Via Resin", "via_resin", "simulation", {}, C.VIA_RESIN_COLOR),
            ("Bottom Mask over Copper", "mask_over_copper", "simulation", {}, M.BOTTOM_MASK_OVER_COPPER_COLOR),
            ("Top Finish Gold", "finish", "simulation", {"metal": "Gold"}, P.Finish.FINISH_COLORS["Gold"]),
            ("Top Finish Unobtainium", "finish", "simulation", {"metal": "Unobtainium"}, B.BOARD_COLOR)):
        with settings({"SolderMask.USE_STACKUP_MASK_COLOR": False}):
            assert look(part, role, mode, props) == (setting["color"], setting["alpha"]), part
    with settings({"Board.DIELECTRIC_GROUPING": "merged"}):               # one laminate solid: the board's colour
        assert look("Board", "board", "simulation", {"kind": "core"})[0] == B.BOARD_COLOR["color"]
    # a look is a colour, an opacity, how metallic and how rough
    assert all(set(m) == {"color", "alpha", "metallic", "roughness"} for m in looks().values())


if __name__ == "__main__":
    run_tests(__file__)
