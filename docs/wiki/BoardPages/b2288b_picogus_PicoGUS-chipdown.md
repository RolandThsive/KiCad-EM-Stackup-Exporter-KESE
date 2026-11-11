# 2288. PicoGUS chipdown

Board 2,288 of the 3,126 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 22](../CorpusTestingPages/Corpus-Testing-22.md#2288-picogus-chipdown).

![PicoGUS chipdown: stages 4 and 6 take 44% to 78% of a run. Simulation, GLB takes 31 s. Simulation, STEP takes 40 s. Simulation, STL takes 32 s. Simulation, OBJ takes 53 s. Visual, GLB takes 56 s. Visual, OBJ takes 71 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2288b_picogus_PicoGUS-chipdown/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.5 | 4.2 | 10.8 | 0.7&nbsp;ms | 11.2 | 0.6 | 1.4 | 0.3 | 31.0 |
| Simulation, STEP | 2.6 | 4.2 | 10.5 | 0.7&nbsp;ms | 11.4 | 9.6 | 1.4 | 0.3 | 39.9 |
| Simulation, STL | 2.6 | 4.1 | 10.8 | 0.7&nbsp;ms | 12.1 | 1.2 | 1.4 | 0.3 | 32.5 |
| Simulation, OBJ | 2.7 | 4.2 | 11.3 | 1&nbsp;ms | 11.7 | 21.0 | 1.4 | 0.3 | 52.6 |
| Visual, GLB | 2.6 | 4.1 | 10.9 | 0.7&nbsp;ms | 32.5 | 0.5 | 4.9 | 0.3 | 55.7 |
| Visual, OBJ | 2.6 | 4.2 | 10.8 | 0.7&nbsp;ms | 32.9 | 15.8 | 4.6 | 0.3 | 71.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [polpo/picogus](https://github.com/polpo/picogus)<br>Board: `PicoGUS chipdown.kicad_pcb` |
|---|---|
| Folder | hw-chipdown |
| Complexity | 396&nbsp;/&nbsp;1000 (size&nbsp;251, features&nbsp;145) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 96, 1,334, 374 |
| Triangles,&nbsp;simulation | 3,281,176 in 178 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">114&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">367&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">164&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">357&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">86&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">272&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2287. PicoGUS chipdown with edge rails](b2287b_picogus_PicoGUS-chipdown-with-edge-rails.md) | [2289. PicoGUS Hand386](b2289b_picogus_PicoGUS-Hand386.md) |
