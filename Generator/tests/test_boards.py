"""Regression suite: every board in tests/boards, featureTest/ and Input/ through every output with
the Verifier on: simulation mode written as GLB, STL and STEP, visual mode as GLB (visual mode is a
surface, so it writes no solids: no STL or STEP).  Every board runs with the parameters in
parameters/, but for the changes ALL_PARTS and SETTINGS list for it.

    python -m pytest tests                 (or:  python tests/test_boards.py)
    python tests/test_boards.py --accept   re-record tests/baseline.json after an intended geometry change
    python tests/test_boards.py --add      record only the boards the baseline does not have yet
    python tests/test_boards.py --accept 18_finishes 18b_finish_pads   only the boards named (by file name)
    python tests/test_boards.py --faceted  the STEP files with flat faces only (Run.STEP_EXACT_ARCS = False)

A board fails when the Verifier fails (open solid, overlap, broken skin), when a STEP solid is
invalid, has a free edge or is not read back, when an STL file is missing, not closed or not its
part's volume, or when a part's volume moved by more than VOLUME_TOLERANCE from the recorded
baseline (so a fix for one board cannot silently change another).

Run on its own (python tests/test_boards.py), the suite reads the STEP files back in AUDITORS
background processes while it exports the next boards, and prints a board's line once its STEP file
is checked, in the order the boards ran."""
import json
import multiprocessing
import os
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

from kese.core.mesh import Mesh  # noqa: E402
from kese.core.names import model_file_names  # noqa: E402
from kese.pipeline import generate  # noqa: E402
from kese.s7_write.stl import TRIANGLE  # noqa: E402
from kese.s8_verify.verify import every_check  # noqa: E402
from parameters import P  # noqa: E402
from step_audit import step_audit  # noqa: E402

BASELINE = ROOT / "tests" / "baseline.json"
OUT = ROOT / "tests" / "out"
VOLUME_TOLERANCE = 1e-3          # relative, per part
AUDITORS = 2                     # background processes reading STEP files back (plain python entry)
FEATURES = sorted((ROOT.parent / "featureTest").glob("*.kicad_pcb"))
# the boards of Input/ that featureTest/ holds too, byte for byte (21_rf_module is rf_module), run once
COPIES = {p.read_bytes() for p in FEATURES}
BOARDS = (sorted((ROOT / "tests" / "boards").glob("*.kicad_pcb")) + FEATURES
          + [p for p in sorted((ROOT / "Input").glob("*.kicad_pcb")) if p.read_bytes() not in COPIES])
MODES = ("simulation", "visual")
FORMATS = {"simulation": ["glb", "stl", "step"], "visual": ["glb"]}
# Boards run with other values than parameters/ has, as {board stem: {"Module.NAME": value}}: the
# boards made for a setting that is off by default.  Every board also runs with ALL_PARTS: the solder
# mask and silkscreen are off by default, but the suite checks every part.
# The boards whose stack-up names a finish other than ENIG (Finish.FINISH_TYPE's default) run with
# FINISH_TYPE = "file", so that their own finish is built and the names are read from the file.
FILE_FINISH = {"Finish.FINISH_TYPE": "file"}
ALL_PARTS = {"SolderMask.SOLDER_MASK_ENABLED": True, "Silkscreen.SILKSCREEN_ENABLED": True}
SETTINGS = {"16_edge_plating_castellation": FILE_FINISH, "17_mask_silk": FILE_FINISH, "18_finishes": FILE_FINISH,
            "22_hdi_module": FILE_FINISH, "23_pcie_card": FILE_FINISH,
            "17b_silk_over_copper": {"Silkscreen.SILKSCREEN_OVER_COPPER": True},
            "18c_finish_before_mask": {"Finish.FINISH_BEFORE_SOLDER_MASK": True, **FILE_FINISH}}


@contextmanager
def settings_for(pcb):
    """ALL_PARTS and the board's SETTINGS, applied for one run and put back after it; -> the (key,
    value) pairs."""
    changes = {**ALL_PARTS, **SETTINGS.get(pcb.stem, {})}
    saved = {key: getattr(getattr(P, key.split(".")[0]), key.split(".")[1]) for key in changes}
    for key, value in changes.items():
        P.override(key, value)
    try:
        yield tuple(changes.items())
    finally:
        for key, value in saved.items():
            P.override(key, value)


def read_stl(path):
    """A binary STL file as a Mesh, corners at the same point joined into one vertex."""
    data = path.read_bytes()
    count = int(np.frombuffer(data, "<u4", 1, 80)[0])
    corners = np.frombuffer(data, TRIANGLE, count, 84)["vertices"].reshape(-1, 3)
    vertices, faces = np.unique(corners, axis=0, return_inverse=True)
    return Mesh(vertices.astype(float), faces.reshape(-1, 3))


def stl_problems(out_dir, model):
    """What is wrong with the STL files of one run: each part read back from its own file must be
    there, be closed and have the part's volume (within VOLUME_TOLERANCE).  STL holds its corners
    as 32-bit floats, which moves a corner by up to a few nm on a board a few cm across: on an 80 nm
    gold finish that is a few tenths of a percent of its volume.  So the volume read back is held
    against the part's mesh with its corners rounded the same way, which the file must give back
    as written."""
    problems, names = [], model_file_names(model)
    for part, mesh in model.meshes.items():
        path = out_dir / "stl" / f"{names[part]}.stl"
        if not path.exists():
            problems.append(f"STL: {path.name} missing")
            continue
        back = read_stl(path)
        if not back.is_watertight:
            problems.append(f"STL: {path.name} is not closed")
            continue
        written = Mesh(mesh.vertices.astype(np.float32).astype(float), mesh.faces).volume
        if abs(back.volume - written) > VOLUME_TOLERANCE * max(abs(written), 1e-30):
            problems.append(f"STL: {path.name} volume {written:.6g} -> {back.volume:.6g} read back")
    return problems


