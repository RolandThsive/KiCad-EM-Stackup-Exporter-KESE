"""The colour boxes of the wiki: one per hex colour of Generator/parameters/color.py, a filled
square with a thin grey border that shows on GitHub's light and dark themes, as VS Code draws
next to a colour code.  A lossless WebP of 24 x 24 px, shown at 12 x 12 so it stays sharp on
high-density screens.

    python tools/make_swatches.py      (from Generator/, after a colour in parameters/color.py changed)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

GENERATOR = Path(__file__).resolve().parents[1]
OUT = GENERATOR.parent / "docs" / "ColorSwatches"
sys.path.insert(0, str(GENERATOR))
from parameters import color as C  # noqa: E402

SIZE, BORDER, EDGE = 24, 2, (110, 119, 129)        # GitHub's muted grey #6E7781
EXAMPLES = ("#1B5E20", "#3D7641")                 # Colorizing's user-defined colour, and over copper


def colours():
    found = {m["color"].upper() for m in C.MATERIALS.values()} | set(EXAMPLES)
    for table in (C.STACKUP_MASK_COLORS, C.STACKUP_SILK_COLORS, C.STACKUP_MASK_OVER_COPPER_COLORS):
        found |= {h.upper() for h in table.values() if h}
    return sorted(found)


def swatch(hexcode, path):
    rgb = tuple(int(hexcode[i:i + 2], 16) for i in (1, 3, 5))
    im = Image.new("RGB", (SIZE, SIZE), EDGE)
    ImageDraw.Draw(im).rectangle([BORDER, BORDER, SIZE - 1 - BORDER, SIZE - 1 - BORDER], fill=rgb)
    im.save(path, "WEBP", lossless=True, quality=100, method=6)


if __name__ == "__main__":
    for h in colours():
        swatch(h, OUT / f"{h[1:]}.webp")
    print(len(colours()), "colour boxes in", OUT)
