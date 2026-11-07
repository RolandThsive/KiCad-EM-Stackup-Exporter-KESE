"""Stroke-font files: which one Silkscreen.FONT_FILE picks, and reading it.

A font is a dict: the header (name, units, first_codepoint, line pitch, italic tilt) and "glyphs",
the glyphs from first_codepoint on, each {"w": advance, "s": strokes}.  Three layouts are read:

- JSON Lines, gzipped or not: the header on the first line, then one glyph per line.  KiCad's
  newstroke (kese/assets/fonts/kicad_newstroke.json.gz) is stored so.  Each glyph is parsed the
  first time it is asked for: a board draws a few dozen of newstroke's 65,487, and parsing them all
  takes about 0.5 s and holds 1.26 million objects that Python then frees, one by one, as it exits.
- One JSON document, the font whole, gzipped or not: custom fonts made for this project.
- A Hershey .jhf file.

tools/font_lines.py writes a font of the second layout in the first."""
import gzip
import json
import operator
from pathlib import Path

from parameters import P

FONTS_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"
DEFAULT_FONT = "kicad_newstroke.json.gz"

_fonts = {}


class Glyphs:
    """A font's glyphs, one JSON document per line, each parsed the first time it is asked for."""

    def __init__(self, lines, name, first_line):
        self._lines, self._parsed = lines, {}
        self._name, self._first_line = name, first_line

    def __len__(self):
        return len(self._lines)

    def __getitem__(self, i):
        i = operator.index(i)
        if i < 0:
            i += len(self._lines)
        g = self._parsed.get(i)
        if g is None:
            if not 0 <= i < len(self._lines):
                raise IndexError(f"{self._name}: no glyph {i}")
            try:
                g = json.loads(self._lines[i])
            except ValueError as e:
                raise ValueError(f"font {self._name}, line {i + self._first_line}: {e}") from None
            self._parsed[i] = g
        return g


def read_json(path):
    """A font in this project's JSON, in either layout (the module's docstring)."""
    path = Path(path)
    data = path.read_bytes()
    if path.suffix == ".gz":
        data = gzip.decompress(data)
    lines = data.split(b"\n")
    while lines and not lines[-1].strip():
        lines.pop()
    try:
        head = json.loads(lines[0]) if lines else None
    except ValueError:
        head = None                                   # the first line of a document over several lines
    if isinstance(head, dict) and "glyphs" not in head:
        head["glyphs"] = Glyphs(lines[1:], path.name, 2)
        return head
    if isinstance(head, dict) and len(lines) == 1:
        return head                                   # the whole font on one line
    return json.loads(data)


def read_jhf(path):
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


def chosen():
    """The font file Silkscreen.FONT_FILE picks, and the report's note on it."""
    name = P.Silkscreen.FONT_FILE
    if not name:
        return FONTS_DIR / DEFAULT_FONT, f"font: KiCad newstroke ({DEFAULT_FONT})"
    custom = FONTS_DIR / name
    if custom.is_file():
        return custom, f"font: custom {name}"
    return FONTS_DIR / DEFAULT_FONT, f"font: {name} not found in kese/assets/fonts, using KiCad newstroke"


def note():
    """The report's note on the font, without reading it: a board with no text never reads one."""
    return chosen()[1]


def load():
    """The font Silkscreen.FONT_FILE picks, read once per file; returns (font, note)."""
    path, text = chosen()
    if path not in _fonts:
        _fonts[path] = read_jhf(path) if path.suffix.lower() == ".jhf" else read_json(path)
    return _fonts[path], text
