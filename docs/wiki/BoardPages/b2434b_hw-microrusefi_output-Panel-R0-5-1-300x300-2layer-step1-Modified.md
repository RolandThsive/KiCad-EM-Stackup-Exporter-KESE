# 2434. output.Panel_R0.5.1_300x300_2layer_step1_Modified

Board 2,434 of the 3,138 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 23](../CorpusTestingPages/Corpus-Testing-23.md#2434-outputpanel_r051_300x300_2layer_step1_modified).

![Stages 4 and 6 take 85% to 86% of a run. Simulation, GLB takes 18 min. Simulation, STL takes 19 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b2434b_hw-microrusefi_output-Panel-R0-5-1-300x300-2layer-step1-Modified/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 11.0 | 95.0 | 420.2 | 6&nbsp;ms | 529.2 | 10.1 | 35.3 | 1.6 | 1102.4 |
| Simulation, STEP |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Simulation, STL | 11.1 | 96.0 | 420.7 | 5&nbsp;ms | 540.8 | 25.8 | 39.3 | 1.9 | 1135.7 |
| Simulation, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, GLB |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Visual, OBJ |  |  |  |  |  |  |  |  | exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |

<table align="center"><tr><td valign="top">

| Board | Repo: [rusefi/hw_microrusefi](https://github.com/rusefi/hw_microrusefi)<br>Board: `output.Panel_R0.5.1_300x300_2layer_step1_Modified.kicad_pcb` |
|---|---|
| Folder | gerbers / R0.5.1 / Panel_source_files |
| Complexity | 423&nbsp;/&nbsp;1000 (size&nbsp;348, features&nbsp;75) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper text,<br>curved board outline |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 2,188, 36,405, 7,605 |
| Triangles,&nbsp;simulation | 42,873,842 in 237 parts |
| Note | panel |
| Verifier | Simulation, STEP: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory<br>Simulation, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory<br>Visual, GLB: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory<br>Visual, OBJ: exceeded 11 GB on a 15 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Run&nbsp;again | Simulation, GLB; Simulation, STL: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">1.5&nbsp;GB</td><td align="right">12&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">2.1&nbsp;GB</td><td align="right">12&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">–</td><td align="right">11&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [2433. output.Panel_R0.5.1_300x300_2layer_step1](b2433b_hw-microrusefi_output-Panel-R0-5-1-300x300-2layer-step1.md) | [2435. output.Panel_R0.5.1_300x300_2layer_step1_Modified_1and5_only](b2435b_hw-microrusefi_output-Panel-R0-5-1-300x300-2layer-step1-Modified-1and5-only.md) |
