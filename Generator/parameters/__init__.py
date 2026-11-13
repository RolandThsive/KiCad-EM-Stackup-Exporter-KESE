"""
parameters package - loads every settings file and can write them all out.

    from parameters import P
    P.Run.MODE, P.Copper.VIA_WALL_MM, P.Stackup.FUSION_BUILD, ...

    P.value("Run.MODE")            -> a setting by its "Module.NAME"
    P.value("Stackup.top_finish")  -> a line of the stack-up being built: True or False
    P.building()                   -> the stack-up being built: {line: True / False}
    P.snapshot()                   -> the text written to parameters.txt next to every output

The files are in three folders, and a setting's Module is its file's name without ".py":
    PCB_elements/   what the board is made of: Stackup.py (what is built) and one file per element
    Run_KESE/       how KESE runs: Run.py, Geometry.py, Parallel.py, Verifier.py, Presets.py
    Fileformats/    the files KESE writes: Step.py, Mesh.py
"""
import difflib
import importlib
import types
from pathlib import Path

_FOLDERS = {
    "PCB_elements": ("Stackup", "Board", "Copper", "Finish", "SolderMask", "SilkScreen"),
    "Run_KESE": ("Run", "Geometry", "Parallel", "Verifier", "Presets"),
    "Fileformats": ("Step", "Mesh"),
}
# short name (P.<name>, and the Module of --set Module.NAME=value): its file under parameters/
_MODULES = {name: f"{folder}.{name}" for folder, names in _FOLDERS.items() for name in names}
STACKUPS = ("PLIES_FUSED", "PLIES_SEPARATE")          # the two stack-ups of PCB_elements/Stackup.py
_TOP = ("top_silkscreen", "top_solder_mask", "top_finish", "top_copper")
_BOTTOM = ("bottom_copper", "bottom_finish", "bottom_solder_mask", "bottom_silkscreen")
_THROUGH = ("plated_holes", "hole_finish", "via_resin")
# the lines each stack-up must have, no more and no fewer (a line missing or misspelt in the file is refused)
LINES = {"PLIES_FUSED": (*_TOP, "board", "resin_between_traces", "inner_copper", *_BOTTOM, *_THROUGH),
         "PLIES_SEPARATE": (*_TOP, "prepreg_plies", "resin_between_traces", "inner_copper", "cores", *_BOTTOM, *_THROUGH)}
# a short name for several lines of a stack-up: --set Stackup.solder_mask=True sets both sides
GROUPS = {
    "silkscreen": ("top_silkscreen", "bottom_silkscreen"),
    "solder_mask": ("top_solder_mask", "bottom_solder_mask"),
    "finish": ("top_finish", "bottom_finish", "hole_finish"),
    "copper": ("top_copper", "inner_copper", "bottom_copper", "plated_holes"),
}

