"""Stage 6 - assemble: the PrismSet -> one in-memory Model: meshes per part (closed solids in
"simulation" mode, the visible skin in "visual" mode), output units and orientation, materials and
properties.  Stage 7 writes every file format from this Model; nothing is rebuilt per format."""
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import Condition

from kese.core.memory import give_back_memory
from kese.core.parallel import workers_wanted
from kese.model.output_model import Model
from kese.s6_assemble.boundaries import boundaries_and_meshes
from kese.s6_assemble.skin_faces import skin_faces
from kese.s6_assemble.skin_mesh import skin_meshes_from_faces
from kese.s6_assemble.transform import finish_mesh, output_transform
from parameters import P

PART_ORDER = ["Board", "Copper", "Plating", "Via Resin", "Top Solder Mask", "Top Mask over Copper", "Bottom Solder Mask",
              "Bottom Mask over Copper", "Top Silkscreen", "Bottom Silkscreen", "Top Finish", "Bottom Finish",
              "Edge Finish"]


def run(ps, job):
    what = "visible skin" if job.mode == "visual" else "joining the solids of every part"
    with job.stage("assemble", f"assemble ({what})"):
        return assemble(ps, job.mode, job.note, job.verify)


def rank(name):
    for i, prefix in enumerate(PART_ORDER):
        if name == prefix or name.startswith((prefix + "_", prefix + " ")):
            return (i, name)
    return (len(PART_ORDER), name)


def finished_meshes(ps, mode, log, finish, boundaries, checks, check):
    """(part, finished mesh) one after another: the skin is made in one go, the solids one part at
    a time.  A solid's Boundary is kept for the STEP writer, and its mesh is finished (and with
    `check` checked for the Verifier, into `checks`) by the worker that built it."""
    if mode == "visual":
        yield from finished_skin(skin_meshes_from_faces(*skin_faces(ps, log), free=ps.free_levels), finish)
    else:
        for part, boundary, m, checked in boundaries_and_meshes(ps, log, finish, check):
            boundaries[part] = boundary
            if checked is not None:
                checks[part] = checked
            yield part, m


def finished_skin(skin, finish):
    """(part, finished mesh) for every mesh of the skin, in threads (the work is numpy's), the biggest
    first.  A finish holds several times its mesh in memory for a while, so the meshes finished at
    once hold no more faces in all than the biggest one: the peak stays that of finishing one mesh
    after another (on NE_Delta with mask and silkscreen, 5.9 GB; 6.3 GB with no such bound), while the
    many small meshes go side by side.  Each raw mesh is let go as soon as it is finished."""
    size = {part: len(mesh.faces) for part, mesh in skin.items()}
    order = sorted(skin, key=lambda part: -size[part])
    most = size[order[0]] if order else 0
    room, held = Condition(), [0]

    def done(part):
        with room:
            room.wait_for(lambda: not held[0] or held[0] + size[part] <= most)
            held[0] += size[part]
        try:
            return part, finish(skin.pop(part))
        finally:
            with room:
                held[0] -= size[part]
                room.notify_all()
    with ThreadPoolExecutor(workers_wanted()) as pool:
        yield from pool.map(done, order)
    give_back_memory()      # what the threads freed, before the Verifier: NE_Delta with mask and silkscreen
                            # peaks at 5.9 GB with --verify so, 7.1 GB with it kept


def assemble(ps, mode, log, check):
    """PrismSet -> Model; `check`: the Verifier will run, so each solid is checked as it is built."""
    mat = output_transform()
    finish = partial(finish_mesh, mat=mat)           # a module's function, for the worker processes
    boundaries, checks = {}, {}
    made = finished_meshes(ps, mode, log, finish, boundaries, checks, check)      # one raw mesh at a time
    done = {part: m for part, m in made if m is not None}
    meshes = {part: done[part] for part in sorted(done, key=rank)}
    boundaries = {part: boundaries[part] for part in sorted(boundaries, key=rank)}   # not in the order built
    props = {part: props_of(prisms) for part, prisms in ps.by_part().items()}
    return Model(name=ps.regions.items.name, mode=mode, prismset=ps, meshes=meshes, materials=ps.materials, props=props,
                 transform=mat, units=P.Run.UNITS, boundaries=boundaries, checks=checks)


def props_of(prisms):
    """A part's properties: its first prism's, then its role, layer and net, its heights and how many
    prisms it has."""
    p0 = prisms[0]
    return {**p0.props, "role": p0.role, "layer": p0.layer, "net": p0.net,
            "z_min_mm": round(min(p.z0 for p in prisms), 6), "z_max_mm": round(max(p.z1 for p in prisms), 6),
            "prisms": len(prisms)}
