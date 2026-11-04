"""The worker processes and threads of kese/core/parallel.py: a thread's own copies of shapes
(kese/core/shape_copies.py) are the same shapes, shapes keep their grid (and type and SRID) on the
way to and from the workers, the run's settings reach the workers, a lost worker or one out of
memory leaves its jobs to the main process, an error in the work is raised at once and the other
workers are stopped, a caller that stops early does not wait, the OOM killer takes a worker first,
KESE runs inside a multiprocessing.Pool, a script without a main guard is not run again in the
workers, and the workers end with Ctrl-C (one traceback) and with the main process.

    python -m pytest tests/test_parallel.py          (or:  python tests/test_parallel.py)"""
import os
import signal
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import numpy as np
import shapely

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core.parallel import in_parallel, in_processes  # noqa: E402
from kese.core.shape_copies import own  # noqa: E402
from parameters import P  # noqa: E402


def with_workers(n, *more):
    """Run.WORKERS = n (and more (key, value) settings) for a block; -> the values to put back."""
    saved = [("Run.WORKERS", P.Run.WORKERS)] + [(k, getattr(getattr(P, k.split(".")[0]), k.split(".")[1])) for k, _ in more]
    for k, v in [("Run.WORKERS", n), *more]:
        P.override(k, v)
    return saved


def put_back(saved):
    for k, v in saved:
        P.override(k, v)


def same(shape):
    """In a worker: the shape as it came (copy.copy would rebuild it through shapely's own pickling)."""
    return shape


def snap_grid():
    """In a worker: the grid it builds on."""
    return P.Geometry.SNAP_GRID_MM


def lost_on_3(n, parent):
    """In a worker, job 3 stops its process, as the system does when memory runs out."""
    if n == 3 and os.getpid() != parent:
        os._exit(9)
    return n * n


def fail_or_sleep(n, error):
    """In a worker: job 0 raises `error` at once, the others take 30 s."""
    if n == 0:
        raise error
    time.sleep(30)
    return n


def out_of_memory_on_2(n, parent):
    """In a worker, job 2 runs out of memory (as on Windows, which has no OOM killer)."""
    if n == 2 and os.getpid() != parent:
        raise MemoryError("no memory in a worker")
    return n * n


def oom_score_adj():
    """In a worker: how readily Linux's OOM killer takes it."""
    return int(Path("/proc/self/oom_score_adj").read_text())


def inside_a_pool(n):
    """In a multiprocessing.Pool's worker (a daemon, which may not start processes): in_processes."""
    P.override("Run.WORKERS", 2)
    return sorted(in_processes(abs, [(k, (-k,)) for k in range(n)]))


def quick_or_sleep(n):
    if n:
        time.sleep(30)
    return n


def test_shapes_keep_their_grid_in_worker_processes():
    square = shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5))
    shapes = [shapely.set_precision(square, 1e-4), square, shapely.Polygon(), shapely.GeometryCollection(),
              shapely.set_precision(shapely.MultiPolygon([shapely.box(0, 0, 1, 1), shapely.box(2, 0, 3, 1)]), 1e-4),
              shapely.GeometryCollection([shapely.Point(1, 2), shapely.LineString([(0, 0), (1, 1)])]),
              shapely.set_precision(shapely.Polygon(), 1e-4),          # what a gridded overlay that meets nothing gives
              shapely.set_precision(shapely.LinearRing([(0, 0), (1, 0), (1, 1)]), 1e-4),
              shapely.set_srid(shapely.set_precision(shapely.Point(1, 2), 1e-4), 4326), *collections_of_grids()]
    saved = with_workers(2)
    try:
        back = dict(in_processes(same, [(k, (s,)) for k, s in enumerate(shapes)]))
    finally:
        put_back(saved)
    for k, s in enumerate(shapes):
        assert shapely.to_wkb(back[k]) == shapely.to_wkb(s), k
        assert grids(back[k]) == grids(s), k
        assert type(back[k]) is type(s) and shapely.get_srid(back[k]) == shapely.get_srid(s), k


