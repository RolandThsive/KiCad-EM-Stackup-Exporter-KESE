"""Stroke-font text, laid out the way KiCad lays it out.

Default font: KiCad's own "newstroke" (kese/assets/fonts/kicad_newstroke.json.gz).  Custom fonts:
this JSON format or a Hershey .jhf file, named in Silkscreen.FONT_FILE.

Glyph coordinates are fractions of the text height, y DOWN (KiCad's convention), baseline near 0.

The layout below is derived from KiCad's common/font/font.cpp and common/font/stroke_font.cpp:
Copyright (C) 2021 Ola Rinta-Koski; Copyright (C) 2012 Torsten Hueter; Copyright (C) 2013 CERN;
Copyright The KiCad Developers, see AUTHORS.txt for contributors.  GPL-2.0-or-later; KESE as a
whole is GPL-3.0-or-later.  The original headers are in licenses/ at the top of the repository;
see NOTICE.md."""
import gzip
import json
import math
from pathlib import Path

import shapely

from kese.core.shapes2d import EMPTY
from parameters import P

FONTS_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"
DEFAULT_FONT = "kicad_newstroke.json.gz"

_font = None
_font_note = ""


def _load_json(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def _load_jhf(path):
    """Hershey .jhf: 5-char id, 3-char vertex count, then coordinate pairs; ' R' = pen up."""
    glyphs = []
    text = Path(path).read_text(encoding="latin-1")
    SCALE, BASE = 1 / 21.0, 9           # Hershey units: ~21 per text height, baseline at +9
    for line in text.splitlines():
        if len(line) < 10:
            continue
        n = int(line[5:8])
        data = line[8:8 + 2 * n]
        x0, x1 = (ord(data[0]) - ord("R")) * SCALE, (ord(data[1]) - ord("R")) * SCALE
        strokes, pen = [], []
        for i in range(2, len(data) - 1, 2):
            a, b = data[i], data[i + 1]
            if a == " " and b == "R":
                if pen:
                    strokes.append(pen)
                pen = []
            else:
                pen.append([(ord(a) - ord("R")) * SCALE - x0, (ord(b) - ord("R") - BASE) * SCALE])
        if pen:
            strokes.append(pen)
        glyphs.append({"w": x1 - x0, "s": strokes})
    return {"name": Path(path).name, "first_codepoint": 32, "glyphs": glyphs}


def load():
    """Load the font once; returns (font dict, note for the report)."""
    global _font, _font_note
    if _font is not None:
        return _font, _font_note
    S = P.Silkscreen
    chosen = FONTS_DIR / DEFAULT_FONT
    note = f"font: KiCad newstroke ({DEFAULT_FONT})"
    if S.FONT_FILE:
        custom = FONTS_DIR / S.FONT_FILE
        if custom.exists():
            chosen, note = custom, f"font: custom {S.FONT_FILE}"
        else:
            note = f"font: {S.FONT_FILE} not found in kese/assets/fonts, using KiCad newstroke"
    _font = _load_jhf(chosen) if chosen.suffix.lower() == ".jhf" else _load_json(chosen)
    _font_note = note
    return _font, _font_note


def _glyph(f, ch):
    idx = ord(ch) - f.get("first_codepoint", 32)
    g = f["glyphs"]
    if 0 <= idx < len(g):
        return g[idx]
    return g[ord("?") - f.get("first_codepoint", 32)]


def render(text, anchor, angle_deg, size_h, size_w, thickness, justify=(), mirror=False,
           italic=False):
    """Text as a shapely polygon in board coordinates (mm, Y down).

    Follows KiCad's STROKE_FONT / FONT::getLinePositions layout: glyph advance from the glyph
    width, interline pitch, H/V justification with KiCad's offsets.  A line is as wide as its pen's
    advance, the spacing after the last glyph included (FONT::getLinePositions measures it so; only
    the bounding box leaves that spacing out), and a centred or right-justified line does not get
    the left offset T / 1.52."""
    S = P.Silkscreen
    f, _ = load()
    if not text.strip():
        return EMPTY
    space_w = f["glyphs"][0]["w"]
    interline = size_h * S.INTERLINE_PITCH * S.INTERLINE_LEGACY_FACTOR      # KiCad 7 to 10 plot no (line_spacing)
    tilt = S.ITALIC_TILT if italic else 0.0
    lines = text.split("\n")

    # layout each line in local coordinates (x right, y down), origin = line start on the baseline
    laid, widths = [], []
    for line in lines:
        cursor, strokes, count = 0.0, [], 0
        for ch in line:
            if ch == " ":
                cursor += size_w * space_w
            elif ch == "\t":                 # to KiCad's next tab stop: every fourth column of width W
                count = (count // 4 + 1) * 4 - 1
                stop = size_w * (count + space_w)
                while stop <= cursor:
                    count += 4
                    stop += size_w * 4
                cursor = stop
            else:
                g = _glyph(f, ch)
                for st in g["s"]:
                    strokes.append([(cursor + (x - y * tilt) * size_w, y * size_h) for x, y in st])
                cursor += g["w"] * size_w
            count += 1
        widths.append(cursor)
        laid.append(strokes)

    n = len(lines)
    height = size_h * 1.17 + (n - 1) * interline          # KiCad's block height
    off_x, off_y = thickness / 1.52, size_h - thickness * 0.052   # KiCad stroke-font offsets
    if "top" in justify:
        pass
    elif "bottom" in justify:
        off_y -= height
    else:
        off_y -= height / 2
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    segs = []
    for i, strokes in enumerate(laid):
        if "left" in justify:
            lx = off_x
        elif "right" in justify:
            lx = -(widths[i] + off_x)
        else:
            lx = -widths[i] / 2
        ly = off_y + i * interline
        for st in strokes:
            pts = []
            for x, y in st:
                x, y = x + lx, y + ly
                if mirror:
                    x = -x
                pts.append((anchor[0] + x * c + y * s, anchor[1] - x * s + y * c))
            if len(pts) >= 2:
                segs.append(pts)
    if not segs:
        return EMPTY
    return shapely.MultiLineString(segs).buffer(thickness / 2, quad_segs=S.TEXT_STROKE_QUAD_SEGS)
