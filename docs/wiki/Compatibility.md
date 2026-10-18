# 20. KiCad And Solver Compatibility

## 20.1 KiCad Files

| KiCad | File format number | Status |
|---|---|---|
| 5 and older | none, or below 20211014 | read best-effort with a warning; KiCad 5 arcs (`start` = centre, `angle`) are understood |
| 6 | 20211014 ... | tested range starts here |
| 7 | 2022xxxx | tested (the two stator examples are 20221018) |
| 8 | 20240108 ... | tested (`Tests/boards/one_layer`) |
| 9 | 20241229 ... | tested (`Tests/boards/six_layer`); per-via `(tenting ...)` read |
| 10 | up to 20260206 | tested (the XIAO example, 20260206); net names stored on items read |
| newer | above 20260206 | read best-effort with a warning; raise `Run.KICAD_VERSION_MAX` once checked |

What is read from the file is listed in [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md);
KiCad itself is not needed, only the `.kicad_pcb` file. Footprints are read from the board file
(KiCad embeds them), so libraries are not needed either.

| Board feature | Support |
|---|---|
| Copper layers | 1 to 6 tested; more are modelled with a warning (`F.Cu` and `B.Cu` must exist; a one-layer board declares both) |
| Stack-up from Board Setup | thickness, type, material, εr, tanδ per dielectric; copper thickness per layer; mask thickness; mask and silk colours; copper finish; edge plating and castellated pads flags |
| Tracks, arc tracks, vias (through, blind, buried, micro) | yes |
| Pads: circle, rect, oval, roundrect, trapezoid, custom | yes; round and oval drills, drill offsets, per-pad mask margins |
| Zones | stored fills only (fill in KiCad first); rule areas skipped |
| Graphics: line, arc, circle, rect, polygon (with arc segments), Bézier | on copper, mask and silk layers; outline from `Edge.Cuts` |
| Text: `gr_text`, `fp_text`, footprint properties | KiCad's stroke font and layout; TrueType faces drawn with the stroke font |
| Text boxes, dimensions, images, groups, tables, generated items | skipped and counted |
| Footprint 3D models | skipped (bare board) |
| Rigid-flex, multiple stack-up regions | not modelled |

## 20.2 Output Formats

| Format | What is in it | Units | Written by |
|---|---|---|---|
| GLB (binary glTF 2.0) | one mesh per part, PBR materials, vertex normals, bufferView targets | `Run.UNITS` (viewers expect m) | `trimesh` |
| STEP AP214 | one named shape per written role: exact B-rep solids built from the prisms, true arcs, fused per part or compounds; mask and silk off by default | `Run.UNITS` (CAD expects mm) | `cadquery` / OCCT |
| STL (binary) | one file per part | `Run.UNITS` | `trimesh` |
| OBJ + MTL | one object per part, normals, colours | `Run.UNITS` | KESE |

Visual mode writes GLB and OBJ only.

## 20.3 Tools

Imports marked "checked" were done with KESE output; the others follow the tool's documented
import formats and are to be confirmed. Research underway.

| Tool | Route | Notes |
|---|---|---|
| Ansys HFSS | STEP, mm, KiCad origin (`--for hfss`) | one solid per net and dielectric to assign materials and ports |
| CST Studio Suite | STEP, plus STL per part (`--for cst`) | |
| openEMS / CSXCAD | STL per part, mm (`--for openems`) with `materials.json` | [openEMS Workflow](OpenEMS-Workflow.md) |
| COMSOL, FEKO | STEP, mm | |
| FreeCAD, Fusion, SolidWorks, Onshape | STEP | true cylinders for vias and round pads thanks to `Run.STEP_EXACT_ARCS` |
| Blender | GLB or OBJ (visual mode for renders) | |
| `<model-viewer>`, three.js, Babylon.js | GLB, m, centred (`--for viewer`) | checked: the visual-mode skin does not z-fight; the Khronos validator reports no hints with the default export settings |
| Thermal / FEA tools reading STL (CalculiX, Elmer with a mesher) | STL per part, mm | one closed solid per part; mesh them with the tool's own mesher |

## 20.4 Python And Packages

| | Version |
|---|---|
| Python | 3.10 or later; 3.11 or later for STEP (`cadquery` 2.8 needs it); tested on 3.13 |
| `numpy` 2.5.3, `scipy` 1.18.1, `networkx` 3.6.1, `shapely` 2.2.0, `trimesh` 5.1.1, `manifold3d` 3.5.4, `mapbox_earcut` 2.1.0, `rtree` 1.4.1 | the versions in `requirements.txt`; wheels for Python 3.11 to 3.14 on Windows, Linux and macOS |
| `cadquery` 2.8.0, `cadquery-ocp` 7.9.x | STEP only |
| `gltf_validator` (Khronos, command line) | optional; used by the Verifier when on the PATH |

Operating systems: anything the packages above run on. Tested on Linux.

| Previous | Next |
|:---|---:|
| [Project Output Organization](Project-Output-Organization.md) | [openEMS Workflow](OpenEMS-Workflow.md) |
