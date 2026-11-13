"""
parameters/Run_KESE/Run.py - the run: its mode, its folders, and the formats, units and origin of
the files it writes.

Every value here is recorded in parameters.txt next to each output.  Beside this file are the
Verifier's settings (Verifier.py), the presets of kese --for (Presets.py), how many cores work at
once (Parallel.py) and the numerical quality of the geometry (Geometry.py).  The STEP files' own
settings are in Fileformats/Step.py, and those of the GLB, STL and OBJ files in Fileformats/Mesh.py.
Which layers of the board are built is in PCB_elements/Stackup.py, and each element's thickness,
material and colour are in its own file in that folder.
"""

# "simulation" : the physical stack-up, every layer a closed solid at its true height (EM solvers, CAD)
# "visual"     : the board's visible surface only, for web viewers such as <model-viewer>
MODE = "simulation"

# Folders, relative to the folder the command is run from (the working directory, normally Generator/)
INPUT_DIR = "Input"
OUTPUT_DIR = "Output"

# Output file formats, any combination of:
#   "glb"  - binary glTF, one mesh per solid, colours from each element's file  (viewers, Blender)
#   "stl"  - one STL file per solid in an stl/ folder                           (openEMS)
#   "obj"  - Wavefront OBJ, one object per solid, colours in an .mtl            (Blender)
#   "step" - STEP AP214 with one named exact solid per part                     (FreeCAD, gmsh, and
#            through gmsh Elmer and CalculiX)
# "visual" mode can only produce "glb" and "obj" (its skin is a surface, not solids), so a visual
# run names its format: `kese board.kicad_pcb --for viewer`, or `--mode visual --format glb`.
# `kese --for <tool>` sets the mode, formats, units, origin and more for one of these tools (Presets.py).
FILE_FORMAT = ["step"]

# Units of the written files: "mm" (EM solvers, CAD) or "m" (glTF viewers expect metres)
UNITS = "mm"

# Where the origin is:
#   "kicad"  - KiCad's own page origin is kept, so coordinates match the layout and Gerbers: a port
#              is placed where the layout editor says it is
#   "center" - the board outline's centre is at (0, 0) (web viewers)
ORIGIN = "kicad"

# "upright": board in the XY plane, F.Cu facing +Z, Y up, KiCad's top view not mirrored
# "flat"   : board in the XZ plane, F.Cu facing +Y
ORIENTATION = "upright"

# Live "running <stage> ... 1m 23s" line in the terminal while a board is generated
SHOW_PROGRESS = True

# Write materials.json next to the outputs (per solid: material, thickness, er, tan d, conductivity, net, layer)
WRITE_MATERIALS_JSON = True

# KiCad file-format versions this project has been tested with (stage 1, read, warns outside this range)
KICAD_VERSION_MIN = 3                  # the BZR builds of 2013-2014 before KiCad 4 (KiCad 4 files say (version 4), KiCad 5 20171130)
KICAD_VERSION_MAX = 20260206           # KiCad 10
TESTED_COPPER_LAYERS = 8               # stage 1 warns above this many copper layers (the most among the test boards)
