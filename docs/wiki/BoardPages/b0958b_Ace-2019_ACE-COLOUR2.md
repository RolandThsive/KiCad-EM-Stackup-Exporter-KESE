# 958. ACE-COLOUR2

Board 958 of the 3,120 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 9](../CorpusTestingPages/Corpus-Testing-09.md#958-ace-colour2).

![ACE-COLOUR2: stages 4 and 6 take 56% to 86% of a run. Simulation, GLB takes 31 s. Simulation, STEP takes 39 s. Simulation, STL takes 32 s. Simulation, OBJ takes 48 s. Visual, GLB takes 40 s. Visual, OBJ takes 45 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0958b_Ace-2019_ACE-COLOUR2/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 2.8 | 15.2 | 0.5&nbsp;ms | 10.5 | 0.5 | 1.4 | 0.3 | 31.2 |
| Simulation, STEP | 0.5 | 2.6 | 15.8 | 0.7&nbsp;ms | 10.9 | 7.6 | 1.3 | 0.3 | 39.1 |
| Simulation, STL | 0.5 | 2.7 | 15.7 | 0.9&nbsp;ms | 10.9 | 1.0 | 1.4 | 0.3 | 32.5 |
| Simulation, OBJ | 0.6 | 2.6 | 15.6 | 0.9&nbsp;ms | 11.1 | 16.0 | 1.5 | 0.3 | 47.7 |
| Visual, GLB | 0.5 | 2.7 | 16.3 | 0.5&nbsp;ms | 18.0 | 0.2 | 1.8 | 0.3 | 39.8 |
| Visual, OBJ | 0.5 | 2.5 | 15.5 | 0.8&nbsp;ms | 17.0 | 7.3 | 2.0 | 0.3 | 45.1 |

<table align="center"><tr><td valign="top">

| Board | Repo: [flypie/Ace-2019](https://github.com/flypie/Ace-2019)<br>Board: `ACE-COLOUR2.kicad_pcb` |
|---|---|
| Folder | KiCad / ACE-COLOUR2 |
| Complexity | 212&nbsp;/&nbsp;1000 (size&nbsp;187, features&nbsp;25) |
| KESE&nbsp;features | through vias, slotted holes |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 95, 1,536, 9 |
| Triangles,&nbsp;simulation | 2,411,700 in 137 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">83&nbsp;MB</td><td align="right">825&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">410&nbsp;MB</td><td align="right">971&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">121&nbsp;MB</td><td align="right">864&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">256&nbsp;MB</td><td align="right">1.6&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">41&nbsp;MB</td><td align="right">834&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">124&nbsp;MB</td><td align="right">940&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [957. ACE-COLOUR](b0957b_Ace-2019_ACE-COLOUR.md) | [959. ACE1](b0959b_Ace-2019_ACE1.md) |