def collections_of_grids():
    """Collections on no grid of parts on one, as as_region builds them: GEOS grows each part on its own."""
    part = shapely.set_precision(shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5)), 1e-4)
    two = shapely.MultiPolygon([part, shapely.box(2, 0, 3, 1)])
    return [two, shapely.set_srid(shapely.GeometryCollection([two, part, shapely.Point(1, 2)]), 4326)]


def grids(shape):
    """The grid of a shape and, in a collection, those of its parts (at any depth)."""
    if shapely.get_type_id(shape) < 4 or shape.is_empty:
        return float(shapely.get_precision(shape))
    return float(shapely.get_precision(shape)), [grids(p) for p in shapely.get_parts(shape)]


def test_a_thread_s_own_copies_are_the_same_shapes_on_factories_of_their_own():
    square = shapely.set_precision(shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5)), 1e-4)
    shapes = [square, shapely.box(0, 0, 1, 1), shapely.set_precision(shapely.Polygon(), 1e-4),
              shapely.set_precision(shapely.LinearRing([(0, 0), (1, 0), (1, 1)]), 1e-4),
              shapely.set_srid(shapely.set_precision(shapely.Point(1, 2), 1e-4), 4326), *collections_of_grids()]
    copies = own({"list": shapes, "tuple": (shapes[0], "net"), "array": np.array(shapes, dtype=object), "n": 3})
    assert copies["n"] == 3 and copies["tuple"][1] == "net" and isinstance(copies["tuple"], tuple)
    for got in (copies["list"], list(copies["array"]), [copies["tuple"][0]]):
        for a, b in zip(shapes, got):
            assert a is not b and type(a) is type(b) and shapely.to_wkb(a) == shapely.to_wkb(b)
            assert grids(a) == grids(b) and shapely.get_srid(a) == shapely.get_srid(b)
            assert shapely.to_wkb(a.buffer(0.01)) == shapely.to_wkb(b.buffer(0.01))     # on the same grids


def make_and_drop(square, n=3000):
    """In a thread: shapes made from `square` (they share its GEOS factory) and dropped, n times."""
    for _ in range(n):
        a = square.buffer(0.01)
        shapely.get_parts(a)
        a.intersection(shapely.box(1, 1, 5, 5))
    return True


def test_threads_on_their_own_copies_of_one_shape():
    # one shape on a grid, used by every thread: each works on its own copy (with the shared shape
    # itself, GEOS 3.14 can lose its factory's count of shapes and crash)
    shared = shapely.set_precision(shapely.box(0, 0, 10, 10).difference(shapely.box(2, 2, 3, 3)), 1e-4)
    parts = shapely.MultiPolygon([shared, shapely.set_precision(shapely.box(20, 0, 30, 10), 1e-4)])
    saved = with_workers(4)
    try:
        assert in_parallel(lambda k: make_and_drop(own((shared, parts)[k % 2])), range(4)) == [True] * 4
    finally:
        put_back(saved)


def test_the_run_s_settings_reach_the_workers():
    saved = with_workers(2, ("Geometry.SNAP_GRID_MM", 0.0002))
    try:
        got = dict(in_processes(snap_grid, [(0, ()), (1, ())]))
    finally:
        put_back(saved)
    assert got == {0: 0.0002, 1: 0.0002}


def test_a_lost_worker_leaves_its_jobs_to_this_process():
    notes = []
    saved = with_workers(2)
    try:
        got = dict(in_processes(lost_on_3, [(n, (n, os.getpid())) for n in range(8)], notes.append))
    finally:
        put_back(saved)
    assert got == {n: n * n for n in range(8)}
    assert len(notes) == 1 and notes[0].startswith("worker processes failed (BrokenProcessPool"), notes


