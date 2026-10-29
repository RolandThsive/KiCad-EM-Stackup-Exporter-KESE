"""GLBs of boards as still pictures: the board turned by Euler angles about the picture's axes, where
(0, 0, 0) is its top facing you with the layout reading as in KiCad's top view, and drawn as large
as fits.  Every GLB of the input folder is drawn in every view of VIEWS.  The settings are in
parameters.py next to this file.

    python StaticImageRenderer/render_image.py                        (Input/*.glb x VIEWS -> Output/)
    python StaticImageRenderer/render_image.py --view -30 20 0        (one view of every GLB)
    python StaticImageRenderer/render_image.py --glb Input/board.glb --view 0 180 0 -o Output/bottom.png
    python StaticImageRenderer/render_image.py --help                 (every option)

Needs Python 3.10 or later with Pillow and Playwright (python -m pip install pillow playwright,
then python -m playwright install chromium).  three.js is fetched once from the npm registry.
"""
import argparse
import base64
import importlib.util
import io
import mimetypes
import tarfile
import time
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HOST = "http://render-image.local"
ORDERS = ("XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX")


def load_parameters(path):
    spec = importlib.util.spec_from_file_location("image_parameters", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {k: v for k, v in vars(module).items() if k.isupper()}


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


def render(jobs, p):
    """Every (GLB, {view name: angles}) of jobs drawn, as {(GLB, view name): RGBA image of WIDTH x HEIGHT}."""
    from playwright.sync_api import sync_playwright

    lib = three(p["THREE_VERSION"])
    files = {f"/glb/{i}.glb": Path(g) for i, (g, _) in enumerate(jobs)}

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
    job = dict(width=p["WIDTH"] * ss, height=p["HEIGHT"] * ss, order=p["ORDER"], projection=p["PROJECTION"],
               fov=p["CAMERA_FOV"], margin=p["MARGIN"], lights=p["LIGHTS"], ambient=p["AMBIENT"],
               metalness=p["METALNESS"], roughness=p["ROUGHNESS"],
               reflectionMetal=p["REFLECTION_METAL"], reflectionOther=p["REFLECTION_OTHER"])
    out = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=p["CHROMIUM"],
                                     args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        page = browser.new_page()
        page.on("pageerror", lambda e: print("page error:", e))
        page.route(f"{HOST}/**", serve)
        page.goto(f"{HOST}/render.html")
        page.wait_for_function("window.ready === true")
        for i, (g, views) in enumerate(jobs):
            t = time.time()
            urls = page.evaluate("o => window.render(o)", dict(job, glb=f"/glb/{i}.glb", views=[list(v) for v in views.values()]))
            for name, u in zip(views, urls):
                im = Image.open(io.BytesIO(base64.b64decode(u.split(",", 1)[1]))).convert("RGBA")
                if ss > 1:      # LANCZOS on premultiplied colours, so the transparent background does not darken the edges
                    im = im.convert("RGBa").resize((p["WIDTH"], p["HEIGHT"]), Image.LANCZOS).convert("RGBA")
                out[(g, name)] = im
            print(f"rendered {Path(g).name}: {len(urls)} views in {time.time() - t:.0f} s")
        browser.close()
    return out


def finish(im, p):
    """The picture cut to the board plus PADDING (CROP), on its background."""
    if p["CROP"]:
        box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if box:
            pad = p["PADDING"]
            im = im.crop((max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, im.width), min(box[3] + pad, im.height)))
    if p["BACKGROUND"] is None:
        return im
    bg = Image.new("RGBA", im.size, p["BACKGROUND"])
    bg.alpha_composite(im)
    return bg.convert("RGB")


def save(im, path, p):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".webp":
        q = p["QUALITY"]
        im.save(path, method=6, **(dict(lossless=True, quality=100) if q == "lossless" else dict(quality=int(q))))
    else:
        im.save(path, optimize=True)
    print(f"{path}  {path.stat().st_size / 1e6:.2f} MB  {im.width} x {im.height}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--glb", nargs="+", type=Path, help="draw these GLBs instead of every GLB of INPUT_DIR")
    ap.add_argument("--view", nargs=3, type=float, metavar=("X", "Y", "Z"), help="draw this one view instead of VIEWS (degrees)")
    ap.add_argument("-o", "--output", type=Path, help="with one GLB and --view: the picture (.png or .webp)")
    ap.add_argument("--parameters", type=Path, default=HERE / "parameters.py", help="a parameters file (default: parameters.py here)")
    ap.add_argument("--order", choices=ORDERS, help="ORDER the turns are made in")
    ap.add_argument("--projection", choices=("perspective", "orthographic"), help="PROJECTION of the camera")
    ap.add_argument("--format", choices=("png", "webp"), help="FORMAT of the pictures")
    ap.add_argument("--quality", help='QUALITY of a WebP: 1 - 100, or "lossless"')
    ap.add_argument("--width", type=int, help="WIDTH of the picture before it is cut")
    ap.add_argument("--height", type=int, help="HEIGHT of the picture before it is cut")
    ap.add_argument("--supersample", type=int, help="SUPERSAMPLE: drawn this many times larger, then scaled down")
    ap.add_argument("--background", help='BACKGROUND colour such as "#ffffff", or "none" for transparent')
    ap.add_argument("--chromium", help="CHROMIUM: path of a Chromium to use instead of Playwright's own")
    a = ap.parse_args()

    p = load_parameters(a.parameters)
    for key, value in (("ORDER", a.order), ("PROJECTION", a.projection), ("FORMAT", a.format), ("WIDTH", a.width),
                       ("HEIGHT", a.height), ("SUPERSAMPLE", a.supersample), ("CHROMIUM", a.chromium)):
        if value is not None:
            p[key] = value
    if a.quality is not None:
        p["QUALITY"] = a.quality if a.quality == "lossless" else int(a.quality)
    if a.background is not None:
        p["BACKGROUND"] = None if a.background.lower() == "none" else a.background
    p["ORDER"] = p["ORDER"].upper()
    if p["ORDER"] not in ORDERS:
        ap.error(f"ORDER must be one of {', '.join(ORDERS)}")

    glbs = a.glb or sorted((ROOT / p["INPUT_DIR"]).glob("*.glb"))
    if not glbs:
        ap.error(f"no GLB in {ROOT / p['INPUT_DIR']}")
    for g in glbs:
        if not g.is_file():
            ap.error(f"no such file: {g}")
    if a.view:
        views = {"view_" + "_".join(f"{v:g}" for v in a.view): tuple(a.view)}
    else:
        views = dict(p["VIEWS"])
    if a.output and (len(glbs) > 1 or len(views) > 1):
        ap.error("-o needs one GLB and one --view")

    drawn = render([(g, views) for g in glbs], p)
    for (g, name), im in drawn.items():
        out = a.output or ROOT / p["OUTPUT_DIR"] / f"{Path(g).stem}_{name}.{p['FORMAT']}"
        save(finish(im, p), out, p)


if __name__ == "__main__":
    main()
