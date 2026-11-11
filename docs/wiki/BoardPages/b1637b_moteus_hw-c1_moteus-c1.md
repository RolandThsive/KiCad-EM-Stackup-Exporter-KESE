# 1637. moteus_c1

Board 1,637 of the 3,107 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 16](../CorpusTestingPages/Corpus-Testing-16.md#1637-moteus_c1).

![moteus_c1: stages 4 and 6 take 47% to 80% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 20 s. Simulation, STL takes 16 s. Simulation, OBJ takes 26 s. Visual, GLB takes 24 s. Visual, OBJ takes 30 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1637b_moteus_hw-c1_moteus-c1/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.6 | 2.1 | 5.7 | 0.6&nbsp;ms | 6.2 | 0.3 | 0.8 | 0.2 | 15.8 |
| Simulation, STEP | 0.5 | 2.2 | 5.7 | 0.6&nbsp;ms | 6.1 | 4.3 | 0.8 | 0.3 | 19.9 |
| Simulation, STL | 0.5 | 2.2 | 5.7 | 0.6&nbsp;ms | 6.2 | 0.5 | 0.8 | 0.3 | 16.2 |
| Simulation, OBJ | 0.5 | 2.1 | 5.9 | 0.5&nbsp;ms | 6.3 | 10.0 | 0.8 | 0.3 | 25.9 |
| Visual, GLB | 0.7 | 2.1 | 5.7 | 0.8&nbsp;ms | 13.5 | 0.2 | 1.5 | 0.3 | 23.9 |
| Visual, OBJ | 0.5 | 2.2 | 5.9 | 0.9&nbsp;ms | 13.3 | 6.1 | 1.5 | 0.3 | 29.9 |

<table align="center"><tr><td valign="top">

| Board | Repo: [mjbots/moteus](https://github.com/mjbots/moteus)<br>Board: `moteus_c1.kicad_pcb` |
|---|---|
| Folder | hw / c1 |
| Complexity | 340&nbsp;/&nbsp;1000 (size&nbsp;250, features&nbsp;90) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>stack-up, dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 120, 1,099, 290 |
| Triangles,&nbsp;simulation | 1,697,714 in 114 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">58&nbsp;MB</td><td align="right">613&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">200&nbsp;MB</td><td align="right">687&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">85&nbsp;MB</td><td align="right">589&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">175&nbsp;MB</td><td align="right">1.2&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">35&nbsp;MB</td><td align="right">738&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">107&nbsp;MB</td><td align="right">831&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1636. EDA-02327-V2-0_pcb](b1636b_fmc-tester-v2_EDA-02327-V2-0-pcb.md) | [1638. moteus_c1](b1638b_moteus_hw-c1-r1-0_moteus-c1.md) |
