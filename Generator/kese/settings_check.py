"""The settings of a run, checked before any work: every setting of the kind and in the range it
takes, the two stack-ups of parameters/PCB_elements/Stackup.py with exactly their own lines, and
no setting or parameter file left where it was before."""
import numbers

from parameters import INNER_ETCH, KINDS, LINES, MOVED, STACKUPS, P, closest, described, file_of, old_files_left

# the settings that take one of a few words, and those words (Run.MODE and Run.FILE_FORMAT are checked in job.py)
CHOICES = {
    "Stackup.FUSION_BUILD": STACKUPS,
    "Run.UNITS": ("mm", "m"),
    "Run.ORIGIN": ("center", "kicad"),
    "Run.ORIENTATION": ("upright", "flat"),
    "Board.DIELECTRIC_GROUPING": ("layer", "merged"),
    "Board.DEFAULT_DIELECTRIC_TYPE": ("core", "prepreg"),
    "Board.OUTLINE_FALLBACK": ("copper_hull", "error"),
    "Board.FUSED_PROPERTIES": ("first", "series"),
    "Board.DIELECTRIC_MODEL": ("constant", "djordjevic_sarkar", "table"),
    "Copper.COPPER_GROUPING": ("net", "layer", "merged"),
    "Copper.CASTELLATION": ("auto", "file", "off"),
    "Copper.EDGE_PLATING": ("file", "yes", "no"),
    "Copper.VIA_PROTECTION": ("file", "off"),
    "Copper.VIA_FILL": ("copper", "resin"),
    "Copper.COPPER_ROUGHNESS_MODEL": ("none", "hammerstad", "huray"),
    "SolderMask.VIA_TENTING": ("file", "tented", "open"),
    "Finish.FINISH_GROUPING": ("metal", "net"),
}
ONE_OR_MORE = ("Geometry.PINCH_CUT_ROUNDS", "Geometry.VERTEX_SHARING_ROUNDS", "Geometry.NODING_ROUNDS",   # at 0 nothing
               "Parallel.SKIN_PROBES_AT_A_TIME", "Parallel.SKIN_PROBES_PER_SHARE", "Parallel.VERIFY_TRIANGLES_AT_A_TIME",
               "Parallel.STEP_ROWS_AT_A_TIME",
               "Verifier.VERIFY_RAYS",                                                                 # (or no test)
               "Geometry.AIR_TILE_VERTICES", "Geometry.FINISH_BORES_AT_A_TIME", "Parallel.VERIFY_POLYGONS_PER_THREAD",
               "Parallel.VERIFY_GROUPS_PER_WORKER")
ZERO_OR_MORE = ("Geometry.HEIGHT_DIGITS", "Geometry.REACH_MARGIN_STEPS", "Geometry.AIR_NEAR_MARGIN_STEPS",
                "Geometry.AIR_TILE_DEPTH", "Geometry.SKIN_FEW_PIECES", "Geometry.SKIN_BIG_PIECE_COORDINATES",
                "Parallel.PROCESS_MIN_NETS", "Verifier.VERIFY_MERGE_EXTRA_DIGITS")
AT_LEAST = {**dict.fromkeys(ZERO_OR_MORE, 0), **dict.fromkeys(ONE_OR_MORE, 1),
            "Step.STEP_ARC_MIN_POINTS": 3,                        # three points make a circle
            "Geometry.PINCH_DISC_SIDES": 3, "Geometry.ELLIPSE_MIN_SEGMENTS": 3}
KIND_WORDS = {bool: "True or False", int: "a number", float: "a number", str: "text, in quotes",
              list: "a list", dict: "a dict"}
