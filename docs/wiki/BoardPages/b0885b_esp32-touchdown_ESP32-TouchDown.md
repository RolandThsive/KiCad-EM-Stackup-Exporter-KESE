# 885. ESP32_TouchDown

Board 885 of the 3,124 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 9](../CorpusTestingPages/Corpus-Testing-09.md#885-esp32_touchdown).

![ESP32_TouchDown: stages 4 and 6 take 58% to 85% of a run. Simulation, GLB takes 14 s. Simulation, STEP takes 18 s. Simulation, STL takes 14 s. Simulation, OBJ takes 19 s. Visual, GLB takes 18 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0885b_esp32-touchdown_ESP32-TouchDown/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.0 | 5.9 | 0.6&nbsp;ms | 5.6 | 0.2 | 0.6 | 0.2 | 13.9 |
| Simulation, STEP | 0.4 | 1.0 | 5.9 | 0.5&nbsp;ms | 5.4 | 4.0 | 0.6 | 0.3 | 17.6 |
| Simulation, STL | 0.3 | 1.0 | 5.9 | 0.7&nbsp;ms | 5.2 | 0.3 | 0.6 | 0.2 | 13.5 |
| Simulation, OBJ | 0.3 | 0.9 | 5.7 | 0.8&nbsp;ms | 5.3 | 6.0 | 0.6 | 0.2 | 19.1 |
| Visual, GLB | 0.4 | 1.0 | 5.8 | 0.6&nbsp;ms | 9.6 | 0.1 | 1.1 | 0.2 | 18.3 |
| Visual, OBJ | 0.4 | 1.0 | 5.8 | 0.6&nbsp;ms | 9.5 | 4.9 | 1.3 | 0.2 | 23.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [DustinWatts/esp32-touchdown](https://github.com/DustinWatts/esp32-touchdown)<br>Board: `ESP32_TouchDown.kicad_pcb` |
|---|---|
| Folder | Hardware / ESP32_TouchDown_Rev1 |
| Complexity | 309&nbsp;/&nbsp;1000 (size&nbsp;219, features&nbsp;90) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 65, 802, 157 |
| Triangles,&nbsp;simulation | 1,138,490 in 106 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">40&nbsp;MB</td><td align="right">535&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">194&nbsp;MB</td><td align="right">638&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">57&nbsp;MB</td><td align="right">543&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">117&nbsp;MB</td><td align="right">810&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">594&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">93&nbsp;MB</td><td align="right">744&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [884. ESP32_TouchDown_Rev1.1](b0884b_esp32-touchdown_ESP32-TouchDown-Rev1-1.md) | [886. PCIe-Adapter](b0886b_ecp5-pcie_PCIe-Adapter.md) |
