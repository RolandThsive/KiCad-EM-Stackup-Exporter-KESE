"""
parameters package - loads every settings file and can write them all out.

    from parameters import P
    P.Run.MODE, P.Copper.VIA_WALL_MM, ...

    P.snapshot()  -> the text written to parameters.txt next to every output
"""
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
}


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
        """P.override('Copper.VIA_WALL_MM', 0.02)  - used by kese --set and by tests."""
        short, name = dotted.split(".", 1)
        mod = getattr(self, short)
        if not hasattr(mod, name):
            raise KeyError(f"parameters/{modname_of(short)}.py has no parameter {name}")
        setattr(mod, name, value)


def modname_of(short):
    return _MODULES[short]


def load():
    ns = {}
    for short, modname in _MODULES.items():
        ns[short] = importlib.import_module(f"parameters.{modname}")
    return _Params(**ns)


P = load()