def run_board(pcb, mode, audit=step_audit):
    """-> (verifier ok, verifier lines, {part: volume mm3}, what `audit` gave for the STEP file or
    None, the STL problems).  The suite's own loop passes an `audit` that hands the file to a
    background process."""
    formats = FORMATS[mode]
    with settings_for(pcb) as overrides:
        out_dir, model = generate(pcb, mode=mode, formats=formats, out_root=OUT, overrides=overrides, verify=False,
                                  log=lambda s: None)
        ok, lines = every_check(model)
    stl = stl_problems(out_dir, model) if "stl" in formats else []
    scale = 1000.0 if model.units == "m" else 1.0
    with np.errstate(divide="ignore", invalid="ignore"):     # a skin part with no volume has no centre either
        volumes = {part: float(m.volume) * scale ** 3 for part, m in model.meshes.items()}
    step = None
    if "step" in formats:
        try:
            step = audit(out_dir / f"{pcb.stem}.step")
        except ImportError:                     # OCP is not installed: the STEP file is not checked
            step = None
    return ok, lines, volumes, step, stl


def step_problems(step):
    """The problem line of a STEP audit, (invalid solids, free edges, seconds, solids left out) or None."""
    if not step or (step[0], step[1], step[3]) == (0, 0, 0):
        return []
    return [f"STEP: {step[0]} invalid solids, {step[1]} free edges, {step[3]} solids not read back"]


def check(pcb, mode, baseline, audit=step_audit):
    """-> (problems but the STEP file's, {part: volume mm3}, what `audit` gave for the STEP file)"""
    ok, lines, volumes, step, stl = run_board(pcb, mode, audit)
    problems = [] if ok else [l.strip() for l in lines[1:] if "False" in l or "worst" in l or "alternate" in l] \
        or ["Verifier: FAIL"]
    problems += stl
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


# ---- continuous integration ---------------------------------------------------------------------------------
# .github/workflows/RegressionTests.yml splits the suite over several machines with two environment
# variables.  Run without them, the suite runs every board on one machine as before.
#   KESE_RUN=board/mode        run only this one run, e.g. 21_rf_module/simulation
#   KESE_SHARD=i/n             run only the i-th of n near-equal shares of the runs HEAVY does not list
# The runs whose STEP file takes minutes to read back: each gets a machine of its own in CI, where the
# file is read back in one process per core (step_audit.py).  The other runs take about 15 minutes of
# processor time in all.
HEAVY = {"21_rf_module/simulation", "22_hdi_module/simulation", "23_pcie_card/simulation"}


def shard(runs, spec):
    """The `spec` ("i/n", i from 1) share of the (board, mode) runs.  The runs are dealt longest first,
    each to the share with the least work so far, by the board file's size and the mode's cost
    (simulation also writes STL and STEP files and reads them back), so the shares take about as long."""
    i, n = (int(x) for x in spec.split("/"))
    if not 1 <= i <= n:
        sys.exit(f"KESE_SHARD={spec}: i must be 1 to n")
    cost = {"simulation": 4.0, "visual": 1.0}
    work = {run: (run[0].stat().st_size + 50_000) * cost[run[1]] for run in runs}    # a fixed cost per run, too
    load, share = [0.0] * n, [[] for _ in range(n)]
    for run in sorted(runs, key=lambda r: (-work[r], r[0].stem, r[1])):
        k = load.index(min(load))
        load[k] += work[run]
        share[k].append(run)
    return sorted(share[i - 1], key=lambda r: (BOARDS.index(r[0]), MODES.index(r[1])))


def ci_runs():
    """The (board, mode) runs, after KESE_RUN and KESE_SHARD."""
    runs = [(p, m) for p in BOARDS for m in MODES]
    one = os.environ.get("KESE_RUN")
    if one:
        runs = [r for r in runs if f"{r[0].stem}/{r[1]}" == one]
        if not runs:
            sys.exit(f"KESE_RUN={one}: no such board/mode")
        return runs
    spec = os.environ.get("KESE_SHARD")
    return shard([r for r in runs if f"{r[0].stem}/{r[1]}" not in HEAVY], spec) if spec else runs


def audit_workers():
    """Processes to read a big STEP file back in: one per core, but one under pytest-xdist, whose
    workers already keep every core busy."""
    return 1 if os.environ.get("PYTEST_XDIST_WORKER") else os.cpu_count() or 1


# ---- pytest entry -----------------------------------------------------------------------------------------
def pytest_generate_tests(metafunc):
    if not os.environ.get("PYTEST_XDIST_WORKER"):       # pytest-xdist workers share OUT: none may clear it
        shutil.rmtree(OUT, ignore_errors=True)
    if "pcb" in metafunc.fixturenames:
        runs = ci_runs()
        metafunc.parametrize("pcb,mode", runs, ids=[f"{p.stem}-{m}" for p, m in runs])


def test_board(pcb, mode):
    problems, _, step = check(pcb, mode, load_baseline(), lambda path: step_audit(path, audit_workers()))
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
    if "--faceted" in args:
        P.override("Run.STEP_EXACT_ARCS", False)
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
