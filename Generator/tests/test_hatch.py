"""KiCad 10's hatched fills (kese/s2_collect/hatch.py): the lines' pitch (ten pen widths, or the larger
side over 100), their direction, the cross hatch's grid of square holes, the knockouts and their
margins (the stroke font's pen growth worked out by hand from KiCad's oval rule, a text box's border
by file version, which items knock out which hatch), and featureTest/27 against KiCad 10 itself:
the copper, silkscreen and mask in a window around each hatched drawing, as KiCad 10's pcbnew draws
them for plotting (TransformShapeToPolySet, TransformTextToPolySet), to 0.3 % (KESE's 0.1 um grid
on the finest lines), and the copper of a hatched shape on the mask opened whole, as KiCad's Gerber
of the mask does.

    python -m pytest tests/test_hatch.py            (or:  python tests/test_hatch.py)"""
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import shapely
from shapely.geometry import Point, box

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core.sexp import parse  # noqa: E402
from kese.core.shapes2d import EMPTY  # noqa: E402
from kese.job import start  # noqa: E402
from kese.s1_read import read  # noqa: E402
from kese.s1_read.parse_kicad_version import TEXTBOX_BORDER_FROM, textbox_border  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s2_collect.hatch import Hatched, Knockout, hatch, hatch_of, hatch_segments, knocks, pen_growth, spacing_nm  # noqa: E402
from kese.s3_resolve import resolve  # noqa: E402
from parameters import P  # noqa: E402

BOARD = ROOT.parent / "featureTest" / "27_hatched_fills.kicad_pcb"
# KiCad 10.0's pcbnew, featureTest/27: the area (mm2) of each layer in a window (mm from the board's
# corner, grown by 0.4) around each hatched drawing, as KiCad draws the layer to plot it
KICAD = {
    "HATCH": ("F.Cu", (3, 3, 11, 9), 9.397171), "REVERSE": ("F.Cu", (14, 3, 22, 9), 9.959158),
    "CROSS": ("F.Cu", (25, 3, 31, 9), 9.016708), "POLY": ("F.Cu", (34, 3, 42, 9), 12.138991),
    "WIDE": ("B.Cu", (45, 3, 61, 9), 38.675978), "BARE": ("F.Cu", (44, 12, 52, 18), 12.020185),
    "NO_PEN": ("F.Cu", (55, 12, 61, 18), 0.0), "KO_TEXT": ("F.Cu", (3, 21, 13, 28), 14.144167),
    "KO_LINE": ("F.Cu", (16, 21, 26, 28), 14.736493), "KO_A_B": ("F.Cu", (29, 21, 41, 28), 12.714286),
    "KO_BOX": ("F.Cu", (44, 21, 61, 28), 16.115455),       # the text box itself left out: KESE does not draw text boxes
    "TURNED": ("F.Cu", (5, 33, 11, 39), 2.469526), "FINE": ("B.Cu", (34, 31, 62, 35), 12.529020),
    "PAD": ("F.Cu", (38, 37, 42, 41), 4.407071),
    "SILK_CIRCLE": ("F.SilkS", (3, 12, 9, 18), 6.697216), "SILK_CROSS": ("F.SilkS", (11, 12, 19, 18), 12.167108),
    "MASK_REVERSE": ("F.Mask", (22, 12, 30, 18), 12.020185), "MASK_TRIANGLE": ("B.Mask", (33, 12, 41, 18), 8.399475),
    "SILK_TURNED": ("F.SilkS", (3, 31, 13, 41), 10.418121), "SILK_FIELDS": ("F.SilkS", (17, 31, 31, 41), 26.213594)}


def test_the_pitch_is_ten_pens_or_the_larger_side_over_100():
    assert spacing_nm(0.1, (0, 0, 10, 10)) == 1_000_000
    assert spacing_nm(0.25, (0, 0, 10, 10)) == 2_500_000
    assert spacing_nm(0.1, (0, 0, 300, 10)) == 3_000_000         # 300 lines would be too many: 100
    assert spacing_nm(0.02, (0, 0, 28, 4)) == 280_000


def test_the_lines_run_at_45_degrees_the_way_kicad_draws_them():
    square = box(0, 0, 10, 10)
    for mode, slope in (("hatch", -1.0), ("reverse_hatch", 1.0)):
        segs = hatch_segments(square, slope, 1_000_000)
        assert len(segs) == 19                                   # k = 1..19: the corners touch only
        for (x0, y0), (x1, y1) in segs:
            assert math.isclose(y1 - y0, slope * (x1 - x0), abs_tol=1e-9)
            assert math.isclose((y0 - slope * x0) % 1.0, 0, abs_tol=1e-9) or math.isclose((y0 - slope * x0) % 1.0, 1, abs_tol=1e-9)
        g = hatch(square, 0.1, mode)
        length = sum(math.dist(a, b) for a, b in segs)
        assert abs(g.area - length * 0.1) < 19 * 0.1 ** 2, (mode, g.area, length * 0.1)  # plus the round ends


def test_a_cross_hatch_is_the_shape_less_a_grid_of_square_holes():
    g = hatch(box(0, 0, 10, 10), 0.1, "cross_hatch")
    assert 0.17 * 100 < g.area < 0.21 * 100                    # 1 - 0.9^2 of it
    holes = [h for p in shapely.get_parts(g) for h in p.interiors]
    assert len(holes) > 60
    for h in holes[:10]:
        hole = shapely.Polygon(h)
        if math.isclose(hole.area, 0.81, rel_tol=1e-6):          # a whole one: a 0.9 mm square turned 45 degrees
            (x0, y0), (x1, y1) = list(h.coords)[:2]
            assert math.isclose(abs(x1 - x0), abs(y1 - y0), abs_tol=2e-6)       # to the nm


