# 2878. V11RC4

Board 2,878 of the 3,126 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 27](../CorpusTestingPages/Corpus-Testing-27.md#2878-v11rc4).

![V11RC4: stages 4 and 6 take 52% to 80% of a run. Simulation, GLB takes 8.8 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.6 s. Simulation, OBJ takes 13 s. Visual, GLB takes 14 s. Visual, OBJ takes 18 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2878b_servomotor_V11RC4/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.9 | 3.4 | 0.6&nbsp;ms | 3.3 | 0.1 | 0.5 | 0.3 | 8.8 |
| Simulation, STEP | 0.3 | 0.9 | 3.7 | 0.4&nbsp;ms | 3.5 | 2.6 | 0.4 | 0.2 | 11.7 |
| Simulation, STL | 0.3 | 1.0 | 3.7 | 0.5&nbsp;ms | 3.6 | 0.3 | 0.5 | 0.2 | 9.6 |
| Simulation, OBJ | 0.3 | 0.9 | 3.3 | 0.7&nbsp;ms | 3.5 | 4.2 | 0.5 | 0.2 | 12.9 |
| Visual, GLB | 0.3 | 0.9 | 3.3 | 0.5&nbsp;ms | 7.7 | 0.1 | 1.1 | 0.3 | 13.7 |
| Visual, OBJ | 0.3 | 0.9 | 3.3 | 0.7&nbsp;ms | 8.1 | 3.9 | 1.2 | 0.3 | 18.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [tomrodinger/servomotor](https://github.com/tomrodinger/servomotor)<br>Board: `V11RC4.kicad_pcb` |
|---|---|
| Folder | PCB / Servomotor3 / V11RC4 |
| Complexity | 346&nbsp;/&nbsp;1000 (size&nbsp;221, features&nbsp;125) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 66, 584, 261 |
| Triangles,&nbsp;simulation | 899,412 in 65 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">404&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">140&nbsp;MB</td><td align="right">529&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">45&nbsp;MB</td><td align="right">419&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">91&nbsp;MB</td><td align="right">630&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">564&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">78&nbsp;MB</td><td align="right">634&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2877. V11RC3](b2877b_servomotor_V11RC3.md) | [2879. servomotorStepper-V2I1](b2879b_servomotor_servomotorStepper-V2I1.md) |
