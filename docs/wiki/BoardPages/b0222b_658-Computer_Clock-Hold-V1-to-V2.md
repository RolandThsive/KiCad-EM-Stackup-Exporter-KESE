# 222. Clock Hold V1 to V2

Board 222 of the 3,122 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 3](../CorpusTestingPages/Corpus-Testing-03.md#222-clock-hold-v1-to-v2).

![Clock Hold V1 to V2: stages 4 and 6 take 51% to 82% of a run. Simulation, GLB takes 4.7 s. Simulation, STEP takes 6.6 s. Simulation, STL takes 5.0 s. Simulation, OBJ takes 6.9 s. Visual, GLB takes 6.7 s. Visual, OBJ takes 8.7 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0222b_658-Computer_Clock-Hold-V1-to-V2/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.4 | 1.9 | 0.2&nbsp;ms | 1.6 | 83&nbsp;ms | 0.3 | 0.3 | 4.7 |
| Simulation, STEP | 0.1 | 0.3 | 1.9 | 0.3&nbsp;ms | 1.9 | 1.8 | 0.3 | 0.3 | 6.6 |
| Simulation, STL | 0.1 | 0.4 | 2.1 | 0.5&nbsp;ms | 1.6 | 0.2 | 0.3 | 0.3 | 5.0 |
| Simulation, OBJ | 0.1 | 0.4 | 1.9 | 0.4&nbsp;ms | 1.7 | 2.3 | 0.3 | 0.3 | 6.9 |
| Visual, GLB | 0.1 | 0.3 | 2.1 | 0.4&nbsp;ms | 3.4 | 34&nbsp;ms | 0.5 | 0.2 | 6.7 |
| Visual, OBJ | 0.1 | 0.4 | 2.3 | 0.4&nbsp;ms | 3.6 | 1.4 | 0.6 | 0.3 | 8.7 |

<table align="center"><tr><td valign="top">

| Board | Repo: [andrewpaterson/658-Computer](https://github.com/andrewpaterson/658-Computer)<br>Board: `Clock Hold V1 to V2.kicad_pcb` |
|---|---|
| Folder | Kicad / Computer / Processor / Clock Hold V1 to V2 |
| Complexity | 195&nbsp;/&nbsp;1000 (size&nbsp;115, features&nbsp;80) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 3, 132, 9 |
| Triangles,&nbsp;simulation | 424,936 in 51 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">14&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">54&nbsp;MB</td><td align="right">303&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">21&nbsp;MB</td><td align="right">262&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">42&nbsp;MB</td><td align="right">329&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">8.2&nbsp;MB</td><td align="right">280&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">24&nbsp;MB</td><td align="right">275&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [221. Address Decode V2 to V3](b0221b_658-Computer_Address-Decode-V2-to-V3.md) | [223. HCP65 Board Presence](b0223b_658-Computer_HCP65-Board-Presence.md) |
