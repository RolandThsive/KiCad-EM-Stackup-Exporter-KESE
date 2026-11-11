# 1075. econet_standalone

Board 1,075 of the 3,139 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 10](../CorpusTestingPages/Corpus-Testing-10.md#1075-econet_standalone).

![econet_standalone: stages 4 and 6 take 52% to 81% of a run. Simulation, GLB takes 6.9 s. Simulation, STEP takes 8.9 s. Simulation, STL takes 6.9 s. Simulation, OBJ takes 9.5 s. Visual, GLB takes 9.9 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1075b_myelin-acorn-electron-hardware_econet-standalone/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 2.7 | 0.4&nbsp;ms | 2.5 | 98&nbsp;ms | 0.4 | 0.3 | 6.9 |
| Simulation, STEP | 0.2 | 0.7 | 2.6 | 0.6&nbsp;ms | 2.5 | 2.3 | 0.4 | 0.3 | 8.9 |
| Simulation, STL | 0.2 | 0.7 | 2.6 | 0.5&nbsp;ms | 2.6 | 0.2 | 0.4 | 0.2 | 6.9 |
| Simulation, OBJ | 0.2 | 0.6 | 2.5 | 0.4&nbsp;ms | 2.4 | 3.1 | 0.4 | 0.2 | 9.5 |
| Visual, GLB | 0.2 | 0.6 | 2.6 | 0.3&nbsp;ms | 5.5 | 0.1 | 0.7 | 0.2 | 9.9 |
| Visual, OBJ | 0.2 | 0.7 | 2.4 | 0.4&nbsp;ms | 5.1 | 3.0 | 0.8 | 0.2 | 12.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [google/myelin-acorn-electron-hardware](https://github.com/google/myelin-acorn-electron-hardware)<br>Board: `econet_standalone.kicad_pcb` |
|---|---|
| Folder | econet_from_scratch / pcb |
| Complexity | 249&nbsp;/&nbsp;1000 (size&nbsp;204, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 42, 614, 22 |
| Triangles,&nbsp;simulation | 583,200 in 75 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">322&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">104&nbsp;MB</td><td align="right">406&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">29&nbsp;MB</td><td align="right">321&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">59&nbsp;MB</td><td align="right">433&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">442&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">52&nbsp;MB</td><td align="right">475&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1074. cpu_socket_minispartan_daughterboard](b1074b_myelin-acorn-electron-hardware_cpu-socket-minispartan-daughterboard.md) | [1076. econet_hub](b1076b_myelin-acorn-electron-hardware_econet-hub.md) |
