"""The worker processes' life (kese/core/parallel.py starts them): started without the run's main
module, given the run's settings, ended with the main process, and stopped at once with the parts
they are building."""
import multiprocessing
import multiprocessing.connection
import os
import signal
import sys
import threading
import time
import types
from contextlib import contextmanager, suppress

from parameters import P


def stop(pool):
    """End a pool's workers now, with the parts they are building, let the pool go, and wait until
    they are gone (Parallel.WORKER_STOP_WAIT_S at most): then no worker writes a file any more (step_parts.py)."""
    processes = list((getattr(pool, "_processes", None) or {}).values())    # shutdown() forgets them
    if hasattr(pool, "terminate_workers"):            # Python 3.14
        pool.terminate_workers()
    else:
        pool.shutdown(wait=False, cancel_futures=True)
        for process in processes:
            with suppress(ValueError, ProcessLookupError):     # already ended and closed
                if process.is_alive():
                    process.terminate()
    running = []
    for process in processes:
        with suppress(ValueError):                    # closed: ended already
            running.append(process.sentinel)
    end = time.monotonic() + P.Parallel.WORKER_STOP_WAIT_S
    while running and time.monotonic() < end:
        for ended in multiprocessing.connection.wait(running, timeout=end - time.monotonic()):
            running.remove(ended)


@contextmanager
def main_left_out():
    """Processes started in this block do not run this run's main module again.  Spawn runs it in
    every new process (as __mp_main__), for what is sent from it, and nothing is; a script that calls
    KESE without `if __name__ == "__main__":` would run KESE all over again in each of them."""
    main = sys.modules.get("__main__")
    sys.modules["__main__"] = types.ModuleType("__main__")
    try:
        yield
    finally:
        if main is None:
            del sys.modules["__main__"]
        else:
            sys.modules["__main__"] = main


def settings():
    """Every value of the files of parameters/ as this run has it (--for and --set included)."""
    return {f"{short}.{name}": getattr(module, name) for short, module in P.modules().items()
            for name in dir(module) if name.isupper()}


def use_settings(values):
    """A worker process takes the run's settings (it read the files of parameters/ afresh), and stops when the
    main process does, however it stopped.  Ctrl-C ends it at once, without a traceback of its own
    (the main process prints one).  Where memory runs out, Linux's OOM killer takes a worker before
    the main process, which then hands the parts left to fewer workers, or builds them itself: the
    biggest process, the one the killer would take, is most often the main one."""
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    with suppress(OSError), open("/proc/self/oom_score_adj", "w", encoding="ascii") as f:   # no such file: not Linux
        f.write("1000")
    threading.Thread(target=stop_with_parent, name="kese-parent-watch", daemon=True).start()
    for key, value in values.items():
        P.override(key, value)


def stop_with_parent():
    """In a worker: wait for the main process to end, then end too.  A worker whose main process was
    killed (SIGTERM, a closed terminal) would otherwise finish its part and wait for work for ever."""
    parent = multiprocessing.parent_process()
    if parent is not None:
        multiprocessing.connection.wait([parent.sentinel])
        os._exit(1)
