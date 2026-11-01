"""The "visual" mode: the board's visible surface, found in 2D as a part's boundary is but for all
parts at once: one part's faces less every part's material across them, walls less those another
part stands against.  Faces keep their part; hidden triangles go in skin_mesh.py."""
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
    """PrismSet -> (levels, the material of every slice, {part: (flats, walls)}): flats as
    (z, region, looks up), walls as (z0, z1, segments), mm, board frame; Run.WORKERS at a time."""
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
    """One part's flat faces: at every height its material below less everyone's above (looking up),
    and its material above less everyone's below (looking down)."""
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
    """The region less the material of a slice: a few pieces joined, a big piece on its own, more as
    one overlay; a region wholly against material (most faces of a board) is gone at once."""
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
    """Whether the slice's material covers the region wholly, asked of a prepared copy of the material
    that each thread makes for itself (prepared geometries cannot be shared between threads)."""
    *_, joined, copies = material
    mine = copies.get(get_ident())
    if mine is None:
        mine = copies[get_ident()] = shapely.from_wkb(shapely.to_wkb(joined))
        shapely.prepare(mine)
    return shapely.covers(mine, region)


def visible_walls(slices, levels, flats, pool):
    """Every part's walls per slice, split at the vertices of faces and other parts' walls, less those
    hidden by another part's segment b -> a.  -> {part: [(z0, z1, segments)]}."""
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
