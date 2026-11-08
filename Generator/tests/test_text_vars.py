"""Text variables whose values hold ${...} of their own, resolved as the KiCad that wrote the board
resolves them (s2_collect/text_vars.py, s1_read/parse_kicad_version.py text_var_rules): a title block
value expanded by the project's variables, which the board's properties copy; the properties before
or after the title block; KiCad 10's passes; and a footprint's reference and value expanded.

    python -m pytest tests/test_text_vars.py        (or:  python tests/test_text_vars.py)"""
import datetime
import tempfile
from pathlib import Path
from types import SimpleNamespace

from helpers import run_stages, run_tests
from kese.core.sexp import child
from kese.s1_read import read
from kese.s2_collect.text_vars import footprint_fields, saved_words, shown_text

# the first format each KiCad writes
K7, K8, K9, K10 = 20221018, 20240108, 20241229, 20260206
TODAY = datetime.date.today().isoformat()


def items_of(version, head):
    """What stage 2 starts from, for a board of the given format with `head` after (general ...)."""
    text = (f'(kicad_pcb (version {version}) (generator pcbnew) (general (thickness 1.6))\n{head}\n'
            '(layers (0 "F.Cu" signal) (31 "B.Cu" signal) (37 "F.SilkS" user "F.Silkscreen")\n'
            '  (44 "Edge.Cuts" user))\n(setup (pad_to_mask_clearance 0)) (net 0 "")\n'
            '(gr_rect (start 0 0) (end 40 20) (stroke (width 0.1) (type solid)) (fill none) (layer "Edge.Cuts")))\n')
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "vars.kicad_pcb"
        path.write_text(text, encoding="utf-8")
        raw, _ = run_stages(path, read)
    return SimpleNamespace(raw=raw, text_vars=None)


def shown(version, head, words, fp=None):
    """The words KESE shows, and the cache pattern (None when every part is known)."""
    items = items_of(version, head)
    fields = footprint_fields(child(items.raw.tree, "footprint")) if fp else None
    pattern = saved_words(items, words, "F.SilkS", fields)
    return shown_text(items, words, "F.SilkS", fields), pattern.pattern if pattern is not None else None


def test_a_title_block_value_naming_a_project_variable_shows_its_value():
    # as on Great Scott Gadgets' boards: the title block holds ${DATE} and ${VERSION}, the project
    # defines them, and the board's properties hold KiCad's copy (BOARD::SynchronizeProperties)
    head = ('(title_block (title "Filters") (date "${DATE}") (rev "${VERSION}") (company "${GONE}"))\n'
            '(property "DATE" "2025-06-15") (property "VERSION" "0.4.0")')
    for v in (K7, K8, K9, K10):
        assert shown(v, head, "${TITLE}\n${REVISION}\n${ISSUE_DATE}") == ("Filters\n0.4.0\n2025-06-15", None), v
        # a variable the properties do not hold stays as written, and may be any words in the cache
        assert shown(v, head, "(c) ${COMPANY}") == ("(c) ${GONE}", r"\(c\)\ (.*?)"), v
    # a title block value that leaves itself, "${TITLE}", is looked up further: here nowhere
    assert shown(K10, '(title_block (title "${TITLE}"))', "${TITLE}") == ("${TITLE}", "(.*?)")


def test_the_properties_come_before_the_title_block_only_in_kicad_8_and_9():
    head = '(title_block (title "the title block")) (property "TITLE" "the properties")'
    assert {v: shown(v, head, "${TITLE}")[0] for v in (K7, K8, K9, K10)} == {
        K7: "the title block", K8: "the properties", K9: "the properties", K10: "the title block"}


def test_kicad_10_expands_a_value_s_own_variables_and_earlier_kicads_show_them_as_written():
    head = '(property "A" "${B}-${C}") (property "B" "b") (property "C" "${B}") (property "D" "${GONE}")'
    for v in (K7, K8, K9):
        assert shown(v, head, "${A}") == ("${B}-${C}", None), v
        assert shown(v, head, "${D}") == ("${GONE}", None), v      # shown as written: KiCad's words too
    assert shown(K10, head, "${A}") == ("b-b", None)
    assert shown(K10, head, "${D}") == ("${GONE}", "(.*?)")
    loop = '(property "A" "<${A}>")'                                 # KiCad 10 stops after its passes
    assert shown(K10, loop, "${A}") == ("<<<<<<${A}>>>>>>", None)


def test_a_title_block_value_s_current_date_is_expanded_from_kicad_9():
    head = '(title_block (date "${CURRENT_DATE}"))'
    assert shown(K8, head, "${ISSUE_DATE}") == ("${CURRENT_DATE}", None)
    for v in (K9, K10):
        assert shown(v, head, "${ISSUE_DATE}") == (TODAY, "(.*?)"), v
    # the date property of scarlet-8088 (KiCad 10): ${DATE} in the title block, ${CURRENT_DATE} in DATE
    head = '(title_block (date "${DATE}")) (property "DATE" "${CURRENT_DATE}")'
    assert shown(K9, head, "${ISSUE_DATE}") == ("${CURRENT_DATE}", None)
    assert shown(K10, head, "${ISSUE_DATE}") == (TODAY, "(.*?)")


def test_a_footprint_s_reference_and_value_are_expanded_as_its_kicad_expands_them():
    fp = ('(footprint "R:R_0603" (layer "F.Cu") (at 5 5)\n'
          '  (property "Reference" "R1" (at 0 0) (layer "F.SilkS"))\n'
          '  (property "Value" "${PART}" (at 0 1) (layer "F.Fab"))\n'
          '  (property "PART" "1k" (at 0 2) (layer "F.Fab"))\n'
          '  (property "NOTE" "${PART} 1%" (at 0 3) (layer "F.Fab")))')
    # its own text: the value's ${PART} is expanded by every KiCad (FOOTPRINT::ResolveTextVar)
    for v in (K7, K8, K9, K10):
        assert shown(v, fp, "${VALUE}", fp=True) == ("1k", None), v
    # another text's ${R1:VALUE} reaches the value one step deeper: KiCad 8 and 9 stop before it
    assert {v: shown(v, fp, "${R1:VALUE}")[0] for v in (K7, K8, K9, K10)} == {
        K7: "1k", K8: "${PART}", K9: "${PART}", K10: "1k"}
    # any other field is given as written before KiCad 10
    assert {v: shown(v, fp, "${NOTE}", fp=True)[0] for v in (K7, K8, K9, K10)} == {
        K7: "${PART} 1%", K8: "${PART} 1%", K9: "${PART} 1%", K10: "1k 1%"}


def test_the_rules_follow_the_release():
    from kese.s1_read.parse_kicad_version import dialect, text_var_rules
    rules = {v: text_var_rules(dialect(["kicad_pcb", ["version", str(v)]])) for v in (K7, K8, K9, K10)}
    assert [r.passes for r in rules.values()] == [1, 1, 1, 6]
    assert [r.properties_first for r in rules.values()] == [False, True, True, False]
    assert [r.date_in_title_block for r in rules.values()] == [False, False, True, True]
    assert [r.field_levels for r in rules.values()] == [(4, 4), (1, 0), (1, 0), (0, 0)]


if __name__ == "__main__":
    run_tests(__file__)
