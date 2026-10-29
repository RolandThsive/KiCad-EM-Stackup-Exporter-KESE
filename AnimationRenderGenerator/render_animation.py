"""GLBs of boards as animated WebPs that loop: the board stood up facing the camera and turned about
the vertical axis, so that its top and its bottom come round in turn (the bottom reading the right
way round, as when a board is turned over in the hand), one full turn a loop at a steady speed.
Several GLBs can be turned together, one above the other or side by side.  The settings are in
parameters.py next to this file.

    python AnimationRenderGenerator/render_animation.py               (Input/*.glb and TOGETHER -> Output/)
    python AnimationRenderGenerator/render_animation.py --frames 18 --rps 0.125
    python AnimationRenderGenerator/render_animation.py --glb a.glb b.glb -o Output/both.webp   (one WebP)
    python AnimationRenderGenerator/render_animation.py --help        (every option)

Needs Python 3.10 or later with Pillow and Playwright (python -m pip install pillow playwright,
then python -m playwright install chromium).  three.js is fetched once from the npm registry.
"""
import argparse
import base64
import importlib.util
import io
import math
import mimetypes
import tarfile
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HOST = "http://glb-to-webp.local"
INK, SOFT, LINE = (24, 26, 30), (88, 94, 102), (222, 225, 230)
MODES = {"visual": ("Visual mode", "only the faces you can see"),
         "simulation": ("Simulation mode", "every layer a closed solid")}


def load_parameters(path):
    spec = importlib.util.spec_from_file_location("animation_parameters", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {k: v for k, v in vars(module).items() if k.isupper()}


def angles(p):
    """The turn of each frame in degrees, moved on by half a step when a step would land edge-on."""
    n = p["FRAMES"]
    step = 360 / n
    start = p["START_ANGLE"]
    if any(min(r := (start + step * i - 90) % 180, 180 - r) < 1e-6 for i in range(n)):
        start += step / 2
    sign = 1 if p["DIRECTION"] == "right" else -1
    return [sign * (start + step * i) for i in range(n)]


def three(version):
    """three.js's build/ and examples/jsm/, fetched once from the npm registry."""
    folder = HERE / ".three" / version
    if not (folder / "build" / "three.module.js").exists():
        url = f"https://registry.npmjs.org/three/-/three-{version}.tgz"
        print(f"fetching three.js {version} from {url}")
        data = urllib.request.urlopen(url, timeout=120).read()
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
            wanted = [m for m in tar.getmembers() if m.isfile()
                      and m.name.startswith(("package/build/", "package/examples/jsm/", "package/LICENSE"))]
            for m in wanted:
                m.name = m.name[len("package/"):]
            tar.extractall(folder, members=wanted, filter="data")
    return folder


DRAWN = {}      # the frames of every GLB drawn in this run, so a GLB alone and with others is drawn once


def render(glbs, p):
    """Every GLB's frames, as RGBA images of WIDTH x HEIGHT (drawn SUPERSAMPLE times larger)."""
    from playwright.sync_api import sync_playwright

    todo = [g for g in glbs if Path(g).resolve() not in DRAWN]
    if not todo:
        return [DRAWN[Path(g).resolve()] for g in glbs]

    lib = three(p["THREE_VERSION"])
    files = {f"/glb/{i}.glb": Path(g) for i, g in enumerate(todo)}

    def serve(route):
        path = route.request.url[len(HOST):].split("?")[0]
        if path == "/render.html":
            f = HERE / "render.html"
        elif path.startswith("/three/"):
            f = lib / path[len("/three/"):]
        else:
            f = files.get(path)
        if f is None or not f.is_file():
            return route.fulfill(status=404)
        route.fulfill(path=str(f), content_type=mimetypes.guess_type(f.name)[0] or "application/octet-stream")

    ss = p["SUPERSAMPLE"]
    job = dict(width=p["WIDTH"] * ss, height=p["HEIGHT"] * ss, angles=angles(p), fov=p["CAMERA_FOV"],
               elevation=p["CAMERA_ELEVATION"], margin=p["MARGIN"], lights=p["LIGHTS"], ambient=p["AMBIENT"],
               metalness=p["METALNESS"], roughness=p["ROUGHNESS"],
               reflectionMetal=p["REFLECTION_METAL"], reflectionOther=p["REFLECTION_OTHER"])
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=p["CHROMIUM"],
                                     args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        page = browser.new_page()
        page.on("pageerror", lambda e: print("page error:", e))
        page.route(f"{HOST}/**", serve)
        page.goto(f"{HOST}/render.html")
        page.wait_for_function("window.ready === true")
        for i, g in enumerate(todo):
            t = time.time()
            urls = page.evaluate("o => window.render(o)", dict(job, glb=f"/glb/{i}.glb"))
            frames = [Image.open(io.BytesIO(base64.b64decode(u.split(",", 1)[1]))).convert("RGBA") for u in urls]
            if ss > 1:
                frames = [premultiplied_resize(f, (p["WIDTH"], p["HEIGHT"])) for f in frames]
            DRAWN[Path(g).resolve()] = frames
            print(f"rendered {Path(g).name}: {len(frames)} frames in {time.time() - t:.0f} s")
        browser.close()
    return [DRAWN[Path(g).resolve()] for g in glbs]


def premultiplied_resize(im, size):
    """LANCZOS on premultiplied colours, so that the transparent background does not darken the edges."""
    return im.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def titles(glbs, value, which):
    if value is None:
        return None
    if value != "auto":
        return list(value)
    names = []
    for g in glbs:
        text = str(Path(g)).lower()
        mode = next((m for m in MODES if m in Path(g).name.lower()), None) or next((m for m in MODES if m in text), None)
        names.append(MODES[mode][which] if mode else (Path(g).stem if which == 0 else ""))
    return names


def font(size, bold=False):
    for name in (("DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf") if bold else ("DejaVuSans.ttf", "Arial.ttf", "arial.ttf")):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size)