NUMBER_AT_LEAST = {"Verifier.VERIFY_VOLUME_TOLERANCE": 0, "Verifier.VERIFY_OPENED_VOLUME_MM3": 0,
                   "Verifier.VERIFY_GONE_AREA_MM2": 0,
                   "Verifier.VERIFY_VOLUME_NOISE_MM3": 0, "Step.STEP_TANGENT_MM": 0, "Step.STEP_ARC_CHECK_FACTOR": 0,
                   "Parallel.WORKER_STOP_WAIT_S": 0, "Copper.VIA_RESIN_EPSILON_R": 1, "Copper.VIA_RESIN_LOSS_TANGENT": 0,
                   "Finish.FINISH_MITRE_LIMIT": 1,     # a corner cut nearer than its thickness would thin the finish
                   "Board.PLY_MIN_THICKNESS_MM": 0, "Board.DEFAULT_EPSILON_R": 1, "Board.DEFAULT_LOSS_TANGENT": 0,
                   "SolderMask.MASK_EPSILON_R": 1, "SolderMask.MASK_LOSS_TANGENT": 0,
                   "SilkScreen.SILK_EPSILON_R": 1, "SilkScreen.SILK_LOSS_TANGENT": 0,
                   **dict.fromkeys((f"Copper.{name}" for name in (
                       "TOP_ETCH_FACTOR", "INNER_ETCH_FACTOR", "BOTTOM_ETCH_FACTOR", "TOP_PLATING_ADDED_MM",
                       "BOTTOM_PLATING_ADDED_MM", "COPPER_ROUGHNESS_RMS_TREATED_UM", "COPPER_ROUGHNESS_RMS_OTHER_UM",
                       "COPPER_HURAY_RADIUS_TREATED_UM", "COPPER_HURAY_RADIUS_OTHER_UM",
                       "COPPER_HURAY_SURFACE_RATIO_TREATED", "COPPER_HURAY_SURFACE_RATIO_OTHER")), 0)}
OR_NONE = {"Board.RESIN_EPSILON_R": 1, "Board.RESIN_LOSS_TANGENT": 0,     # None: the value of the ply the resin flowed from
           "Board.BOARD_THICKNESS_MM": 0, "SolderMask.MASK_MIN_WIDTH_MM": 0}    # None: what the board file says
NONE_OR = {"SolderMask.PAD_TO_MASK_CLEARANCE_MM": float, "SilkScreen.FONT_FILE": str}    # None, or a value of this kind
MORE_THAN_ZERO = ("Step.STEP_ARC_MAX_SWEEP_DEG", "Step.STEP_STRIP_MAX_TURN_DEG",   # arcs are cut in pieces of at most this
                  "Geometry.SMOOTH_FACET_AREA_DIVISOR", "Board.COUNTERSINK_STEP_TOLERANCE_MM",
                  "Board.DEFAULT_SPEC_FREQUENCY_HZ", "Board.DS_LOW_FREQUENCY_HZ", "Board.DS_HIGH_FREQUENCY_HZ",
                  "Copper.DEFAULT_TOP_FOIL_MM", "Copper.DEFAULT_INNER_FOIL_MM", "Copper.DEFAULT_BOTTOM_FOIL_MM")
