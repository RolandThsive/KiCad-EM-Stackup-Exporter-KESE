# 1265. simpleIO

Board 1,265 of the 3,132 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 12](../CorpusTestingPages/Corpus-Testing-12.md#1265-simpleio).

![simpleIO: stages 4 and 6 take 45% to 81% of a run. Simulation, GLB takes 4.4 s. Simulation, STEP takes 5.9 s. Simulation, STL takes 4.6 s. Simulation, OBJ takes 7.4 s. Visual, GLB takes 7.0 s. Visual, OBJ takes 9.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1265b_Extension-Boards-for-Olimex-GateMate_simpleIO/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 1.4 | 0.3&nbsp;ms | 1.7 | 84&nbsp;ms | 0.3 | 0.2 | 4.4 |
| Simulation, STEP | 0.2 | 0.5 | 1.3 | 0.3&nbsp;ms | 1.8 | 1.6 | 0.3 | 0.2 | 5.9 |
| Simulation, STL | 0.2 | 0.5 | 1.5 | 0.3&nbsp;ms | 1.8 | 0.2 | 0.3 | 0.2 | 4.6 |
| Simulation, OBJ | 0.3 | 0.5 | 1.4 | 0.3&nbsp;ms | 1.9 | 2.7 | 0.3 | 0.2 | 7.4 |
| Visual, GLB | 0.2 | 0.5 | 1.4 | 0.3&nbsp;ms | 4.2 | 55&nbsp;ms | 0.4 | 0.2 | 7.0 |
| Visual, OBJ | 0.3 | 0.5 | 1.4 | 0.2&nbsp;ms | 3.8 | 2.3 | 0.5 | 0.2 | 9.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [intergalaktik/Extension_Boards_for_Olimex_GateMate](https://github.com/intergalaktik/Extension_Boards_for_Olimex_GateMate)<br>Board: `simpleIO.kicad_pcb` |
|---|---|
| Folder | simpleIO / KiCad |
| Complexity | 252&nbsp;/&nbsp;1000 (size&nbsp;177, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 48, 247, 82 |
| Triangles,&nbsp;simulation | 455,592 in 69 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">289&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">63&nbsp;MB</td><td align="right">350&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">23&nbsp;MB</td><td align="right">288&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">46&nbsp;MB</td><td align="right">370&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">365&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">36&nbsp;MB</td><td align="right">345&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1264. pwrIO](b1264b_Extension-Boards-for-Olimex-GateMate_pwrIO.md) | [1266. tmrIO](b1266b_Extension-Boards-for-Olimex-GateMate_tmrIO.md) |
