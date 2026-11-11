# 2449. adc_amp_divider

Board 2,449 of the 3,139 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 23](../CorpusTestingPages/Corpus-Testing-23.md#2449-adc_amp_divider).

![adc_amp_divider: stages 4 and 6 take 54% to 82% of a run. Simulation, GLB takes 11 s. Simulation, STEP takes 15 s. Simulation, STL takes 11 s. Simulation, OBJ takes 16 s. Visual, GLB takes 18 s. Visual, OBJ takes 23 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2449b_rusefi-hardware_classic-designs-adc-amp-divider-vertical12_adc-amp-divider/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.0 | 4.3 | 0.5&nbsp;ms | 3.9 | 0.1 | 0.6 | 0.3 | 10.6 |
| Simulation, STEP | 0.3 | 1.1 | 4.3 | 0.5&nbsp;ms | 4.1 | 3.9 | 0.5 | 0.3 | 14.6 |
| Simulation, STL | 0.3 | 1.0 | 4.3 | 0.7&nbsp;ms | 4.2 | 0.3 | 0.5 | 0.3 | 10.9 |
| Simulation, OBJ | 0.3 | 1.0 | 4.3 | 0.8&nbsp;ms | 4.2 | 4.9 | 0.6 | 0.4 | 15.7 |
| Visual, GLB | 0.3 | 1.0 | 4.4 | 1&nbsp;ms | 10.6 | 0.2 | 1.6 | 0.3 | 18.3 |
| Visual, OBJ | 0.3 | 1.0 | 4.3 | 1.0&nbsp;ms | 10.9 | 4.5 | 1.9 | 0.3 | 23.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [rusefi/rusefi-hardware](https://github.com/rusefi/rusefi-hardware)<br>Board: `adc_amp_divider.kicad_pcb` |
|---|---|
| Folder | classic-designs / adc_amp_divider.vertical12 |
| Complexity | 209&nbsp;/&nbsp;1000 (size&nbsp;174, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 111, 567, 33 |
| Triangles,&nbsp;simulation | 889,936 in 79 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">31&nbsp;MB</td><td align="right">525&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">178&nbsp;MB</td><td align="right">589&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">45&nbsp;MB</td><td align="right">544&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">92&nbsp;MB</td><td align="right">642&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">658&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">88&nbsp;MB</td><td align="right">664&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2448. adc_amp_divider_vert](b2448b_rusefi-hardware_adc-amp-divider-vert.md) | [2450. adc_amp_divider](b2450b_rusefi-hardware_classic-designs-adc-amp-divider_adc-amp-divider.md) |
