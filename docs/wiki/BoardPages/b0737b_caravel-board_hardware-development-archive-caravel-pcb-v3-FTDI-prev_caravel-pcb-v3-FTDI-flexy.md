# 737. caravel_pcb_v3_FTDI_flexy

Board 737 of the 3,121 of [Corpus Testing](../Corpus-Testing.md), on [Corpus Page 7](../CorpusTestingPages/Corpus-Testing-07.md#737-caravel_pcb_v3_ftdi_flexy).

![caravel_pcb_v3_FTDI_flexy: stages 4 and 6 take 53% to 85% of a run. Simulation, GLB takes 16 s. Simulation, STEP takes 19 s. Simulation, STL takes 15 s. Simulation, OBJ takes 22 s. Visual, GLB takes 20 s. Visual, OBJ takes 26 s](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images/b0737b_caravel-board_hardware-development-archive-caravel-pcb-v3-FTDI-prev_caravel-pcb-v3-FTDI-flexy/stages.webp)

| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Simulation, GLB | 0.5 | 1.3 | 7.5 | 0.7&nbsp;ms | 5.1 | 0.3 | 0.7 | 0.3 | 15.6 |
| Simulation, STEP | 0.5 | 1.2 | 6.9 | 0.9&nbsp;ms | 4.9 | 4.4 | 0.7 | 0.3 | 18.9 |
| Simulation, STL | 0.4 | 1.5 | 7.1 | 0.9&nbsp;ms | 4.7 | 0.5 | 0.8 | 0.2 | 15.2 |
| Simulation, OBJ | 0.4 | 1.2 | 7.2 | 1&nbsp;ms | 4.6 | 7.7 | 0.6 | 0.3 | 22.0 |
| Visual, GLB | 0.3 | 1.3 | 6.7 | 1&nbsp;ms | 10.5 | 0.2 | 1.0 | 0.2 | 20.2 |
| Visual, OBJ | 0.3 | 1.3 | 6.8 | 0.6&nbsp;ms | 10.8 | 5.4 | 1.0 | 0.3 | 26.0 |

<table align="center"><tr><td valign="top">

| Board | Repo: [chipfoundry/caravel_board](https://github.com/chipfoundry/caravel_board)<br>Board: `caravel_pcb_v3_FTDI_flexy.kicad_pcb` |
|---|---|
| Folder | hardware / development / _archive / caravel_pcb_v3_FTDI_prev |
| Complexity | 311&nbsp;/&nbsp;1000 (size&nbsp;216, features&nbsp;95) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>drill offsets, filled zones,<br>stack-up, dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 6 (20211014) |
| Parts,&nbsp;tracks,&nbsp;vias | 58, 822, 104 |
| Triangles,&nbsp;simulation | 1,330,166 in 97 parts |
| Verifier | PASS in all six runs |

</td><td valign="top">

<table>
<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>
<tr><th colspan="3" align="left">Simulation</th></tr>
<tr><td>GLB</td><td align="right">45&nbsp;MB</td><td align="right">549&nbsp;MB</td></tr>
<tr><td>STEP</td><td align="right">229&nbsp;MB</td><td align="right">652&nbsp;MB</td></tr>
<tr><td>STL</td><td align="right">67&nbsp;MB</td><td align="right">511&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">136&nbsp;MB</td><td align="right">893&nbsp;MB</td></tr>
<tr><th colspan="3" align="left">Visual</th></tr>
<tr><td>GLB</td><td align="right">32&nbsp;MB</td><td align="right">703&nbsp;MB</td></tr>
<tr><td>OBJ</td><td align="right">96&nbsp;MB</td><td align="right">802&nbsp;MB</td></tr>
</table>

</td></tr></table>

| Previous | Next |
|:---|---:|
| [736. caravel-5V-dev-v6-M.2](b0736b_caravel-board_caravel-5V-dev-v6-M-2.md) | [738. caravel_pcb_v3_FTDI_flexy_fixed](b0738b_caravel-board_caravel-pcb-v3-FTDI-flexy-fixed.md) |
