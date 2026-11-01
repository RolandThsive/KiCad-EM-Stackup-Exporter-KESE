"""Connected components of an undirected graph, in numpy.  Every component is numbered in the
order of its smallest node, as scipy and trimesh number them."""
import numpy as np


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
