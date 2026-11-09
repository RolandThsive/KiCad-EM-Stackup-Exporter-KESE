# 6. Time Distribution

Where the time of a run goes, stage by stage, for the three example boards of `Generator/Input/`
([Examples](Examples.md)). Each board was exported in every format KESE writes, one format a run:
GLB, STEP, STL and OBJ in simulation mode, and GLB and OBJ in visual mode. Each of those six runs
was made three times, with the Verifier on, and each bar is the median of the three runs for that
stage, read from the `timing` block of
[`report.txt`](Project-Output-Organization.md#2022-reporttxt):

```text
python run_KESE.py Input/rf_module.kicad_pcb --mode simulation --format glb --verify
python run_KESE.py Input/rf_module.kicad_pcb --mode simulation --format step --verify
python run_KESE.py Input/rf_module.kicad_pcb --mode simulation --format stl --verify
python run_KESE.py Input/rf_module.kicad_pcb --mode simulation --format obj --verify
python run_KESE.py Input/rf_module.kicad_pcb --mode visual --format glb --verify
python run_KESE.py Input/rf_module.kicad_pcb --mode visual --format obj --verify
```

All 54 runs passed the Verifier. Beside each board's facts, a second table gives, for each of the
six runs, the size of the model file it writes and the most memory it used at once: the
proportional set size (PSS) of KESE's process and its workers, summed and sampled every 10 ms, the
median of three more runs. The STL size is that of the `stl/` folder, one file a part, and the OBJ
size includes its `.mtl`. MB is a million bytes.

**The runs used the default parameters on one Linux machine with 4 cores (an Intel Xeon at 2.1 GHz)
and 16 GB of RAM, so `Parallel.WORKERS = 0` gave four workers
([Work Done In Parallel](Working-Principle.md#74-work-done-in-parallel)). On another machine the
seconds differ.**

| Bar | Stages | What runs in it |
|---|---|---|
| 1–2 read | 1 read, 2 collect | The file parsed; every track, pad, zone, graphic and text as a flat shape; the stroke font unpacked and split into lines (about 0.06 s), and the glyphs the text uses parsed |
| 3 resolve | 3 | The copper joined per layer and net, clipped and drilled; barrels, edge plating, mask openings and silkscreen |
| 4 geometry | 4 | Every part as prisms, between the heights of the stack-up |
| 5 materials | 5 | A material for every part, from `parameters/color.py` and the stack-up's colours: 0.2 to 0.3 ms |
| 6 assemble | 6 | Closed solids in simulation mode, the visible skin in visual mode; with `--verify`, each solid is also checked here by the worker that built it |
| 7 write | 7 | The files, the one stage the format changes much. On the three boards GLB takes 0.11 to 0.19 s in simulation mode and 33 to 53 ms in visual mode, STL 0.15 to 0.32 s, STEP 1.7 to 2.5 s, and OBJ 3.6 to 6.9 s in simulation mode and 0.9 to 1.7 s in visual mode |
| 8 verify | 8 | The Verifier's checks of the written files ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md)) |
| start-up and exit | none | The wall-clock time less the stages, about 0.2 s: Python starting (13 ms), KESE and the libraries it uses imported (0.12 s), the run set up and closed around the stages (14 ms), stage 9 writing `report.txt` and `parameters.txt` (1 to 3 ms), and Python freeing the run's memory as it ends (0.04 s) |

Under each chart a table gives the same numbers, in seconds unless marked ms. A stage too thin to
see at this scale is marked with a line and a label.

## 6.1 RF Sensor Module

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Time-Distribution/rf_module/top_straight_visual.webp" width="49.5%" alt="The RF sensor module straight from above in visual mode: the blue mask, the white silkscreen, the gold of the ENIG pads, the plated edge and cut-out, and the fence of vias in the GND border">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Time-Distribution/rf_module/bottom_straight_visual.webp" width="49.5%" alt="The RF sensor module straight from below: the KESE logo, the outline of the CR1220 coin cell BT1, the pads of the I2C and UART lines, and the plated edge and cut-out">
</p>

![RF sensor module: stacked bars of seconds per stage, one format a run. Simulation with GLB takes 15.2 s: read 0.3, resolve 1.6, geometry 7.2, materials 0.3 ms, assemble 5.2, write 0.2, verify 0.4, start-up and exit 0.2. Simulation with STEP takes 17.8 s: read 0.3, resolve 1.6, geometry 7.2, materials 0.2 ms, assemble 5.4, write 2.5, verify 0.5, start-up and exit 0.2. Simulation with STL takes 15.8 s: read 0.3, resolve 1.8, geometry 7.1, materials 0.2 ms, assemble 5.5, write 0.3, verify 0.5, start-up and exit 0.2. Simulation with OBJ takes 22.1 s: read 0.3, resolve 1.7, geometry 7.1, materials 0.2 ms, assemble 5.4, write 6.9, verify 0.5, start-up and exit 0.2. Visual with GLB takes 16.6 s: read 0.3, resolve 1.7, geometry 7.3, materials 0.2 ms, assemble 6.7, write 53 ms, verify 0.4, start-up and exit 0.2. Visual with OBJ takes 18.2 s: read 0.3, resolve 1.7, geometry 7.3, materials 0.3 ms, assemble 6.6, write 1.7, verify 0.4, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Time-Distribution/time_1_rf_module.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.6 | 7.2 | 0.3&nbsp;ms | 5.2 | 0.2 | 0.4 | 0.2 | 15.2 |
| Simulation, STEP | 0.3 | 1.6 | 7.2 | 0.2&nbsp;ms | 5.4 | 2.5 | 0.5 | 0.2 | 17.8 |
| Simulation, STL | 0.3 | 1.8 | 7.1 | 0.2&nbsp;ms | 5.5 | 0.3 | 0.5 | 0.2 | 15.8 |
| Simulation, OBJ | 0.3 | 1.7 | 7.1 | 0.2&nbsp;ms | 5.4 | 6.9 | 0.5 | 0.2 | 22.1 |
| Visual, GLB | 0.3 | 1.7 | 7.3 | 0.2&nbsp;ms | 6.7 | 53&nbsp;ms | 0.4 | 0.2 | 16.6 |
| Visual, OBJ | 0.3 | 1.7 | 7.3 | 0.3&nbsp;ms | 6.6 | 1.7 | 0.4 | 0.2 | 18.2 |

<table align="left">
<thead><tr><th>Board</th><th><code>Input/rf_module.kicad_pcb</code><br>(<a href="https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/Examples#51-rf-sensor-module">5.1</a>)</th></tr></thead>
<tbody>
<tr><td>Outline</td><td>64 × 44 mm, a cut-out</td></tr>
<tr><td>Thickness</td><td>1.6 mm</td></tr>
<tr><td>Copper layers</td><td>4</td></tr>
<tr><td>Vias</td><td>307 through</td></tr>
<tr><td>Board edge</td><td>Plated all round<br>and in the cut-out</td></tr>
<tr><td>Mask, silkscreen,<br>finish</td><td>Blue, white, ENIG</td></tr>
</tbody>
</table>
<table align="right">
<tr><th>File type</th><th>File size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">37.3 MB</td><td align="right">503 MB</td></tr>
<tr><td>STEP</td><td align="right">114.7 MB</td><td align="right">605 MB</td></tr>
<tr><td>STL</td><td align="right">55.3 MB</td><td align="right">507 MB</td></tr>
<tr><td>OBJ</td><td align="right">111.2 MB</td><td align="right">769 MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">10.3 MB</td><td align="right">390 MB</td></tr>
<tr><td>OBJ</td><td align="right">30.6 MB</td><td align="right">398 MB</td></tr>
</table>
<br clear="all">

## 6.2 HDI Radio Module

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Time-Distribution/hdi_module/top_straight_visual.webp" width="36%" alt="The HDI radio module straight from above in visual mode: the black mask, the meander antenna reading through it, the BGA's pads, the flash U2, the crystal Y1 and the castellated pads on three sides">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Time-Distribution/hdi_module/bottom_straight_visual.webp" width="36%" alt="The HDI radio module straight from below: the exposed GND pad, the logo, the pin numbers 1 to 43 beside the castellated pads, and the test pads TX, RX, BOOT, 3V3, EN and GND">
</p>

![HDI radio module: stacked bars of seconds per stage, one format a run. Simulation with GLB takes 7.4 s: read 0.2, resolve 1.1, geometry 3.2, materials 0.3 ms, assemble 2.3, write 0.1, verify 0.4, start-up and exit 0.2. Simulation with STEP takes 9.1 s: read 0.2, resolve 1.1, geometry 3.2, materials 0.3 ms, assemble 2.4, write 1.7, verify 0.4, start-up and exit 0.2. Simulation with STL takes 7.7 s: read 0.2, resolve 1.1, geometry 3.3, materials 0.2 ms, assemble 2.3, write 0.2, verify 0.4, start-up and exit 0.2. Simulation with OBJ takes 11.3 s: read 0.2, resolve 1.1, geometry 3.3, materials 0.2 ms, assemble 2.4, write 3.6, verify 0.4, start-up and exit 0.2. Visual with GLB takes 8.2 s: read 0.2, resolve 1.1, geometry 3.2, materials 0.3 ms, assemble 3.2, write 33 ms, verify 0.2, start-up and exit 0.2. Visual with OBJ takes 8.8 s: read 0.2, resolve 1.0, geometry 3.2, materials 0.2 ms, assemble 3.1, write 0.9, verify 0.2, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Time-Distribution/time_2_hdi_module.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 1.1 | 3.2 | 0.3&nbsp;ms | 2.3 | 0.1 | 0.4 | 0.2 | 7.4 |
| Simulation, STEP | 0.2 | 1.1 | 3.2 | 0.3&nbsp;ms | 2.4 | 1.7 | 0.4 | 0.2 | 9.1 |
| Simulation, STL | 0.2 | 1.1 | 3.3 | 0.2&nbsp;ms | 2.3 | 0.2 | 0.4 | 0.2 | 7.7 |
| Simulation, OBJ | 0.2 | 1.1 | 3.3 | 0.2&nbsp;ms | 2.4 | 3.6 | 0.4 | 0.2 | 11.3 |
| Visual, GLB | 0.2 | 1.1 | 3.2 | 0.3&nbsp;ms | 3.2 | 33&nbsp;ms | 0.2 | 0.2 | 8.2 |
| Visual, OBJ | 0.2 | 1.0 | 3.2 | 0.2&nbsp;ms | 3.1 | 0.9 | 0.2 | 0.2 | 8.8 |

<table align="left">
<thead><tr><th>Board</th><th><code>Input/hdi_module.kicad_pcb</code><br>(<a href="https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/Examples#52-hdi-radio-module">5.2</a>)</th></tr></thead>
<tbody>
<tr><td>Outline</td><td>22 × 30 mm</td></tr>
<tr><td>Thickness</td><td>0.925 mm</td></tr>
<tr><td>Copper layers</td><td>6, built 1+4+1</td></tr>
<tr><td>Vias</td><td>150: 71 micro,<br>34 blind and buried, 45 through</td></tr>
<tr><td>Board edge</td><td>43 castellated pads</td></tr>
<tr><td>Mask, silkscreen,<br>finish</td><td>Black, white, immersion silver</td></tr>
</tbody>
</table>
<table align="right">
<tr><th>File type</th><th>File size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">20.4 MB</td><td align="right">344 MB</td></tr>
<tr><td>STEP</td><td align="right">72.7 MB</td><td align="right">357 MB</td></tr>
<tr><td>STL</td><td align="right">29.8 MB</td><td align="right">355 MB</td></tr>
<tr><td>OBJ</td><td align="right">61.1 MB</td><td align="right">452 MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.6 MB</td><td align="right">232 MB</td></tr>
<tr><td>OBJ</td><td align="right">16.6 MB</td><td align="right">234 MB</td></tr>
</table>
<br clear="all">

## 6.3 PCIe x1 Card

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Time-Distribution/pcie_card/top_straight_visual.webp" width="49.5%" alt="The PCIe x1 card straight from above in visual mode: the green mask, the controller, the RJ45 footprint, the PoE side behind its dashed isolation line and slot, the logo and the gold fingers">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Time-Distribution/pcie_card/bottom_straight_visual.webp" width="49.5%" alt="The PCIe x1 card straight from below: the A side of the fingers, the tracks reading through the mask and the name in silkscreen">
</p>

![PCIe x1 card: stacked bars of seconds per stage, one format a run. Simulation with GLB takes 9.8 s: read 0.3, resolve 1.3, geometry 4.6, materials 0.2 ms, assemble 2.9, write 0.1, verify 0.4, start-up and exit 0.3. Simulation with STEP takes 11.9 s: read 0.3, resolve 1.2, geometry 4.7, materials 0.3 ms, assemble 2.8, write 2.3, verify 0.4, start-up and exit 0.2. Simulation with STL takes 10.4 s: read 0.4, resolve 1.4, geometry 4.8, materials 0.2 ms, assemble 2.9, write 0.3, verify 0.4, start-up and exit 0.2. Simulation with OBJ takes 14.7 s: read 0.3, resolve 1.3, geometry 4.7, materials 0.2 ms, assemble 2.8, write 5.0, verify 0.4, start-up and exit 0.2. Visual with GLB takes 10.7 s: read 0.3, resolve 1.2, geometry 4.5, materials 0.2 ms, assemble 4.0, write 46 ms, verify 0.4, start-up and exit 0.2. Visual with OBJ takes 12.6 s: read 0.3, resolve 1.2, geometry 4.7, materials 0.3 ms, assemble 4.2, write 1.6, verify 0.3, start-up and exit 0.2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Time-Distribution/time_3_pcie_card.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.3 | 4.6 | 0.2&nbsp;ms | 2.9 | 0.1 | 0.4 | 0.3 | 9.8 |
| Simulation, STEP | 0.3 | 1.2 | 4.7 | 0.3&nbsp;ms | 2.8 | 2.3 | 0.4 | 0.2 | 11.9 |
| Simulation, STL | 0.4 | 1.4 | 4.8 | 0.2&nbsp;ms | 2.9 | 0.3 | 0.4 | 0.2 | 10.4 |
| Simulation, OBJ | 0.3 | 1.3 | 4.7 | 0.2&nbsp;ms | 2.8 | 5.0 | 0.4 | 0.2 | 14.7 |
| Visual, GLB | 0.3 | 1.2 | 4.5 | 0.2&nbsp;ms | 4.0 | 46&nbsp;ms | 0.4 | 0.2 | 10.7 |
| Visual, OBJ | 0.3 | 1.2 | 4.7 | 0.3&nbsp;ms | 4.2 | 1.6 | 0.3 | 0.2 | 12.6 |

<table align="left">
<thead><tr><th>Board</th><th><code>Input/pcie_card.kicad_pcb</code><br>(<a href="https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/Examples#53-pcie-x1-card">5.3</a>)</th></tr></thead>
<tbody>
<tr><td>Outline</td><td>80 × 64.4 mm with the fingers' tongue,<br>a slot</td></tr>
<tr><td>Thickness</td><td>1.57 mm</td></tr>
<tr><td>Copper layers</td><td>4</td></tr>
<tr><td>Vias</td><td>239 through</td></tr>
<tr><td>Board edge</td><td>36 gold fingers</td></tr>
<tr><td>Mask, silkscreen,<br>finish</td><td>Green, white, hard gold</td></tr>
</tbody>
</table>
<table align="right">
<tr><th>File type</th><th>File size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">29.0 MB</td><td align="right">444 MB</td></tr>
<tr><td>STEP</td><td align="right">80.1 MB</td><td align="right">482 MB</td></tr>
<tr><td>STL</td><td align="right">42.3 MB</td><td align="right">434 MB</td></tr>
<tr><td>OBJ</td><td align="right">85.6 MB</td><td align="right">624 MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.8 MB</td><td align="right">323 MB</td></tr>
<tr><td>OBJ</td><td align="right">25.7 MB</td><td align="right">318 MB</td></tr>
</table>
<br clear="all">

## 6.4 Timing Your Own Board

Every run writes the same block in its `report.txt`, after the parts and before the Verifier's
lines, so the time of any board can be read the same way. The HDI module's third simulation run
with STEP:

```text
timing
  read              0.0631 s
  collect           0.1707 s
  resolve           1.0373 s
  geometry          3.0882 s
  materials         0.0002 s
  assemble          2.2221 s
  write             1.6603 s
  verify            0.3499 s
```

`verify` is there only when the Verifier ran. Each value is in seconds, to 0.1 ms.

| Previous | Next |
|:---|---:|
| [Examples](Examples.md) | [Working Principle](Working-Principle.md) |
