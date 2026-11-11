# 938. icebreaker

Board 938 of the 3,111 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 9](../CorpusTestingPages/Corpus-Testing-09.md#938-icebreaker).

![icebreaker: stages 4 and 6 take 58% to 86% of a run. Simulation, GLB takes 42 s. Simulation, STEP takes 53 s. Simulation, STL takes 43 s. Simulation, OBJ takes 61 s. Visual, GLB takes 54 s. Visual, OBJ takes 64 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0938b_icebreaker_hardware-v1-0d_icebreaker/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.8 | 3.2 | 16.3 | 0.7&nbsp;ms | 18.9 | 0.6 | 1.8 | 0.3 | 42.0 |
| Simulation, STEP | 0.8 | 3.4 | 17.7 | 0.7&nbsp;ms | 20.4 | 8.9 | 1.7 | 0.3 | 53.2 |
| Simulation, STL | 0.7 | 3.2 | 16.4 | 0.6&nbsp;ms | 19.7 | 0.9 | 1.8 | 0.3 | 43.0 |
| Simulation, OBJ | 0.8 | 3.5 | 16.6 | 0.9&nbsp;ms | 19.1 | 19.0 | 1.8 | 0.3 | 61.2 |
| Visual, GLB | 0.8 | 3.3 | 17.0 | 0.7&nbsp;ms | 29.1 | 0.3 | 3.1 | 0.3 | 53.9 |
| Visual, OBJ | 0.7 | 3.6 | 16.8 | 0.7&nbsp;ms | 27.8 | 12.5 | 2.8 | 0.3 | 64.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [esden/icebreaker](https://github.com/esden/icebreaker)<br>Board: `icebreaker.kicad_pcb` |
|---|---|
| Folder | hardware / v1.0d |
| Complexity | 311&nbsp;/&nbsp;1000 (size&nbsp;256, features&nbsp;55) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 128, 1,393, 157 |
| Triangles,&nbsp;simulation | 3,032,728 in 140 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">106&nbsp;MB</td><td align="right">927&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">504&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">152&nbsp;MB</td><td align="right">954&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">325&nbsp;MB</td><td align="right">2.0&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">68&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">210&nbsp;MB</td><td align="right">1.5&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [937. icebreaker](b0937b_icebreaker_hardware-v1-0c_icebreaker.md) | [939. icebreaker](b0939b_icebreaker_hardware-v1-0e_icebreaker.md) |
