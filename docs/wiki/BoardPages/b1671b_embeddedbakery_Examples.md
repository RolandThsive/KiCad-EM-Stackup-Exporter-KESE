# 1671. Examples

Board 1,671 of the 3,105 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 16](../CorpusTestingPages/Corpus-Testing-16.md#1671-examples).

![Examples: stages 4 and 6 take 55% to 81% of a run. Simulation, GLB takes 5.1 s. Simulation, STEP takes 6.8 s. Simulation, STL takes 5.2 s. Simulation, OBJ takes 7.8 s. Visual, GLB takes 6.2 s. Visual, OBJ takes 7.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1671b_embeddedbakery_Examples/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 2.1 | 0.5&nbsp;ms | 1.8 | 69&nbsp;ms | 0.2 | 0.2 | 5.1 |
| Simulation, STEP | 0.2 | 0.4 | 2.3 | 0.3&nbsp;ms | 1.9 | 1.6 | 0.2 | 0.2 | 6.8 |
| Simulation, STL | 0.2 | 0.4 | 2.2 | 0.4&nbsp;ms | 1.8 | 0.1 | 0.2 | 0.3 | 5.2 |
| Simulation, OBJ | 0.2 | 0.5 | 2.4 | 0.2&nbsp;ms | 1.9 | 2.4 | 0.2 | 0.2 | 7.8 |
| Visual, GLB | 0.2 | 0.4 | 2.1 | 0.3&nbsp;ms | 2.8 | 41&nbsp;ms | 0.3 | 0.2 | 6.2 |
| Visual, OBJ | 0.2 | 0.4 | 2.2 | 0.3&nbsp;ms | 2.8 | 1.7 | 0.3 | 0.2 | 7.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Examples.kicad_pcb` |
|---|---|
| Folder | circuits / DiodeLogicBoards / Examples |
| Complexity | 57&nbsp;/&nbsp;1000 (size&nbsp;57, features&nbsp;0) |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 41, 0, 0 |
| Triangles,&nbsp;simulation | 446,392 in 31 parts |
| Note | mostly unrouted |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">264&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">48&nbsp;MB</td><td align="right">314&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">22&nbsp;MB</td><td align="right">262&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">45&nbsp;MB</td><td align="right">340&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.6&nbsp;MB</td><td align="right">303&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">25&nbsp;MB</td><td align="right">301&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1670. Digital Logic Board](b1670b_embeddedbakery_Digital-Logic-Board.md) | [1672. PROM](b1672b_embeddedbakery_PROM.md) |
