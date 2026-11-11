# 24. Glossary

The words this wiki uses, grouped by subject, each with the section that explains it in full.
Terms from KiCad and PCB manufacturing keep their usual meaning; names in `code` are KESE's own
parameters, roles and files.

| Subject | Terms |
|---|---|
| [24.1 Board And Stack-Up](#241-board-and-stack-up) | Core, Dielectric, εr (epsilon_r), tanδ (loss tangent), Foil, Laminate, Mid-plane, Prepreg, Stack-up |
| [24.2 Holes And Vias](#242-holes-and-vias) | Annular ring, Backdrill, Barrel, Blind / buried via, Bore, Capped via, Castellation, Counterbore, Countersink, Covered via, Filled via, IPC-4761, Microvia, NPTH, Plugged via, PTH, Tenting, Through via, Via resin |
| [24.3 Copper](#243-copper) | Conductivity, Copper grouping, Edge plating, Etch factor, Hatched fill, Net, Outer plating, Surface roughness |
| [24.4 Solder Mask, Silkscreen And Finish](#244-solder-mask-silkscreen-and-finish) | Conformal mask, Finish, LPI, Mask opening, Mask web, Pull-back, Silkscreen |
| [24.5 How KESE Builds A Model](#245-how-kese-builds-a-model) | Board frame, Part, Pinch point, Prism, Role, Skin, Slice, Snap grid, Stage, Verifier |
| [24.6 Output And Files](#246-output-and-files) | GLB, materials.json, OBJ, Preset, report.txt, Run folder, Simulation mode, STEP, STL, Visual mode, Z-fighting |

## 24.1 Board And Stack-Up

The layers a board is made of and the numbers that describe them.

| Term | Meaning | See |
|---|---|---|
| **Core** | A dielectric sheet that comes with copper already bonded to it; stiff, fixed thickness. | [8.1.4](Stack-Up-Model.md#814-dielectrics) |
| **Dielectric** | A non-conducting layer of the laminate: a core or a prepreg, with εr and tanδ. KESE makes one solid per dielectric. | [12.1](Board.md#121-dielectric-solids), [21.2](Material-Properties.md#212-properties-per-role) |
| **Foil** | The base copper thickness of a layer, before plating (1 oz = 35 µm). | [13.4](Copper-And-Traces.md#134-copper-thickness-and-plating) |
| **Laminate** | The stack of dielectrics and inner copper between the two outer copper layers. | [8.1.1](Stack-Up-Model.md#811-laminate-and-faces) |
| **Mid-plane** | The height half-way through the laminate; z = 0 in KESE. | [8.1.1](Stack-Up-Model.md#811-laminate-and-faces) |
| **Prepreg** | A resin-impregnated glass sheet that bonds cores together under heat; its resin flows into the gaps between inner traces, which KESE models as resin fill. | [12.2](Board.md#122-resin-fill-beside-inner-copper) |
| **Stack-up** | The ordered list of copper and dielectric layers with their thicknesses and materials; KiCad stores it in Board Setup. Without one KESE uses its defaults and says so. | [8.2](Stack-Up-Model.md#82-where-the-numbers-come-from) |
| **tanδ (loss tangent)** | Dielectric loss of a material: the share of a signal's energy it turns into heat each cycle. | [21.3](Material-Properties.md#213-the-default-numbers) |
| **εr (epsilon_r)** | Relative permittivity of a dielectric: how much it slows a signal and adds capacitance. From the stack-up, else a default. | [21.3](Material-Properties.md#213-the-default-numbers) |

## 24.2 Holes And Vias

Every kind of hole KESE models, including the via options KiCad 10 added.

| Term | Meaning | See |
|---|---|---|
| **Annular ring** | The copper of a via or pad around its hole on one layer. | [13.3](Copper-And-Traces.md#133-vias-and-plated-holes) |
| **Backdrill** | A second, wider drill into a plated hole from one face, through the layer it must cut, that takes off the stub of the barrel no signal uses (KiCad 10); one from the other face is a tertiary drill. | [13.3.3](Copper-And-Traces.md#1333-backdrills) |
| **Barrel** | The plated copper on the wall of a hole, from one copper layer to another. | [13.3](Copper-And-Traces.md#133-vias-and-plated-holes) |
| **Blind / buried via** | A via that spans from an outer layer to an inner one, or between inner layers only; it drills only those dielectrics. | [13.3](Copper-And-Traces.md#133-vias-and-plated-holes) |
| **Bore** | The open hole left inside a plated barrel: the drill minus the plating wall. | [13.3](Copper-And-Traces.md#133-vias-and-plated-holes) |
| **Capped via** | A via plated over at its outer ends, so the copper closes the hole; with a fill, IPC-4761's Type VII (KiCad 10). | [13.3.4](Copper-And-Traces.md#1334-via-protection) |
| **Castellation** | A plated hole cut through by the board edge, leaving a half-barrel on the edge. | [13.6](Copper-And-Traces.md#136-castellated-holes) |
| **Counterbore** | A flat-bottomed step machined into the end of a hole from a face, for a screw head (KiCad 10). | [12.4.1](Board.md#1241-counterbores-and-countersinks) |
| **Countersink** | A cone machined into the end of a hole from a face, for a countersunk screw (KiCad 10). | [12.4.1](Board.md#1241-counterbores-and-countersinks) |
| **Covered via** | A via whose hole the solder mask spans on one face (IPC-4761; KiCad 10). | [13.3.4](Copper-And-Traces.md#1334-via-protection) |
| **Filled via** | A via whose hole is filled through its whole length inside the plating, with copper or resin (IPC-4761; KiCad 10). | [13.3.4](Copper-And-Traces.md#1334-via-protection) |
| **IPC-4761** | The standard that names the ways a via can be protected: covered, plugged, capped and filled, and their combinations. KiCad 10 stores them on each via. | [13.3.4](Copper-And-Traces.md#1334-via-protection) |
| **Microvia** | A small laser-drilled blind via that spans one dielectric, from an outer layer to the layer under it, as on HDI boards. | [18.2.6](Feature-Test-Collection.md#1826-05-microvias) |
| **NPTH** | Non-plated through hole: a hole with no copper in it. | [12.4](Board.md#124-holes) |
| **Plugged via** | A via whose hole is plugged with resin from one face, part of the way in (IPC-4761; KiCad 10). | [13.3.4](Copper-And-Traces.md#1334-via-protection) |
| **PTH** | Plated through hole. | [13.3](Copper-And-Traces.md#133-vias-and-plated-holes) |
| **Tenting** | Covering a via with solder mask instead of leaving it open. | [13.3.2](Copper-And-Traces.md#1332-via-tenting) |
| **Through via** | A via from `F.Cu` to `B.Cu`. | [13.3](Copper-And-Traces.md#133-vias-and-plated-holes) |
| **Via resin** | The resin inside a plugged or filled via; its own part with the role `via_resin`, carrying `Copper.VIA_RESIN_EPSILON_R` and `Copper.VIA_RESIN_LOSS_TANGENT`. | [21.2](Material-Properties.md#212-properties-per-role) |

## 24.3 Copper

How traces, zones and plating become copper solids.

| Term | Meaning | See |
|---|---|---|
| **Conductivity** | How well copper carries current, written for every copper part to `materials.json` (`Copper.COPPER_CONDUCTIVITY_S_PER_M`, 5.8 × 10⁷ S/m). | [13.8](Copper-And-Traces.md#138-electrical-properties) |
| **Copper grouping** | How copper is split into parts (`Copper.COPPER_GROUPING`): one solid per net (the default), one per layer with the plating apart, or all in one. | [13.2](Copper-And-Traces.md#132-grouping-and-part-names) |
| **Edge plating** | Copper on the routed edge of the board. | [13.7](Copper-And-Traces.md#137-edge-plating) |
| **Etch factor** | How much a trace's side walls lean in because etching undercuts the resist; a trapezoid instead of a rectangle. | [13.5](Copper-And-Traces.md#135-etch-factor) |
| **Hatched fill** | A shape filled with lines at 45 degrees, or a cross hatch of square holes, instead of solid (KiCad 10). | [13.1.2](Copper-And-Traces.md#1312-hatched-fills) |
| **Net** | A set of electrically connected copper items; with the default `Copper.COPPER_GROUPING = "net"`, KESE makes one solid per net. | [13.1.1](Copper-And-Traces.md#1311-nets) |
| **Outer plating** | The copper electroplating adds to the outer layers while it plates the holes (`Copper.OUTER_PLATING_ADDED_MM`, typically 20 µm on real boards, 0 by default so the geometry matches KiCad). | [13.4](Copper-And-Traces.md#134-copper-thickness-and-plating) |
| **Surface roughness** | The roughness of the copper's faces, which raises its loss at high frequency; written to `materials.json` for the solver (`Copper.COPPER_SURFACE_ROUGHNESS_UM`, 0 = ignore). | [13.8](Copper-And-Traces.md#138-electrical-properties) |

## 24.4 Solder Mask, Silkscreen And Finish

The layers on top of the outer copper.

| Term | Meaning | See |
|---|---|---|
| **Conformal mask** | Solder mask that follows the copper: it lies on top of each trace and on the laminate between them, with a wall beside each trace. On real boards it is often thinner on top of copper; KESE has a parameter for each (both 10 µm by default); a mask thickness in the board's stack-up replaces both unless `SolderMask.USE_STACKUP_MASK_THICKNESS = False`. | [17.2](Solder-Masks.md#172-conformal-mask) |
| **Finish** | The metal deposited on every bare copper face after the mask (faces, walls, plated holes, plated edges): ENIG (nickel + gold), ENEPIG (nickel + palladium + gold), HASL (tin), OSP, immersion silver or tin, hard gold. | [15.3](Finish.md#153-finish-types) |
| **LPI** | Liquid photo-imageable solder mask, the common mask process. | [17.2](Solder-Masks.md#172-conformal-mask) |
| **Mask opening** | A place where the solder mask is absent: pads, untented vias, drawn openings. KiCad's mask layers draw openings, not mask. | [17.1](Solder-Masks.md#171-kicads-mask-layers-are-negative) |
| **Mask web** | A strip of solder mask between two mask openings; KESE removes one narrower than the solder mask minimum width (the board's, or `SolderMask.MASK_MIN_WIDTH_MM`), joining the two openings, as KiCad does when it plots the mask. | [17.1](Solder-Masks.md#171-kicads-mask-layers-are-negative) |
| **Pull-back** | The distance the mask and silk stop short of the board edge. | [17.3](Solder-Masks.md#173-edge-pull-back) |
| **Silkscreen** | The printed ink on top of the mask: KiCad's lines, shapes and text, drawn by KESE with KiCad's own stroke font. | [16.1](Silkscreens.md#161-what-is-drawn), [16.2](Silkscreens.md#162-text-rendering) |

## 24.5 How KESE Builds A Model

The words the Working Principle and the checks use.

| Term | Meaning | See |
|---|---|---|
| **Board frame** | KESE's internal coordinates: mm, Y up, origin at the outline centre or KiCad's origin, z = 0 at the laminate mid-plane, `F.Cu` toward +Z. | [7.3](Working-Principle.md#73-coordinate-frames) |
| **Part** | One named solid (or skin piece) in the output: `Copper_GND`, `Board_dielectric 1`, `Top Solder Mask`. | [11.3](Project-Output-Organization.md#113-part-names) |
| **Pinch point** | A place where a shape's outline touches itself at a single point. It cannot be meshed as it is, so KESE opens it by a tiny cut (`Geometry.PINCH_POINT_OPENING_MM`, 0.1 µm) and `report.txt` notes it. | [7.2](Working-Principle.md#72-how-a-part-becomes-a-closed-solid) |
| **Prism** | A flat 2D region between two heights: the building block of every KESE part. | [7.2](Working-Principle.md#72-how-a-part-becomes-a-closed-solid) |
| **Role** | The kind of a part: `board`, `copper`, `plating`, `via_resin`, `finish`, `mask`, `mask_over_copper`, `silk`. | [21.2](Material-Properties.md#212-properties-per-role) |
| **Skin** | The visible outer surface of the board; what visual mode writes. | [9.2](Output-Modes.md#92-visual-mode) |
| **Slice** | The material of one part between two neighbouring heights where its prisms start or end; stage 6 builds a part's surface from its slices. | [7.2](Working-Principle.md#72-how-a-part-becomes-a-closed-solid) |
| **Snap grid** | The 0.1 µm grid every 2D shape is rounded to, so neighbouring layers share exact vertices (`Geometry.SNAP_GRID_MM`). | [19.7](Parameter-Reference.md#197-geometry-parametersgeometrypy) |
| **Stage** | One of the nine steps of KESE's pipeline, from reading the file (1) to writing the report (9); each is a folder in `kese/`. | [7](Working-Principle.md) |
| **Verifier** | KESE's opt-in check (`--verify`) that every solid is closed and holds the volume of its prisms, no parts overlap, and the skin is one surface. | [20.3](Checks-Errors-And-Warnings.md#203-the-verifier) |

## 24.6 Output And Files

What a run writes and how to pick it.

| Term | Meaning | See |
|---|---|---|
| **GLB** | Binary glTF 2.0, the web and real-time 3D format. | [22.2](Compatibility.md#222-output-formats) |
| **materials.json** | The file beside the outputs that carries what geometry cannot: each part's role, layer, net, heights, εr, tanδ, conductivity and colour. | [21.1](Material-Properties.md#211-the-file) |
| **OBJ** | Wavefront OBJ with its `.mtl`: one object per part, with normals and colours. | [22.2](Compatibility.md#222-output-formats) |
| **Preset** | A named set of parameter overrides applied with `--for` (`freecad`, `elmer`, `calculix`, `openems`, `viewer`, `blender_glb`, `blender_obj`), from `parameters/presets.py`. | [10.2](Choosing-An-Export.md#102-the-presets) |
| **report.txt** | The run's report: what was read and skipped, the warnings, the time of each stage and the Verifier's result. | [11.2.2](Project-Output-Organization.md#1122-reporttxt) |
| **Run folder** | The new folder each run writes to, `<OUTPUT_DIR>/<board>/<mode>_<FORMATS>/`; no run overwrites another. | [11.2](Project-Output-Organization.md#112-run-folders) |
| **Simulation mode** | Output as closed solids, for solvers and CAD. | [9.1](Output-Modes.md#91-simulation-mode) |
| **STEP** | The CAD exchange format (ISO 10303); KESE writes AP214, every part as closed solids, with round outlines as true arcs and cylinders (`Step.STEP_EXACT_ARCS`) and planar faces elsewhere. | [22.2](Compatibility.md#222-output-formats) |
| **STL** | Binary STL, one file per part: triangles only, no colour or units. | [22.2](Compatibility.md#222-output-formats) |
| **Visual mode** | Output as the visible skin only, for viewers and renders. | [9.2](Output-Modes.md#92-visual-mode) |
| **Z-fighting** | Flicker in a 3D viewer when two surfaces lie at almost the same depth; the reason visual mode exists. | [9.2](Output-Modes.md#92-visual-mode) |
| Previous | Next |
|:---|---:|
| [openEMS Workflow](OpenEMS-Workflow.md) | [Future Upgrades And Planning](Future-Upgrades-And-Planning.md) |
