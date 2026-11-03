"""The regression suite's check of a STEP file (tests/test_boards.py): read back with OCP, every
solid valid and every edge shared by two faces.  On its own module so that the suite can run it in
background processes while it exports the next boards: reading a big file back takes minutes.

By default the file is read as it is, without OpenCascade's shape healing (which takes most of the
reading time and would mend what it finds rather than report it).  Only what a reader must work out
itself is added before the check, and no geometry moves: the curves of the edges in the parameters
of their faces (pcurves; KESE writes none, as KiCad does not), stored once instead of projected
again at every query, and on a cylinder an edge's pcurve moved by a whole turn where it came out a
turn off.  healed=True reads as OpenCascade does by default, with healing (the old, slower check)."""
import time

NO_HEALING = {"read.step.resource.name": "", "FromSTEP.exec.op": ""}     # OpenCascade 7.8's static settings


def step_audit(path, healed=False):
    """(invalid solids, free edges, seconds) of a STEP file, via OCP."""
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.Interface import Interface_Static
    from OCP.STEPControl import STEPControl_Reader
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID
    from OCP.TopExp import TopExp, TopExp_Explorer
    from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
    t0 = time.perf_counter()
    rd = STEPControl_Reader()
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
    ex, invalid, free = TopExp_Explorer(shape, TopAbs_SOLID), 0, 0
    while ex.More():
        s = ex.Current()
        invalid += not BRepCheck_Analyzer(s).IsValid()
        m = TopTools_IndexedDataMapOfShapeListOfShape()
        TopExp.MapShapesAndAncestors_s(s, TopAbs_EDGE, TopAbs_FACE, m)
        free += sum(1 for i in range(1, m.Extent() + 1) if m.FindFromIndex(i).Size() < 2)
        ex.Next()
    return invalid, free, time.perf_counter() - t0


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
