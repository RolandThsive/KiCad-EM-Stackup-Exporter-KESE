"""E01: one circular trace on F.Cu, opened by a 0.2 mm gap where its terminals sit.

    python make_board.py        writes E01_circular_loop.kicad_pcb beside this file

The trace's centre line has radius R; its two ends are round, as every KiCad track end is, so the
copper-to-copper gap is GAP_MM when the centre-line ends lie GAP_MM + W_MM apart."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))                # Examples/kicad_writer.py
from kicad_writer import Board  # noqa: E402

R_MM, W_MM, GAP_MM = 10.0, 0.5, 0.2          # loop radius (to the trace's centre), trace width, copper gap
CENTRE = (100.0, 100.0)


def build():
    b = Board("E01_circular_loop", copper=2, thickness=1.6)
    half_gap_deg = math.degrees(math.asin((GAP_MM + W_MM) / 2 / R_MM))
    # the gap sits at angle 0 (towards +x); the trace runs from +half_gap round to 360 - half_gap, in two arcs
    a0, a1 = half_gap_deg, 360.0 - half_gap_deg
    mid = (a0 + a1) / 2
    b.arc_centre(CENTRE, R_MM, a0, mid, W_MM, "F.Cu", "LOOP")
    b.arc_centre(CENTRE, R_MM, mid, a1, W_MM, "F.Cu", "LOOP")
    b.outline_rect(85, 85, 115, 115)
    return b


if __name__ == "__main__":
    build().write(os.path.join(HERE, "E01_circular_loop.kicad_pcb"))
    print("wrote E01_circular_loop.kicad_pcb")
