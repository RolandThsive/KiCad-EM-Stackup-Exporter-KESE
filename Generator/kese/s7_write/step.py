"""STEP: every part's exact solid, written from its Boundary (the faces found in 2D in stage 6)
straight into a STEP assembly, one named product per part, with no CAD kernel.  The flat faces
and the walls are written as they are, planar, with the vertices and edges that neighbouring
faces share written once (kese/s7_write/step_topology.py); so every part is a closed solid by
construction, and the file says so to any reader.  With Run.BUILD_WITH_KERNELS the solids are
built and written by OpenCascade instead (kese/s7_write/step_cadquery.py)."""
from kese.s7_write.step_brep import write_brep
from kese.s7_write.step_topology import topology_of
from kese.s7_write.step_writer import StepWriter
from parameters import P


def write(model, path, log):
    if P.Run.BUILD_WITH_KERNELS:
        from kese.s7_write.step_cadquery import write as write_with_cadquery
        return write_with_cadquery(model, path, log)
    w = StepWriter(path, model.name, model.units)
    try:
        for part in model.meshes:                         # in the order the parts are listed everywhere
            if part in model.boundaries and model.props[part]["role"] in P.Run.STEP_WRITE_ROLES:
                solids = write_part(w, part, model.boundaries[part], model.transform, log)
                if solids:
                    w.add_part(part, model.materials[part]["rgb"], solids)
    except BaseException:
        w.discard()
        raise
    written = w.close()
    if written is None:
        log("step: no part to write; STEP skipped")
    return written


def write_part(w, part, boundary, transform, log):
    """One part's solids -> the ids of its MANIFOLD_SOLID_BREP entities."""
    if not boundary.flats:
        return []
    topo = topology_of(boundary)
    if topo.edges_not_used_twice:
        log(f"step: {part}: {topo.edges_not_used_twice} edges are not shared by two faces (the solid is open there)")
    return write_brep(w, topo, transform)
