"""A disk that fills up while the files are written: no half-written file is left behind, the
files written whole before it stay as they are (nor are the files a big board's STEP parts are
written into on the way), the error is the system's own (a clean-up that fails too does not hide
it), and a run folder left empty is removed; and two runs started together each get a folder of
their own.  The disk is made full by letting the files opened for writing in a temporary folder
take only so many bytes in all.  Takes about fifteen seconds.

    python -m pytest tests/test_full_disk.py           (or:  python tests/test_full_disk.py)"""
import builtins
import errno
import io
import re
import tempfile
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path

from helpers import BOARDS, run_stages, run_tests, settings
from kese.core import parallel
from kese.core.whole_files import remove_if_empty, whole
from kese.s6_assemble import assemble
from kese.s7_write import write
from kese.s7_write.output_folder import new_folder
from kese.s9_report.report import write_parameters

PCB = BOARDS / "six_layer.kicad_pcb"
FORMATS = ["glb", "obj", "stl", "step"]
PARTS = ".six_layer.step.parts/"            # where a big board's STEP parts are written on their own
# the disk full in the first round (the topologies kept), the second (the parts' text) and the join
FILLED = {PARTS + "0.topology", PARTS + "1.topology", PARTS + "0.step", PARTS + "1.step", "six_layer.step"}


class Full:
    """A file that takes what is written to it until the disk's room is spent, then fails as a
    full disk does.  `taken` counts what each file took, in the order the files were opened."""

    def __init__(self, f, name, room, taken):
        self.f, self.name, self.room, self.taken, self.full = f, name, room, taken, False
        taken.setdefault(name, 0)

    def write(self, data):
        piece = data if isinstance(data, str) else memoryview(data).cast("B")
        if len(piece) > self.room[0]:
            self.f.write(piece[:self.room[0]])
            self.taken[self.name] += self.room[0]
            self.room[0], self.full = 0, True
            raise OSError(errno.ENOSPC, "No space left on device")
        self.room[0] -= len(piece)
        self.taken[self.name] += len(piece)
        return self.f.write(data)

    def close(self):
        """Closed; once the disk is full, closing fails too, as the flush of what is left in the
        buffer does."""
        self.f.close()
        if self.full:
            raise OSError(errno.ENOSPC, "No space left on device")

    def __getattr__(self, name):
        return getattr(self.f, name)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


@contextmanager
def disk_with_room(folder, room=float("inf")):
    """Files opened for writing in `folder` take `room` bytes (or characters, in a text file) in all.
    -> {file name relative to folder: what it took}, filled as the files are written."""
    real, left, taken = io.open, [room], {}
    folder = Path(folder).resolve()

    def opened(file, mode="r", *args, **kwargs):
        f = real(file, mode, *args, **kwargs)
        if not isinstance(file, (str, Path)) or not any(m in mode for m in "wax"):
            return f
        path = Path(file).resolve()
        return Full(f, path.relative_to(folder).as_posix(), left, taken) if path.is_relative_to(folder) else f

    builtins.open = io.open = opened
    try:
        yield taken
    finally:
        builtins.open = io.open = real


def files_in(folder):
    """{name: bytes}, the time in a STEP file's header left out (a file written a second later)."""
    return {p.relative_to(folder).as_posix(): re.sub(rb"FILE_NAME\('[^']*','[^']*'", b"FILE_NAME(", p.read_bytes(), count=1)
            for p in sorted(folder.rglob("*")) if p.is_file()}


def written(model, folder):
    files = write.write(model, folder, FORMATS, lambda s: None, lambda s: None)
    return [p.relative_to(folder).as_posix() for p in files.written]


def test_a_full_disk_leaves_only_whole_files():
    full_disk_leaves_only_whole_files(lambda name: True)


def test_a_full_disk_while_the_step_parts_are_written_leaves_only_whole_files():
    # a big board's STEP parts are written each into a file of its own, then joined (step_parts.py):
    # here in this process, where the disk is made full (the worker processes are kept from starting)
    real = parallel.ProcessPoolExecutor
    parallel.ProcessPoolExecutor = no_processes
    try:
        with settings({"Parallel.WORKERS": 2, "Parallel.PROCESS_MIN_COORDINATES": 0}):
            full_disk_leaves_only_whole_files(lambda name: name in FILLED, PARTS)
    finally:
        parallel.ProcessPoolExecutor = real


def no_processes(*args, **kwargs):
    raise OSError("no processes here")


