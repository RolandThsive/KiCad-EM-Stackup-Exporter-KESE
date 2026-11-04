"""Copies of shapes that keep the grid they are on: sent to and from worker processes
(kese/core/parallel.py), and own() for a thread.

The grid.  shapely's own pickling drops it (get_precision 1e-4 becomes 0.0), and GEOS cuts and grows
a shape on the grid it carries.  A collection made of parts on a grid (as_region, MultiPolygon(...))
is itself on none, so each of its parts keeps its own.  Only multiprocessing's pickling is changed,
for every shape it sends once register() has run (kese/core/parallel.py runs it when imported).

Threads.  GEOS (3.14 and before) counts the shapes made on each of its factories in a plain
integer, and a shape on a grid shares its factory with every shape made from it: the result of an
operation (on the first operand's factory), its parts, the members of a union.  Two threads that
make or drop shapes from one shared shape at once can lose a count, and GEOS then frees the factory
while shapes still use it (a segmentation fault).  A thread therefore works on own() copies of the
shapes other threads may use: each copy is on a factory of its own.  Making it reads the original
(its WKB, which no count records) and the parts of a collection, which shapely hands out as copies
on the original's factories: that is done by one thread at a time (_READING)."""
import threading
from multiprocessing.reduction import ForkingPickler

import numpy as np
import shapely
from shapely.geometry.base import BaseGeometry

_READING = threading.Lock()
RING, COLLECTION = 2, 4  # shapely.get_type_id of a LinearRing, and of a MultiPoint (the collections follow it)


def _shape(rebuild, args, grid):
    """A shape made again on its grid (with its SRID, which set_precision drops).  An empty shape
    keeps its type: pointwise turns POLYGON EMPTY into a ring."""
    shape = rebuild(*args)
    if not grid:
        return shape
    srid = shapely.get_srid(shape)
    shape = shapely.set_precision(shape, grid, mode="keep_collapsed" if shape.is_empty else "pointwise")
    return shapely.set_srid(shape, srid) if srid else shape


def _whole(shape):
    """("whole", rebuild, args, grid): shapely's own pickling (WKB with the SRID, a ring rebuilt as a
    ring), and the grid.  Only reads the shape."""
    return ("whole", *shape.__reduce__(), float(shapely.get_precision(shape)))


def _by_parts(shape):
    """("parts", type, the plan of each part, SRID) for a collection on no grid with a part on one
    (at any depth), else None.  Reads the parts, which are copies on the original's factories: under
    _READING, and let go on return (a plan holds no shape)."""
    if shapely.get_precision(shape) or shapely.get_type_id(shape) < COLLECTION or shape.is_empty:
        return None
    parts = shapely.get_parts(shape)
    if not (shapely.get_precision(parts).any() or (shapely.get_type_id(parts) >= COLLECTION).any()):
        return None
    plans = [_by_parts(p) or _whole(p) for p in parts]
    if all(p[0] == "whole" and not p[3] for p in plans):
        return None
    return "parts", type(shape), plans, int(shapely.get_srid(shape))


def _made(plan):
    """The shape a plan describes."""
    if plan[0] == "whole":
        return _shape(*plan[1:])
    _, kind, parts, srid = plan
    shape = kind([_made(p) for p in parts])      # on no grid, its parts each on theirs
    return shapely.set_srid(shape, srid) if srid else shape


def _send_shape(shape):
    with _READING:
        plan = _by_parts(shape)
    return _made, (plan or _whole(shape),)


def register():
    """From now on, multiprocessing sends every shape with its grid."""
    for kind in (shapely.Point, shapely.LineString, shapely.LinearRing, shapely.Polygon, shapely.MultiPoint,
                 shapely.MultiLineString, shapely.MultiPolygon, shapely.GeometryCollection):
        ForkingPickler.register(kind, _send_shape)


def own(x):
    """x with every shape in it copied for this thread (see above): a shape, or a list, tuple or dict
    of them (nested), or a numpy array of shapes; anything else is kept as it is."""
    if isinstance(x, BaseGeometry):
        return _copies([x])[0]
    if isinstance(x, np.ndarray) and x.dtype == object:
        out = np.empty(x.shape, dtype=object)
        out.flat[:] = own(list(x.flat))
        return out
    if isinstance(x, (list, tuple)):
        if x and all(isinstance(v, BaseGeometry) for v in x):
            return type(x)(_copies(list(x)))
        return type(x)(own(v) for v in x)
    if isinstance(x, dict):
        return {k: own(v) for k, v in x.items()}
    return x


def _copies(shapes):
    """Copies of a list of shapes, those whole (not rings, nor collections with parts on a grid of
    their own) in one go: as _shape() makes each, a quarter of the time for many small ones."""
    every = np.empty(len(shapes), dtype=object)
    every[:] = shapes
    grid, kind = shapely.get_precision(every), shapely.get_type_id(every)
    whole = (kind != RING) & ((grid > 0) | (kind < COLLECTION))
    out = np.empty(len(shapes), dtype=object)
    for k in np.flatnonzero(~whole):
        rebuild, (plan,) = _send_shape(shapes[k])
        out[k] = rebuild(plan)
    if whole.any():
        made = shapely.from_wkb(shapely.to_wkb(every[whole], include_srid=True))
        on, srid, empty = grid[whole], shapely.get_srid(made), shapely.is_empty(made)
        for mode, which in (("pointwise", (on > 0) & ~empty), ("keep_collapsed", (on > 0) & empty)):
            if which.any():
                made[which] = shapely.set_precision(made[which], on[which], mode=mode)
        again = (on > 0) & (srid != 0)              # set_precision drops the SRID
        made[again] = shapely.set_srid(made[again], srid[again])
        out[whole] = made
    return list(out)
