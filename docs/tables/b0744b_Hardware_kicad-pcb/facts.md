| Board | Repo: [ciaa/Hardware](https://github.com/ciaa/Hardware)<br>Board: `.kicad_pcb.kicad_pcb` |
|---|---|
| Folder | PCB / RX / hw |
| Complexity | 145&nbsp;/&nbsp;1000 (size&nbsp;145, features&nbsp;0) |
| Tested | 9th November 2026 |
| Copper&nbsp;layers | 4 |
| File&nbsp;format | KiCad 3 (3) |
| Parts,&nbsp;tracks,&nbsp;vias | 418, 0, 0 |
| Triangles,&nbsp;simulation | 1,351,032 in 323 parts |
| Note | mostly unrouted |
| Verifier | Simulation, GLB: Verifier FAIL<br>Simulation, STEP: Verifier FAIL<br>Simulation, STL: Verifier FAIL<br>Simulation, OBJ: Verifier FAIL |
| Bad&nbsp;design | Bad design according to KESE: copper of two nets on top of each other in the file, a short KiCad's DRC reports; terminal blocks J10 and J11 placed overlapping at (67.15, 16.50) mm: J10 pad 1 (net `N-00000409`) and J11 pad 3 (no net), plated holes 0.06 mm apart. KESE models what the file says, so the Verifier rightly finds the two nets' solids overlapping |
