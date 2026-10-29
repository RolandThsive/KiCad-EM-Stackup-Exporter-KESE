"""
parameters/run.py - what to make, where, and in which formats.

Every value here is recorded in parameters.txt next to each output.
"""

# "simulation" : the physical stack-up, every layer a closed solid at its true height (EM solvers, CAD)
# "visual"     : the board's visible surface only, for web viewers such as <model-viewer>
MODE = "simulation"

# Folders, relative to the folder the command is run from (the working directory, normally Generator/)
INPUT_DIR = "Input"
OUTPUT_DIR = "Output"

# Output file formats, any combination of:
#   "glb"  - binary glTF, one mesh per solid, materials from parameters/color.py (viewing)
#   "stl"  - one STL file per solid in an stl/ folder                           (openEMS, CST)
#   "obj"  - Wavefront OBJ, one object per solid                                (viewing, Blender)
#   "step" - STEP AP214 with one named exact solid per part                     (HFSS, CST, FEKO, COMSOL)
# "visual" mode can only produce "glb" and "obj" (its skin is a surface, not solids).
FILE_FORMAT = ["glb"]

# Units of the written files: "mm" (EM solvers, CAD) or "m" (glTF viewers expect metres)
UNITS = "m"

# Where the origin is:
#   "center" - the board outline's centre is at (0, 0)
#   "kicad"  - KiCad's own page origin is kept, so coordinates match the layout and Gerbers
ORIGIN = "center"

# "upright": board in the XY plane, F.Cu facing +Z, Y up, KiCad's top view not mirrored
# "flat"   : board in the XZ plane, F.Cu facing +Y
ORIENTATION = "upright"

# Copper grouping in "simulation" mode:
#   "net"    - one solid per net (all its layers and vias joined)  <- what EM ports need
#   "layer"  - one solid per copper layer, plating separate
#   "merged" - all copper in one solid
COPPER_GROUPING = "net"

# Dielectric grouping in "simulation" mode:
#   "layer"  - one solid per stackup dielectric (core / prepreg), each with its own material
#   "merged" - the whole laminate as one solid
DIELECTRIC_GROUPING = "layer"

# How the solids of "simulation" mode are built:
#   False - the boundary of every part is found in 2D from its prisms (the material between two
#           heights, the faces at every height) and written as it is: the same faces go into the
#           meshes and, without a CAD kernel, into the STEP file
#   True  - the old way: every prism extruded and joined by Manifold; STEP solids built and fused
#           by OpenCascade (slow on dense boards)
BUILD_WITH_KERNELS = False

# How many threads stage 6 works with without a kernel (the 2D geometry library runs outside
# Python's lock): parts built at once in "simulation" mode, slices in "visual" mode.  0 = one per
# processor core
WORKERS = 0

# Live "running <stage> ... 1m 23s" line in the terminal while a board is generated
SHOW_PROGRESS = True

# Run the Verifier after generation (adds about 2-4 s per board on the example boards, more on
# dense boards). Results go in report.txt.
VERIFY = False

# Write materials.json next to the outputs (per solid: material, thickness, er, tan d, conductivity, net, layer)
WRITE_MATERIALS_JSON = True

# Mesh export (glb / stl / obj)
EXPORT_INCLUDE_NORMALS = True
EXPORT_SET_BUFFERVIEW_TARGETS = True   # keeps the Khronos glTF validator report free of hints
SMOOTH_SHADE_ANGLE_DEG = 25.0          # edges sharper than this stay crisp; cylinders shade smooth

