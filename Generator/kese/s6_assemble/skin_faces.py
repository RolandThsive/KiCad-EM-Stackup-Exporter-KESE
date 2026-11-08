"""The "visual" mode: the board's visible surface, found in 2D as a part's boundary is but for all
parts at once: one part's faces less every part's material across them, walls less those another
part stands against.  Faces keep their part; hidden triangles go in skin_mesh.py.  The threads make
shapes only from their own copies of the slices (kese/core/shape_copies.py)."""
from concurrent.futures import ThreadPoolExecutor
from itertools import pairwise
from threading import Lock

import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.boundary import heights_of, joined_regions, slices_of_part, wall_segments
from kese.core.graph import shared_tree
from kese.core.vertices import (
    grid_keys,
    pairs_in,
    same_vertices,
    walls_split_at_vertices,
)
from kese.core.memory import give_back_memory
from kese.core.parallel import biggest_first, in_processes, workers_wanted, worth_processes
from kese.core.shape_copies import floating, own

COVERS_BY_PATTERN = shapely.geos_version >= (3, 13, 0)    # a prepared shape answers a pattern with RelateNG


def skin_faces(ps, log):
    """PrismSet -> (levels, the material of every slice, {part: (flats, walls)}): flats as
    (z, region, looks up), walls as (z0, z1, segments), mm, board frame; Parallel.WORKERS at a time."""
    levels = heights_of(ps.prisms)
    by_part = {part: [p for p in prisms if not p.region.is_empty] for part, prisms in ps.by_part().items()}
    slices = slices_of_parts(by_part, levels, log)
    order = list(slices)
    with ThreadPoolExecutor(workers_wanted()) as pool:
        pieces = material_of_every_slice(slices, pool)
        flats = dict(zip(order, pool.map(lambda part: visible_flats(own(slices[part]), levels, pieces), order)))
        for *_, prepared in pieces:
            prepared.pop("copy", None)       # the prepared copies of the material, one per slice
        give_back_memory()
        walls = visible_walls(slices, levels, flats, pool)
    give_back_memory()
    return levels, pieces, {part: (flats[part], walls[part]) for part in by_part}


def slices_of_parts(by_part, levels, log):
    """{part: its slices}, the part with the most coordinates first: the dielectrics and the masks
    take the longest to slice and to cut, and started first no worker is left alone with one at the
    end.  In processes of their own on all but a small board (the work is much of it Python's,
    which threads would take in turn), the notes logged in that order."""
    size = {part: sum(shapely.get_num_coordinates(p.region) for p in prisms) for part, prisms in by_part.items()}
    order = sorted(by_part, key=lambda part: -size[part])
    jobs = [(part, (by_part[part], levels)) for part in order]
    if worth_processes(len(jobs), sum(size.values())):
        done = dict(in_processes(slices_and_notes, jobs, log, "sliced"))
    else:
        done = {part: slices_and_notes(*args) for part, args in jobs}
    for part in order:
        for s in done[part][1]:
            log(f"{part}: {s}")
    return {part: done[part][0] for part in order}


def slices_and_notes(prisms, levels):
    """One part's slices, as a skin needs them (pinches left), and the notes made on the way."""
    notes = []
    return slices_of_part(prisms, levels, notes.append, pinches_opened=False), notes


def material_of_every_slice(slices, pool):
    """Per slice: (every part's polygons in it, the part of each, an index of the polygons, all of
    them joined as one region, and a place for a prepared copy of that region that the threads take
    turns with, see lies_against_material()), for lookups by place and for cutting the faces."""
    gathered = []
    for k in range(len(next(iter(slices.values()), []))):
        polys, parts = [], []
        for part, s in slices.items():
            for p in shapely.get_parts(s[k]):
                polys.append(p)
                parts.append(part)
        polys = np.array(polys, dtype=object)
        gathered.append((polys, np.array(parts, dtype=object), shared_tree(polys)))
    joined = biggest_first(pool, lambda material: joined_regions(list(material[0]), exact=False, shared=True), gathered,
                           [shapely.get_num_coordinates(material[0]).sum() for material in gathered])
    return [(*material, region, {"turn": Lock()}) for material, region in zip(gathered, joined)]


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
    """The region less the material of a slice.  Most faces of a board lie wholly against material
    (inner copper between the dielectrics, copper under the mask, the laminate under the copper) and
    are gone after one covers test.  Otherwise the index finds the pieces that meet the region, with
    the region prepared once (its edges indexed: tested against each piece on its own, its rings were
    walked again for every piece), and the region is cut by a few of them joined, by a big piece on
    its own, or by more as the whole slice.  CIAA ACC's 23,290 cuts, 22,197 of them faces wholly
    against material, take 41 s of thread time so (93 s with the index first and shapely.covers)."""
    polys, _, tree, joined, _ = material
    if lies_against_material(region, material):
        return sh.EMPTY
    near = tree.query(region, predicate="intersects")
    if not len(near):
        return region
    if len(near) > sh.G().SKIN_FEW_PIECES:
        return sh.diff(region, joined)
    cutters = polys[near]
    big = shapely.get_num_coordinates(cutters) > sh.G().SKIN_BIG_PIECE_COORDINATES
    for piece in cutters[big]:
        region = sh.diff(region, piece)
    return sh.diff(region, joined_regions(list(cutters[~big]), exact=False, shared=True)) if (~big).any() else region


