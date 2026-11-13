"""What the test files share: the folders, KESE's own folder on the import path, the settings every
test starts from, settings changed for a block and put back after it, a board run through the first
stages in this process, and the plain-python run of a file's tests (python tests/test_x.py), which
pytest does not need."""
import copy
import importlib
import inspect
import sys
import tempfile
import traceback
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]                # Generator/
sys.path.insert(0, str(ROOT))
BOARDS = ROOT / "tests" / "boards"
FEATURES = ROOT.parent / "featureTest"

# The settings every test starts from.  The tests, and tests/baseline.json, were written for a GLB in
# metres with the board centred, the plies fused, ENIG on every board, er and tan d the same at
# every frequency, smooth copper and no Verifier, and each test changes what it tests.  The
# parameter files give other values (STEP in mm, the plies separate, the finish from the board file:
# the defaults for RF work), which tests/test_defaults.py tests.
TEST_SETTINGS = {
    "Run.FILE_FORMAT": ["glb"], "Run.UNITS": "m", "Run.ORIGIN": "center",
    "Stackup.FUSION_BUILD": "PLIES_FUSED", "Finish.FINISH_TYPE": "ENIG",
    "Board.DIELECTRIC_MODEL": "constant", "Copper.COPPER_ROUGHNESS_MODEL": "none",
    "Copper.COPPER_HURAY_SURFACE_RATIO_TREATED": 1.0, "Copper.COPPER_HURAY_SURFACE_RATIO_OTHER": 1.0,
    "Verifier.VERIFY": False,
}


def start_settings():
    """Set TEST_SETTINGS: once, when this file is imported (the parameters are no KESE code, so
    test_layout.py still imports none)."""
    from parameters import P
    for key, value in TEST_SETTINGS.items():
        P.override(key, value)


def setting(key):
    """The value of a setting, "Module.NAME"."""
    from parameters import P                            # here: test_layout.py imports no KESE code
    return P.value(key)


@contextmanager
def settings(changes):
    """The settings {"Module.NAME": value} for the block, put back after it.  A line of the stack-ups
    ("Stackup.top_finish") or a short name for several ("Stackup.finish") is set in both stack-ups,
    and both are put back whole."""
    from parameters import STACKUPS, P
    lines = [key for key in changes if key.startswith("Stackup.") and not key.split(".")[1].isupper()]
    saved = {key: setting(key) for key in changes if key not in lines}
    stackups = {name: copy.deepcopy(getattr(P.Stackup, name)) for name in STACKUPS} if lines else {}
    try:
        for key, value in changes.items():
            P.override(key, value)
        yield
    finally:
        for key, value in saved.items():
            P.override(key, value)
        for name, stackup in stackups.items():
            if isinstance(getattr(P.Stackup, name), dict):      # (a test may have set the whole stack-up to something else)
                getattr(P.Stackup, name).clear()
                getattr(P.Stackup, name).update(stackup)
            else:
                setattr(P.Stackup, name, stackup)


def run_stages(pcb, last, mode="simulation", formats=("glb",), verify=False, out_root=None):
    """A board through the stages from read to `last` (a stage's module, as kese.pipeline.STAGES
    lists them) in this process, quietly: -> (what `last` made, the Job)."""
    from kese.job import start
    from kese.pipeline import STAGES
    job = start(mode, list(formats), out_root, (), verify, lambda s: None)
    out = str(pcb)
    try:
        for stage in STAGES[:STAGES.index(last) + 1]:
            out = stage.run(out, job)
    finally:
        job.status.stop()
    return out, job


def run_tests(path):
    """Every test_ function of the test file at `path`, in turn, as pytest runs them: one that takes
    tmp_path is given a new temporary folder.  A line per test, and exit status 1 if any failed.
    The file is imported by its name, so that worker processes find the functions it hands them."""
    module = importlib.import_module(Path(path).stem)
    failed = 0
    for name, test in list(vars(module).items()):
        if not name.startswith("test_") or not inspect.isfunction(test):
            continue
        try:
            if "tmp_path" in inspect.signature(test).parameters:
                with tempfile.TemporaryDirectory() as tmp:
                    test(Path(tmp))
            else:
                test()
        except Exception:
            failed += 1
            print(f"{name:72s} FAIL", flush=True)
            traceback.print_exc()
        else:
            print(f"{name:72s} ok", flush=True)
    sys.exit(1 if failed else 0)


start_settings()
