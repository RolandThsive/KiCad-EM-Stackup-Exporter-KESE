"""KiCad version rules (kese/s1_read/parse_kicad_version.py) and the text markup every version shares
(kese/core/markup.py), each checked against what KiCad's own parser does.  No board is run.

    python -m pytest tests/test_kicad_version.py        (or:  python tests/test_kicad_version.py)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kese.core import font, markup  # noqa: E402
from kese.core.sexp import parse  # noqa: E402
from kese.s1_read import parse_kicad_version as kv  # noqa: E402


def board(text):
    return parse(f"(kicad_pcb {text})")


def test_release_of_each_format():
    """A release's own format, and a development build's, which counts as the next release."""
    for fmt, release in ((3, 3), (4, 4), (20171130, 5), (20201116, 6), (20211014, 6), (20221018, 7),
                         (20240108, 8), (20241228, 9), (20241229, 9), (20250513, 10), (20260206, 10), (20261031, 11)):
        assert kv.dialect(board(f"(version {fmt})")).release == release, fmt
    d = kv.dialect(board("(generator pcbnew)"))
    assert not d.stated and d.format == kv.NO_VERSION


def test_copper_layers_read_by_place():
    """KiCad 3 numbers F.Cu 15 and B.Cu 0; KiCad 4/5 keep a renamed layer's name only; KiCad reads
    them by their place in the list, a canonical name keeping its layer."""
    v3 = parse("(layers (15 Top signal) (0 Bottom signal) (28 Contorno.scheda user))")
    assert kv.copper_layer_names(v3) == {"Top": "F.Cu", "Bottom": "B.Cu", "Contorno.scheda": "Edge.Cuts"}
    v5 = parse("(layers (0 F.Cu signal) (1 GND.Cu power) (2 PWR mixed) (31 Bottom signal) (44 Edge.Cuts user))")
    assert kv.copper_layer_names(v5) == {"GND.Cu": "In1.Cu", "PWR": "In2.Cu", "Bottom": "B.Cu"}
    v9 = parse('(layers (0 "F.Cu" signal) (2 "B.Cu" signal) (4 "In1.Cu" signal) (6 "In2.Cu" power))')
    assert kv.copper_layer_names(v9) == {}
    user = parse('(layers (0 "F.Cu" signal) (2 "B.Cu" signal) (25 "Edge.Cuts" user) (39 "User.1" signal))')
    assert kv.copper_layer_names(user) == {}           # a signal-typed User layer after the copper is not copper


def test_zero_mask_margin_inherits_before_kicad_9():
    pad = parse("(pad 1 smd rect (solder_mask_margin 0))")
    assert kv.mask_margin(pad, kv.dialect(board("(version 20240108)"))) is None
    assert kv.mask_margin(pad, kv.dialect(board("(version 20241229)"))) == 0.0
    assert kv.mask_margin(parse("(pad 1 smd rect (solder_mask_margin 0.05))"), kv.dialect(board("(version 4)"))) == 0.05


def test_kicad_4_default_text_size():
    assert kv.text_size(parse("(font (thickness 0.15))")) == (1.524, 1.524)
    assert kv.text_size(parse("(font (size 1 0.8))")) == (1.0, 0.8)


def test_text_pen():
    """The file's thickness; none (or 0) leaves it to KiCad's default; after format 20260826 a bold
    text's thickness is its base pen, drawn 1.6 times as wide."""
    k10, k11 = kv.dialect(board("(version 20260206)")), kv.dialect(board("(version 20261031)"))
    assert kv.text_pen(parse("(font (size 1 1) (thickness 0.15))"), k10) == 0.15
    assert kv.text_pen(parse("(font (size 1 1) (thickness 0))"), k10) is None
    assert kv.text_pen(parse("(font (size 1 1) (thickness 0.15) (bold yes))"), k10) == 0.15
    assert abs(kv.text_pen(parse("(font (size 1 1) (thickness 0.15) (bold yes))"), k11) - 0.24) < 1e-12


def test_legacy_segment_fill():
    """A KiCad 4/5 zone filled with segments only; with polygons too, the polygons are the fill."""
    only = parse("(zone (min_thickness 0.25) (fill_segments (pts (xy 0 0) (xy 1 0)) (pts (xy 0 0.2) (xy 1 0.2))))")
    assert kv.legacy_fill_segments(only) == [((0.0, 0.0), (1.0, 0.0)), ((0.0, 0.2), (1.0, 0.2))]
    both = parse("(zone (filled_polygon (pts (xy 0 0) (xy 1 0) (xy 1 1))) (fill_segments (pts (xy 0 0) (xy 1 0))))")
    assert kv.legacy_fill_segments(both) == []


def test_old_overbar_notation():
    """string_utils.cpp ConvertToNewOverbarNotation, for files before format 20210606."""
    k5, k6 = kv.dialect(board("(version 20171130)")), kv.dialect(board("(version 20211014)"))
    cases = {"~RESET~": "~{RESET}", "~RESET": "~{RESET}", "A ~CS~ B": "A ~{CS} B", "~~x": "~x", "~": "~",
             "~A B": "~{A} B", "(~WR)": "(~{WR})", "~{x}": "~{x}", "~~{": "~~{"}
    for old, new in cases.items():
        assert kv.overbar_markup(old, k5) == new, old
    assert kv.overbar_markup("~RESET~", k6) == "~RESET~"


def test_markup_runs():
    assert markup.parse("RESET") == ([("RESET", ())], [])
    assert markup.parse("A~{B}C") == ([("A", ()), ("B", ("~",)), ("C", ())], [(1, 2)])
    assert markup.parse("x^{2}_{i}") == ([("x", ()), ("2", ("^",)), ("i", ("_",))], [])
    assert markup.parse("~{a^{b}}") == ([("a", ("~",)), ("b", ("~", "^"))], [(0, 2)])
    assert markup.parse("~{open") == ([("~{open", ())], [])          # never closed: plain text
    assert markup.parse("~{x{slash}y}") == ([("x{slash}y", ("~",))], [(0, 1)])


def test_markup_is_drawn_not_printed():
    """~{CS} draws CS and a bar over it, no tilde or braces; a subscript is smaller and lower."""
    plain = font.render("CS", (0, 0), 0, 1.0, 1.0, 0.1, ["left"])
    barred = font.render("~{CS}", (0, 0), 0, 1.0, 1.0, 0.1, ["left"])
    assert abs(barred.bounds[2] - plain.bounds[2]) < 0.15         # about as wide as CS: the bar runs
    assert abs(barred.bounds[0] - plain.bounds[0]) < 0.15         # over the letters' advance, 0.1 W in
    assert barred.bounds[1] < plain.bounds[1] - 0.15              # the bar sits above the letters
    sub = font.render("K_{0}", (0, 0), 0, 1.0, 1.0, 0.1, ["left"])
    assert sub.bounds[2] < font.render("K0", (0, 0), 0, 1.0, 1.0, 0.1, ["left"]).bounds[2]


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"{name:56s} ok")
            except AssertionError as exc:
                failed += 1
                print(f"{name:56s} FAIL {exc}")
    sys.exit(1 if failed else 0)
