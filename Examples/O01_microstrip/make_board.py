"""O01: a straight microstrip on a 1.53 mm FR-4 core over a solid ground plane, for its characteristic impedance
and effective permittivity.

    python make_board.py        writes O01_microstrip.kicad_pcb beside this file

The trace (net RF) runs along x across the whole board, on F.Cu; B.Cu is one filled polygon (no net) under the whole board.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "bridge"))
from kicad_writer import Board  # noqa: E402

LENGTH_MM, WIDTH_MM, BOARD_W_MM = 50.0, 2.9, 30.0
X0, Y0 = 100.0, 100.0                       # the board's centre


def build():
    b = Board("O01_microstrip", copper=2, thickness=1.6, er=4.4, tand=0.02)
    x0, x1 = X0 - LENGTH_MM / 2, X0 + LENGTH_MM / 2
    y0, y1 = Y0 - BOARD_W_MM / 2, Y0 + BOARD_W_MM / 2
    # the track's round ends just touch the board's edges; each port's own strip covers the end it sits on
    b.segment((x0 + WIDTH_MM / 2, Y0), (x1 - WIDTH_MM / 2, Y0), WIDTH_MM, "F.Cu", "RF")
    b.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "B.Cu")
    b.outline_rect(x0, y0, x1, y1)
    return b


if __name__ == "__main__":
    build().write(os.path.join(HERE, "O01_microstrip.kicad_pcb"))
    print("wrote O01_microstrip.kicad_pcb")
