# 20. KiCad And Solver Compatibility

## 20.1 KiCad Files

| KiCad | File format number of the release | Status |
|---|---|---|
| 5 and older | 20171130 (KiCad 5), or no `(version ...)` | read best-effort with a warning; KiCad 5 arcs (`start` = centre, `angle`) are understood |
| 6 | 20211014 | inside the accepted range (`Run.KICAD_VERSION_MIN`); no KiCad 6 file in the repository |
| 7 | 20221018 | the two stator examples and `tests/boards/synthetic` |
| 8 | 20240108 | `tests/boards/one_layer`, a small hand-written file with KiCad 8's version number |
| 9 | 20241229 | `tests/boards/six_layer`, likewise hand-written; per-via `(tenting ...)` is parsed, though no file in the repository uses it |
| 10 | 20260206 | inside the accepted range (`Run.KICAD_VERSION_MAX`); no KiCad 10 file in the repository; net names stored directly on items (KiCad 10's form) are read |
| newer | above 20260206 | read best-effort with a warning; raise `Run.KICAD_VERSION_MAX` once checked |

What is read from the file is listed in [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md);
KiCad itself is not needed, only the `.kicad_pcb` file. Footprints are read from the board file
(KiCad embeds them), so libraries are not needed either.

| Board feature | Support |
|---|---|
| Copper layers | boards with 2, 4 and 6 declared copper layers are in the repository (one of them single-sided: tracks only on `F.Cu`, and on `B.Cu` only its two through-hole pads); more than 6 are modelled with a warning; `F.Cu` and `B.Cu` must be declared |
| Stack-up from Board Setup | thickness, type, material, εr, tanδ per dielectric; copper thickness per layer; mask thickness; mask and silk colours; copper finish; edge plating and castellated pads flags |
| Tracks, arc tracks, vias (through, blind, buried, micro) | yes |
| Pads: circle, rect, oval, roundrect, trapezoid, custom | yes; round and oval drills, drill offsets (which move the copper, not the hole), per-pad mask margins; chamfered corners are drawn as the plain rounded rectangle |
| Zones | stored fills only (fill in KiCad first); rule areas skipped |
| Graphics: line, arc, circle, rect, polygon (with arc segments), Bézier | on copper, mask and silk layers; outline from `Edge.Cuts` |
| Text: `gr_text`, `fp_text`, footprint properties | KiCad's stroke font and layout; TrueType faces drawn with the stroke font |
| Text boxes, dimensions, images, groups, tables, generated items | skipped; counted when they sit on a copper, silk or mask layer (text boxes, dimensions) or at the top level of the file (images, groups, tables, generated items), otherwise left out without a count. For groups and generated items (such as length-tuning patterns) only the record itself is skipped: the tracks, footprints and graphics they hold are read as usual |
| Footprint 3D models | skipped (bare board) |
| Rigid-flex, multiple stack-up regions | not modelled |

## 20.2 Output Formats

| Format | What is in it | Units | Written by |
|---|---|---|---|
| GLB (binary glTF 2.0) | one mesh per part, PBR materials, vertex normals, bufferView targets | `Run.UNITS` (viewers expect m) | `trimesh` |
| STEP AP214 | one named shape per part whose role is in `Run.STEP_WRITE_ROLES`: exact B-rep solids built from the prisms, true arcs, fused per part or compounds; mask and silk off by default | mm only in practice: the file always declares millimetres, so with `Run.UNITS = "m"` (the default) the board comes in 1000 times too small; use `--set Run.UNITS=mm` or a preset | `cadquery` / OCCT |
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
| FreeCAD, Fusion, SolidWorks, Onshape | STEP | true cylinders for vias and round pads thanks to `Run.STEP_EXACT_ARCS` |
| Blender | GLB or OBJ (visual mode for renders) | |
| `<model-viewer>`, three.js | GLB, m, centred (`--for viewer`) | the visual-mode skin is made to avoid z-fighting ([Output Modes](Output-Modes.md)) |
| Thermal / FEA tools reading STL (CalculiX, Elmer with a mesher) | STL per part, mm | closed solids per part (a part can hold several separate bodies); mesh them with the tool's own mesher |

## 20.4 Python And Packages

| | Version |
|---|---|
| Python | 3.12 or later with the pinned versions (`numpy` 2.5.3 and `scipy` 1.18.1 require it); 3.11 with the packages installed unpinned, as `requirements.txt` describes, or through `pyproject.toml` (`requires-python >= 3.11`, not tested); tested on 3.13 |
| `numpy` 2.5.3, `scipy` 1.18.1, `networkx` 3.6.1, `shapely` 2.2.0, `trimesh` 5.1.1, `manifold3d` 3.5.4, `mapbox_earcut` 2.1.0, `rtree` 1.4.1 | the versions in `requirements.txt` |
| `cadquery` 2.8.0, `cadquery-ocp` 7.9.3.1 or later below 8.0 | STEP only |
| `gltf_validator` (Khronos, command line) | optional; used by the Verifier when on the PATH |

Operating systems: anything the packages above run on. Tested on Linux.

| Previous | Next |
|:---|---:|
| [Project Output Organization](Project-Output-Organization.md) | [openEMS Workflow](OpenEMS-Workflow.md) |
