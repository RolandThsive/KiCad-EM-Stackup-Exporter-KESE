# 1835. ESP32-EVB_Rev_K

Board 1,835 of the 3,129 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 17](../CorpusTestingPages/Corpus-Testing-17.md#1835-esp32-evb_rev_k).

![ESP32-EVB_Rev_K: stages 4 and 6 take 55% to 84% of a run. Simulation, GLB takes 25 s. Simulation, STEP takes 30 s. Simulation, STL takes 26 s. Simulation, OBJ takes 37 s. Visual, GLB takes 38 s. Visual, OBJ takes 47 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1835b_ESP32-EVB_ESP32-EVB-Rev-K/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 2.6 | 11.4 | 0.8&nbsp;ms | 8.8 | 0.3 | 1.1 | 0.3 | 25.3 |
| Simulation, STEP | 0.7 | 2.4 | 11.1 | 0.6&nbsp;ms | 8.7 | 5.9 | 1.1 | 0.2 | 30.0 |
| Simulation, STL | 0.8 | 2.5 | 11.5 | 0.9&nbsp;ms | 8.9 | 0.5 | 1.2 | 0.2 | 25.6 |
| Simulation, OBJ | 0.8 | 2.4 | 11.3 | 0.7&nbsp;ms | 8.8 | 12.1 | 1.2 | 0.2 | 36.8 |
| Visual, GLB | 0.7 | 2.5 | 11.0 | 0.4&nbsp;ms | 20.7 | 0.3 | 2.5 | 0.2 | 38.0 |
| Visual, OBJ | 0.7 | 2.4 | 10.7 | 0.8&nbsp;ms | 20.6 | 9.7 | 2.6 | 0.2 | 47.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [OLIMEX/ESP32-EVB](https://github.com/OLIMEX/ESP32-EVB)<br>Board: `ESP32-EVB_Rev_K.kicad_pcb` |
|---|---|
| Folder | HARDWARE / REV-K |
| Complexity | 303&nbsp;/&nbsp;1000 (size&nbsp;248, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 157, 3,236, 315 |
| Triangles,&nbsp;simulation | 2,291,902 in 145 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">81&nbsp;MB</td><td align="right">890&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">430&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">115&nbsp;MB</td><td align="right">886&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">247&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">66&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">203&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1834. ESP32-EVB_Rev_J](b1834b_ESP32-EVB_ESP32-EVB-Rev-J.md) | [1836. ESP32-EVB_Rev_K1](b1836b_ESP32-EVB_ESP32-EVB-Rev-K1.md) |