def test_out_of_memory_in_a_worker_leaves_its_job_to_this_process():
    notes = []
    saved = with_workers(2)
    try:
        got = dict(in_processes(out_of_memory_on_2, [(n, (n, os.getpid())) for n in range(6)], notes.append))
    finally:
        put_back(saved)
    assert got == {n: n * n for n in range(6)}
    assert notes == ["worker processes failed (MemoryError: no memory in a worker); the 1 part left is built "
                     "in this process, one after another (most often a lack of memory: Run.WORKERS = 1 uses "
                     "less)"], notes


def spawned():
    return set(workers_of(os.getpid())) if sys.platform.startswith("linux") else set()


def gone(before):
    """Whether the worker processes started since `before` have ended (within 10 s)."""
    t0 = time.time()
    while any(alive(w) for w in spawned() - before) and time.time() - t0 < 10:
        time.sleep(0.1)
    return not any(alive(w) for w in spawned() - before)


def test_an_error_in_the_work_is_raised_at_once_and_not_taken_for_lost_processes():
    for error in (ValueError("a bug in the work"), FileNotFoundError(2, "No such file", "/nowhere")):
        notes, before, raised = [], spawned(), None
        saved = with_workers(4)
        t0 = time.time()
        try:
            list(in_processes(fail_or_sleep, [(n, (n, error)) for n in range(4)], notes.append))
        except type(error) as e:
            raised = e
        finally:
            put_back(saved)
        assert str(raised) == str(error) and time.time() - t0 < 15, (raised, time.time() - t0)
        assert notes == [], notes                    # not built again here
        assert gone(before), "the workers building the other parts were not stopped"


def test_a_caller_that_stops_early_does_not_wait():
    before = spawned()
    saved = with_workers(3)
    t0 = time.time()
    try:
        results = in_processes(quick_or_sleep, [(n, (n,)) for n in range(3)])
        assert next(results) == (0, 0)
        results.close()
    finally:
        put_back(saved)
    assert time.time() - t0 < 15, time.time() - t0
    assert gone(before)


def test_the_oom_killer_takes_a_worker_first():
    if not sys.platform.startswith("linux"):
        return
    saved = with_workers(2)
    try:
        got = dict(in_processes(oom_score_adj, [(0, ()), (1, ())]))
    finally:
        put_back(saved)
    assert got == {0: 1000, 1: 1000}


def test_inside_a_multiprocessing_pool():
    import multiprocessing
    with multiprocessing.get_context("spawn").Pool(1) as pool:
        assert pool.apply(inside_a_pool, (4,)) == [(0, 0), (1, 1), (2, 2), (3, 3)]


def test_no_jobs():
    assert list(in_processes(abs, [])) == []


def run_script(tmp_path, body, stderr=subprocess.STDOUT):
    script = tmp_path / "script.py"
    script.write_text(textwrap.dedent(f"""\
        import sys
        sys.path.insert(0, {str(ROOT)!r})
        from kese.core.parallel import in_processes
        from parameters import P
        P.override("Run.WORKERS", 2)
        print("top-level code", flush=True)
        """) + textwrap.dedent(body))
    return subprocess.Popen([sys.executable, str(script)], stdout=subprocess.PIPE, stderr=stderr, text=True,
                            cwd=tmp_path)


def test_a_script_without_a_main_guard_is_not_run_again_in_the_workers(tmp_path):
    p = run_script(tmp_path, 'print(sorted(in_processes(abs, [(k, (-k,)) for k in range(4)])), flush=True)\n')
    out, _ = p.communicate(timeout=120)
    assert p.returncode == 0, out
    assert out.count("top-level code") == 1, out
    assert "[(0, 0), (1, 1), (2, 2), (3, 3)]" in out, out


def workers_of(pid):
    """The pids of the worker processes a process started (Linux)."""
    out = []
    for d in Path("/proc").iterdir():
        try:
            if d.name.isdigit() and int((d / "stat").read_text().rsplit(")", 1)[1].split()[1]) == pid \
                    and b"spawn_main" in (d / "cmdline").read_bytes():
                out.append(int(d.name))
        except (OSError, ValueError):
            pass
    return out


