"""The regression suite's check of a STEP file (tests/test_boards.py): read back with OCP, every
solid there, every solid valid and every edge shared by two faces.  On its own module so that the
suite can run it in background processes while it exports the next boards: reading a big file back
takes minutes.

Reading a big file back is slow in one process: OpenCascade turns the whole file into shapes in one
thread (minutes for the example boards) before the first solid is checked.  With `workers` above
one, the file is cut into smaller STEP files of whole parts, which a pool of `workers` processes
reads back and checks at once, so the reading is shared out as well as the checking.  The cutting
relies on how KESE writes a STEP file (step_writer.py): the shared entities #1 to #24, and each
part's entities in one block that ends with its ADVANCED_BREP_SHAPE_REPRESENTATION, after its
SHAPE_DEFINITION_REPRESENTATION.  When a file is not laid out that way (a reference that leads out
of its part's block), or the pieces give back fewer solids than the file has, the whole file is
read back in one process as before, so the result never depends on the cutting."""
import multiprocessing
import re
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

SHARED = range(1, 25)           # ids of the entities every part refers to: contexts, units, origin
ASSEMBLY = {3, 4, 5, 6, 7, 8, 9, 10, 24}        # the shared entities that list or name every part
SPLIT_FROM_BYTES = 5_000_000    # smaller files are checked whole: cutting them saves nothing
# Pieces per process: more pieces than processes, handed out biggest first as processes come free,
# because a piece's size says little about how long it takes (a solder mask takes far longer to
# check than a copper part of the same size), so a slow piece does not hold up the pieces behind it
PIECES_PER_WORKER = 3
REF = re.compile(r"#(\d+)")
ID = re.compile(r"#(\d+)\s*=")


def check_shape(shape):
    """(invalid solids, free edges, solids) of an OCP shape."""
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID
    from OCP.TopExp import TopExp, TopExp_Explorer
    from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
    ex, invalid, free, solids = TopExp_Explorer(shape, TopAbs_SOLID), 0, 0, 0
    while ex.More():
        s = ex.Current()
        solids += 1
        invalid += not BRepCheck_Analyzer(s).IsValid()
        m = TopTools_IndexedDataMapOfShapeListOfShape()
        TopExp.MapShapesAndAncestors_s(s, TopAbs_EDGE, TopAbs_FACE, m)
        free += sum(1 for i in range(1, m.Extent() + 1) if m.FindFromIndex(i).Size() < 2)
        ex.Next()
    return invalid, free, solids


def read_and_check(path):
    """(invalid solids, free edges, solids) of one STEP file, read back with OCP."""
    from OCP.STEPControl import STEPControl_Reader
    rd = STEPControl_Reader()
    rd.ReadFile(str(path))
    rd.TransferRoots()
    return check_shape(rd.OneShape())


def entities(path):
    """(id, text) of every entity in the DATA section of a STEP file, in file order."""
    buf = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or buf:
                buf.append(line)
                if line.rstrip().endswith(";"):
                    text = "".join(buf)
                    buf = []
                    yield int(ID.match(text).group(1)), text


def cut(path, n, folder):
    """Cut a STEP file KESE wrote into at most `n` files of whole parts in `folder`, about equal in
    size; -> (their paths, the number of solids in the whole file), or None when the file is not
    laid out the way the cutting needs."""
    shared, parts, block, solids = {}, [], {}, 0
    for eid, text in entities(path):
        if eid in SHARED:
            shared[eid] = text
            continue
        block[eid] = text
        solids += "MANIFOLD_SOLID_BREP(" in text
        if "ADVANCED_BREP_SHAPE_REPRESENTATION(" in text:
            # the part: what its representation and its product (the shape definition that names
            # the representation, which makes it a root for the reader) lead to, in its block
            keep, todo = {}, [eid] + [i for i, t in block.items() if "SHAPE_DEFINITION_REPRESENTATION(" in t]
            while todo:
                i = todo.pop()
                if i in keep or i in SHARED:
                    continue
                if i not in block:
                    return None             # a reference out of the part's block
                keep[i] = block[i]
                todo += [int(r) for r in REF.findall(block[i].split("=", 1)[1])]
            parts.append("".join(keep[i] for i in sorted(keep)))
            block = {}
    if not parts or set(SHARED) - set(shared):
        return None
    head = "".join(text for i, text in sorted(shared.items()) if i not in ASSEMBLY)
    loads, shares = [0] * min(n, len(parts)), [[] for _ in range(min(n, len(parts)))]
    for text in sorted(parts, key=len, reverse=True):           # biggest first, to the lightest share
        k = loads.index(min(loads))
        loads[k] += len(text)
        shares[k].append(text)
    paths = []
    for k, share in enumerate(shares):
        p = Path(folder) / f"share_{k}.step"
        p.write_text("ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('KESE audit share'),'2;1');\n"
                     "FILE_NAME('share.step','',(''),(''),'KESE','KESE','');\n"
                     "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n"
                     + head + "".join(share) + "ENDSEC;\nEND-ISO-10303-21;\n", encoding="utf-8")
        paths.append(p)
    return paths, solids


def solids_in(path):
    """How many solids (MANIFOLD_SOLID_BREP) a STEP file has."""
    with open(path, encoding="utf-8") as f:
        return sum(line.count("MANIFOLD_SOLID_BREP(") for line in f)


def step_audit(path, workers=1):
    """(invalid solids, free edges, seconds, solids the reader left out) of a STEP file, via OCP, in
    `workers` processes.  The reader leaves out a solid it cannot build (a shell with a face missing,
    for one) without an error, so the solids read back are counted against the file's."""
    t0 = time.perf_counter()
    if workers > 1 and Path(path).stat().st_size >= SPLIT_FROM_BYTES:
        with tempfile.TemporaryDirectory() as folder:
            split = cut(path, workers * PIECES_PER_WORKER, folder)
            if split:
                paths, solids = split
                paths.sort(key=lambda q: q.stat().st_size, reverse=True)      # biggest first
                with ProcessPoolExecutor(workers, mp_context=multiprocessing.get_context("spawn")) as pool:
                    results = list(pool.map(read_and_check, paths, chunksize=1))
                if sum(r[2] for r in results) == solids:        # else: read the whole file to be sure
                    return sum(r[0] for r in results), sum(r[1] for r in results), time.perf_counter() - t0, 0
    invalid, free, read = read_and_check(path)
    return invalid, free, time.perf_counter() - t0, solids_in(path) - read
