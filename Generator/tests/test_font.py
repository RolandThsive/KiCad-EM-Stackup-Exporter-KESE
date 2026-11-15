"""The stroke font and the faces a board's text can name (kese/core/font_file.py, kese/s2_collect/text.py):
KiCad's newstroke is read glyph by glyph and is the font it was, all three font layouts give the same
glyphs, a broken line names its file and line, a board with no text reads no font, SilkScreen.FONT_FILE
picks a custom JSON or Hershey font and a changed one takes effect, and text in a TrueType face is drawn
from its render cache, or with the stroke font and a warning, or left out, while (face "KiCad Font") is
the stroke font itself.  Takes a few seconds.

    python -m pytest tests/test_font.py         (or:  python tests/test_font.py)"""
import gzip
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

from helpers import ROOT, run_stages, run_tests, settings

sys.path.insert(0, str(ROOT / "tools"))

from font_lines import font_lines  # noqa: E402
from kese.core import font, font_file  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s2_collect.text import STROKED  # noqa: E402
from parameters import P  # noqa: E402

NEWSTROKE = font_file.FONTS_DIR / font_file.DEFAULT_FONT
# sha256 of newstroke as one JSON document, keys sorted, as main stored it before 6 November 2026
NEWSTROKE_SHA256 = "967ec46a1493eb29ceecfa89b78d35eb9985f08de69edc4f0d6bb8c5ff6d840d"
SMALL = {"name": "small", "first_codepoint": 32, "interline_pitch": 1.68,
         "glyphs": [{"w": 0.5, "s": []}, {"w": 0.3, "s": [[[0.1, -1.0], [0.1, -0.3]]]},
                    {"w": 0.6, "s": [[[0.1, -1.0], [0.1, -0.7]], [[0.4, -1.0], [0.4, -0.7]]]}]}
# A Hershey font of three glyphs from the space on: a blank, then "!" as one stroke, then a gap
HERSHEY = "12345  1JZ\n12346  3JZRFRT\n12347  6JZNFNM RVFVM\n"


def whole(f):
    """A font with every glyph parsed, as one dict."""
    return dict(f, glyphs=[f["glyphs"][i] for i in range(len(f["glyphs"]))])


def test_newstroke_is_read_glyph_by_glyph_and_is_kicads_font_unchanged():
    f = font_file.read_json(NEWSTROKE)
    assert isinstance(f["glyphs"], font_file.Glyphs) and len(f["glyphs"]) == 65487
    assert f["first_codepoint"] == 32 and f["glyphs"][-1] == f["glyphs"][65486]
    text = json.dumps(whole(f), separators=(",", ":"), sort_keys=True)
    assert hashlib.sha256(text.encode()).hexdigest() == NEWSTROKE_SHA256


def test_every_layout_gives_the_same_glyphs():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        written = {"lines.json": font_lines(SMALL), "one_line.json": json.dumps(SMALL).encode(),
                   "indented.json": json.dumps(SMALL, indent=2).encode()}
        for name, data in list(written.items()):
            written[name + ".gz"] = gzip.compress(data)
        for name, data in written.items():
            (tmp / name).write_bytes(data)
            assert whole(font_file.read_json(tmp / name)) == SMALL, name
        lines = font_file.read_json(tmp / "lines.json")
        assert isinstance(lines["glyphs"], font_file.Glyphs) and lines["glyphs"][-1] == SMALL["glyphs"][-1]
        (tmp / "newstroke_one_document.json.gz").write_bytes(
            gzip.compress(json.dumps(whole(font_file.read_json(NEWSTROKE))).encode()))
        old, new = font_file.read_json(tmp / "newstroke_one_document.json.gz"), font_file.read_json(NEWSTROKE)
        assert isinstance(old["glyphs"], list) and len(old["glyphs"]) == len(new["glyphs"])
        assert all(old["glyphs"][i] == new["glyphs"][i] for i in (0, 1, 33, 95, 1000, 20000, 65486))


