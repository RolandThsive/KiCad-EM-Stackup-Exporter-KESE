"""Shared vertices.  Where two polygons meet, each must have the other's vertices that lie on its
edges, so that no edge ends in the middle of another edge (no T-junctions): then the faces built
on them meet on identical edges.  The same holds between the rings of one polygon.  Polygons cut
from one another on the snap grid share their vertices already, so the vertices are first looked
up and only the rings that lack one are changed.  A region is first brought into the form the
grid's set operations leave it in (noded()), so that cutting from it changes nothing else.
Everything here is 2D, on the grid of Geometry.SNAP_GRID_MM."""
import numpy as np
import shapely

from kese.core import shapes2d as sh


def near_edge():
    """How far from an edge a vertex may lie and still count as on it.  Where two edges cross,
    GEOS rounds the crossing to the grid, which puts it up to half a grid diagonal (0.71 of a
    step) off either edge; and two distinct grid points are a full step apart, so nothing else
    is caught."""
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


def vertex_keys(region):
    """The vertices of a region as grid keys, the ring each lies on, and the xy."""
    xy, ring = shapely.get_coordinates(shapely.get_rings(shapely.get_parts(region)), return_index=True)
    return grid_keys(xy), ring, xy


def pairs_in(a, b, c, d):
    """Whether each pair (a[i], b[i]) is among the pairs (c[j], d[j]).  Each column is numbered
    through its distinct values, so that a pair is one integer and np.isin sorts plain integers
    (a record of two integers it sorts twenty times slower, holding the whole program up)."""
    if not len(a):
        return np.zeros(0, dtype=bool)
    first = np.unique(np.concatenate([a, c]), return_inverse=True)[1]
    second = np.unique(np.concatenate([b, d]), return_inverse=True)[1]
    key = first.astype(np.int64) * (second.max() + 1) + second
    return np.isin(key[:len(a)], key[len(a):])


def share_vertices(regions, sources=()):
    """The regions, every ring of them with every vertex of the other regions and of the sources
    that lies on one of its edges, and the indices of the regions that changed.  A vertex of its
    own region a ring has already wherever it matters: GEOS put it on the edge, noding (noded()),
    if the edge came within the vertex's hot pixel, and no set operation will bend the edge
    otherwise.  The vertices are gathered once, and against the edges of each region only the
    vertices it lacks are looked up, in one query of an index of those edges."""
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


def walls_split_at_vertices(walls, sources=()):
    """The wall segments of several regions (wall_segments() of each), every segment split at each
    vertex of the other regions and of the sources that lies on it, within near_edge(): where
    share_vertices() would bend the edge onto the vertex, nothing moves here; the vertex goes into
    the wall as it is, so that the wall meets the face or the neighbouring wall that has the vertex
    on identical edges.  A region's own vertices its walls have already (its rings are noded).
    -> the segments per region, (n, 2, 2) arrays."""
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


NODING_ROUNDS = 8        # of a set operation on the grid, until it changes nothing (one or two, in practice)


def noded(g):
    """The region as a set operation on the grid leaves it.  GEOS nodes the inputs of every set
    operation on the grid: wherever an edge passes within half a grid step of a vertex (through
    the vertex's "hot pixel"), the vertex is put on the edge, and a spike that collapses onto its
    own edge then goes.  It does so in one pass, which can bend an edge onto a vertex and through
    another vertex's hot pixel; so the operation (taking nothing away) is repeated until it changes
    nothing, and from then on every set operation meets the region on identical edges.  (Not
    set_precision(), which leaves an edge that only touches the corner of one of its own ring's
    hot pixels as it is.)"""
    g = sh.polys_only(g)
    for _ in range(NODING_ROUNDS):
        again = sh.polys_only(g.difference(sh.EMPTY, grid_size=sh.grid()))
        if same_vertices(again, g):
            return again
        g = again
    return g


def same_vertices(a, b):
    """Whether two regions have the same vertices, whatever point each ring starts at."""
    xa, xb = ring_points(a), ring_points(b)
    return len(xa) == len(xb) and np.array_equal(xa[np.lexsort(xa.T)], xb[np.lexsort(xb.T)])


def ring_points(region):
    """The xy of every vertex of the region's rings, each ring's closing point left out."""
    xy, ring = shapely.get_coordinates(shapely.get_rings(shapely.get_parts(region)), return_index=True)
    return xy[np.r_[ring[1:] == ring[:-1], False][:len(xy)]]       # [:len(xy)]: nothing of an empty region
