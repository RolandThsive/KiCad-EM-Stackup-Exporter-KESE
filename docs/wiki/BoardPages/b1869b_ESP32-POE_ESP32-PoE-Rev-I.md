# 1869. ESP32-PoE_Rev_I

Board 1,869 of the 3,138 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 18](../CorpusTestingPages/Corpus-Testing-18.md#1869-esp32-poe_rev_i).

![ESP32-PoE_Rev_I: stages 4 and 6 take 50% to 84% of a run. Simulation, GLB takes 18 s. Simulation, STEP takes 22 s. Simulation, STL takes 18 s. Simulation, OBJ takes 27 s. Visual, GLB takes 26 s. Visual, OBJ takes 33 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1869b_ESP32-POE_ESP32-PoE-Rev-I/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 1.9 | 7.1 | 0.6&nbsp;ms | 7.0 | 0.3 | 1.0 | 0.3 | 18.2 |
| Simulation, STEP | 0.6 | 1.8 | 7.0 | 0.5&nbsp;ms | 7.0 | 4.8 | 0.9 | 0.2 | 22.3 |
| Simulation, STL | 0.6 | 2.0 | 7.0 | 0.6&nbsp;ms | 7.0 | 0.5 | 1.0 | 0.2 | 18.3 |
| Simulation, OBJ | 0.6 | 1.9 | 6.8 | 0.6&nbsp;ms | 6.8 | 10.0 | 1.0 | 0.2 | 27.5 |
| Visual, GLB | 0.6 | 1.9 | 7.0 | 0.6&nbsp;ms | 15.1 | 0.2 | 1.3 | 0.2 | 26.3 |
| Visual, OBJ | 0.6 | 1.8 | 6.8 | 0.7&nbsp;ms | 15.1 | 7.6 | 1.3 | 0.2 | 33.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [OLIMEX/ESP32-POE](https://github.com/OLIMEX/ESP32-POE)<br>Board: `ESP32-PoE_Rev_I.kicad_pcb` |
|---|---|
| Folder | HARDWARE / ESP32-PoE-hardware-revision-I |
| Complexity | 324&nbsp;/&nbsp;1000 (size&nbsp;259, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 123, 2,830, 219 |
| Triangles,&nbsp;simulation | 1,907,268 in 138 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">67&nbsp;MB</td><td align="right">694&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">306&nbsp;MB</td><td align="right">846&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">95&nbsp;MB</td><td align="right">691&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">204&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">48&nbsp;MB</td><td align="right">859&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">147&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1868. ESP32-PoE_Rev_G1](b1868b_ESP32-POE_ESP32-PoE-Rev-G1.md) | [1870. ESP32-PoE_Rev_J](b1870b_ESP32-POE_ESP32-PoE-Rev-J.md) |
