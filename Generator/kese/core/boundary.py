"""The boundary of a stack of flat prisms, found in 2D.

Every prism is a flat region between two heights, and the prisms of one part only touch, never
overlap.  So between two neighbouring heights (a slice) the material is one 2D region, the union
of the prisms that span the slice; at a height, the material below minus the material above is a
face that looks up, and the material above minus the material below a face that looks down; and
each ring of a slice's region, stood up between the slice's two heights, is a row of walls with
the material on its left.  Nothing is computed in 3D.

The faces and the walls must meet on identical edges, with no edge ending in the middle of
another (no T-junctions).  GEOS cuts the faces from the slices on the snap grid, and wherever an
edge of one slice passes within half a grid step of a vertex of the other it puts that vertex on
the edge: the faces have it, the slice does not.  So the slices that meet at a height are given
each other's vertices first (kese/core/vertices.py), which bends an edge by up to a grid step;
then the faces are cut, and the slices are given the vertices of their faces as well; where that
changed a slice, its faces are cut again, until nothing changes any more.  Then the boundary
closes by construction, and its volume says so (kese/s8_verify/volumes.py)."""
from dataclasses import dataclass, field
from itertools import pairwise

import numpy as np
import shapely
import shapely.errors

from kese.core import shapes2d as sh
from kese.core.pinches import open_pinches, open_pinches_between
from kese.core.triangulate import rings_of
from kese.core.vertices import noded, share_vertices

HEIGHT_DIGITS = 9                # heights are told apart to 1e-9 mm, a picometre
ROUNDS = 20                      # of cutting the faces and sharing their vertices, see above


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
    for _ in range(ROUNDS):
        flats = flat_faces(slices, levels)
        slices, changed = slices_sharing_vertices(slices, flats, levels, log)
        if not changed:
            break
    else:
        if log:
            log(f"faces and walls still changing after {ROUNDS} rounds")
    return Boundary(part, levels, [(z0, z1, s) for (z0, z1), s in zip(pairwise(levels), slices)], flats)


def heights_of(prisms):
    """Every distinct height of the prisms, low to high."""
    return sorted({round(z, HEIGHT_DIGITS) for p in prisms for z in (p.z0, p.z1)})


def slices_of_part(prisms, levels, log=None, pinches_opened=True):
    """One part's material between every two neighbouring heights, ready for its faces to be cut
    from: the slices sharing each other's vertices (then the faces bring few new ones), and the
    pinch points of every slice opened, unless the part is only looked at (a skin need not be
    manifold, and the gap would show)."""
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


def joined_regions(regions, exact=True):
    """The union of regions that touch but never overlap: GEOS's coverage union, which only drops
    the edges two pieces share, in a fraction of the time a union takes.  Where the pieces' shared
    edges do not match (a vertex of one on an edge of the other, as happens between two parts) the
    coverage union is not a valid region, and a union is taken instead: on the grid when exact (a
    solid's own slices, whose faces must meet on identical edges), else in floating point, three
    times faster (the material of several parts, which only cuts faces and answers questions)."""
    pieces = [piece for r in regions for piece in shapely.get_parts(sh.polys_only(r))]
    try:
        joined = sh.polys_only(shapely.coverage_union_all(pieces))
    except shapely.errors.GEOSException:                       # "cannot process incorrectly noded inputs"
        joined = sh.EMPTY
    if shapely.is_valid(joined) and abs(joined.area - sum(shapely.area(pieces))) <= 1e-9 * joined.area:
        return joined
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
    """The slices, each with every vertex of the faces at its two heights, and of the slice it
    meets there, that lies on one of its edges; a slice that changed is noded again.  For a solid
    (pinches_opened) a gap is cut wherever the two slices at a height meet along an edge, and the
    pinch points of a changed slice are opened again (kese/core/pinches.py).  The heights are gone
    through again as long as a slice changes: a vertex a slice got can lie on an edge of the next
    slice up as well (a via barrel through every layer).
    (slices, the indices of the slices that changed)."""
    slices, changed = list(slices), set()
    while True:
        moved_now = set()
        for k, z in enumerate(levels):
            at = [i for i in (k - 1, k) if 0 <= i < len(slices)]
            if len(at) == 2 and pinches_opened:
                slices[k - 1], slices[k], cut = open_pinches_between(slices[k - 1], slices[k], log)
                if cut:
                    moved_now |= {k - 1, k}
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


def wall_segments(region):
    """Every edge of the region's rings as (a, b), the material on the left: outer rings run
    counter-clockwise, holes clockwise.  An (n, 2, 2) array."""
    polys = np.array([p for p in shapely.get_parts(sh.polys_only(region)) if p.area > 1e-10], dtype=object)
    if not len(polys):
        return np.empty((0, 2, 2))
    xy, nxt, _, _, _ = rings_of(polys)
    return np.stack([xy, xy[nxt]], axis=1)
