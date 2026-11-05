"""The worker processes and threads of kese/core/parallel.py: a thread's own copies of shapes
(kese/core/shape_copies.py) are the same shapes, made only where GEOS needs them (and on no grid
where the grid is not used: a join of shared regions is the same join), threads share one prepared
copy of a slice's material and one set of joined holes, cut faces only by the pieces of material
that meet them, work in batches of any size with the same
result (the STEP writer's slices too, to the byte, and a STEP file written part by part in worker
processes), and hand back the memory they freed (unless
Parallel.GIVE_BACK_MEMORY is off), Parallel.PROCESS_WORKERS caps the worker processes and boards under
Parallel.PROCESS_MIN_COORDINATES stay in one process, shapes keep their grid (and type and SRID) on the way to and from the workers, the run's settings reach
the workers, a lost worker or one out of memory leaves its jobs to the main process, an error in the
work is raised at once and the other workers are stopped, a caller that stops early does not wait,
the OOM killer takes a worker first, KESE runs inside a multiprocessing.Pool, a script without a
main guard is not run again in the workers, and the workers end with Ctrl-C (one traceback) and
with the main process.

    python -m pytest tests/test_parallel.py          (or:  python tests/test_parallel.py)"""
import os
import platform
import signal
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import shapely

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core import memory, shape_copies  # noqa: E402
from kese.core.boundary import Boundary  # noqa: E402
from kese.core.parallel import in_parallel, in_processes, processes_wanted, workers_wanted, worth_processes  # noqa: E402
from kese.core.shape_copies import _owned, own  # noqa: E402
from kese.s3_resolve.holes import made_once  # noqa: E402
from kese.s6_assemble.skin_faces import cut_away, lies_against_material  # noqa: E402
from kese.s6_assemble.skin_mesh import looks_at_material  # noqa: E402
from kese.s7_write import step  # noqa: E402
from kese.s7_write.step import write_part  # noqa: E402
from kese.s7_write.step_writer import StepWriter  # noqa: E402
from kese.s8_verify.vertical_rays import vertical_hits  # noqa: E402
from parameters import P  # noqa: E402


def with_workers(n, *more):
    """Parallel.WORKERS = n (and more (key, value) settings) for a block; -> the values to put back."""
    saved = [("Parallel.WORKERS", P.Parallel.WORKERS)] + [(k, getattr(getattr(P, k.split(".")[0]), k.split(".")[1])) for k, _ in more]
    for k, v in [("Parallel.WORKERS", n), *more]:
        P.override(k, v)
    return saved


def put_back(saved):
    for k, v in saved:
        P.override(k, v)


def same(shape):
    """In a worker: the shape as it came (copy.copy would rebuild it through shapely's own pickling)."""
    return shape


def snap_grid():
    """In a worker: the grid it builds on."""
    return P.Geometry.SNAP_GRID_MM


def lost_on_3(n, parent):
    """In a worker, job 3 stops its process, as the system does when memory runs out."""
    if n == 3 and os.getpid() != parent:
        os._exit(9)
    return n * n


def fail_or_sleep(n, error):
    """In a worker: job 0 raises `error` at once, the others take 30 s."""
    if n == 0:
        raise error
    time.sleep(30)
    return n


def out_of_memory_on_2(n, parent):
    """In a worker, job 2 runs out of memory (as on Windows, which has no OOM killer)."""
    if n == 2 and os.getpid() != parent:
        raise MemoryError("no memory in a worker")
    return n * n


def oom_score_adj():
    """In a worker: how readily Linux's OOM killer takes it."""
    return int(Path("/proc/self/oom_score_adj").read_text())


def inside_a_pool(n):
    """In a multiprocessing.Pool's worker (a daemon, which may not start processes): in_processes."""
    P.override("Parallel.WORKERS", 2)
    return sorted(in_processes(abs, [(k, (-k,)) for k in range(n)]))


def pid_after_a_while(n):
    """In a worker: its process id, once the other workers have had time to start."""
    time.sleep(0.3)
    return os.getpid()


def quick_or_sleep(n):
    if n:
        time.sleep(30)
    return n


