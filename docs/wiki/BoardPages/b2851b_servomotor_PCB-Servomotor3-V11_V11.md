# 2851. V11

Board 2,851 of the 3,103 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 27](../CorpusTestingPages/Corpus-Testing-27.md#2851-v11).

![V11: stages 4 and 6 take 52% to 82% of a run. Simulation, GLB takes 9.8 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.8 s. Simulation, OBJ takes 14 s. Visual, GLB takes 15 s. Visual, OBJ takes 19 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2851b_servomotor_PCB-Servomotor3-V11_V11/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.0 | 3.9 | 0.4&nbsp;ms | 3.5 | 0.2 | 0.6 | 0.2 | 9.8 |
| Simulation, STEP | 0.4 | 1.1 | 4.0 | 0.3&nbsp;ms | 3.7 | 2.6 | 0.5 | 0.2 | 12.5 |
| Simulation, STL | 0.4 | 1.0 | 3.7 | 0.4&nbsp;ms | 3.5 | 0.3 | 0.5 | 0.2 | 9.8 |
| Simulation, OBJ | 0.4 | 1.0 | 3.8 | 0.4&nbsp;ms | 3.6 | 4.8 | 0.5 | 0.2 | 14.4 |
| Visual, GLB | 0.4 | 1.1 | 4.0 | 0.3&nbsp;ms | 8.4 | 0.1 | 0.8 | 0.2 | 15.0 |
| Visual, OBJ | 0.5 | 1.1 | 3.8 | 0.4&nbsp;ms | 8.3 | 4.4 | 1.0 | 0.2 | 19.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [tomrodinger/servomotor](https://github.com/tomrodinger/servomotor)<br>Board: `V11.kicad_pcb` |
|---|---|
| Folder | PCB / Servomotor3 / V11 |
| Complexity | 346&nbsp;/&nbsp;1000 (size&nbsp;221, features&nbsp;125) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 66, 584, 261 |
| Triangles,&nbsp;simulation | 930,538 in 65 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">424&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">146&nbsp;MB</td><td align="right">532&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">47&nbsp;MB</td><td align="right">432&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">94&nbsp;MB</td><td align="right">655&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">563&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">81&nbsp;MB</td><td align="right">639&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2850. V10](b2850b_servomotor_V10.md) | [2852. V11](b2852b_servomotor_PCB-Servomotor3-V11RC1_V11.md) |
