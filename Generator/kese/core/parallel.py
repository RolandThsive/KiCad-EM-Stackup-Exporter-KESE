"""Work done on several processor cores at once, in threads: the 2D geometry library (GEOS, under
shapely) runs outside Python's lock, so threads that mostly cut shapes run side by side."""
import os
from concurrent.futures import ThreadPoolExecutor

from parameters import P


def workers_wanted():
    """How many threads work at once: Run.WORKERS, or one per processor thread (os.cpu_count())."""
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