def compose(glbs, panels, p):
    """The frames of every GLB, one panel each, stacked (LAYOUT "stacked") or side by side, cut to the
    rows any of them draws in, each with its title over it."""
    w, h = p["WIDTH"], p["HEIGHT"]
    y0, y1 = 0, h
    if p["CROP"]:
        rows = [b for frames in panels for f in frames if (b := f.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox())]
        if rows:
            y0 = max(min(b[1] for b in rows) - p["PADDING"], 0)
            y1 = min(max(b[3] for b in rows) + p["PADDING"], h)
    head = titles(glbs, p["TITLES"], 0) if len(glbs) > 1 else None
    sub = titles(glbs, p["SUBTITLES"], 1) if len(glbs) > 1 else None
    top = (86 if sub and any(sub) else 56) if head else 0
    ph = top + y1 - y0                                  # one panel, its title band included
    stacked = p["LAYOUT"] == "stacked"
    at = [(0, k * ph) if stacked else (k * w, 0) for k in range(len(panels))]
    size = (w, len(panels) * ph) if stacked else (len(panels) * w, ph)
    bg = p["BACKGROUND"]
    fill = (0, 0, 0, 0) if bg is None else Image.new("RGBA", (1, 1), bg).getpixel((0, 0))
    out = []
    for i in range(len(panels[0])):
        cv = Image.new("RGBA", size, fill)
        for k, frames in enumerate(panels):
            cv.alpha_composite(frames[i].crop((0, y0, w, y1)), (at[k][0], at[k][1] + top))
        d = ImageDraw.Draw(cv)
        for k, (x, y) in enumerate(at):
            if head and head[k]:
                d.text((x + w / 2, y + 18), head[k], font=font(30, True), fill=INK, anchor="mt")
            if sub and sub[k]:
                d.text((x + w / 2, y + 56), sub[k], font=font(22), fill=SOFT, anchor="mt")
            if k and p["DIVIDER"]:
                d.line([(40, y), (w - 40, y)] if stacked else [(x, 22), (x, ph - 22)], fill=LINE, width=2)
        out.append(cv if bg is None else cv.convert("RGB"))
    return out


