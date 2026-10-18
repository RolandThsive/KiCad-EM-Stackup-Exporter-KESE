"""STEP packaging: exact B-rep solids built from the prisms (not from triangles), written as a
STEP assembly with one named shape per part.  Parts whose role is in STEP_FUSE_ROLES become one
fused solid; the others are compounds of touching solids.  Needs cadquery (pip install cadquery)."""
import numpy as np

from Generator.Common import shapes as sh
from Parameters import P


def available():
    try:
        import cadquery  # noqa: F401
        return True
    except ImportError:
        return False


def _xf(M, x, y, z):
    v = M @ np.array([x, y, z, 1.0])
    return float(v[0]), float(v[1]), float(v[2])


def _face(poly, z, cq, M):
    outer = cq.Wire.makePolygon([cq.Vector(*_xf(M, x, y, z)) for x, y in list(poly.exterior.coords)[:-1]], close=True)
    inners = [cq.Wire.makePolygon([cq.Vector(*_xf(M, x, y, z)) for x, y in list(r.coords)[:-1]], close=True)
              for r in poly.interiors]
    return cq.Face.makeFromWires(outer, inners)


def _solid(prism, cq, M):
    """All polygons of one prism, extruded, as a list of cq.Solid, built directly in output
    units and orientation (transforming afterwards would convert every edge to splines)."""
    out = []
    d = M[:3, :3] @ np.array([0.0, 0.0, prism.z1 - prism.z0])
    for poly in sh.polygons(prism.region):
        if poly.area <= 1e-10:
            continue
        face = _face(poly, prism.z0, cq, M)
        out.append(cq.Solid.extrudeLinear(face, cq.Vector(*map(float, d))))
    return out


def write(model, path, log):
    if not available():
        log("step: cadquery is not installed (pip install cadquery); STEP skipped")
        return None
    import cadquery as cq
    R = P.Run
    M = np.asarray(model.transform, dtype=float)
    asm = cq.Assembly(name=model.name)
    for part, prisms in model.prismset.by_part().items():
        role = prisms[0].role
        if role not in R.STEP_WRITE_ROLES:
            continue
        # pieces with the same z band are merged in 2D first: a mask layer becomes a handful of
        # multipolygon prisms instead of thousands of tiny solids (keeps memory and file size sane)
        bands = {}
        for p in prisms:
            bands.setdefault((round(p.z0, 9), round(p.z1, 9)), []).append(p)
        solids = []
        for (z0, z1), group in bands.items():
            region = group[0].region if len(group) == 1 else sh.snap(sh.union([g.region for g in group]))
            q = type(group[0])(group[0].part, group[0].role, region, z0, z1)
            solids += _solid(q, cq, M)
        if not solids:
            continue
        if role in R.STEP_FUSE_ROLES and len(solids) > 1:
            try:
                shape = solids[0].fuse(*solids[1:], glue=True).clean()
            except Exception as exc:
                log(f"step: fuse failed for {part} ({exc}); written as a compound")
                shape = cq.Compound.makeCompound(solids)
        else:
            shape = solids[0] if len(solids) == 1 else cq.Compound.makeCompound(solids)
        rgb = model.materials[part]["rgb"]
        asm.add(shape, name=part, color=cq.Color(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, model.materials[part]["alpha"]))
    asm.save(str(path), exportType="STEP")
    return path
