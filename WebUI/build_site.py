"""
build_site.py - puts the web tool together in one folder, as GitHub Pages serves it.

    python WebUI/build_site.py _site          (the Pages workflow; LocalTesting/serve.py does the same)

The folder gets:
  WebUI/...               the page (every file of WebUI/ except this script and BloggerPage.html)
  WebUI/generator.zip     the generator the browser runs: Generator/kese and Generator/parameters as they are on the
                          branch, without tests, tools, boards or caches.  KiCad's stroke font is cut to the
                          characters up to webui.json "fontLastCodepoint" (60 KB instead of 1.36 MB).
  WebUI/version.json      the generator's version, a hash of the zip (so a browser fetches the zip again only
                          when it changed) and the example boards
  WebUI/logo.svg, favicon.ico   the KESE logo (docs/logo/Kese_Square.svg) and favicon (docs/logo/favicon.ico)
  WebUI/examples/         the example boards of Generator/Input
  index.html              a redirect to WebUI/

Only the standard library is used.
"""
import gzip
import hashlib
import io
import json
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent              # WebUI/
REPO = HERE.parent
GENERATOR = REPO / "Generator"
NOT_PUBLISHED = {"build_site.py", "BloggerPage.html", "__pycache__"}
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


def build(site):
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
    data = generator_zip(config)
    (site / "WebUI" / "generator.zip").write_bytes(data)
    version = {}
    for line in (GENERATOR / "kese" / "__init__.py").read_text(encoding="utf-8").splitlines():
        if line.startswith("__version__"):
            version["kese"] = line.split("=", 1)[1].strip().strip("\"'")
    version["zip"] = hashlib.sha256(data).hexdigest()[:16]
    version["bytes"] = len(data)
    version["examples"] = [b.name for b in boards]
    (site / "WebUI" / "version.json").write_text(json.dumps(version), encoding="utf-8")
    (site / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; '
                                     'url=WebUI/"><a href="WebUI/">KiCad EM Stackup Exporter</a>\n', encoding="utf-8")
    return version


if __name__ == "__main__":
    v = build(sys.argv[1] if len(sys.argv) > 1 else "_site")
    print(f"built: KESE {v.get('kese')}, generator.zip {v['bytes'] / 1024:.0f} KB ({v['zip']})")
