"""STEP packaging: exact B-rep solids built from the prisms (not from triangles), written as a
STEP assembly with one named shape per part.  Parts whose role is in STEP_FUSE_ROLES become one
fused solid; the others are compounds of touching solids.  Needs cadquery (pip install cadquery)."""
import math

import numpy as np

from Generator.Common import shapes as sh
from Generator.Geometry import geometry as geo
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


def _wire(ring, z, cq, M):
    """Closed wire of one polygon ring in output coordinates.  With STEP_EXACT_ARCS the vertex
    runs that lie on one circle (faceted vias, pads, round outlines, track ends, arc tracks)
    become true circular arcs; everything else stays a straight edge."""
    R = P.Run
    pts = list(ring.coords)[:-1]
    V = lambda p: cq.Vector(*_xf(M, p[0], p[1], z))
    arcs = geo.arcs_in_ring(pts, R.STEP_ARC_FIT_TOLERANCE_MM, R.STEP_ARC_MIN_POINTS) if R.STEP_EXACT_ARCS else []
    if not arcs:
        return cq.Wire.makePolygon([V(p) for p in pts], close=True)
    n = len(pts)
    if arcs[0][1] - arcs[0][0] < n:          # an arc found at index 0 may continue from the ring's end:
        s = arcs[0][1] % n                   # restart the ring where it ends and look again
        pts = pts[s:] + pts[:s]
        arcs = geo.arcs_in_ring(pts, R.STEP_ARC_FIT_TOLERANCE_MM, R.STEP_ARC_MIN_POINTS)
    on = lambda c, r, a: (c[0] + r * math.cos(a), c[1] + r * math.sin(a))
    edges, k = [], arcs[0][0]                # walk once around the ring from the first arc
    for i, j, c, r, ccw in arcs:
        for m in range(k, i):                # straight edges up to the arc
            edges.append(cq.Edge.makeLine(V(pts[m % n]), V(pts[(m + 1) % n])))
        a0 = geo.angle(c, pts[i % n])
        if j - i == n:                       # a full circle: two half arcs through the ring's own vertices
            h = (i + n // 2) % n
            q1, q3 = on(c, r, a0 + (1 if ccw else -1) * math.pi / 2), on(c, r, a0 + (3 if ccw else -3) * math.pi / 2)
            edges.append(cq.Edge.makeThreePointArc(V(pts[i % n]), V(q1), V(pts[h])))
            edges.append(cq.Edge.makeThreePointArc(V(pts[h]), V(q3), V(pts[i % n])))
            k = i + n
            break
        else:
            a1 = geo.angle(c, pts[j % n])
            sweep = (a1 - a0) % geo.TAU if ccw else -((a0 - a1) % geo.TAU)
            edges.append(cq.Edge.makeThreePointArc(V(pts[i % n]), V(on(c, r, a0 + sweep / 2)), V(pts[j % n])))
        k = j
    for m in range(k, arcs[0][0] + n):       # straight edges back to the start
        edges.append(cq.Edge.makeLine(V(pts[m % n]), V(pts[(m + 1) % n])))
    return cq.Wire.assembleEdges(edges)


def _face(poly, z, cq, M):
    return cq.Face.makeFromWires(_wire(poly.exterior, z, cq, M), [_wire(r, z, cq, M) for r in poly.interiors])


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
    asm.export(str(path), exportType="STEP")      # cadquery >= 2.5 (save() is deprecated)
    return path
