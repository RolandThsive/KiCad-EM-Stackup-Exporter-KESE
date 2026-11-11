# 1518. siw

Board 1,518 of the 3,108 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 15](../CorpusTestingPages/Corpus-Testing-15.md#1518-siw).

![siw: stages 4 and 6 take 50% to 75% of a run. Simulation, GLB takes 1.5 s. Simulation, STEP takes 2.2 s. Simulation, STL takes 1.5 s. Simulation, OBJ takes 1.9 s. Visual, GLB takes 1.6 s. Visual, OBJ takes 1.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1518b_vna_breakouts-sw-edge-fr408-oshpark-lpf-20ghz_siw/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 78&nbsp;ms | 84&nbsp;ms | 0.4 | 0.1&nbsp;ms | 0.6 | 18&nbsp;ms | 75&nbsp;ms | 0.2 | 1.5 |
| Simulation, STEP | 73&nbsp;ms | 85&nbsp;ms | 0.5 | 0.1&nbsp;ms | 0.6 | 0.7 | 52&nbsp;ms | 0.2 | 2.2 |
| Simulation, STL | 80&nbsp;ms | 0.1 | 0.4 | 0.1&nbsp;ms | 0.6 | 25&nbsp;ms | 58&nbsp;ms | 0.2 | 1.5 |
| Simulation, OBJ | 75&nbsp;ms | 0.1 | 0.4 | 0.1&nbsp;ms | 0.6 | 0.5 | 56&nbsp;ms | 0.2 | 1.9 |
| Visual, GLB | 78&nbsp;ms | 89&nbsp;ms | 0.4 | 0.2&nbsp;ms | 0.8 | 6&nbsp;ms | 44&nbsp;ms | 0.2 | 1.6 |
| Visual, OBJ | 81&nbsp;ms | 97&nbsp;ms | 0.4 | 0.1&nbsp;ms | 0.8 | 0.2 | 38&nbsp;ms | 0.2 | 1.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `siw.kicad_pcb` |
|---|---|
| Folder | breakouts / sw_edge_fr408_oshpark / lpf_20ghz |
| Complexity | 108&nbsp;/&nbsp;1000 (size&nbsp;78, features&nbsp;30) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 3, 5, 0 |
| Triangles,&nbsp;simulation | 105,776 in 16 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">3.5&nbsp;MB</td><td align="right">192&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">8.5&nbsp;MB</td><td align="right">196&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">5.3&nbsp;MB</td><td align="right">192&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.9&nbsp;MB</td><td align="right">188&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">969&nbsp;kB</td><td align="right">156&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">2.7&nbsp;MB</td><td align="right">153&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1517. splitter_breakout](b1517b_vna_splitter-breakout.md) | [1519. siw](b1519b_vna_breakouts-sw-edge-fr408-oshpark-lpf-8ghz_siw.md) |
