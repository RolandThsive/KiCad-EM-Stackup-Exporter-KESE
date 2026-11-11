# 1812. ESP32-EVB_Rev_J

Board 1,812 of the 3,104 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 17](../CorpusTestingPages/Corpus-Testing-17.md#1812-esp32-evb_rev_j).

![ESP32-EVB_Rev_J: stages 4 and 6 take 57% to 84% of a run. Simulation, GLB takes 25 s. Simulation, STEP takes 32 s. Simulation, STL takes 26 s. Simulation, OBJ takes 36 s. Visual, GLB takes 40 s. Visual, OBJ takes 49 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1812b_ESP32-EVB_ESP32-EVB-Rev-J/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.6 | 11.0 | 0.8&nbsp;ms | 9.1 | 0.4 | 1.2 | 0.3 | 25.3 |
| Simulation, STEP | 0.8 | 2.3 | 11.6 | 1&nbsp;ms | 9.3 | 6.3 | 1.2 | 0.3 | 31.7 |
| Simulation, STL | 0.8 | 2.5 | 11.1 | 1&nbsp;ms | 9.1 | 0.6 | 1.3 | 0.3 | 25.7 |
| Simulation, OBJ | 0.7 | 2.7 | 11.3 | 1.0&nbsp;ms | 9.2 | 10.5 | 1.2 | 0.2 | 35.8 |
| Visual, GLB | 0.7 | 2.5 | 11.4 | 0.9&nbsp;ms | 22.5 | 0.3 | 2.6 | 0.3 | 40.3 |
| Visual, OBJ | 0.7 | 2.2 | 11.0 | 0.9&nbsp;ms | 23.5 | 8.8 | 2.7 | 0.3 | 49.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [OLIMEX/ESP32-EVB](https://github.com/OLIMEX/ESP32-EVB)<br>Board: `ESP32-EVB_Rev_J.kicad_pcb` |
|---|---|
| Folder | HARDWARE / REV-J |
| Complexity | 303&nbsp;/&nbsp;1000 (size&nbsp;248, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 157, 3,235, 315 |
| Triangles,&nbsp;simulation | 2,334,232 in 145 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">82&nbsp;MB</td><td align="right">886&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">445&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">117&nbsp;MB</td><td align="right">890&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">251&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">66&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">203&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1811. ESP32-EVB_Rev_I](b1811b_ESP32-EVB_ESP32-EVB-Rev-I.md) | [1813. ESP32-EVB_Rev_K](b1813b_ESP32-EVB_ESP32-EVB-Rev-K.md) |
