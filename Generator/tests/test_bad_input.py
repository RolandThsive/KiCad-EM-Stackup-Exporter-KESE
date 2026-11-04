"""Wrong settings and damaged board files: a setting that is not one of its values, a misspelt
--set or preset, a setting of another kind than its file gives it (the word "false" for False), a
setting left under its old name in a parameter file, or a shapely too old, stops the run with a
message before any work (a setting's old name in --set still works, with a note; every preset
names real settings and passes the checks), and a damaged item is left out with a warning, not a
Python error.

    python -m pytest tests/test_bad_input.py        (or:  python tests/test_bad_input.py)"""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core.sexp import parse  # noqa: E402
from kese.job import AT_LEAST, CHOICES, KIND_WORDS, ONE_OR_MORE, WHOLE_NUMBERS, ZERO_OR_MORE, start  # noqa: E402
from kese.s1_read import parse_kicad_version as kv  # noqa: E402
from kese.s1_read import read  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s2_collect.vias import OFF_BOARD  # noqa: E402
from parameters import KINDS, MOVED, P  # noqa: E402

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


def test_the_parallel_settings_are_checked():
    for key in WHOLE_NUMBERS:
        key = f"Parallel.{key}"
        for n in (0, 1, 3, 20_000):
            assert not isinstance(started({key: n}), str), (key, n)
        for n in (-1, 1.5, "4", None, True):
            refused = started({key: n})
            assert isinstance(refused, str) and f"{key} must be a whole number" in refused, (key, n, refused)
    for value in (True, False):
        assert not isinstance(started({"Parallel.GIVE_BACK_MEMORY": value}), str), value
    for value in ("false", 0, None):        # --set Parallel.GIVE_BACK_MEMORY=false is the word, which is true
        refused = started({"Parallel.GIVE_BACK_MEMORY": value})
        assert refused == f"Parallel.GIVE_BACK_MEMORY must be True or False, not {value!r}", (value, refused)


def test_the_old_name_of_workers_still_works():
    saved = P.Parallel.WORKERS
    lines = []
    try:
        P.override("Run.WORKERS", 3)                                    # as --set Run.WORKERS=3 does
        assert P.Parallel.WORKERS == 3 and not hasattr(P.Run, "WORKERS")
        start("simulation", None, None, (("Run.WORKERS", 3),), False, lines.append)
    finally:
        P.override("Parallel.WORKERS", saved)
    assert lines == ["  Run.WORKERS is now Parallel.WORKERS (parameters/parallel.py): the value given for "
                     "Run.WORKERS is used as Parallel.WORKERS"], lines
    P.Run.WORKERS = 2                                                   # left in an old parameters/run.py
    try:
        refused = started({})
    finally:
        del P.Run.WORKERS
    assert refused == ("parameters/run.py sets WORKERS, which is now Parallel.WORKERS in parameters/parallel.py: "
                       "set it there"), refused



def test_every_moved_setting_still_works_by_its_old_name():
    # run.py's STEP, Verifier and preset settings moved to step.py, verifier.py and presets.py
    for old, new in MOVED.items():
        (old_module, name), (new_module, new_name) = old.split("."), new.split(".")
        value = getattr(getattr(P, new_module), new_name)
        P.override(old, value)                                          # as --set Run.VERIFY=... does
        assert getattr(getattr(P, new_module), new_name) is value and not hasattr(getattr(P, old_module), name), old
    P.Run.VERIFY, P.Run.STEP_EXACT_ARCS = True, False                   # left in an old parameters/run.py
    try:
        refused = started({})
    finally:
        del P.Run.VERIFY, P.Run.STEP_EXACT_ARCS
    assert refused == ("parameters/run.py sets STEP_EXACT_ARCS, which is now Step.STEP_EXACT_ARCS in parameters/step.py; "
                       "parameters/run.py sets VERIFY, which is now Verifier.VERIFY in parameters/verifier.py: "
                       "set them there"), refused


def test_every_preset_names_real_settings_and_passes_the_checks():
    assert {"freecad", "elmer", "calculix", "openems", "viewer", "blender_glb", "blender_obj"} <= set(P.Presets.PRESETS)
    for name, preset in P.Presets.PRESETS.items():
        saved = {key: getattr(getattr(P, key.split(".")[0]), key.split(".")[1]) for key in preset}
        try:
            for key, value in preset.items():
                P.override(key, value)                                  # a name that is not a setting raises
            job = start(None, None, None, (("PRESET", name), *preset.items()), False, lambda s: None)
        finally:
            for key, value in saved.items():
                P.override(key, value)
        assert (job.mode, job.formats) == (preset["Run.MODE"], preset["Run.FILE_FORMAT"]), name


def test_a_misspelt_preset_is_named_before_the_run():
    from kese.cli import main
    units = P.Run.UNITS
    for preset, said in (({"Run.UNITS": "mm", "Copper.VIA_WAL_MM": 0.02},
                          "--for misspelt: parameters/copper.py has no parameter VIA_WAL_MM (did you mean VIA_WALL_MM?)"),
                         (["Run.UNITS", "mm"], "--for misspelt: parameters/presets.py gives it ['Run.UNITS', 'mm'], not")):
        err, argv = io.StringIO(), sys.argv
        P.Presets.PRESETS["misspelt"] = preset
        sys.argv = ["kese", "--for", "misspelt"]
        try:
            with contextlib.redirect_stderr(err):
                main()
        except SystemExit as e:
            assert e.code == 2, e.code
        else:
            raise AssertionError("the misspelt preset was taken")
        finally:
            sys.argv = argv
            del P.Presets.PRESETS["misspelt"]
            P.override("Run.UNITS", units)
        assert said in err.getvalue(), err.getvalue()
        assert "Traceback" not in err.getvalue()

