# 470. la-pod-mmcx

Board 470 of the 3,111 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 5](../CorpusTestingPages/Corpus-Testing-05.md#470-la-pod-mmcx).

![la-pod-mmcx: stages 4 and 6 take 52% to 82% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 13 s. Simulation, STL takes 11 s. Simulation, OBJ takes 15 s. Visual, GLB takes 12 s. Visual, OBJ takes 15 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0470b_starshipraider_la-pod-mmcx/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 1.0 | 4.7 | 0.3&nbsp;ms | 3.8 | 0.2 | 0.5 | 0.2 | 10.7 |
| Simulation, STEP | 0.2 | 1.0 | 4.2 | 0.2&nbsp;ms | 3.7 | 2.5 | 0.6 | 0.3 | 12.6 |
| Simulation, STL | 0.3 | 0.9 | 4.5 | 0.2&nbsp;ms | 3.7 | 0.3 | 0.5 | 0.3 | 10.5 |
| Simulation, OBJ | 0.3 | 1.0 | 4.4 | 0.2&nbsp;ms | 3.4 | 5.1 | 0.5 | 0.2 | 15.0 |
| Visual, GLB | 0.3 | 0.9 | 4.0 | 0.2&nbsp;ms | 6.2 | 76&nbsp;ms | 0.6 | 0.3 | 12.4 |
| Visual, OBJ | 0.3 | 1.1 | 4.4 | 0.2&nbsp;ms | 6.7 | 2.2 | 0.5 | 0.2 | 15.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [azonenberg/starshipraider](https://github.com/azonenberg/starshipraider)<br>Board: `la-pod-mmcx.kicad_pcb` |
|---|---|
| Folder | boards / probes / la-pod-mmcx |
| Complexity | 211&nbsp;/&nbsp;1000 (size&nbsp;176, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 11, 635, 187 |
| Triangles,&nbsp;simulation | 911,210 in 28 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">424&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">106&nbsp;MB</td><td align="right">476&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">46&nbsp;MB</td><td align="right">405&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">92&nbsp;MB</td><td align="right">650&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">396&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">37&nbsp;MB</td><td align="right">428&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [469. integralstick-mead](b0469b_starshipraider_integralstick-mead.md) | [471. sma-test](b0471b_starshipraider_boards-probes-oshpark-sma-test-sma-test_sma-test.md) |
