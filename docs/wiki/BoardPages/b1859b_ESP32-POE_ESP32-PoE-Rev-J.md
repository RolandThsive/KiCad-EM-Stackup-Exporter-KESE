# 1859. ESP32-PoE_Rev_J

Board 1,859 of the 3,122 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 18](../CorpusTestingPages/Corpus-Testing-18.md#1859-esp32-poe_rev_j).

![ESP32-PoE_Rev_J: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 18 s. Simulation, STEP takes 22 s. Simulation, STL takes 18 s. Simulation, OBJ takes 27 s. Visual, GLB takes 29 s. Visual, OBJ takes 36 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1859b_ESP32-POE_ESP32-PoE-Rev-J/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 2.0 | 6.4 | 0.6&nbsp;ms | 7.0 | 0.3 | 1.0 | 0.3 | 17.5 |
| Simulation, STEP | 0.5 | 2.1 | 6.6 | 0.7&nbsp;ms | 6.9 | 4.3 | 0.9 | 0.2 | 21.6 |
| Simulation, STL | 0.5 | 1.7 | 6.5 | 0.6&nbsp;ms | 6.9 | 0.6 | 0.9 | 0.3 | 17.5 |
| Simulation, OBJ | 0.6 | 2.1 | 6.7 | 0.9&nbsp;ms | 7.0 | 9.7 | 0.9 | 0.3 | 27.3 |
| Visual, GLB | 0.6 | 1.8 | 6.7 | 0.8&nbsp;ms | 17.0 | 0.2 | 2.1 | 0.3 | 28.7 |
| Visual, OBJ | 0.6 | 2.0 | 6.5 | 0.7&nbsp;ms | 17.5 | 7.1 | 2.4 | 0.3 | 36.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [OLIMEX/ESP32-POE](https://github.com/OLIMEX/ESP32-POE)<br>Board: `ESP32-PoE_Rev_J.kicad_pcb` |
|---|---|
| Folder | HARDWARE / ESP32-PoE-hardware-revision-J |
| Complexity | 323&nbsp;/&nbsp;1000 (size&nbsp;258, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 126, 2,532, 219 |
| Triangles,&nbsp;simulation | 2,002,088 in 139 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">71&nbsp;MB</td><td align="right">687&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">310&nbsp;MB</td><td align="right">840&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">100&nbsp;MB</td><td align="right">708&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">214&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">48&nbsp;MB</td><td align="right">854&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">147&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1858. ESP32-PoE_Rev_I](b1858b_ESP32-POE_ESP32-PoE-Rev-I.md) | [1860. ESP32-PoE_Rev_K](b1860b_ESP32-POE_ESP32-PoE-Rev-K.md) |
