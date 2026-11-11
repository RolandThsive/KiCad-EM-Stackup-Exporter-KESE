# 797. wago kf141r adapter

Board 797 of the 3,100 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 8](../CorpusTestingPages/Corpus-Testing-08.md#797-wago-kf141r-adapter).

![wago kf141r adapter: stages 4 and 6 take 47% to 74% of a run. Simulation, GLB takes 1.7 s. Simulation, STEP takes 2.5 s. Simulation, STL takes 1.7 s. Simulation, OBJ takes 2.3 s. Visual, GLB takes 2.0 s. Visual, OBJ takes 2.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0797b_BusPirate5-hardware_wago-kf141r-adapter/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 78&nbsp;ms | 98&nbsp;ms | 0.6 | 0.2&nbsp;ms | 0.6 | 21&nbsp;ms | 73&nbsp;ms | 0.2 | 1.7 |
| Simulation, STEP | 0.1 | 0.1 | 0.6 | 0.1&nbsp;ms | 0.6 | 0.9 | 76&nbsp;ms | 0.2 | 2.5 |
| Simulation, STL | 91&nbsp;ms | 0.1 | 0.6 | 0.1&nbsp;ms | 0.6 | 45&nbsp;ms | 78&nbsp;ms | 0.2 | 1.7 |
| Simulation, OBJ | 81&nbsp;ms | 0.1 | 0.6 | 0.1&nbsp;ms | 0.6 | 0.7 | 78&nbsp;ms | 0.2 | 2.3 |
| Visual, GLB | 80&nbsp;ms | 0.1 | 0.6 | 0.1&nbsp;ms | 0.9 | 11&nbsp;ms | 0.1 | 0.2 | 2.0 |
| Visual, OBJ | 78&nbsp;ms | 0.1 | 0.6 | 0.1&nbsp;ms | 0.9 | 0.4 | 82&nbsp;ms | 0.2 | 2.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [DangerousPrototypes/BusPirate5-hardware](https://github.com/DangerousPrototypes/BusPirate5-hardware)<br>Board: `wago kf141r adapter.kicad_pcb` |
|---|---|
| Folder | adapter-kf141r-quick-connect-1REV0 |
| Complexity | 95&nbsp;/&nbsp;1000 (size&nbsp;85, features&nbsp;10) |
| KESE&nbsp;features | curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 30, 0 |
| Triangles,&nbsp;simulation | 132,576 in 20 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.1&nbsp;MB</td><td align="right">182&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">15&nbsp;MB</td><td align="right">195&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">6.6&nbsp;MB</td><td align="right">182&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">13&nbsp;MB</td><td align="right">185&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">2.3&nbsp;MB</td><td align="right">154&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">6.5&nbsp;MB</td><td align="right">155&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [796. bp5-ir-toy-v3-rev3](b0796b_BusPirate5-hardware_bp5-ir-toy-v3-rev3.md) | [798. wago kf141v adapter](b0798b_BusPirate5-hardware_wago-kf141v-adapter.md) |
