"""Regression suite: every board in tests/boards, featureTest/ and Input/ through every output with
the Verifier on: simulation mode written as GLB and STEP, visual mode as GLB.  Every board runs with
the parameters in parameters/, but for the changes SETTINGS lists for it.

    python -m pytest tests                 (or:  python tests/test_boards.py)
    python tests/test_boards.py --accept   re-record tests/baseline.json after an intended geometry change
    python tests/test_boards.py --add      record only the boards the baseline does not have yet
    python tests/test_boards.py --accept 18_finishes 18b_finish_pads   only the boards named (by file name)

A board fails when the Verifier fails (open solid, overlap, broken skin), when a STEP solid is
invalid or has a free edge, or when a part's volume moved by more than VOLUME_TOLERANCE from the
recorded baseline (so a fix for one board cannot silently change another).

Run on its own (python tests/test_boards.py), the suite reads the STEP files back in AUDITORS
background processes while it exports the next boards, and prints a board's line once its STEP file
is checked, in the order the boards ran."""
import json
import multiprocessing
import shutil
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402

from kese.pipeline import generate  # noqa: E402
from kese.s8_verify.verify import every_check  # noqa: E402
from parameters import P  # noqa: E402
from step_audit import step_audit  # noqa: E402

BASELINE = ROOT / "tests" / "baseline.json"
OUT = ROOT / "tests" / "out"
VOLUME_TOLERANCE = 1e-3          # relative, per part
AUDITORS = 2                     # background processes reading STEP files back (plain python entry)
BOARDS = (sorted((ROOT / "tests" / "boards").glob("*.kicad_pcb")) + sorted((ROOT.parent / "featureTest").glob("*.kicad_pcb"))
          + sorted((ROOT / "Input").glob("*.kicad_pcb")))
MODES = ("simulation", "visual")
FORMATS = {"simulation": ["glb", "step"], "visual": ["glb"]}
# Boards run with other values than parameters/ has: the finish boards with the finish on, which is
# off by default (Finish.FINISH_ENABLED), so that the finish parts are built and checked too
SETTINGS = {"18_finishes": {"Finish.FINISH_ENABLED": True},
            "18b_finish_pads": {"Finish.FINISH_ENABLED": True}}


@contextmanager
def settings_for(pcb):
    """The board's SETTINGS, applied for one run and put back after it; -> the (key, value) pairs."""
    changes = SETTINGS.get(pcb.stem, {})
    saved = {key: getattr(getattr(P, key.split(".")[0]), key.split(".")[1]) for key in changes}
    for key, value in changes.items():
        P.override(key, value)
    try:
        yield tuple(changes.items())
    finally:
        for key, value in saved.items():
            P.override(key, value)


def run_board(pcb, mode, audit=step_audit):
    """-> (verifier ok, verifier lines, {part: volume mm3}, what `audit` gave for the STEP file or
    None).  The suite's own loop passes an `audit` that hands the file to a background process."""
    formats = FORMATS[mode]
    with settings_for(pcb) as overrides:
        out_dir, model = generate(pcb, mode=mode, formats=formats, out_root=OUT, overrides=overrides, verify=False,
                                  log=lambda s: None)
        ok, lines = every_check(model)
    scale = 1000.0 if model.units == "m" else 1.0
    with np.errstate(divide="ignore", invalid="ignore"):     # a skin part with no volume has no centre either
        volumes = {part: float(m.volume) * scale ** 3 for part, m in model.meshes.items()}
    step = None
    if "step" in formats:
        try:
            step = audit(out_dir / f"{pcb.stem}.step")
        except ImportError:                     # OCP is not installed: the STEP file is not checked
            step = None
    return ok, lines, volumes, step


def step_problems(step):
    """The problem line of a STEP audit, (invalid solids, free edges, seconds) or None."""
    return [f"STEP: {step[0]} invalid solids, {step[1]} free edges"] if step and step[:2] != (0, 0) else []


def check(pcb, mode, baseline, audit=step_audit):
    """-> (problems but the STEP file's, {part: volume mm3}, what `audit` gave for the STEP file)"""
    ok, lines, volumes, step = run_board(pcb, mode, audit)
    problems = [] if ok else [l.strip() for l in lines[1:] if "False" in l or "worst" in l or "alternate" in l] \
        or ["Verifier: FAIL"]
    key = f"{pcb.stem}/{mode}"
    for part, vol in baseline.get(key, {}).items():
        now = volumes.get(part)
        if now is None:
            problems.append(f"part {part!r} disappeared")
        elif abs(now - vol) > VOLUME_TOLERANCE * max(abs(vol), 1e-9):
            problems.append(f"{part}: volume {vol:.6f} -> {now:.6f} mm3")
    for part in volumes:
        if key in baseline and part not in baseline[key]:
            problems.append(f"new part {part!r}")
    return problems, volumes, step


def load_baseline():
    return json.loads(BASELINE.read_text()) if BASELINE.exists() else {}


# ---- pytest entry -----------------------------------------------------------------------------------------
def pytest_generate_tests(metafunc):
    shutil.rmtree(OUT, ignore_errors=True)
    if "pcb" in metafunc.fixturenames:
        metafunc.parametrize("pcb,mode", [(p, m) for p in BOARDS for m in MODES],
                             ids=[f"{p.stem}-{m}" for p in BOARDS for m in MODES])


def test_board(pcb, mode):
    problems, _, step = check(pcb, mode, load_baseline())
    problems += step_problems(step)
    assert not problems, "\n".join(problems)


# ---- plain python entry -----------------------------------------------------------------------------------
def report(queue, wait):
    """Print the boards at the head of the queue whose STEP file is checked (all of them when
    `wait`), in the order they ran; -> how many of them failed."""
    failed = 0
    while queue and (wait or queue[0][3] is None or queue[0][3].done()):
        key, problems, seconds, step = queue.pop(0)
        read_back = ""
        if step is not None:
            try:
                step = step.result()
                problems += step_problems(step)
                read_back = f"   STEP read back in {step[2]:.1f} s"
            except ImportError:                 # OCP is not installed: the STEP file is not checked
                pass
        failed += bool(problems)
        print(f"{key:56s} {'FAIL' if problems else 'ok':4s} {seconds:7.1f} s{read_back}", flush=True)
        for p in problems:
            print("    " + p, flush=True)
    return failed


def main(args):
    accept, add = "--accept" in args, "--add" in args
    named = [a for a in args if not a.startswith("--")]
    unknown = sorted(set(named) - {p.stem for p in BOARDS})
    if unknown:
        sys.exit(f"no such board: {', '.join(unknown)}")
    shutil.rmtree(OUT, ignore_errors=True)
    baseline, queue, failed = load_baseline(), [], 0
    with ProcessPoolExecutor(AUDITORS, mp_context=multiprocessing.get_context("spawn")) as pool:
        for pcb in [p for p in BOARDS if p.stem in named] if named else BOARDS:
            for mode in MODES:
                key = f"{pcb.stem}/{mode}"
                record = accept or (add and key not in baseline)
                t0 = time.perf_counter()
                problems, volumes, step = check(pcb, mode, {} if record else baseline,
                                                lambda path: pool.submit(step_audit, path))
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
