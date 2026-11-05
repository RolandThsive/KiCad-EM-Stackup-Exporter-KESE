"""Graphs of shapes: which shapes lie within a distance of each other (pairs_within), and the
connected components of an undirected graph, in numpy.  Every component is numbered in the order of
its smallest node, as scipy and trimesh number them."""
import numpy as np
import shapely


def connected_components(n, a, b):
    """(number of components, component of every node 0 .. n-1) of the graph with the edges a[i]-b[i]."""
    parent = np.arange(n)
    a, b = np.asarray(a, dtype=np.int64).ravel(), np.asarray(b, dtype=np.int64).ravel()
    while len(a):
        ra, rb = parent[a], parent[b]
        cross = ra != rb
        if not cross.any():
            break
        lo, hi = np.minimum(ra[cross], rb[cross]), np.maximum(ra[cross], rb[cross])
        np.minimum.at(parent, hi, lo)
        while True:
            up = parent[parent]
            if np.array_equal(up, parent):
                break
            parent = up
        a, b = a[cross], b[cross]            # an edge inside one component stays inside it
    roots, label = np.unique(parent, return_inverse=True)
    return len(roots), label


def pairs_within(parts, d):
    """(i, j), i < j: the pairs of parts within d of each other, the pairs an STRtree's dwithin query
    of the parts against themselves finds, but each pair measured once, from the part with more
    points (prepared, its edges indexed).  The query measures from both sides, and from a small pad's
    side every edge of a zone fill around it is walked: on a board of thousands of pads 2 s a layer,
    against 0.1 s.  Candidates are the parts whose boxes come within d; parts prepared here are let
    go after (a prepared part serves one thread at a time, and holds memory)."""
    parts = np.asarray(parts, dtype=object)
    box = shapely.bounds(parts)
    i, j = shapely.STRtree(parts).query(shapely.box(box[:, 0] - d, box[:, 1] - d, box[:, 2] + d, box[:, 3] + d))
    i, j = i[i < j], j[i < j]
    n = shapely.get_num_coordinates(parts)
    first = n[i] >= n[j]
    big, small = np.where(first, i, j), np.where(first, j, i)
    fresh = np.unique(big)
    fresh = fresh[~shapely.is_prepared(parts[fresh])]
    shapely.prepare(parts[fresh])
    try:
        near = shapely.dwithin(parts[big], parts[small], d)
    finally:
        shapely.destroy_prepared(parts[fresh])
    return i[near], j[near]
