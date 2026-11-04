"""The Verifier's visual check (kese/s8_verify/meshes.py): its rays run along the board's normal in
either orientation (Run.ORIENTATION), so a correct skin passes "flat" as it passes "upright", with
the same faces met on every ray.  Takes a moment.

    python -m pytest tests/test_verifier.py         (or:  python tests/test_verifier.py)"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core.mesh import Mesh  # noqa: E402
from kese.s6_assemble.transform import output_transform  # noqa: E402
from kese.s8_verify.meshes import _skin_surfaces  # noqa: E402
from parameters import P  # noqa: E402

CORNERS = np.array([(x, y, z) for z in (0, 1) for y in (0, 1) for x in (0, 1)], dtype=float)
SIDES = np.array([(0, 2, 3), (0, 3, 1), (4, 5, 7), (4, 7, 6), (0, 1, 5), (0, 5, 4),     # wound outward
                  (2, 6, 7), (2, 7, 3), (0, 4, 6), (0, 6, 2), (1, 3, 7), (1, 7, 5)])


def box(lo, hi):
    """The corners of a box from lo to hi (mm), in the order SIDES takes them."""
    return CORNERS * np.subtract(hi, lo) + lo


def test_the_visual_check_runs_along_the_board_normal_in_either_orientation():
    # a laminate and a pad above it, apart: 2 faces on a ray through the laminate, 4 through both
    boxes = {"board": box((0, 0, 0), (10, 6, 1.6)), "pad": box((3, 2, 2.0), (5, 4, 2.035))}
    met, saved = {}, P.Run.ORIENTATION
    try:
        for orientation in ("upright", "flat"):
            P.override("Run.ORIENTATION", orientation)
            M = output_transform()
            meshes = {name: Mesh(v @ M[:3, :3].T, SIDES) for name, v in boxes.items()}
            met[orientation], wrong = _skin_surfaces(meshes, 500, M)
            assert wrong == 0, orientation
    finally:
        P.override("Run.ORIENTATION", saved)
    assert set(met["upright"]) == {2, 4} and met["flat"] == met["upright"], met


if __name__ == "__main__":
    test_the_visual_check_runs_along_the_board_normal_in_either_orientation()
    print("ok")
