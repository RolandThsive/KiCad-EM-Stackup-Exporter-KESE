# 1819. ESP32-C6-EVB_Rev_A

Board 1,819 of the 3,123 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 17](../CorpusTestingPages/Corpus-Testing-17.md#1819-esp32-c6-evb_rev_a).

![ESP32-C6-EVB_Rev_A: stages 4 and 6 take 53% to 83% of a run. Simulation, GLB takes 14 s. Simulation, STEP takes 17 s. Simulation, STL takes 14 s. Simulation, OBJ takes 21 s. Visual, GLB takes 21 s. Visual, OBJ takes 26 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1819b_ESP32-C6-EVB_ESP32-C6-EVB-Rev-A/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.6 | 6.4 | 0.5&nbsp;ms | 4.3 | 0.2 | 0.6 | 0.2 | 13.8 |
| Simulation, STEP | 0.4 | 1.4 | 6.5 | 0.7&nbsp;ms | 4.4 | 3.6 | 0.6 | 0.2 | 17.2 |
| Simulation, STL | 0.4 | 1.4 | 6.4 | 0.5&nbsp;ms | 4.5 | 0.4 | 0.6 | 0.2 | 14.0 |
| Simulation, OBJ | 0.5 | 1.4 | 6.4 | 0.5&nbsp;ms | 4.5 | 7.0 | 0.6 | 0.3 | 20.6 |
| Visual, GLB | 0.5 | 1.5 | 6.3 | 0.6&nbsp;ms | 10.7 | 0.2 | 1.1 | 0.2 | 20.6 |
| Visual, OBJ | 0.5 | 1.5 | 6.6 | 2&nbsp;ms | 10.8 | 5.7 | 1.1 | 0.3 | 26.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [OLIMEX/ESP32-C6-EVB](https://github.com/OLIMEX/ESP32-C6-EVB)<br>Board: `ESP32-C6-EVB_Rev_A.kicad_pcb` |
|---|---|
| Folder | HARDWARE / Hardware-revision-A |
| Complexity | 252&nbsp;/&nbsp;1000 (size&nbsp;187, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 102, 1,162, 124 |
| Triangles,&nbsp;simulation | 1,271,824 in 99 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">543&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">237&nbsp;MB</td><td align="right">662&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">64&nbsp;MB</td><td align="right">551&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">134&nbsp;MB</td><td align="right">876&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">36&nbsp;MB</td><td align="right">767&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">108&nbsp;MB</td><td align="right">791&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1818. ESP32-C6-EVB_DIMM_Rev_A](b1818b_ESP32-C6-EVB_ESP32-C6-EVB-DIMM-Rev-A.md) | [1820. ESP32-DevKit-Lipo_Rev_A1](b1820b_ESP32-DevKit-LiPo_ESP32-DevKit-Lipo-Rev-A1.md) |
