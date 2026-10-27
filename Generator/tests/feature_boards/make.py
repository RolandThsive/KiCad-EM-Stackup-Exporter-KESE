"""Writes the feature boards to the repository's featureTest/ folder, with a README listing them.

    python tests/feature_boards/make.py            (from Generator/)
    python tests/feature_boards/make.py --drc      also print KiCad 7's DRC findings per board

Boards in KiCad 7's format are read back by KiCad 7 when its Python module (pcbnew) is installed:
KiCad fills their zones, adds the outlines of TrueType text and saves them, so the files are
KiCad's own and come out the same on every run.  Without pcbnew they are written as built here,
with unfilled zones.  Boards in KiCad 6, 8, 9 or 10's format are written by hand, token for token
as that KiCad's file writer does; their zone fills are the ones KiCad 7 makes for the same zone,
and are left out without pcbnew."""
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUT = HERE.parents[2] / "featureTest"

import boards_holes_vias as hv  # noqa: E402
import boards_later as later  # noqa: E402
import boards_pads_copper as pc  # noqa: E402
import boards_skipped as sk  # noqa: E402
import boards_stackup_mask as sm  # noqa: E402
import boards_zones_outline as zo  # noqa: E402
from common import kicad7, kicad7_filled  # noqa: E402

ORDER = [("01", hv.holes_slotted), ("02", hv.holes_round), ("03", hv.vias_through),
         ("03b", later.vias_k10), ("04", hv.vias_blind_buried), ("05", hv.vias_micro),
         ("06", later.padstacks), ("07", pc.pad_shapes), ("08", pc.copper_graphics),
         ("08b", later.copper_graphics_nets), ("09", pc.copper_text), ("10", pc.tracks_arcs),
         ("11", zo.zones), ("12", zo.outline_shapes), ("13a", zo.outline_none), ("13b", zo.outline_two),
         ("14", sm.stackup_full), ("15", sm.stackup_none), ("16", sm.edge_plating_castellation),
         ("16b", sm.edge_plating_border),
         ("17", sm.mask_silk), ("18", sm.finishes), ("19", sk.skipped_items),
         ("19b", sk.skipped_items_k10), *[(f"20{c}", fn) for c, fn in later.VERSIONS]]
FORMATS = {20211014: "KiCad 6", 20221018: "KiCad 7", 20240108: "KiCad 8", 20241229: "KiCad 9",
           20260206: "KiCad 10"}


def kicad_save(pcbnew, src, dst, unfilled):
    """Have KiCad 7 read src, fill every zone except the ones named in unfilled, and save dst."""
    if not pcbnew.SaveBoard(str(dst), kicad7_filled(pcbnew, src, unfilled), True):
        raise RuntimeError(f"KiCad could not save {dst}")


def drc(pcbnew, path):
    """KiCad 7's DRC findings for one board, without the footprint-library warnings."""
    with tempfile.TemporaryDirectory() as d:
        rpt = Path(d) / "drc.rpt"
        board = pcbnew.LoadBoard(str(path))
        pcbnew.WriteDRCReport(board, str(rpt), pcbnew.EDA_UNITS_MILLIMETRES, True)
        lines = rpt.read_text(encoding="utf-8").splitlines()
    return [l for l in lines if l.startswith("[") and "lib_footprint" not in l]


def main():
    OUT.mkdir(exist_ok=True)
    kicad = kicad7()
    rows = []
    for num, build in ORDER:
        b = build()
        name = f"{num}_{b.name}.kicad_pcb"
        version = getattr(b, "version", 20221018)
        if version == 20221018 and kicad:
            kicad_save(kicad, b.text(), OUT / name, b.unfilled)
            how = "saved by KiCad 7"
        else:
            (OUT / name).write_text(b.text(), encoding="utf-8")
            how = "unfilled, KiCad 7 not installed" if version == 20221018 else "hand-written"
        doc = " ".join((build.__doc__ or "").split())
        rows.append(f"| `{name}` | {FORMATS[version]} ({how}) | {doc} |")
        print(f"{name:42s} {FORMATS[version]:8s} {how}")
        if "--drc" in sys.argv and kicad and version <= 20221018:
            for line in drc(kicad, OUT / name):
                print("    " + line)
    (OUT / "README.md").write_text(README.format(rows="\n".join(rows)), encoding="utf-8")


README = """# Feature Test Boards

One small board per group of KiCad features that KESE reads. Each board is made by
`Generator/tests/feature_boards/make.py`; change a board there and run it again rather than
editing these files by hand:

```bash
cd Generator
python tests/feature_boards/make.py
```

The regression suite (`Generator/tests/test_boards.py`) runs every board here through every
output; after changing a board, run `python tests/test_boards.py --accept` to record it again.

Boards in KiCad 7's format were read back, zone-filled and saved by KiCad 7 itself, so they are
exactly what KiCad writes, including the outlines of TrueType text. Features that only KiCad 8, 9
or 10 have are on hand-written boards in that version's format, written from KiCad's own file
writer source; open those once in that KiCad to confirm they load.

| File | Format | What it covers |
|---|---|---|
{rows}
"""

if __name__ == "__main__":
    main()
