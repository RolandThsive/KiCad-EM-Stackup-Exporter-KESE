"""Wrong settings and damaged board files: a setting that is not one of its values, a misspelt
--set or preset, a setting of another kind than its file gives it (the word "false" for False), a
setting left under its old name in a parameter file, or a shapely too old, stops the run with a
message before any work (a setting's old name in --set still works, with a note; every preset
names real settings and passes the checks), and a damaged item is left out with a warning, not a
Python error.  A board file KiCad itself refuses (a number that is not one, not UTF-8 text) stops
with its name and the reason; a thickness below zero is read as not given, with a warning, and a
board too thin for its copper stops with the setting to change; a byte order mark is passed over.

    python -m pytest tests/test_bad_input.py        (or:  python tests/test_bad_input.py)"""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

from helpers import FEATURES, run_tests, settings
from kese.core.sexp import parse
from kese.job import start
from kese.settings_check import (AT_LEAST, CHOICES, KIND_WORDS, MORE_THAN_ZERO, NUMBER_AT_LEAST, ONE_OR_MORE, OR_NONE,
                                 SHARES, WHOLE_NUMBERS)
from kese.s1_read import parse_kicad_version as kv
from kese.s1_read import read
from kese.s2_collect import collect
from kese.s2_collect.vias import OFF_BOARD
from parameters import KINDS, LINES, MOVED, P

VIAS = FEATURES / "03b_vias_k10.kicad_pcb"      # two copper layers


def started(changes, log=lambda s: None):
    """start() with the settings `changes` ({"Module.NAME": value}), put back after: the Job, or the
    error's text."""
    with settings(changes):
        try:
            return start("simulation", None, None, (), False, log)
        except ValueError as e:
            return str(e)


def test_a_single_format_may_be_a_string():
    assert started({"Run.FILE_FORMAT": "step"}).formats == ["step"]       # not ["s", "t", "e", "p"]


def test_every_setting_with_a_few_values_is_checked():
    assert not isinstance(started({}), str)                                # the defaults pass
    for key, words in CHOICES.items():
        for word in words:
            more = {"Board.DIELECTRIC_TABLE": ((1e9, 4.5, 0.02),)} if word == "table" else {}      # "table" needs one
            assert not isinstance(started({key: word, **more}), str), (key, word)
        refused = started({key: "bogus"})
        assert isinstance(refused, str) and key in refused, (key, refused)
    refused = started({"Board.DIELECTRIC_MODEL": "table"})
    assert refused == ("Board.DIELECTRIC_MODEL is 'table' but Board.DIELECTRIC_TABLE is empty: give it rows of "
                       "(frequency in Hz, er, tan d)"), refused
    for table in ("1e9", ((1e9, 4.5),), ((1e9, 4.5, 0.02), (1e8, 4.6, 0.02)), ((0, 4.5, 0.02),), [(1e9, 0.5, 0.02)]):
        refused = started({"Board.DIELECTRIC_TABLE": table})
        assert isinstance(refused, str) and refused.startswith("Board.DIELECTRIC_TABLE must be rows of"), (table, refused)


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
    assert lines == ["  Run.WORKERS is now Parallel.WORKERS (parameters/Run_KESE/Parallel.py): the value given for "
                     "Run.WORKERS is used as Parallel.WORKERS"], lines
    P.Run.WORKERS = 2                                                   # left in a Run.py kept through an update
    try:
        refused = started({})
    finally:
        del P.Run.WORKERS
    assert refused == ("parameters/Run_KESE/Run.py sets WORKERS, which is now Parallel.WORKERS "
                       "(parameters/Run_KESE/Parallel.py): set it there"), refused


def everywhere(name):
    """The values a setting of today has: its own, or for a line of the stack-ups that line in each
    stack-up that has it."""
    module, name = name.split(".")
    if module == "Stackup" and not name.isupper():
        return [getattr(P.Stackup, stackup)[name] for stackup in LINES if name in LINES[stackup]]
    return [getattr(getattr(P, module), name)]


