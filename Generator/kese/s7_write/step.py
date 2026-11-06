"""STEP: every part's solid written from its Boundary straight into a STEP assembly, one named
product per part, planar faces sharing their edges and vertices: closed by construction.  A big
board's parts are worked on in processes of their own (step_parts.py), to the same file."""
from kese.core.parallel import worth_processes
from kese.s7_write.step_brep import write_brep
from kese.s7_write.step_parts import size, topology, write_in_processes
from kese.s7_write.step_writer import StepWriter


def write(model, path, log):
    parts = [part for part in model.meshes                # in the order the parts are listed everywhere
             if part in model.boundaries and model.boundaries[part].flats]
    w = StepWriter(path, model.name, model.units)
    try:
        if worth_processes(len(parts), sum(size(model.boundaries[part]) for part in parts)):
            write_in_processes(w, model, parts, log)
        else:
            for part in parts:
                solids = write_part(w, part, model.boundaries[part], model.transform, log)
                if solids:
                    w.add_part(part, model.materials[part]["rgb"], solids)
        written = w.close()                               # the assembly and the end: a full disk can stop it too
    except BaseException:
        w.discard()
        raise
    if written is None:
        log("step: no part has a solid; STEP skipped")
    return written


def write_part(w, part, boundary, transform, log):
    """One part's solids -> the ids of its MANIFOLD_SOLID_BREP entities."""
    if not boundary.flats:
        return []
    return write_brep(w, topology(part, boundary, log), transform)
