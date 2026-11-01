"""
WebGenerator.py - the web tool's way into KESE (runs inside the browser, in Pyodide).

It does what `kese --set ...` does, without changing KESE:
  1. every parameter comes from Generator/parameters/*.py itself: its name, its default, the comment above it
     (the help text) and, where the comment lists them, its choices.  Nothing about a parameter is written here.
  2. a run resets the parameter modules, applies the visitor's values with P.override (as `kese --set` does),
     and calls kese.pipeline.generate.  The run's own parameters.txt and report.txt record everything.
  3. Export writes the visitor's values into copies of the parameter files (only the changed values change).

Every function returns JSON text, so the JavaScript side never sees Python objects.

Folder layout in the browser's in-memory file system (ROOT):
    ROOT/kese/...  ROOT/parameters/...   the generator, as in Generator/ (unpacked from generator.zip)
    ROOT/web/WebGenerator.py             this file, and mapbox_earcut.py (the earcut shim)
    ROOT/Input/<board>.kicad_pcb         the visitor's board
    ROOT/Output/<board>/<mode>_<FORMATS>/ the run's folder, as KESE names it
"""

import ast
import concurrent.futures
import importlib
import io
import json
import os
import re
import shutil
import sys
import traceback
import zipfile

ROOT = "/kese"
WEB_ONLY = {}                     # filled by configure(): the few web settings (see webui.json)


# =============================================================================
# threads: the browser has none.  KESE's thread pools run their jobs one after another, the same results in the
# same order (KESE sorts what its workers return).
# =============================================================================
class _SerialPool:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def submit(self, fn, *args, **kwargs):
        f = concurrent.futures.Future()
        try:
            f.set_result(fn(*args, **kwargs))
        except BaseException as e:                # noqa: BLE001  (handed to the caller, as a real pool would)
            f.set_exception(e)
        return f

    def map(self, fn, *iterables, **kwargs):
        return map(fn, *iterables)

    def shutdown(self, *args, **kwargs):
        pass


concurrent.futures.ThreadPoolExecutor = _SerialPool


def configure(config_json):
    """The web settings from webui.json that the Python side needs (hidden parameters, forced values)."""
    WEB_ONLY.clear()
    WEB_ONLY.update(json.loads(config_json))
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    sys.dont_write_bytecode = True
    return json.dumps({"ok": True})


# =============================================================================
# the parameter files
# =============================================================================
def _module_files():
    """{short name: file name} in KESE's own order (parameters/__init__.py, _MODULES)."""
    import parameters
    return {short: f"{mod}.py" for short, mod in parameters._MODULES.items()}


def _source(fname):
    with open(os.path.join(ROOT, "parameters", fname), encoding="utf-8") as fh:
        return fh.read()


def _assignments(source):
    """[(NAME, value node)] of every top-level NAME = value, in file order."""
    out = []
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id.isupper():
            out.append((node.targets[0].id, node.value))
    return out


def _comment(line):
    s = line.strip()
    return s[1:].strip() if s.startswith("#") else None


def _help_texts(source):
    """{NAME: help}: the comment block above the assignment (or above the run of assignments it belongs to), its
    trailing comment, and comment lines right below that continue the trailing comment."""
    lines = source.split("\n")
    out = {}
    for name, v in _assignments(source):
        i = v.lineno - 1
        # walk up over assignments written directly above (no blank line): they share the block above them
        j = i - 1
        while j >= 0 and lines[j].strip() and not lines[j].lstrip().startswith("#"):
            j -= 1
        above = []
        while j >= 0 and lines[j].startswith("#"):          # a block comment starts in column 0; an indented
            above.insert(0, lines[j].rstrip())              # comment continues the trailing comment above it
            j -= 1
        # the block's own indentation is kept (lists of choices are indented in the files)
        block = []
        for l in above:
            t = l.lstrip()[1:]
            block.append(t[1:] if t.startswith(" ") else t)
        trailing = []
        last = lines[v.end_lineno - 1]
        cut = v.end_col_offset
        if "#" in last[cut:]:
            col = last.index("#", cut)
            trailing.append(last[col + 1:].strip())
            k = v.end_lineno
            while k < len(lines) and lines[k].lstrip().startswith("#") and len(lines[k]) - len(lines[k].lstrip()) >= col - 2:
                trailing.append(lines[k].strip()[1:].strip())
                k += 1
        text = "\n".join(block).strip("\n")
        if trailing:
            text = (text + "\n" if text else "") + " ".join(trailing)
        out[name] = text.strip()
    return out


