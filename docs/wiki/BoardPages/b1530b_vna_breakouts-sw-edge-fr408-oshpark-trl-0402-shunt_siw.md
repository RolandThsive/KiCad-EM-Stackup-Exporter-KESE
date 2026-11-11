# 1530. siw

Board 1,530 of the 3,117 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 15](../CorpusTestingPages/Corpus-Testing-15.md#1530-siw).

![siw: stages 4 and 6 take 43% to 66% of a run. Simulation, GLB takes 1.3 s. Simulation, STEP takes 1.9 s. Simulation, STL takes 1.2 s. Simulation, OBJ takes 1.5 s. Visual, GLB takes 1.3 s. Visual, OBJ takes 1.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1530b_vna_breakouts-sw-edge-fr408-oshpark-trl-0402-shunt_siw/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 80&nbsp;ms | 76&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.5 | 12&nbsp;ms | 44&nbsp;ms | 0.3 | 1.3 |
| Simulation, STEP | 74&nbsp;ms | 77&nbsp;ms | 0.3 | 0.2&nbsp;ms | 0.5 | 0.7 | 40&nbsp;ms | 0.2 | 1.9 |
| Simulation, STL | 78&nbsp;ms | 70&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.5 | 18&nbsp;ms | 44&nbsp;ms | 0.2 | 1.2 |
| Simulation, OBJ | 91&nbsp;ms | 81&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.5 | 0.3 | 43&nbsp;ms | 0.3 | 1.5 |
| Visual, GLB | 80&nbsp;ms | 83&nbsp;ms | 0.2 | 0.2&nbsp;ms | 0.6 | 6&nbsp;ms | 47&nbsp;ms | 0.2 | 1.3 |
| Visual, OBJ | 85&nbsp;ms | 82&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.6 | 0.1 | 42&nbsp;ms | 0.3 | 1.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `siw.kicad_pcb` |
|---|---|
| Folder | breakouts / sw_edge_fr408_oshpark / trl_0402_shunt |
| Complexity | 109&nbsp;/&nbsp;1000 (size&nbsp;79, features&nbsp;30) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 7, 0 |
| Triangles,&nbsp;simulation | 63,998 in 14 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">2.2&nbsp;MB</td><td align="right">73&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">5.3&nbsp;MB</td><td align="right">176&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">3.2&nbsp;MB</td><td align="right">74&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.0&nbsp;MB</td><td align="right">99&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">760&nbsp;kB</td><td align="right">100&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">2.1&nbsp;MB</td><td align="right">101&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1529. siw](b1529b_vna_breakouts-sw-edge-fr408-oshpark-trl-0402-series_siw.md) | [1531. siw](b1531b_vna_breakouts-sw-edge-fr408-oshpark-trl-admv_siw.md) |
