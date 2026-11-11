# 1545. trl_line

Board 1,545 of the 3,110 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 15](../CorpusTestingPages/Corpus-Testing-15.md#1545-trl_line).

![trl_line: stages 4 and 6 take 51% to 79% of a run. Simulation, GLB takes 2.4 s. Simulation, STEP takes 3.1 s. Simulation, STL takes 2.3 s. Simulation, OBJ takes 3.4 s. Visual, GLB takes 2.9 s. Visual, OBJ takes 3.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1545b_vna_hardware-archive-oshpark-4layer-trl-cal-trl-thru_trl-line/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 81&nbsp;ms | 0.2 | 0.9 | 0.2&nbsp;ms | 0.8 | 32&nbsp;ms | 98&nbsp;ms | 0.2 | 2.4 |
| Simulation, STEP | 77&nbsp;ms | 0.2 | 0.9 | 0.2&nbsp;ms | 0.8 | 0.9 | 0.1 | 0.2 | 3.1 |
| Simulation, STL | 78&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 0.8 | 47&nbsp;ms | 98&nbsp;ms | 0.2 | 2.3 |
| Simulation, OBJ | 79&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 0.8 | 1.1 | 0.1 | 0.2 | 3.4 |
| Visual, GLB | 83&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 1.4 | 14&nbsp;ms | 0.1 | 0.2 | 2.9 |
| Visual, OBJ | 77&nbsp;ms | 0.2 | 0.9 | 0.2&nbsp;ms | 1.4 | 0.5 | 0.1 | 0.2 | 3.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `trl_line.kicad_pcb` |
|---|---|
| Folder | hardware / archive / oshpark_4layer_trl_cal / trl_thru |
| Complexity | 77&nbsp;/&nbsp;1000 (size&nbsp;57, features&nbsp;20) |
| KESE&nbsp;features | filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 1, 0 |
| Triangles,&nbsp;simulation | 226,164 in 14 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">7.4&nbsp;MB</td><td align="right">228&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">22&nbsp;MB</td><td align="right">243&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">11&nbsp;MB</td><td align="right">233&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">233&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.2&nbsp;MB</td><td align="right">167&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.0&nbsp;MB</td><td align="right">168&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1544. trl_reflect](b1544b_vna_trl-reflect.md) | [1546. trl_line](b1546b_vna_hardware-archive-oshpark-4layer-trl-cal-trl-ustrip-test_trl-line.md) |
