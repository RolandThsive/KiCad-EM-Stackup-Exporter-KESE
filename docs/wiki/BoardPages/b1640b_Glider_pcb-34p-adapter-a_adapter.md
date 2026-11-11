# 1640. adapter

Board 1,640 of the 3,102 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 16](../CorpusTestingPages/Corpus-Testing-16.md#1640-adapter).

![adapter: stages 4 and 6 take 47% to 70% of a run. Simulation, GLB takes 3.2 s. Simulation, STEP takes 4.5 s. Simulation, STL takes 3.3 s. Simulation, OBJ takes 4.2 s. Visual, GLB takes 4.1 s. Visual, OBJ takes 5.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1640b_Glider_pcb-34p-adapter-a_adapter/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 0.3 | 0.8 | 0.4&nbsp;ms | 1.2 | 38&nbsp;ms | 0.2 | 0.2 | 3.2 |
| Simulation, STEP | 0.5 | 0.3 | 0.9 | 0.2&nbsp;ms | 1.2 | 1.3 | 0.1 | 0.2 | 4.5 |
| Simulation, STL | 0.5 | 0.3 | 0.8 | 0.3&nbsp;ms | 1.2 | 66&nbsp;ms | 0.1 | 0.3 | 3.3 |
| Simulation, OBJ | 0.5 | 0.3 | 0.8 | 0.2&nbsp;ms | 1.2 | 1.1 | 0.1 | 0.2 | 4.2 |
| Visual, GLB | 0.5 | 0.3 | 0.8 | 0.2&nbsp;ms | 2.1 | 29&nbsp;ms | 0.2 | 0.2 | 4.1 |
| Visual, OBJ | 0.5 | 0.3 | 0.8 | 0.3&nbsp;ms | 2.2 | 0.9 | 0.2 | 0.2 | 5.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Modos-Labs/Glider](https://github.com/Modos-Labs/Glider)<br>Board: `adapter.kicad_pcb` |
|---|---|
| Folder | pcb / 34p-adapter-a |
| Complexity | 214&nbsp;/&nbsp;1000 (size&nbsp;139, features&nbsp;75) |
| KESE&nbsp;features | through vias, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 6, 255, 74 |
| Triangles,&nbsp;simulation | 197,086 in 71 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">6.9&nbsp;MB</td><td align="right">231&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">32&nbsp;MB</td><td align="right">256&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">9.9&nbsp;MB</td><td align="right">232&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">20&nbsp;MB</td><td align="right">232&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.8&nbsp;MB</td><td align="right">226&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">17&nbsp;MB</td><td align="right">227&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1639. videoslot](b1639b_amiga2000-gfxcard_videoslot.md) | [1641. adapter](b1641b_Glider_pcb-34p-adapter-b_adapter.md) |
