# 821. 7-REV0

Board 821 of the 3,118 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 8](../CorpusTestingPages/Corpus-Testing-08.md#821-7-rev0).

![7-REV0: stages 4 and 6 take 52% to 83% of a run. Simulation, GLB takes 28 s. Simulation, STEP takes 34 s. Simulation, STL takes 27 s. Simulation, OBJ takes 42 s. Visual, GLB takes 39 s. Visual, OBJ takes 48 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0821b_BusPirate5-hardware_7-REV0/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 2.7 | 10.0 | 0.6&nbsp;ms | 12.2 | 0.5 | 1.1 | 0.2 | 27.5 |
| Simulation, STEP | 0.8 | 2.8 | 9.8 | 0.9&nbsp;ms | 12.1 | 7.3 | 1.1 | 0.2 | 34.2 |
| Simulation, STL | 0.8 | 2.8 | 9.5 | 0.5&nbsp;ms | 11.5 | 0.9 | 1.2 | 0.3 | 27.0 |
| Simulation, OBJ | 0.8 | 2.8 | 9.9 | 0.8&nbsp;ms | 12.3 | 15.4 | 1.1 | 0.3 | 42.5 |
| Visual, GLB | 0.7 | 2.9 | 10.0 | 0.8&nbsp;ms | 22.0 | 0.3 | 2.5 | 0.2 | 38.6 |
| Visual, OBJ | 0.7 | 2.8 | 9.4 | 0.7&nbsp;ms | 21.3 | 10.6 | 2.9 | 0.2 | 48.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [DangerousPrototypes/BusPirate5-hardware](https://github.com/DangerousPrototypes/BusPirate5-hardware)<br>Board: `7-REV0.kicad_pcb` |
|---|---|
| Folder | bus_pirate_pcb / development / 7-REV0A-prototype-1 |
| Complexity | 390&nbsp;/&nbsp;1000 (size&nbsp;270, features&nbsp;120) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 241, 2,812, 465 |
| Triangles,&nbsp;simulation | 2,913,992 in 247 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">99&nbsp;MB</td><td align="right">993&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">404&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">146&nbsp;MB</td><td align="right">970&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">308&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">70&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">220&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [820. BusPirate-5-rev10](b0820b_BusPirate5-hardware_BusPirate-5-rev10.md) | [822. 7-REV1-freeze](b0822b_BusPirate5-hardware_7-REV1-freeze.md) |
