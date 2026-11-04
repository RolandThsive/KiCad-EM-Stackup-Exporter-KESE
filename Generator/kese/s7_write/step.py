"""STEP: every part's solid written from its Boundary straight into a STEP assembly, one named
product per part, planar faces sharing their edges and vertices: closed by construction."""
from kese.s7_write.step_brep import write_brep
from kese.s7_write.step_curved import with_arcs
from kese.s7_write.step_topology import topology_of
from kese.s7_write.step_writer import StepWriter
from parameters import P


def write(model, path, log):
    w = StepWriter(path, model.name, model.units)
    try:
        for part in model.meshes:                         # in the order the parts are listed everywhere
            if part in model.boundaries:
                solids = write_part(w, part, model.boundaries[part], model.transform, log)
                if solids:
                    w.add_part(part, model.materials[part]["rgb"], solids)
    except BaseException:
        w.discard()
        raise
    written = w.close()
    if written is None:
        log("step: no part has a solid; STEP skipped")
    return written


def write_part(w, part, boundary, transform, log):
    """One part's solids -> the ids of its MANIFOLD_SOLID_BREP entities."""
    if not boundary.flats:
        return []
    topo = topology_of(boundary)
    if topo.edges_not_used_twice:
        log(f"step: {part}: {topo.edges_not_used_twice} edges are not shared by two faces (the solid is open there)")
    if P.Step.STEP_EXACT_ARCS:
        try:
            topo = with_arcs(topo)
        except Exception as e:                            # a bug in the arcs must not cost the file: faceted instead
            log(f"step: {part}: written without arcs ({type(e).__name__}: {e})")
    return write_brep(w, topo, transform)
