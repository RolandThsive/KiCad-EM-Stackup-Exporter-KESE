"""One run of one board: what was asked (mode, formats, output root, verify), the live status
line, and the notes and timings every stage adds for report.txt."""
import time
from contextlib import contextmanager
from dataclasses import dataclass, field

from kese.progress import Status
from kese.s4_geometry.switches import SWITCHES, is_on
from parameters import P

MODES = ("simulation", "visual")
VISUAL_FORMATS = {"glb", "obj"}
FORMATS = ("glb", "stl", "obj", "step")
# the settings that take one of a few words, and those words (Run.MODE and Run.FILE_FORMAT are checked below)
CHOICES = {
    "Run.UNITS": ("mm", "m"),
    "Run.ORIGIN": ("center", "kicad"),
    "Run.ORIENTATION": ("upright", "flat"),
    "Board.DIELECTRIC_GROUPING": ("layer", "merged"),
    "Board.DEFAULT_DIELECTRIC_TYPE": ("core", "prepreg"),
    "Board.OUTLINE_FALLBACK": ("copper_hull", "error"),
    "Copper.COPPER_GROUPING": ("net", "layer", "merged"),
    "Copper.CASTELLATION": ("auto", "file", "off"),
    "Copper.EDGE_PLATING": ("file", "yes", "no"),
    "Copper.VIA_TENTING": ("file", "tented", "open"),
    "Finish.FINISH_GROUPING": ("metal", "net"),
}


@dataclass
class Job:
    mode: str                                       # "simulation" or "visual"
    formats: list                                   # entries of FORMATS
    out_root: object                                # None: Run.OUTPUT_DIR
    overrides: tuple                                # (key, value) pairs, for parameters.txt
    verify: bool
    log: object                                     # where log lines go (print by default)
    status: Status
    log_lines: list = field(default_factory=list)   # the notes, repeated in report.txt
    timings: list = field(default_factory=list)     # (stage, seconds)

    def say(self, s):
        """A log line; the status line is erased first."""
        self.status.clear()
        self.log(s)

    def note(self, s):
        """A log line that report.txt repeats under "notes"."""
        self.log_lines.append(s)
        self.say("  " + s)

    @contextmanager
    def stage(self, name, status=None):
        """Time the block as stage `name`, showing `status` on the status line."""
        if status:
            self.status.set(status)
        t = time.time()
        yield
        self.timings.append((name, time.time() - t))


def start(mode=None, formats=None, out_root=None, overrides=(), verify=None, log=print):
    """The request, checked; None takes the value from parameters/run.py.  Raises ValueError."""
    R = P.Run
    mode = mode or R.MODE
    formats = formats or R.FILE_FORMAT
    formats = [formats] if isinstance(formats, str) else list(formats)       # "glb" is ["glb"]
    if mode not in MODES:
        raise ValueError(f"MODE must be 'simulation' or 'visual', not {mode!r}")
    bad = [f for f in formats if f not in FORMATS]
    if bad:
        raise ValueError(f"unknown FILE_FORMAT entries {bad}")
    if mode == "visual" and set(formats) - VISUAL_FORMATS:
        raise ValueError("visual mode is a surface, not solids: FILE_FORMAT may only contain glb / obj "
                         f"(asked for {sorted(set(formats) - VISUAL_FORMATS)})")
    for key, words in CHOICES.items():
        module, name = key.split(".")
        value = getattr(getattr(P, module), name)
        if value not in words:
            raise ValueError(f"{key} must be {' or '.join(map(repr, words))}, not {value!r}")
    if type(R.WORKERS) is not int or R.WORKERS < 0:
        raise ValueError(f"Run.WORKERS must be a whole number, 0 or more (0: one per processor thread), not {R.WORKERS!r}")
    if not any(is_on(key) for key in SWITCHES.values()):
        raise ValueError(f"nothing to build: {', '.join(sorted(set(SWITCHES.values())))} are all False")
    return Job(mode=mode, formats=formats, out_root=out_root, overrides=tuple(overrides),
               verify=R.VERIFY if verify is None else verify, log=log, status=Status(R.SHOW_PROGRESS))
