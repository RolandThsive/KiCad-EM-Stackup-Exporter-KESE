"""Regression suite: every board in tests/boards, featureTest/ and Input/ through every output with
the Verifier on: simulation mode written as GLB and STEP, visual mode as GLB.  Every board runs with
the settings the tests start from (helpers.TEST_SETTINGS: the plies fused, ENIG, metres, the board
centred, as tests/baseline.json was recorded) and the changes SETTINGS lists for it; the boards of
SEPARATE_TOO run a second time with the plies of the laminate built apart.

    python -m pytest tests                 (or:  python tests/test_boards.py)
    python tests/test_boards.py --accept   re-record tests/baseline.json after an intended geometry change
    python tests/test_boards.py --add      record only the boards the baseline does not have yet
    python tests/test_boards.py --accept 18_finishes 18b_finish_pads   only the boards named (by file name)
    python tests/test_boards.py --faceted  the STEP files with flat faces only (Step.STEP_EXACT_ARCS = False)
    python tests/test_boards.py --healed   read the STEP files back with OpenCascade's healing (slower)

A board fails when the Verifier fails (open solid, overlap, broken skin), when a STEP solid is
invalid or has a free edge, or when a part's volume moved by more than VOLUME_TOLERANCE from the
recorded baseline (so a fix for one board cannot silently change another).

Run on its own (python tests/test_boards.py), the suite reads the STEP files back part by part in
AUDITORS background processes while it exports the next boards, and prints a board's line once
every part of its STEP file is checked, in the order the boards ran.  The STEP files are read as
written, without OpenCascade's healing (tests/step_audit.py says what is still added before the
check)."""
import json
import multiprocessing
import shutil
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import helpers
from helpers import ROOT, settings
from kese.core.parallel import process_limit, processor_threads
from kese.pipeline import generate
from kese.s8_verify.verify import every_check
from parameters import P
from step_audit import audit_part, parts, step_audit, total

BASELINE = ROOT / "tests" / "baseline.json"
OUT = ROOT / "tests" / "out"
VOLUME_TOLERANCE = 1e-3          # relative, per part
# background processes reading STEP files back (plain python entry): one per processor thread, as
# each holds one part of a file in OpenCascade, not the whole file (gigabytes for the biggest boards)
AUDITORS = process_limit(max(2, processor_threads()))
FEATURES = sorted(helpers.FEATURES.glob("*.kicad_pcb"))
# the boards of Input/ that featureTest/ holds too, byte for byte (21_rf_module is rf_module), run once
COPIES = {p.read_bytes() for p in FEATURES}
BOARDS = (sorted(helpers.BOARDS.glob("*.kicad_pcb")) + FEATURES
          + [p for p in sorted((ROOT / "Input").glob("*.kicad_pcb")) if p.read_bytes() not in COPIES])
MODES = ("simulation", "visual")
FORMATS = {"simulation": ["glb", "step"], "visual": ["glb"]}
# Boards run with other values than the tests start from, as {board stem: {"Module.NAME": value}}:
# the boards made for a setting that is off by default.  Every board also runs with ALL_PARTS: the
# solder mask and silkscreen are off by default, but the suite checks every part.
# The boards whose stack-up names a finish other than ENIG (the tests' Finish.FINISH_TYPE) run with
# FINISH_TYPE = "file", the parameter files' own value, so that their own finish is built and the
# names are read from the file.
FILE_FINISH = {"Finish.FINISH_TYPE": "file"}
ALL_PARTS = {"Stackup.solder_mask": True, "Stackup.silkscreen": True}
SETTINGS = {"16_edge_plating_castellation": FILE_FINISH, "17_mask_silk": FILE_FINISH, "18_finishes": FILE_FINISH,
            "22_hdi_module": FILE_FINISH, "23_pcie_card": FILE_FINISH,
            "17b_silk_over_copper": {"SilkScreen.SILKSCREEN_OVER_COPPER": True},
            "18c_finish_before_mask": {"Finish.FINISH_BEFORE_SOLDER_MASK": True, **FILE_FINISH}}
# The boards that run a second time with the plies separate (Stackup.FUSION_BUILD), recorded as
# "<board>+plies_separate": those whose gaps are laid up of plies, and boards whose laminate is cut
# by what ends inside it (blind vias, backdrills, counterbores, countersinks, via plugs)
PLIES_SEPARATE = {"Stackup.FUSION_BUILD": "PLIES_SEPARATE"}
VARIANT = "+plies_separate"
SEPARATE_TOO = ("04_vias_blind_buried", "14_stackup_full", "22_hdi_module", "24_backdrills", "25_post_machining",
                "26_via_protection", "29_stackup_plies", "29b_stackup_plies_machined", "29c_stackup_frequency",
                "29d_stackup_real")
RUNS = [(p, "") for p in BOARDS] + [(p, VARIANT) for p in BOARDS if p.stem in SEPARATE_TOO]


