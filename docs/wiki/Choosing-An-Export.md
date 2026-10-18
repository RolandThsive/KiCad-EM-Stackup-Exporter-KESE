# 9. Choosing An Export

The choices to make before a run are the mode, the file formats, the units, the origin and how
copper and dielectrics are grouped. The presets bundle the right combination per tool; `--set`
or the files in `Parameters/` change any single value.

## 9.1 Decision Table

| Need | Choice | Reason |
|---|---|---|
| HFSS | `--for hfss`: simulation, STEP, mm, KiCad origin, copper per net, dielectrics per layer | HFSS imports STEP with one named solid per part; with mm and KiCad's origin a port position read off the layout is the same x and the negated y in the model (KiCad's Y points down, KESE's up) |
| CST | `--for cst`: as hfss plus one STL per part | CST imports STEP; the STL files serve the import route CST falls back to |
| openEMS / CSXCAD | `--for openems`: simulation, STL, mm, KiCad origin, per net, per layer | openEMS has no STEP reader; it imports one STL per material, and `materials.json` carries the properties. See [openEMS Workflow](OpenEMS-Workflow.md) |
| FEKO, COMSOL, mechanical CAD | `--format step --set Run.UNITS=mm` | STEP with exact solids |
| Web viewer, three.js, `<model-viewer>` | `--for viewer`: visual, GLB, metres, centred | glTF viewers expect metres and a model around the origin; the skin does not z-fight |
| Blender, renders | `--mode visual --format glb obj` | OBJ carries an `.mtl` with the colours; GLB carries PBR materials |
| Thermal or FEA tool that reads STL | `--format stl --set Run.UNITS=mm` | one closed STL per part |
| DC-IR / PDN with one solid per copper layer | `--set Run.COPPER_GROUPING=layer` | copper per layer, plating as its own `Plating` part |
| A single body for the whole laminate | `--set Run.DIELECTRIC_GROUPING=merged` | one `Board` solid instead of one per dielectric |

> [!NOTE]
> By default the STEP file holds only the board, copper, plating and finish parts
> (`Run.STEP_WRITE_ROLES`). Add `"mask"`, `"mask_over_copper"` and `"silk"` there when the solver
> must see the solder mask or silkscreen; GLB, STL and OBJ always contain them.

## 9.2 The Presets

`Run_Parameters.PRESETS`; `--for <name>` applies these overrides before any `--set`, and
`parameters.txt` records the preset and every value it changed.

| Preset | `MODE` | `FILE_FORMAT` | `UNITS` | `ORIGIN` | `COPPER_GROUPING` | `DIELECTRIC_GROUPING` | `WRITE_MATERIALS_JSON` |
|---|---|---|---|---|---|---|---|
| `hfss` | simulation | step | mm | kicad | net | layer | True |
| `cst` | simulation | step, stl | mm | kicad | net | layer | True |
| `openems` | simulation | stl | mm | kicad | net | layer | True |
| `viewer` | visual | glb | m | center | (unchanged) | (unchanged) | (unchanged) |

A preset is only a set of overrides: `--for hfss --format step glb` writes both.

## 9.3 Units And Origin

| | `mm` | `m` |
|---|---|---|
| **`Run.UNITS`** | EM solvers and CAD. Dimensions in the file equal the layout's. | glTF viewers (the glTF specification is in metres). The default. |

| | `center` | `kicad` |
|---|---|---|
| **`Run.ORIGIN`** | The outline's bounding-box centre is at (0, 0). Good for viewers. The default. | KiCad's page origin is kept: x equals the layout's x and y is the layout's y negated, since KESE's Y points up. Good for placing ports. |

`Run.ORIENTATION`: `upright` (board in XY, `F.Cu` toward +Z, Y up, KiCad's top view not
mirrored) or `flat` (board in XZ, `F.Cu` toward +Y, the convention of some viewers).

## 9.4 Grouping

| `Run.COPPER_GROUPING` | Parts | Use |
|---|---|---|
| `net` | `Copper_<net>`: all layers and vias of a net in one solid | EM ports, parasitic extraction, per-net anything |
| `layer` | `Copper_F.Cu`, `Copper_In1.Cu`, ... plus `Plating` | layer-by-layer DC or thermal studies |
| `merged` | one `Copper` | a single conductor body |

| `Run.DIELECTRIC_GROUPING` | Parts |
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
| `Run.COPPER_GROUPING` | `net` |
| `Run.DIELECTRIC_GROUPING` | `layer` |
| `Run.WRITE_MATERIALS_JSON` | `True` |
| `Run.VERIFY` or `--verify` | on, for the first export of a new board |

That is the `hfss` preset with `--verify`. Then set the fabricator's values in
`Copper_Parameters.py`, `SolderMask_Parameters.py` and `Board_Parameters.py` before trusting the
results; see [Parameter Reference](Parameter-Reference.md).

| Previous | Next |
|:---|---:|
| [Output Modes](Output-Modes.md) | [Board](Board.md) |
