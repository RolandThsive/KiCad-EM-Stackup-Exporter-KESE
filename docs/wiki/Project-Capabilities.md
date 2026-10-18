# 4. Project Capabilities

## 4.1 Capability Table

| Area | Capability |
|---|---|
| Input | `.kicad_pcb` from KiCad 6 to 10 (file formats 20211014 to 20260206; older files are read best-effort with a warning), 1 to 6 copper layers, stack-up read from Board Setup when present |
| Copper | One closed solid per net (default), per layer, or all copper merged; tracks, arc tracks, pads of every KiCad shape, zone fills; through, blind, buried and micro vias with plated barrels; plated through-hole pads; castellated holes; edge plating; via tenting; optional etch-factor trapezoids; KiCad's "remove unused layers" on vias |
| Dielectrics | One solid per core / prepreg with its own εr and tanδ from the stack-up, or the whole laminate as one solid; resin fill beside inner copper; plated and non-plated holes; board cut-outs |
| Solder mask | Negative mask layers as KiCad draws them: pads, drawn openings and untented vias open the mask; conformal mask that climbs over every trace; edge pull-back; stack-up colour names honoured |
| Silkscreen | Legend ink on top of the mask in KiCad's own stroke font, with KiCad's text layout; clipped off mask openings as fabricators do; custom stroke or Hershey fonts |
| Surface finish | ENIG, HASL, OSP, immersion silver, immersion tin and hard gold as their own metal layers on bare copper (off by default) |
| Output | GLB (one mesh per part, PBR materials), STEP (one named exact solid per part, true arcs), one STL per part, OBJ with `.mtl`; in mm or m; board centred or on KiCad's origin; upright or flat |
| Records | `materials.json` per part (role, layer, net, z range, εr, tanδ, conductivity, file names), `parameters.txt` (every setting of the run), `report.txt` (stack-up heights, what was read, what was skipped and why, triangle counts, timings) |
| Checks | Opt-in Verifier: every solid closed and consistently wound, no overlap between parts, exactly one visible surface in visual mode, Khronos glTF validation when the validator is installed; a regression suite with recorded part volumes |
| Not modelled | Component 3D models, text boxes, dimensions, images, groups, rigid-flex. See [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) for the complete list of skipped items. |

## 4.2 What The Simulation Model Is Good For

These uses rely on the simulation-mode output: per-net copper, dielectrics with εr and tanδ,
plating and finish.

- **Full-wave EM.** S-parameters, impedance, crosstalk, antenna patterns and resonances.
- **Signal integrity.** Trace impedance and eye diagrams, where the exact copper thickness, the
  etch trapezoid and the prepreg-versus-core εr matter.
- **Power integrity and DC-IR drop.** A per-net GND or power solid with real plating thickness is
  what PDN tools need.
- **Thermal.** The same solids with electrical conductivity swapped for thermal conductivity;
  copper planes, via barrels and the laminate are the heat paths.
- **Mechanical and FEA.** Warp and stress with the real copper distribution and core / prepreg
  layers, since every layer is a closed solid.
- **Parasitic extraction.** Capacitance and inductance between nets, because each net is its own
  body.
- **What-if on fabrication.** Change plating, via wall, mask thickness or etch factor in
  `Parameters/` and re-simulate to see how much fabrication tolerances move your results.

## 4.3 Tested Sizes

The numbers below come from runs of the example boards in `Input/` and the boards in
`Tests/boards/` with the default parameters on `main` (35 µm copper, 10 µm mask, GLB in metres),
on one Linux machine. They say what to expect, not what the limit is.

| Board | Layers | Items | Simulation run | Parts and triangles |
|---|---|---|---|---|
| `Stator` (1-loop encoder stator) | 2 | 2,414 tracks, 13 vias | 16 s with the Verifier (assemble 8.9 s, verify 3.4 s); GLB 5.0 MB, OBJ 13.5 MB, six STL files 6.3 MB together | `Copper_TX` 9,068, `Copper_1` and `Copper_2` 9,516 each, `Board_dielectric 1` 3,540, top and bottom mask 33,728 and 63,402 |
| `Coil_30_50_4_1_3_Series_SteppedDiagonal_Stator` (4-loop encoder stator) | 4 | 6,216 tracks, 53 vias | 47 s with the Verifier (assemble 43 s); 50 s in visual mode; GLB 15.1 MB, visual-mode GLB 10.2 MB | `Copper_SIN_Signal` 42,436, `Copper_COS_Signal` 42,444, `Copper_TX` 24,384, three dielectrics 57,220 together, both masks 212,518 together |
| `XIAO_ESP32C3_v1.3` (4-layer module with 68 footprints) | 4 | 449 tracks, 128 vias, 207 pads, 28 zone fills | 69 s (breakdown 18 s, geometry 8 s, assemble 40 s) | 46 copper parts, `Copper_GND` 102,786, top mask 147,484, top silkscreen 66,658 |
| `six_layer` (test board) | 6 | 6 tracks, 6 vias, 2 zone fills | 7 s with the Verifier | 10 parts, 23,600 triangles |

- The slowest stages are the boolean union of a net's pieces (assemble) and, for STEP, the fusing
  of every part into one solid: the GND net of a dense board takes about a minute to fuse.
- STEP files leave out the solder mask and silkscreen by default (`Run.STEP_WRITE_ROLES`): on a
  dense board they are thousands of solids and the export would need many GB of memory. GLB, STL
  and OBJ always contain them.
- The Verifier adds 10 to 60 s per board.

> [!NOTE]
> Every dimension in the model is a model value until it is measured. Validation against
> fabricated boards and reference solvers is planned but not done.

| Previous | Next |
|:---|---:|
| [Getting Started](Getting-Started.md) | [Examples](Examples.md) |
