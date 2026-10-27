"""The "simulation" mode without a geometry kernel: every part as one closed solid, its boundary
found in 2D from its prisms (kese/core/boundary.py) and then cut into triangles
(kese/core/boundary_mesh.py).  The Boundary itself is kept on the Model, so that the STEP writer
can write the same faces as exact solids.  Run.WORKERS parts are built at once, in threads: the 2D
work is done by GEOS, outside Python's lock."""
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
    """PrismSet -> (part name, Boundary, trimesh or None) for one part after another, the mesh
    finished by `finish` (output units, vertices merged) by the worker that built it, so that the
    raw mesh of a part, several times the size of the finished one, is gone before the next part
    is begun.  The biggest parts go first, so the one that needs the most memory runs while
    little else is held."""
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
