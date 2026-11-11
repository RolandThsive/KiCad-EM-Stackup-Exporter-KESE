| Board | Repo: [flypie/NewBrain](https://github.com/flypie/NewBrain)<br>Board: `NewBrain Original.kicad_pcb` |
|---|---|
| Folder | NewBrain MainBoard Original KiCad |
| Complexity | 85&nbsp;/&nbsp;1000 (size&nbsp;75, features&nbsp;10) |
| KESE&nbsp;features | rounded,<br>trapezoid or chamfered pads |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 2 |
| File&nbsp;format | KiCad 5 (20171130) |
| Parts,&nbsp;tracks,&nbsp;vias | 209, 0, 0 |
| Triangles,&nbsp;simulation | 7,779,384 in 422 parts |
| Note | mostly unrouted |
| Verifier | Simulation, GLB: Verifier FAIL<br>Simulation, STEP: Verifier FAIL<br>Simulation, STL: Verifier FAIL<br>Simulation, OBJ: Verifier FAIL |
| Bad&nbsp;design | Bad design according to KESE: copper of two nets on top of each other in the file, a short KiCad's DRC reports; C118 pad 2 and C82 pad 1 overlap at (100.32, 170.52) mm, plated holes 0.25 mm apart (the file also has no Edge.Cuts outline). KESE models what the file says, so the Verifier rightly finds the two nets' solids overlapping |
