"""The boundary of a stack of flat prisms, found in 2D: per slice the material as one region, at
every height the faces looking up and down, and the walls of every ring.  Slices and faces share
their vertices (kese/core/vertices.py) until nothing changes, so the boundary closes."""
from dataclasses import dataclass, field
from itertools import pairwise

import numpy as np
import shapely
import shapely.errors

from kese.core import shapes2d as sh
from kese.core.pinches import open_pinches, open_pinches_between
from kese.core.shape_copies import floating, own
from kese.core.triangulate import rings_of
from kese.core.vertices import noded, share_vertices

HEIGHT_DIGITS = 9                # heights are told apart to 1e-9 mm, a picometre


@dataclass
class Boundary:
    """The faces of one part, in mm and board coordinates."""
    part: str
    levels: list = field(default_factory=list)   # every distinct height, low to high
    slices: list = field(default_factory=list)   # (z0, z1, region): the material between two neighbouring heights
    flats: list = field(default_factory=list)    # (z, region, looks up): a flat face with its holes

    def walls(self):
        """(z0, z1, segments) per slice: every ring edge of the slice as (a, b) with the material
        on its left, stood up between the slice's heights.  An (n, 2, 2) array of segments."""
        return [(z0, z1, wall_segments(region)) for z0, z1, region in self.slices if not region.is_empty]

    def volume(self):
        """The volume between the faces, from the flat faces alone: for a closed surface the
        volume is the sum of height times signed area over its faces, and walls are vertical."""
        return sum((1 if up else -1) * z * region.area for z, region, up in self.flats)

    def volume_of_slices(self):
        """The volume of the material, slice by slice: what volume() must come to."""
        return sum((z1 - z0) * region.area for z0, z1, region in self.slices)


def boundary_of(part, prisms, log=None):
    """The prisms of one part -> its Boundary, closed by construction."""
    levels = heights_of(prisms)
    slices = slices_of_part(prisms, levels, log)
    for _ in range(sh.G().VERTEX_SHARING_ROUNDS):
        flats = flat_faces(slices, levels)
        slices, changed = slices_sharing_vertices(slices, flats, levels, log)
        if not changed:
            break
    else:
        if log:
            log(f"faces and walls still changing after {sh.G().VERTEX_SHARING_ROUNDS} rounds")
    return Boundary(part, levels, [(z0, z1, s) for (z0, z1), s in zip(pairwise(levels), slices)], flats)


def heights_of(prisms):
    """Every distinct height of the prisms, low to high."""
    return sorted({round(z, HEIGHT_DIGITS) for p in prisms for z in (p.z0, p.z1)})


def slices_of_part(prisms, levels, log=None, pinches_opened=True):
    """One part's material between every two neighbouring heights, sharing each other's vertices,
    with the pinch points of every slice opened unless the part is only looked at (a skin)."""
    slices = slices_of(prisms, levels)
    if pinches_opened:
        slices = [open_pinches(s, log) for s in slices]
    return slices_sharing_vertices(slices, [], levels, log, pinches_opened)[0]


def slices_of(prisms, levels):
    """The material between each pair of neighbouring heights: the union of the prisms that span
    the slice, noded on the grid."""
    out = []
    for z0, z1 in pairwise(levels):
        spanning = [p.region for p in prisms if round(p.z0, HEIGHT_DIGITS) <= z0 and round(p.z1, HEIGHT_DIGITS) >= z1]
        region = spanning[0] if len(spanning) == 1 else joined_regions(spanning)
        out.append(noded(region) if spanning else sh.EMPTY)
    return out


def joined_regions(regions, exact=True, shared=False):
    """The union of regions that touch but never overlap: GEOS's coverage union, or, where the shared
    edges do not match, a union (on the grid when exact, else in floating point).  shared: regions
    other threads use too, so made of copies (kese/core/shape_copies.py): floating() ones for the
    coverage union, which uses no grid, and own() ones, each part on its grid, for a union."""
    readable = floating(regions) if shared else regions
    pieces = [piece for r in readable for piece in shapely.get_parts(sh.polys_only(r))]
    try:
        joined = sh.polys_only(shapely.coverage_union_all(pieces))
    except shapely.errors.GEOSException:                       # "cannot process incorrectly noded inputs"
        joined = sh.EMPTY
    if shapely.is_valid(joined) and abs(joined.area - sum(shapely.area(pieces))) <= 1e-9 * joined.area:
        return joined
    regions = own(regions) if shared else regions
    return shapely.union_all(regions, grid_size=sh.grid()) if exact else sh.polys_only(shapely.union_all(regions))


def flat_faces(slices, levels):
    """At every height, what looks up (the material below minus the material above) and what
    looks down: [(z, region, looks up)]."""
    out = []
    for k, z in enumerate(levels):
        below = slices[k - 1] if k else sh.EMPTY
        above = slices[k] if k < len(slices) else sh.EMPTY
        for region, up in ((sh.diff(below, above), True), (sh.diff(above, below), False)):
            if not region.is_empty:
                out.append((z, region, up))
    return out


def slices_sharing_vertices(slices, flats, levels, log, pinches_opened=True):
    """The slices, each with the vertices of the faces and the slice it meets that lie on its edges,
    repeated until no slice changes (at most Geometry.VERTEX_SHARING_ROUNDS times; a height cut again is
    cut wider).
    -> (slices, the indices of the slices that changed)."""
    slices, changed, cuts = list(slices), set(), [0] * len(levels)
    for _ in range(sh.G().VERTEX_SHARING_ROUNDS):
        moved_now = set()
        for k, z in enumerate(levels):
            at = [i for i in (k - 1, k) if 0 <= i < len(slices)]
            if len(at) == 2 and pinches_opened:
                slices[k - 1], slices[k], cut = open_pinches_between(slices[k - 1], slices[k], log, cuts[k])
                if cut:
                    moved_now |= {k - 1, k}
                    cuts[k] += 1
            new, moved = share_vertices([slices[i] for i in at], [region for height, region, _ in flats if height == z])
            for j, i in enumerate(at):
                slices[i] = new[j]
                if j in moved:
                    moved_now.add(i)
        for i in moved_now:
            slices[i] = open_pinches(noded(slices[i]), log) if pinches_opened else noded(slices[i])
        changed |= moved_now
        if not moved_now:
            return slices, changed
    if log:
        log(f"slices still sharing new vertices after {sh.G().VERTEX_SHARING_ROUNDS} rounds")
    return slices, changed


def wall_segments(region):
    """Every edge of the region's rings as (a, b), the material on the left: outer rings run
    counter-clockwise, holes clockwise.  An (n, 2, 2) array."""
    polys = np.array([p for p in shapely.get_parts(sh.polys_only(region)) if p.area > sh.G().SLIVER_AREA_MM2], dtype=object)
    if not len(polys):
        return np.empty((0, 2, 2))
    xy, nxt, _, _, _ = rings_of(polys)
    return np.stack([xy, xy[nxt]], axis=1)
