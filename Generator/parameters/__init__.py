"""
parameters package - loads every settings file and can write them all out.

    from parameters import P
    P.Run.MODE, P.Copper.VIA_WALL_MM, ...

    P.snapshot()  -> the text written to parameters.txt next to every output
"""
import difflib
import importlib
import types

_MODULES = {
    "Run": "run",
    "Board": "board",
    "Copper": "copper",
    "SolderMask": "solder_mask",
    "Silkscreen": "silkscreen",
    "Finish": "finish",
    "Geometry": "geometry",
    "Color": "color",
    "Parallel": "parallel",
}
MOVED = {"Run.WORKERS": "Parallel.WORKERS"}        # a setting's old name (it still works): its name now


class _Params(types.SimpleNamespace):
    def modules(self):
        return {k: getattr(self, k) for k in _MODULES}

    def snapshot(self):
        lines = []
        for short, modname in _MODULES.items():
            mod = getattr(self, short)
            lines.append(f"[parameters/{modname}.py]")
            for name in dir(mod):
                if name.isupper():
                    lines.append(f"{name} = {getattr(mod, name)!r}")
            lines.append("")
        return "\n".join(lines)

    def override(self, dotted, value):
        """P.override('Copper.VIA_WALL_MM', 0.02)  - used by kese --set and by tests.  A name that is
        not a parameter raises a ValueError that says so and names the closest one.  A moved setting
        may still be given by its old name (MOVED)."""
        short, dot, name = dotted.partition(".")
        if dotted in MOVED and not (short in _MODULES and name in self.names(short)):
            short, _, name = MOVED[dotted].partition(".")
        if not (dot and short and name):
            where = [f"{s}.{dotted}" for s in _MODULES if dotted in self.names(s)]
            raise ValueError(f"{dotted} is not Module.NAME" + (f" (did you mean {where[0]}?)" if len(where) == 1 else
                             f"; the modules are {', '.join(_MODULES)}"))
        if short not in _MODULES:
            raise ValueError(f"there is no parameter module {short}{closest(short, _MODULES)}; "
                             f"the modules are {', '.join(_MODULES)}")
        if name not in self.names(short):
            near = closest(name, self.names(short))
            raise ValueError(f"{file_of(short)} has no parameter {name}{near}")
        setattr(getattr(self, short), name, value)

    def names(self, short):
        """The parameters of one module: its names in capitals."""
        return [name for name in dir(getattr(self, short)) if name.isupper()]


def file_of(short):
    """'parameters/run.py' for 'Run'."""
    return f"parameters/{_MODULES[short]}.py"


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
