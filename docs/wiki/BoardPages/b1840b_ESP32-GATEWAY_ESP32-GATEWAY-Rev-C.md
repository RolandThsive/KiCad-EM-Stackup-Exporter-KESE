# 1840. ESP32-GATEWAY_Rev_C

Board 1,840 of the 3,128 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 18](../CorpusTestingPages/Corpus-Testing-18.md#1840-esp32-gateway_rev_c).

![ESP32-GATEWAY_Rev_C: stages 4 and 6 take 54% to 84% of a run. Simulation, GLB takes 15 s. Simulation, STEP takes 18 s. Simulation, STL takes 15 s. Simulation, OBJ takes 22 s. Visual, GLB takes 24 s. Visual, OBJ takes 30 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1840b_ESP32-GATEWAY_ESP32-GATEWAY-Rev-C/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.5 | 7.0 | 0.5&nbsp;ms | 4.8 | 0.2 | 0.6 | 0.3 | 14.9 |
| Simulation, STEP | 0.5 | 1.4 | 6.8 | 0.5&nbsp;ms | 4.6 | 3.8 | 0.6 | 0.2 | 17.9 |
| Simulation, STL | 0.5 | 1.5 | 6.9 | 0.6&nbsp;ms | 4.8 | 0.5 | 0.7 | 0.2 | 15.1 |
| Simulation, OBJ | 0.5 | 1.5 | 7.1 | 0.6&nbsp;ms | 4.8 | 7.4 | 0.6 | 0.3 | 22.1 |
| Visual, GLB | 0.4 | 1.6 | 6.8 | 0.5&nbsp;ms | 13.1 | 0.2 | 1.4 | 0.3 | 23.7 |
| Visual, OBJ | 0.5 | 1.6 | 6.9 | 0.5&nbsp;ms | 12.6 | 6.2 | 1.7 | 0.3 | 29.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [OLIMEX/ESP32-GATEWAY](https://github.com/OLIMEX/ESP32-GATEWAY)<br>Board: `ESP32-GATEWAY_Rev_C.kicad_pcb` |
|---|---|
| Folder | HARDWARE / Hardware revision C |
| Complexity | 288&nbsp;/&nbsp;1000 (size&nbsp;233, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 84, 1,868, 232 |
| Triangles,&nbsp;simulation | 1,333,358 in 104 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">47&nbsp;MB</td><td align="right">554&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">246&nbsp;MB</td><td align="right">670&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">67&nbsp;MB</td><td align="right">558&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">141&nbsp;MB</td><td align="right">950&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">758&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">117&nbsp;MB</td><td align="right">822&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1839. ESP32-GATEWAY_Rev_B](b1839b_ESP32-GATEWAY_ESP32-GATEWAY-Rev-B.md) | [1841. ESP32-GATEWAY_Rev_D](b1841b_ESP32-GATEWAY_ESP32-GATEWAY-Rev-D.md) |
