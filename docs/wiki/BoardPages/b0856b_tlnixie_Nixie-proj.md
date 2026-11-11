# 856. Nixie_proj

Board 856 of the 3,111 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 8](../CorpusTestingPages/Corpus-Testing-08.md#856-nixie_proj).

![Nixie_proj: stages 4 and 6 take 53% to 82% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 14 s. Simulation, STL takes 11 s. Simulation, OBJ takes 16 s. Visual, GLB takes 17 s. Visual, OBJ takes 21 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0856b_tlnixie_Nixie-proj/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.1 | 4.0 | 0.8&nbsp;ms | 4.2 | 0.2 | 0.5 | 0.2 | 10.6 |
| Simulation, STEP | 0.4 | 1.0 | 4.0 | 0.7&nbsp;ms | 4.5 | 3.1 | 0.5 | 0.2 | 13.6 |
| Simulation, STL | 0.4 | 1.1 | 4.1 | 0.7&nbsp;ms | 4.7 | 0.3 | 0.5 | 0.2 | 11.3 |
| Simulation, OBJ | 0.3 | 1.0 | 4.2 | 0.8&nbsp;ms | 4.3 | 5.4 | 0.5 | 0.2 | 16.0 |
| Visual, GLB | 0.3 | 1.1 | 4.1 | 0.7&nbsp;ms | 9.7 | 0.1 | 1.2 | 0.2 | 16.7 |
| Visual, OBJ | 0.4 | 1.0 | 4.0 | 0.9&nbsp;ms | 9.7 | 4.1 | 1.5 | 0.2 | 20.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [dm2lct/tlnixie](https://github.com/dm2lct/tlnixie)<br>Board: `Nixie_proj.kicad_pcb` |
|---|---|
| Complexity | 300&nbsp;/&nbsp;1000 (size&nbsp;235, features&nbsp;65) |
| KESE&nbsp;features | through vias, drill offsets,<br>filled zones, copper text,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 109, 1,235, 117 |
| Triangles,&nbsp;simulation | 1,284,986 in 121 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">503&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">218&nbsp;MB</td><td align="right">640&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">64&nbsp;MB</td><td align="right">508&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">133&nbsp;MB</td><td align="right">874&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">34&nbsp;MB</td><td align="right">705&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">102&nbsp;MB</td><td align="right">740&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [855. Piunora](b0855b_Piunora-Hardware_Piunora.md) | [857. Nixie_proj_conflict-20171112-163801](b0857b_tlnixie_Nixie-proj-conflict-20171112-163801.md) |
