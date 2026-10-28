# 5. Examples

The repository ships two boards in `Generator/Input/`. `python run_KESE.py` with no arguments exports both
of them. The boards in `tests/boards/` are small synthetic boards for the regression suite and are
described in [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md).

## 5.1 Stator (2 Layers)

`Input/Stator.kicad_pcb`, KiCad file format 20221018 (KiCad 7). A 2-layer inductive encoder
stator with one loop and three nets: `TX`, `1` and `2`. 2,414 track segments and 13 through
vias, no footprints, no zones, no stack-up block in the file.

![The Stator in simulation mode: its top, and its bottom seen from below, as a web viewer draws them, the copper showing faintly through the translucent mask; and a true-scale side profile through the TX via, where the 1.6 mm FR4 core, the copper on each face and the mask fill the cut](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/examples_3_stator_simulation.png)

![The Stator in visual mode, drawn the same way: the opaque mask, the tracks reading through it as Mask over Copper and the open via bores as the only copper in the file; in the same side profile only the mask's outside, the via's bore and the board's edge are left, and neither F.Cu nor B.Cu leaves anything in the cut](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/examples_4_stator_visual.png)

What this board shows:

- A board **without a stack-up** in Board Setup: the laminate is the file's `(general (thickness 1.6))`,
  one FR4 core with the default εr 4.5 and tanδ 0.02, copper 35 µm from the defaults.
- Copper per net: `Copper_TX`, `Copper_1` and `Copper_2`, each with its vias joined.
- No pad or drawn mask openings: the board has no pads, and its vias are tented (KiCad's default
  when the file sets nothing), so the mask covers their rings; only the 13 open via bores
  (0.4 mm drill less the 25 µm plated wall on each side: 0.35 mm across) pass through it. The two
  mask solids climb over every trace and carry three quarters of the triangles.

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
  Copper_1                                 9508 triangles  material Copper #CD803E alpha 1.0
  Copper_2                                 9516 triangles  material Copper #CD803E alpha 1.0
  Copper_TX                                9068 triangles  material Copper #CD803E alpha 1.0
  Top Solder Mask                         33814 triangles  material Top Solder Mask #EBEBE6 alpha 0.8
  Bottom Solder Mask                      63646 triangles  material Bottom Solder Mask #EBEBE6 alpha 0.8

Verifier: PASS
  Board_dielectric 1                   closed=True winding=True volume=2530.6188 mm3
  Copper_1                             closed=True winding=True volume=2.1699 mm3
  Copper_2                             closed=True winding=True volume=2.1699 mm3
  Copper_TX                            closed=True winding=True volume=3.1674 mm3
  Top Solder Mask                      closed=True winding=True volume=16.0024 mm3
  Bottom Solder Mask                   closed=True winding=True volume=16.2848 mm3
  overlap between different parts, every slice against the others: none
  gltf_validator not on PATH: glTF validation skipped
  Board_dielectric 1                   volume from faces 2530.618759 mesh 2530.618759 slices 2530.618759 prisms 2530.618759 mm3 closed=True whole=True
  ...
```

The volume lines are explained in
[Checks, Errors And Warnings](Checks-Errors-And-Warnings.md#173-the-verifier).

## 5.2 Coil Stator (4 Layers)

`Input/Coil_30_50_4_1_3_Series_SteppedDiagonal_Stator.kicad_pcb`, KiCad file format 20221018.
A 4-layer inductive encoder stator, a ring from 30 to 50 mm radius, with the nets `SIN_Signal`,
`COS_Signal` and `TX`. 6,216 track segments and 53 through vias: the sine and cosine loops run on
`F.Cu` and `In1.Cu`, with a short run on `In2.Cu` at each pair of vias, and the three turns of the
`TX` coil on `F.Cu` and `B.Cu`.

![The Coil stator in simulation mode as a web viewer draws it: the whole board with its translucent mask, the same with the masks hidden and each net's copper in its own colour, and a close-up of the right edge with only the copper shown, at its true heights on the four layers, joined by the through vias](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/examples_1_coil_simulation.png)

![The Coil stator in visual mode, drawn exactly as the simulation picture: the whole board with its opaque mask, the same with the masks hidden, where only the laminate's edge walls and the walls of the 53 via bores are left, and the close-up of the right edge, where each net keeps only the walls of its via bores](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/examples_2_coil_visual.png)

What this board shows:

- A **4-layer board without a stack-up**: the 1.6 mm laminate is split evenly into three
  dielectrics between the four copper layers (`Board.DIELECTRIC_SPLIT = "even"`), each
  0.51 mm after the inner copper is taken out.
- Copper per net across layers: each of the three nets is one solid, its tracks on every layer
  joined by the barrels and rings of its vias (53 through vias, a ring on every layer; no blind
  or buried vias).
- The largest example: exporting it in simulation mode with the Verifier takes 7 s on a 4-core
  machine (3.8 s of it in assembly, 1.5 s verifying) and gives a GLB of 13.3 MB; the visual-mode
  GLB is 6.5 MB and takes 5 s, 7 s with the Verifier. In visual mode the copper under the mask
  is not in the file at all: each copper part keeps only the walls of its via bores.

| Part (simulation mode) | Triangles |
|---|---|
| `Copper_SIN_Signal` | 49,100 |
| `Copper_COS_Signal` | 49,096 |
| `Copper_TX` | 24,640 |
| `Board_dielectric 1` to `3` (FR4, 0.51 mm each) | 57,216 together |
| `Top Solder Mask`, `Bottom Solder Mask` | 213,788 together |

## 5.3 Running The Examples

```bash
cd Generator                                           # the program folder
python run_KESE.py                                     # both boards, simulation, GLB in metres
python run_KESE.py Input/Stator.kicad_pcb --for viewer # visual mode for <model-viewer>
python run_KESE.py Input/Stator.kicad_pcb --for openems
```

| Previous | Next |
|:---|---:|
| [Project Capabilities](Project-Capabilities.md) | [Working Principle](Working-Principle.md) |
