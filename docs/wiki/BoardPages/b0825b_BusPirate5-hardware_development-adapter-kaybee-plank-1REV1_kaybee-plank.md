# 825. kaybee-plank

Board 825 of the 3,112 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 8](../CorpusTestingPages/Corpus-Testing-08.md#825-kaybee-plank).

![kaybee-plank: stages 4 and 6 take 51% to 83% of a run. Simulation, GLB takes 5.5 s. Simulation, STEP takes 7.1 s. Simulation, STL takes 5.7 s. Simulation, OBJ takes 8.1 s. Visual, GLB takes 7.7 s. Visual, OBJ takes 9.2 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0825b_BusPirate5-hardware_development-adapter-kaybee-plank-1REV1_kaybee-plank/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.4 | 2.3 | 0.4&nbsp;ms | 2.0 | 76&nbsp;ms | 0.3 | 0.2 | 5.5 |
| Simulation, STEP | 0.2 | 0.4 | 2.2 | 0.2&nbsp;ms | 1.9 | 1.8 | 0.3 | 0.3 | 7.1 |
| Simulation, STL | 0.2 | 0.6 | 2.3 | 0.3&nbsp;ms | 1.9 | 0.1 | 0.3 | 0.3 | 5.7 |
| Simulation, OBJ | 0.2 | 0.6 | 2.2 | 0.3&nbsp;ms | 1.9 | 2.7 | 0.3 | 0.2 | 8.1 |
| Visual, GLB | 0.2 | 0.5 | 2.2 | 0.3&nbsp;ms | 4.1 | 53&nbsp;ms | 0.4 | 0.2 | 7.7 |
| Visual, OBJ | 0.2 | 0.4 | 2.3 | 0.4&nbsp;ms | 3.8 | 1.8 | 0.4 | 0.2 | 9.2 |

<table align="center"><tr><td valign="top">

| Board | Repo: [DangerousPrototypes/BusPirate5-hardware](https://github.com/DangerousPrototypes/BusPirate5-hardware)<br>Board: `kaybee-plank.kicad_pcb` |
|---|---|
| Folder | development / adapter-kaybee-plank-1REV1 |
| Complexity | 259&nbsp;/&nbsp;1000 (size&nbsp;149, features&nbsp;110) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 27, 220, 47 |
| Triangles,&nbsp;simulation | 490,076 in 41 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">17&nbsp;MB</td><td align="right">290&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">81&nbsp;MB</td><td align="right">344&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">25&nbsp;MB</td><td align="right">287&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">50&nbsp;MB</td><td align="right">388&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">12&nbsp;MB</td><td align="right">344&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">36&nbsp;MB</td><td align="right">349&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [824. kaybee-plank](b0824b_BusPirate5-hardware_development-adapter-kaybee-plank-1REV0_kaybee-plank.md) | [826. ram-ddr5](b0826b_BusPirate5-hardware_ram-ddr5.md) |
