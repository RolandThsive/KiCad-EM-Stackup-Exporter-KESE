# 20. KiCad And Solver Compatibility

## 20.1 KiCad Files

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
| newer | above 20260206 | read best-effort with a warning; raise `Run.KICAD_VERSION_MAX` once checked. A bold text's thickness after format 20260826 is read as its base pen, drawn 1.6 times as wide, as KiCad's development version does |

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
| via tenting and protection off unless stated | before format 20250228 |
| a bold text's thickness is its base pen | after format 20260826 |

What is read from the file is listed in [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md);
KiCad itself is not needed, only the `.kicad_pcb` file. Footprints are read from the board file
(KiCad embeds them), so libraries are not needed either.

| Board feature | Support |
|---|---|
| Copper layers | boards with 2, 4, 6 and 8 declared copper layers are in the repository (one of them single-sided: tracks only on `F.Cu`, and on `B.Cu` only its two through-hole pads); more than 8 are modelled with a warning; `F.Cu` and `B.Cu` must be declared. copper layers are read as KiCad reads them, by their place in the list: the first is `F.Cu`, the last `B.Cu`, and the ones between `In1.Cu`, `In2.Cu`, ... unless already named so; a file whose copper layers the user renamed (`(0 TOP_L1.Sig mixed)`, `(1 GND.Cu power)`) gets a warning that lists the names; a signal-typed `User.n` layer after the copper is not copper |
| Stack-up from Board Setup | thickness, type, material, εr, tanδ per dielectric; copper thickness per layer; mask thickness; mask and silk colours; copper finish; edge plating and castellated pads flags |
| Tracks, arc tracks, vias (through, blind, buried, micro) | yes; "remove unused layers" with KiCad 7+'s `zone_layer_connections`, and KiCad 10's `start_end_only`; a track the solder mask leaves bare (KiCad 9 and later) opens the mask over itself, grown by its own mask margin or the board's pad-to-mask clearance |
| Pads: circle, rect, oval, roundrect, trapezoid, custom | yes; round and oval drills, drill offsets (which move the copper, not the hole), per-pad mask margins; chamfered corners; copper rings on non-plated holes where KiCad flashes them; "remove unused layers" on through-hole pads |
| Zones | stored fills only (fill in KiCad first); rule areas skipped; KiCad 5 fills drawn with a pen of `min_thickness` grown by half of it, as KiCad does on reading |
| Graphics: line, arc, circle, rect, polygon (with arc segments), Bézier, ellipse and elliptical arc (KiCad's development version) | on copper, mask and silk layers; outline from `Edge.Cuts`; rectangles with rounded corners (KiCad 10), on every layer and on `Edge.Cuts`; copper drawings the mask leaves bare (KiCad 9 and later) open it as tracks do |
| Text: `gr_text`, `fp_text`, footprint properties | KiCad's stroke font and layout; markup drawn as KiCad draws it (`~{overbar}`, `^{superscript}`, `_{subscript}`, nested); the pen KiCad uses when the file gives none (a fifth of the width for bold, an eighth otherwise), and never more than a quarter of the smaller of width and height; knockout text; TrueType faces from the glyphs KiCad saves with them (`render_cache`), else with the stroke font |
| Text boxes, dimensions, images, groups, tables, generated items; grid items, drill charts and drill maps (KiCad's development version) | skipped; counted when they sit on a copper, silk or mask layer (text boxes, dimensions) or at the top level of the file (images, groups, tables, generated items, grid items, drill charts, drill maps), otherwise left out without a count. For groups and generated items (such as length-tuning patterns) only the record itself is skipped: the tracks, footprints and graphics they hold are read as usual |
| Footprint 3D models | skipped (bare board) |
| Padstacks (KiCad 9 and later: another pad or via shape on the inner layers or on the back) | yes: front / inner / back and custom (per layer) modes; each copper layer gets its own pad shape or via size; the back mask opening follows the back shape |
| Backdrills, tertiary drills, counterbores and countersinks of pads and vias; covered, plugged, capped and filled vias, also when the board setup makes them so (KiCad 10) | not modelled: the hole is drilled and plated through its whole span and left open; counted under `skipped` in `report.txt`, with a warning |
| Item kinds KESE does not know | skipped; counted under `skipped` in `report.txt` as `<kind> items (unknown to KESE)`, with a warning |
| Hatched fills of graphics (KiCad 10) | not modelled: the shape is drawn as its outline only |
| Edge connector flag of Board Setup (`(edge_connector yes)` or `bevelled`) | not read: the fingers are the pads they are, and a bevelled edge stays square |
| Rigid-flex, multiple stack-up regions | not modelled |

## 20.2 Output Formats

| Format | What is in it | Units | Written by |
|---|---|---|---|
| GLB (binary glTF 2.0) | one mesh per part, PBR materials, vertex normals, bufferView targets | `Run.UNITS` (viewers expect m) | KESE (`kese/s7_write/glb.py`) |
| STEP AP214 | one named shape per part whose role is in `Run.STEP_WRITE_ROLES`: the part's closed solids from stage 6, one per separate body, with planar faces (curves are polygons, as in the meshes), or with `Run.STEP_EXACT_ARCS` circular arcs (`CIRCLE`) and cylindrical walls (`CYLINDRICAL_SURFACE`) where the outline is round; mask and silk off by default | `Run.UNITS`: the file declares millimetres or metres | KESE (`kese/s7_write/step.py`) |
| STL (binary) | one file per part | `Run.UNITS` | KESE (`kese/s7_write/stl.py`) |
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
| FreeCAD, Fusion, SolidWorks, Onshape | STEP | vias and round pads are faceted, as in the meshes |
| Blender | GLB or OBJ (visual mode for renders) | |
| `<model-viewer>`, three.js | GLB, m, centred (`--for viewer`) | the visual-mode skin is made to avoid z-fighting ([Output Modes](Output-Modes.md)) |
| Thermal / FEA tools reading STL (CalculiX, Elmer with a mesher) | STL per part, mm | closed solids per part (a part can hold several separate bodies); mesh them with the tool's own mesher |

## 20.4 Python And Packages

| | Version |
|---|---|
| Python | 3.12 or later with the pinned versions (`numpy` 2.5.3 requires it); 3.11 with the packages installed unpinned, as `requirements.txt` describes, or through `pyproject.toml` (`requires-python >= 3.11`, not tested); tested on 3.13 |
| `numpy` 2.5.3, `shapely` 2.2.0, `mapbox_earcut` 2.1.0 | the versions in `requirements.txt` |
| `cadquery-ocp` 7.9.3.1 or later below 8.0 | optional, for the tests only: they read STEP files back with OpenCascade, and skip that check without it |
| `gltf_validator` (Khronos, command line) | optional; used by the Verifier when on the PATH |

Operating systems: anything the packages above run on. Tested on Linux.

| Previous | Next |
|:---|---:|
| [Project Output Organization](Project-Output-Organization.md) | [openEMS Workflow](OpenEMS-Workflow.md) |
