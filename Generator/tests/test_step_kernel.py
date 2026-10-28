"""The STEP writer with a CAD kernel (kese/s7_write/step_cadquery.py, Run.BUILD_WITH_KERNELS): a
board written in metres and in millimetres declares the units it is written in, so both read back
at the same size, and a STEP file read afterwards in the same process still comes in millimetres.
Needs cadquery; takes ten seconds.

    python -m pytest tests/test_step_kernel.py      (or:  python tests/test_step_kernel.py)"""
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.pipeline import generate  # noqa: E402
from parameters import P  # noqa: E402

try:
    import cadquery  # noqa: F401
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    from OCP.STEPControl import STEPControl_Reader
except ImportError:
    STEPControl_Reader = None

BOARD = ROOT / "tests" / "boards" / "one_layer.kicad_pcb"


def size(path):
    """(declared length unit, (dx, dy, dz) in mm as OpenCascade reads the file)"""
    unit = re.search(r"LENGTH_UNIT\(\)\s*NAMED_UNIT\(\*\)\s*SI_UNIT\(([^)]*)\)", path.read_text(encoding="latin-1"))
    reader = STEPControl_Reader()
    reader.ReadFile(str(path))
    reader.TransferRoots()
    box = Bnd_Box()
    BRepBndLib.Add_s(reader.OneShape(), box)
    x0, y0, z0, x1, y1, z1 = box.Get()
    return unit.group(1), tuple(round(v, 4) for v in (x1 - x0, y1 - y0, z1 - z0))


def test_kernel_step_declares_its_units():
    if STEPControl_Reader is None:
        return                                    # cadquery is not installed
    saved = P.Run.BUILD_WITH_KERNELS, P.Run.UNITS
    read = {}
    try:
        with tempfile.TemporaryDirectory() as tmp:
            for units in ("m", "mm"):
                P.override("Run.BUILD_WITH_KERNELS", True)
                P.override("Run.UNITS", units)
                out, _ = generate(BOARD, mode="simulation", formats=["step"], out_root=Path(tmp) / units,
                                  verify=False, log=lambda s: None)
                read[units] = size(out / f"{BOARD.stem}.step")
    finally:
        P.override("Run.BUILD_WITH_KERNELS", saved[0])
        P.override("Run.UNITS", saved[1])
    assert read["m"][0] == "$,.METRE." and read["mm"][0] == ".MILLI.,.METRE."
    assert read["m"][1] == read["mm"][1] and read["mm"][1][0] > 1.0      # the same board, in mm


if __name__ == "__main__":
    test_kernel_step_declares_its_units()
    print("ok")
