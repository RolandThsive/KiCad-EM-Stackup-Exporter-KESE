"""Work cut up any way gives the same result (parameters/Run_KESE/Parallel.py): batches of any size (the
skin's probes, the Verifier's rays and the STEP writer's slices, the last to the byte), a STEP file
written part by part in worker processes, to the byte and with the same notes (a part whose worker
is lost in its second round written again here), and the copper layers joined in worker processes,
to the byte and on the same grid, whatever the number of workers.

    python -m pytest tests/test_same_result.py      (or:  python tests/test_same_result.py)"""
import tempfile
from pathlib import Path

import numpy as np
import shapely

from helpers import BOARDS, run_stages, run_tests, settings
from kese.core.boundary import Boundary
from kese.s3_resolve import resolve
from kese.s6_assemble import assemble
from kese.s6_assemble.skin_mesh import looks_at_material
from kese.s7_write import step
from kese.s7_write.step import write_part
from kese.s7_write.step_writer import StepWriter
from kese.s8_verify.vertical_rays import vertical_hits
from parameters import P


def test_batches_of_any_size_give_the_same_result():
    # the batch sizes of parameters/Run_KESE/Parallel.py set how much is held at once, not what comes out
    rng = np.random.default_rng(1)
    v, f = rng.random((60, 3)), rng.integers(0, 60, (40, 3))
    material = shapely.box(0.2, 0.2, 0.7, 0.9)
    levels, xy = np.array([0.0, 0.5, 1.0]), rng.random((50, 2))
    def pieces():
        return [(None, None, None, material, {}), (None, None, None, material, {})]
    whole = (looks_at_material(v, f, levels, pieces()), vertical_hits(v, f, xy))
    with settings({"Parallel.WORKERS": 2, "Parallel.SKIN_PROBES_AT_A_TIME": 7, "Parallel.VERIFY_TRIANGLES_AT_A_TIME": 3}):
        batched = (looks_at_material(v, f, levels, pieces()), vertical_hits(v, f, xy))
    with settings({"Parallel.WORKERS": 4, "Parallel.SKIN_PROBES_PER_SHARE": 2}):     # each slice's probes shared
        shared = looks_at_material(v, f, levels, pieces())
    assert whole[0].tolist() == batched[0].tolist() == shared.tolist() and whole[0].any() and not whole[0].all()
    assert all(np.array_equal(a, b) for a, b in zip(whole[1], batched[1])) and len(whole[1][0])


def step_data(tmp, rows, arcs):
    """The DATA section of a STEP file of one part (a seven-pointed star with a round hole) written
    Parallel.STEP_ROWS_AT_A_TIME = rows at a time, with or without its arcs."""
    t = np.arange(14) * np.pi / 7
    star = shapely.Polygon(np.c_[np.cos(t), np.sin(t)] * np.where(np.arange(14) % 2, 4.0, 10.0)[:, None],
                           [shapely.Point(0.3, 0.2).buffer(1.5, quad_segs=16).exterior.coords])
    region = shapely.MultiPolygon([star, shapely.box(12, 0, 15, 3)])
    part = Boundary("star", [0.0, 1.6], [(0.0, 1.6, region)], [(0.0, region, False), (1.6, region, True)])
    with settings({"Parallel.WORKERS": 1, "Parallel.STEP_ROWS_AT_A_TIME": rows, "Step.STEP_EXACT_ARCS": arcs}):
        path = Path(tmp) / f"{rows}_{arcs}.step"
        w = StepWriter(path, "star", "mm")
        w.add_part("star", (205, 128, 62), write_part(w, "star", part, np.diag([0.001, 0.001, 0.001, 1.0]), print))
        text = w.close().read_text(encoding="latin-1")
    return text[text.index("\nDATA;"):]


def test_a_step_part_is_written_the_same_in_slices_of_any_size():
    # the STEP writer's slices (Parallel.STEP_ROWS_AT_A_TIME) bound what it holds at once: the
    # entities, their numbers and their order are the same whatever their size
    with tempfile.TemporaryDirectory() as tmp:
        for arcs in (True, False):
            whole = step_data(tmp, 100_000, arcs)
            assert whole.count("DIRECTION(") > 10 and ("CIRCLE(" in whole) == arcs
            for rows in (1, 4, 7):
                assert step_data(tmp, rows, arcs) == whole, (rows, arcs)


