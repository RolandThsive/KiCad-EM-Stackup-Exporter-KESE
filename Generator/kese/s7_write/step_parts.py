"""A big board's STEP parts worked on in processes of their own (much of the work is Python's), in
two rounds.  First each part's topology and arcs, which give the exact number of entities it takes
(step_brep.entity_count), so that every part's first number is known; then each part's entities,
numbered from there, written into a file of its own.  Those files are copied into the STEP file
in the parts' order, which comes out the same, byte for byte, as one written part after part.  The
files go into a hidden folder beside the STEP file, removed when it is done or fails."""
import pickle
import shutil
from pathlib import Path

import shapely

from kese.core.parallel import in_processes
from kese.s7_write.step_brep import entity_count, write_brep
from kese.s7_write.step_curved import with_arcs
from kese.s7_write.step_topology import topology_of
from kese.s7_write.step_writer import PRODUCT, Entities
from parameters import P


def topology(part, boundary, log):
    """A part's Topology for STEP, with its arcs (Step.STEP_EXACT_ARCS); what is wrong with it logged."""
    topo = topology_of(boundary)
    if topo.edges_not_used_twice:
        log(f"step: {part}: {topo.edges_not_used_twice} edges are not shared by two faces (the solid is open there)")
    if P.Step.STEP_EXACT_ARCS:
        try:
            topo = with_arcs(topo)
        except Exception as e:                            # a bug in the arcs must not cost the file: faceted instead
            log(f"step: {part}: written without arcs ({type(e).__name__}: {e})")
    return topo


def size(boundary):
    """The coordinates of a part's faces: what its work grows with."""
    return sum(int(shapely.get_num_coordinates(region)) for _, region, _ in boundary.flats)


def found(part, boundary, transform, kept):
    """First round, in a worker: a part's topology, kept in file `kept` for the second ->
    (the entity numbers it takes, its solids, the notes made on the way)."""
    notes = []
    topo = topology(part, boundary, notes.append)
    with open(kept, "wb") as f:
        pickle.dump(topo, f, protocol=pickle.HIGHEST_PROTOCOL)
    return entity_count(topo, transform), topo.shells, notes


def written(kept, transform, first, path):
    """Second round, in a worker: the part's entities, numbered from `first`, into file `path` ->
    (the ids of its solids, the entity numbers it took).  The topology's file goes only once the
    part is written: a worker lost on the way (out of memory) leaves it to the main process, which
    writes the part again from it."""
    with open(kept, "rb") as f:
        topo = pickle.load(f)
    w = Entities(path, first)
    try:
        done = write_brep(w, topo, transform), w.next - first
    finally:
        w.file.close()
    Path(kept).unlink()
    return done


def write_in_processes(w, model, parts, log):
    """The parts (their names, in the order they are listed) into the StepWriter w, each with its
    product, through the two rounds above."""
    folder = w.path.with_name(f".{w.path.name[:40]}.parts")     # a long name cut: Windows' 260-character paths
    folder.mkdir(exist_ok=True)
    try:
        at = {part: folder / str(k) for k, part in enumerate(parts)}
        biggest = sorted(parts, key=lambda part: -size(model.boundaries[part]))
        jobs = [(part, (part, model.boundaries[part], model.transform, at[part].with_suffix(".topology")))
                for part in biggest]
        done = dict(in_processes(found, jobs, log, "made ready for STEP"))
        first, n = {}, w.next
        for part in parts:
            count, shells, notes = done[part]
            for s in notes:
                log(s)
            first[part] = n
            n += count + (PRODUCT + shells if shells else 0)
        jobs = [(part, (at[part].with_suffix(".topology"), model.transform, first[part], at[part].with_suffix(".step")))
                for part in sorted(parts, key=lambda part: -done[part][0])]
        texts = dict(in_processes(written, jobs, log, "written to STEP"))
        for part in parts:
            solids, took = texts[part]
            if took != done[part][0] or w.next != first[part]:     # a bug in entity_count: no file rather than a wrong one
                raise RuntimeError(f"step: {part} took {took} entity numbers from #{first[part]}, "
                                   f"counted {done[part][0]} from #{w.next}")
            w.add_text(at[part].with_suffix(".step"), took)
            at[part].with_suffix(".step").unlink()
            if solids:
                w.add_part(part, model.materials[part]["rgb"], solids)
    finally:
        shutil.rmtree(folder, ignore_errors=True)
