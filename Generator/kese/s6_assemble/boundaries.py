"""The "simulation" mode: every part as one closed solid, its boundary found in 2D
(kese/core/boundary.py) and cut into triangles; Run.WORKERS parts at once, in threads."""
import os
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from itertools import islice

import shapely

from kese.core.boundary import boundary_of
from kese.core.boundary_mesh import mesh_of_boundary
from parameters import P


def workers_wanted():
    """How many parts are worked on at once: Run.WORKERS, or one per processor."""
    return P.Run.WORKERS or os.cpu_count() or 1


def boundaries_and_meshes(ps, log, finish):
    """PrismSet -> (part name, Boundary, mesh or None) one part after another, biggest first, each mesh
    finished by `finish` in the worker that built it, so a raw mesh never outlives its part."""
    parts = ps.by_part()
    size = {part: sum(shapely.get_num_coordinates(p.region) for p in prisms) for part, prisms in parts.items()}
    order = sorted(parts, key=lambda k: -size[k])

    def build(part):
        boundary = boundary_of(part, parts[part], lambda s, part=part: log(f"{part}: {s}"))
        return boundary, finish(mesh_of_boundary(boundary))

    workers = workers_wanted()
    if workers == 1 or len(order) == 1:
        for part in order:
            yield part, *build(part)
        return
    queue = iter(order)
    with ThreadPoolExecutor(workers) as pool:
        running = {pool.submit(build, part): part for part in islice(queue, workers)}   # never more than the workers
        while running:
            done, _ = wait(running, return_when=FIRST_COMPLETED)
            for future in done:
                yield running.pop(future), *future.result()
            for part in islice(queue, len(done)):
                running[pool.submit(build, part)] = part
