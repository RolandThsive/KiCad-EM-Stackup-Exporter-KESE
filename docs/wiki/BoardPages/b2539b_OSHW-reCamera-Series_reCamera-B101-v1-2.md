# 2539. reCamera B101 v1.2

Board 2,539 of the 3,138 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 24](../CorpusTestingPages/Corpus-Testing-24.md#2539-recamera-b101-v12).

![reCamera B101 v1.2: stages 4 and 6 take 42% to 76% of a run. Simulation, GLB takes 7.4 s. Simulation, STEP takes 9.7 s. Simulation, STL takes 7.3 s. Simulation, OBJ takes 12 s. Visual, GLB takes 11 s. Visual, OBJ takes 14 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2539b_OSHW-reCamera-Series_reCamera-B101-v1-2/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.2 | 2.2 | 0.3&nbsp;ms | 2.8 | 0.2 | 0.5 | 0.3 | 7.4 |
| Simulation, STEP | 0.3 | 1.2 | 2.2 | 0.4&nbsp;ms | 2.9 | 2.4 | 0.5 | 0.2 | 9.7 |
| Simulation, STL | 0.3 | 1.2 | 2.1 | 0.3&nbsp;ms | 2.8 | 0.3 | 0.5 | 0.3 | 7.3 |
| Simulation, OBJ | 0.3 | 1.2 | 2.2 | 0.3&nbsp;ms | 3.0 | 4.9 | 0.5 | 0.3 | 12.4 |
| Visual, GLB | 0.3 | 1.2 | 2.2 | 0.4&nbsp;ms | 6.4 | 93&nbsp;ms | 0.8 | 0.2 | 11.3 |
| Visual, OBJ | 0.4 | 1.2 | 2.1 | 0.4&nbsp;ms | 6.2 | 3.3 | 0.8 | 0.3 | 14.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [Seeed-Studio/OSHW-reCamera-Series](https://github.com/Seeed-Studio/OSHW-reCamera-Series)<br>Board: `reCamera B101 v1.2.kicad_pcb` |
|---|---|
| Folder | hardware / recamera-2002 / base / b101-default / PCB / V1.2 |
| Complexity | 305&nbsp;/&nbsp;1000 (size&nbsp;190, features&nbsp;115) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>copper finish |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 48, 581, 162 |
| Triangles,&nbsp;simulation | 798,866 in 84 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">382&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">114&nbsp;MB</td><td align="right">463&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">40&nbsp;MB</td><td align="right">396&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">80&nbsp;MB</td><td align="right">574&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">19&nbsp;MB</td><td align="right">455&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">58&nbsp;MB</td><td align="right">506&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2538. reCamera B101 v1.1](b2538b_OSHW-reCamera-Series_reCamera-B101-v1-1.md) | [2540. reCamera B101_B2_v0.1](b2540b_OSHW-reCamera-Series_reCamera-B101-B2-v0-1.md) |
