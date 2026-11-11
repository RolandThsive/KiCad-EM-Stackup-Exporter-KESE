| Board | Repo: [schlae/cm5-reveng](https://github.com/schlae/cm5-reveng)<br>Board: `CM5RevEng.kicad_pcb` |
|---|---|
| Complexity | 537&nbsp;/&nbsp;1000 (size&nbsp;347, features&nbsp;190) |
| KESE&nbsp;features | through vias,<br>blind and buried vias, microvias,<br>custom pads, rounded,<br>trapezoid or chamfered pads,<br>filled zones, copper drawings,<br>curved board outline, stack-up,<br>dielectric εr and tanδ |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 10 |
| File&nbsp;format | KiCad 9 (20241229) |
| Parts,&nbsp;tracks,&nbsp;vias | 417, 8,115, 2,902 |
| Triangles,&nbsp;simulation | 13,000,160 in 456 parts |
| Verifier | Simulation, GLB: Verifier FAIL<br>Simulation, STEP: Verifier FAIL<br>Simulation, STL: Verifier FAIL<br>Simulation, OBJ: Verifier FAIL |
| Bad&nbsp;design | Bad design according to KESE: copper of two nets on top of each other in the file, a short KiCad's DRC reports; a GND via and a `CM5_1V8` via 0.056 mm apart at (128.38, 64.01) mm. KESE models what the file says, so the Verifier rightly finds the two nets' solids overlapping |
