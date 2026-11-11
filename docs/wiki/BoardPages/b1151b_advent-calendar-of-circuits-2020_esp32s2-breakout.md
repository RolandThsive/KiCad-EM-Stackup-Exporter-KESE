# 1151. esp32s2-breakout

Board 1,151 of the 3,110 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 11](../CorpusTestingPages/Corpus-Testing-11.md#1151-esp32s2-breakout).

![esp32s2-breakout: stages 4 and 6 take 56% to 84% of a run. Simulation, GLB takes 31 s. Simulation, STEP takes 39 s. Simulation, STL takes 32 s. Simulation, OBJ takes 46 s. Visual, GLB takes 49 s. Visual, OBJ takes 61 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1151b_advent-calendar-of-circuits-2020_esp32s2-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 2.4 | 12.0 | 0.5&nbsp;ms | 13.3 | 0.5 | 1.4 | 0.3 | 30.8 |
| Simulation, STEP | 0.8 | 2.4 | 11.8 | 1&nbsp;ms | 13.4 | 9.1 | 1.4 | 0.3 | 39.1 |
| Simulation, STL | 0.9 | 2.7 | 12.1 | 0.6&nbsp;ms | 13.2 | 1.1 | 1.4 | 0.3 | 31.7 |
| Simulation, OBJ | 0.7 | 2.5 | 12.2 | 1.0&nbsp;ms | 13.3 | 15.3 | 1.3 | 0.3 | 45.6 |
| Visual, GLB | 0.8 | 2.3 | 12.3 | 0.4&nbsp;ms | 28.2 | 0.4 | 4.2 | 0.2 | 48.5 |
| Visual, OBJ | 0.8 | 2.5 | 12.0 | 1&nbsp;ms | 29.2 | 11.9 | 4.8 | 0.3 | 61.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [gregdavill/advent-calendar-of-circuits-2020](https://github.com/gregdavill/advent-calendar-of-circuits-2020)<br>Board: `esp32s2-breakout.kicad_pcb` |
|---|---|
| Folder | esp32s2-breakout / kicad-src |
| Complexity | 360&nbsp;/&nbsp;1000 (size&nbsp;245, features&nbsp;115) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20201220) |
| Parts,&nbsp;tracks,&nbsp;vias | 64, 1,459, 252 |
| Triangles,&nbsp;simulation | 3,009,806 in 93 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">101&nbsp;MB</td><td align="right">988&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">527&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">150&nbsp;MB</td><td align="right">992&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">316&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">75&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">235&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1150. ecpbreaker](b1150b_advent-calendar-of-circuits-2020_ecpbreaker.md) | [1152. esp32s2-co2-monitor](b1152b_advent-calendar-of-circuits-2020_esp32s2-co2-monitor.md) |