def full_disk_leaves_only_whole_files(filled, passing=None):
    """The disk full in each file `filled` takes in turn; `passing`: the folder of the files that are
    written and removed again on the way."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        model, _ = run_stages(PCB, assemble, formats=FORMATS, out_root=str(tmp))
        (tmp / "whole").mkdir()
        with disk_with_room(tmp / "whole") as taken:
            written(model, tmp / "whole")
        complete = files_in(tmp / "whole")
        order = list(taken)                                    # every file, in the order it was written
        gone = {name for name in order if passing and name.startswith(passing)}
        assert set(order) - gone == set(complete) and {"six_layer.glb", "six_layer.obj", "six_layer.mtl", "six_layer.step",
                                                    "materials.json"} <= set(order) and len(order) > 6, order
        assert bool(gone) == bool(passing), gone
        for k, name in enumerate(order):     # the disk full half-way through each file in turn, and at its last byte
            if not filled(name):
                continue
            for room in (taken[name] // 2, taken[name] - 1):  # (a STEP file's assembly and end, written as it closes)
                folder = tmp / f"full_{k}_{room}"
                folder.mkdir()
                try:
                    with disk_with_room(folder, sum(taken[n] for n in order[:k]) + room):
                        written(model, folder)
                except OSError as e:
                    assert e.errno == errno.ENOSPC, e
                else:
                    raise AssertionError(f"{name}: the write did not fail with the disk full")
                left = files_in(folder)
                before = (set(order[:k]) - gone - ({"six_layer.obj"} if name == "six_layer.mtl" else set())   # an OBJ goes with
                          - ({"six_layer.step"} if name in gone else set()))      # its MTL, the STEP file with its parts
                assert set(left) == before, (name, room, sorted(set(left) ^ before))
                for n, data in left.items():
                    assert data == complete[n], f"{n}: not as it is when the disk has room"


def test_a_run_whose_first_file_does_not_fit_leaves_no_folder():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        model, job = run_stages(PCB, assemble, formats=FORMATS, out_root=str(tmp / "runs"))
        try:
            with disk_with_room(tmp, 100):
                write.run(model, job)
        except OSError as e:
            assert e.errno == errno.ENOSPC, e
        else:
            raise AssertionError("the write did not fail with the disk full")
        assert not (tmp / "runs" / "six_layer").exists(), sorted(p.as_posix() for p in tmp.rglob("*"))
        assert (tmp / "runs").is_dir()                         # the folder asked for is kept


def test_the_settings_file_that_does_not_fit_is_not_left_half_written():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "parameters.txt"
        try:
            with disk_with_room(tmp, 1000):
                write_parameters(path, [("Run.MODE", "simulation")])
        except OSError as e:
            assert e.errno == errno.ENOSPC, e
        else:
            raise AssertionError("the write did not fail with the disk full")
        assert not path.exists()


def test_only_empty_folders_are_removed():
    with tempfile.TemporaryDirectory() as tmp:
        run = Path(tmp) / "board" / "simulation_GLB"
        (run / "stl").mkdir(parents=True)
        (Path(tmp) / "board" / "visual_GLB").mkdir()
        remove_if_empty(run)
        assert not run.exists() and (Path(tmp) / "board").is_dir()   # another run of the board is there
        run = Path(tmp) / "other" / "simulation_STL"
        (run / "stl").mkdir(parents=True)
        (run / "stl" / "a.stl").write_bytes(b"x")
        remove_if_empty(run)
        assert (run / "stl" / "a.stl").is_file()


def test_a_clean_up_that_fails_does_not_hide_the_error():
    """The full disk is the error that comes out, even when the half-written file cannot be removed
    (a folder made read-only meanwhile) and the folders cannot be either."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "board" / "simulation_GLB" / "board.glb"
        path.parent.mkdir(parents=True)
        unlink, rmdir = Path.unlink, Path.rmdir

        def refused(self, *args, **kwargs):
            raise PermissionError(errno.EACCES, "Permission denied", str(self))
        Path.unlink = Path.rmdir = refused
        try:
            with whole(path), open(path, "wb") as f:
                f.write(b"half")
                raise OSError(errno.ENOSPC, "No space left on device")
        except OSError as e:
            assert e.errno == errno.ENOSPC, e
        else:
            raise AssertionError("the error did not come out")
        finally:
            remove_if_empty(path.parent)                       # refused too: no error of its own
            Path.unlink, Path.rmdir = unlink, rmdir


def test_two_runs_started_together_get_a_folder_each():
    """Another run makes the folder between this run's look and its making of it: this run takes the
    next name instead of stopping (looked at as if the folder were free, then made); and sixteen at
    once, in threads, get sixteen folders."""
    with tempfile.TemporaryDirectory() as tmp:
        first = new_folder(tmp, "board", "simulation", ["glb"])
        exists = Path.exists
        Path.exists = lambda self, *args, **kwargs: False      # every look says free
        try:
            second = new_folder(tmp, "board", "simulation", ["glb"])
        finally:
            Path.exists = exists
        assert (first.name, second.name) == ("simulation_GLB", "simulation_GLB__1"), (first, second)
        with ThreadPoolExecutor(16) as pool:
            made = list(pool.map(lambda _: new_folder(tmp, "board", "visual", ["glb", "obj"]), range(16)))
        assert len(set(made)) == 16 and all(p.is_dir() for p in made), sorted(p.name for p in made)


if __name__ == "__main__":
    run_tests(__file__)
