# 5. Examples

The repository ships two boards in `Input/`. `python run_KESE.py` with no arguments exports both
of them. The boards in `Tests/boards/` are small synthetic boards for the regression suite and are
described in [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md).

<!-- Pictures wanted for this page (made by Roland):
     Examples 1: the Coil stator GLB rendered in a viewer, simulation mode, copper per net in its own colour.
     Examples 2: the same board in visual mode. -->

## 5.1 Stator (2 Layers)

`Input/Stator.kicad_pcb`, KiCad file format 20221018 (KiCad 7). A 2-layer inductive encoder
stator with one loop and three nets: `TX`, `1` and `2`. 2,414 track segments and 13 through
vias, no footprints, no zones, no stack-up block in the file.

What this board shows:

- A board **without a stack-up** in Board Setup: the laminate is the file's `(general (thickness 1.6))`,
  one FR4 core with the default εr 4.5 and tanδ 0.02, copper 35 µm from the defaults.
- Copper per net: `Copper_TX`, `Copper_1` and `Copper_2`, each with its vias joined.
- No pad or drawn mask openings: the board has no pads, and its vias are tented (KiCad's default
  when the file sets nothing), so the mask covers their rings; only the 13 open via bores
  (0.35 mm across) pass through it. The two mask solids climb over every
  trace and carry three quarters of the triangles.

Excerpt of `report.txt` from `python run_KESE.py Input/Stator.kicad_pcb --format glb stl obj --verify`:

```text
stack-up
  copper layers: F.Cu, B.Cu
  laminate 1.6000 mm (file (general (thickness)) - no usable stackup)
  F.Cu     z +0.8000 .. +0.8350 mm  (foil 0.035 mm)
  B.Cu     z -0.8350 .. -0.8000 mm  (foil 0.035 mm)
  dielectric 1             core     FR4        1.6000 mm  er 4.5  tan d 0.02   z -0.8000 .. +0.8000

parts
  Board_dielectric 1                       3540 triangles  material Board_core #968A58 alpha 1.0
  Copper_1                                 9516 triangles  material Copper #CD803E alpha 1.0
  Copper_2                                 9516 triangles  material Copper #CD803E alpha 1.0
  Copper_TX                                9068 triangles  material Copper #CD803E alpha 1.0
  Top Solder Mask                         33728 triangles  material Top Solder Mask #126830 alpha 0.8
  Bottom Solder Mask                      63402 triangles  material Bottom Solder Mask #126830 alpha 0.8

Verifier: PASS
  Board_dielectric 1                   closed=True winding=True volume=2530.6188 mm3
  Copper_1                             closed=True winding=True volume=2.1699 mm3
  Copper_2                             closed=True winding=True volume=2.1699 mm3
  Copper_TX                            closed=True winding=True volume=3.1673 mm3
  Top Solder Mask                      closed=True winding=True volume=16.0024 mm3
  Bottom Solder Mask                   closed=True winding=True volume=16.2848 mm3
  overlap between different parts along 3000 vertical rays: worst 0.000 um
  gltf_validator not on PATH: glTF validation skipped
```

## 5.2 Coil Stator (4 Layers)

`Input/Coil_30_50_4_1_3_Series_SteppedDiagonal_Stator.kicad_pcb`, KiCad file format 20221018.
A 4-layer inductive encoder stator, 50 mm outer radius, four loops, with the nets `SIN_Signal`,
`COS_Signal` and `TX`. 6,216 track segments and 53 vias across `F.Cu`, `In1.Cu`, `In2.Cu` and
`B.Cu`.

What this board shows:

- A **4-layer board without a stack-up**: the 1.6 mm laminate is split evenly into three
  dielectrics between the four copper layers (`Board.DIELECTRIC_SPLIT = "even"`), each
  0.51 mm after the inner copper is taken out.
- 53 through vias joining the loops on all four layers (no blind or buried vias).
- The largest example: exporting it in simulation mode with the Verifier takes 48 s on the test
  machine (31 s of it in assembly, mostly preparing the two solder masks; 7 s verifying) and gives
  a GLB of 15.1 MB; the visual-mode GLB is 10.2 MB and takes 50 s.

| Part | Triangles |
|---|---|
| `Copper_SIN_Signal` | 42,436 |
| `Copper_COS_Signal` | 42,444 |
| `Copper_TX` | 24,384 |
| `Board_dielectric 1` to `3` (FR4, 0.51 mm each) | 57,220 together |
| `Top Solder Mask`, `Bottom Solder Mask` | 212,518 together |

## 5.3 Running The Examples

```bash
python run_KESE.py                                     # both boards, simulation, GLB in metres
python run_KESE.py Input/Stator.kicad_pcb --for viewer # visual mode for <model-viewer>
python run_KESE.py Input/Stator.kicad_pcb --for openems
```

| Previous | Next |
|:---|---:|
| [Project Capabilities](Project-Capabilities.md) | [Working Principle](Working-Principle.md) |
