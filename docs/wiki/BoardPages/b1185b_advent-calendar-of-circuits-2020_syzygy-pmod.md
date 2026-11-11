# 1185. syzygy-pmod

Board 1,185 of the 3,125 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 11](../CorpusTestingPages/Corpus-Testing-11.md#1185-syzygy-pmod).

![syzygy-pmod: stages 4 and 6 take 47% to 80% of a run. Simulation, GLB takes 5.0 s. Simulation, STEP takes 7.0 s. Simulation, STL takes 5.6 s. Simulation, OBJ takes 8.4 s. Visual, GLB takes 8.1 s. Visual, OBJ takes 9.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1185b_advent-calendar-of-circuits-2020_syzygy-pmod/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 1.8 | 0.3&nbsp;ms | 1.8 | 90&nbsp;ms | 0.4 | 0.2 | 5.0 |
| Simulation, STEP | 0.2 | 0.6 | 1.8 | 0.3&nbsp;ms | 2.0 | 1.8 | 0.4 | 0.2 | 7.0 |
| Simulation, STL | 0.2 | 0.6 | 2.0 | 0.3&nbsp;ms | 2.0 | 0.2 | 0.4 | 0.2 | 5.6 |
| Simulation, OBJ | 0.2 | 0.6 | 1.9 | 0.3&nbsp;ms | 2.0 | 3.0 | 0.4 | 0.2 | 8.4 |
| Visual, GLB | 0.2 | 0.6 | 1.9 | 0.3&nbsp;ms | 4.6 | 61&nbsp;ms | 0.5 | 0.2 | 8.1 |
| Visual, OBJ | 0.2 | 0.6 | 1.9 | 0.3&nbsp;ms | 4.4 | 1.8 | 0.6 | 0.2 | 9.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [gregdavill/advent-calendar-of-circuits-2020](https://github.com/gregdavill/advent-calendar-of-circuits-2020)<br>Board: `syzygy-pmod.kicad_pcb` |
|---|---|
| Folder | syzygy-pmod / kicad-src |
| Complexity | 281&nbsp;/&nbsp;1000 (size&nbsp;166, features&nbsp;115) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20201116) |
| Parts,&nbsp;tracks,&nbsp;vias | 16, 387, 36 |
| Triangles,&nbsp;simulation | 702,838 in 70 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">340&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">93&nbsp;MB</td><td align="right">381&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">35&nbsp;MB</td><td align="right">331&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">71&nbsp;MB</td><td align="right">506&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">392&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">39&nbsp;MB</td><td align="right">390&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1184. syzygy-flir-tau2](b1184b_advent-calendar-of-circuits-2020_syzygy-flir-tau2.md) | [1186. syzygy-rgb888-lcd](b1186b_advent-calendar-of-circuits-2020_syzygy-rgb888-lcd.md) |
