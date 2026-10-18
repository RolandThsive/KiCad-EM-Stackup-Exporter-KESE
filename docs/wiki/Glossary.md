# 22. Glossary

| Term | Meaning |
|---|---|
| Annular ring | The copper of a via or pad around its hole on one layer. |
| Barrel | The plated copper on the wall of a hole, from one copper layer to another. |
| Blind / buried via | A via that spans from an outer layer to an inner one, or between inner layers only; it drills only those dielectrics. |
| Board frame | KESE's internal coordinates: mm, Y up, origin at the outline centre or KiCad's origin, z = 0 at the laminate mid-plane, `F.Cu` toward +Z. |
| Bore | The open hole left inside a plated barrel: the drill minus the plating wall. |
| Castellation | A plated hole cut through by the board edge, leaving a half-barrel on the edge. |
| Conformal mask | Solder mask that follows the copper: thin on top of a trace, thicker on the laminate, with a wall beside each trace. |
| Core | A dielectric sheet that comes with copper already bonded to it; stiff, fixed thickness. |
| Dielectric | A non-conducting layer of the laminate: a core or a prepreg, with εr and tanδ. |
| Edge plating | Copper on the routed edge of the board. |
| Etch factor | How much a trace's side walls lean in because etching undercuts the resist; a trapezoid instead of a rectangle. |
| εr (epsilon_r) | Relative permittivity of a dielectric. |
| Finish | The metal deposited on bare copper after the mask: ENIG (nickel + gold), HASL (tin), OSP, immersion silver or tin, hard gold. |
| Foil | The base copper thickness of a layer, before plating (1 oz = 35 µm). |
| GLB | Binary glTF 2.0, the web and real-time 3D format. |
| Laminate | The stack of dielectrics and inner copper between the two outer copper layers. |
| LPI | Liquid photo-imageable solder mask, the common mask process. |
| Mask opening | A place where the solder mask is absent: pads, untented vias, drawn openings. KiCad's mask layers draw openings, not mask. |
| Mid-plane | The height half-way through the laminate; z = 0 in KESE. |
| Net | A set of electrically connected copper items; KESE makes one solid per net. |
| NPTH | Non-plated through hole: a hole with no copper in it. |
| Part | One named solid (or skin piece) in the output: `Copper_GND`, `Board_dielectric 1`, `Top Solder Mask`. |
| Prepreg | A resin-impregnated glass sheet that bonds cores together under heat; its resin flows into the gaps between inner traces. |
| Preset | A named set of parameter overrides applied with `--for` (`hfss`, `cst`, `openems`, `viewer`). |
| Prism | A flat 2D region between two heights: the building block of every KESE part. |
| PTH | Plated through hole. |
| Pull-back | The distance the mask and silk stop short of the board edge. |
| Role | The kind of a part: `board`, `copper`, `plating`, `finish`, `mask`, `mask_over_copper`, `silk`. |
| Simulation mode | Output as closed solids, for solvers and CAD. |
| Skin | The visible outer surface of the board; what visual mode writes. |
| Snap grid | The 0.1 µm grid every 2D shape is rounded to, so neighbouring layers share exact vertices. |
| Stack-up | The ordered list of copper and dielectric layers with their thicknesses and materials; KiCad stores it in Board Setup. |
| STEP | The CAD exchange format (ISO 10303); KESE writes AP214 with exact solids. |
| tanδ (loss tangent) | Dielectric loss of a material. |
| Tenting | Covering a via with solder mask instead of leaving it open. |
| Through via | A via from `F.Cu` to `B.Cu`. |
| Verifier | KESE's opt-in check that every solid is closed, no parts overlap, and the skin is one surface. |
| Visual mode | Output as the visible skin only, for viewers and renders. |
| Z-fighting | Flicker in a 3D viewer when two surfaces lie at almost the same depth; the reason visual mode exists. |

| Previous | Next |
|:---|---:|
| [openEMS Workflow](OpenEMS-Workflow.md) | [Immediate Next Steps](Immediate-Next-Steps.md) |
