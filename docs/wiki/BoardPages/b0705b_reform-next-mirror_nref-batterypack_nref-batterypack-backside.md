# 705. nref-batterypack-backside

Board 705 of the 3,120 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 7](../CorpusTestingPages/Corpus-Testing-07.md#705-nref-batterypack-backside).

![nref-batterypack-backside: stages 4 and 6 take 37% to 61% of a run. Simulation, GLB takes 1.0 s. Simulation, STEP takes 1.2 s. Simulation, STL takes 1.0 s. Simulation, OBJ takes 1.2 s. Visual, GLB takes 1.2 s. Visual, OBJ takes 1.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0705b_reform-next-mirror_nref-batterypack_nref-batterypack-backside/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 99&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 7&nbsp;ms | 23&nbsp;ms | 0.2 | 1.0 |
| Simulation, STEP | 0.1 | 90&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 0.3 | 20&nbsp;ms | 0.3 | 1.2 |
| Simulation, STL | 0.1 | 0.1 | 0.2 | 0.1&nbsp;ms | 0.3 | 11&nbsp;ms | 25&nbsp;ms | 0.2 | 1.0 |
| Simulation, OBJ | 0.1 | 0.1 | 0.2 | 0.1&nbsp;ms | 0.3 | 0.2 | 21&nbsp;ms | 0.2 | 1.2 |
| Visual, GLB | 0.1 | 90&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.6 | 8&nbsp;ms | 49&nbsp;ms | 0.2 | 1.2 |
| Visual, OBJ | 0.2 | 0.1 | 0.2 | 0.1&nbsp;ms | 0.6 | 0.3 | 48&nbsp;ms | 0.2 | 1.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-batterypack-backside.kicad_pcb` |
|---|---|
| Folder | nref-batterypack |
| Complexity | 122&nbsp;/&nbsp;1000 (size&nbsp;72, features&nbsp;50) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>curved board outline,<br>knockout text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 1, 12, 2 |
| Triangles,&nbsp;simulation | 31,336 in 12 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.2&nbsp;MB</td><td align="right">72&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">7.0&nbsp;MB</td><td align="right">77&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">1.6&nbsp;MB</td><td align="right">72&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.2&nbsp;MB</td><td align="right">79&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">1.1&nbsp;MB</td><td align="right">88&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.1&nbsp;MB</td><td align="right">101&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [704. nref-batterypack](b0704b_reform-next-mirror_nref-batterypack-v3_nref-batterypack.md) | [706. nref-batterypack](b0706b_reform-next-mirror_nref-batterypack_nref-batterypack.md) |
