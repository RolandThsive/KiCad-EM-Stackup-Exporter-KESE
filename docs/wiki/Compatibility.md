# 20. KiCad And Solver Compatibility

## 20.1 KiCad Files

| KiCad | File format number of the release | Status |
|---|---|---|
| 5 and older | 20171130 (KiCad 5), or no `(version ...)` | read best-effort with a warning; KiCad 5 arcs (`start` = centre, `angle`) are understood |
| 6 | 20211014 | the lower end of the accepted range (`Run.KICAD_VERSION_MIN`); `featureTest/20a_format_kicad6`, written by hand in KiCad 6's format |
| 7 | 20221018 | the two stator examples, `tests/boards/synthetic` and most of `featureTest/`, saved by KiCad 7 itself |
| 8 | 20240108 | `tests/boards/one_layer` and `featureTest/20c_format_kicad8`, small hand-written files in KiCad 8's format |
| 9 | 20241229 | `tests/boards/six_layer` and `featureTest/20d_format_kicad9`, likewise hand-written; per-via `(tenting front back)` is parsed, though no file in the repository uses it; tracks and drawings left bare by the solder mask, `(layers "F.Cu" "F.Mask")` with an optional `(solder_mask_margin ...)`, are read (in `featureTest/08b_copper_graphics_nets`) |
| 10 | 20260206 | the upper end of the accepted range (`Run.KICAD_VERSION_MAX`); five hand-written feature boards (`03b_vias_k10`, `06_padstacks`, `08b_copper_graphics_nets`, `19b_skipped_items_k10`, `20e_format_kicad10`); net names stored directly on items and per-via `(tenting (front yes) (back no))` are read |
| newer | above 20260206 | read best-effort with a warning; raise `Run.KICAD_VERSION_MAX` once checked |

What is read from the file is listed in [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md);
KiCad itself is not needed, only the `.kicad_pcb` file. Footprints are read from the board file
(KiCad embeds them), so libraries are not needed either.