def _doc(source):
    """The first line of the file's docstring after its name: 'parameters/board.py - the laminate: ...'."""
    try:
        d = ast.get_docstring(ast.parse(source)) or ""
    except SyntaxError:
        return ""
    first = d.strip().split("\n")[0]
    return first.split(" - ", 1)[1].strip() if " - " in first else first


_QUOTED = re.compile(r'(?<![\w.])"([^"\n]{1,40})"')
_LISTED = re.compile(r'^\s*"(\w+)"\s*(?:[-:]|\s{2,})', re.M)


def _choices(help_text, module, value):
    """The values a parameter's comment offers.  First the list the comment gives, one per line
    ('   "net"    - one solid per net'); else every quoted word of the comment, without examples
    ('e.g. "GND"').  Plus the keys of a table the comment names ('one of the keys of FINISH_TYPES')."""
    def quoted():
        words = []
        for m in _QUOTED.finditer(help_text):
            before = help_text[max(0, m.start() - 6):m.start()]
            if "e.g." in before or "i.e." in before or not re.fullmatch(r"[\w.+-]+", m.group(1)):
                continue
            if m.group(1) not in words:
                words.append(m.group(1))
        return words

    def tables():
        out = []
        for table in re.findall(r"keys of ([A-Z][A-Z0-9_]+)", help_text):
            t = getattr(module, table, None)
            if isinstance(t, dict):
                out += [k for k in t if isinstance(k, str)]
        return out

    if isinstance(value, str):
        wanted = [value]
    elif isinstance(value, list) and value and all(isinstance(x, str) for x in value):
        wanted = value
    else:
        return []                                     # only words and lists of words have choices
    for words in (list(dict.fromkeys(_LISTED.findall(help_text))), quoted()):
        words = list(dict.fromkeys(words + tables()))
        if len(words) >= 2 and set(wanted) <= set(words):
            return words
    if isinstance(value, list) and value and all(isinstance(x, str) for x in value):
        return list(value)                            # a list with no choices in its comment: its own items
    return []


def _kind(value, choices):
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "num"
    if value is None:
        return "num_or_none"
    if isinstance(value, str):
        return "choice" if choices else "str"
    if isinstance(value, list) and choices:
        return "multi"
    return "literal"                                  # lists and tables: edited as Python text in Advanced


def describe():
    """Every parameter of every parameter file, in file order, plus what the page needs to know about KESE."""
    _forget_kese()
    _reset_parameters()
    import kese
    import parameters
    from kese import job
    P = parameters.P
    hidden = set(WEB_ONLY.get("hidden", []))
    files, out = [], []
    for short, fname in _module_files().items():
        src = _source(fname)
        helps = _help_texts(src)
        mod = getattr(P, short)
        files.append({"module": short, "file": fname, "doc": _doc(src)})
        for name, _node in _assignments(src):
            key = f"{short}.{name}"
            if key in hidden or not hasattr(mod, name):
                continue
            value = getattr(mod, name)
            try:
                json.dumps(value)
            except TypeError:
                continue                              # not a plain value: not offered on the web
            help_text = helps.get(name, "")
            choices = _choices(help_text, mod, value)
            out.append({"key": key, "module": short, "file": fname, "name": name, "kind": _kind(value, choices),
                        "choices": choices, "default": value, "help": help_text})
    return json.dumps({"version": kese.__version__, "files": files, "parameters": out,
                       "modes": list(job.MODES), "formats": list(job.FORMATS),
                       "visualFormats": sorted(job.VISUAL_FORMATS), "presets": P.Run.PRESETS})


# =============================================================================
# a run
# =============================================================================
def _forget_kese():
    """Drop KESE's modules, so the next import starts from the parameter modules as they are now."""
    importlib.invalidate_caches()
    for name in list(sys.modules):
        if name == "kese" or name.startswith("kese."):
            sys.modules.pop(name, None)


