# 23.16 Corpus Testing 16: mwelling To nuclearfutureslab

Part 16 of 29 of [Corpus Testing](../Corpus-Testing.md): every board of these projects, six runs each, one file format a run, as [Corpus Testing](../Corpus-Testing.md) describes.

## 23.16.1 lofive

![lofive: stages 4 and 6 take 51% to 82% of a run. Simulation, GLB takes 7.5 s. Simulation, STEP takes 8.9 s. Simulation, STL takes 7.3 s. Simulation, OBJ takes 11 s. Visual, GLB takes 11 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lofive_lofive.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 1.0 | 3.1 | 0.3&nbsp;ms | 2.5 | 0.1 | 0.4 | 0.2 | 7.5 |
| Simulation, STEP | 0.2 | 1.0 | 3.0 | 0.3&nbsp;ms | 2.4 | 1.9 | 0.3 | 0.2 | 8.9 |
| Simulation, STL | 0.2 | 0.9 | 3.0 | 0.3&nbsp;ms | 2.4 | 0.3 | 0.3 | 0.2 | 7.3 |
| Simulation, OBJ | 0.2 | 0.9 | 3.1 | 0.3&nbsp;ms | 2.4 | 3.7 | 0.3 | 0.2 | 10.9 |
| Visual, GLB | 0.2 | 1.0 | 3.1 | 0.5&nbsp;ms | 5.6 | 69&nbsp;ms | 0.5 | 0.2 | 10.7 |
| Visual, OBJ | 0.2 | 1.0 | 3.1 | 0.3&nbsp;ms | 5.9 | 2.1 | 0.7 | 0.2 | 13.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwelling/lofive](https://github.com/mwelling/lofive)<br>Board: `lofive.kicad_pcb` |
|---|---|
| Complexity | 264&nbsp;/&nbsp;1000 (size&nbsp;219, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 33, 445, 83 |
| Triangles,&nbsp;simulation | 899,502 in 64 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">419&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">149&nbsp;MB</td><td align="right">452&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">45&nbsp;MB</td><td align="right">407&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">93&nbsp;MB</td><td align="right">646&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">464&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">56&nbsp;MB</td><td align="right">464&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.2 pocketbone-kicad

![pocketbone-kicad: stages 4 and 6 take 57% to 83% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 16 s. Simulation, STL takes 14 s. Simulation, OBJ takes 20 s. Visual, GLB takes 19 s. Visual, OBJ takes 22 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocketbone-kicad_pocketbone-kicad.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.2 | 6.5 | 0.4&nbsp;ms | 4.5 | 0.2 | 0.5 | 0.2 | 13.4 |
| Simulation, STEP | 0.3 | 1.1 | 6.3 | 0.4&nbsp;ms | 4.5 | 3.6 | 0.5 | 0.2 | 16.5 |
| Simulation, STL | 0.3 | 1.2 | 6.5 | 0.8&nbsp;ms | 4.7 | 0.4 | 0.6 | 0.2 | 13.9 |
| Simulation, OBJ | 0.3 | 1.2 | 6.6 | 0.6&nbsp;ms | 4.7 | 6.2 | 0.5 | 0.2 | 19.6 |
| Visual, GLB | 0.3 | 1.2 | 6.4 | 0.4&nbsp;ms | 9.3 | 0.1 | 1.3 | 0.2 | 18.8 |
| Visual, OBJ | 0.3 | 1.2 | 6.3 | 0.4&nbsp;ms | 9.1 | 3.9 | 1.1 | 0.2 | 22.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwelling/pocketbone-kicad](https://github.com/mwelling/pocketbone-kicad)<br>Board: `pocketbone-kicad.kicad_pcb` |
|---|---|
| Complexity | 292&nbsp;/&nbsp;1000 (size&nbsp;247, features&nbsp;45) |
| KESE&nbsp;features | through vias, filled zones,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 56, 891, 151 |
| Triangles,&nbsp;simulation | 1,477,718 in 88 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">52&nbsp;MB</td><td align="right">655&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">247&nbsp;MB</td><td align="right">754&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">74&nbsp;MB</td><td align="right">652&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">155&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">34&nbsp;MB</td><td align="right">687&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">102&nbsp;MB</td><td align="right">791&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.3 OpenCAPI-to-PCIe_for_MNV303212A_RevA2

![Stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 17 s. Simulation, STL takes 13 s. Simulation, OBJ takes 20 s. Visual, GLB takes 21 s. Visual, OBJ takes 27 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/opencapi-to-pcie-for-mnv303212a-reva2_OpenCAPI-to-PCIe-for-MNV303212A-RevA2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.2 | 4.3 | 0.5&nbsp;ms | 5.6 | 0.2 | 0.7 | 0.3 | 12.7 |
| Simulation, STEP | 0.4 | 1.2 | 4.3 | 0.4&nbsp;ms | 5.8 | 4.5 | 0.8 | 0.3 | 17.3 |
| Simulation, STL | 0.4 | 1.3 | 4.4 | 0.4&nbsp;ms | 5.8 | 0.4 | 0.8 | 0.3 | 13.3 |
| Simulation, OBJ | 0.4 | 1.2 | 4.6 | 0.4&nbsp;ms | 5.6 | 7.6 | 0.8 | 0.2 | 20.4 |
| Visual, GLB | 0.4 | 1.2 | 4.3 | 0.4&nbsp;ms | 12.9 | 0.2 | 1.4 | 0.3 | 20.7 |
| Visual, OBJ | 0.4 | 1.2 | 4.2 | 0.5&nbsp;ms | 12.5 | 6.9 | 1.6 | 0.3 | 27.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwrnd/opencapi-to-pcie_for_mnv303212a_reva2](https://github.com/mwrnd/opencapi-to-pcie_for_mnv303212a_reva2)<br>Board: `OpenCAPI-to-PCIe_for_MNV303212A_RevA2.kicad_pcb` |
|---|---|
| Complexity | 284&nbsp;/&nbsp;1000 (size&nbsp;184, features&nbsp;100) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 5, 2,398, 175 |
| Triangles,&nbsp;simulation | 1,358,418 in 85 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">46&nbsp;MB</td><td align="right">650&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">212&nbsp;MB</td><td align="right">780&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">68&nbsp;MB</td><td align="right">645&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">139&nbsp;MB</td><td align="right">897&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">37&nbsp;MB</td><td align="right">720&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">112&nbsp;MB</td><td align="right">828&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.4 AnalogComputer

![AnalogComputer: stages 4 and 6 take 50% to 85% of a run. Simulation, GLB takes 53 s. Simulation, STEP takes 62 s. Simulation, STL takes 52 s. Simulation, OBJ takes 77 s. Visual, GLB takes 67 s. Visual, OBJ takes 81 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_AnalogComputer.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.1 | 5.2 | 20.7 | 0.9&nbsp;ms | 21.3 | 0.9 | 3.4 | 0.4 | 53.0 |
| Simulation, STEP | 1.1 | 4.7 | 19.1 | 1&nbsp;ms | 20.5 | 12.8 | 3.0 | 0.3 | 61.5 |
| Simulation, STL | 1.1 | 5.0 | 18.5 | 0.8&nbsp;ms | 21.5 | 2.2 | 3.1 | 0.3 | 51.9 |
| Simulation, OBJ | 1.1 | 4.9 | 18.5 | 0.9&nbsp;ms | 19.8 | 29.1 | 3.1 | 0.4 | 76.8 |
| Visual, GLB | 1.0 | 4.5 | 17.8 | 0.8&nbsp;ms | 39.2 | 0.3 | 4.0 | 0.3 | 67.2 |
| Visual, OBJ | 1.0 | 4.7 | 17.5 | 0.9&nbsp;ms | 39.0 | 13.2 | 4.8 | 0.3 | 80.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `AnalogComputer.kicad_pcb` |
|---|---|
| Folder | circuits / AnalogCalculator / AnalogComputer |
| Complexity | 285&nbsp;/&nbsp;1000 (size&nbsp;210, features&nbsp;75) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 113, 2,006, 31 |
| Triangles,&nbsp;simulation | 4,617,684 in 226 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">159&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">681&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">231&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">495&nbsp;MB</td><td align="right">3.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">73&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">228&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.5 Diode Function

![Diode Function: stages 4 and 6 take 55% to 84% of a run. Simulation, GLB takes 8.0 s. Simulation, STEP takes 11 s. Simulation, STL takes 8.4 s. Simulation, OBJ takes 12 s. Visual, GLB takes 10 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Diode-Function.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 3.7 | 1.0&nbsp;ms | 2.7 | 0.1 | 0.4 | 0.2 | 8.0 |
| Simulation, STEP | 0.2 | 0.7 | 3.9 | 0.4&nbsp;ms | 3.0 | 2.2 | 0.4 | 0.2 | 10.5 |
| Simulation, STL | 0.2 | 0.7 | 3.9 | 0.5&nbsp;ms | 2.8 | 0.2 | 0.4 | 0.2 | 8.4 |
| Simulation, OBJ | 0.2 | 0.6 | 3.9 | 0.4&nbsp;ms | 2.8 | 4.1 | 0.3 | 0.2 | 12.3 |
| Visual, GLB | 0.3 | 0.6 | 3.9 | 0.5&nbsp;ms | 4.5 | 69&nbsp;ms | 0.5 | 0.2 | 10.0 |
| Visual, OBJ | 0.2 | 0.7 | 3.8 | 0.8&nbsp;ms | 4.7 | 2.4 | 0.5 | 0.2 | 12.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Diode Function.kicad_pcb` |
|---|---|
| Folder | circuits / AnalogCalculator / Diode Function / Diode Function |
| Complexity | 173&nbsp;/&nbsp;1000 (size&nbsp;158, features&nbsp;15) |
| KESE&nbsp;features | through vias |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 69, 320, 7 |
| Triangles,&nbsp;simulation | 845,732 in 56 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">392&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">109&nbsp;MB</td><td align="right">462&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">42&nbsp;MB</td><td align="right">375&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">84&nbsp;MB</td><td align="right">592&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">464&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">48&nbsp;MB</td><td align="right">497&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.6 OperationalAmplifierExamples

![OperationalAmplifierExamples: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 7.2 s. Simulation, STEP takes 9.5 s. Simulation, STL takes 7.3 s. Simulation, OBJ takes 11 s. Visual, GLB takes 11 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_OperationalAmplifierExamples.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 3.2 | 0.6&nbsp;ms | 2.6 | 0.1 | 0.4 | 0.2 | 7.2 |
| Simulation, STEP | 0.2 | 0.5 | 3.1 | 0.5&nbsp;ms | 2.9 | 2.1 | 0.4 | 0.3 | 9.5 |
| Simulation, STL | 0.2 | 0.5 | 3.2 | 0.5&nbsp;ms | 2.6 | 0.2 | 0.4 | 0.2 | 7.3 |
| Simulation, OBJ | 0.2 | 0.4 | 3.2 | 0.5&nbsp;ms | 2.8 | 4.1 | 0.4 | 0.3 | 11.3 |
| Visual, GLB | 0.2 | 0.5 | 3.4 | 1&nbsp;ms | 5.4 | 72&nbsp;ms | 0.5 | 0.3 | 10.5 |
| Visual, OBJ | 0.2 | 0.7 | 3.2 | 0.4&nbsp;ms | 5.6 | 2.2 | 0.8 | 0.2 | 13.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `OperationalAmplifierExamples.kicad_pcb` |
|---|---|
| Folder | circuits / AnalogCalculator / OperationalAmplifierExamples / OperationalAmplifierExamples |
| Complexity | 175&nbsp;/&nbsp;1000 (size&nbsp;145, features&nbsp;30) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 48, 195, 0 |
| Triangles,&nbsp;simulation | 846,610 in 53 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">409&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">117&nbsp;MB</td><td align="right">469&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">42&nbsp;MB</td><td align="right">392&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">84&nbsp;MB</td><td align="right">589&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">498&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">50&nbsp;MB</td><td align="right">466&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.7 Connectors

![Connectors: stages 4 and 6 take 48% to 76% of a run. Simulation, GLB takes 2.2 s. Simulation, STEP takes 3.1 s. Simulation, STL takes 2.2 s. Simulation, OBJ takes 3.1 s. Visual, GLB takes 3.1 s. Visual, OBJ takes 3.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Connectors.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.2 | 0.8 | 0.2&nbsp;ms | 0.7 | 32&nbsp;ms | 0.1 | 0.2 | 2.2 |
| Simulation, STEP | 0.1 | 0.2 | 0.8 | 0.2&nbsp;ms | 0.7 | 1.0 | 0.1 | 0.2 | 3.1 |
| Simulation, STL | 0.1 | 0.2 | 0.7 | 0.1&nbsp;ms | 0.8 | 46&nbsp;ms | 0.1 | 0.3 | 2.2 |
| Simulation, OBJ | 0.1 | 0.2 | 0.8 | 0.2&nbsp;ms | 0.7 | 1.0 | 0.1 | 0.2 | 3.1 |
| Visual, GLB | 0.1 | 0.2 | 0.8 | 0.3&nbsp;ms | 1.6 | 21&nbsp;ms | 0.2 | 0.3 | 3.1 |
| Visual, OBJ | 89&nbsp;ms | 0.2 | 0.8 | 0.2&nbsp;ms | 1.5 | 0.5 | 0.1 | 0.2 | 3.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Connectors.kicad_pcb` |
|---|---|
| Folder | circuits / AnalogCalculator / SimpleOpAmp / Connectors / Connectors |
| Complexity | 120&nbsp;/&nbsp;1000 (size&nbsp;105, features&nbsp;15) |
| KESE&nbsp;features | through vias |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 1, 122, 4 |
| Triangles,&nbsp;simulation | 231,562 in 30 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">7.7&nbsp;MB</td><td align="right">216&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">28&nbsp;MB</td><td align="right">229&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">12&nbsp;MB</td><td align="right">221&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">213&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.3&nbsp;MB</td><td align="right">203&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">12&nbsp;MB</td><td align="right">200&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.8 Simple OpAmp

![Simple OpAmp: stages 4 and 6 take 56% to 84% of a run. Simulation, GLB takes 36 s. Simulation, STEP takes 45 s. Simulation, STL takes 37 s. Simulation, OBJ takes 54 s. Visual, GLB takes 45 s. Visual, OBJ takes 55 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Simple-OpAmp.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 3.2 | 15.7 | 1&nbsp;ms | 14.2 | 0.5 | 1.3 | 0.3 | 35.8 |
| Simulation, STEP | 0.6 | 3.2 | 15.7 | 1&nbsp;ms | 14.7 | 9.0 | 1.4 | 0.3 | 44.9 |
| Simulation, STL | 0.7 | 3.2 | 15.7 | 1&nbsp;ms | 14.9 | 1.1 | 1.5 | 0.3 | 37.3 |
| Simulation, OBJ | 0.6 | 3.2 | 16.1 | 1&nbsp;ms | 14.6 | 18.1 | 1.5 | 0.3 | 54.3 |
| Visual, GLB | 0.7 | 3.2 | 15.6 | 1&nbsp;ms | 22.3 | 0.3 | 2.6 | 0.3 | 45.0 |
| Visual, OBJ | 0.7 | 3.2 | 16.2 | 1&nbsp;ms | 22.2 | 9.6 | 2.8 | 0.3 | 54.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Simple OpAmp.kicad_pcb` |
|---|---|
| Folder | circuits / AnalogCalculator / SimpleOpAmp / Simple OpAmp |
| Complexity | 83&nbsp;/&nbsp;1000 (size&nbsp;73, features&nbsp;10) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 174, 0, 0 |
| Triangles,&nbsp;simulation | 3,102,728 in 334 parts |
| Note | mostly unrouted |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">98&nbsp;MB</td><td align="right">895&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">366&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">155&nbsp;MB</td><td align="right">904&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">330&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">57&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">178&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.9 Regulator7913-1

![Regulator7913-1: stages 4 and 6 take 52% to 81% of a run. Simulation, GLB takes 4.9 s. Simulation, STEP takes 6.6 s. Simulation, STL takes 4.9 s. Simulation, OBJ takes 7.2 s. Visual, GLB takes 6.1 s. Visual, OBJ takes 7.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Regulator7913-1.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 1.9 | 0.4&nbsp;ms | 1.8 | 76&nbsp;ms | 0.3 | 0.2 | 4.9 |
| Simulation, STEP | 0.2 | 0.4 | 2.1 | 0.3&nbsp;ms | 1.8 | 1.6 | 0.3 | 0.3 | 6.6 |
| Simulation, STL | 0.2 | 0.4 | 2.0 | 0.3&nbsp;ms | 1.8 | 0.1 | 0.2 | 0.2 | 4.9 |
| Simulation, OBJ | 0.2 | 0.4 | 2.0 | 0.3&nbsp;ms | 1.8 | 2.3 | 0.3 | 0.3 | 7.2 |
| Visual, GLB | 0.1 | 0.4 | 1.9 | 0.4&nbsp;ms | 3.0 | 45&nbsp;ms | 0.4 | 0.2 | 6.1 |
| Visual, OBJ | 0.2 | 0.3 | 2.0 | 0.4&nbsp;ms | 3.0 | 1.2 | 0.4 | 0.2 | 7.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Regulator7913-1.kicad_pcb` |
|---|---|
| Folder | circuits / ComdynaGP6 / Regulator7913-1 |
| Complexity | 160&nbsp;/&nbsp;1000 (size&nbsp;145, features&nbsp;15) |
| KESE&nbsp;features | through vias |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 34, 242, 1 |
| Triangles,&nbsp;simulation | 497,452 in 48 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">275&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">64&nbsp;MB</td><td align="right">337&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">25&nbsp;MB</td><td align="right">282&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">49&nbsp;MB</td><td align="right">376&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">9.0&nbsp;MB</td><td align="right">311&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">27&nbsp;MB</td><td align="right">316&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.10 Digital Logic Board

![Digital Logic Board: stages 4 and 6 take 48% to 78% of a run. Simulation, GLB takes 4.9 s. Simulation, STEP takes 6.3 s. Simulation, STL takes 5.2 s. Simulation, OBJ takes 7.4 s. Visual, GLB takes 6.8 s. Visual, OBJ takes 8.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Digital-Logic-Board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.7 | 2.0 | 0.4&nbsp;ms | 1.5 | 65&nbsp;ms | 0.3 | 0.2 | 4.9 |
| Simulation, STEP | 0.1 | 0.7 | 1.8 | 0.5&nbsp;ms | 1.5 | 1.6 | 0.3 | 0.2 | 6.3 |
| Simulation, STL | 0.1 | 0.8 | 1.9 | 0.4&nbsp;ms | 1.7 | 0.2 | 0.3 | 0.3 | 5.2 |
| Simulation, OBJ | 0.1 | 0.7 | 2.0 | 0.3&nbsp;ms | 1.5 | 2.4 | 0.3 | 0.3 | 7.4 |
| Visual, GLB | 0.2 | 0.7 | 2.0 | 0.4&nbsp;ms | 3.2 | 44&nbsp;ms | 0.4 | 0.2 | 6.8 |
| Visual, OBJ | 0.1 | 0.7 | 1.9 | 0.3&nbsp;ms | 3.2 | 1.3 | 0.4 | 0.2 | 8.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Digital Logic Board.kicad_pcb` |
|---|---|
| Folder | circuits / Digital Tools / Digital Logic Board |
| Complexity | 176&nbsp;/&nbsp;1000 (size&nbsp;131, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 10, 194, 8 |
| Triangles,&nbsp;simulation | 509,302 in 44 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">284&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">82&nbsp;MB</td><td align="right">349&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">25&nbsp;MB</td><td align="right">296&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">51&nbsp;MB</td><td align="right">384&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">9.7&nbsp;MB</td><td align="right">328&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">29&nbsp;MB</td><td align="right">332&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.11 Examples

![Examples: stages 4 and 6 take 55% to 81% of a run. Simulation, GLB takes 5.1 s. Simulation, STEP takes 6.8 s. Simulation, STL takes 5.2 s. Simulation, OBJ takes 7.8 s. Visual, GLB takes 6.2 s. Visual, OBJ takes 7.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Examples.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 2.1 | 0.5&nbsp;ms | 1.8 | 69&nbsp;ms | 0.2 | 0.2 | 5.1 |
| Simulation, STEP | 0.2 | 0.4 | 2.3 | 0.3&nbsp;ms | 1.9 | 1.6 | 0.2 | 0.2 | 6.8 |
| Simulation, STL | 0.2 | 0.4 | 2.2 | 0.4&nbsp;ms | 1.8 | 0.1 | 0.2 | 0.3 | 5.2 |
| Simulation, OBJ | 0.2 | 0.5 | 2.4 | 0.2&nbsp;ms | 1.9 | 2.4 | 0.2 | 0.2 | 7.8 |
| Visual, GLB | 0.2 | 0.4 | 2.1 | 0.3&nbsp;ms | 2.8 | 41&nbsp;ms | 0.3 | 0.2 | 6.2 |
| Visual, OBJ | 0.2 | 0.4 | 2.2 | 0.3&nbsp;ms | 2.8 | 1.7 | 0.3 | 0.2 | 7.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Examples.kicad_pcb` |
|---|---|
| Folder | circuits / DiodeLogicBoards / Examples |
| Complexity | 57&nbsp;/&nbsp;1000 (size&nbsp;57, features&nbsp;0) |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 41, 0, 0 |
| Triangles,&nbsp;simulation | 446,392 in 31 parts |
| Note | mostly unrouted |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">264&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">48&nbsp;MB</td><td align="right">314&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">22&nbsp;MB</td><td align="right">262&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">45&nbsp;MB</td><td align="right">340&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.6&nbsp;MB</td><td align="right">303&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">25&nbsp;MB</td><td align="right">301&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.12 PROM

![PROM: stages 4 and 6 take 59% to 85% of a run. Simulation, GLB takes 20 s. Simulation, STEP takes 25 s. Simulation, STL takes 21 s. Simulation, OBJ takes 29 s. Visual, GLB takes 23 s. Visual, OBJ takes 29 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_PROM.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.8 | 8.4 | 1&nbsp;ms | 8.7 | 0.3 | 0.7 | 0.2 | 20.5 |
| Simulation, STEP | 0.4 | 1.9 | 8.7 | 0.9&nbsp;ms | 8.4 | 4.7 | 0.7 | 0.2 | 25.1 |
| Simulation, STL | 0.4 | 1.8 | 8.5 | 0.8&nbsp;ms | 8.5 | 0.7 | 0.7 | 0.2 | 20.7 |
| Simulation, OBJ | 0.4 | 1.7 | 8.3 | 1&nbsp;ms | 8.9 | 8.7 | 0.7 | 0.2 | 29.0 |
| Visual, GLB | 0.4 | 1.7 | 8.5 | 1&nbsp;ms | 11.2 | 0.2 | 1.0 | 0.2 | 23.2 |
| Visual, OBJ | 0.5 | 1.7 | 8.4 | 1.0&nbsp;ms | 11.2 | 5.0 | 1.6 | 0.2 | 28.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `PROM.kicad_pcb` |
|---|---|
| Folder | circuits / DiodeLogicBoards / PROM |
| Complexity | 71&nbsp;/&nbsp;1000 (size&nbsp;71, features&nbsp;0) |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 145, 0, 0 |
| Triangles,&nbsp;simulation | 2,224,624 in 179 parts |
| Note | mostly unrouted |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">65&nbsp;MB</td><td align="right">720&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">243&nbsp;MB</td><td align="right">920&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">111&nbsp;MB</td><td align="right">713&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">232&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">41&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">123&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.13 h4n2rs485

![h4n2rs485: stages 4 and 6 take 50% to 78% of a run. Simulation, GLB takes 2.9 s. Simulation, STEP takes 4.1 s. Simulation, STL takes 3.0 s. Simulation, OBJ takes 4.4 s. Visual, GLB takes 3.5 s. Visual, OBJ takes 4.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_h4n2rs485.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 98&nbsp;ms | 0.3 | 1.2 | 0.3&nbsp;ms | 0.9 | 41&nbsp;ms | 0.1 | 0.2 | 2.9 |
| Simulation, STEP | 0.1 | 0.3 | 1.3 | 0.2&nbsp;ms | 0.9 | 1.1 | 0.2 | 0.2 | 4.1 |
| Simulation, STL | 97&nbsp;ms | 0.3 | 1.2 | 0.3&nbsp;ms | 1.0 | 61&nbsp;ms | 0.1 | 0.2 | 3.0 |
| Simulation, OBJ | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 1.0 | 1.4 | 0.2 | 0.2 | 4.4 |
| Visual, GLB | 97&nbsp;ms | 0.3 | 1.3 | 0.2&nbsp;ms | 1.5 | 19&nbsp;ms | 0.2 | 0.2 | 3.5 |
| Visual, OBJ | 0.1 | 0.3 | 1.2 | 0.2&nbsp;ms | 1.6 | 0.7 | 0.2 | 0.2 | 4.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `h4n2rs485.kicad_pcb` |
|---|---|
| Folder | circuits / h4n2rs485 |
| Complexity | 58&nbsp;/&nbsp;1000 (size&nbsp;48, features&nbsp;10) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 17, 0, 0 |
| Triangles,&nbsp;simulation | 277,192 in 40 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.4&nbsp;MB</td><td align="right">226&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">41&nbsp;MB</td><td align="right">250&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">228&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">28&nbsp;MB</td><td align="right">245&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.4&nbsp;MB</td><td align="right">206&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">13&nbsp;MB</td><td align="right">199&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.14 Analog Controller

![Analog Controller: stages 4 and 6 take 55% to 83% of a run. Simulation, GLB takes 6.5 s. Simulation, STEP takes 8.5 s. Simulation, STL takes 6.8 s. Simulation, OBJ takes 9.6 s. Visual, GLB takes 9.2 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Analog-Controller.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 2.9 | 0.4&nbsp;ms | 2.2 | 0.1 | 0.3 | 0.2 | 6.5 |
| Simulation, STEP | 0.2 | 0.6 | 3.1 | 0.4&nbsp;ms | 2.3 | 1.8 | 0.3 | 0.2 | 8.5 |
| Simulation, STL | 0.2 | 0.6 | 3.0 | 0.8&nbsp;ms | 2.3 | 0.2 | 0.4 | 0.2 | 6.8 |
| Simulation, OBJ | 0.2 | 0.6 | 3.0 | 0.2&nbsp;ms | 2.3 | 3.1 | 0.3 | 0.2 | 9.6 |
| Visual, GLB | 0.2 | 0.6 | 3.2 | 0.3&nbsp;ms | 4.4 | 51&nbsp;ms | 0.5 | 0.2 | 9.2 |
| Visual, OBJ | 0.2 | 0.6 | 3.0 | 0.4&nbsp;ms | 4.3 | 1.7 | 0.7 | 0.2 | 10.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Analog Controller.kicad_pcb` |
|---|---|
| Folder | circuits / HelperBoards / Controller / Analog Controller |
| Complexity | 179&nbsp;/&nbsp;1000 (size&nbsp;154, features&nbsp;25) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 42, 313, 13 |
| Triangles,&nbsp;simulation | 784,554 in 68 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">374&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">108&nbsp;MB</td><td align="right">452&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">39&nbsp;MB</td><td align="right">369&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">78&nbsp;MB</td><td align="right">560&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">452&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">46&nbsp;MB</td><td align="right">452&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.15 Analog Converter Backplane

![Analog Converter Backplane: stages 4 and 6 take 53% to 80% of a run. Simulation, GLB takes 3.0 s. Simulation, STEP takes 4.2 s. Simulation, STL takes 3.2 s. Simulation, OBJ takes 4.1 s. Visual, GLB takes 3.7 s. Visual, OBJ takes 4.2 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Analog-Converter-Backplane.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 85&nbsp;ms | 0.2 | 1.2 | 0.4&nbsp;ms | 1.1 | 55&nbsp;ms | 0.2 | 0.2 | 3.0 |
| Simulation, STEP | 95&nbsp;ms | 0.2 | 1.2 | 0.4&nbsp;ms | 1.2 | 1.2 | 0.2 | 0.2 | 4.2 |
| Simulation, STL | 0.1 | 0.2 | 1.3 | 0.3&nbsp;ms | 1.2 | 91&nbsp;ms | 0.1 | 0.2 | 3.2 |
| Simulation, OBJ | 94&nbsp;ms | 0.2 | 1.2 | 0.3&nbsp;ms | 1.0 | 1.3 | 0.2 | 0.2 | 4.1 |
| Visual, GLB | 0.1 | 0.2 | 1.2 | 0.6&nbsp;ms | 1.7 | 25&nbsp;ms | 0.2 | 0.2 | 3.7 |
| Visual, OBJ | 0.1 | 0.2 | 1.1 | 0.3&nbsp;ms | 1.7 | 0.7 | 0.2 | 0.3 | 4.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Analog Converter Backplane.kicad_pcb` |
|---|---|
| Folder | circuits / HelperBoards / Controller / Analog Converter Backplane / Analog Converter Backplane |
| Complexity | 138&nbsp;/&nbsp;1000 (size&nbsp;123, features&nbsp;15) |
| KESE&nbsp;features | through vias |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 8, 144, 3 |
| Triangles,&nbsp;simulation | 276,700 in 35 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">8.9&nbsp;MB</td><td align="right">220&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">34&nbsp;MB</td><td align="right">253&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">14&nbsp;MB</td><td align="right">221&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">27&nbsp;MB</td><td align="right">235&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.0&nbsp;MB</td><td align="right">226&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">15&nbsp;MB</td><td align="right">226&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.16 Analog Converter

![Analog Converter: stages 4 and 6 take 49% to 83% of a run. Simulation, GLB takes 4.0 s. Simulation, STEP takes 5.2 s. Simulation, STL takes 3.9 s. Simulation, OBJ takes 6.0 s. Visual, GLB takes 5.4 s. Visual, OBJ takes 6.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Analog-Converter.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.7 | 0.2&nbsp;ms | 1.5 | 64&nbsp;ms | 0.2 | 0.2 | 4.0 |
| Simulation, STEP | 0.1 | 0.3 | 1.6 | 0.2&nbsp;ms | 1.4 | 1.4 | 0.2 | 0.2 | 5.2 |
| Simulation, STL | 0.1 | 0.3 | 1.6 | 0.2&nbsp;ms | 1.4 | 88&nbsp;ms | 0.2 | 0.2 | 3.9 |
| Simulation, OBJ | 0.1 | 0.3 | 1.6 | 0.3&nbsp;ms | 1.3 | 2.2 | 0.3 | 0.2 | 6.0 |
| Visual, GLB | 0.1 | 0.3 | 1.6 | 0.2&nbsp;ms | 2.9 | 35&nbsp;ms | 0.2 | 0.2 | 5.4 |
| Visual, OBJ | 0.1 | 0.3 | 1.6 | 0.2&nbsp;ms | 3.0 | 1.2 | 0.2 | 0.2 | 6.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Analog Converter.kicad_pcb` |
|---|---|
| Folder | circuits / HelperBoards / Controller / Analog Converter / Analog Converter |
| Complexity | 161&nbsp;/&nbsp;1000 (size&nbsp;131, features&nbsp;30) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 17, 161, 0 |
| Triangles,&nbsp;simulation | 402,410 in 34 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">257&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">59&nbsp;MB</td><td align="right">304&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">20&nbsp;MB</td><td align="right">264&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">40&nbsp;MB</td><td align="right">310&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.9&nbsp;MB</td><td align="right">278&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">23&nbsp;MB</td><td align="right">280&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.17 Wave Form Generator Amplifier

![Wave Form Generator Amplifier: stages 4 and 6 take 47% to 85% of a run. Simulation, GLB takes 5.8 s. Simulation, STEP takes 7.2 s. Simulation, STL takes 5.6 s. Simulation, OBJ takes 8.9 s. Visual, GLB takes 8.5 s. Visual, OBJ takes 10 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_Wave-Form-Generator-Amplifier.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 2.4 | 0.5&nbsp;ms | 1.9 | 91&nbsp;ms | 0.3 | 0.3 | 5.8 |
| Simulation, STEP | 0.2 | 0.5 | 2.3 | 0.4&nbsp;ms | 1.8 | 1.8 | 0.3 | 0.2 | 7.2 |
| Simulation, STL | 0.2 | 0.4 | 2.5 | 0.2&nbsp;ms | 1.8 | 0.1 | 0.4 | 0.2 | 5.6 |
| Simulation, OBJ | 0.3 | 0.4 | 2.3 | 0.2&nbsp;ms | 1.8 | 3.4 | 0.3 | 0.3 | 8.9 |
| Visual, GLB | 0.2 | 0.4 | 2.4 | 0.3&nbsp;ms | 4.7 | 52&nbsp;ms | 0.4 | 0.2 | 8.5 |
| Visual, OBJ | 0.2 | 0.4 | 2.3 | 0.4&nbsp;ms | 4.6 | 1.9 | 0.4 | 0.2 | 10.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `Wave Form Generator Amplifier.kicad_pcb` |
|---|---|
| Folder | circuits / HelperBoards / Wave Form Generator Amplifier |
| Complexity | 169&nbsp;/&nbsp;1000 (size&nbsp;139, features&nbsp;30) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 22, 223, 0 |
| Triangles,&nbsp;simulation | 532,854 in 33 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">330&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">86&nbsp;MB</td><td align="right">354&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">27&nbsp;MB</td><td align="right">344&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">53&nbsp;MB</td><td align="right">393&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">355&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">32&nbsp;MB</td><td align="right">354&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.18 MyIOShield

![MyIOShield: stages 4 and 6 take 52% to 80% of a run. Simulation, GLB takes 4.4 s. Simulation, STEP takes 5.8 s. Simulation, STL takes 4.5 s. Simulation, OBJ takes 6.6 s. Visual, GLB takes 5.8 s. Visual, OBJ takes 6.9 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_MyIOShield.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 2.1 | 0.5&nbsp;ms | 1.3 | 81&nbsp;ms | 0.2 | 0.2 | 4.4 |
| Simulation, STEP | 0.1 | 0.4 | 2.0 | 0.4&nbsp;ms | 1.3 | 1.5 | 0.3 | 0.2 | 5.8 |
| Simulation, STL | 0.1 | 0.4 | 2.0 | 0.6&nbsp;ms | 1.3 | 0.1 | 0.3 | 0.2 | 4.5 |
| Simulation, OBJ | 0.1 | 0.4 | 2.1 | 0.4&nbsp;ms | 1.3 | 2.2 | 0.2 | 0.2 | 6.6 |
| Visual, GLB | 0.1 | 0.3 | 2.0 | 0.4&nbsp;ms | 2.7 | 33&nbsp;ms | 0.4 | 0.2 | 5.8 |
| Visual, OBJ | 0.1 | 0.3 | 2.1 | 0.4&nbsp;ms | 2.5 | 1.2 | 0.4 | 0.2 | 6.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `MyIOShield.kicad_pcb` |
|---|---|
| Folder | circuits / MyIOShield |
| Complexity | 52&nbsp;/&nbsp;1000 (size&nbsp;52, features&nbsp;0) |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 24, 0, 0 |
| Triangles,&nbsp;simulation | 442,126 in 47 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">58&nbsp;MB</td><td align="right">306&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">22&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">45&nbsp;MB</td><td align="right">352&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.8&nbsp;MB</td><td align="right">292&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">23&nbsp;MB</td><td align="right">315&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.19 16bit Banked Switches

![16bit Banked Switches: stages 4 and 6 take 55% to 81% of a run. Simulation, GLB takes 5.2 s. Simulation, STEP takes 6.2 s. Simulation, STL takes 5.0 s. Simulation, OBJ takes 7.3 s. Visual, GLB takes 6.1 s. Visual, OBJ takes 7.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_16bit-Banked-Switches.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.4 | 2.6 | 0.3&nbsp;ms | 1.7 | 76&nbsp;ms | 0.2 | 0.2 | 5.2 |
| Simulation, STEP | 0.1 | 0.4 | 2.3 | 0.3&nbsp;ms | 1.5 | 1.4 | 0.2 | 0.2 | 6.2 |
| Simulation, STL | 0.1 | 0.4 | 2.4 | 0.5&nbsp;ms | 1.5 | 95&nbsp;ms | 0.2 | 0.2 | 5.0 |
| Simulation, OBJ | 0.1 | 0.4 | 2.4 | 0.3&nbsp;ms | 1.6 | 2.3 | 0.2 | 0.2 | 7.3 |
| Visual, GLB | 0.2 | 0.4 | 2.4 | 0.3&nbsp;ms | 2.6 | 32&nbsp;ms | 0.3 | 0.2 | 6.1 |
| Visual, OBJ | 0.2 | 0.4 | 2.3 | 0.5&nbsp;ms | 2.5 | 1.1 | 0.3 | 0.2 | 7.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `16bit Banked Switches.kicad_pcb` |
|---|---|
| Folder | circuits / Pmod16bitBanked |
| Complexity | 147&nbsp;/&nbsp;1000 (size&nbsp;137, features&nbsp;10) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 24, 182, 0 |
| Triangles,&nbsp;simulation | 448,056 in 40 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">266&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">70&nbsp;MB</td><td align="right">310&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">22&nbsp;MB</td><td align="right">287&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">46&nbsp;MB</td><td align="right">362&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.7&nbsp;MB</td><td align="right">267&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">23&nbsp;MB</td><td align="right">278&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.20 SimpleClock

![SimpleClock: stages 4 and 6 take 54% to 79% of a run. Simulation, GLB takes 4.3 s. Simulation, STEP takes 5.7 s. Simulation, STL takes 4.3 s. Simulation, OBJ takes 6.2 s. Visual, GLB takes 5.0 s. Visual, OBJ takes 5.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/embeddedbakery_SimpleClock.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.8 | 0.3&nbsp;ms | 1.6 | 63&nbsp;ms | 0.2 | 0.2 | 4.3 |
| Simulation, STEP | 0.1 | 0.3 | 1.8 | 0.6&nbsp;ms | 1.6 | 1.4 | 0.2 | 0.2 | 5.7 |
| Simulation, STL | 0.1 | 0.4 | 1.7 | 0.4&nbsp;ms | 1.6 | 0.1 | 0.2 | 0.2 | 4.3 |
| Simulation, OBJ | 0.1 | 0.3 | 1.7 | 0.5&nbsp;ms | 1.6 | 1.9 | 0.2 | 0.3 | 6.2 |
| Visual, GLB | 0.2 | 0.4 | 1.8 | 0.4&nbsp;ms | 2.2 | 31&nbsp;ms | 0.3 | 0.2 | 5.0 |
| Visual, OBJ | 0.1 | 0.3 | 1.7 | 0.3&nbsp;ms | 2.2 | 1.0 | 0.3 | 0.2 | 5.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mwwhited/embeddedbakery](https://github.com/mwwhited/embeddedbakery)<br>Board: `SimpleClock.kicad_pcb` |
|---|---|
| Folder | circuits / SimpleClock / SimpleClock |
| Complexity | 54&nbsp;/&nbsp;1000 (size&nbsp;54, features&nbsp;0) |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 31, 0, 0 |
| Triangles,&nbsp;simulation | 454,624 in 46 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">264&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">46&nbsp;MB</td><td align="right">309&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">23&nbsp;MB</td><td align="right">264&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">45&nbsp;MB</td><td align="right">351&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.4&nbsp;MB</td><td align="right">305&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">25&nbsp;MB</td><td align="right">304&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.21 LimeSDR_Sony

![LimeSDR_Sony: stages 4 and 6 take 50% to 81% of a run. Simulation, GLB takes 43 s. Simulation, STEP takes 51 s. Simulation, STL takes 43 s. Simulation, OBJ takes 64 s. Visual, GLB takes 64 s. Visual, OBJ takes 80 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/front-end-modules_LimeSDR-Sony.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 5.3 | 14.9 | 2&nbsp;ms | 18.5 | 0.8 | 1.9 | 0.3 | 42.5 |
| Simulation, STEP | 0.8 | 5.5 | 14.8 | 2&nbsp;ms | 18.5 | 9.5 | 1.9 | 0.3 | 51.4 |
| Simulation, STL | 1.0 | 5.4 | 14.4 | 1&nbsp;ms | 18.2 | 1.9 | 1.9 | 0.3 | 43.1 |
| Simulation, OBJ | 0.8 | 5.2 | 14.0 | 1&nbsp;ms | 18.2 | 24.0 | 2.0 | 0.3 | 64.5 |
| Visual, GLB | 0.8 | 5.3 | 14.0 | 0.6&nbsp;ms | 38.0 | 0.5 | 5.4 | 0.3 | 64.2 |
| Visual, OBJ | 0.8 | 5.4 | 14.5 | 2&nbsp;ms | 38.9 | 14.0 | 5.6 | 0.3 | 79.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/front-end-modules](https://github.com/myriadrf/front-end-modules)<br>Board: `LimeSDR_Sony.kicad_pcb` |
|---|---|
| Folder | LimeSDR_PA_LNA / hardware / v1r3 / KiCAD |
| Complexity | 319&nbsp;/&nbsp;1000 (size&nbsp;274, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 244, 2,265, 237 |
| Triangles,&nbsp;simulation | 4,502,856 in 159 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">155&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">559&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">225&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">487&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">89&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">282&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.22 lc-b3-mpa

![lc-b3-mpa: stages 4 and 6 take 53% to 81% of a run. Simulation, GLB takes 2.5 s. Simulation, STEP takes 3.5 s. Simulation, STL takes 2.7 s. Simulation, OBJ takes 3.4 s. Visual, GLB takes 3.1 s. Visual, OBJ takes 3.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lc-b3-mpa_hardware-0v1_lc-b3-mpa.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 95&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 1.1 | 34&nbsp;ms | 0.1 | 0.2 | 2.5 |
| Simulation, STEP | 97&nbsp;ms | 0.2 | 0.8 | 0.2&nbsp;ms | 1.0 | 1.1 | 0.1 | 0.2 | 3.5 |
| Simulation, STL | 0.1 | 0.2 | 0.9 | 0.1&nbsp;ms | 1.1 | 57&nbsp;ms | 0.1 | 0.3 | 2.7 |
| Simulation, OBJ | 96&nbsp;ms | 0.1 | 0.8 | 0.1&nbsp;ms | 1.0 | 1.0 | 0.1 | 0.2 | 3.4 |
| Visual, GLB | 0.1 | 0.2 | 0.9 | 0.1&nbsp;ms | 1.7 | 17&nbsp;ms | 97&nbsp;ms | 0.2 | 3.1 |
| Visual, OBJ | 97&nbsp;ms | 0.2 | 0.9 | 0.1&nbsp;ms | 1.6 | 0.4 | 81&nbsp;ms | 0.2 | 3.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/lc-b3-mpa](https://github.com/myriadrf/lc-b3-mpa)<br>Board: `lc-b3-mpa.kicad_pcb` |
|---|---|
| Folder | hardware / 0v1 |
| Complexity | 219&nbsp;/&nbsp;1000 (size&nbsp;149, features&nbsp;70) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>drill offsets, arc tracks,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20201220) |
| Parts,&nbsp;tracks,&nbsp;vias | 15, 8, 57 |
| Triangles,&nbsp;simulation | 213,914 in 19 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">7.0&nbsp;MB</td><td align="right">210&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">22&nbsp;MB</td><td align="right">236&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">11&nbsp;MB</td><td align="right">214&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">21&nbsp;MB</td><td align="right">232&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">2.8&nbsp;MB</td><td align="right">168&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">7.9&nbsp;MB</td><td align="right">168&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.23 lc-b3-mpa

![lc-b3-mpa: stages 4 and 6 take 55% to 81% of a run. Simulation, GLB takes 2.4 s. Simulation, STEP takes 3.3 s. Simulation, STL takes 2.4 s. Simulation, OBJ takes 3.1 s. Visual, GLB takes 2.8 s. Visual, OBJ takes 3.2 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lc-b3-mpa_hardware-1v0_lc-b3-mpa.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 88&nbsp;ms | 0.1 | 0.8 | 0.1&nbsp;ms | 1.0 | 32&nbsp;ms | 0.1 | 0.2 | 2.4 |
| Simulation, STEP | 96&nbsp;ms | 0.2 | 0.8 | 0.1&nbsp;ms | 1.0 | 0.9 | 92&nbsp;ms | 0.2 | 3.3 |
| Simulation, STL | 96&nbsp;ms | 0.1 | 0.8 | 0.1&nbsp;ms | 0.9 | 57&nbsp;ms | 0.1 | 0.2 | 2.4 |
| Simulation, OBJ | 95&nbsp;ms | 0.1 | 0.8 | 0.1&nbsp;ms | 1.0 | 0.8 | 97&nbsp;ms | 0.3 | 3.1 |
| Visual, GLB | 97&nbsp;ms | 0.2 | 0.8 | 0.2&nbsp;ms | 1.5 | 13&nbsp;ms | 84&nbsp;ms | 0.2 | 2.8 |
| Visual, OBJ | 90&nbsp;ms | 0.1 | 0.8 | 0.1&nbsp;ms | 1.6 | 0.3 | 88&nbsp;ms | 0.2 | 3.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/lc-b3-mpa](https://github.com/myriadrf/lc-b3-mpa)<br>Board: `lc-b3-mpa.kicad_pcb` |
|---|---|
| Folder | hardware / 1v0 |
| Complexity | 209&nbsp;/&nbsp;1000 (size&nbsp;149, features&nbsp;60) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 15, 10, 57 |
| Triangles,&nbsp;simulation | 217,420 in 19 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">7.1&nbsp;MB</td><td align="right">219&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">23&nbsp;MB</td><td align="right">239&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">11&nbsp;MB</td><td align="right">217&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">21&nbsp;MB</td><td align="right">233&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">2.9&nbsp;MB</td><td align="right">170&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">8.2&nbsp;MB</td><td align="right">168&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.24 CSAD10

![CSAD10: stages 4 and 6 take 52% to 81% of a run. Simulation, GLB takes 6.1 s. Simulation, STEP takes 8.9 s. Simulation, STL takes 6.6 s. Simulation, OBJ takes 9.2 s. Visual, GLB takes 9.0 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lc-clock_CSAD10.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.6 | 2.0 | 0.5&nbsp;ms | 2.6 | 88&nbsp;ms | 0.3 | 0.2 | 6.1 |
| Simulation, STEP | 0.3 | 0.6 | 2.1 | 0.3&nbsp;ms | 2.9 | 2.5 | 0.3 | 0.2 | 8.9 |
| Simulation, STL | 0.3 | 0.6 | 2.1 | 0.2&nbsp;ms | 3.0 | 0.2 | 0.3 | 0.2 | 6.6 |
| Simulation, OBJ | 0.3 | 0.6 | 2.1 | 0.3&nbsp;ms | 2.7 | 3.1 | 0.3 | 0.2 | 9.2 |
| Visual, GLB | 0.3 | 0.6 | 2.3 | 0.3&nbsp;ms | 4.9 | 80&nbsp;ms | 0.5 | 0.2 | 9.0 |
| Visual, OBJ | 0.3 | 0.6 | 2.0 | 0.2&nbsp;ms | 4.5 | 2.5 | 0.7 | 0.2 | 10.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/lc-clock](https://github.com/myriadrf/lc-clock)<br>Board: `CSAD10.kicad_pcb` |
|---|---|
| Folder | csad10 |
| Complexity | 340&nbsp;/&nbsp;1000 (size&nbsp;225, features&nbsp;115) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 60, 440, 81 |
| Triangles,&nbsp;simulation | 595,804 in 67 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">355&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">91&nbsp;MB</td><td align="right">415&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">30&nbsp;MB</td><td align="right">357&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">60&nbsp;MB</td><td align="right">415&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">424&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">48&nbsp;MB</td><td align="right">480&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.25 CSAD2

![CSAD2: stages 4 and 6 take 47% to 76% of a run. Simulation, GLB takes 3.0 s. Simulation, STEP takes 4.1 s. Simulation, STL takes 2.9 s. Simulation, OBJ takes 4.6 s. Visual, GLB takes 3.9 s. Visual, OBJ takes 5.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lc-clock_CSAD2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.3 | 0.9 | 0.2&nbsp;ms | 1.2 | 42&nbsp;ms | 0.1 | 0.3 | 3.0 |
| Simulation, STEP | 0.2 | 0.3 | 0.8 | 0.2&nbsp;ms | 1.2 | 1.2 | 0.1 | 0.2 | 4.1 |
| Simulation, STL | 0.2 | 0.3 | 0.8 | 0.2&nbsp;ms | 1.2 | 74&nbsp;ms | 0.1 | 0.2 | 2.9 |
| Simulation, OBJ | 0.2 | 0.3 | 1.0 | 0.2&nbsp;ms | 1.2 | 1.6 | 0.2 | 0.2 | 4.6 |
| Visual, GLB | 0.2 | 0.3 | 0.9 | 0.2&nbsp;ms | 2.1 | 32&nbsp;ms | 0.3 | 0.2 | 3.9 |
| Visual, OBJ | 0.2 | 0.3 | 0.9 | 0.3&nbsp;ms | 2.2 | 1.1 | 0.2 | 0.2 | 5.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/lc-clock](https://github.com/myriadrf/lc-clock)<br>Board: `CSAD2.kicad_pcb` |
|---|---|
| Folder | csad2 |
| Complexity | 278&nbsp;/&nbsp;1000 (size&nbsp;163, features&nbsp;115) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 37, 121, 43 |
| Triangles,&nbsp;simulation | 293,046 in 44 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">10&nbsp;MB</td><td align="right">245&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">44&nbsp;MB</td><td align="right">284&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">15&nbsp;MB</td><td align="right">242&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">29&nbsp;MB</td><td align="right">261&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.4&nbsp;MB</td><td align="right">258&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">252&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.26 B3LPD

![B3LPD: stages 4 and 6 take 45% to 74% of a run. Simulation, GLB takes 2.4 s. Simulation, STEP takes 3.2 s. Simulation, STL takes 2.5 s. Simulation, OBJ takes 3.5 s. Visual, GLB takes 2.8 s. Visual, OBJ takes 3.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lc-filters_B3LPD.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 0.6 | 0.1&nbsp;ms | 1.1 | 34&nbsp;ms | 86&nbsp;ms | 0.2 | 2.4 |
| Simulation, STEP | 0.1 | 0.3 | 0.6 | 0.2&nbsp;ms | 1.1 | 0.8 | 82&nbsp;ms | 0.2 | 3.2 |
| Simulation, STL | 0.1 | 0.3 | 0.6 | 0.2&nbsp;ms | 1.1 | 58&nbsp;ms | 89&nbsp;ms | 0.2 | 2.5 |
| Simulation, OBJ | 0.1 | 0.3 | 0.6 | 0.2&nbsp;ms | 1.0 | 1.2 | 89&nbsp;ms | 0.2 | 3.5 |
| Visual, GLB | 0.1 | 0.3 | 0.6 | 0.1&nbsp;ms | 1.5 | 21&nbsp;ms | 0.1 | 0.2 | 2.8 |
| Visual, OBJ | 0.1 | 0.3 | 0.6 | 0.2&nbsp;ms | 1.5 | 0.7 | 0.1 | 0.2 | 3.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/lc-filters](https://github.com/myriadrf/lc-filters)<br>Board: `B3LPD.kicad_pcb` |
|---|---|
| Folder | b3lpd |
| Complexity | 240&nbsp;/&nbsp;1000 (size&nbsp;150, features&nbsp;90) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 7, 22, 96 |
| Triangles,&nbsp;simulation | 214,242 in 20 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">7.2&nbsp;MB</td><td align="right">233&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">13&nbsp;MB</td><td align="right">246&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">11&nbsp;MB</td><td align="right">233&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">21&nbsp;MB</td><td align="right">233&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">4.3&nbsp;MB</td><td align="right">192&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">12&nbsp;MB</td><td align="right">191&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.27 LC_RFE-RevA1

![LC_RFE-RevA1: stages 4 and 6 take 53% to 82% of a run. Simulation, GLB takes 42 s. Simulation, STEP takes 51 s. Simulation, STL takes 45 s. Simulation, OBJ takes 66 s. Visual, GLB takes 62 s. Visual, OBJ takes 72 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lc-rfe_LC-RFE-RevA1.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 5.2 | 16.9 | 2&nbsp;ms | 16.4 | 0.7 | 1.6 | 0.3 | 42.2 |
| Simulation, STEP | 0.9 | 5.0 | 17.3 | 2&nbsp;ms | 17.1 | 8.5 | 1.8 | 0.4 | 51.0 |
| Simulation, STL | 1.1 | 5.4 | 17.4 | 2&nbsp;ms | 16.9 | 2.1 | 1.8 | 0.3 | 44.9 |
| Simulation, OBJ | 0.9 | 5.6 | 17.4 | 2&nbsp;ms | 17.5 | 22.7 | 1.7 | 0.4 | 66.2 |
| Visual, GLB | 0.9 | 5.6 | 17.1 | 2&nbsp;ms | 33.6 | 0.4 | 3.9 | 0.3 | 61.9 |
| Visual, OBJ | 0.9 | 5.2 | 16.5 | 1&nbsp;ms | 32.4 | 12.5 | 4.0 | 0.3 | 71.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/lc-rfe](https://github.com/myriadrf/lc-rfe)<br>Board: `LC_RFE-RevA1.kicad_pcb` |
|---|---|
| Folder | revisions / LC_RFE-RevA1 |
| Complexity | 399&nbsp;/&nbsp;1000 (size&nbsp;284, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 228, 1,247, 1,393 |
| Triangles,&nbsp;simulation | 4,623,948 in 206 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">154&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">422&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">231&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">482&nbsp;MB</td><td align="right">3.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">89&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">283&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.28 LC_RFE-RevA2

![LC_RFE-RevA2: stages 4 and 6 take 56% to 82% of a run. Simulation, GLB takes 73 s. Simulation, STEP takes 79 s. Simulation, STL takes 70 s. Simulation, OBJ takes 2 min. Visual, GLB takes 96 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lc-rfe_LC-RFE-RevA2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.4 | 8.1 | 27.0 | 2&nbsp;ms | 31.8 | 1.2 | 2.5 | 0.4 | 72.6 |
| Simulation, STEP | 1.4 | 8.4 | 26.6 | 2&nbsp;ms | 29.6 | 10.7 | 2.2 | 0.3 | 79.2 |
| Simulation, STL | 1.2 | 8.0 | 25.8 | 3&nbsp;ms | 29.5 | 2.4 | 2.5 | 0.4 | 69.8 |
| Simulation, OBJ | 1.1 | 8.0 | 25.3 | 3&nbsp;ms | 30.3 | 32.2 | 2.6 | 0.4 | 99.9 |
| Visual, GLB | 1.3 | 8.1 | 26.0 | 3&nbsp;ms | 52.7 | 0.6 | 7.2 | 0.4 | 96.4 |
| Visual, OBJ | 1.3 | 7.9 | 26.1 | 2&nbsp;ms | 54.4 | 17.7 | 7.4 | 0.3 | 115.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/lc-rfe](https://github.com/myriadrf/lc-rfe)<br>Board: `LC_RFE-RevA2.kicad_pcb` |
|---|---|
| Folder | revisions / LC_RFE-RevA2 |
| Complexity | 406&nbsp;/&nbsp;1000 (size&nbsp;291, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 256, 1,307, 2,201 |
| Triangles,&nbsp;simulation | 6,245,326 in 210 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">208&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">521&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">312&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">653&nbsp;MB</td><td align="right">3.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">122&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">391&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.29 LC-RFE-Mini-RevA1

![LC-RFE-Mini-RevA1: stages 4 and 6 take 54% to 83% of a run. Simulation, GLB takes 37 s. Simulation, STEP takes 47 s. Simulation, STL takes 38 s. Simulation, OBJ takes 51 s. Visual, GLB takes 52 s. Visual, OBJ takes 58 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lc-rfe-mini_LC-RFE-Mini-RevA1.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 4.2 | 15.0 | 0.5&nbsp;ms | 14.4 | 0.5 | 1.7 | 0.3 | 37.0 |
| Simulation, STEP | 1.1 | 5.3 | 17.4 | 1.0&nbsp;ms | 15.0 | 6.7 | 1.6 | 0.4 | 47.5 |
| Simulation, STL | 0.8 | 4.6 | 14.8 | 1&nbsp;ms | 14.9 | 1.0 | 1.6 | 0.3 | 38.1 |
| Simulation, OBJ | 0.7 | 3.9 | 14.0 | 0.7&nbsp;ms | 13.8 | 17.4 | 1.3 | 0.3 | 51.3 |
| Visual, GLB | 0.7 | 3.7 | 14.0 | 1.0&nbsp;ms | 28.9 | 0.4 | 4.0 | 0.2 | 52.0 |
| Visual, OBJ | 0.8 | 4.0 | 14.1 | 0.9&nbsp;ms | 24.3 | 11.7 | 2.9 | 0.3 | 58.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/lc-rfe-mini](https://github.com/myriadrf/lc-rfe-mini)<br>Board: `LC-RFE-Mini-RevA1.kicad_pcb` |
|---|---|
| Folder | revisions / LC-RFE-Mini-RevA1 |
| Complexity | 370&nbsp;/&nbsp;1000 (size&nbsp;255, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 98, 458, 910 |
| Triangles,&nbsp;simulation | 3,268,520 in 110 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">110&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">319&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">163&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">339&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">64&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">199&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.30 LC-RFE-Mini-RevA2

![LC-RFE-Mini-RevA2: stages 4 and 6 take 53% to 83% of a run. Simulation, GLB takes 15 s. Simulation, STEP takes 19 s. Simulation, STL takes 15 s. Simulation, OBJ takes 22 s. Visual, GLB takes 21 s. Visual, OBJ takes 26 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/lc-rfe-mini_LC-RFE-Mini-RevA2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.5 | 6.1 | 0.3&nbsp;ms | 6.1 | 0.3 | 0.7 | 0.2 | 15.3 |
| Simulation, STEP | 0.4 | 1.4 | 6.3 | 0.2&nbsp;ms | 5.9 | 4.0 | 0.7 | 0.2 | 19.1 |
| Simulation, STL | 0.4 | 1.4 | 6.0 | 0.3&nbsp;ms | 5.8 | 0.5 | 0.7 | 0.2 | 15.0 |
| Simulation, OBJ | 0.4 | 1.5 | 5.9 | 0.3&nbsp;ms | 5.7 | 7.6 | 0.8 | 0.2 | 22.2 |
| Visual, GLB | 0.4 | 1.5 | 6.0 | 0.3&nbsp;ms | 11.7 | 0.2 | 1.2 | 0.2 | 21.3 |
| Visual, OBJ | 0.4 | 1.5 | 6.2 | 0.3&nbsp;ms | 11.5 | 4.6 | 1.6 | 0.2 | 26.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/lc-rfe-mini](https://github.com/myriadrf/lc-rfe-mini)<br>Board: `LC-RFE-Mini-RevA2.kicad_pcb` |
|---|---|
| Folder | revisions / LC-RFE-Mini-RevA2 |
| Complexity | 355&nbsp;/&nbsp;1000 (size&nbsp;240, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 95, 396, 289 |
| Triangles,&nbsp;simulation | 1,923,076 in 108 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">65&nbsp;MB</td><td align="right">717&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">244&nbsp;MB</td><td align="right">821&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">96&nbsp;MB</td><td align="right">835&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">199&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">38&nbsp;MB</td><td align="right">764&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">116&nbsp;MB</td><td align="right">866&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.31 Lime_RFE

![Lime_RFE: stages 4 and 6 take 67% to 88% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 4 min. Simulation, STL takes 3 min. Visual, GLB takes 6 min. Visual, OBJ takes 7 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LimeRFE_archived-0v3-hardware-KiCad_Lime-RFE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.4 | 20.3 | 84.9 | 4&nbsp;ms | 70.3 | 4.4 | 8.9 | 0.5 | 192.7 |
| Simulation, STEP | 3.4 | 19.9 | 83.0 | 2&nbsp;ms | 71.9 | 43.5 | 9.6 | 0.5 | 231.8 |
| Simulation, STL | 3.5 | 22.1 | 91.1 | 3&nbsp;ms | 74.9 | 7.9 | 10.0 | 0.6 | 210.0 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB | 3.4 | 21.2 | 90.4 | 3&nbsp;ms | 215.7 | 1.5 | 14.3 | 0.5 | 346.9 |
| Visual, OBJ | 3.5 | 21.2 | 87.9 | 3&nbsp;ms | 221.3 | 58.0 | 14.8 | 0.5 | 407.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LimeRFE](https://github.com/myriadrf/LimeRFE)<br>Board: `Lime_RFE.kicad_pcb` |
|---|---|
| Folder | archived / 0v3 / hardware / KiCad |
| Complexity | 325&nbsp;/&nbsp;1000 (size&nbsp;270, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 986, 8,840, 623 |
| Triangles,&nbsp;simulation | 18,078,138 in 810 parts |
| Verifier | Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">668&nbsp;MB</td><td align="right">4.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.6&nbsp;GB</td><td align="right">6.1&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">904&nbsp;MB</td><td align="right">4.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">320&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.0&nbsp;GB</td><td align="right">6.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.32 Lime_RFE_fab

![Lime_RFE_fab: stages 4 and 6 take 48% to 87% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 3 min. Simulation, STL takes 3 min. Simulation, OBJ takes 6 min. Visual, GLB takes 5 min. Visual, OBJ takes 6 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LimeRFE_Lime-RFE-fab.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.7 | 18.2 | 73.3 | 3&nbsp;ms | 63.0 | 3.8 | 8.2 | 0.5 | 169.8 |
| Simulation, STEP | 2.6 | 17.6 | 73.0 | 3&nbsp;ms | 62.9 | 37.6 | 8.2 | 0.5 | 202.5 |
| Simulation, STL | 2.9 | 18.4 | 74.3 | 3&nbsp;ms | 64.9 | 7.8 | 8.4 | 0.5 | 177.3 |
| Simulation, OBJ | 4.4 | 24.9 | 93.2 | 3&nbsp;ms | 79.3 | 143.3 | 10.8 | 1.1 | 357.0 |
| Visual, GLB | 2.9 | 18.7 | 74.9 | 3&nbsp;ms | 188.2 | 1.5 | 16.8 | 0.4 | 303.4 |
| Visual, OBJ | 2.7 | 17.9 | 72.9 | 4&nbsp;ms | 201.1 | 48.2 | 16.9 | 0.5 | 360.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LimeRFE](https://github.com/myriadrf/LimeRFE)<br>Board: `Lime_RFE_fab.kicad_pcb` |
|---|---|
| Folder | archived / 0v3 / hardware / KiCad |
| Complexity | 325&nbsp;/&nbsp;1000 (size&nbsp;270, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 986, 8,840, 623 |
| Triangles,&nbsp;simulation | 18,079,684 in 810 parts |
| Verifier | PASS in all six runs |
| Run&nbsp;again | Simulation, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">668&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.6&nbsp;GB</td><td align="right">5.8&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">904&nbsp;MB</td><td align="right">4.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">2.1&nbsp;GB</td><td align="right">12&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">320&nbsp;MB</td><td align="right">4.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.0&nbsp;GB</td><td align="right">6.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.33 Lime_RFE

![Lime_RFE: stages 4 and 6 take 9% to 10% of a run. Simulation, GLB takes 15 s. Simulation, STEP takes 15 s. Simulation, STL takes 15 s. Simulation, OBJ takes 15 s. Visual, GLB takes 15 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LimeRFE_archived-1v0-hardware-KiCAD_Lime-RFE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.4 | 9.2 | 1.4 | 1&nbsp;ms | 37&nbsp;ms | 2&nbsp;ms | 6&nbsp;ms | 0.3 | 15.3 |
| Simulation, STEP | 4.4 | 9.1 | 1.5 | 1&nbsp;ms | 36&nbsp;ms | 41&nbsp;ms | 7&nbsp;ms | 0.3 | 15.3 |
| Simulation, STL | 4.4 | 9.2 | 1.4 | 1&nbsp;ms | 37&nbsp;ms | 2&nbsp;ms | 6&nbsp;ms | 0.3 | 15.4 |
| Simulation, OBJ | 4.3 | 9.1 | 1.4 | 0.7&nbsp;ms | 38&nbsp;ms | 14&nbsp;ms | 6&nbsp;ms | 0.3 | 15.2 |
| Visual, GLB | 4.3 | 9.2 | 1.5 | 1&nbsp;ms | 93&nbsp;ms | 4&nbsp;ms | 12&nbsp;ms | 0.3 | 15.3 |
| Visual, OBJ | 4.6 | 9.3 | 1.5 | 1&nbsp;ms | 0.1 | 13&nbsp;ms | 15&nbsp;ms | 0.2 | 15.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LimeRFE](https://github.com/myriadrf/LimeRFE)<br>Board: `Lime_RFE.kicad_pcb` |
|---|---|
| Folder | archived / 1v0 / hardware / KiCAD |
| Complexity | 339&nbsp;/&nbsp;1000 (size&nbsp;274, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 1,278, 9,448, 585 |
| Triangles,&nbsp;simulation | 2,136 in 8 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">63&nbsp;kB</td><td align="right">478&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">381&nbsp;kB</td><td align="right">478&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">107&nbsp;kB</td><td align="right">479&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">216&nbsp;kB</td><td align="right">476&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">75&nbsp;kB</td><td align="right">479&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">194&nbsp;kB</td><td align="right">478&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.34 Lime_RFE

![Lime_RFE: stages 4 and 6 take 11% to 12% of a run. Simulation, GLB takes 15 s. Simulation, STEP takes 15 s. Simulation, STL takes 16 s. Simulation, OBJ takes 15 s. Visual, GLB takes 15 s. Visual, OBJ takes 15 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LimeRFE_archived-1v2-hardware-KiCAD_Lime-RFE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.3 | 8.9 | 1.6 | 1&nbsp;ms | 31&nbsp;ms | 2&nbsp;ms | 5&nbsp;ms | 0.2 | 15.1 |
| Simulation, STEP | 4.1 | 9.2 | 1.7 | 1&nbsp;ms | 31&nbsp;ms | 34&nbsp;ms | 7&nbsp;ms | 0.3 | 15.3 |
| Simulation, STL | 4.6 | 9.5 | 1.7 | 2&nbsp;ms | 31&nbsp;ms | 2&nbsp;ms | 5&nbsp;ms | 0.3 | 16.1 |
| Simulation, OBJ | 4.2 | 8.8 | 1.6 | 2&nbsp;ms | 33&nbsp;ms | 14&nbsp;ms | 5&nbsp;ms | 0.3 | 15.0 |
| Visual, GLB | 4.2 | 9.4 | 1.6 | 2&nbsp;ms | 96&nbsp;ms | 2&nbsp;ms | 14&nbsp;ms | 0.3 | 15.5 |
| Visual, OBJ | 4.0 | 8.8 | 1.7 | 1&nbsp;ms | 95&nbsp;ms | 12&nbsp;ms | 12&nbsp;ms | 0.3 | 14.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LimeRFE](https://github.com/myriadrf/LimeRFE)<br>Board: `Lime_RFE.kicad_pcb` |
|---|---|
| Folder | archived / 1v2 / hardware / KiCAD |
| Complexity | 340&nbsp;/&nbsp;1000 (size&nbsp;275, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 1,295, 10,180, 591 |
| Triangles,&nbsp;simulation | 2,136 in 8 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">63&nbsp;kB</td><td align="right">542&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">381&nbsp;kB</td><td align="right">542&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">107&nbsp;kB</td><td align="right">542&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">216&nbsp;kB</td><td align="right">542&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">75&nbsp;kB</td><td align="right">542&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">194&nbsp;kB</td><td align="right">542&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.35 Lime_RFE

![Lime_RFE: stages 4 and 6 take 10% to 12% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 13 s. Simulation, STL takes 12 s. Simulation, OBJ takes 13 s. Visual, GLB takes 13 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LimeRFE_hardware-1v31-KiCAD_Lime-RFE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.4 | 8.0 | 1.4 | 2&nbsp;ms | 27&nbsp;ms | 1&nbsp;ms | 6&nbsp;ms | 0.2 | 13.1 |
| Simulation, STEP | 3.5 | 7.7 | 1.3 | 2&nbsp;ms | 27&nbsp;ms | 49&nbsp;ms | 6&nbsp;ms | 0.3 | 12.9 |
| Simulation, STL | 3.4 | 7.4 | 1.3 | 1&nbsp;ms | 24&nbsp;ms | 1&nbsp;ms | 5&nbsp;ms | 0.3 | 12.3 |
| Simulation, OBJ | 3.3 | 7.5 | 1.4 | 2&nbsp;ms | 25&nbsp;ms | 8&nbsp;ms | 6&nbsp;ms | 0.3 | 12.5 |
| Visual, GLB | 3.4 | 7.6 | 1.2 | 1&nbsp;ms | 74&nbsp;ms | 2&nbsp;ms | 9&nbsp;ms | 0.3 | 12.7 |
| Visual, OBJ | 3.4 | 7.7 | 1.5 | 1&nbsp;ms | 83&nbsp;ms | 7&nbsp;ms | 9&nbsp;ms | 0.3 | 12.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LimeRFE](https://github.com/myriadrf/LimeRFE)<br>Board: `Lime_RFE.kicad_pcb` |
|---|---|
| Folder | hardware / 1v31 / KiCAD |
| Complexity | 341&nbsp;/&nbsp;1000 (size&nbsp;276, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 1,317, 10,728, 612 |
| Triangles,&nbsp;simulation | 1,736 in 8 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">51&nbsp;kB</td><td align="right">545&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">240&nbsp;kB</td><td align="right">546&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">87&nbsp;kB</td><td align="right">544&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">169&nbsp;kB</td><td align="right">548&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">52&nbsp;kB</td><td align="right">545&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">133&nbsp;kB</td><td align="right">545&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.36 FrontEnd_5G

![FrontEnd_5G: stages 4 and 6 take 67% to 83% of a run. Simulation, GLB takes 7 min. Simulation, STEP takes 9 min. Simulation, STL takes 8 min. Visual, GLB takes 12 min. Visual, OBJ takes 13 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LimeRFE-8001P_hardware-1v0-KiCAD_FrontEnd-5G.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 23.3 | 57.8 | 171.2 | 5&nbsp;ms | 157.3 | 6.5 | 25.0 | 1.2 | 442.2 |
| Simulation, STEP | 25.1 | 60.0 | 185.7 | 4&nbsp;ms | 176.8 | 67.2 | 25.0 | 1.2 | 541.0 |
| Simulation, STL | 26.0 | 62.1 | 185.2 | 5&nbsp;ms | 177.1 | 17.1 | 24.2 | 1.1 | 492.8 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB | 26.7 | 64.2 | 182.8 | 4&nbsp;ms | 397.2 | 3.0 | 28.0 | 0.9 | 702.8 |
| Visual, OBJ | 24.3 | 59.7 | 177.6 | 5&nbsp;ms | 404.0 | 88.9 | 29.9 | 1.0 | 785.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LimeRFE-8001P](https://github.com/myriadrf/LimeRFE-8001P)<br>Board: `FrontEnd_5G.kicad_pcb` |
|---|---|
| Folder | hardware / 1v0 / KiCAD |
| Complexity | 376&nbsp;/&nbsp;1000 (size&nbsp;291, features&nbsp;85) |
| KESE&nbsp;features | through vias,<br>blind and buried vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 1,605, 23,739, 1,538 |
| Triangles,&nbsp;simulation | 30,808,402 in 1307 parts |
| Verifier | Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Run&nbsp;again | Visual, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.0&nbsp;GB</td><td align="right">8.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.9&nbsp;GB</td><td align="right">10&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.5&nbsp;GB</td><td align="right">8.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">535&nbsp;MB</td><td align="right">8.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.8&nbsp;GB</td><td align="right">11&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.37 FrontEnd_5G

![FrontEnd_5G: stages 4 and 6 take 67% to 85% of a run. Simulation, GLB takes 6 min. Simulation, STEP takes 7 min. Simulation, STL takes 6 min. Visual, GLB takes 10 min. Visual, OBJ takes 11 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LimeRFE-8001P_hardware-1v1-KiCAD_FrontEnd-5G.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 5.7 | 54.4 | 150.5 | 4&nbsp;ms | 131.1 | 6.3 | 19.7 | 0.8 | 368.5 |
| Simulation, STEP | 5.9 | 54.3 | 149.9 | 4&nbsp;ms | 124.6 | 51.7 | 19.8 | 0.7 | 406.8 |
| Simulation, STL | 5.9 | 53.3 | 150.3 | 4&nbsp;ms | 128.2 | 13.6 | 18.8 | 0.7 | 370.8 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB | 5.8 | 52.2 | 147.2 | 4&nbsp;ms | 351.3 | 2.4 | 26.8 | 0.5 | 586.1 |
| Visual, OBJ | 5.6 | 52.1 | 143.3 | 4&nbsp;ms | 352.7 | 74.3 | 25.1 | 0.6 | 653.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LimeRFE-8001P](https://github.com/myriadrf/LimeRFE-8001P)<br>Board: `FrontEnd_5G.kicad_pcb` |
|---|---|
| Folder | hardware / 1v1 / KiCAD |
| Complexity | 383&nbsp;/&nbsp;1000 (size&nbsp;288, features&nbsp;95) |
| KESE&nbsp;features | through vias,<br>blind and buried vias,<br>slotted holes, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 1,461, 20,552, 1,349 |
| Triangles,&nbsp;simulation | 27,133,154 in 1073 parts |
| Verifier | Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">916&nbsp;MB</td><td align="right">7.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.5&nbsp;GB</td><td align="right">8.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.4&nbsp;GB</td><td align="right">7.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">462&nbsp;MB</td><td align="right">7.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.5&nbsp;GB</td><td align="right">9.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.38 LimeSDR_Breakout

![LimeSDR_Breakout: reading, start-up and exit take 42% to 46% of a run. Simulation, GLB takes 1.4 s. Simulation, STEP takes 1.4 s. Simulation, STL takes 1.4 s. Simulation, OBJ takes 1.4 s. Visual, GLB takes 1.4 s. Visual, OBJ takes 1.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LimeSDR-GPIO-Board_LimeSDR-Breakout.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 0.6 | 0.1 | 0.1&nbsp;ms | 23&nbsp;ms | 2&nbsp;ms | 3&nbsp;ms | 0.2 | 1.4 |
| Simulation, STEP | 0.4 | 0.6 | 0.1 | 0.1&nbsp;ms | 25&nbsp;ms | 34&nbsp;ms | 3&nbsp;ms | 0.2 | 1.4 |
| Simulation, STL | 0.4 | 0.6 | 0.1 | 0.1&nbsp;ms | 23&nbsp;ms | 2&nbsp;ms | 4&nbsp;ms | 0.2 | 1.4 |
| Simulation, OBJ | 0.4 | 0.6 | 0.2 | 0.1&nbsp;ms | 25&nbsp;ms | 26&nbsp;ms | 4&nbsp;ms | 0.2 | 1.4 |
| Visual, GLB | 0.4 | 0.6 | 0.1 | 0.1&nbsp;ms | 57&nbsp;ms | 3&nbsp;ms | 21&nbsp;ms | 0.2 | 1.4 |
| Visual, OBJ | 0.4 | 0.6 | 0.1 | 0.1&nbsp;ms | 57&nbsp;ms | 24&nbsp;ms | 13&nbsp;ms | 0.2 | 1.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LimeSDR_GPIO_Board](https://github.com/myriadrf/LimeSDR_GPIO_Board)<br>Board: `LimeSDR_Breakout.kicad_pcb` |
|---|---|
| Folder | hardware / 0402_Variant / CAD2 |
| Complexity | 244&nbsp;/&nbsp;1000 (size&nbsp;199, features&nbsp;45) |
| KESE&nbsp;features | through vias, filled zones,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 90, 2,265, 397 |
| Triangles,&nbsp;simulation | 5,712 in 3 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">165&nbsp;kB</td><td align="right">90&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">74&nbsp;kB</td><td align="right">92&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">286&nbsp;kB</td><td align="right">90&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">542&nbsp;kB</td><td align="right">90&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">212&nbsp;kB</td><td align="right">90&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">545&nbsp;kB</td><td align="right">90&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.39 LMS6002-Pmod

![LMS6002-Pmod: stages 4 and 6 take 59% to 86% of a run. Simulation, GLB takes 8.7 s. Simulation, STEP takes 11 s. Simulation, STL takes 9.2 s. Simulation, OBJ takes 13 s. Visual, GLB takes 13 s. Visual, OBJ takes 15 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LMS6002-Pmod_LMS6002-Pmod.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 3.8 | 0.5&nbsp;ms | 3.4 | 99&nbsp;ms | 0.4 | 0.2 | 8.7 |
| Simulation, STEP | 0.2 | 0.7 | 3.8 | 0.4&nbsp;ms | 3.6 | 2.2 | 0.4 | 0.2 | 11.1 |
| Simulation, STL | 0.3 | 0.7 | 4.1 | 0.3&nbsp;ms | 3.3 | 0.2 | 0.4 | 0.2 | 9.2 |
| Simulation, OBJ | 0.2 | 0.7 | 3.8 | 0.5&nbsp;ms | 3.6 | 3.6 | 0.4 | 0.2 | 12.5 |
| Visual, GLB | 0.2 | 0.6 | 4.3 | 0.4&nbsp;ms | 7.1 | 90&nbsp;ms | 0.7 | 0.2 | 13.2 |
| Visual, OBJ | 0.2 | 0.6 | 3.8 | 0.3&nbsp;ms | 7.1 | 2.8 | 0.7 | 0.2 | 15.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LMS6002-Pmod](https://github.com/myriadrf/LMS6002-Pmod)<br>Board: `LMS6002-Pmod.kicad_pcb` |
|---|---|
| Folder | board / KiCad |
| Complexity | 270&nbsp;/&nbsp;1000 (size&nbsp;215, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>drill offsets, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 55, 891, 65 |
| Triangles,&nbsp;simulation | 724,500 in 95 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">370&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">139&nbsp;MB</td><td align="right">450&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">36&nbsp;MB</td><td align="right">391&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">77&nbsp;MB</td><td align="right">545&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">512&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">60&nbsp;MB</td><td align="right">487&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.40 LMS8001_Companion

![LMS8001_Companion: stages 4 and 6 take 12% to 14% of a run. Simulation, GLB takes 2.8 s. Simulation, STEP takes 2.6 s. Simulation, STL takes 2.7 s. Simulation, OBJ takes 2.6 s. Visual, GLB takes 2.7 s. Visual, OBJ takes 2.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LMS8001-Companion_hardware-2v1-KiCAD_LMS8001-Companion.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 1.3 | 0.4 | 0.1&nbsp;ms | 11&nbsp;ms | 1&nbsp;ms | 3&nbsp;ms | 0.3 | 2.8 |
| Simulation, STEP | 0.9 | 1.1 | 0.3 | 0.0&nbsp;ms | 10&nbsp;ms | 6&nbsp;ms | 3&nbsp;ms | 0.2 | 2.6 |
| Simulation, STL | 0.9 | 1.2 | 0.4 | 0.1&nbsp;ms | 18&nbsp;ms | 2&nbsp;ms | 3&nbsp;ms | 0.2 | 2.7 |
| Simulation, OBJ | 0.8 | 1.1 | 0.3 | 0.1&nbsp;ms | 11&nbsp;ms | 1&nbsp;ms | 3&nbsp;ms | 0.3 | 2.6 |
| Visual, GLB | 0.9 | 1.2 | 0.3 | 0.1&nbsp;ms | 30&nbsp;ms | 2&nbsp;ms | 13&nbsp;ms | 0.2 | 2.7 |
| Visual, OBJ | 1.0 | 1.2 | 0.3 | 0.0&nbsp;ms | 31&nbsp;ms | 1&nbsp;ms | 12&nbsp;ms | 0.3 | 2.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LMS8001-Companion](https://github.com/myriadrf/LMS8001-Companion)<br>Board: `LMS8001_Companion.kicad_pcb` |
|---|---|
| Folder | hardware / 2v1 / KiCAD |
| Complexity | 320&nbsp;/&nbsp;1000 (size&nbsp;265, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 351, 2,038, 174 |
| Triangles,&nbsp;simulation | 52 in 3 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.6&nbsp;kB</td><td align="right">136&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">23&nbsp;kB</td><td align="right">136&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">2.9&nbsp;kB</td><td align="right">136&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.2&nbsp;kB</td><td align="right">136&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.0&nbsp;kB</td><td align="right">136&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">5.2&nbsp;kB</td><td align="right">136&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.41 LMS8001_Companion

![LMS8001_Companion: stages 4 and 6 take 12% to 14% of a run. Simulation, GLB takes 3.1 s. Simulation, STEP takes 3.3 s. Simulation, STL takes 3.2 s. Simulation, OBJ takes 3.1 s. Visual, GLB takes 3.0 s. Visual, OBJ takes 3.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LMS8001-Companion_hardware-3v1-KiCAD_LMS8001-Companion.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 1.5 | 0.4 | 0.0&nbsp;ms | 12&nbsp;ms | 1&nbsp;ms | 3&nbsp;ms | 0.3 | 3.1 |
| Simulation, STEP | 1.1 | 1.5 | 0.4 | 0.1&nbsp;ms | 13&nbsp;ms | 9&nbsp;ms | 3&nbsp;ms | 0.2 | 3.3 |
| Simulation, STL | 1.0 | 1.6 | 0.4 | 0.1&nbsp;ms | 11&nbsp;ms | 1&nbsp;ms | 2&nbsp;ms | 0.3 | 3.2 |
| Simulation, OBJ | 1.1 | 1.4 | 0.4 | 0.1&nbsp;ms | 13&nbsp;ms | 2&nbsp;ms | 3&nbsp;ms | 0.2 | 3.1 |
| Visual, GLB | 1.0 | 1.4 | 0.4 | 0.0&nbsp;ms | 24&nbsp;ms | 1&nbsp;ms | 12&nbsp;ms | 0.2 | 3.0 |
| Visual, OBJ | 1.0 | 1.4 | 0.4 | 0.1&nbsp;ms | 31&nbsp;ms | 2&nbsp;ms | 14&nbsp;ms | 0.2 | 3.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LMS8001-Companion](https://github.com/myriadrf/LMS8001-Companion)<br>Board: `LMS8001_Companion.kicad_pcb` |
|---|---|
| Folder | hardware / 3v1 / KiCAD |
| Complexity | 332&nbsp;/&nbsp;1000 (size&nbsp;267, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 351, 2,332, 176 |
| Triangles,&nbsp;simulation | 52 in 3 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.6&nbsp;kB</td><td align="right">139&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">23&nbsp;kB</td><td align="right">139&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">2.9&nbsp;kB</td><td align="right">139&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.2&nbsp;kB</td><td align="right">139&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.0&nbsp;kB</td><td align="right">139&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">5.2&nbsp;kB</td><td align="right">139&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.42 LMS8001_Companion

![LMS8001_Companion: stages 4 and 6 take 12% to 16% of a run. Simulation, GLB takes 3.2 s. Simulation, STEP takes 3.4 s. Simulation, STL takes 3.4 s. Simulation, OBJ takes 3.3 s. Visual, GLB takes 3.3 s. Visual, OBJ takes 3.5 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/LMS8001-Companion_hardware-3v2-KiCAD_LMS8001-Companion.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.2 | 1.5 | 0.4 | 0.0&nbsp;ms | 12&nbsp;ms | 1&nbsp;ms | 3&nbsp;ms | 0.2 | 3.2 |
| Simulation, STEP | 1.2 | 1.5 | 0.4 | 0.0&nbsp;ms | 11&nbsp;ms | 8&nbsp;ms | 5&nbsp;ms | 0.3 | 3.4 |
| Simulation, STL | 1.0 | 1.5 | 0.5 | 0.0&nbsp;ms | 12&nbsp;ms | 0.9&nbsp;ms | 3&nbsp;ms | 0.3 | 3.4 |
| Simulation, OBJ | 1.1 | 1.6 | 0.4 | 0.0&nbsp;ms | 11&nbsp;ms | 1&nbsp;ms | 3&nbsp;ms | 0.2 | 3.3 |
| Visual, GLB | 1.1 | 1.5 | 0.4 | 0.0&nbsp;ms | 31&nbsp;ms | 2&nbsp;ms | 13&nbsp;ms | 0.3 | 3.3 |
| Visual, OBJ | 1.1 | 1.6 | 0.4 | 0.0&nbsp;ms | 26&nbsp;ms | 1&nbsp;ms | 11&nbsp;ms | 0.3 | 3.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/LMS8001-Companion](https://github.com/myriadrf/LMS8001-Companion)<br>Board: `LMS8001_Companion.kicad_pcb` |
|---|---|
| Folder | hardware / 3v2 / KiCAD |
| Complexity | 333&nbsp;/&nbsp;1000 (size&nbsp;268, features&nbsp;65) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 352, 2,467, 192 |
| Triangles,&nbsp;simulation | 52 in 3 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.6&nbsp;kB</td><td align="right">141&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">23&nbsp;kB</td><td align="right">141&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">2.9&nbsp;kB</td><td align="right">141&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.2&nbsp;kB</td><td align="right">141&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">5.0&nbsp;kB</td><td align="right">142&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">5.2&nbsp;kB</td><td align="right">142&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.43 DigiRED_v1.0

![DigiRED_v1.0: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 50 s. Simulation, STEP takes 59 s. Simulation, STL takes 51 s. Simulation, OBJ takes 79 s. Visual, GLB takes 67 s. Visual, OBJ takes 83 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/RASDR_DigiRED-v1-0.webp)

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

## 23.16.44 DigiRED

![DigiRED: stages 4 and 6 take 49% to 83% of a run. Simulation, GLB takes 54 s. Simulation, STEP takes 63 s. Simulation, STL takes 54 s. Simulation, OBJ takes 84 s. Visual, GLB takes 75 s. Visual, OBJ takes 92 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/RASDR_DigiRED.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 6.8 | 20.2 | 2&nbsp;ms | 21.2 | 1.0 | 3.1 | 0.4 | 53.7 |
| Simulation, STEP | 0.9 | 6.2 | 20.4 | 2&nbsp;ms | 20.8 | 11.1 | 2.9 | 0.4 | 62.6 |
| Simulation, STL | 0.9 | 6.3 | 20.3 | 1&nbsp;ms | 21.2 | 2.3 | 2.9 | 0.3 | 54.1 |
| Simulation, OBJ | 1.0 | 6.1 | 20.0 | 2&nbsp;ms | 21.7 | 32.4 | 2.9 | 0.3 | 84.3 |
| Visual, GLB | 1.0 | 6.2 | 21.1 | 0.8&nbsp;ms | 40.9 | 0.5 | 5.1 | 0.3 | 75.0 |
| Visual, OBJ | 1.0 | 6.3 | 19.7 | 1&nbsp;ms | 39.3 | 19.3 | 5.6 | 0.3 | 91.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/RASDR](https://github.com/myriadrf/RASDR)<br>Board: `DigiRED.kicad_pcb` |
|---|---|
| Folder | DigiRED / hardware / v2 / KiCAD |
| Complexity | 347&nbsp;/&nbsp;1000 (size&nbsp;302, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 239, 3,701, 600 |
| Triangles,&nbsp;simulation | 5,592,164 in 262 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">191&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">634&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">280&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">595&nbsp;MB</td><td align="right">3.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">105&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">339&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.45 LMS8001_Companion

![LMS8001_Companion: stages 4 and 6 take 51% to 80% of a run. Simulation, GLB takes 21 s. Simulation, STEP takes 25 s. Simulation, STL takes 22 s. Simulation, OBJ takes 32 s. Visual, GLB takes 36 s. Visual, OBJ takes 43 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/reference-development-kit_LMS8001-Companion.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 3.1 | 7.9 | 1&nbsp;ms | 7.9 | 0.3 | 0.8 | 0.3 | 21.0 |
| Simulation, STEP | 0.6 | 3.0 | 7.9 | 1&nbsp;ms | 7.8 | 4.8 | 0.9 | 0.3 | 25.3 |
| Simulation, STL | 0.6 | 3.2 | 8.2 | 1&nbsp;ms | 8.2 | 0.8 | 0.9 | 0.3 | 22.2 |
| Simulation, OBJ | 0.6 | 3.2 | 8.3 | 1&nbsp;ms | 8.0 | 11.0 | 0.9 | 0.3 | 32.3 |
| Visual, GLB | 0.6 | 3.0 | 8.3 | 1&nbsp;ms | 20.6 | 0.3 | 2.8 | 0.3 | 35.9 |
| Visual, OBJ | 0.6 | 3.1 | 8.4 | 1&nbsp;ms | 20.0 | 7.9 | 2.6 | 0.2 | 42.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/reference-development-kit](https://github.com/myriadrf/reference-development-kit)<br>Board: `LMS8001_Companion.kicad_pcb` |
|---|---|
| Folder | myriadrf-8001 / 1v0 / KiCAD |
| Complexity | 312&nbsp;/&nbsp;1000 (size&nbsp;257, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 282, 1,241, 165 |
| Triangles,&nbsp;simulation | 2,106,934 in 170 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">73&nbsp;MB</td><td align="right">912&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">259&nbsp;MB</td><td align="right">1.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">105&nbsp;MB</td><td align="right">902&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">221&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">51&nbsp;MB</td><td align="right">905&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">158&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.46 uMyriad6002

![uMyriad6002: stages 4 and 6 take 27% to 36% of a run. Simulation, GLB takes 1.5 s. Simulation, STEP takes 1.6 s. Simulation, STL takes 1.5 s. Simulation, OBJ takes 1.5 s. Visual, GLB takes 1.7 s. Visual, OBJ takes 1.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/reference-development-kit_uMyriad6002.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.5 | 0.3 | 0.2&nbsp;ms | 0.1 | 4&nbsp;ms | 10&nbsp;ms | 0.2 | 1.5 |
| Simulation, STEP | 0.3 | 0.6 | 0.3 | 0.2&nbsp;ms | 0.1 | 0.1 | 11&nbsp;ms | 0.2 | 1.6 |
| Simulation, STL | 0.3 | 0.5 | 0.3 | 0.2&nbsp;ms | 0.1 | 5&nbsp;ms | 11&nbsp;ms | 0.2 | 1.5 |
| Simulation, OBJ | 0.3 | 0.6 | 0.3 | 0.2&nbsp;ms | 0.1 | 57&nbsp;ms | 11&nbsp;ms | 0.2 | 1.5 |
| Visual, GLB | 0.3 | 0.5 | 0.4 | 0.2&nbsp;ms | 0.2 | 3&nbsp;ms | 19&nbsp;ms | 0.2 | 1.7 |
| Visual, OBJ | 0.3 | 0.5 | 0.3 | 0.2&nbsp;ms | 0.2 | 49&nbsp;ms | 18&nbsp;ms | 0.2 | 1.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/reference-development-kit](https://github.com/myriadrf/reference-development-kit)<br>Board: `uMyriad6002.kicad_pcb` |
|---|---|
| Folder | umyriadrf-6002 / v2 / KiCAD |
| Complexity | 301&nbsp;/&nbsp;1000 (size&nbsp;266, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 102, 1,365, 264 |
| Triangles,&nbsp;simulation | 14,060 in 15 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">414&nbsp;kB</td><td align="right">88&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">1.8&nbsp;MB</td><td align="right">88&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">704&nbsp;kB</td><td align="right">88&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">1.4&nbsp;MB</td><td align="right">87&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">390&nbsp;kB</td><td align="right">93&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">1.1&nbsp;MB</td><td align="right">91&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.47 uMyriad7002-append

![uMyriad7002-append: stages 4 and 6 take 24% to 30% of a run. Simulation, GLB takes 5.0 s. Simulation, STEP takes 5.4 s. Simulation, STL takes 4.6 s. Simulation, OBJ takes 4.9 s. Visual, GLB takes 5.0 s. Visual, OBJ takes 5.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/reference-development-kit_uMyriad7002-append.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 2.3 | 1.0 | 0.6&nbsp;ms | 0.5 | 13&nbsp;ms | 23&nbsp;ms | 0.3 | 5.0 |
| Simulation, STEP | 0.8 | 2.3 | 0.9 | 0.8&nbsp;ms | 0.4 | 0.7 | 20&nbsp;ms | 0.3 | 5.4 |
| Simulation, STL | 0.9 | 2.2 | 0.9 | 0.7&nbsp;ms | 0.4 | 15&nbsp;ms | 24&nbsp;ms | 0.2 | 4.6 |
| Simulation, OBJ | 0.7 | 2.3 | 1.0 | 0.7&nbsp;ms | 0.4 | 0.3 | 20&nbsp;ms | 0.2 | 4.9 |
| Visual, GLB | 0.9 | 2.3 | 1.0 | 0.5&nbsp;ms | 0.5 | 9&nbsp;ms | 54&nbsp;ms | 0.3 | 5.0 |
| Visual, OBJ | 0.8 | 2.2 | 1.0 | 0.6&nbsp;ms | 0.5 | 0.2 | 51&nbsp;ms | 0.2 | 5.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/reference-development-kit](https://github.com/myriadrf/reference-development-kit)<br>Board: `uMyriad7002-append.kicad_pcb` |
|---|---|
| Folder | umyriadrf-7002 / v2 / KiCAD |
| Complexity | 333&nbsp;/&nbsp;1000 (size&nbsp;298, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 272, 3,360, 701 |
| Triangles,&nbsp;simulation | 55,824 in 16 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.6&nbsp;MB</td><td align="right">223&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">6.6&nbsp;MB</td><td align="right">227&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">2.8&nbsp;MB</td><td align="right">224&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">5.5&nbsp;MB</td><td align="right">230&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">1.4&nbsp;MB</td><td align="right">230&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">4.5&nbsp;MB</td><td align="right">225&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.48 uMyriad7002

![uMyriad7002: stages 4 and 6 take 21% to 28% of a run. Simulation, GLB takes 2.7 s. Simulation, STEP takes 2.8 s. Simulation, STL takes 2.8 s. Simulation, OBJ takes 2.8 s. Visual, GLB takes 3.0 s. Visual, OBJ takes 3.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/reference-development-kit_uMyriad7002.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 1.3 | 0.5 | 0.3&nbsp;ms | 0.1 | 4&nbsp;ms | 12&nbsp;ms | 0.2 | 2.7 |
| Simulation, STEP | 0.6 | 1.3 | 0.5 | 0.2&nbsp;ms | 0.1 | 0.1 | 14&nbsp;ms | 0.2 | 2.8 |
| Simulation, STL | 0.6 | 1.3 | 0.5 | 0.2&nbsp;ms | 99&nbsp;ms | 4&nbsp;ms | 12&nbsp;ms | 0.2 | 2.8 |
| Simulation, OBJ | 0.6 | 1.3 | 0.5 | 0.3&nbsp;ms | 0.1 | 76&nbsp;ms | 13&nbsp;ms | 0.2 | 2.8 |
| Visual, GLB | 0.6 | 1.4 | 0.5 | 0.2&nbsp;ms | 0.3 | 5&nbsp;ms | 27&nbsp;ms | 0.2 | 3.0 |
| Visual, OBJ | 0.6 | 1.3 | 0.5 | 0.3&nbsp;ms | 0.3 | 51&nbsp;ms | 18&nbsp;ms | 0.2 | 3.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/reference-development-kit](https://github.com/myriadrf/reference-development-kit)<br>Board: `uMyriad7002.kicad_pcb` |
|---|---|
| Folder | umyriadrf-7002 / v2 / KiCAD |
| Complexity | 314&nbsp;/&nbsp;1000 (size&nbsp;279, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 177, 2,058, 436 |
| Triangles,&nbsp;simulation | 11,772 in 16 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">359&nbsp;kB</td><td align="right">104&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">1.5&nbsp;MB</td><td align="right">105&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">590&nbsp;kB</td><td align="right">105&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">1.2&nbsp;MB</td><td align="right">106&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">340&nbsp;kB</td><td align="right">104&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">959&nbsp;kB</td><td align="right">105&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.49 Zipper

![Zipper: stages 4 and 6 take 49% to 82% of a run. Simulation, GLB takes 70 s. Simulation, STEP takes 81 s. Simulation, STL takes 73 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/reference-development-kit_Zipper.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.5 | 8.6 | 25.9 | 2&nbsp;ms | 28.0 | 1.3 | 4.2 | 0.4 | 69.9 |
| Simulation, STEP | 1.2 | 7.9 | 25.0 | 1&nbsp;ms | 27.7 | 14.4 | 4.4 | 0.4 | 81.0 |
| Simulation, STL | 1.3 | 7.9 | 26.1 | 2&nbsp;ms | 29.2 | 3.4 | 4.4 | 0.4 | 72.8 |
| Simulation, OBJ | 1.4 | 8.3 | 26.0 | 1&nbsp;ms | 28.5 | 43.2 | 4.1 | 0.4 | 111.9 |
| Visual, GLB | 1.3 | 8.4 | 25.3 | 2&nbsp;ms | 57.4 | 0.7 | 7.5 | 0.3 | 101.1 |
| Visual, OBJ | 1.4 | 8.2 | 25.8 | 2&nbsp;ms | 56.9 | 24.7 | 7.6 | 0.3 | 124.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/reference-development-kit](https://github.com/myriadrf/reference-development-kit)<br>Board: `Zipper.kicad_pcb` |
|---|---|
| Folder | zipper / hardware / v2 / KiCAD |
| Complexity | 350&nbsp;/&nbsp;1000 (size&nbsp;295, features&nbsp;55) |
| KESE&nbsp;features | through vias, filled zones,<br>copper text, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 173, 3,620, 614 |
| Triangles,&nbsp;simulation | 7,391,440 in 297 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">251&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">764&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">370&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">786&nbsp;MB</td><td align="right">4.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">137&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">446&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.50 Stream

![Stream: stages 4 and 6 take 27% to 28% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 13 s. Simulation, STL takes 13 s. Simulation, OBJ takes 14 s. Visual, GLB takes 14 s. Visual, OBJ takes 14 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/STREAM_Stream.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.4 | 6.8 | 3.4 | 0.4&nbsp;ms | 0.2 | 7&nbsp;ms | 13&nbsp;ms | 0.3 | 13.1 |
| Simulation, STEP | 2.4 | 6.9 | 3.4 | 0.1&nbsp;ms | 0.2 | 0.3 | 12&nbsp;ms | 0.2 | 13.4 |
| Simulation, STL | 2.3 | 6.9 | 3.3 | 0.1&nbsp;ms | 0.2 | 11&nbsp;ms | 13&nbsp;ms | 0.3 | 13.1 |
| Simulation, OBJ | 2.3 | 6.9 | 3.6 | 0.2&nbsp;ms | 0.3 | 0.3 | 18&nbsp;ms | 0.3 | 13.7 |
| Visual, GLB | 2.5 | 7.3 | 3.5 | 0.1&nbsp;ms | 0.6 | 8&nbsp;ms | 33&nbsp;ms | 0.3 | 14.2 |
| Visual, OBJ | 2.5 | 7.1 | 3.4 | 0.1&nbsp;ms | 0.5 | 0.2 | 27&nbsp;ms | 0.3 | 13.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/STREAM](https://github.com/myriadrf/STREAM)<br>Board: `Stream.kicad_pcb` |
|---|---|
| Folder | hardware / STREAM / v2 / v2r1 / KiCAD |
| Complexity | 402&nbsp;/&nbsp;1000 (size&nbsp;357, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 12 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 695, 10,937, 1,470 |
| Triangles,&nbsp;simulation | 41,954 in 20 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.2&nbsp;MB</td><td align="right">416&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">3.4&nbsp;MB</td><td align="right">414&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">2.1&nbsp;MB</td><td align="right">419&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">4.2&nbsp;MB</td><td align="right">421&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">931&nbsp;kB</td><td align="right">417&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">3.2&nbsp;MB</td><td align="right">414&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.51 uSTREAM

![uSTREAM: stages 4 and 6 take 23% to 28% of a run. Simulation, GLB takes 6.9 s. Simulation, STEP takes 7.1 s. Simulation, STL takes 7.0 s. Simulation, OBJ takes 6.8 s. Visual, GLB takes 7.5 s. Visual, OBJ takes 7.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/STREAM_uSTREAM.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.4 | 3.6 | 1.5 | 0.4&nbsp;ms | 0.2 | 6&nbsp;ms | 14&nbsp;ms | 0.2 | 6.9 |
| Simulation, STEP | 1.5 | 3.5 | 1.5 | 0.1&nbsp;ms | 0.2 | 0.2 | 20&nbsp;ms | 0.2 | 7.1 |
| Simulation, STL | 1.4 | 3.6 | 1.6 | 0.4&nbsp;ms | 0.2 | 8&nbsp;ms | 16&nbsp;ms | 0.2 | 7.0 |
| Simulation, OBJ | 1.4 | 3.5 | 1.4 | 0.1&nbsp;ms | 0.2 | 0.2 | 17&nbsp;ms | 0.2 | 6.8 |
| Visual, GLB | 1.4 | 3.7 | 1.6 | 0.1&nbsp;ms | 0.5 | 7&nbsp;ms | 32&nbsp;ms | 0.2 | 7.5 |
| Visual, OBJ | 1.5 | 3.6 | 1.6 | 0.2&nbsp;ms | 0.6 | 0.1 | 33&nbsp;ms | 0.2 | 7.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/STREAM](https://github.com/myriadrf/STREAM)<br>Board: `uSTREAM.kicad_pcb` |
|---|---|
| Folder | hardware / uSTREAM / v2 / KiCAD |
| Complexity | 379&nbsp;/&nbsp;1000 (size&nbsp;334, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 12 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 346, 5,344, 992 |
| Triangles,&nbsp;simulation | 28,340 in 20 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">832&nbsp;kB</td><td align="right">282&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">3.5&nbsp;MB</td><td align="right">281&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">1.4&nbsp;MB</td><td align="right">282&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">2.9&nbsp;MB</td><td align="right">282&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">755&nbsp;kB</td><td align="right">281&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">2.3&nbsp;MB</td><td align="right">281&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.52 Vivaldi

![Vivaldi: reading, start-up and exit take 41% to 61% of a run. Simulation, GLB takes 0.5 s. Simulation, STEP takes 0.7 s. Simulation, STL takes 0.5 s. Simulation, OBJ takes 0.6 s. Visual, GLB takes 0.7 s. Visual, OBJ takes 0.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/vivaldi-antenna_Vivaldi.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 96&nbsp;ms | 33&nbsp;ms | 42&nbsp;ms | 0.1&nbsp;ms | 0.1 | 3&nbsp;ms | 11&nbsp;ms | 0.2 | 0.5 |
| Simulation, STEP | 82&nbsp;ms | 27&nbsp;ms | 34&nbsp;ms | 0.1&nbsp;ms | 0.1 | 95&nbsp;ms | 11&nbsp;ms | 0.4 | 0.7 |
| Simulation, STL | 73&nbsp;ms | 24&nbsp;ms | 32&nbsp;ms | 0.1&nbsp;ms | 0.1 | 5&nbsp;ms | 18&nbsp;ms | 0.2 | 0.5 |
| Simulation, OBJ | 72&nbsp;ms | 25&nbsp;ms | 35&nbsp;ms | 0.1&nbsp;ms | 0.1 | 50&nbsp;ms | 14&nbsp;ms | 0.3 | 0.6 |
| Visual, GLB | 75&nbsp;ms | 26&nbsp;ms | 32&nbsp;ms | 0.1&nbsp;ms | 0.2 | 4&nbsp;ms | 51&nbsp;ms | 0.3 | 0.7 |
| Visual, OBJ | 74&nbsp;ms | 26&nbsp;ms | 57&nbsp;ms | 0.1&nbsp;ms | 0.3 | 49&nbsp;ms | 35&nbsp;ms | 0.2 | 0.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [myriadrf/vivaldi-antenna](https://github.com/myriadrf/vivaldi-antenna)<br>Board: `Vivaldi.kicad_pcb` |
|---|---|
| Folder | hardware / KiCAD |
| Complexity | 98&nbsp;/&nbsp;1000 (size&nbsp;63, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 1, 4, 2 |
| Triangles,&nbsp;simulation | 9,304 in 10 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">331&nbsp;kB</td><td align="right">62&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">2.0&nbsp;MB</td><td align="right">62&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">466&nbsp;kB</td><td align="right">62&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">845&nbsp;kB</td><td align="right">62&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">302&nbsp;kB</td><td align="right">83&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">772&nbsp;kB</td><td align="right">84&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.53 Yellow

![Yellow: stages 4 and 6 take 50% to 82% of a run. Simulation, GLB takes 72 s. Simulation, STEP takes 86 s. Simulation, STL takes 74 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/yellow_Yellow.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.9 | 9.3 | 31.4 | 1&nbsp;ms | 24.0 | 1.2 | 3.6 | 0.3 | 71.7 |
| Simulation, STEP | 2.0 | 9.1 | 31.9 | 1&nbsp;ms | 24.1 | 15.0 | 3.6 | 0.4 | 86.1 |
| Simulation, STL | 2.0 | 9.0 | 32.7 | 2&nbsp;ms | 24.0 | 2.3 | 3.4 | 0.3 | 73.7 |
| Simulation, OBJ | 1.9 | 9.1 | 31.8 | 1&nbsp;ms | 23.4 | 41.2 | 3.7 | 0.3 | 111.3 |
| Visual, GLB | 2.1 | 9.2 | 31.9 | 2&nbsp;ms | 58.6 | 0.7 | 7.6 | 0.3 | 110.3 |
| Visual, OBJ | 1.9 | 9.1 | 31.1 | 0.9&nbsp;ms | 57.7 | 26.8 | 7.0 | 0.3 | 133.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [NabuCasa/yellow](https://github.com/NabuCasa/yellow)<br>Board: `Yellow.kicad_pcb` |
|---|---|
| Complexity | 441&nbsp;/&nbsp;1000 (size&nbsp;291, features&nbsp;150) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 280, 3,463, 1,961 |
| Triangles,&nbsp;simulation | 6,590,014 in 390 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">222&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">788&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">330&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">695&nbsp;MB</td><td align="right">4.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">159&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">511&nbsp;MB</td><td align="right">3.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.54 keyboard_system

![keyboard_system: stages 4 and 6 take 46% to 79% of a run. Simulation, GLB takes 5.2 s. Simulation, STEP takes 6.4 s. Simulation, STL takes 4.8 s. Simulation, OBJ takes 7.5 s. Visual, GLB takes 7.6 s. Visual, OBJ takes 9.0 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/vohm_keyboard-system.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.5 | 1.7 | 0.2&nbsp;ms | 2.0 | 86&nbsp;ms | 0.3 | 0.3 | 5.2 |
| Simulation, STEP | 0.3 | 0.5 | 1.6 | 0.2&nbsp;ms | 1.9 | 1.6 | 0.3 | 0.2 | 6.4 |
| Simulation, STL | 0.3 | 0.5 | 1.5 | 0.2&nbsp;ms | 2.0 | 0.1 | 0.3 | 0.2 | 4.8 |
| Simulation, OBJ | 0.3 | 0.5 | 1.6 | 0.3&nbsp;ms | 1.8 | 2.8 | 0.3 | 0.2 | 7.5 |
| Visual, GLB | 0.3 | 0.5 | 1.6 | 0.3&nbsp;ms | 4.3 | 56&nbsp;ms | 0.5 | 0.2 | 7.6 |
| Visual, OBJ | 0.3 | 0.5 | 1.5 | 0.2&nbsp;ms | 4.1 | 1.8 | 0.6 | 0.2 | 9.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nalgonda-tiger/vohm](https://github.com/nalgonda-tiger/vohm)<br>Board: `keyboard_system.kicad_pcb` |
|---|---|
| Folder | keyboard_system |
| Complexity | 327&nbsp;/&nbsp;1000 (size&nbsp;217, features&nbsp;110) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 34, 433, 59 |
| Triangles,&nbsp;simulation | 574,658 in 55 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">316&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">84&nbsp;MB</td><td align="right">393&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">29&nbsp;MB</td><td align="right">316&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">59&nbsp;MB</td><td align="right">436&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">409&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">47&nbsp;MB</td><td align="right">423&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.55 LattePandaMu_Motherboard

![LattePandaMu_Motherboard: stages 4 and 6 take 60% to 82% of a run. Simulation, GLB takes 64 s. Simulation, STEP takes 74 s. Simulation, STL takes 64 s. Simulation, OBJ takes 86 s. Visual, GLB takes 83 s. Visual, OBJ takes 99 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/vohm_LattePandaMu-Motherboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.6 | 5.7 | 22.3 | 2&nbsp;ms | 30.8 | 0.9 | 2.9 | 0.4 | 64.4 |
| Simulation, STEP | 1.7 | 5.4 | 21.6 | 2&nbsp;ms | 29.3 | 13.1 | 2.8 | 0.3 | 74.2 |
| Simulation, STL | 1.5 | 5.9 | 22.5 | 2&nbsp;ms | 29.3 | 1.7 | 2.9 | 0.4 | 64.2 |
| Simulation, OBJ | 1.6 | 5.8 | 22.1 | 2&nbsp;ms | 29.4 | 23.7 | 3.2 | 0.3 | 86.0 |
| Visual, GLB | 1.7 | 6.0 | 22.5 | 3&nbsp;ms | 45.8 | 0.5 | 6.1 | 0.3 | 83.0 |
| Visual, OBJ | 1.8 | 5.9 | 23.6 | 2&nbsp;ms | 44.9 | 15.9 | 6.5 | 0.4 | 99.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nalgonda-tiger/vohm](https://github.com/nalgonda-tiger/vohm)<br>Board: `LattePandaMu_Motherboard.kicad_pcb` |
|---|---|
| Folder | LattePandaMu_Motherboard-Main |
| Complexity | 413&nbsp;/&nbsp;1000 (size&nbsp;278, features&nbsp;135) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 305, 4,033, 724 |
| Triangles,&nbsp;simulation | 4,431,648 in 487 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">153&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">679&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">222&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">478&nbsp;MB</td><td align="right">2.9&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">110&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">350&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.56 NewAudio_System

![NewAudio_System: stages 4 and 6 take 60% to 83% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 20 s. Simulation, STL takes 16 s. Simulation, OBJ takes 22 s. Visual, GLB takes 20 s. Visual, OBJ takes 25 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/vohm_NewAudio-System.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.2 | 5.5 | 0.6&nbsp;ms | 7.6 | 0.2 | 0.6 | 0.2 | 15.8 |
| Simulation, STEP | 0.5 | 1.1 | 5.4 | 0.6&nbsp;ms | 7.6 | 4.3 | 0.5 | 0.2 | 19.6 |
| Simulation, STL | 0.5 | 1.1 | 5.5 | 0.7&nbsp;ms | 7.9 | 0.5 | 0.6 | 0.2 | 16.4 |
| Simulation, OBJ | 0.5 | 1.2 | 5.6 | 0.5&nbsp;ms | 7.6 | 6.3 | 0.6 | 0.2 | 22.1 |
| Visual, GLB | 0.5 | 1.3 | 5.5 | 0.6&nbsp;ms | 11.3 | 0.1 | 1.3 | 0.2 | 20.3 |
| Visual, OBJ | 0.5 | 1.2 | 5.4 | 0.4&nbsp;ms | 11.8 | 4.7 | 1.3 | 0.2 | 25.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nalgonda-tiger/vohm](https://github.com/nalgonda-tiger/vohm)<br>Board: `NewAudio_System.kicad_pcb` |
|---|---|
| Folder | NewAudio_System |
| Complexity | 307&nbsp;/&nbsp;1000 (size&nbsp;212, features&nbsp;95) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 198, 1,101, 188 |
| Triangles,&nbsp;simulation | 1,635,412 in 155 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">56&nbsp;MB</td><td align="right">661&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">276&nbsp;MB</td><td align="right">792&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">82&nbsp;MB</td><td align="right">642&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">171&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">40&nbsp;MB</td><td align="right">734&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">123&nbsp;MB</td><td align="right">878&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.57 webcam_microphone_system

![webcam_microphone_system: stages 4 and 6 take 48% to 80% of a run. Simulation, GLB takes 7.0 s. Simulation, STEP takes 9.3 s. Simulation, STL takes 6.9 s. Simulation, OBJ takes 11 s. Visual, GLB takes 9.9 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/vohm_webcam-microphone-system.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 0.7 | 2.1 | 0.3&nbsp;ms | 2.9 | 0.1 | 0.4 | 0.3 | 7.0 |
| Simulation, STEP | 0.4 | 0.7 | 2.2 | 0.3&nbsp;ms | 2.9 | 2.6 | 0.4 | 0.2 | 9.3 |
| Simulation, STL | 0.4 | 0.6 | 2.1 | 0.3&nbsp;ms | 2.9 | 0.2 | 0.4 | 0.2 | 6.9 |
| Simulation, OBJ | 0.4 | 0.6 | 2.3 | 0.3&nbsp;ms | 3.1 | 4.1 | 0.4 | 0.2 | 11.1 |
| Visual, GLB | 0.4 | 0.7 | 2.1 | 0.4&nbsp;ms | 5.8 | 86&nbsp;ms | 0.6 | 0.2 | 9.9 |
| Visual, OBJ | 0.4 | 0.6 | 2.1 | 0.4&nbsp;ms | 5.9 | 2.9 | 0.7 | 0.2 | 12.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nalgonda-tiger/vohm](https://github.com/nalgonda-tiger/vohm)<br>Board: `webcam_microphone_system.kicad_pcb` |
|---|---|
| Folder | webcam_microphone_system |
| Complexity | 353&nbsp;/&nbsp;1000 (size&nbsp;228, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 61, 593, 73 |
| Triangles,&nbsp;simulation | 696,602 in 95 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">24&nbsp;MB</td><td align="right">365&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">106&nbsp;MB</td><td align="right">430&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">35&nbsp;MB</td><td align="right">367&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">71&nbsp;MB</td><td align="right">509&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">484&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">52&nbsp;MB</td><td align="right">475&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.58 PQ_ADCS

![PQ_ADCS: stages 4 and 6 take 46% to 82% of a run. Simulation, GLB takes 10 s. Simulation, STEP takes 13 s. Simulation, STL takes 11 s. Simulation, OBJ takes 17 s. Visual, GLB takes 15 s. Visual, OBJ takes 19 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_pq-adcs-PQ-ADCS_PQ-ADCS.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.2 | 3.7 | 0.3&nbsp;ms | 3.8 | 0.2 | 0.7 | 0.3 | 10.2 |
| Simulation, STEP | 0.4 | 1.2 | 3.7 | 0.4&nbsp;ms | 4.0 | 3.1 | 0.7 | 0.2 | 13.3 |
| Simulation, STL | 0.3 | 1.2 | 3.8 | 0.4&nbsp;ms | 4.1 | 0.3 | 0.6 | 0.2 | 10.6 |
| Simulation, OBJ | 0.4 | 1.3 | 3.8 | 0.4&nbsp;ms | 4.1 | 6.9 | 0.6 | 0.2 | 17.3 |
| Visual, GLB | 0.4 | 1.1 | 3.7 | 0.4&nbsp;ms | 8.5 | 0.1 | 0.9 | 0.2 | 14.8 |
| Visual, OBJ | 0.4 | 1.1 | 3.5 | 0.5&nbsp;ms | 8.3 | 4.1 | 1.1 | 0.3 | 18.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_ADCS.kicad_pcb` |
|---|---|
| Folder | pq_adcs / PQ_ADCS |
| Complexity | 296&nbsp;/&nbsp;1000 (size&nbsp;196, features&nbsp;100) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 45, 603, 89 |
| Triangles,&nbsp;simulation | 1,290,194 in 93 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">43&nbsp;MB</td><td align="right">503&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">171&nbsp;MB</td><td align="right">593&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">65&nbsp;MB</td><td align="right">496&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">132&nbsp;MB</td><td align="right">871&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">638&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">79&nbsp;MB</td><td align="right">603&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.59 PQ_ADCS

![PQ_ADCS: stages 4 and 6 take 47% to 83% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 16 s. Simulation, STL takes 13 s. Simulation, OBJ takes 20 s. Visual, GLB takes 18 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_pq-adcs-PQ-ADCS-HBridge_PQ-ADCS.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.5 | 4.9 | 0.4&nbsp;ms | 4.9 | 0.2 | 0.7 | 0.2 | 12.9 |
| Simulation, STEP | 0.4 | 1.3 | 4.7 | 0.7&nbsp;ms | 4.9 | 3.6 | 0.6 | 0.3 | 15.9 |
| Simulation, STL | 0.4 | 1.3 | 4.7 | 0.4&nbsp;ms | 4.9 | 0.5 | 0.7 | 0.3 | 12.8 |
| Simulation, OBJ | 0.4 | 1.4 | 4.7 | 0.4&nbsp;ms | 4.9 | 8.1 | 0.7 | 0.2 | 20.3 |
| Visual, GLB | 0.4 | 1.3 | 4.8 | 0.4&nbsp;ms | 10.2 | 0.2 | 1.0 | 0.3 | 18.2 |
| Visual, OBJ | 0.4 | 1.4 | 4.8 | 0.4&nbsp;ms | 9.7 | 4.7 | 1.2 | 0.2 | 22.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_ADCS.kicad_pcb` |
|---|---|
| Folder | pq_adcs / PQ_ADCS_HBridge |
| Complexity | 302&nbsp;/&nbsp;1000 (size&nbsp;202, features&nbsp;100) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 56, 779, 123 |
| Triangles,&nbsp;simulation | 1,549,468 in 103 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">52&nbsp;MB</td><td align="right">532&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">204&nbsp;MB</td><td align="right">653&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">77&nbsp;MB</td><td align="right">532&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">160&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">674&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">93&nbsp;MB</td><td align="right">724&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.60 PQ_BotBoard

![PQ_BotBoard: stages 4 and 6 take 54% to 76% of a run. Simulation, GLB takes 13 s. Simulation, STEP takes 17 s. Simulation, STL takes 13 s. Simulation, OBJ takes 18 s. Visual, GLB takes 16 s. Visual, OBJ takes 19 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ-BotBoard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 1.5 | 3.7 | 0.2&nbsp;ms | 6.2 | 0.2 | 0.5 | 0.3 | 13.2 |
| Simulation, STEP | 0.9 | 1.5 | 3.6 | 0.2&nbsp;ms | 6.0 | 3.8 | 0.5 | 0.2 | 16.5 |
| Simulation, STL | 0.9 | 1.5 | 3.6 | 0.2&nbsp;ms | 6.0 | 0.3 | 0.5 | 0.3 | 13.1 |
| Simulation, OBJ | 0.9 | 1.5 | 3.4 | 0.3&nbsp;ms | 6.2 | 5.2 | 0.5 | 0.2 | 17.9 |
| Visual, GLB | 1.0 | 1.6 | 3.6 | 0.2&nbsp;ms | 8.4 | 0.1 | 0.9 | 0.3 | 15.8 |
| Visual, OBJ | 0.8 | 1.5 | 3.7 | 0.2&nbsp;ms | 8.5 | 3.7 | 0.9 | 0.2 | 19.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_BotBoard.kicad_pcb` |
|---|---|
| Folder | pq_botboard / PQ_BotBoard |
| Complexity | 279&nbsp;/&nbsp;1000 (size&nbsp;189, features&nbsp;90) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 21, 808, 57 |
| Triangles,&nbsp;simulation | 861,722 in 44 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">448&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">120&nbsp;MB</td><td align="right">514&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">43&nbsp;MB</td><td align="right">459&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">90&nbsp;MB</td><td align="right">661&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">22&nbsp;MB</td><td align="right">564&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">66&nbsp;MB</td><td align="right">537&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.61 PQ_Botnotsobot

![PQ_Botnotsobot: stages 4 and 6 take 52% to 73% of a run. Simulation, GLB takes 8.0 s. Simulation, STEP takes 11 s. Simulation, STL takes 8.4 s. Simulation, OBJ takes 9.9 s. Visual, GLB takes 8.9 s. Visual, OBJ takes 11 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ-Botnotsobot.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 0.9 | 1.6 | 0.2&nbsp;ms | 4.1 | 90&nbsp;ms | 0.2 | 0.2 | 8.0 |
| Simulation, STEP | 0.7 | 0.9 | 1.6 | 0.1&nbsp;ms | 4.1 | 3.2 | 0.2 | 0.2 | 10.8 |
| Simulation, STL | 0.8 | 1.0 | 1.6 | 0.2&nbsp;ms | 4.3 | 0.2 | 0.2 | 0.3 | 8.4 |
| Simulation, OBJ | 0.7 | 0.9 | 1.5 | 0.1&nbsp;ms | 3.9 | 2.4 | 0.2 | 0.2 | 9.9 |
| Visual, GLB | 0.8 | 0.9 | 1.7 | 0.1&nbsp;ms | 4.7 | 66&nbsp;ms | 0.4 | 0.2 | 8.9 |
| Visual, OBJ | 0.7 | 0.9 | 1.9 | 0.2&nbsp;ms | 4.3 | 2.4 | 0.7 | 0.2 | 11.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_Botnotsobot.kicad_pcb` |
|---|---|
| Folder | pq_botnotsobot / PQ_Botnotsobot |
| Complexity | 84&nbsp;/&nbsp;1000 (size&nbsp;29, features&nbsp;55) |
| KESE&nbsp;features | copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 0, 0 |
| Triangles,&nbsp;simulation | 363,220 in 21 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">366&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">54&nbsp;MB</td><td align="right">368&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">18&nbsp;MB</td><td align="right">367&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">40&nbsp;MB</td><td align="right">367&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">382&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">37&nbsp;MB</td><td align="right">338&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.62 EGSE

![EGSE: stages 4 and 6 take 47% to 80% of a run. Simulation, GLB takes 65 s. Simulation, STEP takes 79 s. Simulation, STL takes 64 s. Simulation, OBJ takes 2 min. Visual, GLB takes 85 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_EGSE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 3.0 | 8.5 | 25.5 | 0.7&nbsp;ms | 22.6 | 1.3 | 3.4 | 0.4 | 64.6 |
| Simulation, STEP | 2.9 | 8.9 | 26.0 | 0.8&nbsp;ms | 22.7 | 14.8 | 3.2 | 0.4 | 78.9 |
| Simulation, STL | 3.0 | 8.7 | 25.2 | 1&nbsp;ms | 21.7 | 2.1 | 2.9 | 0.4 | 64.1 |
| Simulation, OBJ | 2.8 | 8.4 | 24.7 | 1&nbsp;ms | 21.8 | 38.5 | 3.0 | 0.3 | 99.6 |
| Visual, GLB | 2.9 | 8.5 | 24.3 | 1&nbsp;ms | 43.4 | 0.6 | 4.5 | 0.3 | 84.6 |
| Visual, OBJ | 3.1 | 8.4 | 24.7 | 2&nbsp;ms | 45.0 | 19.6 | 5.0 | 0.3 | 106.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `EGSE.kicad_pcb` |
|---|---|
| Folder | pq_egse |
| Complexity | 323&nbsp;/&nbsp;1000 (size&nbsp;223, features&nbsp;100) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 104, 2,243, 172 |
| Triangles,&nbsp;simulation | 7,126,428 in 99 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">241&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">746&nbsp;MB</td><td align="right">2.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">356&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">760&nbsp;MB</td><td align="right">4.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">123&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">386&nbsp;MB</td><td align="right">2.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.63 PQ_EPS

![PQ_EPS: stages 4 and 6 take 48% to 81% of a run. Simulation, GLB takes 8.4 s. Simulation, STEP takes 11 s. Simulation, STL takes 8.7 s. Simulation, OBJ takes 13 s. Visual, GLB takes 13 s. Visual, OBJ takes 16 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ-EPS.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 0.8 | 3.1 | 0.5&nbsp;ms | 3.3 | 0.2 | 0.5 | 0.2 | 8.4 |
| Simulation, STEP | 0.3 | 0.8 | 3.3 | 0.4&nbsp;ms | 3.2 | 2.5 | 0.5 | 0.2 | 10.9 |
| Simulation, STL | 0.4 | 0.8 | 3.1 | 0.5&nbsp;ms | 3.3 | 0.4 | 0.5 | 0.2 | 8.7 |
| Simulation, OBJ | 0.4 | 0.8 | 3.1 | 0.6&nbsp;ms | 3.2 | 4.9 | 0.5 | 0.2 | 13.1 |
| Visual, GLB | 0.4 | 0.9 | 3.1 | 0.5&nbsp;ms | 7.8 | 0.1 | 0.9 | 0.3 | 13.4 |
| Visual, OBJ | 0.3 | 0.8 | 3.1 | 0.5&nbsp;ms | 7.6 | 3.3 | 1.1 | 0.2 | 16.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_EPS.kicad_pcb` |
|---|---|
| Folder | pq_eps / PQ_EPS |
| Complexity | 280&nbsp;/&nbsp;1000 (size&nbsp;190, features&nbsp;90) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 82, 475, 96 |
| Triangles,&nbsp;simulation | 1,126,386 in 91 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">38&nbsp;MB</td><td align="right">538&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">167&nbsp;MB</td><td align="right">584&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">56&nbsp;MB</td><td align="right">508&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">114&nbsp;MB</td><td align="right">807&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">658&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">80&nbsp;MB</td><td align="right">661&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.64 PQ_Lat_Board

![PQ_Lat_Board: stages 4 and 6 take 53% to 74% of a run. Simulation, GLB takes 9.5 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.2 s. Simulation, OBJ takes 11 s. Visual, GLB takes 10 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ-Lat-Board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 1.1 | 2.1 | 0.3&nbsp;ms | 4.8 | 0.1 | 0.3 | 0.3 | 9.5 |
| Simulation, STEP | 0.7 | 1.1 | 1.9 | 0.6&nbsp;ms | 4.6 | 3.4 | 0.3 | 0.3 | 12.4 |
| Simulation, STL | 0.7 | 1.0 | 1.9 | 0.2&nbsp;ms | 4.9 | 0.2 | 0.3 | 0.3 | 9.2 |
| Simulation, OBJ | 0.7 | 1.1 | 1.9 | 0.2&nbsp;ms | 4.5 | 2.8 | 0.3 | 0.3 | 11.5 |
| Visual, GLB | 0.7 | 1.0 | 2.1 | 0.2&nbsp;ms | 5.5 | 67&nbsp;ms | 0.6 | 0.2 | 10.2 |
| Visual, OBJ | 0.7 | 1.0 | 1.9 | 0.3&nbsp;ms | 5.4 | 2.3 | 0.7 | 0.3 | 12.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_Lat_Board.kicad_pcb` |
|---|---|
| Folder | pq_latboard / PQ_Lat_Board |
| Complexity | 260&nbsp;/&nbsp;1000 (size&nbsp;180, features&nbsp;80) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 14, 670, 19 |
| Triangles,&nbsp;simulation | 554,510 in 30 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">20&nbsp;MB</td><td align="right">417&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">80&nbsp;MB</td><td align="right">413&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">28&nbsp;MB</td><td align="right">417&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">60&nbsp;MB</td><td align="right">466&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">459&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">47&nbsp;MB</td><td align="right">419&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.65 PQ_Lat_Board_Deploy

![PQ_Lat_Board_Deploy: stages 4 and 6 take 55% to 74% of a run. Simulation, GLB takes 7.7 s. Simulation, STEP takes 10 s. Simulation, STL takes 7.7 s. Simulation, OBJ takes 10 s. Visual, GLB takes 8.9 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ-Lat-Board-Deploy.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 0.9 | 1.9 | 0.3&nbsp;ms | 3.6 | 90&nbsp;ms | 0.3 | 0.2 | 7.7 |
| Simulation, STEP | 0.6 | 0.9 | 1.9 | 0.2&nbsp;ms | 3.8 | 2.7 | 0.3 | 0.2 | 10.3 |
| Simulation, STL | 0.6 | 0.9 | 1.9 | 0.2&nbsp;ms | 3.6 | 0.2 | 0.2 | 0.2 | 7.7 |
| Simulation, OBJ | 0.6 | 0.9 | 1.9 | 0.2&nbsp;ms | 3.9 | 2.5 | 0.2 | 0.2 | 10.3 |
| Visual, GLB | 0.6 | 0.9 | 1.9 | 0.2&nbsp;ms | 4.7 | 71&nbsp;ms | 0.5 | 0.2 | 8.9 |
| Visual, OBJ | 0.6 | 1.0 | 1.9 | 0.3&nbsp;ms | 5.0 | 2.1 | 0.8 | 0.2 | 11.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_Lat_Board_Deploy.kicad_pcb` |
|---|---|
| Folder | pq_latboard_deploy |
| Complexity | 271&nbsp;/&nbsp;1000 (size&nbsp;181, features&nbsp;90) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 14, 675, 21 |
| Triangles,&nbsp;simulation | 593,064 in 29 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">22&nbsp;MB</td><td align="right">421&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">84&nbsp;MB</td><td align="right">439&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">30&nbsp;MB</td><td align="right">418&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">64&nbsp;MB</td><td align="right">491&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">418&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">49&nbsp;MB</td><td align="right">412&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.66 pq_obc_comms

![pq_obc_comms: stages 4 and 6 take 51% to 83% of a run. Simulation, GLB takes 9.5 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.7 s. Simulation, OBJ takes 15 s. Visual, GLB takes 14 s. Visual, OBJ takes 18 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_pq-obc-comms.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.8 | 3.5 | 0.4&nbsp;ms | 3.9 | 0.2 | 0.6 | 0.3 | 9.5 |
| Simulation, STEP | 0.3 | 0.8 | 3.3 | 0.4&nbsp;ms | 3.9 | 3.0 | 0.5 | 0.3 | 12.1 |
| Simulation, STL | 0.3 | 0.8 | 3.4 | 0.4&nbsp;ms | 3.9 | 0.4 | 0.6 | 0.2 | 9.7 |
| Simulation, OBJ | 0.3 | 0.8 | 3.5 | 0.4&nbsp;ms | 4.0 | 5.2 | 0.5 | 0.2 | 14.6 |
| Visual, GLB | 0.3 | 0.8 | 3.5 | 0.7&nbsp;ms | 8.4 | 0.1 | 0.9 | 0.3 | 14.2 |
| Visual, OBJ | 0.3 | 0.8 | 3.5 | 0.6&nbsp;ms | 8.6 | 3.3 | 0.9 | 0.2 | 17.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `pq_obc_comms.kicad_pcb` |
|---|---|
| Folder | pq_obc_comms / pq_obc_comms |
| Complexity | 346&nbsp;/&nbsp;1000 (size&nbsp;231, features&nbsp;115) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 68, 538, 131 |
| Triangles,&nbsp;simulation | 1,237,286 in 105 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">42&nbsp;MB</td><td align="right">526&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">194&nbsp;MB</td><td align="right">606&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">62&nbsp;MB</td><td align="right">510&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">127&nbsp;MB</td><td align="right">855&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">28&nbsp;MB</td><td align="right">708&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">85&nbsp;MB</td><td align="right">738&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.67 PQ_PL1

![PQ_PL1: stages 4 and 6 take 50% to 81% of a run. Simulation, GLB takes 2.6 s. Simulation, STEP takes 3.6 s. Simulation, STL takes 2.6 s. Simulation, OBJ takes 3.8 s. Visual, GLB takes 4.1 s. Visual, OBJ takes 5.1 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ-PL1.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 97&nbsp;ms | 0.2 | 1.0 | 0.2&nbsp;ms | 0.9 | 47&nbsp;ms | 0.2 | 0.2 | 2.6 |
| Simulation, STEP | 97&nbsp;ms | 0.2 | 1.0 | 0.2&nbsp;ms | 0.9 | 1.1 | 0.2 | 0.2 | 3.6 |
| Simulation, STL | 0.1 | 0.2 | 1.0 | 0.3&nbsp;ms | 0.9 | 70&nbsp;ms | 0.2 | 0.2 | 2.6 |
| Simulation, OBJ | 0.1 | 0.2 | 1.0 | 0.2&nbsp;ms | 0.9 | 1.3 | 0.2 | 0.2 | 3.8 |
| Visual, GLB | 97&nbsp;ms | 0.2 | 1.0 | 0.2&nbsp;ms | 2.4 | 33&nbsp;ms | 0.3 | 0.2 | 4.1 |
| Visual, OBJ | 92&nbsp;ms | 0.2 | 1.0 | 0.2&nbsp;ms | 2.4 | 1.0 | 0.3 | 0.2 | 5.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_PL1.kicad_pcb` |
|---|---|
| Folder | pq_pl1 / PQ_PL1 |
| Complexity | 139&nbsp;/&nbsp;1000 (size&nbsp;74, features&nbsp;65) |
| KESE&nbsp;features | filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 5, 9, 0 |
| Triangles,&nbsp;simulation | 341,986 in 49 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">255&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">52&nbsp;MB</td><td align="right">272&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">17&nbsp;MB</td><td align="right">258&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">34&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.0&nbsp;MB</td><td align="right">266&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">23&nbsp;MB</td><td align="right">265&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.68 PCB_P L2_PCB_2022-10-05

![PCB_P L2_PCB_2022-10-05: stages 4 and 6 take 52% to 82% of a run. Simulation, GLB takes 8.7 s. Simulation, STEP takes 11 s. Simulation, STL takes 8.4 s. Simulation, OBJ takes 12 s. Visual, GLB takes 13 s. Visual, OBJ takes 14 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PCB-P-L2-PCB-2022-10-05.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.1 | 3.3 | 0.4&nbsp;ms | 3.1 | 0.1 | 0.4 | 0.2 | 8.7 |
| Simulation, STEP | 0.3 | 1.1 | 3.2 | 0.3&nbsp;ms | 3.0 | 2.2 | 0.4 | 0.2 | 10.6 |
| Simulation, STL | 0.4 | 1.0 | 3.2 | 0.3&nbsp;ms | 3.0 | 0.2 | 0.4 | 0.2 | 8.4 |
| Simulation, OBJ | 0.3 | 1.1 | 3.3 | 0.3&nbsp;ms | 3.1 | 3.9 | 0.4 | 0.2 | 12.3 |
| Visual, GLB | 0.4 | 1.1 | 3.4 | 0.4&nbsp;ms | 6.9 | 56&nbsp;ms | 0.5 | 0.2 | 12.5 |
| Visual, OBJ | 0.3 | 1.2 | 3.2 | 0.3&nbsp;ms | 6.9 | 2.0 | 0.6 | 0.2 | 14.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PCB_P L2_PCB_2022-10-05.kicad_pcb` |
|---|---|
| Folder | pq_pl2 / Imports |
| Complexity | 261&nbsp;/&nbsp;1000 (size&nbsp;181, features&nbsp;80) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, filled zones,<br>copper drawings,<br>curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 66, 267, 78 |
| Triangles,&nbsp;simulation | 791,228 in 117 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">400&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">134&nbsp;MB</td><td align="right">458&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">40&nbsp;MB</td><td align="right">393&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">80&nbsp;MB</td><td align="right">571&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">450&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">42&nbsp;MB</td><td align="right">407&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.69 PQ_PL2

![PQ_PL2: stages 4 and 6 take 49% to 78% of a run. Simulation, GLB takes 12 s. Simulation, STEP takes 15 s. Simulation, STL takes 13 s. Simulation, OBJ takes 19 s. Visual, GLB takes 18 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ-PL2.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 1.5 | 4.5 | 0.7&nbsp;ms | 4.5 | 0.2 | 0.5 | 0.2 | 12.4 |
| Simulation, STEP | 0.9 | 1.6 | 4.5 | 0.6&nbsp;ms | 4.7 | 3.0 | 0.5 | 0.2 | 15.4 |
| Simulation, STL | 0.9 | 1.7 | 4.5 | 0.6&nbsp;ms | 4.5 | 0.4 | 0.5 | 0.2 | 12.8 |
| Simulation, OBJ | 0.9 | 1.5 | 4.7 | 0.5&nbsp;ms | 4.7 | 6.5 | 0.5 | 0.3 | 19.1 |
| Visual, GLB | 0.9 | 1.5 | 4.6 | 0.4&nbsp;ms | 9.4 | 0.1 | 1.1 | 0.2 | 17.8 |
| Visual, OBJ | 0.9 | 1.5 | 4.8 | 0.6&nbsp;ms | 9.5 | 4.8 | 1.4 | 0.2 | 23.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_PL2.kicad_pcb` |
|---|---|
| Folder | pq_pl2 / PQ_PL2 |
| Complexity | 319&nbsp;/&nbsp;1000 (size&nbsp;189, features&nbsp;130) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 72, 364, 136 |
| Triangles,&nbsp;simulation | 1,196,648 in 104 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">42&nbsp;MB</td><td align="right">510&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">159&nbsp;MB</td><td align="right">662&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">60&nbsp;MB</td><td align="right">510&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">125&nbsp;MB</td><td align="right">856&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">599&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">90&nbsp;MB</td><td align="right">728&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.70 PQ1_TopBoard

![PQ1_TopBoard: stages 4 and 6 take 55% to 75% of a run. Simulation, GLB takes 9.5 s. Simulation, STEP takes 12 s. Simulation, STL takes 9.8 s. Simulation, OBJ takes 12 s. Visual, GLB takes 9.9 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ1-TopBoard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.9 | 1.1 | 2.5 | 0.2&nbsp;ms | 4.5 | 77&nbsp;ms | 0.2 | 0.2 | 9.5 |
| Simulation, STEP | 0.8 | 1.0 | 2.4 | 0.2&nbsp;ms | 4.5 | 3.3 | 0.2 | 0.2 | 12.4 |
| Simulation, STL | 0.8 | 1.0 | 2.5 | 0.1&nbsp;ms | 4.8 | 0.3 | 0.2 | 0.3 | 9.8 |
| Simulation, OBJ | 0.8 | 1.0 | 2.5 | 0.2&nbsp;ms | 4.7 | 2.5 | 0.2 | 0.3 | 11.9 |
| Visual, GLB | 0.8 | 1.0 | 2.6 | 0.2&nbsp;ms | 4.8 | 77&nbsp;ms | 0.4 | 0.2 | 9.9 |
| Visual, OBJ | 0.8 | 1.0 | 2.7 | 0.2&nbsp;ms | 4.8 | 2.4 | 0.6 | 0.2 | 12.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ1_TopBoard.kicad_pcb` |
|---|---|
| Folder | pq_topboard / PQ1_TopBoard |
| Complexity | 211&nbsp;/&nbsp;1000 (size&nbsp;121, features&nbsp;90) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 10, 64, 17 |
| Triangles,&nbsp;simulation | 405,998 in 22 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">390&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">66&nbsp;MB</td><td align="right">397&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">20&nbsp;MB</td><td align="right">387&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">44&nbsp;MB</td><td align="right">388&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">382&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">41&nbsp;MB</td><td align="right">408&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.71 PQ1_TopBoardV9

![PQ1_TopBoardV9: stages 4 and 6 take 56% to 76% of a run. Simulation, GLB takes 8.6 s. Simulation, STEP takes 11 s. Simulation, STL takes 8.4 s. Simulation, OBJ takes 11 s. Visual, GLB takes 9.7 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ1-TopBoardV9.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 1.0 | 2.6 | 0.2&nbsp;ms | 3.8 | 94&nbsp;ms | 0.3 | 0.2 | 8.6 |
| Simulation, STEP | 0.7 | 0.9 | 2.5 | 0.2&nbsp;ms | 3.9 | 2.9 | 0.2 | 0.2 | 11.3 |
| Simulation, STL | 0.7 | 0.9 | 2.4 | 0.2&nbsp;ms | 3.8 | 0.1 | 0.2 | 0.2 | 8.4 |
| Simulation, OBJ | 0.7 | 0.9 | 2.4 | 0.2&nbsp;ms | 3.8 | 2.8 | 0.2 | 0.2 | 11.1 |
| Visual, GLB | 0.7 | 0.9 | 2.4 | 0.2&nbsp;ms | 4.9 | 68&nbsp;ms | 0.5 | 0.2 | 9.7 |
| Visual, OBJ | 0.7 | 0.9 | 2.4 | 0.2&nbsp;ms | 5.1 | 2.5 | 0.8 | 0.2 | 12.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ1_TopBoardV9.kicad_pcb` |
|---|---|
| Folder | pq_topboard_lband |
| Complexity | 251&nbsp;/&nbsp;1000 (size&nbsp;136, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper text, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 14, 89, 50 |
| Triangles,&nbsp;simulation | 494,486 in 21 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">397&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">78&nbsp;MB</td><td align="right">395&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">25&nbsp;MB</td><td align="right">394&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">53&nbsp;MB</td><td align="right">427&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">440&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">48&nbsp;MB</td><td align="right">446&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.72 PQ_MagYBoard

![PQ_MagYBoard: stages 4 and 6 take 43% to 73% of a run. Simulation, GLB takes 3.7 s. Simulation, STEP takes 5.5 s. Simulation, STL takes 3.8 s. Simulation, OBJ takes 4.6 s. Visual, GLB takes 4.8 s. Visual, OBJ takes 5.8 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/pocat-hw_PQ-MagYBoard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 1.0 | 0.1&nbsp;ms | 1.5 | 46&nbsp;ms | 0.1 | 0.2 | 3.7 |
| Simulation, STEP | 0.2 | 0.6 | 1.0 | 0.1&nbsp;ms | 1.4 | 2.1 | 0.1 | 0.2 | 5.5 |
| Simulation, STL | 0.2 | 0.6 | 1.0 | 0.1&nbsp;ms | 1.5 | 80&nbsp;ms | 0.1 | 0.2 | 3.8 |
| Simulation, OBJ | 0.2 | 0.6 | 1.0 | 0.1&nbsp;ms | 1.3 | 1.2 | 92&nbsp;ms | 0.2 | 4.6 |
| Visual, GLB | 0.2 | 0.6 | 0.9 | 0.1&nbsp;ms | 2.6 | 41&nbsp;ms | 0.3 | 0.2 | 4.8 |
| Visual, OBJ | 0.2 | 0.6 | 1.0 | 0.1&nbsp;ms | 2.5 | 1.1 | 0.3 | 0.2 | 5.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nanosatlab/pocat-hw](https://github.com/nanosatlab/pocat-hw)<br>Board: `PQ_MagYBoard.kicad_pcb` |
|---|---|
| Folder | pq_ymag_board / PQ_MAGY / PQ_MagYBoard |
| Complexity | 226&nbsp;/&nbsp;1000 (size&nbsp;156, features&nbsp;70) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 468, 5 |
| Triangles,&nbsp;simulation | 248,848 in 13 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">9.1&nbsp;MB</td><td align="right">273&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">39&nbsp;MB</td><td align="right">289&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">12&nbsp;MB</td><td align="right">279&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">27&nbsp;MB</td><td align="right">278&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.7&nbsp;MB</td><td align="right">265&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">253&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.73 Control_Boards

![Control_Boards: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 47 s. Simulation, STEP takes 58 s. Simulation, STL takes 48 s. Simulation, OBJ takes 71 s. Visual, GLB takes 79 s. Visual, OBJ takes 94 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/open-source-rover_Control-Boards.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.2 | 4.3 | 21.1 | 2&nbsp;ms | 16.9 | 0.9 | 2.4 | 0.3 | 47.1 |
| Simulation, STEP | 1.1 | 4.5 | 20.4 | 3&nbsp;ms | 16.3 | 12.6 | 2.6 | 0.4 | 57.9 |
| Simulation, STL | 1.1 | 4.3 | 20.4 | 2&nbsp;ms | 17.1 | 1.9 | 2.5 | 0.4 | 47.9 |
| Simulation, OBJ | 1.2 | 4.1 | 20.4 | 2&nbsp;ms | 16.2 | 25.9 | 2.5 | 0.3 | 70.6 |
| Visual, GLB | 1.0 | 4.3 | 20.9 | 1&nbsp;ms | 45.2 | 0.6 | 6.3 | 0.4 | 78.8 |
| Visual, OBJ | 1.1 | 4.6 | 21.3 | 2&nbsp;ms | 42.9 | 17.4 | 6.0 | 0.3 | 93.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nasa-jpl/open-source-rover](https://github.com/nasa-jpl/open-source-rover)<br>Board: `Control_Boards.kicad_pcb` |
|---|---|
| Folder | electrical / pcb / control_board |
| Complexity | 241&nbsp;/&nbsp;1000 (size&nbsp;206, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 112, 3,720, 265 |
| Triangles,&nbsp;simulation | 5,125,220 in 242 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">173&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">782&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">256&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">545&nbsp;MB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">123&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">392&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.74 groundlark-field-head

![groundlark-field-head: stages 4 and 6 take 49% to 82% of a run. Simulation, GLB takes 5.8 s. Simulation, STEP takes 7.7 s. Simulation, STL takes 5.7 s. Simulation, OBJ takes 9.3 s. Visual, GLB takes 8.6 s. Visual, OBJ takes 10 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_groundlark-field-head.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 2.2 | 0.2&nbsp;ms | 2.1 | 0.1 | 0.4 | 0.2 | 5.8 |
| Simulation, STEP | 0.2 | 0.6 | 2.3 | 0.2&nbsp;ms | 2.3 | 1.7 | 0.4 | 0.2 | 7.7 |
| Simulation, STL | 0.2 | 0.6 | 2.0 | 0.2&nbsp;ms | 2.1 | 0.2 | 0.4 | 0.2 | 5.7 |
| Simulation, OBJ | 0.2 | 0.6 | 2.3 | 0.2&nbsp;ms | 2.2 | 3.3 | 0.4 | 0.2 | 9.3 |
| Visual, GLB | 0.2 | 0.6 | 2.2 | 0.2&nbsp;ms | 4.8 | 61&nbsp;ms | 0.5 | 0.2 | 8.6 |
| Visual, OBJ | 0.2 | 0.6 | 2.3 | 0.3&nbsp;ms | 4.9 | 1.8 | 0.4 | 0.2 | 10.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `groundlark-field-head.kicad_pcb` |
|---|---|
| Folder | hw / burrowlark-usb / boards / groundlark-field-head |
| Complexity | 321&nbsp;/&nbsp;1000 (size&nbsp;216, features&nbsp;105) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 34, 455, 46 |
| Triangles,&nbsp;simulation | 742,580 in 66 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">24&nbsp;MB</td><td align="right">347&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">86&nbsp;MB</td><td align="right">402&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">37&nbsp;MB</td><td align="right">359&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">74&nbsp;MB</td><td align="right">541&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">13&nbsp;MB</td><td align="right">355&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">39&nbsp;MB</td><td align="right">382&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.75 field_head

![field_head: stages 4 and 6 take 49% to 80% of a run. Simulation, GLB takes 3.7 s. Simulation, STEP takes 5.1 s. Simulation, STL takes 3.9 s. Simulation, OBJ takes 5.4 s. Visual, GLB takes 5.8 s. Visual, OBJ takes 7.2 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_field-head.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.4 | 1.6 | 0.4&nbsp;ms | 1.1 | 83&nbsp;ms | 0.2 | 0.2 | 3.7 |
| Simulation, STEP | 0.1 | 0.5 | 1.7 | 0.4&nbsp;ms | 1.1 | 1.3 | 0.2 | 0.2 | 5.1 |
| Simulation, STL | 0.1 | 0.4 | 1.7 | 0.3&nbsp;ms | 1.2 | 0.1 | 0.2 | 0.2 | 3.9 |
| Simulation, OBJ | 0.1 | 0.4 | 1.5 | 0.3&nbsp;ms | 1.1 | 1.8 | 0.2 | 0.2 | 5.4 |
| Visual, GLB | 0.1 | 0.4 | 1.8 | 0.3&nbsp;ms | 2.9 | 38&nbsp;ms | 0.3 | 0.2 | 5.8 |
| Visual, OBJ | 0.1 | 0.5 | 1.8 | 0.3&nbsp;ms | 3.0 | 1.2 | 0.4 | 0.2 | 7.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `field_head.kicad_pcb` |
|---|---|
| Folder | hw / burrowlark-usb / layout / field_head |
| Complexity | 165&nbsp;/&nbsp;1000 (size&nbsp;95, features&nbsp;70) |
| KESE&nbsp;features | slotted holes, rounded,<br>trapezoid or chamfered pads,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 34, 0, 0 |
| Triangles,&nbsp;simulation | 398,116 in 64 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">268&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">56&nbsp;MB</td><td align="right">292&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">20&nbsp;MB</td><td align="right">291&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">41&nbsp;MB</td><td align="right">322&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.6&nbsp;MB</td><td align="right">301&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">25&nbsp;MB</td><td align="right">297&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.76 groundlark-daqhat-01

![groundlark-daqhat-01: stages 4 and 6 take 43% to 83% of a run. Simulation, GLB takes 40 s. Simulation, STEP takes 53 s. Simulation, STL takes 43 s. Simulation, OBJ takes 70 s. Visual, GLB takes 76 s. Visual, OBJ takes 93 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_groundlark-daqhat-01.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.3 | 5.4 | 12.3 | 0.9&nbsp;ms | 17.6 | 1.2 | 2.0 | 0.3 | 40.1 |
| Simulation, STEP | 1.2 | 5.5 | 12.9 | 1&nbsp;ms | 18.7 | 12.2 | 2.2 | 0.4 | 53.0 |
| Simulation, STL | 1.3 | 5.5 | 12.7 | 1&nbsp;ms | 18.2 | 2.2 | 2.2 | 0.4 | 42.6 |
| Simulation, OBJ | 1.4 | 5.2 | 12.4 | 1&nbsp;ms | 17.6 | 30.7 | 2.3 | 0.4 | 69.9 |
| Visual, GLB | 1.2 | 5.4 | 12.0 | 1&nbsp;ms | 51.2 | 0.5 | 5.5 | 0.3 | 76.2 |
| Visual, OBJ | 1.3 | 5.3 | 13.3 | 1&nbsp;ms | 51.3 | 15.5 | 5.8 | 0.3 | 92.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `groundlark-daqhat-01.kicad_pcb` |
|---|---|
| Folder | hw / groundlark-fpga-hat / boards / groundlark-daqhat-01 |
| Complexity | 417&nbsp;/&nbsp;1000 (size&nbsp;297, features&nbsp;120) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 190, 12,366, 745 |
| Triangles,&nbsp;simulation | 5,819,912 in 381 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">195&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">676&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">291&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">625&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">106&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">343&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.77 pi-trenz-stack-concept

![pi-trenz-stack-concept: stages 4 and 6 take 41% to 85% of a run. Simulation, GLB takes 39 s. Simulation, STEP takes 49 s. Simulation, STL takes 39 s. Simulation, OBJ takes 71 s. Visual, GLB takes 74 s. Visual, OBJ takes 85 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_pi-trenz-stack-concept.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.2 | 5.1 | 12.2 | 0.9&nbsp;ms | 17.3 | 0.8 | 2.1 | 0.3 | 39.1 |
| Simulation, STEP | 1.3 | 5.0 | 12.0 | 0.8&nbsp;ms | 17.3 | 11.2 | 2.1 | 0.3 | 49.1 |
| Simulation, STL | 1.2 | 4.9 | 12.1 | 0.8&nbsp;ms | 17.0 | 1.7 | 2.1 | 0.3 | 39.5 |
| Simulation, OBJ | 1.3 | 5.4 | 12.0 | 0.9&nbsp;ms | 17.2 | 32.2 | 2.1 | 0.3 | 70.6 |
| Visual, GLB | 1.3 | 5.0 | 12.2 | 0.9&nbsp;ms | 50.6 | 0.4 | 4.3 | 0.3 | 74.1 |
| Visual, OBJ | 1.5 | 5.0 | 12.1 | 0.9&nbsp;ms | 45.4 | 16.4 | 4.6 | 0.3 | 85.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `pi-trenz-stack-concept.kicad_pcb` |
|---|---|
| Folder | hw / groundlark-fpga-hat / boards / groundlark-daqhat-01 |
| Complexity | 417&nbsp;/&nbsp;1000 (size&nbsp;297, features&nbsp;120) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 190, 12,366, 745 |
| Triangles,&nbsp;simulation | 5,819,912 in 381 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">195&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">676&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">291&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">625&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">106&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">343&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.78 stack-exploded

![stack-exploded: stages 4 and 6 take 45% to 82% of a run. Simulation, GLB takes 39 s. Simulation, STEP takes 49 s. Simulation, STL takes 40 s. Simulation, OBJ takes 65 s. Visual, GLB takes 71 s. Visual, OBJ takes 87 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_stack-exploded.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.1 | 4.9 | 11.7 | 1&nbsp;ms | 17.7 | 0.9 | 2.0 | 0.3 | 38.6 |
| Simulation, STEP | 1.1 | 5.0 | 11.8 | 2&nbsp;ms | 17.6 | 11.2 | 2.0 | 0.3 | 49.1 |
| Simulation, STL | 1.2 | 5.2 | 11.6 | 1&nbsp;ms | 17.3 | 2.0 | 2.1 | 0.3 | 39.8 |
| Simulation, OBJ | 1.2 | 4.5 | 12.3 | 1&nbsp;ms | 17.0 | 27.4 | 2.2 | 0.3 | 64.9 |
| Visual, GLB | 1.2 | 5.4 | 11.7 | 1&nbsp;ms | 47.1 | 0.4 | 5.2 | 0.3 | 71.4 |
| Visual, OBJ | 1.2 | 5.1 | 11.4 | 1&nbsp;ms | 47.7 | 15.4 | 6.4 | 0.3 | 87.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `stack-exploded.kicad_pcb` |
|---|---|
| Folder | hw / groundlark-fpga-hat / boards / groundlark-daqhat-01 |
| Complexity | 417&nbsp;/&nbsp;1000 (size&nbsp;297, features&nbsp;120) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 190, 12,366, 745 |
| Triangles,&nbsp;simulation | 5,819,912 in 381 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">195&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">676&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">291&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">625&nbsp;MB</td><td align="right">3.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">106&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">343&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.79 stack-service-envelopes

![stack-service-envelopes: stages 4 and 6 take 42% to 84% of a run. Simulation, GLB takes 50 s. Simulation, STEP takes 59 s. Simulation, STL takes 48 s. Simulation, OBJ takes 81 s. Visual, GLB takes 82 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_stack-service-envelopes.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.5 | 6.0 | 16.2 | 2&nbsp;ms | 21.9 | 1.2 | 2.5 | 0.3 | 49.7 |
| Simulation, STEP | 1.5 | 6.2 | 14.3 | 1&nbsp;ms | 20.2 | 13.4 | 2.5 | 0.4 | 58.5 |
| Simulation, STL | 1.5 | 6.4 | 14.7 | 1&nbsp;ms | 21.0 | 1.9 | 2.4 | 0.4 | 48.3 |
| Simulation, OBJ | 1.5 | 5.9 | 14.7 | 2&nbsp;ms | 19.8 | 36.7 | 2.5 | 0.4 | 81.3 |
| Visual, GLB | 1.6 | 5.8 | 13.8 | 1&nbsp;ms | 55.2 | 0.5 | 5.2 | 0.3 | 82.3 |
| Visual, OBJ | 1.5 | 5.8 | 14.5 | 1.0&nbsp;ms | 54.6 | 18.3 | 5.5 | 0.3 | 100.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `stack-service-envelopes.kicad_pcb` |
|---|---|
| Folder | hw / groundlark-fpga-hat / boards / groundlark-daqhat-01 |
| Complexity | 417&nbsp;/&nbsp;1000 (size&nbsp;297, features&nbsp;120) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 190, 12,366, 745 |
| Triangles,&nbsp;simulation | 5,819,912 in 381 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">195&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">676&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">291&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">625&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">106&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">343&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.80 trenz-mounted

![trenz-mounted: stages 4 and 6 take 43% to 84% of a run. Simulation, GLB takes 46 s. Simulation, STEP takes 57 s. Simulation, STL takes 45 s. Simulation, OBJ takes 80 s. Visual, GLB takes 81 s. Visual, OBJ takes 99 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_trenz-mounted.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.5 | 6.2 | 14.6 | 1&nbsp;ms | 20.4 | 1.0 | 2.4 | 0.4 | 46.4 |
| Simulation, STEP | 1.4 | 5.9 | 14.1 | 1&nbsp;ms | 19.3 | 13.8 | 2.4 | 0.4 | 57.2 |
| Simulation, STL | 1.5 | 5.8 | 14.1 | 1&nbsp;ms | 19.1 | 2.0 | 2.3 | 0.4 | 45.3 |
| Simulation, OBJ | 1.6 | 6.2 | 14.7 | 1&nbsp;ms | 19.7 | 35.4 | 2.5 | 0.3 | 80.4 |
| Visual, GLB | 1.4 | 6.0 | 14.2 | 1.0&nbsp;ms | 53.9 | 0.5 | 5.1 | 0.3 | 81.4 |
| Visual, OBJ | 1.6 | 5.9 | 14.1 | 1&nbsp;ms | 52.3 | 19.7 | 5.0 | 0.3 | 98.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `trenz-mounted.kicad_pcb` |
|---|---|
| Folder | hw / groundlark-fpga-hat / boards / groundlark-daqhat-01 |
| Complexity | 417&nbsp;/&nbsp;1000 (size&nbsp;297, features&nbsp;120) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 190, 12,366, 745 |
| Triangles,&nbsp;simulation | 5,819,912 in 381 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">195&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">676&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">291&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">625&nbsp;MB</td><td align="right">3.7&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">106&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">343&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.81 trenz_hat

![trenz_hat: stages 4 and 6 take 40% to 64% of a run. Simulation, GLB takes 18 s. Simulation, STEP takes 20 s. Simulation, STL takes 17 s. Simulation, OBJ takes 22 s. Visual, GLB takes 25 s. Visual, OBJ takes 30 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_trenz-hat.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 7.3 | 5.2 | 0.7&nbsp;ms | 4.4 | 0.2 | 0.4 | 0.2 | 18.3 |
| Simulation, STEP | 0.4 | 7.0 | 4.8 | 0.6&nbsp;ms | 4.1 | 3.4 | 0.4 | 0.3 | 20.4 |
| Simulation, STL | 0.4 | 7.2 | 4.6 | 1&nbsp;ms | 3.9 | 0.3 | 0.4 | 0.2 | 17.1 |
| Simulation, OBJ | 0.4 | 7.0 | 4.8 | 0.7&nbsp;ms | 4.0 | 5.4 | 0.4 | 0.2 | 22.1 |
| Visual, GLB | 0.4 | 7.0 | 4.7 | 0.6&nbsp;ms | 11.5 | 0.1 | 1.2 | 0.2 | 25.1 |
| Visual, OBJ | 0.4 | 7.0 | 4.7 | 0.6&nbsp;ms | 11.5 | 4.6 | 1.5 | 0.2 | 29.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `trenz_hat.kicad_pcb` |
|---|---|
| Folder | hw / groundlark-fpga-hat / layout / trenz_hat |
| Complexity | 199&nbsp;/&nbsp;1000 (size&nbsp;114, features&nbsp;85) |
| KESE&nbsp;features | custom pads, rounded,<br>trapezoid or chamfered pads,<br>copper drawings, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 190, 0, 0 |
| Triangles,&nbsp;simulation | 1,028,724 in 290 parts |
| Note | mostly unrouted |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">36&nbsp;MB</td><td align="right">496&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">145&nbsp;MB</td><td align="right">605&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">51&nbsp;MB</td><td align="right">498&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">107&nbsp;MB</td><td align="right">719&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">630&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">89&nbsp;MB</td><td align="right">781&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.82 raspberrypi_hat

![raspberrypi_hat: stages 4 and 6 take 50% to 83% of a run. Simulation, GLB takes 4.2 s. Simulation, STEP takes 5.7 s. Simulation, STL takes 4.0 s. Simulation, OBJ takes 6.4 s. Visual, GLB takes 5.3 s. Visual, OBJ takes 6.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_raspberrypi-hat.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.8 | 0.2&nbsp;ms | 1.4 | 70&nbsp;ms | 0.3 | 0.2 | 4.2 |
| Simulation, STEP | 0.1 | 0.3 | 1.9 | 0.2&nbsp;ms | 1.5 | 1.5 | 0.2 | 0.2 | 5.7 |
| Simulation, STL | 0.1 | 0.3 | 1.7 | 0.2&nbsp;ms | 1.3 | 88&nbsp;ms | 0.2 | 0.2 | 4.0 |
| Simulation, OBJ | 0.1 | 0.3 | 1.9 | 0.2&nbsp;ms | 1.4 | 2.3 | 0.2 | 0.2 | 6.4 |
| Visual, GLB | 0.1 | 0.3 | 1.8 | 0.3&nbsp;ms | 2.6 | 34&nbsp;ms | 0.2 | 0.2 | 5.3 |
| Visual, OBJ | 0.1 | 0.3 | 1.8 | 0.2&nbsp;ms | 2.6 | 1.2 | 0.2 | 0.2 | 6.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `raspberrypi_hat.kicad_pcb` |
|---|---|
| Folder | hw / shared / reference |
| Complexity | 161&nbsp;/&nbsp;1000 (size&nbsp;131, features&nbsp;30) |
| KESE&nbsp;features | filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 14, 63, 0 |
| Triangles,&nbsp;simulation | 438,762 in 24 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">271&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">62&nbsp;MB</td><td align="right">288&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">22&nbsp;MB</td><td align="right">266&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">44&nbsp;MB</td><td align="right">338&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.7&nbsp;MB</td><td align="right">258&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">22&nbsp;MB</td><td align="right">257&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.83 skylark-usb

![skylark-usb: stages 4 and 6 take 45% to 81% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 15 s. Simulation, STL takes 11 s. Simulation, OBJ takes 18 s. Visual, GLB takes 16 s. Visual, OBJ takes 22 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_skylark-usb.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.1 | 3.3 | 0.4&nbsp;ms | 4.5 | 0.2 | 0.7 | 0.3 | 10.6 |
| Simulation, STEP | 0.4 | 1.2 | 3.4 | 0.3&nbsp;ms | 5.0 | 4.0 | 0.7 | 0.3 | 15.0 |
| Simulation, STL | 0.4 | 1.1 | 3.4 | 0.4&nbsp;ms | 5.0 | 0.4 | 0.7 | 0.3 | 11.3 |
| Simulation, OBJ | 0.5 | 1.2 | 3.3 | 0.4&nbsp;ms | 4.7 | 7.3 | 0.7 | 0.2 | 17.9 |
| Visual, GLB | 0.4 | 1.1 | 3.3 | 0.4&nbsp;ms | 9.9 | 0.1 | 1.2 | 0.2 | 16.3 |
| Visual, OBJ | 0.4 | 1.2 | 3.4 | 0.4&nbsp;ms | 9.8 | 5.4 | 1.2 | 0.2 | 21.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `skylark-usb.kicad_pcb` |
|---|---|
| Folder | hw / skylark-usb / boards / skylark-usb |
| Complexity | 350&nbsp;/&nbsp;1000 (size&nbsp;245, features&nbsp;105) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 121, 1,037, 159 |
| Triangles,&nbsp;simulation | 1,271,024 in 109 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">43&nbsp;MB</td><td align="right">524&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">175&nbsp;MB</td><td align="right">671&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">64&nbsp;MB</td><td align="right">530&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">130&nbsp;MB</td><td align="right">861&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">735&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">93&nbsp;MB</td><td align="right">725&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.84 skylark

![skylark: stages 4 and 6 take 48% to 78% of a run. Simulation, GLB takes 6.0 s. Simulation, STEP takes 8.0 s. Simulation, STL takes 5.7 s. Simulation, OBJ takes 8.6 s. Visual, GLB takes 10 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/groundlark_skylark.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 0.9 | 2.0 | 0.3&nbsp;ms | 2.1 | 83&nbsp;ms | 0.2 | 0.2 | 6.0 |
| Simulation, STEP | 0.3 | 0.9 | 2.3 | 0.3&nbsp;ms | 2.0 | 1.9 | 0.2 | 0.2 | 8.0 |
| Simulation, STL | 0.3 | 0.9 | 2.0 | 0.2&nbsp;ms | 1.8 | 0.2 | 0.2 | 0.2 | 5.7 |
| Simulation, OBJ | 0.4 | 1.0 | 2.1 | 0.3&nbsp;ms | 2.0 | 2.7 | 0.2 | 0.2 | 8.6 |
| Visual, GLB | 0.3 | 1.0 | 2.2 | 0.6&nbsp;ms | 5.8 | 96&nbsp;ms | 0.7 | 0.3 | 10.3 |
| Visual, OBJ | 0.3 | 0.9 | 2.1 | 0.3&nbsp;ms | 6.1 | 2.3 | 0.8 | 0.2 | 12.8 |

<table align="center"><tr><td valign="top">

| Board | Repo: [naturalhazardscience/groundlark](https://github.com/naturalhazardscience/groundlark)<br>Board: `skylark.kicad_pcb` |
|---|---|
| Folder | hw / skylark-usb / layout / skylark |
| Complexity | 179&nbsp;/&nbsp;1000 (size&nbsp;109, features&nbsp;70) |
| KESE&nbsp;features | slotted holes, rounded,<br>trapezoid or chamfered pads,<br>stack-up, dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 121, 0, 0 |
| Triangles,&nbsp;simulation | 507,884 in 104 parts |
| Note | mostly unrouted |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">18&nbsp;MB</td><td align="right">344&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">72&nbsp;MB</td><td align="right">413&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">25&nbsp;MB</td><td align="right">340&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">53&nbsp;MB</td><td align="right">410&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">16&nbsp;MB</td><td align="right">436&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">46&nbsp;MB</td><td align="right">469&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.85 C64C-250469-01-A

![C64C-250469-01-A: stages 4 and 6 take 55% to 86% of a run. Simulation, GLB takes 69 s. Simulation, STEP takes 86 s. Simulation, STL takes 70 s. Simulation, OBJ takes 2 min. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/Commodore64C_C64C-250469-01-A.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 5.9 | 32.6 | 1&nbsp;ms | 25.3 | 1.1 | 3.2 | 0.3 | 69.4 |
| Simulation, STEP | 1.0 | 5.9 | 32.7 | 0.9&nbsp;ms | 25.2 | 17.2 | 3.4 | 0.3 | 85.7 |
| Simulation, STL | 0.9 | 5.9 | 32.2 | 0.8&nbsp;ms | 25.0 | 2.3 | 3.6 | 0.3 | 70.4 |
| Simulation, OBJ | 0.9 | 5.8 | 32.4 | 0.9&nbsp;ms | 24.6 | 35.7 | 3.3 | 0.3 | 103.1 |
| Visual, GLB | 1.0 | 5.8 | 33.1 | 1&nbsp;ms | 55.0 | 0.6 | 6.6 | 0.3 | 102.4 |
| Visual, OBJ | 1.0 | 5.9 | 33.6 | 0.9&nbsp;ms | 54.9 | 20.3 | 6.3 | 0.3 | 122.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [NeedfulThings/Commodore64C](https://github.com/NeedfulThings/Commodore64C)<br>Board: `C64C-250469-01-A.kicad_pcb` |
|---|---|
| Folder | 250469-RevA |
| Complexity | 257&nbsp;/&nbsp;1000 (size&nbsp;202, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 131, 2,533, 241 |
| Triangles,&nbsp;simulation | 6,379,874 in 215 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">218&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.1&nbsp;GB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">319&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">683&nbsp;MB</td><td align="right">4.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">131&nbsp;MB</td><td align="right">2.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">415&nbsp;MB</td><td align="right">2.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.86 ethersweep

![ethersweep: stages 4 and 6 take 56% to 82% of a run. Simulation, GLB takes 21 s. Simulation, STEP takes 26 s. Simulation, STL takes 22 s. Simulation, OBJ takes 30 s. Visual, GLB takes 31 s. Visual, OBJ takes 37 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/ethersweep_electronic-design-development-ethersweep402_ethersweep.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 2.2 | 9.7 | 0.4&nbsp;ms | 7.2 | 0.3 | 0.9 | 0.3 | 21.1 |
| Simulation, STEP | 0.7 | 2.3 | 9.9 | 0.4&nbsp;ms | 6.9 | 4.9 | 0.8 | 0.3 | 25.7 |
| Simulation, STL | 0.7 | 2.2 | 9.7 | 0.9&nbsp;ms | 7.1 | 0.8 | 0.8 | 0.3 | 21.6 |
| Simulation, OBJ | 0.7 | 2.0 | 9.5 | 0.6&nbsp;ms | 7.2 | 9.1 | 0.9 | 0.2 | 29.6 |
| Visual, GLB | 0.7 | 2.2 | 9.6 | 0.4&nbsp;ms | 15.5 | 0.2 | 2.2 | 0.2 | 30.7 |
| Visual, OBJ | 0.7 | 2.1 | 9.5 | 0.9&nbsp;ms | 15.6 | 6.7 | 2.3 | 0.2 | 37.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Neumi/ethersweep](https://github.com/Neumi/ethersweep)<br>Board: `ethersweep.kicad_pcb` |
|---|---|
| Folder | electronic_design / development / ethersweep402 |
| Complexity | 365&nbsp;/&nbsp;1000 (size&nbsp;240, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 105, 1,249, 325 |
| Triangles,&nbsp;simulation | 1,969,696 in 117 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">69&nbsp;MB</td><td align="right">769&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">359&nbsp;MB</td><td align="right">856&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">98&nbsp;MB</td><td align="right">738&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">208&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">49&nbsp;MB</td><td align="right">861&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">149&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.87 ethersweep

![ethersweep: stages 4 and 6 take 52% to 83% of a run. Simulation, GLB takes 20 s. Simulation, STEP takes 24 s. Simulation, STL takes 20 s. Simulation, OBJ takes 30 s. Visual, GLB takes 29 s. Visual, OBJ takes 36 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/ethersweep_electronic-design-development-ethersweep406_ethersweep.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 2.2 | 8.9 | 0.6&nbsp;ms | 6.7 | 0.3 | 0.7 | 0.2 | 19.8 |
| Simulation, STEP | 0.7 | 2.2 | 9.0 | 0.5&nbsp;ms | 6.9 | 4.7 | 0.7 | 0.3 | 24.4 |
| Simulation, STL | 0.7 | 2.2 | 9.1 | 0.5&nbsp;ms | 6.8 | 0.6 | 0.8 | 0.2 | 20.5 |
| Simulation, OBJ | 0.7 | 2.3 | 9.0 | 0.5&nbsp;ms | 6.8 | 10.7 | 0.8 | 0.2 | 30.4 |
| Visual, GLB | 0.7 | 2.3 | 8.9 | 0.7&nbsp;ms | 15.1 | 0.2 | 1.5 | 0.2 | 28.9 |
| Visual, OBJ | 0.7 | 2.4 | 9.3 | 0.5&nbsp;ms | 15.5 | 6.2 | 1.9 | 0.2 | 36.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Neumi/ethersweep](https://github.com/Neumi/ethersweep)<br>Board: `ethersweep.kicad_pcb` |
|---|---|
| Folder | electronic_design / development / ethersweep406 |
| Complexity | 381&nbsp;/&nbsp;1000 (size&nbsp;256, features&nbsp;125) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 105, 1,174, 149 |
| Triangles,&nbsp;simulation | 2,029,642 in 138 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">70&nbsp;MB</td><td align="right">655&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">302&nbsp;MB</td><td align="right">787&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">101&nbsp;MB</td><td align="right">712&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">214&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">40&nbsp;MB</td><td align="right">847&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">122&nbsp;MB</td><td align="right">940&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.88 ethersweep

![ethersweep: stages 4 and 6 take 48% to 78% of a run. Simulation, GLB takes 5.4 s. Simulation, STEP takes 6.9 s. Simulation, STL takes 5.3 s. Simulation, OBJ takes 8.1 s. Visual, GLB takes 7.0 s. Visual, OBJ takes 8.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/ethersweep_electronic-design-development-ethersweep407-CAN_ethersweep.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 0.5 | 2.2 | 0.2&nbsp;ms | 1.8 | 85&nbsp;ms | 0.3 | 0.2 | 5.4 |
| Simulation, STEP | 0.3 | 0.5 | 2.2 | 0.3&nbsp;ms | 1.7 | 1.7 | 0.3 | 0.2 | 6.9 |
| Simulation, STL | 0.2 | 0.6 | 2.1 | 0.2&nbsp;ms | 1.7 | 0.1 | 0.3 | 0.2 | 5.3 |
| Simulation, OBJ | 0.3 | 0.6 | 2.2 | 0.4&nbsp;ms | 1.7 | 2.8 | 0.3 | 0.2 | 8.1 |
| Visual, GLB | 0.3 | 0.6 | 2.2 | 0.3&nbsp;ms | 3.3 | 43&nbsp;ms | 0.4 | 0.3 | 7.0 |
| Visual, OBJ | 0.3 | 0.6 | 2.1 | 0.3&nbsp;ms | 3.4 | 1.4 | 0.3 | 0.2 | 8.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Neumi/ethersweep](https://github.com/Neumi/ethersweep)<br>Board: `ethersweep.kicad_pcb` |
|---|---|
| Folder | electronic_design / development / ethersweep407_CAN |
| Complexity | 295&nbsp;/&nbsp;1000 (size&nbsp;155, features&nbsp;140) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 24, 154, 13 |
| Triangles,&nbsp;simulation | 503,738 in 44 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">274&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">67&nbsp;MB</td><td align="right">308&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">25&nbsp;MB</td><td align="right">278&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">51&nbsp;MB</td><td align="right">383&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.8&nbsp;MB</td><td align="right">276&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">26&nbsp;MB</td><td align="right">275&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.89 ethersweep

![ethersweep: stages 4 and 6 take 58% to 84% of a run. Simulation, GLB takes 18 s. Simulation, STEP takes 21 s. Simulation, STL takes 18 s. Simulation, OBJ takes 25 s. Visual, GLB takes 27 s. Visual, OBJ takes 30 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/ethersweep_electronic-design-development-ethersweep-tmc2209_ethersweep.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.9 | 8.7 | 0.4&nbsp;ms | 5.8 | 0.2 | 0.7 | 0.2 | 18.0 |
| Simulation, STEP | 0.4 | 1.9 | 8.6 | 0.6&nbsp;ms | 5.7 | 4.0 | 0.7 | 0.2 | 21.5 |
| Simulation, STL | 0.4 | 1.9 | 8.6 | 0.4&nbsp;ms | 5.8 | 0.5 | 0.6 | 0.2 | 18.0 |
| Simulation, OBJ | 0.4 | 1.8 | 8.6 | 0.7&nbsp;ms | 5.8 | 7.2 | 0.7 | 0.2 | 24.7 |
| Visual, GLB | 0.4 | 1.8 | 8.6 | 0.9&nbsp;ms | 13.9 | 0.2 | 1.5 | 0.3 | 26.6 |
| Visual, OBJ | 0.4 | 1.9 | 8.4 | 0.6&nbsp;ms | 12.4 | 4.9 | 1.9 | 0.3 | 30.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Neumi/ethersweep](https://github.com/Neumi/ethersweep)<br>Board: `ethersweep.kicad_pcb` |
|---|---|
| Folder | electronic_design / development / ethersweep_tmc2209 |
| Complexity | 334&nbsp;/&nbsp;1000 (size&nbsp;239, features&nbsp;95) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 105, 1,094, 319 |
| Triangles,&nbsp;simulation | 1,767,076 in 122 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">61&nbsp;MB</td><td align="right">705&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">326&nbsp;MB</td><td align="right">809&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">88&nbsp;MB</td><td align="right">712&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">186&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">42&nbsp;MB</td><td align="right">884&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">127&nbsp;MB</td><td align="right">947&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.90 ethersweep

![ethersweep: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 23 s. Simulation, STEP takes 27 s. Simulation, STL takes 23 s. Simulation, OBJ takes 36 s. Visual, GLB takes 34 s. Visual, OBJ takes 40 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/ethersweep_electronic-design-production-ethersweep405_ethersweep.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 2.5 | 10.6 | 0.6&nbsp;ms | 7.3 | 0.3 | 0.9 | 0.3 | 22.7 |
| Simulation, STEP | 0.8 | 2.5 | 10.4 | 0.6&nbsp;ms | 7.3 | 5.1 | 0.9 | 0.4 | 27.4 |
| Simulation, STL | 0.8 | 2.5 | 10.7 | 0.6&nbsp;ms | 7.5 | 0.6 | 0.8 | 0.3 | 23.2 |
| Simulation, OBJ | 0.8 | 2.6 | 10.6 | 0.6&nbsp;ms | 7.8 | 12.6 | 0.9 | 0.3 | 35.6 |
| Visual, GLB | 0.8 | 2.7 | 11.1 | 0.6&nbsp;ms | 17.2 | 0.2 | 1.5 | 0.3 | 33.9 |
| Visual, OBJ | 0.8 | 2.7 | 10.8 | 0.7&nbsp;ms | 16.6 | 6.8 | 1.8 | 0.3 | 39.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Neumi/ethersweep](https://github.com/Neumi/ethersweep)<br>Board: `ethersweep.kicad_pcb` |
|---|---|
| Folder | electronic_design / production / ethersweep405 |
| Complexity | 370&nbsp;/&nbsp;1000 (size&nbsp;255, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 104, 1,173, 151 |
| Triangles,&nbsp;simulation | 2,021,426 in 138 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">70&nbsp;MB</td><td align="right">681&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">300&nbsp;MB</td><td align="right">775&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">101&nbsp;MB</td><td align="right">692&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">213&nbsp;MB</td><td align="right">1.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">40&nbsp;MB</td><td align="right">864&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">122&nbsp;MB</td><td align="right">946&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.91 FreeEEG32

![FreeEEG32: stages 4 and 6 take 53% to 86% of a run. Simulation, GLB takes 32 s. Simulation, STEP takes 38 s. Simulation, STL takes 32 s. Simulation, OBJ takes 49 s. Visual, GLB takes 47 s. Visual, OBJ takes 57 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/freeeeg32_FreeEEG32.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.7 | 3.2 | 13.3 | 1&nbsp;ms | 12.3 | 0.5 | 1.6 | 0.3 | 31.9 |
| Simulation, STEP | 0.8 | 3.2 | 13.2 | 1&nbsp;ms | 12.5 | 6.8 | 1.6 | 0.3 | 38.4 |
| Simulation, STL | 0.8 | 3.1 | 13.0 | 1&nbsp;ms | 12.4 | 0.9 | 1.5 | 0.3 | 32.0 |
| Simulation, OBJ | 0.8 | 3.1 | 13.0 | 1&nbsp;ms | 12.9 | 17.3 | 1.6 | 0.3 | 49.0 |
| Visual, GLB | 0.8 | 3.2 | 13.4 | 1&nbsp;ms | 27.0 | 0.3 | 2.3 | 0.3 | 47.3 |
| Visual, OBJ | 0.7 | 3.3 | 13.1 | 1&nbsp;ms | 26.8 | 10.3 | 2.7 | 0.2 | 57.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [neuroidss/freeeeg32](https://github.com/neuroidss/freeeeg32)<br>Board: `FreeEEG32.kicad_pcb` |
|---|---|
| Folder | KiCad |
| Complexity | 332&nbsp;/&nbsp;1000 (size&nbsp;287, features&nbsp;45) |
| KESE&nbsp;features | through vias, slotted holes,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 213, 4,412, 279 |
| Triangles,&nbsp;simulation | 2,598,444 in 378 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">93&nbsp;MB</td><td align="right">753&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">404&nbsp;MB</td><td align="right">988&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">130&nbsp;MB</td><td align="right">768&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">284&nbsp;MB</td><td align="right">1.8&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">59&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">183&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.92 tmp

![tmp: stages 4 and 6 take 58% to 86% of a run. Simulation, GLB takes 7.9 s. Simulation, STEP takes 9.9 s. Simulation, STL takes 8.1 s. Simulation, OBJ takes 11 s. Visual, GLB takes 11 s. Visual, OBJ takes 13 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/freeeeg32_tmp.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.7 | 4.2 | 0.5&nbsp;ms | 2.1 | 99&nbsp;ms | 0.3 | 0.3 | 7.9 |
| Simulation, STEP | 0.1 | 0.6 | 4.3 | 0.7&nbsp;ms | 2.2 | 2.0 | 0.4 | 0.2 | 9.9 |
| Simulation, STL | 0.2 | 0.7 | 4.1 | 0.7&nbsp;ms | 2.3 | 0.2 | 0.3 | 0.2 | 8.1 |
| Simulation, OBJ | 0.1 | 0.7 | 3.9 | 0.6&nbsp;ms | 2.2 | 3.1 | 0.3 | 0.2 | 10.5 |
| Visual, GLB | 0.2 | 0.6 | 4.0 | 0.5&nbsp;ms | 5.4 | 55&nbsp;ms | 0.5 | 0.2 | 11.0 |
| Visual, OBJ | 0.2 | 0.6 | 4.0 | 0.7&nbsp;ms | 5.6 | 1.6 | 0.6 | 0.2 | 12.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [neuroidss/freeeeg32](https://github.com/neuroidss/freeeeg32)<br>Board: `tmp.kicad_pcb` |
|---|---|
| Folder | KiCad |
| Complexity | 209&nbsp;/&nbsp;1000 (size&nbsp;209, features&nbsp;0) |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 57, 360, 0 |
| Triangles,&nbsp;simulation | 756,624 in 90 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">376&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">121&nbsp;MB</td><td align="right">442&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">38&nbsp;MB</td><td align="right">382&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">78&nbsp;MB</td><td align="right">551&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">414&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">42&nbsp;MB</td><td align="right">418&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.93 nu8051-ufo-target-board

![nu8051-ufo-target-board: stages 4 and 6 take 54% to 84% of a run. Simulation, GLB takes 6.7 s. Simulation, STEP takes 8.1 s. Simulation, STL takes 6.4 s. Simulation, OBJ takes 9.2 s. Visual, GLB takes 10 s. Visual, OBJ takes 12 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/chipwhisperer-target-cw308t_nu8051-ufo-target-board.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.6 | 3.2 | 0.5&nbsp;ms | 2.0 | 80&nbsp;ms | 0.4 | 0.2 | 6.7 |
| Simulation, STEP | 0.2 | 0.5 | 3.0 | 0.3&nbsp;ms | 2.0 | 1.8 | 0.4 | 0.2 | 8.1 |
| Simulation, STL | 0.2 | 0.6 | 3.0 | 0.4&nbsp;ms | 1.9 | 0.2 | 0.4 | 0.2 | 6.4 |
| Simulation, OBJ | 0.2 | 0.5 | 3.0 | 0.4&nbsp;ms | 2.0 | 3.0 | 0.3 | 0.2 | 9.2 |
| Visual, GLB | 0.2 | 0.5 | 3.1 | 0.4&nbsp;ms | 5.4 | 66&nbsp;ms | 0.5 | 0.3 | 10.1 |
| Visual, OBJ | 0.2 | 0.6 | 3.1 | 0.6&nbsp;ms | 5.2 | 2.1 | 0.6 | 0.2 | 11.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [newaetech/chipwhisperer-target-cw308t](https://github.com/newaetech/chipwhisperer-target-cw308t)<br>Board: `nu8051-ufo-target-board.kicad_pcb` |
|---|---|
| Folder | CW308T_NU8051_AT20 / kicad_src |
| Complexity | 241&nbsp;/&nbsp;1000 (size&nbsp;141, features&nbsp;100) |
| KESE&nbsp;features | through vias, custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 9, 181, 86 |
| Triangles,&nbsp;simulation | 612,998 in 55 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">21&nbsp;MB</td><td align="right">340&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">96&nbsp;MB</td><td align="right">391&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">31&nbsp;MB</td><td align="right">338&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">62&nbsp;MB</td><td align="right">444&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">398&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">44&nbsp;MB</td><td align="right">392&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.94 SONATA-ONE

![SONATA-ONE: stages 4 and 6 take 46% to 83% of a run. Simulation, GLB takes 2 min. Simulation, STEP takes 3 min. Simulation, STL takes 2 min. Simulation, OBJ takes 4 min. Visual, GLB takes 4 min. Visual, OBJ takes 4 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/sonata-pcb_SONATA-ONE.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 4.2 | 15.9 | 46.5 | 3&nbsp;ms | 58.2 | 3.3 | 9.4 | 0.6 | 138.2 |
| Simulation, STEP | 4.2 | 15.8 | 45.5 | 2&nbsp;ms | 57.4 | 30.6 | 10.7 | 0.6 | 164.8 |
| Simulation, STL | 4.1 | 15.9 | 46.8 | 2&nbsp;ms | 58.3 | 6.6 | 10.2 | 0.6 | 142.4 |
| Simulation, OBJ | 4.3 | 15.6 | 45.3 | 2&nbsp;ms | 61.3 | 95.8 | 9.0 | 0.7 | 232.0 |
| Visual, GLB | 4.1 | 15.4 | 45.2 | 2&nbsp;ms | 140.1 | 1.3 | 15.8 | 0.5 | 222.4 |
| Visual, OBJ | 4.2 | 15.6 | 45.8 | 3&nbsp;ms | 140.8 | 45.2 | 16.0 | 0.6 | 268.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [newaetech/sonata-pcb](https://github.com/newaetech/sonata-pcb)<br>Board: `SONATA-ONE.kicad_pcb` |
|---|---|
| Folder | sonata-one / sonata_kicad_project |
| Complexity | 487&nbsp;/&nbsp;1000 (size&nbsp;327, features&nbsp;160) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline,<br>knockout text, TrueType text,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 8 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 468, 12,952, 1,328 |
| Triangles,&nbsp;simulation | 14,886,156 in 664 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">495&nbsp;MB</td><td align="right">3.2&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">1.8&nbsp;GB</td><td align="right">4.4&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">744&nbsp;MB</td><td align="right">3.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.7&nbsp;GB</td><td align="right">9.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">262&nbsp;MB</td><td align="right">4.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">881&nbsp;MB</td><td align="right">5.8&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.95 amulet_controller

![amulet_controller: stages 4 and 6 take 50% to 88% of a run. Simulation, GLB takes 62 s. Simulation, STEP takes 72 s. Simulation, STL takes 63 s. Simulation, OBJ takes 97 s. Visual, GLB takes 2 min. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/amulet-controller-kibot_amulet-controller.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.6 | 6.7 | 23.0 | 0.7&nbsp;ms | 26.5 | 1.3 | 2.9 | 0.3 | 62.3 |
| Simulation, STEP | 1.7 | 6.5 | 23.0 | 0.6&nbsp;ms | 26.3 | 11.8 | 2.7 | 0.3 | 72.3 |
| Simulation, STL | 1.6 | 6.5 | 22.9 | 0.7&nbsp;ms | 26.1 | 2.5 | 3.0 | 0.3 | 62.8 |
| Simulation, OBJ | 1.6 | 6.6 | 23.0 | 0.7&nbsp;ms | 25.9 | 36.6 | 3.0 | 0.4 | 97.1 |
| Visual, GLB | 1.6 | 6.6 | 22.9 | 0.9&nbsp;ms | 72.2 | 0.4 | 4.6 | 0.3 | 108.6 |
| Visual, OBJ | 1.7 | 6.6 | 22.6 | 0.7&nbsp;ms | 72.1 | 15.4 | 4.4 | 0.3 | 123.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nguyen-v/amulet_controller_kibot](https://github.com/nguyen-v/amulet_controller_kibot)<br>Board: `amulet_controller.kicad_pcb` |
|---|---|
| Complexity | 457&nbsp;/&nbsp;1000 (size&nbsp;287, features&nbsp;170) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ,<br>copper finish,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 6 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 285, 1,583, 794 |
| Triangles,&nbsp;simulation | 6,621,630 in 197 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">219&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">735&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">331&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">697&nbsp;MB</td><td align="right">4.1&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">94&nbsp;MB</td><td align="right">1.9&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">299&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.96 Asteroids_PCB

![Asteroids_PCB: stages 4 and 6 take 66% to 90% of a run. Simulation, GLB takes 6 min. Simulation, STEP takes 7 min. Simulation, STL takes 6 min. Simulation, OBJ takes 6 min. Visual, GLB takes 8 min. Visual, OBJ takes 9 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/asteroids-pcb_Asteroids-PCB.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.1 | 18.3 | 180.3 | 5&nbsp;ms | 125.1 | 6.0 | 15.1 | 0.8 | 347.7 |
| Simulation, STEP | 2.3 | 19.1 | 185.8 | 4&nbsp;ms | 126.2 | 76.5 | 15.0 | 0.8 | 425.6 |
| Simulation, STL | 2.2 | 18.3 | 178.1 | 3&nbsp;ms | 121.7 | 11.6 | 14.9 | 0.8 | 347.7 |
| Simulation, OBJ | 1.7 | 15.7 | 152.2 | 5&nbsp;ms | 101.5 | 103.8 | 11.1 | 0.8 | 386.8 |
| Visual, GLB | 2.7 | 21.4 | 190.9 | 5&nbsp;ms | 246.2 | 1.9 | 19.5 | 0.6 | 483.3 |
| Visual, OBJ | 2.5 | 18.3 | 181.5 | 4&nbsp;ms | 253.5 | 70.1 | 18.9 | 0.6 | 545.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nmikstas/asteroids-pcb](https://github.com/nmikstas/asteroids-pcb)<br>Board: `Asteroids_PCB.kicad_pcb` |
|---|---|
| Folder | Asteroids_PCB |
| Complexity | 286&nbsp;/&nbsp;1000 (size&nbsp;236, features&nbsp;50) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>curved board outline |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 475, 10,686, 0 |
| Triangles,&nbsp;simulation | 21,815,320 in 718 parts |
| Verifier | PASS in all six runs |
| Run&nbsp;again | Simulation, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">750&nbsp;MB</td><td align="right">5.6&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">3.9&nbsp;GB</td><td align="right">7.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">1.1&nbsp;GB</td><td align="right">5.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">2.4&nbsp;GB</td><td align="right">14&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">349&nbsp;MB</td><td align="right">5.8&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.1&nbsp;GB</td><td align="right">6.9&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.97 ROM_To_2716

![ROM_To_2716: stages 4 and 6 take 59% to 90% of a run. Simulation, GLB takes 5.4 s. Simulation, STEP takes 6.8 s. Simulation, STL takes 5.5 s. Simulation, OBJ takes 7.6 s. Visual, GLB takes 8.4 s. Visual, OBJ takes 9.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/asteroids-pcb_ROM-To-2716.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 31&nbsp;ms | 0.2 | 2.2 | 0.2&nbsp;ms | 2.3 | 87&nbsp;ms | 0.4 | 0.2 | 5.4 |
| Simulation, STEP | 29&nbsp;ms | 0.2 | 2.1 | 0.4&nbsp;ms | 2.4 | 1.6 | 0.3 | 0.2 | 6.8 |
| Simulation, STL | 32&nbsp;ms | 0.2 | 2.2 | 0.3&nbsp;ms | 2.5 | 0.1 | 0.4 | 0.2 | 5.5 |
| Simulation, OBJ | 30&nbsp;ms | 0.2 | 2.1 | 0.2&nbsp;ms | 2.4 | 2.4 | 0.3 | 0.2 | 7.6 |
| Visual, GLB | 30&nbsp;ms | 0.2 | 2.1 | 0.2&nbsp;ms | 5.4 | 54&nbsp;ms | 0.3 | 0.2 | 8.4 |
| Visual, OBJ | 37&nbsp;ms | 0.2 | 2.2 | 0.2&nbsp;ms | 5.3 | 1.5 | 0.3 | 0.2 | 9.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nmikstas/asteroids-pcb](https://github.com/nmikstas/asteroids-pcb)<br>Board: `ROM_To_2716.kicad_pcb` |
|---|---|
| Folder | ROM_to_2716 |
| Complexity | 106&nbsp;/&nbsp;1000 (size&nbsp;86, features&nbsp;20) |
| KESE&nbsp;features | filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 32, 0 |
| Triangles,&nbsp;simulation | 398,426 in 28 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">15&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">92&nbsp;MB</td><td align="right">288&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">20&nbsp;MB</td><td align="right">241&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">43&nbsp;MB</td><td align="right">322&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.9&nbsp;MB</td><td align="right">245&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">26&nbsp;MB</td><td align="right">247&nbsp;MB</td></tr>
</table>

</td></tr></table>

## 23.16.98 quantum_arcade_pcb

![quantum_arcade_pcb: stages 4 and 6 take 57% to 87% of a run. Simulation, GLB takes 4 min. Simulation, STEP takes 5 min. Simulation, STL takes 4 min. Simulation, OBJ takes 6 min. Visual, GLB takes 6 min. Visual, OBJ takes 7 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/quantum-arcade-pcb_quantum-arcade-pcb.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.9 | 19.7 | 137.8 | 6&nbsp;ms | 83.9 | 5.0 | 13.1 | 0.8 | 262.2 |
| Simulation, STEP | 2.1 | 22.3 | 135.2 | 4&nbsp;ms | 82.6 | 63.7 | 13.4 | 0.8 | 320.0 |
| Simulation, STL | 1.9 | 20.5 | 135.2 | 4&nbsp;ms | 85.6 | 11.1 | 12.2 | 0.9 | 267.5 |
| Simulation, OBJ | 2.2 | 21.3 | 139.5 | 5&nbsp;ms | 78.9 | 129.4 | 13.5 | 1.0 | 385.7 |
| Visual, GLB | 2.2 | 21.3 | 135.7 | 4&nbsp;ms | 190.2 | 2.2 | 21.8 | 0.6 | 374.0 |
| Visual, OBJ | 2.0 | 20.0 | 131.5 | 4&nbsp;ms | 192.4 | 59.8 | 21.0 | 0.7 | 427.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nmikstas/quantum_arcade_pcb](https://github.com/nmikstas/quantum_arcade_pcb)<br>Board: `quantum_arcade_pcb.kicad_pcb` |
|---|---|
| Folder | quantum_arcade_pcb |
| Complexity | 297&nbsp;/&nbsp;1000 (size&nbsp;242, features&nbsp;55) |
| KESE&nbsp;features | through vias, filled zones,<br>copper text, curved board outline |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 482, 13,501, 809 |
| Triangles,&nbsp;simulation | 18,765,660 in 702 parts |
| Verifier | PASS in all six runs |
| Run&nbsp;again | Simulation, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">643&nbsp;MB</td><td align="right">4.8&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">3.3&nbsp;GB</td><td align="right">6.0&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">938&nbsp;MB</td><td align="right">5.0&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">2.1&nbsp;GB</td><td align="right">12&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">350&nbsp;MB</td><td align="right">5.6&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.1&nbsp;GB</td><td align="right">7.4&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.99 alu

![alu: stages 4 and 6 take 57% to 84% of a run. Simulation, GLB takes 45 s. Simulation, STEP takes 56 s. Simulation, STL takes 45 s. Simulation, OBJ takes 65 s. Visual, GLB takes 52 s. Visual, OBJ takes 63 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/74cpu_alu.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 3.8 | 18.8 | 2&nbsp;ms | 18.8 | 0.8 | 1.8 | 0.3 | 45.1 |
| Simulation, STEP | 0.7 | 3.7 | 19.1 | 1&nbsp;ms | 19.3 | 11.5 | 1.7 | 0.3 | 56.3 |
| Simulation, STL | 0.6 | 3.7 | 18.7 | 1&nbsp;ms | 18.9 | 1.7 | 1.5 | 0.3 | 45.4 |
| Simulation, OBJ | 0.7 | 3.8 | 19.1 | 1&nbsp;ms | 18.3 | 21.4 | 1.6 | 0.3 | 65.2 |
| Visual, GLB | 0.7 | 3.6 | 18.2 | 1&nbsp;ms | 25.2 | 0.3 | 3.5 | 0.3 | 51.9 |
| Visual, OBJ | 0.7 | 3.4 | 19.3 | 1&nbsp;ms | 23.6 | 11.8 | 3.4 | 0.3 | 62.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Noah1989/74cpu](https://github.com/Noah1989/74cpu)<br>Board: `alu.kicad_pcb` |
|---|---|
| Complexity | 205&nbsp;/&nbsp;1000 (size&nbsp;190, features&nbsp;15) |
| KESE&nbsp;features | through vias |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 4 (4) |
| Parts,&nbsp;tracks,&nbsp;vias | 280, 688, 86 |
| Triangles,&nbsp;simulation | 4,036,698 in 159 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">135&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">547&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">202&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">424&nbsp;MB</td><td align="right">2.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">75&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">234&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.100 adcboard

![adcboard: stages 4 and 6 take 57% to 86% of a run. Simulation, GLB takes 45 s. Simulation, STEP takes 55 s. Simulation, STL takes 46 s. Simulation, OBJ takes 66 s. Visual, GLB takes 58 s. Visual, OBJ takes 70 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/ibxII-hardware_adcboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.0 | 3.7 | 21.7 | 1&nbsp;ms | 15.5 | 0.6 | 1.8 | 0.4 | 44.6 |
| Simulation, STEP | 1.0 | 3.6 | 21.3 | 0.9&nbsp;ms | 15.9 | 11.5 | 1.9 | 0.3 | 55.5 |
| Simulation, STL | 0.9 | 3.8 | 21.5 | 0.7&nbsp;ms | 16.1 | 1.4 | 1.7 | 0.3 | 45.8 |
| Simulation, OBJ | 1.1 | 3.6 | 22.2 | 0.9&nbsp;ms | 15.4 | 21.9 | 1.7 | 0.3 | 66.2 |
| Visual, GLB | 0.9 | 3.5 | 20.6 | 1.0&nbsp;ms | 29.2 | 0.4 | 3.1 | 0.3 | 58.0 |
| Visual, OBJ | 1.1 | 3.4 | 20.4 | 0.6&nbsp;ms | 29.5 | 12.5 | 2.8 | 0.3 | 70.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nuclearfutureslab/ibxII-hardware](https://github.com/nuclearfutureslab/ibxII-hardware)<br>Board: `adcboard.kicad_pcb` |
|---|---|
| Folder | adcboard |
| Complexity | 219&nbsp;/&nbsp;1000 (size&nbsp;184, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 115, 920, 72 |
| Triangles,&nbsp;simulation | 3,351,378 in 110 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">116&nbsp;MB</td><td align="right">1.1&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">590&nbsp;MB</td><td align="right">1.3&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">168&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">358&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">71&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">220&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
</table>

</td></tr></table>

## 23.16.101 hvboard

![hvboard: stages 4 and 6 take 54% to 84% of a run. Simulation, GLB takes 15 s. Simulation, STEP takes 18 s. Simulation, STL takes 15 s. Simulation, OBJ takes 23 s. Visual, GLB takes 19 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Corpus-Testing/Corpus-Testing-16/ibxII-hardware_hvboard.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.4 | 7.1 | 0.8&nbsp;ms | 5.0 | 0.2 | 0.6 | 0.2 | 14.9 |
| Simulation, STEP | 0.3 | 1.4 | 6.9 | 0.6&nbsp;ms | 5.2 | 3.7 | 0.6 | 0.2 | 18.3 |
| Simulation, STL | 0.3 | 1.4 | 6.9 | 0.6&nbsp;ms | 5.2 | 0.4 | 0.6 | 0.3 | 15.2 |
| Simulation, OBJ | 0.3 | 1.4 | 7.2 | 0.6&nbsp;ms | 5.2 | 7.8 | 0.6 | 0.2 | 22.9 |
| Visual, GLB | 0.3 | 1.4 | 7.0 | 0.8&nbsp;ms | 9.3 | 0.1 | 1.0 | 0.2 | 19.3 |
| Visual, OBJ | 0.3 | 1.4 | 7.0 | 0.7&nbsp;ms | 9.1 | 4.3 | 0.9 | 0.2 | 23.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [nuclearfutureslab/ibxII-hardware](https://github.com/nuclearfutureslab/ibxII-hardware)<br>Board: `hvboard.kicad_pcb` |
|---|---|
| Folder | hvboard |
| Complexity | 205&nbsp;/&nbsp;1000 (size&nbsp;160, features&nbsp;45) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 50, 447, 5 |
| Triangles,&nbsp;simulation | 1,305,990 in 75 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">532&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">226&nbsp;MB</td><td align="right">593&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">65&nbsp;MB</td><td align="right">522&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">135&nbsp;MB</td><td align="right">901&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">26&nbsp;MB</td><td align="right">578&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">76&nbsp;MB</td><td align="right">578&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [Corpus Testing 15: ltbrain To mwelling](Corpus-Testing-15.md) | [Corpus Testing 17: NUSGreyhats To OLIMEX](Corpus-Testing-17.md) |