def test_shapes_keep_their_grid_in_worker_processes():
    square = shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5))
    shapes = [shapely.set_precision(square, 1e-4), square, shapely.Polygon(), shapely.GeometryCollection(),
              shapely.set_precision(shapely.MultiPolygon([shapely.box(0, 0, 1, 1), shapely.box(2, 0, 3, 1)]), 1e-4),
              shapely.GeometryCollection([shapely.Point(1, 2), shapely.LineString([(0, 0), (1, 1)])]),
              shapely.set_precision(shapely.Polygon(), 1e-4),          # what a gridded overlay that meets nothing gives
              shapely.set_precision(shapely.LinearRing([(0, 0), (1, 0), (1, 1)]), 1e-4),
              shapely.set_srid(shapely.set_precision(shapely.Point(1, 2), 1e-4), 4326), *collections_of_grids()]
    saved = with_workers(2)
    try:
        back = dict(in_processes(same, [(k, (s,)) for k, s in enumerate(shapes)]))
    finally:
        put_back(saved)
    for k, s in enumerate(shapes):
        assert shapely.to_wkb(back[k]) == shapely.to_wkb(s), k
        assert grids(back[k]) == grids(s), k
        assert type(back[k]) is type(s) and shapely.get_srid(back[k]) == shapely.get_srid(s), k


def collections_of_grids():
    """Collections on no grid of parts on one, as as_region builds them: GEOS grows each part on its own."""
    part = shapely.set_precision(shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5)), 1e-4)
    two = shapely.MultiPolygon([part, shapely.box(2, 0, 3, 1)])
    return [two, shapely.set_srid(shapely.GeometryCollection([two, part, shapely.Point(1, 2)]), 4326)]


def grids(shape):
    """The grid of a shape and, in a collection, those of its parts (at any depth)."""
    if shapely.get_type_id(shape) < 4 or shape.is_empty:
        return float(shapely.get_precision(shape))
    return float(shapely.get_precision(shape)), [grids(p) for p in shapely.get_parts(shape)]


def test_a_thread_s_own_copies_are_the_same_shapes_on_factories_of_their_own():
    square = shapely.set_precision(shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5)), 1e-4)
    shapes = [square, shapely.box(0, 0, 1, 1), shapely.set_precision(shapely.Polygon(), 1e-4),
              shapely.set_precision(shapely.LinearRing([(0, 0), (1, 0), (1, 1)]), 1e-4),
              shapely.set_srid(shapely.set_precision(shapely.Point(1, 2), 1e-4), 4326), *collections_of_grids()]
    copies = _owned({"list": shapes, "tuple": (shapes[0], "net"), "array": np.array(shapes, dtype=object), "n": 3})
    assert copies["n"] == 3 and copies["tuple"][1] == "net" and isinstance(copies["tuple"], tuple)
    for got in (copies["list"], list(copies["array"]), [copies["tuple"][0]]):
        for a, b in zip(shapes, got):
            assert a is not b and type(a) is type(b) and shapely.to_wkb(a) == shapely.to_wkb(b)
            assert grids(a) == grids(b) and shapely.get_srid(a) == shapely.get_srid(b)
            assert shapely.to_wkb(a.buffer(0.01)) == shapely.to_wkb(b.buffer(0.01))     # on the same grids


def test_copies_only_where_geos_needs_them():
    # GEOS 3.15 counts a factory's shapes atomically: there threads may share shapes, and own() is x itself
    assert shape_copies.SHARED_SAFELY == (shapely.geos_version >= (3, 15, 0))
    shapes = [shapely.set_precision(shapely.box(0, 0, 1, 1), 1e-4)]
    saved = shape_copies.SHARED_SAFELY
    try:
        shape_copies.SHARED_SAFELY = True
        assert own(shapes) is shapes
        shape_copies.SHARED_SAFELY = False
        assert own(shapes)[0] is not shapes[0]
    finally:
        shape_copies.SHARED_SAFELY = saved


