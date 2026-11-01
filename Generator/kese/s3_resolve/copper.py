"""Copper: on every layer, the items of each net joined, cut by the holes they touch and clipped
to the outline.  Where two nets overlap, the first keeps the shared area."""
from collections import defaultdict

import shapely

from kese.core import shapes2d as sh
from kese.core.shapes2d import side_by_side, union
from kese.s3_resolve.holes import hole_shapes
from parameters import P


def copper_layers(r, items, outline_k):
    """r.copper {layer: {net: region}} and r.copper_all {layer: region}."""
    T, last = r.to_board_T, len(items.layers) - 1
    for k, l in enumerate(items.layers):
        # outer copper caps the barrel (cut by the open bore); inner copper stops at the drill wall
        holes = [g for g in hole_shapes(items, lambda h, k=k: h.i <= k <= h.j, bore=k in (0, last)) if not g.is_empty]
        tree = shapely.STRtree(holes)
        per_net = defaultdict(list)
        for g, net in items.copper_items.get(l, []):
            per_net[net].append(g)
        regions = {}
        for net, gs in per_net.items():
            # joined on the grid: two shapes whose edges run along the same line only to within
            # floating point (two zone fills, a fill and a pad) join cleanly instead of leaving a crack
            cu = shapely.union_all(gs, grid_size=sh.grid()) if len(gs) > 1 else gs[0]
            if P.Geometry.SIMPLIFY_TOLERANCE_MM > 0:   # before the cuts: the board edge and the holes stay exact
                cu = cu.simplify(P.Geometry.SIMPLIFY_TOLERANCE_MM)
            cu = cu.intersection(outline_k)
            near = tree.query(cu, predicate="intersects") if not cu.is_empty else []
            if len(near):                          # only the holes this net touches, as KiCad cuts
                cu = cu.difference(union([holes[i] for i in near]))
            cu = close_hairline_gaps(fill_hairline_holes(T(cu)))     # on the grid, where the hairlines show
            if not cu.is_empty:
                regions[net] = cu
        r.copper[l] = first_net_keeps(regions)
        r.copper_all[l] = side_by_side(list(r.copper[l].values()))


def close_hairline_gaps(cu):
    """A net's copper with the pieces that meet within two grid steps joined (grown and shrunk back
    by a grid step, mitred), which would otherwise leave two walls that do not quite agree."""
    parts = list(shapely.get_parts(cu)) if cu.geom_type == "MultiPolygon" else []
    if len(parts) < 2:
        return cu
    g = sh.grid()
    i, j = shapely.STRtree(parts).query(parts, predicate="dwithin", distance=2 * g)
    near = sorted(set(i[i < j].tolist()) | set(j[i < j].tolist()))
    if not near:
        return cu
    joined = union([parts[k].buffer(g, join_style="mitre") for k in near]).buffer(-g, join_style="mitre")
    keep = set(near)
    return sh.snap(union([joined] + [p for k, p in enumerate(parts) if k not in keep]))




def fill_hairline_holes(cu):
    """A net's copper with its hairline holes filled: a hole whose mean width (twice its area over its
    perimeter) is under Copper.HAIRLINE_HOLE_MM, as KiCad's zone fill leaves round its own pads."""
    if cu.is_empty or cu.geom_type not in ("Polygon", "MultiPolygon"):
        return cu
    parts, changed = [], False
    for p in shapely.get_parts(cu):
        keep = [r for r in p.interiors if 2 * shapely.Polygon(r).area >= P.Copper.HAIRLINE_HOLE_MM * r.length]
        changed |= len(keep) != len(p.interiors)
        parts.append(shapely.Polygon(p.exterior, keep) if len(keep) != len(p.interiors) else p)
    return union(parts) if changed else cu      # union: a filled hole may hold a speck of its own


def first_net_keeps(regions):
    """Copper of different nets never overlaps on a real board; if the file has overlaps, the first
    net keeps the shared area so the solids stay disjoint.  A net is cut only by the earlier nets
    it really meets (the union of those, trimmed or not, is the same area)."""
    nets = list(regions)
    geoms = [regions[n] for n in nets]
    tree = shapely.STRtree(geoms)
    for i, n in enumerate(nets):
        hits = [geoms[j] for j in tree.query(geoms[i]) if j < i and geoms[i].intersects(geoms[j])]
        if hits:
            regions[n] = sh.diff(regions[n], union(hits))
    return {n: g for n, g in regions.items() if not g.is_empty}


def join_nets(r):
    """r.copper_all once more, after edge plating has changed the copper (nothing changed without it)."""
    if r.edge_band is None:
        return
    for l in r.layers:
        r.copper_all[l] = side_by_side(list(r.copper[l].values()))
