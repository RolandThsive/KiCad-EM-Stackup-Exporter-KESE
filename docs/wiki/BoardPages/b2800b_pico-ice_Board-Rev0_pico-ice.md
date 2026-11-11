# 2800. pico-ice

Board 2,800 of the 3,117 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 26](../CorpusTestingPages/Corpus-Testing-26.md#2800-pico-ice).

![pico-ice: stages 4 and 6 take 48% to 83% of a run. Simulation, GLB takes 20 s. Simulation, STEP takes 25 s. Simulation, STL takes 21 s. Simulation, OBJ takes 34 s. Visual, GLB takes 30 s. Visual, OBJ takes 38 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2800b_pico-ice_Board-Rev0_pico-ice/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 2.3 | 8.0 | 0.6&nbsp;ms | 7.9 | 0.3 | 1.0 | 0.2 | 20.4 |
| Simulation, STEP | 0.6 | 2.2 | 7.9 | 0.6&nbsp;ms | 7.9 | 5.5 | 1.0 | 0.2 | 25.3 |
| Simulation, STL | 0.6 | 2.3 | 8.6 | 0.5&nbsp;ms | 7.8 | 0.7 | 1.0 | 0.3 | 21.3 |
| Simulation, OBJ | 0.7 | 2.2 | 8.7 | 0.5&nbsp;ms | 8.0 | 13.5 | 1.0 | 0.3 | 34.4 |
| Visual, GLB | 0.7 | 2.5 | 8.1 | 0.8&nbsp;ms | 16.6 | 0.2 | 1.6 | 0.3 | 29.9 |
| Visual, OBJ | 0.6 | 2.3 | 8.1 | 0.6&nbsp;ms | 17.4 | 7.3 | 1.9 | 0.3 | 38.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [tinyvision-ai-inc/pico-ice](https://github.com/tinyvision-ai-inc/pico-ice)<br>Board: `pico-ice.kicad_pcb` |
|---|---|
| Folder | Board / Rev0 |
| Complexity | 375&nbsp;/&nbsp;1000 (size&nbsp;255, features&nbsp;120) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 95, 1,537, 178 |
| Triangles,&nbsp;simulation | 2,230,612 in 110 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">77&nbsp;MB</td><td align="right">749&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">401&nbsp;MB</td><td align="right">889&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">112&nbsp;MB</td><td align="right">779&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">242&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">48&nbsp;MB</td><td align="right">888&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">149&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2799. syzygy-mipi-adapter](b2799b_oshw-adapters_syzygy-mipi-adapter-board-Rev1_syzygy-mipi-adapter.md) | [2801. pico-ice](b2801b_pico-ice_Board-Rev1_pico-ice.md) |
