"""The "simulation" mode: every part as one closed solid, the union of its extruded prisms."""
import shapely

from kese.core import shapes2d as sh
from kese.core.extrude import extrude, solid_union
from parameters import P


def part_regions(prisms):
    """The 2D regions of one part, prepared so their solids union cleanly:
    - where two regions touch, each gets the other's boundary vertices (no T-junctions, so the
      shared faces are exactly coplanar);
    - regions that touch only at a point while overlapping in z would meet along a single edge in
      3D and are parted by Geometry.PINCH_POINT_OPENING_MM, as polygons() does inside one polygon."""
    regions = [p.region for p in prisms]
    grid = P.Geometry.SNAP_GRID_MM
    for i in range(len(prisms)):
        for j in range(i + 1, len(prisms)):
            if prisms[i].z1 <= prisms[j].z0 or prisms[j].z1 <= prisms[i].z0 or not regions[i].intersects(regions[j]):
                continue
            regions[i] = sh.polys_only(shapely.snap(regions[i], regions[j], grid / 2))
            regions[j] = sh.polys_only(shapely.snap(regions[j], regions[i], grid / 2))
            touch = regions[i].intersection(regions[j])
            if touch.is_empty or not all(g.geom_type == "Point" for g in getattr(touch, "geoms", [touch])):
                continue
            k = j if regions[j].area <= regions[i].area else i
            regions[k] = sh.polys_only(regions[k].difference(touch.buffer(P.Geometry.PINCH_POINT_OPENING_MM, quad_segs=1)))
    return regions


def solid_meshes(ps, log):
    """PrismSet -> {part name: closed trimesh, or None when the union failed} (mm, board frame)."""
    out = {}
    for part, prisms in ps.by_part().items():
        regions = part_regions(prisms)
        solids = [m for m in (extrude(r, p.z0, p.z1) for r, p in zip(regions, prisms)) if m is not None]
        out[part] = solid_union(solids, log=lambda s: log(f"{part}: {s}"))
    return out
