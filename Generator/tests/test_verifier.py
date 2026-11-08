"""The Verifier's visual check (kese/s8_verify/meshes.py): its rays run along the board's normal in
either orientation (Run.ORIENTATION), so a correct skin passes "flat" as it passes "upright", with
the same faces met on every ray, and it runs on a 32-bit Python (Pyodide), whose numpy index type is
32 bits; and on a board's skin, rays through the faces left flat on their own take turns in and out
(those faces go).  In simulation mode, the checks made where each part is built
(kese/core/part_checks.py) give the report stage 8 gives on its own, an open part they found
fails the run, a part whose slices lack a little of its prisms in each of thousands of pieces is
whole (but not with a piece gone, or one lacking much), and the overlap check finds the same
overlaps in threads as in one.  Takes about half a minute.

    python -m pytest tests/test_verifier.py         (or:  python tests/test_verifier.py)"""
from types import SimpleNamespace

import numpy as np
import shapely
from shapely.affinity import translate

from helpers import BOARDS, FEATURES, run_stages, run_tests, settings
from kese.core.boundary import Boundary
from kese.core.graph import connected_components
from kese.core.mesh import Mesh
from kese.core.part_checks import mesh_check, volume_check, whole
from kese.s6_assemble import assemble, skin_mesh
from kese.s6_assemble.transform import output_transform
from kese.s8_verify import overlap, vertical_rays
from kese.s8_verify.meshes import _skin_surfaces
from kese.s8_verify.verify import every_check

CORNERS = np.array([(x, y, z) for z in (0, 1) for y in (0, 1) for x in (0, 1)], dtype=float)
SIDES = np.array([(0, 2, 3), (0, 3, 1), (4, 5, 7), (4, 7, 6), (0, 1, 5), (0, 5, 4),     # wound outward
                  (2, 6, 7), (2, 7, 3), (0, 4, 6), (0, 6, 2), (1, 3, 7), (1, 7, 5)])


def box(lo, hi):
    """The corners of a box from lo to hi (mm), in the order SIDES takes them."""
    return CORNERS * np.subtract(hi, lo) + lo


def test_the_visual_check_runs_along_the_board_normal_in_either_orientation():
    # a laminate and a pad above it, apart: 2 faces on a ray through the laminate, 4 through both
    boxes = {"board": box((0, 0, 0), (10, 6, 1.6)), "pad": box((3, 2, 2.0), (5, 4, 2.035))}
    met = {}
    for orientation in ("upright", "flat"):
        with settings({"Run.ORIENTATION": orientation}):
            M = output_transform()
            meshes = {name: Mesh(v @ M[:3, :3].T, SIDES) for name, v in boxes.items()}
            met[orientation], wrong = _skin_surfaces(meshes, 500, M)
        assert wrong == 0, orientation
    assert set(met["upright"]) == {2, 4} and met["flat"] == met["upright"], met


def test_the_visual_check_runs_on_a_32_bit_python():
    # On a 32-bit Python (Pyodide in the browser) numpy's index type np.intp is 32 bits, np.repeat
    # takes its counts only if they cast to it safely, and searchsorted and argsort return it.  The
    # rays are cast here with that numpy, so counts of np.int64 fail as they did in the browser.
    def repeat(a, repeats, axis=None):
        if not np.can_cast(np.asarray(repeats).dtype, np.int32, "safe"):
            raise TypeError("Cannot cast array data from dtype('int64') to dtype('int32') according to the rule 'safe'")
        return np.repeat(a, repeats, axis)

    numpy_32 = SimpleNamespace(**{k: getattr(np, k) for k in dir(np) if not k.startswith("__")})
    numpy_32.intp, numpy_32.repeat = np.int32, repeat
    numpy_32.searchsorted = lambda *a, **k: np.searchsorted(*a, **k).astype(np.int32)
    numpy_32.argsort = lambda *a, **k: np.argsort(*a, **k).astype(np.int32)
    v = np.concatenate([box((0, 0, 0), (10, 6, 1.6)), box((3, 2, 2.0), (5, 4, 2.035))])
    f = np.concatenate([SIDES[:4], SIDES[:4] + 8])                 # the flat faces, as the check casts them
    xy = np.random.default_rng(1).uniform((-1, -1), (11, 7), (500, 2))
    expected = vertical_rays.vertical_hits(v, f, xy)
    saved = vertical_rays.np
    try:
        vertical_rays.np = numpy_32
        found = vertical_rays.vertical_hits(v, f, xy)
    finally:
        vertical_rays.np = saved
    assert len(expected[0]) > 100
    assert all(np.array_equal(a, b) for a, b in zip(found, expected))


