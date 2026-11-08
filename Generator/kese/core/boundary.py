"""The boundary of a stack of flat prisms, found in 2D: per slice the material as one region, at
every height the faces looking up and down, and the walls of every ring.  Slices and faces share
their vertices (kese/core/vertices.py) until nothing changes, so the boundary closes."""
from dataclasses import dataclass, field
from itertools import pairwise

import numpy as np
import shapely
import shapely.errors

from kese.core import shapes2d as sh
from kese.core.flat_faces import flat_faces
from kese.core.pinches import cut_open_at, open_pinches, open_pinches_between
from kese.core.shape_copies import floating, own
from kese.core.tall_walls import tall_walls
from kese.core.triangulate import oriented_rings
from kese.core.vertices import grid_keys, noded, ring_points, share_vertices


@dataclass
class Boundary:
    """The faces of one part, in mm and board coordinates."""
    part: str
    levels: list = field(default_factory=list)   # every distinct height, low to high
    slices: list = field(default_factory=list)   # (z0, z1, region): the material between two neighbouring heights
    flats: list = field(default_factory=list)    # (z, region, looks up): a flat face with its holes
    free: frozenset = frozenset()                # heights the walls may run on across (PrismSet.free_levels)
    _walls: list = field(default=None, repr=False)

    def walls(self):
        """(z0, z1, segments): every ring edge of every slice as (a, b) with the material on its left,
        stood up between the slice's heights, an (n, 2, 2) array of segments; across the heights in
        `free`, the segments that go on unchanged as one taller wall (kese/core/tall_walls.py)."""
        if self._walls is None:
            walls = [(z0, z1, wall_segments(region)) for z0, z1, region in self.slices if not region.is_empty]
            self._walls = tall_walls(walls, self.flats, self.levels, self.free) if self.free else walls
        return self._walls

    def volume(self):
        """The volume between the faces, from the flat faces alone: for a closed surface the
        volume is the sum of height times signed area over its faces, and walls are vertical."""
        return sum((1 if up else -1) * z * region.area for z, region, up in self.flats)

    def volume_of_slices(self):
        """The volume of the material, slice by slice: what volume() must come to."""
        return sum((z1 - z0) * region.area for z0, z1, region in self.slices)


def boundary_of(part, prisms, log=None, free=frozenset()):
    """The prisms of one part -> its Boundary, closed by construction; `free`: heights its walls may
    run on across (PrismSet.free_levels)."""
    levels = heights_of(prisms)
    slices = slices_of_part(prisms, levels, log)
    flats, again = [], range(len(levels))
    for _ in range(sh.G().VERTEX_SHARING_ROUNDS):
        flats = flat_faces(slices, levels, flats, again)
        slices, changed = slices_sharing_vertices(slices, flats, levels, log)
        if not changed:
            break
        again = {k for i in changed for k in (i, i + 1)}      # the heights at a changed slice's ends
    else:
        if log:
            log(f"faces and walls still changing after {sh.G().VERTEX_SHARING_ROUNDS} rounds")
    return Boundary(part, levels, [(z0, z1, s) for (z0, z1), s in zip(pairwise(levels), slices)], flats,
                    frozenset(free) & frozenset(levels))


def heights_of(prisms):
    """Every distinct height of the prisms, low to high."""
    return sorted({round(z, sh.G().HEIGHT_DIGITS) for p in prisms for z in (p.z0, p.z1)})


def slices_of_part(prisms, levels, log=None, pinches_opened=True):
    """One part's material between every two neighbouring heights, sharing each other's vertices,
    with the pinch points of every slice opened unless the part is only looked at (a skin)."""
    slices = slices_of(prisms, levels)
    if pinches_opened:
        slices = [open_pinches(s, log) for s in slices]
    return slices_sharing_vertices(slices, [], levels, log, pinches_opened)[0]


