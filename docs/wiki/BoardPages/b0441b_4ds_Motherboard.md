# 441. Motherboard

Board 441 of the 3,125 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 5](../CorpusTestingPages/Corpus-Testing-05.md#441-motherboard).

![Motherboard: stages 4 and 6 take 54% to 84% of a run. Simulation, GLB takes 57 s. Simulation, STEP takes 71 s. Simulation, STL takes 56 s. Simulation, OBJ takes 79 s. Visual, GLB takes 95 s. Visual, OBJ takes 2 min](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0441b_4ds_Motherboard/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 1.9 | 5.7 | 21.7 | 3&nbsp;ms | 23.3 | 0.9 | 3.1 | 0.4 | 57.1 |
| Simulation, STEP | 2.0 | 5.6 | 21.2 | 3&nbsp;ms | 23.5 | 15.1 | 3.0 | 0.4 | 70.8 |
| Simulation, STL | 1.9 | 5.5 | 20.6 | 2&nbsp;ms | 22.8 | 2.2 | 2.9 | 0.4 | 56.3 |
| Simulation, OBJ | 2.0 | 5.2 | 20.7 | 3&nbsp;ms | 21.9 | 25.6 | 2.9 | 0.4 | 78.6 |
| Visual, GLB | 1.8 | 5.5 | 21.5 | 3&nbsp;ms | 59.2 | 0.6 | 6.6 | 0.3 | 95.5 |
| Visual, OBJ | 1.9 | 5.5 | 21.2 | 2&nbsp;ms | 58.5 | 18.6 | 6.9 | 0.3 | 113.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [astronuat21/4ds](https://github.com/astronuat21/4ds)<br>Board: `Motherboard.kicad_pcb` |
|---|---|
| Folder | Motherboard |
| Complexity | 435&nbsp;/&nbsp;1000 (size&nbsp;280, features&nbsp;155) |
| KESE&nbsp;features | through vias, slotted holes,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>arc tracks, filled zones,<br>copper drawings,<br>curved board outline,<br>knockout text, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 355, 4,274, 657 |
| Triangles,&nbsp;simulation | 5,230,646 in 623 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">181&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>STEP</td><td align="right">920&nbsp;MB</td><td align="right">2.2&nbsp;GB</td></tr>
<tr><td>STL</td><td align="right">262&nbsp;MB</td><td align="right">1.7&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">566&nbsp;MB</td><td align="right">3.4&nbsp;GB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">128&nbsp;MB</td><td align="right">2.1&nbsp;GB</td></tr>
<tr><td>OBJ</td><td align="right">414&nbsp;MB</td><td align="right">2.7&nbsp;GB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [440. CTRL_Z](b0440b_4ds_CTRL-Z.md) | [442. usb-sniffer](b0442b_usb-sniffer_usb-sniffer.md) |