def test_floating_copies_keep_the_coordinates_on_no_grid():
    # where the grid is not used: polygons through WKB alone (GEOS's default factory, shared safely),
    # anything else an own() copy, each part on its grid
    square = shapely.set_precision(shapely.box(0, 0, 1, 1).difference(shapely.box(0.25, 0.25, 0.5, 0.5)), 1e-4)
    shapes = [square, shapely.MultiPolygon([square, shapely.set_precision(shapely.box(2, 0, 3, 1), 1e-4)]),
              shapely.Polygon(), *collections_of_grids()]
    saved = shape_copies.SHARED_SAFELY
    try:
        shape_copies.SHARED_SAFELY = False
        got = shape_copies.floating(shapes)
    finally:
        shape_copies.SHARED_SAFELY = saved
    for a, b in zip(shapes, got):
        assert a is not b and type(a) is type(b) and shapely.to_wkb(a) == shapely.to_wkb(b)
        if shapely.get_type_id(a) in shape_copies.POLYGONAL:
            assert not shapely.get_precision([b, *shapely.get_parts(b)]).any(), a.geom_type
        else:
            assert grids(b) == grids(a), a.geom_type


def test_a_join_of_shared_regions_is_the_same_join():
    from kese.core.boundary import joined_regions
    on_grid = [shapely.set_precision(shapely.box(*b), 1e-4) for b in ((0, 0, 1, 1), (1, 0, 2, 1), (0.5, 0.5, 1.5, 2))]
    for regions in (on_grid[:2], on_grid):              # a coverage union, and a union of overlapping ones
        for exact in (True, False):
            a, b = joined_regions(regions, exact, shared=True), joined_regions(_owned(regions), exact)
            assert shapely.to_wkb(a) == shapely.to_wkb(b) and grids(a) == grids(b), (len(regions), exact)


def make_and_drop(square, n=3000):
    """In a thread: shapes made from `square` (they share its GEOS factory) and dropped, n times."""
    for _ in range(n):
        a = square.buffer(0.01)
        shapely.get_parts(a)
        a.intersection(shapely.box(1, 1, 5, 5))
    return True


def test_threads_on_their_own_copies_of_one_shape():
    # one shape on a grid, used by every thread: each works on its own copy (with the shared shape
    # itself, GEOS 3.14 can lose its factory's count of shapes and crash)
    shared = shapely.set_precision(shapely.box(0, 0, 10, 10).difference(shapely.box(2, 2, 3, 3)), 1e-4)
    parts = shapely.MultiPolygon([shared, shapely.set_precision(shapely.box(20, 0, 30, 10), 1e-4)])
    saved = with_workers(4)
    try:
        assert in_parallel(lambda k: make_and_drop(own((shared, parts)[k % 2])), range(4)) == [True] * 4
    finally:
        put_back(saved)


def test_threads_share_one_prepared_copy_of_a_slice():
    # a prepared copy for each thread would grow with the number of threads: one per slice, in turns
    material = shapely.set_precision(shapely.box(0, 0, 10, 10).difference(shapely.box(2, 2, 3, 3)), 1e-4)
    slice_ = (None, None, None, material, {"turn": threading.Lock()})
    regions = [shapely.box(k % 9, 4, k % 9 + 1, 5) for k in range(8)] + [shapely.box(1, 1, 4, 4)]
    saved = with_workers(8)
    try:
        got = in_parallel(lambda r: lies_against_material(r, slice_), regions)
    finally:
        put_back(saved)
    assert got == [True] * 8 + [False]
    assert set(slice_[4]) == {"turn", "copy"} and shapely.is_prepared(slice_[4]["copy"])
    assert not shapely.is_prepared(material)


