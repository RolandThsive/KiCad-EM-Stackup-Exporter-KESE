"""The STEP writer without a kernel (kese/s7_write/step.py): a part built from its Boundary, a
box with a through hole beside a second, separate box, written and read back by OpenCascade as
two valid solids with no free edge, the right faces and the right volume; names with a quote
and letters outside ASCII come back as they went in.  Needs OCP (cadquery's OpenCascade);
takes a second.

    python -m pytest tests/test_step_native.py     (or:  python tests/test_step_native.py)"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
import shapely  # noqa: E402

from kese.core.boundary import Boundary  # noqa: E402
from kese.s7_write.step import write_part  # noqa: E402
from kese.s7_write.step_writer import StepWriter, text  # noqa: E402

try:
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from OCP.STEPControl import STEPControl_Reader
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID
    from OCP.TopExp import TopExp, TopExp_Explorer
    from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
except ImportError:
    STEPControl_Reader = None


def boundary():
    """A 10 x 10 x 2 box with a 2 x 2 hole through it, and a 3 x 3 x 2 box beside it."""
    holed = shapely.Polygon([(0, 0), (10, 0), (10, 10), (0, 10)], [[(4, 4), (4, 6), (6, 6), (6, 4)]])
    beside = shapely.box(12, 0, 15, 3)
    region = shapely.MultiPolygon([holed, beside])
    return Boundary("Copper_Net-(U1-GND)", [0.0, 2.0], [(0.0, 2.0, region)], [(0.0, region, False), (2.0, region, True)])


def read_back(path):
    """[(valid, faces, free edges, volume)] per solid."""
    reader = STEPControl_Reader()
    reader.ReadFile(str(path))
    reader.TransferRoots()
    out, ex = [], TopExp_Explorer(reader.OneShape(), TopAbs_SOLID)
    while ex.More():
        solid = ex.Current()
        props = GProp_GProps()
        BRepGProp.VolumeProperties_s(solid, props)
        m = TopTools_IndexedDataMapOfShapeListOfShape()
        TopExp.MapShapesAndAncestors_s(solid, TopAbs_EDGE, TopAbs_FACE, m)
        free = sum(1 for i in range(1, m.Extent() + 1) if m.FindFromIndex(i).Size() < 2)
        faces, fx = 0, TopExp_Explorer(solid, TopAbs_FACE)
        while fx.More():
            faces += 1
            fx.Next()
        out.append((BRepCheck_Analyzer(solid).IsValid(), faces, free, round(props.Mass(), 6)))
        ex.Next()
    return sorted(out, key=lambda r: -r[3])


def test_a_boundary_reads_back_as_valid_solids():
    if STEPControl_Reader is None:
        return                                    # OCP is not installed
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "two.step"
        w = StepWriter(path, "Ünïcode 'board'", "mm")
        solids = write_part(w, "part", boundary(), np.eye(4), lambda s: None)
        assert len(solids) == 2
        w.add_part("Copper_Net-(U1-GND)", (205, 128, 62), solids)
        assert w.close() == path
        assert read_back(path) == [(True, 10, 0, 192.0), (True, 6, 0, 18.0)]
        data = path.read_text(encoding="latin-1")
        name = text("Ünïcode 'board'")                        # the board's name, as STEP spells it
        assert name == "'\\X2\\00DC\\X0\\n\\X2\\00EF\\X0\\code ''board'''" and name in data


def test_step_strings_and_reals():
    assert text("a'b") == "'a''b'"
    assert text("µ") == "'\\X2\\00B5\\X0\\'"
    from kese.s7_write.step_writer import real
    assert real(1) == "1.0" and real(1e-5) == "1.E-05" and real(0.000355) == "0.000355" and real(-2.5e-7) == "-2.5E-07"


if __name__ == "__main__":
    test_a_boundary_reads_back_as_valid_solids()
    test_step_strings_and_reals()
    print("ok")
