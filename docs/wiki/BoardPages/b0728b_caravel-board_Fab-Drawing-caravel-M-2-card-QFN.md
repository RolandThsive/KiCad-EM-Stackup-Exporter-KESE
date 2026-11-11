# 728. Fab-Drawing-caravel-M.2-card-QFN

Board 728 of the 3,112 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 7](../CorpusTestingPages/Corpus-Testing-07.md#728-fab-drawing-caravel-m2-card-qfn).

![Stages 4 and 6 take 48% to 81% of a run. Simulation, GLB takes 5.2 s. Simulation, STEP takes 6.4 s. Simulation, STL takes 5.1 s. Simulation, OBJ takes 7.6 s. Visual, GLB takes 8.4 s. Visual, OBJ takes 10 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0728b_caravel-board_Fab-Drawing-caravel-M-2-card-QFN/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.7 | 1.6 | 0.3&nbsp;ms | 1.9 | 92&nbsp;ms | 0.4 | 0.2 | 5.2 |
| Simulation, STEP | 0.3 | 0.6 | 1.5 | 0.3&nbsp;ms | 1.9 | 1.6 | 0.4 | 0.2 | 6.4 |
| Simulation, STL | 0.3 | 0.6 | 1.5 | 0.2&nbsp;ms | 2.0 | 0.2 | 0.4 | 0.2 | 5.1 |
| Simulation, OBJ | 0.2 | 0.6 | 1.6 | 0.2&nbsp;ms | 2.1 | 2.5 | 0.4 | 0.2 | 7.6 |
| Visual, GLB | 0.3 | 0.6 | 1.6 | 0.2&nbsp;ms | 5.2 | 67&nbsp;ms | 0.5 | 0.2 | 8.4 |
| Visual, OBJ | 0.3 | 0.6 | 1.5 | 0.3&nbsp;ms | 5.2 | 1.8 | 0.5 | 0.2 | 10.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [chipfoundry/caravel_board](https://github.com/chipfoundry/caravel_board)<br>Board: `Fab-Drawing-caravel-M.2-card-QFN.kicad_pcb` |
|---|---|
| Folder | hardware / breakout / caravel-M.2-card-QFN |
| Complexity | 301&nbsp;/&nbsp;1000 (size&nbsp;211, features&nbsp;90) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 11, 592, 95 |
| Triangles,&nbsp;simulation | 547,288 in 77 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">305&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">85&nbsp;MB</td><td align="right">362&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">27&nbsp;MB</td><td align="right">299&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">56&nbsp;MB</td><td align="right">429&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">368&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">40&nbsp;MB</td><td align="right">369&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [727. caravel-M.2-card-QFN](b0727b_caravel-board_caravel-M-2-card-QFN.md) | [729. caravel-M.2-card-WCSP](b0729b_caravel-board_caravel-M-2-card-WCSP.md) |
