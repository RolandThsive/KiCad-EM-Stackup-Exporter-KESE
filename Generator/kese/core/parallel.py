"""Work done on several processor cores at once.  In threads where the 2D geometry library (GEOS,
under shapely) does the work, as it runs outside Python's lock; in processes of their own where
Python's own steps are much of it (stage 6, which builds each part's solid)."""
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
from multiprocessing.reduction import ForkingPickler

import shapely

from parameters import P

FEW_COORDINATES = 20_000      # in all the shapes of a job list: below this the jobs are done here, one after
                              # another (well under a second), as starting the processes would take longer


def workers_wanted():
    """How many threads or processes work at once: Run.WORKERS, or one per processor thread (os.cpu_count())."""
    return P.Run.WORKERS or os.cpu_count() or 1


def in_parallel(work, items):
    """[work(item) for item in items], Run.WORKERS items at a time, the results in the items' order
    (so that what is built from them comes out the same however many threads ran)."""
    items = list(items)
    workers = min(workers_wanted(), len(items))
    if workers <= 1:
        return [work(item) for item in items]
    with ThreadPoolExecutor(workers) as pool:
        return list(pool.map(work, items))


def worth_processes(jobs, coordinates):
    """Whether `jobs` jobs on shapes of `coordinates` coordinates in all are worth processes of their own."""
    return workers_wanted() > 1 and jobs > 1 and coordinates >= FEW_COORDINATES


def in_processes(work, jobs, log=None):
    """(key, work(*args)) for every (key, args) of jobs, each as it is done, Run.WORKERS at a time in
    processes started afresh (as Windows and macOS start them), with this run's settings.  `work`
    must be a module's function.  Where processes cannot be started, or one is lost (stopped by the
    system for lack of memory), the jobs not done yet run here, one after another, with a note (log)."""
    left = dict(jobs)
    try:
        pool = ProcessPoolExecutor(min(workers_wanted(), len(left)), mp_context=multiprocessing.get_context("spawn"),
                                   initializer=use_settings, initargs=(settings(),))
        try:
            running = {pool.submit(work, *args): key for key, args in left.items()}
            for future in as_completed(running):
                key = running.pop(future)
                yield key, future.result()
                del left[key]
        finally:
            pool.shutdown(cancel_futures=True)
    except (OSError, NotImplementedError, BrokenProcessPool) as e:     # no processes here (some sandboxes)
        if log:
            log(f"worker processes failed ({type(e).__name__}: {e}); the {len(left)} parts left are built "
                "in this process, one after another")
    for key, args in left.items():
        yield key, work(*args)


def settings():
    """Every value of parameters/*.py as this run has it (--for and --set included)."""
    return {f"{short}.{name}": getattr(module, name) for short, module in P.modules().items()
            for name in dir(module) if name.isupper()}


def use_settings(values):
    """A worker process takes the run's settings (it read parameters/*.py afresh)."""
    for key, value in values.items():
        P.override(key, value)


def _shape(wkb, grid):
    """A shape sent to or from a worker process, on its grid again."""
    shape = shapely.from_wkb(wkb)
    return shapely.set_precision(shape, grid, mode="pointwise") if grid else shape


def _send_shape(shape):
    # shapely's own pickling drops the grid a shape is on, and shapes on a grid are cut on it
    return _shape, (shapely.to_wkb(shape), float(shapely.get_precision(shape)))


for _kind in (shapely.Point, shapely.LineString, shapely.Polygon, shapely.MultiPoint, shapely.MultiLineString,
              shapely.MultiPolygon, shapely.GeometryCollection):
    ForkingPickler.register(_kind, _send_shape)
