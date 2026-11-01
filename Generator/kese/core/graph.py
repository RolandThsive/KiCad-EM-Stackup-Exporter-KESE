"""Connected components of an undirected graph, in numpy: what scipy's csgraph gave KESE, without
scipy.  Every edge hooks the larger of its two roots under the smaller, then the pointers jump until
each node points at its root, again until no edge joins two roots.  So every component's root is
its smallest node, and the components are numbered in the order of their smallest nodes, as scipy
and trimesh number them."""
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
