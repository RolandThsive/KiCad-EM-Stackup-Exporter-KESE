"""The "simulation" mode: every part as one closed solid, its boundary found in 2D
(kese/core/boundary.py) and cut into triangles; Run.WORKERS parts at once, in processes of their
own (much of the work is Python's, which threads would take in turn)."""
import shapely

from kese.core.boundary import boundary_of
from kese.core.boundary_mesh import mesh_of_boundary
from kese.core.parallel import in_processes, worth_processes


def boundaries_and_meshes(ps, log, finish):
    """PrismSet -> (part name, Boundary, mesh or None) one part after another, the biggest started
    first, each mesh finished by `finish` (a module's function) in the process that built it.  The
    notes made on the way are logged at the end, in that order, however the processes finished."""
    parts = ps.by_part()
    size = {part: sum(shapely.get_num_coordinates(p.region) for p in prisms) for part, prisms in parts.items()}
    order = sorted(parts, key=lambda k: -size[k])
    jobs = [(part, (part, parts[part], finish)) for part in order]
    if worth_processes(len(jobs), sum(size.values())):
        done = in_processes(build, jobs, log)
    else:
        done = ((part, build(*args)) for part, args in jobs)
    notes = {}
    for part, (boundary, mesh, notes[part]) in done:
        yield part, boundary, mesh
    for part in order:
        for s in notes[part]:
            log(f"{part}: {s}")


def build(part, prisms, finish):
    """One part's Boundary, its finished mesh, and the notes made on the way."""
    notes = []
    boundary = boundary_of(part, prisms, notes.append)
    return boundary, finish(mesh_of_boundary(boundary)), notes
