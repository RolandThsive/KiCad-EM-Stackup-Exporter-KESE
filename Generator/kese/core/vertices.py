"""Shared vertices: where two polygons meet, each gets the other's vertices that lie on its edges,
so the faces built on them meet on identical edges (no T-junctions).  All 2D, on the grid of
Geometry.SNAP_GRID_MM."""
import numpy as np
import shapely

from kese.core import shapes2d as sh


def near_edge():
    """How far from an edge a vertex may lie and still count as on it: half a grid diagonal (GEOS
    rounds crossings to the grid), less than the full step between two grid points."""
    return sh.grid() * 0.75


def grid_keys(xy):
    """One integer per point: which grid point it is."""
    k = np.round(xy / sh.grid()).astype(np.int64)
    return k[:, 0] * (1 << 32) + k[:, 1]


def vertices_in_order(level, key):
    """One vertex per distinct (height, grid point), numbered from the lowest height up: the vertex
    of every (level, key) given, and the first position of every vertex.  Faces that share a
    vertex get the same number for it, which is what makes a mesh or a B-rep closed."""
    order = np.lexsort((key, level))
    new = np.r_[True, (level[order][1:] != level[order][:-1]) | (key[order][1:] != key[order][:-1])]
    vertex = np.empty(len(order), dtype=np.int64)
    vertex[order] = np.cumsum(new) - 1
    return vertex, order[new]


def pairs_in(a, b, c, d):
    """Whether each pair of integers (a[i], b[i]) is among the pairs (c[j], d[j]).  Each pair is
    hashed to one integer, the pairs (c, d) sorted by it once and every (a, b) found by binary search
    and then compared in full.  Where two different pairs (c, d) hash alike, which a 64-bit hash all
    but never does, each column is numbered through its distinct values instead (pairs_numbered)."""
    if not len(a) or not len(c):
        return np.zeros(len(a), dtype=bool)
    a, b, c, d = (np.asarray(x, dtype=np.int64) for x in (a, b, c, d))
    hc = pair_hash(c, d)
    order = np.argsort(hc)
    hc = hc[order]
    run = np.flatnonzero(hc[1:] == hc[:-1])              # sorted next to a pair of the same hash
    if ((c[order[run]] != c[order[run + 1]]) | (d[order[run]] != d[order[run + 1]])).any():
        return pairs_numbered(a, b, c, d)
    ha = pair_hash(a, b)
    at = np.minimum(np.searchsorted(hc, ha), len(hc) - 1)
    j = order[at]
    return (hc[at] == ha) & (c[j] == a) & (d[j] == b)


def pair_hash(x, y):
    """One 64-bit integer for each pair (x[i], y[i]): SplitMix64's mixing of x, plus y, mixed again."""
    return _mixed(_mixed(x.view(np.uint64)) + y.view(np.uint64))


def _mixed(z):
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return z ^ (z >> np.uint64(31))


def pairs_numbered(a, b, c, d):
    """pairs_in() by numbering each column through its distinct values, so that a pair is one integer
    np.isin can sort (a record of two integers it sorts twenty times slower)."""
    first = np.unique(np.concatenate([a, c]), return_inverse=True)[1]
    second = np.unique(np.concatenate([b, d]), return_inverse=True)[1]
    key = first.astype(np.int64) * (second.max() + 1) + second
    return np.isin(key[:len(a)], key[len(a):])


def share_vertices(regions, sources):
    """The regions, every ring with every vertex of the other regions and the sources that lies on one
    of its edges, and the indices of the regions that changed."""
    pieces, owner = [], []
    for i, r in enumerate(regions):
        for p in shapely.get_parts(r):
            pieces.append(p)
            owner.append(i)
    if not pieces:
        return list(regions), set()
    pieces, owner = np.array(pieces, dtype=object), np.array(owner)
    rings, of_piece = shapely.get_rings(pieces, return_index=True)
    xy, ring = shapely.get_coordinates(rings, return_index=True)
    key, region = grid_keys(xy), owner[of_piece[ring]]
    more = shapely.get_coordinates(list(sources)) if len(sources) else np.empty((0, 2))
    every, every_key = np.concatenate([xy, more]), np.concatenate([key, grid_keys(more)])
    edge = np.flatnonzero(ring[1:] == ring[:-1])                        # the edge from point i to point i + 1
    first, which = np.unique(every_key, return_index=True, return_inverse=True)[1:]   # grid points: the first point at each, which each point is at
    wanted = {}                                                          # ring -> the vertices (indices into every) it gets
    for i in range(len(regions)):
        mine = edge[region[edge] == i]
        has = np.zeros(len(first), dtype=bool)
        has[which[:len(xy)][region == i]] = True
        lacking = first[~has]                                            # one vertex per grid point the region has none at
        if not len(mine) or not len(lacking):
            continue
        tree = shapely.STRtree(shapely.linestrings(np.stack([xy[mine], xy[mine + 1]], axis=1)))
        pt, ed = tree.query(shapely.points(every[lacking]), predicate="dwithin", distance=near_edge())
        for h, p in zip(ring[mine[ed]].tolist(), lacking[pt].tolist()):
            wanted.setdefault(h, []).append(p)
    if not wanted:
        return list(regions), set()
    for h, pts in wanted.items():
        rings[h] = shapely.snap(rings[h], shapely.multipoints(every[pts]), near_edge())
    changed = set()
    for h in np.unique(of_piece[list(wanted)]).tolist():
        shell, *holes = [np.asarray(r.coords) for r in rings[of_piece == h]]
        pieces[h] = shapely.Polygon(shell, holes)
        changed.add(int(owner[h]))
    out = [sh.as_region([q for p in pieces[owner == i] for q in shapely.get_parts(p)]) if i in changed else r
           for i, r in enumerate(regions)]
    return out, changed


