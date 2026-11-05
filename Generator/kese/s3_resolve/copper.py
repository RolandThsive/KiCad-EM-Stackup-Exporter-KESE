"""Copper: on every layer, the items of each net joined, cut by the holes they touch and clipped
to the outline.  Where two nets overlap, the first keeps the shared area."""
from collections import defaultdict

import shapely
import shapely.errors

from kese.core import shapes2d as sh
from kese.core.graph import pairs_within
from kese.core.parallel import in_parallel, in_processes, worth_processes
from kese.core.shape_copies import own
from kese.core.shapes2d import side_by_side, union
from kese.s3_resolve.holes import hole_shapes
from parameters import P

# nets, counted layer by layer: from this many the layers are joined in processes of their own (if
# worth_processes agrees).  Much of a net's work is then Python's (the loop over the nets, the copies
# of the shapes), which threads take in turn: CIAA ACC (6,200) takes 24.3 s in four threads and 13.2 s
# in four processes, ULX4M (5,526) 17.9 s and 8.7 s, a 4-layer board of 1,720 3.7 s and 2.1 s.  With
# fewer nets most of the work is GEOS's, which threads run as fast without sending the shapes to the
# processes and back: NE_Delta (804 nets on 2 layers, 1.6 million coordinates) 8.0 s and 9.3 s.
PROCESS_MIN_NETS = 1000


def copper_layers(r, items, outline_k, log):
    """r.copper {layer: {net: region}} and r.copper_all {layer: region}; Parallel.WORKERS layers at a
    time, the biggest first, kept in the layers' order: in processes of their own on a board of many
    nets (PROCESS_MIN_NETS), else in threads (copper_of_layer takes its own copies of the shapes
    there)."""
    last = len(items.layers) - 1
    jobs = {k: (k == 0 or k == last, items.copper_items.get(l, []), [h for h in items.holes if h.i <= k <= h.j],
                outline_k, r.to_board_T) for k, l in enumerate(items.layers)}
    size = {k: sum(int(shapely.get_num_coordinates(g)) for g, _ in job[1]) for k, job in jobs.items()}
    order = sorted(jobs, key=lambda k: -size[k])
    nets = sum(len({net for _, net in job[1]}) for job in jobs.values())
    if nets >= PROCESS_MIN_NETS and worth_processes(len(jobs), sum(size.values())):
        done = dict(in_processes(copper_of_layer, [(k, jobs[k]) for k in order], log, "joined", "copper layer"))
    else:
        done = dict(zip(order, in_parallel(lambda k: copper_of_layer(*jobs[k], take=own), order)))
    for k, l in enumerate(items.layers):
        r.copper[l] = done[k]
        r.copper_all[l] = side_by_side(list(done[k].values()))


def copper_of_layer(outer, mine, holes, outline_k, T, take=lambda g: g):
    """{net: region} of one copper layer: each net's items `mine` [(shape, net)] joined, cut by the
    holes it touches, clipped to the outline, board frame (by T).  `outer`: a face's layer.  In a
    thread, take=own: the outline, the holes and the items (a pad or a via is on several layers) are
    this thread's own copies (kese/core/shape_copies.py)."""
    outline_k = take(outline_k)
    # outer copper caps the barrel (cut by the open bore); inner copper stops at the drill wall
    holes = [g for g in hole_shapes(holes, lambda h: True, bore=outer, take=take) if not g.is_empty]
    tree = shapely.STRtree(holes)
    per_net = defaultdict(list)
    for (_, net), g in zip(mine, take([g for g, _ in mine])):
        per_net[net].append(g)
    regions = {}
    for net, gs in per_net.items():
        cu = net_union(gs) if len(gs) > 1 else gs[0]
        if P.Geometry.SIMPLIFY_TOLERANCE_MM > 0:   # before the cuts: the board edge and the holes stay exact
            cu = cu.simplify(P.Geometry.SIMPLIFY_TOLERANCE_MM)
        cu = cu.intersection(outline_k)
        near = tree.query(cu, predicate="intersects") if not cu.is_empty else []
        if len(near):                          # only the holes this net touches, as KiCad cuts
            cu = cu.difference(union([holes[i] for i in near]))
        cu = close_hairline_gaps(fill_hairline_holes(T(cu)))     # on the grid, where the hairlines show
        if not cu.is_empty:
            regions[net] = cu
    return first_net_keeps(regions)


def net_union(gs):
    """A net's items on one layer joined: in floating point, then the union rounded to the grid as a
    whole (set_precision), so two shapes whose edges run along the same line only to within floating
    point (two zone fills, a fill and a pad) meet on the grid and join cleanly instead of leaving a
    crack.  A union on the grid rounds every item first and costs about three times as much on a big
    board; it is still the way when GEOS cannot join the items in floating point.  The whole union in
    one call, not part by part (shapes2d.snap): the work stays GEOS's, which runs outside Python's
    lock, so the layers' threads keep working at once.  The result is copied through WKB onto no grid,
    as a union on the grid comes out: a shape rounded by set_precision carries the grid, and GEOS
    would then clip it to the outline on the grid, bending the outline's edge through every copper
    vertex within a grid step of it (a burr past the board edge where a zone fill follows its own
    chords of an arc)."""
    try:
        g = shapely.set_precision(shapely.union_all(gs), sh.grid())
    except shapely.errors.GEOSException:
        return shapely.union_all(gs, grid_size=sh.grid())
    g = shapely.from_wkb(shapely.to_wkb(g))
    return g.geoms[0] if g.geom_type == "MultiPolygon" and len(g.geoms) == 1 else g     # as a union gives it


def close_hairline_gaps(cu):
    """A net's copper with the pieces that meet within two grid steps joined (grown and shrunk back
    by a grid step, mitred), which would otherwise leave two walls that do not quite agree."""
    parts = list(shapely.get_parts(cu)) if cu.geom_type == "MultiPolygon" else []
    if len(parts) < 2:
        return cu
    g = sh.grid()
    i, j = pairs_within(parts, 2 * g)
    near = sorted(set(i.tolist()) | set(j.tolist()))
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
