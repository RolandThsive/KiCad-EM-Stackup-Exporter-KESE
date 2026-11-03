"""The regression suite's check of a STEP file (tests/test_boards.py): read back with OCP, every
solid valid and every edge shared by two faces.

OpenCascade reads a file in one thread and holds about ten times its size in memory, so a file KESE
wrote is read back one part at a time: parts() finds where each part's entities are (they stand on
their own; the few the parts share are the assembly's, #1 to #24, at the end of the file), and
audit_part() copies one part into a STEP file of its own, with the assembly cut down to that part,
and checks it.  step_audit() reads the parts side by side in background processes, the biggest first;
the suite hands the parts to its own processes instead.  A solid is checked on its own either way,
so the counts are those of reading the whole file.

By default a file is read as it is, without OpenCascade's shape healing (which takes most of the
reading time and would mend what it finds rather than report it).  Only what a reader must work out
itself is added before the check, and no geometry moves: the curves of the edges in the parameters
of their faces (pcurves; KESE writes none, as KiCad does not), stored once instead of projected
again at every query, and on a cylinder an edge's pcurve moved by a whole turn where it came out a
turn off.  healed=True reads as OpenCascade does by default, with healing (the old, slower check)."""
import mmap
import multiprocessing
import os
import re
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor

NO_HEALING = {"read.step.resource.name": "", "FromSTEP.exec.op": ""}     # OpenCascade 7.8's static settings
DATA = b"\nDATA;\n"
PART_END = re.compile(rb"= COLOUR_RGB\(")                 # a part's last entity (StepWriter.add_part)
ASSEMBLY = b"\n#1 = "                                     # the assembly's entities, after the last part
PLACEMENTS = re.compile(rb"#10 = SHAPE_REPRESENTATION\('',\(#11,([^)]*)\),#19\);")    # one per part
SMALL = 20 * 2**20                # bytes: a file this small is read here, part after part (no processes)