def test_only_the_glyphs_drawn_are_parsed():
    with settings({"SilkScreen.FONT_FILE": None}):
        font_file._fonts.clear()
        assert not font.render("   ", (0, 0), 0, 1.0, 1.0, 0.1).area and not font_file._fonts   # blank: no font read
        assert font.render("AB 12 A", (0, 0), 0, 1.0, 1.0, 0.1).area > 0
        f, _ = font_file.load()
        assert sorted(f["glyphs"]._parsed) == sorted({ord(c) - 32 for c in " AB12"})


def test_a_broken_line_names_the_file_and_the_line():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "broken.json"
        p.write_bytes(font_lines(SMALL).replace(b'{"w":0.3', b'{"w":0.3,,'))
        f = font_file.read_json(p)
        assert f["glyphs"][0] == SMALL["glyphs"][0]
        try:
            f["glyphs"][1]
        except ValueError as e:
            assert str(e).startswith("font broken.json, line 3: "), e
        else:
            raise AssertionError("a broken glyph was read")


def collected(board_text, changes=None):
    """Stages 1 and 2 on a board written from board_text, with the settings `changes`
    ({"SilkScreen.X": value}) for the run: (Items, the run's notes and warnings)."""
    with settings(changes or {}), tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "fonts.kicad_pcb"
        path.write_text(board_text, encoding="utf-8")
        items, job = run_stages(path, collect)
    return items, list(job.log_lines)


def board(*texts):
    """A two-layer board, 40 by 20 mm, with gr_texts on F.Cu: each (words, face or None, cache words or
    None), the cache a 4 by 2 mm box around (10, 10)."""
    out = []
    for words, face, cache in texts:
        face = f'(face "{face}") ' if face is not None else ""
        rc = (f'(render_cache "{cache}" 0 (polygon (pts (xy 8 9) (xy 12 9) (xy 12 11) (xy 8 11))))'
              if cache is not None else "")
        out.append(f'(gr_text "{words}" (at 10 10) (layer "F.Cu") '
                   f'(effects (font {face}(size 1 1) (thickness 0.15))) {rc})')
    return ('(kicad_pcb (version 20221018) (generator pcbnew) (general (thickness 1.6))\n'
            '(layers (0 "F.Cu" signal) (31 "B.Cu" signal) (36 "B.SilkS" user) (37 "F.SilkS" user)\n'
            '  (38 "B.Mask" user) (39 "F.Mask" user) (44 "Edge.Cuts" user))\n'
            '(setup (pad_to_mask_clearance 0)) (net 0 "")\n'
            '(gr_rect (start 0 0) (end 40 20) (stroke (width 0.1) (type solid)) (fill none) (layer "Edge.Cuts"))\n'
            + "\n".join(out) + ")\n")


def copper(items):
    return [g for g, _ in items.copper_items["F.Cu"]]


def faces(items):
    return {k: n for k, n in list(items.found.items()) + list(items.skipped.items()) if "TrueType" in k}


def test_a_board_with_no_text_reads_no_font():
    font_file._fonts.clear()
    items, lines = collected(board())
    assert not font_file._fonts and "font: KiCad newstroke (kicad_newstroke.json.gz)" in items.notes


def test_text_in_a_truetype_face_is_drawn_from_its_cache_else_with_the_stroke_font_and_a_warning():
    items, lines = collected(board(("TTF", "Some Font Nobody Has", "TTF")))
    assert faces(items) == {"text in a TrueType face, from the file's render cache, on F.Cu": 1}
    assert abs(copper(items)[0].area - 8.0) < 1e-9 and not any("TrueType" in s for s in lines)
    items, lines = collected(board(("TTF", "Some Font Nobody Has", None), ("NEW", "Some Font Nobody Has", "OLD")))
    assert faces(items) == {f"{STROKED}, on F.Cu": 2}
    assert [s for s in lines if "TrueType" in s] == [
        "warning: 2 text(s) in a TrueType face drawn with KiCad's stroke font, in other letter shapes: the file has "
        "no render cache for them, or one made for other words or another angle (open the board in KiCad and "
        "save it)"]
    items, lines = collected(board(("TTF", "Some Font Nobody Has", None)),
                             {"SilkScreen.DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT": False})
    assert faces(items) == {"TrueType text on F.Cu (DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT is False)": 1}
    assert not copper(items) and not any("stroke font, in other" in s for s in lines)


