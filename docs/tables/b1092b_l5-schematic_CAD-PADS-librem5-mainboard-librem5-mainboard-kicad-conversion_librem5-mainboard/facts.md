| Board | Repo: [gralco/l5-schematic](https://github.com/gralco/l5-schematic)<br>Board: `librem5_mainboard.kicad_pcb` |
|---|---|
| Folder | CAD / PADS / librem5_mainboard / librem5_mainboard_kicad_conversion |
| Complexity | 536&nbsp;/&nbsp;1000 (size&nbsp;371, features&nbsp;165) |
| KESE&nbsp;features | through vias, padstacks,<br>slotted holes, drill offsets,<br>arc tracks, filled zones,<br>copper drawings, copper text,<br>curved board outline, stack-up,<br>dielectric εr and tanδ,<br>mask and silkscreen colours |
| Tested | 9th November 2026 to 10th November 2026 |
| Copper&nbsp;layers | 10 |
| File&nbsp;format | KiCad 10 (20260206) |
| Parts,&nbsp;tracks,&nbsp;vias | 1,161, 23,746, 5,044 |
| Triangles,&nbsp;simulation | 42,957,272 in 866 parts |
| Verifier | Simulation, GLB: Verifier FAIL<br>Simulation, STEP: Verifier FAIL<br>Simulation, STL: Verifier FAIL<br>Simulation, OBJ: exceeded 11 GB on a 16 GB machine (stopped there, not a KESE failure); it will be run again on a machine with more memory |
| Bad&nbsp;design | Bad design according to KESE: copper of two nets on top of each other in the file, a short KiCad's DRC reports; GND and `4G_POWER_KEY` vias about 0.01 mm apart in 238 places, the first at (149.77, 116.06) mm (left so by the conversion from PADS). KESE models what the file says, so the Verifier rightly finds the two nets' solids overlapping |
| Run&nbsp;again | Visual, OBJ: failed in the corpus run, run again with the memory cap raised from 11 GB to 14.5 GB, and passed |
