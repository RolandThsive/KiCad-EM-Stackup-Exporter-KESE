"""One run of one board: what was asked (mode, formats, output root, verify), the live status
line, and the notes and timings every stage adds for report.txt."""
import time
from contextlib import contextmanager
from dataclasses import dataclass, field

from kese.progress import Status
from kese.settings_check import check_settings
from parameters import P, described

MODES = ("simulation", "visual")
VISUAL_FORMATS = {"glb", "obj"}
FORMATS = ("glb", "stl", "obj", "step")


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
        t = time.perf_counter()
        yield
        self.timings.append((name, time.perf_counter() - t))


def start(mode=None, formats=None, out_root=None, overrides=(), verify=None, log=print):
    """The request, checked; None takes the value from parameters/Run_KESE/Run.py (verify: from
    parameters/Run_KESE/Verifier.py).  Raises ValueError."""
    R = P.Run
    P.settle()                                                               # an old name whose value waits for the others
    mode = mode or R.MODE
    formats = formats or R.FILE_FORMAT
    formats = [formats] if isinstance(formats, str) else list(formats)       # "glb" is ["glb"]
    check_request(mode, formats)
    check_settings()
    job = Job(mode=mode, formats=formats, out_root=out_root, overrides=tuple(overrides),
              verify=P.Verifier.VERIFY if verify is None else verify, log=log, status=Status(R.SHOW_PROGRESS))
    for old in sorted({key for key, _ in overrides if key != "PRESET" and P.now(key)}):
        new = P.now(old)
        job.note(f"{old} is now {described(new)}: the value given for {old} is used "
                 + (f"as {new[0]}" if len(new) == 1 else "for each of them"))
    return job


def check_request(mode, formats):
    """The mode and the formats asked for, or ValueError."""
    if mode not in MODES:
        raise ValueError(f"MODE must be 'simulation' or 'visual', not {mode!r}")
    bad = [f for f in formats if f not in FORMATS]
    if bad:
        raise ValueError(f"unknown FILE_FORMAT entries {bad}")
    if mode == "visual" and set(formats) - VISUAL_FORMATS:
        raise ValueError("visual mode is a surface, not solids: FILE_FORMAT may only contain glb / obj "
                         f"(asked for {sorted(set(formats) - VISUAL_FORMATS)})")
