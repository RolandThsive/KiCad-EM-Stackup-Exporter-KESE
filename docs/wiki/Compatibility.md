# 21. KiCad And Solver Compatibility

## 21.1 KiCad Files

| KiCad | File format number of the release | Status |
|---|---|---|
| older | no `(version ...)` | read best-effort with a warning, as format 20201115, as KiCad reads such a file |
| BZR builds of 2013-2014 | 3 | the lower end of the tested range (`Run.KICAD_VERSION_MIN`); 6 public boards; the layer names those builds wrote in Italian, Polish and French are understood |
| 4 | 4 | 19 public boards saved by KiCad 4 |
| 5 | 20171130 | 25 public boards saved by KiCad 5; KiCad 5 arcs (`start` = centre, `angle`), zones filled with segments only (`fill_segments`), net names written with the old overbar (`~RESET~`) |
| 6 | 20211014 | 25 public boards, among them development builds of 6 (formats 20201116 to 20210925, read as KiCad 6); `featureTest/20a_format_kicad6`, written by hand in KiCad 6's format |
| 7 | 20221018 | 25 public boards; the three example boards of `Input/`, `tests/boards/synthetic` and most of `featureTest/`, saved by KiCad 7 itself |
| 8 | 20240108 | 25 public boards; `tests/boards/one_layer` and `featureTest/20c_format_kicad8`, small hand-written files in KiCad 8's format |
| 9 | 20241229 | 25 public boards; `tests/boards/six_layer` and `featureTest/20d_format_kicad9`, likewise hand-written; per-via `(tenting front back)` is parsed; tracks and drawings left bare by the solder mask, `(layers "F.Cu" "F.Mask")` with an optional `(solder_mask_margin ...)`, are read (in `featureTest/08b_copper_graphics_nets`) |
| 10 | 20260206 | the upper end of the tested range (`Run.KICAD_VERSION_MAX`); five hand-written feature boards (`03b_vias_k10`, `06_padstacks`, `08b_copper_graphics_nets`, `19b_skipped_items_k10`, `20e_format_kicad10`); net names stored directly on items and per-via `(tenting (front yes) (back no))` are read |
| newer | above 20260206 | read best-effort with a warning; raise `Run.KICAD_VERSION_MAX` once checked. A bold text's thickness from format 20260826 on is read as its base pen, drawn 1.6 times as wide, as KiCad's development version does |

The 150 public boards (25 for each release from 4 to 9, six of the "KiCad 4" ones saved by the builds before it) were downloaded for testing and are not kept
in the repository; every complete one of them runs, and the Verifier passes on all but one, whose file
places two pin headers of different nets on the same spot. One more KiCad 5 file is cut short (it
ends inside a pad) and is refused with a message that says so, as KiCad refuses it. Every rule that depends on the version
is in one file, `kese/s1_read/parse_kicad_version.py`, and follows KiCad's own board parser:

| Rule | Files it applies to |
|---|---|
| copper layers are read by their place in the leading run of copper layers (first = `F.Cu`, last = `B.Cu`, inner ones `In1.Cu`, `In2.Cu`, ... unless already named so) | every version; KiCad 3 to 5 files whose layers the user renamed get a warning that lists them |
| a text with no size is 1.524 mm (60 mils) | KiCad 4 |
| a `solder_mask_margin` of 0 means "use the board's value" | up to format 20240201 (KiCad 8) |
| an overbar is text between two `~`, converted to `~{...}` | before format 20210606 (KiCad 5 and early 6) |
| a zone fill is drawn with a pen of `min_thickness` | before format 20250210, unless the zone says `(filled_areas_thickness no)` |
| a zone with only `fill_segments` is filled with those segments | KiCad 4 and 5 |
| a via that does not say is tented as the plot setting `viasonmask` says (open when `yes`), else tented | files whose board setup has no `(tenting ...)` (KiCad 8 and older) |
| a via is not covered, plugged, filled or capped unless it says so: files that old have no board-wide setting for these (KESE counts them in `report.txt` and does not model them) | before format 20250228 |
| a bold text's thickness is its base pen | from format 20260826 |

What is read from the file is listed in [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md);
KiCad itself is not needed, only the `.kicad_pcb` file. Footprints are read from the board file
(KiCad embeds them), so libraries are not needed either.