# a module's old name (it still works in --set and in a preset): its name now
OLD_MODULES = {"Silkscreen": "SilkScreen"}
# a setting's old name (it still works in --set and in a preset): its name now, or its names where
# one old setting is now several.  "Stackup.top_finish" is that line of both stack-ups.
MOVED = {
    # before 25.2
    "Run.WORKERS": ("Parallel.WORKERS",),
    **{f"Run.{name}": (f"Step.{name}",) for name in ("STEP_EXACT_ARCS", "STEP_ARC_FIT_TOLERANCE_MM", "STEP_ARC_MIN_POINTS",
                                                     "STEP_ARC_MIN_SWEEP_DEG", "STEP_ARC_MAX_TURN_DEG")},
    **{f"Run.{name}": (f"Verifier.{name}",) for name in ("VERIFY", "VERIFY_RAYS", "VERIFY_VOLUME_TOLERANCE",
                                                         "VERIFY_OPENED_VOLUME_MM3")},
    "Run.PRESETS": ("Presets.PRESETS",),
    # 25.2: the mesh settings of Run.py are Fileformats/Mesh.py
    **{f"Run.{name}": (f"Mesh.{name}",) for name in ("EXPORT_INCLUDE_NORMALS", "EXPORT_SET_BUFFERVIEW_TARGETS",
                                                     "SMOOTH_SHADE_ANGLE_DEG")},
    # 25.2: the part switches are lines of PCB_elements/Stackup.py
    "Silkscreen.SILKSCREEN_ENABLED": ("Stackup.top_silkscreen", "Stackup.bottom_silkscreen"),
    "SolderMask.SOLDER_MASK_ENABLED": ("Stackup.top_solder_mask", "Stackup.bottom_solder_mask"),
    "Finish.FINISH_ENABLED": ("Stackup.top_finish", "Stackup.bottom_finish", "Stackup.hole_finish"),
    "Copper.COPPER_ENABLED": ("Stackup.top_copper", "Stackup.inner_copper", "Stackup.bottom_copper", "Stackup.plated_holes"),
    "Copper.VIA_RESIN_ENABLED": ("Stackup.via_resin",),
    "Board.BOARD_ENABLED": ("Stackup.board", "Stackup.prepreg_plies", "Stackup.cores"),
    "Board.RESIN_FILL_BETWEEN_INNER_COPPER": ("Stackup.resin_between_traces",),
    # 25.2: color.py is gone, every colour is in its element's file
    "Color.VISUAL_MASK_OPAQUE": ("SolderMask.VISUAL_MASK_OPAQUE",),
    "Color.USE_STACKUP_COLORS": ("SolderMask.USE_STACKUP_MASK_COLOR", "SilkScreen.USE_STACKUP_SILK_COLOR"),
    "Color.STACKUP_MASK_COLORS": ("SolderMask.STACKUP_MASK_COLORS",),
    "Color.STACKUP_MASK_OVER_COPPER_COLORS": ("SolderMask.STACKUP_MASK_OVER_COPPER_COLORS",),
    "Color.USER_MASK_OVER_COPPER_LIGHTEN": ("SolderMask.USER_MASK_OVER_COPPER_LIGHTEN",),
    "Color.STACKUP_SILK_COLORS": ("SilkScreen.STACKUP_SILK_COLORS",),
    # 25.2: the copper by top, inner and bottom
    "Copper.DEFAULT_OUTER_FOIL_MM": ("Copper.DEFAULT_TOP_FOIL_MM", "Copper.DEFAULT_BOTTOM_FOIL_MM"),
    "Copper.OUTER_PLATING_ADDED_MM": ("Copper.TOP_PLATING_ADDED_MM", "Copper.BOTTOM_PLATING_ADDED_MM"),
    "Copper.ETCH_FACTOR": ("Copper.TOP_ETCH_FACTOR", "Copper.BOTTOM_ETCH_FACTOR"),
    "Copper.COPPER_SURFACE_ROUGHNESS_UM": ("Copper.COPPER_ROUGHNESS_RMS_TREATED_UM", "Copper.COPPER_ROUGHNESS_RMS_OTHER_UM"),
    # 25.2: tenting is the mask over a via
    "Copper.VIA_TENTING": ("SolderMask.VIA_TENTING",),
}
# old settings with no single new name: what to set now
GONE = {
    "Color.MATERIALS": "every colour is now a setting of its own in its element's file: Board.CORE_COLOR, "
                       "Board.PREPREG_COLOR, Board.BOARD_COLOR, Copper.COPPER_COLOR, Copper.PLATING_COLOR, "
                       "Copper.EXPOSED_COPPER_COLOR, Copper.VIA_RESIN_COLOR, Finish.FINISH_COLORS, "
                       "SolderMask.TOP_MASK_COLOR, SolderMask.BOTTOM_MASK_COLOR, SolderMask.TOP_MASK_OVER_COPPER_COLOR, "
                       "SolderMask.BOTTOM_MASK_OVER_COPPER_COLOR, SilkScreen.TOP_SILK_COLOR, SilkScreen.BOTTOM_SILK_COLOR",
}
INNER_ETCH = "Copper.ETCH_APPLY_TO_INNER_LAYERS"      # old: True gives the inner copper the top's etch factor
# the parameter files of before 25.2, which lay in parameters/ itself: where each one's settings are now
OLD_FILES = {"board": "PCB_elements/Board.py", "color": "the element files of PCB_elements/ (each has a Color section)",
             "copper": "PCB_elements/Copper.py", "finish": "PCB_elements/Finish.py", "geometry": "Run_KESE/Geometry.py",
             "parallel": "Run_KESE/Parallel.py", "presets": "Run_KESE/Presets.py", "run": "Run_KESE/Run.py",
             "silkscreen": "PCB_elements/SilkScreen.py", "solder_mask": "PCB_elements/SolderMask.py",
             "step": "Fileformats/Step.py", "verifier": "Run_KESE/Verifier.py"}


