"""Runs KESE as run_KESE.py does, and writes every stage's time, unrounded, to $KESE_TIMES (JSON): the bars of a
board's chart. run_a_board.py starts it, with $KESE_GENERATOR the folder of run_KESE.py."""
import atexit, json, os, sys, time
from contextlib import contextmanager
GEN = os.environ["KESE_GENERATOR"]
sys.path.insert(0, GEN)
os.chdir(GEN)
from kese import job as J
times = []
_orig = J.Job.stage
@contextmanager
def stage(self, name, status=None):
    t = time.perf_counter()
    with _orig(self, name, status):
        yield
    times.append((name, time.perf_counter() - t))
J.Job.stage = stage
atexit.register(lambda: json.dump(times, open(os.environ["KESE_TIMES"], "w")))
from kese.cli import main
main()
