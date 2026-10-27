"""STEP with a CAD kernel (Run.BUILD_WITH_KERNELS): exact B-rep solids built from the prisms by
OpenCascade, written as a STEP assembly with one named shape per part.  Parts whose role is in
STEP_FUSE_ROLES become one fused solid; the others are compounds of touching solids.  Each part is
written to the file as soon as it is made (see step_file.py), so only one part is held in memory
at a time.  Needs cadquery (pip install cadquery)."""
from pathlib import Path

import numpy as np

from kese.core import shapes2d as sh
from kese.s7_write.step_arcs import ring_arcs
from kese.s7_write.step_curves import Circles, wire
from kese.s7_write.step_file import StepFile
from parameters import P


def available():
    try:
        import cadquery  # noqa: F401
        return True
    except ImportError:
        return False


def _face(rings, z, cq, M):
    return cq.Face.makeFromWires(wire(*rings[0], z, cq, M), [wire(*r, z, cq, M) for r in rings[1:]])


def _solid(prism, cq, M, circles):
    """All polygons of one prism, extruded, as a list of cq.Solid, built directly in output
    units and orientation (transforming afterwards would convert every edge to splines)."""
    d = M[:3, :3] @ np.array([0.0, 0.0, prism.z1 - prism.z0])
    polys = [poly for poly in sh.polygons(prism.region) if poly.area > 1e-10]
    return [cq.Solid.extrudeLinear(_face(rings, prism.z0, cq, M), cq.Vector(*map(float, d)))
            for rings in ring_arcs(polys, circles)]


def write(model, path, log):
    if not available():
        log("step: cadquery is not installed (pip install cadquery); STEP skipped")
        return None
    import cadquery as cq
    R = P.Run
    M = np.asarray(model.transform, dtype=float)
    circles = Circles(model.circles)
    out, one = StepFile(path), Path(path).with_name(Path(path).name + ".part")
    try:
        for part, prisms in model.prismset.by_part().items():
            if prisms[0].role in R.STEP_WRITE_ROLES and _write_part(part, prisms, model, cq, M, circles, one, log):
                out.add(one)                          # (the part's solids are freed by now)
        written = out.close()
    finally:
        out.discard()
        one.unlink(missing_ok=True)
    if written is None:
        log("step: no part to write; STEP skipped")
    return written


def _write_part(part, prisms, model, cq, M, circles, one, log):
    """One part as an exact solid, written to `one` as an assembly of that part.  -> False when
    the part has no solid."""
    R = P.Run
    role = prisms[0].role
    # pieces with the same z band are merged in 2D first: a mask layer becomes a handful of
    # multipolygon prisms instead of thousands of tiny solids (keeps memory and file size sane)
    bands = {}
    for p in prisms:
        bands.setdefault((round(p.z0, 9), round(p.z1, 9)), []).append(p)
    solids = []
    for (z0, z1), group in bands.items():
        region = group[0].region if len(group) == 1 else sh.snap(sh.union([g.region for g in group]))
        q = type(group[0])(group[0].part, group[0].role, region, z0, z1)
        solids += _solid(q, cq, M, circles)
    if not solids:
        return False
    if role in R.STEP_FUSE_ROLES and len(solids) > 1:
        try:
            shape = solids[0].fuse(*solids[1:], glue=True).clean()
        except Exception as exc:
            log(f"step: fuse failed for {part} ({exc}); written as a compound")
            shape = cq.Compound.makeCompound(solids)
    else:
        shape = solids[0] if len(solids) == 1 else cq.Compound.makeCompound(solids)
    rgb = model.materials[part]["rgb"]
    asm = cq.Assembly(name=model.name)
    asm.add(shape, name=part, color=cq.Color(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, model.materials[part]["alpha"]))
    asm.export(str(one), exportType="STEP")   # cadquery >= 2.5 (save() is deprecated)
    return True
