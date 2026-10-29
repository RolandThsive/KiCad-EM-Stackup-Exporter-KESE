# 4. Project Capabilities

KESE turns a `.kicad_pcb` file into a 3D model of the bare board as it is made, every layer a
named part with its physical properties, in two forms: a **simulation model** of closed solids for
solvers and CAD, and a **visual model** of the visible surface for viewers.

## 4.1 What KESE Models

| Board feature | What KESE builds |
|---|---|
| Board file | `.kicad_pcb` from KiCad 6 to 10 (file formats 20211014 to 20260206); older and newer files are read with a warning. KiCad itself is not needed. |
| Copper layers | 1 to 8 in the test boards. Above 8, KESE warns but still models the board. `F.Cu` and `B.Cu` must be declared. |
| Stack-up | From Board Setup: every core and prepreg with its thickness, εr and tanδ, the copper and mask thicknesses, the mask and silk colours, the finish. Defaults from `parameters/` when the file has none. |
| Outline | `Edge.Cuts` of any shape, with cut-outs |
| Copper | Tracks, arc tracks, pads (circle, rect, oval, roundrect, trapezoid, custom), zone fills, copper graphics and text |
| Vias | Through, blind, buried and micro vias with plated barrels; rings on unconnected layers dropped as KiCad does |
| Holes | Plated and non-plated, round and slotted; plated walls on the plated ones |
| Board edge | Castellated holes and edge plating |
| Dielectrics | One solid per gap between copper layers with its own εr and tanδ; resin fills the space beside inner copper |
| Solder mask | Openings as KiCad draws them (pads, drawn openings, untented vias, and tracks and copper drawings the mask leaves bare); conformal over every trace; pulled back from the board edge; open over every bore, so on a tented via it covers only the ring |
| Silkscreen | KiCad's stroke font and text layout (TrueType text is drawn in the stroke font; a custom stroke or Hershey font is optional); removed inside mask openings, as fabricators do |
| Surface finish | ENIG, ENEPIG, HASL, lead-free HASL, OSP, immersion silver, immersion tin, hard gold: each metal its own layer on the bare copper, taken from KiCad's finish name. Off by default. |
| Etching | Optional sloped copper walls (`Copper.ETCH_FACTOR`) |
| Colours | One material per part; KiCad's mask and silk colour names honoured |

## 4.2 Simulation Model And Visual Model

| | Simulation model (`--mode simulation`, the default) | Visual model (`--mode visual`) |
|---|---|---|
| What it is | Every part a closed solid. Parts touch exactly and never overlap. | Only the surface you can see: the faces between material and air. Nothing hidden, so nothing flickers. |
| Use it for | Full-wave EM, SI and PI, DC-IR drop, parasitic extraction, thermal, mechanical and CAD | Web viewers (`<model-viewer>`, three.js), renders, Blender |
| Formats | GLB, STEP, STL, OBJ | GLB, OBJ |
| Copper | One part per net: its tracks on every layer and its vias (or one per layer, or one for all) | All copper in the bare-copper colour |
| Solder mask | Translucent, one part per side | Opaque; lighter where it lies on copper, so traces show through |
| Other parts | Each dielectric, plating, silkscreen, finish | The same; a part with nothing in sight is left out |
| Physical data | εr, tanδ, conductivity, thickness and z range per part in `materials.json` | The same file |
| What-if | Change plating, via wall, mask thickness or etch factor in `parameters/` and export again | |
| Verifier (`--verify`) | Every part closed and consistently wound; its volume the same from its faces, slices, mesh and prisms; no two parts sharing material, every slice against every other | Along 3,000 vertical rays the faces take turns, into the material and out of it |
| 4-layer PCIe card example | GLB 32.1 MB, 942,340 triangles | GLB 18.3 MB, 591,381 triangles |
| Presets | `--for hfss`, `--for cst`, `--for openems` | `--for viewer` |

More in [Output Modes](Output-Modes.md).

## 4.3 Output Files

| File | What it holds |
|---|---|
| GLB | One mesh per part with its colour; metres by default (`Run.UNITS`) |
| STEP | Written by KESE itself, no CAD kernel needed: every part under its own name, as closed solids of flat faces, curves as polygons; board, copper, plating and finish by default (`Run.STEP_WRITE_ROLES`) |
| STL | One closed file per part, in `stl/` |
| OBJ | One object per part, colours in an `.mtl` |
| `materials.json` | Per part: role, layer, net, z range, εr, tanδ, conductivity, colour, file names |
| `parameters.txt` | Every setting of the run, with what was changed for it |
| `report.txt` | Stack-up heights, what was read and what was skipped, parts and triangles, timings, the Verifier's result |
| Options | mm or m; centred or at KiCad's origin; board upright or flat |

## 4.4 Not Modelled

| Item | What happens |
|---|---|
| Component 3D models | Left out: KESE models the bare board |
| Text boxes, dimensions, images, targets, tables | Skipped and listed in `report.txt` |
| Groups, length-tuning patterns | The group record is skipped; the tracks and footprints in it are modelled |
| KiCad 10 barcodes and points | Skipped and listed in `report.txt`; the file holds no pattern for a barcode, only its text |
| Keepout and rule areas | No copper, by design |
| Zones never filled | No copper, with a warning: fill them in KiCad (**B**) and save |
| Chamfered pad corners | Drawn as the plain rounded rectangle |
| Bevel of an edge connector | Not read: the edge stays square |
| Rigid-flex, several stack-ups in one board | Not modelled |

The full list is in [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md).

## 4.5 Tested Sizes

| Board | Layers | Items | Simulation GLB | STEP in mm | Visual GLB |
|---|---|---|---|---|---|
| `rf_module` | 4 | 190 tracks, 33 arcs, 307 vias, 7 zone fills | 21 s, 29.9 MB | 22 s, 224.3 MB; with mask and silk 26 s, 330.2 MB | 20 s, 17.1 MB |
| `hdi_module` | 6 | 199 tracks, 150 vias, 34 zone fills | 14 s, 17.0 MB | 15 s, 125.3 MB; with mask and silk 16 s, 183.2 MB | 15 s, 8.8 MB |
| `pcie_card` | 4 | 226 tracks, 239 vias, 19 zone fills | 19 s, 32.1 MB | 21 s, 214.6 MB; with mask and silk 24 s, 347.8 MB | 21 s, 18.3 MB |
| `six_layer` | 6 | 6 tracks, 6 vias, 2 zone fills | 1 s, 0.9 MB | 1 s, 6.2 MB | 1 s, 0.45 MB |

Default parameters, GLB runs with the Verifier, on one Linux machine with 4 cores: what to expect,
not a limit. The times are the ones the run prints (`in 0m 21s`); starting Python and loading its
packages adds about 2.5 s to each command.

> [!NOTE]
> Every dimension in the model is a model value until it is measured. Validation against
> fabricated boards and reference solvers is planned but not done.

| Previous | Next |
|:---|---:|
| [Getting Started](Getting-Started.md) | [Examples](Examples.md) |
