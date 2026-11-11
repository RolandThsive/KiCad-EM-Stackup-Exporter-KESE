# 1900. ICE40-IO_Rev_A

Board 1,900 of the 3,124 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 18](../CorpusTestingPages/Corpus-Testing-18.md#1900-ice40-io_rev_a).

![ICE40-IO_Rev_A: stages 4 and 6 take 51% to 82% of a run. Simulation, GLB takes 10 s. Simulation, STEP takes 13 s. Simulation, STL takes 10 s. Simulation, OBJ takes 16 s. Visual, GLB takes 15 s. Visual, OBJ takes 20 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b1900b_iCE40-IO_ICE40-IO-Rev-A/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.3 | 1.0 | 4.7 | 0.6&nbsp;ms | 3.5 | 0.2 | 0.5 | 0.3 | 10.5 |
| Simulation, STEP | 0.3 | 1.0 | 4.7 | 0.5&nbsp;ms | 3.5 | 2.8 | 0.5 | 0.2 | 13.0 |
| Simulation, STL | 0.3 | 1.0 | 4.6 | 0.7&nbsp;ms | 3.5 | 0.2 | 0.5 | 0.2 | 10.3 |
| Simulation, OBJ | 0.3 | 1.0 | 4.6 | 0.7&nbsp;ms | 3.4 | 5.7 | 0.5 | 0.3 | 15.8 |
| Visual, GLB | 0.4 | 1.2 | 4.9 | 0.6&nbsp;ms | 7.8 | 0.1 | 0.8 | 0.2 | 15.4 |
| Visual, OBJ | 0.4 | 1.1 | 5.1 | 0.5&nbsp;ms | 7.9 | 4.3 | 0.7 | 0.2 | 19.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [OLIMEX/iCE40-IO](https://github.com/OLIMEX/iCE40-IO)<br>Board: `ICE40-IO_Rev_A.kicad_pcb` |
|---|---|
| Complexity | 206&nbsp;/&nbsp;1000 (size&nbsp;171, features&nbsp;35) |
| KESE&nbsp;features | through vias, filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20170123) |
| Parts,&nbsp;tracks,&nbsp;vias | 33, 751, 146 |
| Triangles,&nbsp;simulation | 1,043,876 in 64 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">36&nbsp;MB</td><td align="right">451&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">185&nbsp;MB</td><td align="right">529&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">52&nbsp;MB</td><td align="right">450&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">107&nbsp;MB</td><td align="right">736&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">27&nbsp;MB</td><td align="right">583&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">80&nbsp;MB</td><td align="right">600&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [1899. ICE40-DIO_Rev_A](b1899b_iCE40-DIO_ICE40-DIO-Rev-A.md) | [1901. ICE40-1KEVB_Rev_A](b1901b_iCE40HX1K-EVB_ICE40-1KEVB-Rev-A.md) |
