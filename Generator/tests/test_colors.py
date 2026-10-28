"""Stack-up colours (kese/s5_materials/materials.py): a colour name of KiCad's Board Setup is looked
up in the tables of parameters/color.py, a user-defined colour (#RRGGBBAA, or #RRGGBB) is used as
it is with the opacity of MATERIALS, lightened toward white for the mask over copper in visual mode,
and anything else keeps the MATERIALS colour with a warning.  Takes a moment.

    python -m pytest tests/test_colors.py           (or:  python tests/test_colors.py)"""
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.s5_materials.materials import material_for, unknown_colors  # noqa: E402
from parameters import P  # noqa: E402

STACKUP = SimpleNamespace(colors={"F.Mask": "#1B5E20D4", "B.Mask": "Green", "F.SilkS": "#aabbcc",
                                  "B.SilkS": "Teal", "dielectric 1": "FR4 natural"})


@contextmanager
def color_settings(**values):
    """parameters/color.py with these values for the block, put back after it."""
    saved = {name: getattr(P.Color, name) for name in values}
    for name, value in values.items():
        P.override(f"Color.{name}", value)
    try:
        yield P.Color
    finally:
        for name, value in saved.items():
            P.override(f"Color.{name}", value)


def look(part, role, mode):
    m = material_for(part, role, {}, STACKUP, mode)
    return m["color"], m["alpha"]


def test_user_defined_colours():
    with color_settings(USE_STACKUP_COLORS=True, VISUAL_MASK_OPAQUE=True, USER_MASK_OVER_COPPER_LIGHTEN=0.15) as C:
        alpha = C.MATERIALS["Top Solder Mask"]["alpha"]
        assert look("Top Solder Mask", "mask", "simulation") == ("#1B5E20", alpha)     # the file's AA is not used
        assert look("Top Solder Mask", "mask", "visual") == ("#1B5E20", 1.0)
        # 15 % toward white: 0x1B + 0.15 * (255 - 0x1B) = 61.2 -> 0x3D, 0x5E -> 0x76, 0x20 -> 0x41
        assert look("Top Mask over Copper", "mask_over_copper", "visual") == ("#3D7641", 1.0)
        assert look("Top Silkscreen", "silk", "simulation") == ("#AABBCC", C.MATERIALS["Top Silkscreen"]["alpha"])


def test_colour_names_and_unknown_values():
    with color_settings(USE_STACKUP_COLORS=True) as C:
        assert look("Bottom Solder Mask", "mask", "simulation")[0] == C.STACKUP_MASK_COLORS["green"]
        assert look("Bottom Mask over Copper", "mask_over_copper", "visual")[0] == C.STACKUP_MASK_OVER_COPPER_COLORS["green"]
        assert look("Bottom Silkscreen", "silk", "simulation")[0] == C.MATERIALS["Bottom Silkscreen"]["color"]
        assert unknown_colors(STACKUP) == [("B.SilkS", "Teal")]


def test_stackup_colours_off():
    with color_settings(USE_STACKUP_COLORS=False) as C:
        assert look("Top Solder Mask", "mask", "simulation")[0] == C.MATERIALS["Top Solder Mask"]["color"]


if __name__ == "__main__":
    test_user_defined_colours()
    test_colour_names_and_unknown_values()
    test_stackup_colours_off()
    print("ok")
