"""
parameters/presets.py - ready-made settings for the tools KESE writes for.

`kese --for <name>` applies a preset's values before any --set on the command line, and
parameters.txt records the preset and every value it changed.  Each entry is Module.NAME: value,
checked as a --set is; a new entry is a new preset.  None of these routes has been tried with KESE
output yet: they follow each tool's documented import formats.
"""

PRESETS = {
    # STEP in mm with KiCad's origin, for FreeCAD (and its FEM workbench: Elmer, CalculiX): positions
    # read off the layout match the model
    "freecad": {"Run.MODE": "simulation", "Run.FILE_FORMAT": ["step"], "Run.UNITS": "mm", "Run.ORIGIN": "kicad",
                "Copper.COPPER_GROUPING": "net", "Board.DIELECTRIC_GROUPING": "layer", "Run.WRITE_MATERIALS_JSON": True},
    # Elmer (ElmerFEM: electrostatics, magnetics, heat) reads neither STEP nor STL: mesh the STEP file
    # with gmsh (its BooleanFragments make the solids share the faces they touch), turn the .msh into
    # an Elmer mesh with `ElmerGrid 14 2 board.msh`, and set Coordinate Scaling = 0.001, as the mesh
    # is in mm.  No finish: its 80 nm of gold would force the mesh down to cells of that size.
    "elmer": {"Run.MODE": "simulation", "Run.FILE_FORMAT": ["step"], "Run.UNITS": "mm", "Run.ORIGIN": "kicad",
              "Copper.COPPER_GROUPING": "net", "Board.DIELECTRIC_GROUPING": "layer", "Run.WRITE_MATERIALS_JSON": True,
              "Finish.FINISH_ENABLED": False},
    # CalculiX (heat and stress; no electromagnetics): mesh the STEP file with gmsh into an Abaqus
    # .inp, or with CalculiX's own cgx, which reads STEP.  Copper one solid per layer, as there are no
    # ports to tell the nets apart; no finish, as for Elmer.
    "calculix": {"Run.MODE": "simulation", "Run.FILE_FORMAT": ["step"], "Run.UNITS": "mm", "Run.ORIGIN": "kicad",
                 "Copper.COPPER_GROUPING": "layer", "Board.DIELECTRIC_GROUPING": "layer", "Run.WRITE_MATERIALS_JSON": True,
                 "Finish.FINISH_ENABLED": False},
    # openEMS has no STEP reader: one STL per net / dielectric, properties from materials.json
    # (no finish: 80 nm of gold is far below any FDTD mesh cell)
    "openems": {"Run.MODE": "simulation", "Run.FILE_FORMAT": ["stl"], "Run.UNITS": "mm", "Run.ORIGIN": "kicad",
                "Copper.COPPER_GROUPING": "net", "Board.DIELECTRIC_GROUPING": "layer", "Run.WRITE_MATERIALS_JSON": True,
                "Finish.FINISH_ENABLED": False},
    # web viewers (<model-viewer>, three.js): metres, centred, the visible surface only
    "viewer": {"Run.MODE": "visual", "Run.FILE_FORMAT": ["glb"], "Run.UNITS": "m", "Run.ORIGIN": "center"},
    # Blender, for renders: the visible surface in metres, centred, with the solder mask and the
    # silkscreen.  Its importers turn Y-up into Z-up (glTF always; OBJ with its default axes, forward
    # -Z and up Y), so "flat" (F.Cu toward +Y) lands with F.Cu up and KiCad's top view in Blender's.
    # The OBJ's colours and transparency come in its .mtl file.
    "blender_glb": {"Run.MODE": "visual", "Run.FILE_FORMAT": ["glb"], "Run.UNITS": "m", "Run.ORIGIN": "center",
                    "Run.ORIENTATION": "flat", "SolderMask.SOLDER_MASK_ENABLED": True, "Silkscreen.SILKSCREEN_ENABLED": True},
    "blender_obj": {"Run.MODE": "visual", "Run.FILE_FORMAT": ["obj"], "Run.UNITS": "m", "Run.ORIGIN": "center",
                    "Run.ORIENTATION": "flat", "SolderMask.SOLDER_MASK_ENABLED": True, "Silkscreen.SILKSCREEN_ENABLED": True},
}
