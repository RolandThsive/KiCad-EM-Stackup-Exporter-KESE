"""KiCad's parser rules for a pad's shape (kese/s2_collect/pad_shapes.py, pads.py), checked against
pcb_io_kicad_sexpr_parser.cpp: a chamfer makes any pad a chamfered rectangle, with KiCad's own ratios
where the file gives none (0.25 rounding and 0.2 chamfer on the front, nothing on a padstack layer).
No board is run.

    python -m pytest tests/test_pad_rules.py        (or:  python tests/test_pad_rules.py)"""
import math
from types import SimpleNamespace

from helpers import run_tests
from kese.core.sexp import parse
from kese.s2_collect.pad_shapes import pad_shape
from kese.s2_collect.pads import padstack_layers

ITEMS = SimpleNamespace(skipped={})


def area(text, w=2.0, h=1.0):
    return pad_shape(ITEMS, parse(text), w, h).area


def rounded(w, h, ratio):
    r = ratio * min(w, h)
    return w * h - (4 - math.pi) * r * r


def test_a_chamfer_makes_any_pad_a_chamfered_rectangle():
    """KiCad's parsePAD: chamfer_ratio above 0, or a chamfer list, makes the pad CHAMFERED_RECT whatever
    its shape word; its corners keep the pad's rounding, 0.25 of the shorter side unless the file
    says, and a listed corner is cut by 0.2 of it unless the file says."""
    cut = 0.5 * 0.2 ** 2                                                      # one corner, legs 0.2 x 1 mm
    for word in ("rect", "circle", "oval", "trapezoid", "custom"):
        got = area(f'(pad "1" smd {word} (chamfer top_left))')
        assert math.isclose(got, rounded(2, 1, 0.25) + (4 - math.pi) / 4 * 0.25 ** 2 - cut, rel_tol=1e-3), (word, got)
    assert math.isclose(area('(pad "1" smd rect (chamfer_ratio 0.3))'), rounded(2, 1, 0.25), rel_tol=1e-3)
    assert math.isclose(area('(pad "1" smd rect (roundrect_rratio 0) (chamfer top_left bottom_right))'), 2 - 2 * cut)
    assert math.isclose(area('(pad "1" smd roundrect (roundrect_rratio 0) (chamfer_ratio 0.5) (chamfer top_left))'),
                        2 - 0.5 * 0.5 ** 2)
    # no chamfer: the shape word holds
    assert math.isclose(area('(pad "1" smd rect (chamfer_ratio 0) (chamfer))'), 2.0)
    assert math.isclose(area('(pad "1" smd circle)', 1, 1), math.pi / 4, rel_tol=1e-2)


def test_a_padstack_layer_starts_from_no_rounding_and_no_chamfer():
    """A (padstack (layer ...)) entry that leaves out its ratios has none (PADSTACK::CopperLayer makes
    a new layer's shape from SHAPE_PROPS: ratios 0), never the front's or the pad's defaults."""
    pad = parse('(pad "1" thru_hole roundrect (size 2 1) (roundrect_rratio 0.25) (chamfer_ratio 0.2) (chamfer top_left)'
                ' (padstack (mode front_inner_back) (layer "Inner" (shape roundrect) (size 2 1))'
                ' (layer "B.Cu" (shape roundrect) (size 2 1) (roundrect_rratio 0.5) (chamfer top_left))))')
    stack = padstack_layers(pad, ["F.Cu", "In1.Cu", "B.Cu"])
    assert math.isclose(pad_shape(ITEMS, stack["In1.Cu"], 2, 1).area, 2.0)               # square corners
    assert math.isclose(pad_shape(ITEMS, stack["B.Cu"], 2, 1).area,
                        rounded(2, 1, 0.5) + (4 - math.pi) / 4 * 0.5 ** 2, rel_tol=5e-3)   # corner squared, no cut


if __name__ == "__main__":
    run_tests(__file__)
