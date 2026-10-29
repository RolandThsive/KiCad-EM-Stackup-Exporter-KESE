"""
StaticImageRenderer/parameters.py - how render_image.py turns GLBs into still pictures.

Most values here can also be given on the command line (python StaticImageRenderer/render_image.py
--help), which wins.  A copy of this file with other values can be passed with --parameters.
"""

# ---- what to make ------------------------------------------------------------------------------

# Folders, relative to the root of this branch (the folder that holds StaticImageRenderer/)
INPUT_DIR = "Input"
OUTPUT_DIR = "Output"

# The pictures made of every GLB in INPUT_DIR, one per entry, named
# OUTPUT_DIR/<GLB name>_<view name>.<FORMAT>.
#
# Each view is the board's rotation in degrees, (X, Y, Z), as Euler angles about the axes of the
# picture: X to the right, Y up, Z out of the picture towards you.  A positive angle turns
# counter-clockwise when that axis points at you (the right-hand rule).  The turns are made in the
# order of ORDER, each about the picture's own fixed axis.  Any orientation at all can be reached.
#
#   (0, 0, 0)     the top of the board facing you, the layout reading as in KiCad's top view
#   (0, 180, 0)   the bottom, turned over left to right (as when a board is turned over in the hand)
#   (180, 0, 0)   the bottom, turned over top to bottom (upside down)
#   (-60, 0, 0)   the top tilted away from you, its far edge at the top of the picture
#   (0, 0, 90)    the top, the layout turned a quarter counter-clockwise
#   (-50, 30, 0)  a three-quarter view: tilted away, then turned to show its left edge
#   (0, 90, 0)    the left edge of the board seen end-on
#   (-90, 0, 0)   the lower edge of the layout seen end-on, the top facing up
VIEWS = {
    "top": (0, 0, 0),
    "bottom": (0, 180, 0),
    "three_quarter": (-50, 30, 0),
}

# The order the three turns are made in: "XYZ" turns about X first, then Y, then Z.  Any of
# "XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX"
ORDER = "XYZ"

# Picture format: "png" (exact, transparent background possible) or "webp" (smaller, see QUALITY)
FORMAT = "png"

# ---- the camera --------------------------------------------------------------------------------

# "perspective"  : as a camera sees it, near parts larger (natural for tilted views)
# "orthographic" : no perspective, sizes true everywhere (flat drawings, top and bottom views)
PROJECTION = "perspective"

# Field of view in degrees, across the height of the picture (perspective only).  Small is close to
# orthographic, large shows more perspective
CAMERA_FOV = 18.0

# ---- the picture -------------------------------------------------------------------------------

# Size of the picture in pixels, before it is cut (see CROP)
WIDTH = 1600
HEIGHT = 1200

# The picture is drawn this many times larger and scaled down, which smooths edges and fine
# detail such as silkscreen text.  1 is fastest, 3 is very clean
SUPERSAMPLE = 3

# Empty space kept around the board, as a fraction of the picture: 0.04 is 4 % on each side.
# The board is made as large as fits inside it
MARGIN = 0.04

# True : the picture is cut to the board, plus PADDING pixels on every side
# False: the picture keeps WIDTH x HEIGHT
CROP = True
PADDING = 30

# Background colour such as "#ffffff", or None for transparent
BACKGROUND = "#ffffff"

# WebP compression when FORMAT is "webp": a number 1 - 100 (90 - 100 for sharp text) or "lossless"
QUALITY = 95

# ---- the look ----------------------------------------------------------------------------------

# Directional lights, fixed to the picture (not to the board, so a turned board is lit the same
# way): where each shines from (x right, y up, z towards you) and how bright
LIGHTS = [{"dir": [-0.5, 1.3, 1.0], "intensity": 2.6},
          {"dir": [0.6, 0.8, -0.4], "intensity": 0.8}]

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

# The pictures are drawn by three.js in a headless Chromium driven by Playwright
#   python -m pip install playwright pillow
#   python -m playwright install chromium
# Path of a Chromium to use instead of Playwright's own, or None
CHROMIUM = None

# three.js is fetched once from the npm registry into StaticImageRenderer/.three/ (MIT licence)
THREE_VERSION = "0.186.1"
