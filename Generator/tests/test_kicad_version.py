"""KiCad version rules (kese/s1_read/parse_kicad_version.py), the text markup every version shares
(kese/core/markup.py) and the tokens of the file (kese/core/sexp.py), each checked against what
KiCad's own parser does.  No board is run.

    python -m pytest tests/test_kicad_version.py        (or:  python tests/test_kicad_version.py)"""
from helpers import run_tests
from kese.core import font, markup
from kese.core.sexp import child, parse
from kese.s1_read import parse_kicad_version as kv
from kese.s1_read.read import copper_layers


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


def test_only_the_leading_run_is_copper():
    """A layer named like copper after the run of copper layers is not copper, as in KiCad's
    parseLayers: it neither stops the run with a Python error (no number in its name) nor adds a layer."""
    tree = board('(layers (0 "F.Cu" signal) (1 "GND" power) (31 "B.Cu" signal) (44 "Edge.Cuts" user) '
                 '(45 "In.Cu" user) (46 "In7.Cu" user))')
    warnings = []
    assert copper_layers(tree, "t.kicad_pcb", warnings) == ["F.Cu", "In1.Cu", "B.Cu"]
    assert [l[1] for l in kv.copper_run(child(tree, "layers"))] == ["F.Cu", "In1.Cu", "B.Cu"]


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


def test_text_words_past_a_bare_locked():
    """KiCad 7 and before write a locked text's bare locked before its words, and KiCad 5's %V and %R
    stand for ${VALUE} and ${REFERENCE} (parsePCB_TEXT)."""
    assert kv.text_value(parse('(gr_text locked "PWR" (at 1 2) (layer "B.SilkS"))')) == "PWR"
    assert kv.text_value(parse('(gr_text "locked" (at 1 2) (layer "B.SilkS"))')) == "locked"
    assert kv.text_value(parse('(gr_text locked "locked" (at 1 2))')) == "locked"
    assert kv.text_value(parse('(fp_text reference locked "R1" (at 0 0))')) == "R1"
    assert kv.text_value(parse('(fp_text user %R (at 0 0))')) == "${REFERENCE}"
    assert kv.text_value(parse('(fp_text value "%V, 1%" (at 0 0))')) == "${VALUE}, 1%"
    fp = parse('(footprint "R" (fp_text reference locked "R7" (at 0 0)) (fp_text value %V (at 0 1)))')
    assert kv.footprint_text_fields(fp) == {"REFERENCE": "R7", "VALUE": "${VALUE}"}


def test_net_class_vias_of_kicad_4_and_5():
    """A KiCad 4/5 via that gives no drill (or size) takes its net's class's: the classes' net names
    read as KiCad shows them (the old overbar notation turned into the new), the setup's sizes for a
    class that gives none, and Default for a net in no class."""
    k4 = board('(version 4) (setup (via_size 0.8) (via_drill 0.4)) '
               '(net_class Default "" (via_dia 0.9652) (via_drill 0.6096) (add_net GND) (add_net "Net-(U1-Pad2)")) '
               '(net_class Power "" (via_drill 0.5) (add_net ~RESET~) (add_net +5V))')
    default, classes = kv.net_class_vias(k4, kv.dialect(k4))
    assert default == (0.9652, 0.6096, kv.KICAD_DEFAULT_VIA[2], kv.KICAD_DEFAULT_VIA[3])
    assert classes["GND"] == classes["Net-(U1-Pad2)"] == default
    assert classes["~{RESET}"] == classes["+5V"] == (0.8, 0.5, kv.KICAD_DEFAULT_VIA[2], kv.KICAD_DEFAULT_VIA[3])


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


def test_the_tokens_of_the_file_as_kicad_reads_them():
    """KiCad's DSNLEXER ends a bare atom only at whitespace (a NUL byte among it) or a parenthesis:
    the inch mark in an old board's text (porcupine, KiCad 4) is a character of the atom, not the
    start of a string that runs on to the next double quote and leaves parentheses open.  A line
    whose first character other than whitespace is # is a comment (Sparky2, brought over from
    another tool, has thousands, some with parentheses); # anywhere else is a character.  In a
    quoted string a backslash escapes as in KiCad, and before any other character it stays."""
    tree = board('(gr_text 0.062" (at 360.68 102.87) (layer Dwgs.User)) (gr_text "B" (at 1 2) (layer F.SilkS))')
    assert [t[1] for t in tree[1:]] == ['0.062"', "B"]
    assert child(tree[1], "at") == ["at", "360.68", "102.87"] and child(tree[2], "layer") == ["layer", "F.SilkS"]
    assert board('(net 1 "a\0b")\0(net 2 c)') == ["kicad_pcb", ["net", "1", "a\0b"], ["net", "2", "c"]]
    commented = board('(net 1 a)\n  #1309 pos:46284(0xB4CC) "x\n\t#(\n(net 2 "#b") # c\n#\n')
    assert commented == ["kicad_pcb", ["net", "1", "a"], ["net", "2", "#b"], "#", "c"]
    assert parse(r'(t "\x41\101\a\v\x\q\8 C:\Users \xc3\xa9")') == ["t", "AA\a\vx\\q\\8 C:\\Users \u00e9"]


if __name__ == "__main__":
    run_tests(__file__)