| Board feature | Support |
|---|---|
| Copper layers | boards with 2, 4, 6 and 8 declared copper layers are in the repository (one of them single-sided: tracks only on `F.Cu`, and on `B.Cu` only its two through-hole pads); more than 8 are modelled with a warning; `F.Cu` and `B.Cu` must be declared |
| Stack-up from Board Setup | thickness, type, material, εr, tanδ per dielectric; copper thickness per layer; mask thickness; mask and silk colours; copper finish; edge plating and castellated pads flags |
| Tracks, arc tracks, vias (through, blind, buried, micro) | yes; a track the solder mask leaves bare (KiCad 9 and later) opens the mask over itself, grown by its own mask margin or the board's pad-to-mask clearance |
| Pads: circle, rect, oval, roundrect, trapezoid, custom | yes; round and oval drills, drill offsets (which move the copper, not the hole), per-pad mask margins; chamfered corners are drawn as the plain rounded rectangle |
| Zones | stored fills only (fill in KiCad first); rule areas skipped |
| Graphics: line, arc, circle, rect, polygon (with arc segments), Bézier | on copper, mask and silk layers; outline from `Edge.Cuts`; rectangles with rounded corners (KiCad 10), on every layer and on `Edge.Cuts`; copper drawings the mask leaves bare (KiCad 9 and later) open it as tracks do |
| Text: `gr_text`, `fp_text`, footprint properties | KiCad's stroke font and layout; TrueType faces drawn with the stroke font |
| Text boxes, dimensions, images, groups, tables, generated items; grid items, drill charts and drill maps (KiCad's development version) | skipped; counted when they sit on a copper, silk or mask layer (text boxes, dimensions) or at the top level of the file (images, groups, tables, generated items, grid items, drill charts, drill maps), otherwise left out without a count. For groups and generated items (such as length-tuning patterns) only the record itself is skipped: the tracks, footprints and graphics they hold are read as usual |
| Footprint 3D models | skipped (bare board) |
| Padstacks (KiCad 9 and later: another pad or via shape on the inner layers or on the back) | not modelled: the front shape is used on every layer; counted under `skipped` in `report.txt`, with a warning |
| Backdrills, tertiary drills, counterbores and countersinks of pads and vias; covered, plugged, capped and filled vias, also when the board setup makes them so (KiCad 10) | not modelled: the hole is drilled and plated through its whole span and left open; counted under `skipped` in `report.txt`, with a warning |
| Item kinds KESE does not know, such as the ellipses and elliptical arcs of KiCad's development version (`gr_ellipse`, `fp_ellipse_arc`, ...) | skipped; counted under `skipped` in `report.txt` as `<kind> items (unknown to KESE)`, with a warning |
| Hatched fills of graphics (KiCad 10) | not modelled: the shape is drawn as its outline only |
| Rigid-flex, multiple stack-up regions | not modelled |

## 20.2 Output Formats

| Format | What is in it | Units | Written by |
|---|---|---|---|
| GLB (binary glTF 2.0) | one mesh per part, PBR materials, vertex normals, bufferView targets | `Run.UNITS` (viewers expect m) | `trimesh` |
| STEP AP214 | one named shape per part whose role is in `Run.STEP_WRITE_ROLES`: the part's closed solids from stage 6, one per separate body, with planar faces (curves are polygons, as in the meshes); mask and silk off by default. With `Run.BUILD_WITH_KERNELS = True`: exact B-rep solids built from the prisms, true arcs, fused per part or compounds | `Run.UNITS`: the file declares millimetres or metres, with or without `Run.BUILD_WITH_KERNELS` | KESE (`kese/s7_write/step.py`); `cadquery` / OCCT with kernels |
| STL (binary) | one file per part | `Run.UNITS` | `trimesh` |
| OBJ + MTL | one object per part, normals, colours | `Run.UNITS` | KESE |

Visual mode writes GLB and OBJ only.

## 20.3 Tools

None of these imports has been tried with KESE output yet: the routes follow each tool's
documented import formats and the presets in `parameters/run.py`, and are to be confirmed.
Research underway.

| Tool | Route | Notes |
|---|---|---|
| Ansys HFSS | STEP, mm, KiCad origin (`--for hfss`) | one solid per net and dielectric to assign materials and ports |
| CST Studio Suite | STEP, plus STL per part (`--for cst`) | |
| openEMS / CSXCAD | STL per part, mm (`--for openems`) with `materials.json` | [openEMS Workflow](OpenEMS-Workflow.md) |
| COMSOL, FEKO | STEP, mm | |
| FreeCAD, Fusion, SolidWorks, Onshape | STEP | vias and round pads are faceted, as in the meshes; true cylinders only with `Run.BUILD_WITH_KERNELS = True` and `Run.STEP_EXACT_ARCS` |
| Blender | GLB or OBJ (visual mode for renders) | |
| `<model-viewer>`, three.js | GLB, m, centred (`--for viewer`) | the visual-mode skin is made to avoid z-fighting ([Output Modes](Output-Modes.md)) |
| Thermal / FEA tools reading STL (CalculiX, Elmer with a mesher) | STL per part, mm | closed solids per part (a part can hold several separate bodies); mesh them with the tool's own mesher |

## 20.4 Python And Packages

| | Version |
|---|---|
| Python | 3.12 or later with the pinned versions (`numpy` 2.5.3 and `scipy` 1.18.1 require it); 3.11 with the packages installed unpinned, as `requirements.txt` describes, or through `pyproject.toml` (`requires-python >= 3.11`, not tested); tested on 3.13 |
| `numpy` 2.5.3, `scipy` 1.18.1, `networkx` 3.6.1, `shapely` 2.2.0, `trimesh` 5.1.1, `manifold3d` 3.5.4, `mapbox_earcut` 2.1.0, `rtree` 1.4.1 | the versions in `requirements.txt` |
| `cadquery` 2.8.0, `cadquery-ocp` 7.9.3.1 or later below 8.0 | optional: only for `Run.BUILD_WITH_KERNELS = True` and for the tests that read STEP files back; STEP is written without it |
| `gltf_validator` (Khronos, command line) | optional; used by the Verifier when on the PATH |

Operating systems: anything the packages above run on. Tested on Linux.

| Previous | Next |
|:---|---:|
| [Project Output Organization](Project-Output-Organization.md) | [openEMS Workflow](OpenEMS-Workflow.md) |
