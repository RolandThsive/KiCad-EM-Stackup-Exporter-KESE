# 1857. ESP32-PoE_Rev_E

Board 1,857 of the 3,123 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 18](../CorpusTestingPages/Corpus-Testing-18.md#1857-esp32-poe_rev_e).

![ESP32-PoE_Rev_E: stages 4 and 6 take 55% to 83% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 20 s. Simulation, STL takes 16 s. Simulation, OBJ takes 23 s. Visual, GLB takes 26 s. Visual, OBJ takes 32 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1857b_ESP32-POE_ESP32-PoE-Rev-E/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.6 | 6.6 | 1&nbsp;ms | 6.1 | 0.3 | 0.8 | 0.3 | 16.2 |
| Simulation, STEP | 0.5 | 1.6 | 6.5 | 0.8&nbsp;ms | 6.0 | 4.0 | 0.8 | 0.3 | 19.6 |
| Simulation, STL | 0.5 | 1.5 | 6.6 | 1&nbsp;ms | 6.0 | 0.5 | 0.9 | 0.3 | 16.2 |
| Simulation, OBJ | 0.4 | 1.5 | 6.8 | 0.9&nbsp;ms | 6.1 | 7.5 | 0.8 | 0.3 | 23.4 |
| Visual, GLB | 0.5 | 1.6 | 6.3 | 0.7&nbsp;ms | 15.5 | 0.3 | 2.0 | 0.3 | 26.3 |
| Visual, OBJ | 0.5 | 1.6 | 6.6 | 0.8&nbsp;ms | 15.1 | 6.2 | 2.1 | 0.3 | 32.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [OLIMEX/ESP32-POE](https://github.com/OLIMEX/ESP32-POE)<br>Board: `ESP32-PoE_Rev_E.kicad_pcb` |
|---|---|
| Folder | HARDWARE / ESP32-PoE-hardware-revision-E |
| Complexity | 308&nbsp;/&nbsp;1000 (size&nbsp;243, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 118, 2,894, 234 |
| Triangles,&nbsp;simulation | 1,515,626 in 139 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">54&nbsp;MB</td><td align="right">670&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">292&nbsp;MB</td><td align="right">760&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">76&nbsp;MB</td><td align="right">661&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">162&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">826&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">137&nbsp;MB</td><td align="right">949&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1856. ESP32-PoE_Rev_D](b1856b_ESP32-POE_ESP32-PoE-Rev-D.md) | [1858. ESP32-PoE_Rev_G1](b1858b_ESP32-POE_ESP32-PoE-Rev-G1.md) |
