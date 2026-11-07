"""
build_site.py - puts the web tool together in one folder, as GitHub Pages serves it.

    python WebUI/build_site.py _site                       (the Pages workflow; LocalTesting/serve.py does the same)
    python WebUI/build_site.py _site --vendor-from DIR     (the backup copy from DIR/pyodide and DIR/three, not the CDN)

The folder gets:
  WebUI/...               the page (every file of WebUI/ except this script, BloggerPage.html, the tests and tools)
  WebUI/generator.zip     the generator the browser runs: Generator/kese and Generator/parameters as they are on the
                          branch, without tests, tools, boards or caches.  KiCad's stroke font is cut to the
                          characters up to webui.json "fontLastCodepoint" (60 KB instead of 1.36 MB).
  WebUI/version.json      the generator's version, a hash of the zip (so a browser fetches the zip again only
                          when it changed) and the example boards
  WebUI/logo.svg, favicon.ico   the KESE logo (docs/logo/Kese_Square.svg) and favicon (docs/logo/favicon.ico)
  WebUI/examples/         the example boards of Generator/Input
  WebUI/vendor/           the backup copy of Pyodide and three.js the page falls back on when jsDelivr fails: the files
                          vendor.json lists, downloaded from jsDelivr (or copied from --vendor-from / KESE_VENDOR_FROM)
                          and checked against vendor.json's SHA-256.  A file that differs stops the build.
  WebUI/importmaps.json   the two import maps boot.js chooses from (three.js from jsDelivr or from vendor/three), each
                          with the SHA-384 of every three.js file ("integrity"), so a browser refuses a changed file
  index.html              a redirect to WebUI/

WebUI/index.html gets its Content-Security-Policy here (CSP below): the import maps are inline scripts, allowed by
their SHA-256, which changes with every three.js update.  version.json also gets the commit and date of the build,
shown in the page's footer.

Only the standard library is used.
"""
import argparse
import base64
import datetime
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent              # WebUI/
REPO = HERE.parent
GENERATOR = REPO / "Generator"
NOT_PUBLISHED = {"build_site.py", "BloggerPage.html", "__pycache__", "tests", "tools", "vendor.json", "node_modules",
                 "docs", "README.md", "CHANGELOG.md"}   # the project's own notes: on GitHub, not on the site
CSP_PLACEHOLDER = 'content="(written by build_site.py)"'


def csp(three_base, map_hashes):
    """The page's Content-Security-Policy.  Workers (Python, the STEP reader, the cross-section) are files of this
    site and follow their own (empty) policy; this one is the page's.  frame-ancestors cannot be set from a meta tag:
    the blog frames the page from another site on purpose."""
    return "; ".join([
        "default-src 'self'",
        f"script-src 'self' {three_base} " + " ".join(f"'sha256-{h}'" for h in map_hashes),
        "style-src 'self'",
        "img-src 'self' data: blob:",
        "font-src 'self'",
        f"connect-src 'self' {three_base} blob: data:",
        "worker-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
    ])                    # no upgrade-insecure-requests: Pages is HTTPS only, and Safari would upgrade http://127.0.0.1 too
FONT = Path("kese/assets/fonts/kicad_newstroke.json.gz")


def _font_subset(last_codepoint):
    """KiCad's newstroke font with the glyphs up to last_codepoint (the font is a list from first_codepoint on;
    KESE draws '?' for a character past the end of the list)."""
    with gzip.open(GENERATOR / FONT, "rt", encoding="utf-8") as fh:
        font = json.load(fh)
    keep = last_codepoint - font.get("first_codepoint", 32) + 1
    font["glyphs"] = font["glyphs"][:keep]
    raw = json.dumps(font, separators=(",", ":")).encode("utf-8")
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb", compresslevel=9, mtime=0) as gz:
        gz.write(raw)
    return out.getvalue()