def slices_of(prisms, levels):
    """The material between each pair of neighbouring heights: the union of the prisms that span
    the slice, noded on the grid.  Slices spanned by the same regions (the same shapes, in the same
    order: a hole's finish in three prisms, one per stretch of the wall) are made once."""
    out, made = [], {}
    shapes = shapely.to_wkb([p.region for p in prisms]).tolist() if prisms else []
    for z0, z1 in pairwise(levels):
        spanning = spanning_prisms(prisms, z0, z1)
        if not spanning:
            out.append(sh.EMPTY)
            continue
        key = tuple(shapes[i] for i in spanning)
        if key not in made:
            regions = [prisms[i].region for i in spanning]
            made[key] = noded(regions[0] if len(regions) == 1 else joined_regions(regions))
        out.append(made[key])
    return out


def spanning_prisms(prisms, z0, z1):
    """The indices of the prisms that span the slice from z0 to z1 (heights of heights_of)."""
    d = sh.G().HEIGHT_DIGITS
    return [i for i, p in enumerate(prisms) if round(p.z0, d) <= z0 and round(p.z1, d) >= z1]


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


def slices_sharing_vertices(slices, flats, levels, log, pinches_opened=True):
    """The slices, each with the vertices of the faces and the slice it meets that lie on its edges,
    repeated until no slice changes (at most Geometry.VERTEX_SHARING_ROUNDS times; a height cut again is
    cut wider).  A round goes through the heights upwards, the next downwards: a vertex goes on through
    every slice in the way a round goes, but only one slice the other way (fifty heights of a part,
    each with the vertex where a backdrill meets the plated edge, took fifty rounds upwards only).
    Needle tips of two slices a grid step or two apart can trade vertices round after round for ever:
    slices still changing then are cut open at the points each further round adds
    (pinches.cut_open_at), the disc doubling, for at most Geometry.PINCH_CUT_ROUNDS more rounds.
    -> (slices, the indices of the slices that changed)."""
    slices, changed, cuts = list(slices), set(), [0] * len(levels)
    rounds, opened, widest = sh.G().VERTEX_SHARING_ROUNDS, 0, 0.0   # points cut open, the widest disc
    for round_ in range(rounds + sh.G().PINCH_CUT_ROUNDS):
        moved_now, added = set(), []
        late = round_ >= rounds
        for k in range(len(levels)) if round_ % 2 == 0 else reversed(range(len(levels))):
            z, at = levels[k], [i for i in (k - 1, k) if 0 <= i < len(slices)]
            if len(at) == 2 and pinches_opened:
                slices[k - 1], slices[k], cut = open_pinches_between(slices[k - 1], slices[k], log, cuts[k])
                if cut:
                    moved_now |= {k - 1, k}
                    cuts[k] += 1
            new, moved = share_vertices([slices[i] for i in at], [region for height, region, _ in flats if height == z])
            for j, i in enumerate(at):
                if late and j in moved:
                    added.append(points_added(slices[i], new[j]))
                slices[i] = new[j]
                if j in moved:
                    moved_now.add(i)
        if added:
            pts = np.concatenate(added)
            pts = pts[np.unique(grid_keys(pts), return_index=True)[1]]       # one per grid point
            cut, r = cut_open_at(slices, pts, round_ - rounds)
            moved_now |= cut
            opened, widest = opened + len(pts), max(widest, r)
        for i in moved_now:
            slices[i] = open_pinches(noded(slices[i]), log) if pinches_opened else noded(slices[i])
        changed |= moved_now
        if not moved_now:
            break
    else:
        if log:
            log(f"slices still sharing new vertices after {rounds} rounds")
    if opened and log:
        log(f"slices still sharing new vertices after {rounds} rounds: cut open at {opened} points, "
            f"by discs of up to {widest:.6g} mm radius")
    return slices, changed


def points_added(old, new):
    """The vertices of `new` at grid points where `old` has none."""
    a, b = ring_points(old), ring_points(new)
    return b[~np.isin(grid_keys(b), grid_keys(a))]


def wall_segments(region):
    """Every edge of the region's rings as (a, b), the material on the left: outer rings run
    counter-clockwise, holes clockwise.  An (n, 2, 2) array."""
    parts = shapely.get_parts(sh.polys_only(region))
    polys = parts[shapely.area(parts) > sh.G().SLIVER_AREA_MM2]
    if not len(polys):
        return np.empty((0, 2, 2))
    xy, nxt = oriented_rings(polys)[:2]
    return np.stack([xy, xy[nxt]], axis=1)
