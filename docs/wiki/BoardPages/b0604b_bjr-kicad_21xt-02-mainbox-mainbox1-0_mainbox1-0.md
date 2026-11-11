# 604. mainbox1.0

Board 604 of the 3,125 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 6](../CorpusTestingPages/Corpus-Testing-06.md#604-mainbox10).

![mainbox1.0: stages 4 and 6 take 53% to 84% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 21 s. Simulation, STL takes 17 s. Simulation, OBJ takes 24 s. Visual, GLB takes 21 s. Visual, OBJ takes 29 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0604b_bjr-kicad_21xt-02-mainbox-mainbox1-0_mainbox1-0/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.4 | 1.6 | 5.8 | 0.7&nbsp;ms | 7.0 | 0.3 | 0.8 | 0.3 | 16.1 |
| Simulation, STEP | 0.4 | 1.5 | 5.8 | 1&nbsp;ms | 7.9 | 4.6 | 0.9 | 0.3 | 21.4 |
| Simulation, STL | 0.4 | 1.5 | 5.8 | 0.6&nbsp;ms | 7.4 | 0.4 | 0.8 | 0.3 | 16.5 |
| Simulation, OBJ | 0.4 | 1.4 | 5.7 | 0.8&nbsp;ms | 7.2 | 8.6 | 0.8 | 0.3 | 24.4 |
| Visual, GLB | 0.4 | 1.3 | 6.3 | 0.9&nbsp;ms | 11.6 | 0.1 | 1.1 | 0.3 | 21.2 |
| Visual, OBJ | 0.5 | 1.5 | 6.0 | 0.8&nbsp;ms | 13.3 | 5.8 | 1.1 | 0.3 | 28.5 |

<table align="center"><tr><td valign="top">

| Board | Repo: [bluejayracing/bjr_kicad](https://github.com/bluejayracing/bjr_kicad)<br>Board: `mainbox1.0.kicad_pcb` |
|---|---|
| Folder | 21xt / 02-mainbox / mainbox1.0 |
| Complexity | 318&nbsp;/&nbsp;1000 (size&nbsp;233, features&nbsp;85) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 58, 804, 111 |
| Triangles,&nbsp;simulation | 1,389,196 in 142 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">47&nbsp;MB</td><td align="right">543&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">206&nbsp;MB</td><td align="right">629&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">69&nbsp;MB</td><td align="right">548&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">143&nbsp;MB</td><td align="right">972&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">29&nbsp;MB</td><td align="right">675&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">89&nbsp;MB</td><td align="right">758&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [603. wsg1.0](b0603b_bjr-kicad_wsg1-0.md) | [605. mainbox2.0](b0605b_bjr-kicad_21xt-02-mainbox-mainbox2-0_mainbox2-0.md) |
