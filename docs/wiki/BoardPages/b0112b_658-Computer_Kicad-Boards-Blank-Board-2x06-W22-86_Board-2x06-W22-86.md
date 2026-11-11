# 112. Board 2x06 W22.86

Board 112 of the 3,100 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 2](../CorpusTestingPages/Corpus-Testing-02.md#112-board-2x06-w2286).

![Board 2x06 W22.86: stages 4 and 6 take 40% to 65% of a run. Simulation, GLB takes 1.3 s. Simulation, STEP takes 2.3 s. Simulation, STL takes 1.5 s. Simulation, OBJ takes 2.0 s. Visual, GLB takes 1.6 s. Visual, OBJ takes 1.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0112b_658-Computer_Kicad-Boards-Blank-Board-2x06-W22-86_Board-2x06-W22-86/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 88&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.5 | 12&nbsp;ms | 41&nbsp;ms | 0.3 | 1.3 |
| Simulation, STEP | 0.1 | 88&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.6 | 0.9 | 60&nbsp;ms | 0.2 | 2.3 |
| Simulation, STL | 0.1 | 97&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.7 | 22&nbsp;ms | 60&nbsp;ms | 0.2 | 1.5 |
| Simulation, OBJ | 78&nbsp;ms | 76&nbsp;ms | 0.3 | 0.2&nbsp;ms | 0.7 | 0.6 | 45&nbsp;ms | 0.2 | 2.0 |
| Visual, GLB | 0.1 | 90&nbsp;ms | 0.3 | 0.4&nbsp;ms | 0.7 | 8&nbsp;ms | 61&nbsp;ms | 0.3 | 1.6 |
| Visual, OBJ | 0.1 | 92&nbsp;ms | 0.3 | 0.2&nbsp;ms | 0.7 | 0.3 | 58&nbsp;ms | 0.2 | 1.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [andrewpaterson/658-Computer](https://github.com/andrewpaterson/658-Computer)<br>Board: `Board 2x06 W22.86.kicad_pcb` |
|---|---|
| Folder | Kicad / Boards / Blank / Board 2x06 W22.86 |
| Complexity | 89&nbsp;/&nbsp;1000 (size&nbsp;34, features&nbsp;55) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 4, 0, 0 |
| Triangles,&nbsp;simulation | 61,696 in 24 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">2.0&nbsp;MB</td><td align="right">70&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">6.6&nbsp;MB</td><td align="right">171&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">3.1&nbsp;MB</td><td align="right">71&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">5.9&nbsp;MB</td><td align="right">94&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">1.3&nbsp;MB</td><td align="right">105&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.7&nbsp;MB</td><td align="right">104&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [111. Board 2x06 W15.24](b0111b_658-Computer_Kicad-Boards-Blank-Board-2x06-W15-24_Board-2x06-W15-24.md) | [113. Board 2x12 W15.24](b0113b_658-Computer_Kicad-Boards-Blank-Board-2x12-W15-24_Board-2x12-W15-24.md) |
