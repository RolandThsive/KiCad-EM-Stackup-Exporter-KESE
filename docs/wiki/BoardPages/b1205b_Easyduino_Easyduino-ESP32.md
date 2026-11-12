# 1205. Easyduino_ESP32

Board 1,205 of the 3,132 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 12](../CorpusTestingPages/Corpus-Testing-12.md#1205-easyduino_esp32).

![Easyduino_ESP32: stages 4 and 6 take 47% to 83% of a run. Simulation, GLB takes 6.5 s. Simulation, STEP takes 9.0 s. Simulation, STL takes 6.6 s. Simulation, OBJ takes 10 s. Visual, GLB takes 9.9 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1205b_Easyduino_Easyduino-ESP32/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.7 | 2.3 | 0.5&nbsp;ms | 2.4 | 0.1 | 0.4 | 0.3 | 6.5 |
| Simulation, STEP | 0.2 | 0.7 | 2.5 | 0.3&nbsp;ms | 2.4 | 2.4 | 0.5 | 0.2 | 9.0 |
| Simulation, STL | 0.3 | 0.7 | 2.4 | 0.3&nbsp;ms | 2.4 | 0.2 | 0.5 | 0.2 | 6.6 |
| Simulation, OBJ | 0.2 | 0.7 | 2.5 | 0.3&nbsp;ms | 2.3 | 3.9 | 0.4 | 0.3 | 10.3 |
| Visual, GLB | 0.2 | 0.6 | 2.4 | 0.4&nbsp;ms | 5.8 | 67&nbsp;ms | 0.5 | 0.3 | 9.9 |
| Visual, OBJ | 0.3 | 0.7 | 2.5 | 0.3&nbsp;ms | 5.4 | 2.5 | 0.5 | 0.3 | 12.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Hanqaqa/Easyduino](https://github.com/Hanqaqa/Easyduino)<br>Board: `Easyduino_ESP32.kicad_pcb` |
|---|---|
| Folder | ESP32 |
| Complexity | 299&nbsp;/&nbsp;1000 (size&nbsp;214, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 29, 372, 64 |
| Triangles,&nbsp;simulation | 663,478 in 86 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">324&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">98&nbsp;MB</td><td align="right">385&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">33&nbsp;MB</td><td align="right">324&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">67&nbsp;MB</td><td align="right">494&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">412&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">42&nbsp;MB</td><td align="right">377&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1204. Easyduino_Atmega](b1204b_Easyduino_Easyduino-Atmega.md) | [1206. Easyduino_ESP32S3](b1206b_Easyduino_Easyduino-ESP32S3.md) |
