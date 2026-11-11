# 2710. ail

Board 2,710 of the 3,139 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 26](../CorpusTestingPages/Corpus-Testing-26.md#2710-ail).

![ail: stages 4 and 6 take 42% to 74% of a run. Simulation, GLB takes 1.9 s. Simulation, STEP takes 2.8 s. Simulation, STL takes 2.0 s. Simulation, OBJ takes 2.3 s. Visual, GLB takes 2.6 s. Visual, OBJ takes 3.3 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2710b_pcb_ail/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.1 | 0.5 | 0.3&nbsp;ms | 0.8 | 25&nbsp;ms | 68&nbsp;ms | 0.2 | 1.9 |
| Simulation, STEP | 0.2 | 0.1 | 0.5 | 0.1&nbsp;ms | 0.7 | 1.0 | 56&nbsp;ms | 0.2 | 2.8 |
| Simulation, STL | 0.2 | 0.2 | 0.5 | 0.2&nbsp;ms | 0.8 | 37&nbsp;ms | 60&nbsp;ms | 0.2 | 2.0 |
| Simulation, OBJ | 0.1 | 0.1 | 0.5 | 0.2&nbsp;ms | 0.7 | 0.6 | 59&nbsp;ms | 0.2 | 2.3 |
| Visual, GLB | 0.2 | 0.1 | 0.5 | 0.2&nbsp;ms | 1.4 | 18&nbsp;ms | 0.1 | 0.2 | 2.6 |
| Visual, OBJ | 0.2 | 0.2 | 0.6 | 0.2&nbsp;ms | 1.5 | 0.5 | 0.1 | 0.3 | 3.3 |

<table align="center"><tr><td valign="top">

| Board | Repo: [sufst/pcb](https://github.com/sufst/pcb)<br>Board: `ail.kicad_pcb` |
|---|---|
| Folder | ail |
| Complexity | 211&nbsp;/&nbsp;1000 (size&nbsp;126, features&nbsp;85) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 8 (20240108) |
| Parts,&nbsp;tracks,&nbsp;vias | 29, 83, 0 |
| Triangles,&nbsp;simulation | 114,676 in 34 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">4.1&nbsp;MB</td><td align="right">199&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">23&nbsp;MB</td><td align="right">212&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">5.7&nbsp;MB</td><td align="right">198&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">11&nbsp;MB</td><td align="right">198&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">3.5&nbsp;MB</td><td align="right">172&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">9.5&nbsp;MB</td><td align="right">167&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2709. ail-LED_handsolder](b2709b_pcb_ail-LED-handsolder.md) | [2711. debug-board](b2711b_pcb_debug-board.md) |
