"""The "simulation" mode: every part as one closed solid, the union of its extruded prisms."""
import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.extrude import extrude, solid_union
from parameters import P


def part_regions(prisms):
    """The 2D regions of one part, prepared so their solids union cleanly:
    - where two regions touch, each gets the other's boundary vertices (no T-junctions, so the
      shared faces are exactly coplanar);
    - regions that touch only at a point while overlapping in z would meet along a single edge in
      3D and are parted by Geometry.PINCH_POINT_OPENING_MM, as polygons() does inside one polygon.
    Regions cut from one another on the grid already share their vertices, so both are checked by
    an index of the vertices first and only the pieces that need it are changed."""
    regions = [p.region for p in prisms]
    for i in range(len(prisms)):
        for j in range(i + 1, len(prisms)):
            if prisms[i].z1 <= prisms[j].z0 or prisms[j].z1 <= prisms[i].z0 or not regions[i].intersects(regions[j]):
                continue
            regions[i] = with_vertices_of(regions[i], regions[j])
            regions[j] = with_vertices_of(regions[j], regions[i])
            if shares_an_edge(regions[i], regions[j]):
                continue
            touch = regions[i].intersection(regions[j])
            if touch.is_empty or not all(g.geom_type == "Point" for g in getattr(touch, "geoms", [touch])):
                continue
            k = j if regions[j].area <= regions[i].area else i
            regions[k] = sh.polys_only(regions[k].difference(touch.buffer(P.Geometry.PINCH_POINT_OPENING_MM, quad_segs=1)))
    return regions


def keys(g):
    """The vertices of a region as integers on the grid, and which ring each lies on."""
    xy, ring = shapely.get_coordinates(shapely.get_rings(shapely.get_parts(g)), return_index=True)
    k = np.round(xy / sh.grid()).astype(np.int64)
    return k[:, 0] * (1 << 32) + k[:, 1], ring, xy


def with_vertices_of(a, b):
    """a, with the vertices of b that lie on a's edges added to it (what shapely.snap does, for
    only the parts of a that need it)."""
    ka, _, _ = keys(a)
    kb, _, xyb = keys(b)
    lone = xyb[~np.isin(kb, ka)]
    if not len(lone):
        return a
    edge = shapely.boundary(a)
    shapely.prepare(edge)
    on = lone[shapely.dwithin(edge, shapely.points(lone), sh.grid() / 2)]
    if not len(on):
        return a
    parts = shapely.get_parts(a)
    pts = shapely.points(on)
    hit = np.unique(shapely.STRtree(parts).query(pts, predicate="dwithin", distance=sh.grid())[1])
    for h in hit.tolist():
        parts[h] = sh.polys_only(shapely.snap(parts[h], shapely.multipoints(on), sh.grid() / 2))
    return sh.polys_only(shapely.MultiPolygon([q for p in parts for q in shapely.get_parts(p)]) if len(parts) > 1 else parts[0])


def edges(g):
    """The edges of a region as sorted pairs of vertex keys."""
    k, ring, _ = keys(g)
    same = ring[1:] == ring[:-1]
    e = np.stack([k[:-1][same], k[1:][same]], axis=1)
    return np.sort(e, axis=1)


def shares_an_edge(a, b):
    ea, eb = edges(a), edges(b)
    va = ea.view([("p", np.int64), ("q", np.int64)]).ravel()
    vb = eb.view([("p", np.int64), ("q", np.int64)]).ravel()
    return bool(np.isin(vb, va).any())


def solid_meshes(ps, log):
    """PrismSet -> (part name, closed trimesh, or None when the union failed) for one part after
    another (mm, board frame), so that each can be finished before the next one is built.  The
    biggest parts come first: their union, the one that needs the most memory, runs while little
    else is held."""
    parts = ps.by_part()
    size = {part: sum(shapely.get_num_coordinates(p.region) for p in prisms) for part, prisms in parts.items()}
    for part in sorted(parts, key=lambda k: -size[k]):
        yield part, part_solid(parts[part], lambda s, part=part: log(f"{part}: {s}"))


def part_solid(prisms, log):
    """The prisms of one part -> its closed trimesh, or None when the union failed."""
    regions = part_regions(prisms)
    return solid_union([m for m in (extrude(r, p.z0, p.z1) for r, p in zip(regions, prisms)) if m is not None], log=log)
