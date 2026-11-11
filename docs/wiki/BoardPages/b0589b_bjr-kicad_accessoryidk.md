# 589. accessoryidk

Board 589 of the 3,101 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 6](../CorpusTestingPages/Corpus-Testing-06.md#589-accessoryidk).

![accessoryidk: stages 4 and 6 take 52% to 87% of a run. Simulation, GLB takes 19 s. Simulation, STEP takes 23 s. Simulation, STL takes 19 s. Simulation, OBJ takes 30 s. Visual, GLB takes 28 s. Visual, OBJ takes 31 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0589b_bjr-kicad_accessoryidk/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.7 | 8.9 | 2&nbsp;ms | 6.7 | 0.3 | 1.0 | 0.3 | 19.4 |
| Simulation, STEP | 0.4 | 1.8 | 8.5 | 1&nbsp;ms | 6.0 | 4.8 | 1.0 | 0.3 | 22.7 |
| Simulation, STL | 0.5 | 1.7 | 8.3 | 1&nbsp;ms | 6.4 | 0.6 | 0.9 | 0.3 | 18.7 |
| Simulation, OBJ | 0.5 | 1.8 | 9.1 | 1&nbsp;ms | 6.6 | 11.2 | 1.0 | 0.3 | 30.4 |
| Visual, GLB | 0.4 | 1.6 | 9.3 | 1&nbsp;ms | 15.4 | 0.2 | 1.4 | 0.2 | 28.5 |
| Visual, OBJ | 0.6 | 1.8 | 8.4 | 0.8&nbsp;ms | 12.3 | 5.4 | 1.7 | 0.3 | 30.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [bluejayracing/bjr_kicad](https://github.com/bluejayracing/bjr_kicad)<br>Board: `accessoryidk.kicad_pcb` |
|---|---|
| Folder | 21xt / 02-mainbox / bjr_kicad_aaren_copy / 21xt / 01-accessory / accessoryidk |
| Complexity | 321&nbsp;/&nbsp;1000 (size&nbsp;236, features&nbsp;85) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 75, 851, 97 |
| Triangles,&nbsp;simulation | 1,736,020 in 176 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">59&nbsp;MB</td><td align="right">619&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">238&nbsp;MB</td><td align="right">680&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">87&nbsp;MB</td><td align="right">607&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">180&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">30&nbsp;MB</td><td align="right">684&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">90&nbsp;MB</td><td align="right">747&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [588. ad5689r](b0588b_bjr-kicad_ad5689r.md) | [590. mainbox1.0](b0590b_bjr-kicad_21xt-02-mainbox-bjr-kicad-aaren-copy-21xt-02-mainbox-mainbox1-0_mainbox1-0.md) |