def step_audit(path, healed=False, workers=None):
    """(invalid solids, free edges, seconds of reading summed over the parts) of a STEP file, via OCP;
    its parts read in `workers` processes (None: one per processor thread, none for a SMALL file)."""
    jobs = parts(path)
    if workers is None:
        workers = 1 if os.path.getsize(path) < SMALL else os.cpu_count() or 1
    workers = min(workers, len(jobs))
    if workers == 1:
        return total([audit_part(job, healed) for job in jobs])
    with ProcessPoolExecutor(workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        return total(list(pool.map(audit_part, jobs, [healed] * len(jobs))))


def total(results):
    """The audit_part() results of a file's parts as one: (invalid solids, free edges, seconds)."""
    return tuple(sum(r[k] for r in results) for k in range(3))


def parts(path):
    """The parts of a STEP file as audit_part() jobs, the biggest first: (path, first byte, end byte,
    the part's placement in the assembly).  A file KESE did not write is one job: (path, None, None,
    None), the whole file."""
    with open(path, "rb") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        ends = [mm.find(b"\n", m.end()) + 1 for m in PART_END.finditer(mm)]
        assembly = mm.rfind(ASSEMBLY)
        listed = PLACEMENTS.search(mm, assembly) if ends and assembly > 0 else None
        placements = [int(p) for p in re.findall(rb"#(\d+)", listed.group(1))] if listed else []
        first = mm.find(DATA) + len(DATA)
    if not ends or len(placements) != len(ends):
        return [(str(path), None, None, None)]
    jobs = [(str(path), a, b, p) for a, b, p in zip([first] + ends[:-1], ends, placements)]
    return sorted(jobs, key=lambda job: job[1] - job[2])


def audit_part(job, healed=False):
    """(invalid solids, free edges, seconds) of one parts() job."""
    t0 = time.perf_counter()
    path, start, end, placement = job
    if start is None:
        return (*check(read(path, healed)), time.perf_counter() - t0)
    fd, name = tempfile.mkstemp(suffix=".step")
    try:
        with os.fdopen(fd, "wb") as out, open(path, "rb") as f, \
                mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            assembly = mm.rfind(ASSEMBLY) + 1
            out.write(mm[:mm.find(DATA) + len(DATA)])                       # the header
            out.write(mm[start:end])                                          # the part
            out.write(PLACEMENTS.sub(b"#10 = SHAPE_REPRESENTATION('',(#11,#%d),#19);" % placement,
                                     mm[assembly:], count=1))                 # the assembly, of this part
        shape = read(name, healed)
    finally:
        os.remove(name)
    return (*check(shape), time.perf_counter() - t0)


def read(path, healed=False):
    """The shape of a STEP file, as OCP reads it (see above)."""
    from OCP.Interface import Interface_Static
    from OCP.STEPControl import STEPControl_Reader
    rd = STEPControl_Reader()             # first: it sets up the STEP settings the next lines change
    # no shape healing while reading: OpenCascade's settings for the whole process, put back after
    saved = {key: Interface_Static.CVal_s(key) for key in NO_HEALING}
    try:
        if not healed:
            for key, value in NO_HEALING.items():
                Interface_Static.SetCVal_s(key, value)
        rd.ReadFile(str(path))
        rd.TransferRoots()
    finally:
        for key, value in saved.items():
            Interface_Static.SetCVal_s(key, value)
    shape = rd.OneShape()
    if not healed:
        add_pcurves(shape)
    return shape


def check(shape):
    """(invalid solids, free edges) of a shape: every solid checked on its own."""
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID
    from OCP.TopExp import TopExp, TopExp_Explorer
    from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
    ex, invalid, free = TopExp_Explorer(shape, TopAbs_SOLID), 0, 0
    while ex.More():
        s = ex.Current()
        invalid += not BRepCheck_Analyzer(s).IsValid()
        m = TopTools_IndexedDataMapOfShapeListOfShape()
        TopExp.MapShapesAndAncestors_s(s, TopAbs_EDGE, TopAbs_FACE, m)
        free += sum(1 for i in range(1, m.Extent() + 1) if m.FindFromIndex(i).Size() < 2)
        ex.Next()
    return invalid, free


def add_pcurves(shape):
    """Every edge's pcurve on each of its faces, as a reader works it out (see above): on a plane
    built once and stored; on a curved face (a cylinder) added where missing, and the wire's pcurves
    moved by a whole turn where they came out a turn off.  No 3D curve or point changes."""
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.BRepLib import BRepLib
    from OCP.GeomAbs import GeomAbs_Plane
    from OCP.ShapeAnalysis import ShapeAnalysis_Edge
    from OCP.ShapeFix import ShapeFix_Edge, ShapeFix_Wire
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_WIRE
    from OCP.TopExp import TopExp, TopExp_Explorer
    from OCP.TopoDS import TopoDS
    from OCP.TopTools import TopTools_IndexedMapOfShape
    faces = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(shape, TopAbs_FACE, faces)
    fix, look = ShapeFix_Edge(), ShapeAnalysis_Edge()
    for i in range(1, faces.Extent() + 1):
        f = TopoDS.Face_s(faces.FindKey(i))
        plane = BRepAdaptor_Surface(f, False).GetType() == GeomAbs_Plane
        ex = TopExp_Explorer(f, TopAbs_EDGE)
        while ex.More():
            e = TopoDS.Edge_s(ex.Current())
            if plane:
                BRepLib.BuildPCurveForEdgeOnPlane_s(e, f)
            elif not look.HasPCurve(e, f):
                fix.FixAddPCurve(e, f, False)
            ex.Next()
        if not plane:
            wires = TopExp_Explorer(f, TopAbs_WIRE)
            while wires.More():
                ShapeFix_Wire(TopoDS.Wire_s(wires.Current()), f, 1e-7).FixShifted()
                wires.Next()
