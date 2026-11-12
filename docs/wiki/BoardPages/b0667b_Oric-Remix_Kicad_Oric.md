# 667. Oric

Board 667 of the 3,132 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 7](../CorpusTestingPages/Corpus-Testing-07.md#667-oric).

![Oric: stages 4 and 6 take 53% to 85% of a run. Simulation, GLB takes 42 s. Simulation, STEP takes 55 s. Simulation, STL takes 46 s. Simulation, OBJ takes 65 s. Visual, GLB takes 65 s. Visual, OBJ takes 80 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0667b_Oric-Remix_Kicad_Oric/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 3.8 | 19.7 | 0.9&nbsp;ms | 15.1 | 0.6 | 2.4 | 0.3 | 42.4 |
| Simulation, STEP | 0.7 | 3.6 | 20.2 | 1&nbsp;ms | 15.6 | 11.6 | 2.7 | 0.3 | 54.8 |
| Simulation, STL | 0.7 | 3.8 | 20.8 | 2&nbsp;ms | 16.1 | 1.6 | 2.6 | 0.3 | 45.7 |
| Simulation, OBJ | 0.6 | 3.7 | 19.2 | 0.9&nbsp;ms | 15.4 | 23.7 | 2.6 | 0.3 | 65.5 |
| Visual, GLB | 0.7 | 3.8 | 20.5 | 2&nbsp;ms | 34.5 | 0.4 | 4.4 | 0.3 | 64.6 |
| Visual, OBJ | 0.7 | 3.9 | 20.8 | 1&nbsp;ms | 34.6 | 15.2 | 4.8 | 0.3 | 80.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Oric-Remix](https://github.com/Board-Folk/Oric-Remix)<br>Board: `Oric.kicad_pcb` |
|---|---|
| Folder | Kicad |
| Complexity | 268&nbsp;/&nbsp;1000 (size&nbsp;203, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 129, 2,832, 234 |
| Triangles,&nbsp;simulation | 4,065,754 in 203 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">137&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">568&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">203&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">426&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">87&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">275&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [666. Oric-PS2USB](b0666b_Oric-Remix_Oric-PS2USB.md) | [668. PCE](b0668b_PC-Engine_PCE.md) |
