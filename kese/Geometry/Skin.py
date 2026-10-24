"""Skin.py - "visual" mode: the board's visible surface only.

Takes the simulation PrismSet, slices every prism at every height in the stack, rebuilds all regions
from one planar arrangement (so neighbours share exact vertices), triangulates, then drops every
face that lies inside another prism.  The result is one closed outer surface, still split into
named parts.  Layers only microns apart no longer fight for the same pixels in web viewers."""
from collections import defaultdict

import numpy as np
import shapely
import trimesh

from kese.Common import shapes as sh
from parameters import P


def _conform(prisms):
    """Rebuild every region from the arrangement of all boundaries -> (prism, cells) pairs."""
    uniq = {}
    for p in prisms:
        uniq.setdefault(id(p.region), p.region)
    regions = list(uniq.values())
    lines = shapely.union_all([shapely.boundary(r) for r in regions], grid_size=sh.grid())
    cells = np.array(list(shapely.polygonize(list(shapely.get_parts(lines))).geoms), dtype=object)
    if not len(cells):
        return [(p, [p.region]) for p in prisms]
    reps = shapely.get_coordinates(shapely.point_on_surface(cells))
    mine = {}
    for key, region in uniq.items():
        shapely.prepare(region)
        inside = shapely.contains_xy(region, reps[:, 0], reps[:, 1])
        mine[key] = list(cells[inside])
    return [(p, mine[id(p.region)]) for p in prisms if mine[id(p.region)]]


def skin_meshes(ps):
    """PrismSet -> {part name: trimesh of its visible faces} (mm, board frame)."""
    levels = sorted({z for p in ps.prisms for z in (p.z0, p.z1)})
    sliced = []
    for p in ps.prisms:
        cuts = [p.z0] + [z for z in levels if p.z0 < z < p.z1] + [p.z1]
        for a, b in zip(cuts[:-1], cuts[1:]):
            q = type(p)(p.part, p.role, p.region, a, b, p.layer, p.net, p.material, p.props)
            sliced.append(q)
    pairs = _conform(sliced)
    for p, _ in pairs:
        shapely.prepare(p.region)

    def buried(points):
        hit = np.zeros(len(points), dtype=bool)
        for p, _ in pairs:
            m = ~hit & (points[:, 2] > p.z0) & (points[:, 2] < p.z1)
            if m.any():
                hit[m] = shapely.contains_xy(p.region, points[m, 0], points[m, 1])
        return hit

    eps = P.Geometry.SKIN_BURIED_TEST_OFFSET_MM
    groups = defaultdict(list)
    for p, cells in pairs:
        pieces = [m for m in (sh.extrude(c, p.z0, p.z1) for c in cells) if m is not None]
        if not pieces:
            continue
        m = trimesh.util.concatenate(pieces)
        keep = ~buried(m.triangles_center + m.face_normals * eps)
        if keep.any():
            m.update_faces(keep)
            m.remove_unreferenced_vertices()
            groups[p.part].append(m)
    return {part: trimesh.util.concatenate(ms) for part, ms in groups.items()}
