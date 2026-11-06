# 23. Feature Test Collection

Every feature test board of `featureTest/` ([its
README](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/main/featureTest/README.md)
says what each one holds), section by section, with its top and bottom and where the time of a run
goes. Each board was exported three times in each mode, with the Verifier, the solder mask and the
silkscreen on, as the regression suite (`Generator/tests/test_boards.py`) runs them, and each bar is
the median of the three runs for that stage, from the stage timers of the `timing` block of
[`report.txt`](Project-Output-Organization.md#2022-reporttxt):

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

All the feature boards but 16b take 1.2 to 3.6 s a run, and on most of them more than half of the
run is the same fixed part: reading the file and the stroke font, and Python starting and exiting.
Board 16b, a plated border and 91 vias on four layers, takes 7.8 to 8.4 s, and the example boards 9
to 21 s.

## 23.2 Holes And Vias

### 23.2.1 01 Slotted Holes

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/01_holes_slotted/top_straight_visual.webp" width="49%" alt="01 Slotted holes straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/01_holes_slotted/bottom_straight_visual.webp" width="49%" alt="01 Slotted holes straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![01 Slotted holes: stacked bars of seconds per stage; reading, start-up and exit take 58% to 59% of a run. Simulation with GLB and STEP takes 2.4 s: read 0.4, resolve 50 ms, geometry 0.2, materials 0.1 ms, assemble 0.3, write 0.4, verify 35 ms, start-up and exit 1.0. Visual with GLB takes 2.5 s: read 0.4, resolve 48 ms, geometry 0.2, materials 0.1 ms, assemble 0.8, write 5 ms, verify 39 ms, start-up and exit 1.0](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_01_holes_slotted.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 50 ms | 0.2 | 0.1 ms | 0.3 | 0.4 | 35 ms | 1.0 | 2.4 |
| Visual, GLB | 0.4 | 48 ms | 0.2 | 0.1 ms | 0.8 | 5 ms | 39 ms | 1.0 | 2.5 |

| Board | `featureTest/01_holes_slotted.kicad_pcb` |
|---|---|
| Outline | 40 × 26 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.2.2 02 Round Holes

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/02_holes_round/top_straight_visual.webp" width="49%" alt="02 Round holes straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/02_holes_round/bottom_straight_visual.webp" width="49%" alt="02 Round holes straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![02 Round holes: stacked bars of seconds per stage; reading, start-up and exit take 58% to 62% of a run. Simulation with GLB and STEP takes 2.3 s: read 0.4, resolve 43 ms, geometry 0.2, materials 0.1 ms, assemble 0.3, write 0.3, verify 32 ms, start-up and exit 1.0. Visual with GLB takes 2.3 s: read 0.4, resolve 47 ms, geometry 0.1, materials 0.1 ms, assemble 0.7, write 6 ms, verify 46 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_02_holes_round.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 43 ms | 0.2 | 0.1 ms | 0.3 | 0.3 | 32 ms | 1.0 | 2.3 |
| Visual, GLB | 0.4 | 47 ms | 0.1 | 0.1 ms | 0.7 | 6 ms | 46 ms | 0.9 | 2.3 |

| Board | `featureTest/02_holes_round.kicad_pcb` |
|---|---|
| Outline | 34 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.2.3 03 Through Vias

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/03_vias_through/top_straight_visual.webp" width="49%" alt="03 Through vias straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/03_vias_through/bottom_straight_visual.webp" width="49%" alt="03 Through vias straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![03 Through vias: stacked bars of seconds per stage; reading, start-up and exit take 54% of a run. Simulation with GLB and STEP takes 2.5 s: read 0.4, resolve 49 ms, geometry 0.2, materials 0.2 ms, assemble 0.5, write 0.3, verify 40 ms, start-up and exit 0.9. Visual with GLB takes 2.5 s: read 0.4, resolve 44 ms, geometry 0.2, materials 0.1 ms, assemble 0.8, write 5 ms, verify 53 ms, start-up and exit 1.0](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_03_vias_through.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 49 ms | 0.2 | 0.2 ms | 0.5 | 0.3 | 40 ms | 0.9 | 2.5 |
| Visual, GLB | 0.4 | 44 ms | 0.2 | 0.1 ms | 0.8 | 5 ms | 53 ms | 1.0 | 2.5 |

| Board | `featureTest/03_vias_through.kicad_pcb` |
|---|---|
| Outline | 32 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 12 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.2.4 03b KiCad 10 Via Options

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/03b_vias_k10/top_straight_visual.webp" width="49%" alt="03b KiCad 10 via options straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/03b_vias_k10/bottom_straight_visual.webp" width="49%" alt="03b KiCad 10 via options straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![03b KiCad 10 via options: stacked bars of seconds per stage; reading, start-up and exit take 44% to 46% of a run. Simulation with GLB and STEP takes 2.7 s: read 0.4, resolve 0.1, geometry 0.2, materials 0.2 ms, assemble 0.5, write 0.7, verify 56 ms, start-up and exit 0.8. Visual with GLB takes 3.0 s: read 0.4, resolve 0.1, geometry 0.2, materials 0.2 ms, assemble 1.3, write 8 ms, verify 77 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_03b_vias_k10.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 0.1 | 0.2 | 0.2 ms | 0.5 | 0.7 | 56 ms | 0.8 | 2.7 |
| Visual, GLB | 0.4 | 0.1 | 0.2 | 0.2 ms | 1.3 | 8 ms | 77 ms | 0.9 | 3.0 |

| Board | `featureTest/03b_vias_k10.kicad_pcb` |
|---|---|
| Outline | 40 × 30 mm |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 18: 1 micro, 2 blind and buried, 15 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.2.5 04 Blind And Buried Vias

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/04_vias_blind_buried/top_straight_visual.webp" width="49%" alt="04 Blind and buried vias straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/04_vias_blind_buried/bottom_straight_visual.webp" width="49%" alt="04 Blind and buried vias straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![04 Blind and buried vias: stacked bars of seconds per stage; reading, start-up and exit take 73% to 75% of a run. Simulation with GLB and STEP takes 2.0 s: read 0.5, resolve 55 ms, geometry 57 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 19 ms, start-up and exit 1.0. Visual with GLB takes 1.9 s: read 0.4, resolve 48 ms, geometry 57 ms, materials 0.1 ms, assemble 0.4, write 3 ms, verify 32 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_04_vias_blind_buried.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.5 | 55 ms | 57 ms | 0.1 ms | 0.2 | 0.1 | 19 ms | 1.0 | 2.0 |
| Visual, GLB | 0.4 | 48 ms | 57 ms | 0.1 ms | 0.4 | 3 ms | 32 ms | 0.9 | 1.9 |

| Board | `featureTest/04_vias_blind_buried.kicad_pcb` |
|---|---|
| Outline | 32 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 6 |
| Vias | 6: 3 blind and buried, 3 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.2.6 05 Microvias

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/05_vias_micro/top_straight_visual.webp" width="49%" alt="05 Microvias straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/05_vias_micro/bottom_straight_visual.webp" width="49%" alt="05 Microvias straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![05 Microvias: stacked bars of seconds per stage; reading, start-up and exit take 77% of a run. Simulation with GLB and STEP takes 1.9 s: read 0.4, resolve 52 ms, geometry 51 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 18 ms, start-up and exit 1.1. Visual with GLB takes 1.9 s: read 0.5, resolve 56 ms, geometry 51 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 49 ms, start-up and exit 1.0](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_05_vias_micro.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 52 ms | 51 ms | 0.1 ms | 0.2 | 0.1 | 18 ms | 1.1 | 1.9 |
| Visual, GLB | 0.5 | 56 ms | 51 ms | 0.1 ms | 0.3 | 3 ms | 49 ms | 1.0 | 1.9 |

| Board | `featureTest/05_vias_micro.kicad_pcb` |
|---|---|
| Outline | 30 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 8 |
| Vias | 12: 10 micro, 2 blind and buried |
| Board edge | Plain |
| Mask, silkscreen, finish | Mask colour not set (drawn green), no silkscreen, ENIG |

## 23.3 Pads

### 23.3.1 06 Padstacks

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/06_padstacks/top_straight_visual.webp" width="49%" alt="06 Padstacks straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/06_padstacks/bottom_straight_visual.webp" width="49%" alt="06 Padstacks straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![06 Padstacks: stacked bars of seconds per stage; reading, start-up and exit take 63% to 68% of a run. Simulation with GLB and STEP takes 2.1 s: read 0.4, resolve 44 ms, geometry 82 ms, materials 0.1 ms, assemble 0.3, write 0.2, verify 29 ms, start-up and exit 1.0. Visual with GLB takes 2.3 s: read 0.4, resolve 44 ms, geometry 87 ms, materials 0.1 ms, assemble 0.7, write 4 ms, verify 34 ms, start-up and exit 1.0](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_06_padstacks.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 44 ms | 82 ms | 0.1 ms | 0.3 | 0.2 | 29 ms | 1.0 | 2.1 |
| Visual, GLB | 0.4 | 44 ms | 87 ms | 0.1 ms | 0.7 | 4 ms | 34 ms | 1.0 | 2.3 |

| Board | `featureTest/06_padstacks.kicad_pcb` |
|---|---|
| Outline | 34 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 3 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.3.2 07 Pad Shapes

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/07_pad_shapes/top_straight_visual.webp" width="49%" alt="07 Pad shapes straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/07_pad_shapes/bottom_straight_visual.webp" width="49%" alt="07 Pad shapes straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![07 Pad shapes: stacked bars of seconds per stage; reading, start-up and exit take 57% of a run. Simulation with GLB and STEP takes 2.1 s: read 0.4, resolve 35 ms, geometry 0.1, materials 0.1 ms, assemble 0.3, write 0.5, verify 22 ms, start-up and exit 0.8. Visual with GLB takes 2.3 s: read 0.4, resolve 39 ms, geometry 0.1, materials 0.1 ms, assemble 0.8, write 6 ms, verify 42 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_07_pad_shapes.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 35 ms | 0.1 | 0.1 ms | 0.3 | 0.5 | 22 ms | 0.8 | 2.1 |
| Visual, GLB | 0.4 | 39 ms | 0.1 | 0.1 ms | 0.8 | 6 ms | 42 ms | 0.9 | 2.3 |

| Board | `featureTest/07_pad_shapes.kicad_pcb` |
|---|---|
| Outline | 44 × 30 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

## 23.4 Copper Drawings, Text And Tracks

### 23.4.1 08 Copper Graphics

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/08_copper_graphics/top_straight_visual.webp" width="49%" alt="08 Copper graphics straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/08_copper_graphics/bottom_straight_visual.webp" width="49%" alt="08 Copper graphics straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![08 Copper graphics: stacked bars of seconds per stage; reading, start-up and exit take 66% to 70% of a run. Simulation with GLB and STEP takes 2.1 s: read 0.4, resolve 22 ms, geometry 34 ms, materials 0.1 ms, assemble 0.2, write 0.4, verify 15 ms, start-up and exit 1.0. Visual with GLB takes 2.0 s: read 0.4, resolve 22 ms, geometry 36 ms, materials 0.1 ms, assemble 0.5, write 4 ms, verify 54 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_08_copper_graphics.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 22 ms | 34 ms | 0.1 ms | 0.2 | 0.4 | 15 ms | 1.0 | 2.1 |
| Visual, GLB | 0.4 | 22 ms | 36 ms | 0.1 ms | 0.5 | 4 ms | 54 ms | 0.9 | 2.0 |

| Board | `featureTest/08_copper_graphics.kicad_pcb` |
|---|---|
| Outline | 30 × 24 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.4.2 08b Copper Graphics On Nets

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/08b_copper_graphics_nets/top_straight_visual.webp" width="49%" alt="08b Copper graphics on nets straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/08b_copper_graphics_nets/bottom_straight_visual.webp" width="49%" alt="08b Copper graphics on nets straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![08b Copper graphics on nets: stacked bars of seconds per stage; reading, start-up and exit take 77% of a run. Simulation with GLB and STEP takes 1.9 s: read 0.5, resolve 24 ms, geometry 47 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 17 ms, start-up and exit 1.0. Visual with GLB takes 1.8 s: read 0.4, resolve 23 ms, geometry 43 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 40 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_08b_copper_graphics_nets.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.5 | 24 ms | 47 ms | 0.1 ms | 0.2 | 0.2 | 17 ms | 1.0 | 1.9 |
| Visual, GLB | 0.4 | 23 ms | 43 ms | 0.1 ms | 0.3 | 4 ms | 40 ms | 0.9 | 1.8 |

| Board | `featureTest/08b_copper_graphics_nets.kicad_pcb` |
|---|---|
| Outline | 36 × 24 mm, rounded corners |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.4.3 09 Copper Text

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/09_copper_text/top_straight_visual.webp" width="49%" alt="09 Copper text straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/09_copper_text/bottom_straight_visual.webp" width="49%" alt="09 Copper text straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![09 Copper text: stacked bars of seconds per stage; reading, start-up and exit take 37% to 49% of a run. Simulation with GLB and STEP takes 3.6 s: read 0.5, resolve 33 ms, geometry 0.1, materials 0.1 ms, assemble 1.0, write 1.0, verify 43 ms, start-up and exit 0.8. Visual with GLB takes 2.5 s: read 0.4, resolve 40 ms, geometry 0.1, materials 0.1 ms, assemble 1.1, write 13 ms, verify 78 ms, start-up and exit 0.8](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_09_copper_text.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.5 | 33 ms | 0.1 | 0.1 ms | 1.0 | 1.0 | 43 ms | 0.8 | 3.6 |
| Visual, GLB | 0.4 | 40 ms | 0.1 | 0.1 ms | 1.1 | 13 ms | 78 ms | 0.8 | 2.5 |

| Board | `featureTest/09_copper_text.kicad_pcb` |
|---|---|
| Outline | 44 × 40 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.4.4 10 Tracks And Arcs

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/10_tracks_arcs/top_straight_visual.webp" width="49%" alt="10 Tracks and arcs straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/10_tracks_arcs/bottom_straight_visual.webp" width="49%" alt="10 Tracks and arcs straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![10 Tracks and arcs: stacked bars of seconds per stage; reading, start-up and exit take 75% to 76% of a run. Simulation with GLB and STEP takes 1.8 s: read 0.4, resolve 21 ms, geometry 37 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 14 ms, start-up and exit 1.0. Visual with GLB takes 1.8 s: read 0.4, resolve 22 ms, geometry 34 ms, materials 0.1 ms, assemble 0.4, write 4 ms, verify 35 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_10_tracks_arcs.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 21 ms | 37 ms | 0.1 ms | 0.2 | 0.2 | 14 ms | 1.0 | 1.8 |
| Visual, GLB | 0.4 | 22 ms | 34 ms | 0.1 ms | 0.4 | 4 ms | 35 ms | 0.9 | 1.8 |

| Board | `featureTest/10_tracks_arcs.kicad_pcb` |
|---|---|
| Outline | 44 × 24 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

## 23.5 Zones

### 23.5.1 11 Zones

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/11_zones/top_straight_visual.webp" width="49%" alt="11 Zones straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/11_zones/bottom_straight_visual.webp" width="49%" alt="11 Zones straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![11 Zones: stacked bars of seconds per stage; stages 4 and 6 take 27% to 53% of a run. Simulation with GLB and STEP takes 3.2 s: read 0.5, resolve 99 ms, geometry 0.3, materials 0.1 ms, assemble 0.6, write 0.8, verify 78 ms, start-up and exit 0.8. Visual with GLB takes 3.2 s: read 0.4, resolve 98 ms, geometry 0.3, materials 0.1 ms, assemble 1.4, write 9 ms, verify 57 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_11_zones.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.5 | 99 ms | 0.3 | 0.1 ms | 0.6 | 0.8 | 78 ms | 0.8 | 3.2 |
| Visual, GLB | 0.4 | 98 ms | 0.3 | 0.1 ms | 1.4 | 9 ms | 57 ms | 0.9 | 3.2 |

| Board | `featureTest/11_zones.kicad_pcb` |
|---|---|
| Outline | 40 × 31 mm |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

## 23.6 Board Outline

### 23.6.1 12 Board Outline Shapes

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/12_outline_shapes/top_straight_visual.webp" width="49%" alt="12 Board outline shapes straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/12_outline_shapes/bottom_straight_visual.webp" width="49%" alt="12 Board outline shapes straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![12 Board outline shapes: stacked bars of seconds per stage; reading, start-up and exit take 49% to 63% of a run. Simulation with GLB and STEP takes 2.9 s: read 0.4, resolve 36 ms, geometry 69 ms, materials 0.1 ms, assemble 0.6, write 0.8, verify 23 ms, start-up and exit 1.0. Visual with GLB takes 2.3 s: read 0.4, resolve 38 ms, geometry 73 ms, materials 0.1 ms, assemble 0.7, write 7 ms, verify 57 ms, start-up and exit 1.0](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_12_outline_shapes.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 36 ms | 69 ms | 0.1 ms | 0.6 | 0.8 | 23 ms | 1.0 | 2.9 |
| Visual, GLB | 0.4 | 38 ms | 73 ms | 0.1 ms | 0.7 | 7 ms | 57 ms | 1.0 | 2.3 |

| Board | `featureTest/12_outline_shapes.kicad_pcb` |
|---|---|
| Outline | 40 × 30.9 mm, arcs, a Bezier edge, a notch and cut-outs |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.6.2 13a No Board Outline

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/13a_outline_none/top_straight_visual.webp" width="49%" alt="13a No board outline straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/13a_outline_none/bottom_straight_visual.webp" width="49%" alt="13a No board outline straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![13a No board outline: stacked bars of seconds per stage; reading, start-up and exit take 80% to 81% of a run. Simulation with GLB and STEP takes 1.6 s: read 0.4, resolve 23 ms, geometry 44 ms, materials 0.1 ms, assemble 0.1, write 0.1, verify 15 ms, start-up and exit 0.8. Visual with GLB takes 1.7 s: read 0.4, resolve 23 ms, geometry 47 ms, materials 0.1 ms, assemble 0.2, write 3 ms, verify 59 ms, start-up and exit 1.0](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_13a_outline_none.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 23 ms | 44 ms | 0.1 ms | 0.1 | 0.1 | 15 ms | 0.8 | 1.6 |
| Visual, GLB | 0.4 | 23 ms | 47 ms | 0.1 ms | 0.2 | 3 ms | 59 ms | 1.0 | 1.7 |

| Board | `featureTest/13a_outline_none.kicad_pcb` |
|---|---|
| Outline | 13.7 × 7.2 mm, from the copper (no Edge.Cuts) |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Mask colour not set (drawn green), no silkscreen, ENIG |

### 23.6.3 13b Two Board Outlines

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/13b_outline_two/top_straight_visual.webp" width="49%" alt="13b Two board outlines straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/13b_outline_two/bottom_straight_visual.webp" width="49%" alt="13b Two board outlines straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![13b Two board outlines: stacked bars of seconds per stage; reading, start-up and exit take 84% of a run. Simulation with GLB and STEP takes 1.6 s: read 0.4, resolve 19 ms, geometry 38 ms, materials 0.1 ms, assemble 99 ms, write 92 ms, verify 13 ms, start-up and exit 1.0. Visual with GLB takes 1.8 s: read 0.4, resolve 20 ms, geometry 40 ms, materials 0.1 ms, assemble 0.2, write 2 ms, verify 22 ms, start-up and exit 1.1](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_13b_outline_two.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 19 ms | 38 ms | 0.1 ms | 99 ms | 92 ms | 13 ms | 1.0 | 1.6 |
| Visual, GLB | 0.4 | 20 ms | 40 ms | 0.1 ms | 0.2 | 2 ms | 22 ms | 1.1 | 1.8 |

| Board | `featureTest/13b_outline_two.kicad_pcb` |
|---|---|
| Outline | 40 × 20 mm, two boards and a third in a hole |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

## 23.7 Stack-Up

### 23.7.1 14 Full Stack-Up

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/14_stackup_full/top_straight_visual.webp" width="49%" alt="14 Full stack-up straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/14_stackup_full/bottom_straight_visual.webp" width="49%" alt="14 Full stack-up straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![14 Full stack-up: stacked bars of seconds per stage; reading, start-up and exit take 78% to 80% of a run. Simulation with GLB and STEP takes 1.8 s: read 0.4, resolve 30 ms, geometry 54 ms, materials 0.1 ms, assemble 0.1, write 0.1, verify 13 ms, start-up and exit 1.0. Visual with GLB takes 1.8 s: read 0.4, resolve 35 ms, geometry 61 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 32 ms, start-up and exit 1.0](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_14_stackup_full.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 30 ms | 54 ms | 0.1 ms | 0.1 | 0.1 | 13 ms | 1.0 | 1.8 |
| Visual, GLB | 0.4 | 35 ms | 61 ms | 0.1 ms | 0.3 | 3 ms | 32 ms | 1.0 | 1.8 |

| Board | `featureTest/14_stackup_full.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.58 mm |
| Copper layers | 4 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Green, white, ENIG |

### 23.7.2 15 No Stack-Up

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/15_stackup_none/top_straight_visual.webp" width="49%" alt="15 No stack-up straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/15_stackup_none/bottom_straight_visual.webp" width="49%" alt="15 No stack-up straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![15 No stack-up: stacked bars of seconds per stage; reading, start-up and exit take 78% to 81% of a run. Simulation with GLB and STEP takes 1.9 s: read 0.4, resolve 30 ms, geometry 53 ms, materials 0.1 ms, assemble 0.1, write 0.1, verify 15 ms, start-up and exit 1.1. Visual with GLB takes 1.7 s: read 0.5, resolve 26 ms, geometry 48 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 29 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_15_stackup_none.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 30 ms | 53 ms | 0.1 ms | 0.1 | 0.1 | 15 ms | 1.1 | 1.9 |
| Visual, GLB | 0.5 | 26 ms | 48 ms | 0.1 ms | 0.3 | 3 ms | 29 ms | 0.9 | 1.7 |

| Board | `featureTest/15_stackup_none.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.2 mm |
| Copper layers | 4 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

## 23.8 Edge Plating

### 23.8.1 16 Castellated Pads And A Plated Edge

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/16_edge_plating_castellation/top_straight_visual.webp" width="49%" alt="16 Castellated pads and a plated edge straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/16_edge_plating_castellation/bottom_straight_visual.webp" width="49%" alt="16 Castellated pads and a plated edge straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![16 Castellated pads and a plated edge: stacked bars of seconds per stage; reading, start-up and exit take 72% to 74% of a run. Simulation with GLB and STEP takes 1.9 s: read 0.4, resolve 66 ms, geometry 87 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 23 ms, start-up and exit 1.0. Visual with GLB takes 1.9 s: read 0.4, resolve 73 ms, geometry 97 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 39 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_16_edge_plating_castellation.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 66 ms | 87 ms | 0.1 ms | 0.2 | 0.1 | 23 ms | 1.0 | 1.9 |
| Visual, GLB | 0.4 | 73 ms | 97 ms | 0.1 ms | 0.3 | 3 ms | 39 ms | 0.9 | 1.9 |

| Board | `featureTest/16_edge_plating_castellation.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Castellated pads on the right edge, plated edge |
| Mask, silkscreen, finish | Not set (drawn green and white), immersion silver |

### 23.8.2 16b Plated Board Edge With A GND Border

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/16b_edge_plating_border/top_straight_visual.webp" width="49%" alt="16b Plated board edge with a GND border straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/16b_edge_plating_border/bottom_straight_visual.webp" width="49%" alt="16b Plated board edge with a GND border straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![16b Plated board edge with a GND border: stacked bars of seconds per stage; stages 4 and 6 take 53% to 77% of a run. Simulation with GLB and STEP takes 7.8 s: read 0.5, resolve 0.4, geometry 2.0, materials 0.2 ms, assemble 2.1, write 1.5, verify 0.5, start-up and exit 0.9. Visual with GLB takes 8.4 s: read 0.5, resolve 0.4, geometry 2.0, materials 0.2 ms, assemble 4.5, write 20 ms, verify 0.1, start-up and exit 0.8](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_16b_edge_plating_border.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.5 | 0.4 | 2.0 | 0.2 ms | 2.1 | 1.5 | 0.5 | 0.9 | 7.8 |
| Visual, GLB | 0.5 | 0.4 | 2.0 | 0.2 ms | 4.5 | 20 ms | 0.1 | 0.8 | 8.4 |

| Board | `featureTest/16b_edge_plating_border.kicad_pcb` |
|---|---|
| Outline | 40 × 28 mm, a cut-out |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 91 through |
| Board edge | Plated all round and in the cut-out |
| Mask, silkscreen, finish | Green, white, ENIG |

## 23.9 Solder Mask And Silkscreen

### 23.9.1 17 Solder Mask And Silkscreen

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/17_mask_silk/top_straight_visual.webp" width="49%" alt="17 Solder mask and silkscreen straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/17_mask_silk/bottom_straight_visual.webp" width="49%" alt="17 Solder mask and silkscreen straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![17 Solder mask and silkscreen: stacked bars of seconds per stage; reading, start-up and exit take 66% to 73% of a run. Simulation with GLB and STEP takes 1.9 s: read 0.4, resolve 61 ms, geometry 94 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 15 ms, start-up and exit 0.9. Visual with GLB takes 2.1 s: read 0.4, resolve 57 ms, geometry 94 ms, materials 0.1 ms, assemble 0.5, write 4 ms, verify 48 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_17_mask_silk.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 61 ms | 94 ms | 0.1 ms | 0.2 | 0.2 | 15 ms | 0.9 | 1.9 |
| Visual, GLB | 0.4 | 57 ms | 94 ms | 0.1 ms | 0.5 | 4 ms | 48 ms | 0.9 | 2.1 |

| Board | `featureTest/17_mask_silk.kicad_pcb` |
|---|---|
| Outline | 40 × 30 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Red, black, lead-free HASL |

### 23.9.2 17b Silkscreen Over Copper

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/17b_silk_over_copper/top_straight_visual.webp" width="49%" alt="17b Silkscreen over copper straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/17b_silk_over_copper/bottom_straight_visual.webp" width="49%" alt="17b Silkscreen over copper straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![17b Silkscreen over copper: stacked bars of seconds per stage; reading, start-up and exit take 57% to 69% of a run. Simulation with GLB and STEP takes 1.9 s: read 0.4, resolve 30 ms, geometry 0.1, materials 0.1 ms, assemble 0.2, write 0.2, verify 20 ms, start-up and exit 0.9. Visual with GLB takes 2.1 s: read 0.4, resolve 29 ms, geometry 0.2, materials 0.1 ms, assemble 0.7, write 4 ms, verify 37 ms, start-up and exit 0.8](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_17b_silk_over_copper.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 30 ms | 0.1 | 0.1 ms | 0.2 | 0.2 | 20 ms | 0.9 | 1.9 |
| Visual, GLB | 0.4 | 29 ms | 0.2 | 0.1 ms | 0.7 | 4 ms | 37 ms | 0.8 | 2.1 |

| Board | `featureTest/17b_silk_over_copper.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | White, black, ENIG |

## 23.10 Surface Finish

### 23.10.1 18 Gold Edge Fingers

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18_finishes/top_straight_visual.webp" width="49%" alt="18 Gold edge fingers straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18_finishes/bottom_straight_visual.webp" width="49%" alt="18 Gold edge fingers straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![18 Gold edge fingers: stacked bars of seconds per stage; reading, start-up and exit take 74% to 77% of a run. Simulation with GLB and STEP takes 1.6 s: read 0.4, resolve 30 ms, geometry 41 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 15 ms, start-up and exit 0.8. Visual with GLB takes 1.8 s: read 0.4, resolve 30 ms, geometry 38 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 43 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_18_finishes.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 30 ms | 41 ms | 0.1 ms | 0.2 | 0.1 | 15 ms | 0.8 | 1.6 |
| Visual, GLB | 0.4 | 30 ms | 38 ms | 0.1 ms | 0.3 | 4 ms | 43 ms | 0.9 | 1.8 |

| Board | `featureTest/18_finishes.kicad_pcb` |
|---|---|
| Outline | 30 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 6 through |
| Board edge | Gold edge fingers on a bevelled edge |
| Mask, silkscreen, finish | Not set (drawn green and white), hard gold |

### 23.10.2 18b Finish On Every Kind Of Bare Copper

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18b_finish_pads/top_straight_visual.webp" width="49%" alt="18b Finish on every kind of bare copper straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18b_finish_pads/bottom_straight_visual.webp" width="49%" alt="18b Finish on every kind of bare copper straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![18b Finish on every kind of bare copper: stacked bars of seconds per stage; reading, start-up and exit take 68% to 73% of a run. Simulation with GLB and STEP takes 1.8 s: read 0.4, resolve 32 ms, geometry 86 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 22 ms, start-up and exit 0.9. Visual with GLB takes 1.8 s: read 0.4, resolve 32 ms, geometry 0.1, materials 0.1 ms, assemble 0.4, write 4 ms, verify 32 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_18b_finish_pads.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 32 ms | 86 ms | 0.1 ms | 0.2 | 0.2 | 22 ms | 0.9 | 1.8 |
| Visual, GLB | 0.4 | 32 ms | 0.1 | 0.1 ms | 0.4 | 4 ms | 32 ms | 0.9 | 1.8 |

| Board | `featureTest/18b_finish_pads.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Green, white, ENIG |

### 23.10.3 18c Finish Before The Solder Mask

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18c_finish_before_mask/top_straight_visual.webp" width="49%" alt="18c Finish before the solder mask straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/18c_finish_before_mask/bottom_straight_visual.webp" width="49%" alt="18c Finish before the solder mask straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![18c Finish before the solder mask: stacked bars of seconds per stage; reading, start-up and exit take 57% of a run. Simulation with GLB and STEP takes 2.2 s: read 0.4, resolve 34 ms, geometry 0.1, materials 0.1 ms, assemble 0.4, write 0.3, verify 31 ms, start-up and exit 0.8. Visual with GLB takes 2.3 s: read 0.4, resolve 31 ms, geometry 0.1, materials 0.1 ms, assemble 0.8, write 4 ms, verify 42 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_18c_finish_before_mask.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 34 ms | 0.1 | 0.1 ms | 0.4 | 0.3 | 31 ms | 0.8 | 2.2 |
| Visual, GLB | 0.4 | 31 ms | 0.1 | 0.1 ms | 0.8 | 4 ms | 42 ms | 0.9 | 2.3 |

| Board | `featureTest/18c_finish_before_mask.kicad_pcb` |
|---|---|
| Outline | 30 × 20 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Blue, white, ENEPIG |

## 23.11 Items KESE Skips

### 23.11.1 19 Items KESE Skips

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/19_skipped_items/top_straight_visual.webp" width="49%" alt="19 Items KESE skips straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/19_skipped_items/bottom_straight_visual.webp" width="49%" alt="19 Items KESE skips straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![19 Items KESE skips: stacked bars of seconds per stage; reading, start-up and exit take 89% to 91% of a run. Simulation with GLB and STEP takes 1.4 s: read 0.4, resolve 19 ms, geometry 21 ms, materials 0.1 ms, assemble 43 ms, write 43 ms, verify 6 ms, start-up and exit 0.9. Visual with GLB takes 1.5 s: read 0.4, resolve 16 ms, geometry 22 ms, materials 0.1 ms, assemble 0.1, write 2 ms, verify 19 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_19_skipped_items.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 19 ms | 21 ms | 0.1 ms | 43 ms | 43 ms | 6 ms | 0.9 | 1.4 |
| Visual, GLB | 0.4 | 16 ms | 22 ms | 0.1 ms | 0.1 | 2 ms | 19 ms | 0.9 | 1.5 |

| Board | `featureTest/19_skipped_items.kicad_pcb` |
|---|---|
| Outline | 40 × 30 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.11.2 19b Items KESE Skips, KiCad 10

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/19b_skipped_items_k10/top_straight_visual.webp" width="49%" alt="19b Items KESE skips, KiCad 10 straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/19b_skipped_items_k10/bottom_straight_visual.webp" width="49%" alt="19b Items KESE skips, KiCad 10 straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![19b Items KESE skips, KiCad 10: stacked bars of seconds per stage; reading, start-up and exit take 96% to 98% of a run. Simulation with GLB and STEP takes 1.3 s: read 0.5, resolve 3 ms, geometry 3 ms, materials 0.0 ms, assemble 15 ms, write 8 ms, verify 1 ms, start-up and exit 0.8. Visual with GLB takes 1.2 s: read 0.4, resolve 3 ms, geometry 3 ms, materials 0.0 ms, assemble 25 ms, write 1.0 ms, verify 11 ms, start-up and exit 0.7](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_19b_skipped_items_k10.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.5 | 3 ms | 3 ms | 0.0 ms | 15 ms | 8 ms | 1 ms | 0.8 | 1.3 |
| Visual, GLB | 0.4 | 3 ms | 3 ms | 0.0 ms | 25 ms | 1.0 ms | 11 ms | 0.7 | 1.2 |

| Board | `featureTest/19b_skipped_items_k10.kicad_pcb` |
|---|---|
| Outline | 40 × 24 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | none |
| Board edge | Plain |
| Mask, silkscreen, finish | Mask colour not set (drawn green), no silkscreen, ENIG |

## 23.12 KiCad File Formats

### 23.12.1 20a KiCad 6 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20a_format_kicad6/top_straight_visual.webp" width="49%" alt="20a KiCad 6 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20a_format_kicad6/bottom_straight_visual.webp" width="49%" alt="20a KiCad 6 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20a KiCad 6 format: stacked bars of seconds per stage; reading, start-up and exit take 75% to 77% of a run. Simulation with GLB and STEP takes 1.7 s: read 0.4, resolve 27 ms, geometry 54 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 18 ms, start-up and exit 0.9. Visual with GLB takes 1.6 s: read 0.4, resolve 26 ms, geometry 55 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 28 ms, start-up and exit 0.8](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20a_format_kicad6.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 27 ms | 54 ms | 0.1 ms | 0.2 | 0.1 | 18 ms | 0.9 | 1.7 |
| Visual, GLB | 0.4 | 26 ms | 55 ms | 0.1 ms | 0.3 | 3 ms | 28 ms | 0.8 | 1.6 |

| Board | `featureTest/20a_format_kicad6.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.12.2 20b KiCad 7 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20b_format_kicad7/top_straight_visual.webp" width="49%" alt="20b KiCad 7 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20b_format_kicad7/bottom_straight_visual.webp" width="49%" alt="20b KiCad 7 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20b KiCad 7 format: stacked bars of seconds per stage; reading, start-up and exit take 74% to 76% of a run. Simulation with GLB and STEP takes 1.6 s: read 0.4, resolve 27 ms, geometry 61 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 18 ms, start-up and exit 0.8. Visual with GLB takes 1.6 s: read 0.4, resolve 27 ms, geometry 61 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 28 ms, start-up and exit 0.8](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20b_format_kicad7.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 27 ms | 61 ms | 0.1 ms | 0.2 | 0.1 | 18 ms | 0.8 | 1.6 |
| Visual, GLB | 0.4 | 27 ms | 61 ms | 0.1 ms | 0.3 | 3 ms | 28 ms | 0.8 | 1.6 |

| Board | `featureTest/20b_format_kicad7.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.12.3 20c KiCad 8 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20c_format_kicad8/top_straight_visual.webp" width="49%" alt="20c KiCad 8 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20c_format_kicad8/bottom_straight_visual.webp" width="49%" alt="20c KiCad 8 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20c KiCad 8 format: stacked bars of seconds per stage; reading, start-up and exit take 74% to 75% of a run. Simulation with GLB and STEP takes 1.5 s: read 0.4, resolve 29 ms, geometry 55 ms, materials 0.1 ms, assemble 0.1, write 0.1, verify 14 ms, start-up and exit 0.7. Visual with GLB takes 1.5 s: read 0.4, resolve 26 ms, geometry 68 ms, materials 0.1 ms, assemble 0.3, write 4 ms, verify 33 ms, start-up and exit 0.7](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20c_format_kicad8.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 29 ms | 55 ms | 0.1 ms | 0.1 | 0.1 | 14 ms | 0.7 | 1.5 |
| Visual, GLB | 0.4 | 26 ms | 68 ms | 0.1 ms | 0.3 | 4 ms | 33 ms | 0.7 | 1.5 |

| Board | `featureTest/20c_format_kicad8.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.12.4 20d KiCad 9 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20d_format_kicad9/top_straight_visual.webp" width="49%" alt="20d KiCad 9 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20d_format_kicad9/bottom_straight_visual.webp" width="49%" alt="20d KiCad 9 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20d KiCad 9 format: stacked bars of seconds per stage; reading, start-up and exit take 75% to 78% of a run. Simulation with GLB and STEP takes 1.6 s: read 0.4, resolve 27 ms, geometry 57 ms, materials 0.1 ms, assemble 0.2, write 0.2, verify 18 ms, start-up and exit 0.8. Visual with GLB takes 1.8 s: read 0.4, resolve 26 ms, geometry 58 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 30 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20d_format_kicad9.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 27 ms | 57 ms | 0.1 ms | 0.2 | 0.2 | 18 ms | 0.8 | 1.6 |
| Visual, GLB | 0.4 | 26 ms | 58 ms | 0.1 ms | 0.3 | 3 ms | 30 ms | 0.9 | 1.8 |

| Board | `featureTest/20d_format_kicad9.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

### 23.12.5 20e KiCad 10 Format

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20e_format_kicad10/top_straight_visual.webp" width="49%" alt="20e KiCad 10 format straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/20e_format_kicad10/bottom_straight_visual.webp" width="49%" alt="20e KiCad 10 format straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![20e KiCad 10 format: stacked bars of seconds per stage; reading, start-up and exit take 76% to 77% of a run. Simulation with GLB and STEP takes 1.8 s: read 0.4, resolve 28 ms, geometry 61 ms, materials 0.1 ms, assemble 0.2, write 0.1, verify 15 ms, start-up and exit 0.9. Visual with GLB takes 1.8 s: read 0.4, resolve 29 ms, geometry 68 ms, materials 0.1 ms, assemble 0.3, write 3 ms, verify 37 ms, start-up and exit 0.9](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_20e_format_kicad10.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.4 | 28 ms | 61 ms | 0.1 ms | 0.2 | 0.1 | 15 ms | 0.9 | 1.8 |
| Visual, GLB | 0.4 | 29 ms | 68 ms | 0.1 ms | 0.3 | 3 ms | 37 ms | 0.9 | 1.8 |

| Board | `featureTest/20e_format_kicad10.kicad_pcb` |
|---|---|
| Outline | 24 × 16 mm |
| Thickness | 1.6 mm |
| Copper layers | 2 |
| Vias | 1 through |
| Board edge | Plain |
| Mask, silkscreen, finish | Not set (drawn green and white), ENIG |

## 23.13 Example Boards

### 23.13.1 21 RF Sensor Module

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/21_rf_module/top_straight_visual.webp" width="49%" alt="21 RF sensor module straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/21_rf_module/bottom_straight_visual.webp" width="49%" alt="21 RF sensor module straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![21 RF sensor module: stacked bars of seconds per stage; stages 4 and 6 take 63% to 80% of a run. Simulation with GLB and STEP takes 19.4 s: read 0.8, resolve 1.6, geometry 6.5, materials 0.4 ms, assemble 5.7, write 3.3, verify 0.6, start-up and exit 1.0. Visual with GLB takes 20.5 s: read 0.8, resolve 1.5, geometry 6.4, materials 0.4 ms, assemble 10.0, write 93 ms, verify 0.7, start-up and exit 1.0](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_21_rf_module.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.8 | 1.6 | 6.5 | 0.4 ms | 5.7 | 3.3 | 0.6 | 1.0 | 19.4 |
| Visual, GLB | 0.8 | 1.5 | 6.4 | 0.4 ms | 10.0 | 93 ms | 0.7 | 1.0 | 20.5 |

| Board | `featureTest/21_rf_module.kicad_pcb` ([5.1](Examples.md#51-rf-sensor-module)) |
|---|---|
| Outline | 64 × 44 mm, a cut-out |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 307 through |
| Board edge | Plated all round and in the cut-out |
| Mask, silkscreen, finish | Blue, white, ENIG |

### 23.13.2 22 HDI Radio Module

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/22_hdi_module/top_straight_visual.webp" width="36%" alt="22 HDI radio module straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/22_hdi_module/bottom_straight_visual.webp" width="36%" alt="22 HDI radio module straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![22 HDI radio module: stacked bars of seconds per stage; stages 4 and 6 take 46% to 72% of a run. Simulation with GLB and STEP takes 9.1 s: read 0.8, resolve 1.0, geometry 2.3, materials 0.3 ms, assemble 1.9, write 1.6, verify 0.4, start-up and exit 1.1. Visual with GLB takes 11.1 s: read 0.8, resolve 1.0, geometry 2.3, materials 0.4 ms, assemble 5.7, write 44 ms, verify 0.3, start-up and exit 1.0](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_22_hdi_module.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.8 | 1.0 | 2.3 | 0.3 ms | 1.9 | 1.6 | 0.4 | 1.1 | 9.1 |
| Visual, GLB | 0.8 | 1.0 | 2.3 | 0.4 ms | 5.7 | 44 ms | 0.3 | 1.0 | 11.1 |

| Board | `featureTest/22_hdi_module.kicad_pcb` ([5.2](Examples.md#52-hdi-radio-module)) |
|---|---|
| Outline | 22 × 30 mm |
| Thickness | 0.925 mm |
| Copper layers | 6 |
| Vias | 150: 71 micro, 34 blind and buried, 45 through |
| Board edge | 43 castellated pads |
| Mask, silkscreen, finish | Black, white, immersion silver |

### 23.13.3 23 PCIe x1 Card

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/23_pcie_card/top_straight_visual.webp" width="49%" alt="23 PCIe x1 card straight from above in visual mode">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/feature_test_images/23_pcie_card/bottom_straight_visual.webp" width="49%" alt="23 PCIe x1 card straight from below in visual mode, mirrored as KiCad flips the board">
</p>

![23 PCIe x1 card: stacked bars of seconds per stage; stages 4 and 6 take 51% to 77% of a run. Simulation with GLB and STEP takes 13.7 s: read 0.9, resolve 1.1, geometry 3.5, materials 0.4 ms, assemble 3.4, write 3.2, verify 0.5, start-up and exit 1.1. Visual with GLB takes 17.0 s: read 0.8, resolve 1.0, geometry 3.6, materials 0.4 ms, assemble 9.4, write 85 ms, verify 0.8, start-up and exit 1.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/feature_23_pcie_card.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.9 | 1.1 | 3.5 | 0.4 ms | 3.4 | 3.2 | 0.5 | 1.1 | 13.7 |
| Visual, GLB | 0.8 | 1.0 | 3.6 | 0.4 ms | 9.4 | 85 ms | 0.8 | 1.2 | 17.0 |

| Board | `featureTest/23_pcie_card.kicad_pcb` ([5.3](Examples.md#53-pcie-x1-card)) |
|---|---|
| Outline | 80 × 64.4 mm with the fingers' tongue, a slot |
| Thickness | 1.57 mm |
| Copper layers | 4 |
| Vias | 239 through |
| Board edge | 36 gold fingers on a bevelled tongue |
| Mask, silkscreen, finish | Green, white, hard gold |

## 23.14 The Numbers

Seconds, the median of three runs for each stage, unless marked ms; the total is the sum of the bars.

| Board | Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 Slotted holes | simulation, GLB + STEP | 0.4 | 50 ms | 0.2 | 0.1 ms | 0.3 | 0.4 | 35 ms | 1.0 | 2.4 |
| 01 Slotted holes | visual, GLB | 0.4 | 48 ms | 0.2 | 0.1 ms | 0.8 | 5 ms | 39 ms | 1.0 | 2.5 |
| 02 Round holes | simulation, GLB + STEP | 0.4 | 43 ms | 0.2 | 0.1 ms | 0.3 | 0.3 | 32 ms | 1.0 | 2.3 |
| 02 Round holes | visual, GLB | 0.4 | 47 ms | 0.1 | 0.1 ms | 0.7 | 6 ms | 46 ms | 0.9 | 2.3 |
| 03 Through vias | simulation, GLB + STEP | 0.4 | 49 ms | 0.2 | 0.2 ms | 0.5 | 0.3 | 40 ms | 0.9 | 2.5 |
| 03 Through vias | visual, GLB | 0.4 | 44 ms | 0.2 | 0.1 ms | 0.8 | 5 ms | 53 ms | 1.0 | 2.5 |
| 03b KiCad 10 via options | simulation, GLB + STEP | 0.4 | 0.1 | 0.2 | 0.2 ms | 0.5 | 0.7 | 56 ms | 0.8 | 2.7 |
| 03b KiCad 10 via options | visual, GLB | 0.4 | 0.1 | 0.2 | 0.2 ms | 1.3 | 8 ms | 77 ms | 0.9 | 3.0 |
| 04 Blind and buried vias | simulation, GLB + STEP | 0.5 | 55 ms | 57 ms | 0.1 ms | 0.2 | 0.1 | 19 ms | 1.0 | 2.0 |
| 04 Blind and buried vias | visual, GLB | 0.4 | 48 ms | 57 ms | 0.1 ms | 0.4 | 3 ms | 32 ms | 0.9 | 1.9 |
| 05 Microvias | simulation, GLB + STEP | 0.4 | 52 ms | 51 ms | 0.1 ms | 0.2 | 0.1 | 18 ms | 1.1 | 1.9 |
| 05 Microvias | visual, GLB | 0.5 | 56 ms | 51 ms | 0.1 ms | 0.3 | 3 ms | 49 ms | 1.0 | 1.9 |
| 06 Padstacks | simulation, GLB + STEP | 0.4 | 44 ms | 82 ms | 0.1 ms | 0.3 | 0.2 | 29 ms | 1.0 | 2.1 |
| 06 Padstacks | visual, GLB | 0.4 | 44 ms | 87 ms | 0.1 ms | 0.7 | 4 ms | 34 ms | 1.0 | 2.3 |
| 07 Pad shapes | simulation, GLB + STEP | 0.4 | 35 ms | 0.1 | 0.1 ms | 0.3 | 0.5 | 22 ms | 0.8 | 2.1 |
| 07 Pad shapes | visual, GLB | 0.4 | 39 ms | 0.1 | 0.1 ms | 0.8 | 6 ms | 42 ms | 0.9 | 2.3 |
| 08 Copper graphics | simulation, GLB + STEP | 0.4 | 22 ms | 34 ms | 0.1 ms | 0.2 | 0.4 | 15 ms | 1.0 | 2.1 |
| 08 Copper graphics | visual, GLB | 0.4 | 22 ms | 36 ms | 0.1 ms | 0.5 | 4 ms | 54 ms | 0.9 | 2.0 |
| 08b Copper graphics on nets | simulation, GLB + STEP | 0.5 | 24 ms | 47 ms | 0.1 ms | 0.2 | 0.2 | 17 ms | 1.0 | 1.9 |
| 08b Copper graphics on nets | visual, GLB | 0.4 | 23 ms | 43 ms | 0.1 ms | 0.3 | 4 ms | 40 ms | 0.9 | 1.8 |
| 09 Copper text | simulation, GLB + STEP | 0.5 | 33 ms | 0.1 | 0.1 ms | 1.0 | 1.0 | 43 ms | 0.8 | 3.6 |
| 09 Copper text | visual, GLB | 0.4 | 40 ms | 0.1 | 0.1 ms | 1.1 | 13 ms | 78 ms | 0.8 | 2.5 |
| 10 Tracks and arcs | simulation, GLB + STEP | 0.4 | 21 ms | 37 ms | 0.1 ms | 0.2 | 0.2 | 14 ms | 1.0 | 1.8 |
| 10 Tracks and arcs | visual, GLB | 0.4 | 22 ms | 34 ms | 0.1 ms | 0.4 | 4 ms | 35 ms | 0.9 | 1.8 |
| 11 Zones | simulation, GLB + STEP | 0.5 | 99 ms | 0.3 | 0.1 ms | 0.6 | 0.8 | 78 ms | 0.8 | 3.2 |
| 11 Zones | visual, GLB | 0.4 | 98 ms | 0.3 | 0.1 ms | 1.4 | 9 ms | 57 ms | 0.9 | 3.2 |
| 12 Board outline shapes | simulation, GLB + STEP | 0.4 | 36 ms | 69 ms | 0.1 ms | 0.6 | 0.8 | 23 ms | 1.0 | 2.9 |
| 12 Board outline shapes | visual, GLB | 0.4 | 38 ms | 73 ms | 0.1 ms | 0.7 | 7 ms | 57 ms | 1.0 | 2.3 |
| 13a No board outline | simulation, GLB + STEP | 0.4 | 23 ms | 44 ms | 0.1 ms | 0.1 | 0.1 | 15 ms | 0.8 | 1.6 |
| 13a No board outline | visual, GLB | 0.4 | 23 ms | 47 ms | 0.1 ms | 0.2 | 3 ms | 59 ms | 1.0 | 1.7 |
| 13b Two board outlines | simulation, GLB + STEP | 0.4 | 19 ms | 38 ms | 0.1 ms | 99 ms | 92 ms | 13 ms | 1.0 | 1.6 |
| 13b Two board outlines | visual, GLB | 0.4 | 20 ms | 40 ms | 0.1 ms | 0.2 | 2 ms | 22 ms | 1.1 | 1.8 |
| 14 Full stack-up | simulation, GLB + STEP | 0.4 | 30 ms | 54 ms | 0.1 ms | 0.1 | 0.1 | 13 ms | 1.0 | 1.8 |
| 14 Full stack-up | visual, GLB | 0.4 | 35 ms | 61 ms | 0.1 ms | 0.3 | 3 ms | 32 ms | 1.0 | 1.8 |
| 15 No stack-up | simulation, GLB + STEP | 0.4 | 30 ms | 53 ms | 0.1 ms | 0.1 | 0.1 | 15 ms | 1.1 | 1.9 |
| 15 No stack-up | visual, GLB | 0.5 | 26 ms | 48 ms | 0.1 ms | 0.3 | 3 ms | 29 ms | 0.9 | 1.7 |
| 16 Castellated pads and a plated edge | simulation, GLB + STEP | 0.4 | 66 ms | 87 ms | 0.1 ms | 0.2 | 0.1 | 23 ms | 1.0 | 1.9 |
| 16 Castellated pads and a plated edge | visual, GLB | 0.4 | 73 ms | 97 ms | 0.1 ms | 0.3 | 3 ms | 39 ms | 0.9 | 1.9 |
| 16b Plated board edge with a GND border | simulation, GLB + STEP | 0.5 | 0.4 | 2.0 | 0.2 ms | 2.1 | 1.5 | 0.5 | 0.9 | 7.8 |
| 16b Plated board edge with a GND border | visual, GLB | 0.5 | 0.4 | 2.0 | 0.2 ms | 4.5 | 20 ms | 0.1 | 0.8 | 8.4 |
| 17 Solder mask and silkscreen | simulation, GLB + STEP | 0.4 | 61 ms | 94 ms | 0.1 ms | 0.2 | 0.2 | 15 ms | 0.9 | 1.9 |
| 17 Solder mask and silkscreen | visual, GLB | 0.4 | 57 ms | 94 ms | 0.1 ms | 0.5 | 4 ms | 48 ms | 0.9 | 2.1 |
| 17b Silkscreen over copper | simulation, GLB + STEP | 0.4 | 30 ms | 0.1 | 0.1 ms | 0.2 | 0.2 | 20 ms | 0.9 | 1.9 |
| 17b Silkscreen over copper | visual, GLB | 0.4 | 29 ms | 0.2 | 0.1 ms | 0.7 | 4 ms | 37 ms | 0.8 | 2.1 |
| 18 Gold edge fingers | simulation, GLB + STEP | 0.4 | 30 ms | 41 ms | 0.1 ms | 0.2 | 0.1 | 15 ms | 0.8 | 1.6 |
| 18 Gold edge fingers | visual, GLB | 0.4 | 30 ms | 38 ms | 0.1 ms | 0.3 | 4 ms | 43 ms | 0.9 | 1.8 |
| 18b Finish on every kind of bare copper | simulation, GLB + STEP | 0.4 | 32 ms | 86 ms | 0.1 ms | 0.2 | 0.2 | 22 ms | 0.9 | 1.8 |
| 18b Finish on every kind of bare copper | visual, GLB | 0.4 | 32 ms | 0.1 | 0.1 ms | 0.4 | 4 ms | 32 ms | 0.9 | 1.8 |
| 18c Finish before the solder mask | simulation, GLB + STEP | 0.4 | 34 ms | 0.1 | 0.1 ms | 0.4 | 0.3 | 31 ms | 0.8 | 2.2 |
| 18c Finish before the solder mask | visual, GLB | 0.4 | 31 ms | 0.1 | 0.1 ms | 0.8 | 4 ms | 42 ms | 0.9 | 2.3 |
| 19 Items KESE skips | simulation, GLB + STEP | 0.4 | 19 ms | 21 ms | 0.1 ms | 43 ms | 43 ms | 6 ms | 0.9 | 1.4 |
| 19 Items KESE skips | visual, GLB | 0.4 | 16 ms | 22 ms | 0.1 ms | 0.1 | 2 ms | 19 ms | 0.9 | 1.5 |
| 19b Items KESE skips, KiCad 10 | simulation, GLB + STEP | 0.5 | 3 ms | 3 ms | 0.0 ms | 15 ms | 8 ms | 1 ms | 0.8 | 1.3 |
| 19b Items KESE skips, KiCad 10 | visual, GLB | 0.4 | 3 ms | 3 ms | 0.0 ms | 25 ms | 1.0 ms | 11 ms | 0.7 | 1.2 |
| 20a KiCad 6 format | simulation, GLB + STEP | 0.4 | 27 ms | 54 ms | 0.1 ms | 0.2 | 0.1 | 18 ms | 0.9 | 1.7 |
| 20a KiCad 6 format | visual, GLB | 0.4 | 26 ms | 55 ms | 0.1 ms | 0.3 | 3 ms | 28 ms | 0.8 | 1.6 |
| 20b KiCad 7 format | simulation, GLB + STEP | 0.4 | 27 ms | 61 ms | 0.1 ms | 0.2 | 0.1 | 18 ms | 0.8 | 1.6 |
| 20b KiCad 7 format | visual, GLB | 0.4 | 27 ms | 61 ms | 0.1 ms | 0.3 | 3 ms | 28 ms | 0.8 | 1.6 |
| 20c KiCad 8 format | simulation, GLB + STEP | 0.4 | 29 ms | 55 ms | 0.1 ms | 0.1 | 0.1 | 14 ms | 0.7 | 1.5 |
| 20c KiCad 8 format | visual, GLB | 0.4 | 26 ms | 68 ms | 0.1 ms | 0.3 | 4 ms | 33 ms | 0.7 | 1.5 |
| 20d KiCad 9 format | simulation, GLB + STEP | 0.4 | 27 ms | 57 ms | 0.1 ms | 0.2 | 0.2 | 18 ms | 0.8 | 1.6 |
| 20d KiCad 9 format | visual, GLB | 0.4 | 26 ms | 58 ms | 0.1 ms | 0.3 | 3 ms | 30 ms | 0.9 | 1.8 |
| 20e KiCad 10 format | simulation, GLB + STEP | 0.4 | 28 ms | 61 ms | 0.1 ms | 0.2 | 0.1 | 15 ms | 0.9 | 1.8 |
| 20e KiCad 10 format | visual, GLB | 0.4 | 29 ms | 68 ms | 0.1 ms | 0.3 | 3 ms | 37 ms | 0.9 | 1.8 |
| 21 RF sensor module | simulation, GLB + STEP | 0.8 | 1.6 | 6.5 | 0.4 ms | 5.7 | 3.3 | 0.6 | 1.0 | 19.4 |
| 21 RF sensor module | visual, GLB | 0.8 | 1.5 | 6.4 | 0.4 ms | 10.0 | 93 ms | 0.7 | 1.0 | 20.5 |
| 22 HDI radio module | simulation, GLB + STEP | 0.8 | 1.0 | 2.3 | 0.3 ms | 1.9 | 1.6 | 0.4 | 1.1 | 9.1 |
| 22 HDI radio module | visual, GLB | 0.8 | 1.0 | 2.3 | 0.4 ms | 5.7 | 44 ms | 0.3 | 1.0 | 11.1 |
| 23 PCIe x1 card | simulation, GLB + STEP | 0.9 | 1.1 | 3.5 | 0.4 ms | 3.4 | 3.2 | 0.5 | 1.1 | 13.7 |
| 23 PCIe x1 card | visual, GLB | 0.8 | 1.0 | 3.6 | 0.4 ms | 9.4 | 85 ms | 0.8 | 1.2 | 17.0 |

| Previous | Next |
|:---|---:|
| [openEMS Workflow](OpenEMS-Workflow.md) | [Glossary](Glossary.md) |
