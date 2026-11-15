"""The values the parameter files give, which every other test file replaces with its own
(helpers.TEST_SETTINGS): a STEP file in mm with KiCad's origin, the plies separate, the solder mask
and the silkscreen left out, the finish the board file names, the Djordjevic-Sarkar model for the
laminate, the Huray model for the copper and the Verifier at the end.  A board runs with them, a
board that names no finish stops before any work, and a visual run is told to name its format.

    python -m pytest tests/test_defaults.py           (or:  python tests/test_defaults.py)"""
import contextlib
import importlib.util
import io
import json
import sys

from helpers import FEATURES, ROOT, TEST_SETTINGS, run_stages, run_tests, settings
from kese.job import start
from kese.pipeline import generate
from kese.s2_collect import collect
from kese.s4_geometry.finish import finish_layers
from parameters import STACKUPS, P

LEFT_OUT = ["top_silkscreen", "top_solder_mask", "bottom_solder_mask", "bottom_silkscreen"]


def shipped(short):
    """The parameter file `short` ("Run") read anew: its values as the file gives them."""
    path, = (ROOT / "parameters").rglob(f"{short}.py")
    spec = importlib.util.spec_from_file_location(f"shipped_{short}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# the files' values of the settings the tests replace
DEFAULTS = {key: getattr(shipped(key.split(".")[0]), key.split(".")[1]) for key in TEST_SETTINGS}


def test_the_parameter_files_give_the_defaults_for_rf_work():
    run, stackup, board, copper = shipped("Run"), shipped("Stackup"), shipped("Board"), shipped("Copper")
    assert (run.MODE, run.FILE_FORMAT, run.UNITS, run.ORIGIN) == ("simulation", ["step"], "mm", "kicad")
    assert run.WRITE_MATERIALS_JSON is True and shipped("Step").STEP_EXACT_ARCS is True
    assert stackup.FUSION_BUILD == "PLIES_SEPARATE"
    for name in STACKUPS:                                         # the mask and the silkscreen, and nothing else, left out
        assert [line for line, on in getattr(stackup, name).items() if not on] == LEFT_OUT, name
    assert shipped("Finish").FINISH_TYPE == "file"
    assert (board.DIELECTRIC_MODEL, board.DIELECTRIC_GROUPING) == ("djordjevic_sarkar", "layer")
    assert (copper.COPPER_GROUPING, copper.COPPER_ROUGHNESS_MODEL) == ("net", "huray")
    assert (copper.COPPER_HURAY_RADIUS_TREATED_UM, copper.COPPER_HURAY_RADIUS_OTHER_UM) == (0.5, 0.5)
    assert (copper.COPPER_HURAY_SURFACE_RATIO_TREATED, copper.COPPER_HURAY_SURFACE_RATIO_OTHER) == (2.9, 2.9)
    assert shipped("Verifier").VERIFY is True


def test_a_board_runs_with_the_defaults(tmp_path):
    said = []
    with settings(DEFAULTS):
        out, _ = generate(FEATURES / "29_stackup_plies.kicad_pcb", out_root=tmp_path, log=said.append)
    assert out.name == "simulation_STEP" and (out / "29_stackup_plies.step").stat().st_size > 0
    assert "  Verifier: PASS" in said, said
    report = (out / "report.txt").read_text(encoding="utf-8")
    for line in ("formats: step   units: mm", "built: PLIES_SEPARATE", "origin: KiCad page origin", "Verifier: PASS"):
        assert line in report, line
    materials = json.loads((out / "materials.json").read_text(encoding="utf-8"))
    assert materials["units_of_files"] == "mm"
    parts = materials["parts"]
    laminate = {name: p["properties"] for name, p in parts.items() if p["role"] == "board"}
    assert any(" ply " in name for name in laminate) and any(name.startswith("Board_resin ") for name in laminate)
    for name, props in laminate.items():                          # every solid of the laminate with the wideband model
        model = props["dielectric_model"]
        assert model["model"] == "djordjevic_sarkar" and model["delta_epsilon"] > 0, name
        assert props["epsilon_r"] > model["epsilon_inf"] > 1, name
    copper = [p["properties"] for p in parts.values() if p["role"] == "copper"]
    assert copper and all(c["roughness"] == {"model": "huray", "radius_treated_um": 0.5, "radius_other_um": 0.5,
                                             "surface_ratio_treated": 2.9, "surface_ratio_other": 2.9} for c in copper)
    # the finish is the file's: this board says ENIG, and no part of a mask or of a silkscreen is built
    assert {p["properties"]["metal"] for p in parts.values() if p["role"] == "finish"} == {"Nickel", "Gold"}
    assert not [name for name, p in parts.items() if p["role"].startswith(("mask", "silk"))]


def test_the_finish_is_the_board_files():
    # "Hard gold" is KiCad's name for the key HardGold; the file of 05 says "None": no finish
    for board, finish in (("18_finishes", "HardGold"), ("29_stackup_plies", "ENIG"), ("05_vias_micro", None)):
        with settings(DEFAULTS):
            items, _ = run_stages(FEATURES / f"{board}.kicad_pcb", collect)
            assert finish_layers(items.stackup)[1] == finish, board


def test_a_board_that_names_no_finish_stops_before_any_work():
    for board in ("15_stackup_none", "19b_skipped_items_k10"):
        with settings(DEFAULTS):
            try:
                run_stages(FEATURES / f"{board}.kicad_pcb", collect)                 # stage 2: nothing is built yet
            except ValueError as e:
                assert str(e).startswith("FINISH ERROR: Finish.FINISH_TYPE = \"file\" but no finish was found"), e
                assert str(e).endswith("--set Finish.FINISH_TYPE=ENIG, or --set Stackup.finish=False"), e
            else:
                raise AssertionError(f"{board} names no finish and was built")
        for way in ({"Finish.FINISH_TYPE": "ENIG"}, {"Stackup.finish": False}):      # the two ways the message gives
            with settings({**DEFAULTS, **way}):
                run_stages(FEATURES / f"{board}.kicad_pcb", collect)


def test_a_visual_run_names_its_format():
    with settings(DEFAULTS):
        try:
            start("visual")
        except ValueError as e:
            assert "asked for ['step']" in str(e) and str(e).endswith("--mode visual --format glb, or use --for viewer"), e
        else:
            raise AssertionError("a visual run was started for a STEP file")
        assert start("visual", ["glb"], log=lambda s: None).formats == ["glb"]
        with settings(P.Presets.PRESETS["viewer"]):
            job = start(log=lambda s: None)
            assert (job.mode, job.formats, P.Run.UNITS, P.Run.ORIGIN) == ("visual", ["glb"], "m", "center")


def test_the_verifier_can_be_left_out_of_one_run():
    from kese.cli import main
    argv = sys.argv
    for flag, verify in (("--no-verify", False), ("--verify", True), (None, None)):
        with settings(DEFAULTS):
            sys.argv = ["kese", "no_such_board.kicad_pcb", "--out", "nowhere"] + ([flag] if flag else [])
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    main()
            except (FileNotFoundError, SystemExit):                # the board is not there: only the settings are wanted
                pass
            finally:
                sys.argv = argv
            assert P.Verifier.VERIFY is (DEFAULTS["Verifier.VERIFY"] if verify is None else verify), flag


if __name__ == "__main__":
    run_tests(__file__)