def test_rounds_and_batches_must_be_one_or_more():
    assert set(ONE_OR_MORE) <= set(AT_LEAST) and AT_LEAST["Step.STEP_ARC_MIN_POINTS"] == 3
    for key, least in AT_LEAST.items():    # at 0 a pinch would be noted as left, a batch would hold nothing
        for n in (least, 10):
            assert not isinstance(started({key: n}), str), (key, n)
        for n in (least - 1, -1, 2.5, "10", True):
            refused = started({key: n})
            assert refused == f"{key} must be a whole number, {least} or more, not {n!r}", (key, n, refused)


def test_every_setting_must_be_of_the_kind_its_file_gives_it():
    # --set Board.BOARD_ENABLED=false gives the word "false", which Python takes as true
    wrong = {bool: "false", int: "10", float: "0.02mm", str: 5, list: "F.SilkS", dict: "freecad"}
    said = {"Board.BOARD_ENABLED": "Board.BOARD_ENABLED must be True or False, not 'false'",
            "Copper.VIA_WALL_MM": "Copper.VIA_WALL_MM must be a number, not '0.02mm'",
            "Copper.NO_NET_NAME": "Copper.NO_NET_NAME must be text, in quotes, not 5",
            "Silkscreen.SILK_LAYERS": "Silkscreen.SILK_LAYERS must be a list, not 'F.SilkS'"}
    for key, kind in KINDS.items():
        if kind not in KIND_WORDS or key == "Run.FILE_FORMAT":
            continue
        refused = started({key: wrong[kind]})
        assert isinstance(refused, str) and refused.startswith(f"{key} must be"), (key, refused)
        if key in said:
            assert refused == said[key], (key, refused)
    for key, value in (("Copper.VIA_WALL_MM", 1), ("Board.BOARD_THICKNESS_MM", 1.2), ("Silkscreen.SILK_LAYERS", ("F.SilkS",))):
        assert not isinstance(started({key: value}), str), (key, value)     # a whole number, None's setting, a tuple


def test_the_verifier_s_tolerances_must_be_zero_or_more():
    for key in ZERO_OR_MORE:
        for x in (0, 0.0, 1e-7, 2):
            assert not isinstance(started({key: x}), str), (key, x)
        for x in (-1e-9, float("nan"), "1e-7", None, False):
            refused = started({key: x})
            assert refused == f"{key} must be a number, 0 or more, not {x!r}", (key, x, refused)


def test_an_old_shapely_is_named_before_the_run():
    import shapely
    from kese.cli import old_packages
    assert old_packages() == []
    triangles = shapely.constrained_delaunay_triangles          # what shapely 2.0 lacks
    del shapely.constrained_delaunay_triangles
    try:
        assert old_packages() == [f"shapely {shapely.__version__} (2.1 or newer)"]
    finally:
        shapely.constrained_delaunay_triangles = triangles


def test_a_misspelt_set_is_named_before_the_run():
    from kese.cli import main
    for item, said in (("Coper.VIA_WALL_MM=0.02", "no parameter module Coper (did you mean Copper?)"),
                       ("copper.VIA_WALL_MM=0.02", "(did you mean Copper?)"),
                       ("Copper.VIA_WAL_MM=0.02", "copper.py has no parameter VIA_WAL_MM (did you mean VIA_WALL_MM?)"),
                       ("Copper.via_wall_mm=0.02", "(did you mean VIA_WALL_MM?)"),
                       ("WORKERS=2", "WORKERS is not Module.NAME (did you mean Parallel.WORKERS?)"),
                       ("Parallel.WORKERS", "give it a value, as in Parallel.WORKERS=value"),
                       ("Parallel.PROCESS_WORKER=2", "parallel.py has no parameter PROCESS_WORKER (did you mean PROCESS_WORKERS?)"),
                       ("Run.WORKER=2", "run.py has no parameter WORKER (did you mean Parallel.WORKERS?)"),
                       ("snapshot.X=1", "no parameter module snapshot")):
        err, argv = io.StringIO(), sys.argv
        sys.argv = ["kese", "--set", item]
        try:
            with contextlib.redirect_stderr(err):
                main()
        except SystemExit as e:
            assert e.code == 2, (item, e.code)
        else:
            raise AssertionError(f"--set {item} was taken")
        finally:
            sys.argv = argv
        assert f"--set {item}: " in err.getvalue() and said in err.getvalue(), (item, err.getvalue())
        assert "Traceback" not in err.getvalue()


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
    test_the_parallel_settings_are_checked()
    test_the_old_name_of_workers_still_works()
    test_every_moved_setting_still_works_by_its_old_name()
    test_every_preset_names_real_settings_and_passes_the_checks()
    test_a_misspelt_preset_is_named_before_the_run()
    test_rounds_and_batches_must_be_one_or_more()
    test_every_setting_must_be_of_the_kind_its_file_gives_it()
    test_the_verifier_s_tolerances_must_be_zero_or_more()
    test_an_old_shapely_is_named_before_the_run()
    test_a_misspelt_set_is_named_before_the_run()
    test_a_tenting_side_with_no_value_keeps_the_default()
    test_a_via_on_a_layer_the_board_does_not_have_is_left_out()
    print("ok")