def _reset_parameters():
    """The parameter modules back to the values in their files (P keeps the same module objects)."""
    import parameters
    for mod in parameters.P.modules().values():
        importlib.reload(mod)


def _apply(values):
    """values {"Module.NAME": value}: the ones that differ from the files are applied with P.override, as
    `kese --set` does, and returned as the run's overrides (they head its parameters.txt)."""
    import parameters
    P = parameters.P
    overrides = []
    for key, value in values.items():
        short, name = key.split(".", 1)
        mod = getattr(P, short, None)
        if mod is None or not hasattr(mod, name):
            continue
        if getattr(mod, name) != value:
            P.override(key, value)
            overrides.append((key, value))
    for key, value in WEB_ONLY.get("forced", {}).items():   # how the browser runs it (no threads, no status line)
        P.override(key, value)
    return overrides


def _checks(report_text, error=None):
    """Error / warning / info rows for the Checks panel, from report.txt (KESE's own record of the run)."""
    rows, section = [], None
    for line in report_text.split("\n"):
        s = line.strip()
        if line.startswith("warning: "):
            rows.append({"level": "warning", "stage": "read", "msg": line[len("warning: "):]})
        elif line and not line.startswith(" "):
            section = s
        elif section == "skipped" and s and s != "nothing":
            rows.append({"level": "info", "stage": "skipped", "msg": re.sub(r"^\d+\s+", lambda m: m.group(0).strip() + " ", s)})
        elif section == "notes" and s:
            rows.append({"level": "info", "stage": "notes", "msg": s})
        elif section and section.startswith("verify") and s:
            level = "error" if "FAIL" in s.upper() else "info"
            rows.append({"level": level, "stage": "verify", "msg": s})
    if error:
        rows.insert(0, {"level": "error", "stage": "run", "msg": error})
    return rows


def _font_check(pcb_text):
    """The web tool ships KiCad's stroke font up to U+2E7F (webui.json "fontLastCodepoint"); a board with text
    beyond it gets '?' for those characters, so the page says so."""
    last = int(WEB_ONLY.get("fontLastCodepoint", 0x10FFFF))
    beyond = sorted({c for c in pcb_text if ord(c) > last})
    if not beyond:
        return []
    shown = "".join(beyond[:12]) + ("…" if len(beyond) > 12 else "")
    return [{"level": "warning", "stage": "web", "msg": f"text with characters the web tool's font does not have "
             f"({shown}) is drawn as '?'; the desktop KESE draws them"}]


def generate(board_name, values_json):
    """One run.  Returns {ok, folder, files [{path, size}], checks, seconds?} or {ok: false, checks}."""
    values = json.loads(values_json)
    pcb = os.path.join(ROOT, "Input", board_name)
    out_root = os.path.join(ROOT, "Output")
    shutil.rmtree(out_root, ignore_errors=True)
    os.makedirs(out_root, exist_ok=True)
    _forget_kese()
    _reset_parameters()
    overrides = _apply(values)
    log = io.StringIO()
    with open(pcb, encoding="utf-8", errors="replace") as fh:
        extra = _font_check(fh.read())
    try:
        from kese.pipeline import generate as kese_generate
        out_dir, _model = kese_generate(__import__("pathlib").Path(pcb), out_root=__import__("pathlib").Path(out_root),
                                        overrides=overrides, log=lambda s: log.write(s + "\n"))
    except Exception as e:                                       # noqa: BLE001  (shown in Checks, not raised)
        msg = f"{type(e).__name__}: {e}"
        tail = traceback.format_exc().strip().split("\n")[-3:]
        return json.dumps({"ok": False, "checks": _checks("", msg) + extra, "log": log.getvalue(),
                           "trace": "\n".join(tail)})
    out_dir = str(out_dir)
    files = []
    for base, _dirs, names in os.walk(out_dir):
        for n in sorted(names):
            p = os.path.join(base, n)
            files.append({"path": os.path.relpath(p, out_dir).replace(os.sep, "/"), "size": os.path.getsize(p)})
    files.sort(key=lambda f: f["path"])
    report = ""
    rp = os.path.join(out_dir, "report.txt")
    if os.path.exists(rp):
        with open(rp, encoding="utf-8") as fh:
            report = fh.read()
    return json.dumps({"ok": True, "folder": out_dir, "name": os.path.basename(out_dir), "files": files,
                       "checks": _checks(report) + extra, "log": log.getvalue()})