def test_threads_cut_faces_by_the_pieces_that_meet_them_alone():
    # a ring round the face meets its box but not the face, a square over its corner meets both: in
    # every thread the face loses that corner alone, and no shape is left prepared
    grid = 1e-4
    ring = shapely.set_precision(shapely.box(-5, -5, 15, 15).difference(shapely.box(-1, -1, 11, 11)), grid)
    polys = np.array([ring, shapely.set_precision(shapely.box(8, 8, 12, 12), grid)], dtype=object)
    material = (polys, np.array(["a", "b"], dtype=object), shapely.STRtree(polys), shapely.union_all(polys, grid_size=grid),
                {"turn": threading.Lock()})
    faces = [shapely.set_precision(shapely.box(0, 0, 10, 10), grid) for _ in range(16)]
    saved = with_workers(8)
    try:
        got = in_parallel(lambda face: cut_away(face, material), faces)
    finally:
        put_back(saved)
    want = shapely.box(0, 0, 10, 10).difference(shapely.box(8, 8, 10, 10))
    assert all(g.equals(want) for g in got)
    assert not shapely.is_prepared(faces).any() and not shapely.is_prepared(polys).any()


def test_the_probe_test_lets_go_of_its_prepared_slices():
    # one triangle standing in the material: the point just in front of it is inside; then the
    # slice's prepared index is freed, not kept for as long as the slices are
    material = shapely.box(0, 0, 1, 1)
    v = np.array([[0.5, 0.2, 0.4], [0.5, 0.8, 0.4], [0.5, 0.5, 0.6]])
    pieces = [(None, None, None, material, {})]
    assert looks_at_material(v, np.array([[0, 1, 2]]), np.array([0.0, 1.0]), pieces).tolist() == [True]
    assert not shapely.is_prepared(material)


def test_batches_of_any_size_give_the_same_result():
    # the batch sizes of parameters/parallel.py set how much is held at once, not what comes out
    rng = np.random.default_rng(1)
    v, f = rng.random((60, 3)), rng.integers(0, 60, (40, 3))
    material = shapely.box(0.2, 0.2, 0.7, 0.9)
    levels, xy = np.array([0.0, 0.5, 1.0]), rng.random((50, 2))
    def pieces():
        return [(None, None, None, material, {}), (None, None, None, material, {})]
    whole = (looks_at_material(v, f, levels, pieces()), vertical_hits(v, f, xy))
    saved = with_workers(2, ("Parallel.SKIN_PROBES_AT_A_TIME", 7), ("Parallel.VERIFY_TRIANGLES_AT_A_TIME", 3))
    try:
        batched = (looks_at_material(v, f, levels, pieces()), vertical_hits(v, f, xy))
    finally:
        put_back(saved)
    assert whole[0].tolist() == batched[0].tolist() and whole[0].any() and not whole[0].all()
    assert all(np.array_equal(a, b) for a, b in zip(whole[1], batched[1])) and len(whole[1][0])


def step_data(tmp, rows, arcs):
    """The DATA section of a STEP file of one part (a seven-pointed star with a round hole) written
    Parallel.STEP_ROWS_AT_A_TIME = rows at a time, with or without its arcs."""
    t = np.arange(14) * np.pi / 7
    star = shapely.Polygon(np.c_[np.cos(t), np.sin(t)] * np.where(np.arange(14) % 2, 4.0, 10.0)[:, None],
                           [shapely.Point(0.3, 0.2).buffer(1.5, quad_segs=16).exterior.coords])
    region = shapely.MultiPolygon([star, shapely.box(12, 0, 15, 3)])
    part = Boundary("star", [0.0, 1.6], [(0.0, 1.6, region)], [(0.0, region, False), (1.6, region, True)])
    saved = with_workers(1, ("Parallel.STEP_ROWS_AT_A_TIME", rows), ("Step.STEP_EXACT_ARCS", arcs))
    try:
        path = Path(tmp) / f"{rows}_{arcs}.step"
        w = StepWriter(path, "star", "mm")
        w.add_part("star", (205, 128, 62), write_part(w, "star", part, np.diag([0.001, 0.001, 0.001, 1.0]), print))
        text = w.close().read_text(encoding="latin-1")
    finally:
        put_back(saved)
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
    from kese.job import start
    from kese.s1_read import read
    from kese.s2_collect import collect
    from kese.s3_resolve import resolve
    from kese.s4_geometry import geometry
    from kese.s5_materials import materials
    from kese.s6_assemble import assemble
    job = start("simulation", ["step"], None, (), False, lambda s: None)
    out = str(pcb)
    for stage in (read, collect, resolve, geometry, materials, assemble):
        out = stage.run(out, job)
    job.status.stop()
    return out