def alive(pid):
    """Whether a process runs (a zombie, ended but not yet reaped, does not)."""
    try:
        return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0] != "Z"
    except OSError:
        return False


def test_ctrl_c_stops_the_workers_with_one_traceback(tmp_path):
    if not sys.platform.startswith("linux"):
        return
    script = tmp_path / "script.py"
    script.write_text(textwrap.dedent(f"""\
        import sys, time
        sys.path.insert(0, {str(ROOT)!r})
        from kese.core.parallel import in_processes
        from parameters import P
        if __name__ == "__main__":
            P.override("Run.WORKERS", 3)                     # the first worker done waits for work
            list(in_processes(time.sleep, [(0, (0,)), (1, (60,)), (2, (60,))]))
        """))
    p = subprocess.Popen([sys.executable, str(script)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         start_new_session=True)
    try:
        t0 = time.time()
        while len(workers := workers_of(p.pid)) < 3 and time.time() - t0 < 60:
            time.sleep(0.1)
        time.sleep(1)
        os.killpg(p.pid, signal.SIGINT)                      # Ctrl-C reaches every process of the terminal's group
        out, _ = p.communicate(timeout=20)
    finally:
        p.kill()
    assert out.count("Traceback") == 1 and "KeyboardInterrupt" in out and "Process Spawn" not in out, out
    assert not [w for w in workers if alive(w)], workers


def test_the_workers_end_with_the_main_process(tmp_path):
    if not sys.platform.startswith("linux"):
        return                                               # reads /proc
    # killed, the script leaves its semaphores to multiprocessing's resource tracker, which says so on stderr
    p = run_script(tmp_path, """\
        import time
        if __name__ == "__main__":
            list(in_processes(time.sleep, [(0, (60,)), (1, (60,))]))
        """, stderr=subprocess.DEVNULL)
    try:
        t0 = time.time()
        while len(workers := workers_of(p.pid)) < 2 and time.time() - t0 < 60:
            time.sleep(0.1)
        assert len(workers) == 2, workers
        time.sleep(1)                                        # the workers have started their jobs
        os.kill(p.pid, signal.SIGKILL)
        p.wait()
        t0 = time.time()
        while any(alive(w) for w in workers) and time.time() - t0 < 20:
            time.sleep(0.1)
        left = [w for w in workers if alive(w)]
    finally:
        p.kill()
    for w in left:
        os.kill(w, signal.SIGKILL)
    assert not left, f"workers {left} still running {time.time() - t0:.0f} s after the main process was killed"


if __name__ == "__main__":
    import tempfile
    import test_parallel as t        # the workers find the jobs' functions in a module, not in __main__
    t.test_shapes_keep_their_grid_in_worker_processes()
    t.test_a_thread_s_own_copies_are_the_same_shapes_on_factories_of_their_own()
    t.test_threads_on_their_own_copies_of_one_shape()
    t.test_the_run_s_settings_reach_the_workers()
    t.test_a_lost_worker_leaves_its_jobs_to_this_process()
    t.test_out_of_memory_in_a_worker_leaves_its_job_to_this_process()
    t.test_an_error_in_the_work_is_raised_at_once_and_not_taken_for_lost_processes()
    t.test_a_caller_that_stops_early_does_not_wait()
    t.test_the_oom_killer_takes_a_worker_first()
    t.test_inside_a_multiprocessing_pool()
    t.test_no_jobs()
    with tempfile.TemporaryDirectory() as d:
        t.test_a_script_without_a_main_guard_is_not_run_again_in_the_workers(Path(d))
        t.test_ctrl_c_stops_the_workers_with_one_traceback(Path(d))
        t.test_the_workers_end_with_the_main_process(Path(d))
    print("ok")
