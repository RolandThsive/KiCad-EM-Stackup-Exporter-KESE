# 9. Choosing An Export

The choices to make before a run are the mode, the file formats, the units, the origin and how
copper and dielectrics are grouped. The presets bundle the right combination per tool; `--set`
or the files in `parameters/` change any single value.

## 9.1 Decision Table

| Need | Choice | Reason |
|---|---|---|
| FreeCAD, and Elmer or CalculiX through its FEM workbench | `--for freecad`: simulation, STEP, mm, KiCad origin, copper per net, dielectrics per layer | FreeCAD imports STEP with every part under its own name, and its FEM workbench meshes the solids and runs Elmer or CalculiX; with mm and KiCad's origin a position read off the layout is the same x and the negated y in the model (KiCad's Y points down, KESE's up) |
| Elmer (ElmerFEM) | `--for elmer`: simulation, STEP, mm, KiCad origin, copper per net, dielectrics per layer, no finish | Elmer reads neither STEP nor STL: gmsh meshes the STEP file and `ElmerGrid 14 2 board.msh` turns the mesh into Elmer's; set `Coordinate Scaling = 0.001`, the mesh being in mm. See [9.2](#92-the-presets) |
| CalculiX (heat and stress) | `--for calculix`: as `elmer`, copper per layer | CalculiX has no electromagnetics; gmsh meshes the STEP file into an Abaqus `.inp`, or CalculiX's own cgx reads the STEP file |
| openEMS / CSXCAD | `--for openems`: simulation, STL, mm, KiCad origin, per net, per layer | openEMS has no STEP reader; it imports STL files, each into one material, and `materials.json` carries the properties. See [openEMS Workflow](OpenEMS-Workflow.md) |
| gmsh, other CAD | `--format step --set Run.UNITS=mm` | STEP with every part as closed solids, holes and round edges as true circles and cylinders (`Step.STEP_EXACT_ARCS`) |
| Web viewer, three.js, `<model-viewer>` | `--for viewer`: visual, GLB, metres, centred | glTF viewers expect metres and a model around the origin; the skin does not z-fight |
| Blender, renders | `--for blender_glb` or `--for blender_obj`: visual, metres, centred, `flat`, with the solder mask and silkscreen | GLB carries PBR materials; OBJ carries an `.mtl` with the colours and transparency, which Blender reads. Blender's importers turn Y-up into Z-up, so `flat` lands with `F.Cu` up |
| Thermal or FEA tool that reads STL | `--format stl --set Run.UNITS=mm` | one closed STL per part |
| DC-IR / PDN with one solid per copper layer | `--set Copper.COPPER_GROUPING=layer` | copper per layer, plating as its own `Plating` part |
| A single body for the whole laminate | `--set Board.DIELECTRIC_GROUPING=merged` | one `Board` solid instead of one per dielectric |

> [!NOTE]
> Every format and both modes hold the same parts: the ones switched on with
> `Board.BOARD_ENABLED`, `Copper.COPPER_ENABLED` (copper and plated barrels),
> `Finish.FINISH_ENABLED`, `SolderMask.SOLDER_MASK_ENABLED` and `Silkscreen.SILKSCREEN_ENABLED`,
> the board, copper and finish on by default, the solder mask and silkscreen off. Switch the mask
> and silkscreen on when the solver or the render must see them:
> `--set SolderMask.SOLDER_MASK_ENABLED=True --set Silkscreen.SILKSCREEN_ENABLED=True`. A STEP file
> with them is 1.4 to 1.9 times as big (the PCIe card in `Input/`, in mm: 151 MB and 1,024 solids
> against 81 MB and 788 solids).

## 9.2 The Presets

`Presets.PRESETS` (in `parameters/presets.py`); `--for <name>` applies these overrides before any `--set`, and
`parameters.txt` records the preset and every value it changed. Each name in a preset is checked as a
`--set` is, and a new entry in the file is a new preset. None of these routes has been tried with
KESE output yet: they follow each tool's documented import formats.

| Preset | `MODE` | `FILE_FORMAT` | `UNITS` | `ORIGIN` | `COPPER_GROUPING` | `DIELECTRIC_GROUPING` | `WRITE_MATERIALS_JSON` | Also |
|---|---|---|---|---|---|---|---|---|
| `freecad` | simulation | step | mm | kicad | net | layer | True | |
| `elmer` | simulation | step | mm | kicad | net | layer | True | no finish |
| `calculix` | simulation | step | mm | kicad | layer | layer | True | no finish |
| `openems` | simulation | stl | mm | kicad | net | layer | True | no finish |
| `viewer` | visual | glb | m | center | (unchanged) | (unchanged) | (unchanged) | |
| `blender_glb` | visual | glb | m | center | (unchanged) | (unchanged) | (unchanged) | `ORIENTATION` flat, solder mask and silkscreen on |
| `blender_obj` | visual | obj | m | center | (unchanged) | (unchanged) | (unchanged) | `ORIENTATION` flat, solder mask and silkscreen on |

