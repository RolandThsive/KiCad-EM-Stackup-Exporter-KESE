# 1858. ESP32-PoE_Rev_D

Board 1,858 of the 3,128 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 18](../CorpusTestingPages/Corpus-Testing-18.md#1858-esp32-poe_rev_d).

![ESP32-PoE_Rev_D: stages 4 and 6 take 51% to 84% of a run. Simulation, GLB takes 17 s. Simulation, STEP takes 21 s. Simulation, STL takes 18 s. Simulation, OBJ takes 26 s. Visual, GLB takes 28 s. Visual, OBJ takes 36 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1858b_ESP32-POE_ESP32-PoE-Rev-D/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 1.8 | 7.4 | 0.5&nbsp;ms | 6.1 | 0.2 | 0.9 | 0.3 | 17.4 |
| Simulation, STEP | 0.6 | 1.7 | 7.0 | 0.5&nbsp;ms | 6.1 | 4.4 | 1.0 | 0.3 | 21.2 |
| Simulation, STL | 0.7 | 1.7 | 7.3 | 0.6&nbsp;ms | 6.2 | 0.5 | 0.9 | 0.3 | 17.6 |
| Simulation, OBJ | 0.6 | 1.8 | 7.2 | 0.7&nbsp;ms | 6.3 | 9.2 | 0.9 | 0.2 | 26.2 |
| Visual, GLB | 0.5 | 1.7 | 7.2 | 0.8&nbsp;ms | 16.5 | 0.2 | 1.8 | 0.3 | 28.3 |
| Visual, OBJ | 0.5 | 1.7 | 7.1 | 0.7&nbsp;ms | 16.0 | 7.8 | 2.1 | 0.3 | 35.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [OLIMEX/ESP32-POE](https://github.com/OLIMEX/ESP32-POE)<br>Board: `ESP32-PoE_Rev_D.kicad_pcb` |
|---|---|
| Folder | HARDWARE / ESP32-PoE-hardware-revision-D |
| Complexity | 307&nbsp;/&nbsp;1000 (size&nbsp;242, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 117, 2,882, 234 |
| Triangles,&nbsp;simulation | 1,515,032 in 139 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">54&nbsp;MB</td><td align="right">653&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">292&nbsp;MB</td><td align="right">748&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">76&nbsp;MB</td><td align="right">640&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">161&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">798&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">137&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1857. ESP32-PoE_Rev_C](b1857b_ESP32-POE_HARDWARE-ESP32-PoE-hardware-revision-C1_ESP32-PoE-Rev-C.md) | [1859. ESP32-PoE_Rev_E](b1859b_ESP32-POE_ESP32-PoE-Rev-E.md) |
