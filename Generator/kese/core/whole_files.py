"""Files written whole or not at all: a write that fails on the way (a full disk, a part that
cannot be written) removes what it left, so no half-written file is left to be opened as if it
were whole."""
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def whole(*paths):
    """The files written in the block are removed when the block raises, then the error goes on."""
    try:
        yield
    except BaseException:
        for p in paths:
            Path(p).unlink(missing_ok=True)
        raise


def remove_if_empty(folder):
    """A folder that a failed run left empty removed, with any empty folders in it (stl/), and its
    parent when that is left empty too (the board's folder of a first run)."""
    folder = Path(folder)
    if not folder.is_dir():
        return
    for d in sorted((p for p in folder.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()
    for d in (folder, folder.parent):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
