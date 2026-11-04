"""Wrong settings and damaged board files: a setting that is not one of its values stops the run
with a message before any work, and a damaged item is left out with a warning, not a Python error.

    python -m pytest tests/test_bad_input.py        (or:  python tests/test_bad_input.py)"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core.sexp import parse  # noqa: E402
from kese.job import CHOICES, start  # noqa: E402
from kese.s1_read import parse_kicad_version as kv  # noqa: E402
from kese.s1_read import read  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s2_collect.vias import OFF_BOARD  # noqa: E402
from parameters import P  # noqa: E402

VIAS = ROOT.parent / "featureTest" / "03b_vias_k10.kicad_pcb"      # two copper layers


def started(settings, log=lambda s: None):
    """start() with `settings` ({"Module.NAME": value}), put back after: the Job, or the error's text."""
    saved = {key: getattr(getattr(P, key.split(".")[0]), key.split(".")[1]) for key in settings}
    try:
        for key, value in settings.items():
            P.override(key, value)
        return start("simulation", None, None, (), False, log)
    except ValueError as e:
        return str(e)
    finally:
        for key, value in saved.items():
            P.override(key, value)


def test_a_single_format_may_be_a_string():
    assert started({"Run.FILE_FORMAT": "step"}).formats == ["step"]       # not ["s", "t", "e", "p"]


def test_every_setting_with_a_few_values_is_checked():
    assert not isinstance(started({}), str)                                # the defaults pass
    for key, words in CHOICES.items():
        for word in words:
            assert not isinstance(started({key: word}), str), (key, word)
        refused = started({key: "bogus"})
        assert isinstance(refused, str) and key in refused, (key, refused)


def test_workers_must_be_zero_or_more():
    for n in (0, 1, 3):
        assert not isinstance(started({"Run.WORKERS": n}), str), n
    for n in (-1, 1.5, "4", None):
        refused = started({"Run.WORKERS": n})
        assert isinstance(refused, str) and "Run.WORKERS" in refused, (n, refused)


def test_a_tenting_side_with_no_value_keeps_the_default():
    via = parse("(via (tenting (front) (back yes)))")
    assert kv.via_tenting(via, {"F": True, "B": False}) == {"F": True, "B": True}


def test_a_via_on_a_layer_the_board_does_not_have_is_left_out():
    head, vias = VIAS.read_text(encoding="utf-8").split("(via", 1)       # the first via ends on In7.Cu
    damaged = head + "(via" + vias.replace('(layers "F.Cu" "B.Cu")', '(layers "F.Cu" "In7.Cu")', 1)
    lines = []
    job = started({}, lines.append)
    with tempfile.TemporaryDirectory() as tmp:
        broken = Path(tmp) / "damaged.kicad_pcb"
        broken.write_text(damaged, encoding="utf-8")
        for board, left_out in ((VIAS, 0), (broken, 1)):
            items = collect.run(read.run(str(board), job), job)
            assert items.skipped.get(OFF_BOARD, 0) == left_out, board
    assert any("copper layer the board does not have" in line for line in lines), lines


if __name__ == "__main__":
    test_a_single_format_may_be_a_string()
    test_every_setting_with_a_few_values_is_checked()
    test_workers_must_be_zero_or_more()
    test_a_tenting_side_with_no_value_keeps_the_default()
    test_a_via_on_a_layer_the_board_does_not_have_is_left_out()
    print("ok")
