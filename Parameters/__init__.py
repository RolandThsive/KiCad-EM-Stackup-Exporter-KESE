"""
Parameters package - loads every parameter module and can write them all out.

    from Parameters import P
    P.Run.MODE, P.Copper.VIA_WALL_MM, ...

    P.snapshot()  -> the text written to parameters.txt next to every output
"""
import importlib
import types

_MODULES = {
    "Run": "Run_Parameters",
    "Board": "Board_Parameters",
    "Copper": "Copper_Parameters",
    "SolderMask": "SolderMask_Parameters",
    "Silkscreen": "Silkscreen_Parameters",
    "Finish": "Finish_Parameters",
    "Geometry": "Geometry_Parameters",
    "Color": "Color_Parameters",
}


class _Params(types.SimpleNamespace):
    def modules(self):
        return {k: getattr(self, k) for k in _MODULES}

    def snapshot(self):
        lines = []
        for short, modname in _MODULES.items():
            mod = getattr(self, short)
            lines.append(f"[{modname}]")
            for name in dir(mod):
                if name.isupper():
                    lines.append(f"{name} = {getattr(mod, name)!r}")
            lines.append("")
        return "\n".join(lines)

    def override(self, dotted, value):
        """P.override('Copper.VIA_WALL_MM', 0.02)  - used by run.py --set and by tests."""
        short, name = dotted.split(".", 1)
        mod = getattr(self, short)
        if not hasattr(mod, name):
            raise KeyError(f"{modname_of(short)} has no parameter {name}")
        setattr(mod, name, value)


def modname_of(short):
    return _MODULES[short]


def load():
    ns = {}
    for short, modname in _MODULES.items():
        ns[short] = importlib.import_module(f"Parameters.{modname}")
    return _Params(**ns)


P = load()
