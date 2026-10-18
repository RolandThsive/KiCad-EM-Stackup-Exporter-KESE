# 5. Examples

The repository ships three boards in `Input/`. `python run_KESE.py` with no arguments exports all
of them. The boards in `Tests/boards/` are small synthetic boards for the regression suite and are
described in [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md).

<!-- Pictures wanted for this page (made by Roland):
     Examples 1: the Coil stator GLB rendered in a viewer, simulation mode, copper per net in its own colour.
     Examples 2: the same board in visual mode.
     Examples 3: the XIAO ESP32C3 board, top view, mask and silkscreen visible. -->

## 5.1 Stator (2 Layers)

`Input/Stator.kicad_pcb`, KiCad file format 20221018 (KiCad 7). A 2-layer inductive encoder
stator with one loop and three nets: `TX`, `1` and `2`. 2,414 track segments and 13 through
vias, no footprints, no zones, no stack-up block in the file.

What this board shows:

- A board **without a stack-up** in Board Setup: the laminate is the file's `(general (thickness 1.6))`,
  one FR4 core with the default εr 4.5 and tanδ 0.02, copper 35 µm from the defaults.
- Copper per net: `Copper_TX`, `Copper_1` and `Copper_2`, each with its vias joined.
- Mask with no openings except the via pads (the vias are tented by KiCad's default), so the two
  mask solids carry most of the triangles.

Output of `python run_KESE.py Input/Stator.kicad_pcb --format glb stl obj --verify`:

```text
stack-up
  copper layers: F.Cu, B.Cu
  laminate 1.6000 mm (file (general (thickness)) - no usable stackup)
  F.Cu     z +0.8000 .. +0.8350 mm  (foil 0.035 mm)
  B.Cu     z -0.8350 .. -0.8000 mm  (foil 0.035 mm)
  dielectric 1             core     FR4        1.6000 mm  er 4.5  tan d 0.02   z -0.8000 .. +0.8000

parts
  Board_dielectric 1                       3540 triangles
  Copper_1                                 9516 triangles
  Copper_2                                 9516 triangles
  Copper_TX                                9068 triangles
  Top Solder Mask                         33728 triangles
  Bottom Solder Mask                      63402 triangles

Verifier: PASS
  overlap between different parts along 3000 vertical rays: worst 0.000 um
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
- Blind / buried vias between inner layers, and through vias.
- The largest example: exporting it in simulation mode with the Verifier takes 47 s on the test
  machine (43 s of it joining the three nets' pieces) and gives a GLB of 15.1 MB; the visual-mode
  GLB is 10.2 MB and takes 50 s.

| Part | Triangles |
|---|---|
| `Copper_SIN_Signal` | 42,436 |
| `Copper_COS_Signal` | 42,444 |
| `Copper_TX` | 24,384 |
| `Board_dielectric 1` to `3` (FR4, 0.51 mm each) | 57,220 together |
| `Top Solder Mask`, `Bottom Solder Mask` | 212,518 together |

## 5.3 XIAO ESP32C3 (4 Layers, Footprints)

`Input/XIAO_ESP32C3_v1.3.kicad_pcb`, KiCad file format 20260206 (KiCad 10). A 4-layer
microcontroller module with 68 footprints, 207 pads, 449 track segments, 128 through vias, four
non-plated holes and 28 zone fills on the copper layers.

What this board shows:

- A **real production board** with footprints: pads of several shapes, pad mask openings with
  the board's pad-to-mask clearance, silkscreen text and footprint graphics, and filled zones
  (ground and power planes) on the inner layers.
- A KiCad 10 file: net names stored directly on items, per-via tenting.
- Many nets: 46 copper parts, one `Copper_<net>` solid per net (`Copper_GND` alone has 102,786
  triangles), plus `Copper_no_net` for copper that belongs to no net (board graphics, unconnected
  pads).
- **Castellated holes**: 14 plated holes are cut by the board edge; with the default
  `Copper.CASTELLATION = "auto"` they are plated as part-barrels on the notch wall.
- Silkscreen with 1,513 footprint graphics and 113 text items, drawn with the stroke font.
- The run takes 69 s in simulation mode on the test machine: the breakdown of 68 footprints
  (18 s), the geometry (8 s) and the union of the GND net (most of the 40 s of assembly).

`report.txt` of this board lists under `skipped` what KESE does not model, with a count for
each, so nothing is dropped silently:

```text
skipped
      14  footprint graphics on B.Fab (not a physical layer)
       2  footprint graphics on Cmts.User (not a physical layer)
      36  footprint graphics on F.CrtYd (not a physical layer)
     279  footprint graphics on F.Fab (not a physical layer)
       4  footprint graphics on F.Paste (not a physical layer)
       5  keepout / rule areas (no copper by design)
```

## 5.4 Running The Examples

```bash
python run_KESE.py                                     # all three, simulation, GLB in metres
python run_KESE.py Input/Stator.kicad_pcb --for viewer # visual mode for <model-viewer>
python run_KESE.py Input/Stator.kicad_pcb --for openems
```

| Previous | Next |
|:---|---:|
| [Project Capabilities](Project-Capabilities.md) | [Working Principle](Working-Principle.md) |
