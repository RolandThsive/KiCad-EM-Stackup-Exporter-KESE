"""Walls that run on unchanged across the heights only a few small shapes bring.  A counterbore or
countersink, or a via's plug, adds heights of its own (PrismSet.free_levels), and every part spanning
them is cut into slices there, each with its walls.  A wall segment that is the same in two slices
one above the other is joined into one taller wall, unless a face or another wall has a vertex at
that height on one of its two upright edges: then the edge must stop there, or the mesh would have a
vertex in the middle of an edge (a crack).  Such a vertex stops every wall that shares the point and
height, and those walls' other ends then stop too: the stops spread along a ring of unchanged walls,
found at once as the connected parts of a graph of (point, height)."""
import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.graph import connected_components
from kese.core.triangulate import rings_of
from kese.core.vertices import grid_keys


def flat_points(flats, at):
    """(level, grid key) of every vertex of the flat faces [(z, region, looks up)]."""
    levels, keys = [], []
    for z, region, _ in flats:
        polys = np.array([p for p in shapely.get_parts(sh.polys_only(region)) if not p.is_empty], dtype=object)
        if not len(polys):
            continue
        xy = rings_of(polys)[0]
        levels.append(np.full(len(xy), at[z]))
        keys.append(grid_keys(xy))
    if not levels:
        return np.zeros(0, np.int64), np.zeros(0, np.int64)
    return np.concatenate(levels), np.concatenate(keys)


def tall_walls(walls, flats, levels, free, owners=None):
    """walls [(z0, z1, segments)], one per slice between neighbouring `levels`, flats [(z, region,
    looks up)] -> the walls with the segments that are the same in neighbouring slices joined across
    the heights in `free` wherever no vertex stops them, as [(z0, z1, segments)] (or, with `owners`,
    one array per entry of walls naming whose each segment is: [(z0, z1, segments, owners)]).  Only a
    segment of the same owner joins."""
    at = {z: k for k, z in enumerate(levels)}
    free_k = np.array(sorted(at[z] for z in free if z in at), dtype=np.int64)
    owners = None if owners is None else [o for w, o in zip(walls, owners) if len(w[2])]
    walls = [w for w in walls if len(w[2])]
    if not len(free_k) or not walls:
        return walls if owners is None else [(z0, z1, s, o) for (z0, z1, s), o in zip(walls, owners)]
    k = np.concatenate([np.full(len(s), at[z0]) for z0, _, s in walls])
    seg = np.concatenate([s for *_, s in walls])
    own = np.concatenate(owners) if owners is not None else np.zeros(len(seg), np.int64)
    ka, kb = grid_keys(seg[:, 0]), grid_keys(seg[:, 1])
    fl, fk = flat_points(flats, at)
    points, inverse = np.unique(np.concatenate([ka, kb, fk]), return_inverse=True)
    pa, pb, pf = inverse[:len(ka)], inverse[len(ka):2 * len(ka)], inverse[2 * len(ka):]
    width = len(levels) + 1
    # each distinct (owner, segment) once, its slices in order
    ident = np.unique(np.c_[own, pa, pb], axis=0, return_inverse=True)[1].ravel()
    order = np.lexsort((k, ident))
    kk, idn, a, b = k[order], ident[order], pa[order], pb[order]
    goes_on = np.r_[False, (idn[1:] == idn[:-1]) & (kk[1:] == kk[:-1] + 1)] & np.isin(kk, free_k)
    ends_here = ~np.r_[goes_on[1:], False]           # the next slice does not carry it on
    # the (point, height) pairs that must be vertices: the faces', and the walls' where they start or stop
    seeds = np.concatenate([pf * width + fl,
                            a[~goes_on] * width + kk[~goes_on], b[~goes_on] * width + kk[~goes_on],
                            a[ends_here] * width + kk[ends_here] + 1, b[ends_here] * width + kk[ends_here] + 1])
    na, nb = a[goes_on] * width + kk[goes_on], b[goes_on] * width + kk[goes_on]
    nodes, idx = np.unique(np.concatenate([seeds, na, nb]), return_inverse=True)
    _, label = connected_components(len(nodes), idx[len(seeds):len(seeds) + len(na)], idx[len(seeds) + len(na):])
    stopped = np.zeros(label.max() + 1 if len(label) else 0, dtype=bool)
    stopped[label[idx[:len(seeds)]]] = True
    split = stopped[label[idx[len(seeds):len(seeds) + len(na)]]]
    joins = goes_on.copy()
    joins[np.flatnonzero(goes_on)[split]] = False
    # each run of joined slices one wall: from its first slice's foot to its last slice's top
    start = np.flatnonzero(~joins)
    stop = np.r_[start[1:], len(joins)] - 1
    z0 = kk[start]
    z1 = kk[stop] + 1
    first = order[start]
    out = []
    for lo, hi in sorted(set(zip(z0.tolist(), z1.tolist()))):
        pick = first[(z0 == lo) & (z1 == hi)]
        pick.sort()
        entry = (levels[lo], levels[hi], seg[pick])
        out.append(entry if owners is None else (*entry, own[pick]))
    return out
