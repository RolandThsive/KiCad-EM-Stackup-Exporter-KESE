# 23.3 Corpus Testing 3: antevens To antmicro

Part 3 of 29 of [Corpus Testing](../Corpus-Testing.md): every board of these projects, six runs each, one file format a run, as [Corpus Testing](../Corpus-Testing.md) describes.

## 23.3.1 CommonCathode60A

![CommonCathode60A: stages 4 and 6 take 47% to 79% of a run. Simulation, GLB takes 10 s. Simulation, STEP takes 13 s. Simulation, STL takes 10 s. Simulation, OBJ takes 17 s. Visual, GLB takes 13 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/boatcontrol_CommonCathode60A.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 1.3 | 4.1 | 0.4&nbsp;ms | 3.3 | 0.2 | 0.6 | 0.3 | 10.0 |
| Simulation, STEP | 0.2 | 1.3 | 4.2 | 0.4&nbsp;ms | 3.3 | 3.3 | 0.6 | 0.2 | 13.2 |
| Simulation, STL | 0.2 | 1.4 | 4.4 | 0.3&nbsp;ms | 3.3 | 0.4 | 0.5 | 0.2 | 10.4 |
| Simulation, OBJ | 0.3 | 1.3 | 4.3 | 0.4&nbsp;ms | 3.5 | 6.5 | 0.5 | 0.3 | 16.6 |
| Visual, GLB | 0.2 | 1.3 | 4.4 | 0.3&nbsp;ms | 5.9 | 83&nbsp;ms | 0.8 | 0.3 | 13.0 |
| Visual, OBJ | 0.2 | 1.3 | 4.3 | 0.3&nbsp;ms | 5.6 | 3.1 | 0.8 | 0.3 | 15.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antevens/boatcontrol](https://github.com/antevens/boatcontrol)<br>Board: `CommonCathode60A.kicad_pcb` |
|---|---|
| Folder | addon / CommonCathode60A |
| Complexity | 186&nbsp;/&nbsp;1000 (size&nbsp;156, features&nbsp;30) |
| KESE&nbsp;features | filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 11, 337, 0 |
| Triangles,&nbsp;simulation | 1,116,070 in 46 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">38&nbsp;MB</td><td align="right">391&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">151&nbsp;MB</td><td align="right">477&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">56&nbsp;MB</td><td align="right">402&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">113&nbsp;MB</td><td align="right">772&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">428&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">45&nbsp;MB</td><td align="right">421&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.2 CurrentSensor

![CurrentSensor: stages 4 and 6 take 47% to 74% of a run. Simulation, GLB takes 3.2 s. Simulation, STEP takes 4.2 s. Simulation, STL takes 3.0 s. Simulation, OBJ takes 4.4 s. Visual, GLB takes 4.0 s. Visual, OBJ takes 4.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/boatcontrol_CurrentSensor.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.4 | 1.2 | 0.2&nbsp;ms | 1.0 | 41&nbsp;ms | 0.2 | 0.3 | 3.2 |
| Simulation, STEP | 0.2 | 0.4 | 1.1 | 0.2&nbsp;ms | 0.9 | 1.2 | 0.1 | 0.3 | 4.2 |
| Simulation, STL | 0.1 | 0.4 | 1.2 | 0.2&nbsp;ms | 0.9 | 58&nbsp;ms | 0.1 | 0.3 | 3.0 |
| Simulation, OBJ | 0.1 | 0.4 | 1.1 | 0.1&nbsp;ms | 0.9 | 1.4 | 0.1 | 0.2 | 4.4 |
| Visual, GLB | 0.2 | 0.4 | 1.1 | 0.2&nbsp;ms | 1.9 | 25&nbsp;ms | 0.2 | 0.2 | 4.0 |
| Visual, OBJ | 0.2 | 0.4 | 1.2 | 0.2&nbsp;ms | 1.9 | 0.7 | 0.2 | 0.2 | 4.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antevens/boatcontrol](https://github.com/antevens/boatcontrol)<br>Board: `CurrentSensor.kicad_pcb` |
|---|---|
| Folder | addon / CurrentSensor |
| Complexity | 85&nbsp;/&nbsp;1000 (size&nbsp;50, features&nbsp;35) |
| KESE&nbsp;features | custom pads, rounded,<br>trapezoid or chamfered pads,<br>copper drawings |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 20, 0, 0 |
| Triangles,&nbsp;simulation | 222,452 in 34 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">7.7&nbsp;MB</td><td align="right">221&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">36&nbsp;MB</td><td align="right">237&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">11&nbsp;MB</td><td align="right">215&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">23&nbsp;MB</td><td align="right">215&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.3&nbsp;MB</td><td align="right">189&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">12&nbsp;MB</td><td align="right">197&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.3 NonLatchingNO30A

![NonLatchingNO30A: stages 4 and 6 take 48% to 80% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 16 s. Simulation, STL takes 13 s. Simulation, OBJ takes 20 s. Visual, GLB takes 21 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/boatcontrol_NonLatchingNO30A.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.5 | 5.6 | 0.8&nbsp;ms | 3.8 | 0.2 | 0.6 | 0.3 | 12.2 |
| Simulation, STEP | 0.3 | 1.5 | 5.9 | 0.6&nbsp;ms | 3.9 | 3.6 | 0.6 | 0.3 | 16.2 |
| Simulation, STL | 0.3 | 1.6 | 5.5 | 0.6&nbsp;ms | 3.7 | 0.4 | 0.8 | 0.3 | 12.6 |
| Simulation, OBJ | 0.3 | 1.5 | 5.6 | 0.5&nbsp;ms | 4.0 | 7.5 | 0.9 | 0.3 | 20.0 |
| Visual, GLB | 0.5 | 1.9 | 6.5 | 0.5&nbsp;ms | 10.0 | 0.2 | 1.1 | 0.3 | 20.6 |
| Visual, OBJ | 0.4 | 1.9 | 6.4 | 0.6&nbsp;ms | 9.2 | 3.9 | 1.1 | 0.3 | 23.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antevens/boatcontrol](https://github.com/antevens/boatcontrol)<br>Board: `NonLatchingNO30A.kicad_pcb` |
|---|---|
| Folder | addon / NonLatchingNO30A |
| Complexity | 198&nbsp;/&nbsp;1000 (size&nbsp;168, features&nbsp;30) |
| KESE&nbsp;features | filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 19, 499, 0 |
| Triangles,&nbsp;simulation | 1,069,614 in 62 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">37&nbsp;MB</td><td align="right">420&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">163&nbsp;MB</td><td align="right">481&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">53&nbsp;MB</td><td align="right">418&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">109&nbsp;MB</td><td align="right">751&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">449&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">54&nbsp;MB</td><td align="right">445&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.4 boatcontrol

![boatcontrol: stages 4 and 6 take 68% to 87% of a run. Simulation, GLB takes 7 min. Simulation, STEP takes 9 min. Simulation, STL takes 8 min. Visual, GLB takes 11 min. Visual, OBJ takes 12 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/boatcontrol_boatcontrol.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 7.9 | 42.7 | 214.7 | 9&nbsp;ms | 139.0 | 8.5 | 24.8 | 1.1 | 438.8 |
| Simulation, STEP | 7.8 | 42.6 | 220.6 | 6&nbsp;ms | 140.7 | 91.5 | 26.0 | 1.2 | 530.4 |
| Simulation, STL | 8.6 | 43.5 | 223.7 | 7&nbsp;ms | 146.5 | 16.8 | 24.9 | 1.3 | 465.2 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB | 8.1 | 42.5 | 223.4 | 7&nbsp;ms | 343.8 | 3.1 | 32.6 | 0.8 | 654.3 |
| Visual, OBJ | 7.7 | 40.5 | 215.3 | 6&nbsp;ms | 339.3 | 92.3 | 33.2 | 0.8 | 729.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antevens/boatcontrol](https://github.com/antevens/boatcontrol)<br>Board: `boatcontrol.kicad_pcb` |
|---|---|
| Folder | boatcontrol |
| Complexity | 358&nbsp;/&nbsp;1000 (size&nbsp;263, features&nbsp;95) |
| KESE&nbsp;features | through vias,<br>blind and buried vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 632, 15,097, 727 |
| Triangles,&nbsp;simulation | 30,876,084 in 1197 parts |
| Verifier | Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.0&nbsp;GB</td><td align="right">6.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">4.8&nbsp;GB</td><td align="right">8.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.5&nbsp;GB</td><td align="right">6.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">516&nbsp;MB</td><td align="right">8.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.7&nbsp;GB</td><td align="right">10&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.5 ac922interposer

![ac922interposer: stages 4 and 6 take 13% to 20% of a run. Simulation, GLB takes 1.3 s. Simulation, STEP takes 1.4 s. Simulation, STL takes 1.3 s. Simulation, OBJ takes 1.4 s. Visual, GLB takes 1.5 s. Visual, OBJ takes 1.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/ac922interposer_ac922interposer.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 0.1 | 0.1&nbsp;ms | 75&nbsp;ms | 3&nbsp;ms | 8&nbsp;ms | 0.2 | 1.3 |
| Simulation, STEP | 0.2 | 0.7 | 0.1 | 0.1&nbsp;ms | 78&nbsp;ms | 86&nbsp;ms | 8&nbsp;ms | 0.2 | 1.4 |
| Simulation, STL | 0.2 | 0.7 | 0.1 | 0.2&nbsp;ms | 81&nbsp;ms | 5&nbsp;ms | 13&nbsp;ms | 0.2 | 1.3 |
| Simulation, OBJ | 0.2 | 0.7 | 0.1 | 0.1&nbsp;ms | 79&nbsp;ms | 71&nbsp;ms | 9&nbsp;ms | 0.2 | 1.4 |
| Visual, GLB | 0.2 | 0.7 | 0.1 | 0.1&nbsp;ms | 0.2 | 6&nbsp;ms | 19&nbsp;ms | 0.2 | 1.5 |
| Visual, OBJ | 0.2 | 0.7 | 0.1 | 0.1&nbsp;ms | 0.2 | 59&nbsp;ms | 14&nbsp;ms | 0.2 | 1.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/ac922interposer](https://github.com/antmicro/ac922interposer)<br>Board: `ac922interposer.kicad_pcb` |
|---|---|
| Complexity | 212&nbsp;/&nbsp;1000 (size&nbsp;177, features&nbsp;35) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 15, 449, 43 |
| Triangles,&nbsp;simulation | 15,704 in 7 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">345&nbsp;kB</td><td align="right">159&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">227&nbsp;kB</td><td align="right">160&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">786&nbsp;kB</td><td align="right">160&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">1.4&nbsp;MB</td><td align="right">158&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">352&nbsp;kB</td><td align="right">160&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">1.1&nbsp;MB</td><td align="right">160&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.6 jetson-agx-thor-baseboard-pcie-x1-interposer

![Stages 4 and 6 take 52% to 81% of a run. Simulation, GLB takes 55 s. Simulation, STEP takes 67 s. Simulation, STL takes 54 s. Simulation, OBJ takes 79 s. Visual, GLB takes 74 s. Visual, OBJ takes 88 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/agx-thor-baseboard-pcie-interposer_jetson-agx-thor-baseboard-pcie-x1-interposer.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.4 | 5.5 | 16.0 | 0.9&nbsp;ms | 26.5 | 0.9 | 2.1 | 0.4 | 54.7 |
| Simulation, STEP | 3.0 | 5.2 | 15.6 | 0.9&nbsp;ms | 28.7 | 12.2 | 2.0 | 0.4 | 67.2 |
| Simulation, STL | 3.1 | 5.2 | 15.7 | 0.9&nbsp;ms | 25.1 | 2.0 | 2.1 | 0.4 | 53.6 |
| Simulation, OBJ | 3.1 | 4.9 | 15.2 | 0.9&nbsp;ms | 25.9 | 27.3 | 2.3 | 0.4 | 79.1 |
| Visual, GLB | 2.9 | 4.8 | 15.4 | 0.9&nbsp;ms | 44.3 | 0.5 | 5.7 | 0.3 | 74.0 |
| Visual, OBJ | 2.9 | 4.7 | 14.9 | 1.0&nbsp;ms | 41.1 | 18.5 | 5.8 | 0.3 | 88.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/agx-thor-baseboard-pcie-interposer](https://github.com/antmicro/agx-thor-baseboard-pcie-interposer)<br>Board: `jetson-agx-thor-baseboard-pcie-x1-interposer.kicad_pcb` |
|---|---|
| Complexity | 364&nbsp;/&nbsp;1000 (size&nbsp;214, features&nbsp;150) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 68, 948, 940 |
| Triangles,&nbsp;simulation | 4,223,912 in 375 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">143&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">533&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">211&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">444&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">101&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">318&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.7 antmicro-alvium-flex-csi-adapter-100mm-double-opposite-sides

![Stages 4 and 6 take 53% to 78% of a run. Simulation, GLB takes 6.6 s. Simulation, STEP takes 8.5 s. Simulation, STL takes 6.3 s. Simulation, OBJ takes 9.4 s. Visual, GLB takes 10 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/alvium-flexible-csi-adapter_antmicro-alvium-flex-csi-adapter-100mm-double-opposite-sides.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 2.2 | 0.4&nbsp;ms | 2.7 | 0.1 | 0.4 | 0.3 | 6.6 |
| Simulation, STEP | 0.3 | 0.9 | 2.3 | 0.2&nbsp;ms | 2.7 | 1.7 | 0.4 | 0.2 | 8.5 |
| Simulation, STL | 0.2 | 0.8 | 2.1 | 0.2&nbsp;ms | 2.5 | 0.2 | 0.4 | 0.2 | 6.3 |
| Simulation, OBJ | 0.2 | 0.7 | 2.3 | 0.2&nbsp;ms | 2.7 | 2.9 | 0.4 | 0.2 | 9.4 |
| Visual, GLB | 0.2 | 0.8 | 2.2 | 0.3&nbsp;ms | 5.7 | 87&nbsp;ms | 0.8 | 0.2 | 10.1 |
| Visual, OBJ | 0.3 | 0.8 | 2.1 | 0.3&nbsp;ms | 5.9 | 2.9 | 0.9 | 0.2 | 13.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/alvium-flexible-csi-adapter](https://github.com/antmicro/alvium-flexible-csi-adapter)<br>Board: `antmicro-alvium-flex-csi-adapter-100mm-double-opposite-sides.kicad_pcb` |
|---|---|
| Folder | 100mm-double-opposite-sides |
| Complexity | 200&nbsp;/&nbsp;1000 (size&nbsp;165, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 5, 1,782, 294 |
| Triangles,&nbsp;simulation | 631,300 in 56 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">22&nbsp;MB</td><td align="right">397&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">86&nbsp;MB</td><td align="right">455&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">32&nbsp;MB</td><td align="right">401&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">63&nbsp;MB</td><td align="right">458&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">498&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">61&nbsp;MB</td><td align="right">534&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.8 antmicro-alvium-flex-csi-adapter-100mm-double-same-side

![Stages 4 and 6 take 60% to 81% of a run. Simulation, GLB takes 8.3 s. Simulation, STEP takes 11 s. Simulation, STL takes 8.2 s. Simulation, OBJ takes 11 s. Visual, GLB takes 11 s. Visual, OBJ takes 14 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/alvium-flexible-csi-adapter_antmicro-alvium-flex-csi-adapter-100mm-double-same-side.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 2.9 | 0.2&nbsp;ms | 3.8 | 0.1 | 0.4 | 0.2 | 8.3 |
| Simulation, STEP | 0.2 | 0.8 | 2.7 | 0.2&nbsp;ms | 3.9 | 2.7 | 0.3 | 0.2 | 10.8 |
| Simulation, STL | 0.2 | 0.7 | 2.7 | 0.2&nbsp;ms | 3.7 | 0.2 | 0.4 | 0.2 | 8.2 |
| Simulation, OBJ | 0.2 | 0.8 | 2.8 | 0.2&nbsp;ms | 3.8 | 2.9 | 0.3 | 0.2 | 11.0 |
| Visual, GLB | 0.2 | 0.8 | 2.8 | 0.2&nbsp;ms | 6.3 | 0.1 | 0.8 | 0.2 | 11.3 |
| Visual, OBJ | 0.2 | 0.8 | 2.7 | 0.2&nbsp;ms | 6.5 | 2.8 | 0.8 | 0.2 | 14.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/alvium-flexible-csi-adapter](https://github.com/antmicro/alvium-flexible-csi-adapter)<br>Board: `antmicro-alvium-flex-csi-adapter-100mm-double-same-side.kicad_pcb` |
|---|---|
| Folder | 100mm-double-same-side |
| Complexity | 206&nbsp;/&nbsp;1000 (size&nbsp;171, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 5, 2,906, 269 |
| Triangles,&nbsp;simulation | 704,936 in 56 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">24&nbsp;MB</td><td align="right">433&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">108&nbsp;MB</td><td align="right">511&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">35&nbsp;MB</td><td align="right">425&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">70&nbsp;MB</td><td align="right">539&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">628&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">69&nbsp;MB</td><td align="right">594&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.9 antmicro-alvium-flex-csi-adapter-100mm-single-opposite-sides

![Stages 4 and 6 take 47% to 74% of a run. Simulation, GLB takes 3.3 s. Simulation, STEP takes 4.3 s. Simulation, STL takes 3.2 s. Simulation, OBJ takes 4.4 s. Visual, GLB takes 4.5 s. Visual, OBJ takes 5.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/alvium-flexible-csi-adapter_antmicro-alvium-flex-csi-adapter-100mm-single-opposite-sides.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 0.9 | 0.2&nbsp;ms | 1.3 | 44&nbsp;ms | 0.1 | 0.3 | 3.3 |
| Simulation, STEP | 0.2 | 0.5 | 0.9 | 0.3&nbsp;ms | 1.2 | 1.2 | 0.1 | 0.2 | 4.3 |
| Simulation, STL | 0.2 | 0.5 | 0.9 | 0.3&nbsp;ms | 1.1 | 65&nbsp;ms | 0.2 | 0.2 | 3.2 |
| Simulation, OBJ | 0.2 | 0.5 | 0.9 | 0.3&nbsp;ms | 1.2 | 1.4 | 0.1 | 0.2 | 4.4 |
| Visual, GLB | 0.2 | 0.5 | 0.9 | 0.2&nbsp;ms | 2.5 | 38&nbsp;ms | 0.3 | 0.2 | 4.5 |
| Visual, OBJ | 0.2 | 0.4 | 0.9 | 0.3&nbsp;ms | 2.4 | 1.3 | 0.2 | 0.2 | 5.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/alvium-flexible-csi-adapter](https://github.com/antmicro/alvium-flexible-csi-adapter)<br>Board: `antmicro-alvium-flex-csi-adapter-100mm-single-opposite-sides.kicad_pcb` |
|---|---|
| Folder | 100mm-single-opposite-sides |
| Complexity | 179&nbsp;/&nbsp;1000 (size&nbsp;144, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 3, 630, 96 |
| Triangles,&nbsp;simulation | 239,248 in 55 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">8.3&nbsp;MB</td><td align="right">231&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">36&nbsp;MB</td><td align="right">265&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">12&nbsp;MB</td><td align="right">232&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">24&nbsp;MB</td><td align="right">232&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.5&nbsp;MB</td><td align="right">235&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">236&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.10 antmicro-alvium-flex-csi-adapter_100mm-single-same-side

![Stages 4 and 6 take 47% to 79% of a run. Simulation, GLB takes 3.5 s. Simulation, STEP takes 5.0 s. Simulation, STL takes 3.3 s. Simulation, OBJ takes 5.0 s. Visual, GLB takes 5.1 s. Visual, OBJ takes 6.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/alvium-flexible-csi-adapter_antmicro-alvium-flex-csi-adapter-100mm-single-same-side.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 1.0 | 0.4&nbsp;ms | 1.4 | 47&nbsp;ms | 0.1 | 0.2 | 3.5 |
| Simulation, STEP | 0.2 | 0.6 | 1.0 | 0.2&nbsp;ms | 1.4 | 1.5 | 0.1 | 0.2 | 5.0 |
| Simulation, STL | 0.2 | 0.4 | 0.9 | 0.2&nbsp;ms | 1.3 | 91&nbsp;ms | 0.2 | 0.2 | 3.3 |
| Simulation, OBJ | 0.2 | 0.5 | 1.1 | 0.3&nbsp;ms | 1.4 | 1.5 | 0.1 | 0.2 | 5.0 |
| Visual, GLB | 0.2 | 0.5 | 1.0 | 0.3&nbsp;ms | 3.0 | 42&nbsp;ms | 0.2 | 0.2 | 5.1 |
| Visual, OBJ | 0.2 | 0.5 | 1.1 | 0.2&nbsp;ms | 2.8 | 1.5 | 0.3 | 0.3 | 6.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/alvium-flexible-csi-adapter](https://github.com/antmicro/alvium-flexible-csi-adapter)<br>Board: `antmicro-alvium-flex-csi-adapter_100mm-single-same-side.kicad_pcb` |
|---|---|
| Folder | 100mm-single-same-side |
| Complexity | 184&nbsp;/&nbsp;1000 (size&nbsp;149, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 3, 918, 115 |
| Triangles,&nbsp;simulation | 282,484 in 55 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.8&nbsp;MB</td><td align="right">248&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">42&nbsp;MB</td><td align="right">289&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">251&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">28&nbsp;MB</td><td align="right">255&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">9.2&nbsp;MB</td><td align="right">281&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">27&nbsp;MB</td><td align="right">284&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.11 antmicro-alvium-flex-csi-adapter-200mm-single-opposite-sides

![Stages 4 and 6 take 48% to 75% of a run. Simulation, GLB takes 5.5 s. Simulation, STEP takes 7.6 s. Simulation, STL takes 5.2 s. Simulation, OBJ takes 6.1 s. Visual, GLB takes 6.0 s. Visual, OBJ takes 8.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/alvium-flexible-csi-adapter_antmicro-alvium-flex-csi-adapter-200mm-single-opposite-sides.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 1.0 | 1.5 | 0.3&nbsp;ms | 1.9 | 73&nbsp;ms | 0.3 | 0.4 | 5.5 |
| Simulation, STEP | 0.3 | 1.0 | 1.6 | 0.7&nbsp;ms | 2.0 | 2.1 | 0.2 | 0.4 | 7.6 |
| Simulation, STL | 0.3 | 0.8 | 1.5 | 0.4&nbsp;ms | 1.8 | 0.1 | 0.2 | 0.4 | 5.2 |
| Simulation, OBJ | 0.2 | 0.7 | 1.3 | 0.2&nbsp;ms | 1.6 | 1.8 | 0.2 | 0.3 | 6.1 |
| Visual, GLB | 0.2 | 0.6 | 1.2 | 0.3&nbsp;ms | 3.3 | 62&nbsp;ms | 0.4 | 0.2 | 6.0 |
| Visual, OBJ | 0.2 | 0.7 | 1.3 | 0.3&nbsp;ms | 3.5 | 2.0 | 0.5 | 0.3 | 8.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/alvium-flexible-csi-adapter](https://github.com/antmicro/alvium-flexible-csi-adapter)<br>Board: `antmicro-alvium-flex-csi-adapter-200mm-single-opposite-sides.kicad_pcb` |
|---|---|
| Folder | 200mm-single-opposite-sides |
| Complexity | 182&nbsp;/&nbsp;1000 (size&nbsp;147, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 3, 635, 173 |
| Triangles,&nbsp;simulation | 306,536 in 55 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">257&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">39&nbsp;MB</td><td align="right">296&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">15&nbsp;MB</td><td align="right">259&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">30&nbsp;MB</td><td align="right">264&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">9.5&nbsp;MB</td><td align="right">280&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">28&nbsp;MB</td><td align="right">317&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.12 antmicro-alvium-flex-csi-adapter_200mm-single-same-side

![Stages 4 and 6 take 50% to 75% of a run. Simulation, GLB takes 4.0 s. Simulation, STEP takes 5.5 s. Simulation, STL takes 3.9 s. Simulation, OBJ takes 5.4 s. Visual, GLB takes 5.9 s. Visual, OBJ takes 7.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/alvium-flexible-csi-adapter_antmicro-alvium-flex-csi-adapter-200mm-single-same-side.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 1.1 | 0.2&nbsp;ms | 1.7 | 62&nbsp;ms | 0.2 | 0.2 | 4.0 |
| Simulation, STEP | 0.2 | 0.6 | 1.3 | 0.3&nbsp;ms | 1.7 | 1.5 | 0.2 | 0.2 | 5.5 |
| Simulation, STL | 0.2 | 0.5 | 1.2 | 0.2&nbsp;ms | 1.5 | 0.1 | 0.2 | 0.2 | 3.9 |
| Simulation, OBJ | 0.2 | 0.6 | 1.2 | 0.2&nbsp;ms | 1.5 | 1.5 | 0.2 | 0.2 | 5.4 |
| Visual, GLB | 0.2 | 0.6 | 1.1 | 0.4&nbsp;ms | 3.3 | 51&nbsp;ms | 0.4 | 0.2 | 5.9 |
| Visual, OBJ | 0.2 | 0.6 | 1.0 | 0.3&nbsp;ms | 3.2 | 1.5 | 0.4 | 0.2 | 7.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/alvium-flexible-csi-adapter](https://github.com/antmicro/alvium-flexible-csi-adapter)<br>Board: `antmicro-alvium-flex-csi-adapter_200mm-single-same-side.kicad_pcb` |
|---|---|
| Folder | 200mm-single-same-side |
| Complexity | 186&nbsp;/&nbsp;1000 (size&nbsp;151, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 3, 913, 181 |
| Triangles,&nbsp;simulation | 337,742 in 55 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">268&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">44&nbsp;MB</td><td align="right">317&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">17&nbsp;MB</td><td align="right">267&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">33&nbsp;MB</td><td align="right">266&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">329&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">32&nbsp;MB</td><td align="right">328&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.13 artix-dc-scm

![artix-dc-scm: stages 4 and 6 take 40% to 76% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 3 min. Simulation, STL takes 2 min. Simulation, OBJ takes 4 min. Visual, GLB takes 3 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/artix-dc-scm_artix-dc-scm.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 18.8 | 18.1 | 45.4 | 2&nbsp;ms | 53.3 | 3.2 | 7.1 | 0.7 | 146.5 |
| Simulation, STEP | 18.4 | 16.7 | 42.7 | 3&nbsp;ms | 48.5 | 29.1 | 6.8 | 0.7 | 162.7 |
| Simulation, STL | 17.9 | 18.2 | 43.7 | 3&nbsp;ms | 49.1 | 5.4 | 6.3 | 0.7 | 141.4 |
| Simulation, OBJ | 17.8 | 17.1 | 40.9 | 2&nbsp;ms | 49.6 | 91.4 | 7.0 | 0.7 | 224.5 |
| Visual, GLB | 18.4 | 18.0 | 43.9 | 3&nbsp;ms | 105.7 | 1.1 | 9.7 | 0.5 | 197.4 |
| Visual, OBJ | 18.1 | 17.4 | 42.1 | 3&nbsp;ms | 106.0 | 44.3 | 9.9 | 0.5 | 238.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/artix-dc-scm](https://github.com/antmicro/artix-dc-scm)<br>Board: `artix-dc-scm.kicad_pcb` |
|---|---|
| Complexity | 504&nbsp;/&nbsp;1000 (size&nbsp;344, features&nbsp;160) |
| KESE&nbsp;features | through vias,<br>blind and buried vias, custom pads,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 529, 12,682, 1,558 |
| Triangles,&nbsp;simulation | 12,211,974 in 719 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">411&nbsp;MB</td><td align="right">3.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.4&nbsp;GB</td><td align="right">4.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">611&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.4&nbsp;GB</td><td align="right">8.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">209&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">707&nbsp;MB</td><td align="right">4.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.14 arty-a7-expansion

![arty-a7-expansion: stages 4 and 6 take 62% to 86% of a run. Simulation, GLB takes 21 s. Simulation, STEP takes 24 s. Simulation, STL takes 20 s. Simulation, OBJ takes 28 s. Visual, GLB takes 28 s. Visual, OBJ takes 33 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/arty-expansion-board_arty-a7-expansion.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.9 | 9.3 | 0.7&nbsp;ms | 7.6 | 0.3 | 0.8 | 0.2 | 20.6 |
| Simulation, STEP | 0.4 | 1.9 | 9.0 | 0.8&nbsp;ms | 7.4 | 4.7 | 0.8 | 0.3 | 24.4 |
| Simulation, STL | 0.4 | 2.0 | 9.5 | 0.6&nbsp;ms | 7.0 | 0.4 | 0.7 | 0.3 | 20.4 |
| Simulation, OBJ | 0.4 | 1.9 | 9.7 | 2&nbsp;ms | 7.3 | 7.3 | 0.7 | 0.3 | 27.5 |
| Visual, GLB | 0.4 | 1.8 | 9.3 | 0.6&nbsp;ms | 14.7 | 0.2 | 1.2 | 0.2 | 27.8 |
| Visual, OBJ | 0.5 | 1.9 | 9.6 | 0.9&nbsp;ms | 15.3 | 4.6 | 1.3 | 0.2 | 33.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/arty-expansion-board](https://github.com/antmicro/arty-expansion-board)<br>Board: `arty-a7-expansion.kicad_pcb` |
|---|---|
| Complexity | 325&nbsp;/&nbsp;1000 (size&nbsp;260, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 108, 3,485, 134 |
| Triangles,&nbsp;simulation | 1,746,946 in 137 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">62&nbsp;MB</td><td align="right">700&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">317&nbsp;MB</td><td align="right">803&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">87&nbsp;MB</td><td align="right">736&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">185&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">36&nbsp;MB</td><td align="right">847&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">109&nbsp;MB</td><td align="right">911&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.15 arty-mpw-tester

![arty-mpw-tester: stages 4 and 6 take 42% to 72% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 29 s. Simulation, STL takes 24 s. Simulation, OBJ takes 34 s. Visual, GLB takes 35 s. Visual, OBJ takes 41 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/arty-mpw-tester_arty-mpw-tester.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 5.0 | 2.2 | 7.2 | 0.9&nbsp;ms | 7.4 | 0.3 | 1.0 | 0.3 | 23.4 |
| Simulation, STEP | 5.3 | 2.2 | 7.5 | 1&nbsp;ms | 7.3 | 5.5 | 1.2 | 0.3 | 29.2 |
| Simulation, STL | 5.1 | 2.0 | 7.2 | 1.0&nbsp;ms | 7.2 | 0.8 | 1.2 | 0.4 | 23.9 |
| Simulation, OBJ | 5.3 | 2.2 | 7.2 | 0.8&nbsp;ms | 7.1 | 10.7 | 1.0 | 0.4 | 33.9 |
| Visual, GLB | 4.9 | 2.4 | 7.2 | 0.9&nbsp;ms | 17.8 | 0.2 | 2.1 | 0.3 | 34.8 |
| Visual, OBJ | 4.8 | 2.3 | 6.8 | 0.8&nbsp;ms | 17.8 | 6.8 | 2.0 | 0.3 | 40.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/arty-mpw-tester](https://github.com/antmicro/arty-mpw-tester)<br>Board: `arty-mpw-tester.kicad_pcb` |
|---|---|
| Complexity | 378&nbsp;/&nbsp;1000 (size&nbsp;248, features&nbsp;130) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 109, 1,456, 147 |
| Triangles,&nbsp;simulation | 2,103,228 in 162 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">72&nbsp;MB</td><td align="right">891&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">309&nbsp;MB</td><td align="right">968&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">105&nbsp;MB</td><td align="right">854&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">219&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">44&nbsp;MB</td><td align="right">949&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">134&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.16 arvsom

![arvsom: stages 4 and 6 take 45% to 84% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 3 min. Simulation, STL takes 3 min. Simulation, OBJ takes 5 min. Visual, GLB takes 4 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/arvsom_arvsom.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.1 | 17.9 | 53.5 | 2&nbsp;ms | 72.8 | 4.0 | 8.9 | 0.7 | 161.0 |
| Simulation, STEP | 3.3 | 17.4 | 52.3 | 2&nbsp;ms | 70.9 | 34.9 | 9.2 | 0.6 | 188.6 |
| Simulation, STL | 3.3 | 16.8 | 52.6 | 2&nbsp;ms | 80.7 | 8.7 | 11.6 | 0.7 | 174.5 |
| Simulation, OBJ | 3.2 | 17.3 | 53.1 | 3&nbsp;ms | 72.8 | 120.8 | 9.7 | 0.6 | 277.5 |
| Visual, GLB | 3.1 | 17.6 | 54.4 | 2&nbsp;ms | 126.4 | 1.3 | 12.1 | 0.5 | 215.3 |
| Visual, OBJ | 3.5 | 17.3 | 53.1 | 2&nbsp;ms | 123.1 | 41.3 | 11.2 | 0.5 | 250.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/arvsom](https://github.com/antmicro/arvsom)<br>Board: `arvsom.kicad_pcb` |
|---|---|
| Complexity | 404&nbsp;/&nbsp;1000 (size&nbsp;349, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 12 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 427, 15,505, 1,202 |
| Triangles,&nbsp;simulation | 15,923,766 in 682 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">544&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.7&nbsp;GB</td><td align="right">4.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">796&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.8&nbsp;GB</td><td align="right">10&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">208&nbsp;MB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">709&nbsp;MB</td><td align="right">4.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.17 audio-latency-tester-board

![audio-latency-tester-board: stages 4 and 6 take 47% to 76% of a run. Simulation, GLB takes 29 s. Simulation, STEP takes 35 s. Simulation, STL takes 29 s. Simulation, OBJ takes 43 s. Visual, GLB takes 43 s. Visual, OBJ takes 52 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/audio-latency-tester-board_audio-latency-tester-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.6 | 2.5 | 8.5 | 0.9&nbsp;ms | 11.4 | 0.4 | 0.9 | 0.3 | 28.6 |
| Simulation, STEP | 4.5 | 2.4 | 8.3 | 0.8&nbsp;ms | 11.0 | 7.6 | 0.9 | 0.3 | 35.0 |
| Simulation, STL | 4.6 | 2.4 | 8.0 | 0.9&nbsp;ms | 11.8 | 0.8 | 0.9 | 0.3 | 28.8 |
| Simulation, OBJ | 4.6 | 2.4 | 8.7 | 1&nbsp;ms | 11.6 | 14.2 | 1.0 | 0.3 | 42.7 |
| Visual, GLB | 4.7 | 2.5 | 8.4 | 1&nbsp;ms | 24.0 | 0.3 | 2.4 | 0.4 | 42.7 |
| Visual, OBJ | 4.7 | 2.5 | 8.4 | 0.8&nbsp;ms | 23.6 | 10.6 | 2.4 | 0.4 | 52.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/audio-latency-tester-board](https://github.com/antmicro/audio-latency-tester-board)<br>Board: `audio-latency-tester-board.kicad_pcb` |
|---|---|
| Complexity | 410&nbsp;/&nbsp;1000 (size&nbsp;270, features&nbsp;140) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, knockout text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 212, 2,202, 302 |
| Triangles,&nbsp;simulation | 2,357,376 in 214 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">81&nbsp;MB</td><td align="right">953&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">375&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">118&nbsp;MB</td><td align="right">958&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">247&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">60&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">184&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.18 caravel_breakout_QFN

![caravel_breakout_QFN: stages 4 and 6 take 53% to 82% of a run. Simulation, GLB takes 6.0 s. Simulation, STEP takes 7.7 s. Simulation, STL takes 5.9 s. Simulation, OBJ takes 8.8 s. Visual, GLB takes 8.8 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_caravel-breakout-QFN.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 2.1 | 0.3&nbsp;ms | 2.5 | 91&nbsp;ms | 0.4 | 0.3 | 6.0 |
| Simulation, STEP | 0.2 | 0.5 | 2.1 | 0.3&nbsp;ms | 2.4 | 1.9 | 0.4 | 0.2 | 7.7 |
| Simulation, STL | 0.2 | 0.4 | 2.1 | 0.3&nbsp;ms | 2.4 | 0.2 | 0.3 | 0.2 | 5.9 |
| Simulation, OBJ | 0.2 | 0.5 | 2.2 | 0.4&nbsp;ms | 2.5 | 2.9 | 0.3 | 0.2 | 8.8 |
| Visual, GLB | 0.2 | 0.5 | 2.1 | 0.4&nbsp;ms | 5.1 | 74&nbsp;ms | 0.6 | 0.2 | 8.8 |
| Visual, OBJ | 0.2 | 0.5 | 2.1 | 0.3&nbsp;ms | 5.2 | 2.3 | 0.8 | 0.2 | 11.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `caravel_breakout_QFN.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_breakout_QFN |
| Complexity | 275&nbsp;/&nbsp;1000 (size&nbsp;200, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 14, 775, 99 |
| Triangles,&nbsp;simulation | 693,354 in 70 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">24&nbsp;MB</td><td align="right">360&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">123&nbsp;MB</td><td align="right">433&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">35&nbsp;MB</td><td align="right">361&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">71&nbsp;MB</td><td align="right">514&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">437&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">54&nbsp;MB</td><td align="right">497&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.19 Caravel_breakout

![Caravel_breakout: stages 4 and 6 take 54% to 84% of a run. Simulation, GLB takes 5.6 s. Simulation, STEP takes 7.1 s. Simulation, STL takes 5.8 s. Simulation, OBJ takes 8.4 s. Visual, GLB takes 8.3 s. Visual, OBJ takes 10 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_Caravel-breakout.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.4 | 2.4 | 0.3&nbsp;ms | 2.1 | 86&nbsp;ms | 0.3 | 0.2 | 5.6 |
| Simulation, STEP | 0.1 | 0.4 | 2.4 | 0.3&nbsp;ms | 2.0 | 1.7 | 0.3 | 0.2 | 7.1 |
| Simulation, STL | 0.2 | 0.5 | 2.4 | 0.3&nbsp;ms | 2.1 | 0.2 | 0.3 | 0.2 | 5.8 |
| Simulation, OBJ | 0.1 | 0.4 | 2.5 | 0.3&nbsp;ms | 2.1 | 2.8 | 0.3 | 0.2 | 8.4 |
| Visual, GLB | 0.1 | 0.4 | 2.4 | 0.3&nbsp;ms | 4.6 | 57&nbsp;ms | 0.5 | 0.2 | 8.3 |
| Visual, OBJ | 0.2 | 0.4 | 2.5 | 0.5&nbsp;ms | 4.6 | 1.7 | 0.6 | 0.2 | 10.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `Caravel_breakout.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_breakout_v1 |
| Complexity | 244&nbsp;/&nbsp;1000 (size&nbsp;199, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 12, 449, 28 |
| Triangles,&nbsp;simulation | 689,454 in 66 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">24&nbsp;MB</td><td align="right">334&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">107&nbsp;MB</td><td align="right">398&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">34&nbsp;MB</td><td align="right">355&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">70&nbsp;MB</td><td align="right">489&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">403&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">46&nbsp;MB</td><td align="right">445&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.20 Caravel_breakout_v2

![Caravel_breakout_v2: stages 4 and 6 take 54% to 82% of a run. Simulation, GLB takes 6.6 s. Simulation, STEP takes 8.4 s. Simulation, STL takes 6.5 s. Simulation, OBJ takes 10 s. Visual, GLB takes 9.1 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_Caravel-breakout-v2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 2.5 | 0.4&nbsp;ms | 2.6 | 91&nbsp;ms | 0.4 | 0.3 | 6.6 |
| Simulation, STEP | 0.3 | 0.5 | 2.5 | 0.4&nbsp;ms | 2.5 | 2.1 | 0.4 | 0.2 | 8.4 |
| Simulation, STL | 0.2 | 0.4 | 2.5 | 0.5&nbsp;ms | 2.5 | 0.1 | 0.5 | 0.3 | 6.5 |
| Simulation, OBJ | 0.2 | 0.4 | 2.5 | 0.4&nbsp;ms | 3.0 | 3.3 | 0.4 | 0.2 | 10.1 |
| Visual, GLB | 0.3 | 0.5 | 2.6 | 0.3&nbsp;ms | 4.9 | 90&nbsp;ms | 0.4 | 0.3 | 9.1 |
| Visual, OBJ | 0.3 | 0.4 | 2.5 | 0.4&nbsp;ms | 4.6 | 2.4 | 0.4 | 0.2 | 10.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `Caravel_breakout_v2.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_breakout_v2 |
| Complexity | 275&nbsp;/&nbsp;1000 (size&nbsp;200, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 12, 469, 28 |
| Triangles,&nbsp;simulation | 522,928 in 69 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">300&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">97&nbsp;MB</td><td align="right">365&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">26&nbsp;MB</td><td align="right">302&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">54&nbsp;MB</td><td align="right">383&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">364&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">38&nbsp;MB</td><td align="right">369&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.21 Caravel_daughter

![Caravel_daughter: stages 4 and 6 take 48% to 77% of a run. Simulation, GLB takes 5.1 s. Simulation, STEP takes 6.4 s. Simulation, STL takes 5.0 s. Simulation, OBJ takes 6.7 s. Visual, GLB takes 6.7 s. Visual, OBJ takes 8.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_Caravel-daughter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.9 | 1.9 | 0.5&nbsp;ms | 1.7 | 74&nbsp;ms | 0.2 | 0.2 | 5.1 |
| Simulation, STEP | 0.2 | 0.9 | 1.7 | 0.5&nbsp;ms | 1.6 | 1.6 | 0.2 | 0.2 | 6.4 |
| Simulation, STL | 0.2 | 0.9 | 1.7 | 0.3&nbsp;ms | 1.6 | 0.1 | 0.2 | 0.3 | 5.0 |
| Simulation, OBJ | 0.2 | 0.8 | 1.7 | 0.6&nbsp;ms | 1.5 | 2.0 | 0.2 | 0.3 | 6.7 |
| Visual, GLB | 0.2 | 0.8 | 1.8 | 0.3&nbsp;ms | 3.4 | 41&nbsp;ms | 0.3 | 0.2 | 6.7 |
| Visual, OBJ | 0.2 | 0.9 | 1.8 | 0.4&nbsp;ms | 3.6 | 1.1 | 0.3 | 0.3 | 8.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `Caravel_daughter.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_daughter |
| Complexity | 138&nbsp;/&nbsp;1000 (size&nbsp;108, features&nbsp;30) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 36, 0, 0 |
| Triangles,&nbsp;simulation | 390,448 in 66 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">269&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">76&nbsp;MB</td><td align="right">318&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">20&nbsp;MB</td><td align="right">265&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">41&nbsp;MB</td><td align="right">322&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.5&nbsp;MB</td><td align="right">267&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">266&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.22 caravel_FTDI_QFN_test_socket

![caravel_FTDI_QFN_test_socket: stages 4 and 6 take 56% to 84% of a run. Simulation, GLB takes 15 s. Simulation, STEP takes 19 s. Simulation, STL takes 16 s. Simulation, OBJ takes 21 s. Visual, GLB takes 23 s. Visual, OBJ takes 27 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_caravel-FTDI-QFN-test-socket.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.2 | 6.3 | 1&nbsp;ms | 5.7 | 0.2 | 0.6 | 0.3 | 14.7 |
| Simulation, STEP | 0.3 | 1.1 | 6.4 | 1&nbsp;ms | 5.5 | 4.5 | 0.6 | 0.2 | 18.7 |
| Simulation, STL | 0.3 | 1.3 | 6.7 | 1&nbsp;ms | 6.4 | 0.5 | 0.7 | 0.2 | 16.1 |
| Simulation, OBJ | 0.4 | 1.3 | 6.5 | 0.9&nbsp;ms | 5.3 | 6.6 | 0.6 | 0.2 | 20.9 |
| Visual, GLB | 0.3 | 1.2 | 6.7 | 0.8&nbsp;ms | 12.4 | 0.2 | 1.7 | 0.2 | 22.8 |
| Visual, OBJ | 0.3 | 1.1 | 6.3 | 0.9&nbsp;ms | 12.7 | 5.0 | 1.4 | 0.2 | 27.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `caravel_FTDI_QFN_test_socket.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_FTDI_QFN_test_socket |
| Complexity | 315&nbsp;/&nbsp;1000 (size&nbsp;230, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 72, 1,076, 164 |
| Triangles,&nbsp;simulation | 1,635,312 in 99 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">56&nbsp;MB</td><td align="right">606&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">277&nbsp;MB</td><td align="right">809&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">82&nbsp;MB</td><td align="right">588&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">169&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">41&nbsp;MB</td><td align="right">784&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">126&nbsp;MB</td><td align="right">936&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.23 caravel_Nucleo

![caravel_Nucleo: stages 4 and 6 take 55% to 84% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 29 s. Simulation, STL takes 23 s. Simulation, OBJ takes 32 s. Visual, GLB takes 36 s. Visual, OBJ takes 44 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_caravel-Nucleo.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.9 | 9.9 | 1&nbsp;ms | 8.7 | 0.4 | 1.1 | 0.3 | 22.7 |
| Simulation, STEP | 0.5 | 1.7 | 9.8 | 2&nbsp;ms | 8.9 | 6.4 | 1.2 | 0.3 | 28.7 |
| Simulation, STL | 0.5 | 1.8 | 9.9 | 1&nbsp;ms | 8.4 | 0.8 | 1.1 | 0.3 | 22.8 |
| Simulation, OBJ | 0.5 | 1.9 | 9.5 | 0.9&nbsp;ms | 8.4 | 10.5 | 1.1 | 0.3 | 32.3 |
| Visual, GLB | 0.5 | 1.9 | 9.8 | 1&nbsp;ms | 20.4 | 0.3 | 2.8 | 0.3 | 35.9 |
| Visual, OBJ | 0.5 | 2.2 | 10.1 | 1&nbsp;ms | 20.5 | 7.6 | 2.8 | 0.2 | 43.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `caravel_Nucleo.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_Nucleo |
| Complexity | 333&nbsp;/&nbsp;1000 (size&nbsp;228, features&nbsp;105) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 89, 1,284, 162 |
| Triangles,&nbsp;simulation | 2,223,932 in 208 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">75&nbsp;MB</td><td align="right">745&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">364&nbsp;MB</td><td align="right">998&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">111&nbsp;MB</td><td align="right">756&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">232&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">55&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">169&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.24 Caravel_pcb

![Caravel_pcb: stages 4 and 6 take 57% to 83% of a run. Simulation, GLB takes 19 s. Simulation, STEP takes 21 s. Simulation, STL takes 17 s. Simulation, OBJ takes 24 s. Visual, GLB takes 23 s. Visual, OBJ takes 30 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_Caravel-pcb.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.2 | 8.0 | 0.6&nbsp;ms | 6.5 | 0.2 | 0.7 | 0.3 | 18.7 |
| Simulation, STEP | 0.4 | 1.7 | 7.5 | 0.5&nbsp;ms | 6.2 | 4.1 | 0.7 | 0.2 | 20.9 |
| Simulation, STL | 0.4 | 1.7 | 7.8 | 0.4&nbsp;ms | 6.0 | 0.5 | 0.7 | 0.3 | 17.3 |
| Simulation, OBJ | 0.4 | 1.6 | 7.4 | 0.5&nbsp;ms | 6.2 | 7.4 | 0.7 | 0.3 | 24.0 |
| Visual, GLB | 0.4 | 1.7 | 7.6 | 0.4&nbsp;ms | 11.7 | 0.2 | 1.4 | 0.2 | 23.3 |
| Visual, OBJ | 0.4 | 1.6 | 8.1 | 0.5&nbsp;ms | 12.2 | 5.8 | 1.4 | 0.2 | 29.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `Caravel_pcb.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_pcb_v1 |
| Complexity | 290&nbsp;/&nbsp;1000 (size&nbsp;235, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 72, 1,749, 98 |
| Triangles,&nbsp;simulation | 1,242,816 in 99 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">44&nbsp;MB</td><td align="right">520&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">248&nbsp;MB</td><td align="right">654&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">62&nbsp;MB</td><td align="right">526&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">131&nbsp;MB</td><td align="right">885&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">628&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">95&nbsp;MB</td><td align="right">747&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.25 caravel_pcb_v3_FTDI_flexy

![caravel_pcb_v3_FTDI_flexy: stages 4 and 6 take 53% to 85% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 21 s. Simulation, STL takes 16 s. Simulation, OBJ takes 25 s. Visual, GLB takes 25 s. Visual, OBJ takes 31 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_hardware-caravel-pcb-v3-FTDI_caravel-pcb-v3-FTDI-flexy.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.4 | 7.8 | 0.6&nbsp;ms | 5.6 | 0.2 | 0.7 | 0.2 | 16.5 |
| Simulation, STEP | 0.5 | 1.5 | 7.5 | 0.7&nbsp;ms | 5.3 | 4.8 | 0.7 | 0.2 | 20.5 |
| Simulation, STL | 0.4 | 1.4 | 7.6 | 0.6&nbsp;ms | 5.4 | 0.4 | 0.8 | 0.2 | 16.3 |
| Simulation, OBJ | 0.5 | 1.4 | 7.7 | 0.4&nbsp;ms | 5.6 | 9.1 | 0.8 | 0.2 | 25.4 |
| Visual, GLB | 0.5 | 1.6 | 7.8 | 1.0&nbsp;ms | 13.7 | 0.2 | 1.3 | 0.3 | 25.3 |
| Visual, OBJ | 0.5 | 1.5 | 7.8 | 0.6&nbsp;ms | 13.5 | 6.5 | 1.4 | 0.3 | 31.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `caravel_pcb_v3_FTDI_flexy.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_pcb_v3_FTDI |
| Complexity | 314&nbsp;/&nbsp;1000 (size&nbsp;219, features&nbsp;95) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, filled zones,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 63, 935, 122 |
| Triangles,&nbsp;simulation | 1,524,006 in 98 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">52&nbsp;MB</td><td align="right">585&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">270&nbsp;MB</td><td align="right">782&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">76&nbsp;MB</td><td align="right">605&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">157&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">715&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">118&nbsp;MB</td><td align="right">875&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.26 caravel_pcb_v3_FTDI_SMD

![caravel_pcb_v3_FTDI_SMD: stages 4 and 6 take 54% to 81% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 15 s. Simulation, STL takes 12 s. Simulation, OBJ takes 18 s. Visual, GLB takes 18 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_caravel-pcb-v3-FTDI-SMD.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.1 | 4.8 | 0.5&nbsp;ms | 5.0 | 0.2 | 0.6 | 0.3 | 12.4 |
| Simulation, STEP | 0.4 | 1.1 | 4.8 | 0.6&nbsp;ms | 4.5 | 3.8 | 0.5 | 0.2 | 15.4 |
| Simulation, STL | 0.3 | 1.0 | 4.7 | 0.8&nbsp;ms | 4.5 | 0.5 | 0.5 | 0.2 | 11.8 |
| Simulation, OBJ | 0.4 | 1.2 | 5.2 | 0.7&nbsp;ms | 4.7 | 5.9 | 0.5 | 0.3 | 18.1 |
| Visual, GLB | 0.4 | 1.1 | 4.8 | 0.7&nbsp;ms | 9.8 | 0.2 | 1.5 | 0.3 | 18.0 |
| Visual, OBJ | 0.4 | 1.1 | 4.8 | 0.7&nbsp;ms | 10.3 | 5.1 | 1.6 | 0.2 | 23.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `caravel_pcb_v3_FTDI_SMD.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_pcb_v3_FTDI |
| Complexity | 305&nbsp;/&nbsp;1000 (size&nbsp;220, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 63, 932, 131 |
| Triangles,&nbsp;simulation | 1,286,120 in 97 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">44&nbsp;MB</td><td align="right">556&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">229&nbsp;MB</td><td align="right">681&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">64&nbsp;MB</td><td align="right">545&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">131&nbsp;MB</td><td align="right">861&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">35&nbsp;MB</td><td align="right">663&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">104&nbsp;MB</td><td align="right">792&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.27 caravel_pcb_v3_MCP

![caravel_pcb_v3_MCP: stages 4 and 6 take 52% to 81% of a run. Simulation, GLB takes 5.1 s. Simulation, STEP takes 6.7 s. Simulation, STL takes 5.0 s. Simulation, OBJ takes 7.5 s. Visual, GLB takes 7.5 s. Visual, OBJ takes 8.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_caravel-pcb-v3-MCP.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 2.1 | 0.7&nbsp;ms | 1.8 | 86&nbsp;ms | 0.3 | 0.3 | 5.1 |
| Simulation, STEP | 0.1 | 0.5 | 2.3 | 0.4&nbsp;ms | 1.7 | 1.6 | 0.3 | 0.2 | 6.7 |
| Simulation, STL | 0.1 | 0.4 | 2.2 | 0.4&nbsp;ms | 1.6 | 0.1 | 0.3 | 0.2 | 5.0 |
| Simulation, OBJ | 0.2 | 0.4 | 2.2 | 0.5&nbsp;ms | 1.7 | 2.6 | 0.3 | 0.2 | 7.5 |
| Visual, GLB | 0.2 | 0.5 | 2.1 | 0.5&nbsp;ms | 3.9 | 47&nbsp;ms | 0.4 | 0.3 | 7.5 |
| Visual, OBJ | 0.2 | 0.4 | 2.2 | 0.7&nbsp;ms | 3.9 | 1.5 | 0.5 | 0.3 | 8.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `caravel_pcb_v3_MCP.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_pcb_v3_MCP |
| Complexity | 76&nbsp;/&nbsp;1000 (size&nbsp;56, features&nbsp;20) |
| KESE&nbsp;features | slotted holes, rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 38, 0, 0 |
| Triangles,&nbsp;simulation | 494,144 in 78 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">287&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">61&nbsp;MB</td><td align="right">325&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">25&nbsp;MB</td><td align="right">281&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">50&nbsp;MB</td><td align="right">377&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">336&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">32&nbsp;MB</td><td align="right">339&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.28 caravel_pcb_v4_FTDI_flexy

![caravel_pcb_v4_FTDI_flexy: stages 4 and 6 take 54% to 85% of a run. Simulation, GLB takes 15 s. Simulation, STEP takes 18 s. Simulation, STL takes 14 s. Simulation, OBJ takes 21 s. Visual, GLB takes 22 s. Visual, OBJ takes 28 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_caravel-pcb-v4-FTDI-flexy.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.2 | 7.0 | 0.4&nbsp;ms | 4.8 | 0.2 | 0.7 | 0.2 | 14.5 |
| Simulation, STEP | 0.4 | 1.1 | 6.6 | 0.4&nbsp;ms | 4.9 | 4.4 | 0.6 | 0.2 | 18.3 |
| Simulation, STL | 0.4 | 1.4 | 6.6 | 0.8&nbsp;ms | 4.6 | 0.5 | 0.7 | 0.2 | 14.4 |
| Simulation, OBJ | 0.4 | 1.2 | 6.4 | 0.6&nbsp;ms | 5.0 | 7.2 | 0.6 | 0.2 | 20.9 |
| Visual, GLB | 0.4 | 1.2 | 6.9 | 0.8&nbsp;ms | 11.5 | 0.1 | 1.2 | 0.2 | 21.6 |
| Visual, OBJ | 0.4 | 1.2 | 6.9 | 0.5&nbsp;ms | 11.7 | 5.7 | 1.6 | 0.2 | 27.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `caravel_pcb_v4_FTDI_flexy.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_pcb_v4_FTDI |
| Complexity | 312&nbsp;/&nbsp;1000 (size&nbsp;217, features&nbsp;95) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, filled zones,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 61, 884, 104 |
| Triangles,&nbsp;simulation | 1,428,776 in 104 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">49&nbsp;MB</td><td align="right">601&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">248&nbsp;MB</td><td align="right">741&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">71&nbsp;MB</td><td align="right">583&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">147&nbsp;MB</td><td align="right">990&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">36&nbsp;MB</td><td align="right">805&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">108&nbsp;MB</td><td align="right">858&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.29 caravel_pcb_v4_FTDI_SMD

![caravel_pcb_v4_FTDI_SMD: stages 4 and 6 take 54% to 83% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 16 s. Simulation, STL takes 13 s. Simulation, OBJ takes 19 s. Visual, GLB takes 17 s. Visual, OBJ takes 22 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/caravel-board_caravel-pcb-v4-FTDI-SMD.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.1 | 5.1 | 0.7&nbsp;ms | 4.9 | 0.2 | 0.6 | 0.3 | 12.6 |
| Simulation, STEP | 0.4 | 1.1 | 5.1 | 0.6&nbsp;ms | 4.7 | 4.0 | 0.6 | 0.2 | 16.1 |
| Simulation, STL | 0.3 | 1.0 | 5.0 | 0.6&nbsp;ms | 4.9 | 0.4 | 0.7 | 0.3 | 12.5 |
| Simulation, OBJ | 0.4 | 1.2 | 5.3 | 0.9&nbsp;ms | 4.8 | 6.3 | 0.5 | 0.2 | 18.7 |
| Visual, GLB | 0.4 | 1.1 | 4.8 | 0.5&nbsp;ms | 9.4 | 0.2 | 1.0 | 0.2 | 17.0 |
| Visual, OBJ | 0.4 | 1.1 | 4.9 | 0.3&nbsp;ms | 9.2 | 5.1 | 1.0 | 0.2 | 22.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/caravel_board](https://github.com/antmicro/caravel_board)<br>Board: `caravel_pcb_v4_FTDI_SMD.kicad_pcb` |
|---|---|
| Folder | hardware / caravel_pcb_v4_FTDI |
| Complexity | 303&nbsp;/&nbsp;1000 (size&nbsp;218, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 61, 854, 123 |
| Triangles,&nbsp;simulation | 1,217,782 in 103 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">42&nbsp;MB</td><td align="right">509&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">212&nbsp;MB</td><td align="right">671&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">61&nbsp;MB</td><td align="right">529&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">124&nbsp;MB</td><td align="right">815&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">33&nbsp;MB</td><td align="right">724&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">98&nbsp;MB</td><td align="right">772&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.30 cm4-baseboard

![cm4-baseboard: stages 4 and 6 take 42% to 79% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 98 s. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/cm4-baseboard_cm4-baseboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 12.0 | 10.4 | 30.5 | 1&nbsp;ms | 39.2 | 1.9 | 6.8 | 0.6 | 101.4 |
| Simulation, STEP | 11.8 | 10.9 | 30.1 | 2&nbsp;ms | 38.8 | 23.4 | 6.0 | 0.5 | 121.5 |
| Simulation, STL | 10.7 | 10.4 | 29.3 | 2&nbsp;ms | 37.0 | 4.0 | 6.0 | 0.5 | 98.0 |
| Simulation, OBJ | 10.8 | 10.0 | 29.6 | 1&nbsp;ms | 36.3 | 62.5 | 5.5 | 0.6 | 155.2 |
| Visual, GLB | 11.4 | 10.1 | 29.3 | 2&nbsp;ms | 95.0 | 0.9 | 9.6 | 0.4 | 156.7 |
| Visual, OBJ | 11.7 | 10.7 | 29.9 | 1&nbsp;ms | 92.1 | 35.7 | 9.0 | 0.4 | 189.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/cm4-baseboard](https://github.com/antmicro/cm4-baseboard)<br>Board: `cm4-baseboard.kicad_pcb` |
|---|---|
| Complexity | 472&nbsp;/&nbsp;1000 (size&nbsp;307, features&nbsp;165) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 442, 6,879, 1,129 |
| Triangles,&nbsp;simulation | 9,169,160 in 522 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">312&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.3&nbsp;GB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">459&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">986&nbsp;MB</td><td align="right">6.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">193&nbsp;MB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">622&nbsp;MB</td><td align="right">4.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.31 cm4-lvds-adapter

![cm4-lvds-adapter: stages 4 and 6 take 42% to 75% of a run. Simulation, GLB takes 19 s. Simulation, STEP takes 23 s. Simulation, STL takes 19 s. Simulation, OBJ takes 30 s. Visual, GLB takes 29 s. Visual, OBJ takes 36 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/cm4-baseboard-lvds-adapter_cm4-lvds-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.7 | 2.1 | 5.2 | 0.6&nbsp;ms | 7.1 | 0.3 | 1.1 | 0.3 | 18.8 |
| Simulation, STEP | 2.9 | 2.0 | 5.0 | 0.8&nbsp;ms | 7.1 | 5.0 | 1.0 | 0.3 | 23.3 |
| Simulation, STL | 2.9 | 2.0 | 4.9 | 0.5&nbsp;ms | 7.3 | 0.7 | 1.0 | 0.3 | 19.1 |
| Simulation, OBJ | 3.0 | 2.1 | 5.1 | 0.7&nbsp;ms | 7.5 | 11.2 | 1.0 | 0.3 | 30.3 |
| Visual, GLB | 2.9 | 1.9 | 4.9 | 0.8&nbsp;ms | 16.6 | 0.2 | 1.8 | 0.3 | 28.7 |
| Visual, OBJ | 3.1 | 2.0 | 5.3 | 0.9&nbsp;ms | 16.3 | 7.1 | 1.7 | 0.3 | 35.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/cm4-baseboard-lvds-adapter](https://github.com/antmicro/cm4-baseboard-lvds-adapter)<br>Board: `cm4-lvds-adapter.kicad_pcb` |
|---|---|
| Complexity | 408&nbsp;/&nbsp;1000 (size&nbsp;263, features&nbsp;145) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 130, 1,596, 254 |
| Triangles,&nbsp;simulation | 2,092,774 in 158 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">71&nbsp;MB</td><td align="right">737&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">278&nbsp;MB</td><td align="right">973&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">105&nbsp;MB</td><td align="right">738&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">218&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">889&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">140&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.32 com-express-7-baseboard

![com-express-7-baseboard: stages 4 and 6 take 42% to 83% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 4 min. Simulation, STL takes 3 min. Simulation, OBJ takes 6 min. Visual, GLB takes 6 min. Visual, OBJ takes 7 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/com-express-7-baseboard_com-express-7-baseboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 17.4 | 17.8 | 54.6 | 3&nbsp;ms | 79.1 | 4.6 | 12.4 | 1.0 | 186.9 |
| Simulation, STEP | 19.1 | 17.8 | 55.2 | 3&nbsp;ms | 77.6 | 42.2 | 12.4 | 0.8 | 225.1 |
| Simulation, STL | 18.8 | 17.4 | 55.7 | 3&nbsp;ms | 79.1 | 10.2 | 11.6 | 0.8 | 193.6 |
| Simulation, OBJ | 18.4 | 18.4 | 58.9 | 5&nbsp;ms | 84.5 | 143.3 | 13.6 | 1.1 | 338.2 |
| Visual, GLB | 19.8 | 17.8 | 56.5 | 3&nbsp;ms | 249.6 | 2.5 | 22.4 | 0.7 | 369.4 |
| Visual, OBJ | 17.6 | 18.0 | 55.6 | 3&nbsp;ms | 231.8 | 66.0 | 22.6 | 0.8 | 412.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/com-express-7-baseboard](https://github.com/antmicro/com-express-7-baseboard)<br>Board: `com-express-7-baseboard.kicad_pcb` |
|---|---|
| Complexity | 525&nbsp;/&nbsp;1000 (size&nbsp;345, features&nbsp;180) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 693, 10,459, 2,865 |
| Triangles,&nbsp;simulation | 21,291,582 in 1018 parts |
| Verifier | PASS in all six runs |
| Run&nbsp;again | Simulation, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">684&nbsp;MB</td><td align="right">6.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.3&nbsp;GB</td><td align="right">7.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.1&nbsp;GB</td><td align="right">6.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">2.3&nbsp;GB</td><td align="right">13&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">388&nbsp;MB</td><td align="right">6.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.3&nbsp;GB</td><td align="right">8.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.33 cvbs-mipi-bridge

![cvbs-mipi-bridge: stages 4 and 6 take 44% to 73% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 14 s. Simulation, STL takes 12 s. Simulation, OBJ takes 17 s. Visual, GLB takes 17 s. Visual, OBJ takes 22 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/cvbs-mipi-bridge_cvbs-mipi-bridge.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.8 | 1.1 | 3.7 | 0.6&nbsp;ms | 4.1 | 0.2 | 0.4 | 0.2 | 11.6 |
| Simulation, STEP | 1.8 | 1.1 | 3.8 | 0.5&nbsp;ms | 3.9 | 2.8 | 0.5 | 0.2 | 14.0 |
| Simulation, STL | 1.9 | 1.2 | 3.8 | 0.5&nbsp;ms | 3.8 | 0.4 | 0.4 | 0.3 | 11.8 |
| Simulation, OBJ | 1.8 | 1.2 | 3.6 | 0.8&nbsp;ms | 3.8 | 5.6 | 0.4 | 0.2 | 16.8 |
| Visual, GLB | 1.9 | 1.2 | 3.7 | 0.4&nbsp;ms | 8.8 | 0.1 | 1.3 | 0.3 | 17.2 |
| Visual, OBJ | 1.9 | 1.2 | 3.9 | 0.5&nbsp;ms | 9.1 | 3.9 | 1.3 | 0.3 | 21.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/cvbs-mipi-bridge](https://github.com/antmicro/cvbs-mipi-bridge)<br>Board: `cvbs-mipi-bridge.kicad_pcb` |
|---|---|
| Complexity | 375&nbsp;/&nbsp;1000 (size&nbsp;255, features&nbsp;120) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 98, 578, 295 |
| Triangles,&nbsp;simulation | 1,334,870 in 113 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">595&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">149&nbsp;MB</td><td align="right">735&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">67&nbsp;MB</td><td align="right">620&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">136&nbsp;MB</td><td align="right">988&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">796&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">92&nbsp;MB</td><td align="right">760&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.34 d1600e-psu-breakout-board

![d1600e-psu-breakout-board: stages 4 and 6 take 48% to 79% of a run. Simulation, GLB takes 37 s. Simulation, STEP takes 46 s. Simulation, STL takes 38 s. Simulation, OBJ takes 56 s. Visual, GLB takes 61 s. Visual, OBJ takes 74 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/d1600e-psu-breakout_d1600e-psu-breakout-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.5 | 4.0 | 13.6 | 0.9&nbsp;ms | 13.0 | 0.6 | 1.6 | 0.3 | 36.7 |
| Simulation, STEP | 3.8 | 4.1 | 13.3 | 1&nbsp;ms | 13.9 | 9.2 | 1.5 | 0.4 | 46.2 |
| Simulation, STL | 3.9 | 4.3 | 13.7 | 0.5&nbsp;ms | 13.1 | 1.3 | 1.6 | 0.3 | 38.2 |
| Simulation, OBJ | 3.6 | 4.0 | 13.7 | 0.5&nbsp;ms | 13.2 | 19.7 | 1.6 | 0.3 | 56.1 |
| Visual, GLB | 3.8 | 4.3 | 14.8 | 1&nbsp;ms | 33.5 | 0.5 | 3.7 | 0.3 | 61.0 |
| Visual, OBJ | 3.8 | 4.1 | 14.9 | 0.6&nbsp;ms | 34.3 | 13.3 | 3.8 | 0.4 | 74.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/d1600e-psu-breakout](https://github.com/antmicro/d1600e-psu-breakout)<br>Board: `d1600e-psu-breakout-board.kicad_pcb` |
|---|---|
| Complexity | 405&nbsp;/&nbsp;1000 (size&nbsp;265, features&nbsp;140) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 185, 985, 903 |
| Triangles,&nbsp;simulation | 4,123,478 in 180 parts |
| Verifier | PASS in all six runs |
| Run&nbsp;again | Visual, GLB; Visual, OBJ: failed in the corpus run, run again with fixes to KESE made after the corpus run, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">137&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">477&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">206&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">433&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">86&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">271&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.35 data-center-rdimm-ddr4-tester

![data-center-rdimm-ddr4-tester: stages 4 and 6 take 54% to 77% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 4 min. Simulation, STL takes 3 min. Visual, GLB takes 5 min. Visual, OBJ takes 6 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/data-center-dram-tester_data-center-rdimm-ddr4-tester.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 22.7 | 30.8 | 44.0 | 2&nbsp;ms | 85.8 | 4.8 | 12.4 | 1.1 | 201.5 |
| Simulation, STEP | 22.8 | 29.9 | 44.3 | 2&nbsp;ms | 89.9 | 47.7 | 12.6 | 0.9 | 248.2 |
| Simulation, STL | 22.5 | 30.1 | 44.6 | 3&nbsp;ms | 86.8 | 9.7 | 12.8 | 1.0 | 207.5 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB | 22.9 | 30.0 | 45.8 | 2&nbsp;ms | 186.0 | 1.9 | 15.6 | 0.6 | 302.7 |
| Visual, OBJ | 20.8 | 27.7 | 44.3 | 3&nbsp;ms | 177.7 | 68.1 | 16.4 | 0.7 | 355.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/data-center-dram-tester](https://github.com/antmicro/data-center-dram-tester)<br>Board: `data-center-rdimm-ddr4-tester.kicad_pcb` |
|---|---|
| Complexity | 559&nbsp;/&nbsp;1000 (size&nbsp;359, features&nbsp;200) |
| KESE&nbsp;features | through vias,<br>blind and buried vias,<br>slotted holes, custom pads,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 12 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 648, 21,939, 2,467 |
| Triangles,&nbsp;simulation | 25,480,794 in 941 parts |
| Verifier | Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">858&nbsp;MB</td><td align="right">6.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.4&nbsp;GB</td><td align="right">7.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.3&nbsp;GB</td><td align="right">6.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">353&nbsp;MB</td><td align="right">6.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.2&nbsp;GB</td><td align="right">7.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.36 dc-sci-debug-interposer

![dc-sci-debug-interposer: stages 4 and 6 take 40% to 78% of a run. Simulation, GLB takes 46 s. Simulation, STEP takes 57 s. Simulation, STL takes 47 s. Simulation, OBJ takes 81 s. Visual, GLB takes 76 s. Visual, OBJ takes 93 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/dc-sci-debug-interposer_dc-sci-debug-interposer.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.6 | 6.3 | 12.2 | 1.0&nbsp;ms | 19.7 | 1.1 | 2.7 | 0.4 | 46.1 |
| Simulation, STEP | 3.4 | 5.9 | 12.4 | 1&nbsp;ms | 20.1 | 11.8 | 3.0 | 0.4 | 57.1 |
| Simulation, STL | 3.8 | 6.0 | 12.2 | 1&nbsp;ms | 20.1 | 2.0 | 2.9 | 0.3 | 47.3 |
| Simulation, OBJ | 3.6 | 6.1 | 12.3 | 2&nbsp;ms | 20.3 | 35.3 | 2.7 | 0.3 | 80.7 |
| Visual, GLB | 3.7 | 6.2 | 12.8 | 1.0&nbsp;ms | 46.9 | 0.6 | 5.6 | 0.4 | 76.2 |
| Visual, OBJ | 3.6 | 6.0 | 12.5 | 1.0&nbsp;ms | 45.2 | 19.8 | 5.6 | 0.4 | 93.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/dc-sci-debug-interposer](https://github.com/antmicro/dc-sci-debug-interposer)<br>Board: `dc-sci-debug-interposer.kicad_pcb` |
|---|---|
| Complexity | 439&nbsp;/&nbsp;1000 (size&nbsp;294, features&nbsp;145) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 266, 4,217, 679 |
| Triangles,&nbsp;simulation | 5,925,818 in 368 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">199&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">706&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">296&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">632&nbsp;MB</td><td align="right">3.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">114&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">371&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.37 dc-scm-breakout-board

![dc-scm-breakout-board: stages 4 and 6 take 46% to 73% of a run. Simulation, GLB takes 60 s. Simulation, STEP takes 74 s. Simulation, STL takes 60 s. Simulation, OBJ takes 88 s. Visual, GLB takes 83 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/dc-scm-breakout-board_dc-scm-breakout-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 6.6 | 9.3 | 15.9 | 1&nbsp;ms | 24.5 | 0.9 | 2.7 | 0.4 | 60.4 |
| Simulation, STEP | 7.1 | 9.5 | 15.9 | 2&nbsp;ms | 24.7 | 13.6 | 2.6 | 0.4 | 73.8 |
| Simulation, STL | 6.8 | 9.4 | 15.8 | 1&nbsp;ms | 23.9 | 1.7 | 2.3 | 0.4 | 60.3 |
| Simulation, OBJ | 6.3 | 9.2 | 15.9 | 2&nbsp;ms | 24.3 | 29.6 | 2.5 | 0.4 | 88.2 |
| Visual, GLB | 6.7 | 9.3 | 15.9 | 1&nbsp;ms | 44.9 | 0.5 | 5.3 | 0.4 | 83.0 |
| Visual, OBJ | 6.4 | 9.3 | 16.0 | 2&nbsp;ms | 44.7 | 19.3 | 5.6 | 0.4 | 101.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/dc-scm-breakout-board](https://github.com/antmicro/dc-scm-breakout-board)<br>Board: `dc-scm-breakout-board.kicad_pcb` |
|---|---|
| Complexity | 449&nbsp;/&nbsp;1000 (size&nbsp;284, features&nbsp;165) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 282, 3,405, 582 |
| Triangles,&nbsp;simulation | 4,927,224 in 410 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">167&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">655&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">246&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">525&nbsp;MB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">105&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">336&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.38 bmc-reference-carrier-board

![bmc-reference-carrier-board: stages 4 and 6 take 40% to 79% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/dc-scm-osm-l-carrier-card_bmc-reference-carrier-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 9.2 | 12.0 | 28.2 | 2&nbsp;ms | 44.9 | 2.9 | 6.4 | 0.5 | 104.1 |
| Simulation, STEP | 9.4 | 11.4 | 27.2 | 2&nbsp;ms | 45.5 | 24.6 | 6.1 | 0.5 | 124.7 |
| Simulation, STL | 9.5 | 11.2 | 26.7 | 2&nbsp;ms | 44.7 | 6.5 | 6.7 | 0.7 | 106.1 |
| Simulation, OBJ | 9.7 | 12.1 | 27.8 | 2&nbsp;ms | 46.2 | 83.2 | 6.3 | 0.6 | 185.9 |
| Visual, GLB | 9.8 | 11.7 | 26.8 | 2&nbsp;ms | 105.3 | 1.0 | 13.2 | 0.5 | 168.3 |
| Visual, OBJ | 9.9 | 12.3 | 28.5 | 2&nbsp;ms | 104.6 | 33.9 | 13.0 | 0.4 | 202.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/dc-scm-osm-l-carrier-card](https://github.com/antmicro/dc-scm-osm-l-carrier-card)<br>Board: `bmc-reference-carrier-board.kicad_pcb` |
|---|---|
| Complexity | 527&nbsp;/&nbsp;1000 (size&nbsp;332, features&nbsp;195) |
| KESE&nbsp;features | through vias, padstacks,<br>slotted holes, custom pads,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 10 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 529, 8,646, 1,355 |
| Triangles,&nbsp;simulation | 14,795,830 in 1092 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">488&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.5&nbsp;GB</td><td align="right">4.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">740&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.6&nbsp;GB</td><td align="right">9.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">231&nbsp;MB</td><td align="right">4.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">765&nbsp;MB</td><td align="right">5.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.39 dc-scm-rot-jumper-card

![dc-scm-rot-jumper-card: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 5.3 s. Simulation, STEP takes 7.3 s. Simulation, STL takes 5.6 s. Simulation, OBJ takes 8.6 s. Visual, GLB takes 8.8 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/dc-scm-rot-jumper-card_dc-scm-rot-jumper-card.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 2.0 | 0.4&nbsp;ms | 2.1 | 65&nbsp;ms | 0.3 | 0.2 | 5.3 |
| Simulation, STEP | 0.2 | 0.4 | 2.1 | 0.8&nbsp;ms | 2.1 | 2.1 | 0.2 | 0.2 | 7.3 |
| Simulation, STL | 0.3 | 0.3 | 2.2 | 0.3&nbsp;ms | 2.2 | 0.2 | 0.2 | 0.2 | 5.6 |
| Simulation, OBJ | 0.2 | 0.4 | 2.3 | 0.2&nbsp;ms | 2.2 | 3.0 | 0.3 | 0.2 | 8.6 |
| Visual, GLB | 0.3 | 0.4 | 2.2 | 0.3&nbsp;ms | 5.1 | 57&nbsp;ms | 0.4 | 0.3 | 8.8 |
| Visual, OBJ | 0.2 | 0.4 | 2.3 | 0.3&nbsp;ms | 6.0 | 2.1 | 0.5 | 0.2 | 11.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/dc-scm-rot-jumper-card](https://github.com/antmicro/dc-scm-rot-jumper-card)<br>Board: `dc-scm-rot-jumper-card.kicad_pcb` |
|---|---|
| Complexity | 188&nbsp;/&nbsp;1000 (size&nbsp;153, features&nbsp;35) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 23, 348, 48 |
| Triangles,&nbsp;simulation | 407,326 in 58 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">292&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">90&nbsp;MB</td><td align="right">353&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">20&nbsp;MB</td><td align="right">314&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">43&nbsp;MB</td><td align="right">353&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">10&nbsp;MB</td><td align="right">326&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">31&nbsp;MB</td><td align="right">331&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.40 ddr4-spd-breakout

![ddr4-spd-breakout: stages 4 and 6 take 53% to 84% of a run. Simulation, GLB takes 26 s. Simulation, STEP takes 33 s. Simulation, STL takes 27 s. Simulation, OBJ takes 37 s. Visual, GLB takes 36 s. Visual, OBJ takes 45 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/ddr4-spd-breakout-board_ddr4-spd-breakout.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 2.8 | 9.8 | 0.7&nbsp;ms | 11.1 | 0.4 | 0.9 | 0.3 | 25.9 |
| Simulation, STEP | 0.5 | 2.7 | 9.6 | 0.2&nbsp;ms | 11.4 | 7.1 | 0.9 | 0.3 | 32.5 |
| Simulation, STL | 0.6 | 2.8 | 10.0 | 0.4&nbsp;ms | 11.7 | 1.0 | 0.9 | 0.3 | 27.4 |
| Simulation, OBJ | 0.7 | 2.7 | 9.2 | 0.4&nbsp;ms | 10.4 | 13.2 | 0.8 | 0.3 | 37.2 |
| Visual, GLB | 0.5 | 2.4 | 9.2 | 0.7&nbsp;ms | 21.4 | 0.3 | 2.1 | 0.3 | 36.2 |
| Visual, OBJ | 0.5 | 2.7 | 9.3 | 0.4&nbsp;ms | 21.7 | 8.2 | 2.0 | 0.3 | 44.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/ddr4-spd-breakout-board](https://github.com/antmicro/ddr4-spd-breakout-board)<br>Board: `ddr4-spd-breakout.kicad_pcb` |
|---|---|
| Complexity | 306&nbsp;/&nbsp;1000 (size&nbsp;241, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 57, 505, 450 |
| Triangles,&nbsp;simulation | 2,164,064 in 47 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">74&nbsp;MB</td><td align="right">807&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">270&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">108&nbsp;MB</td><td align="right">799&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">226&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">47&nbsp;MB</td><td align="right">926&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">144&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.41 ddr5-testbed

![ddr5-testbed: stages 4 and 6 take 45% to 79% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 20 s. Simulation, STL takes 16 s. Simulation, OBJ takes 25 s. Visual, GLB takes 22 s. Visual, OBJ takes 27 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/ddr5-testbed_ddr5-testbed.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.6 | 1.6 | 5.5 | 0.6&nbsp;ms | 5.9 | 0.3 | 0.8 | 0.2 | 16.0 |
| Simulation, STEP | 1.6 | 1.7 | 5.8 | 0.8&nbsp;ms | 5.9 | 4.1 | 0.9 | 0.2 | 20.3 |
| Simulation, STL | 1.7 | 1.7 | 5.4 | 0.6&nbsp;ms | 5.8 | 0.5 | 0.8 | 0.2 | 16.2 |
| Simulation, OBJ | 1.8 | 1.6 | 5.3 | 0.7&nbsp;ms | 6.0 | 9.2 | 0.8 | 0.3 | 25.0 |
| Visual, GLB | 1.8 | 1.6 | 5.5 | 0.7&nbsp;ms | 12.2 | 0.2 | 1.0 | 0.2 | 22.4 |
| Visual, OBJ | 1.6 | 1.6 | 5.6 | 0.8&nbsp;ms | 12.0 | 5.2 | 1.1 | 0.3 | 27.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/ddr5-testbed](https://github.com/antmicro/ddr5-testbed)<br>Board: `ddr5-testbed.kicad_pcb` |
|---|---|
| Complexity | 379&nbsp;/&nbsp;1000 (size&nbsp;284, features&nbsp;95) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 59, 5,140, 180 |
| Triangles,&nbsp;simulation | 1,652,750 in 238 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">57&nbsp;MB</td><td align="right">655&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">245&nbsp;MB</td><td align="right">736&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">83&nbsp;MB</td><td align="right">618&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">175&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">750&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">97&nbsp;MB</td><td align="right">809&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.42 data-center-rdimm-ddr5-tester

![data-center-rdimm-ddr5-tester: stages 4 and 6 take 42% to 76% of a run. Simulation, GLB takes 4 min. Simulation, STEP takes 5 min. Simulation, STL takes 4 min. Simulation, OBJ takes 4 min. Visual, GLB takes 6 min. Visual, OBJ takes 8 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/ddr5-tester_data-center-rdimm-ddr5-tester.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 34.9 | 27.7 | 60.3 | 5&nbsp;ms | 98.7 | 5.8 | 15.7 | 1.0 | 244.2 |
| Simulation, STEP | 34.6 | 23.9 | 55.8 | 2&nbsp;ms | 93.1 | 58.3 | 13.8 | 1.3 | 280.9 |
| Simulation, STL | 34.0 | 25.2 | 57.9 | 2&nbsp;ms | 106.4 | 14.7 | 16.3 | 1.6 | 256.0 |
| Simulation, OBJ | 20.1 | 16.2 | 39.6 | 2&nbsp;ms | 65.3 | 98.1 | 8.5 | 0.8 | 248.7 |
| Visual, GLB | 36.2 | 26.9 | 57.6 | 3&nbsp;ms | 228.3 | 2.3 | 23.4 | 0.9 | 375.5 |
| Visual, OBJ | 33.2 | 24.7 | 58.6 | 5&nbsp;ms | 232.4 | 115.4 | 23.1 | 1.0 | 488.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/ddr5-tester](https://github.com/antmicro/ddr5-tester)<br>Board: `data-center-rdimm-ddr5-tester.kicad_pcb` |
|---|---|
| Complexity | 560&nbsp;/&nbsp;1000 (size&nbsp;365, features&nbsp;195) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 12 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 761, 19,710, 2,625 |
| Triangles,&nbsp;simulation | 22,023,050 in 849 parts |
| Verifier | PASS in all six runs |
| Run&nbsp;again | Simulation, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">698&nbsp;MB</td><td align="right">6.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.2&nbsp;GB</td><td align="right">6.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.1&nbsp;GB</td><td align="right">5.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">2.4&nbsp;GB</td><td align="right">14&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">361&nbsp;MB</td><td align="right">6.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.2&nbsp;GB</td><td align="right">8.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.43 dual-camera-to-gmsl-serializer-csi-adapter

![Stages 4 and 6 take 43% to 76% of a run. Simulation, GLB takes 19 s. Simulation, STEP takes 29 s. Simulation, STL takes 20 s. Simulation, OBJ takes 31 s. Visual, GLB takes 31 s. Visual, OBJ takes 41 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/dual-gmsl-serializer-adapter_dual-camera-to-gmsl-serializer-csi-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.4 | 1.9 | 6.7 | 0.6&nbsp;ms | 6.7 | 0.3 | 0.8 | 0.3 | 19.1 |
| Simulation, STEP | 2.6 | 2.3 | 7.5 | 0.9&nbsp;ms | 9.5 | 5.7 | 0.8 | 0.3 | 28.8 |
| Simulation, STL | 2.4 | 2.0 | 6.5 | 1.0&nbsp;ms | 7.0 | 0.6 | 0.8 | 0.3 | 19.7 |
| Simulation, OBJ | 2.8 | 2.0 | 6.6 | 0.5&nbsp;ms | 6.7 | 12.0 | 0.8 | 0.4 | 31.2 |
| Visual, GLB | 2.3 | 1.9 | 6.2 | 0.6&nbsp;ms | 17.1 | 0.3 | 2.4 | 0.3 | 30.6 |
| Visual, OBJ | 2.6 | 1.9 | 6.7 | 1&nbsp;ms | 17.6 | 9.3 | 2.6 | 0.3 | 40.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/dual-gmsl-serializer-adapter](https://github.com/antmicro/dual-gmsl-serializer-adapter)<br>Board: `dual-camera-to-gmsl-serializer-csi-adapter.kicad_pcb` |
|---|---|
| Complexity | 357&nbsp;/&nbsp;1000 (size&nbsp;212, features&nbsp;145) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 95, 1,730, 289 |
| Triangles,&nbsp;simulation | 1,904,014 in 141 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">66&nbsp;MB</td><td align="right">850&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">246&nbsp;MB</td><td align="right">891&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">95&nbsp;MB</td><td align="right">836&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">202&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">48&nbsp;MB</td><td align="right">911&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">150&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.44 dual-ipex-csi-interposer

![dual-ipex-csi-interposer: stages 4 and 6 take 49% to 82% of a run. Simulation, GLB takes 6.3 s. Simulation, STEP takes 8.3 s. Simulation, STL takes 5.9 s. Simulation, OBJ takes 9.2 s. Visual, GLB takes 8.6 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/dual-ipex-csi-interposer_dual-ipex-csi-interposer.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 2.2 | 0.4&nbsp;ms | 2.5 | 0.1 | 0.4 | 0.3 | 6.3 |
| Simulation, STEP | 0.3 | 0.6 | 2.1 | 0.4&nbsp;ms | 2.5 | 2.3 | 0.3 | 0.2 | 8.3 |
| Simulation, STL | 0.2 | 0.6 | 2.0 | 0.4&nbsp;ms | 2.4 | 0.2 | 0.4 | 0.2 | 5.9 |
| Simulation, OBJ | 0.2 | 0.6 | 1.9 | 0.3&nbsp;ms | 2.6 | 3.3 | 0.4 | 0.2 | 9.2 |
| Visual, GLB | 0.2 | 0.6 | 1.9 | 0.4&nbsp;ms | 5.1 | 67&nbsp;ms | 0.4 | 0.2 | 8.6 |
| Visual, OBJ | 0.2 | 0.6 | 2.0 | 0.3&nbsp;ms | 5.2 | 2.5 | 0.5 | 0.2 | 11.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/dual-ipex-csi-interposer](https://github.com/antmicro/dual-ipex-csi-interposer)<br>Board: `dual-ipex-csi-interposer.kicad_pcb` |
|---|---|
| Complexity | 267&nbsp;/&nbsp;1000 (size&nbsp;172, features&nbsp;95) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 13, 511, 107 |
| Triangles,&nbsp;simulation | 645,608 in 69 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">22&nbsp;MB</td><td align="right">348&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">103&nbsp;MB</td><td align="right">417&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">32&nbsp;MB</td><td align="right">350&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">65&nbsp;MB</td><td align="right">479&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">457&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">45&nbsp;MB</td><td align="right">455&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.45 ecp5-dc-scm

![ecp5-dc-scm: stages 4 and 6 take 47% to 80% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 3 min. Simulation, STL takes 3 min. Simulation, OBJ takes 4 min. Visual, GLB takes 4 min. Visual, OBJ takes 5 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/ecp5-dc-scm_ecp5-dc-scm.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 16.6 | 18.0 | 61.9 | 5&nbsp;ms | 63.3 | 3.7 | 9.1 | 0.8 | 173.4 |
| Simulation, STEP | 16.2 | 16.0 | 63.4 | 2&nbsp;ms | 61.9 | 33.5 | 8.7 | 0.8 | 200.4 |
| Simulation, STL | 14.5 | 15.6 | 61.0 | 2&nbsp;ms | 64.6 | 7.6 | 9.2 | 0.8 | 173.4 |
| Simulation, OBJ | 15.7 | 15.8 | 61.9 | 2&nbsp;ms | 63.8 | 100.0 | 9.4 | 0.9 | 267.5 |
| Visual, GLB | 16.0 | 16.3 | 60.4 | 2&nbsp;ms | 139.2 | 1.4 | 14.8 | 0.7 | 248.8 |
| Visual, OBJ | 15.8 | 15.7 | 60.2 | 3&nbsp;ms | 140.8 | 42.4 | 14.3 | 0.7 | 289.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/ecp5-dc-scm](https://github.com/antmicro/ecp5-dc-scm)<br>Board: `ecp5-dc-scm.kicad_pcb` |
|---|---|
| Complexity | 508&nbsp;/&nbsp;1000 (size&nbsp;343, features&nbsp;165) |
| KESE&nbsp;features | through vias,<br>blind and buried vias, custom pads,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 488, 12,884, 1,545 |
| Triangles,&nbsp;simulation | 13,991,872 in 803 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">480&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.8&nbsp;GB</td><td align="right">4.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">700&nbsp;MB</td><td align="right">3.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.5&nbsp;GB</td><td align="right">9.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">231&nbsp;MB</td><td align="right">4.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">763&nbsp;MB</td><td align="right">5.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.46 environment-sensor

![environment-sensor: stages 4 and 6 take 47% to 75% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 16 s. Simulation, STL takes 13 s. Simulation, OBJ takes 17 s. Visual, GLB takes 18 s. Visual, OBJ takes 22 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/environment-sensor_environment-sensor.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.8 | 1.0 | 3.2 | 0.6&nbsp;ms | 5.0 | 0.2 | 0.6 | 0.3 | 12.0 |
| Simulation, STEP | 1.8 | 0.9 | 3.4 | 0.5&nbsp;ms | 5.1 | 3.4 | 0.6 | 0.3 | 15.5 |
| Simulation, STL | 1.8 | 1.0 | 3.4 | 0.5&nbsp;ms | 5.1 | 0.4 | 0.5 | 0.3 | 12.5 |
| Simulation, OBJ | 1.9 | 1.0 | 3.4 | 0.5&nbsp;ms | 4.9 | 5.5 | 0.5 | 0.2 | 17.4 |
| Visual, GLB | 1.9 | 1.1 | 3.4 | 0.5&nbsp;ms | 9.9 | 0.1 | 1.2 | 0.3 | 17.8 |
| Visual, OBJ | 1.9 | 1.0 | 3.2 | 0.5&nbsp;ms | 9.9 | 4.4 | 1.1 | 0.2 | 21.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/environment-sensor](https://github.com/antmicro/environment-sensor)<br>Board: `environment-sensor.kicad_pcb` |
|---|---|
| Complexity | 341&nbsp;/&nbsp;1000 (size&nbsp;246, features&nbsp;95) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 92, 863, 144 |
| Triangles,&nbsp;simulation | 1,221,012 in 105 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">42&nbsp;MB</td><td align="right">559&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">208&nbsp;MB</td><td align="right">681&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">61&nbsp;MB</td><td align="right">555&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">126&nbsp;MB</td><td align="right">890&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">803&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">91&nbsp;MB</td><td align="right">793&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.47 environment-sensor-sip-baseboard

![Stages 4 and 6 take 49% to 80% of a run. Simulation, GLB takes 9.6 s. Simulation, STEP takes 13 s. Simulation, STL takes 10 s. Simulation, OBJ takes 15 s. Visual, GLB takes 14 s. Visual, OBJ takes 17 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/environment-sensor-myra-baseboard_environment-sensor-sip-baseboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 0.8 | 3.3 | 0.4&nbsp;ms | 3.8 | 0.1 | 0.5 | 0.3 | 9.6 |
| Simulation, STEP | 0.8 | 0.9 | 3.5 | 0.4&nbsp;ms | 3.8 | 3.0 | 0.5 | 0.2 | 12.6 |
| Simulation, STL | 0.9 | 0.9 | 3.5 | 0.4&nbsp;ms | 3.8 | 0.2 | 0.6 | 0.3 | 10.3 |
| Simulation, OBJ | 0.8 | 0.8 | 3.4 | 0.3&nbsp;ms | 3.9 | 4.9 | 0.7 | 0.3 | 14.9 |
| Visual, GLB | 0.8 | 0.9 | 3.6 | 0.4&nbsp;ms | 7.7 | 0.1 | 0.8 | 0.2 | 14.1 |
| Visual, OBJ | 0.8 | 0.8 | 3.3 | 0.5&nbsp;ms | 8.2 | 3.2 | 0.7 | 0.2 | 17.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/environment-sensor-myra-baseboard](https://github.com/antmicro/environment-sensor-myra-baseboard)<br>Board: `environment-sensor-sip-baseboard.kicad_pcb` |
|---|---|
| Complexity | 372&nbsp;/&nbsp;1000 (size&nbsp;232, features&nbsp;140) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 33, 434, 106 |
| Triangles,&nbsp;simulation | 824,680 in 64 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">410&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">133&nbsp;MB</td><td align="right">482&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">41&nbsp;MB</td><td align="right">407&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">84&nbsp;MB</td><td align="right">636&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">545&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">58&nbsp;MB</td><td align="right">550&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.48 lz1-led-driver

![lz1-led-driver: stages 4 and 6 take 46% to 79% of a run. Simulation, GLB takes 7.2 s. Simulation, STEP takes 9.6 s. Simulation, STL takes 7.1 s. Simulation, OBJ takes 11 s. Visual, GLB takes 10 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/flickerless-led-driver_lz1-led-driver.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.1 | 0.5 | 2.6 | 0.2&nbsp;ms | 2.4 | 97&nbsp;ms | 0.4 | 0.2 | 7.2 |
| Simulation, STEP | 1.1 | 0.5 | 2.7 | 0.2&nbsp;ms | 2.5 | 2.1 | 0.4 | 0.3 | 9.6 |
| Simulation, STL | 1.0 | 0.5 | 2.5 | 0.2&nbsp;ms | 2.3 | 0.2 | 0.4 | 0.2 | 7.1 |
| Simulation, OBJ | 1.0 | 0.5 | 2.6 | 0.2&nbsp;ms | 2.3 | 3.7 | 0.4 | 0.2 | 10.7 |
| Visual, GLB | 0.9 | 0.5 | 2.6 | 0.2&nbsp;ms | 5.6 | 74&nbsp;ms | 0.4 | 0.2 | 10.3 |
| Visual, OBJ | 0.9 | 0.5 | 2.6 | 0.2&nbsp;ms | 5.8 | 2.7 | 0.5 | 0.2 | 13.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/flickerless-led-driver](https://github.com/antmicro/flickerless-led-driver)<br>Board: `lz1-led-driver.kicad_pcb` |
|---|---|
| Complexity | 253&nbsp;/&nbsp;1000 (size&nbsp;158, features&nbsp;95) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 41, 161, 101 |
| Triangles,&nbsp;simulation | 675,574 in 39 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">391&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">135&nbsp;MB</td><td align="right">447&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">34&nbsp;MB</td><td align="right">391&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">69&nbsp;MB</td><td align="right">512&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">460&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">49&nbsp;MB</td><td align="right">490&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.49 fmc2sata

![fmc2sata: stages 4 and 6 take 49% to 82% of a run. Simulation, GLB takes 19 s. Simulation, STEP takes 24 s. Simulation, STL takes 20 s. Simulation, OBJ takes 30 s. Visual, GLB takes 28 s. Visual, OBJ takes 34 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/fmc-sata-adapter_fmc2sata.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.2 | 8.1 | 0.7&nbsp;ms | 6.5 | 0.3 | 0.7 | 0.3 | 18.9 |
| Simulation, STEP | 0.8 | 2.2 | 8.1 | 0.8&nbsp;ms | 6.9 | 5.3 | 0.7 | 0.3 | 24.2 |
| Simulation, STL | 0.7 | 2.2 | 8.3 | 1.0&nbsp;ms | 6.9 | 0.7 | 0.7 | 0.3 | 19.8 |
| Simulation, OBJ | 0.7 | 2.3 | 8.1 | 0.7&nbsp;ms | 6.8 | 11.2 | 0.8 | 0.3 | 30.0 |
| Visual, GLB | 0.7 | 2.3 | 8.2 | 0.7&nbsp;ms | 15.0 | 0.2 | 1.5 | 0.3 | 28.3 |
| Visual, OBJ | 0.8 | 2.2 | 8.2 | 0.7&nbsp;ms | 14.4 | 6.6 | 1.6 | 0.3 | 34.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/fmc-sata-adapter](https://github.com/antmicro/fmc-sata-adapter)<br>Board: `fmc2sata.kicad_pcb` |
|---|---|
| Complexity | 253&nbsp;/&nbsp;1000 (size&nbsp;198, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 59, 769, 258 |
| Triangles,&nbsp;simulation | 1,824,356 in 179 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">63&nbsp;MB</td><td align="right">888&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">287&nbsp;MB</td><td align="right">891&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">91&nbsp;MB</td><td align="right">821&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">193&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">865&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">119&nbsp;MB</td><td align="right">887&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.50 framos-csi-adapter

![framos-csi-adapter: stages 4 and 6 take 43% to 75% of a run. Simulation, GLB takes 7.7 s. Simulation, STEP takes 10 s. Simulation, STL takes 8.0 s. Simulation, OBJ takes 12 s. Visual, GLB takes 12 s. Visual, OBJ takes 15 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/framos-csi-adapter_framos-csi-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.4 | 0.6 | 2.1 | 0.6&nbsp;ms | 2.9 | 0.1 | 0.4 | 0.2 | 7.7 |
| Simulation, STEP | 1.5 | 0.6 | 2.1 | 0.3&nbsp;ms | 2.8 | 2.5 | 0.5 | 0.2 | 10.3 |
| Simulation, STL | 1.4 | 0.7 | 2.1 | 0.3&nbsp;ms | 3.0 | 0.2 | 0.4 | 0.2 | 8.0 |
| Simulation, OBJ | 1.4 | 0.6 | 2.2 | 0.3&nbsp;ms | 3.0 | 4.1 | 0.5 | 0.2 | 12.0 |
| Visual, GLB | 1.4 | 0.7 | 2.3 | 0.6&nbsp;ms | 6.8 | 87&nbsp;ms | 0.6 | 0.3 | 12.1 |
| Visual, OBJ | 1.4 | 0.7 | 2.3 | 0.3&nbsp;ms | 6.5 | 3.1 | 0.6 | 0.2 | 14.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/framos-csi-adapter](https://github.com/antmicro/framos-csi-adapter)<br>Board: `framos-csi-adapter.kicad_pcb` |
|---|---|
| Complexity | 297&nbsp;/&nbsp;1000 (size&nbsp;187, features&nbsp;110) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 41, 705, 87 |
| Triangles,&nbsp;simulation | 762,210 in 81 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">418&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">131&nbsp;MB</td><td align="right">457&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">38&nbsp;MB</td><td align="right">415&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">77&nbsp;MB</td><td align="right">589&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">554&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">58&nbsp;MB</td><td align="right">541&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.51 gem-demo-board

![gem-demo-board: stages 4 and 6 take 50% to 81% of a run. Simulation, GLB takes 39 s. Simulation, STEP takes 45 s. Simulation, STL takes 39 s. Simulation, OBJ takes 57 s. Visual, GLB takes 50 s. Visual, OBJ takes 63 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/gem-baseboard_gem-demo-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 5.4 | 15.6 | 1&nbsp;ms | 14.2 | 0.8 | 1.8 | 0.3 | 39.0 |
| Simulation, STEP | 0.7 | 5.1 | 14.7 | 1&nbsp;ms | 14.0 | 8.2 | 2.2 | 0.3 | 45.2 |
| Simulation, STL | 0.8 | 5.3 | 15.6 | 2&nbsp;ms | 14.5 | 1.2 | 1.7 | 0.3 | 39.4 |
| Simulation, OBJ | 0.8 | 5.1 | 14.5 | 1&nbsp;ms | 14.1 | 20.8 | 1.7 | 0.3 | 57.3 |
| Visual, GLB | 0.8 | 5.1 | 14.3 | 1.0&nbsp;ms | 25.7 | 0.3 | 2.9 | 0.3 | 49.5 |
| Visual, OBJ | 0.8 | 5.1 | 14.8 | 1&nbsp;ms | 27.6 | 11.1 | 3.0 | 0.3 | 62.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/gem-baseboard](https://github.com/antmicro/gem-baseboard)<br>Board: `gem-demo-board.kicad_pcb` |
|---|---|
| Complexity | 290&nbsp;/&nbsp;1000 (size&nbsp;235, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 122, 3,756, 417 |
| Triangles,&nbsp;simulation | 3,761,442 in 229 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">130&nbsp;MB</td><td align="right">988&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">482&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">188&nbsp;MB</td><td align="right">954&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">403&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">64&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">206&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.52 zglue-gem1-adapter

![zglue-gem1-adapter: stages 4 and 6 take 43% to 79% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 17 s. Simulation, STL takes 14 s. Simulation, OBJ takes 22 s. Visual, GLB takes 20 s. Visual, OBJ takes 26 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/gem1-adapter_zglue-gem1-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 2.1 | 4.6 | 0.7&nbsp;ms | 4.9 | 0.3 | 0.8 | 0.3 | 13.4 |
| Simulation, STEP | 0.3 | 2.1 | 5.0 | 0.6&nbsp;ms | 5.1 | 3.5 | 0.8 | 0.2 | 17.0 |
| Simulation, STL | 0.4 | 2.1 | 4.9 | 0.6&nbsp;ms | 5.2 | 0.4 | 0.8 | 0.2 | 14.1 |
| Simulation, OBJ | 0.4 | 2.1 | 4.6 | 0.6&nbsp;ms | 5.0 | 9.2 | 0.8 | 0.2 | 22.4 |
| Visual, GLB | 0.4 | 2.1 | 4.8 | 0.6&nbsp;ms | 10.8 | 0.1 | 1.1 | 0.2 | 19.6 |
| Visual, OBJ | 0.4 | 2.1 | 4.9 | 0.6&nbsp;ms | 11.4 | 5.3 | 1.3 | 0.2 | 25.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/gem1-adapter](https://github.com/antmicro/gem1-adapter)<br>Board: `zglue-gem1-adapter.kicad_pcb` |
|---|---|
| Complexity | 315&nbsp;/&nbsp;1000 (size&nbsp;270, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 44, 2,794, 221 |
| Triangles,&nbsp;simulation | 1,631,130 in 133 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">54&nbsp;MB</td><td align="right">571&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">188&nbsp;MB</td><td align="right">658&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">82&nbsp;MB</td><td align="right">574&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">170&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">29&nbsp;MB</td><td align="right">717&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">91&nbsp;MB</td><td align="right">714&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.53 gem2-adapter

![gem2-adapter: stages 4 and 6 take 48% to 82% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 16 s. Simulation, STL takes 13 s. Simulation, OBJ takes 19 s. Visual, GLB takes 19 s. Visual, OBJ takes 24 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/gem2-adapter_gem2-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 2.0 | 4.5 | 0.6&nbsp;ms | 5.0 | 0.2 | 0.8 | 0.3 | 13.1 |
| Simulation, STEP | 0.3 | 2.2 | 4.4 | 0.6&nbsp;ms | 5.2 | 2.9 | 0.8 | 0.3 | 16.0 |
| Simulation, STL | 0.3 | 1.8 | 4.3 | 0.8&nbsp;ms | 5.1 | 0.4 | 0.7 | 0.2 | 12.9 |
| Simulation, OBJ | 0.3 | 1.8 | 4.3 | 0.6&nbsp;ms | 5.1 | 7.0 | 0.8 | 0.2 | 19.4 |
| Visual, GLB | 0.3 | 1.7 | 4.2 | 0.5&nbsp;ms | 11.3 | 0.1 | 1.0 | 0.2 | 18.8 |
| Visual, OBJ | 0.3 | 1.9 | 4.5 | 0.7&nbsp;ms | 11.4 | 3.9 | 1.2 | 0.3 | 23.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/gem2-adapter](https://github.com/antmicro/gem2-adapter)<br>Board: `gem2-adapter.kicad_pcb` |
|---|---|
| Complexity | 313&nbsp;/&nbsp;1000 (size&nbsp;268, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 46, 2,404, 212 |
| Triangles,&nbsp;simulation | 1,644,764 in 133 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">55&nbsp;MB</td><td align="right">576&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">198&nbsp;MB</td><td align="right">633&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">82&nbsp;MB</td><td align="right">541&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">172&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">747&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">94&nbsp;MB</td><td align="right">769&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.54 gmsl-deserializer

![gmsl-deserializer: stages 4 and 6 take 52% to 75% of a run. Simulation, GLB takes 30 s. Simulation, STEP takes 37 s. Simulation, STL takes 30 s. Simulation, OBJ takes 43 s. Visual, GLB takes 41 s. Visual, OBJ takes 51 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/gmsl-deserializer_gmsl-deserializer.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.8 | 2.5 | 8.1 | 1&nbsp;ms | 13.4 | 0.5 | 1.1 | 0.3 | 29.7 |
| Simulation, STEP | 3.7 | 2.4 | 8.3 | 0.4&nbsp;ms | 13.7 | 7.5 | 1.0 | 0.3 | 37.0 |
| Simulation, STL | 3.7 | 2.3 | 8.4 | 0.7&nbsp;ms | 13.7 | 1.0 | 1.0 | 0.3 | 30.5 |
| Simulation, OBJ | 3.9 | 2.2 | 8.0 | 0.9&nbsp;ms | 14.0 | 13.4 | 1.0 | 0.3 | 42.8 |
| Visual, GLB | 3.8 | 2.4 | 8.0 | 0.8&nbsp;ms | 22.8 | 0.3 | 3.2 | 0.3 | 40.9 |
| Visual, OBJ | 3.7 | 2.5 | 8.5 | 0.8&nbsp;ms | 23.0 | 10.0 | 3.4 | 0.3 | 51.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/gmsl-deserializer](https://github.com/antmicro/gmsl-deserializer)<br>Board: `gmsl-deserializer.kicad_pcb` |
|---|---|
| Complexity | 420&nbsp;/&nbsp;1000 (size&nbsp;265, features&nbsp;155) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 206, 2,413, 362 |
| Triangles,&nbsp;simulation | 2,685,502 in 163 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">91&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">412&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">134&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">281&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">69&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">215&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.55 gmsl-serializer

![gmsl-serializer: stages 4 and 6 take 48% to 73% of a run. Simulation, GLB takes 14 s. Simulation, STEP takes 19 s. Simulation, STL takes 14 s. Simulation, OBJ takes 21 s. Visual, GLB takes 20 s. Visual, OBJ takes 25 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/gmsl-serializer_gmsl-serializer.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.9 | 1.3 | 4.1 | 0.4&nbsp;ms | 5.8 | 0.3 | 0.6 | 0.3 | 14.2 |
| Simulation, STEP | 2.4 | 1.3 | 4.3 | 0.5&nbsp;ms | 6.2 | 3.8 | 0.6 | 0.2 | 18.9 |
| Simulation, STL | 2.2 | 1.2 | 4.3 | 0.6&nbsp;ms | 5.5 | 0.5 | 0.5 | 0.3 | 14.5 |
| Simulation, OBJ | 2.2 | 1.3 | 4.3 | 0.5&nbsp;ms | 5.8 | 6.4 | 0.6 | 0.3 | 20.9 |
| Visual, GLB | 2.3 | 1.3 | 4.0 | 0.6&nbsp;ms | 10.2 | 0.1 | 1.4 | 0.3 | 19.5 |
| Visual, OBJ | 2.2 | 1.5 | 4.4 | 0.6&nbsp;ms | 10.9 | 4.6 | 1.7 | 0.2 | 25.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/gmsl-serializer](https://github.com/antmicro/gmsl-serializer)<br>Board: `gmsl-serializer.kicad_pcb` |
|---|---|
| Complexity | 374&nbsp;/&nbsp;1000 (size&nbsp;244, features&nbsp;130) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, knockout text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 104, 878, 206 |
| Triangles,&nbsp;simulation | 1,204,088 in 110 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">42&nbsp;MB</td><td align="right">561&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">154&nbsp;MB</td><td align="right">643&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">60&nbsp;MB</td><td align="right">558&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">125&nbsp;MB</td><td align="right">876&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">709&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">90&nbsp;MB</td><td align="right">792&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.56 gpu-cluster-backplane

![gpu-cluster-backplane: stages 4 and 6 take 45% to 81% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 3 min. Simulation, STL takes 3 min. Simulation, OBJ takes 4 min. Visual, GLB takes 4 min. Visual, OBJ takes 5 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/gpu-cluster-backplane_gpu-cluster-backplane.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 10.8 | 17.0 | 48.5 | 1&nbsp;ms | 57.8 | 2.3 | 5.8 | 0.6 | 143.0 |
| Simulation, STEP | 10.8 | 18.0 | 50.4 | 1&nbsp;ms | 60.0 | 30.1 | 6.2 | 0.6 | 176.2 |
| Simulation, STL | 11.6 | 18.3 | 52.8 | 1&nbsp;ms | 60.1 | 6.3 | 6.6 | 0.6 | 156.2 |
| Simulation, OBJ | 11.2 | 18.9 | 51.9 | 2&nbsp;ms | 60.7 | 100.6 | 6.9 | 0.6 | 250.7 |
| Visual, GLB | 11.5 | 18.5 | 51.9 | 1&nbsp;ms | 148.1 | 1.4 | 15.8 | 0.7 | 248.0 |
| Visual, OBJ | 12.1 | 21.0 | 52.6 | 1&nbsp;ms | 152.4 | 56.9 | 14.6 | 0.5 | 310.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/gpu-cluster-backplane](https://github.com/antmicro/gpu-cluster-backplane)<br>Board: `gpu-cluster-backplane.kicad_pcb` |
|---|---|
| Complexity | 457&nbsp;/&nbsp;1000 (size&nbsp;307, features&nbsp;150) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 541, 4,646, 3,885 |
| Triangles,&nbsp;simulation | 13,710,074 in 399 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">448&nbsp;MB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.3&nbsp;GB</td><td align="right">4.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">686&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.5&nbsp;GB</td><td align="right">8.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">294&nbsp;MB</td><td align="right">5.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">956&nbsp;MB</td><td align="right">6.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.57 hdmi-edid-debug-board

![hdmi-edid-debug-board: stages 4 and 6 take 47% to 78% of a run. Simulation, GLB takes 14 s. Simulation, STEP takes 17 s. Simulation, STL takes 14 s. Simulation, OBJ takes 21 s. Visual, GLB takes 20 s. Visual, OBJ takes 25 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/hdmi-edid-debug-board_hdmi-edid-debug-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.1 | 1.3 | 5.0 | 0.6&nbsp;ms | 4.5 | 0.2 | 0.5 | 0.2 | 13.8 |
| Simulation, STEP | 1.9 | 1.3 | 5.1 | 0.4&nbsp;ms | 4.8 | 3.6 | 0.5 | 0.2 | 17.4 |
| Simulation, STL | 2.0 | 1.3 | 5.1 | 0.5&nbsp;ms | 5.0 | 0.4 | 0.5 | 0.2 | 14.4 |
| Simulation, OBJ | 1.9 | 1.2 | 5.0 | 0.4&nbsp;ms | 4.8 | 7.2 | 0.6 | 0.2 | 21.0 |
| Visual, GLB | 2.0 | 1.3 | 5.0 | 0.5&nbsp;ms | 10.8 | 0.1 | 0.9 | 0.2 | 20.3 |
| Visual, OBJ | 2.0 | 1.3 | 4.9 | 0.4&nbsp;ms | 10.3 | 5.3 | 1.1 | 0.3 | 25.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/hdmi-edid-debug-board](https://github.com/antmicro/hdmi-edid-debug-board)<br>Board: `hdmi-edid-debug-board.kicad_pcb` |
|---|---|
| Complexity | 396&nbsp;/&nbsp;1000 (size&nbsp;246, features&nbsp;150) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 98, 1,266, 175 |
| Triangles,&nbsp;simulation | 1,401,090 in 109 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">49&nbsp;MB</td><td align="right">634&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">193&nbsp;MB</td><td align="right">732&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">70&nbsp;MB</td><td align="right">613&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">146&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">36&nbsp;MB</td><td align="right">882&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">109&nbsp;MB</td><td align="right">882&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.58 antmicro-hdmi-mipi-bridge-hw

![antmicro-hdmi-mipi-bridge-hw: stages 4 and 6 take 50% to 75% of a run. Simulation, GLB takes 22 s. Simulation, STEP takes 27 s. Simulation, STL takes 21 s. Simulation, OBJ takes 30 s. Visual, GLB takes 27 s. Visual, OBJ takes 35 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/hdmi-mipi-bridge_antmicro-hdmi-mipi-bridge-hw.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.8 | 1.8 | 6.3 | 0.4&nbsp;ms | 9.4 | 0.4 | 0.9 | 0.3 | 21.8 |
| Simulation, STEP | 2.8 | 1.7 | 6.1 | 0.4&nbsp;ms | 9.6 | 5.9 | 0.8 | 0.3 | 27.2 |
| Simulation, STL | 3.0 | 1.7 | 5.6 | 0.4&nbsp;ms | 8.8 | 0.7 | 0.8 | 0.3 | 21.0 |
| Simulation, OBJ | 2.9 | 1.8 | 5.9 | 0.4&nbsp;ms | 9.0 | 9.2 | 0.8 | 0.3 | 29.8 |
| Visual, GLB | 2.8 | 1.6 | 5.8 | 0.5&nbsp;ms | 14.9 | 0.2 | 1.8 | 0.3 | 27.4 |
| Visual, OBJ | 2.8 | 1.7 | 6.0 | 0.5&nbsp;ms | 15.3 | 7.0 | 2.1 | 0.3 | 35.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/hdmi-mipi-bridge](https://github.com/antmicro/hdmi-mipi-bridge)<br>Board: `antmicro-hdmi-mipi-bridge-hw.kicad_pcb` |
|---|---|
| Complexity | 404&nbsp;/&nbsp;1000 (size&nbsp;274, features&nbsp;130) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 111, 1,960, 312 |
| Triangles,&nbsp;simulation | 2,009,788 in 160 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">67&nbsp;MB</td><td align="right">813&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">298&nbsp;MB</td><td align="right">974&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">101&nbsp;MB</td><td align="right">807&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">209&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">49&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">152&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.59 icicle-hdmi-breakout

![icicle-hdmi-breakout: stages 4 and 6 take 51% to 84% of a run. Simulation, GLB takes 9.8 s. Simulation, STEP takes 12 s. Simulation, STL takes 10 s. Simulation, OBJ takes 15 s. Visual, GLB takes 14 s. Visual, OBJ takes 17 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/icicle-hdmi-breakout_icicle-hdmi-breakout.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.0 | 4.2 | 0.5&nbsp;ms | 3.6 | 0.1 | 0.4 | 0.2 | 9.8 |
| Simulation, STEP | 0.3 | 1.0 | 4.0 | 0.5&nbsp;ms | 3.4 | 2.9 | 0.4 | 0.2 | 12.3 |
| Simulation, STL | 0.3 | 1.0 | 4.1 | 0.5&nbsp;ms | 3.6 | 0.3 | 0.5 | 0.2 | 10.0 |
| Simulation, OBJ | 0.3 | 1.0 | 3.9 | 0.3&nbsp;ms | 3.5 | 5.2 | 0.5 | 0.2 | 14.7 |
| Visual, GLB | 0.3 | 1.1 | 4.1 | 0.4&nbsp;ms | 8.0 | 87&nbsp;ms | 0.6 | 0.2 | 14.4 |
| Visual, OBJ | 0.5 | 1.0 | 3.8 | 0.4&nbsp;ms | 7.7 | 3.0 | 0.7 | 0.3 | 17.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/icicle-hdmi-breakout](https://github.com/antmicro/icicle-hdmi-breakout)<br>Board: `icicle-hdmi-breakout.kicad_pcb` |
|---|---|
| Complexity | 254&nbsp;/&nbsp;1000 (size&nbsp;189, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 34, 1,178, 41 |
| Triangles,&nbsp;simulation | 851,176 in 64 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">29&nbsp;MB</td><td align="right">401&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">166&nbsp;MB</td><td align="right">464&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">43&nbsp;MB</td><td align="right">404&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">88&nbsp;MB</td><td align="right">637&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">457&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">50&nbsp;MB</td><td align="right">468&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.60 ict-baseboard

![ict-baseboard: stages 4 and 6 take 51% to 77% of a run. Simulation, GLB takes 36 s. Simulation, STEP takes 44 s. Simulation, STL takes 36 s. Simulation, OBJ takes 55 s. Visual, GLB takes 47 s. Visual, OBJ takes 59 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/ict-baseboard_ict-baseboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.6 | 2.7 | 10.7 | 0.6&nbsp;ms | 16.0 | 0.4 | 1.2 | 0.3 | 36.0 |
| Simulation, STEP | 4.4 | 2.6 | 10.6 | 1.0&nbsp;ms | 16.2 | 8.7 | 1.2 | 0.3 | 44.2 |
| Simulation, STL | 4.4 | 2.8 | 10.5 | 0.9&nbsp;ms | 16.1 | 1.0 | 1.3 | 0.3 | 36.4 |
| Simulation, OBJ | 4.9 | 2.8 | 11.0 | 0.6&nbsp;ms | 17.1 | 17.2 | 1.4 | 0.3 | 54.7 |
| Visual, GLB | 4.5 | 2.8 | 11.1 | 1&nbsp;ms | 24.7 | 0.3 | 3.1 | 0.3 | 46.9 |
| Visual, OBJ | 4.6 | 2.8 | 10.7 | 0.9&nbsp;ms | 26.4 | 10.9 | 3.4 | 0.3 | 59.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/ict-baseboard](https://github.com/antmicro/ict-baseboard)<br>Board: `ict-baseboard.kicad_pcb` |
|---|---|
| Complexity | 413&nbsp;/&nbsp;1000 (size&nbsp;258, features&nbsp;155) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text, knockout text,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 206, 1,672, 214 |
| Triangles,&nbsp;simulation | 2,622,894 in 218 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">89&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">384&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">131&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">276&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">60&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">185&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.61 ir-irradiance-probe

![ir-irradiance-probe: stages 4 and 6 take 49% to 76% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 13 s. Simulation, STL takes 12 s. Simulation, OBJ takes 16 s. Visual, GLB takes 16 s. Visual, OBJ takes 19 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/infrared-irradiance-probe_ir-irradiance-probe.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.1 | 1.1 | 4.1 | 1&nbsp;ms | 3.5 | 0.2 | 0.5 | 0.4 | 11.9 |
| Simulation, STEP | 1.5 | 0.9 | 3.8 | 0.4&nbsp;ms | 3.5 | 2.9 | 0.5 | 0.3 | 13.4 |
| Simulation, STL | 1.8 | 1.0 | 4.7 | 0.4&nbsp;ms | 3.7 | 0.2 | 0.5 | 0.3 | 12.1 |
| Simulation, OBJ | 1.3 | 0.9 | 4.1 | 0.4&nbsp;ms | 3.7 | 5.0 | 0.5 | 0.3 | 15.8 |
| Visual, GLB | 1.6 | 1.0 | 4.3 | 0.3&nbsp;ms | 7.9 | 0.1 | 0.8 | 0.3 | 16.0 |
| Visual, OBJ | 1.3 | 0.9 | 3.6 | 0.4&nbsp;ms | 8.0 | 3.9 | 0.8 | 0.3 | 18.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/infrared-irradiance-probe](https://github.com/antmicro/infrared-irradiance-probe)<br>Board: `ir-irradiance-probe.kicad_pcb` |
|---|---|
| Complexity | 282&nbsp;/&nbsp;1000 (size&nbsp;172, features&nbsp;110) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 52, 330, 196 |
| Triangles,&nbsp;simulation | 735,330 in 43 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">490&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">124&nbsp;MB</td><td align="right">484&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">37&nbsp;MB</td><td align="right">482&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">77&nbsp;MB</td><td align="right">563&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">532&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">61&nbsp;MB</td><td align="right">578&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.62 jetson-agx-csi-adapter

![jetson-agx-csi-adapter: stages 4 and 6 take 52% to 82% of a run. Simulation, GLB takes 29 s. Simulation, STEP takes 40 s. Simulation, STL takes 30 s. Simulation, OBJ takes 47 s. Visual, GLB takes 49 s. Visual, OBJ takes 59 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/jetson-agx-csi-adapter_jetson-agx-csi-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.5 | 2.2 | 7.7 | 0.7&nbsp;ms | 14.4 | 0.4 | 1.4 | 0.4 | 29.0 |
| Simulation, STEP | 2.6 | 2.2 | 7.5 | 0.8&nbsp;ms | 14.8 | 11.0 | 1.3 | 0.3 | 39.7 |
| Simulation, STL | 3.1 | 2.1 | 8.0 | 0.7&nbsp;ms | 14.5 | 1.0 | 1.3 | 0.4 | 30.4 |
| Simulation, OBJ | 2.8 | 2.4 | 8.6 | 0.9&nbsp;ms | 15.5 | 15.5 | 1.3 | 0.4 | 46.6 |
| Visual, GLB | 2.5 | 2.0 | 9.6 | 0.9&nbsp;ms | 30.8 | 0.4 | 3.4 | 0.3 | 49.0 |
| Visual, OBJ | 2.6 | 2.3 | 8.3 | 1&nbsp;ms | 27.3 | 13.6 | 4.2 | 0.4 | 58.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/jetson-agx-csi-adapter](https://github.com/antmicro/jetson-agx-csi-adapter)<br>Board: `jetson-agx-csi-adapter.kicad_pcb` |
|---|---|
| Complexity | 345&nbsp;/&nbsp;1000 (size&nbsp;215, features&nbsp;130) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 80, 2,929, 225 |
| Triangles,&nbsp;simulation | 2,205,664 in 193 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">74&nbsp;MB</td><td align="right">935&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">344&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">110&nbsp;MB</td><td align="right">935&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">230&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">63&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">196&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.63 jetson-agx-thor-baseboard

![jetson-agx-thor-baseboard: stages 4 and 6 take 57% to 81% of a run. Simulation, GLB takes 4 min. Simulation, STEP takes 5 min. Simulation, STL takes 5 min. Visual, GLB takes 9 min. Visual, OBJ takes 8 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/jetson-agx-thor-baseboard_jetson-agx-thor-baseboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 26.6 | 32.6 | 75.6 | 3&nbsp;ms | 106.5 | 5.8 | 16.9 | 1.1 | 265.1 |
| Simulation, STEP | 26.9 | 33.0 | 79.2 | 3&nbsp;ms | 106.7 | 60.6 | 17.0 | 1.1 | 324.4 |
| Simulation, STL | 27.1 | 33.4 | 78.6 | 3&nbsp;ms | 116.7 | 13.6 | 19.5 | 1.0 | 289.9 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB | 29.1 | 37.1 | 83.3 | 3&nbsp;ms | 333.1 | 2.5 | 26.7 | 0.8 | 512.8 |
| Visual, OBJ | 23.1 | 31.4 | 69.2 | 3&nbsp;ms | 284.4 | 67.0 | 21.0 | 0.7 | 496.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/jetson-agx-thor-baseboard](https://github.com/antmicro/jetson-agx-thor-baseboard)<br>Board: `jetson-agx-thor-baseboard.kicad_pcb` |
|---|---|
| Complexity | 526&nbsp;/&nbsp;1000 (size&nbsp;351, features&nbsp;175) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, knockout text,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 10 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 1,025, 22,645, 3,223 |
| Triangles,&nbsp;simulation | 32,687,176 in 1419 parts |
| Verifier | Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Run&nbsp;again | Visual, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.1&nbsp;GB</td><td align="right">7.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">3.3&nbsp;GB</td><td align="right">9.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.6&nbsp;GB</td><td align="right">7.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">485&nbsp;MB</td><td align="right">8.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.6&nbsp;GB</td><td align="right">11&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.64 jetson-nano-baseboard

![jetson-nano-baseboard: stages 4 and 6 take 43% to 78% of a run. Simulation, GLB takes 57 s. Simulation, STEP takes 69 s. Simulation, STL takes 59 s. Simulation, OBJ takes 96 s. Visual, GLB takes 89 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/jetson-nano-baseboard_jetson-nano-baseboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 6.9 | 6.5 | 15.4 | 1&nbsp;ms | 23.4 | 1.1 | 3.0 | 0.4 | 56.8 |
| Simulation, STEP | 7.1 | 6.2 | 15.8 | 1&nbsp;ms | 23.1 | 13.0 | 3.2 | 0.4 | 68.8 |
| Simulation, STL | 6.9 | 5.8 | 15.9 | 1&nbsp;ms | 24.8 | 2.2 | 3.1 | 0.4 | 59.3 |
| Simulation, OBJ | 7.5 | 7.2 | 16.7 | 1&nbsp;ms | 24.0 | 36.6 | 3.2 | 0.5 | 95.6 |
| Visual, GLB | 7.2 | 6.5 | 16.2 | 1&nbsp;ms | 53.8 | 0.5 | 4.9 | 0.3 | 89.4 |
| Visual, OBJ | 7.2 | 6.1 | 16.3 | 2&nbsp;ms | 52.3 | 17.1 | 5.0 | 0.3 | 104.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/jetson-nano-baseboard](https://github.com/antmicro/jetson-nano-baseboard)<br>Board: `jetson-nano-baseboard.kicad_pcb` |
|---|---|
| Complexity | 448&nbsp;/&nbsp;1000 (size&nbsp;313, features&nbsp;135) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 326, 15,624, 794 |
| Triangles,&nbsp;simulation | 7,900,080 in 506 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">263&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">948&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">395&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">871&nbsp;MB</td><td align="right">5.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">130&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">440&nbsp;MB</td><td align="right">3.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.65 jetson-orin-baseboard

![jetson-orin-baseboard: stages 4 and 6 take 41% to 80% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 3 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/jetson-orin-baseboard_jetson-orin-baseboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 11.9 | 13.2 | 30.7 | 2&nbsp;ms | 53.6 | 2.4 | 7.0 | 0.6 | 119.4 |
| Simulation, STEP | 12.0 | 13.6 | 31.4 | 3&nbsp;ms | 54.3 | 28.5 | 7.8 | 0.6 | 148.2 |
| Simulation, STL | 11.9 | 13.6 | 31.1 | 3&nbsp;ms | 54.9 | 5.1 | 7.3 | 0.6 | 124.4 |
| Simulation, OBJ | 11.6 | 13.6 | 30.9 | 2&nbsp;ms | 53.8 | 86.9 | 7.4 | 0.7 | 205.0 |
| Visual, GLB | 12.4 | 13.5 | 33.0 | 3&nbsp;ms | 122.5 | 1.1 | 11.1 | 0.5 | 194.1 |
| Visual, OBJ | 11.8 | 13.2 | 31.7 | 2&nbsp;ms | 122.7 | 45.0 | 12.6 | 0.5 | 237.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/jetson-orin-baseboard](https://github.com/antmicro/jetson-orin-baseboard)<br>Board: `jetson-orin-baseboard.kicad_pcb` |
|---|---|
| Complexity | 522&nbsp;/&nbsp;1000 (size&nbsp;327, features&nbsp;195) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 618, 14,181, 1,345 |
| Triangles,&nbsp;simulation | 13,533,484 in 817 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">455&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.7&nbsp;GB</td><td align="right">4.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">677&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.5&nbsp;GB</td><td align="right">8.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">249&nbsp;MB</td><td align="right">4.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">822&nbsp;MB</td><td align="right">5.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.66 job-ict-bottom-board

![job-ict-bottom-board: stages 4 and 6 take 51% to 77% of a run. Simulation, GLB takes 20 s. Simulation, STEP takes 28 s. Simulation, STL takes 22 s. Simulation, OBJ takes 31 s. Visual, GLB takes 27 s. Visual, OBJ takes 35 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/job-ict-bottom-board_job-ict-bottom-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.5 | 1.8 | 7.8 | 0.6&nbsp;ms | 6.8 | 0.3 | 0.9 | 0.3 | 20.3 |
| Simulation, STEP | 2.8 | 2.0 | 9.0 | 0.7&nbsp;ms | 7.2 | 5.7 | 0.9 | 0.3 | 27.8 |
| Simulation, STL | 2.8 | 2.1 | 8.2 | 0.7&nbsp;ms | 7.0 | 0.5 | 0.9 | 0.3 | 21.9 |
| Simulation, OBJ | 2.6 | 2.0 | 8.5 | 3&nbsp;ms | 7.1 | 9.1 | 1.0 | 0.3 | 30.6 |
| Visual, GLB | 2.5 | 2.0 | 8.0 | 0.8&nbsp;ms | 12.6 | 0.2 | 1.4 | 0.2 | 26.9 |
| Visual, OBJ | 2.6 | 1.8 | 8.0 | 0.7&nbsp;ms | 13.6 | 7.1 | 1.6 | 0.3 | 34.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/job-ict-bottom-board](https://github.com/antmicro/job-ict-bottom-board)<br>Board: `job-ict-bottom-board.kicad_pcb` |
|---|---|
| Complexity | 323&nbsp;/&nbsp;1000 (size&nbsp;173, features&nbsp;150) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 93, 492, 64 |
| Triangles,&nbsp;simulation | 1,493,234 in 119 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">51&nbsp;MB</td><td align="right">653&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">219&nbsp;MB</td><td align="right">798&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">75&nbsp;MB</td><td align="right">670&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">155&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">37&nbsp;MB</td><td align="right">744&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">111&nbsp;MB</td><td align="right">851&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.67 job-ict-support-board

![job-ict-support-board: stages 4 and 6 take 50% to 77% of a run. Simulation, GLB takes 4.1 s. Simulation, STEP takes 5.5 s. Simulation, STL takes 3.8 s. Simulation, OBJ takes 5.8 s. Visual, GLB takes 5.8 s. Visual, OBJ takes 7.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/job-ict-support-board_job-ict-support-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.5 | 0.4&nbsp;ms | 1.5 | 67&nbsp;ms | 0.2 | 0.2 | 4.1 |
| Simulation, STEP | 0.2 | 0.5 | 1.4 | 0.2&nbsp;ms | 1.5 | 1.5 | 0.2 | 0.3 | 5.5 |
| Simulation, STL | 0.3 | 0.4 | 1.3 | 0.2&nbsp;ms | 1.3 | 0.1 | 0.2 | 0.2 | 3.8 |
| Simulation, OBJ | 0.2 | 0.4 | 1.4 | 0.5&nbsp;ms | 1.5 | 1.9 | 0.2 | 0.2 | 5.8 |
| Visual, GLB | 0.2 | 0.4 | 1.4 | 0.8&nbsp;ms | 3.1 | 46&nbsp;ms | 0.4 | 0.2 | 5.8 |
| Visual, OBJ | 0.3 | 0.5 | 1.5 | 0.3&nbsp;ms | 3.0 | 1.2 | 0.4 | 0.2 | 7.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/job-ict-support-board](https://github.com/antmicro/job-ict-support-board)<br>Board: `job-ict-support-board.kicad_pcb` |
|---|---|
| Complexity | 112&nbsp;/&nbsp;1000 (size&nbsp;17, features&nbsp;95) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones, knockout text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 0, 0, 0 |
| Triangles,&nbsp;simulation | 434,326 in 38 parts |
| Note | no components |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">331&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">66&nbsp;MB</td><td align="right">337&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">22&nbsp;MB</td><td align="right">315&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">44&nbsp;MB</td><td align="right">354&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">10&nbsp;MB</td><td align="right">317&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">30&nbsp;MB</td><td align="right">312&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.68 jetson-orin-baseboard-oculink-expansion

![Stages 4 and 6 take 48% to 77% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 19 s. Simulation, STL takes 15 s. Simulation, OBJ takes 22 s. Visual, GLB takes 26 s. Visual, OBJ takes 31 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/job-oculink-expansion_jetson-orin-baseboard-oculink-expansion.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.0 | 1.2 | 4.5 | 0.7&nbsp;ms | 6.9 | 0.3 | 0.6 | 0.3 | 15.7 |
| Simulation, STEP | 2.3 | 1.2 | 4.1 | 0.5&nbsp;ms | 6.4 | 4.4 | 0.6 | 0.3 | 19.3 |
| Simulation, STL | 2.0 | 1.2 | 4.0 | 0.5&nbsp;ms | 6.1 | 0.5 | 0.6 | 0.3 | 14.7 |
| Simulation, OBJ | 1.9 | 1.1 | 4.3 | 0.5&nbsp;ms | 6.6 | 7.7 | 0.6 | 0.3 | 22.4 |
| Visual, GLB | 2.1 | 1.3 | 4.4 | 0.7&nbsp;ms | 15.5 | 0.2 | 1.9 | 0.3 | 25.6 |
| Visual, OBJ | 1.9 | 1.2 | 4.3 | 0.8&nbsp;ms | 15.6 | 5.8 | 2.0 | 0.3 | 31.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/job-oculink-expansion](https://github.com/antmicro/job-oculink-expansion)<br>Board: `jetson-orin-baseboard-oculink-expansion.kicad_pcb` |
|---|---|
| Complexity | 374&nbsp;/&nbsp;1000 (size&nbsp;254, features&nbsp;120) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, knockout text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 97, 1,265, 219 |
| Triangles,&nbsp;simulation | 1,861,222 in 153 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">64&nbsp;MB</td><td align="right">787&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">312&nbsp;MB</td><td align="right">930&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">93&nbsp;MB</td><td align="right">801&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">194&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">46&nbsp;MB</td><td align="right">984&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">142&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.69 jetson-orin-baseboard-pcie-switch-expansion

![Stages 4 and 6 take 41% to 76% of a run. Simulation, GLB takes 58 s. Simulation, STEP takes 71 s. Simulation, STL takes 58 s. Simulation, OBJ takes 94 s. Visual, GLB takes 91 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/job-pcie-switch-expansion_jetson-orin-baseboard-pcie-switch-expansion.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 8.9 | 6.4 | 15.3 | 1&nbsp;ms | 23.0 | 1.2 | 2.6 | 0.5 | 58.0 |
| Simulation, STEP | 8.3 | 6.3 | 15.9 | 1&nbsp;ms | 22.5 | 14.5 | 2.7 | 0.5 | 70.6 |
| Simulation, STL | 8.2 | 6.2 | 15.5 | 1&nbsp;ms | 22.4 | 2.5 | 2.6 | 0.5 | 57.8 |
| Simulation, OBJ | 8.3 | 6.2 | 15.7 | 1&nbsp;ms | 22.7 | 37.7 | 2.9 | 0.5 | 94.0 |
| Visual, GLB | 8.3 | 6.3 | 16.0 | 1&nbsp;ms | 53.4 | 0.6 | 6.4 | 0.4 | 91.4 |
| Visual, OBJ | 8.6 | 6.4 | 15.6 | 2&nbsp;ms | 54.1 | 22.8 | 6.6 | 0.4 | 114.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/job-pcie-switch-expansion](https://github.com/antmicro/job-pcie-switch-expansion)<br>Board: `jetson-orin-baseboard-pcie-switch-expansion.kicad_pcb` |
|---|---|
| Complexity | 489&nbsp;/&nbsp;1000 (size&nbsp;304, features&nbsp;185) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 297, 4,689, 779 |
| Triangles,&nbsp;simulation | 5,931,152 in 404 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">202&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">759&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">297&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">632&nbsp;MB</td><td align="right">3.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">122&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">396&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.70 jetson-orin-baseboard-storage-expansion

![Stages 4 and 6 take 46% to 77% of a run. Simulation, GLB takes 18 s. Simulation, STEP takes 22 s. Simulation, STL takes 17 s. Simulation, OBJ takes 26 s. Visual, GLB takes 28 s. Visual, OBJ takes 35 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/job-storage-expansion_jetson-orin-baseboard-storage-expansion.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.1 | 1.7 | 5.3 | 0.8&nbsp;ms | 7.1 | 0.3 | 0.8 | 0.3 | 17.6 |
| Simulation, STEP | 2.3 | 1.7 | 5.0 | 0.7&nbsp;ms | 6.9 | 4.8 | 0.7 | 0.3 | 21.8 |
| Simulation, STL | 2.3 | 1.6 | 5.1 | 0.9&nbsp;ms | 6.7 | 0.7 | 0.7 | 0.3 | 17.4 |
| Simulation, OBJ | 2.2 | 1.8 | 5.0 | 0.7&nbsp;ms | 6.8 | 8.9 | 0.7 | 0.3 | 25.8 |
| Visual, GLB | 2.4 | 1.7 | 5.2 | 0.7&nbsp;ms | 16.4 | 0.2 | 1.9 | 0.3 | 28.1 |
| Visual, OBJ | 2.3 | 1.6 | 5.1 | 0.8&nbsp;ms | 17.0 | 7.0 | 2.0 | 0.3 | 35.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/job-storage-expansion](https://github.com/antmicro/job-storage-expansion)<br>Board: `jetson-orin-baseboard-storage-expansion.kicad_pcb` |
|---|---|
| Complexity | 411&nbsp;/&nbsp;1000 (size&nbsp;251, features&nbsp;160) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 88, 1,551, 378 |
| Triangles,&nbsp;simulation | 1,932,092 in 167 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">64&nbsp;MB</td><td align="right">850&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">274&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">97&nbsp;MB</td><td align="right">810&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">200&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">48&nbsp;MB</td><td align="right">934&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">149&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.71 k410t-devboard

![k410t-devboard: stages 4 and 6 take 57% to 81% of a run. Simulation, GLB takes 4 min. Simulation, STEP takes 5 min. Simulation, STL takes 4 min. Visual, GLB takes 7 min. Visual, OBJ takes 8 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/kintex-410t-devboard_k410t-devboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 25.1 | 31.1 | 68.8 | 3&nbsp;ms | 92.3 | 6.0 | 16.1 | 1.2 | 240.7 |
| Simulation, STEP | 24.5 | 29.8 | 69.7 | 3&nbsp;ms | 92.5 | 49.7 | 16.0 | 1.1 | 283.2 |
| Simulation, STL | 23.7 | 29.2 | 68.6 | 3&nbsp;ms | 93.4 | 11.7 | 20.5 | 1.3 | 248.4 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB | 24.4 | 30.5 | 70.9 | 3&nbsp;ms | 256.2 | 2.1 | 18.5 | 0.7 | 403.3 |
| Visual, OBJ | 24.8 | 29.6 | 66.0 | 3&nbsp;ms | 265.3 | 62.1 | 19.9 | 0.8 | 468.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/kintex-410t-devboard](https://github.com/antmicro/kintex-410t-devboard)<br>Board: `k410t-devboard.kicad_pcb` |
|---|---|
| Complexity | 497&nbsp;/&nbsp;1000 (size&nbsp;367, features&nbsp;130) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 10 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 962, 19,907, 2,762 |
| Triangles,&nbsp;simulation | 29,401,472 in 1433 parts |
| Verifier | Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">978&nbsp;MB</td><td align="right">6.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.9&nbsp;GB</td><td align="right">8.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.5&nbsp;GB</td><td align="right">6.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">430&nbsp;MB</td><td align="right">7.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.5&nbsp;GB</td><td align="right">9.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.72 kria-k26-devboard

![kria-k26-devboard: stages 4 and 6 take 39% to 76% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 3 min. Simulation, STL takes 2 min. Simulation, OBJ takes 4 min. Visual, GLB takes 4 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/kria-k26-devboard_kria-k26-devboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 20.2 | 18.3 | 40.0 | 2&nbsp;ms | 55.9 | 3.6 | 7.6 | 0.7 | 146.4 |
| Simulation, STEP | 18.7 | 16.7 | 36.4 | 2&nbsp;ms | 54.0 | 31.5 | 7.5 | 0.7 | 165.6 |
| Simulation, STL | 18.7 | 17.3 | 38.3 | 2&nbsp;ms | 54.4 | 7.5 | 7.2 | 0.8 | 144.1 |
| Simulation, OBJ | 18.7 | 16.8 | 38.0 | 2&nbsp;ms | 54.6 | 101.3 | 7.9 | 0.8 | 238.1 |
| Visual, GLB | 19.1 | 17.9 | 42.9 | 2&nbsp;ms | 124.4 | 1.8 | 13.1 | 0.7 | 219.9 |
| Visual, OBJ | 18.7 | 18.1 | 39.4 | 2&nbsp;ms | 120.3 | 47.8 | 13.1 | 0.7 | 257.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/kria-k26-devboard](https://github.com/antmicro/kria-k26-devboard)<br>Board: `kria-k26-devboard.kicad_pcb` |
|---|---|
| Complexity | 491&nbsp;/&nbsp;1000 (size&nbsp;336, features&nbsp;155) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 577, 20,506, 1,901 |
| Triangles,&nbsp;simulation | 15,836,218 in 822 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">527&nbsp;MB</td><td align="right">4.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.6&nbsp;GB</td><td align="right">5.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">792&nbsp;MB</td><td align="right">4.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.7&nbsp;GB</td><td align="right">10&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">256&nbsp;MB</td><td align="right">4.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">853&nbsp;MB</td><td align="right">5.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.73 lpddr4-test-board

![lpddr4-test-board: stages 4 and 6 take 43% to 73% of a run. Simulation, GLB takes 83 s. Simulation, STEP takes 98 s. Simulation, STL takes 84 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/lpddr4-test-board_lpddr4-test-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 12.7 | 9.9 | 20.3 | 1&nbsp;ms | 34.8 | 1.5 | 3.1 | 0.6 | 82.9 |
| Simulation, STEP | 12.9 | 10.4 | 20.3 | 1&nbsp;ms | 33.7 | 17.2 | 3.1 | 0.5 | 98.2 |
| Simulation, STL | 12.9 | 10.2 | 20.1 | 1&nbsp;ms | 33.7 | 3.6 | 3.1 | 0.6 | 84.1 |
| Simulation, OBJ | 13.0 | 9.9 | 19.3 | 1&nbsp;ms | 33.7 | 43.7 | 2.9 | 0.8 | 123.3 |
| Visual, GLB | 13.2 | 10.1 | 20.3 | 1&nbsp;ms | 65.6 | 0.8 | 7.1 | 0.5 | 117.6 |
| Visual, OBJ | 12.8 | 10.4 | 19.6 | 1&nbsp;ms | 64.9 | 23.1 | 6.8 | 0.5 | 138.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/lpddr4-test-board](https://github.com/antmicro/lpddr4-test-board)<br>Board: `lpddr4-test-board.kicad_pcb` |
|---|---|
| Complexity | 514&nbsp;/&nbsp;1000 (size&nbsp;324, features&nbsp;190) |
| KESE&nbsp;features | through vias,<br>blind and buried vias,<br>slotted holes, custom pads,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 445, 5,712, 1,214 |
| Triangles,&nbsp;simulation | 9,482,776 in 688 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">314&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.0&nbsp;GB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">474&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.0&nbsp;GB</td><td align="right">6.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">171&nbsp;MB</td><td align="right">3.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">569&nbsp;MB</td><td align="right">3.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.74 lpddr4-testbed

![lpddr4-testbed: stages 4 and 6 take 48% to 81% of a run. Simulation, GLB takes 20 s. Simulation, STEP takes 25 s. Simulation, STL takes 20 s. Simulation, OBJ takes 31 s. Visual, GLB takes 28 s. Visual, OBJ takes 34 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/lpddr4-testbed_lpddr4-testbed.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.9 | 1.8 | 7.4 | 0.9&nbsp;ms | 7.4 | 0.3 | 0.9 | 0.3 | 20.0 |
| Simulation, STEP | 1.9 | 1.9 | 7.5 | 0.8&nbsp;ms | 7.5 | 4.9 | 0.9 | 0.3 | 24.7 |
| Simulation, STL | 1.9 | 1.8 | 7.1 | 0.8&nbsp;ms | 7.4 | 0.6 | 0.8 | 0.3 | 20.0 |
| Simulation, OBJ | 1.8 | 1.8 | 7.3 | 0.8&nbsp;ms | 7.3 | 11.3 | 0.9 | 0.3 | 30.6 |
| Visual, GLB | 1.8 | 1.8 | 7.3 | 0.9&nbsp;ms | 15.5 | 0.2 | 1.4 | 0.3 | 28.2 |
| Visual, OBJ | 1.8 | 1.9 | 7.3 | 0.9&nbsp;ms | 15.0 | 6.5 | 1.4 | 0.2 | 34.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/lpddr4-testbed](https://github.com/antmicro/lpddr4-testbed)<br>Board: `lpddr4-testbed.kicad_pcb` |
|---|---|
| Complexity | 377&nbsp;/&nbsp;1000 (size&nbsp;267, features&nbsp;110) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 63, 1,498, 248 |
| Triangles,&nbsp;simulation | 2,042,424 in 275 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">69&nbsp;MB</td><td align="right">747&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">283&nbsp;MB</td><td align="right">897&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">102&nbsp;MB</td><td align="right">840&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">216&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">844&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">121&nbsp;MB</td><td align="right">932&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.75 lpddr5-testbed

![lpddr5-testbed: stages 4 and 6 take 51% to 82% of a run. Simulation, GLB takes 53 s. Simulation, STEP takes 66 s. Simulation, STL takes 56 s. Simulation, OBJ takes 82 s. Visual, GLB takes 85 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/lpddr5-testbed_lpddr5-testbed.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.5 | 5.1 | 19.1 | 0.8&nbsp;ms | 21.5 | 0.9 | 2.8 | 0.4 | 53.2 |
| Simulation, STEP | 3.4 | 5.2 | 20.4 | 0.8&nbsp;ms | 21.8 | 12.4 | 2.8 | 0.4 | 66.4 |
| Simulation, STL | 3.6 | 5.2 | 19.7 | 0.8&nbsp;ms | 22.2 | 2.0 | 2.9 | 0.4 | 56.0 |
| Simulation, OBJ | 3.4 | 5.0 | 19.6 | 0.8&nbsp;ms | 22.5 | 28.8 | 2.8 | 0.4 | 82.5 |
| Visual, GLB | 3.5 | 5.1 | 19.5 | 0.8&nbsp;ms | 49.8 | 0.5 | 6.3 | 0.4 | 85.0 |
| Visual, OBJ | 3.5 | 5.0 | 19.9 | 0.9&nbsp;ms | 48.8 | 16.3 | 6.2 | 0.3 | 100.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/lpddr5-testbed](https://github.com/antmicro/lpddr5-testbed)<br>Board: `lpddr5-testbed.kicad_pcb` |
|---|---|
| Complexity | 417&nbsp;/&nbsp;1000 (size&nbsp;302, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 152, 5,078, 590 |
| Triangles,&nbsp;simulation | 5,169,826 in 244 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">176&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">766&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">259&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">555&nbsp;MB</td><td align="right">3.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">100&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">323&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.76 antmicro-m2-oculink-adapter-hw

![Stages 4 and 6 take 50% to 81% of a run. Simulation, GLB takes 8.5 s. Simulation, STEP takes 11 s. Simulation, STL takes 8.7 s. Simulation, OBJ takes 13 s. Visual, GLB takes 13 s. Visual, OBJ takes 17 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/m2-oculink-adapter_antmicro-m2-oculink-adapter-hw.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 0.7 | 2.6 | 0.3&nbsp;ms | 3.8 | 0.1 | 0.4 | 0.3 | 8.5 |
| Simulation, STEP | 0.5 | 0.7 | 2.5 | 0.6&nbsp;ms | 4.1 | 2.9 | 0.4 | 0.2 | 11.3 |
| Simulation, STL | 0.5 | 0.7 | 2.4 | 0.3&nbsp;ms | 3.9 | 0.4 | 0.4 | 0.2 | 8.7 |
| Simulation, OBJ | 0.5 | 0.8 | 2.7 | 0.4&nbsp;ms | 3.8 | 4.5 | 0.4 | 0.3 | 13.0 |
| Visual, GLB | 0.5 | 0.7 | 2.6 | 0.4&nbsp;ms | 8.2 | 0.1 | 0.9 | 0.2 | 13.3 |
| Visual, OBJ | 0.5 | 0.7 | 2.6 | 0.3&nbsp;ms | 8.2 | 3.4 | 1.2 | 0.3 | 16.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/m2-oculink-adapter](https://github.com/antmicro/m2-oculink-adapter)<br>Board: `antmicro-m2-oculink-adapter-hw.kicad_pcb` |
|---|---|
| Complexity | 296&nbsp;/&nbsp;1000 (size&nbsp;181, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 19, 577, 183 |
| Triangles,&nbsp;simulation | 873,538 in 72 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">440&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">132&nbsp;MB</td><td align="right">533&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">44&nbsp;MB</td><td align="right">429&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">89&nbsp;MB</td><td align="right">638&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">22&nbsp;MB</td><td align="right">590&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">67&nbsp;MB</td><td align="right">584&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.77 m2-pcie-adapter

![m2-pcie-adapter: stages 4 and 6 take 48% to 82% of a run. Simulation, GLB takes 7.2 s. Simulation, STEP takes 9.6 s. Simulation, STL takes 7.1 s. Simulation, OBJ takes 11 s. Visual, GLB takes 12 s. Visual, OBJ takes 15 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/m2-pcie-adapter_m2-pcie-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 0.5 | 2.2 | 0.4&nbsp;ms | 3.0 | 0.1 | 0.4 | 0.2 | 7.2 |
| Simulation, STEP | 0.6 | 0.5 | 2.1 | 0.3&nbsp;ms | 3.1 | 2.6 | 0.4 | 0.2 | 9.6 |
| Simulation, STL | 0.6 | 0.5 | 2.2 | 0.4&nbsp;ms | 3.0 | 0.2 | 0.4 | 0.2 | 7.1 |
| Simulation, OBJ | 0.6 | 0.6 | 2.2 | 0.4&nbsp;ms | 3.2 | 4.1 | 0.4 | 0.2 | 11.2 |
| Visual, GLB | 0.6 | 0.5 | 2.3 | 0.5&nbsp;ms | 7.3 | 91&nbsp;ms | 0.6 | 0.2 | 11.7 |
| Visual, OBJ | 0.6 | 0.5 | 2.2 | 0.3&nbsp;ms | 7.7 | 3.1 | 0.5 | 0.2 | 15.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/m2-pcie-adapter](https://github.com/antmicro/m2-pcie-adapter)<br>Board: `m2-pcie-adapter.kicad_pcb` |
|---|---|
| Complexity | 288&nbsp;/&nbsp;1000 (size&nbsp;178, features&nbsp;110) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 16, 787, 92 |
| Triangles,&nbsp;simulation | 808,562 in 81 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">497&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">142&nbsp;MB</td><td align="right">498&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">40&nbsp;MB</td><td align="right">453&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">83&nbsp;MB</td><td align="right">586&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">21&nbsp;MB</td><td align="right">538&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">63&nbsp;MB</td><td align="right">600&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.78 m2-smart-iot-module

![m2-smart-iot-module: stages 4 and 6 take 47% to 83% of a run. Simulation, GLB takes 27 s. Simulation, STEP takes 37 s. Simulation, STL takes 29 s. Simulation, OBJ takes 48 s. Visual, GLB takes 47 s. Visual, OBJ takes 60 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/m2-smart-iot-module_m2-smart-iot-module.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 3.0 | 9.3 | 0.9&nbsp;ms | 11.7 | 0.5 | 1.4 | 0.3 | 27.1 |
| Simulation, STEP | 1.2 | 2.9 | 9.4 | 1&nbsp;ms | 12.1 | 9.5 | 1.4 | 0.3 | 36.9 |
| Simulation, STL | 1.3 | 3.2 | 9.9 | 1&nbsp;ms | 12.0 | 0.9 | 1.4 | 0.3 | 29.1 |
| Simulation, OBJ | 1.1 | 3.0 | 10.1 | 1&nbsp;ms | 12.6 | 19.5 | 1.5 | 0.4 | 48.2 |
| Visual, GLB | 1.2 | 2.9 | 9.7 | 0.9&nbsp;ms | 29.4 | 0.3 | 3.3 | 0.3 | 47.2 |
| Visual, OBJ | 0.9 | 2.8 | 10.0 | 1.0&nbsp;ms | 30.3 | 12.3 | 3.4 | 0.2 | 59.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/m2-smart-iot-module](https://github.com/antmicro/m2-smart-iot-module)<br>Board: `m2-smart-iot-module.kicad_pcb` |
|---|---|
| Complexity | 393&nbsp;/&nbsp;1000 (size&nbsp;268, features&nbsp;125) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 195, 1,615, 435 |
| Triangles,&nbsp;simulation | 2,528,042 in 263 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">87&nbsp;MB</td><td align="right">817&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">423&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">126&nbsp;MB</td><td align="right">876&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">271&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">61&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">190&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.79 machxo5-espi-debugger

![machxo5-espi-debugger: stages 4 and 6 take 44% to 77% of a run. Simulation, GLB takes 41 s. Simulation, STEP takes 50 s. Simulation, STL takes 44 s. Simulation, OBJ takes 65 s. Visual, GLB takes 65 s. Visual, OBJ takes 76 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/machx05-espi-debugger_machxo5-espi-debugger.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 6.3 | 4.0 | 12.4 | 1&nbsp;ms | 15.9 | 0.6 | 1.7 | 0.4 | 41.3 |
| Simulation, STEP | 6.3 | 4.0 | 12.7 | 1&nbsp;ms | 15.2 | 10.2 | 1.6 | 0.4 | 50.4 |
| Simulation, STL | 6.4 | 4.2 | 12.8 | 1&nbsp;ms | 17.5 | 1.3 | 1.9 | 0.4 | 44.5 |
| Simulation, OBJ | 7.0 | 5.0 | 13.5 | 2&nbsp;ms | 15.2 | 22.4 | 1.8 | 0.4 | 65.3 |
| Visual, GLB | 6.6 | 4.1 | 13.5 | 1&nbsp;ms | 36.2 | 0.4 | 3.3 | 0.4 | 64.5 |
| Visual, OBJ | 6.4 | 4.1 | 12.2 | 2&nbsp;ms | 34.6 | 14.4 | 3.4 | 0.3 | 75.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/machx05-espi-debugger](https://github.com/antmicro/machx05-espi-debugger)<br>Board: `machxo5-espi-debugger.kicad_pcb` |
|---|---|
| Complexity | 461&nbsp;/&nbsp;1000 (size&nbsp;291, features&nbsp;170) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 227, 2,121, 491 |
| Triangles,&nbsp;simulation | 3,681,402 in 482 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">122&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">478&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">184&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">382&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">81&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">259&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.80 mec1723-espi-debugger

![mec1723-espi-debugger: stages 4 and 6 take 40% to 76% of a run. Simulation, GLB takes 47 s. Simulation, STEP takes 60 s. Simulation, STL takes 47 s. Simulation, OBJ takes 78 s. Visual, GLB takes 70 s. Visual, OBJ takes 89 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/mec1723-espi-debugger_mec1723-espi-debugger.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.8 | 6.1 | 12.2 | 2&nbsp;ms | 19.0 | 1.0 | 3.1 | 0.4 | 46.6 |
| Simulation, STEP | 5.2 | 6.4 | 12.9 | 2&nbsp;ms | 19.5 | 12.8 | 2.8 | 0.5 | 60.1 |
| Simulation, STL | 4.7 | 6.1 | 12.2 | 1&nbsp;ms | 18.5 | 2.3 | 2.6 | 0.4 | 46.8 |
| Simulation, OBJ | 4.9 | 5.9 | 12.0 | 2&nbsp;ms | 19.3 | 33.2 | 2.6 | 0.4 | 78.3 |
| Visual, GLB | 4.9 | 5.9 | 12.8 | 1&nbsp;ms | 40.5 | 0.6 | 5.3 | 0.4 | 70.5 |
| Visual, OBJ | 5.0 | 6.5 | 12.9 | 2&nbsp;ms | 40.7 | 17.8 | 6.1 | 0.4 | 89.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/mec1723-espi-debugger](https://github.com/antmicro/mec1723-espi-debugger)<br>Board: `mec1723-espi-debugger.kicad_pcb` |
|---|---|
| Complexity | 471&nbsp;/&nbsp;1000 (size&nbsp;301, features&nbsp;170) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 212, 3,327, 470 |
| Triangles,&nbsp;simulation | 4,657,560 in 302 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">158&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">528&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">233&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">497&nbsp;MB</td><td align="right">3.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">86&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">283&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.81 microphone-board

![microphone-board: stages 4 and 6 take 38% to 66% of a run. Simulation, GLB takes 1.5 s. Simulation, STEP takes 2.3 s. Simulation, STL takes 1.6 s. Simulation, OBJ takes 2.1 s. Visual, GLB takes 2.1 s. Visual, OBJ takes 2.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/microphone-board_microphone-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.1 | 0.3 | 0.1&nbsp;ms | 0.5 | 21&nbsp;ms | 60&nbsp;ms | 0.2 | 1.5 |
| Simulation, STEP | 0.2 | 0.1 | 0.3 | 0.1&nbsp;ms | 0.5 | 0.7 | 63&nbsp;ms | 0.2 | 2.3 |
| Simulation, STL | 0.3 | 0.1 | 0.3 | 0.1&nbsp;ms | 0.5 | 35&nbsp;ms | 63&nbsp;ms | 0.2 | 1.6 |
| Simulation, OBJ | 0.2 | 0.1 | 0.4 | 0.1&nbsp;ms | 0.6 | 0.6 | 70&nbsp;ms | 0.2 | 2.1 |
| Visual, GLB | 0.2 | 0.1 | 0.3 | 0.1&nbsp;ms | 1.1 | 15&nbsp;ms | 0.1 | 0.2 | 2.1 |
| Visual, OBJ | 0.2 | 0.1 | 0.3 | 0.1&nbsp;ms | 1.1 | 0.4 | 92&nbsp;ms | 0.2 | 2.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/microphone-board](https://github.com/antmicro/microphone-board)<br>Board: `microphone-board.kicad_pcb` |
|---|---|
| Complexity | 273&nbsp;/&nbsp;1000 (size&nbsp;143, features&nbsp;130) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 12, 60, 28 |
| Triangles,&nbsp;simulation | 147,964 in 16 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">5.1&nbsp;MB</td><td align="right">204&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">22&nbsp;MB</td><td align="right">212&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">7.4&nbsp;MB</td><td align="right">211&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">14&nbsp;MB</td><td align="right">201&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.4&nbsp;MB</td><td align="right">163&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.4&nbsp;MB</td><td align="right">163&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.82 altera-modular-agilex-5-dc-scm

![Stages 4 and 6 take 45% to 78% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 3 min. Simulation, STL takes 3 min. Simulation, OBJ takes 4 min. Visual, GLB takes 4 min. Visual, OBJ takes 5 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/modular-agilex5e-dc-scm_altera-modular-agilex-5-dc-scm.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 19.3 | 17.9 | 42.0 | 3&nbsp;ms | 79.3 | 3.6 | 10.6 | 0.9 | 173.6 |
| Simulation, STEP | 17.8 | 17.9 | 40.6 | 4&nbsp;ms | 77.0 | 37.8 | 10.8 | 0.8 | 202.6 |
| Simulation, STL | 18.6 | 17.8 | 40.1 | 2&nbsp;ms | 78.4 | 8.6 | 11.5 | 0.8 | 175.9 |
| Simulation, OBJ | 18.1 | 17.3 | 39.3 | 4&nbsp;ms | 75.9 | 94.2 | 11.1 | 0.8 | 256.7 |
| Visual, GLB | 17.3 | 16.6 | 38.2 | 3&nbsp;ms | 148.3 | 2.0 | 14.4 | 0.9 | 237.6 |
| Visual, OBJ | 17.9 | 18.0 | 39.9 | 3&nbsp;ms | 145.7 | 46.0 | 16.1 | 0.8 | 284.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/modular-agilex5e-dc-scm](https://github.com/antmicro/modular-agilex5e-dc-scm)<br>Board: `altera-modular-agilex-5-dc-scm.kicad_pcb` |
|---|---|
| Complexity | 520&nbsp;/&nbsp;1000 (size&nbsp;340, features&nbsp;180) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 782, 15,441, 1,606 |
| Triangles,&nbsp;simulation | 15,504,394 in 963 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">520&nbsp;MB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.8&nbsp;GB</td><td align="right">5.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">775&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.7&nbsp;GB</td><td align="right">10&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">282&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">934&nbsp;MB</td><td align="right">6.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.83 myra-sip-interposer

![myra-sip-interposer: stages 4 and 6 take 49% to 80% of a run. Simulation, GLB takes 9.5 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.8 s. Simulation, OBJ takes 15 s. Visual, GLB takes 13 s. Visual, OBJ takes 15 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/myra-sip-interposer_myra-sip-interposer.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 0.9 | 3.9 | 0.4&nbsp;ms | 3.0 | 0.1 | 0.5 | 0.2 | 9.5 |
| Simulation, STEP | 0.7 | 0.9 | 4.0 | 0.3&nbsp;ms | 3.0 | 2.3 | 0.5 | 0.2 | 11.6 |
| Simulation, STL | 0.8 | 0.9 | 4.0 | 0.4&nbsp;ms | 3.0 | 0.3 | 0.6 | 0.2 | 9.8 |
| Simulation, OBJ | 0.9 | 0.9 | 4.1 | 0.4&nbsp;ms | 3.1 | 4.9 | 0.5 | 0.3 | 14.7 |
| Visual, GLB | 0.8 | 0.9 | 3.8 | 0.4&nbsp;ms | 6.4 | 75&nbsp;ms | 0.5 | 0.3 | 12.8 |
| Visual, OBJ | 0.8 | 1.0 | 4.0 | 0.6&nbsp;ms | 6.1 | 2.5 | 0.7 | 0.3 | 15.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/myra-sip-interposer](https://github.com/antmicro/myra-sip-interposer)<br>Board: `myra-sip-interposer.kicad_pcb` |
|---|---|
| Complexity | 405&nbsp;/&nbsp;1000 (size&nbsp;240, features&nbsp;165) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ,<br>copper finish, castellated pads,<br>plated board edge |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 31, 354, 164 |
| Triangles,&nbsp;simulation | 866,652 in 96 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">29&nbsp;MB</td><td align="right">377&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">103&nbsp;MB</td><td align="right">446&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">43&nbsp;MB</td><td align="right">396&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">86&nbsp;MB</td><td align="right">607&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">483&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">46&nbsp;MB</td><td align="right">449&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.84 oculink-to-10gbe-adapter

![oculink-to-10gbe-adapter: stages 4 and 6 take 43% to 82% of a run. Simulation, GLB takes 79 s. Simulation, STEP takes 94 s. Simulation, STL takes 84 s. Simulation, OBJ takes 2 min. Visual, GLB takes 3 min. Visual, OBJ takes 3 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/oculink-10gbe-adapter_oculink-to-10gbe-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 12.0 | 6.8 | 23.7 | 2&nbsp;ms | 31.0 | 1.4 | 3.3 | 0.5 | 78.7 |
| Simulation, STEP | 12.3 | 7.2 | 23.6 | 2&nbsp;ms | 30.1 | 16.7 | 3.5 | 0.5 | 93.9 |
| Simulation, STL | 12.2 | 7.3 | 24.7 | 2&nbsp;ms | 31.7 | 3.6 | 3.5 | 0.5 | 83.5 |
| Simulation, OBJ | 12.7 | 7.5 | 26.7 | 3&nbsp;ms | 32.8 | 55.9 | 3.6 | 0.6 | 139.8 |
| Visual, GLB | 12.5 | 7.2 | 24.1 | 2&nbsp;ms | 101.6 | 0.7 | 7.4 | 0.4 | 153.9 |
| Visual, OBJ | 11.7 | 7.1 | 23.8 | 2&nbsp;ms | 99.8 | 28.1 | 7.6 | 0.4 | 178.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/oculink-10gbe-adapter](https://github.com/antmicro/oculink-10gbe-adapter)<br>Board: `oculink-to-10gbe-adapter.kicad_pcb` |
|---|---|
| Complexity | 466&nbsp;/&nbsp;1000 (size&nbsp;311, features&nbsp;155) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 460, 2,463, 1,174 |
| Triangles,&nbsp;simulation | 9,149,554 in 437 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">295&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">962&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">458&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">950&nbsp;MB</td><td align="right">5.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">167&nbsp;MB</td><td align="right">3.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">537&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.85 oculink-to-pcie-adapter

![oculink-to-pcie-adapter: stages 4 and 6 take 44% to 73% of a run. Simulation, GLB takes 28 s. Simulation, STEP takes 33 s. Simulation, STL takes 28 s. Simulation, OBJ takes 41 s. Visual, GLB takes 36 s. Visual, OBJ takes 47 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/oculink-pcie-adapter_oculink-to-pcie-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.0 | 3.1 | 8.7 | 1&nbsp;ms | 10.1 | 0.5 | 1.1 | 0.3 | 27.9 |
| Simulation, STEP | 4.0 | 3.0 | 8.4 | 1&nbsp;ms | 10.1 | 6.2 | 1.0 | 0.3 | 33.0 |
| Simulation, STL | 4.2 | 3.0 | 8.4 | 2&nbsp;ms | 10.4 | 1.0 | 1.0 | 0.3 | 28.3 |
| Simulation, OBJ | 3.8 | 2.9 | 8.6 | 1&nbsp;ms | 9.6 | 14.9 | 1.0 | 0.3 | 41.1 |
| Visual, GLB | 3.9 | 2.8 | 8.4 | 1&nbsp;ms | 18.3 | 0.3 | 2.6 | 0.3 | 36.5 |
| Visual, OBJ | 3.9 | 3.0 | 8.7 | 1&nbsp;ms | 17.9 | 10.2 | 2.5 | 0.3 | 46.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/oculink-pcie-adapter](https://github.com/antmicro/oculink-pcie-adapter)<br>Board: `oculink-to-pcie-adapter.kicad_pcb` |
|---|---|
| Complexity | 366&nbsp;/&nbsp;1000 (size&nbsp;221, features&nbsp;145) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, knockout text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 144, 1,642, 583 |
| Triangles,&nbsp;simulation | 2,446,380 in 211 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">83&nbsp;MB</td><td align="right">934&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">283&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">122&nbsp;MB</td><td align="right">881&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">253&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">56&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">172&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.86 optiga-tpm

![optiga-tpm: stages 4 and 6 take 51% to 80% of a run. Simulation, GLB takes 4.8 s. Simulation, STEP takes 6.7 s. Simulation, STL takes 4.9 s. Simulation, OBJ takes 6.9 s. Visual, GLB takes 7.2 s. Visual, OBJ takes 8.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/optiga-tpm_optiga-tpm.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 0.4 | 1.7 | 0.3&nbsp;ms | 1.8 | 58&nbsp;ms | 0.2 | 0.2 | 4.8 |
| Simulation, STEP | 0.5 | 0.4 | 1.6 | 0.2&nbsp;ms | 1.8 | 2.0 | 0.2 | 0.2 | 6.7 |
| Simulation, STL | 0.5 | 0.4 | 1.6 | 0.2&nbsp;ms | 1.8 | 0.1 | 0.2 | 0.2 | 4.9 |
| Simulation, OBJ | 0.5 | 0.4 | 1.6 | 0.2&nbsp;ms | 1.8 | 1.9 | 0.3 | 0.3 | 6.9 |
| Visual, GLB | 0.5 | 0.4 | 1.6 | 0.2&nbsp;ms | 4.2 | 56&nbsp;ms | 0.3 | 0.2 | 7.2 |
| Visual, OBJ | 0.5 | 0.4 | 1.6 | 0.3&nbsp;ms | 4.0 | 1.3 | 0.2 | 0.2 | 8.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/optiga-tpm](https://github.com/antmicro/optiga-tpm)<br>Board: `optiga-tpm.kicad_pcb` |
|---|---|
| Complexity | 302&nbsp;/&nbsp;1000 (size&nbsp;182, features&nbsp;120) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 22, 189, 27 |
| Triangles,&nbsp;simulation | 339,494 in 70 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">302&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">77&nbsp;MB</td><td align="right">331&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">17&nbsp;MB</td><td align="right">298&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">35&nbsp;MB</td><td align="right">312&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.5&nbsp;MB</td><td align="right">342&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">25&nbsp;MB</td><td align="right">308&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.87 bmc-reference-osm

![bmc-reference-osm: stages 4 and 6 take 45% to 84% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 2 min. Simulation, STL takes 2 min. Simulation, OBJ takes 3 min. Visual, GLB takes 4 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/osm-l-bmc-som_bmc-reference-osm.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 12.1 | 11.9 | 40.1 | 2&nbsp;ms | 42.6 | 2.1 | 7.8 | 0.6 | 117.2 |
| Simulation, STEP | 12.7 | 12.3 | 40.8 | 2&nbsp;ms | 42.9 | 24.5 | 8.0 | 0.6 | 141.7 |
| Simulation, STL | 12.6 | 12.4 | 41.8 | 3&nbsp;ms | 43.3 | 4.1 | 7.8 | 0.7 | 122.7 |
| Simulation, OBJ | 12.3 | 12.5 | 41.1 | 3&nbsp;ms | 42.2 | 66.9 | 7.8 | 0.5 | 183.3 |
| Visual, GLB | 12.7 | 12.0 | 40.4 | 3&nbsp;ms | 141.6 | 1.0 | 7.3 | 0.5 | 215.6 |
| Visual, OBJ | 12.5 | 12.4 | 40.9 | 3&nbsp;ms | 143.6 | 33.7 | 7.2 | 0.5 | 250.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/osm-l-bmc-som](https://github.com/antmicro/osm-l-bmc-som)<br>Board: `bmc-reference-osm.kicad_pcb` |
|---|---|
| Complexity | 553&nbsp;/&nbsp;1000 (size&nbsp;338, features&nbsp;215) |
| KESE&nbsp;features | through vias,<br>blind and buried vias, microvias,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 10 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 376, 7,768, 1,763 |
| Triangles,&nbsp;simulation | 11,357,820 in 1082 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">371&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.2&nbsp;GB</td><td align="right">3.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">568&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.2&nbsp;GB</td><td align="right">7.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">179&nbsp;MB</td><td align="right">3.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">592&nbsp;MB</td><td align="right">4.0&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.88 OV5640-dual-camera-board

![OV5640-dual-camera-board: stages 4 and 6 take 47% to 83% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 15 s. Simulation, STL takes 12 s. Simulation, OBJ takes 19 s. Visual, GLB takes 18 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/ov5640-dual-camera-board_OV5640-dual-camera-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.2 | 4.0 | 1&nbsp;ms | 4.8 | 0.2 | 0.7 | 0.2 | 11.6 |
| Simulation, STEP | 0.4 | 1.2 | 3.7 | 0.8&nbsp;ms | 4.9 | 3.8 | 0.7 | 0.3 | 14.9 |
| Simulation, STL | 0.4 | 1.2 | 3.6 | 0.6&nbsp;ms | 4.9 | 0.5 | 0.7 | 0.3 | 11.6 |
| Simulation, OBJ | 0.4 | 1.3 | 3.8 | 0.6&nbsp;ms | 5.0 | 7.2 | 0.7 | 0.3 | 18.7 |
| Visual, GLB | 0.4 | 1.1 | 3.7 | 0.7&nbsp;ms | 10.9 | 0.2 | 1.1 | 0.2 | 17.6 |
| Visual, OBJ | 0.4 | 1.2 | 3.7 | 0.6&nbsp;ms | 10.9 | 5.0 | 1.4 | 0.2 | 22.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/ov5640-dual-camera-board](https://github.com/antmicro/ov5640-dual-camera-board)<br>Board: `OV5640-dual-camera-board.kicad_pcb` |
|---|---|
| Complexity | 308&nbsp;/&nbsp;1000 (size&nbsp;203, features&nbsp;105) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 82, 943, 234 |
| Triangles,&nbsp;simulation | 1,484,392 in 137 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">51&nbsp;MB</td><td align="right">688&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">231&nbsp;MB</td><td align="right">752&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">74&nbsp;MB</td><td align="right">666&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">154&nbsp;MB</td><td align="right">990&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">34&nbsp;MB</td><td align="right">711&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">103&nbsp;MB</td><td align="right">774&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.89 ov9281-dual-camera-board

![ov9281-dual-camera-board: stages 4 and 6 take 45% to 77% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 21 s. Simulation, STL takes 17 s. Simulation, OBJ takes 25 s. Visual, GLB takes 24 s. Visual, OBJ takes 31 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/ov9281-camera-board_ov9281-dual-camera-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.2 | 1.5 | 4.6 | 0.6&nbsp;ms | 6.8 | 0.3 | 0.8 | 0.3 | 16.4 |
| Simulation, STEP | 2.1 | 1.5 | 4.6 | 0.7&nbsp;ms | 6.9 | 4.9 | 0.8 | 0.3 | 21.1 |
| Simulation, STL | 2.3 | 1.6 | 4.5 | 0.5&nbsp;ms | 6.9 | 0.5 | 0.7 | 0.2 | 16.7 |
| Simulation, OBJ | 2.1 | 1.4 | 4.4 | 0.6&nbsp;ms | 6.6 | 9.3 | 0.7 | 0.2 | 24.9 |
| Visual, GLB | 2.1 | 1.4 | 4.3 | 0.5&nbsp;ms | 13.7 | 0.2 | 1.4 | 0.3 | 23.5 |
| Visual, OBJ | 2.3 | 1.5 | 4.5 | 0.6&nbsp;ms | 13.9 | 6.8 | 1.5 | 0.3 | 30.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/ov9281-camera-board](https://github.com/antmicro/ov9281-camera-board)<br>Board: `ov9281-dual-camera-board.kicad_pcb` |
|---|---|
| Complexity | 329&nbsp;/&nbsp;1000 (size&nbsp;204, features&nbsp;125) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 77, 1,196, 233 |
| Triangles,&nbsp;simulation | 1,594,572 in 138 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">54&nbsp;MB</td><td align="right">770&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">244&nbsp;MB</td><td align="right">842&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">80&nbsp;MB</td><td align="right">752&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">164&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">39&nbsp;MB</td><td align="right">849&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">119&nbsp;MB</td><td align="right">917&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.90 pmod-i3c-driver

![pmod-i3c-driver: stages 4 and 6 take 49% to 80% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 14 s. Simulation, STL takes 11 s. Simulation, OBJ takes 15 s. Visual, GLB takes 17 s. Visual, OBJ takes 20 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/pmod-i3c-driver_pmod-i3c-driver.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.2 | 0.9 | 4.1 | 0.4&nbsp;ms | 3.9 | 0.2 | 0.6 | 0.3 | 11.1 |
| Simulation, STEP | 1.2 | 0.8 | 3.9 | 0.4&nbsp;ms | 3.9 | 3.4 | 0.4 | 0.3 | 14.0 |
| Simulation, STL | 1.1 | 0.9 | 3.8 | 0.3&nbsp;ms | 3.6 | 0.4 | 0.5 | 0.3 | 10.6 |
| Simulation, OBJ | 1.2 | 0.8 | 3.9 | 0.4&nbsp;ms | 3.6 | 4.9 | 0.6 | 0.3 | 15.2 |
| Visual, GLB | 1.2 | 0.8 | 4.0 | 0.4&nbsp;ms | 9.7 | 0.1 | 1.0 | 0.3 | 17.1 |
| Visual, OBJ | 1.1 | 0.9 | 3.8 | 0.9&nbsp;ms | 9.7 | 3.6 | 1.0 | 0.3 | 20.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/pmod-i3c-driver](https://github.com/antmicro/pmod-i3c-driver)<br>Board: `pmod-i3c-driver.kicad_pcb` |
|---|---|
| Complexity | 304&nbsp;/&nbsp;1000 (size&nbsp;189, features&nbsp;115) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 62, 610, 83 |
| Triangles,&nbsp;simulation | 1,045,598 in 59 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">36&nbsp;MB</td><td align="right">504&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">162&nbsp;MB</td><td align="right">564&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">52&nbsp;MB</td><td align="right">489&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">106&nbsp;MB</td><td align="right">785&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">23&nbsp;MB</td><td align="right">629&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">69&nbsp;MB</td><td align="right">697&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.91 pmod-i3c-sensor-board

![pmod-i3c-sensor-board: stages 4 and 6 take 47% to 76% of a run. Simulation, GLB takes 8.9 s. Simulation, STEP takes 11 s. Simulation, STL takes 8.8 s. Simulation, OBJ takes 13 s. Visual, GLB takes 13 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/pmod-i3c-sensor-board_pmod-i3c-sensor-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.2 | 0.8 | 2.8 | 0.6&nbsp;ms | 3.4 | 0.2 | 0.4 | 0.2 | 8.9 |
| Simulation, STEP | 1.0 | 0.7 | 2.6 | 0.4&nbsp;ms | 3.3 | 2.7 | 0.4 | 0.3 | 11.0 |
| Simulation, STL | 1.1 | 0.7 | 2.6 | 0.3&nbsp;ms | 3.4 | 0.3 | 0.4 | 0.3 | 8.8 |
| Simulation, OBJ | 1.1 | 0.8 | 2.7 | 0.4&nbsp;ms | 3.4 | 4.2 | 0.4 | 0.3 | 12.9 |
| Visual, GLB | 1.1 | 0.8 | 2.7 | 0.4&nbsp;ms | 6.9 | 0.1 | 0.8 | 0.3 | 12.5 |
| Visual, OBJ | 1.1 | 0.8 | 2.6 | 0.7&nbsp;ms | 7.3 | 3.2 | 0.8 | 0.3 | 16.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/pmod-i3c-sensor-board](https://github.com/antmicro/pmod-i3c-sensor-board)<br>Board: `pmod-i3c-sensor-board.kicad_pcb` |
|---|---|
| Complexity | 311&nbsp;/&nbsp;1000 (size&nbsp;191, features&nbsp;120) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, knockout text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 75, 642, 71 |
| Triangles,&nbsp;simulation | 825,250 in 62 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">415&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">135&nbsp;MB</td><td align="right">499&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">41&nbsp;MB</td><td align="right">419&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">84&nbsp;MB</td><td align="right">651&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">21&nbsp;MB</td><td align="right">562&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">62&nbsp;MB</td><td align="right">558&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.92 antmicro-poe-to-usbc-pd-adapter

![Stages 4 and 6 take 49% to 80% of a run. Simulation, GLB takes 45 s. Simulation, STEP takes 53 s. Simulation, STL takes 44 s. Simulation, OBJ takes 64 s. Visual, GLB takes 70 s. Visual, OBJ takes 85 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/poe-usb-c-pd-converter_antmicro-poe-to-usbc-pd-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 5.2 | 4.2 | 15.9 | 0.8&nbsp;ms | 15.9 | 1.0 | 2.1 | 0.4 | 44.7 |
| Simulation, STEP | 4.7 | 4.0 | 15.8 | 2&nbsp;ms | 15.7 | 10.4 | 1.7 | 0.4 | 52.5 |
| Simulation, STL | 4.2 | 4.2 | 16.0 | 0.7&nbsp;ms | 15.2 | 2.1 | 1.8 | 0.4 | 43.8 |
| Simulation, OBJ | 4.9 | 4.5 | 15.8 | 2&nbsp;ms | 15.7 | 20.9 | 1.8 | 0.3 | 63.8 |
| Visual, GLB | 4.5 | 3.8 | 15.7 | 1&nbsp;ms | 40.2 | 0.4 | 4.7 | 0.4 | 69.7 |
| Visual, OBJ | 5.3 | 3.8 | 15.1 | 0.8&nbsp;ms | 39.7 | 14.1 | 7.0 | 0.4 | 85.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/poe-usb-c-pd-converter](https://github.com/antmicro/poe-usb-c-pd-converter)<br>Board: `antmicro-poe-to-usbc-pd-adapter.kicad_pcb` |
|---|---|
| Complexity | 394&nbsp;/&nbsp;1000 (size&nbsp;269, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, knockout text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 230, 1,786, 767 |
| Triangles,&nbsp;simulation | 3,931,522 in 244 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">133&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">481&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">197&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">411&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">83&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">261&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.93 polarfire-som

![polarfire-som: stages 4 and 6 take 39% to 85% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 3 min. Simulation, STL takes 2 min. Simulation, OBJ takes 4 min. Visual, GLB takes 5 min. Visual, OBJ takes 5 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/polarfire-som_polarfire-som.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 16.1 | 11.9 | 35.7 | 1&nbsp;ms | 57.0 | 3.3 | 8.5 | 0.6 | 133.1 |
| Simulation, STEP | 16.0 | 12.1 | 36.2 | 2&nbsp;ms | 60.9 | 33.6 | 9.5 | 0.6 | 168.8 |
| Simulation, STL | 15.2 | 11.0 | 32.7 | 2&nbsp;ms | 53.6 | 6.7 | 8.6 | 0.6 | 128.4 |
| Simulation, OBJ | 14.9 | 11.5 | 33.0 | 2&nbsp;ms | 54.4 | 98.5 | 8.8 | 0.7 | 221.9 |
| Visual, GLB | 15.7 | 11.4 | 33.1 | 2&nbsp;ms | 203.4 | 1.2 | 12.1 | 0.6 | 277.5 |
| Visual, OBJ | 15.9 | 12.0 | 35.1 | 2&nbsp;ms | 207.8 | 42.4 | 11.7 | 0.7 | 325.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/polarfire-som](https://github.com/antmicro/polarfire-som)<br>Board: `polarfire-som.kicad_pcb` |
|---|---|
| Complexity | 517&nbsp;/&nbsp;1000 (size&nbsp;357, features&nbsp;160) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 14 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 421, 13,972, 1,565 |
| Triangles,&nbsp;simulation | 15,008,058 in 793 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">476&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.6&nbsp;GB</td><td align="right">4.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">750&nbsp;MB</td><td align="right">3.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.6&nbsp;GB</td><td align="right">9.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">226&nbsp;MB</td><td align="right">4.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">760&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.94 led-panel

![led-panel: stages 4 and 6 take 42% to 72% of a run. Simulation, GLB takes 68 s. Simulation, STEP takes 81 s. Simulation, STL takes 69 s. Simulation, OBJ takes 2 min. Visual, GLB takes 79 s. Visual, OBJ takes 95 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/programmable-led-panel_led-panel.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 10.6 | 7.8 | 23.3 | 2&nbsp;ms | 20.7 | 1.1 | 3.9 | 0.5 | 67.9 |
| Simulation, STEP | 10.2 | 7.2 | 24.0 | 2&nbsp;ms | 21.0 | 13.8 | 4.0 | 0.4 | 80.5 |
| Simulation, STL | 9.8 | 7.4 | 24.2 | 1&nbsp;ms | 21.1 | 2.1 | 4.2 | 0.5 | 69.2 |
| Simulation, OBJ | 10.3 | 7.5 | 23.2 | 0.8&nbsp;ms | 21.0 | 38.5 | 4.1 | 0.4 | 105.0 |
| Visual, GLB | 10.0 | 7.3 | 24.1 | 2&nbsp;ms | 32.6 | 0.5 | 3.8 | 0.4 | 78.7 |
| Visual, OBJ | 10.6 | 7.5 | 23.3 | 2&nbsp;ms | 33.9 | 15.3 | 3.8 | 0.4 | 94.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/programmable-led-panel](https://github.com/antmicro/programmable-led-panel)<br>Board: `led-panel.kicad_pcb` |
|---|---|
| Complexity | 441&nbsp;/&nbsp;1000 (size&nbsp;296, features&nbsp;145) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 294, 3,031, 741 |
| Triangles,&nbsp;simulation | 5,718,302 in 275 parts |
| Note | panel |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">194&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">538&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">286&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">611&nbsp;MB</td><td align="right">3.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">87&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">273&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.95 qomu-board

![qomu-board: stages 4 and 6 take 48% to 80% of a run. Simulation, GLB takes 8.9 s. Simulation, STEP takes 11 s. Simulation, STL takes 8.9 s. Simulation, OBJ takes 14 s. Visual, GLB takes 13 s. Visual, OBJ takes 14 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/qomu-dev-board_qomu-board_1290.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.4 | 3.2 | 0.4&nbsp;ms | 3.0 | 0.2 | 0.5 | 0.2 | 8.9 |
| Simulation, STEP | 0.3 | 1.4 | 3.4 | 0.4&nbsp;ms | 3.0 | 2.1 | 0.4 | 0.2 | 10.8 |
| Simulation, STL | 0.3 | 1.4 | 3.3 | 0.3&nbsp;ms | 3.0 | 0.2 | 0.4 | 0.2 | 8.9 |
| Simulation, OBJ | 0.3 | 1.4 | 3.6 | 0.3&nbsp;ms | 3.1 | 4.9 | 0.4 | 0.2 | 14.0 |
| Visual, GLB | 0.3 | 1.5 | 3.5 | 0.4&nbsp;ms | 6.8 | 76&nbsp;ms | 0.5 | 0.2 | 12.9 |
| Visual, OBJ | 0.3 | 1.4 | 3.4 | 0.3&nbsp;ms | 6.3 | 2.2 | 0.5 | 0.2 | 14.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/qomu-dev-board](https://github.com/antmicro/qomu-dev-board)<br>Board: `qomu-board.kicad_pcb` |
|---|---|
| Complexity | 418&nbsp;/&nbsp;1000 (size&nbsp;258, features&nbsp;160) |
| KESE&nbsp;features | through vias,<br>blind and buried vias, microvias,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 56, 853, 194 |
| Triangles,&nbsp;simulation | 866,700 in 66 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">353&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">118&nbsp;MB</td><td align="right">411&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">43&nbsp;MB</td><td align="right">349&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">89&nbsp;MB</td><td align="right">615&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">412&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">44&nbsp;MB</td><td align="right">405&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.96 quickfeather-board

![quickfeather-board: stages 4 and 6 take 51% to 80% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 26 s. Simulation, STL takes 22 s. Simulation, OBJ takes 32 s. Visual, GLB takes 29 s. Visual, OBJ takes 36 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/quickfeather-dev-board_quickfeather-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.1 | 1.9 | 9.5 | 0.7&nbsp;ms | 8.2 | 0.3 | 0.9 | 0.3 | 23.2 |
| Simulation, STEP | 2.1 | 1.8 | 8.5 | 0.5&nbsp;ms | 8.0 | 4.7 | 0.9 | 0.3 | 26.2 |
| Simulation, STL | 2.1 | 1.8 | 8.3 | 0.9&nbsp;ms | 8.0 | 0.5 | 0.9 | 0.3 | 21.9 |
| Simulation, OBJ | 2.1 | 1.8 | 8.2 | 0.6&nbsp;ms | 8.2 | 10.7 | 0.9 | 0.3 | 32.1 |
| Visual, GLB | 2.2 | 1.8 | 8.4 | 0.6&nbsp;ms | 15.1 | 0.2 | 1.2 | 0.3 | 29.2 |
| Visual, OBJ | 2.1 | 1.8 | 8.3 | 0.6&nbsp;ms | 15.3 | 6.7 | 1.5 | 0.3 | 36.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/quickfeather-dev-board](https://github.com/antmicro/quickfeather-dev-board)<br>Board: `quickfeather-board.kicad_pcb` |
|---|---|
| Complexity | 334&nbsp;/&nbsp;1000 (size&nbsp;249, features&nbsp;85) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 90, 1,689, 224 |
| Triangles,&nbsp;simulation | 1,752,598 in 158 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">60&nbsp;MB</td><td align="right">666&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">263&nbsp;MB</td><td align="right">799&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">88&nbsp;MB</td><td align="right">674&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">185&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">35&nbsp;MB</td><td align="right">796&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">107&nbsp;MB</td><td align="right">906&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.97 rpi-cm4-csi-adapter

![rpi-cm4-csi-adapter: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 4.5 s. Simulation, STEP takes 6.3 s. Simulation, STL takes 4.9 s. Simulation, OBJ takes 6.8 s. Visual, GLB takes 7.3 s. Visual, OBJ takes 8.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/raspberry-pi-cm4-csi-adapter_rpi-cm4-csi-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.5 | 0.2&nbsp;ms | 1.8 | 78&nbsp;ms | 0.2 | 0.3 | 4.5 |
| Simulation, STEP | 0.2 | 0.4 | 1.5 | 0.2&nbsp;ms | 1.9 | 1.9 | 0.2 | 0.2 | 6.3 |
| Simulation, STL | 0.3 | 0.4 | 1.6 | 0.2&nbsp;ms | 2.0 | 0.1 | 0.2 | 0.3 | 4.9 |
| Simulation, OBJ | 0.2 | 0.4 | 1.4 | 0.3&nbsp;ms | 2.0 | 2.4 | 0.2 | 0.2 | 6.8 |
| Visual, GLB | 0.2 | 0.3 | 1.5 | 0.3&nbsp;ms | 4.5 | 52&nbsp;ms | 0.4 | 0.2 | 7.3 |
| Visual, OBJ | 0.2 | 0.3 | 1.4 | 0.2&nbsp;ms | 4.4 | 1.6 | 0.4 | 0.2 | 8.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/raspberry-pi-cm4-csi-adapter](https://github.com/antmicro/raspberry-pi-cm4-csi-adapter)<br>Board: `rpi-cm4-csi-adapter.kicad_pcb` |
|---|---|
| Complexity | 227&nbsp;/&nbsp;1000 (size&nbsp;172, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 6, 1,229, 38 |
| Triangles,&nbsp;simulation | 471,986 in 33 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">297&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">93&nbsp;MB</td><td align="right">349&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">24&nbsp;MB</td><td align="right">292&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">48&nbsp;MB</td><td align="right">373&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">332&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">32&nbsp;MB</td><td align="right">334&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.98 rpi-led-flex-board

![rpi-led-flex-board: stages 4 and 6 take 55% to 80% of a run. Simulation, GLB takes 4.1 s. Simulation, STEP takes 5.7 s. Simulation, STL takes 4.1 s. Simulation, OBJ takes 5.7 s. Visual, GLB takes 5.2 s. Visual, OBJ takes 6.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/rpi-led-flex-board_rpi-led-flex-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.3 | 1.5 | 0.3&nbsp;ms | 1.7 | 58&nbsp;ms | 0.2 | 0.2 | 4.1 |
| Simulation, STEP | 0.2 | 0.3 | 1.6 | 0.4&nbsp;ms | 1.8 | 1.6 | 0.2 | 0.2 | 5.7 |
| Simulation, STL | 0.2 | 0.3 | 1.5 | 0.2&nbsp;ms | 1.7 | 90&nbsp;ms | 0.2 | 0.2 | 4.1 |
| Simulation, OBJ | 0.2 | 0.3 | 1.6 | 0.2&nbsp;ms | 1.6 | 1.7 | 0.2 | 0.2 | 5.7 |
| Visual, GLB | 0.2 | 0.3 | 1.5 | 0.3&nbsp;ms | 2.7 | 44&nbsp;ms | 0.3 | 0.2 | 5.2 |
| Visual, OBJ | 0.2 | 0.3 | 1.5 | 0.2&nbsp;ms | 2.9 | 1.4 | 0.3 | 0.2 | 6.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/rpi-led-flex-board](https://github.com/antmicro/rpi-led-flex-board)<br>Board: `rpi-led-flex-board.kicad_pcb` |
|---|---|
| Complexity | 245&nbsp;/&nbsp;1000 (size&nbsp;190, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 27, 252, 43 |
| Triangles,&nbsp;simulation | 351,834 in 50 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">272&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">64&nbsp;MB</td><td align="right">316&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">18&nbsp;MB</td><td align="right">271&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">35&nbsp;MB</td><td align="right">282&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">9.5&nbsp;MB</td><td align="right">305&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">27&nbsp;MB</td><td align="right">302&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.3.99 scalenode-adapter

![scalenode-adapter: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 28 s. Simulation, STL takes 24 s. Simulation, OBJ takes 37 s. Visual, GLB takes 37 s. Visual, OBJ takes 45 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/scalenode-adapter_scalenode-adapter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.5 | 9.1 | 0.9&nbsp;ms | 9.1 | 0.4 | 1.0 | 0.2 | 23.0 |
| Simulation, STEP | 0.7 | 2.5 | 8.9 | 0.8&nbsp;ms | 8.5 | 5.9 | 1.1 | 0.3 | 27.9 |
| Simulation, STL | 0.7 | 2.4 | 9.3 | 0.9&nbsp;ms | 9.0 | 0.9 | 1.1 | 0.2 | 23.7 |
| Simulation, OBJ | 0.6 | 2.3 | 9.3 | 0.8&nbsp;ms | 9.4 | 14.3 | 1.2 | 0.3 | 37.4 |
| Visual, GLB | 0.7 | 2.7 | 10.5 | 0.7&nbsp;ms | 20.6 | 0.2 | 2.4 | 0.3 | 37.4 |
| Visual, OBJ | 0.7 | 2.9 | 9.5 | 0.7&nbsp;ms | 20.0 | 9.2 | 2.4 | 0.3 | 45.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/scalenode-adapter](https://github.com/antmicro/scalenode-adapter)<br>Board: `scalenode-adapter.kicad_pcb` |
|---|---|
| Complexity | 356&nbsp;/&nbsp;1000 (size&nbsp;266, features&nbsp;90) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>copper text |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 152, 2,106, 319 |
| Triangles,&nbsp;simulation | 2,397,452 in 181 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">84&nbsp;MB</td><td align="right">883&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">361&nbsp;MB</td><td align="right">985&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">120&nbsp;MB</td><td align="right">888&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">256&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">51&nbsp;MB</td><td align="right">944&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">157&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.3.100 scalenode-cm4-baseboard

![scalenode-cm4-baseboard: stages 4 and 6 take 45% to 77% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 27 s. Simulation, STL takes 23 s. Simulation, OBJ takes 34 s. Visual, GLB takes 39 s. Visual, OBJ takes 47 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-03/scalenode-cm4-baseboard_scalenode-cm4-baseboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.7 | 2.5 | 7.9 | 0.8&nbsp;ms | 7.8 | 0.4 | 1.1 | 0.3 | 22.7 |
| Simulation, STEP | 2.6 | 2.5 | 7.7 | 0.9&nbsp;ms | 7.8 | 5.3 | 0.9 | 0.3 | 27.0 |
| Simulation, STL | 2.7 | 2.6 | 7.8 | 0.8&nbsp;ms | 7.7 | 0.9 | 0.9 | 0.3 | 22.8 |
| Simulation, OBJ | 2.9 | 2.7 | 7.9 | 0.9&nbsp;ms | 7.6 | 12.0 | 0.9 | 0.3 | 34.3 |
| Visual, GLB | 2.7 | 2.5 | 8.1 | 1&nbsp;ms | 21.9 | 0.3 | 3.4 | 0.3 | 39.1 |
| Visual, OBJ | 2.7 | 2.5 | 7.9 | 2&nbsp;ms | 22.0 | 8.1 | 3.1 | 0.3 | 46.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [antmicro/scalenode-cm4-baseboard](https://github.com/antmicro/scalenode-cm4-baseboard)<br>Board: `scalenode-cm4-baseboard.kicad_pcb` |
|---|---|
| Complexity | 358&nbsp;/&nbsp;1000 (size&nbsp;223, features&nbsp;135) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 129, 2,743, 536 |
| Triangles,&nbsp;simulation | 2,773,950 in 292 parts |
| Verifier | Simulation, GLB: Verifier FAIL<br>Simulation, STEP: Verifier FAIL<br>Simulation, STL: Verifier FAIL<br>Simulation, OBJ: Verifier FAIL |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">97&nbsp;MB</td><td align="right">971&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">324&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">139&nbsp;MB</td><td align="right">920&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">297&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">66&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">209&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [Corpus Testing 2: alvaroalea To andrewpaterson](Corpus-Testing-02.md) | [Corpus Testing 4: antmicro To baldengineer](Corpus-Testing-04.md) |
