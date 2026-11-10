# 23.6 Corpus Testing 6: Board-Folk To cheyao

Part 6 of 29 of [Corpus Testing](../Corpus-Testing.md): every board of these projects, six runs each, one file format a run, as [Corpus Testing](../Corpus-Testing.md) describes.

## 23.6.1 Commodore PC10 III

![Commodore PC10 III: stages 4 and 6 take 68% to 88% of a run. Simulation, GLB takes 20 min. Simulation, STEP takes 21 min. Simulation, STL takes 20 min. Visual, GLB takes 28 min. Visual, OBJ takes 22 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Commodore-PC10-III-Reproduction_312628-REV-5-7A_Commodore-PC10-III.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 72.9 | 90.2 | 534.8 | 4&nbsp;ms | 328.3 | 7.2 | 139.7 | 1.6 | 1174.7 |
| Simulation, STEP | 72.0 | 85.7 | 521.9 | 4&nbsp;ms | 330.3 | 92.3 | 145.4 | 1.9 | 1249.4 |
| Simulation, STL | 80.3 | 94.4 | 531.7 | 5&nbsp;ms | 310.5 | 14.5 | 141.0 | 2.0 | 1174.4 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB | 74.2 | 91.4 | 545.4 | 6&nbsp;ms | 941.9 | 4.3 | 37.8 | 1.6 | 1696.6 |
| Visual, OBJ | 57.0 | 67.9 | 447.4 | 2&nbsp;ms | 663.1 | 79.1 | 28.6 | 0.9 | 1344.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Commodore-PC10-III-Reproduction](https://github.com/Board-Folk/Commodore-PC10-III-Reproduction)<br>Board: `Commodore PC10 III.kicad_pcb` |
|---|---|
| Folder | 312628-REV-5.7A |
| Complexity | 384&nbsp;/&nbsp;1000 (size&nbsp;299, features&nbsp;85) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 397, 28,255, 1,516 |
| Triangles,&nbsp;simulation | 24,329,594 in 614 parts |
| Verifier | Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Run&nbsp;again | Visual, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">883&nbsp;MB</td><td align="right">6.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">4.9&nbsp;GB</td><td align="right">9.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.2&nbsp;GB</td><td align="right">7.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">618&nbsp;MB</td><td align="right">10.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">2.0&nbsp;GB</td><td align="right">13&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.2 Commodore PC10 III

![Commodore PC10 III: stages 4 and 6 take 54% to 87% of a run. Simulation, GLB takes 4 min. Simulation, STEP takes 5 min. Simulation, STL takes 4 min. Simulation, OBJ takes 6 min. Visual, GLB takes 6 min. Visual, OBJ takes 8 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Commodore-PC10-III-Reproduction_312628-REV-6C_Commodore-PC10-III.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 9.4 | 18.5 | 105.7 | 2&nbsp;ms | 78.0 | 3.4 | 11.7 | 0.6 | 227.3 |
| Simulation, STEP | 9.2 | 17.9 | 104.4 | 2&nbsp;ms | 77.8 | 57.1 | 13.1 | 0.7 | 280.3 |
| Simulation, STL | 9.5 | 18.1 | 101.6 | 3&nbsp;ms | 74.4 | 8.0 | 11.7 | 0.7 | 224.1 |
| Simulation, OBJ | 9.1 | 18.9 | 108.1 | 4&nbsp;ms | 80.7 | 118.2 | 13.9 | 1.1 | 349.9 |
| Visual, GLB | 8.8 | 17.8 | 102.3 | 2&nbsp;ms | 236.8 | 2.4 | 19.8 | 0.5 | 388.4 |
| Visual, OBJ | 10.4 | 18.4 | 105.0 | 3&nbsp;ms | 242.4 | 82.6 | 18.9 | 0.5 | 478.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Commodore-PC10-III-Reproduction](https://github.com/Board-Folk/Commodore-PC10-III-Reproduction)<br>Board: `Commodore PC10 III.kicad_pcb` |
|---|---|
| Folder | 312628-REV-6C |
| Complexity | 390&nbsp;/&nbsp;1000 (size&nbsp;305, features&nbsp;85) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 406, 41,077, 1,838 |
| Triangles,&nbsp;simulation | 18,353,260 in 652 parts |
| Verifier | PASS in all six runs |
| Run&nbsp;again | Simulation, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">619&nbsp;MB</td><td align="right">5.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">3.0&nbsp;GB</td><td align="right">6.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">918&nbsp;MB</td><td align="right">5.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">2.0&nbsp;GB</td><td align="right">12&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">414&nbsp;MB</td><td align="right">6.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.3&nbsp;GB</td><td align="right">8.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.3 CPC464-2MINIITX

![CPC464-2MINIITX: stages 4 and 6 take 56% to 85% of a run. Simulation, GLB takes 67 s. Simulation, STEP takes 84 s. Simulation, STL takes 67 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINIITX.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 5.4 | 30.3 | 2&nbsp;ms | 25.5 | 1.2 | 3.4 | 0.4 | 67.1 |
| Simulation, STEP | 1.0 | 5.6 | 30.9 | 2&nbsp;ms | 25.3 | 17.7 | 3.4 | 0.4 | 84.4 |
| Simulation, STL | 1.0 | 5.4 | 29.9 | 2&nbsp;ms | 24.7 | 2.2 | 3.6 | 0.4 | 67.0 |
| Simulation, OBJ | 1.0 | 5.3 | 30.8 | 2&nbsp;ms | 24.4 | 34.3 | 3.3 | 0.4 | 99.5 |
| Visual, GLB | 1.0 | 5.3 | 30.2 | 2&nbsp;ms | 61.3 | 0.7 | 8.6 | 0.3 | 107.3 |
| Visual, OBJ | 1.1 | 5.6 | 31.1 | 2&nbsp;ms | 57.0 | 20.8 | 8.2 | 0.3 | 124.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINIITX.kicad_pcb` |
|---|---|
| Folder | Archive / MINIITXv1.2 / Kicad |
| Complexity | 364&nbsp;/&nbsp;1000 (size&nbsp;274, features&nbsp;90) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>copper drawings, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 239, 8,256, 638 |
| Triangles,&nbsp;simulation | 6,998,502 in 372 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">240&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.2&nbsp;GB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">350&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">752&nbsp;MB</td><td align="right">4.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">160&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">511&nbsp;MB</td><td align="right">3.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.4 CPC464-2MINI

![CPC464-2MINI: stages 4 and 6 take 55% to 84% of a run. Simulation, GLB takes 44 s. Simulation, STEP takes 53 s. Simulation, STL takes 44 s. Simulation, OBJ takes 66 s. Visual, GLB takes 74 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_Archive-v1-Kicad_CPC464-2MINI.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 4.0 | 18.8 | 0.9&nbsp;ms | 17.1 | 0.7 | 2.3 | 0.4 | 44.3 |
| Simulation, STEP | 0.8 | 3.7 | 18.0 | 1&nbsp;ms | 16.2 | 11.8 | 2.1 | 0.3 | 53.0 |
| Simulation, STL | 0.8 | 3.9 | 18.0 | 0.9&nbsp;ms | 17.1 | 1.5 | 2.3 | 0.3 | 43.8 |
| Simulation, OBJ | 0.9 | 3.8 | 18.9 | 0.7&nbsp;ms | 17.2 | 21.9 | 2.5 | 0.3 | 65.5 |
| Visual, GLB | 0.8 | 3.9 | 19.8 | 0.9&nbsp;ms | 42.4 | 0.4 | 6.6 | 0.3 | 74.3 |
| Visual, OBJ | 1.0 | 4.1 | 20.6 | 1&nbsp;ms | 52.1 | 18.0 | 7.2 | 0.4 | 103.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINI.kicad_pcb` |
|---|---|
| Folder | Archive / v1 / Kicad |
| Complexity | 300&nbsp;/&nbsp;1000 (size&nbsp;215, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 127, 5,893, 450 |
| Triangles,&nbsp;simulation | 4,314,836 in 201 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">146&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">675&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">216&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">455&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">103&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">325&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.5 CPC464-2MINIDDI3ADAPT

![CPC464-2MINIDDI3ADAPT: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 3.5 s. Simulation, STEP takes 4.7 s. Simulation, STL takes 3.4 s. Simulation, OBJ takes 5.0 s. Visual, GLB takes 4.5 s. Visual, OBJ takes 5.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINIDDI3ADAPT.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.4 | 0.2&nbsp;ms | 1.2 | 53&nbsp;ms | 0.2 | 0.3 | 3.5 |
| Simulation, STEP | 0.1 | 0.2 | 1.4 | 0.2&nbsp;ms | 1.2 | 1.4 | 0.2 | 0.2 | 4.7 |
| Simulation, STL | 0.1 | 0.3 | 1.4 | 0.2&nbsp;ms | 1.2 | 90&nbsp;ms | 0.2 | 0.2 | 3.4 |
| Simulation, OBJ | 0.1 | 0.2 | 1.3 | 0.3&nbsp;ms | 1.2 | 1.7 | 0.2 | 0.2 | 5.0 |
| Visual, GLB | 0.1 | 0.2 | 1.3 | 0.4&nbsp;ms | 2.4 | 29&nbsp;ms | 0.2 | 0.2 | 4.5 |
| Visual, OBJ | 0.1 | 0.2 | 1.2 | 0.2&nbsp;ms | 2.5 | 1.0 | 0.2 | 0.2 | 5.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINIDDI3ADAPT.kicad_pcb` |
|---|---|
| Folder | Expansions / MINIDDI / Extras / MINIDDI3ADAPT / Kicad |
| Complexity | 150&nbsp;/&nbsp;1000 (size&nbsp;90, features&nbsp;60) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 41, 0 |
| Triangles,&nbsp;simulation | 332,256 in 30 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">241&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">47&nbsp;MB</td><td align="right">281&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">17&nbsp;MB</td><td align="right">255&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">33&nbsp;MB</td><td align="right">245&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">6.2&nbsp;MB</td><td align="right">238&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">18&nbsp;MB</td><td align="right">237&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.6 CPC464-2MINIDDI

![CPC464-2MINIDDI: stages 4 and 6 take 53% to 86% of a run. Simulation, GLB takes 25 s. Simulation, STEP takes 31 s. Simulation, STL takes 25 s. Simulation, OBJ takes 37 s. Visual, GLB takes 37 s. Visual, OBJ takes 48 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINIDDI.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 2.0 | 10.7 | 1&nbsp;ms | 9.3 | 0.4 | 1.4 | 0.3 | 24.6 |
| Simulation, STEP | 0.5 | 2.0 | 10.9 | 0.9&nbsp;ms | 8.3 | 7.9 | 1.5 | 0.3 | 31.4 |
| Simulation, STL | 0.6 | 2.3 | 11.2 | 0.8&nbsp;ms | 8.8 | 0.7 | 1.3 | 0.4 | 25.2 |
| Simulation, OBJ | 0.6 | 2.1 | 11.3 | 0.7&nbsp;ms | 8.5 | 13.2 | 1.3 | 0.3 | 37.3 |
| Visual, GLB | 0.6 | 1.8 | 10.9 | 0.6&nbsp;ms | 20.8 | 0.2 | 2.3 | 0.2 | 36.8 |
| Visual, OBJ | 0.5 | 1.8 | 11.0 | 0.9&nbsp;ms | 20.7 | 10.9 | 3.0 | 0.3 | 48.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINIDDI.kicad_pcb` |
|---|---|
| Folder | Expansions / MINIDDI / Kicad |
| Complexity | 263&nbsp;/&nbsp;1000 (size&nbsp;188, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 59, 1,939, 128 |
| Triangles,&nbsp;simulation | 2,016,044 in 143 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">68&nbsp;MB</td><td align="right">794&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">321&nbsp;MB</td><td align="right">906&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">101&nbsp;MB</td><td align="right">844&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">208&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">49&nbsp;MB</td><td align="right">912&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">151&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.7 CPC464-2MINIDOCK

![CPC464-2MINIDOCK: stages 4 and 6 take 54% to 86% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 29 s. Simulation, STL takes 23 s. Simulation, OBJ takes 34 s. Visual, GLB takes 29 s. Visual, OBJ takes 38 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINIDOCK.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.4 | 10.0 | 0.6&nbsp;ms | 9.6 | 0.4 | 1.1 | 0.3 | 23.2 |
| Simulation, STEP | 0.4 | 1.6 | 9.8 | 0.6&nbsp;ms | 8.3 | 7.0 | 1.0 | 0.3 | 28.5 |
| Simulation, STL | 0.5 | 1.4 | 10.3 | 0.4&nbsp;ms | 8.5 | 0.6 | 1.1 | 0.3 | 22.6 |
| Simulation, OBJ | 0.4 | 1.6 | 10.3 | 0.4&nbsp;ms | 8.5 | 12.6 | 0.9 | 0.3 | 34.5 |
| Visual, GLB | 0.4 | 1.4 | 9.5 | 0.5&nbsp;ms | 15.8 | 0.2 | 1.8 | 0.3 | 29.3 |
| Visual, OBJ | 0.4 | 1.5 | 10.3 | 0.5&nbsp;ms | 15.9 | 7.6 | 2.3 | 0.2 | 38.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINIDOCK.kicad_pcb` |
|---|---|
| Folder | Expansions / MINIDOCK / Kicad |
| Complexity | 245&nbsp;/&nbsp;1000 (size&nbsp;160, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 13, 1,020, 14 |
| Triangles,&nbsp;simulation | 1,908,702 in 61 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">63&nbsp;MB</td><td align="right">697&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">261&nbsp;MB</td><td align="right">837&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">95&nbsp;MB</td><td align="right">706&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">196&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">37&nbsp;MB</td><td align="right">846&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">113&nbsp;MB</td><td align="right">943&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.8 CPC464-2MINI-EDGE

![CPC464-2MINI-EDGE: stages 4 and 6 take 48% to 83% of a run. Simulation, GLB takes 3.4 s. Simulation, STEP takes 4.4 s. Simulation, STL takes 3.3 s. Simulation, OBJ takes 5.2 s. Visual, GLB takes 4.8 s. Visual, OBJ takes 5.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINI-EDGE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 1.4 | 0.3&nbsp;ms | 1.1 | 54&nbsp;ms | 0.2 | 0.3 | 3.4 |
| Simulation, STEP | 0.1 | 0.3 | 1.3 | 0.2&nbsp;ms | 1.1 | 1.2 | 0.2 | 0.2 | 4.4 |
| Simulation, STL | 0.1 | 0.2 | 1.3 | 0.3&nbsp;ms | 1.1 | 0.1 | 0.2 | 0.2 | 3.3 |
| Simulation, OBJ | 0.1 | 0.3 | 1.3 | 0.3&nbsp;ms | 1.2 | 1.9 | 0.2 | 0.2 | 5.2 |
| Visual, GLB | 0.1 | 0.2 | 1.3 | 0.3&nbsp;ms | 2.8 | 34&nbsp;ms | 0.2 | 0.2 | 4.8 |
| Visual, OBJ | 0.1 | 0.2 | 1.3 | 0.3&nbsp;ms | 2.6 | 1.0 | 0.2 | 0.3 | 5.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINI-EDGE.kicad_pcb` |
|---|---|
| Folder | Expansions / MINIEDGE / Kicad |
| Complexity | 185&nbsp;/&nbsp;1000 (size&nbsp;120, features&nbsp;65) |
| KESE&nbsp;features | through vias, filled zones,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 253, 3 |
| Triangles,&nbsp;simulation | 286,622 in 60 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.7&nbsp;MB</td><td align="right">230&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">41&nbsp;MB</td><td align="right">246&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">228&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">29&nbsp;MB</td><td align="right">244&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">6.1&nbsp;MB</td><td align="right">251&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">18&nbsp;MB</td><td align="right">248&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.9 CPC464-2MINIPS2

![CPC464-2MINIPS2: stages 4 and 6 take 48% to 80% of a run. Simulation, GLB takes 5.7 s. Simulation, STEP takes 7.7 s. Simulation, STL takes 6.0 s. Simulation, OBJ takes 7.8 s. Visual, GLB takes 8.5 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINIPS2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.6 | 2.1 | 0.6&nbsp;ms | 1.9 | 98&nbsp;ms | 0.4 | 0.3 | 5.7 |
| Simulation, STEP | 0.3 | 0.5 | 2.2 | 0.5&nbsp;ms | 2.0 | 2.0 | 0.4 | 0.3 | 7.7 |
| Simulation, STL | 0.3 | 0.6 | 2.3 | 0.7&nbsp;ms | 2.0 | 0.1 | 0.4 | 0.3 | 6.0 |
| Simulation, OBJ | 0.2 | 0.5 | 2.0 | 0.6&nbsp;ms | 1.8 | 2.7 | 0.3 | 0.3 | 7.8 |
| Visual, GLB | 0.2 | 0.5 | 2.0 | 0.5&nbsp;ms | 4.8 | 77&nbsp;ms | 0.6 | 0.3 | 8.5 |
| Visual, OBJ | 0.2 | 0.5 | 1.8 | 0.5&nbsp;ms | 4.9 | 2.1 | 0.9 | 0.3 | 10.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINIPS2.kicad_pcb` |
|---|---|
| Folder | Expansions / MINIPS2 / Kicad |
| Complexity | 309&nbsp;/&nbsp;1000 (size&nbsp;199, features&nbsp;110) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 17, 440, 47 |
| Triangles,&nbsp;simulation | 418,416 in 75 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">266&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">68&nbsp;MB</td><td align="right">315&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">21&nbsp;MB</td><td align="right">292&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">42&nbsp;MB</td><td align="right">336&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">343&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">34&nbsp;MB</td><td align="right">336&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.10 CPC464-2MINIRS232C

![CPC464-2MINIRS232C: stages 4 and 6 take 53% to 86% of a run. Simulation, GLB takes 18 s. Simulation, STEP takes 25 s. Simulation, STL takes 20 s. Simulation, OBJ takes 30 s. Visual, GLB takes 30 s. Visual, OBJ takes 37 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINIRS232C.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.7 | 8.7 | 0.7&nbsp;ms | 6.2 | 0.3 | 0.9 | 0.2 | 18.4 |
| Simulation, STEP | 0.4 | 1.5 | 9.1 | 0.7&nbsp;ms | 6.9 | 5.6 | 0.9 | 0.3 | 24.8 |
| Simulation, STL | 0.4 | 1.5 | 8.8 | 0.5&nbsp;ms | 6.8 | 0.6 | 1.0 | 0.3 | 19.5 |
| Simulation, OBJ | 0.4 | 1.6 | 9.2 | 0.5&nbsp;ms | 6.9 | 10.9 | 1.0 | 0.3 | 30.3 |
| Visual, GLB | 0.5 | 1.6 | 9.5 | 0.7&nbsp;ms | 16.2 | 0.2 | 1.7 | 0.2 | 29.9 |
| Visual, OBJ | 0.5 | 1.5 | 9.0 | 0.9&nbsp;ms | 15.3 | 7.8 | 2.3 | 0.3 | 36.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINIRS232C.kicad_pcb` |
|---|---|
| Folder | Expansions / MINIRS232C / Kicad |
| Complexity | 255&nbsp;/&nbsp;1000 (size&nbsp;180, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 39, 1,501, 104 |
| Triangles,&nbsp;simulation | 1,751,162 in 121 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">59&nbsp;MB</td><td align="right">700&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">268&nbsp;MB</td><td align="right">814&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">88&nbsp;MB</td><td align="right">754&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">180&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">42&nbsp;MB</td><td align="right">871&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">127&nbsp;MB</td><td align="right">924&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.11 CPC464-2MINIUSIFACII

![CPC464-2MINIUSIFACII: stages 4 and 6 take 52% to 85% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 16 s. Simulation, STL takes 13 s. Simulation, OBJ takes 20 s. Visual, GLB takes 20 s. Visual, OBJ takes 24 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINIUSIFACII.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.0 | 6.2 | 0.6&nbsp;ms | 4.4 | 0.2 | 0.6 | 0.3 | 13.0 |
| Simulation, STEP | 0.3 | 1.1 | 5.9 | 0.8&nbsp;ms | 4.3 | 3.7 | 0.7 | 0.3 | 16.3 |
| Simulation, STL | 0.3 | 1.0 | 6.2 | 0.6&nbsp;ms | 4.3 | 0.4 | 0.7 | 0.3 | 13.2 |
| Simulation, OBJ | 0.3 | 1.1 | 6.2 | 0.7&nbsp;ms | 4.4 | 7.3 | 0.7 | 0.3 | 20.1 |
| Visual, GLB | 0.4 | 1.1 | 6.5 | 0.7&nbsp;ms | 10.2 | 0.1 | 1.0 | 0.2 | 19.6 |
| Visual, OBJ | 0.3 | 1.0 | 6.0 | 0.5&nbsp;ms | 9.9 | 4.9 | 1.4 | 0.2 | 23.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINIUSIFACII.kicad_pcb` |
|---|---|
| Folder | Expansions / MINIUSIFACII / Kicad |
| Complexity | 242&nbsp;/&nbsp;1000 (size&nbsp;167, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 29, 860, 43 |
| Triangles,&nbsp;simulation | 1,270,196 in 101 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">43&nbsp;MB</td><td align="right">531&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">190&nbsp;MB</td><td align="right">628&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">64&nbsp;MB</td><td align="right">573&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">129&nbsp;MB</td><td align="right">875&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">29&nbsp;MB</td><td align="right">770&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">87&nbsp;MB</td><td align="right">707&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.12 CPC-40007AdapterLM1117

![CPC-40007AdapterLM1117: stages 4 and 6 take 49% to 83% of a run. Simulation, GLB takes 6.0 s. Simulation, STEP takes 7.5 s. Simulation, STL takes 6.0 s. Simulation, OBJ takes 9.1 s. Visual, GLB takes 8.7 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC-40007AdapterLM1117.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 2.6 | 0.4&nbsp;ms | 2.0 | 93&nbsp;ms | 0.4 | 0.2 | 6.0 |
| Simulation, STEP | 0.2 | 0.5 | 2.5 | 0.4&nbsp;ms | 1.9 | 1.8 | 0.4 | 0.3 | 7.5 |
| Simulation, STL | 0.2 | 0.5 | 2.6 | 0.5&nbsp;ms | 1.9 | 0.1 | 0.4 | 0.2 | 6.0 |
| Simulation, OBJ | 0.2 | 0.5 | 2.5 | 0.3&nbsp;ms | 1.9 | 3.3 | 0.4 | 0.2 | 9.1 |
| Visual, GLB | 0.2 | 0.6 | 2.6 | 0.5&nbsp;ms | 4.6 | 64&nbsp;ms | 0.4 | 0.2 | 8.7 |
| Visual, OBJ | 0.2 | 0.5 | 2.6 | 0.3&nbsp;ms | 4.7 | 2.3 | 0.4 | 0.2 | 11.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC-40007AdapterLM1117.kicad_pcb` |
|---|---|
| Folder | v4.1 / Extras / CPC-40007Adapter / Kicad |
| Complexity | 224&nbsp;/&nbsp;1000 (size&nbsp;149, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 11, 506, 36 |
| Triangles,&nbsp;simulation | 558,168 in 51 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">319&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">92&nbsp;MB</td><td align="right">354&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">28&nbsp;MB</td><td align="right">321&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">56&nbsp;MB</td><td align="right">394&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">394&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">40&nbsp;MB</td><td align="right">392&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.13 CPC464-2MINICAS1

![CPC464-2MINICAS1: stages 4 and 6 take 54% to 83% of a run. Simulation, GLB takes 7.2 s. Simulation, STEP takes 9.0 s. Simulation, STL takes 7.3 s. Simulation, OBJ takes 11 s. Visual, GLB takes 9.9 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINICAS1.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 3.1 | 0.6&nbsp;ms | 2.7 | 0.1 | 0.4 | 0.2 | 7.2 |
| Simulation, STEP | 0.1 | 0.5 | 3.1 | 0.3&nbsp;ms | 2.6 | 2.0 | 0.4 | 0.2 | 9.0 |
| Simulation, STL | 0.1 | 0.5 | 3.2 | 0.3&nbsp;ms | 2.6 | 0.2 | 0.4 | 0.2 | 7.3 |
| Simulation, OBJ | 0.1 | 0.5 | 3.1 | 0.5&nbsp;ms | 2.7 | 3.7 | 0.3 | 0.2 | 10.8 |
| Visual, GLB | 0.1 | 0.5 | 3.2 | 0.2&nbsp;ms | 5.1 | 77&nbsp;ms | 0.7 | 0.2 | 9.9 |
| Visual, OBJ | 0.1 | 0.5 | 3.2 | 0.4&nbsp;ms | 4.7 | 2.2 | 0.8 | 0.2 | 11.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINICAS1.kicad_pcb` |
|---|---|
| Folder | v4.1 / Extras / MINICAS1 / Kicad |
| Complexity | 218&nbsp;/&nbsp;1000 (size&nbsp;163, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 19, 952, 30 |
| Triangles,&nbsp;simulation | 939,968 in 44 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">432&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">132&nbsp;MB</td><td align="right">491&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">47&nbsp;MB</td><td align="right">413&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">94&nbsp;MB</td><td align="right">668&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">505&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">57&nbsp;MB</td><td align="right">500&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.14 CPC464-2MINITapeAdapter

![CPC464-2MINITapeAdapter: stages 4 and 6 take 50% to 82% of a run. Simulation, GLB takes 4.1 s. Simulation, STEP takes 5.3 s. Simulation, STL takes 4.0 s. Simulation, OBJ takes 5.8 s. Visual, GLB takes 6.0 s. Visual, OBJ takes 7.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_CPC464-2MINITapeAdapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.6 | 0.4&nbsp;ms | 1.3 | 72&nbsp;ms | 0.2 | 0.3 | 4.1 |
| Simulation, STEP | 0.2 | 0.3 | 1.4 | 0.3&nbsp;ms | 1.3 | 1.6 | 0.2 | 0.2 | 5.3 |
| Simulation, STL | 0.2 | 0.4 | 1.5 | 0.2&nbsp;ms | 1.4 | 73&nbsp;ms | 0.2 | 0.3 | 4.0 |
| Simulation, OBJ | 0.2 | 0.3 | 1.5 | 0.2&nbsp;ms | 1.5 | 1.8 | 0.2 | 0.3 | 5.8 |
| Visual, GLB | 0.2 | 0.3 | 1.5 | 0.2&nbsp;ms | 3.4 | 40&nbsp;ms | 0.3 | 0.2 | 6.0 |
| Visual, OBJ | 0.2 | 0.4 | 1.7 | 0.3&nbsp;ms | 3.1 | 1.3 | 0.3 | 0.3 | 7.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINITapeAdapter.kicad_pcb` |
|---|---|
| Folder | v4.1 / Extras / TapeAdapter / Kicad |
| Complexity | 176&nbsp;/&nbsp;1000 (size&nbsp;116, features&nbsp;60) |
| KESE&nbsp;features | slotted holes, filled zones,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 13, 75, 0 |
| Triangles,&nbsp;simulation | 278,362 in 28 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.5&nbsp;MB</td><td align="right">246&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">42&nbsp;MB</td><td align="right">250&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">246&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">28&nbsp;MB</td><td align="right">239&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">6.6&nbsp;MB</td><td align="right">248&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">19&nbsp;MB</td><td align="right">249&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.15 CPC464-2MINI

![CPC464-2MINI: stages 4 and 6 take 55% to 86% of a run. Simulation, GLB takes 69 s. Simulation, STEP takes 87 s. Simulation, STL takes 73 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_v4-1-Kicad_CPC464-2MINI.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.2 | 6.0 | 31.4 | 2&nbsp;ms | 24.9 | 1.2 | 3.9 | 0.4 | 69.0 |
| Simulation, STEP | 1.2 | 6.1 | 31.2 | 1&nbsp;ms | 25.2 | 19.0 | 4.2 | 0.5 | 87.4 |
| Simulation, STL | 1.1 | 6.1 | 32.1 | 2&nbsp;ms | 27.0 | 2.2 | 4.0 | 0.4 | 73.0 |
| Simulation, OBJ | 1.2 | 6.1 | 31.8 | 1&nbsp;ms | 25.9 | 35.3 | 3.8 | 0.4 | 104.6 |
| Visual, GLB | 1.1 | 5.8 | 31.3 | 2&nbsp;ms | 62.3 | 0.8 | 7.2 | 0.3 | 108.8 |
| Visual, OBJ | 1.4 | 6.2 | 32.5 | 1&nbsp;ms | 61.1 | 27.0 | 9.4 | 0.3 | 137.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINI.kicad_pcb` |
|---|---|
| Folder | v4.1 / Kicad |
| Complexity | 346&nbsp;/&nbsp;1000 (size&nbsp;261, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 145, 7,612, 738 |
| Triangles,&nbsp;simulation | 5,887,166 in 239 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">199&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">944&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">294&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">623&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">145&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">462&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.16 CPC464-2MINI

![CPC464-2MINI: stages 4 and 6 take 58% to 86% of a run. Simulation, GLB takes 72 s. Simulation, STEP takes 89 s. Simulation, STL takes 73 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/CPC464-2MINI_v5-3-Kicad_CPC464-2MINI.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 5.7 | 31.3 | 1&nbsp;ms | 29.1 | 0.9 | 4.0 | 0.4 | 72.4 |
| Simulation, STEP | 1.1 | 5.6 | 30.9 | 1&nbsp;ms | 29.8 | 17.1 | 3.7 | 0.3 | 88.6 |
| Simulation, STL | 1.0 | 5.4 | 31.4 | 2&nbsp;ms | 28.9 | 2.3 | 4.1 | 0.3 | 73.3 |
| Simulation, OBJ | 1.1 | 5.7 | 31.3 | 2&nbsp;ms | 28.5 | 31.8 | 3.8 | 0.3 | 102.6 |
| Visual, GLB | 1.2 | 5.4 | 30.9 | 1&nbsp;ms | 71.1 | 0.7 | 9.2 | 0.3 | 118.9 |
| Visual, OBJ | 1.1 | 5.7 | 30.8 | 1&nbsp;ms | 70.3 | 23.9 | 9.2 | 0.3 | 141.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/CPC464-2MINI](https://github.com/Board-Folk/CPC464-2MINI)<br>Board: `CPC464-2MINI.kicad_pcb` |
|---|---|
| Folder | v5.3 / Kicad |
| Complexity | 357&nbsp;/&nbsp;1000 (size&nbsp;272, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 157, 7,238, 705 |
| Triangles,&nbsp;simulation | 5,789,680 in 321 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">196&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">937&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">290&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">614&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">149&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">478&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.17 EinsteinTC01

![EinsteinTC01: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Einstein-TC-01_Archive-MainBoard-v1-1-Kicad_EinsteinTC01.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.2 | 8.3 | 50.7 | 3&nbsp;ms | 39.4 | 1.8 | 5.7 | 0.4 | 110.5 |
| Simulation, STEP | 4.3 | 8.3 | 52.0 | 3&nbsp;ms | 39.6 | 26.0 | 5.5 | 0.4 | 136.1 |
| Simulation, STL | 4.1 | 8.4 | 49.1 | 2&nbsp;ms | 39.3 | 4.6 | 5.6 | 0.4 | 111.5 |
| Simulation, OBJ | 4.2 | 8.5 | 49.8 | 3&nbsp;ms | 39.7 | 63.9 | 5.9 | 0.4 | 172.4 |
| Visual, GLB | 4.1 | 8.5 | 50.3 | 2&nbsp;ms | 97.8 | 1.0 | 13.3 | 0.3 | 175.4 |
| Visual, OBJ | 4.5 | 8.4 | 52.6 | 2&nbsp;ms | 95.6 | 32.9 | 13.3 | 0.4 | 207.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Einstein-TC-01](https://github.com/Board-Folk/Einstein-TC-01)<br>Board: `EinsteinTC01.kicad_pcb` |
|---|---|
| Folder | Archive / MainBoard / v1.1 / Kicad |
| Complexity | 309&nbsp;/&nbsp;1000 (size&nbsp;234, features&nbsp;75) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, filled zones,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 346, 9,719, 769 |
| Triangles,&nbsp;simulation | 11,902,236 in 528 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">398&nbsp;MB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.7&nbsp;GB</td><td align="right">4.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">595&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.3&nbsp;GB</td><td align="right">7.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">238&nbsp;MB</td><td align="right">3.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">765&nbsp;MB</td><td align="right">5.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.18 EinsteinTC01PS2

![EinsteinTC01PS2: stages 4 and 6 take 51% to 87% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 15 s. Simulation, STL takes 12 s. Simulation, OBJ takes 17 s. Visual, GLB takes 15 s. Visual, OBJ takes 18 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Einstein-TC-01_EinsteinTC01PS2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.9 | 5.1 | 0.5&nbsp;ms | 3.6 | 0.2 | 0.6 | 0.3 | 10.9 |
| Simulation, STEP | 0.2 | 0.9 | 5.0 | 0.6&nbsp;ms | 4.1 | 3.5 | 0.6 | 0.3 | 14.6 |
| Simulation, STL | 0.3 | 0.8 | 5.2 | 0.9&nbsp;ms | 4.1 | 0.3 | 0.6 | 0.3 | 11.6 |
| Simulation, OBJ | 0.2 | 0.8 | 4.9 | 0.8&nbsp;ms | 3.5 | 6.2 | 0.6 | 0.3 | 16.6 |
| Visual, GLB | 0.2 | 0.9 | 5.3 | 0.8&nbsp;ms | 7.5 | 86&nbsp;ms | 0.5 | 0.3 | 14.7 |
| Visual, OBJ | 0.2 | 0.7 | 5.0 | 1&nbsp;ms | 7.7 | 3.5 | 0.6 | 0.2 | 18.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Einstein-TC-01](https://github.com/Board-Folk/Einstein-TC-01)<br>Board: `EinsteinTC01PS2.kicad_pcb` |
|---|---|
| Folder | Expansions / EinsteinTC01PS2 / Kicad |
| Complexity | 183&nbsp;/&nbsp;1000 (size&nbsp;153, features&nbsp;30) |
| KESE&nbsp;features | slotted holes, rounded,<br>trapezoid or chamfered pads,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 22, 500, 0 |
| Triangles,&nbsp;simulation | 898,748 in 71 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">374&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">132&nbsp;MB</td><td align="right">479&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">45&nbsp;MB</td><td align="right">395&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">91&nbsp;MB</td><td align="right">653&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">476&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">50&nbsp;MB</td><td align="right">484&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.19 EinsteinTC01PS2Mini

![EinsteinTC01PS2Mini: stages 4 and 6 take 55% to 84% of a run. Simulation, GLB takes 9.4 s. Simulation, STEP takes 11 s. Simulation, STL takes 9.3 s. Simulation, OBJ takes 14 s. Visual, GLB takes 13 s. Visual, OBJ takes 15 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Einstein-TC-01_EinsteinTC01PS2Mini.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 4.1 | 0.7&nbsp;ms | 3.5 | 0.2 | 0.5 | 0.3 | 9.4 |
| Simulation, STEP | 0.2 | 0.6 | 4.0 | 0.6&nbsp;ms | 3.3 | 2.5 | 0.5 | 0.3 | 11.4 |
| Simulation, STL | 0.2 | 0.6 | 4.1 | 0.5&nbsp;ms | 3.3 | 0.4 | 0.5 | 0.2 | 9.3 |
| Simulation, OBJ | 0.2 | 0.6 | 4.1 | 0.6&nbsp;ms | 3.4 | 4.6 | 0.5 | 0.2 | 13.6 |
| Visual, GLB | 0.2 | 0.7 | 4.0 | 0.6&nbsp;ms | 6.6 | 91&nbsp;ms | 0.9 | 0.2 | 12.7 |
| Visual, OBJ | 0.2 | 0.6 | 4.0 | 0.5&nbsp;ms | 6.4 | 2.7 | 0.8 | 0.3 | 14.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Einstein-TC-01](https://github.com/Board-Folk/Einstein-TC-01)<br>Board: `EinsteinTC01PS2Mini.kicad_pcb` |
|---|---|
| Folder | Expansions / EinsteinTC01PS2Mini / Kicad |
| Complexity | 198&nbsp;/&nbsp;1000 (size&nbsp;148, features&nbsp;50) |
| KESE&nbsp;features | slotted holes, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 18, 430, 0 |
| Triangles,&nbsp;simulation | 943,244 in 72 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">426&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">130&nbsp;MB</td><td align="right">493&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">47&nbsp;MB</td><td align="right">434&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">94&nbsp;MB</td><td align="right">652&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">500&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">57&nbsp;MB</td><td align="right">537&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.20 TC01AtariJoystick

![TC01AtariJoystick: stages 4 and 6 take 51% to 84% of a run. Simulation, GLB takes 5.0 s. Simulation, STEP takes 6.3 s. Simulation, STL takes 4.9 s. Simulation, OBJ takes 7.6 s. Visual, GLB takes 7.2 s. Visual, OBJ takes 7.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Einstein-TC-01_TC01AtariJoystick.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.3 | 2.2 | 0.3&nbsp;ms | 1.7 | 85&nbsp;ms | 0.3 | 0.2 | 5.0 |
| Simulation, STEP | 0.1 | 0.3 | 2.2 | 0.3&nbsp;ms | 1.6 | 1.6 | 0.3 | 0.2 | 6.3 |
| Simulation, STL | 0.1 | 0.3 | 2.0 | 0.2&nbsp;ms | 1.7 | 0.1 | 0.3 | 0.2 | 4.9 |
| Simulation, OBJ | 0.1 | 0.3 | 2.2 | 0.4&nbsp;ms | 1.7 | 2.7 | 0.3 | 0.2 | 7.6 |
| Visual, GLB | 0.2 | 0.4 | 2.9 | 0.4&nbsp;ms | 3.2 | 39&nbsp;ms | 0.3 | 0.2 | 7.2 |
| Visual, OBJ | 0.1 | 0.3 | 2.2 | 0.3&nbsp;ms | 3.2 | 1.4 | 0.3 | 0.2 | 7.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Einstein-TC-01](https://github.com/Board-Folk/Einstein-TC-01)<br>Board: `TC01AtariJoystick.kicad_pcb` |
|---|---|
| Folder | Expansions / TC01AtariJoystick / Kicad |
| Complexity | 191&nbsp;/&nbsp;1000 (size&nbsp;131, features&nbsp;60) |
| KESE&nbsp;features | filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 10, 219, 0 |
| Triangles,&nbsp;simulation | 503,944 in 29 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">287&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">68&nbsp;MB</td><td align="right">334&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">25&nbsp;MB</td><td align="right">284&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">50&nbsp;MB</td><td align="right">377&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">9.4&nbsp;MB</td><td align="right">333&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">28&nbsp;MB</td><td align="right">327&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.21 TC02Mini

![TC02Mini: stages 4 and 6 take 53% to 86% of a run. Simulation, GLB takes 32 s. Simulation, STEP takes 37 s. Simulation, STL takes 30 s. Simulation, OBJ takes 45 s. Visual, GLB takes 42 s. Visual, OBJ takes 52 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Einstein-TC-01_TC02Mini.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 2.4 | 15.2 | 1&nbsp;ms | 11.2 | 0.5 | 2.0 | 0.3 | 32.2 |
| Simulation, STEP | 0.5 | 2.4 | 13.3 | 0.8&nbsp;ms | 10.3 | 8.3 | 1.8 | 0.3 | 36.9 |
| Simulation, STL | 0.6 | 2.4 | 13.4 | 0.8&nbsp;ms | 10.5 | 1.0 | 1.8 | 0.3 | 29.9 |
| Simulation, OBJ | 0.6 | 2.3 | 13.4 | 0.8&nbsp;ms | 10.3 | 16.3 | 1.8 | 0.3 | 45.0 |
| Visual, GLB | 0.6 | 2.3 | 14.3 | 0.8&nbsp;ms | 22.1 | 0.3 | 2.3 | 0.3 | 42.2 |
| Visual, OBJ | 0.6 | 2.4 | 14.2 | 1&nbsp;ms | 21.9 | 9.9 | 2.6 | 0.3 | 51.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Einstein-TC-01](https://github.com/Board-Folk/Einstein-TC-01)<br>Board: `TC02Mini.kicad_pcb` |
|---|---|
| Folder | Expansions / TC02Mini / Kicad |
| Complexity | 264&nbsp;/&nbsp;1000 (size&nbsp;189, features&nbsp;75) |
| KESE&nbsp;features | through vias, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 51, 2,290, 128 |
| Triangles,&nbsp;simulation | 2,815,452 in 155 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">96&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">419&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">141&nbsp;MB</td><td align="right">972&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">295&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">57&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">176&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.22 TMSAdapterTC01

![TMSAdapterTC01: stages 4 and 6 take 56% to 86% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 13 s. Simulation, STL takes 11 s. Simulation, OBJ takes 16 s. Visual, GLB takes 14 s. Visual, OBJ takes 18 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Einstein-TC-01_TMSAdapterTC01.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 4.9 | 0.4&nbsp;ms | 3.8 | 0.2 | 0.6 | 0.2 | 10.6 |
| Simulation, STEP | 0.2 | 0.7 | 4.9 | 0.5&nbsp;ms | 4.1 | 2.8 | 0.5 | 0.2 | 13.4 |
| Simulation, STL | 0.2 | 0.8 | 4.8 | 0.5&nbsp;ms | 3.8 | 0.3 | 0.6 | 0.3 | 10.8 |
| Simulation, OBJ | 0.2 | 0.7 | 4.6 | 0.4&nbsp;ms | 4.0 | 5.4 | 0.5 | 0.2 | 15.6 |
| Visual, GLB | 0.2 | 0.7 | 4.7 | 0.4&nbsp;ms | 7.7 | 92&nbsp;ms | 0.9 | 0.2 | 14.4 |
| Visual, OBJ | 0.2 | 0.7 | 4.8 | 0.3&nbsp;ms | 7.4 | 3.4 | 1.1 | 0.3 | 17.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Einstein-TC-01](https://github.com/Board-Folk/Einstein-TC-01)<br>Board: `TMSAdapterTC01.kicad_pcb` |
|---|---|
| Folder | Expansions / TMSAdapterTC01 / Kicad |
| Complexity | 238&nbsp;/&nbsp;1000 (size&nbsp;163, features&nbsp;75) |
| KESE&nbsp;features | through vias, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 22, 850, 24 |
| Triangles,&nbsp;simulation | 1,335,060 in 72 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">542&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">191&nbsp;MB</td><td align="right">630&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">67&nbsp;MB</td><td align="right">537&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">135&nbsp;MB</td><td align="right">903&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">646&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">83&nbsp;MB</td><td align="right">728&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.23 V9958AdapterTC01

![V9958AdapterTC01: stages 4 and 6 take 53% to 86% of a run. Simulation, GLB takes 18 s. Simulation, STEP takes 23 s. Simulation, STL takes 18 s. Simulation, OBJ takes 27 s. Visual, GLB takes 27 s. Visual, OBJ takes 33 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Einstein-TC-01_V9958AdapterTC01.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.3 | 8.3 | 0.8&nbsp;ms | 6.5 | 0.3 | 1.1 | 0.3 | 18.2 |
| Simulation, STEP | 0.4 | 1.4 | 8.2 | 0.8&nbsp;ms | 6.6 | 5.1 | 1.0 | 0.3 | 22.9 |
| Simulation, STL | 0.4 | 1.3 | 8.1 | 0.5&nbsp;ms | 6.8 | 0.6 | 0.9 | 0.3 | 18.3 |
| Simulation, OBJ | 0.4 | 1.2 | 7.9 | 1&nbsp;ms | 6.4 | 10.0 | 1.0 | 0.3 | 27.2 |
| Visual, GLB | 0.4 | 1.3 | 7.9 | 0.9&nbsp;ms | 15.5 | 0.2 | 1.8 | 0.3 | 27.3 |
| Visual, OBJ | 0.4 | 1.3 | 8.3 | 0.8&nbsp;ms | 14.9 | 5.9 | 1.7 | 0.3 | 32.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Einstein-TC-01](https://github.com/Board-Folk/Einstein-TC-01)<br>Board: `V9958AdapterTC01.kicad_pcb` |
|---|---|
| Folder | Expansions / V9958AdapterTC01 / Kicad |
| Complexity | 276&nbsp;/&nbsp;1000 (size&nbsp;176, features&nbsp;100) |
| KESE&nbsp;features | through vias, custom pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 46, 1,132, 49 |
| Triangles,&nbsp;simulation | 1,913,332 in 118 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">64&nbsp;MB</td><td align="right">732&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">272&nbsp;MB</td><td align="right">858&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">96&nbsp;MB</td><td align="right">730&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">196&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">41&nbsp;MB</td><td align="right">942&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">125&nbsp;MB</td><td align="right">978&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.24 EinsteinTC01

![EinsteinTC01: stages 4 and 6 take 51% to 85% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 3 min. Simulation, STL takes 3 min. Simulation, OBJ takes 4 min. Visual, GLB takes 4 min. Visual, OBJ takes 5 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Einstein-TC-01_Kicad_EinsteinTC01.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 5.5 | 12.5 | 72.6 | 4&nbsp;ms | 56.2 | 3.0 | 9.2 | 0.6 | 159.6 |
| Simulation, STEP | 6.6 | 12.3 | 72.4 | 3&nbsp;ms | 62.7 | 41.9 | 9.1 | 0.6 | 205.7 |
| Simulation, STL | 6.2 | 12.9 | 73.8 | 3&nbsp;ms | 66.7 | 7.0 | 8.6 | 0.6 | 175.7 |
| Simulation, OBJ | 6.0 | 12.7 | 70.4 | 3&nbsp;ms | 57.5 | 93.5 | 8.5 | 0.6 | 249.3 |
| Visual, GLB | 5.9 | 12.3 | 75.4 | 4&nbsp;ms | 141.9 | 1.7 | 17.1 | 0.5 | 254.7 |
| Visual, OBJ | 6.3 | 13.1 | 73.8 | 4&nbsp;ms | 131.1 | 52.0 | 15.7 | 0.7 | 292.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Einstein-TC-01](https://github.com/Board-Folk/Einstein-TC-01)<br>Board: `EinsteinTC01.kicad_pcb` |
|---|---|
| Folder | Kicad |
| Complexity | 309&nbsp;/&nbsp;1000 (size&nbsp;234, features&nbsp;75) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, filled zones,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 346, 9,719, 769 |
| Triangles,&nbsp;simulation | 11,902,236 in 528 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">398&nbsp;MB</td><td align="right">3.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.7&nbsp;GB</td><td align="right">4.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">595&nbsp;MB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.3&nbsp;GB</td><td align="right">7.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">238&nbsp;MB</td><td align="right">3.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">765&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.25 EinsteinCE

![EinsteinCE: stages 4 and 6 take 55% to 87% of a run. Simulation, GLB takes 83 s. Simulation, STEP takes 2 min. Simulation, STL takes 85 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Einstein-TC-01_EinsteinCE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 6.7 | 37.3 | 2&nbsp;ms | 30.4 | 1.7 | 5.1 | 0.4 | 82.6 |
| Simulation, STEP | 0.8 | 6.2 | 36.1 | 2&nbsp;ms | 30.8 | 22.2 | 5.0 | 0.5 | 101.5 |
| Simulation, STL | 1.0 | 5.9 | 38.1 | 2&nbsp;ms | 30.7 | 3.7 | 5.5 | 0.5 | 85.3 |
| Simulation, OBJ | 0.9 | 6.0 | 35.8 | 2&nbsp;ms | 30.0 | 41.1 | 5.1 | 0.4 | 119.6 |
| Visual, GLB | 1.1 | 6.1 | 36.4 | 2&nbsp;ms | 78.8 | 0.8 | 8.8 | 0.3 | 132.2 |
| Visual, OBJ | 1.0 | 6.1 | 35.7 | 3&nbsp;ms | 78.9 | 25.2 | 9.3 | 0.3 | 156.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Einstein-TC-01](https://github.com/Board-Folk/Einstein-TC-01)<br>Board: `EinsteinCE.kicad_pcb` |
|---|---|
| Folder | Remix / EinsteinCE / Kicad |
| Complexity | 253&nbsp;/&nbsp;1000 (size&nbsp;218, features&nbsp;35) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 154, 6,261, 418 |
| Triangles,&nbsp;simulation | 7,959,458 in 329 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">265&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.3&nbsp;GB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">398&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">836&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">170&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">542&nbsp;MB</td><td align="right">3.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.26 MegaCD

![MegaCD: stages 4 and 6 take 49% to 83% of a run. Simulation, GLB takes 65 s. Simulation, STEP takes 81 s. Simulation, STL takes 65 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/MegaCD-Main-BD_MegaCD-837-8015-01-Rev1-MCE2_MegaCD.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.2 | 6.4 | 23.6 | 2&nbsp;ms | 26.0 | 1.3 | 5.1 | 0.4 | 64.9 |
| Simulation, STEP | 2.3 | 6.3 | 24.0 | 2&nbsp;ms | 26.3 | 16.7 | 4.6 | 0.4 | 80.6 |
| Simulation, STL | 2.1 | 6.1 | 22.8 | 2&nbsp;ms | 26.5 | 2.5 | 4.9 | 0.4 | 65.3 |
| Simulation, OBJ | 2.3 | 6.3 | 23.4 | 2&nbsp;ms | 25.5 | 38.1 | 4.9 | 0.4 | 100.9 |
| Visual, GLB | 2.2 | 6.4 | 23.0 | 2&nbsp;ms | 67.6 | 0.8 | 8.1 | 0.4 | 108.6 |
| Visual, OBJ | 2.2 | 6.4 | 23.6 | 2&nbsp;ms | 70.5 | 23.2 | 8.4 | 0.3 | 134.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/MegaCD-Main-BD](https://github.com/Board-Folk/MegaCD-Main-BD)<br>Board: `MegaCD.kicad_pcb` |
|---|---|
| Folder | MegaCD-837-8015-01-Rev1-MCE2 |
| Complexity | 428&nbsp;/&nbsp;1000 (size&nbsp;293, features&nbsp;135) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 103, 10,727, 883 |
| Triangles,&nbsp;simulation | 6,854,478 in 355 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">234&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">994&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">343&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">733&nbsp;MB</td><td align="right">4.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">149&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">486&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.27 MegaCD

![MegaCD: stages 4 and 6 take 50% to 84% of a run. Simulation, GLB takes 68 s. Simulation, STEP takes 83 s. Simulation, STL takes 74 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/MegaCD-Main-BD_MegaCD-837-8015-Rev0-MCE1_MegaCD.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.3 | 7.3 | 25.1 | 1&nbsp;ms | 25.6 | 1.1 | 5.0 | 0.4 | 67.9 |
| Simulation, STEP | 2.2 | 6.2 | 24.1 | 1&nbsp;ms | 26.7 | 18.5 | 4.5 | 0.5 | 82.6 |
| Simulation, STL | 2.8 | 6.8 | 26.1 | 1&nbsp;ms | 30.2 | 3.2 | 4.6 | 0.4 | 74.3 |
| Simulation, OBJ | 2.9 | 6.0 | 26.0 | 1&nbsp;ms | 28.3 | 40.3 | 4.5 | 0.4 | 108.6 |
| Visual, GLB | 2.4 | 6.1 | 25.7 | 1&nbsp;ms | 71.8 | 0.7 | 9.4 | 0.4 | 116.6 |
| Visual, OBJ | 2.3 | 5.8 | 24.3 | 1&nbsp;ms | 70.0 | 27.4 | 10.9 | 0.4 | 141.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/MegaCD-Main-BD](https://github.com/Board-Folk/MegaCD-Main-BD)<br>Board: `MegaCD.kicad_pcb` |
|---|---|
| Folder | MegaCD-837-8015-Rev0-MCE1 |
| Complexity | 425&nbsp;/&nbsp;1000 (size&nbsp;290, features&nbsp;135) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 93, 9,360, 822 |
| Triangles,&nbsp;simulation | 6,425,034 in 355 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">220&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">897&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">321&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">686&nbsp;MB</td><td align="right">4.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">138&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">450&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.28 MegaCD

![MegaCD: stages 4 and 6 take 46% to 81% of a run. Simulation, GLB takes 60 s. Simulation, STEP takes 74 s. Simulation, STL takes 61 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/MegaCD-Main-BD_MegaCD-837-8952-Export_MegaCD.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.3 | 5.7 | 22.2 | 2&nbsp;ms | 22.5 | 1.0 | 3.7 | 0.4 | 59.9 |
| Simulation, STEP | 4.3 | 5.7 | 21.4 | 2&nbsp;ms | 22.7 | 15.3 | 3.9 | 0.4 | 73.6 |
| Simulation, STL | 4.2 | 5.6 | 21.5 | 1&nbsp;ms | 22.8 | 2.0 | 4.2 | 0.4 | 60.7 |
| Simulation, OBJ | 4.4 | 5.7 | 22.4 | 1&nbsp;ms | 24.0 | 39.2 | 4.1 | 0.4 | 100.1 |
| Visual, GLB | 4.8 | 5.7 | 22.4 | 2&nbsp;ms | 61.2 | 0.6 | 7.6 | 0.4 | 102.5 |
| Visual, OBJ | 4.3 | 6.1 | 21.9 | 2&nbsp;ms | 60.2 | 24.5 | 8.1 | 0.3 | 125.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/MegaCD-Main-BD](https://github.com/Board-Folk/MegaCD-Main-BD)<br>Board: `MegaCD.kicad_pcb` |
|---|---|
| Folder | MegaCD-837-8952-Export |
| Complexity | 424&nbsp;/&nbsp;1000 (size&nbsp;289, features&nbsp;135) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 117, 7,524, 826 |
| Triangles,&nbsp;simulation | 6,123,290 in 361 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">210&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">862&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">306&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">655&nbsp;MB</td><td align="right">4.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">137&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">445&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.29 MegaCD

![MegaCD: stages 4 and 6 take 46% to 82% of a run. Simulation, GLB takes 6.9 s. Simulation, STEP takes 8.7 s. Simulation, STL takes 6.7 s. Simulation, OBJ takes 11 s. Visual, GLB takes 10 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/MegaCD-Main-BD_RAM-Adapter-837-8015-01_MegaCD.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.8 | 2.5 | 0.4&nbsp;ms | 2.5 | 99&nbsp;ms | 0.5 | 0.2 | 6.9 |
| Simulation, STEP | 0.3 | 0.7 | 2.5 | 0.3&nbsp;ms | 2.3 | 2.2 | 0.4 | 0.3 | 8.7 |
| Simulation, STL | 0.4 | 0.7 | 2.3 | 0.4&nbsp;ms | 2.3 | 0.2 | 0.5 | 0.3 | 6.7 |
| Simulation, OBJ | 0.2 | 0.7 | 2.6 | 0.5&nbsp;ms | 2.3 | 4.2 | 0.5 | 0.2 | 10.7 |
| Visual, GLB | 0.2 | 0.6 | 2.7 | 0.4&nbsp;ms | 5.5 | 88&nbsp;ms | 0.6 | 0.2 | 10.0 |
| Visual, OBJ | 0.3 | 0.7 | 2.6 | 0.5&nbsp;ms | 5.6 | 2.2 | 0.8 | 0.3 | 12.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/MegaCD-Main-BD](https://github.com/Board-Folk/MegaCD-Main-BD)<br>Board: `MegaCD.kicad_pcb` |
|---|---|
| Folder | RAM-Adapter-837-8015-01 |
| Complexity | 251&nbsp;/&nbsp;1000 (size&nbsp;156, features&nbsp;95) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 7, 359, 27 |
| Triangles,&nbsp;simulation | 814,600 in 54 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">396&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">115&nbsp;MB</td><td align="right">407&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">41&nbsp;MB</td><td align="right">415&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">82&nbsp;MB</td><td align="right">557&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">460&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">48&nbsp;MB</td><td align="right">442&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.30 MegaCD

![MegaCD: stages 4 and 6 take 45% to 81% of a run. Simulation, GLB takes 6.5 s. Simulation, STEP takes 8.5 s. Simulation, STL takes 6.7 s. Simulation, OBJ takes 10 s. Visual, GLB takes 10 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/MegaCD-Main-BD_RAM-Adapter-837-8015_MegaCD.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 2.4 | 0.3&nbsp;ms | 2.3 | 0.1 | 0.4 | 0.2 | 6.5 |
| Simulation, STEP | 0.2 | 0.6 | 2.6 | 0.4&nbsp;ms | 2.3 | 2.0 | 0.5 | 0.2 | 8.5 |
| Simulation, STL | 0.3 | 0.6 | 2.6 | 0.4&nbsp;ms | 2.3 | 0.3 | 0.4 | 0.2 | 6.7 |
| Simulation, OBJ | 0.3 | 0.6 | 2.3 | 0.3&nbsp;ms | 2.3 | 4.0 | 0.4 | 0.2 | 10.2 |
| Visual, GLB | 0.3 | 0.7 | 2.5 | 0.5&nbsp;ms | 5.7 | 79&nbsp;ms | 0.6 | 0.2 | 10.1 |
| Visual, OBJ | 0.4 | 0.7 | 2.6 | 0.3&nbsp;ms | 5.5 | 2.4 | 0.6 | 0.3 | 12.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/MegaCD-Main-BD](https://github.com/Board-Folk/MegaCD-Main-BD)<br>Board: `MegaCD.kicad_pcb` |
|---|---|
| Folder | RAM-Adapter-837-8015 |
| Complexity | 252&nbsp;/&nbsp;1000 (size&nbsp;157, features&nbsp;95) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 7, 398, 27 |
| Triangles,&nbsp;simulation | 817,738 in 54 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">400&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">119&nbsp;MB</td><td align="right">413&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">41&nbsp;MB</td><td align="right">391&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">82&nbsp;MB</td><td align="right">568&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">460&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">50&nbsp;MB</td><td align="right">461&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.31 NeoGeoAES3_5

![NeoGeoAES3_5: stages 4 and 6 take 51% to 86% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 4 min. Simulation, STL takes 3 min. Simulation, OBJ takes 5 min. Visual, GLB takes 5 min. Visual, OBJ takes 6 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/NeoGeoAES-3-5_NeoGeoAES3-5.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 7.0 | 15.4 | 76.5 | 3&nbsp;ms | 65.1 | 2.4 | 11.5 | 0.6 | 178.5 |
| Simulation, STEP | 7.1 | 14.2 | 80.6 | 3&nbsp;ms | 73.0 | 40.3 | 11.2 | 0.7 | 227.1 |
| Simulation, STL | 6.8 | 14.2 | 76.9 | 3&nbsp;ms | 65.3 | 5.6 | 11.2 | 0.5 | 180.6 |
| Simulation, OBJ | 5.9 | 14.2 | 77.2 | 3&nbsp;ms | 63.5 | 104.7 | 10.0 | 0.6 | 276.2 |
| Visual, GLB | 6.7 | 15.2 | 77.7 | 3&nbsp;ms | 186.0 | 1.4 | 19.6 | 0.4 | 307.1 |
| Visual, OBJ | 6.3 | 13.2 | 77.2 | 3&nbsp;ms | 185.2 | 72.4 | 19.3 | 0.5 | 374.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/NeoGeoAES-3.5](https://github.com/Board-Folk/NeoGeoAES-3.5)<br>Board: `NeoGeoAES3_5.kicad_pcb` |
|---|---|
| Complexity | 368&nbsp;/&nbsp;1000 (size&nbsp;243, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, filled zones,<br>copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 298, 18,210, 1,498 |
| Triangles,&nbsp;simulation | 12,427,738 in 777 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">421&nbsp;MB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.0&nbsp;GB</td><td align="right">4.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">621&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.3&nbsp;GB</td><td align="right">7.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">290&nbsp;MB</td><td align="right">4.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">940&nbsp;MB</td><td align="right">5.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.32 Neptune-32x-315-5805-bypass

![Neptune-32x-315-5805-bypass: stages 4 and 6 take 52% to 81% of a run. Simulation, GLB takes 3.1 s. Simulation, STEP takes 4.3 s. Simulation, STL takes 3.2 s. Simulation, OBJ takes 5.3 s. Visual, GLB takes 5.0 s. Visual, OBJ takes 6.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Neptune_Neptune-32x-315-5805-bypass.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 1.1 | 47&nbsp;ms | 0.2 | 0.2 | 3.1 |
| Simulation, STEP | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 1.1 | 1.2 | 0.2 | 0.2 | 4.3 |
| Simulation, STL | 0.1 | 0.3 | 1.2 | 0.3&nbsp;ms | 1.1 | 72&nbsp;ms | 0.2 | 0.2 | 3.2 |
| Simulation, OBJ | 0.1 | 0.3 | 1.6 | 0.4&nbsp;ms | 1.2 | 1.7 | 0.2 | 0.2 | 5.3 |
| Visual, GLB | 0.1 | 0.3 | 1.2 | 0.3&nbsp;ms | 2.8 | 44&nbsp;ms | 0.3 | 0.2 | 5.0 |
| Visual, OBJ | 0.1 | 0.3 | 1.3 | 0.2&nbsp;ms | 3.1 | 1.2 | 0.3 | 0.2 | 6.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Neptune](https://github.com/Board-Folk/Neptune)<br>Board: `Neptune-32x-315-5805-bypass.kicad_pcb` |
|---|---|
| Folder | helpers / Neptune-32x-315-5805-bypass |
| Complexity | 234&nbsp;/&nbsp;1000 (size&nbsp;124, features&nbsp;110) |
| KESE&nbsp;features | through vias, padstacks,<br>drill offsets, stack-up,<br>dielectric εr and tanδ,<br>castellated pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 1, 306, 44 |
| Triangles,&nbsp;simulation | 282,880 in 67 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">10&nbsp;MB</td><td align="right">224&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">49&nbsp;MB</td><td align="right">263&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">232&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">30&nbsp;MB</td><td align="right">257&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.5&nbsp;MB</td><td align="right">266&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">268&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.33 Neptune-32x-315-5818-bypass

![Neptune-32x-315-5818-bypass: stages 4 and 6 take 47% to 76% of a run. Simulation, GLB takes 2.8 s. Simulation, STEP takes 3.8 s. Simulation, STL takes 2.8 s. Simulation, OBJ takes 4.0 s. Visual, GLB takes 4.5 s. Visual, OBJ takes 5.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Neptune_Neptune-32x-315-5818-bypass.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 0.8 | 0.2&nbsp;ms | 1.1 | 42&nbsp;ms | 0.2 | 0.2 | 2.8 |
| Simulation, STEP | 0.1 | 0.3 | 0.9 | 0.3&nbsp;ms | 1.1 | 1.1 | 0.2 | 0.2 | 3.8 |
| Simulation, STL | 0.1 | 0.2 | 0.8 | 0.3&nbsp;ms | 1.1 | 77&nbsp;ms | 0.2 | 0.2 | 2.8 |
| Simulation, OBJ | 0.1 | 0.3 | 0.7 | 0.3&nbsp;ms | 1.1 | 1.3 | 0.2 | 0.2 | 4.0 |
| Visual, GLB | 0.1 | 0.3 | 0.8 | 0.3&nbsp;ms | 2.6 | 40&nbsp;ms | 0.5 | 0.2 | 4.5 |
| Visual, OBJ | 0.1 | 0.3 | 0.8 | 0.3&nbsp;ms | 2.6 | 1.0 | 0.4 | 0.3 | 5.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Neptune](https://github.com/Board-Folk/Neptune)<br>Board: `Neptune-32x-315-5818-bypass.kicad_pcb` |
|---|---|
| Folder | helpers / Neptune-32x-315-5818-bypass |
| Complexity | 173&nbsp;/&nbsp;1000 (size&nbsp;128, features&nbsp;45) |
| KESE&nbsp;features | through vias, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 1, 367, 65 |
| Triangles,&nbsp;simulation | 244,460 in 70 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.2&nbsp;MB</td><td align="right">253&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">47&nbsp;MB</td><td align="right">258&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">12&nbsp;MB</td><td align="right">259&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">26&nbsp;MB</td><td align="right">262&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.5&nbsp;MB</td><td align="right">293&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">23&nbsp;MB</td><td align="right">281&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.34 Neptune-Region-Fix

![Reading, start-up and exit take 40% to 63% of a run. Simulation, GLB takes 0.4 s. Simulation, STEP takes 0.5 s. Simulation, STL takes 0.4 s. Simulation, OBJ takes 0.4 s. Visual, GLB takes 0.5 s. Visual, OBJ takes 0.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Neptune_Neptune-Region-Fix.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 67&nbsp;ms | 25&nbsp;ms | 41&nbsp;ms | 0.1&nbsp;ms | 85&nbsp;ms | 3&nbsp;ms | 11&nbsp;ms | 0.2 | 0.4 |
| Simulation, STEP | 68&nbsp;ms | 26&nbsp;ms | 34&nbsp;ms | 0.1&nbsp;ms | 79&nbsp;ms | 68&nbsp;ms | 10&nbsp;ms | 0.2 | 0.5 |
| Simulation, STL | 63&nbsp;ms | 23&nbsp;ms | 39&nbsp;ms | 0.1&nbsp;ms | 83&nbsp;ms | 3&nbsp;ms | 10&nbsp;ms | 0.2 | 0.4 |
| Simulation, OBJ | 58&nbsp;ms | 22&nbsp;ms | 43&nbsp;ms | 0.1&nbsp;ms | 77&nbsp;ms | 35&nbsp;ms | 10&nbsp;ms | 0.2 | 0.4 |
| Visual, GLB | 58&nbsp;ms | 23&nbsp;ms | 36&nbsp;ms | 0.1&nbsp;ms | 0.2 | 3&nbsp;ms | 25&nbsp;ms | 0.2 | 0.5 |
| Visual, OBJ | 53&nbsp;ms | 20&nbsp;ms | 41&nbsp;ms | 0.1&nbsp;ms | 0.2 | 31&nbsp;ms | 23&nbsp;ms | 0.2 | 0.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Neptune](https://github.com/Board-Folk/Neptune)<br>Board: `Neptune-Region-Fix.kicad_pcb` |
|---|---|
| Folder | helpers / Neptune-Region-Fix |
| Complexity | 87&nbsp;/&nbsp;1000 (size&nbsp;62, features&nbsp;25) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 0, 12, 1 |
| Triangles,&nbsp;simulation | 8,908 in 9 parts |
| Note | no components |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">336&nbsp;kB</td><td align="right">59&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">1.7&nbsp;MB</td><td align="right">61&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">446&nbsp;kB</td><td align="right">60&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">853&nbsp;kB</td><td align="right">63&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">299&nbsp;kB</td><td align="right">83&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">754&nbsp;kB</td><td align="right">83&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.35 Neptune

![Neptune: stages 4 and 6 take 51% to 85% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Neptune_Neptune.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.5 | 10.8 | 37.4 | 2&nbsp;ms | 41.5 | 2.1 | 8.3 | 0.6 | 103.3 |
| Simulation, STEP | 2.5 | 10.4 | 36.6 | 2&nbsp;ms | 41.6 | 24.4 | 8.0 | 0.5 | 124.0 |
| Simulation, STL | 2.6 | 10.5 | 37.1 | 2&nbsp;ms | 42.2 | 4.5 | 8.6 | 0.6 | 106.1 |
| Simulation, OBJ | 2.6 | 11.1 | 37.5 | 2&nbsp;ms | 43.3 | 56.7 | 8.1 | 0.5 | 159.8 |
| Visual, GLB | 2.5 | 11.0 | 36.8 | 2&nbsp;ms | 128.6 | 1.3 | 14.9 | 0.4 | 195.4 |
| Visual, OBJ | 2.7 | 11.0 | 37.8 | 2&nbsp;ms | 126.1 | 36.0 | 14.8 | 0.5 | 229.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Neptune](https://github.com/Board-Folk/Neptune)<br>Board: `Neptune.kicad_pcb` |
|---|---|
| Complexity | 468&nbsp;/&nbsp;1000 (size&nbsp;318, features&nbsp;150) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 374, 11,140, 1,391 |
| Triangles,&nbsp;simulation | 9,804,248 in 748 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">339&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.5&nbsp;GB</td><td align="right">3.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">490&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.1&nbsp;GB</td><td align="right">6.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">223&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">725&nbsp;MB</td><td align="right">4.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.36 Oric

![Oric: stages 4 and 6 take 54% to 85% of a run. Simulation, GLB takes 42 s. Simulation, STEP takes 50 s. Simulation, STL takes 41 s. Simulation, OBJ takes 61 s. Visual, GLB takes 60 s. Visual, OBJ takes 76 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Oric-Remix_Archive-IssueAv1-1_Oric.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 3.5 | 18.8 | 0.8&nbsp;ms | 15.7 | 0.6 | 2.5 | 0.2 | 42.1 |
| Simulation, STEP | 0.6 | 3.7 | 18.9 | 2&nbsp;ms | 14.3 | 10.5 | 2.2 | 0.3 | 50.4 |
| Simulation, STL | 0.6 | 3.3 | 18.2 | 0.8&nbsp;ms | 14.6 | 1.4 | 2.2 | 0.3 | 40.7 |
| Simulation, OBJ | 0.6 | 3.3 | 18.0 | 2&nbsp;ms | 14.9 | 22.0 | 2.1 | 0.2 | 61.2 |
| Visual, GLB | 0.6 | 3.5 | 17.6 | 0.8&nbsp;ms | 33.1 | 0.4 | 4.4 | 0.2 | 59.8 |
| Visual, OBJ | 0.7 | 3.7 | 18.4 | 0.9&nbsp;ms | 32.3 | 15.7 | 5.2 | 0.3 | 76.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Oric-Remix](https://github.com/Board-Folk/Oric-Remix)<br>Board: `Oric.kicad_pcb` |
|---|---|
| Folder | Archive / IssueAv1.1 |
| Complexity | 268&nbsp;/&nbsp;1000 (size&nbsp;203, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 129, 2,835, 234 |
| Triangles,&nbsp;simulation | 4,060,494 in 203 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">136&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">566&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">203&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">426&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">87&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">275&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.37 Oric-PS2USB

![Oric-PS2USB: stages 4 and 6 take 51% to 87% of a run. Simulation, GLB takes 7.8 s. Simulation, STEP takes 9.6 s. Simulation, STL takes 7.8 s. Simulation, OBJ takes 12 s. Visual, GLB takes 11 s. Visual, OBJ takes 14 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Oric-Remix_Oric-PS2USB.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 3.6 | 0.5&nbsp;ms | 2.7 | 0.1 | 0.4 | 0.2 | 7.8 |
| Simulation, STEP | 0.2 | 0.6 | 3.5 | 0.4&nbsp;ms | 2.6 | 2.1 | 0.4 | 0.2 | 9.6 |
| Simulation, STL | 0.2 | 0.6 | 3.5 | 0.5&nbsp;ms | 2.7 | 0.2 | 0.4 | 0.2 | 7.8 |
| Simulation, OBJ | 0.2 | 0.5 | 3.4 | 0.5&nbsp;ms | 2.9 | 4.6 | 0.4 | 0.2 | 12.3 |
| Visual, GLB | 0.2 | 0.6 | 3.5 | 0.5&nbsp;ms | 6.4 | 70&nbsp;ms | 0.6 | 0.2 | 11.4 |
| Visual, OBJ | 0.2 | 0.6 | 3.6 | 0.7&nbsp;ms | 6.4 | 2.7 | 0.7 | 0.2 | 14.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Oric-Remix](https://github.com/Board-Folk/Oric-Remix)<br>Board: `Oric-PS2USB.kicad_pcb` |
|---|---|
| Folder | Expansions / Oric-PS2USB / Kicad |
| Complexity | 234&nbsp;/&nbsp;1000 (size&nbsp;149, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 11, 554, 26 |
| Triangles,&nbsp;simulation | 859,924 in 74 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">29&nbsp;MB</td><td align="right">461&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">143&nbsp;MB</td><td align="right">456&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">43&nbsp;MB</td><td align="right">466&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">88&nbsp;MB</td><td align="right">611&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">514&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">52&nbsp;MB</td><td align="right">492&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.38 Oric

![Oric: stages 4 and 6 take 53% to 85% of a run. Simulation, GLB takes 42 s. Simulation, STEP takes 55 s. Simulation, STL takes 46 s. Simulation, OBJ takes 65 s. Visual, GLB takes 65 s. Visual, OBJ takes 80 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/Oric-Remix_Kicad_Oric.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 3.8 | 19.7 | 0.9&nbsp;ms | 15.1 | 0.6 | 2.4 | 0.3 | 42.4 |
| Simulation, STEP | 0.7 | 3.6 | 20.2 | 1&nbsp;ms | 15.6 | 11.6 | 2.7 | 0.3 | 54.8 |
| Simulation, STL | 0.7 | 3.8 | 20.8 | 2&nbsp;ms | 16.1 | 1.6 | 2.6 | 0.3 | 45.7 |
| Simulation, OBJ | 0.6 | 3.7 | 19.2 | 0.9&nbsp;ms | 15.4 | 23.7 | 2.6 | 0.3 | 65.5 |
| Visual, GLB | 0.7 | 3.8 | 20.5 | 2&nbsp;ms | 34.5 | 0.4 | 4.4 | 0.3 | 64.6 |
| Visual, OBJ | 0.7 | 3.9 | 20.8 | 1&nbsp;ms | 34.6 | 15.2 | 4.8 | 0.3 | 80.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/Oric-Remix](https://github.com/Board-Folk/Oric-Remix)<br>Board: `Oric.kicad_pcb` |
|---|---|
| Folder | Kicad |
| Complexity | 268&nbsp;/&nbsp;1000 (size&nbsp;203, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 129, 2,832, 234 |
| Triangles,&nbsp;simulation | 4,065,754 in 203 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">137&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">568&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">203&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">426&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">87&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">275&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.39 PCE

![PCE: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 33 s. Simulation, STEP takes 41 s. Simulation, STL takes 34 s. Simulation, OBJ takes 51 s. Visual, GLB takes 54 s. Visual, OBJ takes 67 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/PC-Engine_PCE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.3 | 2.9 | 13.4 | 0.9&nbsp;ms | 12.4 | 0.6 | 1.9 | 0.3 | 32.7 |
| Simulation, STEP | 1.4 | 3.1 | 13.2 | 1.0&nbsp;ms | 12.8 | 8.7 | 1.8 | 0.3 | 41.3 |
| Simulation, STL | 1.2 | 2.8 | 13.6 | 1&nbsp;ms | 12.6 | 1.0 | 2.1 | 0.3 | 33.5 |
| Simulation, OBJ | 1.3 | 2.8 | 13.6 | 0.9&nbsp;ms | 12.8 | 17.7 | 2.0 | 0.3 | 50.5 |
| Visual, GLB | 1.3 | 2.8 | 13.8 | 0.9&nbsp;ms | 31.5 | 0.4 | 3.8 | 0.2 | 53.7 |
| Visual, OBJ | 1.3 | 2.8 | 13.3 | 1&nbsp;ms | 31.3 | 13.7 | 4.0 | 0.3 | 66.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/PC-Engine](https://github.com/Board-Folk/PC-Engine)<br>Board: `PCE.kicad_pcb` |
|---|---|
| Complexity | 325&nbsp;/&nbsp;1000 (size&nbsp;210, features&nbsp;115) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 123, 4,523, 290 |
| Triangles,&nbsp;simulation | 3,209,090 in 199 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">112&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">614&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">160&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">345&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">87&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">273&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.40 PCE

![PCE: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 99 s. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/PC-Engine-Duo_PCE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 5.0 | 9.3 | 37.0 | 2&nbsp;ms | 40.5 | 1.5 | 5.1 | 0.4 | 98.8 |
| Simulation, STEP | 5.6 | 9.5 | 36.2 | 2&nbsp;ms | 40.3 | 27.0 | 5.1 | 0.4 | 124.1 |
| Simulation, STL | 5.0 | 9.6 | 36.5 | 3&nbsp;ms | 40.2 | 3.2 | 5.1 | 0.5 | 100.1 |
| Simulation, OBJ | 5.4 | 9.2 | 36.1 | 3&nbsp;ms | 39.2 | 55.7 | 5.4 | 0.5 | 151.5 |
| Visual, GLB | 5.3 | 10.0 | 38.4 | 4&nbsp;ms | 108.7 | 1.3 | 12.6 | 0.3 | 176.7 |
| Visual, OBJ | 5.0 | 9.3 | 35.9 | 2&nbsp;ms | 109.2 | 43.4 | 13.1 | 0.5 | 216.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/PC-Engine-Duo](https://github.com/Board-Folk/PC-Engine-Duo)<br>Board: `PCE.kicad_pcb` |
|---|---|
| Complexity | 414&nbsp;/&nbsp;1000 (size&nbsp;309, features&nbsp;105) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 618, 15,551, 1,491 |
| Triangles,&nbsp;simulation | 8,529,616 in 690 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">295&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.6&nbsp;GB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">427&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">921&nbsp;MB</td><td align="right">5.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">256&nbsp;MB</td><td align="right">3.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">826&nbsp;MB</td><td align="right">5.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.41 PCE

![PCE: stages 4 and 6 take 49% to 79% of a run. Simulation, GLB takes 32 s. Simulation, STEP takes 40 s. Simulation, STL takes 32 s. Simulation, OBJ takes 47 s. Visual, GLB takes 50 s. Visual, OBJ takes 63 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/PC-Engine-GT_PCE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.1 | 3.7 | 10.5 | 0.9&nbsp;ms | 13.1 | 0.6 | 1.7 | 0.3 | 32.1 |
| Simulation, STEP | 2.2 | 3.7 | 10.3 | 1&nbsp;ms | 13.1 | 8.5 | 1.7 | 0.3 | 39.8 |
| Simulation, STL | 2.0 | 3.5 | 10.2 | 1&nbsp;ms | 13.0 | 1.2 | 1.8 | 0.3 | 32.0 |
| Simulation, OBJ | 2.1 | 3.4 | 9.6 | 0.9&nbsp;ms | 13.5 | 16.5 | 1.9 | 0.3 | 47.3 |
| Visual, GLB | 2.2 | 3.5 | 10.1 | 1&nbsp;ms | 29.6 | 0.4 | 4.4 | 0.3 | 50.4 |
| Visual, OBJ | 2.2 | 3.6 | 9.9 | 1&nbsp;ms | 29.3 | 13.2 | 4.3 | 0.3 | 62.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/PC-Engine-GT](https://github.com/Board-Folk/PC-Engine-GT)<br>Board: `PCE.kicad_pcb` |
|---|---|
| Complexity | 348&nbsp;/&nbsp;1000 (size&nbsp;233, features&nbsp;115) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 195, 4,794, 322 |
| Triangles,&nbsp;simulation | 3,256,982 in 307 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">113&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">511&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">163&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">349&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">81&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">255&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.42 TRS80I-Charmap

![TRS80I-Charmap: stages 4 and 6 take 48% to 81% of a run. Simulation, GLB takes 3.5 s. Simulation, STEP takes 4.6 s. Simulation, STL takes 3.4 s. Simulation, OBJ takes 5.1 s. Visual, GLB takes 4.9 s. Visual, OBJ takes 5.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/TRS80IJP_TRS80I-Charmap.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.4 | 0.3&nbsp;ms | 1.1 | 81&nbsp;ms | 0.3 | 0.2 | 3.5 |
| Simulation, STEP | 0.1 | 0.3 | 1.4 | 0.3&nbsp;ms | 1.1 | 1.2 | 0.2 | 0.2 | 4.6 |
| Simulation, STL | 0.1 | 0.3 | 1.4 | 0.3&nbsp;ms | 1.1 | 80&nbsp;ms | 0.2 | 0.2 | 3.4 |
| Simulation, OBJ | 0.1 | 0.3 | 1.3 | 0.3&nbsp;ms | 1.1 | 1.8 | 0.2 | 0.3 | 5.1 |
| Visual, GLB | 0.1 | 0.3 | 1.4 | 0.2&nbsp;ms | 2.5 | 35&nbsp;ms | 0.2 | 0.2 | 4.9 |
| Visual, OBJ | 0.1 | 0.3 | 1.4 | 0.3&nbsp;ms | 2.3 | 1.2 | 0.2 | 0.2 | 5.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/TRS80IJP](https://github.com/Board-Folk/TRS80IJP)<br>Board: `TRS80I-Charmap.kicad_pcb` |
|---|---|
| Folder | Extras / Charmap / Kicad |
| Complexity | 163&nbsp;/&nbsp;1000 (size&nbsp;123, features&nbsp;40) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 5, 197, 0 |
| Triangles,&nbsp;simulation | 323,104 in 38 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">238&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">42&nbsp;MB</td><td align="right">261&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">16&nbsp;MB</td><td align="right">231&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">32&nbsp;MB</td><td align="right">266&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">6.5&nbsp;MB</td><td align="right">238&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">19&nbsp;MB</td><td align="right">242&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.43 TRSG3JPMod

![TRSG3JPMod: stages 4 and 6 take 48% to 80% of a run. Simulation, GLB takes 3.5 s. Simulation, STEP takes 4.5 s. Simulation, STL takes 3.3 s. Simulation, OBJ takes 5.3 s. Visual, GLB takes 4.8 s. Visual, OBJ takes 6.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/TRS80IJP_TRSG3JPMod.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 1.4 | 0.2&nbsp;ms | 1.2 | 56&nbsp;ms | 0.2 | 0.3 | 3.5 |
| Simulation, STEP | 0.1 | 0.3 | 1.3 | 0.4&nbsp;ms | 1.2 | 1.2 | 0.2 | 0.3 | 4.5 |
| Simulation, STL | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 1.1 | 0.1 | 0.2 | 0.2 | 3.3 |
| Simulation, OBJ | 0.2 | 0.3 | 1.3 | 0.4&nbsp;ms | 1.2 | 1.8 | 0.2 | 0.3 | 5.3 |
| Visual, GLB | 0.1 | 0.3 | 1.4 | 0.2&nbsp;ms | 2.5 | 36&nbsp;ms | 0.3 | 0.3 | 4.8 |
| Visual, OBJ | 0.1 | 0.3 | 1.4 | 0.2&nbsp;ms | 2.6 | 1.3 | 0.2 | 0.2 | 6.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/TRS80IJP](https://github.com/Board-Folk/TRS80IJP)<br>Board: `TRSG3JPMod.kicad_pcb` |
|---|---|
| Folder | Extras / TRSG3Mod / TRSG3JPModv1 |
| Complexity | 179&nbsp;/&nbsp;1000 (size&nbsp;114, features&nbsp;65) |
| KESE&nbsp;features | through vias, filled zones,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 3, 129, 8 |
| Triangles,&nbsp;simulation | 282,270 in 33 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.8&nbsp;MB</td><td align="right">232&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">47&nbsp;MB</td><td align="right">249&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">227&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">28&nbsp;MB</td><td align="right">242&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.8&nbsp;MB</td><td align="right">237&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">17&nbsp;MB</td><td align="right">236&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.44 TRSG3Mod

![TRSG3Mod: stages 4 and 6 take 49% to 83% of a run. Simulation, GLB takes 3.0 s. Simulation, STEP takes 3.9 s. Simulation, STL takes 3.0 s. Simulation, OBJ takes 4.3 s. Visual, GLB takes 4.3 s. Visual, OBJ takes 5.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/TRS80IJP_TRSG3Mod.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 1.2 | 0.3&nbsp;ms | 1.0 | 45&nbsp;ms | 0.2 | 0.2 | 3.0 |
| Simulation, STEP | 0.1 | 0.2 | 1.1 | 0.2&nbsp;ms | 1.0 | 1.1 | 0.2 | 0.2 | 3.9 |
| Simulation, STL | 0.1 | 0.2 | 1.2 | 0.2&nbsp;ms | 1.0 | 87&nbsp;ms | 0.2 | 0.2 | 3.0 |
| Simulation, OBJ | 0.1 | 0.2 | 1.1 | 0.2&nbsp;ms | 1.0 | 1.5 | 0.2 | 0.2 | 4.3 |
| Visual, GLB | 0.1 | 0.2 | 1.2 | 0.2&nbsp;ms | 2.4 | 28&nbsp;ms | 0.2 | 0.2 | 4.3 |
| Visual, OBJ | 0.1 | 0.2 | 1.1 | 0.2&nbsp;ms | 2.3 | 0.9 | 0.2 | 0.2 | 5.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/TRS80IJP](https://github.com/Board-Folk/TRS80IJP)<br>Board: `TRSG3Mod.kicad_pcb` |
|---|---|
| Folder | Extras / TRSG3Mod / TRSG3Modv1 |
| Complexity | 198&nbsp;/&nbsp;1000 (size&nbsp;123, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 6, 153, 10 |
| Triangles,&nbsp;simulation | 308,292 in 34 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">238&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">52&nbsp;MB</td><td align="right">261&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">15&nbsp;MB</td><td align="right">243&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">31&nbsp;MB</td><td align="right">245&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">6.6&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">19&nbsp;MB</td><td align="right">262&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.45 TRS80IJP_1

![TRS80IJP_1: stages 4 and 6 take 51% to 84% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/TRS80IJP_TRS80IJP-1.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.9 | 11.4 | 52.1 | 2&nbsp;ms | 42.3 | 2.1 | 5.8 | 0.5 | 119.0 |
| Simulation, STEP | 4.5 | 10.8 | 56.2 | 2&nbsp;ms | 42.3 | 26.1 | 5.9 | 0.5 | 146.3 |
| Simulation, STL | 5.2 | 11.0 | 54.8 | 6&nbsp;ms | 42.2 | 5.4 | 6.5 | 0.5 | 125.6 |
| Simulation, OBJ | 5.0 | 11.2 | 51.0 | 3&nbsp;ms | 39.9 | 65.1 | 6.4 | 0.6 | 179.2 |
| Visual, GLB | 5.0 | 10.2 | 53.8 | 4&nbsp;ms | 101.5 | 1.4 | 12.4 | 0.4 | 184.6 |
| Visual, OBJ | 4.7 | 10.9 | 50.5 | 3&nbsp;ms | 106.4 | 38.3 | 11.6 | 0.5 | 222.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/TRS80IJP](https://github.com/Board-Folk/TRS80IJP)<br>Board: `TRS80IJP_1.kicad_pcb` |
|---|---|
| Folder | v1.1 / Kicad |
| Complexity | 297&nbsp;/&nbsp;1000 (size&nbsp;232, features&nbsp;65) |
| KESE&nbsp;features | through vias, filled zones,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 254, 10,574, 737 |
| Triangles,&nbsp;simulation | 9,938,980 in 419 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">335&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.5&nbsp;GB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">497&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.1&nbsp;GB</td><td align="right">6.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">223&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">715&nbsp;MB</td><td align="right">4.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.46 TRS80ILCMod

![TRS80ILCMod: stages 4 and 6 take 50% to 81% of a run. Simulation, GLB takes 2.5 s. Simulation, STEP takes 3.6 s. Simulation, STL takes 2.6 s. Simulation, OBJ takes 3.7 s. Visual, GLB takes 3.2 s. Visual, OBJ takes 3.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/TRS80IUS_TRS80ILCMod.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 79&nbsp;ms | 0.2 | 0.9 | 0.2&nbsp;ms | 1.0 | 37&nbsp;ms | 0.1 | 0.2 | 2.5 |
| Simulation, STEP | 87&nbsp;ms | 0.2 | 1.0 | 0.2&nbsp;ms | 1.1 | 1.0 | 0.1 | 0.2 | 3.6 |
| Simulation, STL | 86&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 1.0 | 58&nbsp;ms | 0.1 | 0.2 | 2.6 |
| Simulation, OBJ | 83&nbsp;ms | 0.2 | 0.9 | 0.2&nbsp;ms | 0.9 | 1.3 | 0.1 | 0.2 | 3.7 |
| Visual, GLB | 86&nbsp;ms | 0.2 | 0.9 | 0.2&nbsp;ms | 1.7 | 19&nbsp;ms | 0.1 | 0.2 | 3.2 |
| Visual, OBJ | 83&nbsp;ms | 0.2 | 0.9 | 0.2&nbsp;ms | 1.7 | 0.7 | 0.1 | 0.2 | 3.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/TRS80IUS](https://github.com/Board-Folk/TRS80IUS)<br>Board: `TRS80ILCMod.kicad_pcb` |
|---|---|
| Folder | Extras / TRS80ILCMod / Kicad |
| Complexity | 139&nbsp;/&nbsp;1000 (size&nbsp;109, features&nbsp;30) |
| KESE&nbsp;features | stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 5, 83, 0 |
| Triangles,&nbsp;simulation | 246,726 in 28 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">8.2&nbsp;MB</td><td align="right">218&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">31&nbsp;MB</td><td align="right">236&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">12&nbsp;MB</td><td align="right">213&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">24&nbsp;MB</td><td align="right">217&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.5&nbsp;MB</td><td align="right">206&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">13&nbsp;MB</td><td align="right">212&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.47 TRS80IUS

![TRS80IUS: stages 4 and 6 take 52% to 85% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/TRS80IUS_TRS80IUS.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.6 | 8.6 | 50.1 | 2&nbsp;ms | 43.5 | 2.1 | 6.7 | 0.5 | 116.2 |
| Simulation, STEP | 4.9 | 8.7 | 48.0 | 3&nbsp;ms | 45.4 | 28.4 | 6.7 | 0.5 | 142.5 |
| Simulation, STL | 4.4 | 9.5 | 52.8 | 3&nbsp;ms | 46.6 | 4.6 | 7.3 | 0.5 | 125.7 |
| Simulation, OBJ | 4.8 | 9.7 | 49.9 | 2&nbsp;ms | 39.7 | 61.4 | 6.5 | 0.5 | 172.5 |
| Visual, GLB | 5.3 | 8.6 | 46.3 | 2&nbsp;ms | 100.2 | 1.0 | 10.0 | 0.4 | 171.7 |
| Visual, OBJ | 4.7 | 8.0 | 50.0 | 17&nbsp;ms | 112.8 | 40.2 | 10.4 | 0.4 | 226.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Board-Folk/TRS80IUS](https://github.com/Board-Folk/TRS80IUS)<br>Board: `TRS80IUS.kicad_pcb` |
|---|---|
| Folder | v1.1 / Kicad |
| Complexity | 308&nbsp;/&nbsp;1000 (size&nbsp;228, features&nbsp;80) |
| KESE&nbsp;features | through vias, custom pads,<br>filled zones, copper drawings,<br>copper text, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 231, 9,962, 380 |
| Triangles,&nbsp;simulation | 8,820,422 in 392 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">296&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.3&nbsp;GB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">441&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">933&nbsp;MB</td><td align="right">5.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">183&nbsp;MB</td><td align="right">3.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">587&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.48 Debug_Adapter

![Debug_Adapter: stages 4 and 6 take 50% to 77% of a run. Simulation, GLB takes 4.3 s. Simulation, STEP takes 5.8 s. Simulation, STL takes 4.4 s. Simulation, OBJ takes 6.1 s. Visual, GLB takes 6.0 s. Visual, OBJ takes 7.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/h616-board_Debug-Adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.5 | 1.4 | 0.3&nbsp;ms | 1.7 | 67&nbsp;ms | 0.2 | 0.2 | 4.3 |
| Simulation, STEP | 0.2 | 0.5 | 1.3 | 0.5&nbsp;ms | 1.7 | 1.6 | 0.2 | 0.2 | 5.8 |
| Simulation, STL | 0.2 | 0.5 | 1.3 | 0.3&nbsp;ms | 1.8 | 0.1 | 0.2 | 0.3 | 4.4 |
| Simulation, OBJ | 0.2 | 0.5 | 1.3 | 0.3&nbsp;ms | 1.7 | 1.9 | 0.2 | 0.3 | 6.1 |
| Visual, GLB | 0.2 | 0.5 | 1.4 | 0.3&nbsp;ms | 3.2 | 52&nbsp;ms | 0.4 | 0.2 | 6.0 |
| Visual, OBJ | 0.2 | 0.5 | 1.3 | 0.3&nbsp;ms | 3.4 | 1.6 | 0.4 | 0.3 | 7.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [bogdan8266/h616-board](https://github.com/bogdan8266/h616-board)<br>Board: `Debug_Adapter.kicad_pcb` |
|---|---|
| Folder | Hardware / Debug_Adapter |
| Complexity | 261&nbsp;/&nbsp;1000 (size&nbsp;161, features&nbsp;100) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>knockout text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 25, 251, 179 |
| Triangles,&nbsp;simulation | 370,438 in 57 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">306&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">50&nbsp;MB</td><td align="right">338&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">19&nbsp;MB</td><td align="right">299&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">37&nbsp;MB</td><td align="right">298&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">334&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">32&nbsp;MB</td><td align="right">337&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.49 H616_devboard

![H616_devboard: stages 4 and 6 take 48% to 87% of a run. Simulation, GLB takes 30 s. Simulation, STEP takes 38 s. Simulation, STL takes 31 s. Simulation, OBJ takes 50 s. Visual, GLB takes 55 s. Visual, OBJ takes 67 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/h616-board_Hardware-H616-DDR3_H616-devboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 3.1 | 10.4 | 2&nbsp;ms | 13.1 | 0.6 | 1.7 | 0.3 | 29.8 |
| Simulation, STEP | 0.6 | 3.0 | 10.4 | 1&nbsp;ms | 13.3 | 8.6 | 2.0 | 0.4 | 38.3 |
| Simulation, STL | 0.6 | 2.9 | 10.1 | 1&nbsp;ms | 13.5 | 1.5 | 1.9 | 0.3 | 30.7 |
| Simulation, OBJ | 0.6 | 3.0 | 10.4 | 1&nbsp;ms | 13.7 | 20.0 | 1.8 | 0.3 | 49.8 |
| Visual, GLB | 0.6 | 2.7 | 10.3 | 2&nbsp;ms | 37.5 | 0.4 | 3.3 | 0.2 | 55.1 |
| Visual, OBJ | 0.6 | 2.8 | 11.0 | 1&nbsp;ms | 38.1 | 10.5 | 3.8 | 0.2 | 67.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [bogdan8266/h616-board](https://github.com/bogdan8266/h616-board)<br>Board: `H616_devboard.kicad_pcb` |
|---|---|
| Folder | Hardware / H616_DDR3 |
| Complexity | 412&nbsp;/&nbsp;1000 (size&nbsp;297, features&nbsp;115) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, arc tracks,<br>copper text, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 167, 1,531, 263 |
| Triangles,&nbsp;simulation | 4,056,192 in 464 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">131&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">460&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">203&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">426&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">73&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">230&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.50 H616_devboard

![H616_devboard: stages 4 and 6 take 53% to 83% of a run. Simulation, GLB takes 34 s. Simulation, STEP takes 41 s. Simulation, STL takes 33 s. Simulation, OBJ takes 49 s. Visual, GLB takes 49 s. Visual, OBJ takes 63 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/h616-board_Hardware-H616-LPDDR4_H616-devboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 3.7 | 10.8 | 2&nbsp;ms | 16.3 | 0.6 | 1.5 | 0.3 | 33.9 |
| Simulation, STEP | 0.8 | 3.7 | 10.3 | 1&nbsp;ms | 15.3 | 9.0 | 1.5 | 0.3 | 40.9 |
| Simulation, STL | 0.8 | 3.6 | 10.2 | 2&nbsp;ms | 15.0 | 1.3 | 1.6 | 0.3 | 32.8 |
| Simulation, OBJ | 0.8 | 3.6 | 10.4 | 0.7&nbsp;ms | 15.7 | 16.6 | 1.5 | 0.3 | 48.9 |
| Visual, GLB | 0.8 | 3.5 | 10.2 | 0.6&nbsp;ms | 31.0 | 0.4 | 3.3 | 0.2 | 49.4 |
| Visual, OBJ | 0.8 | 3.5 | 10.2 | 1&nbsp;ms | 31.1 | 12.8 | 4.2 | 0.2 | 62.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [bogdan8266/h616-board](https://github.com/bogdan8266/h616-board)<br>Board: `H616_devboard.kicad_pcb` |
|---|---|
| Folder | Hardware / H616_LPDDR4 |
| Complexity | 447&nbsp;/&nbsp;1000 (size&nbsp;297, features&nbsp;150) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 152, 6,210, 715 |
| Triangles,&nbsp;simulation | 4,013,826 in 333 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">135&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">567&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">201&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">422&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">99&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">316&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.51 SmartPrintCoreH7x

![SmartPrintCoreH7x: stages 4 and 6 take 57% to 85% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/SmartPrintCoreH7x_SmartPrintCoreH7x.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.4 | 10.3 | 42.8 | 1&nbsp;ms | 46.4 | 1.7 | 5.0 | 0.4 | 109.0 |
| Simulation, STEP | 2.4 | 9.9 | 43.2 | 2&nbsp;ms | 46.0 | 25.5 | 5.1 | 0.4 | 132.5 |
| Simulation, STL | 2.4 | 10.1 | 41.5 | 1&nbsp;ms | 45.8 | 3.5 | 5.3 | 0.4 | 108.9 |
| Simulation, OBJ | 2.4 | 9.7 | 41.7 | 1&nbsp;ms | 44.3 | 48.0 | 5.1 | 0.4 | 151.6 |
| Visual, GLB | 2.3 | 9.6 | 41.8 | 2&nbsp;ms | 123.1 | 1.2 | 14.7 | 0.4 | 193.2 |
| Visual, OBJ | 2.4 | 9.6 | 41.3 | 1&nbsp;ms | 125.7 | 39.2 | 14.1 | 0.4 | 232.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [BoltzRnD/SmartPrintCoreH7x](https://github.com/BoltzRnD/SmartPrintCoreH7x)<br>Board: `SmartPrintCoreH7x.kicad_pcb` |
|---|---|
| Folder | SmartPrintCoreH7x |
| Complexity | 410&nbsp;/&nbsp;1000 (size&nbsp;280, features&nbsp;130) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 541, 8,490, 1,506 |
| Triangles,&nbsp;simulation | 7,949,190 in 428 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">273&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.5&nbsp;GB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">397&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">851&nbsp;MB</td><td align="right">5.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">238&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">764&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.52 other-m68k

![other-m68k: stages 4 and 6 take 48% to 80% of a run. Simulation, GLB takes 52 s. Simulation, STEP takes 64 s. Simulation, STL takes 53 s. Simulation, OBJ takes 84 s. Visual, GLB takes 78 s. Visual, OBJ takes 93 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/other-m68k_other-m68k.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.1 | 6.0 | 18.7 | 2&nbsp;ms | 21.2 | 1.1 | 3.1 | 0.3 | 51.5 |
| Simulation, STEP | 1.1 | 6.2 | 19.5 | 1.0&nbsp;ms | 20.1 | 13.3 | 3.2 | 0.3 | 63.9 |
| Simulation, STL | 1.1 | 6.0 | 19.3 | 2&nbsp;ms | 20.7 | 2.6 | 3.1 | 0.4 | 53.2 |
| Simulation, OBJ | 1.1 | 6.2 | 19.3 | 1&nbsp;ms | 20.8 | 33.4 | 3.1 | 0.4 | 84.3 |
| Visual, GLB | 1.1 | 6.3 | 19.8 | 0.9&nbsp;ms | 43.1 | 0.5 | 7.1 | 0.3 | 78.1 |
| Visual, OBJ | 1.1 | 6.3 | 19.6 | 2&nbsp;ms | 43.2 | 15.9 | 7.0 | 0.3 | 93.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [bradgrantham/other-m68k](https://github.com/bradgrantham/other-m68k)<br>Board: `other-m68k.kicad_pcb` |
|---|---|
| Folder | kicad / release |
| Complexity | 349&nbsp;/&nbsp;1000 (size&nbsp;284, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 163, 6,720, 665 |
| Triangles,&nbsp;simulation | 6,929,688 in 267 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">234&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">837&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">347&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">734&nbsp;MB</td><td align="right">4.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">126&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">403&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.53 ClassicIIReloaded

![ClassicIIReloaded: stages 4 and 6 take 45% to 83% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/ClassicII_ClassicIIReloaded.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 6.6 | 11.4 | 37.7 | 2&nbsp;ms | 47.1 | 2.1 | 6.4 | 0.5 | 111.8 |
| Simulation, STEP | 6.8 | 11.9 | 39.4 | 2&nbsp;ms | 48.4 | 28.7 | 6.6 | 0.5 | 142.3 |
| Simulation, STL | 7.1 | 11.7 | 38.8 | 2&nbsp;ms | 47.0 | 4.2 | 6.1 | 0.5 | 115.4 |
| Simulation, OBJ | 7.0 | 12.5 | 40.7 | 2&nbsp;ms | 48.2 | 82.5 | 6.9 | 0.5 | 198.3 |
| Visual, GLB | 6.9 | 11.6 | 40.3 | 3&nbsp;ms | 116.8 | 1.1 | 12.5 | 0.4 | 189.7 |
| Visual, OBJ | 7.1 | 12.0 | 40.5 | 2&nbsp;ms | 120.9 | 43.4 | 11.4 | 0.4 | 235.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [btb/ClassicII](https://github.com/btb/ClassicII)<br>Board: `ClassicIIReloaded.kicad_pcb` |
|---|---|
| Folder | ClassicIIReloaded |
| Complexity | 450&nbsp;/&nbsp;1000 (size&nbsp;305, features&nbsp;145) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, arc tracks,<br>filled zones, copper drawings,<br>copper text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 290, 10,450, 1,255 |
| Triangles,&nbsp;simulation | 11,075,382 in 454 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">378&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.5&nbsp;GB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">554&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.2&nbsp;GB</td><td align="right">7.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">223&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">726&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.54 ClassicIIRevB

![ClassicIIRevB: stages 4 and 6 take 47% to 83% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/ClassicII_ClassicIIRevB.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 8.9 | 9.8 | 35.0 | 1&nbsp;ms | 42.5 | 1.9 | 6.0 | 0.7 | 104.9 |
| Simulation, STEP | 9.6 | 11.1 | 36.8 | 2&nbsp;ms | 44.9 | 25.1 | 5.6 | 0.5 | 133.5 |
| Simulation, STL | 8.9 | 9.8 | 35.6 | 2&nbsp;ms | 42.0 | 4.2 | 5.6 | 0.5 | 106.6 |
| Simulation, OBJ | 8.8 | 9.6 | 35.9 | 2&nbsp;ms | 42.3 | 62.1 | 6.2 | 0.5 | 165.5 |
| Visual, GLB | 8.2 | 9.6 | 36.5 | 4&nbsp;ms | 106.1 | 1.1 | 10.9 | 0.4 | 172.8 |
| Visual, OBJ | 8.8 | 10.1 | 36.0 | 2&nbsp;ms | 107.6 | 35.2 | 10.1 | 0.4 | 208.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [btb/ClassicII](https://github.com/btb/ClassicII)<br>Board: `ClassicIIRevB.kicad_pcb` |
|---|---|
| Folder | ClassicIIRevB |
| Complexity | 449&nbsp;/&nbsp;1000 (size&nbsp;304, features&nbsp;145) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, arc tracks,<br>filled zones, copper drawings,<br>copper text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 281, 10,002, 1,306 |
| Triangles,&nbsp;simulation | 10,662,252 in 454 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">365&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.4&nbsp;GB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">533&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.1&nbsp;GB</td><td align="right">6.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">217&nbsp;MB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">706&nbsp;MB</td><td align="right">4.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.55 ButterStick

![ButterStick: stages 4 and 6 take 50% to 84% of a run. Simulation, GLB takes 65 s. Simulation, STEP takes 82 s. Simulation, STL takes 65 s. Simulation, OBJ takes 2 min. Visual, GLB takes 91 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/butterstick-hardware_hardware-ButterStick-r0-1_ButterStick.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.6 | 6.6 | 24.3 | 2&nbsp;ms | 27.9 | 1.4 | 3.3 | 0.4 | 65.4 |
| Simulation, STEP | 1.6 | 6.4 | 24.3 | 0.9&nbsp;ms | 28.8 | 17.2 | 3.1 | 0.4 | 81.8 |
| Simulation, STL | 1.6 | 6.6 | 24.2 | 2&nbsp;ms | 27.0 | 2.4 | 3.2 | 0.4 | 65.3 |
| Simulation, OBJ | 1.6 | 6.9 | 25.1 | 1&nbsp;ms | 27.7 | 41.4 | 3.2 | 0.4 | 106.2 |
| Visual, GLB | 1.6 | 6.7 | 24.3 | 2&nbsp;ms | 52.3 | 0.6 | 5.6 | 0.3 | 91.4 |
| Visual, OBJ | 1.8 | 7.1 | 24.3 | 2&nbsp;ms | 48.8 | 22.7 | 6.4 | 0.4 | 111.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [butterstick-fpga/butterstick-hardware](https://github.com/butterstick-fpga/butterstick-hardware)<br>Board: `ButterStick.kicad_pcb` |
|---|---|
| Folder | hardware / ButterStick_r0.1 |
| Complexity | 398&nbsp;/&nbsp;1000 (size&nbsp;318, features&nbsp;80) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 181, 17,618, 671 |
| Triangles,&nbsp;simulation | 6,232,652 in 340 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">214&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">881&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">312&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">667&nbsp;MB</td><td align="right">4.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">114&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">374&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.56 ButterStick

![ButterStick: stages 4 and 6 take 51% to 82% of a run. Simulation, GLB takes 53 s. Simulation, STEP takes 67 s. Simulation, STL takes 57 s. Simulation, OBJ takes 85 s. Visual, GLB takes 76 s. Visual, OBJ takes 91 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/butterstick-hardware_hardware-ButterStick-r0-2_ButterStick.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.1 | 5.9 | 19.9 | 1&nbsp;ms | 22.5 | 0.9 | 2.6 | 0.3 | 53.3 |
| Simulation, STEP | 1.1 | 5.9 | 20.8 | 1&nbsp;ms | 22.7 | 13.0 | 2.7 | 0.3 | 66.7 |
| Simulation, STL | 1.2 | 5.7 | 21.5 | 0.8&nbsp;ms | 22.7 | 2.1 | 3.3 | 0.4 | 56.9 |
| Simulation, OBJ | 1.2 | 5.9 | 21.2 | 1&nbsp;ms | 22.4 | 31.5 | 2.8 | 0.3 | 85.3 |
| Visual, GLB | 1.2 | 6.2 | 20.1 | 1.0&nbsp;ms | 42.1 | 0.5 | 5.8 | 0.3 | 76.2 |
| Visual, OBJ | 1.2 | 5.9 | 20.5 | 1&nbsp;ms | 43.5 | 15.1 | 4.8 | 0.3 | 91.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [butterstick-fpga/butterstick-hardware](https://github.com/butterstick-fpga/butterstick-hardware)<br>Board: `ButterStick.kicad_pcb` |
|---|---|
| Folder | hardware / ButterStick_r0.2 |
| Complexity | 410&nbsp;/&nbsp;1000 (size&nbsp;320, features&nbsp;90) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 223, 16,942, 792 |
| Triangles,&nbsp;simulation | 6,727,172 in 339 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">231&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">896&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">336&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">722&nbsp;MB</td><td align="right">4.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">117&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">383&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.57 ButterStick

![ButterStick: stages 4 and 6 take 42% to 85% of a run. Simulation, GLB takes 75 s. Simulation, STEP takes 90 s. Simulation, STL takes 77 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/butterstick-hardware_hardware-ButterStick-r1-0_ButterStick.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.4 | 8.4 | 23.0 | 2&nbsp;ms | 34.1 | 1.6 | 5.1 | 0.5 | 75.0 |
| Simulation, STEP | 2.4 | 8.7 | 22.4 | 2&nbsp;ms | 33.3 | 18.1 | 5.2 | 0.4 | 90.4 |
| Simulation, STL | 2.2 | 8.5 | 22.7 | 2&nbsp;ms | 33.9 | 3.7 | 5.2 | 0.5 | 76.7 |
| Simulation, OBJ | 2.3 | 8.8 | 22.7 | 1&nbsp;ms | 33.8 | 62.1 | 5.1 | 0.4 | 135.3 |
| Visual, GLB | 2.3 | 9.1 | 23.0 | 2&nbsp;ms | 86.7 | 0.8 | 7.4 | 0.4 | 129.6 |
| Visual, OBJ | 2.4 | 9.4 | 24.2 | 1&nbsp;ms | 92.7 | 26.0 | 8.7 | 0.4 | 163.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [butterstick-fpga/butterstick-hardware](https://github.com/butterstick-fpga/butterstick-hardware)<br>Board: `ButterStick.kicad_pcb` |
|---|---|
| Folder | hardware / ButterStick_r1.0 |
| Complexity | 491&nbsp;/&nbsp;1000 (size&nbsp;341, features&nbsp;150) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 327, 19,487, 1,061 |
| Triangles,&nbsp;simulation | 10,425,092 in 367 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">345&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.1&nbsp;GB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">521&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.1&nbsp;GB</td><td align="right">6.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">154&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">520&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.58 250407_

![250407_: stages 4 and 6 take 57% to 87% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/C64-250407-Replica-KiCad_250407.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 6.7 | 54.4 | 2&nbsp;ms | 42.1 | 1.5 | 7.6 | 0.5 | 113.9 |
| Simulation, STEP | 1.1 | 7.2 | 50.4 | 3&nbsp;ms | 42.2 | 25.0 | 6.7 | 0.5 | 133.1 |
| Simulation, STL | 1.0 | 7.1 | 51.7 | 3&nbsp;ms | 44.6 | 4.6 | 8.5 | 0.4 | 117.9 |
| Simulation, OBJ | 1.1 | 7.2 | 53.3 | 3&nbsp;ms | 48.3 | 60.9 | 7.3 | 0.5 | 178.6 |
| Visual, GLB | 1.4 | 7.2 | 51.6 | 2&nbsp;ms | 93.9 | 0.8 | 11.6 | 0.4 | 166.9 |
| Visual, OBJ | 1.1 | 7.0 | 49.6 | 3&nbsp;ms | 88.2 | 24.3 | 11.3 | 0.4 | 181.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [bwack/C64-250407-Replica-KiCad](https://github.com/bwack/C64-250407-Replica-KiCad)<br>Board: `250407_.kicad_pcb` |
|---|---|
| Complexity | 283&nbsp;/&nbsp;1000 (size&nbsp;223, features&nbsp;60) |
| KESE&nbsp;features | through vias, custom pads,<br>filled zones, copper drawings |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 215, 6,552, 574 |
| Triangles,&nbsp;simulation | 8,877,004 in 261 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">301&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.4&nbsp;GB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">444&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">949&nbsp;MB</td><td align="right">5.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">152&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">484&nbsp;MB</td><td align="right">3.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.59 C64-250469-KiCad

![C64-250469-KiCad: stages 4 and 6 take 64% to 88% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 3 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/C64C-250469-KiCAD-Replica_C64-250469-KiCad.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.1 | 6.4 | 42.8 | 0.8&nbsp;ms | 78.3 | 1.4 | 5.4 | 0.4 | 137.8 |
| Simulation, STEP | 3.1 | 6.2 | 40.1 | 0.9&nbsp;ms | 76.9 | 22.2 | 5.1 | 0.4 | 154.0 |
| Simulation, STL | 3.1 | 6.1 | 37.8 | 0.9&nbsp;ms | 74.8 | 2.8 | 5.1 | 0.4 | 130.2 |
| Simulation, OBJ | 3.4 | 6.3 | 39.6 | 1.0&nbsp;ms | 77.0 | 49.7 | 4.9 | 0.4 | 181.2 |
| Visual, GLB | 3.3 | 6.0 | 37.9 | 1&nbsp;ms | 95.1 | 0.9 | 9.2 | 0.3 | 152.7 |
| Visual, OBJ | 3.4 | 6.5 | 39.9 | 0.9&nbsp;ms | 98.6 | 32.6 | 10.5 | 0.4 | 191.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [bwack/C64C-250469-KiCAD-Replica](https://github.com/bwack/C64C-250469-KiCAD-Replica)<br>Board: `C64-250469-KiCad.kicad_pcb` |
|---|---|
| Complexity | 322&nbsp;/&nbsp;1000 (size&nbsp;222, features&nbsp;100) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 138, 8,544, 642 |
| Triangles,&nbsp;simulation | 8,242,430 in 213 parts |
| Verifier | Simulation, GLB: Verifier FAIL<br>Simulation, STEP: Verifier FAIL<br>Simulation, STL: Verifier FAIL<br>Simulation, OBJ: Verifier FAIL |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">280&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.4&nbsp;GB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">412&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">880&nbsp;MB</td><td align="right">5.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">191&nbsp;MB</td><td align="right">3.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">615&nbsp;MB</td><td align="right">3.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.60 audio

![audio: stages 4 and 6 take 53% to 82% of a run. Simulation, GLB takes 5.7 s. Simulation, STEP takes 7.9 s. Simulation, STL takes 5.9 s. Simulation, OBJ takes 8.3 s. Visual, GLB takes 8.0 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/laptop_audio.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 0.5 | 2.0 | 0.4&nbsp;ms | 2.3 | 75&nbsp;ms | 0.3 | 0.2 | 5.7 |
| Simulation, STEP | 0.3 | 0.5 | 2.0 | 0.3&nbsp;ms | 2.8 | 1.9 | 0.3 | 0.3 | 7.9 |
| Simulation, STL | 0.3 | 0.4 | 1.9 | 0.3&nbsp;ms | 2.6 | 0.1 | 0.3 | 0.2 | 5.9 |
| Simulation, OBJ | 0.4 | 0.5 | 1.9 | 0.3&nbsp;ms | 2.5 | 2.5 | 0.3 | 0.3 | 8.3 |
| Visual, GLB | 0.2 | 0.5 | 1.9 | 0.3&nbsp;ms | 4.7 | 58&nbsp;ms | 0.4 | 0.2 | 8.0 |
| Visual, OBJ | 0.3 | 0.6 | 2.2 | 0.3&nbsp;ms | 4.8 | 2.3 | 0.7 | 0.3 | 11.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [byrantech/laptop](https://github.com/byrantech/laptop)<br>Board: `audio.kicad_pcb` |
|---|---|
| Folder | audio |
| Complexity | 291&nbsp;/&nbsp;1000 (size&nbsp;196, features&nbsp;95) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>TrueType text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241007) |
| Parts,&nbsp;tracks,&nbsp;vias | 41, 244, 58 |
| Triangles,&nbsp;simulation | 416,276 in 71 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">272&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">74&nbsp;MB</td><td align="right">305&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">21&nbsp;MB</td><td align="right">272&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">42&nbsp;MB</td><td align="right">313&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">318&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">35&nbsp;MB</td><td align="right">310&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.61 encoder

![encoder: stages 4 and 6 take 47% to 62% of a run. Simulation, GLB takes 1.1 s. Simulation, STEP takes 1.4 s. Simulation, STL takes 1.1 s. Simulation, OBJ takes 1.4 s. Visual, GLB takes 1.2 s. Visual, OBJ takes 1.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/laptop_encoder.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 97&nbsp;ms | 45&nbsp;ms | 0.2 | 0.2&nbsp;ms | 0.4 | 8&nbsp;ms | 35&nbsp;ms | 0.3 | 1.1 |
| Simulation, STEP | 94&nbsp;ms | 53&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.4 | 0.3 | 36&nbsp;ms | 0.3 | 1.4 |
| Simulation, STL | 76&nbsp;ms | 49&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.5 | 12&nbsp;ms | 39&nbsp;ms | 0.3 | 1.1 |
| Simulation, OBJ | 80&nbsp;ms | 50&nbsp;ms | 0.3 | 0.3&nbsp;ms | 0.5 | 0.3 | 43&nbsp;ms | 0.2 | 1.4 |
| Visual, GLB | 78&nbsp;ms | 49&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.5 | 7&nbsp;ms | 58&nbsp;ms | 0.2 | 1.2 |
| Visual, OBJ | 99&nbsp;ms | 61&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.5 | 0.1 | 48&nbsp;ms | 0.2 | 1.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [byrantech/laptop](https://github.com/byrantech/laptop)<br>Board: `encoder.kicad_pcb` |
|---|---|
| Folder | haptic / encoder |
| Complexity | 101&nbsp;/&nbsp;1000 (size&nbsp;81, features&nbsp;20) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20240225) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 24, 0 |
| Triangles,&nbsp;simulation | 43,206 in 17 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.5&nbsp;MB</td><td align="right">67&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">7.1&nbsp;MB</td><td align="right">72&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">2.2&nbsp;MB</td><td align="right">68&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">4.1&nbsp;MB</td><td align="right">77&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">990&nbsp;kB</td><td align="right">102&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">2.7&nbsp;MB</td><td align="right">103&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.62 keyboard

![keyboard: stages 4 and 6 take 56% to 82% of a run. Simulation, GLB takes 35 s. Simulation, STEP takes 43 s. Simulation, STL takes 36 s. Simulation, OBJ takes 51 s. Visual, GLB takes 53 s. Visual, OBJ takes 66 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/laptop_keyboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.2 | 3.5 | 14.0 | 0.8&nbsp;ms | 14.2 | 0.4 | 1.3 | 0.3 | 34.9 |
| Simulation, STEP | 1.2 | 3.6 | 13.7 | 0.5&nbsp;ms | 14.5 | 8.9 | 1.3 | 0.3 | 43.5 |
| Simulation, STL | 1.2 | 3.5 | 13.8 | 0.4&nbsp;ms | 14.6 | 0.8 | 1.3 | 0.3 | 35.5 |
| Simulation, OBJ | 1.2 | 3.5 | 13.8 | 1&nbsp;ms | 14.5 | 16.0 | 1.5 | 0.3 | 50.7 |
| Visual, GLB | 1.3 | 3.6 | 14.2 | 1&nbsp;ms | 29.4 | 0.4 | 4.0 | 0.3 | 53.2 |
| Visual, OBJ | 1.4 | 3.7 | 14.5 | 0.5&nbsp;ms | 28.1 | 13.6 | 4.0 | 0.3 | 65.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [byrantech/laptop](https://github.com/byrantech/laptop)<br>Board: `keyboard.kicad_pcb` |
|---|---|
| Folder | keyboard |
| Complexity | 327&nbsp;/&nbsp;1000 (size&nbsp;247, features&nbsp;80) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>TrueType text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20240225) |
| Parts,&nbsp;tracks,&nbsp;vias | 208, 1,484, 571 |
| Triangles,&nbsp;simulation | 2,715,872 in 171 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">94&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">491&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">136&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">290&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">84&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">261&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.63 protector

![protector: stages 4 and 6 take 52% to 80% of a run. Simulation, GLB takes 2.5 s. Simulation, STEP takes 3.2 s. Simulation, STL takes 2.4 s. Simulation, OBJ takes 3.0 s. Visual, GLB takes 3.4 s. Visual, OBJ takes 3.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/laptop_protector.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 61&nbsp;ms | 0.2 | 1.2 | 0.2&nbsp;ms | 0.7 | 34&nbsp;ms | 97&nbsp;ms | 0.2 | 2.5 |
| Simulation, STEP | 57&nbsp;ms | 0.2 | 0.9 | 0.2&nbsp;ms | 0.7 | 0.9 | 0.1 | 0.2 | 3.2 |
| Simulation, STL | 54&nbsp;ms | 0.2 | 1.0 | 0.2&nbsp;ms | 0.8 | 51&nbsp;ms | 97&nbsp;ms | 0.2 | 2.4 |
| Simulation, OBJ | 54&nbsp;ms | 0.2 | 1.0 | 0.2&nbsp;ms | 0.7 | 0.8 | 96&nbsp;ms | 0.2 | 3.0 |
| Visual, GLB | 53&nbsp;ms | 0.2 | 1.0 | 0.2&nbsp;ms | 1.7 | 20&nbsp;ms | 0.2 | 0.3 | 3.4 |
| Visual, OBJ | 55&nbsp;ms | 0.2 | 1.0 | 0.2&nbsp;ms | 1.6 | 0.6 | 0.1 | 0.2 | 3.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [byrantech/laptop](https://github.com/byrantech/laptop)<br>Board: `protector.kicad_pcb` |
|---|---|
| Folder | keyboard / protector |
| Complexity | 218&nbsp;/&nbsp;1000 (size&nbsp;133, features&nbsp;85) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>knockout text, TrueType text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20240225) |
| Parts,&nbsp;tracks,&nbsp;vias | 6, 37, 97 |
| Triangles,&nbsp;simulation | 203,696 in 21 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">6.9&nbsp;MB</td><td align="right">193&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">23&nbsp;MB</td><td align="right">202&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">10&nbsp;MB</td><td align="right">196&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">20&nbsp;MB</td><td align="right">194&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.5&nbsp;MB</td><td align="right">162&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">13&nbsp;MB</td><td align="right">159&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.64 display_eval

![display_eval: stages 4 and 6 take 48% to 81% of a run. Simulation, GLB takes 4.5 s. Simulation, STEP takes 5.6 s. Simulation, STL takes 4.1 s. Simulation, OBJ takes 6.4 s. Visual, GLB takes 6.3 s. Visual, OBJ takes 7.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/laptop_display-eval.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.4 | 1.5 | 0.4&nbsp;ms | 1.9 | 0.1 | 0.2 | 0.2 | 4.5 |
| Simulation, STEP | 0.1 | 0.5 | 1.4 | 0.3&nbsp;ms | 1.7 | 1.4 | 0.2 | 0.2 | 5.6 |
| Simulation, STL | 0.1 | 0.4 | 1.3 | 0.2&nbsp;ms | 1.8 | 0.1 | 0.2 | 0.2 | 4.1 |
| Simulation, OBJ | 0.1 | 0.4 | 1.3 | 0.2&nbsp;ms | 1.8 | 2.3 | 0.3 | 0.2 | 6.4 |
| Visual, GLB | 0.1 | 0.4 | 1.4 | 0.4&nbsp;ms | 3.8 | 59&nbsp;ms | 0.4 | 0.2 | 6.3 |
| Visual, OBJ | 0.1 | 0.5 | 1.5 | 0.3&nbsp;ms | 3.3 | 1.6 | 0.5 | 0.2 | 7.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [byrantech/laptop](https://github.com/byrantech/laptop)<br>Board: `display_eval.kicad_pcb` |
|---|---|
| Folder | motherboard / display_eval |
| Complexity | 296&nbsp;/&nbsp;1000 (size&nbsp;171, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20240225) |
| Parts,&nbsp;tracks,&nbsp;vias | 10, 577, 108 |
| Triangles,&nbsp;simulation | 523,320 in 47 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">311&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">66&nbsp;MB</td><td align="right">353&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">26&nbsp;MB</td><td align="right">286&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">52&nbsp;MB</td><td align="right">383&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">322&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">36&nbsp;MB</td><td align="right">348&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.65 display_eval_short

![display_eval_short: stages 4 and 6 take 46% to 80% of a run. Simulation, GLB takes 2.2 s. Simulation, STEP takes 3.0 s. Simulation, STL takes 2.1 s. Simulation, OBJ takes 3.0 s. Visual, GLB takes 3.2 s. Visual, OBJ takes 3.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/laptop_display-eval-short.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 87&nbsp;ms | 0.2 | 0.7 | 0.2&nbsp;ms | 0.8 | 31&nbsp;ms | 0.1 | 0.3 | 2.2 |
| Simulation, STEP | 89&nbsp;ms | 0.2 | 0.6 | 0.2&nbsp;ms | 0.8 | 1.0 | 0.1 | 0.2 | 3.0 |
| Simulation, STL | 0.1 | 0.2 | 0.6 | 0.2&nbsp;ms | 0.8 | 48&nbsp;ms | 0.1 | 0.3 | 2.1 |
| Simulation, OBJ | 82&nbsp;ms | 0.2 | 0.6 | 0.2&nbsp;ms | 0.8 | 1.0 | 0.1 | 0.2 | 3.0 |
| Visual, GLB | 82&nbsp;ms | 0.2 | 0.6 | 0.2&nbsp;ms | 1.9 | 21&nbsp;ms | 0.1 | 0.2 | 3.2 |
| Visual, OBJ | 90&nbsp;ms | 0.2 | 0.6 | 0.2&nbsp;ms | 2.0 | 0.7 | 0.1 | 0.2 | 3.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [byrantech/laptop](https://github.com/byrantech/laptop)<br>Board: `display_eval_short.kicad_pcb` |
|---|---|
| Folder | motherboard / display_eval_short |
| Complexity | 224&nbsp;/&nbsp;1000 (size&nbsp;134, features&nbsp;90) |
| KESE&nbsp;features | through vias, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20240225) |
| Parts,&nbsp;tracks,&nbsp;vias | 4, 121, 13 |
| Triangles,&nbsp;simulation | 165,308 in 43 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">5.9&nbsp;MB</td><td align="right">174&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">25&nbsp;MB</td><td align="right">188&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">8.3&nbsp;MB</td><td align="right">184&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">17&nbsp;MB</td><td align="right">183&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.1&nbsp;MB</td><td align="right">145&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">12&nbsp;MB</td><td align="right">141&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.66 motherboard

![motherboard: stages 4 and 6 take 54% to 83% of a run. Simulation, GLB takes 70 s. Simulation, STEP takes 84 s. Simulation, STL takes 71 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/laptop_motherboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.1 | 6.3 | 24.5 | 3&nbsp;ms | 32.0 | 1.2 | 3.6 | 0.4 | 70.2 |
| Simulation, STEP | 2.1 | 5.8 | 23.8 | 1&nbsp;ms | 32.4 | 16.2 | 3.6 | 0.4 | 84.5 |
| Simulation, STL | 2.2 | 5.9 | 24.0 | 2&nbsp;ms | 31.9 | 2.9 | 3.6 | 0.5 | 71.1 |
| Simulation, OBJ | 2.1 | 6.0 | 24.6 | 2&nbsp;ms | 32.7 | 36.2 | 4.0 | 0.5 | 106.0 |
| Visual, GLB | 2.1 | 6.2 | 24.4 | 2&nbsp;ms | 59.9 | 0.7 | 7.5 | 0.4 | 101.1 |
| Visual, OBJ | 2.3 | 6.2 | 24.7 | 2&nbsp;ms | 60.6 | 21.2 | 7.5 | 0.5 | 122.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [byrantech/laptop](https://github.com/byrantech/laptop)<br>Board: `motherboard.kicad_pcb` |
|---|---|
| Folder | motherboard |
| Complexity | 417&nbsp;/&nbsp;1000 (size&nbsp;247, features&nbsp;170) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241007) |
| Parts,&nbsp;tracks,&nbsp;vias | 258, 4,080, 734 |
| Triangles,&nbsp;simulation | 6,514,532 in 491 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">222&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">900&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">326&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">698&nbsp;MB</td><td align="right">4.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">132&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">425&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.67 power

![power: stages 4 and 6 take 54% to 82% of a run. Simulation, GLB takes 24 s. Simulation, STEP takes 31 s. Simulation, STL takes 25 s. Simulation, OBJ takes 33 s. Visual, GLB takes 32 s. Visual, OBJ takes 39 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/laptop_power.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.2 | 2.0 | 8.4 | 0.7&nbsp;ms | 11.1 | 0.3 | 1.1 | 0.3 | 24.3 |
| Simulation, STEP | 1.5 | 2.1 | 9.0 | 1.0&nbsp;ms | 10.8 | 6.0 | 1.1 | 0.3 | 30.7 |
| Simulation, STL | 1.1 | 2.1 | 9.2 | 0.6&nbsp;ms | 10.7 | 0.5 | 1.0 | 0.3 | 24.8 |
| Simulation, OBJ | 1.2 | 1.9 | 7.5 | 0.6&nbsp;ms | 10.4 | 11.2 | 0.9 | 0.3 | 33.5 |
| Visual, GLB | 1.4 | 2.3 | 7.7 | 0.8&nbsp;ms | 18.7 | 0.2 | 1.7 | 0.3 | 32.3 |
| Visual, OBJ | 1.1 | 2.0 | 8.1 | 0.6&nbsp;ms | 17.8 | 7.4 | 2.0 | 0.3 | 38.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [byrantech/laptop](https://github.com/byrantech/laptop)<br>Board: `power.kicad_pcb` |
|---|---|
| Folder | power |
| Complexity | 394&nbsp;/&nbsp;1000 (size&nbsp;239, features&nbsp;155) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 13 |
| File&nbsp;format | KiCad 9 (20241007) |
| Parts,&nbsp;tracks,&nbsp;vias | 176, 1,129, 167 |
| Triangles,&nbsp;simulation | 1,717,024 in 153 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">59&nbsp;MB</td><td align="right">647&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">289&nbsp;MB</td><td align="right">811&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">86&nbsp;MB</td><td align="right">658&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">179&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">42&nbsp;MB</td><td align="right">857&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">126&nbsp;MB</td><td align="right">959&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.68 switch

![switch: stages 4 and 6 take 42% to 65% of a run. Simulation, GLB takes 0.8 s. Simulation, STEP takes 1.2 s. Simulation, STL takes 0.8 s. Simulation, OBJ takes 1.1 s. Visual, GLB takes 1.0 s. Visual, OBJ takes 1.2 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/laptop_switch.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 15&nbsp;ms | 52&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.3 | 8&nbsp;ms | 29&nbsp;ms | 0.3 | 0.8 |
| Simulation, STEP | 15&nbsp;ms | 46&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.4 | 0.3 | 35&nbsp;ms | 0.3 | 1.2 |
| Simulation, STL | 19&nbsp;ms | 54&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 12&nbsp;ms | 27&nbsp;ms | 0.2 | 0.8 |
| Simulation, OBJ | 18&nbsp;ms | 54&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 0.2 | 41&nbsp;ms | 0.2 | 1.1 |
| Visual, GLB | 17&nbsp;ms | 48&nbsp;ms | 0.1 | 0.2&nbsp;ms | 0.5 | 9&nbsp;ms | 58&nbsp;ms | 0.2 | 1.0 |
| Visual, OBJ | 19&nbsp;ms | 49&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.5 | 0.2 | 60&nbsp;ms | 0.2 | 1.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [byrantech/laptop](https://github.com/byrantech/laptop)<br>Board: `switch.kicad_pcb` |
|---|---|
| Folder | switch |
| Complexity | 151&nbsp;/&nbsp;1000 (size&nbsp;101, features&nbsp;50) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>curved board outline,<br>TrueType text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241007) |
| Parts,&nbsp;tracks,&nbsp;vias | 6, 32, 5 |
| Triangles,&nbsp;simulation | 39,470 in 15 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.4&nbsp;MB</td><td align="right">46&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">5.5&nbsp;MB</td><td align="right">52&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">2.0&nbsp;MB</td><td align="right">48&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.7&nbsp;MB</td><td align="right">60&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">1.0&nbsp;MB</td><td align="right">71&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">2.9&nbsp;MB</td><td align="right">78&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.69 motherboard-stable

![motherboard-stable: stages 4 and 6 take 67% to 86% of a run. Simulation, GLB takes 5 min. Simulation, STEP takes 7 min. Simulation, STL takes 6 min. Visual, GLB takes 8 min. Visual, OBJ takes 9 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/motherboard_motherboard-stable.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.7 | 27.2 | 131.4 | 5&nbsp;ms | 110.6 | 8.4 | 20.1 | 1.0 | 302.5 |
| Simulation, STEP | 3.7 | 30.1 | 136.6 | 4&nbsp;ms | 126.0 | 71.8 | 25.0 | 1.1 | 394.3 |
| Simulation, STL | 4.6 | 29.6 | 146.5 | 5&nbsp;ms | 121.8 | 17.4 | 22.6 | 1.3 | 343.7 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB | 3.7 | 30.4 | 139.3 | 4&nbsp;ms | 282.3 | 2.4 | 30.8 | 0.7 | 489.6 |
| Visual, OBJ | 4.4 | 28.4 | 134.8 | 0.2 | 277.4 | 81.2 | 32.7 | 1.0 | 560.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [c4puter/motherboard](https://github.com/c4puter/motherboard)<br>Board: `motherboard-stable.kicad_pcb` |
|---|---|
| Complexity | 402&nbsp;/&nbsp;1000 (size&nbsp;327, features&nbsp;75) |
| KESE&nbsp;features | through vias, slotted holes,<br>drill offsets, filled zones,<br>copper text, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 591, 22,267, 2,074 |
| Triangles,&nbsp;simulation | 22,500,734 in 1157 parts |
| Verifier | Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">775&nbsp;MB</td><td align="right">4.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">3.1&nbsp;GB</td><td align="right">6.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.1&nbsp;GB</td><td align="right">4.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">389&nbsp;MB</td><td align="right">6.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.3&nbsp;GB</td><td align="right">8.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.70 motherboard

![motherboard: stages 4 and 6 take 53% to 87% of a run. Simulation, GLB takes 5 min. Simulation, STEP takes 6 min. Simulation, STL takes 5 min. Simulation, OBJ takes 8 min. Visual, GLB takes 8 min. Visual, OBJ takes 9 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/motherboard_motherboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.5 | 27.8 | 135.1 | 5&nbsp;ms | 111.7 | 7.1 | 20.4 | 0.8 | 306.4 |
| Simulation, STEP | 3.7 | 27.8 | 132.8 | 4&nbsp;ms | 106.6 | 61.4 | 19.2 | 1.0 | 352.4 |
| Simulation, STL | 3.7 | 27.5 | 132.6 | 4&nbsp;ms | 102.8 | 11.9 | 17.2 | 0.9 | 296.6 |
| Simulation, OBJ | 4.3 | 28.6 | 135.9 | 4&nbsp;ms | 104.3 | 162.5 | 18.3 | 1.1 | 455.0 |
| Visual, GLB | 3.7 | 26.6 | 131.1 | 4&nbsp;ms | 266.9 | 2.9 | 23.8 | 0.6 | 455.7 |
| Visual, OBJ | 3.8 | 27.6 | 132.1 | 4&nbsp;ms | 263.7 | 72.5 | 23.1 | 0.6 | 523.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [c4puter/motherboard](https://github.com/c4puter/motherboard)<br>Board: `motherboard.kicad_pcb` |
|---|---|
| Complexity | 402&nbsp;/&nbsp;1000 (size&nbsp;327, features&nbsp;75) |
| KESE&nbsp;features | through vias, slotted holes,<br>drill offsets, filled zones,<br>copper text, curved board outline |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 5 (20160815) |
| Parts,&nbsp;tracks,&nbsp;vias | 591, 22,267, 2,074 |
| Triangles,&nbsp;simulation | 22,500,734 in 1157 parts |
| Verifier | PASS in all six runs |
| Run&nbsp;again | Simulation, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">775&nbsp;MB</td><td align="right">4.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">3.1&nbsp;GB</td><td align="right">6.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.1&nbsp;GB</td><td align="right">4.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">2.5&nbsp;GB</td><td align="right">14&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">389&nbsp;MB</td><td align="right">6.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.3&nbsp;GB</td><td align="right">7.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.71 OBC Development Board

![OBC Development Board: stages 4 and 6 take 51% to 81% of a run. Simulation, GLB takes 53 s. Simulation, STEP takes 59 s. Simulation, STL takes 53 s. Simulation, OBJ takes 78 s. Visual, GLB takes 75 s. Visual, OBJ takes 86 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/cts-sat-2-obc-pcb_OBC-Development-Board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 6.4 | 21.5 | 4&nbsp;ms | 19.8 | 1.0 | 2.6 | 0.4 | 52.7 |
| Simulation, STEP | 1.0 | 6.2 | 20.1 | 2&nbsp;ms | 19.3 | 10.1 | 2.4 | 0.4 | 59.4 |
| Simulation, STL | 1.4 | 6.1 | 21.6 | 2&nbsp;ms | 19.2 | 2.3 | 2.3 | 0.4 | 53.4 |
| Simulation, OBJ | 1.2 | 5.7 | 20.2 | 3&nbsp;ms | 19.7 | 28.2 | 2.8 | 0.3 | 78.1 |
| Visual, GLB | 1.1 | 6.6 | 21.6 | 1&nbsp;ms | 39.7 | 0.4 | 5.8 | 0.4 | 75.5 |
| Visual, OBJ | 1.1 | 6.0 | 20.7 | 0.9&nbsp;ms | 37.8 | 13.7 | 6.1 | 0.3 | 85.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [calgarytospace/cts-sat-2-obc-pcb](https://github.com/calgarytospace/cts-sat-2-obc-pcb)<br>Board: `OBC Development Board.kicad_pcb` |
|---|---|
| Folder | CTS-SAT-1 Hardware |
| Complexity | 337&nbsp;/&nbsp;1000 (size&nbsp;237, features&nbsp;100) |
| KESE&nbsp;features | through vias, padstacks, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 221, 1,889, 667 |
| Triangles,&nbsp;simulation | 5,120,894 in 206 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">176&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">525&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">256&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">565&nbsp;MB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">87&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">280&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.72 CTS-SAT-2-OBC-PCB

![CTS-SAT-2-OBC-PCB: stages 4 and 6 take 52% to 83% of a run. Simulation, GLB takes 42 s. Simulation, STEP takes 53 s. Simulation, STL takes 43 s. Simulation, OBJ takes 65 s. Visual, GLB takes 66 s. Visual, OBJ takes 79 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/cts-sat-2-obc-pcb_CTS-SAT-2-OBC-PCB.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.4 | 4.4 | 16.4 | 2&nbsp;ms | 16.0 | 0.8 | 2.4 | 0.4 | 41.7 |
| Simulation, STEP | 1.2 | 4.4 | 16.6 | 3&nbsp;ms | 16.3 | 11.5 | 2.3 | 0.4 | 52.7 |
| Simulation, STL | 1.3 | 4.4 | 16.8 | 3&nbsp;ms | 16.6 | 1.7 | 2.2 | 0.3 | 43.3 |
| Simulation, OBJ | 1.3 | 4.2 | 16.9 | 2&nbsp;ms | 16.6 | 23.4 | 2.2 | 0.4 | 64.9 |
| Visual, GLB | 1.3 | 4.3 | 16.7 | 2&nbsp;ms | 38.0 | 0.5 | 4.8 | 0.4 | 65.9 |
| Visual, OBJ | 1.2 | 4.4 | 16.6 | 1&nbsp;ms | 37.9 | 13.6 | 4.9 | 0.4 | 79.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [calgarytospace/cts-sat-2-obc-pcb](https://github.com/calgarytospace/cts-sat-2-obc-pcb)<br>Board: `CTS-SAT-2-OBC-PCB.kicad_pcb` |
|---|---|
| Folder | Hardware |
| Complexity | 395&nbsp;/&nbsp;1000 (size&nbsp;280, features&nbsp;115) |
| KESE&nbsp;features | through vias, padstacks,<br>slotted holes, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 219, 1,783, 433 |
| Triangles,&nbsp;simulation | 4,523,508 in 424 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">149&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">573&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">226&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">475&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">93&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">293&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.73 MiniLatteLedArray

![MiniLatteLedArray: stages 4 and 6 take 60% to 83% of a run. Simulation, GLB takes 14 s. Simulation, STEP takes 19 s. Simulation, STL takes 15 s. Simulation, OBJ takes 20 s. Visual, GLB takes 20 s. Visual, OBJ takes 25 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/minilatte_MiniLatteLedArray.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.3 | 5.2 | 0.7&nbsp;ms | 6.1 | 0.2 | 0.8 | 0.2 | 14.3 |
| Simulation, STEP | 0.5 | 1.2 | 5.1 | 0.6&nbsp;ms | 6.4 | 4.8 | 0.8 | 0.2 | 18.9 |
| Simulation, STL | 0.5 | 1.2 | 5.4 | 0.7&nbsp;ms | 6.7 | 0.4 | 0.8 | 0.2 | 15.2 |
| Simulation, OBJ | 0.5 | 1.3 | 5.4 | 1&nbsp;ms | 6.8 | 4.7 | 0.8 | 0.2 | 19.7 |
| Visual, GLB | 0.5 | 1.3 | 5.2 | 0.8&nbsp;ms | 11.3 | 0.1 | 1.2 | 0.2 | 20.0 |
| Visual, OBJ | 0.5 | 1.3 | 5.2 | 0.8&nbsp;ms | 11.5 | 4.6 | 1.7 | 0.2 | 24.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cath272/minilatte](https://github.com/cath272/minilatte)<br>Board: `MiniLatteLedArray.kicad_pcb` |
|---|---|
| Folder | MiniLatteLedArray |
| Complexity | 294&nbsp;/&nbsp;1000 (size&nbsp;204, features&nbsp;90) |
| KESE&nbsp;features | through vias, arc tracks,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 225, 1,844, 229 |
| Triangles,&nbsp;simulation | 1,114,792 in 235 parts |
| Note | panel |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">626&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">201&nbsp;MB</td><td align="right">665&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">56&nbsp;MB</td><td align="right">631&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">117&nbsp;MB</td><td align="right">760&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">37&nbsp;MB</td><td align="right">933&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">110&nbsp;MB</td><td align="right">806&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.74 MiniLatte

![MiniLatte: stages 4 and 6 take 53% to 84% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 3 min. Simulation, STL takes 2 min. Simulation, OBJ takes 4 min. Visual, GLB takes 4 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/minilatte_MiniLatte.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 5.5 | 10.3 | 40.3 | 2&nbsp;ms | 71.5 | 2.5 | 7.7 | 0.5 | 138.3 |
| Simulation, STEP | 5.5 | 10.6 | 42.1 | 2&nbsp;ms | 74.8 | 38.8 | 7.4 | 0.6 | 179.8 |
| Simulation, STL | 5.9 | 10.5 | 42.3 | 2&nbsp;ms | 76.6 | 5.2 | 8.0 | 0.5 | 149.0 |
| Simulation, OBJ | 5.6 | 11.0 | 42.0 | 2&nbsp;ms | 80.8 | 85.1 | 8.3 | 0.6 | 233.4 |
| Visual, GLB | 6.2 | 11.5 | 46.0 | 2&nbsp;ms | 132.9 | 2.6 | 13.5 | 0.5 | 213.3 |
| Visual, OBJ | 5.7 | 10.2 | 40.8 | 2&nbsp;ms | 135.9 | 49.2 | 14.7 | 0.5 | 257.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cath272/minilatte](https://github.com/cath272/minilatte)<br>Board: `MiniLatte.kicad_pcb` |
|---|---|
| Folder | PCB |
| Complexity | 450&nbsp;/&nbsp;1000 (size&nbsp;315, features&nbsp;135) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 495, 11,156, 736 |
| Triangles,&nbsp;simulation | 8,966,200 in 848 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">306&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.5&nbsp;GB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">448&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">971&nbsp;MB</td><td align="right">5.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">232&nbsp;MB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">752&nbsp;MB</td><td align="right">4.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.75 hdmi-edp2

![hdmi-edp2: stages 4 and 6 take 50% to 81% of a run. Simulation, GLB takes 10 s. Simulation, STEP takes 13 s. Simulation, STL takes 10 s. Simulation, OBJ takes 16 s. Visual, GLB takes 15 s. Visual, OBJ takes 20 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_hdmi-edp2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.1 | 3.6 | 0.5&nbsp;ms | 4.1 | 0.2 | 0.6 | 0.2 | 10.1 |
| Simulation, STEP | 0.4 | 1.1 | 3.5 | 0.3&nbsp;ms | 4.1 | 3.3 | 0.6 | 0.2 | 13.2 |
| Simulation, STL | 0.4 | 1.1 | 3.5 | 0.5&nbsp;ms | 4.2 | 0.3 | 0.6 | 0.2 | 10.2 |
| Simulation, OBJ | 0.4 | 1.2 | 3.7 | 0.4&nbsp;ms | 4.5 | 5.9 | 0.6 | 0.2 | 16.5 |
| Visual, GLB | 0.4 | 1.0 | 3.5 | 0.4&nbsp;ms | 9.0 | 0.1 | 1.0 | 0.2 | 15.4 |
| Visual, OBJ | 0.4 | 1.2 | 3.8 | 0.6&nbsp;ms | 8.3 | 4.4 | 1.4 | 0.2 | 19.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `hdmi-edp2.kicad_pcb` |
|---|---|
| Folder | hdmi-edp2 |
| Complexity | 329&nbsp;/&nbsp;1000 (size&nbsp;254, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 93, 910, 170 |
| Triangles,&nbsp;simulation | 1,071,490 in 92 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">37&nbsp;MB</td><td align="right">460&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">156&nbsp;MB</td><td align="right">547&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">54&nbsp;MB</td><td align="right">452&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">108&nbsp;MB</td><td align="right">740&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">635&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">81&nbsp;MB</td><td align="right">626&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.76 nref-batterypack-backside

![nref-batterypack-backside: stages 4 and 6 take 38% to 72% of a run. Simulation, GLB takes 1.5 s. Simulation, STEP takes 2.4 s. Simulation, STL takes 1.5 s. Simulation, OBJ takes 1.9 s. Visual, GLB takes 2.1 s. Visual, OBJ takes 2.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-batterypack-v3_nref-batterypack-backside.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 0.5 | 16&nbsp;ms | 48&nbsp;ms | 0.3 | 1.5 |
| Simulation, STEP | 0.2 | 0.1 | 0.4 | 0.1&nbsp;ms | 0.5 | 0.8 | 48&nbsp;ms | 0.3 | 2.4 |
| Simulation, STL | 0.2 | 0.1 | 0.4 | 0.1&nbsp;ms | 0.5 | 31&nbsp;ms | 49&nbsp;ms | 0.2 | 1.5 |
| Simulation, OBJ | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 0.5 | 0.5 | 48&nbsp;ms | 0.2 | 1.9 |
| Visual, GLB | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 1.2 | 13&nbsp;ms | 79&nbsp;ms | 0.3 | 2.1 |
| Visual, OBJ | 0.1 | 0.1 | 0.4 | 0.2&nbsp;ms | 1.1 | 0.4 | 0.1 | 0.2 | 2.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-batterypack-backside.kicad_pcb` |
|---|---|
| Folder | nref-batterypack-v3 |
| Complexity | 229&nbsp;/&nbsp;1000 (size&nbsp;114, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 3, 16, 13 |
| Triangles,&nbsp;simulation | 82,176 in 16 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">2.9&nbsp;MB</td><td align="right">183&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">13&nbsp;MB</td><td align="right">185&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">4.1&nbsp;MB</td><td align="right">178&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">8.0&nbsp;MB</td><td align="right">176&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">2.3&nbsp;MB</td><td align="right">151&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.3&nbsp;MB</td><td align="right">153&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.77 nref-batterypack

![nref-batterypack: stages 4 and 6 take 49% to 81% of a run. Simulation, GLB takes 9.0 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.5 s. Simulation, OBJ takes 14 s. Visual, GLB takes 13 s. Visual, OBJ takes 18 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-batterypack-v3_nref-batterypack.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.0 | 3.0 | 0.4&nbsp;ms | 3.6 | 0.2 | 0.6 | 0.2 | 9.0 |
| Simulation, STEP | 0.5 | 1.0 | 3.1 | 0.3&nbsp;ms | 3.3 | 2.8 | 0.5 | 0.3 | 11.6 |
| Simulation, STL | 0.4 | 1.0 | 3.2 | 0.2&nbsp;ms | 3.8 | 0.3 | 0.6 | 0.3 | 9.5 |
| Simulation, OBJ | 0.4 | 1.0 | 3.1 | 0.5&nbsp;ms | 3.5 | 4.8 | 0.5 | 0.3 | 13.6 |
| Visual, GLB | 0.4 | 1.0 | 3.1 | 0.3&nbsp;ms | 7.7 | 0.1 | 0.9 | 0.2 | 13.4 |
| Visual, OBJ | 0.4 | 1.0 | 3.2 | 0.4&nbsp;ms | 8.0 | 3.6 | 1.1 | 0.2 | 17.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-batterypack.kicad_pcb` |
|---|---|
| Folder | nref-batterypack-v3 |
| Complexity | 355&nbsp;/&nbsp;1000 (size&nbsp;240, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 85, 776, 191 |
| Triangles,&nbsp;simulation | 978,200 in 77 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">33&nbsp;MB</td><td align="right">421&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">142&nbsp;MB</td><td align="right">545&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">49&nbsp;MB</td><td align="right">418&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">98&nbsp;MB</td><td align="right">700&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">24&nbsp;MB</td><td align="right">617&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">72&nbsp;MB</td><td align="right">599&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.78 nref-batterypack-backside

![nref-batterypack-backside: stages 4 and 6 take 37% to 61% of a run. Simulation, GLB takes 1.0 s. Simulation, STEP takes 1.2 s. Simulation, STL takes 1.0 s. Simulation, OBJ takes 1.2 s. Visual, GLB takes 1.2 s. Visual, OBJ takes 1.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-batterypack_nref-batterypack-backside.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 99&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 7&nbsp;ms | 23&nbsp;ms | 0.2 | 1.0 |
| Simulation, STEP | 0.1 | 90&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 0.3 | 20&nbsp;ms | 0.3 | 1.2 |
| Simulation, STL | 0.1 | 0.1 | 0.2 | 0.1&nbsp;ms | 0.3 | 11&nbsp;ms | 25&nbsp;ms | 0.2 | 1.0 |
| Simulation, OBJ | 0.1 | 0.1 | 0.2 | 0.1&nbsp;ms | 0.3 | 0.2 | 21&nbsp;ms | 0.2 | 1.2 |
| Visual, GLB | 0.1 | 90&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.6 | 8&nbsp;ms | 49&nbsp;ms | 0.2 | 1.2 |
| Visual, OBJ | 0.2 | 0.1 | 0.2 | 0.1&nbsp;ms | 0.6 | 0.3 | 48&nbsp;ms | 0.2 | 1.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-batterypack-backside.kicad_pcb` |
|---|---|
| Folder | nref-batterypack |
| Complexity | 122&nbsp;/&nbsp;1000 (size&nbsp;72, features&nbsp;50) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>curved board outline,<br>knockout text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 1, 12, 2 |
| Triangles,&nbsp;simulation | 31,336 in 12 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.2&nbsp;MB</td><td align="right">72&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">7.0&nbsp;MB</td><td align="right">77&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">1.6&nbsp;MB</td><td align="right">72&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.2&nbsp;MB</td><td align="right">79&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">1.1&nbsp;MB</td><td align="right">88&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.1&nbsp;MB</td><td align="right">101&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.79 nref-batterypack

![nref-batterypack: stages 4 and 6 take 49% to 81% of a run. Simulation, GLB takes 6.7 s. Simulation, STEP takes 8.7 s. Simulation, STL takes 6.7 s. Simulation, OBJ takes 9.6 s. Visual, GLB takes 9.6 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-batterypack_nref-batterypack.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.7 | 2.3 | 0.4&nbsp;ms | 2.7 | 98&nbsp;ms | 0.3 | 0.3 | 6.7 |
| Simulation, STEP | 0.3 | 0.7 | 2.2 | 0.4&nbsp;ms | 2.6 | 2.3 | 0.4 | 0.2 | 8.7 |
| Simulation, STL | 0.3 | 0.7 | 2.2 | 0.3&nbsp;ms | 2.7 | 0.2 | 0.4 | 0.3 | 6.7 |
| Simulation, OBJ | 0.3 | 0.6 | 2.1 | 0.3&nbsp;ms | 2.6 | 3.3 | 0.4 | 0.2 | 9.6 |
| Visual, GLB | 0.4 | 0.7 | 2.2 | 0.3&nbsp;ms | 5.6 | 71&nbsp;ms | 0.5 | 0.3 | 9.6 |
| Visual, OBJ | 0.3 | 0.7 | 2.3 | 0.4&nbsp;ms | 5.1 | 2.6 | 0.6 | 0.2 | 11.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-batterypack.kicad_pcb` |
|---|---|
| Folder | nref-batterypack |
| Complexity | 334&nbsp;/&nbsp;1000 (size&nbsp;224, features&nbsp;110) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 59, 456, 67 |
| Triangles,&nbsp;simulation | 555,620 in 64 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">321&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">88&nbsp;MB</td><td align="right">389&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">28&nbsp;MB</td><td align="right">320&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">56&nbsp;MB</td><td align="right">422&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">425&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">43&nbsp;MB</td><td align="right">368&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.80 nref-camera-adapter

![nref-camera-adapter: stages 4 and 6 take 42% to 75% of a run. Simulation, GLB takes 3.2 s. Simulation, STEP takes 4.3 s. Simulation, STL takes 3.4 s. Simulation, OBJ takes 5.0 s. Visual, GLB takes 4.4 s. Visual, OBJ takes 5.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-camera-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.0 | 0.2&nbsp;ms | 1.1 | 51&nbsp;ms | 0.2 | 0.2 | 3.2 |
| Simulation, STEP | 0.2 | 0.4 | 0.9 | 0.2&nbsp;ms | 1.2 | 1.2 | 0.2 | 0.2 | 4.3 |
| Simulation, STL | 0.2 | 0.4 | 1.0 | 0.2&nbsp;ms | 1.2 | 0.1 | 0.2 | 0.2 | 3.4 |
| Simulation, OBJ | 0.2 | 0.4 | 1.0 | 0.2&nbsp;ms | 1.2 | 1.9 | 0.2 | 0.3 | 5.0 |
| Visual, GLB | 0.2 | 0.4 | 1.0 | 0.3&nbsp;ms | 2.3 | 44&nbsp;ms | 0.3 | 0.2 | 4.4 |
| Visual, OBJ | 0.2 | 0.4 | 1.0 | 0.2&nbsp;ms | 2.4 | 1.1 | 0.2 | 0.3 | 5.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-camera-adapter.kicad_pcb` |
|---|---|
| Folder | nref-camera-adapter |
| Complexity | 236&nbsp;/&nbsp;1000 (size&nbsp;146, features&nbsp;90) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 157, 101 |
| Triangles,&nbsp;simulation | 308,202 in 36 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">273&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">31&nbsp;MB</td><td align="right">278&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">15&nbsp;MB</td><td align="right">269&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">30&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.0&nbsp;MB</td><td align="right">233&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">21&nbsp;MB</td><td align="right">237&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.81 reform-camera

![reform-camera: stages 4 and 6 take 54% to 84% of a run. Simulation, GLB takes 20 s. Simulation, STEP takes 24 s. Simulation, STL takes 20 s. Simulation, OBJ takes 29 s. Visual, GLB takes 26 s. Visual, OBJ takes 34 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_reform-camera.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.0 | 7.9 | 0.5&nbsp;ms | 8.1 | 0.3 | 0.8 | 0.4 | 20.1 |
| Simulation, STEP | 0.6 | 1.6 | 7.4 | 0.4&nbsp;ms | 8.0 | 5.6 | 0.8 | 0.3 | 24.3 |
| Simulation, STL | 0.6 | 1.7 | 7.5 | 0.4&nbsp;ms | 8.3 | 0.4 | 0.8 | 0.3 | 19.6 |
| Simulation, OBJ | 0.6 | 1.6 | 7.4 | 0.6&nbsp;ms | 8.0 | 9.8 | 0.9 | 0.3 | 28.6 |
| Visual, GLB | 0.6 | 1.7 | 7.4 | 0.4&nbsp;ms | 14.7 | 0.2 | 1.6 | 0.3 | 26.4 |
| Visual, OBJ | 0.6 | 1.7 | 7.8 | 0.4&nbsp;ms | 15.2 | 7.3 | 1.6 | 0.3 | 34.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `reform-camera.kicad_pcb` |
|---|---|
| Folder | nref-camera |
| Complexity | 356&nbsp;/&nbsp;1000 (size&nbsp;261, features&nbsp;95) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 114, 1,298, 235 |
| Triangles,&nbsp;simulation | 1,605,780 in 148 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">54&nbsp;MB</td><td align="right">613&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">253&nbsp;MB</td><td align="right">747&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">80&nbsp;MB</td><td align="right">622&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">165&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">755&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">119&nbsp;MB</td><td align="right">902&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.82 nref-flex-eth

![nref-flex-eth: stages 4 and 6 take 48% to 77% of a run. Simulation, GLB takes 2.0 s. Simulation, STEP takes 2.9 s. Simulation, STL takes 2.0 s. Simulation, OBJ takes 2.6 s. Visual, GLB takes 3.0 s. Visual, OBJ takes 3.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-flex-eth.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.7 | 0.2&nbsp;ms | 0.7 | 27&nbsp;ms | 95&nbsp;ms | 0.2 | 2.0 |
| Simulation, STEP | 0.1 | 0.2 | 0.7 | 0.3&nbsp;ms | 0.7 | 0.9 | 94&nbsp;ms | 0.2 | 2.9 |
| Simulation, STL | 0.1 | 0.2 | 0.6 | 0.1&nbsp;ms | 0.7 | 34&nbsp;ms | 84&nbsp;ms | 0.3 | 2.0 |
| Simulation, OBJ | 98&nbsp;ms | 0.2 | 0.6 | 0.2&nbsp;ms | 0.7 | 0.7 | 80&nbsp;ms | 0.2 | 2.6 |
| Visual, GLB | 94&nbsp;ms | 0.2 | 0.8 | 0.2&nbsp;ms | 1.6 | 24&nbsp;ms | 0.2 | 0.2 | 3.0 |
| Visual, OBJ | 94&nbsp;ms | 0.2 | 0.6 | 0.2&nbsp;ms | 1.7 | 0.7 | 0.2 | 0.2 | 3.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-flex-eth.kicad_pcb` |
|---|---|
| Folder | nref-flex / nref-flex-eth |
| Complexity | 176&nbsp;/&nbsp;1000 (size&nbsp;126, features&nbsp;50) |
| KESE&nbsp;features | through vias, filled zones,<br>TrueType text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 88, 98 |
| Triangles,&nbsp;simulation | 147,362 in 22 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">5.2&nbsp;MB</td><td align="right">212&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">18&nbsp;MB</td><td align="right">223&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">7.4&nbsp;MB</td><td align="right">211&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">15&nbsp;MB</td><td align="right">217&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.4&nbsp;MB</td><td align="right">205&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">15&nbsp;MB</td><td align="right">203&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.83 nref-flex-dp-140mm

![nref-flex-dp-140mm: stages 4 and 6 take 47% to 77% of a run. Simulation, GLB takes 1.9 s. Simulation, STEP takes 2.7 s. Simulation, STL takes 1.8 s. Simulation, OBJ takes 2.4 s. Visual, GLB takes 2.4 s. Visual, OBJ takes 2.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-flex-dp-140mm.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.6 | 0.1&nbsp;ms | 0.7 | 20&nbsp;ms | 69&nbsp;ms | 0.2 | 1.9 |
| Simulation, STEP | 0.1 | 0.1 | 0.5 | 0.1&nbsp;ms | 0.8 | 0.9 | 51&nbsp;ms | 0.2 | 2.7 |
| Simulation, STL | 0.1 | 0.1 | 0.5 | 0.1&nbsp;ms | 0.7 | 25&nbsp;ms | 67&nbsp;ms | 0.2 | 1.8 |
| Simulation, OBJ | 0.1 | 0.1 | 0.6 | 0.1&nbsp;ms | 0.8 | 0.5 | 51&nbsp;ms | 0.2 | 2.4 |
| Visual, GLB | 0.1 | 0.1 | 0.5 | 0.1&nbsp;ms | 1.3 | 19&nbsp;ms | 0.1 | 0.2 | 2.4 |
| Visual, OBJ | 0.1 | 0.1 | 0.5 | 0.1&nbsp;ms | 1.3 | 0.6 | 0.1 | 0.2 | 2.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-flex-dp-140mm.kicad_pcb` |
|---|---|
| Folder | nref-flex / nref-flex-hdmi |
| Complexity | 165&nbsp;/&nbsp;1000 (size&nbsp;115, features&nbsp;50) |
| KESE&nbsp;features | through vias, filled zones,<br>TrueType text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 75, 40 |
| Triangles,&nbsp;simulation | 89,198 in 23 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">3.3&nbsp;MB</td><td align="right">185&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">16&nbsp;MB</td><td align="right">203&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">4.5&nbsp;MB</td><td align="right">190&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.1&nbsp;MB</td><td align="right">187&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.0&nbsp;MB</td><td align="right">174&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">11&nbsp;MB</td><td align="right">171&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.84 nref-flex-hdmi

![nref-flex-hdmi: stages 4 and 6 take 46% to 74% of a run. Simulation, GLB takes 1.7 s. Simulation, STEP takes 2.6 s. Simulation, STL takes 1.7 s. Simulation, OBJ takes 2.2 s. Visual, GLB takes 2.3 s. Visual, OBJ takes 2.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-flex-hdmi.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.1 | 0.5 | 0.1&nbsp;ms | 0.7 | 18&nbsp;ms | 59&nbsp;ms | 0.2 | 1.7 |
| Simulation, STEP | 0.1 | 0.2 | 0.5 | 0.1&nbsp;ms | 0.7 | 0.9 | 53&nbsp;ms | 0.2 | 2.6 |
| Simulation, STL | 0.1 | 0.1 | 0.5 | 0.1&nbsp;ms | 0.7 | 24&nbsp;ms | 57&nbsp;ms | 0.2 | 1.7 |
| Simulation, OBJ | 0.1 | 0.1 | 0.5 | 0.1&nbsp;ms | 0.7 | 0.5 | 57&nbsp;ms | 0.2 | 2.2 |
| Visual, GLB | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 1.3 | 19&nbsp;ms | 0.1 | 0.2 | 2.3 |
| Visual, OBJ | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 1.3 | 0.6 | 0.1 | 0.2 | 2.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-flex-hdmi.kicad_pcb` |
|---|---|
| Folder | nref-flex / nref-flex-hdmi |
| Complexity | 166&nbsp;/&nbsp;1000 (size&nbsp;116, features&nbsp;50) |
| KESE&nbsp;features | through vias, filled zones,<br>TrueType text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 76, 44 |
| Triangles,&nbsp;simulation | 91,684 in 23 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">3.4&nbsp;MB</td><td align="right">189&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">16&nbsp;MB</td><td align="right">195&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">4.6&nbsp;MB</td><td align="right">193&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.3&nbsp;MB</td><td align="right">194&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.1&nbsp;MB</td><td align="right">166&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">11&nbsp;MB</td><td align="right">167&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.85 nref-flex-pcie

![nref-flex-pcie: stages 4 and 6 take 45% to 75% of a run. Simulation, GLB takes 1.7 s. Simulation, STEP takes 2.5 s. Simulation, STL takes 1.7 s. Simulation, OBJ takes 2.2 s. Visual, GLB takes 2.5 s. Visual, OBJ takes 3.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-flex-pcie.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.4 | 0.2&nbsp;ms | 0.6 | 26&nbsp;ms | 66&nbsp;ms | 0.3 | 1.7 |
| Simulation, STEP | 0.1 | 0.1 | 0.5 | 0.2&nbsp;ms | 0.7 | 0.8 | 68&nbsp;ms | 0.2 | 2.5 |
| Simulation, STL | 0.1 | 0.2 | 0.4 | 0.1&nbsp;ms | 0.7 | 25&nbsp;ms | 64&nbsp;ms | 0.2 | 1.7 |
| Simulation, OBJ | 0.1 | 0.1 | 0.4 | 0.2&nbsp;ms | 0.6 | 0.6 | 88&nbsp;ms | 0.3 | 2.2 |
| Visual, GLB | 0.1 | 0.1 | 0.4 | 0.2&nbsp;ms | 1.4 | 20&nbsp;ms | 0.1 | 0.2 | 2.5 |
| Visual, OBJ | 0.1 | 0.1 | 0.4 | 0.2&nbsp;ms | 1.4 | 0.6 | 0.1 | 0.3 | 3.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-flex-pcie.kicad_pcb` |
|---|---|
| Folder | nref-flex / nref-flex-pcie |
| Complexity | 195&nbsp;/&nbsp;1000 (size&nbsp;115, features&nbsp;80) |
| KESE&nbsp;features | through vias, filled zones,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 95, 32 |
| Triangles,&nbsp;simulation | 97,104 in 24 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">3.4&nbsp;MB</td><td align="right">181&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">16&nbsp;MB</td><td align="right">195&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">4.9&nbsp;MB</td><td align="right">185&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.6&nbsp;MB</td><td align="right">190&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.5&nbsp;MB</td><td align="right">158&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.9&nbsp;MB</td><td align="right">166&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.86 nref-flex-sdcard

![nref-flex-sdcard: stages 4 and 6 take 45% to 75% of a run. Simulation, GLB takes 1.4 s. Simulation, STEP takes 2.1 s. Simulation, STL takes 1.3 s. Simulation, OBJ takes 1.7 s. Visual, GLB takes 2.3 s. Visual, OBJ takes 2.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-flex-sdcard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 97&nbsp;ms | 0.1 | 0.3 | 0.1&nbsp;ms | 0.6 | 15&nbsp;ms | 65&nbsp;ms | 0.2 | 1.4 |
| Simulation, STEP | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 0.6 | 0.7 | 50&nbsp;ms | 0.2 | 2.1 |
| Simulation, STL | 88&nbsp;ms | 0.1 | 0.3 | 0.1&nbsp;ms | 0.5 | 22&nbsp;ms | 52&nbsp;ms | 0.2 | 1.3 |
| Simulation, OBJ | 85&nbsp;ms | 0.1 | 0.3 | 0.1&nbsp;ms | 0.5 | 0.4 | 51&nbsp;ms | 0.2 | 1.7 |
| Visual, GLB | 95&nbsp;ms | 0.1 | 0.4 | 0.1&nbsp;ms | 1.4 | 20&nbsp;ms | 0.1 | 0.2 | 2.3 |
| Visual, OBJ | 0.1 | 0.1 | 0.3 | 0.1&nbsp;ms | 1.3 | 0.4 | 0.1 | 0.2 | 2.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-flex-sdcard.kicad_pcb` |
|---|---|
| Folder | nref-flex / nref-flex-sdcard |
| Complexity | 163&nbsp;/&nbsp;1000 (size&nbsp;113, features&nbsp;50) |
| KESE&nbsp;features | through vias, filled zones,<br>TrueType text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 32, 48 |
| Triangles,&nbsp;simulation | 93,212 in 19 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">3.4&nbsp;MB</td><td align="right">182&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">15&nbsp;MB</td><td align="right">199&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">4.7&nbsp;MB</td><td align="right">184&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.2&nbsp;MB</td><td align="right">184&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.0&nbsp;MB</td><td align="right">168&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">11&nbsp;MB</td><td align="right">158&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.87 nref-flex-sound

![nref-flex-sound: stages 4 and 6 take 45% to 73% of a run. Simulation, GLB takes 1.8 s. Simulation, STEP takes 2.6 s. Simulation, STL takes 1.6 s. Simulation, OBJ takes 2.4 s. Visual, GLB takes 2.4 s. Visual, OBJ takes 3.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-flex-sound.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.1 | 0.5 | 0.1&nbsp;ms | 0.7 | 23&nbsp;ms | 70&nbsp;ms | 0.2 | 1.8 |
| Simulation, STEP | 0.1 | 0.1 | 0.5 | 0.2&nbsp;ms | 0.7 | 0.9 | 60&nbsp;ms | 0.2 | 2.6 |
| Simulation, STL | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 0.6 | 36&nbsp;ms | 67&nbsp;ms | 0.2 | 1.6 |
| Simulation, OBJ | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 0.8 | 0.6 | 97&nbsp;ms | 0.2 | 2.4 |
| Visual, GLB | 0.1 | 0.2 | 0.4 | 0.1&nbsp;ms | 1.3 | 20&nbsp;ms | 0.1 | 0.2 | 2.4 |
| Visual, OBJ | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 1.4 | 0.7 | 0.1 | 0.3 | 3.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-flex-sound.kicad_pcb` |
|---|---|
| Folder | nref-flex / nref-flex-sound |
| Complexity | 162&nbsp;/&nbsp;1000 (size&nbsp;112, features&nbsp;50) |
| KESE&nbsp;features | through vias, filled zones,<br>TrueType text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 29, 44 |
| Triangles,&nbsp;simulation | 89,318 in 19 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">3.2&nbsp;MB</td><td align="right">185&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">15&nbsp;MB</td><td align="right">197&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">4.5&nbsp;MB</td><td align="right">179&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">8.9&nbsp;MB</td><td align="right">184&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.8&nbsp;MB</td><td align="right">163&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">11&nbsp;MB</td><td align="right">163&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.88 nref-flex-usb3-camera

![nref-flex-usb3-camera: stages 4 and 6 take 43% to 74% of a run. Simulation, GLB takes 1.7 s. Simulation, STEP takes 2.3 s. Simulation, STL takes 1.6 s. Simulation, OBJ takes 2.1 s. Visual, GLB takes 2.2 s. Visual, OBJ takes 3.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-flex-usb3-camera.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.5 | 0.5&nbsp;ms | 0.6 | 22&nbsp;ms | 63&nbsp;ms | 0.3 | 1.7 |
| Simulation, STEP | 98&nbsp;ms | 0.2 | 0.4 | 0.4&nbsp;ms | 0.6 | 0.8 | 60&nbsp;ms | 0.2 | 2.3 |
| Simulation, STL | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 0.6 | 31&nbsp;ms | 60&nbsp;ms | 0.3 | 1.6 |
| Simulation, OBJ | 0.1 | 0.2 | 0.4 | 0.1&nbsp;ms | 0.6 | 0.6 | 65&nbsp;ms | 0.2 | 2.1 |
| Visual, GLB | 0.1 | 0.1 | 0.4 | 0.1&nbsp;ms | 1.3 | 19&nbsp;ms | 0.1 | 0.2 | 2.2 |
| Visual, OBJ | 0.1 | 0.1 | 0.7 | 0.2&nbsp;ms | 1.4 | 0.7 | 98&nbsp;ms | 0.2 | 3.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-flex-usb3-camera.kicad_pcb` |
|---|---|
| Folder | nref-flex / nref-flex-usb3-one |
| Complexity | 199&nbsp;/&nbsp;1000 (size&nbsp;119, features&nbsp;80) |
| KESE&nbsp;features | through vias, filled zones,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 66, 60 |
| Triangles,&nbsp;simulation | 97,574 in 19 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">3.4&nbsp;MB</td><td align="right">186&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">13&nbsp;MB</td><td align="right">195&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">4.9&nbsp;MB</td><td align="right">190&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.5&nbsp;MB</td><td align="right">188&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.6&nbsp;MB</td><td align="right">157&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">10.0&nbsp;MB</td><td align="right">156&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.89 nref-flex-usb3-one-130mm

![nref-flex-usb3-one-130mm: stages 4 and 6 take 43% to 75% of a run. Simulation, GLB takes 1.3 s. Simulation, STEP takes 2.1 s. Simulation, STL takes 1.4 s. Simulation, OBJ takes 1.8 s. Visual, GLB takes 2.0 s. Visual, OBJ takes 2.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-flex-usb3-one-130mm.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 88&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.6 | 15&nbsp;ms | 45&nbsp;ms | 0.2 | 1.3 |
| Simulation, STEP | 0.1 | 0.1 | 0.4 | 0.3&nbsp;ms | 0.6 | 0.7 | 43&nbsp;ms | 0.2 | 2.1 |
| Simulation, STL | 0.1 | 98&nbsp;ms | 0.3 | 0.2&nbsp;ms | 0.6 | 20&nbsp;ms | 49&nbsp;ms | 0.2 | 1.4 |
| Simulation, OBJ | 0.1 | 98&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.6 | 0.5 | 50&nbsp;ms | 0.2 | 1.8 |
| Visual, GLB | 98&nbsp;ms | 88&nbsp;ms | 0.3 | 0.1&nbsp;ms | 1.2 | 23&nbsp;ms | 0.1 | 0.2 | 2.0 |
| Visual, OBJ | 0.1 | 94&nbsp;ms | 0.3 | 0.1&nbsp;ms | 1.2 | 0.4 | 87&nbsp;ms | 0.2 | 2.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-flex-usb3-one-130mm.kicad_pcb` |
|---|---|
| Folder | nref-flex / nref-flex-usb3-one |
| Complexity | 189&nbsp;/&nbsp;1000 (size&nbsp;109, features&nbsp;80) |
| KESE&nbsp;features | through vias, filled zones,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 62, 25 |
| Triangles,&nbsp;simulation | 74,446 in 17 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">2.7&nbsp;MB</td><td align="right">177&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">14&nbsp;MB</td><td align="right">189&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">3.7&nbsp;MB</td><td align="right">179&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">7.4&nbsp;MB</td><td align="right">179&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.2&nbsp;MB</td><td align="right">155&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">8.8&nbsp;MB</td><td align="right">154&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.90 nref-flex-usb3-one

![nref-flex-usb3-one: stages 4 and 6 take 47% to 75% of a run. Simulation, GLB takes 2.1 s. Simulation, STEP takes 2.9 s. Simulation, STL takes 2.0 s. Simulation, OBJ takes 2.6 s. Visual, GLB takes 2.8 s. Visual, OBJ takes 3.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-flex-usb3-one.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.7 | 0.1&nbsp;ms | 0.7 | 25&nbsp;ms | 73&nbsp;ms | 0.3 | 2.1 |
| Simulation, STEP | 0.1 | 0.2 | 0.6 | 0.1&nbsp;ms | 0.7 | 0.9 | 77&nbsp;ms | 0.2 | 2.9 |
| Simulation, STL | 0.1 | 0.2 | 0.6 | 0.2&nbsp;ms | 0.7 | 39&nbsp;ms | 85&nbsp;ms | 0.2 | 2.0 |
| Simulation, OBJ | 0.1 | 0.2 | 0.6 | 0.1&nbsp;ms | 0.7 | 0.7 | 81&nbsp;ms | 0.2 | 2.6 |
| Visual, GLB | 0.1 | 0.2 | 0.6 | 0.2&nbsp;ms | 1.5 | 26&nbsp;ms | 0.1 | 0.2 | 2.8 |
| Visual, OBJ | 0.1 | 0.2 | 0.6 | 0.2&nbsp;ms | 1.5 | 0.8 | 0.1 | 0.3 | 3.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-flex-usb3-one.kicad_pcb` |
|---|---|
| Folder | nref-flex / nref-flex-usb3-one |
| Complexity | 203&nbsp;/&nbsp;1000 (size&nbsp;123, features&nbsp;80) |
| KESE&nbsp;features | through vias, filled zones,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 66, 81 |
| Triangles,&nbsp;simulation | 127,254 in 19 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.5&nbsp;MB</td><td align="right">197&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">17&nbsp;MB</td><td align="right">215&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">6.4&nbsp;MB</td><td align="right">191&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">13&nbsp;MB</td><td align="right">198&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.9&nbsp;MB</td><td align="right">190&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">14&nbsp;MB</td><td align="right">182&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.91 nref-motherboard

![nref-motherboard: stages 4 and 6 take 47% to 82% of a run. Simulation, GLB takes 56 s. Simulation, STEP takes 67 s. Simulation, STL takes 56 s. Simulation, OBJ takes 91 s. Visual, GLB takes 89 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-motherboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.7 | 7.3 | 20.6 | 0.9&nbsp;ms | 22.1 | 1.0 | 3.4 | 0.4 | 56.3 |
| Simulation, STEP | 1.7 | 6.6 | 19.9 | 1.0&nbsp;ms | 21.6 | 13.9 | 3.3 | 0.3 | 67.3 |
| Simulation, STL | 1.8 | 6.5 | 20.0 | 1.0&nbsp;ms | 21.3 | 2.3 | 3.3 | 0.3 | 55.5 |
| Simulation, OBJ | 1.7 | 7.0 | 20.3 | 1.0&nbsp;ms | 22.3 | 36.7 | 3.1 | 0.3 | 91.4 |
| Visual, GLB | 1.6 | 6.7 | 19.6 | 1&nbsp;ms | 53.6 | 0.6 | 6.6 | 0.3 | 88.9 |
| Visual, OBJ | 1.7 | 6.7 | 20.2 | 1&nbsp;ms | 52.6 | 21.1 | 7.0 | 0.3 | 109.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-motherboard.kicad_pcb` |
|---|---|
| Folder | nref-motherboard |
| Complexity | 452&nbsp;/&nbsp;1000 (size&nbsp;302, features&nbsp;150) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, knockout text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 267, 4,810, 1,094 |
| Triangles,&nbsp;simulation | 6,534,402 in 430 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">219&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">770&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">327&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">691&nbsp;MB</td><td align="right">4.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">129&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">418&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.92 nref-ports-one

![nref-ports-one: stages 4 and 6 take 53% to 82% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 30 s. Simulation, STL takes 25 s. Simulation, OBJ takes 35 s. Visual, GLB takes 35 s. Visual, OBJ takes 45 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-ports-one.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.4 | 8.2 | 1.0&nbsp;ms | 10.3 | 0.5 | 1.1 | 0.3 | 23.5 |
| Simulation, STEP | 0.7 | 2.5 | 8.3 | 0.9&nbsp;ms | 10.3 | 6.7 | 1.2 | 0.3 | 30.0 |
| Simulation, STL | 0.7 | 2.7 | 8.8 | 0.9&nbsp;ms | 10.6 | 0.8 | 1.1 | 0.3 | 25.2 |
| Simulation, OBJ | 0.6 | 2.5 | 8.4 | 0.9&nbsp;ms | 10.0 | 11.8 | 1.2 | 0.3 | 34.8 |
| Visual, GLB | 0.7 | 2.5 | 8.3 | 0.8&nbsp;ms | 20.1 | 0.3 | 2.4 | 0.2 | 34.6 |
| Visual, OBJ | 0.8 | 2.6 | 8.7 | 1&nbsp;ms | 21.0 | 8.6 | 3.0 | 0.3 | 45.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-ports-one.kicad_pcb` |
|---|---|
| Folder | nref-ports-one |
| Complexity | 376&nbsp;/&nbsp;1000 (size&nbsp;261, features&nbsp;115) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 146, 2,113, 461 |
| Triangles,&nbsp;simulation | 2,380,888 in 187 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">81&nbsp;MB</td><td align="right">821&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">339&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">119&nbsp;MB</td><td align="right">815&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">248&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">56&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">174&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.93 nref-ports-two

![nref-ports-two: stages 4 and 6 take 55% to 84% of a run. Simulation, GLB takes 26 s. Simulation, STEP takes 33 s. Simulation, STL takes 26 s. Simulation, OBJ takes 38 s. Visual, GLB takes 40 s. Visual, OBJ takes 48 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-ports-two.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.4 | 10.0 | 1&nbsp;ms | 11.1 | 0.4 | 1.1 | 0.3 | 26.2 |
| Simulation, STEP | 0.7 | 2.4 | 10.2 | 1.0&nbsp;ms | 10.9 | 7.1 | 1.1 | 0.3 | 32.9 |
| Simulation, STL | 0.7 | 2.3 | 9.8 | 1&nbsp;ms | 11.2 | 0.9 | 1.2 | 0.3 | 26.4 |
| Simulation, OBJ | 0.7 | 2.5 | 9.9 | 1&nbsp;ms | 11.2 | 12.6 | 1.2 | 0.3 | 38.4 |
| Visual, GLB | 0.7 | 2.5 | 10.4 | 1&nbsp;ms | 23.4 | 0.3 | 2.7 | 0.3 | 40.3 |
| Visual, OBJ | 0.7 | 2.4 | 10.2 | 1&nbsp;ms | 22.2 | 8.9 | 3.0 | 0.3 | 47.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-ports-two.kicad_pcb` |
|---|---|
| Folder | nref-ports-two |
| Complexity | 381&nbsp;/&nbsp;1000 (size&nbsp;266, features&nbsp;115) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 137, 1,989, 422 |
| Triangles,&nbsp;simulation | 2,497,724 in 191 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">86&nbsp;MB</td><td align="right">825&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">366&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">125&nbsp;MB</td><td align="right">853&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">262&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">57&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">175&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.94 Trackpad_IQS9150

![Trackpad_IQS9150: stages 4 and 6 take 56% to 82% of a run. Simulation, GLB takes 18 s. Simulation, STEP takes 24 s. Simulation, STL takes 18 s. Simulation, OBJ takes 27 s. Visual, GLB takes 24 s. Visual, OBJ takes 31 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_Trackpad-IQS9150.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.9 | 5.2 | 0.3&nbsp;ms | 8.6 | 0.3 | 1.0 | 0.3 | 17.7 |
| Simulation, STEP | 0.4 | 1.8 | 5.0 | 0.4&nbsp;ms | 8.9 | 6.6 | 0.9 | 0.3 | 24.0 |
| Simulation, STL | 0.5 | 1.7 | 5.1 | 0.2&nbsp;ms | 8.8 | 0.5 | 0.8 | 0.3 | 17.7 |
| Simulation, OBJ | 0.5 | 1.7 | 5.3 | 0.3&nbsp;ms | 9.5 | 8.4 | 0.9 | 0.3 | 26.6 |
| Visual, GLB | 0.4 | 1.9 | 5.2 | 0.4&nbsp;ms | 14.4 | 0.2 | 1.6 | 0.3 | 24.0 |
| Visual, OBJ | 0.5 | 1.9 | 5.0 | 0.2&nbsp;ms | 13.9 | 8.1 | 1.6 | 0.3 | 31.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `Trackpad_IQS9150.kicad_pcb` |
|---|---|
| Folder | nref-trackpad-sensor |
| Complexity | 259&nbsp;/&nbsp;1000 (size&nbsp;174, features&nbsp;85) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 10, 1,065, 633 |
| Triangles,&nbsp;simulation | 1,517,980 in 63 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">52&nbsp;MB</td><td align="right">712&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">213&nbsp;MB</td><td align="right">789&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">76&nbsp;MB</td><td align="right">702&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">156&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">46&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">141&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.95 nref-trackpad

![nref-trackpad: stages 4 and 6 take 49% to 75% of a run. Simulation, GLB takes 2.9 s. Simulation, STEP takes 4.4 s. Simulation, STL takes 2.9 s. Simulation, OBJ takes 4.3 s. Visual, GLB takes 3.6 s. Visual, OBJ takes 4.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-trackpad.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.2 | 0.7 | 0.2&nbsp;ms | 1.3 | 39&nbsp;ms | 0.1 | 0.3 | 2.9 |
| Simulation, STEP | 0.2 | 0.2 | 0.8 | 0.3&nbsp;ms | 1.4 | 1.4 | 0.1 | 0.3 | 4.4 |
| Simulation, STL | 0.2 | 0.2 | 0.8 | 0.2&nbsp;ms | 1.3 | 59&nbsp;ms | 0.1 | 0.3 | 2.9 |
| Simulation, OBJ | 0.2 | 0.2 | 0.9 | 0.2&nbsp;ms | 1.4 | 1.1 | 0.1 | 0.3 | 4.3 |
| Visual, GLB | 0.2 | 0.2 | 0.7 | 0.2&nbsp;ms | 2.1 | 30&nbsp;ms | 0.2 | 0.3 | 3.6 |
| Visual, OBJ | 0.2 | 0.2 | 0.7 | 0.2&nbsp;ms | 2.4 | 1.0 | 0.2 | 0.3 | 4.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-trackpad.kicad_pcb` |
|---|---|
| Folder | nref-trackpad |
| Complexity | 243&nbsp;/&nbsp;1000 (size&nbsp;168, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 12, 93, 22 |
| Triangles,&nbsp;simulation | 162,486 in 36 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">5.6&nbsp;MB</td><td align="right">209&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">27&nbsp;MB</td><td align="right">230&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">8.1&nbsp;MB</td><td align="right">210&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">16&nbsp;MB</td><td align="right">212&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.8&nbsp;MB</td><td align="right">210&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">14&nbsp;MB</td><td align="right">209&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.96 nref-usb3-redriver

![nref-usb3-redriver: stages 4 and 6 take 48% to 77% of a run. Simulation, GLB takes 6.2 s. Simulation, STEP takes 8.3 s. Simulation, STL takes 6.6 s. Simulation, OBJ takes 10 s. Visual, GLB takes 8.9 s. Visual, OBJ takes 10 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-usb3-redriver.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 2.0 | 0.5&nbsp;ms | 2.6 | 0.1 | 0.4 | 0.2 | 6.2 |
| Simulation, STEP | 0.3 | 0.7 | 2.0 | 0.3&nbsp;ms | 2.5 | 2.2 | 0.4 | 0.2 | 8.3 |
| Simulation, STL | 0.2 | 0.8 | 2.2 | 0.3&nbsp;ms | 2.6 | 0.2 | 0.4 | 0.3 | 6.6 |
| Simulation, OBJ | 0.3 | 0.7 | 2.0 | 0.4&nbsp;ms | 2.8 | 3.6 | 0.4 | 0.3 | 10.1 |
| Visual, GLB | 0.2 | 0.8 | 2.0 | 0.4&nbsp;ms | 4.8 | 0.1 | 0.7 | 0.3 | 8.9 |
| Visual, OBJ | 0.3 | 0.7 | 1.9 | 0.3&nbsp;ms | 4.4 | 2.4 | 0.5 | 0.2 | 10.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-usb3-redriver.kicad_pcb` |
|---|---|
| Folder | nref-usb3-redriver |
| Complexity | 287&nbsp;/&nbsp;1000 (size&nbsp;187, features&nbsp;100) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, knockout text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 40, 496, 171 |
| Triangles,&nbsp;simulation | 669,168 in 65 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">378&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">84&nbsp;MB</td><td align="right">442&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">33&nbsp;MB</td><td align="right">380&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">67&nbsp;MB</td><td align="right">489&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">381&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">47&nbsp;MB</td><td align="right">431&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.97 nref-wifi-m2

![nref-wifi-m2: stages 4 and 6 take 45% to 80% of a run. Simulation, GLB takes 6.2 s. Simulation, STEP takes 8.0 s. Simulation, STL takes 6.1 s. Simulation, OBJ takes 9.5 s. Visual, GLB takes 8.6 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-wifi-m2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 0.7 | 1.8 | 0.3&nbsp;ms | 2.5 | 0.1 | 0.4 | 0.3 | 6.2 |
| Simulation, STEP | 0.3 | 0.6 | 1.9 | 0.4&nbsp;ms | 2.4 | 2.2 | 0.4 | 0.3 | 8.0 |
| Simulation, STL | 0.3 | 0.7 | 1.9 | 0.4&nbsp;ms | 2.5 | 0.2 | 0.4 | 0.2 | 6.1 |
| Simulation, OBJ | 0.3 | 0.7 | 1.8 | 0.3&nbsp;ms | 2.5 | 3.6 | 0.3 | 0.3 | 9.5 |
| Visual, GLB | 0.3 | 0.7 | 1.8 | 0.9&nbsp;ms | 5.0 | 67&nbsp;ms | 0.4 | 0.3 | 8.6 |
| Visual, OBJ | 0.3 | 0.7 | 1.8 | 0.4&nbsp;ms | 4.9 | 2.7 | 0.8 | 0.3 | 11.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-wifi-m2.kicad_pcb` |
|---|---|
| Folder | nref-wifi-m2 |
| Complexity | 280&nbsp;/&nbsp;1000 (size&nbsp;180, features&nbsp;100) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 28, 402, 141 |
| Triangles,&nbsp;simulation | 588,790 in 76 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">332&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">80&nbsp;MB</td><td align="right">393&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">29&nbsp;MB</td><td align="right">320&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">59&nbsp;MB</td><td align="right">448&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">382&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">43&nbsp;MB</td><td align="right">410&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.98 nref-wifi

![nref-wifi: stages 4 and 6 take 52% to 80% of a run. Simulation, GLB takes 4.0 s. Simulation, STEP takes 5.5 s. Simulation, STL takes 4.1 s. Simulation, OBJ takes 5.7 s. Visual, GLB takes 5.4 s. Visual, OBJ takes 6.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/reform-next-mirror_nref-wifi.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.5 | 0.2&nbsp;ms | 1.5 | 59&nbsp;ms | 0.2 | 0.2 | 4.0 |
| Simulation, STEP | 0.2 | 0.4 | 1.6 | 0.2&nbsp;ms | 1.5 | 1.5 | 0.2 | 0.2 | 5.5 |
| Simulation, STL | 0.2 | 0.4 | 1.5 | 0.3&nbsp;ms | 1.6 | 79&nbsp;ms | 0.2 | 0.2 | 4.1 |
| Simulation, OBJ | 0.2 | 0.4 | 1.5 | 0.3&nbsp;ms | 1.5 | 1.7 | 0.2 | 0.2 | 5.7 |
| Visual, GLB | 0.2 | 0.4 | 1.5 | 0.2&nbsp;ms | 2.9 | 50&nbsp;ms | 0.2 | 0.2 | 5.4 |
| Visual, OBJ | 0.2 | 0.4 | 1.6 | 0.2&nbsp;ms | 2.8 | 1.5 | 0.3 | 0.2 | 6.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cetola/reform-next-mirror](https://github.com/cetola/reform-next-mirror)<br>Board: `nref-wifi.kicad_pcb` |
|---|---|
| Folder | nref-wifi |
| Complexity | 232&nbsp;/&nbsp;1000 (size&nbsp;157, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 23, 351, 98 |
| Triangles,&nbsp;simulation | 336,550 in 54 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">272&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">56&nbsp;MB</td><td align="right">312&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">17&nbsp;MB</td><td align="right">275&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">34&nbsp;MB</td><td align="right">274&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">10&nbsp;MB</td><td align="right">297&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">30&nbsp;MB</td><td align="right">300&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.6.99 cm0

![cm0: stages 4 and 6 take 57% to 85% of a run. Simulation, GLB takes 71 s. Simulation, STEP takes 79 s. Simulation, STL takes 72 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/icepi-sbc_cm0.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.0 | 6.1 | 26.1 | 2&nbsp;ms | 32.7 | 1.0 | 2.9 | 0.4 | 71.0 |
| Simulation, STEP | 1.6 | 4.8 | 22.9 | 2&nbsp;ms | 31.7 | 15.2 | 2.9 | 0.4 | 79.4 |
| Simulation, STL | 2.0 | 5.6 | 23.1 | 3&nbsp;ms | 34.7 | 2.9 | 3.6 | 0.4 | 72.2 |
| Simulation, OBJ | 1.9 | 5.5 | 24.1 | 3&nbsp;ms | 33.4 | 31.9 | 3.2 | 0.6 | 100.6 |
| Visual, GLB | 2.0 | 5.6 | 25.4 | 3&nbsp;ms | 72.5 | 0.8 | 8.2 | 0.3 | 114.9 |
| Visual, OBJ | 2.5 | 6.1 | 28.2 | 2&nbsp;ms | 70.8 | 23.0 | 8.2 | 0.4 | 139.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cheyao/icepi-sbc](https://github.com/cheyao/icepi-sbc)<br>Board: `cm0.kicad_pcb` |
|---|---|
| Folder | hardware |
| Complexity | 438&nbsp;/&nbsp;1000 (size&nbsp;303, features&nbsp;135) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 269, 5,249, 823 |
| Triangles,&nbsp;simulation | 4,795,238 in 480 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">161&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">691&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">240&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">511&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">109&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">356&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.100 icepi-zero

![icepi-zero: stages 4 and 6 take 54% to 85% of a run. Simulation, GLB takes 22 s. Simulation, STEP takes 28 s. Simulation, STL takes 22 s. Simulation, OBJ takes 32 s. Visual, GLB takes 34 s. Visual, OBJ takes 42 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/icepi-zero_hardware-v1-0_icepi-zero.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 2.0 | 9.1 | 1&nbsp;ms | 8.7 | 0.4 | 1.0 | 0.3 | 22.1 |
| Simulation, STEP | 0.7 | 2.0 | 9.2 | 1&nbsp;ms | 8.5 | 6.1 | 1.1 | 0.3 | 27.7 |
| Simulation, STL | 0.6 | 1.9 | 8.8 | 1.0&nbsp;ms | 8.5 | 0.7 | 1.1 | 0.3 | 22.0 |
| Simulation, OBJ | 0.6 | 2.0 | 8.8 | 1.0&nbsp;ms | 8.6 | 11.0 | 1.1 | 0.3 | 32.4 |
| Visual, GLB | 0.6 | 1.9 | 8.8 | 0.9&nbsp;ms | 20.0 | 0.2 | 2.0 | 0.3 | 33.8 |
| Visual, OBJ | 0.6 | 2.1 | 9.6 | 2&nbsp;ms | 20.5 | 6.7 | 2.1 | 0.4 | 42.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cheyao/icepi-zero](https://github.com/cheyao/icepi-zero)<br>Board: `icepi-zero.kicad_pcb` |
|---|---|
| Folder | hardware / v1.0 |
| Complexity | 397&nbsp;/&nbsp;1000 (size&nbsp;267, features&nbsp;130) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 119, 2,041, 256 |
| Triangles,&nbsp;simulation | 2,163,986 in 265 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">75&nbsp;MB</td><td align="right">754&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">328&nbsp;MB</td><td align="right">932&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">108&nbsp;MB</td><td align="right">745&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">227&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">47&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">144&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.101 icepi-zero

![icepi-zero: stages 4 and 6 take 54% to 86% of a run. Simulation, GLB takes 22 s. Simulation, STEP takes 27 s. Simulation, STL takes 21 s. Simulation, OBJ takes 31 s. Visual, GLB takes 33 s. Visual, OBJ takes 39 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/icepi-zero_hardware-v1-1_icepi-zero.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 1.9 | 9.0 | 0.7&nbsp;ms | 8.5 | 0.4 | 1.1 | 0.3 | 21.9 |
| Simulation, STEP | 0.7 | 2.0 | 8.5 | 0.6&nbsp;ms | 8.1 | 5.9 | 1.0 | 0.2 | 26.5 |
| Simulation, STL | 0.5 | 1.9 | 8.5 | 0.6&nbsp;ms | 8.3 | 0.6 | 1.0 | 0.3 | 21.1 |
| Simulation, OBJ | 0.5 | 1.9 | 8.5 | 0.6&nbsp;ms | 8.2 | 10.6 | 1.0 | 0.2 | 31.0 |
| Visual, GLB | 0.6 | 1.9 | 8.6 | 0.8&nbsp;ms | 19.3 | 0.2 | 1.7 | 0.3 | 32.6 |
| Visual, OBJ | 0.6 | 2.0 | 8.4 | 0.6&nbsp;ms | 19.0 | 6.6 | 1.8 | 0.2 | 38.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cheyao/icepi-zero](https://github.com/cheyao/icepi-zero)<br>Board: `icepi-zero.kicad_pcb` |
|---|---|
| Folder | hardware / v1.1 |
| Complexity | 397&nbsp;/&nbsp;1000 (size&nbsp;267, features&nbsp;130) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 124, 1,947, 269 |
| Triangles,&nbsp;simulation | 2,216,300 in 265 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">76&nbsp;MB</td><td align="right">777&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">334&nbsp;MB</td><td align="right">955&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">111&nbsp;MB</td><td align="right">787&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">236&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">48&nbsp;MB</td><td align="right">902&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">149&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.102 icepi-zero

![icepi-zero: stages 4 and 6 take 54% to 84% of a run. Simulation, GLB takes 20 s. Simulation, STEP takes 24 s. Simulation, STL takes 20 s. Simulation, OBJ takes 30 s. Visual, GLB takes 30 s. Visual, OBJ takes 37 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/icepi-zero_hardware-v1-2_icepi-zero.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.7 | 7.8 | 0.8&nbsp;ms | 8.1 | 0.3 | 0.9 | 0.2 | 19.6 |
| Simulation, STEP | 0.5 | 1.6 | 7.6 | 0.8&nbsp;ms | 7.6 | 5.2 | 0.9 | 0.3 | 23.9 |
| Simulation, STL | 0.6 | 1.8 | 8.0 | 1.0&nbsp;ms | 7.8 | 0.7 | 1.0 | 0.3 | 19.9 |
| Simulation, OBJ | 0.6 | 1.7 | 8.0 | 0.8&nbsp;ms | 8.1 | 10.0 | 1.0 | 0.3 | 29.7 |
| Visual, GLB | 0.5 | 1.7 | 7.7 | 1&nbsp;ms | 17.6 | 0.2 | 2.0 | 0.2 | 30.1 |
| Visual, OBJ | 0.5 | 1.6 | 7.5 | 0.8&nbsp;ms | 18.1 | 6.3 | 2.3 | 0.2 | 36.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cheyao/icepi-zero](https://github.com/cheyao/icepi-zero)<br>Board: `icepi-zero.kicad_pcb` |
|---|---|
| Folder | hardware / v1.2 |
| Complexity | 399&nbsp;/&nbsp;1000 (size&nbsp;269, features&nbsp;130) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 140, 2,064, 271 |
| Triangles,&nbsp;simulation | 2,281,968 in 274 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">79&nbsp;MB</td><td align="right">797&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">349&nbsp;MB</td><td align="right">991&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">114&nbsp;MB</td><td align="right">794&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">244&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">49&nbsp;MB</td><td align="right">905&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">154&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.103 icepi-zero

![icepi-zero: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 24 s. Simulation, STEP takes 30 s. Simulation, STL takes 25 s. Simulation, OBJ takes 38 s. Visual, GLB takes 37 s. Visual, OBJ takes 45 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/icepi-zero_hardware-v1-3_icepi-zero.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 2.1 | 9.3 | 2&nbsp;ms | 9.7 | 0.5 | 1.2 | 0.3 | 23.9 |
| Simulation, STEP | 0.8 | 2.2 | 9.4 | 0.8&nbsp;ms | 9.6 | 6.9 | 1.1 | 0.3 | 30.3 |
| Simulation, STL | 0.8 | 2.2 | 9.6 | 0.8&nbsp;ms | 9.5 | 0.9 | 1.2 | 0.3 | 24.6 |
| Simulation, OBJ | 1.0 | 2.3 | 10.1 | 0.9&nbsp;ms | 9.5 | 13.4 | 1.3 | 0.3 | 37.8 |
| Visual, GLB | 1.0 | 2.2 | 9.6 | 0.9&nbsp;ms | 21.0 | 0.2 | 2.3 | 0.3 | 36.5 |
| Visual, OBJ | 0.8 | 2.1 | 9.8 | 0.8&nbsp;ms | 21.0 | 8.5 | 2.4 | 0.2 | 44.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cheyao/icepi-zero](https://github.com/cheyao/icepi-zero)<br>Board: `icepi-zero.kicad_pcb` |
|---|---|
| Folder | hardware / v1.3 |
| Complexity | 401&nbsp;/&nbsp;1000 (size&nbsp;271, features&nbsp;130) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 143, 2,234, 272 |
| Triangles,&nbsp;simulation | 2,347,416 in 277 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">81&nbsp;MB</td><td align="right">773&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">369&nbsp;MB</td><td align="right">992&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">117&nbsp;MB</td><td align="right">890&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">250&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">51&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">160&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.6.104 icepi-zero

![icepi-zero: stages 4 and 6 take 54% to 85% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 29 s. Simulation, STL takes 23 s. Simulation, OBJ takes 35 s. Visual, GLB takes 36 s. Visual, OBJ takes 44 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-06/icepi-zero_hardware-v1-4_icepi-zero.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 1.8 | 9.3 | 1&nbsp;ms | 9.2 | 0.4 | 1.3 | 0.3 | 23.0 |
| Simulation, STEP | 0.7 | 1.9 | 9.3 | 1&nbsp;ms | 9.3 | 6.4 | 1.2 | 0.3 | 29.1 |
| Simulation, STL | 0.7 | 2.1 | 9.2 | 1.0&nbsp;ms | 9.2 | 0.7 | 1.1 | 0.3 | 23.3 |
| Simulation, OBJ | 0.7 | 2.2 | 9.2 | 1&nbsp;ms | 9.3 | 11.7 | 1.2 | 0.3 | 34.7 |
| Visual, GLB | 0.7 | 2.1 | 9.5 | 1&nbsp;ms | 21.4 | 0.3 | 2.1 | 0.2 | 36.3 |
| Visual, OBJ | 0.7 | 2.2 | 9.4 | 1.0&nbsp;ms | 21.8 | 7.6 | 2.3 | 0.3 | 44.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [cheyao/icepi-zero](https://github.com/cheyao/icepi-zero)<br>Board: `icepi-zero.kicad_pcb` |
|---|---|
| Folder | hardware / v1.4 |
| Complexity | 416&nbsp;/&nbsp;1000 (size&nbsp;271, features&nbsp;145) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 144, 2,286, 277 |
| Triangles,&nbsp;simulation | 2,359,720 in 277 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">81&nbsp;MB</td><td align="right">818&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">373&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">118&nbsp;MB</td><td align="right">925&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">252&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">51&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">161&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [Corpus Testing 5: Bambelweeny57 To Board-Folk](Corpus-Testing-05.md) | [Corpus Testing 7: chipfoundry To DangerousPrototypes](Corpus-Testing-07.md) |
