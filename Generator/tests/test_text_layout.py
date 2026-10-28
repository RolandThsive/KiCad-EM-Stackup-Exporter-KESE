"""Text layout (kese/core/font.py, kese/s2_collect/text.py) against KiCad's own: a KiCad 7 board with
one text per case (justification, two lines, two lines with a line spacing that KiCad does not plot,
tabs, an angle, italic, bold, a wide font, an escaped quote, mirrored text on the back, the
reference of a footprint turned so that KiCad keeps it upright) goes through stages 1 and 2, and
every text's ink must have the bounds KiCad 7.0.11 plots for it (kicad-cli pcb export svg, the
stroked text thickened as the SVG draws it), to 5 µm: KESE draws round ends with
Silkscreen.TEXT_STROKE_QUAD_SEGS segments per quarter circle.  Takes a moment.

    python -m pytest tests/test_text_layout.py           (or:  python tests/test_text_layout.py)"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.job import start  # noqa: E402
from kese.pipeline import STAGES  # noqa: E402
from kese.s2_collect.text import kept_upright, unescape, upright  # noqa: E402
from parameters import P  # noqa: E402

TOLERANCE_MM = 0.005
ONE = "(font (size 1 1) (thickness 0.15))"
TEXTS = [  # as written in the file, (at ...), layer, effects, bounds KiCad 7.0.11 plots (KiCad frame, mm)
    ("LEFT", "100 100", "F.SilkS", f"{ONE} (justify left)", (100.2618, 99.3798, 103.4118, 100.5298)),
    ("CENTRE", "100 104", "F.SilkS", ONE, (97.3060, 103.3798, 102.6940, 104.5298)),
    ("RIGHT", "100 108", "F.SilkS", f"{ONE} (justify right)", (95.7787, 107.3798, 99.8811, 108.5298)),
    ("TOP LEFT", "100 112", "F.SilkS", f"{ONE} (justify left top)", (100.1189, 111.9648, 106.9832, 113.1148)),
    ("BOTTOM RIGHT", "100 118", "F.SilkS", f"{ONE} (justify right bottom)", (89.2549, 116.7948, 99.8811, 117.9448)),
    ("LINE ONE\\nLINE TWO", "125 100", "F.SilkS", ONE, (121.6631, 98.5748, 128.3845, 101.3348)),
    ("R1\\nR22", "125 108", "F.SilkS", f"{ONE} (justify right)", (122.1596, 106.5748, 124.7858, 109.3348)),
    ("A\tB\tC", "125 114", "F.SilkS", f"{ONE} (justify left)", (125.1189, 113.3798, 133.7451, 114.5298)),
    ("SPACED\\nLINES", "170 105", "F.SilkS", "(font (size 1 1) (thickness 0.15) (line_spacing 1.5)) (justify left)",
     (170.2142, 103.5748, 175.6975, 106.3348)),
    ("ROT30", "125 120 30", "F.SilkS", "(font (size 1.2 1.2) (thickness 0.2))", (122.3702, 118.1677, 127.4679, 121.8432)),
    ("ITALIC", "150 100", "F.SilkS", "(font (size 1.5 1.5) (thickness 0.25) italic)", (146.9375, 99.0559, 153.2857, 100.8059)),
    ("BOLD", "150 106", "F.SilkS", "(font (size 1.5 1.5) (thickness 0.3) bold)", (147.3143, 105.0283, 152.7571, 106.8283)),
    ("Wide 2x1.5", "150 112", "F.SilkS", "(font (size 2 1.5) (thickness 0.3))", (143.8500, 110.7596, 156.0786, 113.0596)),
    ('Q\\"uote', "150 118", "F.SilkS", ONE, (147.5917, 117.3798, 152.4083, 118.6251)),
    ("MIRROR", "125 126", "B.SilkS", "(font (size 1.5 1.5) (thickness 0.25)) (justify mirror)", (120.9107, 125.0559, 129.0179, 126.8059)),
]
U12 = (167.4147, 122.2498, 169.8544, 124.8915)    # (at 0 -2 135) on a footprint at 45 degrees: drawn at -45


def board():
    """The board file: TEXTS, and U12 on its footprint."""
    rows = [row[:4] for row in TEXTS]
    texts = "\n".join(f'  (gr_text "{t}" (at {at}) (layer "{layer}") (tstamp 00000000-0000-0000-0000-{k:012d})\n'
                      f'    (effects {fx})\n  )' for k, (t, at, layer, fx) in enumerate(rows))
    return f'''(kicad_pcb (version 20221018) (generator pcbnew)
  (general (thickness 1.6))
  (paper "A4")
  (layers (0 "F.Cu" signal) (31 "B.Cu" signal) (36 "B.SilkS" user "B.Silkscreen") (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user) (39 "F.Mask" user) (44 "Edge.Cuts" user))
  (setup (pad_to_mask_clearance 0))
  (net 0 "")
  (footprint "Test:U" (layer "F.Cu") (tstamp 00000000-0000-0000-0001-000000000001) (at 170 125 45)
    (fp_text reference "U12" (at 0 -2 135) (layer "F.SilkS") (tstamp 00000000-0000-0000-0001-000000000002)
      (effects (font (size 1 1) (thickness 0.15))))
  )
{texts}
  (gr_rect (start 85 90) (end 185 135) (layer "Edge.Cuts") (stroke (width 0.1) (type default)) (fill none)
    (tstamp 00000000-0000-0000-0002-000000000001))
)
'''


def collect(text):
    """Items of a board file, from stages 1 and 2."""
    with tempfile.TemporaryDirectory() as tmp:
        pcb = Path(tmp) / "texts.kicad_pcb"
        pcb.write_text(text)
        job = start("simulation", ["glb"], Path(tmp) / "out", (), True, lambda s: None)
        try:
            return STAGES[1].run(STAGES[0].run(pcb, job), job)
        finally:
            job.status.stop()


def overlap(a, b):
    """The area two bounds (x0, y0, x1, y1) share."""
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def test_texts_where_kicad_plots_them():
    P.Run.SHOW_PROGRESS = False
    items = collect(board())
    expected = [(t, layer[0], b) for t, _, layer, _, b in TEXTS] + [("U12", "F", U12)]
    for text, side, want in expected:
        got = max(items.silk_items[side], key=lambda g: overlap(g.bounds, want)).bounds
        off = max(abs(a - b) for a, b in zip(got, want))
        assert off <= TOLERANCE_MM, f"{text!r}: bounds {got} against KiCad's {want}, {off * 1000:.1f} um off"


def test_upright_and_escapes():
    assert [upright(a) for a in (0.0, 90.0, 90.5, 135.0, 180.0, 270.0, -90.0, -135.0)] == \
           [0.0, 90.0, -89.5, -45.0, 0.0, 90.0, 90.0, 45.0]
    assert kept_upright(["fp_text", "reference", "U1", ["at", "0", "0", "135"]])
    assert not kept_upright(["fp_text", "reference", "U1", ["at", "0", "0", "135", "unlocked"]])     # KiCad <= 7
    assert not kept_upright(["property", "Reference", "U1", ["at", "0", "0", "135"], ["unlocked", "yes"]])
    assert kept_upright(["property", "Reference", "U1", ["at", "0", "0", "135"], ["unlocked", "no"]])
    assert unescape('A\\"B\\\\C\\nD\\tE') == 'A"B\\C\nD\tE'


if __name__ == "__main__":
    test_upright_and_escapes()
    test_texts_where_kicad_plots_them()
    print("ok")