def test_rays_through_the_faces_a_board_s_skin_left_flat_on_their_own_take_turns_in_and_out():
    # featureTest/21's finish: where stage 6 moved the edge of a slice a fraction of a grid step onto a
    # vertex of the slice above, it left a gap that thin under the nickel, its walls hidden; its top and
    # bottom were faces left on their own, and the skin kept one of each two.  A ray through any of
    # them met an odd number of faces (64 of the 90 rays here); the Verifier's random rays seldom do
    flat, kept = [], skin_mesh.sealed

    def spy(v, f):                      # the middle of every face of a piece of the skin flat at one height
        edges = np.concatenate([f[:, :2], f[:, 1:]])
        shell = connected_components(len(v), edges[:, 0], edges[:, 1])[1][f[:, 0]]
        z = v[f, 2]
        low, high = np.full(shell.max() + 1, np.inf), np.full(shell.max() + 1, -np.inf)
        np.minimum.at(low, shell, z.min(axis=1))
        np.maximum.at(high, shell, z.max(axis=1))
        flat.append(v[f[(low == high)[shell]]].mean(axis=1)[:, :2])
        return kept(v, f)
    parts = {"Finish.FINISH_ENABLED": True, "SolderMask.SOLDER_MASK_ENABLED": True, "Silkscreen.SILKSCREEN_ENABLED": True}
    skin_mesh.sealed = spy
    try:
        with settings(parts):
            model = run_stages(FEATURES / "21_rf_module.kicad_pcb", assemble, mode="visual")[0]
    finally:
        skin_mesh.sealed = kept
    at = np.concatenate(flat) * (0.001 if model.units == "m" else 1.0)
    met, wrong = _skin_surfaces(model.meshes, 0, model.transform, points=at)
    assert len(at) > 50 and wrong == 0, (len(at), met, wrong)


def checked_model(pcb):
    """A board's Model in simulation mode with the Verifier on, its parts built (and checked) in
    two worker processes."""
    with settings({"Parallel.WORKERS": 2, "Parallel.PROCESS_MIN_COORDINATES": 0}):
        return run_stages(pcb, assemble, verify=True)[0]


def test_the_checks_made_where_the_parts_are_built_give_the_same_report():
    model = checked_model(BOARDS / "six_layer.kicad_pcb")
    assert set(model.checks) == set(model.boundaries) and set(model.meshes) <= set(model.checks)
    ok, lines = every_check(model)
    model.checks.clear()                               # stage 8 checks every part itself
    assert every_check(model) == (ok, lines) and ok, lines


def test_an_open_part_found_where_it_was_built_fails_the_run():
    model = checked_model(BOARDS / "six_layer.kicad_pcb")
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
    model = checked_model(BOARDS / "six_layer.kicad_pcb")
    assert overlap.overlaps(model) == []
    for part in list(model.boundaries)[:6]:           # each a copy of its own, shifted a little
        slices = [(z0, z1, translate(g, 0.05, 0.03)) for z0, z1, g in model.boundaries[part].slices]
        model.boundaries[f"{part} copy"] = SimpleNamespace(slices=slices)
    with settings({"Parallel.WORKERS": 1}):
        alone = overlap.overlaps(model)
    with settings({"Parallel.WORKERS": 3, "Parallel.VERIFY_POLYGONS_PER_THREAD": 1}):      # every group a thread's
        assert len(overlap.dealt(np.arange(50), np.ones(50), 50)) == 12
        assert len(alone) > 100 and overlap.overlaps(model) == alone


if __name__ == "__main__":
    run_tests(__file__)
