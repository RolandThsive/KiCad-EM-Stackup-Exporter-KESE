"""The "visual" mode without a kernel: the board's visible surface, found in 2D as the boundary of
a part is (kese/core/boundary.py), but for all parts at once.  At every height, what looks up is
one part's material below minus every part's material above, and what looks down one part's
material above minus every part's material below; a wall of a part is visible where no other
part's material stands against it.  Every face keeps the part it came from.  Faces and walls meet
on identical edges, as for a solid, but nothing is bent to that end and nothing is cut twice: a
wall is split wherever a vertex of a face at its heights, or of a neighbouring part's wall, lies on
it (kese/core/vertices.py).  What looks at other material across less than a hair, and the
surfaces of hollows sealed inside the board, are taken out afterwards, triangle by triangle
(kese/s6_assemble/skin_mesh.py)."""
from concurrent.futures import ThreadPoolExecutor
from itertools import pairwise
from threading import get_ident

import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.boundary import heights_of, joined_regions, slices_of_part, wall_segments
from kese.core.vertices import (
    grid_keys,
    pairs_in,
    same_vertices,
    walls_split_at_vertices,
)
from kese.s6_assemble.boundaries import workers_wanted

FEW_PIECES = 200         # of material reaching a face: up to this many are cut away piece by piece (cut_away)
BIG_PIECE = 10_000       # coordinates: a piece this big (a dielectric, with every via hole in it) is cut away on its own


def skin_faces(ps, log):
    """PrismSet -> (levels, the material of every slice (material_of_every_slice), {part: (flats,
    walls)}): the visible faces of every part, mm, board frame; flats as (z, region, looks up),
    walls as (z0, z1, segments).  The parts are cut, and the slices' walls found, Run.WORKERS at
    a time."""
    levels = heights_of(ps.prisms)
    by_part = {part: [p for p in prisms if not p.region.is_empty] for part, prisms in ps.by_part().items()}
    order = biggest_first(by_part)
    with ThreadPoolExecutor(workers_wanted()) as pool:
        slices = dict(zip(order, pool.map(lambda part: slices_of_part(by_part[part], levels, log, pinches_opened=False), order)))
        pieces = material_of_every_slice(slices, pool)
        flats = dict(zip(order, pool.map(lambda part: visible_flats(slices[part], levels, pieces), order)))
        for *_, copies in pieces:
            copies.clear()                   # the threads' prepared copies: gigabytes on a dense board
        walls = visible_walls(slices, levels, flats, pool)
    return levels, pieces, {part: (flats[part], walls[part]) for part in by_part}


def biggest_first(by_part):
    """The parts, the one with the most coordinates first: the dielectrics and the masks take the
    longest to slice and to cut, and started first no thread is left alone with one at the end."""
    return sorted(by_part, key=lambda part: -sum(shapely.get_num_coordinates(p.region) for p in by_part[part]))


def material_of_every_slice(slices, pool):
    """Per slice: (every part's polygons in it, the part of each, an index of the polygons, all of
    them joined as one region, and a place for each thread's prepared copy of that region, see
    lies_against_material()), for lookups by place and for cutting the faces."""
    gathered = []
    for k in range(len(next(iter(slices.values()), []))):
        polys, parts = [], []
        for part, s in slices.items():
            for p in shapely.get_parts(s[k]):
                polys.append(p)
                parts.append(part)
        polys = np.array(polys, dtype=object)
        gathered.append((polys, np.array(parts, dtype=object), shapely.STRtree(polys)))
    joined = pool.map(lambda polys_parts_tree: joined_regions(list(polys_parts_tree[0]), exact=False), gathered)
    return [(*material, region, {}) for material, region in zip(gathered, joined)]