def test_no_pen_or_no_shape_draws_nothing_and_a_knockout_cuts_it_back():
    assert hatch(box(0, 0, 10, 10), 0.0, "hatch") is EMPTY and hatch(None, 0.1, "hatch") is EMPTY
    whole = hatch(box(0, 0, 10, 10), 0.1, "hatch")
    cut = hatch(box(0, 0, 10, 10), 0.1, "hatch", Point(5, 5).buffer(2))
    assert cut.area < whole.area and cut.intersection(Point(5, 5).buffer(1.9)).area == 0


def test_a_stroke_text_knocks_out_as_far_as_kicads_ovals_reach():
    """KiCad's oval of pen p (TransformOvalToPolygon, ERROR_OUTSIDE at ARC_LOW_DEF 0.02 mm): n sides
    to the circle, at least 8 and a multiple of 8, its sides r (1 / cos(pi / n) - 1) out."""
    for pen, grow in ((0.3, 0.012359), (0.15, 0.006179), (2.0, 0.019591), (0.05, 0.00206), (0.0, 0.0)):
        assert math.isclose(pen_growth(pen), grow, abs_tol=1e-9), pen


def test_a_text_box_has_a_border_by_its_file_version():
    old = SimpleNamespace(format=TEXTBOX_BORDER_FROM - 1)
    new = SimpleNamespace(format=TEXTBOX_BORDER_FROM)
    tb = lambda s: parse(f"(gr_text_box \"x\" {s})")             # noqa: E731
    assert textbox_border(tb(""), old) == 0.0                   # no stroke: KiCad's default pen is -1
    assert textbox_border(tb("(stroke (width 0.2))"), old) == 0.2
    assert textbox_border(tb("(stroke (width 0.2))"), new) == 0.2      # a border unless it says not
    assert textbox_border(tb("(border no) (stroke (width 0.2))"), new) == 0.0
    assert textbox_border(tb("(border yes) (stroke (width 0.2))"), new) == 0.2


def test_which_items_knock_out_which_hatch():
    h = Hatched("F.Cu", box(0, 0, 10, 10), 0.1, "hatch", footprint=7, net="", bounds=(0, 0, 10, 10), key=1)
    k = lambda layer="F.Cu", fp=None, kind="shape", bounds=(1, 1, 2, 2), key=2: Knockout(layer, fp, kind, bounds, None, key)  # noqa: E731
    assert knocks(h, k())                                        # a board drawing
    assert knocks(h, k(kind="text")) and knocks(h, k(kind="textbox"))
    assert not knocks(h, k(layer="B.Cu")) and not knocks(h, k(bounds=(20, 20, 21, 21)))
    assert not knocks(h, k(key=1))                               # not itself
    assert knocks(h, k(fp=8)) and knocks(h, k(fp=8, kind="field"))     # another footprint's drawings and fields
    assert not knocks(h, k(fp=8, kind="text"))                   # but not its other text
    assert not knocks(h, k(fp=7)) and not knocks(h, k(fp=7, kind="field"))   # nor its own footprint's


def test_the_fill_word_is_read_as_kicad_10_writes_it():
    for word in ("hatch", "reverse_hatch", "cross_hatch"):
        assert hatch_of(parse(f"(gr_rect (fill {word}))")) == word
    for s in ("(gr_rect (fill yes))", "(gr_rect (fill solid))", "(gr_rect (fill none))", "(gr_rect)"):
        assert hatch_of(parse(s)) is None


def test_the_hatches_are_what_kicad_draws():
    saved = P.SolderMask.SOLDER_MASK_ENABLED, P.Silkscreen.SILKSCREEN_ENABLED
    P.override("SolderMask.SOLDER_MASK_ENABLED", True)
    P.override("Silkscreen.SILKSCREEN_ENABLED", True)
    try:
        job = start("simulation", ["glb"], None, (), False, lambda s: None)
        r = resolve.run(collect.run(read.run(str(BOARD), job), job), job)
    finally:
        P.override("SolderMask.SOLDER_MASK_ENABLED", saved[0])
        P.override("Silkscreen.SILKSCREEN_ENABLED", saved[1])
    mine = {"F.Cu": r.copper_all["F.Cu"], "B.Cu": r.copper_all["B.Cu"], "F.SilkS": r.silk["F"],
            "F.Mask": r.mask_open["F"], "B.Mask": r.mask_open["B"]}
    for name, (layer, (x0, y0, x1, y1), kicad) in KICAD.items():
        w = r.to_board_T(box(100 + x0 - 0.4, 100 + y0 - 0.4, 100 + x1 + 0.4, 100 + y1 + 0.4))
        a = mine[layer].intersection(w).area
        assert abs(a - kicad) <= 3e-3 * kicad + 1e-6, (name, a, kicad)
    # copper hatched on F.Mask too: KiCad's Gerber of the mask opens the whole rectangle with its pen
    bare = mine["F.Mask"].intersection(r.to_board_T(box(144 - 0.4, 112 - 0.4, 152 + 0.4, 118 + 0.4))).area
    assert math.isclose(bare, 8.2 * 6.2 - 0.1 ** 2 * (4 - math.pi), rel_tol=1e-3), bare
    assert r.items.found["hatched graphics on F.Cu"] == 10 and r.items.skipped["gr_text_box on F.Cu (not modelled)"] == 1


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
