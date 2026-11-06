"""The Verifier's visual check (kese/s8_verify/meshes.py): its rays run along the board's normal in
either orientation (Run.ORIENTATION), so a correct skin passes "flat" as it passes "upright", with
the same faces met on every ray.  In simulation mode, the checks made where each part is built
(kese/core/part_checks.py) give the report stage 8 gives on its own, an open part they found
fails the run, a part whose slices lack a little of its prisms in each of thousands of pieces is
whole (but not with a piece gone, or one lacking much), and the overlap check finds the same
overlaps in threads as in one.  Takes a few seconds.

    python -m pytest tests/test_verifier.py         (or:  python tests/test_verifier.py)"""
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import shapely
from shapely.affinity import translate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core.boundary import Boundary  # noqa: E402
from kese.core.mesh import Mesh  # noqa: E402
from kese.core.part_checks import mesh_check, volume_check, whole  # noqa: E402
from kese.job import start  # noqa: E402
from kese.s1_read import read  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s3_resolve import resolve  # noqa: E402
from kese.s4_geometry import geometry  # noqa: E402
from kese.s5_materials import materials  # noqa: E402
from kese.s6_assemble import assemble  # noqa: E402
from kese.s6_assemble.transform import output_transform  # noqa: E402
from kese.s8_verify import overlap  # noqa: E402
from kese.s8_verify.meshes import _skin_surfaces  # noqa: E402
from kese.s8_verify.verify import every_check  # noqa: E402
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


def checked_model(pcb):
    """A board's Model in simulation mode with the Verifier on, its parts built (and checked) in
    two worker processes."""
    saved = {k: getattr(P.Parallel, k) for k in ("WORKERS", "PROCESS_MIN_COORDINATES")}
    P.override("Parallel.WORKERS", 2)
    P.override("Parallel.PROCESS_MIN_COORDINATES", 0)
    try:
        job = start("simulation", ["glb"], None, (), True, lambda s: None)
        out = str(pcb)
        for stage in (read, collect, resolve, geometry, materials, assemble):
            out = stage.run(out, job)
        job.status.stop()
    finally:
        for k, v in saved.items():
            P.override(f"Parallel.{k}", v)
    return out


def test_the_checks_made_where_the_parts_are_built_give_the_same_report():
    model = checked_model(ROOT / "tests" / "boards" / "six_layer.kicad_pcb")
    assert set(model.checks) == set(model.boundaries) and set(model.meshes) <= set(model.checks)
    ok, lines = every_check(model)
    model.checks.clear()                               # stage 8 checks every part itself
    assert every_check(model) == (ok, lines) and ok, lines


def test_an_open_part_found_where_it_was_built_fails_the_run():
    model = checked_model(ROOT / "tests" / "boards" / "six_layer.kicad_pcb")
    part = next(iter(model.meshes))
    m = model.meshes[part]
    _, volumes = model.checks[part]
    model.checks[part] = (mesh_check(Mesh(m.vertices, m.faces[1:]), model.units), volumes)     # a face missing
    ok, lines = every_check(model)
    assert not ok and lines[0] == "Verifier: FAIL" and any(l.startswith(f"  {part} ") and "closed=False" in l for l in lines)


def test_a_part_lacking_a_little_in_each_of_thousands_of_pieces_is_whole():
    # 2000 holes' finish, 0.1 mm squares 1 mm apart; each sliced a grid step narrower (1e-5 mm3 less):
    # 0.02 mm3 in all, past what a part may lack (Verifier.VERIFY_OPENED_VOLUME_MM3), but no piece is
    squares = [shapely.box(x, y, x + 0.1, y + 0.1) for x in range(50) for y in range(40)]
    prisms = [SimpleNamespace(region=s, z0=-0.8, z1=0.2) for s in squares]

    def checked(regions):
        return volume_check(Boundary("Hole Finish", [-0.8, 0.2], [(-0.8, 0.2, shapely.union_all(regions))]), prisms)
    narrower = [shapely.box(x0, y0, x1 - 1e-4, y1) for x0, y0, x1, y1 in shapely.bounds(squares)]
    c = checked(narrower)
    assert abs(c.prisms - c.slices - 0.02) < 1e-9 and c.pieces.pieces == 2000 and c.pieces.gone == 0
    assert abs(c.pieces.worst - 1e-5) < 1e-12 and whole(c)
    assert not whole(checked(narrower[1:])) and checked(narrower[1:]).pieces.gone == 1       # a piece gone
    halved = checked([shapely.box(10, 10, 10.05, 10.1)] + [r for r, s in zip(narrower, squares) if s.bounds[:2] != (10, 10)])
    assert not whole(halved) and abs(halved.pieces.worst - 0.005) < 1e-12 and halved.pieces.at == (10.05, 10.05, -0.8, 0.2)
    assert checked(squares).pieces is None                                    # pieces compared only where needed


def test_the_overlap_check_finds_the_same_overlaps_in_threads_as_in_one():
    model = checked_model(ROOT / "tests" / "boards" / "six_layer.kicad_pcb")
    assert overlap.overlaps(model) == []
    for part in list(model.boundaries)[:6]:           # each a copy of its own, shifted a little
        slices = [(z0, z1, translate(g, 0.05, 0.03)) for z0, z1, g in model.boundaries[part].slices]
        model.boundaries[f"{part} copy"] = SimpleNamespace(slices=slices)
    saved = P.Parallel.WORKERS, overlap.LEAST_PER_THREAD
    try:
        P.override("Parallel.WORKERS", 1)
        alone = overlap.overlaps(model)
        P.override("Parallel.WORKERS", 3)
        overlap.LEAST_PER_THREAD = 1                  # every group a thread's
        assert len(overlap.dealt(np.arange(50), np.ones(50), 50)) == 12
        assert len(alone) > 100 and overlap.overlaps(model) == alone
    finally:
        P.override("Parallel.WORKERS", saved[0])
        overlap.LEAST_PER_THREAD = saved[1]


if __name__ == "__main__":
    test_the_visual_check_runs_along_the_board_normal_in_either_orientation()
    test_the_checks_made_where_the_parts_are_built_give_the_same_report()
    test_an_open_part_found_where_it_was_built_fails_the_run()
    test_a_part_lacking_a_little_in_each_of_thousands_of_pieces_is_whole()
    test_the_overlap_check_finds_the_same_overlaps_in_threads_as_in_one()
    print("ok")