def visible_flats(part_slices, levels, pieces):
    """One part's flat faces: at every height, its material below minus everyone's material
    above (looking up), and its material above minus everyone's material below (looking down).
    Where the part's material is the same below and above a height, there is no face there (a
    via barrel through every layer)."""
    out = []
    for k, z in enumerate(levels):
        below = part_slices[k - 1] if k else sh.EMPTY
        above = part_slices[k] if k < len(part_slices) else sh.EMPTY
        if same_vertices(below, above):
            continue
        for mine, cutter, up in ((below, k, True), (above, k - 1, False)):
            if mine.is_empty:
                continue
            region = cut_away(mine, pieces[cutter]) if 0 <= cutter < len(pieces) else mine
            if not region.is_empty:
                out.append((z, region, up))
    return out


def cut_away(region, material):
    """The region less the material of a slice (its polygons, their parts, an index of them, all
    of them joined, and each thread's prepared copy of that).  What reaches into the region is cut
    away: a few small pieces joined; a big piece on its own (GEOS keeps only what reaches into the
    region's box); and more pieces than that as all the slice's material in one overlay, which
    costs less than joining them.  Where a big piece or many reach it, the region is first asked
    whether it lies wholly against material, as most faces of a board do (a trace's underside on
    the dielectric, its top under the solder mask), and is gone if so."""
    polys, _, tree, joined, _ = material
    near = tree.query(region)                                  # by box; the exact test below costs a tenth of the
    near = near[shapely.intersects(polys[near], region)]       # index's own, which would try every ring of a big piece
    if not len(near):
        return region
    cutters = polys[near]
    big = shapely.get_num_coordinates(cutters) > BIG_PIECE
    if (big.any() or len(near) > FEW_PIECES) and lies_against_material(region, material):
        return sh.EMPTY
    if len(near) > FEW_PIECES:
        return sh.diff(region, joined)
    for piece in cutters[big]:
        region = sh.diff(region, piece)
    return sh.diff(region, joined_regions(list(cutters[~big]), exact=False)) if (~big).any() else region


def lies_against_material(region, material):
    """Whether the slice's material covers the region wholly.  GEOS answers in a fraction of the
    time an overlay takes once the material is prepared (indexed), but a prepared geometry keeps
    working state that two threads cannot share: so every thread asks a copy of its own, made the
    first time it asks about this slice."""
    *_, joined, copies = material
    mine = copies.get(get_ident())
    if mine is None:
        mine = copies[get_ident()] = shapely.from_wkb(shapely.to_wkb(joined))
        shapely.prepare(mine)
    return shapely.covers(mine, region)


def visible_walls(slices, levels, flats, pool):
    """Every part's walls per slice, split where a face at the slice's heights or another part's
    wall has a vertex on them, less those another part's material stands against: a wall segment
    a -> b (the material on its left) is hidden when some part has b -> a.  (No part has a segment
    both ways itself: the pieces of one region never share an edge.)  -> {part: [(z0, z1, segments)]}."""
    faces_at = {}
    for part_flats in flats.values():
        for z, region, _ in part_flats:
            faces_at.setdefault(z, []).append(region)
    out = {part: [] for part in slices}
    for (z0, z1), segments in zip(pairwise(levels), pool.map(lambda k: walls_of_slice(slices, k, faces_at.get(levels[k], []) + faces_at.get(levels[k + 1], [])),
                                                              range(len(levels) - 1))):
        if not segments:
            continue
        every = np.concatenate(list(segments.values()))
        start, end = grid_keys(every[:, 0]), grid_keys(every[:, 1])
        hidden = pairs_in(end, start, start, end)                       # b -> a among the a -> b
        first = 0
        for part, mine in segments.items():
            kept = mine[~hidden[first:first + len(mine)]]
            first += len(mine)
            if len(kept):
                out[part].append((z0, z1, kept))
    return out


def walls_of_slice(slices, k, faces):
    """{part: the wall segments of its material in slice k}, each split where a vertex of the
    faces at the slice's heights or of another part's walls lies on it."""
    walls = {part: wall_segments(s[k]) for part, s in slices.items() if not s[k].is_empty}
    walls = {part: w for part, w in walls.items() if len(w)}
    if not walls:
        return {}
    return dict(zip(walls, walls_split_at_vertices(list(walls.values()), faces)))
