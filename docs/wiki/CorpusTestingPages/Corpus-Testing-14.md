# Corpus Page 14

Part 14 of 29 of [Corpus Testing](../Corpus-Testing.md): boards 1,405 to 1,512, six runs each, one file format a run, as [Corpus Testing](../Corpus-Testing.md) describes.

## 1405. DFTBoard

![DFTBoard: stages 4 and 6 take 44% to 83% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 2 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1405b_zynqpcb_DFTBoard/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.6 | 12.8 | 34.2 | 2&nbsp;ms | 41.6 | 2.3 | 6.6 | 0.5 | 100.6 |
| Simulation, STEP | 2.5 | 12.4 | 33.1 | 1&nbsp;ms | 40.6 | 25.3 | 6.5 | 0.4 | 121.0 |
| Simulation, STL | 2.5 | 12.7 | 33.7 | 3&nbsp;ms | 41.4 | 4.9 | 6.5 | 0.4 | 102.2 |
| Simulation, OBJ | 2.7 | 12.4 | 33.8 | 2&nbsp;ms | 41.4 | 73.2 | 6.9 | 0.5 | 170.8 |
| Visual, GLB | 2.6 | 12.4 | 34.2 | 2&nbsp;ms | 87.2 | 1.0 | 8.5 | 0.3 | 146.4 |
| Visual, OBJ | 2.6 | 12.7 | 34.1 | 1&nbsp;ms | 87.7 | 32.7 | 8.1 | 0.4 | 178.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [julianfl0w/zynqpcb](https://github.com/julianfl0w/zynqpcb)<br>Board: `DFTBoard.kicad_pcb` |
|---|---|
| Complexity | 395&nbsp;/&nbsp;1000 (size&nbsp;335, features&nbsp;60) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 295, 12,613, 964 |
| Triangles,&nbsp;simulation | 11,448,918 in 320 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">391&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.3&nbsp;GB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">572&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.3&nbsp;GB</td><td align="right">7.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">179&nbsp;MB</td><td align="right">3.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">591&nbsp;MB</td><td align="right">3.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1406. PCB

![PCB: stages 4 and 6 take 47% to 83% of a run. Simulation, GLB takes 63 s. Simulation, STEP takes 80 s. Simulation, STL takes 63 s. Simulation, OBJ takes 97 s. Visual, GLB takes 87 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1406b_m-2-fpga-accelerator_PCB/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.2 | 6.2 | 21.9 | 1&nbsp;ms | 28.0 | 1.3 | 3.2 | 0.4 | 63.3 |
| Simulation, STEP | 2.3 | 6.3 | 23.1 | 2&nbsp;ms | 27.1 | 17.1 | 3.5 | 0.4 | 79.8 |
| Simulation, STL | 2.1 | 6.2 | 20.6 | 2&nbsp;ms | 27.4 | 2.9 | 3.6 | 0.4 | 63.1 |
| Simulation, OBJ | 2.0 | 6.1 | 19.4 | 1.0&nbsp;ms | 25.8 | 39.5 | 3.6 | 0.4 | 96.8 |
| Visual, GLB | 2.1 | 6.2 | 20.3 | 2&nbsp;ms | 52.1 | 0.6 | 5.7 | 0.3 | 87.3 |
| Visual, OBJ | 1.9 | 5.8 | 19.8 | 1&nbsp;ms | 50.5 | 20.9 | 5.5 | 0.3 | 104.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kaipereira/m.2-fpga-accelerator](https://github.com/kaipereira/m.2-fpga-accelerator)<br>Board: `PCB.kicad_pcb` |
|---|---|
| Folder | PCB |
| Complexity | 414&nbsp;/&nbsp;1000 (size&nbsp;314, features&nbsp;100) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 277, 6,345, 829 |
| Triangles,&nbsp;simulation | 6,455,524 in 441 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">217&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">936&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">323&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">685&nbsp;MB</td><td align="right">4.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">122&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">396&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1407. ZYNQ7020_AD9364_V2

![ZYNQ7020_AD9364_V2: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 70 s. Simulation, STEP takes 83 s. Simulation, STL takes 73 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1407b_zynq7010-7020-ad9363_ZYNQ7020-AD9364-V2/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 8.2 | 27.4 | 1&nbsp;ms | 29.2 | 1.3 | 3.0 | 0.4 | 70.4 |
| Simulation, STEP | 0.8 | 7.9 | 26.3 | 2&nbsp;ms | 29.4 | 15.5 | 3.0 | 0.3 | 83.3 |
| Simulation, STL | 1.0 | 8.0 | 26.3 | 1&nbsp;ms | 31.2 | 3.1 | 3.2 | 0.4 | 73.2 |
| Simulation, OBJ | 1.0 | 7.9 | 27.1 | 2&nbsp;ms | 30.1 | 40.5 | 3.2 | 0.4 | 110.2 |
| Visual, GLB | 0.9 | 7.8 | 27.4 | 2&nbsp;ms | 77.6 | 0.8 | 10.0 | 0.4 | 124.9 |
| Visual, OBJ | 1.3 | 8.1 | 26.2 | 1&nbsp;ms | 72.0 | 25.5 | 8.5 | 0.4 | 142.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kangyuzhe666/zynq7010-7020_ad9363](https://github.com/kangyuzhe666/zynq7010-7020_ad9363)<br>Board: `ZYNQ7020_AD9364_V2.kicad_pcb` |
|---|---|
| Folder | kicad |
| Complexity | 318&nbsp;/&nbsp;1000 (size&nbsp;248, features&nbsp;70) |
| KESE&nbsp;features | through vias, slotted holes,<br>drill offsets, arc tracks,<br>copper drawings,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20201116) |
| Parts,&nbsp;tracks,&nbsp;vias | 287, 6,546, 1,628 |
| Triangles,&nbsp;simulation | 7,777,178 in 292 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">264&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">929&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">389&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">829&nbsp;MB</td><td align="right">4.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">176&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">574&nbsp;MB</td><td align="right">3.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1408. Lily58_Lite_Rev3_TOP_Case

![Lily58_Lite_Rev3_TOP_Case: stages 4 and 6 take 44% to 81% of a run. Simulation, GLB takes 2.8 s. Simulation, STEP takes 4.0 s. Simulation, STL takes 2.7 s. Simulation, OBJ takes 4.3 s. Visual, GLB takes 3.7 s. Visual, OBJ takes 4.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1408b_Lily58_Lily58-Lite-Rev3-TOP-Case/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 59&nbsp;ms | 0.2 | 0.8 | 0.5&nbsp;ms | 1.3 | 58&nbsp;ms | 0.2 | 0.2 | 2.8 |
| Simulation, STEP | 55&nbsp;ms | 0.2 | 0.7 | 0.3&nbsp;ms | 1.2 | 1.4 | 0.2 | 0.2 | 4.0 |
| Simulation, STL | 57&nbsp;ms | 0.2 | 0.8 | 0.2&nbsp;ms | 1.2 | 0.1 | 0.2 | 0.2 | 2.7 |
| Simulation, OBJ | 58&nbsp;ms | 0.2 | 0.8 | 0.2&nbsp;ms | 1.1 | 1.8 | 0.2 | 0.2 | 4.3 |
| Visual, GLB | 49&nbsp;ms | 0.2 | 0.8 | 0.2&nbsp;ms | 2.2 | 36&nbsp;ms | 0.2 | 0.2 | 3.7 |
| Visual, OBJ | 52&nbsp;ms | 0.2 | 0.7 | 0.2&nbsp;ms | 2.2 | 0.9 | 0.2 | 0.2 | 4.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kata0510/Lily58](https://github.com/kata0510/Lily58)<br>Board: `Lily58_Lite_Rev3_TOP_Case.kicad_pcb` |
|---|---|
| Folder | case / top-plate |
| Complexity | 94&nbsp;/&nbsp;1000 (size&nbsp;54, features&nbsp;40) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 29, 0, 0 |
| Triangles,&nbsp;simulation | 405,304 in 68 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">277&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">63&nbsp;MB</td><td align="right">283&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">20&nbsp;MB</td><td align="right">277&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">40&nbsp;MB</td><td align="right">295&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.6&nbsp;MB</td><td align="right">233&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">235&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1409. Lily58_Lite_Rev3

![Lily58_Lite_Rev3: stages 4 and 6 take 51% to 84% of a run. Simulation, GLB takes 22 s. Simulation, STEP takes 27 s. Simulation, STL takes 22 s. Simulation, OBJ takes 33 s. Visual, GLB takes 32 s. Visual, OBJ takes 43 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1409b_Lily58_Lily58-Lite-Rev3/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 2.0 | 9.0 | 0.5&nbsp;ms | 8.4 | 0.4 | 1.2 | 0.2 | 21.8 |
| Simulation, STEP | 0.6 | 1.8 | 8.8 | 0.8&nbsp;ms | 7.9 | 6.4 | 1.0 | 0.2 | 26.8 |
| Simulation, STL | 0.6 | 1.8 | 9.3 | 0.5&nbsp;ms | 8.0 | 0.6 | 1.0 | 0.2 | 21.7 |
| Simulation, OBJ | 0.6 | 1.8 | 8.7 | 0.4&nbsp;ms | 7.9 | 12.6 | 1.0 | 0.2 | 32.8 |
| Visual, GLB | 0.6 | 1.8 | 8.7 | 0.6&nbsp;ms | 18.5 | 0.3 | 2.1 | 0.2 | 32.2 |
| Visual, OBJ | 0.7 | 1.8 | 8.8 | 0.7&nbsp;ms | 18.8 | 9.3 | 2.9 | 0.2 | 42.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kata0510/Lily58](https://github.com/kata0510/Lily58)<br>Board: `Lily58_Lite_Rev3.kicad_pcb` |
|---|---|
| Folder | Lite_Rev3 |
| Complexity | 240&nbsp;/&nbsp;1000 (size&nbsp;175, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 102, 637, 29 |
| Triangles,&nbsp;simulation | 2,400,690 in 116 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">81&nbsp;MB</td><td align="right">951&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">336&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">120&nbsp;MB</td><td align="right">987&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">250&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">60&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">184&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1410. Lily58

![Lily58: stages 4 and 6 take 57% to 86% of a run. Simulation, GLB takes 34 s. Simulation, STEP takes 45 s. Simulation, STL takes 36 s. Simulation, OBJ takes 54 s. Visual, GLB takes 55 s. Visual, OBJ takes 72 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1410b_Lily58_Lily58/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 2.4 | 16.3 | 0.3&nbsp;ms | 12.4 | 0.5 | 1.6 | 0.3 | 34.0 |
| Simulation, STEP | 0.5 | 2.5 | 17.5 | 0.3&nbsp;ms | 12.9 | 10.1 | 1.7 | 0.3 | 45.4 |
| Simulation, STL | 0.6 | 2.4 | 17.0 | 0.3&nbsp;ms | 12.7 | 1.4 | 1.6 | 0.3 | 36.1 |
| Simulation, OBJ | 0.6 | 2.4 | 17.4 | 0.3&nbsp;ms | 13.2 | 17.9 | 1.8 | 0.3 | 53.8 |
| Visual, GLB | 0.6 | 2.6 | 17.6 | 0.3&nbsp;ms | 29.9 | 0.4 | 3.9 | 0.3 | 55.3 |
| Visual, OBJ | 0.5 | 2.6 | 18.3 | 0.3&nbsp;ms | 31.7 | 13.3 | 5.2 | 0.3 | 71.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kata0510/Lily58](https://github.com/kata0510/Lily58)<br>Board: `Lily58.kicad_pcb` |
|---|---|
| Folder | pcb |
| Complexity | 223&nbsp;/&nbsp;1000 (size&nbsp;178, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 75, 991, 28 |
| Triangles,&nbsp;simulation | 2,925,400 in 69 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">100&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">533&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">146&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">311&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">63&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">195&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1411. Lily58_Pro_BOTTOM

![Lily58_Pro_BOTTOM: stages 4 and 6 take 42% to 59% of a run. Simulation, GLB takes 0.6 s. Simulation, STEP takes 0.9 s. Simulation, STL takes 0.7 s. Simulation, OBJ takes 0.7 s. Visual, GLB takes 0.7 s. Visual, OBJ takes 0.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1411b_Lily58_Lily58-Pro-BOTTOM/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 5&nbsp;ms | 29&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.2 | 6&nbsp;ms | 19&nbsp;ms | 0.2 | 0.6 |
| Simulation, STEP | 5&nbsp;ms | 31&nbsp;ms | 99&nbsp;ms | 0.1&nbsp;ms | 0.3 | 0.2 | 23&nbsp;ms | 0.2 | 0.9 |
| Simulation, STL | 5&nbsp;ms | 30&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.2 | 11&nbsp;ms | 32&nbsp;ms | 0.3 | 0.7 |
| Simulation, OBJ | 5&nbsp;ms | 35&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.2 | 0.1 | 19&nbsp;ms | 0.2 | 0.7 |
| Visual, GLB | 4&nbsp;ms | 30&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.2 | 3&nbsp;ms | 47&nbsp;ms | 0.2 | 0.7 |
| Visual, OBJ | 5&nbsp;ms | 47&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.2 | 57&nbsp;ms | 38&nbsp;ms | 0.2 | 0.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kata0510/Lily58](https://github.com/kata0510/Lily58)<br>Board: `Lily58_Pro_BOTTOM.kicad_pcb` |
|---|---|
| Folder | Pro / Case |
| Complexity | 17&nbsp;/&nbsp;1000 (size&nbsp;17, features&nbsp;0) |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 0, 0, 0 |
| Triangles,&nbsp;simulation | 32,200 in 10 parts |
| Note | no components |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.0&nbsp;MB</td><td align="right">43&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">4.5&nbsp;MB</td><td align="right">46&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">1.6&nbsp;MB</td><td align="right">45&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">2.9&nbsp;MB</td><td align="right">51&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">447&nbsp;kB</td><td align="right">61&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">1.2&nbsp;MB</td><td align="right">70&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1412. Lily58_Pro_TOP

![Lily58_Pro_TOP: reading, start-up and exit take 66% to 76% of a run. Simulation, GLB takes 0.3 s. Simulation, STEP takes 0.3 s. Simulation, STL takes 0.3 s. Simulation, OBJ takes 0.3 s. Visual, GLB takes 0.3 s. Visual, OBJ takes 0.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1412b_Lily58_Lily58-Pro-TOP/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 23&nbsp;ms | 42&nbsp;ms | 9&nbsp;ms | 0.0&nbsp;ms | 14&nbsp;ms | 1&nbsp;ms | 3&nbsp;ms | 0.2 | 0.3 |
| Simulation, STEP | 24&nbsp;ms | 41&nbsp;ms | 8&nbsp;ms | 0.0&nbsp;ms | 13&nbsp;ms | 12&nbsp;ms | 2&nbsp;ms | 0.2 | 0.3 |
| Simulation, STL | 22&nbsp;ms | 43&nbsp;ms | 8&nbsp;ms | 0.0&nbsp;ms | 14&nbsp;ms | 1.0&nbsp;ms | 3&nbsp;ms | 0.2 | 0.3 |
| Simulation, OBJ | 22&nbsp;ms | 44&nbsp;ms | 8&nbsp;ms | 0.0&nbsp;ms | 14&nbsp;ms | 7&nbsp;ms | 4&nbsp;ms | 0.2 | 0.3 |
| Visual, GLB | 25&nbsp;ms | 42&nbsp;ms | 9&nbsp;ms | 0.0&nbsp;ms | 37&nbsp;ms | 1&nbsp;ms | 10&nbsp;ms | 0.2 | 0.3 |
| Visual, OBJ | 22&nbsp;ms | 41&nbsp;ms | 8&nbsp;ms | 0.0&nbsp;ms | 44&nbsp;ms | 7&nbsp;ms | 10&nbsp;ms | 0.2 | 0.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kata0510/Lily58](https://github.com/kata0510/Lily58)<br>Board: `Lily58_Pro_TOP.kicad_pcb` |
|---|---|
| Folder | Pro / Case |
| Complexity | 37&nbsp;/&nbsp;1000 (size&nbsp;17, features&nbsp;20) |
| KESE&nbsp;features | filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 0, 0, 0 |
| Triangles,&nbsp;simulation | 1,048 in 3 parts |
| Note | no components |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">53&nbsp;kB</td><td align="right">40&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">353&nbsp;kB</td><td align="right">40&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">53&nbsp;kB</td><td align="right">40&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">158&nbsp;kB</td><td align="right">40&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">69&nbsp;kB</td><td align="right">44&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">165&nbsp;kB</td><td align="right">44&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1413. Lily58_Pro

![Lily58_Pro: stages 4 and 6 take 53% to 82% of a run. Simulation, GLB takes 20 s. Simulation, STEP takes 26 s. Simulation, STL takes 20 s. Simulation, OBJ takes 31 s. Visual, GLB takes 31 s. Visual, OBJ takes 40 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1413b_Lily58_Lily58-Pro/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 2.1 | 8.6 | 0.7&nbsp;ms | 7.1 | 0.3 | 0.8 | 0.3 | 19.8 |
| Simulation, STEP | 0.7 | 2.4 | 8.6 | 0.7&nbsp;ms | 7.2 | 5.8 | 0.8 | 0.3 | 25.7 |
| Simulation, STL | 0.5 | 2.1 | 8.5 | 0.6&nbsp;ms | 7.4 | 0.7 | 0.8 | 0.2 | 20.3 |
| Simulation, OBJ | 0.5 | 2.0 | 9.0 | 0.6&nbsp;ms | 7.5 | 11.1 | 0.7 | 0.2 | 31.2 |
| Visual, GLB | 0.5 | 2.1 | 8.8 | 0.7&nbsp;ms | 16.5 | 0.3 | 2.6 | 0.2 | 31.0 |
| Visual, OBJ | 0.6 | 2.1 | 8.4 | 0.8&nbsp;ms | 17.3 | 8.8 | 2.8 | 0.3 | 40.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kata0510/Lily58](https://github.com/kata0510/Lily58)<br>Board: `Lily58_Pro.kicad_pcb` |
|---|---|
| Folder | Pro / PCB |
| Complexity | 234&nbsp;/&nbsp;1000 (size&nbsp;189, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 74, 1,658, 149 |
| Triangles,&nbsp;simulation | 2,025,324 in 69 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">71&nbsp;MB</td><td align="right">888&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">389&nbsp;MB</td><td align="right">912&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">101&nbsp;MB</td><td align="right">891&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">217&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">57&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">177&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1414. Pro_V2

![Pro_V2: stages 4 and 6 take 53% to 80% of a run. Simulation, GLB takes 40 s. Simulation, STEP takes 48 s. Simulation, STL takes 41 s. Simulation, OBJ takes 57 s. Visual, GLB takes 62 s. Visual, OBJ takes 77 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1414b_Lily58_Pro-V2/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.6 | 5.4 | 14.8 | 1&nbsp;ms | 15.6 | 0.5 | 1.6 | 0.3 | 39.8 |
| Simulation, STEP | 1.7 | 5.3 | 14.9 | 1&nbsp;ms | 14.9 | 9.6 | 1.6 | 0.3 | 48.3 |
| Simulation, STL | 1.6 | 5.3 | 14.7 | 1&nbsp;ms | 16.0 | 1.4 | 1.5 | 0.3 | 41.1 |
| Simulation, OBJ | 1.7 | 5.6 | 15.2 | 1&nbsp;ms | 14.8 | 17.7 | 1.5 | 0.3 | 56.8 |
| Visual, GLB | 1.6 | 5.6 | 14.5 | 1&nbsp;ms | 35.0 | 0.5 | 4.7 | 0.3 | 62.1 |
| Visual, OBJ | 1.8 | 5.5 | 14.5 | 1&nbsp;ms | 35.2 | 14.9 | 5.0 | 0.3 | 77.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kata0510/Lily58](https://github.com/kata0510/Lily58)<br>Board: `Pro_V2.kicad_pcb` |
|---|---|
| Folder | Pro_V2 |
| Complexity | 394&nbsp;/&nbsp;1000 (size&nbsp;259, features&nbsp;135) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 260, 2,389, 497 |
| Triangles,&nbsp;simulation | 3,913,124 in 252 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">138&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">746&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">196&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">425&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">121&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">380&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1415. Kilsyth

![Kilsyth: stages 4 and 6 take 56% to 85% of a run. Simulation, GLB takes 51 s. Simulation, STEP takes 56 s. Simulation, STL takes 44 s. Simulation, OBJ takes 63 s. Visual, GLB takes 63 s. Visual, OBJ takes 77 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1415b_Kilsyth_hardware-RevA_Kilsyth/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 6.1 | 24.4 | 1&nbsp;ms | 16.4 | 0.7 | 2.4 | 0.4 | 51.4 |
| Simulation, STEP | 0.9 | 5.0 | 22.0 | 0.8&nbsp;ms | 14.6 | 11.3 | 2.3 | 0.3 | 56.3 |
| Simulation, STL | 0.8 | 4.8 | 21.3 | 0.8&nbsp;ms | 14.0 | 1.1 | 2.0 | 0.3 | 44.4 |
| Simulation, OBJ | 0.8 | 4.7 | 21.1 | 1&nbsp;ms | 13.9 | 20.1 | 2.0 | 0.3 | 62.9 |
| Visual, GLB | 0.9 | 4.6 | 20.7 | 0.8&nbsp;ms | 32.6 | 0.4 | 3.5 | 0.3 | 63.0 |
| Visual, OBJ | 0.8 | 4.8 | 20.8 | 0.8&nbsp;ms | 33.3 | 13.6 | 3.5 | 0.3 | 77.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kbeckmann/Kilsyth](https://github.com/kbeckmann/Kilsyth)<br>Board: `Kilsyth.kicad_pcb` |
|---|---|
| Folder | hardware / RevA |
| Complexity | 344&nbsp;/&nbsp;1000 (size&nbsp;279, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 160, 2,415, 431 |
| Triangles,&nbsp;simulation | 3,456,240 in 342 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">120&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">570&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">173&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">369&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">76&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">240&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1416. Kilsyth

![Kilsyth: stages 4 and 6 take 54% to 83% of a run. Simulation, GLB takes 31 s. Simulation, STEP takes 39 s. Simulation, STL takes 32 s. Simulation, OBJ takes 47 s. Visual, GLB takes 44 s. Visual, OBJ takes 54 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1416b_Kilsyth_hardware-RevB_Kilsyth/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 3.5 | 13.1 | 0.3&nbsp;ms | 12.0 | 0.6 | 1.2 | 0.3 | 31.4 |
| Simulation, STEP | 0.7 | 3.5 | 13.2 | 0.6&nbsp;ms | 12.0 | 7.9 | 1.1 | 0.3 | 38.6 |
| Simulation, STL | 0.7 | 3.5 | 13.1 | 0.3&nbsp;ms | 12.2 | 0.9 | 1.2 | 0.3 | 31.9 |
| Simulation, OBJ | 0.7 | 3.5 | 13.3 | 0.4&nbsp;ms | 12.3 | 16.2 | 1.1 | 0.2 | 47.2 |
| Visual, GLB | 0.7 | 3.5 | 13.3 | 0.8&nbsp;ms | 23.1 | 0.3 | 2.5 | 0.3 | 43.6 |
| Visual, OBJ | 0.7 | 3.6 | 13.2 | 0.4&nbsp;ms | 22.9 | 10.7 | 2.9 | 0.3 | 54.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kbeckmann/Kilsyth](https://github.com/kbeckmann/Kilsyth)<br>Board: `Kilsyth.kicad_pcb` |
|---|---|
| Folder | hardware / RevB |
| Complexity | 335&nbsp;/&nbsp;1000 (size&nbsp;270, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 145, 1,393, 378 |
| Triangles,&nbsp;simulation | 2,713,328 in 113 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">93&nbsp;MB</td><td align="right">871&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">406&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">136&nbsp;MB</td><td align="right">831&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">286&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">60&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">187&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1417. usb-c-breakout

![usb-c-breakout: stages 4 and 6 take 48% to 81% of a run. Simulation, GLB takes 6.9 s. Simulation, STEP takes 8.6 s. Simulation, STL takes 7.0 s. Simulation, OBJ takes 10 s. Visual, GLB takes 9.8 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1417b_Kilsyth_usb-c-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.9 | 2.8 | 0.3&nbsp;ms | 2.3 | 0.1 | 0.4 | 0.2 | 6.9 |
| Simulation, STEP | 0.2 | 0.8 | 2.9 | 0.3&nbsp;ms | 2.2 | 1.9 | 0.4 | 0.2 | 8.6 |
| Simulation, STL | 0.2 | 1.0 | 3.0 | 0.2&nbsp;ms | 2.2 | 0.2 | 0.3 | 0.2 | 7.0 |
| Simulation, OBJ | 0.1 | 0.8 | 2.7 | 0.2&nbsp;ms | 2.1 | 3.6 | 0.3 | 0.2 | 10.0 |
| Visual, GLB | 0.2 | 0.9 | 2.8 | 0.3&nbsp;ms | 5.1 | 70&nbsp;ms | 0.5 | 0.2 | 9.8 |
| Visual, OBJ | 0.2 | 0.8 | 3.0 | 0.3&nbsp;ms | 5.1 | 2.0 | 0.5 | 0.2 | 11.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kbeckmann/Kilsyth](https://github.com/kbeckmann/Kilsyth)<br>Board: `usb-c-breakout.kicad_pcb` |
|---|---|
| Folder | hardware / usb-c-breakout |
| Complexity | 245&nbsp;/&nbsp;1000 (size&nbsp;180, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 33, 602, 41 |
| Triangles,&nbsp;simulation | 823,370 in 66 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">29&nbsp;MB</td><td align="right">340&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">124&nbsp;MB</td><td align="right">398&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">41&nbsp;MB</td><td align="right">336&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">84&nbsp;MB</td><td align="right">583&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">401&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">45&nbsp;MB</td><td align="right">406&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1418. doj

![doj: stages 4 and 6 take 58% to 86% of a run. Simulation, GLB takes 22 s. Simulation, STEP takes 26 s. Simulation, STL takes 22 s. Simulation, OBJ takes 30 s. Visual, GLB takes 28 s. Visual, OBJ takes 34 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1418b_echomods_doj-source-v1-1-kicad_doj/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.6 | 11.1 | 1&nbsp;ms | 7.1 | 0.3 | 0.9 | 0.3 | 21.7 |
| Simulation, STEP | 0.2 | 1.6 | 10.9 | 0.8&nbsp;ms | 6.8 | 5.4 | 0.9 | 0.2 | 26.0 |
| Simulation, STL | 0.2 | 1.7 | 11.0 | 0.9&nbsp;ms | 7.2 | 0.6 | 0.9 | 0.2 | 21.8 |
| Simulation, OBJ | 0.2 | 1.7 | 10.7 | 0.7&nbsp;ms | 7.0 | 9.7 | 0.9 | 0.3 | 30.5 |
| Visual, GLB | 0.2 | 1.6 | 10.6 | 0.8&nbsp;ms | 13.7 | 0.2 | 1.7 | 0.2 | 28.2 |
| Visual, OBJ | 0.3 | 1.6 | 10.9 | 0.7&nbsp;ms | 13.7 | 5.5 | 1.8 | 0.2 | 33.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kelu124/echomods](https://github.com/kelu124/echomods)<br>Board: `doj.kicad_pcb` |
|---|---|
| Folder | doj / source / v1.1-kicad |
| Complexity | 197&nbsp;/&nbsp;1000 (size&nbsp;152, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 17, 530, 8 |
| Triangles,&nbsp;simulation | 2,267,576 in 123 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">77&nbsp;MB</td><td align="right">871&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">395&nbsp;MB</td><td align="right">901&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">113&nbsp;MB</td><td align="right">828&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">240&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">885&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">137&nbsp;MB</td><td align="right">978&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1419. doj

![doj: stages 4 and 6 take 58% to 84% of a run. Simulation, GLB takes 24 s. Simulation, STEP takes 30 s. Simulation, STL takes 24 s. Simulation, OBJ takes 34 s. Visual, GLB takes 33 s. Visual, OBJ takes 39 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1419b_echomods_doj-source-v1-2-kicad_doj/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 2.1 | 11.9 | 0.8&nbsp;ms | 7.9 | 0.4 | 0.9 | 0.2 | 23.7 |
| Simulation, STEP | 0.3 | 1.9 | 12.0 | 1.0&nbsp;ms | 7.8 | 6.2 | 1.0 | 0.3 | 29.5 |
| Simulation, STL | 0.3 | 2.0 | 11.8 | 1&nbsp;ms | 7.7 | 0.8 | 1.0 | 0.3 | 23.9 |
| Simulation, OBJ | 0.3 | 2.0 | 11.6 | 1&nbsp;ms | 7.9 | 10.7 | 1.1 | 0.3 | 33.9 |
| Visual, GLB | 0.3 | 2.2 | 11.4 | 0.9&nbsp;ms | 16.2 | 0.2 | 2.1 | 0.3 | 32.7 |
| Visual, OBJ | 0.3 | 2.1 | 12.2 | 1.0&nbsp;ms | 15.8 | 6.7 | 2.0 | 0.3 | 39.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kelu124/echomods](https://github.com/kelu124/echomods)<br>Board: `doj.kicad_pcb` |
|---|---|
| Folder | doj / source / v1.2-kicad |
| Complexity | 197&nbsp;/&nbsp;1000 (size&nbsp;152, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 17, 557, 8 |
| Triangles,&nbsp;simulation | 2,371,252 in 118 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">81&nbsp;MB</td><td align="right">883&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">416&nbsp;MB</td><td align="right">946&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">119&nbsp;MB</td><td align="right">828&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">252&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">51&nbsp;MB</td><td align="right">923&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">156&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1420. doj_v2

![doj_v2: stages 4 and 6 take 56% to 86% of a run. Simulation, GLB takes 22 s. Simulation, STEP takes 28 s. Simulation, STL takes 22 s. Simulation, OBJ takes 34 s. Visual, GLB takes 31 s. Visual, OBJ takes 37 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1420b_echomods_doj-v2/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.7 | 11.0 | 0.5&nbsp;ms | 7.4 | 0.3 | 1.0 | 0.2 | 22.1 |
| Simulation, STEP | 0.4 | 1.7 | 11.1 | 0.5&nbsp;ms | 7.5 | 5.9 | 0.9 | 0.2 | 27.9 |
| Simulation, STL | 0.4 | 1.7 | 11.0 | 0.6&nbsp;ms | 7.3 | 0.7 | 1.0 | 0.3 | 22.3 |
| Simulation, OBJ | 0.4 | 1.7 | 11.3 | 0.5&nbsp;ms | 7.7 | 11.4 | 1.0 | 0.3 | 33.9 |
| Visual, GLB | 0.4 | 1.8 | 11.0 | 0.5&nbsp;ms | 15.5 | 0.2 | 1.8 | 0.3 | 30.8 |
| Visual, OBJ | 0.5 | 1.7 | 10.8 | 0.5&nbsp;ms | 14.7 | 7.1 | 1.8 | 0.2 | 36.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kelu124/echomods](https://github.com/kelu124/echomods)<br>Board: `doj_v2.kicad_pcb` |
|---|---|
| Folder | doj / source / v2.0-kicad |
| Complexity | 208&nbsp;/&nbsp;1000 (size&nbsp;153, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20170123) |
| Parts,&nbsp;tracks,&nbsp;vias | 22, 497, 9 |
| Triangles,&nbsp;simulation | 1,926,826 in 53 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">67&nbsp;MB</td><td align="right">670&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">331&nbsp;MB</td><td align="right">782&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">96&nbsp;MB</td><td align="right">706&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">204&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">41&nbsp;MB</td><td align="right">811&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">124&nbsp;MB</td><td align="right">885&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1421. goblin

![goblin: stages 4 and 6 take 54% to 78% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 13 s. Simulation, STL takes 11 s. Simulation, OBJ takes 15 s. Visual, GLB takes 14 s. Visual, OBJ takes 17 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1421b_echomods_goblin/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.5 | 4.3 | 0.7&nbsp;ms | 3.9 | 0.1 | 0.6 | 0.3 | 11.1 |
| Simulation, STEP | 0.4 | 1.5 | 4.2 | 0.4&nbsp;ms | 3.8 | 2.5 | 0.5 | 0.2 | 13.1 |
| Simulation, STL | 0.3 | 1.6 | 4.2 | 0.3&nbsp;ms | 3.9 | 0.3 | 0.5 | 0.3 | 11.0 |
| Simulation, OBJ | 0.3 | 1.4 | 4.3 | 0.4&nbsp;ms | 3.6 | 4.1 | 0.5 | 0.3 | 14.6 |
| Visual, GLB | 0.3 | 1.5 | 4.4 | 0.3&nbsp;ms | 6.3 | 0.1 | 0.9 | 0.3 | 13.7 |
| Visual, OBJ | 0.4 | 1.5 | 4.5 | 0.5&nbsp;ms | 6.1 | 3.4 | 1.0 | 0.3 | 17.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kelu124/echomods](https://github.com/kelu124/echomods)<br>Board: `goblin.kicad_pcb` |
|---|---|
| Folder | goblin / source / Kicad |
| Complexity | 198&nbsp;/&nbsp;1000 (size&nbsp;163, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 60, 459, 12 |
| Triangles,&nbsp;simulation | 718,532 in 94 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">25&nbsp;MB</td><td align="right">376&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">123&nbsp;MB</td><td align="right">462&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">36&nbsp;MB</td><td align="right">370&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">74&nbsp;MB</td><td align="right">553&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">471&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">58&nbsp;MB</td><td align="right">504&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1422. tobo

![tobo: stages 4 and 6 take 60% to 77% of a run. Simulation, GLB takes 6.6 s. Simulation, STEP takes 8.4 s. Simulation, STL takes 6.7 s. Simulation, OBJ takes 8.4 s. Visual, GLB takes 7.1 s. Visual, OBJ takes 8.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1422b_echomods_tobo/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 1.0 | 2.5 | 0.3&nbsp;ms | 2.4 | 72&nbsp;ms | 0.3 | 0.2 | 6.6 |
| Simulation, STEP | 0.2 | 0.9 | 2.5 | 0.3&nbsp;ms | 2.6 | 1.7 | 0.3 | 0.2 | 8.4 |
| Simulation, STL | 0.2 | 0.9 | 2.5 | 0.3&nbsp;ms | 2.5 | 0.1 | 0.3 | 0.2 | 6.7 |
| Simulation, OBJ | 0.2 | 0.9 | 2.5 | 0.3&nbsp;ms | 2.5 | 1.8 | 0.3 | 0.2 | 8.4 |
| Visual, GLB | 0.2 | 0.9 | 2.5 | 0.3&nbsp;ms | 2.9 | 40&nbsp;ms | 0.3 | 0.2 | 7.1 |
| Visual, OBJ | 0.2 | 0.9 | 2.5 | 0.3&nbsp;ms | 3.0 | 1.2 | 0.3 | 0.2 | 8.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kelu124/echomods](https://github.com/kelu124/echomods)<br>Board: `tobo.kicad_pcb` |
|---|---|
| Folder | retired / tobo / source / Kicad |
| Complexity | 156&nbsp;/&nbsp;1000 (size&nbsp;141, features&nbsp;15) |
| KESE&nbsp;features | through vias |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 23, 227, 6 |
| Triangles,&nbsp;simulation | 443,022 in 60 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">290&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">67&nbsp;MB</td><td align="right">344&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">22&nbsp;MB</td><td align="right">286&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">46&nbsp;MB</td><td align="right">375&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">324&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">31&nbsp;MB</td><td align="right">334&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1423. CM5_MINIMA_3

![CM5_MINIMA_3: stages 4 and 6 take 50% to 85% of a run. Simulation, GLB takes 38 s. Simulation, STEP takes 45 s. Simulation, STL takes 38 s. Simulation, OBJ takes 61 s. Visual, GLB takes 50 s. Visual, OBJ takes 62 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1423b_kicad-source-mirror_CM5-MINIMA-3/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 3.5 | 14.3 | 1&nbsp;ms | 15.6 | 0.8 | 2.2 | 0.3 | 37.6 |
| Simulation, STEP | 0.9 | 3.4 | 14.2 | 1&nbsp;ms | 15.7 | 8.8 | 2.2 | 0.3 | 45.4 |
| Simulation, STL | 0.9 | 3.5 | 14.2 | 1.0&nbsp;ms | 15.9 | 1.3 | 2.2 | 0.3 | 38.4 |
| Simulation, OBJ | 1.0 | 3.7 | 14.5 | 1&nbsp;ms | 15.7 | 23.5 | 2.2 | 0.3 | 60.9 |
| Visual, GLB | 1.0 | 3.8 | 14.7 | 1&nbsp;ms | 27.4 | 0.3 | 2.2 | 0.3 | 49.6 |
| Visual, OBJ | 0.9 | 3.7 | 14.9 | 1&nbsp;ms | 29.9 | 10.3 | 2.5 | 0.3 | 62.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `CM5_MINIMA_3.kicad_pcb` |
|---|---|
| Folder | demos / cm5_minima |
| Complexity | 348&nbsp;/&nbsp;1000 (size&nbsp;223, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20250513) |
| Parts,&nbsp;tracks,&nbsp;vias | 72, 2,084, 444 |
| Triangles,&nbsp;simulation | 4,184,934 in 236 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">143&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">541&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">209&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">451&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">67&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">211&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1424. complex_hierarchy

![complex_hierarchy: stages 4 and 6 take 53% to 83% of a run. Simulation, GLB takes 9.8 s. Simulation, STEP takes 13 s. Simulation, STL takes 10 s. Simulation, OBJ takes 16 s. Visual, GLB takes 13 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1424b_kicad-source-mirror_complex-hierarchy/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 0.8 | 4.1 | 0.6&nbsp;ms | 3.4 | 0.2 | 0.6 | 0.3 | 9.8 |
| Simulation, STEP | 0.3 | 0.9 | 4.1 | 0.6&nbsp;ms | 3.9 | 3.3 | 0.5 | 0.3 | 13.2 |
| Simulation, STL | 0.4 | 0.8 | 4.2 | 0.9&nbsp;ms | 3.9 | 0.3 | 0.6 | 0.3 | 10.5 |
| Simulation, OBJ | 0.4 | 0.8 | 4.3 | 0.7&nbsp;ms | 4.1 | 5.5 | 0.6 | 0.3 | 15.9 |
| Visual, GLB | 0.3 | 0.8 | 4.2 | 1.0&nbsp;ms | 7.0 | 80&nbsp;ms | 0.8 | 0.2 | 13.5 |
| Visual, OBJ | 0.3 | 0.8 | 4.0 | 0.5&nbsp;ms | 6.9 | 3.2 | 0.8 | 0.2 | 16.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `complex_hierarchy.kicad_pcb` |
|---|---|
| Folder | demos / complex_hierarchy |
| Complexity | 244&nbsp;/&nbsp;1000 (size&nbsp;159, features&nbsp;85) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>drill offsets, filled zones,<br>copper text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 68, 364, 0 |
| Triangles,&nbsp;simulation | 932,774 in 63 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">450&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">148&nbsp;MB</td><td align="right">515&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">47&nbsp;MB</td><td align="right">418&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">94&nbsp;MB</td><td align="right">677&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">523&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">55&nbsp;MB</td><td align="right">538&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1425. ecc83-pp

![ecc83-pp: stages 4 and 6 take 49% to 78% of a run. Simulation, GLB takes 2.2 s. Simulation, STEP takes 3.4 s. Simulation, STL takes 2.2 s. Simulation, OBJ takes 3.1 s. Visual, GLB takes 2.8 s. Visual, OBJ takes 3.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1425b_kicad-source-mirror_ecc83-pp/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.7 | 0.1&nbsp;ms | 0.8 | 30&nbsp;ms | 0.1 | 0.2 | 2.2 |
| Simulation, STEP | 0.1 | 0.2 | 0.9 | 0.2&nbsp;ms | 0.9 | 1.1 | 0.1 | 0.2 | 3.4 |
| Simulation, STL | 0.1 | 0.2 | 0.8 | 0.3&nbsp;ms | 0.8 | 41&nbsp;ms | 96&nbsp;ms | 0.2 | 2.2 |
| Simulation, OBJ | 0.1 | 0.1 | 0.7 | 0.1&nbsp;ms | 0.8 | 1.0 | 0.1 | 0.2 | 3.1 |
| Visual, GLB | 0.1 | 0.1 | 0.7 | 0.1&nbsp;ms | 1.5 | 17&nbsp;ms | 0.1 | 0.2 | 2.8 |
| Visual, OBJ | 0.1 | 0.2 | 0.7 | 0.2&nbsp;ms | 1.5 | 0.6 | 0.1 | 0.2 | 3.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `ecc83-pp.kicad_pcb` |
|---|---|
| Folder | demos / ecc83 |
| Complexity | 166&nbsp;/&nbsp;1000 (size&nbsp;111, features&nbsp;55) |
| KESE&nbsp;features | filled zones, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 11, 59, 0 |
| Triangles,&nbsp;simulation | 177,454 in 23 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">5.9&nbsp;MB</td><td align="right">201&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">23&nbsp;MB</td><td align="right">214&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">8.9&nbsp;MB</td><td align="right">201&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">17&nbsp;MB</td><td align="right">200&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.5&nbsp;MB</td><td align="right">175&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.8&nbsp;MB</td><td align="right">172&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1426. ecc83-pp_v2

![ecc83-pp_v2: stages 4 and 6 take 51% to 78% of a run. Simulation, GLB takes 2.3 s. Simulation, STEP takes 3.4 s. Simulation, STL takes 2.3 s. Simulation, OBJ takes 3.2 s. Visual, GLB takes 2.8 s. Visual, OBJ takes 3.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1426b_kicad-source-mirror_ecc83-pp-v2/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.8 | 0.3&nbsp;ms | 0.9 | 30&nbsp;ms | 0.1 | 0.2 | 2.3 |
| Simulation, STEP | 0.1 | 0.2 | 0.7 | 0.2&nbsp;ms | 1.0 | 1.0 | 0.1 | 0.2 | 3.4 |
| Simulation, STL | 0.1 | 0.2 | 0.7 | 0.2&nbsp;ms | 0.9 | 45&nbsp;ms | 0.1 | 0.2 | 2.3 |
| Simulation, OBJ | 0.1 | 0.2 | 0.8 | 0.2&nbsp;ms | 1.0 | 0.9 | 0.1 | 0.2 | 3.2 |
| Visual, GLB | 0.1 | 0.1 | 0.7 | 0.3&nbsp;ms | 1.5 | 18&nbsp;ms | 0.1 | 0.2 | 2.8 |
| Visual, OBJ | 0.1 | 0.2 | 0.7 | 0.2&nbsp;ms | 1.5 | 0.6 | 0.1 | 0.2 | 3.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `ecc83-pp_v2.kicad_pcb` |
|---|---|
| Folder | demos / ecc83 |
| Complexity | 174&nbsp;/&nbsp;1000 (size&nbsp;109, features&nbsp;65) |
| KESE&nbsp;features | slotted holes, filled zones,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 11, 53, 0 |
| Triangles,&nbsp;simulation | 167,764 in 24 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">5.6&nbsp;MB</td><td align="right">195&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">25&nbsp;MB</td><td align="right">212&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">8.4&nbsp;MB</td><td align="right">199&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">16&nbsp;MB</td><td align="right">196&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.4&nbsp;MB</td><td align="right">169&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.5&nbsp;MB</td><td align="right">167&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1427. interf_u

![interf_u: stages 4 and 6 take 56% to 85% of a run. Simulation, GLB takes 19 s. Simulation, STEP takes 23 s. Simulation, STL takes 18 s. Simulation, OBJ takes 26 s. Visual, GLB takes 24 s. Visual, OBJ takes 30 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1427b_kicad-source-mirror_interf-u/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.4 | 7.9 | 0.8&nbsp;ms | 7.4 | 0.3 | 0.9 | 0.3 | 18.5 |
| Simulation, STEP | 0.3 | 1.3 | 7.8 | 0.7&nbsp;ms | 7.1 | 5.0 | 0.9 | 0.3 | 22.6 |
| Simulation, STL | 0.3 | 1.4 | 8.0 | 1&nbsp;ms | 6.9 | 0.8 | 0.9 | 0.3 | 18.5 |
| Simulation, OBJ | 0.3 | 1.4 | 7.8 | 0.7&nbsp;ms | 6.8 | 8.7 | 0.9 | 0.3 | 26.1 |
| Visual, GLB | 0.3 | 1.3 | 7.5 | 0.7&nbsp;ms | 13.1 | 0.2 | 1.6 | 0.2 | 24.2 |
| Visual, OBJ | 0.3 | 1.4 | 7.6 | 0.7&nbsp;ms | 13.0 | 5.3 | 2.0 | 0.3 | 29.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `interf_u.kicad_pcb` |
|---|---|
| Folder | demos / interf_u |
| Complexity | 245&nbsp;/&nbsp;1000 (size&nbsp;165, features&nbsp;80) |
| KESE&nbsp;features | through vias, filled zones,<br>copper text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 24, 731, 84 |
| Triangles,&nbsp;simulation | 1,806,582 in 184 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">60&nbsp;MB</td><td align="right">680&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">248&nbsp;MB</td><td align="right">817&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">90&nbsp;MB</td><td align="right">714&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">185&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">35&nbsp;MB</td><td align="right">812&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">107&nbsp;MB</td><td align="right">790&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1428. kit-dev-coldfire-xilinx_5213

![kit-dev-coldfire-xilinx_5213: stages 4 and 6 take 48% to 82% of a run. Simulation, GLB takes 35 s. Simulation, STEP takes 46 s. Simulation, STL takes 37 s. Simulation, OBJ takes 59 s. Visual, GLB takes 53 s. Visual, OBJ takes 66 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1428b_kicad-source-mirror_kit-dev-coldfire-xilinx-5213/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 3.7 | 12.9 | 0.7&nbsp;ms | 14.9 | 0.7 | 1.9 | 0.3 | 35.4 |
| Simulation, STEP | 0.9 | 3.9 | 12.9 | 1&nbsp;ms | 15.6 | 10.3 | 1.9 | 0.3 | 45.8 |
| Simulation, STL | 0.9 | 3.8 | 12.9 | 1&nbsp;ms | 15.4 | 1.5 | 1.9 | 0.3 | 36.7 |
| Simulation, OBJ | 0.9 | 3.9 | 13.0 | 1&nbsp;ms | 15.4 | 23.2 | 2.0 | 0.3 | 58.9 |
| Visual, GLB | 1.0 | 4.1 | 13.3 | 1.0&nbsp;ms | 30.1 | 0.3 | 3.6 | 0.3 | 52.6 |
| Visual, OBJ | 1.0 | 4.0 | 13.1 | 0.9&nbsp;ms | 29.9 | 14.1 | 3.8 | 0.3 | 66.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `kit-dev-coldfire-xilinx_5213.kicad_pcb` |
|---|---|
| Folder | demos / kit-dev-coldfire-xilinx_5213 |
| Complexity | 384&nbsp;/&nbsp;1000 (size&nbsp;269, features&nbsp;115) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 154, 2,935, 253 |
| Triangles,&nbsp;simulation | 3,721,378 in 292 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">126&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">487&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">186&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">392&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">76&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">240&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1429. microwave

![microwave: stages 4 and 6 take 30% to 60% of a run. Simulation, GLB takes 0.9 s. Simulation, STEP takes 1.9 s. Simulation, STL takes 1.1 s. Simulation, OBJ takes 1.3 s. Visual, GLB takes 1.1 s. Visual, OBJ takes 1.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1429b_kicad-source-mirror_microwave/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 94&nbsp;ms | 43&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.4 | 8&nbsp;ms | 27&nbsp;ms | 0.2 | 0.9 |
| Simulation, STEP | 0.1 | 44&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.4 | 0.9 | 25&nbsp;ms | 0.2 | 1.9 |
| Simulation, STL | 0.1 | 45&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.5 | 21&nbsp;ms | 29&nbsp;ms | 0.2 | 1.1 |
| Simulation, OBJ | 91&nbsp;ms | 42&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.4 | 0.3 | 26&nbsp;ms | 0.2 | 1.3 |
| Visual, GLB | 94&nbsp;ms | 44&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.5 | 13&nbsp;ms | 82&nbsp;ms | 0.2 | 1.1 |
| Visual, OBJ | 0.1 | 46&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.5 | 0.2 | 58&nbsp;ms | 0.2 | 1.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `microwave.kicad_pcb` |
|---|---|
| Folder | demos / microwave |
| Complexity | 34&nbsp;/&nbsp;1000 (size&nbsp;34, features&nbsp;0) |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 4, 0, 0 |
| Triangles,&nbsp;simulation | 54,124 in 5 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.8&nbsp;MB</td><td align="right">81&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">14&nbsp;MB</td><td align="right">205&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">2.7&nbsp;MB</td><td align="right">80&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">5.0&nbsp;MB</td><td align="right">92&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">1.1&nbsp;MB</td><td align="right">98&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.0&nbsp;MB</td><td align="right">106&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1430. multichannel_mixer-unrouted

![multichannel_mixer-unrouted: stages 4 and 6 take 48% to 82% of a run. Simulation, GLB takes 9.8 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.7 s. Simulation, OBJ takes 15 s. Visual, GLB takes 14 s. Visual, OBJ takes 19 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1430b_kicad-source-mirror_multichannel-mixer-unrouted/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.0 | 4.2 | 0.6&nbsp;ms | 3.2 | 0.2 | 0.5 | 0.2 | 9.8 |
| Simulation, STEP | 0.5 | 0.9 | 4.0 | 1&nbsp;ms | 3.1 | 3.0 | 0.5 | 0.3 | 12.3 |
| Simulation, STL | 0.5 | 0.9 | 4.0 | 0.6&nbsp;ms | 3.1 | 0.3 | 0.5 | 0.3 | 9.7 |
| Simulation, OBJ | 0.5 | 0.9 | 4.1 | 0.6&nbsp;ms | 3.2 | 5.6 | 0.5 | 0.2 | 15.1 |
| Visual, GLB | 0.5 | 0.9 | 4.0 | 0.6&nbsp;ms | 7.9 | 0.1 | 0.9 | 0.2 | 14.4 |
| Visual, OBJ | 0.5 | 0.9 | 4.2 | 0.5&nbsp;ms | 7.8 | 4.1 | 1.0 | 0.2 | 18.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `multichannel_mixer-unrouted.kicad_pcb` |
|---|---|
| Folder | demos / multichannel |
| Complexity | 251&nbsp;/&nbsp;1000 (size&nbsp;196, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 11 |
| File&nbsp;format | KiCad 9 (20241030) |
| Parts,&nbsp;tracks,&nbsp;vias | 114, 140, 19 |
| Triangles,&nbsp;simulation | 941,284 in 88 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">466&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">148&nbsp;MB</td><td align="right">526&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">47&nbsp;MB</td><td align="right">477&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">95&nbsp;MB</td><td align="right">673&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">637&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">69&nbsp;MB</td><td align="right">623&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1431. multichannel_mixer

![multichannel_mixer: stages 4 and 6 take 51% to 81% of a run. Simulation, GLB takes 9.7 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.4 s. Simulation, OBJ takes 14 s. Visual, GLB takes 14 s. Visual, OBJ takes 18 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1431b_kicad-source-mirror_multichannel-mixer/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 0.9 | 4.1 | 1&nbsp;ms | 3.4 | 0.2 | 0.5 | 0.2 | 9.7 |
| Simulation, STEP | 0.5 | 0.8 | 3.9 | 0.8&nbsp;ms | 3.1 | 2.8 | 0.4 | 0.2 | 11.8 |
| Simulation, STL | 0.5 | 0.9 | 4.0 | 0.6&nbsp;ms | 3.3 | 0.2 | 0.4 | 0.2 | 9.4 |
| Simulation, OBJ | 0.4 | 0.8 | 4.0 | 0.5&nbsp;ms | 3.3 | 5.3 | 0.4 | 0.2 | 14.4 |
| Visual, GLB | 0.4 | 0.8 | 3.9 | 0.5&nbsp;ms | 7.4 | 0.1 | 1.0 | 0.2 | 14.0 |
| Visual, OBJ | 0.4 | 0.9 | 3.9 | 0.6&nbsp;ms | 7.5 | 4.0 | 1.1 | 0.2 | 18.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `multichannel_mixer.kicad_pcb` |
|---|---|
| Folder | demos / multichannel |
| Complexity | 230&nbsp;/&nbsp;1000 (size&nbsp;175, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 114, 576, 29 |
| Triangles,&nbsp;simulation | 1,027,228 in 92 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">34&nbsp;MB</td><td align="right">449&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">171&nbsp;MB</td><td align="right">548&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">51&nbsp;MB</td><td align="right">456&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">104&nbsp;MB</td><td align="right">741&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">621&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">78&nbsp;MB</td><td align="right">649&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1432. One-Air-Max

![One-Air-Max: stages 4 and 6 take 46% to 81% of a run. Simulation, GLB takes 21 s. Simulation, STEP takes 27 s. Simulation, STL takes 22 s. Simulation, OBJ takes 34 s. Visual, GLB takes 34 s. Visual, OBJ takes 44 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1432b_kicad-source-mirror_One-Air-Max/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 3.0 | 8.4 | 1.0&nbsp;ms | 7.2 | 0.4 | 1.0 | 0.3 | 21.0 |
| Simulation, STEP | 0.8 | 3.0 | 8.5 | 0.8&nbsp;ms | 7.1 | 6.0 | 1.0 | 0.3 | 26.6 |
| Simulation, STL | 0.9 | 3.0 | 8.5 | 0.9&nbsp;ms | 7.3 | 0.7 | 1.0 | 0.3 | 21.6 |
| Simulation, OBJ | 0.8 | 3.0 | 8.6 | 1&nbsp;ms | 7.2 | 13.1 | 1.0 | 0.3 | 34.0 |
| Visual, GLB | 0.8 | 2.9 | 8.5 | 1&nbsp;ms | 18.7 | 0.2 | 2.2 | 0.2 | 33.6 |
| Visual, OBJ | 0.8 | 3.0 | 8.5 | 1&nbsp;ms | 19.1 | 9.3 | 2.6 | 0.3 | 43.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `One-Air-Max.kicad_pcb` |
|---|---|
| Folder | demos / openair-max |
| Complexity | 361&nbsp;/&nbsp;1000 (size&nbsp;221, features&nbsp;140) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, arc tracks,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 199, 1,654, 410 |
| Triangles,&nbsp;simulation | 2,177,588 in 169 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">76&nbsp;MB</td><td align="right">790&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">294&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">109&nbsp;MB</td><td align="right">775&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">230&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">55&nbsp;MB</td><td align="right">963&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">170&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1433. pic_programmer

![pic_programmer: stages 4 and 6 take 54% to 86% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 15 s. Simulation, STL takes 12 s. Simulation, OBJ takes 18 s. Visual, GLB takes 17 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1433b_kicad-source-mirror_pic-programmer/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.0 | 5.2 | 0.4&nbsp;ms | 4.7 | 0.2 | 0.6 | 0.2 | 12.2 |
| Simulation, STEP | 0.3 | 0.9 | 5.2 | 0.5&nbsp;ms | 4.6 | 3.7 | 0.6 | 0.3 | 15.4 |
| Simulation, STL | 0.3 | 0.9 | 5.1 | 0.4&nbsp;ms | 4.8 | 0.4 | 0.6 | 0.2 | 12.4 |
| Simulation, OBJ | 0.3 | 0.9 | 5.2 | 0.4&nbsp;ms | 4.7 | 6.5 | 0.5 | 0.2 | 18.4 |
| Visual, GLB | 0.3 | 0.9 | 5.1 | 0.7&nbsp;ms | 9.9 | 0.1 | 1.0 | 0.2 | 17.4 |
| Visual, OBJ | 0.3 | 0.9 | 5.7 | 0.4&nbsp;ms | 9.9 | 4.4 | 1.1 | 0.2 | 22.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `pic_programmer.kicad_pcb` |
|---|---|
| Folder | demos / pic_programmer |
| Complexity | 273&nbsp;/&nbsp;1000 (size&nbsp;158, features&nbsp;115) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 57, 370, 6 |
| Triangles,&nbsp;simulation | 1,330,386 in 123 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">44&nbsp;MB</td><td align="right">573&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">211&nbsp;MB</td><td align="right">662&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">67&nbsp;MB</td><td align="right">546&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">134&nbsp;MB</td><td align="right">884&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">792&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">84&nbsp;MB</td><td align="right">687&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1434. RoyalBlue54L-NFC-Antenna

![RoyalBlue54L-NFC-Antenna: stages 4 and 6 take 39% to 71% of a run. Simulation, GLB takes 0.9 s. Simulation, STEP takes 1.6 s. Simulation, STL takes 1.0 s. Simulation, OBJ takes 1.3 s. Visual, GLB takes 1.4 s. Visual, OBJ takes 1.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1434b_kicad-source-mirror_RoyalBlue54L-NFC-Antenna/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 28&nbsp;ms | 56&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.5 | 11&nbsp;ms | 25&nbsp;ms | 0.2 | 0.9 |
| Simulation, STEP | 30&nbsp;ms | 59&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.5 | 0.7 | 25&nbsp;ms | 0.2 | 1.6 |
| Simulation, STL | 31&nbsp;ms | 56&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.5 | 19&nbsp;ms | 26&nbsp;ms | 0.2 | 1.0 |
| Simulation, OBJ | 29&nbsp;ms | 56&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.5 | 0.3 | 32&nbsp;ms | 0.2 | 1.3 |
| Visual, GLB | 33&nbsp;ms | 62&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.9 | 11&nbsp;ms | 72&nbsp;ms | 0.2 | 1.4 |
| Visual, OBJ | 29&nbsp;ms | 61&nbsp;ms | 0.1 | 0.1&nbsp;ms | 0.8 | 0.3 | 64&nbsp;ms | 0.2 | 1.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `RoyalBlue54L-NFC-Antenna.kicad_pcb` |
|---|---|
| Folder | demos / royalblue54L_feather / nfc_antenna / RoyalBlue54L-NFC-Antenna |
| Complexity | 168&nbsp;/&nbsp;1000 (size&nbsp;108, features&nbsp;60) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, copper drawings,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 1, 160, 2 |
| Triangles,&nbsp;simulation | 67,926 in 7 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">2.3&nbsp;MB</td><td align="right">159&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">7.9&nbsp;MB</td><td align="right">160&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">3.4&nbsp;MB</td><td align="right">154&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.4&nbsp;MB</td><td align="right">158&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">2.2&nbsp;MB</td><td align="right">132&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.2&nbsp;MB</td><td align="right">131&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1435. RoyalBlue54L-Feather

![RoyalBlue54L-Feather: stages 4 and 6 take 44% to 81% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 19 s. Simulation, STL takes 16 s. Simulation, OBJ takes 24 s. Visual, GLB takes 20 s. Visual, OBJ takes 26 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1435b_kicad-source-mirror_RoyalBlue54L-Feather/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 2.1 | 4.9 | 2&nbsp;ms | 6.5 | 0.3 | 1.1 | 0.3 | 16.0 |
| Simulation, STEP | 0.8 | 1.9 | 4.8 | 0.5&nbsp;ms | 6.2 | 4.4 | 1.1 | 0.3 | 19.4 |
| Simulation, STL | 0.9 | 1.9 | 4.8 | 0.6&nbsp;ms | 6.4 | 0.5 | 1.1 | 0.2 | 15.8 |
| Simulation, OBJ | 0.8 | 2.0 | 4.6 | 0.5&nbsp;ms | 6.0 | 9.6 | 1.1 | 0.3 | 24.3 |
| Visual, GLB | 0.7 | 1.8 | 4.6 | 0.6&nbsp;ms | 12.0 | 0.1 | 0.9 | 0.3 | 20.5 |
| Visual, OBJ | 0.8 | 1.9 | 4.6 | 0.5&nbsp;ms | 12.4 | 5.0 | 1.2 | 0.3 | 26.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `RoyalBlue54L-Feather.kicad_pcb` |
|---|---|
| Folder | demos / royalblue54L_feather |
| Complexity | 500&nbsp;/&nbsp;1000 (size&nbsp;270, features&nbsp;230) |
| KESE&nbsp;features | blind and buried vias,<br>slotted holes, custom pads,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, arc tracks,<br>filled zones, copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours,<br>castellated pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 54, 943, 183 |
| Triangles,&nbsp;simulation | 1,623,990 in 115 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">56&nbsp;MB</td><td align="right">547&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">233&nbsp;MB</td><td align="right">667&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">81&nbsp;MB</td><td align="right">550&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">171&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">708&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">82&nbsp;MB</td><td align="right">652&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1436. sonde xilinx

![sonde xilinx: stages 4 and 6 take 49% to 82% of a run. Simulation, GLB takes 3.5 s. Simulation, STEP takes 4.5 s. Simulation, STL takes 3.4 s. Simulation, OBJ takes 5.1 s. Visual, GLB takes 5.6 s. Visual, OBJ takes 6.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1436b_kicad-source-mirror_sonde-xilinx/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.3 | 0.2&nbsp;ms | 1.3 | 63&nbsp;ms | 0.2 | 0.2 | 3.5 |
| Simulation, STEP | 0.1 | 0.2 | 1.3 | 0.3&nbsp;ms | 1.2 | 1.3 | 0.2 | 0.2 | 4.5 |
| Simulation, STL | 0.1 | 0.2 | 1.3 | 0.3&nbsp;ms | 1.3 | 89&nbsp;ms | 0.2 | 0.2 | 3.4 |
| Simulation, OBJ | 0.1 | 0.2 | 1.3 | 0.2&nbsp;ms | 1.2 | 1.8 | 0.2 | 0.2 | 5.1 |
| Visual, GLB | 0.2 | 0.3 | 1.3 | 0.2&nbsp;ms | 3.3 | 36&nbsp;ms | 0.3 | 0.2 | 5.6 |
| Visual, OBJ | 0.1 | 0.3 | 1.3 | 0.3&nbsp;ms | 3.3 | 1.2 | 0.3 | 0.2 | 6.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `sonde xilinx.kicad_pcb` |
|---|---|
| Folder | demos / sonde xilinx |
| Complexity | 235&nbsp;/&nbsp;1000 (size&nbsp;140, features&nbsp;95) |
| KESE&nbsp;features | through vias, filled zones,<br>copper text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 25, 208, 3 |
| Triangles,&nbsp;simulation | 454,014 in 54 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">311&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">72&nbsp;MB</td><td align="right">333&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">23&nbsp;MB</td><td align="right">320&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">45&nbsp;MB</td><td align="right">347&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">10.0&nbsp;MB</td><td align="right">345&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">30&nbsp;MB</td><td align="right">343&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1437. StickHub

![StickHub: stages 4 and 6 take 52% to 83% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 13 s. Simulation, STL takes 11 s. Simulation, OBJ takes 17 s. Visual, GLB takes 14 s. Visual, OBJ takes 18 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1437b_kicad-source-mirror_StickHub/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 0.7 | 3.8 | 0.4&nbsp;ms | 4.7 | 0.2 | 0.5 | 0.2 | 10.5 |
| Simulation, STEP | 0.4 | 0.7 | 3.7 | 0.4&nbsp;ms | 4.9 | 2.8 | 0.4 | 0.3 | 13.2 |
| Simulation, STL | 0.4 | 0.7 | 3.9 | 0.7&nbsp;ms | 4.9 | 0.3 | 0.4 | 0.3 | 10.9 |
| Simulation, OBJ | 0.4 | 0.7 | 3.9 | 0.4&nbsp;ms | 4.8 | 6.0 | 0.5 | 0.2 | 16.6 |
| Visual, GLB | 0.5 | 0.7 | 4.0 | 0.4&nbsp;ms | 7.9 | 0.1 | 0.7 | 0.3 | 14.4 |
| Visual, OBJ | 0.4 | 0.7 | 3.9 | 0.5&nbsp;ms | 8.3 | 3.7 | 0.8 | 0.2 | 18.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `StickHub.kicad_pcb` |
|---|---|
| Folder | demos / stickhub |
| Complexity | 366&nbsp;/&nbsp;1000 (size&nbsp;226, features&nbsp;140) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20250907) |
| Parts,&nbsp;tracks,&nbsp;vias | 88, 1,293, 87 |
| Triangles,&nbsp;simulation | 930,590 in 58 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">384&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">166&nbsp;MB</td><td align="right">505&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">47&nbsp;MB</td><td align="right">396&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">95&nbsp;MB</td><td align="right">663&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">21&nbsp;MB</td><td align="right">547&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">62&nbsp;MB</td><td align="right">516&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1438. tinytapeout-demo

![tinytapeout-demo: stages 4 and 6 take 50% to 81% of a run. Simulation, GLB takes 42 s. Simulation, STEP takes 52 s. Simulation, STL takes 42 s. Simulation, OBJ takes 63 s. Visual, GLB takes 72 s. Visual, OBJ takes 88 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1438b_kicad-source-mirror_tinytapeout-demo/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.3 | 5.0 | 16.5 | 0.5&nbsp;ms | 16.1 | 0.8 | 2.2 | 0.4 | 42.2 |
| Simulation, STEP | 1.4 | 5.0 | 16.1 | 2&nbsp;ms | 16.1 | 11.3 | 2.2 | 0.3 | 52.5 |
| Simulation, STL | 1.3 | 4.9 | 15.8 | 0.6&nbsp;ms | 15.6 | 1.6 | 2.0 | 0.3 | 41.6 |
| Simulation, OBJ | 1.3 | 4.7 | 16.1 | 0.5&nbsp;ms | 15.7 | 22.7 | 2.2 | 0.3 | 62.9 |
| Visual, GLB | 1.3 | 4.8 | 16.0 | 1&nbsp;ms | 42.0 | 0.5 | 6.8 | 0.3 | 71.6 |
| Visual, OBJ | 1.5 | 5.0 | 16.3 | 0.8&nbsp;ms | 41.9 | 16.3 | 7.1 | 0.3 | 88.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `tinytapeout-demo.kicad_pcb` |
|---|---|
| Folder | demos / tiny_tapeout |
| Complexity | 415&nbsp;/&nbsp;1000 (size&nbsp;260, features&nbsp;155) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 140, 2,143, 405 |
| Triangles,&nbsp;simulation | 4,352,312 in 127 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">150&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">672&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">218&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">472&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">107&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">340&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1439. video

![video: stages 4 and 6 take 48% to 88% of a run. Simulation, GLB takes 90 s. Simulation, STEP takes 2 min. Simulation, STL takes 91 s. Simulation, OBJ takes 2 min. Visual, GLB takes 3 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1439b_kicad-source-mirror_video/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.6 | 8.0 | 36.2 | 2&nbsp;ms | 36.9 | 1.8 | 5.1 | 0.4 | 90.1 |
| Simulation, STEP | 1.6 | 8.2 | 34.1 | 2&nbsp;ms | 35.9 | 23.5 | 4.7 | 0.4 | 108.3 |
| Simulation, STL | 1.6 | 7.7 | 36.3 | 2&nbsp;ms | 36.6 | 3.9 | 4.9 | 0.4 | 91.5 |
| Simulation, OBJ | 1.6 | 7.7 | 35.0 | 2&nbsp;ms | 36.4 | 62.0 | 4.9 | 0.4 | 148.0 |
| Visual, GLB | 1.6 | 7.9 | 34.5 | 2&nbsp;ms | 114.3 | 0.9 | 9.3 | 0.3 | 168.6 |
| Visual, OBJ | 1.8 | 8.0 | 35.5 | 2&nbsp;ms | 115.3 | 33.2 | 9.3 | 0.3 | 203.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [KiCad/kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)<br>Board: `video.kicad_pcb` |
|---|---|
| Folder | demos / video |
| Complexity | 405&nbsp;/&nbsp;1000 (size&nbsp;300, features&nbsp;105) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 185, 7,932, 808 |
| Triangles,&nbsp;simulation | 10,648,432 in 602 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">352&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.3&nbsp;GB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">532&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.2&nbsp;GB</td><td align="right">6.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">197&nbsp;MB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">660&nbsp;MB</td><td align="right">4.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1440. reform-kintex-edp

![reform-kintex-edp: stages 4 and 6 take 47% to 81% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 15 s. Simulation, STL takes 12 s. Simulation, OBJ takes 18 s. Visual, GLB takes 15 s. Visual, OBJ takes 20 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1440b_reform-kintex-som_reform-kintex-edp/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.3 | 3.7 | 0.8&nbsp;ms | 4.3 | 0.2 | 0.8 | 0.3 | 10.9 |
| Simulation, STEP | 0.4 | 1.3 | 3.8 | 0.4&nbsp;ms | 4.7 | 3.8 | 0.8 | 0.3 | 15.0 |
| Simulation, STL | 0.4 | 1.5 | 3.9 | 0.5&nbsp;ms | 4.5 | 0.4 | 0.7 | 0.2 | 11.7 |
| Simulation, OBJ | 0.4 | 1.3 | 3.9 | 0.9&nbsp;ms | 4.6 | 6.9 | 0.9 | 0.3 | 18.2 |
| Visual, GLB | 0.4 | 1.3 | 3.9 | 0.6&nbsp;ms | 8.5 | 0.1 | 0.9 | 0.3 | 15.4 |
| Visual, OBJ | 0.4 | 1.3 | 3.9 | 0.5&nbsp;ms | 8.8 | 4.7 | 1.0 | 0.3 | 20.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kitspace-forks/reform-kintex-som](https://github.com/kitspace-forks/reform-kintex-som)<br>Board: `reform-kintex-edp.kicad_pcb` |
|---|---|
| Folder | reform-kintex-edp-pcb |
| Complexity | 320&nbsp;/&nbsp;1000 (size&nbsp;245, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 48, 715, 189 |
| Triangles,&nbsp;simulation | 1,185,508 in 100 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">470&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">159&nbsp;MB</td><td align="right">587&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">59&nbsp;MB</td><td align="right">493&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">119&nbsp;MB</td><td align="right">812&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">25&nbsp;MB</td><td align="right">674&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">77&nbsp;MB</td><td align="right">642&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1441. reform-kintex

![reform-kintex: stages 4 and 6 take 43% to 81% of a run. Simulation, GLB takes 92 s. Simulation, STEP takes 2 min. Simulation, STL takes 95 s. Simulation, OBJ takes 3 min. Visual, GLB takes 2 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1441b_reform-kintex-som_reform-kintex/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.7 | 10.8 | 31.0 | 3&nbsp;ms | 38.6 | 2.2 | 6.4 | 0.5 | 92.1 |
| Simulation, STEP | 2.6 | 10.4 | 31.6 | 3&nbsp;ms | 38.4 | 23.8 | 6.0 | 0.4 | 113.3 |
| Simulation, STL | 2.6 | 10.7 | 31.4 | 3&nbsp;ms | 38.4 | 4.9 | 6.6 | 0.4 | 95.0 |
| Simulation, OBJ | 2.6 | 10.5 | 32.1 | 3&nbsp;ms | 39.8 | 73.1 | 7.2 | 0.5 | 165.8 |
| Visual, GLB | 3.0 | 11.4 | 31.9 | 3&nbsp;ms | 79.8 | 0.9 | 10.2 | 0.4 | 137.4 |
| Visual, OBJ | 2.7 | 10.3 | 31.4 | 3&nbsp;ms | 78.1 | 29.0 | 11.2 | 0.4 | 163.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kitspace-forks/reform-kintex-som](https://github.com/kitspace-forks/reform-kintex-som)<br>Board: `reform-kintex.kicad_pcb` |
|---|---|
| Complexity | 407&nbsp;/&nbsp;1000 (size&nbsp;337, features&nbsp;70) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 277, 14,859, 1,145 |
| Triangles,&nbsp;simulation | 10,654,866 in 669 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">361&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.3&nbsp;GB</td><td align="right">3.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">533&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.1&nbsp;GB</td><td align="right">6.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">169&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">563&nbsp;MB</td><td align="right">3.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1442. meko

![meko: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 47 s. Simulation, STEP takes 58 s. Simulation, STL takes 48 s. Simulation, OBJ takes 74 s. Visual, GLB takes 81 s. Visual, OBJ takes 99 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1442b_meko_meko/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 5.1 | 17.0 | 3&nbsp;ms | 20.6 | 1.0 | 2.4 | 0.3 | 47.5 |
| Simulation, STEP | 1.0 | 5.3 | 17.3 | 2&nbsp;ms | 20.3 | 11.7 | 2.3 | 0.4 | 58.3 |
| Simulation, STL | 1.1 | 5.1 | 16.8 | 1&nbsp;ms | 20.4 | 2.3 | 2.2 | 0.4 | 48.3 |
| Simulation, OBJ | 1.1 | 5.3 | 17.0 | 2&nbsp;ms | 20.1 | 27.9 | 2.4 | 0.4 | 74.2 |
| Visual, GLB | 1.1 | 5.3 | 17.6 | 2&nbsp;ms | 49.7 | 0.7 | 6.3 | 0.3 | 81.0 |
| Visual, OBJ | 1.2 | 5.9 | 18.1 | 2&nbsp;ms | 50.0 | 17.4 | 6.2 | 0.3 | 99.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [koeglike/meko](https://github.com/koeglike/meko)<br>Board: `meko.kicad_pcb` |
|---|---|
| Folder | hardware / pcb |
| Complexity | 479&nbsp;/&nbsp;1000 (size&nbsp;309, features&nbsp;170) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 217, 4,129, 1,105 |
| Triangles,&nbsp;simulation | 5,914,532 in 361 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">194&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">736&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">296&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">623&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">128&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">418&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1443. touchpad

![touchpad: stages 4 and 6 take 50% to 77% of a run. Simulation, GLB takes 3.2 s. Simulation, STEP takes 4.7 s. Simulation, STL takes 3.2 s. Simulation, OBJ takes 4.5 s. Visual, GLB takes 4.0 s. Visual, OBJ takes 5.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1443b_meko_touchpad/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 0.8 | 0.2&nbsp;ms | 1.6 | 58&nbsp;ms | 0.1 | 0.2 | 3.2 |
| Simulation, STEP | 0.1 | 0.3 | 0.8 | 0.2&nbsp;ms | 1.7 | 1.5 | 0.1 | 0.2 | 4.7 |
| Simulation, STL | 0.2 | 0.2 | 0.8 | 0.2&nbsp;ms | 1.6 | 91&nbsp;ms | 0.1 | 0.2 | 3.2 |
| Simulation, OBJ | 0.1 | 0.2 | 0.8 | 0.2&nbsp;ms | 1.5 | 1.5 | 0.2 | 0.2 | 4.5 |
| Visual, GLB | 0.1 | 0.2 | 0.8 | 0.2&nbsp;ms | 2.4 | 39&nbsp;ms | 0.2 | 0.2 | 4.0 |
| Visual, OBJ | 0.2 | 0.2 | 0.8 | 0.1&nbsp;ms | 2.4 | 1.4 | 0.3 | 0.2 | 5.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [koeglike/meko](https://github.com/koeglike/meko)<br>Board: `touchpad.kicad_pcb` |
|---|---|
| Folder | hardware / pcb_touchpad |
| Complexity | 232&nbsp;/&nbsp;1000 (size&nbsp;137, features&nbsp;95) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, knockout text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 5, 190, 90 |
| Triangles,&nbsp;simulation | 273,730 in 26 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.3&nbsp;MB</td><td align="right">252&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">43&nbsp;MB</td><td align="right">276&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">255&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">27&nbsp;MB</td><td align="right">253&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.7&nbsp;MB</td><td align="right">277&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">23&nbsp;MB</td><td align="right">276&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1444. H616_devboard

![H616_devboard: stages 4 and 6 take 53% to 81% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 30 s. Simulation, STL takes 23 s. Simulation, OBJ takes 35 s. Visual, GLB takes 34 s. Visual, OBJ takes 42 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1444b_allwinner-h616-devboard_H616-devboard/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.4 | 7.2 | 0.5&nbsp;ms | 10.8 | 0.4 | 1.0 | 0.3 | 22.7 |
| Simulation, STEP | 0.6 | 2.3 | 7.0 | 0.9&nbsp;ms | 12.1 | 6.9 | 1.1 | 0.2 | 30.2 |
| Simulation, STL | 0.7 | 2.3 | 6.9 | 0.5&nbsp;ms | 11.4 | 0.8 | 1.1 | 0.2 | 23.4 |
| Simulation, OBJ | 0.7 | 2.3 | 7.1 | 0.5&nbsp;ms | 11.5 | 12.2 | 1.0 | 0.2 | 35.1 |
| Visual, GLB | 0.7 | 2.3 | 7.1 | 0.8&nbsp;ms | 20.4 | 0.3 | 3.0 | 0.2 | 34.0 |
| Visual, OBJ | 0.7 | 2.2 | 7.3 | 0.5&nbsp;ms | 20.6 | 8.7 | 2.3 | 0.2 | 42.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [kononenko-k/allwinner_h616_devboard](https://github.com/kononenko-k/allwinner_h616_devboard)<br>Board: `H616_devboard.kicad_pcb` |
|---|---|
| Folder | Hardware / H616_DDR3 |
| Complexity | 411&nbsp;/&nbsp;1000 (size&nbsp;286, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 112, 4,034, 406 |
| Triangles,&nbsp;simulation | 2,861,090 in 279 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">97&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">451&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">143&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">300&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">73&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">229&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1445. ovio_core

![ovio_core: stages 4 and 6 take 53% to 83% of a run. Simulation, GLB takes 49 s. Simulation, STEP takes 60 s. Simulation, STL takes 49 s. Simulation, OBJ takes 74 s. Visual, GLB takes 66 s. Visual, OBJ takes 79 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1445b_ovio-core_ovio-core/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 5.0 | 20.7 | 1&nbsp;ms | 19.1 | 1.0 | 2.3 | 0.4 | 49.4 |
| Simulation, STEP | 0.8 | 5.1 | 20.2 | 1.0&nbsp;ms | 19.2 | 11.5 | 2.4 | 0.3 | 59.7 |
| Simulation, STL | 0.9 | 5.1 | 19.6 | 1.0&nbsp;ms | 18.4 | 2.0 | 2.1 | 0.4 | 48.5 |
| Simulation, OBJ | 0.9 | 5.0 | 19.8 | 1&nbsp;ms | 19.1 | 26.4 | 2.2 | 0.3 | 73.7 |
| Visual, GLB | 0.8 | 5.0 | 19.8 | 2&nbsp;ms | 34.7 | 0.4 | 4.6 | 0.3 | 65.7 |
| Visual, OBJ | 0.9 | 5.1 | 19.6 | 2&nbsp;ms | 35.2 | 12.8 | 4.8 | 0.3 | 78.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [korken89/ovio_core](https://github.com/korken89/ovio_core)<br>Board: `ovio_core.kicad_pcb` |
|---|---|
| Complexity | 371&nbsp;/&nbsp;1000 (size&nbsp;306, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 194, 5,830, 552 |
| Triangles,&nbsp;simulation | 5,013,746 in 342 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">173&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">687&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">251&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">535&nbsp;MB</td><td align="right">3.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">89&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">287&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1446. keyb2

![keyb2: stages 4 and 6 take 59% to 82% of a run. Simulation, GLB takes 10 s. Simulation, STEP takes 14 s. Simulation, STL takes 10 s. Simulation, OBJ takes 14 s. Visual, GLB takes 13 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1446b_ZX-Spectrum-diy_keyb2/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.8 | 3.4 | 0.3&nbsp;ms | 5.1 | 0.1 | 0.5 | 0.2 | 10.5 |
| Simulation, STEP | 0.3 | 0.8 | 3.1 | 0.2&nbsp;ms | 5.2 | 3.7 | 0.5 | 0.2 | 13.8 |
| Simulation, STL | 0.3 | 0.7 | 3.2 | 0.1&nbsp;ms | 5.0 | 0.2 | 0.5 | 0.2 | 10.0 |
| Simulation, OBJ | 0.3 | 0.7 | 3.2 | 0.2&nbsp;ms | 5.3 | 4.2 | 0.5 | 0.2 | 14.3 |
| Visual, GLB | 0.3 | 0.8 | 3.3 | 0.1&nbsp;ms | 6.6 | 0.1 | 1.1 | 0.3 | 12.5 |
| Visual, OBJ | 0.3 | 0.7 | 3.2 | 0.1&nbsp;ms | 6.5 | 3.9 | 1.1 | 0.2 | 15.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `keyb2.kicad_pcb` |
|---|---|
| Folder | Kicad4 / keyb2 |
| Complexity | 218&nbsp;/&nbsp;1000 (size&nbsp;173, features&nbsp;45) |
| KESE&nbsp;features | through vias, filled zones,<br>copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 59, 667, 94 |
| Triangles,&nbsp;simulation | 676,712 in 30 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">24&nbsp;MB</td><td align="right">420&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">135&nbsp;MB</td><td align="right">476&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">34&nbsp;MB</td><td align="right">430&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">70&nbsp;MB</td><td align="right">466&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">21&nbsp;MB</td><td align="right">519&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">64&nbsp;MB</td><td align="right">555&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1447. keyb2_nofill

![keyb2_nofill: stages 4 and 6 take 58% to 79% of a run. Simulation, GLB takes 5.3 s. Simulation, STEP takes 7.0 s. Simulation, STL takes 5.2 s. Simulation, OBJ takes 7.4 s. Visual, GLB takes 6.4 s. Visual, OBJ takes 8.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1447b_ZX-Spectrum-diy_keyb2-nofill/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.7 | 0.2&nbsp;ms | 2.4 | 60&nbsp;ms | 0.2 | 0.3 | 5.3 |
| Simulation, STEP | 0.2 | 0.4 | 1.6 | 0.4&nbsp;ms | 2.5 | 1.9 | 0.2 | 0.2 | 7.0 |
| Simulation, STL | 0.2 | 0.5 | 1.7 | 0.2&nbsp;ms | 2.2 | 0.1 | 0.2 | 0.2 | 5.2 |
| Simulation, OBJ | 0.2 | 0.5 | 1.8 | 0.4&nbsp;ms | 2.6 | 1.9 | 0.2 | 0.3 | 7.4 |
| Visual, GLB | 0.3 | 0.4 | 1.6 | 0.5&nbsp;ms | 3.5 | 51&nbsp;ms | 0.4 | 0.2 | 6.4 |
| Visual, OBJ | 0.2 | 0.5 | 1.8 | 0.5&nbsp;ms | 3.8 | 1.9 | 0.4 | 0.3 | 8.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `keyb2_nofill.kicad_pcb` |
|---|---|
| Folder | Kicad4 / keyb2 |
| Complexity | 172&nbsp;/&nbsp;1000 (size&nbsp;162, features&nbsp;10) |
| KESE&nbsp;features | copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 59, 480, 0 |
| Triangles,&nbsp;simulation | 303,980 in 30 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">296&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">62&nbsp;MB</td><td align="right">319&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">15&nbsp;MB</td><td align="right">293&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">33&nbsp;MB</td><td align="right">294&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">10&nbsp;MB</td><td align="right">312&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">30&nbsp;MB</td><td align="right">349&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1448. z2_io

![z2_io: stages 4 and 6 take 53% to 86% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 21 s. Simulation, STL takes 16 s. Simulation, OBJ takes 25 s. Visual, GLB takes 23 s. Visual, OBJ takes 29 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1448b_ZX-Spectrum-diy_z2-io/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.3 | 6.6 | 0.6&nbsp;ms | 6.7 | 0.3 | 0.8 | 0.2 | 16.2 |
| Simulation, STEP | 0.4 | 1.3 | 6.6 | 0.5&nbsp;ms | 6.8 | 5.3 | 0.7 | 0.3 | 21.3 |
| Simulation, STL | 0.3 | 1.3 | 6.5 | 0.6&nbsp;ms | 6.4 | 0.4 | 0.8 | 0.3 | 16.1 |
| Simulation, OBJ | 0.4 | 1.3 | 6.6 | 0.5&nbsp;ms | 6.7 | 9.2 | 0.9 | 0.3 | 25.4 |
| Visual, GLB | 0.3 | 1.4 | 6.5 | 0.5&nbsp;ms | 12.9 | 0.2 | 1.1 | 0.2 | 22.7 |
| Visual, OBJ | 0.4 | 1.4 | 6.4 | 0.4&nbsp;ms | 12.6 | 6.2 | 1.6 | 0.3 | 28.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `z2_io.kicad_pcb` |
|---|---|
| Folder | Kicad5 / z2_io |
| Complexity | 221&nbsp;/&nbsp;1000 (size&nbsp;186, features&nbsp;35) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 65, 1,620, 97 |
| Triangles,&nbsp;simulation | 1,643,896 in 104 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">54&nbsp;MB</td><td align="right">582&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">240&nbsp;MB</td><td align="right">732&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">82&nbsp;MB</td><td align="right">579&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">168&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">38&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">114&nbsp;MB</td><td align="right">828&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1449. z2_io_test01

![z2_io_test01: stages 4 and 6 take 52% to 85% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 20 s. Simulation, STL takes 17 s. Simulation, OBJ takes 26 s. Visual, GLB takes 24 s. Visual, OBJ takes 30 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1449b_ZX-Spectrum-diy_z2-io-test01/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.5 | 7.1 | 0.7&nbsp;ms | 6.0 | 0.3 | 0.8 | 0.3 | 16.3 |
| Simulation, STEP | 0.3 | 1.5 | 7.1 | 0.8&nbsp;ms | 5.8 | 4.7 | 0.8 | 0.2 | 20.4 |
| Simulation, STL | 0.3 | 1.5 | 7.2 | 0.5&nbsp;ms | 5.9 | 0.7 | 0.8 | 0.2 | 16.6 |
| Simulation, OBJ | 0.3 | 1.5 | 7.7 | 1&nbsp;ms | 6.1 | 9.6 | 0.9 | 0.2 | 26.3 |
| Visual, GLB | 0.3 | 1.5 | 7.2 | 0.5&nbsp;ms | 13.0 | 0.2 | 1.3 | 0.2 | 23.7 |
| Visual, OBJ | 0.3 | 1.5 | 6.9 | 0.4&nbsp;ms | 12.7 | 6.3 | 1.8 | 0.2 | 29.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `z2_io_test01.kicad_pcb` |
|---|---|
| Folder | Kicad5 / z2_io |
| Complexity | 209&nbsp;/&nbsp;1000 (size&nbsp;184, features&nbsp;25) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 67, 1,203, 138 |
| Triangles,&nbsp;simulation | 1,836,454 in 107 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">63&nbsp;MB</td><td align="right">742&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">302&nbsp;MB</td><td align="right">823&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">92&nbsp;MB</td><td align="right">812&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">192&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">921&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">120&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1450. z2_io_test02

![z2_io_test02: stages 4 and 6 take 55% to 84% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 15 s. Simulation, STL takes 13 s. Simulation, OBJ takes 18 s. Visual, GLB takes 18 s. Visual, OBJ takes 22 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1450b_ZX-Spectrum-diy_z2-io-test02/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 1.0 | 4.8 | 0.6&nbsp;ms | 4.9 | 0.2 | 0.6 | 0.3 | 12.1 |
| Simulation, STEP | 0.2 | 1.0 | 4.9 | 0.4&nbsp;ms | 4.9 | 3.7 | 0.6 | 0.2 | 15.5 |
| Simulation, STL | 0.2 | 1.0 | 4.9 | 0.7&nbsp;ms | 5.3 | 0.4 | 0.6 | 0.2 | 12.7 |
| Simulation, OBJ | 0.2 | 1.1 | 5.0 | 0.5&nbsp;ms | 5.0 | 5.9 | 0.6 | 0.2 | 18.1 |
| Visual, GLB | 0.2 | 1.0 | 4.8 | 0.4&nbsp;ms | 10.1 | 0.1 | 1.4 | 0.2 | 17.7 |
| Visual, OBJ | 0.2 | 0.9 | 4.8 | 0.4&nbsp;ms | 9.6 | 4.5 | 1.6 | 0.2 | 22.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `z2_io_test02.kicad_pcb` |
|---|---|
| Folder | Kicad5 / z2_io |
| Complexity | 214&nbsp;/&nbsp;1000 (size&nbsp;179, features&nbsp;35) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 65, 1,038, 82 |
| Triangles,&nbsp;simulation | 1,564,634 in 104 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">52&nbsp;MB</td><td align="right">602&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">223&nbsp;MB</td><td align="right">728&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">78&nbsp;MB</td><td align="right">585&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">159&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">35&nbsp;MB</td><td align="right">722&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">106&nbsp;MB</td><td align="right">768&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1451. zx2_backplane

![zx2_backplane: stages 4 and 6 take 55% to 86% of a run. Simulation, GLB takes 15 s. Simulation, STEP takes 22 s. Simulation, STL takes 17 s. Simulation, OBJ takes 25 s. Visual, GLB takes 22 s. Visual, OBJ takes 28 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1451b_ZX-Spectrum-diy_zx2-backplane/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 1.1 | 6.6 | 0.3&nbsp;ms | 5.7 | 0.3 | 0.6 | 0.2 | 14.7 |
| Simulation, STEP | 0.2 | 1.2 | 7.3 | 0.5&nbsp;ms | 6.4 | 5.5 | 0.8 | 0.2 | 21.5 |
| Simulation, STL | 0.3 | 1.2 | 7.6 | 0.3&nbsp;ms | 6.4 | 0.6 | 0.7 | 0.3 | 17.1 |
| Simulation, OBJ | 0.3 | 1.3 | 7.4 | 0.4&nbsp;ms | 6.6 | 8.8 | 0.6 | 0.3 | 25.2 |
| Visual, GLB | 0.2 | 1.2 | 6.7 | 0.9&nbsp;ms | 12.6 | 0.2 | 1.2 | 0.3 | 22.3 |
| Visual, OBJ | 0.2 | 1.0 | 6.8 | 0.6&nbsp;ms | 12.3 | 6.4 | 1.5 | 0.2 | 28.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_backplane.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_backplane |
| Complexity | 187&nbsp;/&nbsp;1000 (size&nbsp;147, features&nbsp;40) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 12, 532, 0 |
| Triangles,&nbsp;simulation | 1,561,198 in 55 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">51&nbsp;MB</td><td align="right">571&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">226&nbsp;MB</td><td align="right">727&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">78&nbsp;MB</td><td align="right">593&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">161&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">955&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">98&nbsp;MB</td><td align="right">787&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1452. zx2_clock

![zx2_clock: stages 4 and 6 take 48% to 84% of a run. Simulation, GLB takes 4.4 s. Simulation, STEP takes 5.9 s. Simulation, STL takes 4.4 s. Simulation, OBJ takes 7.0 s. Visual, GLB takes 6.6 s. Visual, OBJ takes 8.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1452b_ZX-Spectrum-diy_zx2-clock/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.5 | 0.2&nbsp;ms | 1.9 | 70&nbsp;ms | 0.3 | 0.2 | 4.4 |
| Simulation, STEP | 0.1 | 0.3 | 1.5 | 0.2&nbsp;ms | 1.8 | 1.6 | 0.3 | 0.2 | 5.9 |
| Simulation, STL | 0.1 | 0.3 | 1.5 | 0.6&nbsp;ms | 1.9 | 0.1 | 0.3 | 0.2 | 4.4 |
| Simulation, OBJ | 0.1 | 0.3 | 1.5 | 0.2&nbsp;ms | 1.8 | 2.7 | 0.3 | 0.2 | 7.0 |
| Visual, GLB | 0.1 | 0.3 | 1.5 | 0.2&nbsp;ms | 4.0 | 53&nbsp;ms | 0.4 | 0.2 | 6.6 |
| Visual, OBJ | 0.1 | 0.3 | 1.5 | 0.2&nbsp;ms | 4.1 | 2.0 | 0.6 | 0.2 | 8.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_clock.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_clock |
| Complexity | 198&nbsp;/&nbsp;1000 (size&nbsp;143, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 24, 221, 12 |
| Triangles,&nbsp;simulation | 552,368 in 32 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">317&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">84&nbsp;MB</td><td align="right">371&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">28&nbsp;MB</td><td align="right">313&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">55&nbsp;MB</td><td align="right">411&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">399&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">40&nbsp;MB</td><td align="right">390&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1453. zx2_clock_test01

![zx2_clock_test01: stages 4 and 6 take 51% to 81% of a run. Simulation, GLB takes 3.6 s. Simulation, STEP takes 4.6 s. Simulation, STL takes 3.6 s. Simulation, OBJ takes 5.4 s. Visual, GLB takes 4.8 s. Visual, OBJ takes 5.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1453b_ZX-Spectrum-diy_zx2-clock-test01/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.4 | 0.2&nbsp;ms | 1.3 | 58&nbsp;ms | 0.2 | 0.2 | 3.6 |
| Simulation, STEP | 0.1 | 0.3 | 1.4 | 0.2&nbsp;ms | 1.2 | 1.2 | 0.2 | 0.2 | 4.6 |
| Simulation, STL | 0.1 | 0.3 | 1.4 | 0.2&nbsp;ms | 1.2 | 84&nbsp;ms | 0.2 | 0.2 | 3.6 |
| Simulation, OBJ | 0.1 | 0.3 | 1.5 | 0.3&nbsp;ms | 1.3 | 1.9 | 0.2 | 0.2 | 5.4 |
| Visual, GLB | 0.1 | 0.3 | 1.5 | 0.2&nbsp;ms | 2.4 | 32&nbsp;ms | 0.3 | 0.2 | 4.8 |
| Visual, OBJ | 0.1 | 0.3 | 1.4 | 0.3&nbsp;ms | 2.4 | 1.1 | 0.3 | 0.2 | 5.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_clock_test01.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_clock |
| Complexity | 163&nbsp;/&nbsp;1000 (size&nbsp;138, features&nbsp;25) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 21, 191, 5 |
| Triangles,&nbsp;simulation | 380,468 in 31 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">248&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">49&nbsp;MB</td><td align="right">288&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">19&nbsp;MB</td><td align="right">243&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">37&nbsp;MB</td><td align="right">279&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.6&nbsp;MB</td><td align="right">276&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">278&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1454. zx2_cpu

![zx2_cpu: stages 4 and 6 take 54% to 85% of a run. Simulation, GLB takes 9.8 s. Simulation, STEP takes 13 s. Simulation, STL takes 10 s. Simulation, OBJ takes 15 s. Visual, GLB takes 15 s. Visual, OBJ takes 18 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1454b_ZX-Spectrum-diy_zx2-cpu/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.7 | 3.8 | 0.7&nbsp;ms | 4.1 | 0.2 | 0.5 | 0.2 | 9.8 |
| Simulation, STEP | 0.2 | 0.8 | 3.9 | 0.6&nbsp;ms | 4.3 | 3.0 | 0.6 | 0.3 | 13.0 |
| Simulation, STL | 0.2 | 0.7 | 3.8 | 1&nbsp;ms | 4.4 | 0.3 | 0.6 | 0.3 | 10.3 |
| Simulation, OBJ | 0.2 | 0.7 | 3.9 | 0.7&nbsp;ms | 4.1 | 5.1 | 0.5 | 0.2 | 14.7 |
| Visual, GLB | 0.2 | 0.7 | 3.9 | 0.6&nbsp;ms | 8.5 | 0.1 | 1.0 | 0.2 | 14.6 |
| Visual, OBJ | 0.2 | 0.8 | 3.8 | 0.6&nbsp;ms | 8.3 | 3.4 | 1.1 | 0.2 | 17.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_cpu.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_cpu |
| Complexity | 213&nbsp;/&nbsp;1000 (size&nbsp;158, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 18, 716, 32 |
| Triangles,&nbsp;simulation | 1,132,234 in 83 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">37&nbsp;MB</td><td align="right">481&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">164&nbsp;MB</td><td align="right">580&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">57&nbsp;MB</td><td align="right">470&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">113&nbsp;MB</td><td align="right">762&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">684&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">80&nbsp;MB</td><td align="right">657&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1455. zx2_cpu_test01

![zx2_cpu_test01: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 9.1 s. Simulation, STEP takes 11 s. Simulation, STL takes 9.5 s. Simulation, OBJ takes 14 s. Visual, GLB takes 13 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1455b_ZX-Spectrum-diy_zx2-cpu-test01/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.8 | 4.0 | 0.6&nbsp;ms | 3.3 | 0.2 | 0.5 | 0.2 | 9.1 |
| Simulation, STEP | 0.2 | 0.8 | 3.8 | 0.6&nbsp;ms | 3.2 | 2.7 | 0.5 | 0.2 | 11.4 |
| Simulation, STL | 0.2 | 0.8 | 4.2 | 0.6&nbsp;ms | 3.3 | 0.2 | 0.5 | 0.2 | 9.5 |
| Simulation, OBJ | 0.2 | 0.8 | 4.0 | 0.5&nbsp;ms | 3.3 | 5.1 | 0.5 | 0.2 | 14.0 |
| Visual, GLB | 0.2 | 0.8 | 4.2 | 0.9&nbsp;ms | 6.9 | 81&nbsp;ms | 0.7 | 0.3 | 13.1 |
| Visual, OBJ | 0.2 | 0.8 | 4.0 | 0.5&nbsp;ms | 7.0 | 3.0 | 0.8 | 0.3 | 16.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_cpu_test01.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_cpu |
| Complexity | 190&nbsp;/&nbsp;1000 (size&nbsp;155, features&nbsp;35) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 18, 493, 51 |
| Triangles,&nbsp;simulation | 980,980 in 83 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">33&nbsp;MB</td><td align="right">460&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">162&nbsp;MB</td><td align="right">513&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">49&nbsp;MB</td><td align="right">479&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">100&nbsp;MB</td><td align="right">701&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">492&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">60&nbsp;MB</td><td align="right">557&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1456. zx2_fpga_int

![zx2_fpga_int: stages 4 and 6 take 51% to 82% of a run. Simulation, GLB takes 5.2 s. Simulation, STEP takes 6.8 s. Simulation, STL takes 5.0 s. Simulation, OBJ takes 7.8 s. Visual, GLB takes 7.2 s. Visual, OBJ takes 9.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1456b_ZX-Spectrum-diy_zx2-fpga-int/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.6 | 0.4&nbsp;ms | 2.5 | 75&nbsp;ms | 0.3 | 0.2 | 5.2 |
| Simulation, STEP | 0.2 | 0.4 | 1.5 | 0.2&nbsp;ms | 2.4 | 1.9 | 0.3 | 0.2 | 6.8 |
| Simulation, STL | 0.2 | 0.4 | 1.6 | 0.3&nbsp;ms | 2.3 | 0.1 | 0.4 | 0.2 | 5.0 |
| Simulation, OBJ | 0.2 | 0.4 | 1.6 | 0.3&nbsp;ms | 2.4 | 2.7 | 0.3 | 0.2 | 7.8 |
| Visual, GLB | 0.2 | 0.4 | 1.5 | 0.3&nbsp;ms | 4.4 | 66&nbsp;ms | 0.4 | 0.2 | 7.2 |
| Visual, OBJ | 0.2 | 0.4 | 1.6 | 0.3&nbsp;ms | 4.4 | 2.2 | 0.5 | 0.3 | 9.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_fpga_int.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_fpga_int |
| Complexity | 209&nbsp;/&nbsp;1000 (size&nbsp;154, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 13, 618, 54 |
| Triangles,&nbsp;simulation | 547,074 in 56 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">332&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">87&nbsp;MB</td><td align="right">387&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">27&nbsp;MB</td><td align="right">332&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">55&nbsp;MB</td><td align="right">413&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">447&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">44&nbsp;MB</td><td align="right">447&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1457. zx2_keyb_conn

![zx2_keyb_conn: stages 4 and 6 take 50% to 82% of a run. Simulation, GLB takes 4.8 s. Simulation, STEP takes 6.0 s. Simulation, STL takes 4.5 s. Simulation, OBJ takes 6.7 s. Visual, GLB takes 6.0 s. Visual, OBJ takes 8.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1457b_ZX-Spectrum-diy_zx2-keyb-conn/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.3 | 1.5 | 0.7&nbsp;ms | 2.1 | 93&nbsp;ms | 0.3 | 0.2 | 4.8 |
| Simulation, STEP | 0.2 | 0.3 | 1.5 | 0.2&nbsp;ms | 1.8 | 1.7 | 0.3 | 0.3 | 6.0 |
| Simulation, STL | 0.2 | 0.3 | 1.5 | 0.2&nbsp;ms | 1.9 | 0.1 | 0.3 | 0.2 | 4.5 |
| Simulation, OBJ | 0.2 | 0.3 | 1.4 | 0.2&nbsp;ms | 2.0 | 2.4 | 0.3 | 0.2 | 6.7 |
| Visual, GLB | 0.2 | 0.3 | 1.4 | 0.2&nbsp;ms | 3.5 | 51&nbsp;ms | 0.3 | 0.2 | 6.0 |
| Visual, OBJ | 0.2 | 0.3 | 1.4 | 0.3&nbsp;ms | 3.6 | 1.9 | 0.4 | 0.2 | 8.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_keyb_conn.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_keyb_conn |
| Complexity | 200&nbsp;/&nbsp;1000 (size&nbsp;145, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 10, 474, 12 |
| Triangles,&nbsp;simulation | 440,002 in 47 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">308&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">68&nbsp;MB</td><td align="right">332&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">22&nbsp;MB</td><td align="right">293&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">44&nbsp;MB</td><td align="right">345&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">351&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">32&nbsp;MB</td><td align="right">349&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1458. zx2_keyb_idc

![zx2_keyb_idc: stages 4 and 6 take 48% to 76% of a run. Simulation, GLB takes 1.7 s. Simulation, STEP takes 2.5 s. Simulation, STL takes 1.7 s. Simulation, OBJ takes 2.3 s. Visual, GLB takes 2.0 s. Visual, OBJ takes 2.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1458b_ZX-Spectrum-diy_zx2-keyb-idc/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 78&nbsp;ms | 92&nbsp;ms | 0.5 | 0.1&nbsp;ms | 0.7 | 20&nbsp;ms | 74&nbsp;ms | 0.2 | 1.7 |
| Simulation, STEP | 80&nbsp;ms | 88&nbsp;ms | 0.5 | 0.1&nbsp;ms | 0.7 | 0.9 | 73&nbsp;ms | 0.2 | 2.5 |
| Simulation, STL | 81&nbsp;ms | 94&nbsp;ms | 0.5 | 0.1&nbsp;ms | 0.8 | 41&nbsp;ms | 84&nbsp;ms | 0.2 | 1.7 |
| Simulation, OBJ | 88&nbsp;ms | 89&nbsp;ms | 0.5 | 0.2&nbsp;ms | 0.7 | 0.7 | 92&nbsp;ms | 0.2 | 2.3 |
| Visual, GLB | 80&nbsp;ms | 0.1 | 0.5 | 0.2&nbsp;ms | 1.1 | 13&nbsp;ms | 78&nbsp;ms | 0.2 | 2.0 |
| Visual, OBJ | 78&nbsp;ms | 87&nbsp;ms | 0.5 | 0.1&nbsp;ms | 1.2 | 0.4 | 93&nbsp;ms | 0.2 | 2.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_keyb_idc.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_keyb_idc |
| Complexity | 141&nbsp;/&nbsp;1000 (size&nbsp;111, features&nbsp;30) |
| KESE&nbsp;features | filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 4, 108, 0 |
| Triangles,&nbsp;simulation | 124,032 in 26 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.1&nbsp;MB</td><td align="right">189&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">19&nbsp;MB</td><td align="right">197&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">6.2&nbsp;MB</td><td align="right">189&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">12&nbsp;MB</td><td align="right">189&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">2.8&nbsp;MB</td><td align="right">154&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">8.0&nbsp;MB</td><td align="right">153&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1459. zx2_mem

![zx2_mem: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 9.3 s. Simulation, STEP takes 13 s. Simulation, STL takes 9.2 s. Simulation, OBJ takes 14 s. Visual, GLB takes 12 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1459b_ZX-Spectrum-diy_zx2-mem/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.8 | 4.1 | 0.5&nbsp;ms | 3.3 | 0.2 | 0.5 | 0.3 | 9.3 |
| Simulation, STEP | 0.2 | 1.0 | 3.9 | 0.7&nbsp;ms | 3.8 | 2.9 | 0.5 | 0.4 | 12.7 |
| Simulation, STL | 0.2 | 0.7 | 3.8 | 0.4&nbsp;ms | 3.5 | 0.2 | 0.5 | 0.2 | 9.2 |
| Simulation, OBJ | 0.2 | 0.7 | 3.8 | 0.8&nbsp;ms | 3.6 | 5.1 | 0.5 | 0.2 | 14.1 |
| Visual, GLB | 0.2 | 0.6 | 3.8 | 0.9&nbsp;ms | 6.7 | 82&nbsp;ms | 0.9 | 0.2 | 12.5 |
| Visual, OBJ | 0.2 | 0.7 | 3.7 | 0.5&nbsp;ms | 6.6 | 3.3 | 0.9 | 0.2 | 15.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_mem.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_mem |
| Complexity | 195&nbsp;/&nbsp;1000 (size&nbsp;160, features&nbsp;35) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 20, 687, 43 |
| Triangles,&nbsp;simulation | 932,552 in 57 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">447&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">129&nbsp;MB</td><td align="right">504&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">47&nbsp;MB</td><td align="right">441&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">93&nbsp;MB</td><td align="right">656&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">589&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">60&nbsp;MB</td><td align="right">548&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1460. zx2_mem_test01

![zx2_mem_test01: stages 4 and 6 take 51% to 83% of a run. Simulation, GLB takes 7.6 s. Simulation, STEP takes 9.8 s. Simulation, STL takes 7.8 s. Simulation, OBJ takes 12 s. Visual, GLB takes 9.5 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1460b_ZX-Spectrum-diy_zx2-mem-test01/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 3.4 | 0.6&nbsp;ms | 2.7 | 0.1 | 0.4 | 0.2 | 7.6 |
| Simulation, STEP | 0.2 | 0.7 | 3.2 | 0.6&nbsp;ms | 2.8 | 2.3 | 0.4 | 0.2 | 9.8 |
| Simulation, STL | 0.2 | 0.6 | 3.2 | 0.4&nbsp;ms | 2.8 | 0.2 | 0.4 | 0.2 | 7.8 |
| Simulation, OBJ | 0.2 | 0.7 | 3.4 | 0.5&nbsp;ms | 2.8 | 4.4 | 0.4 | 0.2 | 12.0 |
| Visual, GLB | 0.2 | 0.7 | 3.3 | 0.5&nbsp;ms | 4.6 | 65&nbsp;ms | 0.5 | 0.2 | 9.5 |
| Visual, OBJ | 0.2 | 0.7 | 3.3 | 0.6&nbsp;ms | 4.8 | 2.4 | 0.5 | 0.2 | 12.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_mem_test01.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_mem |
| Complexity | 176&nbsp;/&nbsp;1000 (size&nbsp;151, features&nbsp;25) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 18, 414, 29 |
| Triangles,&nbsp;simulation | 777,604 in 56 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">376&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">110&nbsp;MB</td><td align="right">440&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">39&nbsp;MB</td><td align="right">378&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">79&nbsp;MB</td><td align="right">555&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">423&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">43&nbsp;MB</td><td align="right">429&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1461. zx2_uart

![zx2_uart: stages 4 and 6 take 50% to 78% of a run. Simulation, GLB takes 1.8 s. Simulation, STEP takes 2.7 s. Simulation, STL takes 1.8 s. Simulation, OBJ takes 2.4 s. Visual, GLB takes 2.3 s. Visual, OBJ takes 2.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1461b_ZX-Spectrum-diy_zx2-uart/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 93&nbsp;ms | 0.1 | 0.5 | 0.1&nbsp;ms | 0.8 | 29&nbsp;ms | 72&nbsp;ms | 0.2 | 1.8 |
| Simulation, STEP | 93&nbsp;ms | 0.1 | 0.6 | 0.1&nbsp;ms | 0.8 | 0.9 | 67&nbsp;ms | 0.2 | 2.7 |
| Simulation, STL | 0.1 | 0.1 | 0.5 | 0.1&nbsp;ms | 0.8 | 34&nbsp;ms | 75&nbsp;ms | 0.2 | 1.8 |
| Simulation, OBJ | 97&nbsp;ms | 0.1 | 0.5 | 0.1&nbsp;ms | 0.8 | 0.6 | 72&nbsp;ms | 0.2 | 2.4 |
| Visual, GLB | 93&nbsp;ms | 0.1 | 0.5 | 0.1&nbsp;ms | 1.4 | 17&nbsp;ms | 0.1 | 0.2 | 2.3 |
| Visual, OBJ | 94&nbsp;ms | 0.1 | 0.5 | 0.1&nbsp;ms | 1.3 | 0.5 | 0.1 | 0.2 | 2.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [krzys9876/ZX_Spectrum_diy](https://github.com/krzys9876/ZX_Spectrum_diy)<br>Board: `zx2_uart.kicad_pcb` |
|---|---|
| Folder | Kicad5 / zx2_uart |
| Complexity | 176&nbsp;/&nbsp;1000 (size&nbsp;131, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 15, 152, 7 |
| Triangles,&nbsp;simulation | 131,734 in 27 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.5&nbsp;MB</td><td align="right">199&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">22&nbsp;MB</td><td align="right">212&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">6.6&nbsp;MB</td><td align="right">199&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">13&nbsp;MB</td><td align="right">200&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.7&nbsp;MB</td><td align="right">180&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">10&nbsp;MB</td><td align="right">181&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1462. rpi-cm4-LiM+-board

![rpi-cm4-LiM+-board: stages 4 and 6 take 54% to 83% of a run. Simulation, GLB takes 4.4 s. Simulation, STEP takes 6.0 s. Simulation, STL takes 4.4 s. Simulation, OBJ takes 6.0 s. Visual, GLB takes 6.8 s. Visual, OBJ takes 8.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1462b_rpi-cm4-LiM-board_hardware-rpi-cm4-LiM-board-KiCad-Files_rpi-cm4-LiM-board_2262/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.6 | 0.7&nbsp;ms | 1.7 | 87&nbsp;ms | 0.2 | 0.3 | 4.4 |
| Simulation, STEP | 0.2 | 0.3 | 1.5 | 0.4&nbsp;ms | 1.7 | 1.7 | 0.2 | 0.2 | 6.0 |
| Simulation, STL | 0.2 | 0.4 | 1.6 | 0.5&nbsp;ms | 1.7 | 0.1 | 0.2 | 0.2 | 4.4 |
| Simulation, OBJ | 0.2 | 0.4 | 1.6 | 0.4&nbsp;ms | 1.8 | 1.6 | 0.2 | 0.2 | 6.0 |
| Visual, GLB | 0.2 | 0.4 | 1.5 | 0.6&nbsp;ms | 4.1 | 56&nbsp;ms | 0.3 | 0.3 | 6.8 |
| Visual, OBJ | 0.2 | 0.4 | 1.6 | 0.4&nbsp;ms | 4.0 | 1.5 | 0.3 | 0.2 | 8.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [l00nix/rpi-cm4-LiM-board](https://github.com/l00nix/rpi-cm4-LiM-board)<br>Board: `rpi-cm4-LiM+-board.kicad_pcb` |
|---|---|
| Folder | hardware / rpi-cm4-LiM+-board / KiCad Files |
| Complexity | 268&nbsp;/&nbsp;1000 (size&nbsp;143, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20210424) |
| Parts,&nbsp;tracks,&nbsp;vias | 12, 284, 45 |
| Triangles,&nbsp;simulation | 273,312 in 161 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.9&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">60&nbsp;MB</td><td align="right">288&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">265&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">28&nbsp;MB</td><td align="right">264&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.9&nbsp;MB</td><td align="right">310&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">26&nbsp;MB</td><td align="right">308&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1463. rpi-cm4-LiM-board

![rpi-cm4-LiM-board: stages 4 and 6 take 53% to 83% of a run. Simulation, GLB takes 3.8 s. Simulation, STEP takes 5.2 s. Simulation, STL takes 3.7 s. Simulation, OBJ takes 4.8 s. Visual, GLB takes 5.8 s. Visual, OBJ takes 7.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1463b_rpi-cm4-LiM-board_hardware-rpi-cm4-LiM-board-KiCad-Files_rpi-cm4-LiM-board_2462/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.3 | 1.2 | 0.4&nbsp;ms | 1.6 | 56&nbsp;ms | 0.2 | 0.2 | 3.8 |
| Simulation, STEP | 0.2 | 0.3 | 1.2 | 0.4&nbsp;ms | 1.6 | 1.6 | 0.2 | 0.2 | 5.2 |
| Simulation, STL | 0.2 | 0.3 | 1.2 | 0.4&nbsp;ms | 1.6 | 84&nbsp;ms | 0.2 | 0.2 | 3.7 |
| Simulation, OBJ | 0.2 | 0.3 | 1.3 | 0.4&nbsp;ms | 1.6 | 1.1 | 0.2 | 0.2 | 4.8 |
| Visual, GLB | 0.2 | 0.3 | 1.3 | 0.4&nbsp;ms | 3.6 | 43&nbsp;ms | 0.3 | 0.2 | 5.8 |
| Visual, OBJ | 0.2 | 0.3 | 1.3 | 0.4&nbsp;ms | 3.8 | 1.1 | 0.3 | 0.2 | 7.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [l00nix/rpi-cm4-LiM-board](https://github.com/l00nix/rpi-cm4-LiM-board)<br>Board: `rpi-cm4-LiM-board.kicad_pcb` |
|---|---|
| Folder | hardware / rpi-cm4-LiM-board / KiCad Files |
| Complexity | 260&nbsp;/&nbsp;1000 (size&nbsp;135, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20210424) |
| Parts,&nbsp;tracks,&nbsp;vias | 11, 147, 36 |
| Triangles,&nbsp;simulation | 258,546 in 165 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.4&nbsp;MB</td><td align="right">270&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">60&nbsp;MB</td><td align="right">285&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">13&nbsp;MB</td><td align="right">266&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">27&nbsp;MB</td><td align="right">265&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.3&nbsp;MB</td><td align="right">289&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">24&nbsp;MB</td><td align="right">287&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1464. LHCbit

![LHCbit: stages 4 and 6 take 50% to 79% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 18 s. Simulation, STL takes 16 s. Simulation, OBJ takes 23 s. Visual, GLB takes 22 s. Visual, OBJ takes 27 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1464b_hardware_LHCbit/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 2.8 | 6.3 | 0.8&nbsp;ms | 5.0 | 0.2 | 0.7 | 0.3 | 15.7 |
| Simulation, STEP | 0.4 | 2.6 | 6.5 | 0.7&nbsp;ms | 4.9 | 3.1 | 0.6 | 0.2 | 18.2 |
| Simulation, STL | 0.4 | 3.1 | 6.2 | 1&nbsp;ms | 5.2 | 0.4 | 0.6 | 0.3 | 16.1 |
| Simulation, OBJ | 0.4 | 2.9 | 6.4 | 0.7&nbsp;ms | 4.9 | 6.9 | 0.6 | 0.3 | 22.5 |
| Visual, GLB | 0.4 | 2.8 | 6.4 | 0.7&nbsp;ms | 11.1 | 0.1 | 1.1 | 0.2 | 22.1 |
| Visual, OBJ | 0.3 | 2.9 | 6.3 | 0.9&nbsp;ms | 11.3 | 4.1 | 1.3 | 0.2 | 26.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lhc/hardware](https://github.com/lhc/hardware)<br>Board: `LHCbit.kicad_pcb` |
|---|---|
| Folder | LHCbit / kicad |
| Complexity | 402&nbsp;/&nbsp;1000 (size&nbsp;197, features&nbsp;205) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours,<br>castellated pads,<br>plated board edge |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 51, 743, 295 |
| Triangles,&nbsp;simulation | 1,407,910 in 124 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">48&nbsp;MB</td><td align="right">578&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">180&nbsp;MB</td><td align="right">681&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">70&nbsp;MB</td><td align="right">607&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">147&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">667&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">91&nbsp;MB</td><td align="right">721&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1465. lhc_tijolo32_board

![lhc_tijolo32_board: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 8.9 s. Simulation, STEP takes 12 s. Simulation, STL takes 8.8 s. Simulation, OBJ takes 14 s. Visual, GLB takes 13 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1465b_hardware_lhc-tijolo32-board/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.7 | 3.3 | 0.5&nbsp;ms | 3.8 | 0.2 | 0.4 | 0.2 | 8.9 |
| Simulation, STEP | 0.2 | 0.7 | 3.3 | 0.5&nbsp;ms | 3.9 | 3.0 | 0.4 | 0.3 | 11.9 |
| Simulation, STL | 0.3 | 0.6 | 3.3 | 0.3&nbsp;ms | 3.6 | 0.3 | 0.4 | 0.2 | 8.8 |
| Simulation, OBJ | 0.3 | 0.8 | 3.5 | 0.6&nbsp;ms | 3.9 | 5.0 | 0.4 | 0.2 | 14.2 |
| Visual, GLB | 0.2 | 0.7 | 3.3 | 0.4&nbsp;ms | 7.9 | 0.1 | 0.7 | 0.3 | 13.3 |
| Visual, OBJ | 0.2 | 0.6 | 3.1 | 0.3&nbsp;ms | 7.5 | 3.8 | 0.9 | 0.2 | 16.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lhc/hardware](https://github.com/lhc/hardware)<br>Board: `lhc_tijolo32_board.kicad_pcb` |
|---|---|
| Folder | nodeLHC-ESP32 / projeto |
| Complexity | 239&nbsp;/&nbsp;1000 (size&nbsp;164, features&nbsp;75) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 46, 405, 75 |
| Triangles,&nbsp;simulation | 901,160 in 76 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">402&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">148&nbsp;MB</td><td align="right">497&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">45&nbsp;MB</td><td align="right">417&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">91&nbsp;MB</td><td align="right">618&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">589&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">77&nbsp;MB</td><td align="right">615&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1466. placas-kicad

![placas-kicad: stages 4 and 6 take 50% to 82% of a run. Simulation, GLB takes 4.0 s. Simulation, STEP takes 5.2 s. Simulation, STL takes 4.0 s. Simulation, OBJ takes 5.8 s. Visual, GLB takes 5.8 s. Visual, OBJ takes 7.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1466b_hardware_placas-kicad/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.3 | 1.6 | 0.3&nbsp;ms | 1.4 | 58&nbsp;ms | 0.2 | 0.3 | 4.0 |
| Simulation, STEP | 0.2 | 0.3 | 1.5 | 0.5&nbsp;ms | 1.4 | 1.4 | 0.2 | 0.2 | 5.2 |
| Simulation, STL | 0.2 | 0.3 | 1.5 | 0.2&nbsp;ms | 1.4 | 85&nbsp;ms | 0.2 | 0.2 | 4.0 |
| Simulation, OBJ | 0.2 | 0.3 | 1.6 | 0.2&nbsp;ms | 1.3 | 2.0 | 0.2 | 0.2 | 5.8 |
| Visual, GLB | 0.2 | 0.3 | 1.5 | 0.2&nbsp;ms | 3.3 | 42&nbsp;ms | 0.3 | 0.2 | 5.8 |
| Visual, OBJ | 0.2 | 0.3 | 1.5 | 0.2&nbsp;ms | 3.2 | 1.4 | 0.3 | 0.3 | 7.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lhc/hardware](https://github.com/lhc/hardware)<br>Board: `placas-kicad.kicad_pcb` |
|---|---|
| Folder | Oficinas / monte-sua-placa-kicad / Projeto Live |
| Complexity | 220&nbsp;/&nbsp;1000 (size&nbsp;140, features&nbsp;80) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 24, 139, 25 |
| Triangles,&nbsp;simulation | 344,872 in 43 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">277&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">53&nbsp;MB</td><td align="right">278&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">17&nbsp;MB</td><td align="right">287&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">34&nbsp;MB</td><td align="right">279&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.4&nbsp;MB</td><td align="right">282&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">25&nbsp;MB</td><td align="right">276&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1467. lhc-esp

![lhc-esp: stages 4 and 6 take 50% to 81% of a run. Simulation, GLB takes 4.4 s. Simulation, STEP takes 5.9 s. Simulation, STL takes 4.6 s. Simulation, OBJ takes 6.6 s. Visual, GLB takes 6.8 s. Visual, OBJ takes 8.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1467b_hardware_lhc-esp/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.7 | 0.2&nbsp;ms | 1.4 | 66&nbsp;ms | 0.3 | 0.2 | 4.4 |
| Simulation, STEP | 0.2 | 0.5 | 1.7 | 0.2&nbsp;ms | 1.4 | 1.5 | 0.3 | 0.3 | 5.9 |
| Simulation, STL | 0.2 | 0.4 | 1.7 | 0.3&nbsp;ms | 1.6 | 0.1 | 0.3 | 0.2 | 4.6 |
| Simulation, OBJ | 0.2 | 0.4 | 1.8 | 0.3&nbsp;ms | 1.6 | 2.2 | 0.2 | 0.2 | 6.6 |
| Visual, GLB | 0.2 | 0.4 | 1.6 | 0.4&nbsp;ms | 3.9 | 57&nbsp;ms | 0.3 | 0.3 | 6.8 |
| Visual, OBJ | 0.2 | 0.4 | 1.6 | 0.2&nbsp;ms | 4.0 | 1.7 | 0.3 | 0.2 | 8.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lhc/hardware](https://github.com/lhc/hardware)<br>Board: `lhc-esp.kicad_pcb` |
|---|---|
| Folder | Oficinas / monte-sua-placa-kicad / Projeto Referência |
| Complexity | 228&nbsp;/&nbsp;1000 (size&nbsp;148, features&nbsp;80) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 24, 194, 58 |
| Triangles,&nbsp;simulation | 398,364 in 43 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">300&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">61&nbsp;MB</td><td align="right">294&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">20&nbsp;MB</td><td align="right">276&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">40&nbsp;MB</td><td align="right">289&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">10&nbsp;MB</td><td align="right">314&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">30&nbsp;MB</td><td align="right">308&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1468. BPS-Minion

![BPS-Minion: stages 4 and 6 take 57% to 85% of a run. Simulation, GLB takes 28 s. Simulation, STEP takes 36 s. Simulation, STL takes 28 s. Simulation, OBJ takes 42 s. Visual, GLB takes 42 s. Visual, OBJ takes 51 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1468b_bps-voltagepcb_BPS-Minion/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.1 | 13.3 | 0.7&nbsp;ms | 10.2 | 0.4 | 1.1 | 0.2 | 28.1 |
| Simulation, STEP | 0.7 | 2.1 | 13.3 | 0.7&nbsp;ms | 10.5 | 7.5 | 1.1 | 0.3 | 35.6 |
| Simulation, STL | 0.8 | 2.1 | 13.3 | 0.8&nbsp;ms | 10.2 | 0.7 | 1.1 | 0.2 | 28.4 |
| Simulation, OBJ | 0.7 | 2.0 | 13.2 | 0.8&nbsp;ms | 10.4 | 13.9 | 1.1 | 0.2 | 41.6 |
| Visual, GLB | 0.7 | 2.1 | 13.3 | 0.7&nbsp;ms | 22.4 | 0.3 | 2.9 | 0.3 | 42.1 |
| Visual, OBJ | 0.7 | 2.1 | 13.4 | 0.8&nbsp;ms | 21.7 | 9.7 | 3.1 | 0.2 | 51.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lhr-solar/bps-voltagepcb](https://github.com/lhr-solar/bps-voltagepcb)<br>Board: `BPS-Minion.kicad_pcb` |
|---|---|
| Complexity | 365&nbsp;/&nbsp;1000 (size&nbsp;255, features&nbsp;110) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 218, 1,543, 223 |
| Triangles,&nbsp;simulation | 2,640,284 in 220 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">92&nbsp;MB</td><td align="right">884&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">521&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">132&nbsp;MB</td><td align="right">893&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">283&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">62&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">190&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1469. BPS-Leader

![BPS-Leader: stages 4 and 6 take 54% to 81% of a run. Simulation, GLB takes 36 s. Simulation, STEP takes 44 s. Simulation, STL takes 36 s. Simulation, OBJ takes 53 s. Visual, GLB takes 56 s. Visual, OBJ takes 69 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1469b_ps-bpsleader_BPS-Leader/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.7 | 4.3 | 15.0 | 1&nbsp;ms | 13.1 | 0.5 | 1.4 | 0.3 | 36.3 |
| Simulation, STEP | 1.7 | 4.3 | 14.8 | 1&nbsp;ms | 12.7 | 8.9 | 1.3 | 0.3 | 43.9 |
| Simulation, STL | 1.7 | 4.2 | 14.4 | 1&nbsp;ms | 13.2 | 0.8 | 1.4 | 0.3 | 36.1 |
| Simulation, OBJ | 1.6 | 4.3 | 15.0 | 1&nbsp;ms | 13.5 | 16.8 | 1.4 | 0.3 | 52.9 |
| Visual, GLB | 1.7 | 4.3 | 15.2 | 0.9&nbsp;ms | 30.7 | 0.5 | 3.7 | 0.3 | 56.4 |
| Visual, OBJ | 1.7 | 4.3 | 14.9 | 1.0&nbsp;ms | 30.1 | 14.6 | 3.2 | 0.3 | 69.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lhr-solar/ps-bpsleader](https://github.com/lhr-solar/ps-bpsleader)<br>Board: `BPS-Leader.kicad_pcb` |
|---|---|
| Folder | Hardware |
| Complexity | 344&nbsp;/&nbsp;1000 (size&nbsp;209, features&nbsp;135) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 225, 1,999, 475 |
| Triangles,&nbsp;simulation | 2,710,942 in 222 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">95&nbsp;MB</td><td align="right">972&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">496&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">136&nbsp;MB</td><td align="right">960&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">290&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">82&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">253&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1470. PowerDistributionUnit

![PowerDistributionUnit: stages 4 and 6 take 51% to 83% of a run. Simulation, GLB takes 76 s. Simulation, STEP takes 98 s. Simulation, STL takes 83 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1470b_ps-powerdistributionunit_PowerDistributionUnit/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.1 | 7.9 | 30.1 | 3&nbsp;ms | 28.7 | 1.5 | 4.0 | 0.5 | 75.8 |
| Simulation, STEP | 3.3 | 7.9 | 31.0 | 4&nbsp;ms | 29.9 | 21.1 | 4.6 | 0.5 | 98.3 |
| Simulation, STL | 3.1 | 8.2 | 32.4 | 3&nbsp;ms | 31.5 | 3.5 | 4.1 | 0.5 | 83.3 |
| Simulation, OBJ | 3.1 | 8.1 | 31.4 | 2&nbsp;ms | 32.1 | 44.8 | 4.4 | 0.5 | 124.4 |
| Visual, GLB | 3.3 | 8.0 | 31.4 | 3&nbsp;ms | 84.8 | 0.8 | 10.8 | 0.4 | 139.5 |
| Visual, OBJ | 3.2 | 8.0 | 30.6 | 2&nbsp;ms | 81.7 | 26.7 | 10.7 | 0.4 | 161.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lhr-solar/ps-powerdistributionunit](https://github.com/lhr-solar/ps-powerdistributionunit)<br>Board: `PowerDistributionUnit.kicad_pcb` |
|---|---|
| Folder | hardware / archive / PowerDistributionUnit_TPS25983 |
| Complexity | 423&nbsp;/&nbsp;1000 (size&nbsp;298, features&nbsp;125) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 693, 5,070, 989 |
| Triangles,&nbsp;simulation | 7,888,204 in 445 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">265&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.1&nbsp;GB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">394&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">838&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">170&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">546&nbsp;MB</td><td align="right">3.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1471. PowerDistributionUnit_Mk1

![PowerDistributionUnit_Mk1: stages 4 and 6 take 51% to 82% of a run. Simulation, GLB takes 76 s. Simulation, STEP takes 95 s. Simulation, STL takes 78 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1471b_ps-powerdistributionunit_PowerDistributionUnit-Mk1/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.6 | 8.9 | 31.9 | 4&nbsp;ms | 26.8 | 1.3 | 3.6 | 0.4 | 75.6 |
| Simulation, STEP | 2.4 | 8.7 | 32.5 | 3&nbsp;ms | 27.6 | 20.1 | 3.7 | 0.5 | 95.5 |
| Simulation, STL | 2.4 | 8.7 | 33.1 | 3&nbsp;ms | 27.2 | 3.0 | 3.6 | 0.4 | 78.4 |
| Simulation, OBJ | 2.4 | 8.9 | 31.8 | 3&nbsp;ms | 27.7 | 41.1 | 3.5 | 0.4 | 115.8 |
| Visual, GLB | 2.4 | 8.7 | 30.0 | 3&nbsp;ms | 69.7 | 1.0 | 9.1 | 0.3 | 121.3 |
| Visual, OBJ | 2.6 | 8.9 | 31.6 | 3&nbsp;ms | 68.5 | 26.7 | 9.0 | 0.3 | 147.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lhr-solar/ps-powerdistributionunit](https://github.com/lhr-solar/ps-powerdistributionunit)<br>Board: `PowerDistributionUnit_Mk1.kicad_pcb` |
|---|---|
| Folder | hardware / PowerDistributionUnit_Mk1 |
| Complexity | 440&nbsp;/&nbsp;1000 (size&nbsp;315, features&nbsp;125) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 518, 5,195, 762 |
| Triangles,&nbsp;simulation | 7,549,914 in 514 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">256&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.1&nbsp;GB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">378&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">809&nbsp;MB</td><td align="right">4.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">178&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">572&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1472. TestBoard_TPS27SA08-Q1

![TestBoard_TPS27SA08-Q1: stages 4 and 6 take 52% to 82% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 16 s. Simulation, STL takes 13 s. Simulation, OBJ takes 19 s. Visual, GLB takes 19 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1472b_ps-powerdistributionunit_TestBoard-TPS27SA08-Q1/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.4 | 5.6 | 0.3&nbsp;ms | 4.2 | 0.2 | 0.5 | 0.2 | 12.7 |
| Simulation, STEP | 0.5 | 1.3 | 5.9 | 0.3&nbsp;ms | 4.1 | 3.5 | 0.5 | 0.2 | 16.1 |
| Simulation, STL | 0.5 | 1.4 | 5.8 | 0.4&nbsp;ms | 4.2 | 0.3 | 0.5 | 0.2 | 13.0 |
| Simulation, OBJ | 0.5 | 1.3 | 5.9 | 0.3&nbsp;ms | 4.2 | 6.8 | 0.5 | 0.2 | 19.3 |
| Visual, GLB | 0.5 | 1.4 | 5.6 | 0.4&nbsp;ms | 9.9 | 0.2 | 1.0 | 0.3 | 18.9 |
| Visual, OBJ | 0.5 | 1.3 | 5.5 | 0.3&nbsp;ms | 9.8 | 5.0 | 0.9 | 0.2 | 23.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lhr-solar/ps-powerdistributionunit](https://github.com/lhr-solar/ps-powerdistributionunit)<br>Board: `TestBoard_TPS27SA08-Q1.kicad_pcb` |
|---|---|
| Folder | hardware / TestBoard_TPS27SA08-Q1 |
| Complexity | 310&nbsp;/&nbsp;1000 (size&nbsp;215, features&nbsp;95) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>knockout text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 102, 576, 52 |
| Triangles,&nbsp;simulation | 1,255,072 in 114 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">43&nbsp;MB</td><td align="right">547&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">203&nbsp;MB</td><td align="right">621&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">63&nbsp;MB</td><td align="right">538&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">129&nbsp;MB</td><td align="right">883&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">753&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">94&nbsp;MB</td><td align="right">724&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1473. LibreRouter_MegaBoard

![LibreRouter_MegaBoard: stages 4 and 6 take 60% to 82% of a run. Simulation, GLB takes 69 s. Simulation, STEP takes 78 s. Simulation, STL takes 68 s. Simulation, OBJ takes 93 s. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1473b_librerouter_LibreRouter-MegaBoard/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.4 | 9.1 | 32.9 | 1&nbsp;ms | 22.0 | 0.8 | 2.3 | 0.3 | 69.0 |
| Simulation, STEP | 1.4 | 9.0 | 32.8 | 3&nbsp;ms | 21.8 | 10.5 | 2.4 | 0.4 | 78.3 |
| Simulation, STL | 1.2 | 8.8 | 31.9 | 1&nbsp;ms | 22.0 | 1.8 | 2.3 | 0.4 | 68.4 |
| Simulation, OBJ | 1.3 | 8.9 | 33.7 | 1&nbsp;ms | 21.9 | 24.4 | 2.5 | 0.4 | 93.0 |
| Visual, GLB | 1.2 | 9.3 | 33.0 | 1&nbsp;ms | 53.4 | 0.6 | 7.0 | 0.3 | 104.8 |
| Visual, OBJ | 1.3 | 8.9 | 32.2 | 1&nbsp;ms | 51.3 | 20.3 | 7.5 | 0.3 | 121.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [libremesh/librerouter](https://github.com/libremesh/librerouter)<br>Board: `LibreRouter_MegaBoard.kicad_pcb` |
|---|---|
| Folder | designs / mega_board |
| Complexity | 282&nbsp;/&nbsp;1000 (size&nbsp;227, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 234, 2,323, 2,552 |
| Triangles,&nbsp;simulation | 4,770,072 in 288 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">164&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">559&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">239&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">510&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">136&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">434&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1474. bms-8s50-ic

![bms-8s50-ic: stages 4 and 6 take 57% to 84% of a run. Simulation, GLB takes 19 s. Simulation, STEP takes 23 s. Simulation, STL takes 19 s. Simulation, OBJ takes 27 s. Visual, GLB takes 26 s. Visual, OBJ takes 32 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1474b_bms-8s50-ic_bms-8s50-ic/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 1.8 | 7.4 | 0.4&nbsp;ms | 8.1 | 0.3 | 0.7 | 0.2 | 19.0 |
| Simulation, STEP | 0.5 | 1.5 | 7.2 | 0.4&nbsp;ms | 8.0 | 4.9 | 0.6 | 0.2 | 23.0 |
| Simulation, STL | 0.5 | 1.6 | 7.4 | 0.5&nbsp;ms | 8.3 | 0.6 | 0.7 | 0.2 | 19.3 |
| Simulation, OBJ | 0.5 | 1.5 | 7.1 | 0.4&nbsp;ms | 8.2 | 8.6 | 0.6 | 0.2 | 26.8 |
| Visual, GLB | 0.5 | 1.5 | 7.4 | 0.4&nbsp;ms | 14.4 | 0.2 | 1.7 | 0.2 | 26.0 |
| Visual, OBJ | 0.5 | 1.6 | 7.0 | 0.4&nbsp;ms | 14.6 | 6.6 | 1.8 | 0.2 | 32.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [libresolar/bms-8s50-ic](https://github.com/libresolar/bms-8s50-ic)<br>Board: `bms-8s50-ic.kicad_pcb` |
|---|---|
| Folder | kicad |
| Complexity | 300&nbsp;/&nbsp;1000 (size&nbsp;245, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 160, 1,428, 275 |
| Triangles,&nbsp;simulation | 1,688,996 in 155 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">58&nbsp;MB</td><td align="right">624&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">257&nbsp;MB</td><td align="right">802&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">84&nbsp;MB</td><td align="right">647&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">174&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">44&nbsp;MB</td><td align="right">809&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">132&nbsp;MB</td><td align="right">918&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1475. bms-c1

![bms-c1: stages 4 and 6 take 49% to 81% of a run. Simulation, GLB takes 39 s. Simulation, STEP takes 57 s. Simulation, STL takes 37 s. Simulation, OBJ takes 57 s. Visual, GLB takes 48 s. Visual, OBJ takes 60 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1475b_bms-c1_bms-c1/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.1 | 5.1 | 16.4 | 1&nbsp;ms | 13.3 | 0.7 | 1.6 | 0.3 | 38.5 |
| Simulation, STEP | 1.4 | 5.7 | 19.6 | 0.8&nbsp;ms | 17.2 | 10.7 | 1.7 | 0.4 | 56.7 |
| Simulation, STL | 1.2 | 5.0 | 15.1 | 0.5&nbsp;ms | 12.3 | 1.6 | 1.4 | 0.3 | 36.9 |
| Simulation, OBJ | 1.0 | 4.6 | 15.4 | 0.7&nbsp;ms | 12.5 | 21.2 | 1.7 | 0.4 | 56.7 |
| Visual, GLB | 1.0 | 4.7 | 14.7 | 0.7&nbsp;ms | 24.3 | 0.3 | 3.2 | 0.3 | 48.4 |
| Visual, OBJ | 1.0 | 4.6 | 14.1 | 0.6&nbsp;ms | 23.5 | 13.0 | 3.4 | 0.3 | 60.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [LibreSolar/bms-c1](https://github.com/LibreSolar/bms-c1)<br>Board: `bms-c1.kicad_pcb` |
|---|---|
| Folder | kicad |
| Complexity | 383&nbsp;/&nbsp;1000 (size&nbsp;263, features&nbsp;120) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 169, 1,097, 805 |
| Triangles,&nbsp;simulation | 3,559,068 in 155 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">120&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">359&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">178&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">369&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">71&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">223&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1476. mppt-1210-hus

![mppt-1210-hus: stages 4 and 6 take 54% to 83% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 19 s. Simulation, STL takes 16 s. Simulation, OBJ takes 23 s. Visual, GLB takes 22 s. Visual, OBJ takes 27 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1476b_mppt-1210-hus_mppt-1210-hus/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 1.7 | 6.5 | 0.5&nbsp;ms | 6.3 | 0.2 | 0.7 | 0.3 | 16.3 |
| Simulation, STEP | 0.5 | 1.6 | 6.2 | 0.8&nbsp;ms | 6.2 | 4.0 | 0.6 | 0.3 | 19.4 |
| Simulation, STL | 0.5 | 1.7 | 6.2 | 0.6&nbsp;ms | 6.3 | 0.4 | 0.6 | 0.2 | 15.8 |
| Simulation, OBJ | 0.5 | 1.6 | 6.3 | 0.6&nbsp;ms | 6.1 | 7.7 | 0.7 | 0.3 | 23.1 |
| Visual, GLB | 0.5 | 1.7 | 6.4 | 0.6&nbsp;ms | 11.4 | 0.2 | 1.1 | 0.2 | 21.5 |
| Visual, OBJ | 0.5 | 1.7 | 6.4 | 0.5&nbsp;ms | 10.8 | 6.5 | 1.1 | 0.3 | 27.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [LibreSolar/mppt-1210-hus](https://github.com/LibreSolar/mppt-1210-hus)<br>Board: `mppt-1210-hus.kicad_pcb` |
|---|---|
| Folder | kicad |
| Complexity | 285&nbsp;/&nbsp;1000 (size&nbsp;230, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 118, 1,023, 212 |
| Triangles,&nbsp;simulation | 1,362,694 in 99 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">47&nbsp;MB</td><td align="right">546&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">217&nbsp;MB</td><td align="right">686&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">68&nbsp;MB</td><td align="right">541&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">140&nbsp;MB</td><td align="right">917&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">736&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">116&nbsp;MB</td><td align="right">866&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1477. mppt-2420-hc

![mppt-2420-hc: stages 4 and 6 take 49% to 82% of a run. Simulation, GLB takes 19 s. Simulation, STEP takes 25 s. Simulation, STL takes 20 s. Simulation, OBJ takes 31 s. Visual, GLB takes 28 s. Visual, OBJ takes 35 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1477b_mppt-2420-hc_mppt-2420-hc/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 2.3 | 7.4 | 0.5&nbsp;ms | 7.5 | 0.3 | 0.9 | 0.3 | 19.4 |
| Simulation, STEP | 0.7 | 2.3 | 7.3 | 0.6&nbsp;ms | 7.5 | 5.7 | 0.9 | 0.3 | 24.7 |
| Simulation, STL | 0.7 | 2.3 | 7.5 | 1&nbsp;ms | 7.7 | 0.6 | 0.9 | 0.2 | 19.8 |
| Simulation, OBJ | 0.7 | 2.3 | 7.2 | 1&nbsp;ms | 7.7 | 11.5 | 0.9 | 0.3 | 30.6 |
| Visual, GLB | 0.7 | 2.3 | 7.3 | 0.9&nbsp;ms | 15.7 | 0.2 | 1.7 | 0.2 | 28.1 |
| Visual, OBJ | 0.6 | 2.4 | 7.3 | 0.6&nbsp;ms | 15.4 | 7.4 | 1.9 | 0.3 | 35.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [LibreSolar/mppt-2420-hc](https://github.com/LibreSolar/mppt-2420-hc)<br>Board: `mppt-2420-hc.kicad_pcb` |
|---|---|
| Folder | kicad |
| Complexity | 307&nbsp;/&nbsp;1000 (size&nbsp;252, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 140, 1,263, 282 |
| Triangles,&nbsp;simulation | 2,031,356 in 113 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">69&nbsp;MB</td><td align="right">658&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">252&nbsp;MB</td><td align="right">834&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">102&nbsp;MB</td><td align="right">668&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">210&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">818&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">137&nbsp;MB</td><td align="right">994&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1478. mppt-2420-hpx

![mppt-2420-hpx: stages 4 and 6 take 49% to 81% of a run. Simulation, GLB takes 18 s. Simulation, STEP takes 23 s. Simulation, STL takes 18 s. Simulation, OBJ takes 27 s. Visual, GLB takes 29 s. Visual, OBJ takes 34 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1478b_mppt-2420-hpx_mppt-2420-hpx/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 2.1 | 7.0 | 1.0&nbsp;ms | 6.5 | 0.4 | 0.9 | 0.2 | 17.6 |
| Simulation, STEP | 0.5 | 2.0 | 7.1 | 0.8&nbsp;ms | 6.9 | 5.2 | 0.9 | 0.2 | 22.9 |
| Simulation, STL | 0.6 | 2.1 | 7.1 | 1&nbsp;ms | 7.0 | 0.6 | 0.8 | 0.2 | 18.4 |
| Simulation, OBJ | 0.6 | 2.1 | 6.8 | 0.9&nbsp;ms | 6.6 | 10.0 | 0.9 | 0.3 | 27.2 |
| Visual, GLB | 0.5 | 2.1 | 6.9 | 0.9&nbsp;ms | 16.3 | 0.2 | 2.2 | 0.2 | 28.6 |
| Visual, OBJ | 0.6 | 2.1 | 6.8 | 1&nbsp;ms | 15.4 | 6.8 | 2.4 | 0.3 | 34.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [libresolar/mppt-2420-hpx](https://github.com/libresolar/mppt-2420-hpx)<br>Board: `mppt-2420-hpx.kicad_pcb` |
|---|---|
| Folder | kicad |
| Complexity | 301&nbsp;/&nbsp;1000 (size&nbsp;256, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 178, 1,413, 274 |
| Triangles,&nbsp;simulation | 2,395,966 in 170 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">82&nbsp;MB</td><td align="right">754&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">300&nbsp;MB</td><td align="right">975&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">120&nbsp;MB</td><td align="right">789&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">250&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">53&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">163&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1479. cantact

![cantact: stages 4 and 6 take 55% to 79% of a run. Simulation, GLB takes 3.5 s. Simulation, STEP takes 4.7 s. Simulation, STL takes 3.5 s. Simulation, OBJ takes 4.7 s. Visual, GLB takes 5.0 s. Visual, OBJ takes 5.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1479b_cantact-hw_cantact/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.2 | 0.3&nbsp;ms | 1.5 | 49&nbsp;ms | 0.2 | 0.2 | 3.5 |
| Simulation, STEP | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 1.5 | 1.3 | 0.2 | 0.2 | 4.7 |
| Simulation, STL | 0.1 | 0.2 | 1.1 | 0.2&nbsp;ms | 1.5 | 82&nbsp;ms | 0.2 | 0.2 | 3.5 |
| Simulation, OBJ | 0.1 | 0.2 | 1.1 | 0.3&nbsp;ms | 1.5 | 1.3 | 0.2 | 0.2 | 4.7 |
| Visual, GLB | 0.1 | 0.3 | 1.2 | 0.3&nbsp;ms | 2.8 | 37&nbsp;ms | 0.3 | 0.3 | 5.0 |
| Visual, OBJ | 0.1 | 0.2 | 1.1 | 0.3&nbsp;ms | 2.8 | 1.1 | 0.3 | 0.2 | 5.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [linklayer/cantact-hw](https://github.com/linklayer/cantact-hw)<br>Board: `cantact.kicad_pcb` |
|---|---|
| Complexity | 228&nbsp;/&nbsp;1000 (size&nbsp;193, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 34, 333, 22 |
| Triangles,&nbsp;simulation | 334,110 in 72 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">256&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">57&nbsp;MB</td><td align="right">297&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">17&nbsp;MB</td><td align="right">258&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">34&nbsp;MB</td><td align="right">263&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">9.4&nbsp;MB</td><td align="right">302&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">28&nbsp;MB</td><td align="right">300&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1480. Issue3B

![Issue3B: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 59 s. Simulation, STEP takes 74 s. Simulation, STL takes 61 s. Simulation, OBJ takes 94 s. Visual, GLB takes 96 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1480b_ZX-Spectrum-48K-Issue-3B-Based-on-Gerbers-by-PABB-on-PCBWay_Issue3B/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.0 | 5.0 | 25.7 | 2&nbsp;ms | 22.5 | 0.9 | 2.8 | 0.4 | 59.2 |
| Simulation, STEP | 2.0 | 5.0 | 26.6 | 2&nbsp;ms | 22.1 | 15.1 | 2.9 | 0.4 | 74.0 |
| Simulation, STL | 1.9 | 4.9 | 25.7 | 2&nbsp;ms | 23.4 | 2.1 | 3.1 | 0.4 | 61.4 |
| Simulation, OBJ | 1.9 | 5.1 | 26.0 | 2&nbsp;ms | 22.8 | 34.7 | 2.9 | 0.4 | 93.8 |
| Visual, GLB | 1.9 | 5.3 | 25.3 | 2&nbsp;ms | 54.6 | 0.6 | 7.4 | 0.3 | 95.5 |
| Visual, OBJ | 2.0 | 5.2 | 27.6 | 2&nbsp;ms | 55.8 | 22.9 | 7.5 | 0.3 | 121.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [liveboxandy/ZX-Spectrum-48K-Issue-3B---Based-on-Gerbers-by-PABB-on-PCBWay](https://github.com/liveboxandy/ZX-Spectrum-48K-Issue-3B---Based-on-Gerbers-by-PABB-on-PCBWay)<br>Board: `Issue3B.kicad_pcb` |
|---|---|
| Complexity | 277&nbsp;/&nbsp;1000 (size&nbsp;222, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>copper drawings,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 201, 7,150, 422 |
| Triangles,&nbsp;simulation | 5,693,544 in 181 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">193&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">842&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">285&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">604&nbsp;MB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">129&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">412&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 1481. dualpmod

![dualpmod: stages 4 and 6 take 50% to 79% of a run. Simulation, GLB takes 2.2 s. Simulation, STEP takes 3.1 s. Simulation, STL takes 2.3 s. Simulation, OBJ takes 3.2 s. Visual, GLB takes 3.0 s. Visual, OBJ takes 3.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1481b_sonata-system_dualpmod/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.9 | 0.1&nbsp;ms | 0.7 | 29&nbsp;ms | 0.1 | 0.2 | 2.2 |
| Simulation, STEP | 0.1 | 0.2 | 0.9 | 0.1&nbsp;ms | 0.7 | 0.9 | 0.1 | 0.2 | 3.1 |
| Simulation, STL | 0.1 | 0.2 | 0.9 | 0.2&nbsp;ms | 0.7 | 38&nbsp;ms | 97&nbsp;ms | 0.2 | 2.3 |
| Simulation, OBJ | 0.1 | 0.2 | 0.9 | 0.2&nbsp;ms | 0.7 | 0.9 | 0.1 | 0.2 | 3.2 |
| Visual, GLB | 97&nbsp;ms | 0.2 | 0.9 | 0.2&nbsp;ms | 1.5 | 19&nbsp;ms | 0.1 | 0.2 | 3.0 |
| Visual, OBJ | 92&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 1.5 | 0.5 | 0.1 | 0.2 | 3.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [lowRISC/sonata-system](https://github.com/lowRISC/sonata-system)<br>Board: `dualpmod.kicad_pcb` |
|---|---|
| Folder | vendor / lowrisc_ip / ip / usbdev / pmod / dualpmod-kicad |
| Complexity | 185&nbsp;/&nbsp;1000 (size&nbsp;130, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 13, 129, 17 |
| Triangles,&nbsp;simulation | 177,628 in 28 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">6.3&nbsp;MB</td><td align="right">207&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">33&nbsp;MB</td><td align="right">216&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">8.9&nbsp;MB</td><td align="right">209&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">18&nbsp;MB</td><td align="right">211&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.9&nbsp;MB</td><td align="right">168&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">11&nbsp;MB</td><td align="right">171&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1482. ad9864_breakout

![ad9864_breakout: stages 4 and 6 take 52% to 82% of a run. Simulation, GLB takes 8.6 s. Simulation, STEP takes 10 s. Simulation, STL takes 8.8 s. Simulation, OBJ takes 12 s. Visual, GLB takes 13 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1482b_vna_ad9864-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.9 | 4.0 | 0.3&nbsp;ms | 2.7 | 0.1 | 0.4 | 0.3 | 8.6 |
| Simulation, STEP | 0.3 | 0.7 | 3.7 | 0.3&nbsp;ms | 2.7 | 2.2 | 0.4 | 0.2 | 10.1 |
| Simulation, STL | 0.2 | 0.9 | 3.9 | 0.5&nbsp;ms | 2.8 | 0.3 | 0.4 | 0.3 | 8.8 |
| Simulation, OBJ | 0.2 | 0.8 | 3.8 | 0.3&nbsp;ms | 2.6 | 4.2 | 0.4 | 0.2 | 12.3 |
| Visual, GLB | 0.2 | 0.8 | 3.8 | 0.3&nbsp;ms | 6.7 | 88&nbsp;ms | 0.9 | 0.3 | 12.8 |
| Visual, OBJ | 0.3 | 0.9 | 3.9 | 0.4&nbsp;ms | 6.8 | 2.8 | 0.8 | 0.2 | 15.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `ad9864_breakout.kicad_pcb` |
|---|---|
| Folder | breakouts / ad9864 |
| Complexity | 264&nbsp;/&nbsp;1000 (size&nbsp;229, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 82, 476, 74 |
| Triangles,&nbsp;simulation | 859,342 in 73 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">384&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">128&nbsp;MB</td><td align="right">434&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">43&nbsp;MB</td><td align="right">395&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">89&nbsp;MB</td><td align="right">633&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">460&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">56&nbsp;MB</td><td align="right">461&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1483. adc32xx_syzygy

![adc32xx_syzygy: stages 4 and 6 take 53% to 85% of a run. Simulation, GLB takes 14 s. Simulation, STEP takes 17 s. Simulation, STL takes 13 s. Simulation, OBJ takes 21 s. Visual, GLB takes 20 s. Visual, OBJ takes 25 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1483b_vna_adc32xx-syzygy/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.2 | 6.3 | 0.6&nbsp;ms | 4.7 | 0.2 | 0.5 | 0.2 | 13.5 |
| Simulation, STEP | 0.4 | 1.2 | 6.0 | 0.6&nbsp;ms | 4.8 | 3.6 | 0.5 | 0.2 | 16.6 |
| Simulation, STL | 0.4 | 1.2 | 6.0 | 0.4&nbsp;ms | 4.6 | 0.4 | 0.5 | 0.2 | 13.2 |
| Simulation, OBJ | 0.4 | 1.2 | 6.4 | 0.5&nbsp;ms | 4.8 | 7.5 | 0.5 | 0.2 | 21.0 |
| Visual, GLB | 0.4 | 1.3 | 6.4 | 0.5&nbsp;ms | 11.0 | 0.1 | 0.9 | 0.2 | 20.3 |
| Visual, OBJ | 0.3 | 1.3 | 6.1 | 0.4&nbsp;ms | 11.2 | 5.0 | 1.3 | 0.2 | 25.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `adc32xx_syzygy.kicad_pcb` |
|---|---|
| Folder | breakouts / adc32xx_syzygy / adc32xx_syzygy |
| Complexity | 346&nbsp;/&nbsp;1000 (size&nbsp;246, features&nbsp;100) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 105, 1,115, 193 |
| Triangles,&nbsp;simulation | 1,389,302 in 112 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">48&nbsp;MB</td><td align="right">598&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">220&nbsp;MB</td><td align="right">667&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">69&nbsp;MB</td><td align="right">613&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">145&nbsp;MB</td><td align="right">962&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">716&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">96&nbsp;MB</td><td align="right">767&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1484. adc344x

![adc344x: stages 4 and 6 take 53% to 82% of a run. Simulation, GLB takes 21 s. Simulation, STEP takes 25 s. Simulation, STL takes 21 s. Simulation, OBJ takes 31 s. Visual, GLB takes 29 s. Visual, OBJ takes 35 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1484b_vna_adc344x/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 2.8 | 9.1 | 0.7&nbsp;ms | 7.0 | 0.3 | 0.8 | 0.3 | 20.7 |
| Simulation, STEP | 0.4 | 2.8 | 9.3 | 0.7&nbsp;ms | 6.8 | 4.5 | 0.8 | 0.3 | 24.8 |
| Simulation, STL | 0.4 | 2.7 | 9.0 | 3&nbsp;ms | 6.7 | 0.6 | 0.8 | 0.3 | 20.6 |
| Simulation, OBJ | 0.4 | 2.8 | 9.3 | 0.9&nbsp;ms | 6.8 | 10.3 | 0.8 | 0.3 | 30.6 |
| Visual, GLB | 0.5 | 2.8 | 9.1 | 0.9&nbsp;ms | 14.7 | 0.2 | 1.5 | 0.3 | 29.0 |
| Visual, OBJ | 0.5 | 2.8 | 9.3 | 1&nbsp;ms | 14.5 | 6.1 | 1.7 | 0.3 | 35.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `adc344x.kicad_pcb` |
|---|---|
| Folder | breakouts / adc344x |
| Complexity | 296&nbsp;/&nbsp;1000 (size&nbsp;251, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20190516) |
| Parts,&nbsp;tracks,&nbsp;vias | 156, 1,475, 112 |
| Triangles,&nbsp;simulation | 1,762,408 in 160 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">61&nbsp;MB</td><td align="right">636&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">262&nbsp;MB</td><td align="right">753&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">88&nbsp;MB</td><td align="right">588&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">186&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">35&nbsp;MB</td><td align="right">829&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">105&nbsp;MB</td><td align="right">820&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1485. adc_32xx

![adc_32xx: stages 4 and 6 take 54% to 82% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 16 s. Simulation, STL takes 14 s. Simulation, OBJ takes 18 s. Visual, GLB takes 18 s. Visual, OBJ takes 21 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1485b_vna_adc-32xx/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.6 | 5.8 | 0.5&nbsp;ms | 4.9 | 0.2 | 0.5 | 0.3 | 13.4 |
| Simulation, STEP | 0.2 | 1.5 | 5.9 | 0.5&nbsp;ms | 5.0 | 3.2 | 0.4 | 0.2 | 16.4 |
| Simulation, STL | 0.2 | 1.4 | 5.6 | 0.7&nbsp;ms | 5.4 | 0.5 | 0.6 | 0.2 | 14.0 |
| Simulation, OBJ | 0.3 | 1.4 | 5.2 | 0.5&nbsp;ms | 4.6 | 5.8 | 0.5 | 0.2 | 18.0 |
| Visual, GLB | 0.2 | 1.4 | 5.5 | 0.7&nbsp;ms | 8.9 | 0.1 | 1.2 | 0.2 | 17.6 |
| Visual, OBJ | 0.3 | 1.4 | 5.7 | 0.4&nbsp;ms | 9.1 | 3.5 | 1.1 | 0.2 | 21.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `adc_32xx.kicad_pcb` |
|---|---|
| Folder | breakouts / adc_32xx / ram_adc |
| Complexity | 296&nbsp;/&nbsp;1000 (size&nbsp;241, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 100, 933, 118 |
| Triangles,&nbsp;simulation | 1,439,468 in 97 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">50&nbsp;MB</td><td align="right">559&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">230&nbsp;MB</td><td align="right">694&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">72&nbsp;MB</td><td align="right">575&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">150&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">29&nbsp;MB</td><td align="right">626&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">86&nbsp;MB</td><td align="right">677&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1486. adc_cape

![adc_cape: stages 4 and 6 take 43% to 82% of a run. Simulation, GLB takes 24 s. Simulation, STEP takes 30 s. Simulation, STL takes 25 s. Simulation, OBJ takes 45 s. Visual, GLB takes 36 s. Visual, OBJ takes 40 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1486b_vna_adc-cape/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 2.3 | 10.2 | 0.4&nbsp;ms | 9.1 | 0.4 | 1.2 | 0.3 | 23.9 |
| Simulation, STEP | 0.3 | 2.3 | 10.9 | 0.3&nbsp;ms | 9.1 | 5.7 | 1.2 | 0.3 | 29.7 |
| Simulation, STL | 0.4 | 2.2 | 10.7 | 0.5&nbsp;ms | 9.1 | 0.8 | 1.5 | 0.3 | 24.9 |
| Simulation, OBJ | 0.3 | 2.3 | 10.3 | 0.5&nbsp;ms | 9.2 | 20.5 | 1.8 | 0.3 | 44.7 |
| Visual, GLB | 0.5 | 3.3 | 12.3 | 0.7&nbsp;ms | 17.5 | 0.2 | 2.0 | 0.3 | 36.2 |
| Visual, OBJ | 0.4 | 2.5 | 10.8 | 0.7&nbsp;ms | 17.5 | 7.1 | 1.4 | 0.3 | 40.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `adc_cape.kicad_pcb` |
|---|---|
| Folder | breakouts / adc_cape |
| Complexity | 231&nbsp;/&nbsp;1000 (size&nbsp;186, features&nbsp;45) |
| KESE&nbsp;features | through vias, filled zones,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 22, 1,037, 129 |
| Triangles,&nbsp;simulation | 2,489,974 in 85 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">85&nbsp;MB</td><td align="right">740&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">321&nbsp;MB</td><td align="right">859&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">125&nbsp;MB</td><td align="right">728&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">262&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">37&nbsp;MB</td><td align="right">805&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">114&nbsp;MB</td><td align="right">835&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1487. adc_dual

![adc_dual: stages 4 and 6 take 51% to 81% of a run. Simulation, GLB takes 7.7 s. Simulation, STEP takes 9.4 s. Simulation, STL takes 7.4 s. Simulation, OBJ takes 11 s. Visual, GLB takes 11 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1487b_vna_adc-dual/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.9 | 3.4 | 0.7&nbsp;ms | 2.4 | 0.1 | 0.3 | 0.2 | 7.7 |
| Simulation, STEP | 0.2 | 0.9 | 3.3 | 0.5&nbsp;ms | 2.5 | 1.9 | 0.3 | 0.3 | 9.4 |
| Simulation, STL | 0.2 | 0.8 | 3.3 | 0.4&nbsp;ms | 2.4 | 0.2 | 0.3 | 0.3 | 7.4 |
| Simulation, OBJ | 0.2 | 0.8 | 3.2 | 0.5&nbsp;ms | 2.4 | 3.7 | 0.3 | 0.3 | 10.9 |
| Visual, GLB | 0.2 | 0.8 | 3.3 | 0.5&nbsp;ms | 5.6 | 83&nbsp;ms | 0.7 | 0.3 | 11.0 |
| Visual, OBJ | 0.2 | 0.8 | 3.2 | 0.5&nbsp;ms | 5.4 | 2.1 | 0.8 | 0.2 | 12.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `adc_dual.kicad_pcb` |
|---|---|
| Folder | breakouts / adc_dual |
| Complexity | 262&nbsp;/&nbsp;1000 (size&nbsp;227, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 77, 465, 61 |
| Triangles,&nbsp;simulation | 697,788 in 69 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">25&nbsp;MB</td><td align="right">387&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">96&nbsp;MB</td><td align="right">398&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">35&nbsp;MB</td><td align="right">375&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">72&nbsp;MB</td><td align="right">513&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">421&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">46&nbsp;MB</td><td align="right">410&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1488. adrf5020_breakout

![adrf5020_breakout: stages 4 and 6 take 56% to 84% of a run. Simulation, GLB takes 9.7 s. Simulation, STEP takes 11 s. Simulation, STL takes 9.7 s. Simulation, OBJ takes 13 s. Visual, GLB takes 12 s. Visual, OBJ takes 15 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1488b_vna_adrf5020-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.8 | 3.4 | 0.1&nbsp;ms | 4.5 | 0.2 | 0.4 | 0.2 | 9.7 |
| Simulation, STEP | 0.2 | 0.9 | 3.5 | 0.1&nbsp;ms | 4.3 | 2.0 | 0.3 | 0.2 | 11.5 |
| Simulation, STL | 0.2 | 0.8 | 3.3 | 0.3&nbsp;ms | 4.6 | 0.2 | 0.4 | 0.2 | 9.7 |
| Simulation, OBJ | 0.2 | 0.8 | 3.2 | 0.1&nbsp;ms | 4.3 | 4.4 | 0.3 | 0.2 | 13.4 |
| Visual, GLB | 0.2 | 0.9 | 3.4 | 0.1&nbsp;ms | 6.8 | 76&nbsp;ms | 0.5 | 0.2 | 12.0 |
| Visual, OBJ | 0.2 | 0.9 | 3.5 | 0.2&nbsp;ms | 6.8 | 2.4 | 0.8 | 0.2 | 14.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `adrf5020_breakout.kicad_pcb` |
|---|---|
| Folder | breakouts / adrf5020_breakout |
| Complexity | 175&nbsp;/&nbsp;1000 (size&nbsp;140, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 18, 78, 5 |
| Triangles,&nbsp;simulation | 1,154,838 in 28 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">488&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">106&nbsp;MB</td><td align="right">615&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">58&nbsp;MB</td><td align="right">516&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">115&nbsp;MB</td><td align="right">775&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">561&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">61&nbsp;MB</td><td align="right">563&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1489. ammp6120_breakout

![ammp6120_breakout: stages 4 and 6 take 47% to 83% of a run. Simulation, GLB takes 2.3 s. Simulation, STEP takes 3.2 s. Simulation, STL takes 2.4 s. Simulation, OBJ takes 3.5 s. Visual, GLB takes 3.7 s. Visual, OBJ takes 4.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1489b_vna_ammp6120-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 90&nbsp;ms | 0.2 | 0.7 | 0.1&nbsp;ms | 0.9 | 34&nbsp;ms | 0.1 | 0.2 | 2.3 |
| Simulation, STEP | 89&nbsp;ms | 0.2 | 0.8 | 0.1&nbsp;ms | 0.9 | 0.9 | 0.1 | 0.2 | 3.2 |
| Simulation, STL | 0.1 | 0.2 | 0.8 | 0.1&nbsp;ms | 0.9 | 57&nbsp;ms | 0.1 | 0.2 | 2.4 |
| Simulation, OBJ | 97&nbsp;ms | 0.2 | 0.8 | 0.1&nbsp;ms | 0.9 | 1.2 | 0.1 | 0.2 | 3.5 |
| Visual, GLB | 99&nbsp;ms | 0.2 | 0.8 | 0.2&nbsp;ms | 2.3 | 18&nbsp;ms | 0.1 | 0.2 | 3.7 |
| Visual, OBJ | 81&nbsp;ms | 0.2 | 0.8 | 0.2&nbsp;ms | 2.5 | 0.5 | 0.1 | 0.2 | 4.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `ammp6120_breakout.kicad_pcb` |
|---|---|
| Folder | breakouts / ammp6120_breakout |
| Complexity | 127&nbsp;/&nbsp;1000 (size&nbsp;107, features&nbsp;20) |
| KESE&nbsp;features | filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 6, 24, 0 |
| Triangles,&nbsp;simulation | 275,826 in 18 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.3&nbsp;MB</td><td align="right">232&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">25&nbsp;MB</td><td align="right">265&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">242&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">27&nbsp;MB</td><td align="right">237&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.5&nbsp;MB</td><td align="right">200&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">13&nbsp;MB</td><td align="right">204&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1490. amp_breakout

![amp_breakout: stages 4 and 6 take 45% to 75% of a run. Simulation, GLB takes 1.4 s. Simulation, STEP takes 2.2 s. Simulation, STL takes 1.4 s. Simulation, OBJ takes 1.9 s. Visual, GLB takes 2.1 s. Visual, OBJ takes 2.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1490b_vna_amp-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 79&nbsp;ms | 0.1 | 0.4 | 0.2&nbsp;ms | 0.5 | 21&nbsp;ms | 57&nbsp;ms | 0.2 | 1.4 |
| Simulation, STEP | 81&nbsp;ms | 0.1 | 0.4 | 0.2&nbsp;ms | 0.6 | 0.7 | 55&nbsp;ms | 0.2 | 2.2 |
| Simulation, STL | 81&nbsp;ms | 0.1 | 0.4 | 0.1&nbsp;ms | 0.5 | 29&nbsp;ms | 55&nbsp;ms | 0.2 | 1.4 |
| Simulation, OBJ | 88&nbsp;ms | 0.1 | 0.4 | 0.1&nbsp;ms | 0.6 | 0.5 | 55&nbsp;ms | 0.2 | 1.9 |
| Visual, GLB | 86&nbsp;ms | 0.1 | 0.4 | 0.2&nbsp;ms | 1.2 | 14&nbsp;ms | 97&nbsp;ms | 0.2 | 2.1 |
| Visual, OBJ | 83&nbsp;ms | 0.1 | 0.4 | 0.1&nbsp;ms | 1.2 | 0.3 | 0.1 | 0.2 | 2.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `amp_breakout.kicad_pcb` |
|---|---|
| Folder | breakouts / amp_breakout |
| Complexity | 184&nbsp;/&nbsp;1000 (size&nbsp;149, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 19, 99, 20 |
| Triangles,&nbsp;simulation | 121,518 in 25 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.4&nbsp;MB</td><td align="right">197&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">15&nbsp;MB</td><td align="right">197&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">6.1&nbsp;MB</td><td align="right">188&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">12&nbsp;MB</td><td align="right">198&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.0&nbsp;MB</td><td align="right">162&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">8.3&nbsp;MB</td><td align="right">160&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1491. amp_cpw_hmc311

![amp_cpw_hmc311: stages 4 and 6 take 50% to 85% of a run. Simulation, GLB takes 2.3 s. Simulation, STEP takes 3.4 s. Simulation, STL takes 2.4 s. Simulation, OBJ takes 3.6 s. Visual, GLB takes 3.7 s. Visual, OBJ takes 4.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1491b_vna_amp-cpw-hmc311/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 86&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 0.8 | 34&nbsp;ms | 0.1 | 0.2 | 2.3 |
| Simulation, STEP | 0.1 | 0.2 | 1.0 | 0.4&nbsp;ms | 0.9 | 1.0 | 0.1 | 0.2 | 3.4 |
| Simulation, STL | 93&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 0.9 | 54&nbsp;ms | 0.1 | 0.2 | 2.4 |
| Simulation, OBJ | 93&nbsp;ms | 0.2 | 1.0 | 0.1&nbsp;ms | 0.8 | 1.2 | 0.1 | 0.2 | 3.6 |
| Visual, GLB | 89&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 2.2 | 18&nbsp;ms | 0.1 | 0.2 | 3.7 |
| Visual, OBJ | 86&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 2.1 | 0.5 | 0.1 | 0.2 | 4.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `amp_cpw_hmc311.kicad_pcb` |
|---|---|
| Folder | breakouts / amp_cpw_hmc311 |
| Complexity | 132&nbsp;/&nbsp;1000 (size&nbsp;112, features&nbsp;20) |
| KESE&nbsp;features | filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 10, 24, 0 |
| Triangles,&nbsp;simulation | 250,288 in 19 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">8.5&nbsp;MB</td><td align="right">245&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">26&nbsp;MB</td><td align="right">245&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">13&nbsp;MB</td><td align="right">243&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">24&nbsp;MB</td><td align="right">227&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.9&nbsp;MB</td><td align="right">190&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">11&nbsp;MB</td><td align="right">186&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1492. amp_macom

![amp_macom: stages 4 and 6 take 43% to 74% of a run. Simulation, GLB takes 1.1 s. Simulation, STEP takes 1.7 s. Simulation, STL takes 1.1 s. Simulation, OBJ takes 1.3 s. Visual, GLB takes 1.6 s. Visual, OBJ takes 1.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1492b_vna_amp-macom/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 72&nbsp;ms | 61&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.4 | 11&nbsp;ms | 35&nbsp;ms | 0.2 | 1.1 |
| Simulation, STEP | 69&nbsp;ms | 59&nbsp;ms | 0.3 | 0.3&nbsp;ms | 0.5 | 0.7 | 36&nbsp;ms | 0.2 | 1.7 |
| Simulation, STL | 82&nbsp;ms | 62&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.4 | 15&nbsp;ms | 37&nbsp;ms | 0.2 | 1.1 |
| Simulation, OBJ | 75&nbsp;ms | 60&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.4 | 0.3 | 38&nbsp;ms | 0.2 | 1.3 |
| Visual, GLB | 77&nbsp;ms | 72&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.9 | 7&nbsp;ms | 56&nbsp;ms | 0.2 | 1.6 |
| Visual, OBJ | 81&nbsp;ms | 65&nbsp;ms | 0.3 | 0.1&nbsp;ms | 0.9 | 0.2 | 54&nbsp;ms | 0.2 | 1.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `amp_macom.kicad_pcb` |
|---|---|
| Folder | breakouts / amp_macom |
| Complexity | 160&nbsp;/&nbsp;1000 (size&nbsp;125, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 8, 43, 6 |
| Triangles,&nbsp;simulation | 63,682 in 19 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">2.3&nbsp;MB</td><td align="right">166&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">9.5&nbsp;MB</td><td align="right">170&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">3.2&nbsp;MB</td><td align="right">169&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.3&nbsp;MB</td><td align="right">171&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">1.3&nbsp;MB</td><td align="right">154&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.6&nbsp;MB</td><td align="right">154&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1493. amp_macom_vga

![amp_macom_vga: stages 4 and 6 take 51% to 81% of a run. Simulation, GLB takes 5.0 s. Simulation, STEP takes 6.5 s. Simulation, STL takes 4.8 s. Simulation, OBJ takes 7.5 s. Visual, GLB takes 7.4 s. Visual, OBJ takes 8.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1493b_vna_amp-macom-vga/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 2.0 | 0.2&nbsp;ms | 1.8 | 83&nbsp;ms | 0.3 | 0.2 | 5.0 |
| Simulation, STEP | 0.2 | 0.5 | 2.1 | 0.2&nbsp;ms | 1.8 | 1.4 | 0.2 | 0.2 | 6.5 |
| Simulation, STL | 0.1 | 0.5 | 1.9 | 0.2&nbsp;ms | 1.7 | 0.1 | 0.2 | 0.2 | 4.8 |
| Simulation, OBJ | 0.1 | 0.5 | 2.0 | 0.2&nbsp;ms | 1.8 | 2.6 | 0.2 | 0.2 | 7.5 |
| Visual, GLB | 0.1 | 0.5 | 1.9 | 0.2&nbsp;ms | 4.1 | 54&nbsp;ms | 0.5 | 0.2 | 7.4 |
| Visual, OBJ | 0.1 | 0.5 | 2.0 | 0.2&nbsp;ms | 4.0 | 1.4 | 0.6 | 0.2 | 8.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `amp_macom_vga.kicad_pcb` |
|---|---|
| Folder | breakouts / amp_macom_vga |
| Complexity | 218&nbsp;/&nbsp;1000 (size&nbsp;173, features&nbsp;45) |
| KESE&nbsp;features | through vias, filled zones,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 48, 203, 57 |
| Triangles,&nbsp;simulation | 661,824 in 43 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">347&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">77&nbsp;MB</td><td align="right">369&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">33&nbsp;MB</td><td align="right">335&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">67&nbsp;MB</td><td align="right">476&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">361&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">39&nbsp;MB</td><td align="right">352&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1494. attenuator

![attenuator: stages 4 and 6 take 48% to 79% of a run. Simulation, GLB takes 3.5 s. Simulation, STEP takes 4.7 s. Simulation, STL takes 3.7 s. Simulation, OBJ takes 5.5 s. Visual, GLB takes 5.3 s. Visual, OBJ takes 6.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1494b_vna_attenuator/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.4 | 0.2&nbsp;ms | 1.1 | 54&nbsp;ms | 0.2 | 0.2 | 3.5 |
| Simulation, STEP | 0.1 | 0.4 | 1.5 | 0.2&nbsp;ms | 1.1 | 1.2 | 0.2 | 0.2 | 4.7 |
| Simulation, STL | 0.2 | 0.4 | 1.5 | 0.2&nbsp;ms | 1.1 | 81&nbsp;ms | 0.2 | 0.2 | 3.7 |
| Simulation, OBJ | 0.1 | 0.4 | 1.5 | 0.2&nbsp;ms | 1.1 | 1.9 | 0.2 | 0.2 | 5.5 |
| Visual, GLB | 0.1 | 0.4 | 1.4 | 0.3&nbsp;ms | 2.8 | 34&nbsp;ms | 0.3 | 0.2 | 5.3 |
| Visual, OBJ | 0.2 | 0.4 | 1.4 | 0.3&nbsp;ms | 2.7 | 1.2 | 0.2 | 0.2 | 6.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `attenuator.kicad_pcb` |
|---|---|
| Folder | breakouts / attenuator |
| Complexity | 204&nbsp;/&nbsp;1000 (size&nbsp;169, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 36, 232, 41 |
| Triangles,&nbsp;simulation | 357,776 in 47 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">247&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">47&nbsp;MB</td><td align="right">264&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">18&nbsp;MB</td><td align="right">236&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">37&nbsp;MB</td><td align="right">290&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.9&nbsp;MB</td><td align="right">248&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">23&nbsp;MB</td><td align="right">240&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1495. balun

![balun: stages 4 and 6 take 48% to 80% of a run. Simulation, GLB takes 1.8 s. Simulation, STEP takes 2.8 s. Simulation, STL takes 1.8 s. Simulation, OBJ takes 2.6 s. Visual, GLB takes 2.4 s. Visual, OBJ takes 2.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1495b_vna_balun/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 94&nbsp;ms | 0.1 | 0.6 | 0.1&nbsp;ms | 0.6 | 24&nbsp;ms | 77&nbsp;ms | 0.3 | 1.8 |
| Simulation, STEP | 98&nbsp;ms | 0.1 | 0.6 | 0.1&nbsp;ms | 0.7 | 0.9 | 84&nbsp;ms | 0.2 | 2.8 |
| Simulation, STL | 87&nbsp;ms | 0.1 | 0.6 | 0.1&nbsp;ms | 0.7 | 35&nbsp;ms | 80&nbsp;ms | 0.2 | 1.8 |
| Simulation, OBJ | 0.1 | 0.1 | 0.7 | 0.1&nbsp;ms | 0.6 | 0.8 | 78&nbsp;ms | 0.2 | 2.6 |
| Visual, GLB | 83&nbsp;ms | 90&nbsp;ms | 0.6 | 0.2&nbsp;ms | 1.3 | 14&nbsp;ms | 0.1 | 0.2 | 2.4 |
| Visual, OBJ | 88&nbsp;ms | 93&nbsp;ms | 0.6 | 0.1&nbsp;ms | 1.3 | 0.4 | 0.1 | 0.2 | 2.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `balun.kicad_pcb` |
|---|---|
| Folder | breakouts / balun |
| Complexity | 121&nbsp;/&nbsp;1000 (size&nbsp;81, features&nbsp;40) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 7, 12, 0 |
| Triangles,&nbsp;simulation | 133,858 in 18 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.7&nbsp;MB</td><td align="right">196&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">24&nbsp;MB</td><td align="right">201&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">6.7&nbsp;MB</td><td align="right">199&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">13&nbsp;MB</td><td align="right">188&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">2.8&nbsp;MB</td><td align="right">157&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">7.7&nbsp;MB</td><td align="right">158&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1496. bias_controller

![bias_controller: stages 4 and 6 take 58% to 82% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 15 s. Simulation, STL takes 12 s. Simulation, OBJ takes 16 s. Visual, GLB takes 17 s. Visual, OBJ takes 21 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1496b_vna_bias-controller/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.2 | 4.2 | 0.5&nbsp;ms | 4.8 | 0.2 | 0.4 | 0.3 | 11.4 |
| Simulation, STEP | 0.4 | 1.2 | 4.4 | 0.4&nbsp;ms | 4.6 | 4.0 | 0.4 | 0.2 | 15.3 |
| Simulation, STL | 0.5 | 1.2 | 4.5 | 0.4&nbsp;ms | 4.9 | 0.5 | 0.4 | 0.3 | 12.2 |
| Simulation, OBJ | 0.5 | 1.2 | 4.3 | 0.4&nbsp;ms | 5.1 | 4.4 | 0.3 | 0.3 | 16.1 |
| Visual, GLB | 0.5 | 1.1 | 4.3 | 0.5&nbsp;ms | 9.7 | 0.1 | 1.0 | 0.2 | 17.1 |
| Visual, OBJ | 0.5 | 1.1 | 4.1 | 0.4&nbsp;ms | 9.6 | 3.8 | 1.4 | 0.2 | 20.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `bias_controller.kicad_pcb` |
|---|---|
| Folder | breakouts / bias_controller / bias_controller |
| Complexity | 134&nbsp;/&nbsp;1000 (size&nbsp;114, features&nbsp;20) |
| KESE&nbsp;features | slotted holes, rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20231212) |
| Parts,&nbsp;tracks,&nbsp;vias | 201, 0, 0 |
| Triangles,&nbsp;simulation | 939,990 in 182 parts |
| Note | mostly unrouted |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">544&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">180&nbsp;MB</td><td align="right">637&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">47&nbsp;MB</td><td align="right">519&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">96&nbsp;MB</td><td align="right">642&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">603&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">81&nbsp;MB</td><td align="right">636&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1497. boosterpack

![boosterpack: stages 4 and 6 take 54% to 85% of a run. Simulation, GLB takes 7.8 s. Simulation, STEP takes 9.7 s. Simulation, STL takes 7.8 s. Simulation, OBJ takes 12 s. Visual, GLB takes 10 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1497b_vna_boosterpack/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 3.8 | 0.3&nbsp;ms | 2.5 | 0.1 | 0.4 | 0.2 | 7.8 |
| Simulation, STEP | 0.2 | 0.6 | 3.7 | 0.3&nbsp;ms | 2.5 | 2.2 | 0.4 | 0.2 | 9.7 |
| Simulation, STL | 0.2 | 0.6 | 3.8 | 0.3&nbsp;ms | 2.4 | 0.2 | 0.4 | 0.3 | 7.8 |
| Simulation, OBJ | 0.2 | 0.6 | 3.8 | 0.2&nbsp;ms | 2.5 | 4.1 | 0.4 | 0.2 | 11.7 |
| Visual, GLB | 0.2 | 0.6 | 3.8 | 0.5&nbsp;ms | 5.1 | 66&nbsp;ms | 0.5 | 0.2 | 10.4 |
| Visual, OBJ | 0.2 | 0.6 | 3.8 | 0.3&nbsp;ms | 5.0 | 2.2 | 0.6 | 0.2 | 12.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `boosterpack.kicad_pcb` |
|---|---|
| Folder | breakouts / boosterpack |
| Complexity | 177&nbsp;/&nbsp;1000 (size&nbsp;142, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 24, 227, 7 |
| Triangles,&nbsp;simulation | 696,784 in 52 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">24&nbsp;MB</td><td align="right">365&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">117&nbsp;MB</td><td align="right">387&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">35&nbsp;MB</td><td align="right">336&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">71&nbsp;MB</td><td align="right">503&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">386&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">41&nbsp;MB</td><td align="right">384&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1498. clk_lo_buffer

![clk_lo_buffer: stages 4 and 6 take 51% to 77% of a run. Simulation, GLB takes 2.9 s. Simulation, STEP takes 4.0 s. Simulation, STL takes 2.8 s. Simulation, OBJ takes 3.9 s. Visual, GLB takes 4.4 s. Visual, OBJ takes 4.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1498b_vna_clk-lo-buffer/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.1 | 0.2&nbsp;ms | 1.0 | 30&nbsp;ms | 0.1 | 0.2 | 2.9 |
| Simulation, STEP | 0.1 | 0.4 | 1.1 | 0.2&nbsp;ms | 0.9 | 1.1 | 0.1 | 0.2 | 4.0 |
| Simulation, STL | 0.1 | 0.3 | 1.1 | 0.2&nbsp;ms | 0.9 | 58&nbsp;ms | 88&nbsp;ms | 0.2 | 2.8 |
| Simulation, OBJ | 0.1 | 0.3 | 1.0 | 0.2&nbsp;ms | 1.0 | 1.1 | 84&nbsp;ms | 0.2 | 3.9 |
| Visual, GLB | 0.1 | 0.3 | 1.1 | 0.3&nbsp;ms | 2.3 | 36&nbsp;ms | 0.3 | 0.2 | 4.4 |
| Visual, OBJ | 0.1 | 0.3 | 1.1 | 0.1&nbsp;ms | 2.0 | 0.9 | 0.2 | 0.2 | 4.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `clk_lo_buffer.kicad_pcb` |
|---|---|
| Folder | breakouts / clk_lo_buffer |
| Complexity | 214&nbsp;/&nbsp;1000 (size&nbsp;159, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 44, 318, 48 |
| Triangles,&nbsp;simulation | 214,972 in 36 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">7.9&nbsp;MB</td><td align="right">239&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">31&nbsp;MB</td><td align="right">258&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">11&nbsp;MB</td><td align="right">233&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">237&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">6.6&nbsp;MB</td><td align="right">224&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">19&nbsp;MB</td><td align="right">225&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1499. coupler_test

![coupler_test: stages 4 and 6 take 55% to 85% of a run. Simulation, GLB takes 6.2 s. Simulation, STEP takes 7.6 s. Simulation, STL takes 6.2 s. Simulation, OBJ takes 8.9 s. Visual, GLB takes 6.8 s. Visual, OBJ takes 8.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1499b_vna_coupler-test/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.5 | 2.8 | 0.2&nbsp;ms | 2.2 | 84&nbsp;ms | 0.3 | 0.2 | 6.2 |
| Simulation, STEP | 0.1 | 0.4 | 2.6 | 0.3&nbsp;ms | 2.3 | 1.6 | 0.3 | 0.2 | 7.6 |
| Simulation, STL | 0.1 | 0.5 | 2.8 | 0.4&nbsp;ms | 2.2 | 0.1 | 0.3 | 0.2 | 6.2 |
| Simulation, OBJ | 0.1 | 0.5 | 2.6 | 0.4&nbsp;ms | 2.2 | 3.0 | 0.3 | 0.2 | 8.9 |
| Visual, GLB | 0.1 | 0.5 | 2.7 | 0.3&nbsp;ms | 3.1 | 30&nbsp;ms | 0.2 | 0.2 | 6.8 |
| Visual, OBJ | 0.1 | 0.4 | 2.8 | 0.6&nbsp;ms | 3.2 | 1.1 | 0.2 | 0.2 | 8.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `coupler_test.kicad_pcb` |
|---|---|
| Folder | breakouts / coupler_test |
| Complexity | 120&nbsp;/&nbsp;1000 (size&nbsp;90, features&nbsp;30) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 4, 10, 0 |
| Triangles,&nbsp;simulation | 592,560 in 19 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">354&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">60&nbsp;MB</td><td align="right">389&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">30&nbsp;MB</td><td align="right">345&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">58&nbsp;MB</td><td align="right">409&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.2&nbsp;MB</td><td align="right">296&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">21&nbsp;MB</td><td align="right">290&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1500. cpw_test

![cpw_test: stages 4 and 6 take 43% to 63% of a run. Simulation, GLB takes 0.8 s. Simulation, STEP takes 1.0 s. Simulation, STL takes 0.8 s. Simulation, OBJ takes 1.0 s. Visual, GLB takes 1.0 s. Visual, OBJ takes 1.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1500b_vna_breakouts-cpw-test_cpw-test/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 62&nbsp;ms | 46&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 8&nbsp;ms | 29&nbsp;ms | 0.2 | 0.8 |
| Simulation, STEP | 67&nbsp;ms | 55&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 0.2 | 32&nbsp;ms | 0.2 | 1.0 |
| Simulation, STL | 71&nbsp;ms | 54&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 13&nbsp;ms | 29&nbsp;ms | 0.2 | 0.8 |
| Simulation, OBJ | 71&nbsp;ms | 54&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.3 | 0.2 | 32&nbsp;ms | 0.2 | 1.0 |
| Visual, GLB | 71&nbsp;ms | 60&nbsp;ms | 0.2 | 0.1&nbsp;ms | 0.5 | 5&nbsp;ms | 43&nbsp;ms | 0.2 | 1.0 |
| Visual, OBJ | 74&nbsp;ms | 50&nbsp;ms | 0.2 | 0.2&nbsp;ms | 0.5 | 97&nbsp;ms | 41&nbsp;ms | 0.2 | 1.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `cpw_test.kicad_pcb` |
|---|---|
| Folder | breakouts / cpw_test |
| Complexity | 78&nbsp;/&nbsp;1000 (size&nbsp;68, features&nbsp;10) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 3, 0 |
| Triangles,&nbsp;simulation | 40,844 in 14 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.3&nbsp;MB</td><td align="right">65&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">4.1&nbsp;MB</td><td align="right">69&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">2.0&nbsp;MB</td><td align="right">66&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.7&nbsp;MB</td><td align="right">74&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">731&nbsp;kB</td><td align="right">95&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">2.0&nbsp;MB</td><td align="right">94&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1501. crystal_filter

![crystal_filter: stages 4 and 6 take 46% to 77% of a run. Simulation, GLB takes 1.4 s. Simulation, STEP takes 2.1 s. Simulation, STL takes 1.5 s. Simulation, OBJ takes 2.0 s. Visual, GLB takes 2.0 s. Visual, OBJ takes 2.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1501b_vna_crystal-filter/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 91&nbsp;ms | 96&nbsp;ms | 0.4 | 0.1&nbsp;ms | 0.5 | 17&nbsp;ms | 51&nbsp;ms | 0.2 | 1.4 |
| Simulation, STEP | 81&nbsp;ms | 0.1 | 0.5 | 0.2&nbsp;ms | 0.5 | 0.7 | 53&nbsp;ms | 0.2 | 2.1 |
| Simulation, STL | 0.1 | 96&nbsp;ms | 0.4 | 0.1&nbsp;ms | 0.5 | 23&nbsp;ms | 57&nbsp;ms | 0.2 | 1.5 |
| Simulation, OBJ | 80&nbsp;ms | 0.1 | 0.4 | 0.1&nbsp;ms | 0.5 | 0.6 | 63&nbsp;ms | 0.2 | 2.0 |
| Visual, GLB | 84&nbsp;ms | 0.1 | 0.4 | 0.1&nbsp;ms | 1.1 | 11&nbsp;ms | 77&nbsp;ms | 0.2 | 2.0 |
| Visual, OBJ | 86&nbsp;ms | 0.1 | 0.5 | 0.1&nbsp;ms | 1.0 | 0.3 | 67&nbsp;ms | 0.2 | 2.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `crystal_filter.kicad_pcb` |
|---|---|
| Folder | breakouts / crystal_filter |
| Complexity | 146&nbsp;/&nbsp;1000 (size&nbsp;111, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 9, 31, 12 |
| Triangles,&nbsp;simulation | 99,888 in 15 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">3.6&nbsp;MB</td><td align="right">178&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">15&nbsp;MB</td><td align="right">185&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">5.0&nbsp;MB</td><td align="right">179&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.8&nbsp;MB</td><td align="right">181&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">2.2&nbsp;MB</td><td align="right">157&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.1&nbsp;MB</td><td align="right">158&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1502. demod_breakout

![demod_breakout: stages 4 and 6 take 49% to 81% of a run. Simulation, GLB takes 5.8 s. Simulation, STEP takes 7.6 s. Simulation, STL takes 6.0 s. Simulation, OBJ takes 9.1 s. Visual, GLB takes 8.8 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1502b_vna_demod-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 2.6 | 0.4&nbsp;ms | 1.8 | 97&nbsp;ms | 0.3 | 0.2 | 5.8 |
| Simulation, STEP | 0.2 | 0.7 | 2.6 | 0.3&nbsp;ms | 1.9 | 1.7 | 0.3 | 0.2 | 7.6 |
| Simulation, STL | 0.2 | 0.6 | 2.7 | 0.3&nbsp;ms | 1.9 | 0.2 | 0.3 | 0.2 | 6.0 |
| Simulation, OBJ | 0.2 | 0.6 | 2.5 | 0.3&nbsp;ms | 1.9 | 3.3 | 0.3 | 0.2 | 9.1 |
| Visual, GLB | 0.2 | 0.7 | 2.6 | 0.3&nbsp;ms | 4.5 | 60&nbsp;ms | 0.5 | 0.2 | 8.8 |
| Visual, OBJ | 0.2 | 0.6 | 2.7 | 0.3&nbsp;ms | 4.4 | 2.1 | 0.5 | 0.2 | 10.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `demod_breakout.kicad_pcb` |
|---|---|
| Folder | breakouts / demod_breakout |
| Complexity | 220&nbsp;/&nbsp;1000 (size&nbsp;185, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 67, 417, 72 |
| Triangles,&nbsp;simulation | 649,436 in 62 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">330&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">85&nbsp;MB</td><td align="right">374&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">32&nbsp;MB</td><td align="right">340&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">67&nbsp;MB</td><td align="right">482&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">371&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">41&nbsp;MB</td><td align="right">371&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1503. filter_bank

![filter_bank: stages 4 and 6 take 49% to 78% of a run. Simulation, GLB takes 3.7 s. Simulation, STEP takes 5.1 s. Simulation, STL takes 4.0 s. Simulation, OBJ takes 5.5 s. Visual, GLB takes 5.7 s. Visual, OBJ takes 7.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1503b_vna_filter-bank/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.4 | 1.5 | 0.2&nbsp;ms | 1.2 | 69&nbsp;ms | 0.2 | 0.2 | 3.7 |
| Simulation, STEP | 0.2 | 0.4 | 1.7 | 0.3&nbsp;ms | 1.2 | 1.2 | 0.2 | 0.2 | 5.1 |
| Simulation, STL | 0.1 | 0.4 | 1.5 | 0.3&nbsp;ms | 1.3 | 0.1 | 0.2 | 0.2 | 4.0 |
| Simulation, OBJ | 0.2 | 0.4 | 1.5 | 0.2&nbsp;ms | 1.2 | 1.9 | 0.2 | 0.2 | 5.5 |
| Visual, GLB | 0.2 | 0.4 | 1.5 | 0.3&nbsp;ms | 3.0 | 36&nbsp;ms | 0.4 | 0.3 | 5.7 |
| Visual, OBJ | 0.1 | 0.4 | 1.5 | 0.2&nbsp;ms | 3.2 | 1.3 | 0.3 | 0.2 | 7.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `filter_bank.kicad_pcb` |
|---|---|
| Folder | breakouts / filter_breakout |
| Complexity | 210&nbsp;/&nbsp;1000 (size&nbsp;175, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 36, 361, 53 |
| Triangles,&nbsp;simulation | 321,342 in 56 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">237&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">40&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">16&nbsp;MB</td><td align="right">253&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">33&nbsp;MB</td><td align="right">269&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.3&nbsp;MB</td><td align="right">235&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">21&nbsp;MB</td><td align="right">237&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1504. trl_thru

![trl_thru: stages 4 and 6 take 48% to 74% of a run. Simulation, GLB takes 2.4 s. Simulation, STEP takes 3.2 s. Simulation, STL takes 2.5 s. Simulation, OBJ takes 3.4 s. Visual, GLB takes 3.1 s. Visual, OBJ takes 3.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1504b_vna_breakouts-hmc576-breakout_trl-thru/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 91&nbsp;ms | 0.3 | 0.8 | 0.2&nbsp;ms | 0.9 | 39&nbsp;ms | 0.1 | 0.2 | 2.4 |
| Simulation, STEP | 96&nbsp;ms | 0.3 | 0.7 | 0.1&nbsp;ms | 0.8 | 0.9 | 0.1 | 0.2 | 3.2 |
| Simulation, STL | 92&nbsp;ms | 0.3 | 0.8 | 0.1&nbsp;ms | 0.9 | 70&nbsp;ms | 0.1 | 0.3 | 2.5 |
| Simulation, OBJ | 98&nbsp;ms | 0.3 | 0.8 | 0.1&nbsp;ms | 0.9 | 1.1 | 0.1 | 0.2 | 3.4 |
| Visual, GLB | 0.1 | 0.3 | 0.9 | 0.1&nbsp;ms | 1.5 | 19&nbsp;ms | 0.1 | 0.2 | 3.1 |
| Visual, OBJ | 93&nbsp;ms | 0.3 | 0.8 | 0.1&nbsp;ms | 1.6 | 0.6 | 0.1 | 0.2 | 3.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `trl_thru.kicad_pcb` |
|---|---|
| Folder | breakouts / hmc576_breakout |
| Complexity | 185&nbsp;/&nbsp;1000 (size&nbsp;140, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 10, 55, 27 |
| Triangles,&nbsp;simulation | 254,354 in 18 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">8.6&nbsp;MB</td><td align="right">236&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">27&nbsp;MB</td><td align="right">244&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">13&nbsp;MB</td><td align="right">254&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">25&nbsp;MB</td><td align="right">229&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.1&nbsp;MB</td><td align="right">184&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">12&nbsp;MB</td><td align="right">184&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1505. hyperram_3p3v

![hyperram_3p3v: stages 4 and 6 take 49% to 80% of a run. Simulation, GLB takes 3.2 s. Simulation, STEP takes 4.1 s. Simulation, STL takes 3.2 s. Simulation, OBJ takes 4.6 s. Visual, GLB takes 4.0 s. Visual, OBJ takes 4.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1505b_vna_hyperram-3p3v/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 84&nbsp;ms | 0.3 | 1.3 | 0.2&nbsp;ms | 1.1 | 51&nbsp;ms | 0.2 | 0.2 | 3.2 |
| Simulation, STEP | 92&nbsp;ms | 0.3 | 1.3 | 0.2&nbsp;ms | 1.0 | 1.0 | 0.2 | 0.2 | 4.1 |
| Simulation, STL | 0.1 | 0.3 | 1.3 | 0.2&nbsp;ms | 1.1 | 81&nbsp;ms | 0.2 | 0.2 | 3.2 |
| Simulation, OBJ | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 1.0 | 1.5 | 0.2 | 0.2 | 4.6 |
| Visual, GLB | 91&nbsp;ms | 0.3 | 1.3 | 0.2&nbsp;ms | 1.9 | 24&nbsp;ms | 0.2 | 0.2 | 4.0 |
| Visual, OBJ | 96&nbsp;ms | 0.3 | 1.2 | 0.5&nbsp;ms | 1.8 | 0.6 | 0.1 | 0.2 | 4.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `hyperram_3p3v.kicad_pcb` |
|---|---|
| Folder | breakouts / hyperram / hyperram_3p3v |
| Complexity | 184&nbsp;/&nbsp;1000 (size&nbsp;139, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 6, 129, 16 |
| Triangles,&nbsp;simulation | 371,994 in 27 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">245&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">48&nbsp;MB</td><td align="right">263&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">19&nbsp;MB</td><td align="right">246&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">37&nbsp;MB</td><td align="right">289&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.4&nbsp;MB</td><td align="right">225&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">16&nbsp;MB</td><td align="right">224&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1506. launchpad_synthcontrol

![launchpad_synthcontrol: stages 4 and 6 take 55% to 83% of a run. Simulation, GLB takes 5.4 s. Simulation, STEP takes 6.9 s. Simulation, STL takes 5.6 s. Simulation, OBJ takes 8.2 s. Visual, GLB takes 7.5 s. Visual, OBJ takes 8.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1506b_vna_launchpad-synthcontrol/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.4 | 2.5 | 0.4&nbsp;ms | 1.8 | 77&nbsp;ms | 0.2 | 0.2 | 5.4 |
| Simulation, STEP | 0.1 | 0.5 | 2.4 | 0.6&nbsp;ms | 1.8 | 1.7 | 0.2 | 0.3 | 6.9 |
| Simulation, STL | 0.1 | 0.4 | 2.5 | 0.4&nbsp;ms | 1.8 | 0.2 | 0.3 | 0.3 | 5.6 |
| Simulation, OBJ | 0.1 | 0.5 | 2.6 | 0.4&nbsp;ms | 1.9 | 2.7 | 0.3 | 0.2 | 8.2 |
| Visual, GLB | 0.1 | 0.4 | 2.5 | 0.4&nbsp;ms | 3.7 | 60&nbsp;ms | 0.5 | 0.2 | 7.5 |
| Visual, OBJ | 0.1 | 0.4 | 2.6 | 0.4&nbsp;ms | 3.7 | 1.5 | 0.4 | 0.2 | 8.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `launchpad_synthcontrol.kicad_pcb` |
|---|---|
| Folder | breakouts / launchpad_synthcontrol |
| Complexity | 147&nbsp;/&nbsp;1000 (size&nbsp;132, features&nbsp;15) |
| KESE&nbsp;features | through vias |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 308, 84 |
| Triangles,&nbsp;simulation | 603,278 in 50 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">21&nbsp;MB</td><td align="right">306&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">92&nbsp;MB</td><td align="right">354&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">30&nbsp;MB</td><td align="right">309&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">61&nbsp;MB</td><td align="right">435&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">342&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">35&nbsp;MB</td><td align="right">345&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1507. maam_011109

![maam_011109: stages 4 and 6 take 46% to 78% of a run. Simulation, GLB takes 2.9 s. Simulation, STEP takes 3.9 s. Simulation, STL takes 3.0 s. Simulation, OBJ takes 4.4 s. Visual, GLB takes 3.8 s. Visual, OBJ takes 4.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1507b_vna_maam-011109/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.0 | 0.1&nbsp;ms | 1.0 | 45&nbsp;ms | 0.2 | 0.2 | 2.9 |
| Simulation, STEP | 0.1 | 0.3 | 1.1 | 0.1&nbsp;ms | 1.0 | 1.1 | 0.1 | 0.2 | 3.9 |
| Simulation, STL | 0.1 | 0.3 | 1.2 | 0.1&nbsp;ms | 1.0 | 68&nbsp;ms | 0.2 | 0.2 | 3.0 |
| Simulation, OBJ | 0.1 | 0.3 | 1.1 | 0.1&nbsp;ms | 1.0 | 1.6 | 0.2 | 0.2 | 4.4 |
| Visual, GLB | 0.1 | 0.3 | 1.1 | 0.1&nbsp;ms | 1.9 | 26&nbsp;ms | 0.2 | 0.3 | 3.8 |
| Visual, OBJ | 97&nbsp;ms | 0.3 | 1.0 | 0.2&nbsp;ms | 1.7 | 0.6 | 0.1 | 0.2 | 4.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `maam_011109.kicad_pcb` |
|---|---|
| Folder | breakouts / maam_011109 / maam_011109 |
| Complexity | 188&nbsp;/&nbsp;1000 (size&nbsp;143, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 8, 51, 47 |
| Triangles,&nbsp;simulation | 316,726 in 23 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">247&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">31&nbsp;MB</td><td align="right">265&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">16&nbsp;MB</td><td align="right">268&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">31&nbsp;MB</td><td align="right">271&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.4&nbsp;MB</td><td align="right">210&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">12&nbsp;MB</td><td align="right">214&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1508. maam_011109_bias

![maam_011109_bias: stages 4 and 6 take 49% to 77% of a run. Simulation, GLB takes 4.6 s. Simulation, STEP takes 5.7 s. Simulation, STL takes 4.4 s. Simulation, OBJ takes 6.3 s. Visual, GLB takes 6.8 s. Visual, OBJ takes 7.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1508b_vna_maam-011109-bias/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 1.7 | 0.3&nbsp;ms | 1.4 | 61&nbsp;ms | 0.2 | 0.3 | 4.6 |
| Simulation, STEP | 0.2 | 0.7 | 1.8 | 0.2&nbsp;ms | 1.3 | 1.3 | 0.2 | 0.2 | 5.7 |
| Simulation, STL | 0.2 | 0.7 | 1.7 | 0.3&nbsp;ms | 1.3 | 0.1 | 0.2 | 0.2 | 4.4 |
| Simulation, OBJ | 0.2 | 0.7 | 1.8 | 0.4&nbsp;ms | 1.3 | 1.9 | 0.2 | 0.3 | 6.3 |
| Visual, GLB | 0.2 | 0.7 | 1.8 | 0.2&nbsp;ms | 3.5 | 47&nbsp;ms | 0.4 | 0.2 | 6.8 |
| Visual, OBJ | 0.2 | 0.7 | 1.8 | 0.3&nbsp;ms | 3.3 | 1.2 | 0.3 | 0.3 | 7.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `maam_011109_bias.kicad_pcb` |
|---|---|
| Folder | breakouts / maam_011109_bias |
| Complexity | 202&nbsp;/&nbsp;1000 (size&nbsp;157, features&nbsp;45) |
| KESE&nbsp;features | through vias, filled zones,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 48, 287, 36 |
| Triangles,&nbsp;simulation | 368,514 in 38 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">279&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">63&nbsp;MB</td><td align="right">305&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">18&nbsp;MB</td><td align="right">288&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">38&nbsp;MB</td><td align="right">315&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">9.6&nbsp;MB</td><td align="right">274&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">28&nbsp;MB</td><td align="right">281&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1509. mixer_breakout

![mixer_breakout: stages 4 and 6 take 51% to 80% of a run. Simulation, GLB takes 3.1 s. Simulation, STEP takes 4.1 s. Simulation, STL takes 3.0 s. Simulation, OBJ takes 4.5 s. Visual, GLB takes 4.0 s. Visual, OBJ takes 4.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1509b_vna_mixer-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 1.0 | 52&nbsp;ms | 0.2 | 0.2 | 3.1 |
| Simulation, STEP | 0.1 | 0.3 | 1.2 | 0.1&nbsp;ms | 1.0 | 1.1 | 0.1 | 0.2 | 4.1 |
| Simulation, STL | 0.1 | 0.3 | 1.2 | 0.1&nbsp;ms | 1.0 | 68&nbsp;ms | 0.1 | 0.2 | 3.0 |
| Simulation, OBJ | 0.1 | 0.3 | 1.3 | 0.2&nbsp;ms | 1.0 | 1.5 | 0.1 | 0.2 | 4.5 |
| Visual, GLB | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 2.0 | 23&nbsp;ms | 0.1 | 0.3 | 4.0 |
| Visual, OBJ | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 2.0 | 0.8 | 0.2 | 0.2 | 4.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `mixer_breakout.kicad_pcb` |
|---|---|
| Folder | breakouts / mixer_breakout |
| Complexity | 170&nbsp;/&nbsp;1000 (size&nbsp;135, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 11, 88, 2 |
| Triangles,&nbsp;simulation | 306,878 in 24 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">10&nbsp;MB</td><td align="right">244&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">35&nbsp;MB</td><td align="right">267&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">15&nbsp;MB</td><td align="right">242&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">31&nbsp;MB</td><td align="right">253&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.3&nbsp;MB</td><td align="right">211&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">15&nbsp;MB</td><td align="right">214&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1510. pe42520_breakout

![pe42520_breakout: stages 4 and 6 take 52% to 85% of a run. Simulation, GLB takes 5.6 s. Simulation, STEP takes 6.8 s. Simulation, STL takes 5.6 s. Simulation, OBJ takes 8.8 s. Visual, GLB takes 7.9 s. Visual, OBJ takes 9.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1510b_vna_pe42520-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.5 | 2.1 | 0.2&nbsp;ms | 2.2 | 0.1 | 0.3 | 0.2 | 5.6 |
| Simulation, STEP | 0.1 | 0.5 | 2.1 | 0.2&nbsp;ms | 2.3 | 1.4 | 0.3 | 0.2 | 6.8 |
| Simulation, STL | 0.1 | 0.5 | 2.1 | 0.2&nbsp;ms | 2.2 | 0.1 | 0.3 | 0.2 | 5.6 |
| Simulation, OBJ | 0.1 | 0.6 | 2.2 | 0.2&nbsp;ms | 2.3 | 3.0 | 0.3 | 0.2 | 8.8 |
| Visual, GLB | 0.1 | 0.5 | 1.9 | 0.2&nbsp;ms | 4.8 | 43&nbsp;ms | 0.3 | 0.2 | 7.9 |
| Visual, OBJ | 0.1 | 0.6 | 2.3 | 0.2&nbsp;ms | 4.6 | 1.3 | 0.4 | 0.2 | 9.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `pe42520_breakout.kicad_pcb` |
|---|---|
| Folder | breakouts / pe42540_breakout |
| Complexity | 210&nbsp;/&nbsp;1000 (size&nbsp;190, features&nbsp;20) |
| KESE&nbsp;features | filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 19, 83, 0 |
| Triangles,&nbsp;simulation | 614,274 in 30 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">21&nbsp;MB</td><td align="right">344&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">46&nbsp;MB</td><td align="right">413&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">31&nbsp;MB</td><td align="right">348&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">61&nbsp;MB</td><td align="right">450&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">9.2&nbsp;MB</td><td align="right">314&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">27&nbsp;MB</td><td align="right">315&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1511. pe42543_breakout

![pe42543_breakout: stages 4 and 6 take 51% to 80% of a run. Simulation, GLB takes 4.3 s. Simulation, STEP takes 5.6 s. Simulation, STL takes 4.3 s. Simulation, OBJ takes 6.2 s. Visual, GLB takes 4.9 s. Visual, OBJ takes 5.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1511b_vna_pe42543-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.5 | 1.6 | 0.2&nbsp;ms | 1.7 | 59&nbsp;ms | 0.2 | 0.2 | 4.3 |
| Simulation, STEP | 0.2 | 0.6 | 1.6 | 0.2&nbsp;ms | 1.6 | 1.2 | 0.2 | 0.2 | 5.6 |
| Simulation, STL | 0.2 | 0.5 | 1.6 | 0.2&nbsp;ms | 1.6 | 0.1 | 0.2 | 0.2 | 4.3 |
| Simulation, OBJ | 0.1 | 0.5 | 1.7 | 0.2&nbsp;ms | 1.5 | 2.0 | 0.2 | 0.2 | 6.2 |
| Visual, GLB | 0.1 | 0.4 | 1.6 | 0.3&nbsp;ms | 2.4 | 29&nbsp;ms | 0.2 | 0.2 | 4.9 |
| Visual, OBJ | 0.1 | 0.5 | 1.7 | 0.2&nbsp;ms | 2.4 | 0.8 | 0.2 | 0.2 | 5.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `pe42543_breakout.kicad_pcb` |
|---|---|
| Folder | breakouts / pe42543_breakout |
| Complexity | 197&nbsp;/&nbsp;1000 (size&nbsp;152, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 21, 106, 23 |
| Triangles,&nbsp;simulation | 427,902 in 35 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">279&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">45&nbsp;MB</td><td align="right">315&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">21&nbsp;MB</td><td align="right">276&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">43&nbsp;MB</td><td align="right">345&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">6.0&nbsp;MB</td><td align="right">240&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">18&nbsp;MB</td><td align="right">238&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 1512. powerdet_breakout

![powerdet_breakout: stages 4 and 6 take 48% to 79% of a run. Simulation, GLB takes 2.1 s. Simulation, STEP takes 2.9 s. Simulation, STL takes 2.2 s. Simulation, OBJ takes 2.9 s. Visual, GLB takes 2.9 s. Visual, OBJ takes 3.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1512b_vna_powerdet-breakout/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.8 | 0.2&nbsp;ms | 0.7 | 29&nbsp;ms | 91&nbsp;ms | 0.2 | 2.1 |
| Simulation, STEP | 0.1 | 0.2 | 0.7 | 0.2&nbsp;ms | 0.7 | 0.9 | 93&nbsp;ms | 0.2 | 2.9 |
| Simulation, STL | 0.1 | 0.2 | 0.8 | 0.3&nbsp;ms | 0.7 | 49&nbsp;ms | 0.1 | 0.2 | 2.2 |
| Simulation, OBJ | 0.1 | 0.2 | 0.7 | 0.2&nbsp;ms | 0.7 | 0.9 | 83&nbsp;ms | 0.2 | 2.9 |
| Visual, GLB | 0.1 | 0.2 | 0.7 | 0.2&nbsp;ms | 1.6 | 20&nbsp;ms | 0.1 | 0.2 | 2.9 |
| Visual, OBJ | 0.1 | 0.2 | 0.8 | 0.2&nbsp;ms | 1.7 | 0.5 | 0.2 | 0.2 | 3.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [loxodes/vna](https://github.com/loxodes/vna)<br>Board: `powerdet_breakout.kicad_pcb` |
|---|---|
| Folder | breakouts / powerdet_breakout |
| Complexity | 193&nbsp;/&nbsp;1000 (size&nbsp;158, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 26, 157, 25 |
| Triangles,&nbsp;simulation | 202,000 in 30 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">7.2&nbsp;MB</td><td align="right">210&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">26&nbsp;MB</td><td align="right">223&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">10&nbsp;MB</td><td align="right">208&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">20&nbsp;MB</td><td align="right">209&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.7&nbsp;MB</td><td align="right">186&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">13&nbsp;MB</td><td align="right">187&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [Corpus Page 13](Corpus-Testing-13.md) | [Corpus Page 15](Corpus-Testing-15.md) |
