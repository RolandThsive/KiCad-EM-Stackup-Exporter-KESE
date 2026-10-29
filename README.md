# KESE Animation Renderer

A standalone branch for making animations of boards exported by KiCad EM Stackup Exporter (KESE).
It turns GLB files into animated WebPs that loop: the board stood up facing the camera and turned
about the vertical axis, so that its top and its bottom come round in turn.

| Path | What It Is |
|---|---|
| `Input/` | The GLBs to animate |
| `Output/` | The WebPs, named `<name>_<frames>f.webp` |
| `AnimationRenderGenerator/render_animation.py` | The script |
| `AnimationRenderGenerator/parameters.py` | Every setting: frames, rotations per second, size, quality, look, GLBs turned together (stacked or side by side) |
| `AnimationRenderGenerator/render.html` | The three.js page that draws the frames |

## Quick Start

```bash
python -m pip install pillow playwright
python -m playwright install chromium
python AnimationRenderGenerator/render_animation.py               # every GLB in Input/, and TOGETHER, into Output/
python AnimationRenderGenerator/render_animation.py --frames 18 --rps 0.125
python AnimationRenderGenerator/render_animation.py --help        # every option
```

Each frame is shown for `1 / (FRAMES * ROTATIONS_PER_SECOND)` seconds: 36 frames at 0.1 rotations a
second is 278 ms a frame and 10 s a turn.  three.js (MIT licence) is fetched once from the npm
registry into `AnimationRenderGenerator/.three/`.
