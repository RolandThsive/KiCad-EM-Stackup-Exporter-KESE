# 1188. syzygy-txr-breakout

Board 1,188 of the 3,125 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 11](../CorpusTestingPages/Corpus-Testing-11.md#1188-syzygy-txr-breakout).

![syzygy-txr-breakout: stages 4 and 6 take 45% to 82% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 15 s. Simulation, STL takes 12 s. Simulation, OBJ takes 20 s. Visual, GLB takes 17 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1188b_advent-calendar-of-circuits-2020_syzygy-txr-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.4 | 4.1 | 0.5&nbsp;ms | 4.7 | 0.2 | 0.6 | 0.3 | 11.9 |
| Simulation, STEP | 0.5 | 1.2 | 4.0 | 0.4&nbsp;ms | 4.8 | 3.5 | 0.7 | 0.3 | 15.0 |
| Simulation, STL | 0.4 | 1.2 | 4.2 | 0.4&nbsp;ms | 5.1 | 0.5 | 0.7 | 0.3 | 12.2 |
| Simulation, OBJ | 0.5 | 1.4 | 4.2 | 0.4&nbsp;ms | 4.9 | 8.1 | 0.7 | 0.3 | 19.9 |
| Visual, GLB | 0.4 | 1.1 | 4.0 | 0.5&nbsp;ms | 10.3 | 0.1 | 1.1 | 0.3 | 17.3 |
| Visual, OBJ | 0.4 | 1.2 | 4.2 | 0.4&nbsp;ms | 11.1 | 4.4 | 1.3 | 0.3 | 22.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [gregdavill/advent-calendar-of-circuits-2020](https://github.com/gregdavill/advent-calendar-of-circuits-2020)<br>Board: `syzygy-txr-breakout.kicad_pcb` |
|---|---|
| Folder | syzygy-txr-breakout / kicad-src |
| Complexity | 314&nbsp;/&nbsp;1000 (size&nbsp;199, features&nbsp;115) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20201116) |
| Parts,&nbsp;tracks,&nbsp;vias | 28, 2,385, 68 |
| Triangles,&nbsp;simulation | 1,349,284 in 70 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">655&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">196&nbsp;MB</td><td align="right">645&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">67&nbsp;MB</td><td align="right">602&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">137&nbsp;MB</td><td align="right">927&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">24&nbsp;MB</td><td align="right">684&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">74&nbsp;MB</td><td align="right">705&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1187. syzygy-sgmii](b1187b_advent-calendar-of-circuits-2020_syzygy-sgmii.md) | [1189. obsidian-boa-r0.1](b1189b_obsidian-boa_obsidian-boa-r0-1.md) |
