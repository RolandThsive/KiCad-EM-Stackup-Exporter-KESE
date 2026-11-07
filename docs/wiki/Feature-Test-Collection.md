# 23. Feature Test Collection

Every board of `featureTest/`, section by section, with its top and bottom and where the time of a
run goes:

- [The folder's README](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/main/featureTest/README.md) says what each board holds.
- Each board was exported three times in each mode, with the Verifier, the solder mask and the
  silkscreen on, as the regression suite (`Generator/tests/test_boards.py`) runs them.
- Each bar is the median of the three runs for that stage, from the `timing` block of
  [`report.txt`](Project-Output-Organization.md#2022-reporttxt).
- The commands, for board 11:

```text
python run_KESE.py ../featureTest/11_zones.kicad_pcb --mode simulation --format glb step --verify \
    --set SolderMask.SOLDER_MASK_ENABLED=True --set Silkscreen.SILKSCREEN_ENABLED=True
python run_KESE.py ../featureTest/11_zones.kicad_pcb --mode visual --format glb --verify \
    --set SolderMask.SOLDER_MASK_ENABLED=True --set Silkscreen.SILKSCREEN_ENABLED=True
```

**The runs used the default parameters otherwise, on one Linux machine with 4 cores (an Intel Xeon
at 2.1 GHz) and 16 GB of RAM, so `Parallel.WORKERS = 0` gave four workers ([Work Done In
Parallel](Working-Principle.md#74-work-done-in-parallel)). On another machine the seconds differ.**

## 23.1 Every Board At A Glance

![Every board's total time in both modes, seconds a run](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_0_all_boards.webp)

All the feature boards but 16b take 0.2 to 2.4 s a run. The fixed part of a run, reading the file and
Python starting and exiting, takes 0.16 to 0.29 s of it; a board without text never reads the stroke
font, so boards 05, 08b and 19b read and collect in under 5 ms. Board 16b, a plated border and 91
vias on four layers, takes 6.4 to 7.0 s, and the example boards 7 to 19 s.

## 23.2 Holes And Vias

### 23.2.1 01 Slotted Holes

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/01_holes_slotted/top_straight_visual.webp" width="49.5%" alt="01 Slotted holes straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/01_holes_slotted/bottom_straight_visual.webp" width="49.5%" alt="01 Slotted holes straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![01 Slotted holes: stacked bars of seconds per stage; stages 4 and 6 take 41% to 66% of a run. Simulation with GLB and STEP takes 1.2 s: read 72 ms, resolve 55 ms, geometry 0.2, materials 0.1 ms, assemble 0.3, write 0.4, verify 38 ms, start-up and exit 0.2. Visual with GLB takes 1.1 s: read 74 ms, resolve 51 ms, geometry 0.2, materials 0.1 ms, assemble 0.6, write 5 ms, verify 43 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_01_holes_slotted.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 72 ms | 55 ms | 0.2 | 0.1 ms | 0.3 | 0.4 | 38 ms | 0.2 | 1.2 |
| Visual, GLB | 74 ms | 51 ms | 0.2 | 0.1 ms | 0.6 | 5 ms | 43 ms | 0.2 | 1.1 |

<div align="center">

| Board | `featureTest/01_holes_slotted.kicad_pcb` |
|---|---|
| Outline | 40 × 26 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.2.2 02 Round Holes

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/02_holes_round/top_straight_visual.webp" width="49.5%" alt="02 Round holes straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/02_holes_round/bottom_straight_visual.webp" width="49.5%" alt="02 Round holes straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![02 Round holes: stacked bars of seconds per stage; stages 4 and 6 take 46% to 65% of a run. Simulation with GLB and STEP takes 1.1 s: read 70 ms, resolve 43 ms, geometry 0.1, materials 0.1 ms, assemble 0.4, write 0.3, verify 33 ms, start-up and exit 0.2. Visual with GLB takes 1.0 s: read 71 ms, resolve 41 ms, geometry 0.2, materials 0.1 ms, assemble 0.5, write 6 ms, verify 49 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_02_holes_round.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 70 ms | 43 ms | 0.1 | 0.1 ms | 0.4 | 0.3 | 33 ms | 0.2 | 1.1 |
| Visual, GLB | 71 ms | 41 ms | 0.2 | 0.1 ms | 0.5 | 6 ms | 49 ms | 0.2 | 1.0 |

<div align="center">

| Board | `featureTest/02_holes_round.kicad_pcb` |
|---|---|
| Outline | 34 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.2.3 03 Through Vias

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/03_vias_through/top_straight_visual.webp" width="49.5%" alt="03 Through vias straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/03_vias_through/bottom_straight_visual.webp" width="49.5%" alt="03 Through vias straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![03 Through vias: stacked bars of seconds per stage; stages 4 and 6 take 51% to 69% of a run. Simulation with GLB and STEP takes 1.5 s: read 80 ms, resolve 59 ms, geometry 0.2, materials 0.1 ms, assemble 0.5, write 0.3, verify 49 ms, start-up and exit 0.2. Visual with GLB takes 1.2 s: read 70 ms, resolve 48 ms, geometry 0.2, materials 0.2 ms, assemble 0.6, write 6 ms, verify 59 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_03_vias_through.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 80 ms | 59 ms | 0.2 | 0.1 ms | 0.5 | 0.3 | 49 ms | 0.2 | 1.5 |
| Visual, GLB | 70 ms | 48 ms | 0.2 | 0.2 ms | 0.6 | 6 ms | 59 ms | 0.2 | 1.2 |

<div align="center">

| Board | `featureTest/03_vias_through.kicad_pcb` |
|---|---|
| Outline | 32 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 12 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.2.4 03b KiCad 10 Via Options

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/03b_vias_k10/top_straight_visual.webp" width="49.5%" alt="03b KiCad 10 via options straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/03b_vias_k10/bottom_straight_visual.webp" width="49.5%" alt="03b KiCad 10 via options straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![03b KiCad 10 via options: stacked bars of seconds per stage; stages 4 and 6 take 38% to 74% of a run. Simulation with GLB and STEP takes 1.8 s: read 73 ms, resolve 0.1, geometry 0.2, materials 0.1 ms, assemble 0.5, write 0.7, verify 49 ms, start-up and exit 0.2. Visual with GLB takes 1.8 s: read 71 ms, resolve 0.1, geometry 0.2, materials 0.2 ms, assemble 1.2, write 9 ms, verify 66 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_03b_vias_k10.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 73 ms | 0.1 | 0.2 | 0.1 ms | 0.5 | 0.7 | 49 ms | 0.2 | 1.8 |
| Visual, GLB | 71 ms | 0.1 | 0.2 | 0.2 ms | 1.2 | 9 ms | 66 ms | 0.2 | 1.8 |

<div align="center">

| Board | `featureTest/03b_vias_k10.kicad_pcb` |
|---|---|
| Outline | 40 × 30 mm |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 18: 1 micro, 2 blind and buried, 15 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.2.5 04 Blind And Buried Vias

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/04_vias_blind_buried/top_straight_visual.webp" width="49.5%" alt="04 Blind and buried vias straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/04_vias_blind_buried/bottom_straight_visual.webp" width="49.5%" alt="04 Blind and buried vias straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![04 Blind and buried vias: stacked bars of seconds per stage; stages 4 and 6 take 37% to 55% of a run. Simulation with GLB and STEP takes 0.7 s: read 68 ms, resolve 59 ms, geometry 78 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 21 ms, start-up and exit 0.2. Visual with GLB takes 0.8 s: read 71 ms, resolve 52 ms, geometry 58 ms, materials 0.1 ms, assemble 0.4, write 4 ms, verify 34 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_04_vias_blind_buried.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 68 ms | 59 ms | 78 ms | 0.1 ms | 0.2 | 0.1 | 21 ms | 0.2 | 0.7 |
| Visual, GLB | 71 ms | 52 ms | 58 ms | 0.1 ms | 0.4 | 4 ms | 34 ms | 0.2 | 0.8 |

<div align="center">

| Board | `featureTest/04_vias_blind_buried.kicad_pcb` |
|---|---|
| Outline | 32 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 6 |
| Vias | 6: 3 blind and buried, 3 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.2.6 05 Microvias

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/05_vias_micro/top_straight_visual.webp" width="49.5%" alt="05 Microvias straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/05_vias_micro/bottom_straight_visual.webp" width="49.5%" alt="05 Microvias straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![05 Microvias: stacked bars of seconds per stage; stages 4 and 6 take 40% to 57% of a run. Simulation with GLB and STEP takes 0.6 s: read 3 ms, resolve 60 ms, geometry 52 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 21 ms, start-up and exit 0.2. Visual with GLB takes 0.6 s: read 2 ms, resolve 54 ms, geometry 43 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 54 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_05_vias_micro.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 3 ms | 60 ms | 52 ms | 0.1 ms | 0.2 | 0.1 | 21 ms | 0.2 | 0.6 |
| Visual, GLB | 2 ms | 54 ms | 43 ms | 0.1 ms | 0.3 | 3 ms | 54 ms | 0.2 | 0.6 |

<div align="center">

| Board | `featureTest/05_vias_micro.kicad_pcb` |
|---|---|
| Outline | 30 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 8 |
| Vias | 12: 10 micro, 2 blind and buried |
| Board edge | Plain |
| Mask, silkscreen, finish | Mask colour not set (drawn green), no silkscreen, ENIG |

</div>

## 23.3 Pads

### 23.3.1 06 Padstacks

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/06_padstacks/top_straight_visual.webp" width="49.5%" alt="06 Padstacks straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/06_padstacks/bottom_straight_visual.webp" width="49.5%" alt="06 Padstacks straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![06 Padstacks: stacked bars of seconds per stage; stages 4 and 6 take 42% to 62% of a run. Simulation with GLB and STEP takes 1.0 s: read 60 ms, resolve 45 ms, geometry 89 ms, materials 0.1 ms, assemble 0.3, write 0.2, verify 38 ms, start-up and exit 0.2. Visual with GLB takes 0.9 s: read 71 ms, resolve 46 ms, geometry 79 ms, materials 0.1 ms, assemble 0.5, write 4 ms, verify 36 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_06_padstacks.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 60 ms | 45 ms | 89 ms | 0.1 ms | 0.3 | 0.2 | 38 ms | 0.2 | 1.0 |
| Visual, GLB | 71 ms | 46 ms | 79 ms | 0.1 ms | 0.5 | 4 ms | 36 ms | 0.2 | 0.9 |

<div align="center">

| Board | `featureTest/06_padstacks.kicad_pcb` |
|---|---|
| Outline | 34 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 3 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.3.2 07 Pad Shapes

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/07_pad_shapes/top_straight_visual.webp" width="49.5%" alt="07 Pad shapes straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/07_pad_shapes/bottom_straight_visual.webp" width="49.5%" alt="07 Pad shapes straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![07 Pad shapes: stacked bars of seconds per stage; stages 4 and 6 take 39% to 64% of a run. Simulation with GLB and STEP takes 1.0 s: read 71 ms, resolve 37 ms, geometry 0.1, materials 0.1 ms, assemble 0.3, write 0.3, verify 27 ms, start-up and exit 0.2. Visual with GLB takes 1.0 s: read 75 ms, resolve 40 ms, geometry 0.1, materials 0.1 ms, assemble 0.5, write 5 ms, verify 40 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_07_pad_shapes.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 71 ms | 37 ms | 0.1 | 0.1 ms | 0.3 | 0.3 | 27 ms | 0.2 | 1.0 |
| Visual, GLB | 75 ms | 40 ms | 0.1 | 0.1 ms | 0.5 | 5 ms | 40 ms | 0.2 | 1.0 |

<div align="center">

| Board | `featureTest/07_pad_shapes.kicad_pcb` |
|---|---|
| Outline | 44 × 30 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

## 23.4 Copper Drawings, Text And Tracks

### 23.4.1 08 Copper Graphics

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/08_copper_graphics/top_straight_visual.webp" width="49.5%" alt="08 Copper graphics straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/08_copper_graphics/bottom_straight_visual.webp" width="49.5%" alt="08 Copper graphics straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![08 Copper graphics: stacked bars of seconds per stage; stages 4 and 6 take 34% to 53% of a run. Simulation with GLB and STEP takes 0.7 s: read 71 ms, resolve 25 ms, geometry 41 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 16 ms, start-up and exit 0.2. Visual with GLB takes 0.6 s: read 61 ms, resolve 23 ms, geometry 35 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 44 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_08_copper_graphics.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 71 ms | 25 ms | 41 ms | 0.1 ms | 0.2 | 0.2 | 16 ms | 0.2 | 0.7 |
| Visual, GLB | 61 ms | 23 ms | 35 ms | 0.1 ms | 0.3 | 4 ms | 44 ms | 0.2 | 0.6 |

<div align="center">

| Board | `featureTest/08_copper_graphics.kicad_pcb` |
|---|---|
| Outline | 30 × 24 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.4.2 08b Copper Graphics On Nets

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/08b_copper_graphics_nets/top_straight_visual.webp" width="49.5%" alt="08b Copper graphics on nets straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/08b_copper_graphics_nets/bottom_straight_visual.webp" width="49.5%" alt="08b Copper graphics on nets straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![08b Copper graphics on nets: stacked bars of seconds per stage; stages 4 and 6 take 36% to 58% of a run. Simulation with GLB and STEP takes 0.6 s: read 4 ms, resolve 21 ms, geometry 45 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 19 ms, start-up and exit 0.2. Visual with GLB takes 0.6 s: read 4 ms, resolve 21 ms, geometry 48 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 45 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_08b_copper_graphics_nets.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 4 ms | 21 ms | 45 ms | 0.1 ms | 0.2 | 0.2 | 19 ms | 0.2 | 0.6 |
| Visual, GLB | 4 ms | 21 ms | 48 ms | 0.1 ms | 0.3 | 4 ms | 45 ms | 0.2 | 0.6 |

<div align="center">

| Board | `featureTest/08b_copper_graphics_nets.kicad_pcb` |
|---|---|
| Outline | 36 × 24 mm, rounded corners |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.4.3 09 Copper Text

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/09_copper_text/top_straight_visual.webp" width="49.5%" alt="09 Copper text straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/09_copper_text/bottom_straight_visual.webp" width="49.5%" alt="09 Copper text straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![09 Copper text: stacked bars of seconds per stage; stages 4 and 6 take 45% to 72% of a run. Simulation with GLB and STEP takes 2.4 s: read 81 ms, resolve 36 ms, geometry 0.1, materials 0.1 ms, assemble 1.0, write 1.0, verify 37 ms, start-up and exit 0.2. Visual with GLB takes 1.4 s: read 82 ms, resolve 38 ms, geometry 0.1, materials 0.1 ms, assemble 0.9, write 8 ms, verify 82 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_09_copper_text.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 81 ms | 36 ms | 0.1 | 0.1 ms | 1.0 | 1.0 | 37 ms | 0.2 | 2.4 |
| Visual, GLB | 82 ms | 38 ms | 0.1 | 0.1 ms | 0.9 | 8 ms | 82 ms | 0.2 | 1.4 |

<div align="center">

| Board | `featureTest/09_copper_text.kicad_pcb` |
|---|---|
| Outline | 44 × 40 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.4.4 10 Tracks And Arcs

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/10_tracks_arcs/top_straight_visual.webp" width="49.5%" alt="10 Tracks and arcs straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/10_tracks_arcs/bottom_straight_visual.webp" width="49.5%" alt="10 Tracks and arcs straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![10 Tracks and arcs: stacked bars of seconds per stage; stages 4 and 6 take 33% to 55% of a run. Simulation with GLB and STEP takes 0.7 s: read 73 ms, resolve 28 ms, geometry 35 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 17 ms, start-up and exit 0.2. Visual with GLB takes 0.7 s: read 68 ms, resolve 24 ms, geometry 31 ms, materials 0.1 ms, assemble 0.4, write 4 ms, verify 39 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_10_tracks_arcs.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 73 ms | 28 ms | 35 ms | 0.1 ms | 0.2 | 0.2 | 17 ms | 0.2 | 0.7 |
| Visual, GLB | 68 ms | 24 ms | 31 ms | 0.1 ms | 0.4 | 4 ms | 39 ms | 0.2 | 0.7 |

<div align="center">

| Board | `featureTest/10_tracks_arcs.kicad_pcb` |
|---|---|
| Outline | 44 × 24 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

## 23.5 Zones

### 23.5.1 11 Zones

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/11_zones/top_straight_visual.webp" width="49.5%" alt="11 Zones straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/11_zones/bottom_straight_visual.webp" width="49.5%" alt="11 Zones straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![11 Zones: stacked bars of seconds per stage; stages 4 and 6 take 42% to 80% of a run. Simulation with GLB and STEP takes 2.2 s: read 83 ms, resolve 0.1, geometry 0.3, materials 0.2 ms, assemble 0.6, write 0.8, verify 75 ms, start-up and exit 0.2. Visual with GLB takes 2.2 s: read 77 ms, resolve 0.1, geometry 0.4, materials 0.2 ms, assemble 1.4, write 9 ms, verify 67 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_11_zones.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 83 ms | 0.1 | 0.3 | 0.2 ms | 0.6 | 0.8 | 75 ms | 0.2 | 2.2 |
| Visual, GLB | 77 ms | 0.1 | 0.4 | 0.2 ms | 1.4 | 9 ms | 67 ms | 0.2 | 2.2 |

<div align="center">

| Board | `featureTest/11_zones.kicad_pcb` |
|---|---|
| Outline | 40 × 31 mm |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

## 23.6 Board Outline

### 23.6.1 12 Board Outline Shapes

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/12_outline_shapes/top_straight_visual.webp" width="49.5%" alt="12 Board outline shapes straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/12_outline_shapes/bottom_straight_visual.webp" width="49.5%" alt="12 Board outline shapes straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![12 Board outline shapes: stacked bars of seconds per stage; stages 4 and 6 take 30% to 60% of a run. Simulation with GLB and STEP takes 1.6 s: read 73 ms, resolve 44 ms, geometry 78 ms, materials 0.1 ms, assemble 0.4, write 0.8, verify 24 ms, start-up and exit 0.2. Visual with GLB takes 0.9 s: read 80 ms, resolve 35 ms, geometry 67 ms, materials 0.1 ms, assemble 0.5, write 8 ms, verify 61 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_12_outline_shapes.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 73 ms | 44 ms | 78 ms | 0.1 ms | 0.4 | 0.8 | 24 ms | 0.2 | 1.6 |
| Visual, GLB | 80 ms | 35 ms | 67 ms | 0.1 ms | 0.5 | 8 ms | 61 ms | 0.2 | 0.9 |

<div align="center">

| Board | `featureTest/12_outline_shapes.kicad_pcb` |
|---|---|
| Outline | 40 × 30.9 mm, arcs, a Bezier edge, a notch and cut-outs |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.6.2 13a No Board Outline

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/13a_outline_none/top_straight_visual.webp" width="49.5%" alt="13a No board outline straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/13a_outline_none/bottom_straight_visual.webp" width="49.5%" alt="13a No board outline straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![13a No board outline: stacked bars of seconds per stage; stages 4 and 6 take 32% to 43% of a run. Simulation with GLB and STEP takes 0.5 s: read 57 ms, resolve 24 ms, geometry 53 ms, materials 0.1 ms, assemble 0.1, write 0.1, verify 17 ms, start-up and exit 0.2. Visual with GLB takes 0.6 s: read 62 ms, resolve 25 ms, geometry 46 ms, materials 0.1 ms, assemble 0.2, write 4 ms, verify 79 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_13a_outline_none.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 57 ms | 24 ms | 53 ms | 0.1 ms | 0.1 | 0.1 | 17 ms | 0.2 | 0.5 |
| Visual, GLB | 62 ms | 25 ms | 46 ms | 0.1 ms | 0.2 | 4 ms | 79 ms | 0.2 | 0.6 |

<div align="center">

| Board | `featureTest/13a_outline_none.kicad_pcb` |
|---|---|
| Outline | 13.7 × 7.2 mm, from the copper (no Edge.Cuts) |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Mask colour not set (drawn green), no silkscreen, ENIG |

</div>

### 23.6.3 13b Two Board Outlines

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/13b_outline_two/top_straight_visual.webp" width="49.5%" alt="13b Two board outlines straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/13b_outline_two/bottom_straight_visual.webp" width="49.5%" alt="13b Two board outlines straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![13b Two board outlines: stacked bars of seconds per stage; reading, start-up and exit take 42% to 51% of a run. Simulation with GLB and STEP takes 0.5 s: read 70 ms, resolve 21 ms, geometry 38 ms, materials 0.1 ms, assemble 83 ms, write 97 ms, verify 14 ms, start-up and exit 0.2. Visual with GLB takes 0.5 s: read 58 ms, resolve 20 ms, geometry 40 ms, materials 0.1 ms, assemble 0.2, write 3 ms, verify 25 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_13b_outline_two.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 70 ms | 21 ms | 38 ms | 0.1 ms | 83 ms | 97 ms | 14 ms | 0.2 | 0.5 |
| Visual, GLB | 58 ms | 20 ms | 40 ms | 0.1 ms | 0.2 | 3 ms | 25 ms | 0.2 | 0.5 |

<div align="center">

| Board | `featureTest/13b_outline_two.kicad_pcb` |
|---|---|
| Outline | 40 × 20 mm, two boards and a third in a hole |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

## 23.7 Stack-Up

### 23.7.1 14 Full Stack-Up

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/14_stackup_full/top_straight_visual.webp" width="49.5%" alt="14 Full stack-up straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/14_stackup_full/bottom_straight_visual.webp" width="49.5%" alt="14 Full stack-up straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![14 Full stack-up: stacked bars of seconds per stage; stages 4 and 6 take 33% to 54% of a run. Simulation with GLB and STEP takes 0.6 s: read 67 ms, resolve 33 ms, geometry 72 ms, materials 0.1 ms, assemble 0.1, write 0.1, verify 19 ms, start-up and exit 0.2. Visual with GLB takes 0.7 s: read 71 ms, resolve 32 ms, geometry 64 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 37 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_14_stackup_full.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 67 ms | 33 ms | 72 ms | 0.1 ms | 0.1 | 0.1 | 19 ms | 0.2 | 0.6 |
| Visual, GLB | 71 ms | 32 ms | 64 ms | 0.1 ms | 0.3 | 3 ms | 37 ms | 0.2 | 0.7 |

<div align="center">

| Board | `featureTest/14_stackup_full.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.58 mm |
| Copper layers | 4 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Green, white, ENIG |

</div>

### 23.7.2 15 No Stack-Up

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/15_stackup_none/top_straight_visual.webp" width="49.5%" alt="15 No stack-up straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/15_stackup_none/bottom_straight_visual.webp" width="49.5%" alt="15 No stack-up straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![15 No stack-up: stacked bars of seconds per stage; stages 4 and 6 take 29% to 56% of a run. Simulation with GLB and STEP takes 0.6 s: read 69 ms, resolve 35 ms, geometry 51 ms, materials 0.1 ms, assemble 0.1, write 0.1, verify 18 ms, start-up and exit 0.2. Visual with GLB takes 0.7 s: read 64 ms, resolve 31 ms, geometry 55 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 32 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_15_stackup_none.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 69 ms | 35 ms | 51 ms | 0.1 ms | 0.1 | 0.1 | 18 ms | 0.2 | 0.6 |
| Visual, GLB | 64 ms | 31 ms | 55 ms | 0.1 ms | 0.3 | 3 ms | 32 ms | 0.2 | 0.7 |

<div align="center">

| Board | `featureTest/15_stackup_none.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.2 mm |
| Copper layers | 4 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

## 23.8 Edge Plating

### 23.8.1 16 Castellated Pads And A Plated Edge

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/16_edge_plating_castellation/top_straight_visual.webp" width="49.5%" alt="16 Castellated pads and a plated edge straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/16_edge_plating_castellation/bottom_straight_visual.webp" width="49.5%" alt="16 Castellated pads and a plated edge straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![16 Castellated pads and a plated edge: stacked bars of seconds per stage; stages 4 and 6 take 34% to 52% of a run. Simulation with GLB and STEP takes 0.8 s: read 70 ms, resolve 66 ms, geometry 82 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 25 ms, start-up and exit 0.2. Visual with GLB takes 0.7 s: read 60 ms, resolve 72 ms, geometry 97 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 31 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_16_edge_plating_castellation.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 70 ms | 66 ms | 82 ms | 0.1 ms | 0.2 | 0.1 | 25 ms | 0.2 | 0.8 |
| Visual, GLB | 60 ms | 72 ms | 97 ms | 0.1 ms | 0.3 | 3 ms | 31 ms | 0.2 | 0.7 |

<div align="center">

| Board | `featureTest/16_edge_plating_castellation.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Castellated pads on the right edge, plated edge |
| Mask, silkscreen, finish | Not set (drawn green and white), immersion silver |

</div>

### 23.8.2 16b Plated Board Edge With A GND Border

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/16b_edge_plating_border/top_straight_visual.webp" width="49.5%" alt="16b Plated board edge with a GND border straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/16b_edge_plating_border/bottom_straight_visual.webp" width="49.5%" alt="16b Plated board edge with a GND border straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![16b Plated board edge with a GND border: stacked bars of seconds per stage; stages 4 and 6 take 63% to 88% of a run. Simulation with GLB and STEP takes 6.4 s: read 0.1, resolve 0.4, geometry 1.9, materials 0.2 ms, assemble 2.1, write 1.4, verify 0.2, start-up and exit 0.2. Visual with GLB takes 7.0 s: read 98 ms, resolve 0.4, geometry 2.0, materials 0.2 ms, assemble 4.2, write 20 ms, verify 0.1, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_16b_edge_plating_border.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.1 | 0.4 | 1.9 | 0.2 ms | 2.1 | 1.4 | 0.2 | 0.2 | 6.4 |
| Visual, GLB | 98 ms | 0.4 | 2.0 | 0.2 ms | 4.2 | 20 ms | 0.1 | 0.2 | 7.0 |

<div align="center">

| Board | `featureTest/16b_edge_plating_border.kicad_pcb` |
|---|---|
| Outline | 40 × 28 mm, a cut-out |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 91 through |
| Board edge | Plated all round and in the cut-out |
| Mask, silkscreen, finish | Green, white, ENIG |

</div>

## 23.9 Solder Mask And Silkscreen

### 23.9.1 17 Solder Mask And Silkscreen

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/17_mask_silk/top_straight_visual.webp" width="49.5%" alt="17 Solder mask and silkscreen straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/17_mask_silk/bottom_straight_visual.webp" width="49.5%" alt="17 Solder mask and silkscreen straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![17 Solder mask and silkscreen: stacked bars of seconds per stage; stages 4 and 6 take 35% to 55% of a run. Simulation with GLB and STEP takes 0.8 s: read 71 ms, resolve 63 ms, geometry 91 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 18 ms, start-up and exit 0.2. Visual with GLB takes 0.8 s: read 71 ms, resolve 80 ms, geometry 0.1, materials 0.1 ms, assemble 0.3, write 5 ms, verify 40 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_17_mask_silk.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 71 ms | 63 ms | 91 ms | 0.1 ms | 0.2 | 0.2 | 18 ms | 0.2 | 0.8 |
| Visual, GLB | 71 ms | 80 ms | 0.1 | 0.1 ms | 0.3 | 5 ms | 40 ms | 0.2 | 0.8 |

<div align="center">

| Board | `featureTest/17_mask_silk.kicad_pcb` |
|---|---|
| Outline | 40 × 30 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Red, black, lead-free HASL |

</div>

### 23.9.2 17b Silkscreen Over Copper

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/17b_silk_over_copper/top_straight_visual.webp" width="49.5%" alt="17b Silkscreen over copper straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/17b_silk_over_copper/bottom_straight_visual.webp" width="49.5%" alt="17b Silkscreen over copper straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![17b Silkscreen over copper: stacked bars of seconds per stage; stages 4 and 6 take 42% to 65% of a run. Simulation with GLB and STEP takes 0.8 s: read 62 ms, resolve 30 ms, geometry 0.1, materials 0.1 ms, assemble 0.2, write 0.2, verify 28 ms, start-up and exit 0.2. Visual with GLB takes 1.1 s: read 75 ms, resolve 36 ms, geometry 0.2, materials 0.1 ms, assemble 0.5, write 5 ms, verify 35 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_17b_silk_over_copper.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 62 ms | 30 ms | 0.1 | 0.1 ms | 0.2 | 0.2 | 28 ms | 0.2 | 0.8 |
| Visual, GLB | 75 ms | 36 ms | 0.2 | 0.1 ms | 0.5 | 5 ms | 35 ms | 0.2 | 1.1 |

<div align="center">

| Board | `featureTest/17b_silk_over_copper.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | White, black, ENIG |

</div>

## 23.10 Surface Finish

### 23.10.1 18 Gold Edge Fingers

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18_finishes/top_straight_visual.webp" width="49.5%" alt="18 Gold edge fingers straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18_finishes/bottom_straight_visual.webp" width="49.5%" alt="18 Gold edge fingers straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![18 Gold edge fingers: stacked bars of seconds per stage; stages 4 and 6 take 32% to 53% of a run. Simulation with GLB and STEP takes 0.6 s: read 70 ms, resolve 32 ms, geometry 42 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 16 ms, start-up and exit 0.2. Visual with GLB takes 0.7 s: read 59 ms, resolve 30 ms, geometry 46 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 61 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_18_finishes.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 70 ms | 32 ms | 42 ms | 0.1 ms | 0.2 | 0.1 | 16 ms | 0.2 | 0.6 |
| Visual, GLB | 59 ms | 30 ms | 46 ms | 0.1 ms | 0.3 | 4 ms | 61 ms | 0.2 | 0.7 |

<div align="center">

| Board | `featureTest/18_finishes.kicad_pcb` |
|---|---|
| Outline | 30 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 6 through |
| Board edge | Gold edge fingers on a bevelled edge |
| Mask, silkscreen, finish | Not set (drawn green and white), hard gold |

</div>

### 23.10.2 18b Finish On Every Kind Of Bare Copper

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18b_finish_pads/top_straight_visual.webp" width="49.5%" alt="18b Finish on every kind of bare copper straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18b_finish_pads/bottom_straight_visual.webp" width="49.5%" alt="18b Finish on every kind of bare copper straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![18b Finish on every kind of bare copper: stacked bars of seconds per stage; stages 4 and 6 take 38% to 59% of a run. Simulation with GLB and STEP takes 0.8 s: read 73 ms, resolve 32 ms, geometry 92 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 24 ms, start-up and exit 0.2. Visual with GLB takes 0.9 s: read 70 ms, resolve 34 ms, geometry 95 ms, materials 0.1 ms, assemble 0.4, write 4 ms, verify 43 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_18b_finish_pads.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 73 ms | 32 ms | 92 ms | 0.1 ms | 0.2 | 0.2 | 24 ms | 0.2 | 0.8 |
| Visual, GLB | 70 ms | 34 ms | 95 ms | 0.1 ms | 0.4 | 4 ms | 43 ms | 0.2 | 0.9 |

<div align="center">

| Board | `featureTest/18b_finish_pads.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Green, white, ENIG |

</div>

### 23.10.3 18c Finish Before The Solder Mask

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18c_finish_before_mask/top_straight_visual.webp" width="49.5%" alt="18c Finish before the solder mask straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18c_finish_before_mask/bottom_straight_visual.webp" width="49.5%" alt="18c Finish before the solder mask straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![18c Finish before the solder mask: stacked bars of seconds per stage; stages 4 and 6 take 45% to 69% of a run. Simulation with GLB and STEP takes 1.1 s: read 71 ms, resolve 34 ms, geometry 0.1, materials 0.1 ms, assemble 0.3, write 0.3, verify 34 ms, start-up and exit 0.2. Visual with GLB takes 1.1 s: read 77 ms, resolve 35 ms, geometry 0.2, materials 0.1 ms, assemble 0.6, write 5 ms, verify 37 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_18c_finish_before_mask.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 71 ms | 34 ms | 0.1 | 0.1 ms | 0.3 | 0.3 | 34 ms | 0.2 | 1.1 |
| Visual, GLB | 77 ms | 35 ms | 0.2 | 0.1 ms | 0.6 | 5 ms | 37 ms | 0.2 | 1.1 |

<div align="center">

| Board | `featureTest/18c_finish_before_mask.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Blue, white, ENEPIG |

</div>

## 23.11 Items KESE Skips

### 23.11.1 19 Items KESE Skips

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/19_skipped_items/top_straight_visual.webp" width="49.5%" alt="19 Items KESE skips straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/19_skipped_items/bottom_straight_visual.webp" width="49.5%" alt="19 Items KESE skips straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![19 Items KESE skips: stacked bars of seconds per stage; reading, start-up and exit take 55% to 67% of a run. Simulation with GLB and STEP takes 0.4 s: read 70 ms, resolve 17 ms, geometry 21 ms, materials 0.1 ms, assemble 44 ms, write 45 ms, verify 8 ms, start-up and exit 0.2. Visual with GLB takes 0.4 s: read 58 ms, resolve 13 ms, geometry 21 ms, materials 0.1 ms, assemble 0.1, write 2 ms, verify 21 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_19_skipped_items.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 70 ms | 17 ms | 21 ms | 0.1 ms | 44 ms | 45 ms | 8 ms | 0.2 | 0.4 |
| Visual, GLB | 58 ms | 13 ms | 21 ms | 0.1 ms | 0.1 | 2 ms | 21 ms | 0.2 | 0.4 |

<div align="center">

| Board | `featureTest/19_skipped_items.kicad_pcb` |
|---|---|
| Outline | 40 × 30 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.11.2 19b Items KESE Skips, KiCad 10

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/19b_skipped_items_k10/top_straight_visual.webp" width="49.5%" alt="19b Items KESE skips, KiCad 10 straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/19b_skipped_items_k10/bottom_straight_visual.webp" width="49.5%" alt="19b Items KESE skips, KiCad 10 straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![19b Items KESE skips, KiCad 10: stacked bars of seconds per stage; reading, start-up and exit take 75% to 80% of a run. Simulation with GLB and STEP takes 0.2 s: read 0.7 ms, resolve 5 ms, geometry 11 ms, materials 0.0 ms, assemble 16 ms, write 7 ms, verify 2 ms, start-up and exit 0.2. Visual with GLB takes 0.2 s: read 0.7 ms, resolve 4 ms, geometry 11 ms, materials 0.0 ms, assemble 31 ms, write 1 ms, verify 11 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_19b_skipped_items_k10.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.7 ms | 5 ms | 11 ms | 0.0 ms | 16 ms | 7 ms | 2 ms | 0.2 | 0.2 |
| Visual, GLB | 0.7 ms | 4 ms | 11 ms | 0.0 ms | 31 ms | 1 ms | 11 ms | 0.2 | 0.2 |

<div align="center">

| Board | `featureTest/19b_skipped_items_k10.kicad_pcb` |
|---|---|
| Outline | 40 × 24 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Mask colour not set (drawn green), no silkscreen, ENIG |

</div>

## 23.12 KiCad File Formats

### 23.12.1 20a KiCad 6 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20a_format_kicad6/top_straight_visual.webp" width="49.5%" alt="20a KiCad 6 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20a_format_kicad6/bottom_straight_visual.webp" width="49.5%" alt="20a KiCad 6 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20a KiCad 6 format: stacked bars of seconds per stage; stages 4 and 6 take 31% to 51% of a run. Simulation with GLB and STEP takes 0.6 s: read 68 ms, resolve 27 ms, geometry 59 ms, materials 0.1 ms, assemble 0.1, write 0.1, verify 16 ms, start-up and exit 0.2. Visual with GLB takes 0.7 s: read 68 ms, resolve 31 ms, geometry 63 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 31 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20a_format_kicad6.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 68 ms | 27 ms | 59 ms | 0.1 ms | 0.1 | 0.1 | 16 ms | 0.2 | 0.6 |
| Visual, GLB | 68 ms | 31 ms | 63 ms | 0.1 ms | 0.3 | 4 ms | 31 ms | 0.2 | 0.7 |

<div align="center">

| Board | `featureTest/20a_format_kicad6.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.12.2 20b KiCad 7 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20b_format_kicad7/top_straight_visual.webp" width="49.5%" alt="20b KiCad 7 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20b_format_kicad7/bottom_straight_visual.webp" width="49.5%" alt="20b KiCad 7 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20b KiCad 7 format: stacked bars of seconds per stage; stages 4 and 6 take 33% to 53% of a run. Simulation with GLB and STEP takes 0.7 s: read 65 ms, resolve 26 ms, geometry 63 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 16 ms, start-up and exit 0.2. Visual with GLB takes 0.6 s: read 66 ms, resolve 28 ms, geometry 56 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 34 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20b_format_kicad7.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 65 ms | 26 ms | 63 ms | 0.1 ms | 0.2 | 0.1 | 16 ms | 0.2 | 0.7 |
| Visual, GLB | 66 ms | 28 ms | 56 ms | 0.1 ms | 0.3 | 4 ms | 34 ms | 0.2 | 0.6 |

<div align="center">

| Board | `featureTest/20b_format_kicad7.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.12.3 20c KiCad 8 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20c_format_kicad8/top_straight_visual.webp" width="49.5%" alt="20c KiCad 8 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20c_format_kicad8/bottom_straight_visual.webp" width="49.5%" alt="20c KiCad 8 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20c KiCad 8 format: stacked bars of seconds per stage; stages 4 and 6 take 33% to 50% of a run. Simulation with GLB and STEP takes 0.6 s: read 71 ms, resolve 28 ms, geometry 59 ms, materials 0.1 ms, assemble 0.1, write 0.1, verify 19 ms, start-up and exit 0.2. Visual with GLB takes 0.7 s: read 66 ms, resolve 28 ms, geometry 53 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 35 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20c_format_kicad8.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 71 ms | 28 ms | 59 ms | 0.1 ms | 0.1 | 0.1 | 19 ms | 0.2 | 0.6 |
| Visual, GLB | 66 ms | 28 ms | 53 ms | 0.1 ms | 0.3 | 4 ms | 35 ms | 0.2 | 0.7 |

<div align="center">

| Board | `featureTest/20c_format_kicad8.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.12.4 20d KiCad 9 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20d_format_kicad9/top_straight_visual.webp" width="49.5%" alt="20d KiCad 9 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20d_format_kicad9/bottom_straight_visual.webp" width="49.5%" alt="20d KiCad 9 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20d KiCad 9 format: stacked bars of seconds per stage; stages 4 and 6 take 31% to 52% of a run. Simulation with GLB and STEP takes 0.7 s: read 71 ms, resolve 27 ms, geometry 59 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 20 ms, start-up and exit 0.2. Visual with GLB takes 0.7 s: read 69 ms, resolve 31 ms, geometry 59 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 34 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20d_format_kicad9.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 71 ms | 27 ms | 59 ms | 0.1 ms | 0.2 | 0.2 | 20 ms | 0.2 | 0.7 |
| Visual, GLB | 69 ms | 31 ms | 59 ms | 0.1 ms | 0.3 | 4 ms | 34 ms | 0.2 | 0.7 |

<div align="center">

| Board | `featureTest/20d_format_kicad9.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

### 23.12.5 20e KiCad 10 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20e_format_kicad10/top_straight_visual.webp" width="49.5%" alt="20e KiCad 10 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20e_format_kicad10/bottom_straight_visual.webp" width="49.5%" alt="20e KiCad 10 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20e KiCad 10 format: stacked bars of seconds per stage; stages 4 and 6 take 31% to 54% of a run. Simulation with GLB and STEP takes 0.7 s: read 70 ms, resolve 30 ms, geometry 60 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 18 ms, start-up and exit 0.2. Visual with GLB takes 0.7 s: read 68 ms, resolve 32 ms, geometry 62 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 31 ms, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20e_format_kicad10.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 70 ms | 30 ms | 60 ms | 0.1 ms | 0.2 | 0.2 | 18 ms | 0.2 | 0.7 |
| Visual, GLB | 68 ms | 32 ms | 62 ms | 0.1 ms | 0.3 | 4 ms | 31 ms | 0.2 | 0.7 |

<div align="center">

| Board | `featureTest/20e_format_kicad10.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

</div>

## 23.13 Example Boards

### 23.13.1 21 RF Sensor Module

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/21_rf_module/top_straight_visual.webp" width="49.5%" alt="21 RF sensor module straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/21_rf_module/bottom_straight_visual.webp" width="49.5%" alt="21 RF sensor module straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![21 RF sensor module: stacked bars of seconds per stage; stages 4 and 6 take 68% to 84% of a run. Simulation with GLB and STEP takes 17.4 s: read 0.2, resolve 1.4, geometry 6.3, materials 0.4 ms, assemble 5.5, write 3.3, verify 0.5, start-up and exit 0.2. Visual with GLB takes 19.1 s: read 0.2, resolve 1.5, geometry 6.2, materials 0.4 ms, assemble 9.8, write 96 ms, verify 1.0, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_21_rf_module.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.2 | 1.4 | 6.3 | 0.4 ms | 5.5 | 3.3 | 0.5 | 0.2 | 17.4 |
| Visual, GLB | 0.2 | 1.5 | 6.2 | 0.4 ms | 9.8 | 96 ms | 1.0 | 0.2 | 19.1 |

<div align="center">

| Board | `featureTest/21_rf_module.kicad_pcb` ([5.1](Examples.md#51-rf-sensor-module)) |
|---|---|
| Outline | 64 × 44 mm, a cut-out |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 307 through |
| Board edge | Plated all round and in the cut-out |
| Mask, silkscreen, finish | Blue, white, ENIG |

</div>

### 23.13.2 22 HDI Radio Module

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/22_hdi_module/top_straight_visual.webp" width="49.5%" alt="22 HDI radio module straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/22_hdi_module/bottom_straight_visual.webp" width="49.5%" alt="22 HDI radio module straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![22 HDI radio module: stacked bars of seconds per stage; stages 4 and 6 take 55% to 82% of a run. Simulation with GLB and STEP takes 7.5 s: read 0.2, resolve 0.9, geometry 2.2, materials 0.4 ms, assemble 1.8, write 1.6, verify 0.4, start-up and exit 0.2. Visual with GLB takes 9.7 s: read 0.2, resolve 1.0, geometry 2.2, materials 0.4 ms, assemble 5.8, write 39 ms, verify 0.3, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_22_hdi_module.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.2 | 0.9 | 2.2 | 0.4 ms | 1.8 | 1.6 | 0.4 | 0.2 | 7.5 |
| Visual, GLB | 0.2 | 1.0 | 2.2 | 0.4 ms | 5.8 | 39 ms | 0.3 | 0.2 | 9.7 |

<div align="center">

| Board | `featureTest/22_hdi_module.kicad_pcb` ([5.2](Examples.md#52-hdi-radio-module)) |
|---|---|
| Outline | 22 × 30 mm |
| Thickness | 0.925 mm |
| Copper layers | 6 |
| Vias | 150: 71 micro, 34 blind and buried, 45 through |
| Board edge | 43 castellated pads |
| Mask, silkscreen, finish | Black, white, immersion silver |

</div>

### 23.13.3 23 PCIe x1 Card

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/23_pcie_card/top_straight_visual.webp" width="49.5%" alt="23 PCIe x1 card straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/23_pcie_card/bottom_straight_visual.webp" width="49.5%" alt="23 PCIe x1 card straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![23 PCIe x1 card: stacked bars of seconds per stage; stages 4 and 6 take 58% to 83% of a run. Simulation with GLB and STEP takes 12.0 s: read 0.2, resolve 1.1, geometry 3.4, materials 0.5 ms, assemble 3.5, write 2.9, verify 0.6, start-up and exit 0.2. Visual with GLB takes 15.9 s: read 0.3, resolve 1.1, geometry 3.4, materials 0.5 ms, assemble 9.9, write 88 ms, verify 1.0, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_23_pcie_card.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.2 | 1.1 | 3.4 | 0.5 ms | 3.5 | 2.9 | 0.6 | 0.2 | 12.0 |
| Visual, GLB | 0.3 | 1.1 | 3.4 | 0.5 ms | 9.9 | 88 ms | 1.0 | 0.2 | 15.9 |

<div align="center">

| Board | `featureTest/23_pcie_card.kicad_pcb` ([5.3](Examples.md#53-pcie-x1-card)) |
|---|---|
| Outline | 80 × 64.4 mm with the fingers' tongue, a slot |
| Thickness | 1.57 mm |
| Copper layers | 4 |
| Vias | 239 through |
| Board edge | 36 gold fingers on a bevelled tongue |
| Mask, silkscreen, finish | Green, white, hard gold |

</div>

## 23.14 The Numbers

Seconds, the median of three runs for each stage, unless marked ms; the total is the sum of the bars.

| Board | Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 Slotted holes | simulation, GLB + STEP | 72 ms | 55 ms | 0.2 | 0.1 ms | 0.3 | 0.4 | 38 ms | 0.2 | 1.2 |
| 01 Slotted holes | visual, GLB | 74 ms | 51 ms | 0.2 | 0.1 ms | 0.6 | 5 ms | 43 ms | 0.2 | 1.1 |
| 02 Round holes | simulation, GLB + STEP | 70 ms | 43 ms | 0.1 | 0.1 ms | 0.4 | 0.3 | 33 ms | 0.2 | 1.1 |
| 02 Round holes | visual, GLB | 71 ms | 41 ms | 0.2 | 0.1 ms | 0.5 | 6 ms | 49 ms | 0.2 | 1.0 |
| 03 Through vias | simulation, GLB + STEP | 80 ms | 59 ms | 0.2 | 0.1 ms | 0.5 | 0.3 | 49 ms | 0.2 | 1.5 |
| 03 Through vias | visual, GLB | 70 ms | 48 ms | 0.2 | 0.2 ms | 0.6 | 6 ms | 59 ms | 0.2 | 1.2 |
| 03b KiCad 10 via options | simulation, GLB + STEP | 73 ms | 0.1 | 0.2 | 0.1 ms | 0.5 | 0.7 | 49 ms | 0.2 | 1.8 |
| 03b KiCad 10 via options | visual, GLB | 71 ms | 0.1 | 0.2 | 0.2 ms | 1.2 | 9 ms | 66 ms | 0.2 | 1.8 |
| 04 Blind and buried vias | simulation, GLB + STEP | 68 ms | 59 ms | 78 ms | 0.1 ms | 0.2 | 0.1 | 21 ms | 0.2 | 0.7 |
| 04 Blind and buried vias | visual, GLB | 71 ms | 52 ms | 58 ms | 0.1 ms | 0.4 | 4 ms | 34 ms | 0.2 | 0.8 |
| 05 Microvias | simulation, GLB + STEP | 3 ms | 60 ms | 52 ms | 0.1 ms | 0.2 | 0.1 | 21 ms | 0.2 | 0.6 |
| 05 Microvias | visual, GLB | 2 ms | 54 ms | 43 ms | 0.1 ms | 0.3 | 3 ms | 54 ms | 0.2 | 0.6 |
| 06 Padstacks | simulation, GLB + STEP | 60 ms | 45 ms | 89 ms | 0.1 ms | 0.3 | 0.2 | 38 ms | 0.2 | 1.0 |
| 06 Padstacks | visual, GLB | 71 ms | 46 ms | 79 ms | 0.1 ms | 0.5 | 4 ms | 36 ms | 0.2 | 0.9 |
| 07 Pad shapes | simulation, GLB + STEP | 71 ms | 37 ms | 0.1 | 0.1 ms | 0.3 | 0.3 | 27 ms | 0.2 | 1.0 |
| 07 Pad shapes | visual, GLB | 75 ms | 40 ms | 0.1 | 0.1 ms | 0.5 | 5 ms | 40 ms | 0.2 | 1.0 |
| 08 Copper graphics | simulation, GLB + STEP | 71 ms | 25 ms | 41 ms | 0.1 ms | 0.2 | 0.2 | 16 ms | 0.2 | 0.7 |
| 08 Copper graphics | visual, GLB | 61 ms | 23 ms | 35 ms | 0.1 ms | 0.3 | 4 ms | 44 ms | 0.2 | 0.6 |
| 08b Copper graphics on nets | simulation, GLB + STEP | 4 ms | 21 ms | 45 ms | 0.1 ms | 0.2 | 0.2 | 19 ms | 0.2 | 0.6 |
| 08b Copper graphics on nets | visual, GLB | 4 ms | 21 ms | 48 ms | 0.1 ms | 0.3 | 4 ms | 45 ms | 0.2 | 0.6 |
| 09 Copper text | simulation, GLB + STEP | 81 ms | 36 ms | 0.1 | 0.1 ms | 1.0 | 1.0 | 37 ms | 0.2 | 2.4 |
| 09 Copper text | visual, GLB | 82 ms | 38 ms | 0.1 | 0.1 ms | 0.9 | 8 ms | 82 ms | 0.2 | 1.4 |
| 10 Tracks and arcs | simulation, GLB + STEP | 73 ms | 28 ms | 35 ms | 0.1 ms | 0.2 | 0.2 | 17 ms | 0.2 | 0.7 |
| 10 Tracks and arcs | visual, GLB | 68 ms | 24 ms | 31 ms | 0.1 ms | 0.4 | 4 ms | 39 ms | 0.2 | 0.7 |
| 11 Zones | simulation, GLB + STEP | 83 ms | 0.1 | 0.3 | 0.2 ms | 0.6 | 0.8 | 75 ms | 0.2 | 2.2 |
| 11 Zones | visual, GLB | 77 ms | 0.1 | 0.4 | 0.2 ms | 1.4 | 9 ms | 67 ms | 0.2 | 2.2 |
| 12 Board outline shapes | simulation, GLB + STEP | 73 ms | 44 ms | 78 ms | 0.1 ms | 0.4 | 0.8 | 24 ms | 0.2 | 1.6 |
| 12 Board outline shapes | visual, GLB | 80 ms | 35 ms | 67 ms | 0.1 ms | 0.5 | 8 ms | 61 ms | 0.2 | 0.9 |
| 13a No board outline | simulation, GLB + STEP | 57 ms | 24 ms | 53 ms | 0.1 ms | 0.1 | 0.1 | 17 ms | 0.2 | 0.5 |
| 13a No board outline | visual, GLB | 62 ms | 25 ms | 46 ms | 0.1 ms | 0.2 | 4 ms | 79 ms | 0.2 | 0.6 |
| 13b Two board outlines | simulation, GLB + STEP | 70 ms | 21 ms | 38 ms | 0.1 ms | 83 ms | 97 ms | 14 ms | 0.2 | 0.5 |
| 13b Two board outlines | visual, GLB | 58 ms | 20 ms | 40 ms | 0.1 ms | 0.2 | 3 ms | 25 ms | 0.2 | 0.5 |
| 14 Full stack-up | simulation, GLB + STEP | 67 ms | 33 ms | 72 ms | 0.1 ms | 0.1 | 0.1 | 19 ms | 0.2 | 0.6 |
| 14 Full stack-up | visual, GLB | 71 ms | 32 ms | 64 ms | 0.1 ms | 0.3 | 3 ms | 37 ms | 0.2 | 0.7 |
| 15 No stack-up | simulation, GLB + STEP | 69 ms | 35 ms | 51 ms | 0.1 ms | 0.1 | 0.1 | 18 ms | 0.2 | 0.6 |
| 15 No stack-up | visual, GLB | 64 ms | 31 ms | 55 ms | 0.1 ms | 0.3 | 3 ms | 32 ms | 0.2 | 0.7 |
| 16 Castellated pads and a plated edge | simulation, GLB + STEP | 70 ms | 66 ms | 82 ms | 0.1 ms | 0.2 | 0.1 | 25 ms | 0.2 | 0.8 |
| 16 Castellated pads and a plated edge | visual, GLB | 60 ms | 72 ms | 97 ms | 0.1 ms | 0.3 | 3 ms | 31 ms | 0.2 | 0.7 |
| 16b Plated board edge with a GND border | simulation, GLB + STEP | 0.1 | 0.4 | 1.9 | 0.2 ms | 2.1 | 1.4 | 0.2 | 0.2 | 6.4 |
| 16b Plated board edge with a GND border | visual, GLB | 98 ms | 0.4 | 2.0 | 0.2 ms | 4.2 | 20 ms | 0.1 | 0.2 | 7.0 |
| 17 Solder mask and silkscreen | simulation, GLB + STEP | 71 ms | 63 ms | 91 ms | 0.1 ms | 0.2 | 0.2 | 18 ms | 0.2 | 0.8 |
| 17 Solder mask and silkscreen | visual, GLB | 71 ms | 80 ms | 0.1 | 0.1 ms | 0.3 | 5 ms | 40 ms | 0.2 | 0.8 |
| 17b Silkscreen over copper | simulation, GLB + STEP | 62 ms | 30 ms | 0.1 | 0.1 ms | 0.2 | 0.2 | 28 ms | 0.2 | 0.8 |
| 17b Silkscreen over copper | visual, GLB | 75 ms | 36 ms | 0.2 | 0.1 ms | 0.5 | 5 ms | 35 ms | 0.2 | 1.1 |
| 18 Gold edge fingers | simulation, GLB + STEP | 70 ms | 32 ms | 42 ms | 0.1 ms | 0.2 | 0.1 | 16 ms | 0.2 | 0.6 |
| 18 Gold edge fingers | visual, GLB | 59 ms | 30 ms | 46 ms | 0.1 ms | 0.3 | 4 ms | 61 ms | 0.2 | 0.7 |
| 18b Finish on every kind of bare copper | simulation, GLB + STEP | 73 ms | 32 ms | 92 ms | 0.1 ms | 0.2 | 0.2 | 24 ms | 0.2 | 0.8 |
| 18b Finish on every kind of bare copper | visual, GLB | 70 ms | 34 ms | 95 ms | 0.1 ms | 0.4 | 4 ms | 43 ms | 0.2 | 0.9 |
| 18c Finish before the solder mask | simulation, GLB + STEP | 71 ms | 34 ms | 0.1 | 0.1 ms | 0.3 | 0.3 | 34 ms | 0.2 | 1.1 |
| 18c Finish before the solder mask | visual, GLB | 77 ms | 35 ms | 0.2 | 0.1 ms | 0.6 | 5 ms | 37 ms | 0.2 | 1.1 |
| 19 Items KESE skips | simulation, GLB + STEP | 70 ms | 17 ms | 21 ms | 0.1 ms | 44 ms | 45 ms | 8 ms | 0.2 | 0.4 |
| 19 Items KESE skips | visual, GLB | 58 ms | 13 ms | 21 ms | 0.1 ms | 0.1 | 2 ms | 21 ms | 0.2 | 0.4 |
| 19b Items KESE skips, KiCad 10 | simulation, GLB + STEP | 0.7 ms | 5 ms | 11 ms | 0.0 ms | 16 ms | 7 ms | 2 ms | 0.2 | 0.2 |
| 19b Items KESE skips, KiCad 10 | visual, GLB | 0.7 ms | 4 ms | 11 ms | 0.0 ms | 31 ms | 1 ms | 11 ms | 0.2 | 0.2 |
| 20a KiCad 6 format | simulation, GLB + STEP | 68 ms | 27 ms | 59 ms | 0.1 ms | 0.1 | 0.1 | 16 ms | 0.2 | 0.6 |
| 20a KiCad 6 format | visual, GLB | 68 ms | 31 ms | 63 ms | 0.1 ms | 0.3 | 4 ms | 31 ms | 0.2 | 0.7 |
| 20b KiCad 7 format | simulation, GLB + STEP | 65 ms | 26 ms | 63 ms | 0.1 ms | 0.2 | 0.1 | 16 ms | 0.2 | 0.7 |
| 20b KiCad 7 format | visual, GLB | 66 ms | 28 ms | 56 ms | 0.1 ms | 0.3 | 4 ms | 34 ms | 0.2 | 0.6 |
| 20c KiCad 8 format | simulation, GLB + STEP | 71 ms | 28 ms | 59 ms | 0.1 ms | 0.1 | 0.1 | 19 ms | 0.2 | 0.6 |
| 20c KiCad 8 format | visual, GLB | 66 ms | 28 ms | 53 ms | 0.1 ms | 0.3 | 4 ms | 35 ms | 0.2 | 0.7 |
| 20d KiCad 9 format | simulation, GLB + STEP | 71 ms | 27 ms | 59 ms | 0.1 ms | 0.2 | 0.2 | 20 ms | 0.2 | 0.7 |
| 20d KiCad 9 format | visual, GLB | 69 ms | 31 ms | 59 ms | 0.1 ms | 0.3 | 4 ms | 34 ms | 0.2 | 0.7 |
| 20e KiCad 10 format | simulation, GLB + STEP | 70 ms | 30 ms | 60 ms | 0.1 ms | 0.2 | 0.2 | 18 ms | 0.2 | 0.7 |
| 20e KiCad 10 format | visual, GLB | 68 ms | 32 ms | 62 ms | 0.1 ms | 0.3 | 4 ms | 31 ms | 0.2 | 0.7 |
| 21 RF sensor module | simulation, GLB + STEP | 0.2 | 1.4 | 6.3 | 0.4 ms | 5.5 | 3.3 | 0.5 | 0.2 | 17.4 |
| 21 RF sensor module | visual, GLB | 0.2 | 1.5 | 6.2 | 0.4 ms | 9.8 | 96 ms | 1.0 | 0.2 | 19.1 |
| 22 HDI radio module | simulation, GLB + STEP | 0.2 | 0.9 | 2.2 | 0.4 ms | 1.8 | 1.6 | 0.4 | 0.2 | 7.5 |
| 22 HDI radio module | visual, GLB | 0.2 | 1.0 | 2.2 | 0.4 ms | 5.8 | 39 ms | 0.3 | 0.2 | 9.7 |
| 23 PCIe x1 card | simulation, GLB + STEP | 0.2 | 1.1 | 3.4 | 0.5 ms | 3.5 | 2.9 | 0.6 | 0.2 | 12.0 |
| 23 PCIe x1 card | visual, GLB | 0.3 | 1.1 | 3.4 | 0.5 ms | 9.9 | 88 ms | 1.0 | 0.2 | 15.9 |

| Previous | Next |
|:---|---:|
| [openEMS Workflow](OpenEMS-Workflow.md) | [Glossary](Glossary.md) |
