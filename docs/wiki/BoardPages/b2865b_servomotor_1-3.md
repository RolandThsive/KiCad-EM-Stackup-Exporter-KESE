# 2865. 1.3

Board 2,865 of the 3,120 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 27](../CorpusTestingPages/Corpus-Testing-27.md#2865-13).

![1.3: stages 4 and 6 take 52% to 83% of a run. Simulation, GLB takes 9.8 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.3 s. Simulation, OBJ takes 14 s. Visual, GLB takes 15 s. Visual, OBJ takes 19 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2865b_servomotor_1-3/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.0 | 3.8 | 0.4&nbsp;ms | 3.5 | 0.2 | 0.5 | 0.3 | 9.8 |
| Simulation, STEP | 0.4 | 1.1 | 3.8 | 0.5&nbsp;ms | 3.4 | 2.5 | 0.5 | 0.2 | 12.0 |
| Simulation, STL | 0.4 | 1.1 | 3.5 | 0.4&nbsp;ms | 3.2 | 0.3 | 0.5 | 0.2 | 9.3 |
| Simulation, OBJ | 0.4 | 0.9 | 3.9 | 0.2&nbsp;ms | 3.5 | 4.6 | 0.6 | 0.2 | 14.1 |
| Visual, GLB | 0.4 | 0.9 | 3.6 | 0.4&nbsp;ms | 9.0 | 0.1 | 1.0 | 0.2 | 15.3 |
| Visual, OBJ | 0.5 | 1.0 | 3.7 | 0.6&nbsp;ms | 9.2 | 3.3 | 1.3 | 0.3 | 19.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [tomrodinger/servomotor](https://github.com/tomrodinger/servomotor)<br>Board: `1.3.kicad_pcb` |
|---|---|
| Folder | PCB / Servomotor3 / 1.3 |
| Complexity | 348&nbsp;/&nbsp;1000 (size&nbsp;223, features&nbsp;125) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 75, 544, 308 |
| Triangles,&nbsp;simulation | 956,536 in 65 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">33&nbsp;MB</td><td align="right">488&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">142&nbsp;MB</td><td align="right">549&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">48&nbsp;MB</td><td align="right">493&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">97&nbsp;MB</td><td align="right">681&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">653&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">83&nbsp;MB</td><td align="right">663&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2864. 1.2](b2864b_servomotor_1-2.md) | [2866. 1.5](b2866b_servomotor_1-5.md) |