def test_a_step_file_written_in_processes_is_the_same_to_the_byte():
    # each part's entities counted first, then written in a worker into a file of their own, and
    # the files joined in order: the same file as one written part after part in this process,
    # whatever the number of workers, with arcs and without, and no temporary file left behind
    model = board_model(ROOT / "tests" / "boards" / "six_layer.kicad_pcb")
    with tempfile.TemporaryDirectory() as tmp:
        for arcs in (True, False):
            files = {}
            for workers, least in ((1, 10 ** 12), (2, 0), (3, 0)):
                saved = with_workers(workers, ("Parallel.PROCESS_MIN_COORDINATES", least), ("Step.STEP_EXACT_ARCS", arcs))
                try:
                    path = step.write(model, Path(tmp) / f"{workers}_{arcs}.step", print)
                finally:
                    put_back(saved)
                text = path.read_text(encoding="latin-1")
                files[workers] = text[text.index("\nDATA;"):]
            assert files[1] == files[2] == files[3] and ("CIRCLE(" in files[1]) == arcs, arcs
        assert sorted(p.name for p in Path(tmp).iterdir()) == sorted(f"{w}_{a}.step" for w in (1, 2, 3) for a in (True, False))


def copper_keys(pcb):
    """Stage 3's copper of a board, per layer and net and per layer, and its mask, as bytes and the
    grid of every part."""
    from kese.job import start
    from kese.s1_read import read
    from kese.s2_collect import collect
    from kese.s3_resolve import resolve

    def key(g):
        return shapely.to_wkb(g, include_srid=True), tuple(shapely.get_precision(shapely.get_parts(g)).tolist())
    job = start("simulation", ["glb"], None, (), False, lambda s: None)
    r = resolve.run(collect.run(read.run(str(pcb), job), job), job)
    job.status.stop()
    return ({l: {n: key(g) for n, g in nets.items()} for l, nets in r.copper.items()},
            {l: key(g) for l, g in r.copper_all.items()}, {s: key(g) for s, g in r.mask.items()})


def test_the_copper_layers_joined_in_processes_are_the_same_to_the_byte():
    # each layer's nets joined, clipped and cut by the holes in a worker of its own, the biggest
    # layer first: the same regions, on the same grid, as in threads, whatever the number of workers
    from kese.s3_resolve import copper
    pcb = ROOT / "tests" / "boards" / "six_layer.kicad_pcb"
    keys, nets = {}, copper.PROCESS_MIN_NETS
    for workers, least in ((1, 10 ** 12), (3, 10 ** 12), (2, 0), (3, 0)):
        saved = with_workers(workers, ("Parallel.PROCESS_MIN_COORDINATES", least))
        copper.PROCESS_MIN_NETS = 0 if least == 0 else nets
        try:
            keys[workers, least] = copper_keys(pcb)
        finally:
            put_back(saved)
            copper.PROCESS_MIN_NETS = nets
    first = keys[1, 10 ** 12]
    assert len(first[0]) == 6 and all(k == first for k in keys.values())

def test_joined_holes_are_made_once_when_threads_ask_at_once():
    made = []

    def make():
        time.sleep(0.05)                    # long enough for every thread to ask before it is made
        made.append(1)
        return shapely.box(0, 0, 1, 1)
    r = SimpleNamespace(items=SimpleNamespace(holes=[SimpleNamespace(wall=0.02)] * 3), holes_made={})
    saved = with_workers(8)
    try:
        got = in_parallel(lambda _: made_once(r, "drills", lambda h: True, make), range(8))
    finally:
        put_back(saved)
    assert len(made) == 1 and all(g is got[0] for g in got)


def test_memory_freed_by_threads_is_handed_back():
    # glibc keeps what threads free in a pool per thread: on NE_Delta a gigabyte more at 16 threads
    if sys.platform.startswith("linux") and platform.libc_ver()[0] == "glibc":
        assert memory._MALLOC_TRIM is not None
    calls, saved = [], (memory._MALLOC_TRIM, with_workers(3))
    memory._MALLOC_TRIM = calls.append
    try:
        assert in_parallel(lambda k: k * k, range(4)) == [0, 1, 4, 9]
    finally:
        memory._MALLOC_TRIM = saved[0]
        put_back(saved[1])
    assert calls == [0]
    memory.give_back_memory()                           # and on this system, it runs


