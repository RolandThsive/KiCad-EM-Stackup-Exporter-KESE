"""Layout rules of kese/ (CONTRIBUTING.md explains them): what may import what, model/ holds data
only, one run() per stage, no import cycles, short files, lowercase names (but the parameter
files, named as their modules), and no code outside Generator/.  Reads the source; no board is run, so it takes a second.

    python -m pytest tests/test_layout.py        (or:  python tests/test_layout.py)"""
import ast
import os
import re
from pathlib import Path

from helpers import ROOT, run_tests

KESE = ROOT / "kese"
MAX_LINES = 200
# every way a board file differs by KiCad version, kept in one file on purpose (its docstring says why)
VERSION_FILE = KESE / "s1_read" / "parse_kicad_version.py"
LONGER = {VERSION_FILE: 500}
FORMAT_NUMBER = range(19_000_000, 21_000_000)      # a KiCad format date, (version 20240108)
RELEASE_NAME = re.compile(r"\bKiCad\s*[<>=]*\s*\d")
STAGE = re.compile(r"s(\d+)_[a-z0-9_]+")
LOWERCASE = re.compile(r"[a-z][a-z0-9_]*|__init__")
CAMELCASE = re.compile(r"[A-Z][A-Za-z0-9]*")


def modules():
    """{dotted name: path} of every .py file in kese/."""
    out = {}
    for p in sorted(KESE.rglob("*.py")):
        parts = p.relative_to(ROOT).with_suffix("").parts
        out[".".join(parts[:-1] if parts[-1] == "__init__" else parts)] = p
    return out


def imports(path, mods):
    """The kese and parameters modules one file imports; `from package import name` counts as the
    module package.name when there is one."""
    out = set()
    for node in ast.walk(tree(path)):
        if isinstance(node, ast.Import):
            out |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            out |= {f"{node.module}.{a.name}" if f"{node.module}.{a.name}" in mods else node.module for a in node.names}
    return {m for m in out if m.split(".")[0] in ("kese", "parameters")}


def area(mod):
    """'parameters', 'core', 'model', the stage number, or 'top' (kese/*.py)."""
    parts = mod.split(".")
    if parts[0] == "parameters":
        return "parameters"
    if len(parts) > 1 and parts[1] in ("core", "model"):
        return parts[1]
    m = STAGE.fullmatch(parts[1]) if len(parts) > 1 else None
    return int(m.group(1)) if m else "top"


def allowed(src, dst):
    if src == "top":
        return True                               # pipeline, job, cli, progress
    if src == "model":
        return dst == "model"
    if src == "core":
        return dst in ("core", "parameters")
    return dst in ("core", "model", "parameters") or (isinstance(dst, int) and dst <= src)


def stages():
    """{number: folder} of the stage folders s1_read ... s9_report."""
    return {int(STAGE.fullmatch(d.name).group(1)): d for d in sorted(KESE.iterdir()) if d.is_dir() and STAGE.fullmatch(d.name)}


def rel(path):
    return path.relative_to(ROOT).as_posix()


def tree(path):
    return ast.parse(path.read_text(encoding="utf-8"))


def test_imports_follow_the_layers():
    """Stages import core/, model/, parameters/ and earlier stages; core/ imports core/ and
    parameters/; model/ imports only model/."""
    mods = modules()
    bad = [f"{rel(path)} imports {dst}" for mod, path in mods.items()
           for dst in sorted(imports(path, mods)) if not allowed(area(mod), area(dst))]
    assert not bad, "\n".join(bad)


def test_model_holds_data_only():
    """model/ is data classes in CamelCase (methods allowed), no free functions or other code."""
    bad = []
    for path in sorted((KESE / "model").glob("*.py")):
        for node in tree(path).body:
            if isinstance(node, (ast.Import, ast.ImportFrom)) or (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)):
                continue
            names = {d.id if isinstance(d, ast.Name) else getattr(getattr(d, "func", None), "id", "")
                     for d in getattr(node, "decorator_list", [])}
            if not (isinstance(node, ast.ClassDef) and "dataclass" in names):
                bad.append(f"{rel(path)}:{node.lineno} is not a dataclass")
            elif not CAMELCASE.fullmatch(node.name):
                bad.append(f"{rel(path)}:{node.lineno} {node.name} is not CamelCase")
    assert not bad, "\n".join(bad)


def test_stages_are_numbered_one_after_another():
    numbers = sorted(stages())
    assert numbers == list(range(1, len(numbers) + 1)), f"stage folders are numbered {numbers}"


def test_one_run_per_stage_and_the_pipeline_runs_them_in_order():
    entry = []
    for _, folder in sorted(stages().items()):
        runs = [p for p in sorted(folder.glob("*.py"))
                if any(isinstance(f, ast.FunctionDef) and f.name == "run" for f in tree(p).body)]
        assert len(runs) == 1, f"{rel(folder)}: run() in {[rel(p) for p in runs] or 'no file'}"
        entry.append(f"kese.{folder.name}.{runs[0].stem}")
    body = tree(KESE / "pipeline.py").body
    names = {a.asname or a.name: f"{node.module}.{a.name}" for node in body if isinstance(node, ast.ImportFrom) for a in node.names}
    listed = next(node.value for node in body if isinstance(node, ast.Assign) and node.targets[0].id == "STAGES")
    got = [names[e.id] for e in listed.elts]
    assert got == entry, f"kese/pipeline.py STAGES runs {got}; the stage folders, in order, are {entry}"


