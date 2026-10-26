"""The STEP file written part by part (kese/s7_write/step_file.py) against the file OpenCascade
writes for the whole assembly at once: four small parts, with a '#', a ';', a quote and letters
outside ASCII in their names, read back with the same names, placements, colours, solids and
volumes, the parts numbered 1 to 4.  Needs cadquery; takes a second.

    python -m pytest tests/test_step_file.py        (or:  python tests/test_step_file.py)"""
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.s7_write.step_file import StepFile  # noqa: E402

try:
    import cadquery as cq
except ImportError:
    cq = None


def parts():
    """{name: (shape, colour)}"""
    box = cq.Solid.makeBox(4, 3, 1)
    holed = cq.Solid.makeBox(4, 3, 1, cq.Vector(5, 0, 0)).cut(cq.Solid.makeCylinder(0.8, 1, cq.Vector(7, 1.5, 0)))
    pin = cq.Solid.makeCylinder(0.4, 2, cq.Vector(0, 5, 0))
    pair = cq.Compound.makeCompound([cq.Solid.makeBox(1, 1, 1, cq.Vector(0, 8, 0)),
                                     cq.Solid.makeBox(1, 1, 1, cq.Vector(1, 8, 0))])
    return {"Board_dielectric 1": (box, cq.Color(0.6, 0.55, 0.35, 1)),
            "Net #1; a'b": (holed, cq.Color(0.9, 0.5, 0.2, 1)),
            "Ünïcode µ": (pin, cq.Color(0.1, 0.2, 0.9, 0.5)),
            "''": (pair, cq.Color(0, 0, 0, 1))}


def read_back(path):
    """(assembly name, [(part name, placement, colour, colours of its solids, solids, volume)])"""
    a = cq.Assembly.importStep(str(path))
    rows = []
    for child in a.children:
        shape = child.obj if child.obj is not None else child.shapes[0]
        colour = lambda c: tuple(round(v, 6) for v in c.toTuple()) if c else None
        rows.append((child.name, child.loc.toTuple(), colour(child.color),
                     sorted(map(colour, getattr(child, "_subshape_colors", {}).values())),
                     len(shape.Solids()), round(shape.Volume(), 9)))
    return a.name, rows


def test_part_by_part_reads_back_as_the_whole_assembly():
    if cq is None:
        return                                    # cadquery is not installed
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        whole = cq.Assembly(name="Board")
        out, one = StepFile(tmp / "joined.step"), tmp / "one.step"
        for name, (shape, colour) in parts().items():
            whole.add(shape, name=name, color=colour)
            asm = cq.Assembly(name="Board")
            asm.add(shape, name=name, color=colour)
            asm.export(str(one), exportType="STEP")
            out.add(one)
        assert out.close() == tmp / "joined.step"
        out.discard()
        whole.export(str(tmp / "whole.step"), exportType="STEP")
        expected, got = read_back(tmp / "whole.step"), read_back(tmp / "joined.step")
        assert got == expected, f"whole assembly: {expected}\npart by part:   {got}"
        # the id of each part in the assembly: OpenCascade counts them over the whole process
        ids = re.findall(r"NEXT_ASSEMBLY_USAGE_OCCURRENCE\('([^']*)'", (tmp / "joined.step").read_text(encoding="latin-1"))
        assert ids == ["1", "2", "3", "4"], f"the ids of the parts: {ids}"
        assert sorted(p.name for p in tmp.iterdir()) == ["joined.step", "one.step", "whole.step"]


def test_no_part_writes_no_file():
    with tempfile.TemporaryDirectory() as tmp:
        out = StepFile(Path(tmp) / "empty.step")
        assert out.close() is None
        out.discard()
        assert not list(Path(tmp).iterdir())


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"{name:64s} ok")
            except AssertionError as exc:
                failed += 1
                print(f"{name:64s} FAIL\n    " + str(exc).replace("\n", "\n    "))
    sys.exit(1 if failed else 0)
