# 1346. MIDAS-MK1.1

Board 1,346 of the 3,139 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 13](../CorpusTestingPages/Corpus-Testing-13.md#1346-midas-mk11).

![MIDAS-MK1.1: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 24 s. Simulation, STEP takes 31 s. Simulation, STL takes 24 s. Simulation, OBJ takes 37 s. Visual, GLB takes 42 s. Visual, OBJ takes 50 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1346b_iss-pcb_boards-MIDAS-MK1-MIDAS-MK1-1-revB_MIDAS-MK1-1/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 2.3 | 8.6 | 1&nbsp;ms | 10.4 | 0.4 | 1.2 | 0.3 | 24.1 |
| Simulation, STEP | 0.9 | 2.3 | 8.7 | 2&nbsp;ms | 10.2 | 7.4 | 1.2 | 0.3 | 31.0 |
| Simulation, STL | 0.8 | 2.3 | 8.5 | 1&nbsp;ms | 10.3 | 0.9 | 1.2 | 0.3 | 24.3 |
| Simulation, OBJ | 0.7 | 2.4 | 8.2 | 2&nbsp;ms | 10.5 | 14.0 | 1.2 | 0.3 | 37.3 |
| Visual, GLB | 0.9 | 2.6 | 8.7 | 1&nbsp;ms | 26.1 | 0.4 | 2.9 | 0.2 | 41.7 |
| Visual, OBJ | 0.9 | 2.4 | 9.0 | 1&nbsp;ms | 24.4 | 9.6 | 3.3 | 0.3 | 49.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [issuiuc/iss-pcb](https://github.com/issuiuc/iss-pcb)<br>Board: `MIDAS-MK1.1.kicad_pcb` |
|---|---|
| Folder | boards / MIDAS-MK1 / MIDAS-MK1.1-revB |
| Complexity | 413&nbsp;/&nbsp;1000 (size&nbsp;273, features&nbsp;140) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 203, 1,158, 279 |
| Triangles,&nbsp;simulation | 2,779,476 in 343 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">95&nbsp;MB</td><td align="right">895&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">416&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">139&nbsp;MB</td><td align="right">924&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">294&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">65&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">205&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1345. MIDAS-MK1.1](b1345b_iss-pcb_boards-MIDAS-MK1-MIDAS-MK1-1-revA_MIDAS-MK1-1.md) | [1347. MIDAS-MK2](b1347b_iss-pcb_MIDAS-MK2.md) |
