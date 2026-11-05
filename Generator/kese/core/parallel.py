"""Work done on several processor cores at once.  In threads where the 2D geometry library (GEOS,
under shapely) does the work, as it runs outside Python's lock; in processes of their own where
Python's own steps are much of it (stage 6, which builds each part's solid; a big board's copper
layers in stage 3 and its STEP parts in stage 7)."""
import contextlib
import multiprocessing
import multiprocessing.connection
import os
import signal
import sys
import threading
import time
import types
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
from contextlib import contextmanager

from kese.core import shape_copies
from kese.core.memory import done_then_given_back, give_back_memory
from parameters import P

WINDOWS_MOST = 61             # processes: ProcessPoolExecutor's limit on Windows (64 wait handles, less its own)
NOT_STARTED = (OSError, NotImplementedError, BrokenProcessPool)    # no processes here (some sandboxes)
LOST = (BrokenProcessPool, MemoryError)     # a worker stopped by the system, or out of memory
STOP_WAIT_S = 10              # seconds stop() waits at most for the workers it ended to be gone

shape_copies.register()                   # shapes keep their grid on the way to and from the workers


def processor_threads():
    """The processor threads this process may run on: os.process_cpu_count() (Python 3.13), else the
    threads of its affinity mask.  os.cpu_count() counts every thread of the machine, also those a job
    scheduler, `taskset` or a container's cpuset keeps the process from."""
    if hasattr(os, "process_cpu_count"):
        return os.process_cpu_count() or 1
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0)) or 1
    return os.cpu_count() or 1


def workers_wanted():
    """How many threads or processes work at once: Parallel.WORKERS, or one per processor thread."""
    return P.Parallel.WORKERS or processor_threads()


def processes_wanted():
    """How many worker processes work at once: as many as workers_wanted(), at most
    Parallel.PROCESS_WORKERS (each holds its own Python and the part it builds)."""
    return min(workers_wanted(), P.Parallel.PROCESS_WORKERS or workers_wanted())


def process_limit(n):
    """n processes, or as many as a ProcessPoolExecutor can hold on this system."""
    return min(n, WINDOWS_MOST) if sys.platform == "win32" else n


def in_parallel(work, items):
    """[work(item) for item in items], Parallel.WORKERS items at a time, the results in the items' order
    (so that what is built from them comes out the same however many threads ran).  `work` must take
    own() copies of the shapes it shares with the other items' work (kese/core/shape_copies.py)."""
    items = list(items)
    workers = min(workers_wanted(), len(items))
    if workers <= 1:
        return [work(item) for item in items]
    with ThreadPoolExecutor(workers) as pool:
        done = list(pool.map(work, items))
    give_back_memory()
    return done


def worth_processes(jobs, coordinates):
    """Whether `jobs` jobs on shapes of `coordinates` coordinates in all are worth processes of their
    own: at least Parallel.PROCESS_MIN_COORDINATES, below which the jobs are done here, one after
    another, faster than starting processes (and a multiprocessing.Pool's worker, a daemon, may start
    no process)."""
    return (processes_wanted() > 1 and jobs > 1 and coordinates >= P.Parallel.PROCESS_MIN_COORDINATES
            and not multiprocessing.current_process().daemon)


