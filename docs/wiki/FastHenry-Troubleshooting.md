# 60. FastHenry Troubleshooting

What went wrong while the bridge was built, what it looked like, and what fixed it. The bridge already does what the
right-hand column says; this page is for reading a failed run of your own, or a case changed by hand. A run's working
files are under the example's `case/`: each solve's `model.inp`, `Zc.mat` and `fasthenry.log`.

## 60.1 NaN In The Impedance Matrix

| Symptom | Cause | Fix |
|---|---|---|
| The whole impedance matrix NaN on the coil board's rotor at 45°, 135°, 225° and 315° | FastHenry's test for parallel filaments is absolute (their cosine 1 to within 1e-13), and its four side filaments for two filaments a few widths apart are each moved by half its width in absolute coordinates. 100 mm from the origin, where KiCad puts the boards, that move rounds the ends by up to 1.4e-17 m, 2e-13 of a 0.06 mm rotor bar, so two bars on one line (the two rotor halves lie on opposite rays) failed the test and went to its formula for skew filaments, which is infinite for two on one line | The bridge writes `model.inp` with x and y measured from the model's middle (rounded to the whole millimetre), to 12 significant digits: every point is then within 12 mm of the origin and the rounding ten times smaller |
| The same NaN from joints in the stator's traces | A straight track split in two, its points rounded to KiCad's nanometre, leaves two pieces a few ten-thousandths of a degree apart. FastHenry takes filaments that meet end to end as parallel only if they are exactly so; at that angle their mutual inductance is infinite | Two consecutive pieces of a trace straight to within 0.01° become one segment (`merge_collinear`) |
| Thousands of *mutual inductance = infinity* warnings and a matrix of NaN, with Whiteley Research's FastHenry 3.0wr (in XicTools, release 031424) | 3.0wr lacks two of FastFieldSolvers' fixes in `mutual.c`: the formula for filaments meeting at a point, and a negative distance clipped to zero. A rotor grid of collinear bars trips exactly those cases | Use FastHenry 3.0.1, the committed build. With the rotor away both give the same matrix, to 1e-20 |

## 60.2 The Solve

| Symptom | Cause | Fix |
|---|---|---|
| FastHenry exits with *filament not expected length* at the 0.1 mm air gap | The multipole refinement splits filaments where they come close, and the split pieces upset its exact formula for parallel filaments | Turn the refinement off (`-a off`): the direct solve has no use for it. At the 1 mm gap, where both ways run, they gave the same numbers to 3 parts in 10⁸ |
| M from the TX to a receiver and M from the receiver back 2.7 % apart | FastHenry's default solve, GMRES with its multipole speed-up, is iterative and approximate | The dense direct solve, `-s ludecomp -m direct`: the matrix comes out symmetric to the last digit |
| A solve is marked not readable | M to and from the TX differ by more than 1 % of the larger receiver's M, or R TX is not positive (`readable()` in the coil board's `make_charts.py`) | Read `fasthenry.log` in that angle's folder under `case/`; with the direct solve none of the 81 solves of this category was unreadable |
| `RuntimeError: FastHenry failed in ... (status ...)` with the end of its log | FastHenry stopped, or wrote no `Zc.mat` | The last 2,000 characters of its log are in the message; the full log is `fasthenry.log` in the case folder |
| The machine runs out of memory | The dense matrix grows with the square of the filaments | Count them first with `--model-only`; see [FastHenry Hardware](FastHenry-Hardware.md) |

## 60.3 Ports

| Symptom | Cause | Fix |
|---|---|---|
| `no track of net X reaches (x, y) on ('F.Cu', 'B.Cu')` | The point given for a left-out via or for stacked ends is not within 0.45 mm of the net's track ends on both layers | Check the point in model coordinates (y = −y_KiCad) against the board; `angle_setup.py` and `rig_picture.py` ring every port |
| `the cut on net X made 1 ends: it does not cross the trace` | The cut's box misses the trace, or lies along it instead of across it | Put `cut.xy_kicad` on the trace's centre line and `along_kicad` along the trace; the box is `gap_mm` long along it and twice `half_width_mm` across |
| `rx_port 'cut' needs a 'cut' for SIN and COS in test_spec.json` | `"rx_port": "cut"` is set, but a receiver has no `cut` | Give both receivers a `cut` under `terminals`, or set `"rx_port": "via"` |
| A receiver's curve comes out with the opposite sign | A cut and a left-out via put the plus terminal on opposite sides of the coil | Harmless: the sign of M follows the port's direction. The branch's comparison scripts turn a receiver's sign where they set boards opened both ways side by side |

## 60.4 References

| Symptom | Cause | Fix |
|---|---|---|
| E01's L 0.7 % under the first reference (55.99 nH) | The first reference was Grover's ring formula times the share of the circle the arc covers. That is not how an open loop's inductance scales: each part of the ring loses its coupling to the missing part, which the share leaves out | Neumann's double integral over the arc itself, with the same GMD: 55.590 nH (`arc_inductance` in `Examples/references.py`), 0.02 % over FastHenry's limit |

## 60.5 Building And Setting Up

| Symptom | Cause | Fix |
|---|---|---|
| GCC refuses to build FastHenry | GCC 10 and newer refuse the program's shared global variables | Build with `-fcommon`, as `Solver_FastHenry/build_fasthenry.sh` does |
| The committed `fasthenry` does not run | It is built for 64-bit Linux with glibc 2.34 or newer | `bash bridge/setup_machine.sh` builds it from source when the committed one does not run; or `bash Solver_FastHenry/build_fasthenry.sh` |
| The bridge runs another FastHenry than you expect | It takes `$FASTHENRY` first, then `Solver_FastHenry/install/bin/fasthenry`, then `fasthenry` on the PATH | Unset `FASTHENRY`, or point it at the program you want; each results file records the version that ran |
| `KESE not found: copy main's Generator into 3D_Geometry ...` | A board's stack-up must be exported, and neither `3D_Geometry/run_KESE.py` nor `KESE_PATH` points at KESE | Copy KESE in ([FastHenry Installation](FastHenry-Installation.md)) or set `KESE_PATH`; boards with a committed, unchanged `3D_Geometry/` need no KESE |
| `KESE failed on <board>` or `KESE wrote no materials.json` | KESE stopped on the board, or wrote no simulation export | Its output is in the message; run `run_KESE.py <board> --for elmer` by hand to see it in full |
| A board is exported again when nothing seemed to change | The board file's hash differs from the one in its export's `source.json` | Expected: any change to the `.kicad_pcb` makes a new export |

## 60.6 The Coil Generator

| Symptom | Cause | Fix |
|---|---|---|
| The generator warns that a via is too close to other copper | The board is not right yet | Change its parameters, often the outer radius, until the warning goes |
| The generator finds no spot with room for two lead vias on a receiver | A small board leaves no room | Expected on `S0d2_1x_OD23_2L_tiny_TX3top_Cut`: each receiver is opened by a cut chosen in `test_spec.json` instead |
| The generator warns that the TX tank's parallel resistance is too low for the IPS2550 | The TX's resistance at its frequency | Does not matter to the simulation |
| The lead-cutting suggestion and the pictures are missing from the generator's output | `Generators/resources` does not sit beside the generator | Run it from a full checkout |

| Previous | Next |
|:---|---:|
| [FastHenry Hardware](FastHenry-Hardware.md) | [Palace Introduction](Palace-Introduction.md) |
