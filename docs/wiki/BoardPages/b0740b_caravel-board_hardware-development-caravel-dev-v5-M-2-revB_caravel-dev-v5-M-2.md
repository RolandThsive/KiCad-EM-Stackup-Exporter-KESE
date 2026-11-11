# 740. caravel-dev-v5-M.2

Board 740 of the 3,117 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 7](../CorpusTestingPages/Corpus-Testing-07.md#740-caravel-dev-v5-m2).

![caravel-dev-v5-M.2: stages 4 and 6 take 55% to 83% of a run. Simulation, GLB takes 15 s. Simulation, STEP takes 19 s. Simulation, STL takes 15 s. Simulation, OBJ takes 22 s. Visual, GLB takes 21 s. Visual, OBJ takes 27 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0740b_caravel-board_hardware-development-caravel-dev-v5-M-2-revB_caravel-dev-v5-M-2/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.3 | 6.5 | 0.6&nbsp;ms | 5.4 | 0.2 | 0.7 | 0.2 | 14.9 |
| Simulation, STEP | 0.5 | 1.4 | 6.4 | 0.6&nbsp;ms | 5.4 | 4.3 | 0.7 | 0.3 | 18.9 |
| Simulation, STL | 0.5 | 1.3 | 6.3 | 0.6&nbsp;ms | 5.4 | 0.4 | 0.7 | 0.3 | 14.8 |
| Simulation, OBJ | 0.5 | 1.4 | 6.4 | 0.6&nbsp;ms | 5.4 | 7.0 | 0.7 | 0.2 | 21.5 |
| Visual, GLB | 0.5 | 1.3 | 6.2 | 0.6&nbsp;ms | 11.5 | 0.2 | 1.3 | 0.3 | 21.3 |
| Visual, OBJ | 0.5 | 1.3 | 6.4 | 0.9&nbsp;ms | 11.3 | 6.1 | 1.3 | 0.2 | 27.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [chipfoundry/caravel_board](https://github.com/chipfoundry/caravel_board)<br>Board: `caravel-dev-v5-M.2.kicad_pcb` |
|---|---|
| Folder | hardware / development / caravel-dev-v5-M.2-revB |
| Complexity | 320&nbsp;/&nbsp;1000 (size&nbsp;220, features&nbsp;100) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, knockout text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 67, 982, 118 |
| Triangles,&nbsp;simulation | 1,221,970 in 111 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">42&nbsp;MB</td><td align="right">559&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">212&nbsp;MB</td><td align="right">651&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">61&nbsp;MB</td><td align="right">525&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">125&nbsp;MB</td><td align="right">843&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">34&nbsp;MB</td><td align="right">734&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">101&nbsp;MB</td><td align="right">799&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [739. caravel-dev-v5-M.2](b0739b_caravel-board_hardware-development-caravel-dev-v5-M-2-revA_caravel-dev-v5-M-2.md) | [741. Fab-Drawing-caravel-dev-v5-M.2](b0741b_caravel-board_Fab-Drawing-caravel-dev-v5-M-2.md) |
