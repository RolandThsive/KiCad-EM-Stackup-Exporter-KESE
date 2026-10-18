"""Regression suite: every board in Tests/boards and Input/ through both modes with the Verifier on.

    python -m pytest Tests                 (or:  python Tests/test_boards.py)
    python Tests/test_boards.py --accept   re-record Tests/baseline.json after an intended geometry change

A board fails when the Verifier fails (open solid, overlap, broken skin), when a STEP solid is
invalid or has a free edge, or when a part's volume moved by more than VOLUME_TOLERANCE from the
recorded baseline (so a fix for one board cannot silently change another)."""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Generator.Pipeline import generate  # noqa: E402
from Generator.Verifier import verify  # noqa: E402

BASELINE = ROOT / "Tests" / "baseline.json"
OUT = ROOT / "Tests" / "out"
VOLUME_TOLERANCE = 1e-3          # relative, per part
BOARDS = sorted((ROOT / "Tests" / "boards").glob("*.kicad_pcb")) + sorted((ROOT / "Input").glob("*.kicad_pcb"))
STEP_BOARDS = {"one_layer", "six_layer", "synthetic"}   # small enough to write and audit STEP every run


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
    formats = ["glb"] + (["step"] if mode == "simulation" and pcb.stem in STEP_BOARDS else [])
    out_dir, model = generate(pcb, mode=mode, formats=formats, out_root=OUT, verify=False, log=lambda s: None)
    ok, lines = verify(model)
    scale = 1000.0 if model.units == "m" else 1.0
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
    problems = [] if ok else [l for l in lines[1:] if "False" in l or "worst" in l]
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
        metafunc.parametrize("pcb,mode", [(p, m) for p in BOARDS for m in ("simulation", "visual")],
                             ids=[f"{p.stem}-{m}" for p in BOARDS for m in ("simulation", "visual")])


def test_board(pcb, mode):
    problems, _ = check(pcb, mode, load_baseline())
    assert not problems, "\n".join(problems)


# ---- plain python entry -----------------------------------------------------------------------------------
if __name__ == "__main__":
    accept = "--accept" in sys.argv
    shutil.rmtree(OUT, ignore_errors=True)
    baseline, failed = load_baseline(), 0
    for pcb in BOARDS:
        for mode in ("simulation", "visual"):
            problems, volumes = check(pcb, mode, {} if accept else baseline)
            key = f"{pcb.stem}/{mode}"
            if accept:
                baseline[key] = {k: round(v, 9) for k, v in sorted(volumes.items())}
            failed += bool(problems)
            print(f"{key:48s} {'FAIL' if problems else 'ok'}")
            for p in problems:
                print("    " + p)
    if accept:
        BASELINE.write_text(json.dumps(baseline, indent=1))
        print(f"baseline written: {BASELINE}")
    sys.exit(1 if failed else 0)
