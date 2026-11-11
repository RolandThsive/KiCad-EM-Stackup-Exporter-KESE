# 894. TS_Front_Endcap

Board 894 of the 3,121 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 9](../CorpusTestingPages/Corpus-Testing-09.md#894-ts_front_endcap).

![TS_Front_Endcap: stages 4 and 6 take 48% to 74% of a run. Simulation, GLB takes 3.3 s. Simulation, STEP takes 4.3 s. Simulation, STL takes 3.3 s. Simulation, OBJ takes 5.0 s. Visual, GLB takes 4.3 s. Visual, OBJ takes 5.4 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0894b_ThunderScope_TS-Front-Endcap/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.2 | 0.5 | 1.2 | 0.1&nbsp;ms | 1.0 | 61&nbsp;ms | 0.1 | 0.2 | 3.3 |
| Simulation, STEP | 0.2 | 0.5 | 1.3 | 0.1&nbsp;ms | 1.0 | 1.1 | 0.2 | 0.2 | 4.3 |
| Simulation, STL | 0.1 | 0.4 | 1.3 | 0.1&nbsp;ms | 1.0 | 72&nbsp;ms | 0.1 | 0.2 | 3.3 |
| Simulation, OBJ | 0.1 | 0.4 | 1.3 | 0.1&nbsp;ms | 1.1 | 1.7 | 0.2 | 0.2 | 5.0 |
| Visual, GLB | 0.1 | 0.4 | 1.2 | 0.2&nbsp;ms | 2.0 | 38&nbsp;ms | 0.3 | 0.2 | 4.3 |
| Visual, OBJ | 0.2 | 0.5 | 1.2 | 0.1&nbsp;ms | 2.0 | 1.1 | 0.2 | 0.2 | 5.4 |

<table align="center"><tr><td valign="top">

| Board | Repo: [EEVengers/ThunderScope](https://github.com/EEVengers/ThunderScope)<br>Board: `TS_Front_Endcap.kicad_pcb` |
|---|---|
| Folder | Hardware / TS_Front_Endcap |
| Complexity | 232&nbsp;/&nbsp;1000 (size&nbsp;132, features&nbsp;100) |
| KESE&nbsp;features | through vias, rounded,<br>trapezoid or chamfered pads,<br>filled zones, curved board outline,<br>TrueType text, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 9 (20241228) |
| Parts,&nbsp;tracks,&nbsp;vias | 2, 5, 180 |
| Triangles,&nbsp;simulation | 317,676 in 13 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">11&nbsp;MB</td><td align="right">276&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">29&nbsp;MB</td><td align="right">281&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">16&nbsp;MB</td><td align="right">271&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">31&nbsp;MB</td><td align="right">271&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">6.8&nbsp;MB</td><td align="right">226&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">20&nbsp;MB</td><td align="right">225&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [893. TS_Back_Endcap](b0893b_ThunderScope_TS-Back-Endcap.md) | [895. TS_FPGA_Module_Rev2](b0895b_ts-hardware-archive_TS-FPGA-Module-Rev2.md) |
