"""Regression suite: every board in tests/boards, featureTest/ and Input/ through every output with
the Verifier on: simulation mode written as GLB and STEP, visual mode as GLB.

    python -m pytest tests                 (or:  python tests/test_boards.py)
    python tests/test_boards.py --accept   re-record tests/baseline.json after an intended geometry change
    python tests/test_boards.py --add      record only the boards the baseline does not have yet

A board fails when the Verifier fails (open solid, overlap, broken skin), when a STEP solid is
invalid or has a free edge, or when a part's volume moved by more than VOLUME_TOLERANCE from the
recorded baseline (so a fix for one board cannot silently change another)."""
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from kese.pipeline import generate  # noqa: E402
from kese.s8_verify.verify import every_check  # noqa: E402

BASELINE = ROOT / "tests" / "baseline.json"
OUT = ROOT / "tests" / "out"
VOLUME_TOLERANCE = 1e-3          # relative, per part
BOARDS = (sorted((ROOT / "tests" / "boards").glob("*.kicad_pcb")) + sorted((ROOT.parent / "featureTest").glob("*.kicad_pcb"))
          + sorted((ROOT / "Input").glob("*.kicad_pcb")))
MODES = ("simulation", "visual")
FORMATS = {"simulation": ["glb", "step"], "visual": ["glb"]}


def step_audit(path):
    """(invalid solids, free edges) of a STEP file, via OCP."""
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.STEPControl import STEPControl_Reader
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID
    from OCP.TopExp import TopExp, TopExp_Explorer
    from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
    rd = STEPControl_Reader()
    rd.ReadFile(str(path))
    rd.TransferRoots()
    ex, invalid, free = TopExp_Explorer(rd.OneShape(), TopAbs_SOLID), 0, 0
    while ex.More():
        s = ex.Current()
        invalid += not BRepCheck_Analyzer(s).IsValid()
        m = TopTools_IndexedDataMapOfShapeListOfShape()
        TopExp.MapShapesAndAncestors_s(s, TopAbs_EDGE, TopAbs_FACE, m)
        free += sum(1 for i in range(1, m.Extent() + 1) if m.FindFromIndex(i).Size() < 2)
        ex.Next()
    return invalid, free


def run_board(pcb, mode):
    """-> (verifier ok, verifier lines, {part: volume mm3}, step problems or None)"""
    formats = FORMATS[mode]
    out_dir, model = generate(pcb, mode=mode, formats=formats, out_root=OUT, verify=False, log=lambda s: None)
    ok, lines = every_check(model)
    scale = 1000.0 if model.units == "m" else 1.0
    with np.errstate(divide="ignore", invalid="ignore"):     # a skin part with no volume has no centre either
        volumes = {part: float(m.volume) * scale ** 3 for part, m in model.meshes.items()}
    step = None
    if "step" in formats:
        try:
            step = step_audit(out_dir / f"{pcb.stem}.step")
        except ImportError:
            step = None
    return ok, lines, volumes, step


def check(pcb, mode, baseline):
    ok, lines, volumes, step = run_board(pcb, mode)
    problems = [] if ok else [l.strip() for l in lines[1:] if "False" in l or "worst" in l or "alternate" in l] \
        or ["Verifier: FAIL"]
    if step and step != (0, 0):
        problems.append(f"STEP: {step[0]} invalid solids, {step[1]} free edges")
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
    return problems, volumes


def load_baseline():
    return json.loads(BASELINE.read_text()) if BASELINE.exists() else {}


# ---- pytest entry -----------------------------------------------------------------------------------------
def pytest_generate_tests(metafunc):
    shutil.rmtree(OUT, ignore_errors=True)
    if "pcb" in metafunc.fixturenames:
        metafunc.parametrize("pcb,mode", [(p, m) for p in BOARDS for m in MODES],
                             ids=[f"{p.stem}-{m}" for p in BOARDS for m in MODES])


def test_board(pcb, mode):
    problems, _ = check(pcb, mode, load_baseline())
    assert not problems, "\n".join(problems)


# ---- plain python entry -----------------------------------------------------------------------------------
if __name__ == "__main__":
    accept, add = "--accept" in sys.argv, "--add" in sys.argv
    shutil.rmtree(OUT, ignore_errors=True)
    baseline, failed = load_baseline(), 0
    for pcb in BOARDS:
        for mode in MODES:
            key = f"{pcb.stem}/{mode}"
            record = accept or (add and key not in baseline)
            t0 = time.perf_counter()
            problems, volumes = check(pcb, mode, {} if record else baseline)
            if record:
                baseline[key] = {k: round(v, 9) for k, v in sorted(volumes.items())}
            failed += bool(problems)
            print(f"{key:56s} {'FAIL' if problems else 'ok':4s} {time.perf_counter() - t0:7.1f} s", flush=True)
            for p in problems:
                print("    " + p, flush=True)
    if accept or add:
        BASELINE.write_text(json.dumps(baseline, indent=1))
        print(f"baseline written: {BASELINE}")
    sys.exit(1 if failed else 0)