SHARES = ("Copper.VIA_PLUG_DEPTH_FRACTION",)       # a share of something: more than 0, at most 1
WHOLE_NUMBERS = {                 # the settings of parameters/Run_KESE/Parallel.py that count, and what their 0 means
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


def number(value):
    return type(value) in (int, float)


def check_settings():
    """Every setting of the kind and in the range it takes, the stack-ups whole, and no setting or
    file left under its old name; or ValueError, for the first that is not."""
    for key, words in CHOICES.items():
        value = P.value(key)
        if value not in words:
            raise ValueError(f"{key} must be {' or '.join(map(repr, words))}, not {value!r}")
    check_stackups()
    check_moved()
    for name, zero in WHOLE_NUMBERS.items():
        value = getattr(P.Parallel, name)
        if type(value) is not int or value < 0:
            raise ValueError(f"Parallel.{name} must be a whole number, 0 or more (0: {zero}), not {value!r}")
    for key, least in AT_LEAST.items():
        value = P.value(key)
        if type(value) is not int or value < least:
            raise ValueError(f"{key} must be a whole number, {least} or more, not {value!r}")
    for key, least in NUMBER_AT_LEAST.items():
        value = P.value(key)
        if not number(value) or not value >= least:
            raise ValueError(f"{key} must be a number, {least} or more, not {value!r}")
    for key, least in OR_NONE.items():
        value = P.value(key)
        if value is not None and (not number(value) or not value >= least):
            raise ValueError(f"{key} must be a number, {least} or more, or None, not {value!r}")
    for key in MORE_THAN_ZERO:
        value = P.value(key)
        if not number(value) or not value > 0:
            raise ValueError(f"{key} must be a number more than 0, not {value!r}")
    for key in SHARES:
        value = P.value(key)
        if not number(value) or not 0 < value <= 1:
            raise ValueError(f"{key} must be a number more than 0 and at most 1, not {value!r}")
    check_table()
    for key, kind in {**KINDS, **NONE_OR}.items():        # every other setting: of the kind its file gives it
        value = P.value(key, None)
        if kind in KIND_WORDS and key not in ("Run.FILE_FORMAT", *OR_NONE) and not of_kind(value, kind) \
                and not (key in NONE_OR and value is None):
            raise ValueError(f"{key} must be {KIND_WORDS[kind]}{', or None' * (key in NONE_OR)}, not {value!r}")


def check_stackups():
    """Both stack-ups of Stackup.py: a dict with exactly its own lines, each True or False, and at
    least one line of the stack-up being built True."""
    for name in STACKUPS:
        stackup = getattr(P.Stackup, name)
        if type(stackup) is not dict:
            raise ValueError(f"Stackup.{name} must be a dict, not {stackup!r}")
        for line in stackup:
            if line not in LINES[name]:
                raise ValueError(f"{file_of('Stackup')}: {name} has the line {line!r}, which is not one of its "
                                 f"lines{closest(str(line), LINES[name])}; they are {', '.join(LINES[name])}")
        for line in LINES[name]:
            if line not in stackup:
                raise ValueError(f"{file_of('Stackup')}: {name} has no line {line!r}; every line must be there, "
                                 "True or False")
            if type(stackup[line]) is not bool:
                raise ValueError(f"Stackup.{line} must be True or False, not {stackup[line]!r}")
    if not any(P.building().values()):
        raise ValueError(f"nothing to build: every line of {P.Stackup.FUSION_BUILD} is False ({file_of('Stackup')})")


def check_moved():
    """No setting left under its old name in a parameter file, and no parameter file left where the
    files were before: a value edited there would do nothing."""
    left = [(f"{file_of(old.split('.')[0])} sets {old.split('.')[1]}", new) for old, new in
            {**MOVED, INNER_ETCH: ("Copper.INNER_ETCH_FACTOR",)}.items()
            if old.split(".")[0] in P.modules() and hasattr(getattr(P, old.split(".")[0]), old.split(".")[1])]
    if left:                                                                # in a parameter file kept through an update
        raise ValueError("; ".join(f"{what}, which is now {described(new)}" for what, new in left)
                         + (": set it there" if len(left) == 1 and len(left[0][1]) == 1 else ": set them there"))
    old = old_files_left()
    if old:
        raise ValueError("; ".join(f"{path} is not read any more: its settings are now in {new}" for path, new in old)
                         + ": move your values there and delete " + ("it" if len(old) == 1 else "them"))


def check_table():
    """Board.DIELECTRIC_TABLE: rows of (frequency Hz, er, tan d) by rising frequency, and not empty
    where Board.DIELECTRIC_MODEL asks for it."""
    table = P.Board.DIELECTRIC_TABLE
    rows = list(table) if isinstance(table, (list, tuple)) else None
    good = rows is not None and all(isinstance(row, (list, tuple)) and len(row) == 3 and all(map(number, row))
                                    and row[0] > 0 and row[1] >= 1 and row[2] >= 0 for row in rows)
    if not good or any(a[0] >= b[0] for a, b in zip(rows, rows[1:])):
        raise ValueError("Board.DIELECTRIC_TABLE must be rows of (frequency in Hz, er, tan d) by rising frequency, "
                         f"not {table!r}")
    if P.Board.DIELECTRIC_MODEL == "table" and not rows:
        raise ValueError("Board.DIELECTRIC_MODEL is 'table' but Board.DIELECTRIC_TABLE is empty: give it rows of "
                         "(frequency in Hz, er, tan d)")
