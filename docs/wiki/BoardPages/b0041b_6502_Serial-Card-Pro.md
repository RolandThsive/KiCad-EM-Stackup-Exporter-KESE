# 41. Serial Card Pro

Board 41 of the 3,117 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 1](../CorpusTestingPages/Corpus-Testing-01.md#41-serial-card-pro).

![Serial Card Pro: stages 4 and 6 take 54% to 82% of a run. Simulation, GLB takes 9.6 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.8 s. Simulation, OBJ takes 14 s. Visual, GLB takes 14 s. Visual, OBJ takes 17 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0041b_6502_Serial-Card-Pro/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.9 | 3.9 | 0.5&nbsp;ms | 3.6 | 0.1 | 0.5 | 0.3 | 9.6 |
| Simulation, STEP | 0.3 | 0.8 | 3.7 | 1.0&nbsp;ms | 3.5 | 3.0 | 0.6 | 0.2 | 12.2 |
| Simulation, STL | 0.3 | 0.8 | 3.9 | 0.7&nbsp;ms | 3.6 | 0.4 | 0.5 | 0.2 | 9.8 |
| Simulation, OBJ | 0.3 | 0.8 | 3.8 | 0.6&nbsp;ms | 3.6 | 4.3 | 0.5 | 0.3 | 13.7 |
| Visual, GLB | 0.3 | 0.8 | 3.8 | 0.5&nbsp;ms | 7.6 | 0.1 | 1.0 | 0.2 | 13.8 |
| Visual, OBJ | 0.3 | 0.8 | 3.5 | 0.6&nbsp;ms | 7.7 | 3.2 | 1.0 | 0.3 | 16.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [acwright/6502](https://github.com/acwright/6502)<br>Board: `Serial Card Pro.kicad_pcb` |
|---|---|
| Folder | Hardware / Serial Card Pro / Rev 1.0 |
| Complexity | 242&nbsp;/&nbsp;1000 (size&nbsp;162, features&nbsp;80) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 27, 435, 112 |
| Triangles,&nbsp;simulation | 922,114 in 94 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">442&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">146&nbsp;MB</td><td align="right">549&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">46&nbsp;MB</td><td align="right">444&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">93&nbsp;MB</td><td align="right">640&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">590&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">71&nbsp;MB</td><td align="right">580&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [40. RTC Card](b0040b_6502_RTC-Card.md) | [42. Serial Card](b0042b_6502_Serial-Card.md) |