def test_memory_is_kept_with_give_back_memory_off():
    calls, saved = [], (memory._MALLOC_TRIM, with_workers(3, ("Parallel.GIVE_BACK_MEMORY", False)))
    memory._MALLOC_TRIM = calls.append
    try:
        assert in_parallel(lambda k: k * k, range(4)) == [0, 1, 4, 9]
        memory.done_then_given_back(abs, -1)
    finally:
        memory._MALLOC_TRIM = saved[0]
        put_back(saved[1])
    assert calls == []


def test_process_workers_caps_the_worker_processes():
    saved = with_workers(4, ("Parallel.PROCESS_WORKERS", 2))
    try:
        assert (workers_wanted(), processes_wanted()) == (4, 2)
        pids = {pid for _, pid in in_processes(pid_after_a_while, [(n, (n,)) for n in range(6)])}
        P.override("Parallel.PROCESS_WORKERS", 8)                      # a cap: never more than WORKERS
        assert processes_wanted() == 4
        P.override("Parallel.PROCESS_WORKERS", 1)                      # stage 6 in this process, threads kept
        assert (workers_wanted(), processes_wanted()) == (4, 1) and not worth_processes(4, 10 ** 6)
    finally:
        put_back(saved)
    assert 0 < len(pids) <= 2 and os.getpid() not in pids, pids


def test_small_boards_stay_in_one_process():
    assert P.Parallel.PROCESS_MIN_COORDINATES == 20_000                  # the default
    saved = with_workers(2, ("Parallel.PROCESS_MIN_COORDINATES", 20_000))
    try:
        assert not worth_processes(4, 19_999) and worth_processes(4, 20_000) and not worth_processes(1, 10 ** 6)
        P.override("Parallel.PROCESS_MIN_COORDINATES", 100)
        assert not worth_processes(4, 99) and worth_processes(4, 100)
        P.override("Parallel.PROCESS_MIN_COORDINATES", 0)              # processes for every board of 2 parts or more
        assert worth_processes(2, 0) and not worth_processes(1, 0)
        P.override("Parallel.WORKERS", 1)                              # 1: everything in this process
        assert not worth_processes(4, 10 ** 6)
    finally:
        put_back(saved)


def test_the_run_s_settings_reach_the_workers():
    saved = with_workers(2, ("Geometry.SNAP_GRID_MM", 0.0002))
    try:
        got = dict(in_processes(snap_grid, [(0, ()), (1, ())]))
    finally:
        put_back(saved)
    assert got == {0: 0.0002, 1: 0.0002}


def test_a_lost_worker_leaves_its_jobs_to_this_process():
    notes = []
    saved = with_workers(2)
    try:
        got = dict(in_processes(lost_on_3, [(n, (n, os.getpid())) for n in range(8)], notes.append))
    finally:
        put_back(saved)
    assert got == {n: n * n for n in range(8)}
    assert len(notes) == 1 and notes[0].startswith("worker processes failed (BrokenProcessPool"), notes


def test_out_of_memory_in_a_worker_leaves_its_job_to_this_process():
    notes = []
    saved = with_workers(2)
    try:
        got = dict(in_processes(out_of_memory_on_2, [(n, (n, os.getpid())) for n in range(6)], notes.append))
    finally:
        put_back(saved)
    assert got == {n: n * n for n in range(6)}
    assert notes == ["worker processes failed (MemoryError: no memory in a worker); the 1 part left is built "
                     "in this process, one after another (most often a lack of memory: fewer processes, "
                     "Parallel.PROCESS_WORKERS, use less)"], notes


def spawned():
    return set(workers_of(os.getpid())) if sys.platform.startswith("linux") else set()


