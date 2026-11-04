"""Memory handed back to the system after work done at once.  glibc, the C library of most Linux
systems, gives each thread that allocates alongside another a pool (arena) of its own and keeps what
is freed there for that pool: after the visual skin's threads, the main process held a gigabyte more
with 16 threads than with 4 (NE_Delta), which the single-threaded steps that follow could not use.
Elsewhere (Windows, macOS, musl) nothing is done."""
import ctypes
import sys


def _malloc_trim():
    """glibc's malloc_trim, or None where the C library is another."""
    if not sys.platform.startswith("linux"):
        return None
    try:
        return ctypes.CDLL(None).malloc_trim
    except (OSError, AttributeError):
        return None


_MALLOC_TRIM = _malloc_trim()


def give_back_memory():
    """Hand back to the system the memory freed so far, in every thread's pool: tens of milliseconds.
    Called after each step done in threads (kese/core/parallel.py, the visual skin)."""
    if _MALLOC_TRIM is not None:
        _MALLOC_TRIM(0)


def done_then_given_back(work, *args):
    """In a worker process: work(*args), then the memory it freed handed back while the worker waits
    for its next part (simulation mode on NE_Delta: 2.82 GB in all with 4 workers, against 3.25 GB)."""
    try:
        return work(*args)
    finally:
        give_back_memory()
