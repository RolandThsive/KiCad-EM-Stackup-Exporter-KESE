"""A disk that fills up while the files are written: no half-written file is left behind, the
files written whole before it stay as they are, the error is the system's own (a clean-up that
fails too does not hide it), and a run folder left empty is removed; and two runs started together
each get a folder of their own.  The disk is made full by letting the files opened for writing in a
temporary folder take only so many bytes in all.  Takes a few seconds.

    python -m pytest tests/test_full_disk.py           (or:  python tests/test_full_disk.py)"""
import builtins
import errno
import io
import re
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.core.whole_files import remove_if_empty, whole  # noqa: E402
from kese.job import start  # noqa: E402
from kese.s1_read import read  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s3_resolve import resolve  # noqa: E402
from kese.s4_geometry import geometry  # noqa: E402
from kese.s5_materials import materials  # noqa: E402
from kese.s6_assemble import assemble  # noqa: E402
from kese.s7_write import write  # noqa: E402
from kese.s7_write.output_folder import new_folder  # noqa: E402
from kese.s9_report.report import write_parameters  # noqa: E402

PCB = ROOT / "tests" / "boards" / "six_layer.kicad_pcb"
FORMATS = ["glb", "obj", "stl", "step"]


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


def model_and_job(out_root):
    job = start("simulation", FORMATS, str(out_root), (), False, lambda s: None)
    out = str(PCB)
    for stage in (read, collect, resolve, geometry, materials, assemble):
        out = stage.run(out, job)
    return out, job


def files_in(folder):
    """{name: bytes}, the time in a STEP file's header left out (a file written a second later)."""
    return {p.relative_to(folder).as_posix(): re.sub(rb"FILE_NAME\('[^']*','[^']*'", b"FILE_NAME(", p.read_bytes(), count=1)
            for p in sorted(folder.rglob("*")) if p.is_file()}


def written(model, folder):
    files = write.write(model, folder, FORMATS, lambda s: None, lambda s: None)
    return [p.relative_to(folder).as_posix() for p in files.written]


def test_a_full_disk_leaves_only_whole_files():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        model, job = model_and_job(tmp)
        job.status.stop()
        (tmp / "whole").mkdir()
        with disk_with_room(tmp / "whole") as taken:
            written(model, tmp / "whole")
        whole = files_in(tmp / "whole")
        order = list(taken)                                    # every file, in the order it was written
        assert set(order) == set(whole) and {"six_layer.glb", "six_layer.obj", "six_layer.mtl", "six_layer.step",
                                             "materials.json"} <= set(order) and len(order) > 6, order
        for k, name in enumerate(order):     # the disk full half-way through each file in turn, and at its last byte
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
                before = set(order[:k]) - ({"six_layer.obj"} if name == "six_layer.mtl" else set())  # an OBJ goes with its MTL
                assert set(left) == before, (name, room, sorted(set(left) ^ before))
                for n, data in left.items():
                    assert data == whole[n], f"{n}: not as it is when the disk has room"


def test_a_run_whose_first_file_does_not_fit_leaves_no_folder():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        model, job = model_and_job(tmp / "runs")
        try:
            with disk_with_room(tmp, 100):
                write.run(model, job)
        except OSError as e:
            assert e.errno == errno.ENOSPC, e
        else:
            raise AssertionError("the write did not fail with the disk full")
        finally:
            job.status.stop()
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
    test_a_full_disk_leaves_only_whole_files()
    test_a_run_whose_first_file_does_not_fit_leaves_no_folder()
    test_the_settings_file_that_does_not_fit_is_not_left_half_written()
    test_only_empty_folders_are_removed()
    test_a_clean_up_that_fails_does_not_hide_the_error()
    test_two_runs_started_together_get_a_folder_each()
    print("ok")
