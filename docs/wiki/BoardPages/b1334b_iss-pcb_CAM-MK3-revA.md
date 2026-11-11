# 1334. CAM-MK3-revA

Board 1,334 of the 3,138 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 13](../CorpusTestingPages/Corpus-Testing-13.md#1334-cam-mk3-reva).

![CAM-MK3-revA: stages 4 and 6 take 45% to 81% of a run. Simulation, GLB takes 14 s. Simulation, STEP takes 18 s. Simulation, STL takes 14 s. Simulation, OBJ takes 22 s. Visual, GLB takes 21 s. Visual, OBJ takes 27 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1334b_iss-pcb_CAM-MK3-revA/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 1.8 | 4.7 | 0.6&nbsp;ms | 5.3 | 0.3 | 0.8 | 0.2 | 13.8 |
| Simulation, STEP | 0.5 | 1.7 | 4.5 | 0.6&nbsp;ms | 5.8 | 4.6 | 0.9 | 0.3 | 18.3 |
| Simulation, STL | 0.4 | 1.6 | 4.6 | 0.6&nbsp;ms | 5.3 | 0.5 | 0.8 | 0.3 | 13.5 |
| Simulation, OBJ | 0.6 | 1.6 | 4.4 | 0.6&nbsp;ms | 5.3 | 8.4 | 0.9 | 0.3 | 21.5 |
| Visual, GLB | 0.5 | 1.8 | 4.7 | 0.5&nbsp;ms | 12.7 | 0.2 | 1.3 | 0.2 | 21.4 |
| Visual, OBJ | 0.5 | 1.7 | 4.6 | 0.8&nbsp;ms | 12.6 | 5.5 | 1.4 | 0.2 | 26.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [issuiuc/iss-pcb](https://github.com/issuiuc/iss-pcb)<br>Board: `CAM-MK3-revA.kicad_pcb` |
|---|---|
| Folder | boards / CAM-MK3 / CAM-MK3-revA |
| Complexity | 381&nbsp;/&nbsp;1000 (size&nbsp;241, features&nbsp;140) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 110, 645, 197 |
| Triangles,&nbsp;simulation | 1,678,810 in 202 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">56&nbsp;MB</td><td align="right">686&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">227&nbsp;MB</td><td align="right">756&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">84&nbsp;MB</td><td align="right">729&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">175&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">36&nbsp;MB</td><td align="right">823&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">111&nbsp;MB</td><td align="right">853&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1333. CAM-MK2.1](b1333b_iss-pcb_CAM-MK2-1.md) | [1335. CAM-MK3-revB](b1335b_iss-pcb_CAM-MK3-revB.md) |
