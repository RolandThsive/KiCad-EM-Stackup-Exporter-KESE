# KESE Animation Renderer

A standalone branch for making pictures and animations of boards exported by KiCad EM Stackup
Exporter (KESE). Both tools read GLBs from `Input/` and write to `Output/`, and draw with three.js
in a headless Chromium, the way a web viewer shows the board.

| Path | What It Is |
|---|---|
| `Input/` | The GLBs to draw |
| `Output/` | The WebP animations and the still pictures |
| `AnimationRenderGenerator/` | Animations: the board stood up and turned so its top and bottom come round in a loop |
| `StaticImageRenderer/` | Still pictures: the board turned to any X, Y, Z Euler angles |

Each folder holds its script, its `parameters.py` (every setting, with what it does) and the three.js
page it draws with.

## Quick Start

```bash
python -m pip install pillow playwright
python -m playwright install chromium

python AnimationRenderGenerator/render_animation.py     # every GLB in Input/, and TOGETHER, into Output/<name>_<frames>f.webp
python AnimationRenderGenerator/render_animation.py --frames 18 --rps 0.125

python StaticImageRenderer/render_image.py              # every GLB in Input/ in every view of VIEWS, into Output/<name>_<view>.png
python StaticImageRenderer/render_image.py --view -30 20 0
```

Every script takes `--help` for its options. three.js (MIT licence) is fetched once from the npm
registry into each folder's `.three/`.

## Animations

Each frame is shown for `1 / (FRAMES * ROTATIONS_PER_SECOND)` seconds: 36 frames at 0.1 rotations a
second is 278 ms a frame and 10 s a turn. GLBs listed in `TOGETHER` are turned together in one WebP,
one above the other (`LAYOUT = "stacked"`) or side by side.

## Still pictures

A view is the board's rotation in degrees, `(X, Y, Z)`, about the picture's axes: X to the right,
Y up, Z towards you. `(0, 0, 0)` is the top of the board facing you, the layout reading as in
KiCad's top view; `(0, 180, 0)` is the bottom. The turns are made in the order of `ORDER` (X first
by default), and the board is drawn as large as fits, in perspective or orthographic.