def save(frames, path, p):
    ms = 1000 / (p["FRAMES"] * p["ROTATIONS_PER_SECOND"])
    # whole milliseconds a frame, spread so that the turn takes its time exactly
    durations = [round(ms * (i + 1)) - round(ms * i) for i in range(len(frames))]
    q = p["QUALITY"]
    opts = dict(lossless=True, quality=100) if q == "lossless" else dict(quality=int(q))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=durations, loop=0, method=p["METHOD"], **opts)
    return ms


def make(glbs, out, p):
    frames = compose(glbs, render(glbs, p), p)
    out.parent.mkdir(parents=True, exist_ok=True)
    ms = save(frames, out, p)
    print(f"{out}  {out.stat().st_size / 1e6:.2f} MB  {frames[0].width} x {frames[0].height}  "
          f"{len(frames)} frames of {ms:.0f} ms, {1 / p['ROTATIONS_PER_SECOND']:.1f} s a turn")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--glb", nargs="+", type=Path, help="make one WebP of these GLBs (together, as LAYOUT, when several) "
                                                         "instead of every GLB of INPUT_DIR")
    ap.add_argument("-o", "--output", type=Path, help="with --glb: the WebP (default: OUTPUT_DIR/<first GLB>_<FRAMES>f.webp)")
    ap.add_argument("--parameters", type=Path, default=HERE / "parameters.py", help="a parameters file (default: parameters.py here)")
    ap.add_argument("--frames", type=int, help="FRAMES: pictures in one turn")
    ap.add_argument("--rps", type=float, help="ROTATIONS_PER_SECOND: full turns a second")
    ap.add_argument("--quality", help='QUALITY: 1 - 100, or "lossless"')
    ap.add_argument("--width", type=int, help="WIDTH of one panel in pixels")
    ap.add_argument("--height", type=int, help="HEIGHT of one panel before it is cut")
    ap.add_argument("--supersample", type=int, help="SUPERSAMPLE: drawn this many times larger, then scaled down")
    ap.add_argument("--background", help='BACKGROUND colour such as "#ffffff", or "none" for transparent')
    ap.add_argument("--layout", choices=("stacked", "side"), help="LAYOUT of several GLBs: one above the other, or side by side")
    ap.add_argument("--direction", choices=("left", "right"), help="DIRECTION the near edge moves")
    ap.add_argument("--chromium", help="CHROMIUM: path of a Chromium to use instead of Playwright's own")
    a = ap.parse_args()

    p = load_parameters(a.parameters)
    for key, value in (("FRAMES", a.frames), ("ROTATIONS_PER_SECOND", a.rps), ("WIDTH", a.width), ("HEIGHT", a.height),
                       ("SUPERSAMPLE", a.supersample), ("DIRECTION", a.direction), ("LAYOUT", a.layout), ("CHROMIUM", a.chromium)):
        if value is not None:
            p[key] = value
    if a.quality is not None:
        p["QUALITY"] = a.quality if a.quality == "lossless" else int(a.quality)
    if a.background is not None:
        p["BACKGROUND"] = None if a.background.lower() == "none" else a.background
    if p["FRAMES"] < 2 or p["ROTATIONS_PER_SECOND"] <= 0:
        ap.error("FRAMES must be 2 or more and ROTATIONS_PER_SECOND above 0")
    src, dst = ROOT / p["INPUT_DIR"], ROOT / p["OUTPUT_DIR"]
    suffix = f"_{p['FRAMES']}f.webp"

    if a.glb:
        for g in a.glb:
            if not g.is_file():
                ap.error(f"no such file: {g}")
        make(a.glb, a.output or dst / (a.glb[0].stem + suffix), p)
        return
    jobs = []
    if p["SINGLE"]:
        jobs += [([g], dst / (g.stem + suffix)) for g in sorted(src.glob("*.glb"))]
    for name, files in p["TOGETHER"].items():
        missing = [f for f in files if not (src / f).is_file()]
        if missing:
            print(f"skipped {name}: not in {src}: {', '.join(missing)}")
            continue
        jobs.append(([src / f for f in files], dst / (name + suffix)))
    if not jobs:
        ap.error(f"no GLB in {src}")
    for glbs, out in jobs:
        make(glbs, out, p)


if __name__ == "__main__":
    main()
