# 523. ROM Interposer board

Board 523 of the 3,118 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 5](../CorpusTestingPages/Corpus-Testing-05.md#523-rom-interposer-board).

![ROM Interposer board: stages 4 and 6 take 51% to 79% of a run. Simulation, GLB takes 3.5 s. Simulation, STEP takes 4.5 s. Simulation, STL takes 3.5 s. Simulation, OBJ takes 4.8 s. Visual, GLB takes 4.7 s. Visual, OBJ takes 5.6 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0523b_Mega-IIe_kicad-files-ROM-Interposer-board_ROM-Interposer-board/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.1 | 0.3 | 1.4 | 0.5&nbsp;ms | 1.1 | 54&nbsp;ms | 0.2 | 0.3 | 3.5 |
| Simulation, STEP | 0.1 | 0.2 | 1.3 | 0.2&nbsp;ms | 1.2 | 1.3 | 0.2 | 0.2 | 4.5 |
| Simulation, STL | 0.1 | 0.2 | 1.4 | 0.3&nbsp;ms | 1.3 | 0.1 | 0.2 | 0.2 | 3.5 |
| Simulation, OBJ | 0.1 | 0.3 | 1.2 | 0.4&nbsp;ms | 1.2 | 1.6 | 0.2 | 0.2 | 4.8 |
| Visual, GLB | 0.1 | 0.2 | 1.3 | 0.3&nbsp;ms | 2.4 | 39&nbsp;ms | 0.3 | 0.2 | 4.7 |
| Visual, OBJ | 93&nbsp;ms | 0.3 | 1.2 | 0.2&nbsp;ms | 2.3 | 1.2 | 0.3 | 0.2 | 5.6 |

<table align="center"><tr><td valign="top">

| Board | Repo: [baldengineer/Mega-IIe](https://github.com/baldengineer/Mega-IIe)<br>Board: `ROM Interposer board.kicad_pcb` |
|---|---|
| Folder | kicad files / ROM Interposer board |
| Complexity | 114&nbsp;/&nbsp;1000 (size&nbsp;104, features&nbsp;10) |
| KESE&nbsp;features | curved board outline |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 7 (20221018) |
| Parts,&nbsp;tracks,&nbsp;vias | 4, 72, 0 |
| Triangles,&nbsp;simulation | 350,958 in 36 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">236&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">42&nbsp;MB</td><td align="right">269&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">18&nbsp;MB</td><td align="right">236&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">35&nbsp;MB</td><td align="right">286&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">7.0&nbsp;MB</td><td align="right">257&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">21&nbsp;MB</td><td align="right">260&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [522. ROM Interposer board](b0522b_Mega-IIe_kicad-files-rev1-ROM-Interposer-board_ROM-Interposer-board.md) | [524. servid-rp2040-hdmi proto rev1](b0524b_Mega-IIe_servid-rp2040-hdmi-proto-rev1.md) |
