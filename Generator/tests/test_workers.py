"""The worker processes of kese/core/parallel.py: shapes keep their grid (and type and SRID) on the
way to and from the workers; Parallel.PROCESS_WORKERS caps them and boards under
Parallel.PROCESS_MIN_COORDINATES stay in one process; the run's settings reach the workers; a lost
worker or one out of memory leaves its jobs to half as many processes, then to the main process;
an error in the work is raised at once and the other workers are stopped; a caller that stops
early does not wait; the OOM killer takes a worker first; KESE runs inside a multiprocessing.Pool;
a script without a main guard is not run again in the workers; and the workers end with Ctrl-C
(one traceback) and with the main process.

    python -m pytest tests/test_workers.py          (or:  python tests/test_workers.py)"""
import os
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

import shapely

from helpers import ROOT, run_tests, settings
from kese.core.parallel import in_processes, processes_wanted, workers_wanted, worth_processes
from parameters import P
from test_threads import collections_of_grids, grids


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


def lost_on_3_slowly(n, parent, marker=None):
    """In a worker, job 3 stops its process (with a `marker`, only the first time: it leaves that
    file); the other jobs take 0.3 s, so that most are still left when it does."""
    if n == 3 and os.getpid() != parent and not (marker and Path(marker).exists()):
        if marker:
            Path(marker).touch()
        os._exit(9)
    time.sleep(0.3)
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
    P.override("Parallel.WORKERS", 2)
    return sorted(in_processes(abs, [(k, (-k,)) for k in range(n)]))


def pid_after_a_while(n):
    """In a worker: its process id, once the other workers have had time to start."""
    time.sleep(0.3)
    return os.getpid()


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
    with settings({"Parallel.WORKERS": 2}):
        back = dict(in_processes(same, [(k, (s,)) for k, s in enumerate(shapes)]))
    for k, s in enumerate(shapes):
        assert shapely.to_wkb(back[k]) == shapely.to_wkb(s), k
        assert grids(back[k]) == grids(s), k
        assert type(back[k]) is type(s) and shapely.get_srid(back[k]) == shapely.get_srid(s), k


def test_process_workers_caps_the_worker_processes():
    with settings({"Parallel.WORKERS": 4, "Parallel.PROCESS_WORKERS": 2}):
        assert (workers_wanted(), processes_wanted()) == (4, 2)
        pids = {pid for _, pid in in_processes(pid_after_a_while, [(n, (n,)) for n in range(6)])}
        P.override("Parallel.PROCESS_WORKERS", 8)                      # a cap: never more than WORKERS
        assert processes_wanted() == 4
        P.override("Parallel.PROCESS_WORKERS", 1)                      # stage 6 in this process, threads kept
        assert (workers_wanted(), processes_wanted()) == (4, 1) and not worth_processes(4, 10 ** 6)
    assert 0 < len(pids) <= 2 and os.getpid() not in pids, pids


def test_small_boards_stay_in_one_process():
    assert P.Parallel.PROCESS_MIN_COORDINATES == 20_000                  # the default
    with settings({"Parallel.WORKERS": 2, "Parallel.PROCESS_MIN_COORDINATES": 20_000}):
        assert not worth_processes(4, 19_999) and worth_processes(4, 20_000) and not worth_processes(1, 10 ** 6)
        P.override("Parallel.PROCESS_MIN_COORDINATES", 100)
        assert not worth_processes(4, 99) and worth_processes(4, 100)
        P.override("Parallel.PROCESS_MIN_COORDINATES", 0)              # processes for every board of 2 parts or more
        assert worth_processes(2, 0) and not worth_processes(1, 0)
        P.override("Parallel.WORKERS", 1)                              # 1: everything in this process
        assert not worth_processes(4, 10 ** 6)


def test_the_run_s_settings_reach_the_workers():
    with settings({"Parallel.WORKERS": 2, "Geometry.SNAP_GRID_MM": 0.0002}):
        got = dict(in_processes(snap_grid, [(0, ()), (1, ())]))
    assert got == {0: 0.0002, 1: 0.0002}


def test_a_lost_worker_leaves_its_jobs_to_this_process():
    notes = []
    with settings({"Parallel.WORKERS": 2}):
        got = dict(in_processes(lost_on_3, [(n, (n, os.getpid())) for n in range(8)], notes.append))
    assert got == {n: n * n for n in range(8)}
    assert len(notes) == 1 and notes[0].startswith("worker processes failed (BrokenProcessPool"), notes


def test_a_lost_worker_leaves_the_jobs_left_to_half_as_many_processes_then_to_this_one():
    # four workers: job 3 stops its worker each time, so the jobs left go to two, then here; lost
    # once, they are all done in the two
    lack = " (most often a lack of memory: fewer processes, Parallel.PROCESS_WORKERS, use less)"
    with settings({"Parallel.WORKERS": 4}):
        notes = []
        got = dict(in_processes(lost_on_3_slowly, [(n, (n, os.getpid())) for n in range(12)], notes.append))
        assert got == {n: n * n for n in range(12)}
        assert len(notes) == 2 and all(s.startswith("worker processes failed (BrokenProcessPool") for s in notes), notes
        assert notes[0].endswith(" left are built in 2 processes" + lack), notes
        assert notes[1].endswith(" in this process, one after another" + lack), notes
        with tempfile.TemporaryDirectory() as tmp:
            notes = []
            marker = str(Path(tmp) / "lost")
            got = dict(in_processes(lost_on_3_slowly, [(n, (n, os.getpid(), marker)) for n in range(12)], notes.append))
        assert got == {n: n * n for n in range(12)}
        assert len(notes) == 1 and notes[0].endswith(" left are built in 2 processes" + lack), notes


def test_out_of_memory_in_a_worker_leaves_its_job_to_this_process():
    notes = []
    with settings({"Parallel.WORKERS": 2}):
        got = dict(in_processes(out_of_memory_on_2, [(n, (n, os.getpid())) for n in range(6)], notes.append))
    assert got == {n: n * n for n in range(6)}
    assert notes == ["worker processes failed (MemoryError: no memory in a worker); the 1 part left is built "
                     "in this process, one after another (most often a lack of memory: fewer processes, "
                     "Parallel.PROCESS_WORKERS, use less)"], notes


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
        t0 = time.time()
        try:
            with settings({"Parallel.WORKERS": 4}):
                list(in_processes(fail_or_sleep, [(n, (n, error)) for n in range(4)], notes.append))
        except type(error) as e:
            raised = e
        assert str(raised) == str(error) and time.time() - t0 < 15, (raised, time.time() - t0)
        assert notes == [], notes                    # not built again here
        # ended before the error is raised: a worker writing a file writes no more (step_parts.py)
        assert not any(alive(w) for w in spawned() - before), "the workers building the other parts were not stopped"


def test_a_caller_that_stops_early_does_not_wait():
    before = spawned()
    t0 = time.time()
    with settings({"Parallel.WORKERS": 3}):
        results = in_processes(quick_or_sleep, [(n, (n,)) for n in range(3)])
        assert next(results) == (0, 0)
        results.close()
    assert time.time() - t0 < 15, time.time() - t0
    assert gone(before)


def test_the_oom_killer_takes_a_worker_first():
    if not sys.platform.startswith("linux"):
        return
    with settings({"Parallel.WORKERS": 2}):
        got = dict(in_processes(oom_score_adj, [(0, ()), (1, ())]))
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
        P.override("Parallel.WORKERS", 2)
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
            P.override("Parallel.WORKERS", 3)                # the first worker done waits for work
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
    run_tests(__file__)
