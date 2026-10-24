"""The live "running <stage> ... 1m 23s" line in the terminal.

A daemon thread redraws the line once a second from the wall clock, independent of what the
pipeline is doing, so the counter keeps running through the long steps (copper unions, STEP
fusing).  It is only drawn on a real terminal and when Run.SHOW_PROGRESS is on; any
normal log line erases it first (Status.clear) so the output stays clean."""
import sys
import threading
import time


def hms(seconds):
    """Seconds -> '1m 23s'."""
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s:02d}s"


class Status:
    def __init__(self, enabled, stream=None):
        self.stream = stream or sys.stderr
        self.enabled = bool(enabled) and hasattr(self.stream, "isatty") and self.stream.isatty()
        self.stage, self.t0, self.width = "", time.time(), 0
        self._lock = threading.Lock()
        self._stop = threading.Event()
        if self.enabled:
            threading.Thread(target=self._run, name="kese-status", daemon=True).start()

    def _run(self):
        while not self._stop.wait(1.0):
            self.draw()

    def draw(self):
        """Redraw the line in place (carriage return, no newline)."""
        if not self.enabled or not self.stage:
            return
        with self._lock:
            line = f"  running {self.stage} ... {hms(time.time() - self.t0)}"
            self.width = max(self.width, len(line))
            self.stream.write("\r" + line.ljust(self.width))
            self.stream.flush()

    def set(self, stage):
        """Name the current stage; the elapsed time keeps counting from the start of the board."""
        self.stage = stage
        self.draw()

    def clear(self):
        """Erase the line so a normal log line can be printed."""
        if self.enabled and self.width:
            with self._lock:
                self.stream.write("\r" + " " * self.width + "\r")
                self.stream.flush()

    def stop(self):
        self._stop.set()
        self.clear()
        self.enabled = False

    def elapsed(self):
        return time.time() - self.t0