def test_an_empty_render_cache_draws_nothing_as_kicad_does():
    # an empty text, and a character the face lacks: KiCad stores a cache with no polygons, and draws none
    text = board(("", "Exo 2", ""), ("\u25cf", "VeriBest Gerber 0", "\u25cf"))
    items, lines = collected(text.replace(" (polygon (pts (xy 8 9) (xy 12 9) (xy 12 11) (xy 8 11)))", ""))
    assert faces(items) == {"text in a TrueType face, from the file's render cache, on F.Cu": 2}
    assert not copper(items) and not any("TrueType" in s for s in lines)


def test_a_cache_differing_only_where_kese_cannot_know_the_words_is_drawn():
    # the title block's title names a project variable, ${PART} only the project file defines, and the
    # date was the day KiCad saved: the cache's words differ only there, so they are KiCad's words then
    head = '(general (thickness 1.6)) (title_block (title "${TITLE}")) (property "REV" "B")'
    words = "${TITLE} rev ${REV}\\n${CURRENT_DATE} ${PART}"
    text = board((words, "FreeMono", "Main board rev B\\n2026-09-21 X7")).replace("(general (thickness 1.6))", head)
    items, lines = collected(text)
    assert faces(items) == {"text in a TrueType face, from the file's render cache as KiCad last showed its "
                            "variables, on F.Cu": 1}
    assert copper(items) and not any("TrueType" in s for s in lines)
    # a known variable that differs (REV is B, the cache says C) leaves the cache stale
    text = board((words, "FreeMono", "Main board rev C\\n2026-09-21 X7")).replace("(general (thickness 1.6))", head)
    items, lines = collected(text)
    assert faces(items) == {f"{STROKED}, on F.Cu": 1} and any("stroke font, in other" in s for s in lines)


def test_the_face_kicad_font_is_the_stroke_font():
    plain, _ = collected(board(("R12", None, None)))
    for changes in ({}, {"SilkScreen.DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT": False}):
        items, lines = collected(board(("R12", "KiCad Font", None)), changes)
        assert not faces(items) and not any("TrueType" in s for s in lines), changes
        assert copper(items)[0].symmetric_difference(copper(plain)[0]).area < 1e-12


def test_font_file_picks_a_custom_font_and_a_changed_one_takes_effect():
    saved = font_file.FONTS_DIR, P.SilkScreen.FONT_FILE
    with tempfile.TemporaryDirectory() as tmp:
        try:
            font_file.FONTS_DIR = Path(tmp)
            shutil.copy(NEWSTROKE, tmp)
            (Path(tmp) / "small.json").write_bytes(font_lines(SMALL))
            (Path(tmp) / "hershey.jhf").write_text(HERSHEY, encoding="latin-1")
            widths = {}
            for name in (None, "small.json", "hershey.jhf", "missing.jhf"):
                P.override("SilkScreen.FONT_FILE", name)
                _, note = font_file.load()
                widths[name] = font.render("!", (0, 0), 0, 1.0, 1.0, 0.1, ["left"]).bounds
                assert note == font_file.note()
            assert font_file.note().startswith("font: missing.jhf not found") and widths["missing.jhf"] == widths[None]
            assert len({widths[None], widths["small.json"], widths["hershey.jhf"]}) == 3
            h = font_file.read_jhf(Path(tmp) / "hershey.jhf")["glyphs"]
            assert [g["w"] for g in h] == [16 / 21] * 3 and h[1]["s"] == [[[8 / 21, -1.0], [8 / 21, -7 / 21]]]
            assert len(h[2]["s"]) == 2                                          # a pen-up splits the strokes
        finally:
            font_file.FONTS_DIR = saved[0]
            P.override("SilkScreen.FONT_FILE", saved[1])
            font_file._fonts.clear()


if __name__ == "__main__":
    run_tests(__file__)
