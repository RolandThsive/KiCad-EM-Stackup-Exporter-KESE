"""The parameter files of 25.2: every setting of before (tests/settings_before_25_2.txt, the 166 of
25.1) still has a home, under its own name, a new one, or with a refusal that says what to set now;
a parameter file left where the files were before is refused; the old switches that became several
settings set all of them; and every setting of today is of a kind the checks know.

    python -m pytest tests/test_parameters.py           (or:  python tests/test_parameters.py)"""
from pathlib import Path

from helpers import ROOT, run_tests, settings
from kese.job import start
from kese.settings_check import KIND_WORDS, NONE_OR, OR_NONE, check_settings
from parameters import GONE, GROUPS, INNER_ETCH, KINDS, LINES, MOVED, OLD_FILES, OLD_MODULES, P, file_of

BEFORE = (Path(__file__).parent / "settings_before_25_2.txt").read_text(encoding="utf-8").split()


def is_setting(dotted):
    module, name = dotted.split(".")
    return module in P.modules() and (name in P.names(module) or (module == "Stackup" and name in P.lines()))


def test_every_setting_of_before_still_has_a_home():
    assert len(BEFORE) == 166 and len(set(BEFORE)) == 166
    same, moved, gone = [], [], []
    for old in BEFORE:
        now = P.now(old)
        if old in GONE:
            try:
                P.override(old, {})
            except ValueError as e:
                assert f"{old} is no longer a parameter: " in str(e), e
            else:
                raise AssertionError(f"{old} was taken")
            gone.append(old)
        elif now is None:
            assert is_setting(old), f"{old} is no setting any more, and nothing says where it went"
            same.append(old)
        else:
            assert all(is_setting(new) for new in now), f"{old} is now {now}, which are not all settings"
            moved.append(old)
    assert (len(same), len(moved), gone) == (130, 35, ["Color.MATERIALS"]), (len(same), len(moved), gone)
    # and every old name the loader knows is one of before, or left Run.py in an earlier version
    known = set(MOVED) | set(GONE) | {INNER_ETCH}
    assert all(old.startswith("Run.") for old in known - set(BEFORE)), sorted(known - set(BEFORE))
    assert {old.split(".")[0] for old in BEFORE if old.split(".")[0] not in P.modules()} == {"Color", *OLD_MODULES}


def test_an_old_module_name_still_works():
    with settings({"SilkScreen.SILKSCREEN_OVER_COPPER": False}):
        P.override("Silkscreen.SILKSCREEN_OVER_COPPER", True)           # as --set Silkscreen.SILKSCREEN_OVER_COPPER=True
        assert P.SilkScreen.SILKSCREEN_OVER_COPPER is True
    assert P.now("Silkscreen.SILKSCREEN_OVER_COPPER") == ("SilkScreen.SILKSCREEN_OVER_COPPER",)
    assert P.now("SilkScreen.SILKSCREEN_OVER_COPPER") is None


def test_the_old_etch_switch_gives_the_inner_copper_the_tops_factor():
    keys = ("Copper.TOP_ETCH_FACTOR", "Copper.INNER_ETCH_FACTOR", "Copper.BOTTOM_ETCH_FACTOR")
    for given in ([("Copper.ETCH_FACTOR", 0.7), (INNER_ETCH, True)], [(INNER_ETCH, True), ("Copper.ETCH_FACTOR", 0.7)]):
        with settings({key: P.value(key) for key in keys}):             # in either order of --set
            for key, value in given:
                P.override(key, value)
            P.settle()
            assert [P.value(key) for key in keys] == [0.7, 0.7, 0.7], given
    with settings({key: P.value(key) for key in keys}):
        P.override("Copper.INNER_ETCH_FACTOR", 0.4)
        P.override(INNER_ETCH, False)
        P.settle()
        assert P.Copper.INNER_ETCH_FACTOR == 0.0
    lines = []
    with settings({key: P.value(key) for key in keys}):
        start("simulation", None, None, ((INNER_ETCH, True),), False, lines.append).status.stop()
    assert lines == [f"  {INNER_ETCH} is now Copper.INNER_ETCH_FACTOR (parameters/PCB_elements/Copper.py): the value "
                     f"given for {INNER_ETCH} is used as Copper.INNER_ETCH_FACTOR"], lines


