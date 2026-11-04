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
#   "stl"  - one STL file per solid in an stl/ folder                           (openEMS, CalculiX, Elmer)
#   "obj"  - Wavefront OBJ, one object per solid                                (viewing, Blender)
#   "step" - STEP AP214 with one named exact solid per part                     (FreeCAD, gmsh)
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

# Live "running <stage> ... 1m 23s" line in the terminal while a board is generated
SHOW_PROGRESS = True

# Run the Verifier after generation (adds about 1-3 s per board on the example boards, more on
# dense boards). Results go in report.txt.
VERIFY = False
VERIFY_RAYS = 3000                     # vertical rays the Verifier casts through a visual model to test its surfaces

# Write materials.json next to the outputs (per solid: material, thickness, er, tan d, conductivity, net, layer)
WRITE_MATERIALS_JSON = True

# Mesh export (glb / stl / obj)
EXPORT_INCLUDE_NORMALS = True
EXPORT_SET_BUFFERVIEW_TARGETS = True   # keeps the Khronos glTF validator report free of hints
SMOOTH_SHADE_ANGLE_DEG = 25.0          # edges sharper than this stay crisp; cylinders shade smooth

# STEP export
#
# Every part is written as the closed solid stage 6 built, one body per connected piece, with its
# flat faces and walls as they are (curves are polygons, as in the meshes), unless STEP_EXACT_ARCS.
#
# STEP_EXACT_ARCS - write circles and arcs as true curves (KESE's own STEP writer, no CAD kernel).
#   Where the outline of a part runs through vertices that lie on one circle (holes, vias, round
#   pads, track ends, arc tracks, round outlines), their chords become one CIRCLE edge and the walls
#   on them one CYLINDRICAL_SURFACE face, at every height alike, except where another edge at that
#   height passes closer to the vertices than the arc bulges out from them (a sliver of a few µm),
#   which the arc would cross.  Smaller files and true cylinders for CAD and EM solvers; every
#   other edge stays a line and every other face a plane.  Meshes (GLB / STL / OBJ) are unchanged.
STEP_EXACT_ARCS = True
STEP_ARC_FIT_TOLERANCE_MM = 0.0002     # vertices within this of one circle form an arc (2 x the snap grid)
STEP_ARC_MIN_POINTS = 5                # at least this many vertices in a run
STEP_ARC_MIN_SWEEP_DEG = 10.0          # and turning at least this far
STEP_ARC_MAX_TURN_DEG = 30.0           # but at most this far at one vertex: a polygon with fewer than 12
                                       # sides (an octagonal pad, a square) is a polygon, not a circle
#
# Which parts are made, in every format and mode alike, is set by one switch per kind of part:
#   Board.BOARD_ENABLED, Copper.COPPER_ENABLED (copper and plated barrels), Finish.FINISH_ENABLED,
#   SolderMask.SOLDER_MASK_ENABLED, Silkscreen.SILKSCREEN_ENABLED; mask and silk are off by default.
#   STEP with mask and silk is bigger (the PCIe card in Input/, in mm: 150 MB and 1,024 solids written
#   in 7.1 s, against 80 MB and 788 solids in 4.9 s without them).

# KiCad file-format versions this project has been tested with (stage 1, read, warns outside this range)
KICAD_VERSION_MIN = 3                  # the BZR builds of 2013-2014 before KiCad 4 (KiCad 4 files say (version 4), KiCad 5 20171130)
KICAD_VERSION_MAX = 20260206           # KiCad 10
TESTED_COPPER_LAYERS = 8               # stage 1 warns above this many copper layers (the most among the test boards)

# Presets: `kese --for <name>` applies these overrides before any --set on the command line, and
# parameters.txt records the preset and every value it changed.  Each entry is Module.NAME: value.
PRESETS = {
    # STEP in mm with KiCad's origin, for FreeCAD (and its FEM workbench: Elmer, CalculiX): positions
    # read off the layout match the model
    "freecad": {"Run.MODE": "simulation", "Run.FILE_FORMAT": ["step"], "Run.UNITS": "mm", "Run.ORIGIN": "kicad",
                "Copper.COPPER_GROUPING": "net", "Board.DIELECTRIC_GROUPING": "layer", "Run.WRITE_MATERIALS_JSON": True},
    # openEMS has no STEP reader: one STL per net / dielectric, properties from materials.json
    # (no finish: 80 nm of gold is far below any FDTD mesh cell)
    "openems": {"Run.MODE": "simulation", "Run.FILE_FORMAT": ["stl"], "Run.UNITS": "mm", "Run.ORIGIN": "kicad",
                "Copper.COPPER_GROUPING": "net", "Board.DIELECTRIC_GROUPING": "layer", "Run.WRITE_MATERIALS_JSON": True,
                "Finish.FINISH_ENABLED": False},
    # web viewers (<model-viewer>, three.js): metres, centred, the visible surface only
    "viewer": {"Run.MODE": "visual", "Run.FILE_FORMAT": ["glb"], "Run.UNITS": "m", "Run.ORIGIN": "center"},
}
