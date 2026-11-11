# 723. icepi-zero

Board 723 of the 3,108 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 7](../CorpusTestingPages/Corpus-Testing-07.md#723-icepi-zero).

![icepi-zero: stages 4 and 6 take 52% to 84% of a run. Simulation, GLB takes 24 s. Simulation, STEP takes 30 s. Simulation, STL takes 25 s. Simulation, OBJ takes 38 s. Visual, GLB takes 37 s. Visual, OBJ takes 45 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0723b_icepi-zero_hardware-v1-3_icepi-zero/stages.webp)

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

| Previous | Next |
|:---|---:|
| [722. icepi-zero](b0722b_icepi-zero_hardware-v1-2_icepi-zero.md) | [724. icepi-zero](b0724b_icepi-zero_hardware-v1-4_icepi-zero.md) |