def in_processes(work, jobs, log=None, done="built", what="part"):
    """(key, work(*args)) for every (key, args) of jobs, each as it is done, processes_wanted() at a
    time in processes started afresh (as Windows and macOS start them), with this run's settings.
    `work` must be a module's function.  Where processes cannot be started, or one is lost (stopped
    by the system for lack of memory, or out of memory), the jobs not done run here, one after
    another, with a note (log): "the 3 parts left are built here" (`what`, `done`) and why.  An
    error in the work itself is raised here at once: the other workers are stopped, not waited for."""
    left = dict(jobs)
    if not left:
        return
    if multiprocessing.current_process().daemon:      # a multiprocessing.Pool's worker may start none
        yield from ((key, work(*args)) for key, args in left.items())
        return
    failed = None
    try:
        pool = ProcessPoolExecutor(process_limit(min(processes_wanted(), len(left))),
                                   mp_context=multiprocessing.get_context("spawn"),
                                   initializer=use_settings, initargs=(settings(),))
    except NOT_STARTED as e:
        failed = e
    else:
        finished = False
        try:
            try:
                with main_left_out():                 # the processes start in the first submits
                    running = {pool.submit(done_then_given_back, work, *args): key for key, args in left.items()}
            except NOT_STARTED as e:
                failed = e
            else:
                for future in as_completed(running):
                    try:
                        result = future.result()
                    except LOST as e:                 # the other workers' parts are still taken
                        failed = failed or e
                        continue
                    yield running[future], result
                    del left[running[future]]
                finished = True
        finally:
            if finished:
                pool.shutdown()
            else:                                     # an error, or the caller stopped early
                stop(pool)
    if failed is not None and log:
        n = len(left)
        log(f"worker processes failed ({type(failed).__name__}: {failed}); the {n} {what}{'s' * (n != 1)} left "
            f"{'are' if n != 1 else 'is'} {done} in this process, one after another"
            + (" (most often a lack of memory: fewer processes, Parallel.PROCESS_WORKERS, use less)"
               if isinstance(failed, LOST) else ""))
    for key, args in left.items():
        yield key, work(*args)


def stop(pool):
    """End a pool's workers now, with the parts they are building, let the pool go, and wait until
    they are gone (STOP_WAIT_S at most): then no worker writes a file any more (step_parts.py)."""
    processes = list((getattr(pool, "_processes", None) or {}).values())    # shutdown() forgets them
    if hasattr(pool, "terminate_workers"):            # Python 3.14
        pool.terminate_workers()
    else:
        pool.shutdown(wait=False, cancel_futures=True)
        for process in processes:
            with contextlib.suppress(ValueError, ProcessLookupError):     # already ended and closed
                if process.is_alive():
                    process.terminate()
    running = []
    for process in processes:
        with contextlib.suppress(ValueError):         # closed: ended already
            running.append(process.sentinel)
    end = time.monotonic() + STOP_WAIT_S
    while running and time.monotonic() < end:
        for ended in multiprocessing.connection.wait(running, timeout=end - time.monotonic()):
            running.remove(ended)


@contextmanager
def main_left_out():
    """Processes started in this block do not run this run's main module again.  Spawn runs it in
    every new process (as __mp_main__), for what is sent from it, and nothing is; a script that calls
    KESE without `if __name__ == "__main__":` would run KESE all over again in each of them."""
    main = sys.modules.get("__main__")
    sys.modules["__main__"] = types.ModuleType("__main__")
    try:
        yield
    finally:
        if main is None:
            del sys.modules["__main__"]
        else:
            sys.modules["__main__"] = main


def settings():
    """Every value of parameters/*.py as this run has it (--for and --set included)."""
    return {f"{short}.{name}": getattr(module, name) for short, module in P.modules().items()
            for name in dir(module) if name.isupper()}


def use_settings(values):
    """A worker process takes the run's settings (it read parameters/*.py afresh), and stops when the
    main process does, however it stopped.  Ctrl-C ends it at once, without a traceback of its own
    (the main process prints one).  Where memory runs out, Linux's OOM killer takes a worker before
    the main process, which then builds the worker's parts itself: the biggest process, the one the
    killer would take, is most often the main one."""
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        with open("/proc/self/oom_score_adj", "w") as f:
            f.write("1000")
    except OSError:                                   # not Linux
        pass
    threading.Thread(target=stop_with_parent, name="kese-parent-watch", daemon=True).start()
    for key, value in values.items():
        P.override(key, value)


def stop_with_parent():
    """In a worker: wait for the main process to end, then end too.  A worker whose main process was
    killed (SIGTERM, a closed terminal) would otherwise finish its part and wait for work for ever."""
    parent = multiprocessing.parent_process()
    if parent is not None:
        multiprocessing.connection.wait([parent.sentinel])
        os._exit(1)