# STEP export
#
# Without a kernel (BUILD_WITH_KERNELS = False) every part is written as the closed solid stage 6
# built, one body per connected piece, with its flat faces and walls as they are: STEP_EXACT_ARCS
# and STEP_FUSE_ROLES below only apply to the OpenCascade writer (BUILD_WITH_KERNELS = True).
#
# STEP_EXACT_ARCS - write circles and arcs as true curves.  The 2D geometry is built from
#   polylines (every curve faceted to parameters/geometry.py); in the STEP file, runs of vertices
#   that lie on one circle (vias, round pads, round outlines, track ends, arc tracks) are written
#   as exact circular arcs instead, except where another outline passes closer to the vertices
#   than the arc bulges out from them (a sliver of a few µm), which the arc would cross.
#   Smaller files, true cylinders for CAD.  Meshes are unchanged.
STEP_EXACT_ARCS = True
STEP_ARC_FIT_TOLERANCE_MM = 0.0002     # vertices within this of one circle form an arc (2 x the snap grid)
STEP_ARC_MIN_POINTS = 5                # at least this many vertices in a run
#
# Every part has a "role".  The roles are:
#   "board"            the laminate: one part per dielectric (core / prepreg), e.g. "Board_dielectric 1"
#   "copper"           copper of the layers, grouped per COPPER_GROUPING, e.g. "Copper_GND"
#   "plating"          via / plated-hole barrels (its own part only when COPPER_GROUPING = "layer";
#                      with "net" or "merged" the barrels belong to the copper parts)
#   "finish"           surface finish metals on bare copper, e.g. "Top Finish Gold" (if FINISH_ENABLED)
#   "mask"             solder mask on laminate and the walls beside traces: "Top Solder Mask", "Bottom Solder Mask"
#   "mask_over_copper" the mask lying on top of copper (a separate part only in "visual" mode; in
#                      "simulation" mode these prisms are part of the "Top/Bottom Solder Mask" parts)
#   "silk"             silkscreen ink: "Top Silkscreen", "Bottom Silkscreen"
#
# STEP_WRITE_ROLES - which roles are written to the STEP file at all.
#   Each written part is made of closed solids.  Mask and silk are left out by default: they are
#   many more solids, which make the file 1.5 to 1.6 times as big (the PCIe card in Input/, in mm:
#   348 MB and 320 solids written in 8.8 s instead of 215 MB and 84 solids in 5.6 s; with
#   BUILD_WITH_KERNELS the difference is bigger still).  GLB / STL / OBJ always contain them.  To
#   write everything:
#   STEP_WRITE_ROLES = ["board", "copper", "plating", "finish", "mask", "mask_over_copper", "silk"]
STEP_WRITE_ROLES = ["board", "copper", "plating", "finish"]
#
# STEP_FUSE_ROLES - which of the written roles are fused into ONE solid per part.
#   fused    : all pieces of the part (e.g. a net's traces on every layer plus its vias) become a
#              single body.  This is what EM solvers need for conductors and dielectrics.  Slow on
#              parts with many pieces (the GND net of a dense board takes about a minute).
#   not fused: the part is a compound of closed solids that touch but are not merged (e.g. the
#              flat mask sheet plus a block over each trace).  Fast; fine for CAD viewing; a
#              solver sees internal boundaries between the pieces.
#   Roles listed here but not in STEP_WRITE_ROLES are ignored.
STEP_FUSE_ROLES = ["board", "copper", "plating", "finish"]

# KiCad file-format versions this project has been tested with (stage 1, read, warns outside this range)
KICAD_VERSION_MIN = 20211014           # KiCad 6
KICAD_VERSION_MAX = 20260206           # KiCad 10

# Presets: `kese --for <name>` applies these overrides before any --set on the command line, and
# parameters.txt records the preset and every value it changed.  Each entry is Module.NAME: value.
PRESETS = {
    # STEP in mm with KiCad's origin: port and probe positions read off the layout match the model
    "hfss": {"Run.MODE": "simulation", "Run.FILE_FORMAT": ["step"], "Run.UNITS": "mm", "Run.ORIGIN": "kicad",
             "Run.COPPER_GROUPING": "net", "Run.DIELECTRIC_GROUPING": "layer", "Run.WRITE_MATERIALS_JSON": True},
    # as hfss, plus one STL per part for the import route CST falls back to
    "cst": {"Run.MODE": "simulation", "Run.FILE_FORMAT": ["step", "stl"], "Run.UNITS": "mm", "Run.ORIGIN": "kicad",
            "Run.COPPER_GROUPING": "net", "Run.DIELECTRIC_GROUPING": "layer", "Run.WRITE_MATERIALS_JSON": True},
    # openEMS has no STEP reader: one STL per net / dielectric, properties from materials.json
    "openems": {"Run.MODE": "simulation", "Run.FILE_FORMAT": ["stl"], "Run.UNITS": "mm", "Run.ORIGIN": "kicad",
                "Run.COPPER_GROUPING": "net", "Run.DIELECTRIC_GROUPING": "layer", "Run.WRITE_MATERIALS_JSON": True},
    # web viewers (<model-viewer>, three.js): metres, centred, the visible surface only
    "viewer": {"Run.MODE": "visual", "Run.FILE_FORMAT": ["glb"], "Run.UNITS": "m", "Run.ORIGIN": "center"},
}
