# 507. gd power supply board pcb

Board 507 of the 3,131 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 5](../CorpusTestingPages/Corpus-Testing-05.md#507-gd-power-supply-board-pcb).

![gd power supply board pcb: stages 4 and 6 take 50% to 77% of a run. Simulation, GLB takes 5.5 s. Simulation, STEP takes 7.9 s. Simulation, STL takes 5.7 s. Simulation, OBJ takes 8.1 s. Visual, GLB takes 9.7 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0507b_Mega-IIe_kicad-files-gd-power-supply-board-pcb-gd-ps-rev1_gd-power-supply-board-pcb/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 0.5 | 2.1 | 0.4&nbsp;ms | 1.9 | 0.1 | 0.3 | 0.2 | 5.5 |
| Simulation, STEP | 0.3 | 0.6 | 2.3 | 0.3&nbsp;ms | 2.1 | 2.1 | 0.3 | 0.2 | 7.9 |
| Simulation, STL | 0.4 | 0.6 | 2.2 | 0.3&nbsp;ms | 1.8 | 0.2 | 0.3 | 0.3 | 5.7 |
| Simulation, OBJ | 0.5 | 0.7 | 2.3 | 1.0&nbsp;ms | 1.7 | 2.5 | 0.2 | 0.3 | 8.1 |
| Visual, GLB | 0.5 | 0.6 | 2.3 | 0.4&nbsp;ms | 5.1 | 70&nbsp;ms | 0.7 | 0.3 | 9.7 |
| Visual, OBJ | 0.3 | 0.6 | 2.6 | 0.3&nbsp;ms | 5.1 | 2.2 | 0.9 | 0.3 | 12.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [baldengineer/Mega-IIe](https://github.com/baldengineer/Mega-IIe)<br>Board: `gd power supply board pcb.kicad_pcb` |
|---|---|
| Folder | kicad files / gd power supply board pcb / gd ps rev1 |
| Complexity | 313&nbsp;/&nbsp;1000 (size&nbsp;158, features&nbsp;155) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 73, 144, 61 |
| Triangles,&nbsp;simulation | 509,766 in 55 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">350&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">101&nbsp;MB</td><td align="right">380&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">25&nbsp;MB</td><td align="right">321&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">53&nbsp;MB</td><td align="right">402&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">397&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">44&nbsp;MB</td><td align="right">397&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [506. gd power supply board pcb](b0506b_Mega-IIe_kicad-files-gd-power-supply-board-pcb_gd-power-supply-board-pcb.md) | [508. proto socket adapter](b0508b_Mega-IIe_proto-socket-adapter.md) |