| Board feature | Support |
|---|---|
| Copper layers | boards with 2, 4, 6 and 8 declared copper layers are in the repository (one of them single-sided: tracks only on `F.Cu`, and on `B.Cu` only its two through-hole pads); more than 8 are modelled with a warning; `F.Cu` and `B.Cu` must be declared. Copper layers are read as KiCad reads them, by their place in the list: the first is `F.Cu`, the last `B.Cu`, and the ones between `In1.Cu`, `In2.Cu`, ... unless already named so; a file whose copper layers the user renamed (`(0 TOP_L1.Sig mixed)`, `(1 GND.Cu power)`) gets a warning that lists the names; a signal-typed `User.n` layer after the copper is not copper |
| Stack-up from Board Setup | thickness, type, material, εr, tanδ per dielectric; copper thickness per layer; mask thickness; mask and silk colours; copper finish; edge plating and castellated pads flags |
| Tracks, arc tracks, vias (through, blind, buried, micro) | yes; "remove unused layers" with KiCad 7+'s `zone_layer_connections`, and KiCad 10's `start_end_only`; a track the solder mask leaves bare (KiCad 9 and later) opens the mask over itself, grown by its own mask margin or the board's pad-to-mask clearance |
| Pads: circle, rect, oval, roundrect, trapezoid, custom | yes; round and oval drills, drill offsets (which move the copper, not the hole), a drill that gives no size taken as KiCad's default of 30 mils (none on an SMD pad), per-pad mask margins; chamfered corners; copper rings on non-plated holes where KiCad flashes them; "remove unused layers" on through-hole pads |
| Zones | stored fills only (fill in KiCad first); rule areas skipped; KiCad 5 fills drawn with a pen of `min_thickness` grown by half of it, as KiCad does on reading |
| Graphics: line, arc, circle, rect, polygon (with arc segments), Bézier, ellipse and elliptical arc (KiCad's development version) | on copper, mask and silk layers; outline from `Edge.Cuts`; rectangles with rounded corners (KiCad 10), on every layer and on `Edge.Cuts`; copper drawings the mask leaves bare (KiCad 9 and later) open it as tracks do |
| Text: `gr_text`, `fp_text`, footprint properties | KiCad's stroke font and layout; markup drawn as KiCad draws it (`~{overbar}`, `^{superscript}`, `_{subscript}`, nested); the pen KiCad uses when the file gives none (a fifth of the width for bold, an eighth otherwise), and never more than a quarter of the smaller of width and height; knockout text; TrueType faces from the glyphs KiCad saves with them (`render_cache`), else with the stroke font and a warning (a cache whose words differ only in variables KESE cannot know, such as project-only ones or `${CURRENT_DATE}`, is drawn); `(face "KiCad Font")` (KiCad 10) is the stroke font; KiCad 7's bare `locked` before the words is a flag, not text; the old `%V` and `%R` are the value and reference |
| Text boxes, dimensions, images, groups, tables, generated items; grid items, drill charts and drill maps (KiCad's development version) | skipped; counted when they sit on a copper, silk or mask layer (text boxes, dimensions) or at the top level of the file (images, groups, tables, generated items, grid items, drill charts, drill maps), otherwise left out without a count. For groups and generated items (such as length-tuning patterns) only the record itself is skipped: the tracks, footprints and graphics they hold are read as usual |
| Footprint 3D models | skipped (bare board) |
| Padstacks (KiCad 9 and later: another pad or via shape on the inner layers or on the back) | yes: front / inner / back and custom (per layer) modes; each copper layer gets its own pad shape or via size; the back mask opening follows the back shape |
| Backdrills, tertiary drills, counterbores and countersinks of pads and vias; covered, plugged, capped and filled vias, also when the board setup makes them so (KiCad 10) | not modelled: the hole is drilled and plated through its whole span and left open; counted under `skipped` in `report.txt`, with a warning |
| Item kinds KESE does not know | skipped; counted under `skipped` in `report.txt` as `<kind> items (unknown to KESE)`, with a warning |
| Hatched fills of graphics (KiCad 10) | not modelled: the shape is drawn as its outline only |
| Edge connector flag of Board Setup (`(edge_connector yes)` or `bevelled`) | not read: the fingers are the pads they are, and a bevelled edge stays square |
| Rigid-flex, multiple stack-up regions | not modelled |

## 21.2 Output Formats

| Format | What is in it | Units | Written by |
|---|---|---|---|
| GLB (binary glTF 2.0) | one mesh per part, PBR materials, vertex normals, bufferView targets | `Run.UNITS` (viewers expect m) | KESE (`kese/s7_write/glb.py`) |
| STEP AP214 | one named shape per part (every part switched on: by default board, copper and finish): the part's closed solids from stage 6, one per separate body, with circular arcs (`Step.STEP_EXACT_ARCS`, the default) (`CIRCLE`) and cylindrical walls (`CYLINDRICAL_SURFACE`) where the outline is round and planar faces elsewhere, or planar faces only (curves as polygons, as in the meshes) with `STEP_EXACT_ARCS = False` | `Run.UNITS`: the file declares millimetres or metres | KESE (`kese/s7_write/step.py`) |
| STL (binary) | one file per part | `Run.UNITS` | KESE (`kese/s7_write/stl.py`) |
| OBJ + MTL | one object per part, normals, colours | `Run.UNITS` | KESE |

Visual mode writes GLB and OBJ only.

## 21.3 Tools

None of these imports has been tried with KESE output yet: the routes follow each tool's
documented import formats and the presets in `parameters/presets.py`, and are to be confirmed.
Research underway.

| Tool | Route | Notes |
|---|---|---|
| openEMS / CSXCAD | STL per part, mm (`--for openems`) with `materials.json` | [openEMS Workflow](OpenEMS-Workflow.md) |
| FreeCAD | STEP, mm, KiCad origin (`--for freecad`) | one solid per net and dielectric, each under its own name, to assign materials; holes and round edges as true circles and cylinders. Its FEM workbench meshes the solids and runs Elmer or CalculiX |
| Elmer (ElmerFEM) | STEP, mm, KiCad origin, no finish (`--for elmer`), meshed by gmsh | neither ElmerGrid nor ElmerSolver reads STEP or STL: gmsh meshes the solids (`BooleanFragments` for shared faces), `ElmerGrid 14 2` converts the mesh, and `Coordinate Scaling = 0.001` makes mm SI ([Choosing An Export](Choosing-An-Export.md#102-the-presets)) |
| CalculiX | STEP, mm, KiCad origin, no finish, copper per layer (`--for calculix`) | heat and stress, no electromagnetics; gmsh meshes the solids into an Abaqus `.inp`, or cgx imports the STEP file |
| gmsh | STEP, mm | meshes the solids for a solver |
| Blender | GLB (`--for blender_glb`) or OBJ with its `.mtl` (`--for blender_obj`): visual mode, metres, centred, `flat`, solder mask and silkscreen on | the importers turn Y-up into Z-up, so the board lies with `F.Cu` up |
| `<model-viewer>`, three.js | GLB, m, centred (`--for viewer`) | the visual-mode skin is made to avoid z-fighting ([Output Modes](Output-Modes.md)) |
| Other thermal / FEA tools reading STL | STL per part, mm | closed solids per part (a part can hold several separate bodies); mesh them with the tool's own mesher |

## 21.4 Python And Packages

| | Version |
|---|---|
| Python | 3.12 or later with the pinned versions (`numpy` 2.5.3 requires it); 3.11 with the packages installed unpinned, as `requirements.txt` describes, or through `pyproject.toml` (`requires-python >= 3.11`, not tested); tested on 3.12, 3.13 and 3.14 |
| `numpy` 2.5.3, `shapely` 2.2.0, `mapbox_earcut` 2.1.0 | the versions in `requirements.txt`; shapely 2.1.2 works too, and 2.0 does not (it lacks the constrained Delaunay triangulation; the run says so before it starts). shapely 2.2.0 brings GEOS 3.14.1, whose shapes may not be shared between threads that make shapes from them; KESE's threads each work on their own copies ([Working Principle](Working-Principle.md#74-work-done-in-parallel)). A shapely built on GEOS 3.15 or newer, which counts the shapes atomically, lets the threads share them, and KESE then copies nothing. Tried with shapely 2.2.0 built on GEOS 3.15.0: the suite passes, the files are the same whatever `Parallel.WORKERS`, and threads that crashed GEOS 3.14.1 without copies run without fault. The files are not byte for byte those of GEOS 3.14.1: its overlays no longer turn rings by a vertex, so some faces are cut into other triangles; the solids are the same within the files' single precision |
| `cadquery-ocp` 7.8.1.1.post1 | optional, for the tests only: they read STEP files back with OpenCascade, and skip that check without it. 7.8 has no wheel for Python 3.14; there use 7.9.3.1.1, with which the STEP tests pass, though it read the file of `16b_edge_plating_border` in about twice the time (125 s against 60 s, the parts added up). 8.0 lacks two classes the check uses (`TopTools_IndexedMapOfShape`, `TopTools_IndexedDataMapOfShapeListOfShape`), so the check is skipped |
| `gltf_validator` (Khronos, command line) | optional; used by the Verifier when on the PATH |

Operating systems: anything the packages above run on. Tested on Linux. The worker processes start
afresh on every system, as Windows and macOS start them; Windows holds at most 61 at once.

| Previous | Next |
|:---|---:|
| [Project Output Organization](Project-Output-Organization.md) | [openEMS Workflow](OpenEMS-Workflow.md) |
