"""
AnimationRenderGenerator/parameters.py - how render_animation.py turns GLBs into turning WebPs.

Most values here can also be given on the command line (python AnimationRenderGenerator/render_animation.py
--help), which wins.  A copy of this file with other values can be passed with --parameters.
"""

# ---- what to make ------------------------------------------------------------------------------

# Folders, relative to the root of this branch (the folder that holds AnimationRenderGenerator/)
INPUT_DIR = "Input"
OUTPUT_DIR = "Output"

# True: every GLB in INPUT_DIR is turned on its own, into OUTPUT_DIR/<name>_<FRAMES>f.webp
SINGLE = True

# GLBs of INPUT_DIR turned together in one WebP, in the order given (top to bottom, or left to
# right, see LAYOUT), named OUTPUT_DIR/<name>_<FRAMES>f.webp.  An empty dict makes none
TOGETHER = {
    "rf_module_blue_visual_and_simulation": ["rf_module_blue_visual.glb", "rf_module_blue_simulation.glb"],
}

# ---- the turn ----------------------------------------------------------------------------------

# Pictures in one full turn.  More frames is smoother and a bigger file: 12 steps of 30 degrees,
# 18 of 20, 36 of 10, 72 of 5
FRAMES = 36

# Speed in full turns a second.  0.1 is one turn in 10 s, the top and the bottom each shown for
# about 5 s.  Each frame is shown for 1 / (FRAMES * ROTATIONS_PER_SECOND) s
ROTATIONS_PER_SECOND = 0.1

# "right": the near edge of the board moves to the right (seen from above, counter-clockwise)
# "left" : the near edge moves to the left
DIRECTION = "right"

# Where the turn starts, in degrees: 0 is the top facing the camera, 180 the bottom.  When a step
# would land on the board seen exactly edge-on (a thin line), every frame is moved on by half a
# step, so no frame is wasted on the edge
START_ANGLE = 0.0

# ---- the camera --------------------------------------------------------------------------------

# The board is stood up (its top facing the camera, the layout reading upright) and turned about the
# vertical axis through its centre.  The camera looks slightly down on it, by this many degrees
CAMERA_ELEVATION = 12.0

# Field of view in degrees, across the height of the picture.  Small is close to a flat
# (orthographic) look, large shows more perspective
CAMERA_FOV = 18.0

# ---- the picture -------------------------------------------------------------------------------

# Size of one board's panel in the WebP, in pixels.  The height is cut afterwards to the band the
# board fills in any frame (see CROP)
WIDTH = 1000
HEIGHT = 750

# Every frame is drawn this many times larger and scaled down, which smooths edges and fine
# detail such as silkscreen text.  1 is fastest, 3 is very clean, 4 rarely shows a difference
SUPERSAMPLE = 3

# Empty space kept around the board, as a fraction of the panel: 0.04 is 4 % on each side
MARGIN = 0.04

# True : the height is cut to the rows the board draws in, in any frame, plus PADDING pixels
# False: the panel keeps HEIGHT
CROP = True
PADDING = 30

# Background colour, or None for transparent (WebP keeps the transparency)
BACKGROUND = "#ffffff"

# WebP compression: a number 1 - 100 (lossy, 90 - 100 for sharp text) or "lossless" (largest files)
QUALITY = 95

# 0 (fast) - 6 (slowest, smallest file for the same quality)
METHOD = 6

# ---- several GLBs together ---------------------------------------------------------------------

# "stacked": one above the other, each panel WIDTH wide (the board takes the most room)
# "side"   : side by side, the WebP as many panels wide
LAYOUT = "stacked"

# Titles over each panel: a list with one entry per GLB, "auto" (Visual mode / Simulation mode
# from the GLB's folder or name, else its file name), or None for no titles
TITLES = "auto"

# A smaller line under each title: a list with one entry per GLB, "auto" or None
SUBTITLES = "auto"

# A thin line between the panels
DIVIDER = True

# ---- the look ----------------------------------------------------------------------------------

# Directional lights: where each shines from (x right, y away from the camera, z up) and how bright
LIGHTS = [{"dir": [-0.5, -1.0, 1.3], "intensity": 2.6},
          {"dir": [0.6, 0.4, 0.8], "intensity": 0.8}]

# Light from every direction, so the side away from the lights is not black
AMBIENT = 0.5

# Copper and the finishes are drawn with this metalness and roughness (1 = mirror-like metal),
# None keeps the GLB's own.  Slightly less than a real mirror reads better on a white page
METALNESS = 0.45
ROUGHNESS = 0.45

# Reflection of a soft studio room: on metals, and on everything else (mask, laminate, silkscreen;
# kept low so their colours do not wash out)
REFLECTION_METAL = 0.6
REFLECTION_OTHER = 0.05

# ---- the renderer ------------------------------------------------------------------------------

# The frames are drawn by three.js in a headless Chromium driven by Playwright
#   python -m pip install playwright pillow
#   python -m playwright install chromium
# Path of a Chromium to use instead of Playwright's own, or None
CHROMIUM = None

# three.js is fetched once from the npm registry into AnimationRenderGenerator/.three/ (MIT licence)
THREE_VERSION = "0.186.1"
