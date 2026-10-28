"""The regression suite's check of a STEP file (tests/test_boards.py): read back with OCP, every
solid valid and every edge shared by two faces.  On its own module so that the suite can run it in
background processes while it exports the next boards: reading a big file back takes minutes."""
import time


def step_audit(path):
    """(invalid solids, free edges, seconds) of a STEP file, via OCP."""
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.STEPControl import STEPControl_Reader
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID
    from OCP.TopExp import TopExp, TopExp_Explorer
    from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
    t0 = time.perf_counter()
    rd = STEPControl_Reader()
    rd.ReadFile(str(path))
    rd.TransferRoots()
    ex, invalid, free = TopExp_Explorer(rd.OneShape(), TopAbs_SOLID), 0, 0
    while ex.More():
        s = ex.Current()
        invalid += not BRepCheck_Analyzer(s).IsValid()
        m = TopTools_IndexedDataMapOfShapeListOfShape()
        TopExp.MapShapesAndAncestors_s(s, TopAbs_EDGE, TopAbs_FACE, m)
        free += sum(1 for i in range(1, m.Extent() + 1) if m.FindFromIndex(i).Size() < 2)
        ex.Next()
    return invalid, free, time.perf_counter() - t0
