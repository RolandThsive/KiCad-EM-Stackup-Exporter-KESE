# 6. Time Distribution

Where the time of a run goes, stage by stage, for the three example boards of `Generator/Input/`
([Examples](Examples.md)). Each board was exported three times in each mode, with the Verifier
on, and each bar is the median of the three runs for that stage, read from the `timing` block of
[`report.txt`](Project-Output-Organization.md#2022-reporttxt):

```text
python run_KESE.py Input/rf_module.kicad_pcb --mode simulation --format glb step --verify
python run_KESE.py Input/rf_module.kicad_pcb --mode visual --format glb --verify
```

All 18 runs passed the Verifier.

**The runs used the default parameters on one Linux machine with 4 cores (an Intel Xeon at 2.1 GHz)
and 16 GB of RAM, so `Parallel.WORKERS = 0` gave four workers
([Work Done In Parallel](Working-Principle.md#74-work-done-in-parallel)). On another machine the
seconds differ.**

| Bar | Stages | What runs in it |
|---|---|---|
| 1–2 read | 1 read, 2 collect | The file parsed; every track, pad, zone, graphic and text as a flat shape; the stroke font unpacked and split into lines (about 0.05 s), and the glyphs the text uses parsed |
| 3 resolve | 3 | The copper joined per layer and net, clipped and drilled; barrels, edge plating, mask openings and silkscreen |
| 4 geometry | 4 | Every part as prisms, between the heights of the stack-up |
| 5 materials | 5 | A material for every part, from `parameters/color.py` and the stack-up's colours: 0.2 to 0.3 ms |
| 6 assemble | 6 | Closed solids in simulation mode, the visible skin in visual mode; with `--verify`, each solid is also checked here by the worker that built it |
| 7 write | 7 | The files. In simulation mode nearly all of it is the STEP file: the HDI module takes 1.6 s with STEP alone and 0.1 s with GLB alone. The visual GLB takes 29 to 45 ms |
| 8 verify | 8 | The Verifier's checks of the written files ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md)) |
| start-up and exit | none | The wall-clock time less the stages, about 0.2 s: Python starting (12 ms), KESE and the libraries it uses imported (0.13 s), the run set up and closed around the stages (16 ms), stage 9 writing `report.txt` and `parameters.txt` (1 to 2 ms), and Python freeing the run's memory as it ends (0.06 s) |

Under each chart a table gives the same numbers, in seconds unless marked ms. A stage too thin to
see at this scale is marked with a line and a label.

## 6.1 RF Sensor Module

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/top_straight_visual.webp" width="49.5%" alt="The RF sensor module straight from above in visual mode: the blue mask, the white silkscreen, the gold of the ENIG pads, the plated edge and cut-out, and the fence of vias in the GND border">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/bottom_straight_visual.webp" width="49.5%" alt="The RF sensor module straight from below: the KESE logo, the outline of the CR1220 coin cell BT1, the pads of the I2C and UART lines, and the plated edge and cut-out">
</p>

![RF sensor module: stacked bars of seconds per stage. Simulation with GLB and STEP takes 16.3 s: read 0.2, resolve 1.6, geometry 6.2, materials 0.3 ms, assemble 5.2, write 2.4, verify 0.4, start-up and exit 0.2. Visual with GLB takes 14.7 s: read 0.3, resolve 1.4, geometry 6.3, materials 0.3 ms, assemble 6.2, write 45 ms, verify 0.4, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/time_1_rf_module.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.2 | 1.6 | 6.2 | 0.3 ms | 5.2 | 2.4 | 0.4 | 0.2 | 16.3 |
| Visual, GLB | 0.3 | 1.4 | 6.3 | 0.3 ms | 6.2 | 45 ms | 0.4 | 0.2 | 14.7 |

<div align="center">

| Board | `Input/rf_module.kicad_pcb` ([5.1](Examples.md#51-rf-sensor-module)) |
|---|---|
| Outline | 64 × 44 mm, a cut-out |
| Thickness | 1.6 mm |
| Copper layers | 4 |
| Vias | 307 through |
| Board edge | Plated all round and in the cut-out |
| Mask, silkscreen, finish | Blue, white, ENIG |

</div>

## 6.2 HDI Radio Module

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/top_straight_visual.webp" width="36%" alt="The HDI radio module straight from above in visual mode: the black mask, the meander antenna reading through it, the BGA's pads, the flash U2, the crystal Y1 and the castellated pads on three sides">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/bottom_straight_visual.webp" width="36%" alt="The HDI radio module straight from below: the exposed GND pad, the logo, the pin numbers 1 to 43 beside the castellated pads, and the test pads TX, RX, BOOT, 3V3, EN and GND">
</p>

![HDI radio module: stacked bars of seconds per stage. Simulation with GLB and STEP takes 8.5 s: read 0.2, resolve 0.9, geometry 3.0, materials 0.2 ms, assemble 2.2, write 1.7, verify 0.4, start-up and exit 0.2. Visual with GLB takes 9.2 s: read 0.2, resolve 1.0, geometry 2.7, materials 0.2 ms, assemble 4.8, write 29 ms, verify 0.2, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/time_2_hdi_module.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.2 | 0.9 | 3.0 | 0.2 ms | 2.2 | 1.7 | 0.4 | 0.2 | 8.5 |
| Visual, GLB | 0.2 | 1.0 | 2.7 | 0.2 ms | 4.8 | 29 ms | 0.2 | 0.2 | 9.2 |

<div align="center">

| Board | `Input/hdi_module.kicad_pcb` ([5.2](Examples.md#52-hdi-radio-module)) |
|---|---|
| Outline | 22 × 30 mm |
| Thickness | 0.925 mm |
| Copper layers | 6, built 1+4+1 |
| Vias | 150: 71 micro, 34 blind and buried, 45 through |
| Board edge | 43 castellated pads |
| Mask, silkscreen, finish | Black, white, immersion silver |

</div>

## 6.3 PCIe x1 Card

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/top_straight_visual.webp" width="49.5%" alt="The PCIe x1 card straight from above in visual mode: the green mask, the controller, the RJ45 footprint, the PoE side behind its dashed isolation line and slot, the logo and the gold fingers">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/bottom_straight_visual.webp" width="49.5%" alt="The PCIe x1 card straight from below: the A side of the fingers, the tracks reading through the mask and the name in silkscreen">
</p>

![PCIe x1 card: stacked bars of seconds per stage. Simulation with GLB and STEP takes 10.8 s: read 0.3, resolve 1.1, geometry 3.9, materials 0.2 ms, assemble 2.7, write 2.1, verify 0.3, start-up and exit 0.3. Visual with GLB takes 11.3 s: read 0.3, resolve 1.1, geometry 4.1, materials 0.2 ms, assemble 5.1, write 41 ms, verify 0.4, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/time_3_pcie_card.webp)

| Mode | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB + STEP | 0.3 | 1.1 | 3.9 | 0.2 ms | 2.7 | 2.1 | 0.3 | 0.3 | 10.8 |
| Visual, GLB | 0.3 | 1.1 | 4.1 | 0.2 ms | 5.1 | 41 ms | 0.4 | 0.2 | 11.3 |

<div align="center">

| Board | `Input/pcie_card.kicad_pcb` ([5.3](Examples.md#53-pcie-x1-card)) |
|---|---|
| Outline | 80 × 64.4 mm with the fingers' tongue, a slot |
| Thickness | 1.57 mm |
| Copper layers | 4 |
| Vias | 239 through |
| Board edge | 36 gold fingers |
| Mask, silkscreen, finish | Green, white, hard gold |

</div>

## 6.4 Timing Your Own Board

Every run writes the same block at the end of its `report.txt`, so the time of any board can be
read the same way. The HDI module's third simulation run:

```text
timing
  read              0.0343 s
  collect           0.1381 s
  resolve           0.8515 s
  geometry          2.7272 s
  materials         0.0003 s
  assemble          2.1252 s
  write             1.7215 s
  verify            0.3686 s
```

`verify` is there only when the Verifier ran. Each value is in seconds, to 0.1 ms.

| Previous | Next |
|:---|---:|
| [Examples](Examples.md) | [Working Principle](Working-Principle.md) |