def test_every_moved_setting_still_works_by_its_old_name():
    # one old name may stand for several settings of today, or for lines of the two stack-ups
    for old, new in MOVED.items():
        old_module, name = old.split(".")
        for value in ([True, False] if type(everywhere(new[0])[0]) is bool else [everywhere(new[0])[0]]):
            with settings(dict.fromkeys(new, P.value(new[0]))):             # put back after
                P.override(old, value)                                      # as --set Run.VERIFY=... does
                assert all(now is value for n in new for now in everywhere(n)), (old, value)
        assert old_module not in P.modules() or not hasattr(getattr(P, old_module), name), old
    P.Run.VERIFY, P.Run.STEP_EXACT_ARCS = True, False                   # left in a Run.py kept through an update
    try:
        refused = started({})
    finally:
        del P.Run.VERIFY, P.Run.STEP_EXACT_ARCS
    assert refused == ("parameters/Run_KESE/Run.py sets STEP_EXACT_ARCS, which is now Step.STEP_EXACT_ARCS "
                       "(parameters/Fileformats/Step.py); parameters/Run_KESE/Run.py sets VERIFY, which is now "
                       "Verifier.VERIFY (parameters/Run_KESE/Verifier.py): set them there"), refused


def test_every_preset_names_real_settings_and_passes_the_checks():
    assert {"freecad", "elmer", "calculix", "openems", "viewer", "blender_glb", "blender_obj"} <= set(P.Presets.PRESETS)
    for name, preset in P.Presets.PRESETS.items():
        with settings(preset):                                          # a name that is not a setting raises
            job = start(None, None, None, (("PRESET", name), *preset.items()), False, lambda s: None)
        assert (job.mode, job.formats) == (preset["Run.MODE"], preset["Run.FILE_FORMAT"]), name


def test_a_misspelt_preset_is_named_before_the_run():
    from kese.cli import main
    units = P.Run.UNITS
    for preset, said in (({"Run.UNITS": "mm", "Copper.VIA_WAL_MM": 0.02},
                          "--for misspelt: parameters/PCB_elements/Copper.py has no parameter VIA_WAL_MM (did you mean VIA_WALL_MM?)"),
                         (["Run.UNITS", "mm"], "--for misspelt: parameters/Run_KESE/Presets.py gives it ['Run.UNITS', 'mm'], not")):
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
    # --set Stackup.top_copper=false gives the word "false", which Python takes as true
    wrong = {bool: "false", int: "10", float: "0.02mm", str: 5, list: "F.SilkS", dict: "freecad"}
    said = {"Stackup.top_copper": "Stackup.top_copper must be True or False, not 'false'",
            "Stackup.cores": "Stackup.cores must be True or False, not 'false'",      # a line of the other stack-up
            "Stackup.PLIES_FUSED": "Stackup.PLIES_FUSED must be a dict, not 'freecad'",
            "Board.JOIN_EQUAL_PLIES": "Board.JOIN_EQUAL_PLIES must be True or False, not 'false'",
            "Board.RESIN_EPSILON_R": "Board.RESIN_EPSILON_R must be a number, 1 or more, or None, not '0.02mm'",
            "Copper.VIA_WALL_MM": "Copper.VIA_WALL_MM must be a number, not '0.02mm'",
            "Copper.NO_NET_NAME": "Copper.NO_NET_NAME must be text, in quotes, not 5",
            "SilkScreen.SILK_LAYERS": "SilkScreen.SILK_LAYERS must be a list, not 'F.SilkS'"}
    assert set(said) <= set(KINDS)
    for key, kind in KINDS.items():
        if kind not in KIND_WORDS or key == "Run.FILE_FORMAT":
            continue
        refused = started({key: wrong[kind]})
        assert isinstance(refused, str) and refused.startswith(f"{key} must be"), (key, refused)
        if key in said:
            assert refused == said[key], (key, refused)
    for key, value in (("Copper.VIA_WALL_MM", 1), ("Board.BOARD_THICKNESS_MM", 1.2), ("SilkScreen.SILK_LAYERS", ("F.SilkS",)),
                       *dict.fromkeys(OR_NONE).items()):
        assert not isinstance(started({key: value}), str), (key, value)     # a whole number, None's setting, a tuple, None


