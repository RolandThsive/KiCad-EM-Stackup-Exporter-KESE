"""One run of one board: what was asked (mode, formats, output root, verify), the live status
line, and the notes and timings every stage adds for report.txt."""
import numbers
import time
from contextlib import contextmanager
from dataclasses import dataclass, field

from kese.progress import Status
from kese.s4_geometry.switches import SWITCHES, is_on
from parameters import KINDS, MOVED, P, file_of

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
ONE_OR_MORE = ("Geometry.PINCH_CUT_ROUNDS", "Geometry.VERTEX_SHARING_ROUNDS", "Geometry.NODING_ROUNDS",   # at 0 nothing
               "Parallel.SKIN_PROBES_AT_A_TIME", "Parallel.VERIFY_TRIANGLES_AT_A_TIME", "Parallel.STEP_ROWS_AT_A_TIME",
               "Verifier.VERIFY_RAYS")                                                                 # (or no test)
AT_LEAST = {**dict.fromkeys(ONE_OR_MORE, 1), "Step.STEP_ARC_MIN_POINTS": 3}     # three points make a circle
KIND_WORDS = {bool: "True or False", int: "a number", float: "a number", str: "text, in quotes",
              list: "a list", dict: "a dict"}
NUMBER_AT_LEAST = {"Verifier.VERIFY_VOLUME_TOLERANCE": 0, "Verifier.VERIFY_OPENED_VOLUME_MM3": 0,
                   "Finish.FINISH_MITRE_LIMIT": 1}     # a corner cut nearer than its thickness would thin the finish
MORE_THAN_ZERO = ("Step.STEP_ARC_MAX_SWEEP_DEG",)      # arcs are cut in pieces of at most this
WHOLE_NUMBERS = {                 # the settings of parameters/parallel.py that count, and what their 0 means
    "WORKERS": "one per processor thread",
    "PROCESS_WORKERS": "as many as WORKERS",
    "PROCESS_MIN_COORDINATES": "processes for every board of more than one part",
}


def of_kind(value, kind):
    """Whether a setting's value is of the kind its file gives it: a number for a number (a whole one
    or not, never True or False), a list or tuple for a list."""
    if kind in (int, float):
        return isinstance(value, numbers.Real) and not isinstance(value, bool)
    return isinstance(value, (list, tuple)) if kind is list else type(value) is kind


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
    """The request, checked; None takes the value from parameters/run.py (verify: from
    parameters/verifier.py).  Raises ValueError."""
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
    left = [(old, new) for old, new in MOVED.items() if hasattr(getattr(P, old.split(".")[0]), old.split(".")[1])]
    if left:                                                                # in a parameter file kept through an update
        raise ValueError("; ".join(f"{file_of(old.split('.')[0])} sets {old.split('.')[1]}, which is now {new} in "
                                   f"{file_of(new.split('.')[0])}" for old, new in left)
                         + (": set it there" if len(left) == 1 else ": set them there"))
    for name, zero in WHOLE_NUMBERS.items():
        value = getattr(P.Parallel, name)
        if type(value) is not int or value < 0:
            raise ValueError(f"Parallel.{name} must be a whole number, 0 or more (0: {zero}), not {value!r}")
    for key, least in AT_LEAST.items():
        value = getattr(getattr(P, key.split(".")[0]), key.split(".")[1])
        if type(value) is not int or value < least:
            raise ValueError(f"{key} must be a whole number, {least} or more, not {value!r}")
    for key, least in NUMBER_AT_LEAST.items():
        value = getattr(getattr(P, key.split(".")[0]), key.split(".")[1])
        if type(value) not in (int, float) or not value >= least:
            raise ValueError(f"{key} must be a number, {least} or more, not {value!r}")
    for key in MORE_THAN_ZERO:
        value = getattr(getattr(P, key.split(".")[0]), key.split(".")[1])
        if type(value) not in (int, float) or not value > 0:
            raise ValueError(f"{key} must be a number more than 0, not {value!r}")
    for key, kind in KINDS.items():                       # every other setting: of the kind its file gives it
        value = getattr(getattr(P, key.split(".")[0]), key.split(".")[1], None)
        if kind in KIND_WORDS and key != "Run.FILE_FORMAT" and not of_kind(value, kind):
            raise ValueError(f"{key} must be {KIND_WORDS[kind]}, not {value!r}")
    if not any(is_on(key) for key in SWITCHES.values()):
        raise ValueError(f"nothing to build: {', '.join(sorted(set(SWITCHES.values())))} are all False")
    job = Job(mode=mode, formats=formats, out_root=out_root, overrides=tuple(overrides),
              verify=P.Verifier.VERIFY if verify is None else verify, log=log, status=Status(R.SHOW_PROGRESS))
    for old in sorted({key for key, _ in overrides} & MOVED.keys()):
        job.note(f"{old} is now {MOVED[old]} ({file_of(MOVED[old].split('.')[0])}): the value given "
                 f"for {old} is used as {MOVED[old]}")
    return job