def gone(before):
    """Whether the worker processes started since `before` have ended (within 10 s)."""
    t0 = time.time()
    while any(alive(w) for w in spawned() - before) and time.time() - t0 < 10:
        time.sleep(0.1)
    return not any(alive(w) for w in spawned() - before)


def test_an_error_in_the_work_is_raised_at_once_and_not_taken_for_lost_processes():
    for error in (ValueError("a bug in the work"), FileNotFoundError(2, "No such file", "/nowhere")):
        notes, before, raised = [], spawned(), None
        saved = with_workers(4)
        t0 = time.time()
        try:
            list(in_processes(fail_or_sleep, [(n, (n, error)) for n in range(4)], notes.append))
        except type(error) as e:
            raised = e
        finally:
            put_back(saved)
        assert str(raised) == str(error) and time.time() - t0 < 15, (raised, time.time() - t0)
        assert notes == [], notes                    # not built again here
        # ended before the error is raised: a worker writing a file writes no more (step_parts.py)
        assert not any(alive(w) for w in spawned() - before), "the workers building the other parts were not stopped"


def test_a_caller_that_stops_early_does_not_wait():
    before = spawned()
    saved = with_workers(3)
    t0 = time.time()
    try:
        results = in_processes(quick_or_sleep, [(n, (n,)) for n in range(3)])
        assert next(results) == (0, 0)
        results.close()
    finally:
        put_back(saved)
    assert time.time() - t0 < 15, time.time() - t0
    assert gone(before)


def test_the_oom_killer_takes_a_worker_first():
    if not sys.platform.startswith("linux"):
        return
    saved = with_workers(2)
    try:
        got = dict(in_processes(oom_score_adj, [(0, ()), (1, ())]))
    finally:
        put_back(saved)
    assert got == {0: 1000, 1: 1000}


def test_inside_a_multiprocessing_pool():
    import multiprocessing
    with multiprocessing.get_context("spawn").Pool(1) as pool:
        assert pool.apply(inside_a_pool, (4,)) == [(0, 0), (1, 1), (2, 2), (3, 3)]


def test_no_jobs():
    assert list(in_processes(abs, [])) == []


def run_script(tmp_path, body, stderr=subprocess.STDOUT):
    script = tmp_path / "script.py"
    script.write_text(textwrap.dedent(f"""\
        import sys
        sys.path.insert(0, {str(ROOT)!r})
        from kese.core.parallel import in_processes
        from parameters import P
        P.override("Parallel.WORKERS", 2)
        print("top-level code", flush=True)
        """) + textwrap.dedent(body))
    return subprocess.Popen([sys.executable, str(script)], stdout=subprocess.PIPE, stderr=stderr, text=True,
                            cwd=tmp_path)


def test_a_script_without_a_main_guard_is_not_run_again_in_the_workers(tmp_path):
    p = run_script(tmp_path, 'print(sorted(in_processes(abs, [(k, (-k,)) for k in range(4)])), flush=True)\n')
    out, _ = p.communicate(timeout=120)
    assert p.returncode == 0, out
    assert out.count("top-level code") == 1, out
    assert "[(0, 0), (1, 1), (2, 2), (3, 3)]" in out, out


def workers_of(pid):
    """The pids of the worker processes a process started (Linux)."""
    out = []
    for d in Path("/proc").iterdir():
        try:
            if d.name.isdigit() and int((d / "stat").read_text().rsplit(")", 1)[1].split()[1]) == pid \
                    and b"spawn_main" in (d / "cmdline").read_bytes():
                out.append(int(d.name))
        except (OSError, ValueError):
            pass
    return out


def alive(pid):
    """Whether a process runs (a zombie, ended but not yet reaped, does not)."""
    try:
        return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0] != "Z"
    except OSError:
        return False