class _Params(types.SimpleNamespace):
    def modules(self):
        return {k: getattr(self, k) for k in _MODULES}

    def snapshot(self):
        lines = []
        for short in _MODULES:
            mod = getattr(self, short)
            lines.append(f"[{file_of(short)}]")
            lines += [f"{name} = {getattr(mod, name)!r}" for name in self.names(short)]
            lines.append("")
        return "\n".join(lines)

    def building(self):
        """The stack-up being built: {line: True / False}, the one Stackup.FUSION_BUILD names."""
        return getattr(self.Stackup, self.Stackup.FUSION_BUILD)

    def lines(self):
        """Every line either stack-up has, in the files' order."""
        return list(dict.fromkeys(e for s in STACKUPS for e in LINES[s]))

    def override(self, dotted, value):
        """P.override('Copper.VIA_WALL_MM', 0.02)  - used by kese --set and by tests.  A name that is
        not a parameter raises a ValueError that says so and names the closest one.  A moved setting
        may still be given by its old name (MOVED, OLD_MODULES).  'Stackup.top_finish' sets that line
        of both stack-ups, and 'Stackup.finish' every line of that group (GROUPS)."""
        short, dot, name = dotted.partition(".")
        of_stackup = short == "Stackup" and (name in self.lines() or name in GROUPS)
        known = short in _MODULES and (name in self.names(short) or of_stackup)
        if not known:
            if dotted in MOVED:
                for new in MOVED[dotted]:
                    self.override(new, value)
                return
            if dotted == INNER_ETCH:
                self.inner_etch_as_top = value                          # settled once every override is in (settle)
                return
            if dotted in GONE:
                raise ValueError(f"{dotted} is no longer a parameter: {GONE[dotted]}")
            if short in OLD_MODULES and dot:
                return self.override(f"{OLD_MODULES[short]}.{name}", value)
        if not (dot and short and name):
            where = [f"{s}.{dotted}" for s in _MODULES if dotted in self.names(s)]
            raise ValueError(f"{dotted} is not Module.NAME" + (f" (did you mean {where[0]}?)" if len(where) == 1 else
                             f"; the modules are {', '.join(_MODULES)}"))
        if short not in _MODULES:
            raise ValueError(f"there is no parameter module {short}{closest(short, _MODULES)}; "
                             f"the modules are {', '.join(_MODULES)}")
        if of_stackup:
            for line in GROUPS.get(name, (name,)):
                for stackup in STACKUPS:
                    if line in LINES[stackup] and isinstance(getattr(self.Stackup, stackup), dict):
                        getattr(self.Stackup, stackup)[line] = value
            return
        if name not in self.names(short):
            near = (closest(name, self.names(short) + (self.lines() + list(GROUPS) if short == "Stackup" else []))
                    or self.elsewhere(name, short))
            raise ValueError(f"{file_of(short)} has no parameter {name}{near}")
        setattr(getattr(self, short), name, value)

    def settle(self):
        """After every override: the old Copper.ETCH_APPLY_TO_INNER_LAYERS, where it was given."""
        given = getattr(self, "inner_etch_as_top", None)
        if given is not None:
            self.Copper.INNER_ETCH_FACTOR = self.Copper.TOP_ETCH_FACTOR if given is True else 0.0
            self.inner_etch_as_top = None

    def now(self, dotted):
        """The names a setting given by an old name has now, as a tuple, or None for a name of today."""
        short, _, name = dotted.partition(".")
        if short in _MODULES and (name in self.names(short) or (short == "Stackup" and name in self.lines() + list(GROUPS))):
            return None
        if dotted in MOVED:
            return MOVED[dotted]
        if dotted == INNER_ETCH:
            return ("Copper.INNER_ETCH_FACTOR",)
        return (f"{OLD_MODULES[short]}.{name}",) if short in OLD_MODULES and name else None

    def elsewhere(self, name, short):
        """' (did you mean Module.NAME?)' for the name closest to `name` in the other modules, or ''
        (Run.WORKER finds Parallel.WORKERS)."""
        others = {n.upper(): f"{s}.{n}" for s in reversed(list(_MODULES)) if s != short for n in self.names(s)}
        near = difflib.get_close_matches(name.upper(), list(others), n=1, cutoff=0.6)
        return f" (did you mean {others[near[0]]}?)" if near else ""

    def value(self, dotted, *default):
        """The value of the setting "Module.NAME" (`default`, if given, where its module has none);
        "Stackup.<line>" is that line of the stack-up being built (False where it has no such line)."""
        short, name = dotted.split(".")
        if short == "Stackup" and name in self.lines():
            return self.building().get(name, False)
        if short == "Stackup" and name in GROUPS:                      # a short name: whether all its lines are built
            return all(self.building().get(line, False) for line in GROUPS[name])
        return getattr(getattr(self, short), name, *default)

    def names(self, short):
        """The parameters of one module: its names in capitals."""
        return [name for name in dir(getattr(self, short)) if name.isupper()]