def lies_against_material(region, material):
    """Whether the slice's material covers the region wholly: nothing of the region outside it, the
    DE-9IM pattern ******FF*, asked of a prepared copy of the material.  GEOS answers a pattern with
    its newer relate engine (RelateNG), which keeps the material's index from one region to the
    next: the very answers of shapely.covers, in about half the time (CIAA ACC's 23,290 tests take
    12.4 s in one thread, 23.8 s with covers).  Before GEOS 3.13, which has no RelateNG, covers is
    asked: a pattern there would go to the old relate, without the index.  A prepared shape is not
    for two threads at once (GEOS builds its indexes on first use), so the threads take turns with
    one copy per slice, made by the first to ask: a copy for each thread would grow with the number
    of threads, and the turns cost little (on CIAA ACC, 1.7 s of waiting in all, beside 20 s of
    tests)."""
    *_, joined, prepared = material
    if region.is_empty:
        return False
    with prepared["turn"]:
        if "copy" not in prepared:
            prepared["copy"] = shapely.from_wkb(shapely.to_wkb(joined))
            shapely.prepare(prepared["copy"])
        if COVERS_BY_PATTERN:
            return bool(shapely.relate_pattern(prepared["copy"], region, "******FF*"))
        return bool(shapely.covers(prepared["copy"], region))


def visible_walls(slices, levels, flats, pool):
    """Every part's walls per slice, split at the vertices of faces and other parts' walls, less those
    hidden by another part's segment b -> a.  -> {part: [(z0, z1, segments)]}."""
    faces_at = {}
    for part_flats in flats.values():
        for z, region, _ in part_flats:
            faces_at.setdefault(z, []).append(region)
    out = {part: [] for part in slices}

    def walls(k):
        return unhidden(walls_of_slice(dict(zip(slices, floating([s[k] for s in slices.values()]))),   # coordinates read
                                       faces_at.get(levels[k], []) + faces_at.get(levels[k + 1], [])))
    heights = range(len(levels) - 1)
    size = [sum(shapely.get_num_coordinates(s[k]) for s in slices.values()) for k in heights]
    for (z0, z1), segments in zip(pairwise(levels), biggest_first(pool, walls, list(heights), size)):
        for part, kept in segments.items():
            out[part].append((z0, z1, kept))
    return out


def unhidden(segments):
    """{part: its wall segments in one slice} less the segments a -> b that another part's segment
    b -> a hides, the parts left with none dropped."""
    if not segments:
        return {}
    every = np.concatenate(list(segments.values()))
    start, end = grid_keys(every[:, 0]), grid_keys(every[:, 1])
    hidden = pairs_in(end, start, start, end)                           # b -> a among the a -> b
    out, first = {}, 0
    for part, mine in segments.items():
        kept = mine[~hidden[first:first + len(mine)]]
        first += len(mine)
        if len(kept):
            out[part] = kept
    return out


def walls_of_slice(slice_of, faces):
    """{part: the wall segments of its material in one slice ({part: its region there})}, each split
    where a vertex of the faces at the slice's heights or of another part's walls lies on it."""
    walls = {part: wall_segments(s) for part, s in slice_of.items() if not s.is_empty}
    walls = {part: w for part, w in walls.items() if len(w)}
    if not walls:
        return {}
    return dict(zip(walls, walls_split_at_vertices(list(walls.values()), faces)))
