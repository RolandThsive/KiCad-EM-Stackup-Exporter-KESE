"""Files written whole or not at all: a write that fails on the way (a full disk, a part that
cannot be written) removes what it left, so no half-written file is left to be opened as if it
were whole.  The clean-up never hides the error that called for it: what cannot be removed is left."""
from contextlib import contextmanager, suppress
from pathlib import Path


@contextmanager
def whole(*paths):
    """The files written in the block are removed when the block raises, then the error goes on."""
    try:
        yield
    except BaseException:
        for p in paths:
            with suppress(OSError):
                Path(p).unlink(missing_ok=True)
        raise


def remove_if_empty(folder):
    """A folder that a failed run left empty removed, with any empty folders in it (stl/), and its
    parent when that is left empty too (the board's folder of a first run).  Only empty folders go:
    rmdir refuses one with anything in it, so a folder another run puts something in meanwhile is
    left, as is one that cannot be removed."""
    folder = Path(folder)
    if not folder.is_dir():
        return
    try:
        inside = sorted((p for p in folder.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True)
    except OSError:
        inside = []
    for d in [*inside, folder, folder.parent]:
        with suppress(OSError):
            d.rmdir()
