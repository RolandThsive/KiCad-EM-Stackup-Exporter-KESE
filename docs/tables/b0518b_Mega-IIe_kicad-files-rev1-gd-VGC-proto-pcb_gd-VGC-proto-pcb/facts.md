| Board | Repo: [baldengineer/Mega-IIe](https://github.com/baldengineer/Mega-IIe)<br>Board: `gd VGC proto pcb.kicad_pcb` |
|---|---|
| Folder | kicad files / rev1 / gd VGC proto pcb |
| Complexity | 293&nbsp;/&nbsp;1000 (size&nbsp;238, features&nbsp;55) |
| KESE&nbsp;features | through vias, slotted holes,<br>rounded,<br>trapezoid or chamfered pads,<br>filled zones |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 101, 856, 77 |
| Triangles,&nbsp;simulation | 3,502,212 in 136 parts |
| Verifier | Simulation, GLB: Verifier FAIL<br>Simulation, STEP: Verifier FAIL<br>Simulation, STL: Verifier FAIL<br>Simulation, OBJ: Verifier FAIL |
| Bad&nbsp;design | Bad design according to KESE: copper of two nets on top of each other in the file, a short KiCad's DRC reports; two through-hole pads at one spot, (143.51, 102.87) mm, of nets `/UG3-7` and `/VBL.L`. KESE models what the file says, so the Verifier rightly finds the two nets' solids overlapping |
