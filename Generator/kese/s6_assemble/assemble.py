"""Stage 6 - assemble: the PrismSet -> one in-memory Model: meshes per part (closed solids in
"simulation" mode, the visible skin in "visual" mode), output units and orientation, materials and
properties.  Stage 7 writes every file format from this Model; nothing is rebuilt per format."""
from kese.model.output_model import Model
from kese.s6_assemble.skin import skin_meshes
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


def assemble(ps, mode, log):
    mat = output_transform()
    raw = skin_meshes(ps) if mode == "visual" else solid_meshes(ps, log)
    meshes = {}
    for part in sorted(raw, key=rank):
        m = raw[part]
        if m is None:
            continue
        m = finish_mesh(m, mat)
        if m is not None:
            meshes[part] = m
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
                 transform=mat, units=P.Run.UNITS, report=[], circles=r.circles)
