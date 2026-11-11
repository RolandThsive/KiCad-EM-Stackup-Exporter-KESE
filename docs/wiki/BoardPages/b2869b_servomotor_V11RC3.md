# 2869. V11RC3

Board 2,869 of the 3,118 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 27](../CorpusTestingPages/Corpus-Testing-27.md#2869-v11rc3).

![V11RC3: stages 4 and 6 take 53% to 81% of a run. Simulation, GLB takes 9.9 s. Simulation, STEP takes 12 s. Simulation, STL takes 10 s. Simulation, OBJ takes 14 s. Visual, GLB takes 15 s. Visual, OBJ takes 19 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2869b_servomotor_V11RC3/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.0 | 3.9 | 0.7&nbsp;ms | 3.6 | 0.2 | 0.5 | 0.2 | 9.9 |
| Simulation, STEP | 0.3 | 1.1 | 3.5 | 0.3&nbsp;ms | 3.7 | 2.7 | 0.6 | 0.3 | 12.2 |
| Simulation, STL | 0.4 | 1.0 | 4.1 | 0.4&nbsp;ms | 3.6 | 0.3 | 0.6 | 0.3 | 10.3 |
| Simulation, OBJ | 0.3 | 1.0 | 3.7 | 0.3&nbsp;ms | 3.5 | 4.4 | 0.6 | 0.2 | 13.7 |
| Visual, GLB | 0.4 | 0.9 | 3.8 | 0.4&nbsp;ms | 8.4 | 0.1 | 1.2 | 0.3 | 15.0 |
| Visual, OBJ | 0.4 | 1.0 | 3.9 | 0.4&nbsp;ms | 8.4 | 3.8 | 1.3 | 0.2 | 19.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [tomrodinger/servomotor](https://github.com/tomrodinger/servomotor)<br>Board: `V11RC3.kicad_pcb` |
|---|---|
| Folder | PCB / Servomotor3 / V11RC3 |
| Complexity | 345&nbsp;/&nbsp;1000 (size&nbsp;220, features&nbsp;125) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 64, 525, 264 |
| Triangles,&nbsp;simulation | 875,720 in 61 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">406&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">134&nbsp;MB</td><td align="right">492&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">44&nbsp;MB</td><td align="right">402&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">89&nbsp;MB</td><td align="right">614&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">25&nbsp;MB</td><td align="right">590&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">76&nbsp;MB</td><td align="right">608&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2868. V11RC2](b2868b_servomotor_V11RC2.md) | [2870. V11RC4](b2870b_servomotor_V11RC4.md) |
