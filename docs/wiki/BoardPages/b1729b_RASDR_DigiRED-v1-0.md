# 1729. DigiRED_v1.0

Board 1,729 of the 3,138 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 17](../CorpusTestingPages/Corpus-Testing-17.md#1729-digired_v10).

![DigiRED_v1.0: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 50 s. Simulation, STEP takes 59 s. Simulation, STL takes 51 s. Simulation, OBJ takes 79 s. Visual, GLB takes 67 s. Visual, OBJ takes 83 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1729b_RASDR_DigiRED-v1-0/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 5.7 | 19.7 | 1&nbsp;ms | 19.5 | 0.8 | 2.7 | 0.3 | 49.7 |
| Simulation, STEP | 0.8 | 5.7 | 19.4 | 1&nbsp;ms | 19.3 | 10.3 | 2.7 | 0.3 | 58.6 |
| Simulation, STL | 0.9 | 5.9 | 19.7 | 1&nbsp;ms | 19.9 | 1.6 | 2.8 | 0.3 | 51.0 |
| Simulation, OBJ | 0.9 | 6.0 | 19.8 | 0.7&nbsp;ms | 19.9 | 29.9 | 2.7 | 0.3 | 79.5 |
| Visual, GLB | 0.9 | 5.8 | 19.7 | 0.7&nbsp;ms | 36.3 | 0.4 | 3.6 | 0.3 | 67.1 |
| Visual, OBJ | 0.9 | 5.8 | 19.5 | 0.7&nbsp;ms | 36.3 | 16.6 | 3.3 | 0.2 | 82.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/RASDR](https://github.com/myriadrf/RASDR)<br>Board: `DigiRED_v1.0.kicad_pcb` |
|---|---|
| Folder | DigiRED / hardware / v1r3 / KiCAD |
| Complexity | 347&nbsp;/&nbsp;1000 (size&nbsp;302, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 239, 3,701, 600 |
| Triangles,&nbsp;simulation | 5,591,800 in 262 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">191&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">634&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">280&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">596&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">105&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">340&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1728. LMS8001_Companion](b1728b_LMS8001-Companion_hardware-3v2-KiCAD_LMS8001-Companion.md) | [1730. DigiRED](b1730b_RASDR_DigiRED.md) |