def test_an_old_name_that_is_now_several_says_so():
    lines = []
    with settings({"Stackup.finish": True}):
        start("simulation", None, None, (("Finish.FINISH_ENABLED", True),), False, lines.append).status.stop()
    assert lines == ['  Finish.FINISH_ENABLED is now the lines "top_finish", "bottom_finish" and "hole_finish" of '
                     "parameters/PCB_elements/Stackup.py: the value given for Finish.FINISH_ENABLED is used for each of them"], lines


def test_a_parameter_file_left_in_its_old_place_is_refused():
    assert set(OLD_FILES) == {"board", "color", "copper", "finish", "geometry", "parallel", "presets", "run",
                              "silkscreen", "solder_mask", "step", "verifier"}
    for old, said in (("copper", "parameters/copper.py is not read any more: its settings are now in "
                                 "parameters/PCB_elements/Copper.py: move your values there and delete it"),
                      ("color", "parameters/color.py is not read any more: its settings are now in the element files of "
                                "PCB_elements/ (each has a Color section): move your values there and delete it")):
        left = ROOT / "parameters" / f"{old}.py"
        assert not left.exists()
        left.write_text("VIA_WALL_MM = 0.03\n", encoding="utf-8")
        try:
            start("simulation", None, None, (), False, lambda s: None)
        except ValueError as e:
            assert str(e) == said, e
        else:
            raise AssertionError(f"start() ran with {left} lying there")
        finally:
            left.unlink()
    start("simulation", None, None, (), False, lambda s: None).status.stop()


def test_every_setting_of_today_is_checked_for_its_kind():
    check_settings()                                                    # the files as they are pass
    today = {f"{module}.{name}" for module in P.modules() for name in P.names(module)}
    assert set(KINDS) == today | {f"Stackup.{line}" for line in P.lines()}
    # a setting that is None in its file, and the table, have a check of their own
    other = {key for key, kind in KINDS.items() if kind not in KIND_WORDS}
    assert other == {"Board.BOARD_THICKNESS_MM", "SolderMask.MASK_MIN_WIDTH_MM", *NONE_OR, "Board.DIELECTRIC_TABLE"}, other
    assert {"Board.BOARD_THICKNESS_MM", "SolderMask.MASK_MIN_WIDTH_MM"} <= set(OR_NONE)
    assert not set(GROUPS) & set(P.lines()) and all(set(lines) <= set(P.lines()) for lines in GROUPS.values())
    assert all(file_of(module).startswith("parameters/") for module in P.modules())
    assert set(P.lines()) == {line for lines in LINES.values() for line in lines}


def test_a_setting_that_may_be_none_is_checked_when_it_is_not():
    for key, good, bad, said in (
            ("Board.BOARD_THICKNESS_MM", 0.8, "0.8", "Board.BOARD_THICKNESS_MM must be a number, 0 or more, or None, not '0.8'"),
            ("Board.BOARD_THICKNESS_MM", None, -1, "Board.BOARD_THICKNESS_MM must be a number, 0 or more, or None, not -1"),
            ("Board.RESIN_EPSILON_R", None, 0.5, "Board.RESIN_EPSILON_R must be a number, 1 or more, or None, not 0.5"),
            ("SolderMask.MASK_MIN_WIDTH_MM", 0.1, "x", "SolderMask.MASK_MIN_WIDTH_MM must be a number, 0 or more, or None, not 'x'"),
            ("SolderMask.PAD_TO_MASK_CLEARANCE_MM", -0.05, True, "SolderMask.PAD_TO_MASK_CLEARANCE_MM must be a number, or None, not True"),
            ("SilkScreen.FONT_FILE", "hershey.jhf", 3, "SilkScreen.FONT_FILE must be text, in quotes, or None, not 3")):
        with settings({key: good}):
            check_settings()
        with settings({key: bad}):
            try:
                check_settings()
            except ValueError as e:
                assert str(e) == said, e
            else:
                raise AssertionError(f"{key} = {bad!r} was taken")


def test_the_snapshot_names_every_file_and_setting():
    text = P.snapshot()
    for module in P.modules():
        assert f"[{file_of(module)}]" in text
        assert all(f"\n{name} = " in text for name in P.names(module)), module
    assert "\nFUSION_BUILD = 'PLIES_FUSED'\n" in text


if __name__ == "__main__":
    run_tests(__file__)