def walls_split_at_vertices(walls, sources):
    """The wall segments of several regions, each split at every vertex of the other regions and the
    sources that lies on it (near_edge()), nothing moved.  -> the segments per region, (n, 2, 2)."""
    segments = np.concatenate(walls)
    region = np.repeat(np.arange(len(walls)), [len(w) for w in walls])
    more = shapely.get_coordinates(list(sources)) if len(sources) else np.empty((0, 2))
    every = np.concatenate([segments[:, 0], more])                       # every vertex starts a segment
    key = grid_keys(every)
    one = np.unique(key, return_index=True)[1]                           # one point per grid point
    tree = shapely.STRtree(shapely.linestrings(segments))
    pt, ed = tree.query(shapely.points(every[one]), predicate="dwithin", distance=near_edge())
    own = pairs_in(region[ed], key[one][pt], region, key[:len(segments)])   # a vertex of the segment's own region
    pt, ed = pt[~own], ed[~own]
    if not len(ed):
        return list(walls)
    p, a, b = every[one][pt], segments[ed, 0], segments[ed, 1]
    along = np.einsum("ij,ij->i", p - a, b - a) / np.einsum("ij,ij->i", b - a, b - a)   # how far along the segment
    order = np.lexsort((along, ed))
    ed, p = ed[order], p[order]
    first = np.r_[True, ed[1:] != ed[:-1]]                               # the first vertex on its segment
    last = np.r_[ed[1:] != ed[:-1], True]
    before = np.where(first[:, None], segments[ed, 0], np.roll(p, 1, axis=0))   # what each vertex follows
    split = np.concatenate([np.stack([before, p], axis=1), np.stack([p[last], segments[ed[last], 1]], axis=1)])
    whole = np.ones(len(segments), dtype=bool)
    whole[ed] = False
    out = np.concatenate([segments[whole], split])
    of = np.concatenate([region[whole], region[ed], region[ed[last]]])
    order = np.argsort(of, kind="stable")
    return np.split(out[order], np.cumsum(np.bincount(of, minlength=len(walls)))[:-1])


def noded(g):
    """The region as a set operation on the grid leaves it: noded (GEOS's hot pixels) again until it
    changes nothing, so every later set operation meets it on identical edges."""
    g = sh.polys_only(g)
    for _ in range(sh.G().NODING_ROUNDS):
        try:
            again = sh.polys_only(g.difference(sh.EMPTY, grid_size=sh.grid()))
        except shapely.errors.GEOSException:      # a ring that crosses itself (a KiCad 4 board): made valid
            again = sh.polys_only(sh.polys_only(shapely.make_valid(g)).difference(sh.EMPTY, grid_size=sh.grid()))
        if same_vertices(again, g):
            return again
        g = again
    return g


def same_vertices(a, b):
    """Whether two regions have the same vertices, whatever point each ring starts at.  Each point
    is sorted as one complex number (x, y), in one pass: three times as fast as by y and then x."""
    xa, xb = ring_points(a), ring_points(b)
    if len(xa) != len(xb):
        return False
    return np.array_equal(*(np.sort(np.ascontiguousarray(x).view(np.complex128).ravel()) for x in (xa, xb)))


def ring_points(region):
    """The xy of every vertex of the region's rings, each ring's closing point left out."""
    xy, ring = shapely.get_coordinates(shapely.get_rings(shapely.get_parts(region)), return_index=True)
    return xy[np.r_[ring[1:] == ring[:-1], False][:len(xy)]]       # [:len(xy)]: nothing of an empty region
