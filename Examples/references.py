"""Textbook values the examples check PyPEEC against. Not part of the bridge: the bridge only turns a board into a
PyPEEC case and reads it back; what a result is compared with belongs to each example."""
import math

MU0 = 1.25663706212e-6               # H/m, CODATA 2018


def ring_inductance(radius_mm, gmd_mm):
    """A circular loop's inductance from the geometric mean distance of its cross-section (Grover):
    mu0 R (ln(8R / g) - 2)."""
    return MU0 * radius_mm * 1e-3 * (math.log(8 * radius_mm / gmd_mm) - 2)