def run_board(pcb, mode, audit=step_audit, variant=""):
    """-> (verifier ok, verifier lines, {part: volume mm3}, what `audit` gave for the STEP file or
    None).  The suite's own loop passes an `audit` that hands the file's parts to background
    processes.  variant: "" or VARIANT, the run with the plies separate, written to a folder of its own."""
    formats = FORMATS[mode]
    changes = {**ALL_PARTS, **SETTINGS.get(pcb.stem, {}), **(PLIES_SEPARATE if variant else {})}
    with settings(changes):
        out_dir, model = generate(pcb, mode=mode, formats=formats, out_root=OUT / variant.strip("+"),
                                  overrides=tuple(changes.items()), verify=False, log=lambda s: None)
        ok, lines = every_check(model)
    scale = 1000.0 if model.units == "m" else 1.0
    with np.errstate(divide="ignore", invalid="ignore"):     # a skin part with no volume has no centre either
        volumes = {part: float(m.volume) * scale ** 3 for part, m in model.meshes.items()}
    step = None
    if "step" in formats:
        try:
            step = audit(out_dir / f"{pcb.stem}.step")
        except ImportError as e:                # OCP is not installed, or lacks what the check uses
            warnings.warn(f"STEP file not read back: {e}", stacklevel=1)
    return ok, lines, volumes, step


def step_problems(step):
    """The problem line of a STEP audit, (invalid solids, free edges, seconds) or None."""
    return [f"STEP: {step[0]} invalid solids, {step[1]} free edges"] if step and step[:2] != (0, 0) else []


def check(pcb, mode, baseline, audit=step_audit, variant=""):
    """-> (problems but the STEP file's, {part: volume mm3}, what `audit` gave for the STEP file)"""
    ok, lines, volumes, step = run_board(pcb, mode, audit, variant)
    problems = [] if ok else [l.strip() for l in lines[1:] if "False" in l or "worst" in l or "alternate" in l] \
        or ["Verifier: FAIL"]
    key = f"{pcb.stem}{variant}/{mode}"
    for part, vol in baseline.get(key, {}).items():
        now = volumes.get(part)
        if now is None:
            problems.append(f"part {part!r} disappeared")
        elif abs(now - vol) > VOLUME_TOLERANCE * max(abs(vol), 1e-9):
            problems.append(f"{part}: volume {vol:.6f} -> {now:.6f} mm3")
    if key in baseline:
        problems += [f"new part {part!r}" for part in volumes if part not in baseline[key]]
    return problems, volumes, step


def load_baseline():
    return json.loads(BASELINE.read_text()) if BASELINE.exists() else {}


# ---- pytest entry -----------------------------------------------------------------------------------------
def pytest_generate_tests(metafunc):
    shutil.rmtree(OUT, ignore_errors=True)
    if "pcb" in metafunc.fixturenames:
        metafunc.parametrize("pcb,mode,variant", [(p, m, v) for p, v in RUNS for m in MODES],
                             ids=[f"{p.stem}{v}-{m}" for p, v in RUNS for m in MODES])


def test_board(pcb, mode, variant):
    problems, _, step = check(pcb, mode, load_baseline(), variant=variant)
    problems += step_problems(step)
    assert not problems, "\n".join(problems)


# ---- plain python entry -----------------------------------------------------------------------------------
def report(queue, wait):
    """Print the boards at the head of the queue whose STEP file is checked (all of them when
    `wait`), in the order they ran; -> how many of them failed."""
    failed = 0
    while queue and (wait or queue[0][3] is None or all(f.done() for f in queue[0][3])):
        key, problems, seconds, step = queue.pop(0)
        read_back = ""
        if step is not None:
            try:
                parts_read, step = len(step), total([f.result() for f in step])
                problems += step_problems(step)
                read_back = f"   STEP read back: {parts_read} parts, {step[2]:.1f} s"
            except ImportError as e:            # OCP is not installed, or lacks what the check uses
                read_back = f"   STEP not read back: {e}"
            except Exception as e:              # a part that did not read back, or a process that died
                problems.append(f"STEP read-back failed: {e}")
        failed += bool(problems)
        print(f"{key:56s} {'FAIL' if problems else 'ok':4s} {seconds:7.1f} s{read_back}", flush=True)
        for p in problems:
            print("    " + p, flush=True)
    return failed


def main(args):
    flags = {"--accept", "--add", "--faceted", "--healed"}
    wrong = sorted(a for a in args if a.startswith("--") and a not in flags)
    if wrong:
        sys.exit(f"unknown option: {', '.join(wrong)} (the options are {', '.join(sorted(flags))})")
    accept, add = "--accept" in args, "--add" in args
    if "--faceted" in args:
        P.override("Step.STEP_EXACT_ARCS", False)
    healed = "--healed" in args
    named = [a for a in args if not a.startswith("--")]
    unknown = sorted(set(named) - {p.stem for p in BOARDS})
    if unknown:
        sys.exit(f"no such board: {', '.join(unknown)}")
    shutil.rmtree(OUT, ignore_errors=True)
    baseline, queue, failed = load_baseline(), [], 0
    with ProcessPoolExecutor(AUDITORS, mp_context=multiprocessing.get_context("spawn")) as pool:
        for pcb, variant in [(p, v) for p, v in RUNS if p.stem in named] if named else RUNS:
            for mode in MODES:
                key = f"{pcb.stem}{variant}/{mode}"
                record = accept or (add and key not in baseline)
                t0 = time.perf_counter()
                problems, volumes, step = check(pcb, mode, {} if record else baseline, lambda path: [
                    pool.submit(audit_part, job, healed) for job in parts(path)], variant)
                if record:
                    baseline[key] = {k: round(v, 9) for k, v in sorted(volumes.items())}
                queue.append((key, problems, time.perf_counter() - t0, step))
                failed += report(queue, wait=False)
        failed += report(queue, wait=True)
    if accept or add:
        BASELINE.write_text(json.dumps(baseline, indent=1) + "\n")
        print(f"baseline written: {BASELINE}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
