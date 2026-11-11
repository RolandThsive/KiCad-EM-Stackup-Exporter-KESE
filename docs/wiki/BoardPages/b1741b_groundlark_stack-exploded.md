# 1741. stack-exploded

Board 1,741 of the 3,110 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 17](../CorpusTestingPages/Corpus-Testing-17.md#1741-stack-exploded).

![stack-exploded: stages 4 and 6 take 45% to 82% of a run. Simulation, GLB takes 39 s. Simulation, STEP takes 49 s. Simulation, STL takes 40 s. Simulation, OBJ takes 65 s. Visual, GLB takes 71 s. Visual, OBJ takes 87 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1741b_groundlark_stack-exploded/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.1 | 4.9 | 11.7 | 1&nbsp;ms | 17.7 | 0.9 | 2.0 | 0.3 | 38.6 |
| Simulation, STEP | 1.1 | 5.0 | 11.8 | 2&nbsp;ms | 17.6 | 11.2 | 2.0 | 0.3 | 49.1 |
| Simulation, STL | 1.2 | 5.2 | 11.6 | 1&nbsp;ms | 17.3 | 2.0 | 2.1 | 0.3 | 39.8 |
| Simulation, OBJ | 1.2 | 4.5 | 12.3 | 1&nbsp;ms | 17.0 | 27.4 | 2.2 | 0.3 | 64.9 |
| Visual, GLB | 1.2 | 5.4 | 11.7 | 1&nbsp;ms | 47.1 | 0.4 | 5.2 | 0.3 | 71.4 |
| Visual, OBJ | 1.2 | 5.1 | 11.4 | 1&nbsp;ms | 47.7 | 15.4 | 6.4 | 0.3 | 87.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `stack-exploded.kicad_pcb` |
|---|---|
| Folder | hw / groundlark-fpga-hat / boards / groundlark-daqhat-01 |
| Complexity | 417&nbsp;/&nbsp;1000 (size&nbsp;297, features&nbsp;120) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 190, 12,366, 745 |
| Triangles,&nbsp;simulation | 5,819,912 in 381 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">195&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">676&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">291&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">625&nbsp;MB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">106&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">343&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1740. pi-trenz-stack-concept](b1740b_groundlark_pi-trenz-stack-concept.md) | [1742. stack-service-envelopes](b1742b_groundlark_stack-service-envelopes.md) |
