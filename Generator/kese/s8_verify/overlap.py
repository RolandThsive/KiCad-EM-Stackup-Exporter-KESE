"""The overlap check of stage 8 in simulation mode: every slice of a part against every slice of
another that overlaps it in height, each polygon shrunk by a grid step (parts that only touch do
not meet), the candidates found by an R-tree.  The slices are split into polygons, and the polygons
shrunk and tested, Parallel.WORKERS at a time, in threads, each on its own copies of the shapes it
uses (kese/core/shape_copies.py): GEOS does that work outside Python's lock."""
import numpy as np
import shapely

from kese.core.parallel import in_parallel, workers_wanted
from kese.core.pinches import polygons
from kese.core.shape_copies import own
from parameters import P


def overlaps(model):
    """[(volume mm3, part, other part, z0, z1)] of every two slices of different parts that share
    material, the biggest first."""
    rows = [(part, z0, z1, region) for part, b in model.boundaries.items() for z0, z1, region in b.slices]
    owner, polys = [], []
    for k, found in enumerate(in_parallel(lambda row: polygons(own(row[3])), rows)):
        owner += [k] * len(found)
        polys += found
    if not polys:
        return []
    owner, polys = np.array(owner), np.array(polys, dtype=object)
    i, j = shapely.STRtree(polys).query(polys)                      # boxes that meet
    part = np.unique([r[0] for r in rows], return_inverse=True)[1]
    z0, z1 = np.array([r[1] for r in rows]), np.array([r[2] for r in rows])
    dz = np.minimum(z1[owner[i]], z1[owner[j]]) - np.maximum(z0[owner[i]], z0[owner[j]])
    keep = (i < j) & (part[owner[i]] != part[owner[j]]) & (dz > 10.0 ** -P.Geometry.HEIGHT_DIGITS)
    i, j, dz = i[keep], j[keep], dz[keep]
    size = shapely.get_num_coordinates(polys)
    first = size[i] >= size[j]
    i, j = np.where(first, i, j), np.where(first, j, i)            # the one with more vertices first
    meet = meeting(polys, i, j, size)
    found = [(polys[p].intersection(polys[q]).area * h, rows[owner[p]][0], rows[owner[q]][0],
              max(z0[owner[p]], z0[owner[q]]), min(z1[owner[p]], z1[owner[q]]))
             for p, q, h in zip(i[meet], j[meet], dz[meet])]
    return sorted(found, key=lambda f: (-f[0], *f[1:]))


def meeting(polys, i, j, size):
    """For each candidate pair (polys[i], polys[j]): whether the two, each shrunk by a grid step,
    still meet.  The polygons are shrunk in groups of about the same number of vertices; the pairs
    are tested in groups that each hold every pair of some first polygons, which the group prepares
    (an index of their edges, made once for all their pairs)."""
    if not len(i):
        return np.zeros(0, dtype=bool)
    used = np.unique(np.r_[i, j])
    shrunk = np.empty(len(polys), dtype=object)
    groups = dealt(used, size[used], len(used))
    for group, done in zip(groups, in_parallel(lambda g: shrink(polys[g]), groups)):
        shrunk[group] = done
    firsts = np.unique(i)
    groups = [np.flatnonzero(np.isin(i, g)) for g in dealt(firsts, size[firsts], len(used))]
    meet = np.zeros(len(i), dtype=bool)
    for rows, done in zip(groups, in_parallel(lambda r: met(shrunk, i[r], j[r]), groups)):
        meet[rows] = done
    return meet


def dealt(items, weight, polygons_in_all):
    """items in groups, dealt in turn from the heaviest: one group where there are fewer than
    2 * Parallel.VERIFY_POLYGONS_PER_THREAD polygons in all, else up to Parallel.VERIFY_GROUPS_PER_WORKER
    for each worker (a slow group is then made up for by the others), each of
    VERIFY_POLYGONS_PER_THREAD polygons or more."""
    least, groups = P.Parallel.VERIFY_POLYGONS_PER_THREAD, P.Parallel.VERIFY_GROUPS_PER_WORKER
    n = max(1, min(groups * workers_wanted(), polygons_in_all // least))
    if n == 1 or len(items) < 2:
        return [items]
    order = items[np.argsort(-weight, kind="stable")]
    return [np.sort(order[k::n]) for k in range(min(n, len(items)))]


def shrink(polys):
    """The polygons each shrunk by a grid step (mitred), made from this thread's own copies."""
    return shapely.buffer(own(polys), -P.Geometry.SNAP_GRID_MM, join_style="mitre")


def met(shrunk, i, j):
    """Whether shrunk[i[k]] meets shrunk[j[k]], for each k, on this thread's own copies, those of
    the first polygons prepared."""
    firsts, a = np.unique(i, return_inverse=True)
    seconds, b = np.unique(j, return_inverse=True)
    first, second = own(shrunk[firsts]), own(shrunk[seconds])
    shapely.prepare(first)
    return shapely.intersects(first[a], second[b])
