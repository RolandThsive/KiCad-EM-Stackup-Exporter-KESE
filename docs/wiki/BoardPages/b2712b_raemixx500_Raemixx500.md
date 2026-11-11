# 2712. Raemixx500

Board 2,712 of the 3,105 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 26](../CorpusTestingPages/Corpus-Testing-26.md#2712-raemixx500).

![Raemixx500: stages 4 and 6 take 57% to 88% of a run. Simulation, GLB takes 3 min. Simulation, STEP takes 4 min. Simulation, STL takes 3 min. Simulation, OBJ takes 5 min. Visual, GLB takes 5 min. Visual, OBJ takes 6 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2712b_raemixx500_Raemixx500/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 2.8 | 14.6 | 101.2 | 3&nbsp;ms | 65.9 | 2.7 | 12.5 | 0.5 | 200.1 |
| Simulation, STEP | 3.2 | 14.4 | 96.3 | 4&nbsp;ms | 65.3 | 42.3 | 12.7 | 0.5 | 234.7 |
| Simulation, STL | 3.0 | 16.0 | 99.5 | 5&nbsp;ms | 66.1 | 6.5 | 12.4 | 0.5 | 204.0 |
| Simulation, OBJ | 3.1 | 14.7 | 94.5 | 3&nbsp;ms | 65.9 | 89.4 | 12.1 | 0.5 | 280.3 |
| Visual, GLB | 3.3 | 14.6 | 96.4 | 3&nbsp;ms | 192.1 | 2.1 | 19.6 | 0.4 | 328.5 |
| Visual, OBJ | 2.8 | 14.5 | 95.5 | 5&nbsp;ms | 188.1 | 57.8 | 18.5 | 0.4 | 377.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [sukkopera/raemixx500](https://github.com/sukkopera/raemixx500)<br>Board: `Raemixx500.kicad_pcb` |
|---|---|
| Complexity | 362&nbsp;/&nbsp;1000 (size&nbsp;277, features&nbsp;85) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, filled zones,<br>copper text, curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 362, 11,735, 902 |
| Triangles,&nbsp;simulation | 15,351,150 in 483 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">519&nbsp;MB</td><td align="right">4.5&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">2.6&nbsp;GB</td><td align="right">5.6&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">768&nbsp;MB</td><td align="right">4.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.7&nbsp;GB</td><td align="right">9.5&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">369&nbsp;MB</td><td align="right">5.5&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">1.2&nbsp;GB</td><td align="right">7.3&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2711. LittleSixteen](b2711b_LittleSixteen_LittleSixteen.md) | [2713. launch-heavy](b2713b_launch_launch-heavy.md) |