def test_tolerances_and_limits_must_be_in_their_range():
    for key, least in NUMBER_AT_LEAST.items():                      # the Verifier's tolerances, the mitre limit
        for x in (least, float(least), least + 1e-7, least + 2):
            assert not isinstance(started({key: x}), str), (key, x)
        for x in (least - 1e-9, float("nan"), "1e-7", None, False):
            refused = started({key: x})
            assert refused == f"{key} must be a number, {least} or more, not {x!r}", (key, x, refused)
    for key in MORE_THAN_ZERO:                                      # the longest arc
        beside = {"Board.DS_LOW_FREQUENCY_HZ": 1e-6} if key == "Board.DS_HIGH_FREQUENCY_HZ" else {}    # the corners stay in order
        for x in (1e-3, 90, 181.0, 400):
            assert not isinstance(started({**beside, key: x}), str), (key, x)
        for x in (0, 0.0, -90, float("nan"), "90", None, True):
            refused = started({key: x})
            assert refused == f"{key} must be a number more than 0, not {x!r}", (key, x, refused)
    for key in SHARES:                                              # how far a via's plug reaches
        for x in (1e-3, 0.5, 1, 1.0):
            assert not isinstance(started({key: x}), str), (key, x)
        for x in (0, 0.0, -0.5, 1.0001, 2, float("nan"), "0.5", None, True):
            refused = started({key: x})
            assert refused == f"{key} must be a number more than 0 and at most 1, not {x!r}", (key, x, refused)
    from kese.s4_geometry.finish import mitre                      # the finish's corners take the limit
    with settings({"Finish.FINISH_MITRE_LIMIT": 3.0}):
        assert mitre() == {"join_style": "mitre", "mitre_limit": 3.0}


def test_an_outline_of_no_size_is_left_out():
    """A closed Edge.Cuts outline of Board.OUTLINE_MIN_AREA_MM2 or less is left out, not made a board."""
    import shapely
    from types import SimpleNamespace
    from kese.s3_resolve.outline import outline_from
    board, speck = shapely.box(0, 0, 10, 5), shapely.box(20, 0, 20.0001, 0.0001)      # 1e-8 mm²
    items = SimpleNamespace(edge_closed=[board, speck], edge_open=[], copper_items={})
    for least, parts in ((P.Board.OUTLINE_MIN_AREA_MM2, 2), (1e-6, 1)):
        with settings({"Board.OUTLINE_MIN_AREA_MM2": least}):
            assert shapely.get_num_geometries(outline_from(items, print)) == parts, least


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
                       ("Copper.VIA_WAL_MM=0.02", "PCB_elements/Copper.py has no parameter VIA_WAL_MM (did you mean VIA_WALL_MM?)"),
                       ("Copper.via_wall_mm=0.02", "(did you mean VIA_WALL_MM?)"),
                       ("WORKERS=2", "WORKERS is not Module.NAME (did you mean Parallel.WORKERS?)"),
                       ("Parallel.WORKERS", "give it a value, as in Parallel.WORKERS=value"),
                       ("Parallel.PROCESS_WORKER=2", "Run_KESE/Parallel.py has no parameter PROCESS_WORKER (did you mean PROCESS_WORKERS?)"),
                       ("Run.WORKER=2", "Run_KESE/Run.py has no parameter WORKER (did you mean Parallel.WORKERS?)"),
                       ("Stackup.top_coper=False", "PCB_elements/Stackup.py has no parameter top_coper (did you mean top_copper?)"),
                       ("Stackup.soldermask=True", "PCB_elements/Stackup.py has no parameter soldermask (did you mean solder_mask?)"),
                       ("Color.MATERIALS={}", "Color.MATERIALS is no longer a parameter: every colour is now a setting of its own"),
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


def board_variant(name, text_of):
    """03b_vias_k10 changed by text_of(text) -> text (or bytes), read and collected: (Items, warnings),
    or the ValueError's text."""
    lines = []
    job = started({}, lines.append)
    with tempfile.TemporaryDirectory() as tmp:
        board = Path(tmp) / name
        changed = text_of(VIAS.read_text(encoding="utf-8"))
        (board.write_bytes if isinstance(changed, bytes) else board.write_text)(changed)
        try:
            return collect.run(read.run(str(board), job), job), lines
        except ValueError as e:
            return str(e), lines


def test_a_number_that_is_not_one_is_refused_with_the_file_named():
    # a via at nan vanished without a word, a pad of size abc stopped with Python's own words; KiCad
    # refuses both ("Expecting ...", "Invalid floating point number")
    for bad in ("nan", "inf", "-Infinity", "1e999", "abc"):
        said, _ = board_variant("damaged.kicad_pcb", lambda t: t.replace("(at 104 104)", f"(at {bad} 104)", 1))
        assert said == (f"damaged.kicad_pcb: {bad!r} where a number belongs, in (at {bad} 104 ...): "
                        "KiCad refuses such a file too (a damaged file?)"), (bad, said)
    said, _ = board_variant("damaged.kicad_pcb", lambda t: t.replace("(thickness 1.6)", "(thickness nan)", 1))
    assert said.startswith("damaged.kicad_pcb: 'nan' where a number belongs, in (thickness nan ...)"), said
    from kese.core.sexp import numbers
    assert numbers(parse("(at 1 2 90 unlocked)")) == [1.0, 2.0, 90.0]          # a word is still passed over


