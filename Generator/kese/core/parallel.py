"""Work done on several processor cores at once.  In threads where the 2D geometry library (GEOS,
under shapely) does the work, as it runs outside Python's lock; in processes of their own where
Python's own steps are much of it (stage 6, which builds each part's solid or slices the parts for
the visual skin; a big board's copper layers in stage 3 and its STEP parts in stage 7)."""
import multiprocessing
import os
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool

from kese.core import shape_copies
from kese.core.memory import done_then_given_back, give_back_memory
from kese.core.workers import main_left_out, settings, stop, use_settings
from parameters import P

WINDOWS_MOST = 61             # processes: ProcessPoolExecutor's limit on Windows (64 wait handles, less its own)
NOT_STARTED = (OSError, NotImplementedError, BrokenProcessPool)    # no processes here (some sandboxes)
LOST = (BrokenProcessPool, MemoryError)     # a worker stopped by the system, or out of memory

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


def biggest_first(pool, work, items, size):
    """[work(item) for item in items] in the pool's threads, the item of the greatest size started
    first, so that no thread is left alone with a big one at the end."""
    order = sorted(range(len(items)), key=lambda i: -size[i])
    done = dict(zip(order, pool.map(work, [items[i] for i in order])))
    return [done[i] for i in range(len(items))]


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
    `work` must be a module's function.  Where a worker is lost (stopped by the system for lack of
    memory, or out of memory), the jobs not done go to half as many processes, and once that would
    be one, or where processes cannot be started, they run here, one after another: each time with
    a note (log), "the 3 parts left are built in 2 processes" (`what`, `done`), and why.  An error in
    the work itself is raised here at once: the other workers are stopped, not waited for."""
    left = dict(jobs)
    n = 0 if multiprocessing.current_process().daemon else process_limit(min(processes_wanted(), len(left)))
    while left and n:                         # a multiprocessing.Pool's worker (a daemon) may start none
        failed, lost = yield from in_pool(work, left, n)
        if failed is None:
            return
        n = (n + 1) // 2 if lost and n > 2 else 0
        n = n if min(n, len(left)) > 1 else 0
        if log:
            k = len(left)
            log(f"worker processes failed ({type(failed).__name__}: {failed}); the {k} {what}{'s' * (k != 1)} left "
                f"{'are' if k != 1 else 'is'} {done} " + (f"in {n} processes" if n else "in this process, one after another")
                + (" (most often a lack of memory: fewer processes, Parallel.PROCESS_WORKERS, use less)" if lost else ""))
    for key, args in left.items():
        yield key, work(*args)


def in_pool(work, left, n):
    """(key, work(*args)) for every job of `left` {key: args}, each as it is done (and taken out of
    `left`), in a pool of n processes -> (what stopped them, or None; whether a worker was lost)."""
    try:
        pool = ProcessPoolExecutor(n, mp_context=multiprocessing.get_context("spawn"),
                                   initializer=use_settings, initargs=(settings(),))
    except NOT_STARTED as e:
        return e, False
    failed, finished = None, False
    try:
        try:
            with main_left_out():                 # the processes start in the first submits
                running = {pool.submit(done_then_given_back, work, *args): key for key, args in left.items()}
        except NOT_STARTED as e:
            return e, False
        for future in as_completed(running):
            try:
                result = future.result()
            except LOST as e:                     # the other workers' parts are still taken
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
    return failed, failed is not None
