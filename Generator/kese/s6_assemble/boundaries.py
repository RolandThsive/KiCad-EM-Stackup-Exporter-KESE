"""The "simulation" mode: every part as one closed solid, its boundary found in 2D
(kese/core/boundary.py) and cut into triangles; Parallel.WORKERS parts at once (at most
Parallel.PROCESS_WORKERS), in processes of their own (much of the work is Python's, which threads
would take in turn).  With the Verifier on, each part is checked where it is built
(kese/core/part_checks.py)."""
import shapely

from kese.core.boundary import boundary_of
from kese.core.boundary_mesh import mesh_of_boundary
from kese.core.parallel import in_processes, worth_processes
from kese.core.part_checks import part_check
from parameters import P


def boundaries_and_meshes(ps, log, finish, check):
    """PrismSet -> (part name, Boundary, mesh or None, its checks or None) one part after another,
    the biggest started first, each mesh finished by `finish` (a module's function) and, with
    `check`, checked for the Verifier, in the process that built it.  The notes made on the way are
    logged at the end, in that order, however the processes finished."""
    parts = ps.by_part()
    size = {part: sum(shapely.get_num_coordinates(p.region) for p in prisms) for part, prisms in parts.items()}
    order = sorted(parts, key=lambda k: -size[k])
    jobs = [(part, (part, parts[part], finish, check, ps.free_levels)) for part in order]
    if worth_processes(len(jobs), sum(size.values())):
        done = in_processes(build, jobs, log)
    else:
        done = ((part, build(*args)) for part, args in jobs)
    notes = {}
    for part, (boundary, mesh, notes[part], checks) in done:
        yield part, boundary, mesh, checks
    for part in order:
        for s in notes[part]:
            log(f"{part}: {s}")


def build(part, prisms, finish, check, free):
    """One part's Boundary, its finished mesh, the notes made on the way, and with `check` what the
    Verifier asks of it (else None); `free`: PrismSet.free_levels."""
    notes = []
    boundary = boundary_of(part, prisms, notes.append, free)
    mesh = finish(mesh_of_boundary(boundary))
    return boundary, mesh, notes, part_check(mesh, boundary, prisms, P.Run.UNITS) if check else None
