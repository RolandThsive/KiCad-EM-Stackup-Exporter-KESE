"""E02: two coaxial circular traces, one on F.Cu (TX) and one on B.Cu (RX), each opened by a 0.2 mm gap.

    python make_board.py        writes E02_coaxial_loops.kicad_pcb beside this file

Both loops are E01's loop: centre-line radius R, width W, round ends GAP_MM apart at angle 0 (towards +x). The
board is 1.6 mm thick, so the two traces' centres sit about 1.565 mm apart in z."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "bridge"))
from kicad_writer import Board  # noqa: E402

R_MM, W_MM, GAP_MM = 10.0, 0.5, 0.2          # loop radius (to the trace's centre), trace width, copper gap
CENTRE = (100.0, 100.0)


def build():
    b = Board("E02_coaxial_loops", copper=2, thickness=1.6)
    half_gap_deg = math.degrees(math.asin((GAP_MM + W_MM) / 2 / R_MM))
    a0, a1 = half_gap_deg, 360.0 - half_gap_deg
    mid = (a0 + a1) / 2
    for layer, net in (("F.Cu", "TX"), ("B.Cu", "RX")):
        b.arc_centre(CENTRE, R_MM, a0, mid, W_MM, layer, net)
        b.arc_centre(CENTRE, R_MM, mid, a1, W_MM, layer, net)
    b.outline_rect(85, 85, 115, 115)
    return b


if __name__ == "__main__":
    build().write(os.path.join(HERE, "E02_coaxial_loops.kicad_pcb"))
    print("wrote E02_coaxial_loops.kicad_pcb")
