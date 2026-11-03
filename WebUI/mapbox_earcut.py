"""
mapbox_earcut.py - the one call KESE makes to the mapbox_earcut package, answered by earcut.js in the browser.

mapbox_earcut (the C++ earcut.hpp) has no Pyodide build.  earcut.js is the same algorithm by the same authors;
PyodideWorker.js loads it and puts it on the worker's global scope as `earcut`.  Only the function KESE uses
(kese/core/triangulate.py) is here.
"""
import numpy as np
from js import Float64Array, earcut                 # noqa: F401  (the worker's globals)
from pyodide.ffi import to_js


def triangulate_float64(vertices, ring_end_indices):
    """vertices (N, 2) float64, ring_end_indices: where each ring ends (the outer ring first, then the holes).
    Returns the triangles as a flat uint32 array of vertex indices, as mapbox_earcut does."""
    xy = np.ascontiguousarray(vertices, dtype=np.float64).reshape(-1)
    ends = [int(e) for e in np.asarray(ring_end_indices).reshape(-1)]
    holes = to_js(ends[:-1]) if len(ends) > 1 else None
    data = Float64Array.new(to_js(memoryview(xy)))
    tri = earcut(data, holes, 2)
    return np.asarray(tri.to_py(), dtype=np.uint32)