def generator_zip(config):
    """The bytes of generator.zip (the same bytes for the same files: fixed dates, sorted names)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for top in ("kese", "parameters"):
            for p in sorted((GENERATOR / top).rglob("*")):
                rel = p.relative_to(GENERATOR)
                if p.is_dir() or "__pycache__" in rel.parts or p.suffix == ".pyc":
                    continue
                info = zipfile.ZipInfo(rel.as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                data = _font_subset(int(config["fontLastCodepoint"])) if rel == FONT else p.read_bytes()
                z.writestr(info, data)
    return buf.getvalue()


def _download(url, tries=4):
    for n in range(1, tries + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception as e:                                     # noqa: BLE001 - reported after the last try
            if n == tries:
                raise SystemExit(f"build_site: {url} could not be downloaded: {e}")
            time.sleep(2 ** n)


def vendor(site, config, source_dir, cache=None):
    """WebUI/vendor/pyodide and WebUI/vendor/three: every file of vendor.json, checked against its SHA-256.
    cache: a folder that keeps the downloads between builds (LocalTesting rebuilds on every page load); a file there
    is used only while its SHA-256 still matches vendor.json."""
    lock = json.loads((HERE / "vendor.json").read_text(encoding="utf-8"))
    bad, files = [], {}
    for name in ("pyodide", "three"):
        if lock[name]["base"] != config[name]:
            raise SystemExit(f"build_site: vendor.json lists {name} from {lock[name]['base']}, webui.json uses "
                             f"{config[name]}: run python WebUI/tools/vendor_lock.py")
        for path, want in lock[name]["files"].items():
            kept = Path(cache) / name / path if cache else None
            if source_dir:
                data = (source_dir / name / path).read_bytes()
            elif kept and kept.is_file() and hashlib.sha256(kept.read_bytes()).hexdigest() == want:
                data = kept.read_bytes()
            else:
                data = _download(config[name] + path)
                if kept and hashlib.sha256(data).hexdigest() == want:
                    kept.parent.mkdir(parents=True, exist_ok=True)
                    kept.write_bytes(data)
            got = hashlib.sha256(data).hexdigest()
            if got != want:
                bad.append(f"  {name}/{path}\n    vendor.json {want}\n    got         {got}")
                continue
            out = site / "WebUI" / "vendor" / name / path
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            files[(name, path)] = data
    if bad:
        raise SystemExit("build_site: these files differ from vendor.json (changed upstream, or a bad download):\n"
                         + "\n".join(bad))
    return files


def import_maps(config, files):
    """The two import maps, as the exact text boot.js inserts (the CSP allows them by the hash of that text)."""
    def one(base):
        return json.dumps({
            "imports": {"three": base + "build/three.module.js", "three/addons/": base + "examples/jsm/"},
            "integrity": {base + path: "sha384-" + base64.b64encode(hashlib.sha384(data).digest()).decode()
                          for (name, path), data in sorted(files.items()) if name == "three"},
        }, separators=(",", ":"))
    return {"probe": config["three"] + "build/three.module.js", "cdn": one(config["three"]),
            "backup": one("./vendor/three/")}


def _commit():
    sha = os.environ.get("GITHUB_SHA", "")
    if not sha:
        try:
            sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True,
                                 check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            sha = ""
    return sha[:7] or "local"


def build(site, vendor_from=None, vendor_cache=None):
    site = Path(site)
    shutil.rmtree(site, ignore_errors=True)
    (site / "WebUI").mkdir(parents=True)
    for p in sorted(HERE.iterdir()):
        if p.name in NOT_PUBLISHED or p.name.startswith("."):
            continue
        (shutil.copytree if p.is_dir() else shutil.copy2)(p, site / "WebUI" / p.name)
    config = json.loads((HERE / "webui.json").read_text(encoding="utf-8"))
    shutil.copy2(REPO / "docs" / "logo" / "Kese_Square.svg", site / "WebUI" / "logo.svg")
    shutil.copy2(REPO / "docs" / "logo" / "favicon.ico", site / "WebUI" / "favicon.ico")
    boards = sorted((GENERATOR / "Input").glob("*.kicad_pcb"))
    if boards:
        (site / "WebUI" / "examples").mkdir()
        for b in boards:
            shutil.copy2(b, site / "WebUI" / "examples" / b.name)
    source_dir = Path(vendor_from) if vendor_from else None
    files = vendor(site, config, source_dir, vendor_cache)
    maps = import_maps(config, files)
    (site / "WebUI" / "importmaps.json").write_text(json.dumps(maps, indent=1), encoding="utf-8")
    hashes = [base64.b64encode(hashlib.sha256(maps[k].encode("utf-8")).digest()).decode() for k in ("cdn", "backup")]
    page = site / "WebUI" / "index.html"
    html = page.read_text(encoding="utf-8")
    if html.count(CSP_PLACEHOLDER) != 1:
        raise SystemExit(f"build_site: WebUI/index.html needs exactly one {CSP_PLACEHOLDER}")
    page.write_text(html.replace(CSP_PLACEHOLDER, f'content="{csp(config["three"], hashes)}"'), encoding="utf-8")
    data = generator_zip(config)
    (site / "WebUI" / "generator.zip").write_bytes(data)
    version = {}
    for line in (GENERATOR / "kese" / "__init__.py").read_text(encoding="utf-8").splitlines():
        if line.startswith("__version__"):
            version["kese"] = line.split("=", 1)[1].strip().strip("\"'")
    version["zip"] = hashlib.sha256(data).hexdigest()[:16]
    version["bytes"] = len(data)
    version["examples"] = [b.name for b in boards]
    version["commit"] = _commit()
    version["built"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    (site / "WebUI" / "version.json").write_text(json.dumps(version), encoding="utf-8")
    (site / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; '
                                     'url=WebUI/"><a href="WebUI/">KiCad EM Stackup Exporter</a>\n', encoding="utf-8")
    return version


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Put the web tool together in one folder, as GitHub Pages serves it.")
    ap.add_argument("site", nargs="?", default="_site", help="the folder to write (emptied first)")
    ap.add_argument("--vendor-from", default=os.environ.get("KESE_VENDOR_FROM"),
                    help="take the backup copy from DIR/pyodide and DIR/three instead of jsDelivr (env KESE_VENDOR_FROM)")
    ap.add_argument("--vendor-cache", default=os.environ.get("KESE_VENDOR_CACHE"),
                    help="keep the downloaded backup copy in DIR and reuse it while it matches vendor.json "
                         "(env KESE_VENDOR_CACHE)")
    a = ap.parse_args()
    v = build(a.site, a.vendor_from, a.vendor_cache)
    print(f"built: KESE {v.get('kese')} ({v['commit']}), generator.zip {v['bytes'] / 1024:.0f} KB ({v['zip']})")
