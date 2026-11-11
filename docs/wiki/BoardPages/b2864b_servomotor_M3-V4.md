# 2864. M3-V4

Board 2,864 of the 3,110 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 27](../CorpusTestingPages/Corpus-Testing-27.md#2864-m3-v4).

![M3-V4: stages 4 and 6 take 51% to 81% of a run. Simulation, GLB takes 8.9 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.4 s. Simulation, OBJ takes 13 s. Visual, GLB takes 13 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2864b_servomotor_M3-V4/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 0.8 | 3.0 | 0.2&nbsp;ms | 3.8 | 0.1 | 0.5 | 0.2 | 8.9 |
| Simulation, STEP | 0.4 | 0.8 | 2.9 | 0.2&nbsp;ms | 3.8 | 3.0 | 0.4 | 0.2 | 11.5 |
| Simulation, STL | 0.4 | 0.9 | 3.2 | 0.2&nbsp;ms | 3.8 | 0.2 | 0.5 | 0.3 | 9.4 |
| Simulation, OBJ | 0.4 | 0.9 | 3.0 | 0.4&nbsp;ms | 3.8 | 4.6 | 0.5 | 0.2 | 13.3 |
| Visual, GLB | 0.4 | 0.8 | 2.9 | 0.3&nbsp;ms | 7.4 | 0.1 | 0.8 | 0.2 | 12.7 |
| Visual, OBJ | 0.4 | 0.9 | 2.9 | 0.3&nbsp;ms | 7.2 | 4.0 | 0.8 | 0.2 | 16.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [tomrodinger/servomotor](https://github.com/tomrodinger/servomotor)<br>Board: `M3-V4.kicad_pcb` |
|---|---|
| Folder | PCB / Servomotor3 / V4 |
| Complexity | 347&nbsp;/&nbsp;1000 (size&nbsp;222, features&nbsp;125) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 65, 1,027, 159 |
| Triangles,&nbsp;simulation | 872,928 in 62 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">462&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">158&nbsp;MB</td><td align="right">528&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">44&nbsp;MB</td><td align="right">451&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">89&nbsp;MB</td><td align="right">620&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">654&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">80&nbsp;MB</td><td align="right">641&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2863. servomotorStepper-V2I1](b2863b_servomotor_servomotorStepper-V2I1.md) | [2865. M3-V5](b2865b_servomotor_M3-V5.md) |