def test_no_import_cycles_inside_a_stage():
    mods = modules()
    for _, folder in sorted(stages().items()):
        own = {m: p for m, p in mods.items() if m.startswith(f"kese.{folder.name}.")}
        graph = {m: imports(p, mods) & own.keys() for m, p in own.items()}
        done, path = set(), []

        def visit(m):
            assert m not in path, f"import cycle: {' -> '.join(path[path.index(m):] + [m])}"
            if m in done:
                return
            path.append(m)
            for d in sorted(graph[m]):
                visit(d)
            path.pop()
            done.add(m)

        for m in sorted(graph):
            visit(m)


def test_files_are_short():
    long = [f"{rel(p)}: {n} lines" for p in sorted(KESE.rglob("*.py"))
            if (n := len(p.read_text(encoding="utf-8").splitlines())) > LONGER.get(p, MAX_LINES)]
    assert not long, f"over {MAX_LINES} lines (split by concern):\n" + "\n".join(long)


def docstrings(t):
    """The ids of the docstring constants of a parsed file (comments are not in the tree at all)."""
    out = set()
    for node in ast.walk(t):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
            out.add(id(body[0].value))
    return out


def test_version_checks_stay_in_parse_kicad_version():
    """Only s1_read/parse_kicad_version.py looks at which KiCad wrote the file: no other file reads a
    .version, the dialect's format or release, or the (version ...) token, holds a format number
    (20240108), or names a KiCad release in its code.  Comments and docstrings may."""
    bad = []
    for p in sorted(KESE.rglob("*.py")):
        if p == VERSION_FILE:
            continue
        t = tree(p)
        doc = docstrings(t)
        for node in ast.walk(t):
            where = f"{rel(p)}:{getattr(node, 'lineno', '?')}"
            if isinstance(node, ast.Attribute):
                if node.attr == "version" or (node.attr in ("format", "release", "stated")
                                              and "dialect" in ast.unparse(node.value)):
                    bad.append(f"{where} reads {ast.unparse(node)}")
            elif isinstance(node, ast.Call) and any(isinstance(a, ast.Constant) and a.value == "version" for a in node.args):
                bad.append(f"{where} reads the (version) token: {ast.unparse(node)}")
            elif isinstance(node, ast.Constant) and id(node) not in doc:
                if isinstance(node.value, int) and not isinstance(node.value, bool) and node.value in FORMAT_NUMBER:
                    bad.append(f"{where} holds the format number {node.value}")
                elif isinstance(node.value, str) and RELEASE_NAME.search(node.value):
                    bad.append(f"{where} names a KiCad release in code: {node.value!r}")
    assert not bad, "version checks outside s1_read/parse_kicad_version.py:\n" + "\n".join(bad)


def test_names_are_lowercase():
    paths = [p for top in ("kese", "tests") for p in sorted((ROOT / top).rglob("*"))
             if (p.suffix == ".py" or (p.is_dir() and (p / "__init__.py").exists())) and "__pycache__" not in p.parts]
    bad = [rel(p) for p in paths if not LOWERCASE.fullmatch(p.stem if p.is_file() else p.name)]
    assert not bad, "\n".join(bad)


def test_the_parameter_files_are_named_as_their_modules():
    """parameters/ is the one place with capitals: its three folders (PCB_elements, Run_KESE,
    Fileformats) hold one file per module, named as the module is (Copper.py is P.Copper, the Module
    of --set Copper.NAME=value), and nothing else lies there: a parameter file anywhere else would
    not be read."""
    import parameters
    listed = {f"parameters/{folder}/{name}.py" for folder, names in parameters._FOLDERS.items() for name in names}
    listed |= {f"parameters/{folder}/__init__.py" for folder in parameters._FOLDERS} | {"parameters/__init__.py"}
    found = {rel(p) for p in (ROOT / "parameters").rglob("*.py")}
    assert found == listed, f"not a parameter file: {sorted(found - listed)}; missing: {sorted(listed - found)}"
    names = [name for names in parameters._FOLDERS.values() for name in names]
    assert all(CAMELCASE.fullmatch(name) for name in names) and len(set(names)) == len(names), names
    assert set(parameters.P.modules()) == set(names)


def test_kese_stays_in_generator():
    """Every Python and TOML file of the repository is inside Generator/; the root and its other
    folders hold the repository's own files (README, licences, docs, workflows, test boards)."""
    repo = ROOT.parent
    if not (repo / ".git").exists():
        return                                    # Generator/ on its own, outside a checkout
    bad = []
    for top, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if not d.startswith(".") and Path(top, d) != ROOT]
        bad += [Path(top, f).relative_to(repo).as_posix() for f in files if Path(f).suffix in (".py", ".toml")]
    assert not bad, "outside Generator/:\n" + "\n".join(sorted(bad))


if __name__ == "__main__":
    run_tests(__file__)
