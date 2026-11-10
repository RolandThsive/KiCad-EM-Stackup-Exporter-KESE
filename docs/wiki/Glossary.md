# 24. Glossary

| Term | Meaning |
|---|---|
| Annular ring | The copper of a via or pad around its hole on one layer. |
| Backdrill | A second, wider drill into a plated hole from one face, through the layer it must cut, that takes off the stub of the barrel no signal uses (KiCad 10); one from the other face is a tertiary drill. |
| Barrel | The plated copper on the wall of a hole, from one copper layer to another. |
| Blind / buried via | A via that spans from an outer layer to an inner one, or between inner layers only; it drills only those dielectrics. |
| Board frame | KESE's internal coordinates: mm, Y up, origin at the outline centre or KiCad's origin, z = 0 at the laminate mid-plane, `F.Cu` toward +Z. |
| Bore | The open hole left inside a plated barrel: the drill minus the plating wall. |
| Capped via | A via plated over at its outer ends, so the copper closes the hole; with a fill, IPC-4761's Type VII (KiCad 10). |
| Castellation | A plated hole cut through by the board edge, leaving a half-barrel on the edge. |
| Conformal mask | Solder mask that follows the copper: it lies on top of each trace and on the laminate between them, with a wall beside each trace. On real boards it is often thinner on top of copper; KESE has a parameter for each (both 10 µm by default); a mask thickness in the board's stack-up replaces both unless `SolderMask.USE_STACKUP_MASK_THICKNESS = False`. |
| Core | A dielectric sheet that comes with copper already bonded to it; stiff, fixed thickness. |
| Counterbore | A flat-bottomed step machined into the end of a hole from a face, for a screw head (KiCad 10). |
| Countersink | A cone machined into the end of a hole from a face, for a countersunk screw (KiCad 10). |
| Covered via | A via whose hole the solder mask spans on one face (IPC-4761; KiCad 10). |
| Dielectric | A non-conducting layer of the laminate: a core or a prepreg, with εr and tanδ. |
| Edge plating | Copper on the routed edge of the board. |
| Etch factor | How much a trace's side walls lean in because etching undercuts the resist; a trapezoid instead of a rectangle. |
| εr (epsilon_r) | Relative permittivity of a dielectric. |
| Filled via | A via whose hole is filled through its whole length inside the plating, with copper or resin (IPC-4761; KiCad 10). |
| Finish | The metal deposited on every bare copper face after the mask (faces, walls, plated holes, plated edges): ENIG (nickel + gold), ENEPIG (nickel + palladium + gold), HASL (tin), OSP, immersion silver or tin, hard gold. |
| Foil | The base copper thickness of a layer, before plating (1 oz = 35 µm). |
| GLB | Binary glTF 2.0, the web and real-time 3D format. |
| Hatched fill | A shape filled with lines at 45 degrees, or a cross hatch of square holes, instead of solid (KiCad 10). |
| Laminate | The stack of dielectrics and inner copper between the two outer copper layers. |
| LPI | Liquid photo-imageable solder mask, the common mask process. |
| Mask opening | A place where the solder mask is absent: pads, untented vias, drawn openings. KiCad's mask layers draw openings, not mask. |
| Mask web | A strip of solder mask between two mask openings; KESE removes one narrower than the solder mask minimum width (the board's, or `SolderMask.MASK_MIN_WIDTH_MM`), joining the two openings, as KiCad does when it plots the mask. |
| Mid-plane | The height half-way through the laminate; z = 0 in KESE. |
| Net | A set of electrically connected copper items; with the default `Copper.COPPER_GROUPING = "net"`, KESE makes one solid per net. |
| NPTH | Non-plated through hole: a hole with no copper in it. |
| Part | One named solid (or skin piece) in the output: `Copper_GND`, `Board_dielectric 1`, `Top Solder Mask`. |
| Plugged via | A via whose hole is plugged with resin from one face, part of the way in (IPC-4761; KiCad 10). |
| Prepreg | A resin-impregnated glass sheet that bonds cores together under heat; its resin flows into the gaps between inner traces. |
| Preset | A named set of parameter overrides applied with `--for` (`freecad`, `elmer`, `calculix`, `openems`, `viewer`, `blender_glb`, `blender_obj`), from `parameters/presets.py`. |
| Prism | A flat 2D region between two heights: the building block of every KESE part. |
| PTH | Plated through hole. |
| Pull-back | The distance the mask and silk stop short of the board edge. |
| Role | The kind of a part: `board`, `copper`, `plating`, `via_resin`, `finish`, `mask`, `mask_over_copper`, `silk`. |
| Simulation mode | Output as closed solids, for solvers and CAD. |
| Skin | The visible outer surface of the board; what visual mode writes. |
| Slice | The material of one part between two neighbouring heights where its prisms start or end; stage 6 builds a part's surface from its slices. |
| Snap grid | The 0.1 µm grid every 2D shape is rounded to, so neighbouring layers share exact vertices. |
| Stack-up | The ordered list of copper and dielectric layers with their thicknesses and materials; KiCad stores it in Board Setup. |
| STEP | The CAD exchange format (ISO 10303); KESE writes AP214, every part as closed solids, with round outlines as true arcs and cylinders (`Step.STEP_EXACT_ARCS`) and planar faces elsewhere. |
| tanδ (loss tangent) | Dielectric loss of a material. |
| Tenting | Covering a via with solder mask instead of leaving it open. |
| Through via | A via from `F.Cu` to `B.Cu`. |
| Verifier | KESE's opt-in check that every solid is closed and holds the volume of its prisms, no parts overlap, and the skin is one surface. |
| Visual mode | Output as the visible skin only, for viewers and renders. |
| Z-fighting | Flicker in a 3D viewer when two surfaces lie at almost the same depth; the reason visual mode exists. |

| Previous | Next |
|:---|---:|
| [openEMS Workflow](OpenEMS-Workflow.md) | [Future Upgrades And Planning](Future-Upgrades-And-Planning.md) |
