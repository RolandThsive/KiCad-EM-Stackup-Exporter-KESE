"""
vendor_lock.py - writes WebUI/vendor.json: the exact files of Pyodide and three.js the web tool uses, with a
SHA-256 of each, so build_site.py can put a checked backup copy of them on the site.

    python WebUI/tools/vendor_lock.py                              (downloads from the CDN named in webui.json)
    python WebUI/tools/vendor_lock.py --from DIR                   (DIR/pyodide/... and DIR/three/..., a local copy)

Run it after changing "pyodide", "three" or "pyodidePackages" in webui.json, or after the page starts importing
another three.js addon.  Which files are listed:
  three.js   every file the page can import: the specifiers "three" and "three/addons/..." found in WebUI/*.js, and
             everything those files import in turn (relative imports, followed to the end).
  Pyodide    the runtime (pyodide.mjs, pyodide.asm.mjs, pyodide.asm.wasm, python_stdlib.zip, pyodide-lock.json) and
             the wheels of webui.json "pyodidePackages" with their dependencies, as pyodide-lock.json lists them.

Only the standard library is used.
"""
import argparse
import hashlib
import json
import posixpath
import re
import sys
import time
import urllib.request
from pathlib import Path

WEBUI = Path(__file__).resolve().parent.parent
PYODIDE_RUNTIME = ["pyodide.mjs", "pyodide.asm.mjs", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]
# import ... from "x"; export ... from "x"; import "x"; import("x")
IMPORT_RE = re.compile(r"""(?:\bimport|\bexport)\s[^;'"`]*?\bfrom\s*(['"])([^'"]+)\1|\bimport\s*\(?\s*(['"])([^'"]+)\3""")


def fetch(url, tries=4):
    for n in range(1, tries + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception as e:                                     # noqa: BLE001 - reported after the last try
            if n == tries:
                raise SystemExit(f"{url} could not be downloaded: {e}")
            time.sleep(2 ** n)


class Source:
    """Where the files are read from: the CDN (base URL) or a local folder."""

    def __init__(self, base, folder):
        self.base, self.folder = base, folder
        self.cache = {}

    def read(self, path):
        if path not in self.cache:
            self.cache[path] = (self.folder / path).read_bytes() if self.folder else fetch(self.base + path)
        return self.cache[path]


def imports(text):
    for m in IMPORT_RE.finditer(text):
        yield m.group(2) or m.group(4)


def three_entries():
    """The three.js files the page imports by name, as paths inside the three package."""
    out = set()
    for js in sorted(WEBUI.glob("*.js")):
        for spec in imports(js.read_text(encoding="utf-8")):
            if spec == "three":
                out.add("build/three.module.js")
            elif spec.startswith("three/addons/"):
                out.add("examples/jsm/" + spec[len("three/addons/"):])
    return out


def three_files(src):
    todo, seen = sorted(three_entries()), set()
    while todo:
        path = todo.pop()
        if path in seen:
            continue
        seen.add(path)
        for spec in imports(src.read(path).decode("utf-8")):
            if spec == "three":
                todo.append("build/three.module.js")
            elif spec.startswith("three/addons/"):
                todo.append("examples/jsm/" + spec[len("three/addons/"):])
            elif spec.startswith("."):
                todo.append(posixpath.normpath(posixpath.join(posixpath.dirname(path), spec)))
            else:
                raise SystemExit(f"{path} imports {spec!r}, which is neither three nor a relative file")
    return sorted(seen)


def pyodide_files(src, packages):
    lock = json.loads(src.read("pyodide-lock.json"))["packages"]
    need, todo = set(), list(packages)
    while todo:
        name = todo.pop()
        if name in need:
            continue
        if name not in lock:
            raise SystemExit(f"{name} is not in pyodide-lock.json")
        need.add(name)
        todo.extend(lock[name].get("depends", []))
    wheels = sorted(lock[n]["file_name"] for n in need)
    for n in need:                                                 # the lock's own hash must match the file
        got = hashlib.sha256(src.read(lock[n]["file_name"])).hexdigest()
        if got != lock[n]["sha256"]:
            raise SystemExit(f"{lock[n]['file_name']}: sha256 {got}, pyodide-lock.json says {lock[n]['sha256']}")
    return PYODIDE_RUNTIME + wheels


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="folder", type=Path, help="a local copy: DIR/pyodide/ and DIR/three/")
    a = ap.parse_args()
    cfg = json.loads((WEBUI / "webui.json").read_text(encoding="utf-8"))
    out = {"_about": "Written by tools/vendor_lock.py: the Pyodide and three.js files of the backup copy, with the "
                     "SHA-256 build_site.py checks each download against.  Do not edit by hand."}
    for name, lister in (("pyodide", lambda s: pyodide_files(s, cfg["pyodidePackages"])), ("three", three_files)):
        src = Source(cfg[name], a.folder / name if a.folder else None)
        files = lister(src)
        out[name] = {"base": cfg[name], "files": {f: hashlib.sha256(src.read(f)).hexdigest() for f in files}}
        size = sum(len(src.read(f)) for f in files)
        print(f"{name}: {len(files)} files, {size / 1048576:.1f} MB")
    (WEBUI / "vendor.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("wrote", WEBUI / "vendor.json")


if __name__ == "__main__":
    sys.exit(main())