def board_model(pcb):
    """A board's Model in simulation mode (stages 1 to 6), built in this process."""
    return run_stages(pcb, assemble, formats=["step"])[0]


def test_a_step_file_written_in_processes_is_the_same_to_the_byte():
    # each part's entities counted first, then written in a worker into a file of their own, and
    # the files joined in order: the same file, and the same notes, as one written part after part
    # in this process, whatever the number of workers, with arcs and without, and no temporary file
    # left behind
    model = board_model(BOARDS / "six_layer.kicad_pcb")
    with tempfile.TemporaryDirectory() as tmp:
        for arcs in (True, False):
            files, notes = {}, {}
            for workers, least in ((1, 10 ** 12), (2, 0), (3, 0)):
                notes[workers] = []
                with settings({"Parallel.WORKERS": workers, "Parallel.PROCESS_MIN_COORDINATES": least,
                               "Step.STEP_EXACT_ARCS": arcs}):
                    path = step.write(model, Path(tmp) / f"{workers}_{arcs}.step", notes[workers].append)
                text = path.read_text(encoding="latin-1")
                files[workers] = text[text.index("\nDATA;"):]
            assert files[1] == files[2] == files[3] and ("CIRCLE(" in files[1]) == arcs, arcs
            assert notes[1] == notes[2] == notes[3], notes
        assert sorted(p.name for p in Path(tmp).iterdir()) == sorted(f"{w}_{a}.step" for w in (1, 2, 3) for a in (True, False))


def test_a_step_part_whose_worker_is_lost_in_the_second_round_is_written_again_here():
    # a worker lost while it writes a part's entities (out of memory) leaves the part's topology
    # behind, so the main process writes the part again from it, to the same text
    from kese.s7_write import step_parts
    model = board_model(BOARDS / "six_layer.kicad_pcb")
    part = max(model.boundaries, key=lambda p: step_parts.size(model.boundaries[p]))
    real = step_parts.write_brep

    def lost(w, topo, transform):
        w.write(["#100 = HALF_WRITTEN();"])
        raise MemoryError

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        texts = []
        for name, dies in (("clean", False), ("lost", True)):
            kept, out = tmp / f"{name}.topology", tmp / f"{name}.step"
            count = step_parts.found(part, model.boundaries[part], model.transform, kept)[0]
            if dies:
                step_parts.write_brep = lost
                try:
                    step_parts.written(kept, model.transform, 100, out)
                    raise AssertionError("the lost write did not fail")
                except MemoryError:
                    assert kept.exists()
                finally:
                    step_parts.write_brep = real
            assert step_parts.written(kept, model.transform, 100, out)[1] == count and not kept.exists()
            texts.append(out.read_text(encoding="latin-1"))
        assert texts[0] == texts[1] and "HALF_WRITTEN" not in texts[1]


def copper_keys(pcb):
    """Stage 3's copper of a board, per layer and net and per layer, and its mask, as bytes and the
    grid of every part."""
    def key(g):
        return shapely.to_wkb(g, include_srid=True), tuple(shapely.get_precision(shapely.get_parts(g)).tolist())
    r, _ = run_stages(pcb, resolve)
    return ({l: {n: key(g) for n, g in nets.items()} for l, nets in r.copper.items()},
            {l: key(g) for l, g in r.copper_all.items()}, {s: key(g) for s, g in r.mask.items()})


def test_the_copper_layers_joined_in_processes_are_the_same_to_the_byte():
    # each layer's nets joined, clipped and cut by the holes in a worker of its own, the biggest
    # layer first: the same regions, on the same grid, as in threads, whatever the number of workers
    pcb = BOARDS / "six_layer.kicad_pcb"
    keys, nets = {}, P.Parallel.PROCESS_MIN_NETS
    for workers, least in ((1, 10 ** 12), (3, 10 ** 12), (2, 0), (3, 0)):
        with settings({"Parallel.WORKERS": workers, "Parallel.PROCESS_MIN_COORDINATES": least,
                       "Parallel.PROCESS_MIN_NETS": 0 if least == 0 else nets}):
            keys[workers, least] = copper_keys(pcb)
    first = keys[1, 10 ** 12]
    assert len(first[0]) == 6 and all(k == first for k in keys.values())


if __name__ == "__main__":
    run_tests(__file__)
