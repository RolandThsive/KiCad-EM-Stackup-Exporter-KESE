"""The colour boxes of the wiki: one per hex colour of the Color sections of the element files in
Generator/parameters/PCB_elements/ (Board.py, Copper.py, Finish.py, SolderMask.py, SilkScreen.py), a filled
square with a thin grey border that shows on GitHub's light and dark themes, as VS Code draws
next to a colour code.  A lossless WebP of 24 x 24 px, shown at 12 x 12 so it stays sharp on
high-density screens.

    python tools/make_swatches.py      (from Generator/, after a colour in one of those files changed)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

GENERATOR = Path(__file__).resolve().parents[1]
OUT = GENERATOR.parent / "docs" / "images" / "Colorizing" / "ColorSwatches"
sys.path.insert(0, str(GENERATOR))
from parameters import P  # noqa: E402

SIZE, BORDER, EDGE = 24, 2, (110, 119, 129)        # GitHub's muted grey #6E7781
EXAMPLES = ("#1B5E20", "#3D7641")                 # Colorizing's user-defined colour, and over copper


def colours():
    """Every hex colour of the element files: each ..._COLOR setting, the finish metals' colours and
    the tables of stack-up colour names."""
    found = set(EXAMPLES)
    for module in (P.Board, P.Copper, P.Finish, P.SolderMask, P.SilkScreen):
        for name in P.names(module.__name__.rsplit(".", 1)[-1]):
            value = getattr(module, name)
            if name.endswith("_COLOR") and isinstance(value, dict):       # a look (USE_STACKUP_MASK_COLOR is a switch)
                found.add(value["color"].upper())
            elif name.endswith("_COLORS"):                    # {metal: a look} or {colour name: hex}
                found |= {(v["color"] if isinstance(v, dict) else v).upper() for v in value.values() if v}
    return sorted(found)


def swatch(hexcode, path):
    rgb = tuple(int(hexcode[i:i + 2], 16) for i in (1, 3, 5))
    im = Image.new("RGB", (SIZE, SIZE), EDGE)
    ImageDraw.Draw(im).rectangle([BORDER, BORDER, SIZE - 1 - BORDER, SIZE - 1 - BORDER], fill=rgb)
    im.save(path, "WEBP", lossless=True, quality=100, method=6)


if __name__ == "__main__":
    found = colours()
    for h in found:
        swatch(h, OUT / f"{h[1:]}.webp")
    print(len(found), "colour boxes in", OUT)
