"""Stage 6 - assemble: the PrismSet -> one in-memory Model: meshes per part (closed solids in
"simulation" mode, the visible skin in "visual" mode), output units and orientation, materials and
properties.  Stage 7 writes every file format from this Model; nothing is rebuilt per format."""
from kese.model.output_model import Model
from kese.s6_assemble.boundaries import boundaries_and_meshes
from kese.s6_assemble.skin import skin_meshes
from kese.s6_assemble.skin_faces import skin_faces
from kese.s6_assemble.skin_mesh import skin_meshes_from_faces
from kese.s6_assemble.solids import solid_meshes
from kese.s6_assemble.transform import finish_mesh, output_transform
from parameters import P

PART_ORDER = ["Board", "Copper", "Plating", "Top Solder Mask", "Top Mask over Copper", "Bottom Solder Mask",
              "Bottom Mask over Copper", "Top Silkscreen", "Bottom Silkscreen", "Top Finish", "Bottom Finish"]


def run(ps, job):
    what = "visible skin" if job.mode == "visual" else "joining the solids of every part"
    with job.stage("assemble", f"assemble ({what})"):
        return assemble(ps, job.mode, job.note)


def rank(name):
    for i, prefix in enumerate(PART_ORDER):
        if name == prefix or name.startswith(prefix + "_") or name.startswith(prefix + " "):
            return (i, name)
    return (len(PART_ORDER), name)


def finished_meshes(ps, mode, log, finish, boundaries):
    """(part, finished mesh) one after another: the skin is made in one go, the solids one part at
    a time.  Without a kernel (Run.BUILD_WITH_KERNELS off) a solid's Boundary is kept for the STEP
    writer, and its mesh is finished by the worker that built it."""
    if mode == "visual":
        skin = skin_meshes(ps) if P.Run.BUILD_WITH_KERNELS else skin_meshes_from_faces(*skin_faces(ps, log))
        while skin:
            part, m = skin.popitem()
            yield part, finish(m)
    elif P.Run.BUILD_WITH_KERNELS:
        for part, m in solid_meshes(ps, log):
            yield part, finish(m)
    else:
        for part, boundary, m in boundaries_and_meshes(ps, log, finish):
            boundaries[part] = boundary
            yield part, m


def assemble(ps, mode, log):
    mat = output_transform()
    merged = not P.Run.BUILD_WITH_KERNELS           # a mesh built from faces has every vertex once already

    def finish(m):
        return finish_mesh(m, mat, merged) if m is not None else None

    done, boundaries = {}, {}
    for part, m in finished_meshes(ps, mode, log, finish, boundaries):   # one raw mesh at a time
        if m is not None:
            done[part] = m
    meshes = {part: done[part] for part in sorted(done, key=rank)}
    props = {}
    for part, prisms in ps.by_part().items():
        p0 = prisms[0]
        pr = dict(p0.props)
        pr.update({"role": p0.role, "layer": p0.layer, "net": p0.net,
                   "z_min_mm": round(min(p.z0 for p in prisms), 6), "z_max_mm": round(max(p.z1 for p in prisms), 6),
                   "prisms": len(prisms)})
        props[part] = pr
    r = ps.regions
    return Model(name=r.items.name, mode=mode, prismset=ps, meshes=meshes, materials=ps.materials, props=props,
                 transform=mat, units=P.Run.UNITS, report=[], circles=r.circles, boundaries=boundaries)