def file_of(short):
    """'parameters/Run_KESE/Run.py' for 'Run'."""
    return f"parameters/{_MODULES[short].replace('.', '/')}.py"


def described(names):
    """Settings in words: 'Copper.TOP_ETCH_FACTOR and Copper.BOTTOM_ETCH_FACTOR (parameters/PCB_elements/Copper.py)',
    or for lines of the stack-ups 'the lines "top_finish" and "bottom_finish" of parameters/PCB_elements/Stackup.py'."""
    def listed(words):
        return words[0] if len(words) == 1 else f"{', '.join(words[:-1])} and {words[-1]}"
    lines = [f'"{n.split(".")[1]}"' for n in names if n.startswith("Stackup.") and not n.split(".")[1].isupper()]
    if lines:
        return f"the line{'s' if len(lines) > 1 else ''} {listed(lines)} of {file_of('Stackup')}"
    return f"{listed(list(names))} ({', '.join(dict.fromkeys(file_of(n.split('.')[0]) for n in names))})"


def old_files_left():
    """[(old file, where its settings are now)] for every parameter file of before 25.2 that still
    lies in parameters/ itself: it is not read any more, so a value edited there would do nothing."""
    here = Path(__file__).parent
    return [(f"parameters/{old}.py", new if new.startswith("the ") else f"parameters/{new}")
            for old, new in OLD_FILES.items() if (here / f"{old}.py").is_file()]


def closest(word, words):
    """' (did you mean X?)' for the one of `words` closest to `word`, case aside, or ''."""
    by_case = {w.upper(): w for w in words}
    near = difflib.get_close_matches(word.upper(), list(by_case), n=1, cutoff=0.6)
    return f" (did you mean {by_case[near[0]]}?)" if near else ""


def load():
    ns = {}
    for short, modname in _MODULES.items():
        ns[short] = importlib.import_module(f"parameters.{modname}")
    return _Params(**ns)


P = load()
# the kind of value each setting has in its file, before any --set: a new value must be of the same
# kind (job.start checks it), so that --set X=false, which gives the word "false", is not taken as true.
# Every line of a stack-up is True or False.
KINDS = {**{f"{s}.{n}": type(getattr(getattr(P, s), n)) for s in _MODULES for n in P.names(s)},
         **{f"Stackup.{e}": bool for e in P.lines()}}
