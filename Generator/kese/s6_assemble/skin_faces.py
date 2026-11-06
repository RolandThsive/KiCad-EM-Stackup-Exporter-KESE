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
from kese.core.parallel import in_processes, workers_wanted, worth_processes
from kese.core.shape_copies import floating, own


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
    joined = pool.map(lambda material: joined_regions(list(material[0]), exact=False, shared=True), gathered)
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
    """The region less the material of a slice: a few pieces joined, a big piece on its own, more as
    one overlay; a region wholly against material (most faces of a board) is gone at once.  The
    index finds the pieces that meet the region with the region prepared once (its edges indexed):
    tested against each piece on its own, the region's rings are walked again for every piece, which
    on NE_Delta's skin took 251 s of thread time where the index takes 43 s."""
    polys, _, tree, joined, _ = material
    near = tree.query(region, predicate="intersects")
    if not len(near):
        return region
    cutters = polys[near]
    few, big = sh.G().SKIN_FEW_PIECES, shapely.get_num_coordinates(cutters) > sh.G().SKIN_BIG_PIECE_COORDINATES
    if (big.any() or len(near) > few) and lies_against_material(region, material):
        return sh.EMPTY
    if len(near) > few:
        return sh.diff(region, joined)
    for piece in cutters[big]:
        region = sh.diff(region, piece)
    return sh.diff(region, joined_regions(list(cutters[~big]), exact=False, shared=True)) if (~big).any() else region


def lies_against_material(region, material):
    """Whether the slice's material covers the region wholly, asked of a prepared copy of the material.
    A prepared shape is not for two threads at once (GEOS builds its indexes on first use), so the
    threads take turns with one copy per slice, made by the first to ask: a copy for each thread
    would grow with the number of threads, and the turns cost nothing to speak of (on the suite's
    biggest boards, a few hundred calls taking a hundredth of the flat faces' time)."""
    *_, joined, prepared = material
    with prepared["turn"]:
        if "copy" not in prepared:
            prepared["copy"] = shapely.from_wkb(shapely.to_wkb(joined))
            shapely.prepare(prepared["copy"])
        return shapely.covers(prepared["copy"], region)


def visible_walls(slices, levels, flats, pool):
    """Every part's walls per slice, split at the vertices of faces and other parts' walls, less those
    hidden by another part's segment b -> a.  -> {part: [(z0, z1, segments)]}."""
    faces_at = {}
    for part_flats in flats.values():
        for z, region, _ in part_flats:
            faces_at.setdefault(z, []).append(region)
    out = {part: [] for part in slices}

    def walls(k):
        return walls_of_slice(dict(zip(slices, floating([s[k] for s in slices.values()]))),     # coordinates read
                              faces_at.get(levels[k], []) + faces_at.get(levels[k + 1], []))
    for (z0, z1), segments in zip(pairwise(levels), pool.map(walls, range(len(levels) - 1))):
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


def walls_of_slice(slice_of, faces):
    """{part: the wall segments of its material in one slice ({part: its region there})}, each split
    where a vertex of the faces at the slice's heights or of another part's walls lies on it."""
    walls = {part: wall_segments(s) for part, s in slice_of.items() if not s.is_empty}
    walls = {part: w for part, w in walls.items() if len(w)}
    if not walls:
        return {}
    return dict(zip(walls, walls_split_at_vertices(list(walls.values()), faces)))