# =============================================================================
# import and export
# =============================================================================
def _literal_text(value):
    return repr(value)


def export_files(values_json):
    """{file name: text} of every parameter file with the visitor's values put in.  Only the value expressions of
    changed parameters are replaced; comments and layout stay as they are."""
    values = json.loads(values_json)
    out = {}
    for short, fname in _module_files().items():
        src = _source(fname)
        lines = src.split("\n")
        spots = [(name, v) for name, v in _assignments(src) if f"{short}.{name}" in values]
        for name, v in sorted(spots, key=lambda s: (s[1].lineno, s[1].col_offset), reverse=True):
            new_value = values[f"{short}.{name}"]
            ln, col, end_ln, end_col = v.lineno, v.col_offset, v.end_lineno, v.end_col_offset
            old = "\n".join([lines[ln - 1][col:]] + lines[ln:end_ln - 1] + [lines[end_ln - 1][:end_col]]) if ln != end_ln \
                else lines[ln - 1][col:end_col]
            try:
                if ast.literal_eval(old) == new_value:
                    continue
            except Exception:                                    # noqa: BLE001
                pass
            new = _literal_text(new_value)
            head, tail = lines[ln - 1][:col], lines[end_ln - 1][end_col:]
            pad = " " * max(0, len(old) - len(new)) if ln == end_ln and tail.lstrip().startswith("#") else ""
            lines[ln - 1:end_ln] = [head + new + pad + tail]
        out[fname] = "\n".join(lines)
    return json.dumps(out)


def export_zip(values_json, zip_path):
    """The Export zip: parameters/*.py with these values, ready to drop into Generator/ on a desktop."""
    files = json.loads(export_files(values_json))
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for fname, text in files.items():
            z.writestr(f"parameters/{fname}", text)
    return json.dumps({"zip": zip_path})


def read_values(text, file_name=""):
    """Values in an imported parameters.txt (any run, web or desktop) or a parameters/*.py file:
    {"values": {"Module.NAME": value}, "ignored": [names this version does not have]}."""
    import parameters
    P = parameters.P
    files = _module_files()
    by_file = {f: short for short, f in files.items()}
    current = by_file.get(os.path.basename(file_name))       # a .py file: its own module
    found, ignored = {}, []
    if file_name.endswith(".py") and current:                # a parameter file: read with Python's own parser
        mod = getattr(P, current)
        for name, node in _assignments(text):
            key = f"{current}.{name}"
            if not hasattr(mod, name):
                ignored.append(key)
            elif key not in set(WEB_ONLY.get("hidden", [])):
                try:
                    found[key] = ast.literal_eval(node)
                except ValueError:
                    pass
        return json.dumps({"values": found, "ignored": ignored})
    for line in text.split("\n"):
        s = line.strip()
        m = re.fullmatch(r"\[parameters/(\w+\.py)\]", s)      # parameters.txt section heading
        if m:
            current = by_file.get(m.group(1))
            continue
        if not s or s.startswith("#") or "=" not in s or current is None:
            continue
        name, _, rest = s.partition("=")
        name = name.strip()
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
            continue
        key = f"{current}.{name}"
        if not hasattr(getattr(P, current), name):
            if key not in ignored:
                ignored.append(key)
            continue
        if key in set(WEB_ONLY.get("hidden", [])):
            continue
        expr = rest.split("#")[0].strip() if not rest.strip().startswith(("{", "[", "(")) else rest.strip()
        for cut in range(len(expr), 0, -1):                   # the longest start that is a Python literal
            try:
                found[key] = ast.literal_eval(expr[:cut].strip())
                break
            except Exception:                                 # noqa: BLE001
                continue
    return json.dumps({"values": found, "ignored": ignored})
