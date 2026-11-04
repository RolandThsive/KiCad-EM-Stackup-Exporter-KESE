"""A part's flat faces, found in 2D (kese/core/boundary.py): at every height, the material of the
slice below less that of the slice above looks up, and the other way round looks down.  Only what
differs is cut: the pieces both slices have are left out, and the rest is cut group by group."""
import numpy as np
import shapely

from kese.core import shapes2d as sh


def flat_faces(slices, levels, before=(), heights=None):
    """At every height, what looks up (the material below minus the material above) and what
    looks down: [(z, region, looks up)].  Only at the indices `heights` (every height when None);
    at the others the faces of `before`, those faces before the slices next to them changed."""
    kept = {}
    for face in before:
        kept.setdefault(face[0], []).append(face)
    out = []
    for k, z in enumerate(levels):
        if heights is not None and k not in heights:
            out += kept.get(z, [])
            continue
        up, down = faces_between(slices[k - 1] if k else sh.EMPTY, slices[k] if k < len(slices) else sh.EMPTY)
        out += [(z, region, looks_up) for region, looks_up in ((up, True), (down, False)) if not region.is_empty]
    return out


def faces_between(below, above):
    """(what looks up, what looks down) where the slice below meets the slice above: below minus
    above and above minus below.  A piece both have, ring for ring, faces nothing there and is
    left out first (a part's slices are often the same on both sides of a height another of its
    prisms ends at: the hole finish of every plated hole, between its layers).  The rest is cut
    group by group (shapes2d.meeting: pieces within a grid step of each other, the most a cut on
    the grid reaches), and a piece with nothing of the other side in its group is a face as it
    is: the slices are noded, so on the grid it would come out the same."""
    below, above = sh.polys_only(below), sh.polys_only(above)
    if not below.is_empty and not above.is_empty:
        below, above = without_common_pieces(below, above)
    if below.is_empty or above.is_empty:
        return below, above
    pa, pb = list(shapely.get_parts(below)), list(shapely.get_parts(above))
    if len(pa) == 1 and len(pb) == 1:
        return sh.diff(below, above), sh.diff(above, below)
    pieces, up, down = pa + pb, [], []
    for group in sh.meeting(np.array(pieces, dtype=object)):
        a = [pieces[i] for i in group if i < len(pa)]
        b = [pieces[i] for i in group if i >= len(pa)]
        if not b or not a:
            up, down = up + a, down + b
            continue
        ga, gb = sh.as_region(a), sh.as_region(b)
        up += list(shapely.get_parts(sh.diff(ga, gb)))
        down += list(shapely.get_parts(sh.diff(gb, ga)))
    return sh.as_region(up), sh.as_region(down)


def without_common_pieces(a, b):
    """Two regions, each without the pieces the other has too (the same rings, from whatever point
    and in whichever direction each ring runs)."""
    pa, pb = shapely.get_parts(a), shapely.get_parts(b)
    ka, kb = (shapely.to_wkb(shapely.normalize(p)).tolist() for p in (pa, pb))
    common = set(ka).intersection(kb)
    if not common:
        return a, b
    return tuple(sh.as_region([q for q, key in zip(p, k) if key not in common]) for p, k in ((pa, ka), (pb, kb)))