def test_ctrl_c_stops_the_workers_with_one_traceback(tmp_path):
    if not sys.platform.startswith("linux"):
        return
    script = tmp_path / "script.py"
    script.write_text(textwrap.dedent(f"""\
        import sys, time
        sys.path.insert(0, {str(ROOT)!r})
        from kese.core.parallel import in_processes
        from parameters import P
        if __name__ == "__main__":
            P.override("Parallel.WORKERS", 3)                # the first worker done waits for work
            list(in_processes(time.sleep, [(0, (0,)), (1, (60,)), (2, (60,))]))
        """))
    p = subprocess.Popen([sys.executable, str(script)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         start_new_session=True)
    try:
        t0 = time.time()
        while len(workers := workers_of(p.pid)) < 3 and time.time() - t0 < 60:
            time.sleep(0.1)
        time.sleep(1)
        os.killpg(p.pid, signal.SIGINT)                      # Ctrl-C reaches every process of the terminal's group
        out, _ = p.communicate(timeout=20)
    finally:
        p.kill()
    assert out.count("Traceback") == 1 and "KeyboardInterrupt" in out and "Process Spawn" not in out, out
    assert not [w for w in workers if alive(w)], workers


def test_the_workers_end_with_the_main_process(tmp_path):
    if not sys.platform.startswith("linux"):
        return                                               # reads /proc
    # killed, the script leaves its semaphores to multiprocessing's resource tracker, which says so on stderr
    p = run_script(tmp_path, """\
        import time
        if __name__ == "__main__":
            list(in_processes(time.sleep, [(0, (60,)), (1, (60,))]))
        """, stderr=subprocess.DEVNULL)
    try:
        t0 = time.time()
        while len(workers := workers_of(p.pid)) < 2 and time.time() - t0 < 60:
            time.sleep(0.1)
        assert len(workers) == 2, workers
        time.sleep(1)                                        # the workers have started their jobs
        os.kill(p.pid, signal.SIGKILL)
        p.wait()
        t0 = time.time()
        while any(alive(w) for w in workers) and time.time() - t0 < 20:
            time.sleep(0.1)
        left = [w for w in workers if alive(w)]
    finally:
        p.kill()
    for w in left:
        os.kill(w, signal.SIGKILL)
    assert not left, f"workers {left} still running {time.time() - t0:.0f} s after the main process was killed"


if __name__ == "__main__":
    import test_parallel as t        # the workers find the jobs' functions in a module, not in __main__
    t.test_shapes_keep_their_grid_in_worker_processes()
    t.test_a_thread_s_own_copies_are_the_same_shapes_on_factories_of_their_own()
    t.test_copies_only_where_geos_needs_them()
    t.test_floating_copies_keep_the_coordinates_on_no_grid()
    t.test_a_join_of_shared_regions_is_the_same_join()
    t.test_threads_on_their_own_copies_of_one_shape()
    t.test_threads_share_one_prepared_copy_of_a_slice()
    t.test_threads_cut_faces_by_the_pieces_that_meet_them_alone()
    t.test_the_probe_test_lets_go_of_its_prepared_slices()
    t.test_batches_of_any_size_give_the_same_result()
    t.test_a_step_part_is_written_the_same_in_slices_of_any_size()
    t.test_a_step_file_written_in_processes_is_the_same_to_the_byte()
    t.test_the_copper_layers_joined_in_processes_are_the_same_to_the_byte()
    t.test_joined_holes_are_made_once_when_threads_ask_at_once()
    t.test_memory_freed_by_threads_is_handed_back()
    t.test_memory_is_kept_with_give_back_memory_off()
    t.test_process_workers_caps_the_worker_processes()
    t.test_small_boards_stay_in_one_process()
    t.test_the_run_s_settings_reach_the_workers()
    t.test_a_lost_worker_leaves_its_jobs_to_this_process()
    t.test_out_of_memory_in_a_worker_leaves_its_job_to_this_process()
    t.test_an_error_in_the_work_is_raised_at_once_and_not_taken_for_lost_processes()
    t.test_a_caller_that_stops_early_does_not_wait()
    t.test_the_oom_killer_takes_a_worker_first()
    t.test_inside_a_multiprocessing_pool()
    t.test_no_jobs()
    with tempfile.TemporaryDirectory() as d:
        t.test_a_script_without_a_main_guard_is_not_run_again_in_the_workers(Path(d))
        t.test_ctrl_c_stops_the_workers_with_one_traceback(Path(d))
        t.test_the_workers_end_with_the_main_process(Path(d))
    print("ok")
