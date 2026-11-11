# 1108. edelweiss

Board 1,108 of the 3,131 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 11](../CorpusTestingPages/Corpus-Testing-11.md#1108-edelweiss).

![edelweiss: stages 4 and 6 take 53% to 83% of a run. Simulation, GLB takes 6.8 s. Simulation, STEP takes 8.5 s. Simulation, STL takes 6.8 s. Simulation, OBJ takes 11 s. Visual, GLB takes 7.7 s. Visual, OBJ takes 8.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1108b_greatfet-hardware_edelweiss/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.5 | 3.1 | 0.1&nbsp;ms | 2.5 | 98&nbsp;ms | 0.3 | 0.2 | 6.8 |
| Simulation, STEP | 0.1 | 0.5 | 3.2 | 0.2&nbsp;ms | 2.1 | 2.0 | 0.3 | 0.2 | 8.5 |
| Simulation, STL | 0.2 | 0.5 | 3.2 | 0.3&nbsp;ms | 2.3 | 0.2 | 0.3 | 0.3 | 6.8 |
| Simulation, OBJ | 0.1 | 0.5 | 3.2 | 0.1&nbsp;ms | 2.5 | 3.9 | 0.3 | 0.3 | 10.8 |
| Visual, GLB | 0.2 | 0.6 | 3.3 | 0.3&nbsp;ms | 3.0 | 43&nbsp;ms | 0.3 | 0.2 | 7.7 |
| Visual, OBJ | 0.2 | 0.5 | 2.9 | 0.4&nbsp;ms | 3.0 | 1.4 | 0.4 | 0.2 | 8.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [greatscottgadgets/greatfet-hardware](https://github.com/greatscottgadgets/greatfet-hardware)<br>Board: `edelweiss.kicad_pcb` |
|---|---|
| Folder | edelweiss |
| Complexity | 96&nbsp;/&nbsp;1000 (size&nbsp;56, features&nbsp;40) |
| KESE&nbsp;features | filled zones, copper text,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 7, 0, 0 |
| Triangles,&nbsp;simulation | 829,404 in 16 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">371&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">99&nbsp;MB</td><td align="right">443&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">41&nbsp;MB</td><td align="right">376&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">83&nbsp;MB</td><td align="right">591&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">10&nbsp;MB</td><td align="right">362&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">30&nbsp;MB</td><td align="right">360&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1107. daffodil](b1107b_greatfet-hardware_daffodil.md) | [1109. foxglove](b1109b_greatfet-hardware_foxglove.md) |
