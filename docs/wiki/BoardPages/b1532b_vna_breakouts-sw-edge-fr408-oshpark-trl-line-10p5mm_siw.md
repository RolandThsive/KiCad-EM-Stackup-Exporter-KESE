# 1532. siw

Board 1,532 of the 3,116 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 15](../CorpusTestingPages/Corpus-Testing-15.md#1532-siw).

![siw: stages 4 and 6 take 45% to 75% of a run. Simulation, GLB takes 1.5 s. Simulation, STEP takes 2.1 s. Simulation, STL takes 1.4 s. Simulation, OBJ takes 1.8 s. Visual, GLB takes 1.8 s. Visual, OBJ takes 1.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1532b_vna_breakouts-sw-edge-fr408-oshpark-trl-line-10p5mm_siw/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 87&nbsp;ms | 0.1 | 0.4 | 0.1&nbsp;ms | 0.6 | 18&nbsp;ms | 59&nbsp;ms | 0.2 | 1.5 |
| Simulation, STEP | 78&nbsp;ms | 97&nbsp;ms | 0.4 | 0.2&nbsp;ms | 0.6 | 0.7 | 55&nbsp;ms | 0.2 | 2.1 |
| Simulation, STL | 80&nbsp;ms | 95&nbsp;ms | 0.4 | 0.1&nbsp;ms | 0.6 | 27&nbsp;ms | 57&nbsp;ms | 0.2 | 1.4 |
| Simulation, OBJ | 74&nbsp;ms | 86&nbsp;ms | 0.4 | 0.1&nbsp;ms | 0.6 | 0.4 | 60&nbsp;ms | 0.2 | 1.8 |
| Visual, GLB | 79&nbsp;ms | 94&nbsp;ms | 0.4 | 0.1&nbsp;ms | 0.9 | 6&nbsp;ms | 46&nbsp;ms | 0.2 | 1.8 |
| Visual, OBJ | 78&nbsp;ms | 92&nbsp;ms | 0.4 | 0.1&nbsp;ms | 0.8 | 0.2 | 57&nbsp;ms | 0.2 | 1.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `siw.kicad_pcb` |
|---|---|
| Folder | breakouts / sw_edge_fr408_oshpark / trl_line_10p5mm |
| Complexity | 107&nbsp;/&nbsp;1000 (size&nbsp;77, features&nbsp;30) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 6, 0 |
| Triangles,&nbsp;simulation | 104,984 in 14 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">3.5&nbsp;MB</td><td align="right">193&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">8.3&nbsp;MB</td><td align="right">195&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">5.3&nbsp;MB</td><td align="right">194&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.8&nbsp;MB</td><td align="right">193&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">956&nbsp;kB</td><td align="right">155&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">2.7&nbsp;MB</td><td align="right">154&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1531. siw](b1531b_vna_breakouts-sw-edge-fr408-oshpark-trl-att-hmc_siw.md) | [1533. siw](b1533b_vna_breakouts-sw-edge-fr408-oshpark-trl-line-20mm_siw.md) |