def test_a_file_that_is_not_utf8_text_is_named():
    for name, data in (("binary.kicad_pcb", bytes(range(256)) * 4),
                       ("utf16.kicad_pcb", VIAS.read_text(encoding="utf-8").encode("utf-16"))):
        said, _ = board_variant(name, lambda t: data)
        assert said.startswith(f"{name} is not a KiCad board file: it is not UTF-8 text, as KiCad writes"), said


def test_a_byte_order_mark_is_passed_over():
    plain, _ = board_variant("plain.kicad_pcb", lambda t: t)
    marked, _ = board_variant("marked.kicad_pcb", lambda t: "\ufeff" + t)
    assert not isinstance(marked, str), marked
    assert marked.found == plain.found and marked.stackup.laminate_thickness == plain.stackup.laminate_thickness


def test_a_thickness_below_zero_is_read_as_not_given():
    # the copper came out -0.2 mm thick, every part turned inside out, with no word but the Verifier's FAIL
    items, lines = board_variant("negative.kicad_pcb", lambda t: t.replace("(thickness 0.035)", "(thickness -0.2)"))
    assert not isinstance(items, str), items
    assert items.stackup.copper_thickness["F.Cu"] == items.stackup.copper_thickness["B.Cu"] == P.Copper.DEFAULT_TOP_FOIL_MM
    assert all(d.thickness > 0 for d in items.stackup.dielectrics)
    assert sum("thickness -0.2 mm is less than 0: read as not given" in line for line in lines) == 2, lines
    items, lines = board_variant("negative.kicad_pcb", lambda t: t.replace("(thickness 1.6)", "(thickness -1.6)", 1))
    assert not isinstance(items, str) and "board thickness in the file is -1.6 mm: read as not given" in "\n".join(lines)


def test_a_board_too_thin_for_its_copper_is_refused():
    # no stackup and 0.05 mm in the file: less than the outer copper and the masks
    import re
    no_stackup = lambda t: re.sub(r"\(stackup\b.*?\n\t\t\)", "", t, count=1, flags=re.S).replace("(thickness 1.6)", "(thickness 0.05)", 1)
    said, _ = board_variant("thin.kicad_pcb", no_stackup)
    assert isinstance(said, str) and said.startswith("the dielectric between F.Cu and In1.Cu comes out -") \
        and said.endswith("the board is too thin for its copper; set Board.BOARD_THICKNESS_MM (parameters/PCB_elements/Board.py)"), said


def test_a_drill_that_gives_no_size_takes_kicads_default():
    # (drill oval (offset -0.1075 0)) with no size, on SMD pads of a KiCad 6 board, stopped the run with
    # an IndexError; KiCad's parser keeps the pad's default drill, 30 mils, and an SMD pad has no hole
    fp = ('(footprint "T:T" (layer "F.Cu") (at 110 128)'
          ' (pad "1" smd rect (at 0 0) (size 1 1.6) (drill oval (offset -0.1075 0)) (layers "F.Cu" "F.Mask"))'
          ' (pad "2" thru_hole circle (at 4 0) (size 1.5 1.5) (drill oval) (layers "*.Cu" "*.Mask"))'
          ' (pad "3" np_thru_hole circle (at 8 0) (size 0.762 0.762) (drill (offset 0 0)) (layers "*.Cu"))))')
    items, _ = board_variant("drills.kicad_pcb", lambda t: t.rstrip()[:-1] + fp + "\n")
    holes = [h for h in items.holes if abs(h.drill.centroid.y - 128) < 1e-6]
    assert [(round(h.drill.centroid.x, 6), h.plated) for h in holes] == [(114.0, True), (118.0, False)]
    disk = 3.141592653589793 * (0.762 / 2) ** 2                          # round, 30 mils across
    assert all(abs(h.drill.area / disk - 1) < 0.02 for h in holes), [h.drill.area for h in holes]
    assert items.found["copper rings on non-plated holes"] == 0        # a round pad no bigger than its drill


if __name__ == "__main__":
    run_tests(__file__)
