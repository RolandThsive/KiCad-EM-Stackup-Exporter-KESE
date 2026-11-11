# 2473. tle6240_driver

Board 2,473 of the 3,128 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 23](../CorpusTestingPages/Corpus-Testing-23.md#2473-tle6240_driver).

![tle6240_driver: stages 4 and 6 take 66% to 85% of a run. Simulation, GLB takes 7.1 s. Simulation, STEP takes 8.7 s. Simulation, STL takes 7.4 s. Simulation, OBJ takes 9.4 s. Visual, GLB takes 7.7 s. Visual, OBJ takes 8.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2473b_rusefi-hardware_classic-designs-rusefi-hardware-history-low-side-tle6240-rev00-11_tle6240-driver/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.8 | 0.3&nbsp;ms | 4.1 | 72&nbsp;ms | 0.3 | 0.2 | 7.1 |
| Simulation, STEP | 0.1 | 0.4 | 1.9 | 0.3&nbsp;ms | 4.2 | 1.5 | 0.3 | 0.2 | 8.7 |
| Simulation, STL | 0.1 | 0.3 | 1.9 | 0.3&nbsp;ms | 4.4 | 0.1 | 0.3 | 0.2 | 7.4 |
| Simulation, OBJ | 0.1 | 0.4 | 1.9 | 0.3&nbsp;ms | 4.2 | 2.2 | 0.3 | 0.2 | 9.4 |
| Visual, GLB | 0.1 | 0.4 | 1.9 | 0.3&nbsp;ms | 4.5 | 53&nbsp;ms | 0.4 | 0.3 | 7.7 |
| Visual, OBJ | 0.1 | 0.4 | 1.9 | 0.4&nbsp;ms | 4.3 | 1.5 | 0.4 | 0.3 | 8.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [rusefi/rusefi-hardware](https://github.com/rusefi/rusefi-hardware)<br>Board: `tle6240_driver.kicad_pcb` |
|---|---|
| Folder | classic-designs / rusefi_hardware_history / low_side_tle6240_rev00.11 |
| Complexity | 181&nbsp;/&nbsp;1000 (size&nbsp;146, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 12, 363, 40 |
| Triangles,&nbsp;simulation | 449,184 in 48 parts |
| Verifier | PASS in all six runs |
| Run&nbsp;again | Simulation, GLB; Simulation, STEP; Simulation, STL; Simulation, OBJ: failed in the corpus run, run again with fixes to KESE made after the corpus run, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">283&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">72&nbsp;MB</td><td align="right">333&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">22&nbsp;MB</td><td align="right">286&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">45&nbsp;MB</td><td align="right">359&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">344&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">33&nbsp;MB</td><td align="right">340&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2472. tle6240_driver](b2472b_rusefi-hardware_classic-designs-rusefi-hardware-history-low-side-tle6240-rev00-10_tle6240-driver.md) | [2474. Map_MPX](b2474b_rusefi-hardware_Map-MPX.md) |