"No finish" is `Finish.FINISH_ENABLED = False`: 80 nm of gold (the default ENIG's) is far below any
FDTD cell of openEMS, and would force the volume mesh of Elmer or CalculiX down to cells of that size.

- **Elmer**: neither ElmerGrid nor ElmerSolver reads STEP or STL. Mesh the STEP file with gmsh, whose
  `BooleanFragments` make the touching solids share their faces, export the mesh in gmsh's format, and
  convert it with `ElmerGrid 14 2 board.msh -autoclean`. Elmer takes coordinates as they come, so with a
  mesh in mm set `Coordinate Scaling = 0.001` (Model > Setup in ElmerGUI) for SI units. gmsh reads STEP
  in mm unless `Geometry.OCCTargetUnit` says otherwise.
- **CalculiX**: gmsh meshes the STEP file and saves an Abaqus `.inp` (`Mesh.Format = 39`), which `ccx`
  runs; or CalculiX's own pre-processor cgx imports the STEP file. CalculiX does heat and stress, not
  electromagnetics; its units are the ones you keep consistent (the mesh is in mm).
- **Blender**: File > Import > glTF 2.0 for `blender_glb`, File > Import > Wavefront (.obj) for
  `blender_obj`. Both importers turn the files' Y-up into Blender's Z-up (glTF always; OBJ with its default
  axes, forward −Z and up Y), so the `flat` board lies with `F.Cu` up and KiCad's top view in Blender's top
  view. glTF is in metres, which Blender takes as its unit; the OBJ importer's scale is 1, so the OBJ is
  written in metres too.

A preset is only a set of overrides: `--for freecad --format step glb` writes both.

## 9.3 Units And Origin

| | `mm` | `m` |
|---|---|---|
| **`Run.UNITS`** | EM solvers and CAD. Dimensions in the file equal the layout's. Use it for STEP: the file declares the units it is written in, but CAD tools and solvers are set up in millimetres. | glTF viewers (the glTF specification is in metres). The default. |

| | `center` | `kicad` |
|---|---|---|
| **`Run.ORIGIN`** | The outline's bounding-box centre is at (0, 0). Good for viewers. The default. | KiCad's page origin is kept: x equals the layout's x and y is the layout's y negated, since KESE's Y points up. Good for placing ports. |

`Run.ORIENTATION`: `upright` (board in XY, `F.Cu` toward +Z, Y up, KiCad's top view not
mirrored) or `flat` (board in XZ, `F.Cu` toward +Y, the convention of some viewers, and what Blender's
importers turn into `F.Cu` up). The Verifier's checks work in either.

## 9.4 Grouping

| `Copper.COPPER_GROUPING` | Parts | Use |
|---|---|---|
| `net` | `Copper_<net>`: all layers and vias of a net in one solid | EM ports, parasitic extraction, per-net anything |
| `layer` | `Copper_F.Cu`, `Copper_In1.Cu`, ... plus `Plating` | layer-by-layer DC or thermal studies |
| `merged` | one `Copper` | a single conductor body |

| `Board.DIELECTRIC_GROUPING` | Parts |
|---|---|
| `layer` | `Board_dielectric 1`, `Board_dielectric 2`, ... each with its own εr and tanδ |
| `merged` | one `Board` (the first dielectric's material) |

## 9.5 Recommended Combination

For an EM simulation of a board in the solver's own units:

| Setting | Value |
|---|---|
| `Run.MODE` | `simulation` |
| `Run.FILE_FORMAT` | `["step"]` (or `["stl"]` for openEMS) |
| `Run.UNITS` | `mm` |
| `Run.ORIGIN` | `kicad` |
| `Copper.COPPER_GROUPING` | `net` |
| `Board.DIELECTRIC_GROUPING` | `layer` |
| `Run.WRITE_MATERIALS_JSON` | `True` |
| `Verifier.VERIFY` or `--verify` | on, for the first export of a new board |

That is the `freecad` preset with `--verify`. Then set the fabricator's values in
`parameters/copper.py`, `parameters/solder_mask.py` and `parameters/board.py` before trusting the
results; see [Parameter Reference](Parameter-Reference.md).

| Previous | Next |
|:---|---:|
| [Output Modes](Output-Modes.md) | [Board](Board.md) |
