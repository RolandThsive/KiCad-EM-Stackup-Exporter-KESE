# 41. OpenEMS Implementation Troubleshooting

What went wrong while the openEMS bridge was built, what it looked like, and what fixed it. The
bridge already does what the right-hand column says; this page is for reading a run of your own that
gives a strange number, or a case changed by hand.

## 41.1 Wrong Numbers That Look Right

Each of these came out of a run that finished without an error, on the first proof board O01.

| Symptom | Cause | Fix |
|---|---|---|
| Z0 about 50 % high (O01 read 76 Ω for a 50 Ω line) | openEMS's microstrip port measures the strip's current with a probe of no height at the strip's underside, made for a strip of no thickness. KESE's copper is a solid of its real thickness, so the probe's loop of H ran through the copper and missed the current on the strip's top and sides | `thick_strip_probes()` stretches each current probe from the strip's underside to its top and `probe_pad` wider each side; give each port its `strip_top` |
| S21 of a through line far below 0 dB (O01 read −34 dB for a line that loses 0.35 dB) | S21 was taken from port 2's incident wave. In openEMS's terms a port's incident wave is the one going into the line from that port, so at an unexcited port it is almost nothing | S<sub>i1</sub> is every port's outgoing wave (`uf_ref`) over port 1's incident wave (`port_results()`) |
| εeff 10 % or more too high, while Z0 looks right | The thirds rule was the wrong way round: lines h/3 outside the metal and 2h/3 inside. openEMS snaps the copper to the nearest line, so the copper ended on the outer line through a half-covered cell | Lines h/3 inside the metal and 2h/3 outside, as openEMS's own tutorials have it (`MSL_NotchFilter.py`). See 41.2 for the test that found it |
| The field energy settles near −40 dB and the run goes on to `max_steps` | openEMS's Gaussian pulse has a cosine carrier, and its small DC part leaves static charge behind (openEMS's own documentation of `SetGaussExcite` says so) | The bridge asks for the sine carrier, `dc_free=True`, which has no DC part; an openEMS build older than the option gets the cosine. With nothing left behind the energy keeps falling, so the bridge now stops at −50 dB (`end_criteria` 1e-5): O01's finer mesh stopped after 26,095 steps instead of running to its cap of 80,000 |

## 41.2 Telling A Model Error From A Solver Error

The εeff error of 41.1 took a chain of single runs to pin down, each changing one thing. The same
chain fits any number that is off by more than the mesh study says it should be:

| Run | What it rules out | What O01 gave |
|---|---|---|
| The same case with `--engine default` | the experimental CPU engine | the same numbers to four digits |
| The substrate set to εr 1 (vacuum) | the dielectric and its loss: a microstrip in vacuum must give εeff = 1 exactly | εeff 1.12: not the dielectric |
| The copper as plain boxes instead of KESE's STL files | KESE's export and `AddPolyhedronReader` | the same as with the STL files: not the import |
| PML instead of MUR | the boundaries | the same: not the boundaries |
| The measurement planes 25 mm from the feeds | the feed's near field | 1.08: smaller, but not gone |
| A parallel-plate line in vacuum, with plain voltage probes | openEMS's time base and propagation | v/c 1.0000: the solver is right |
| A strip in a small PEC box in vacuum, on a uniform mesh | the graded mesh | εeff 0.99 to 1.05: the graded mesh at the strip's edges was the cause |

## 41.3 Messages From openEMS

| Message | Meaning |
|---|---|
| `openEMS::SetupFDTD: Warning, the timestep seems to be very small --> long simulation. Check your mesh!?` | Expected with KESE's copper: one cell of 35 µm through each copper layer sets the time step. The run is right, only longer |
| `RunFDTD: Warning: Max. number of timesteps was reached before the end-criteria of -40dB was reached...` | The field energy did not fall by `end_criteria` within `max_steps`. With ports ended far from their line's impedance the line rings for long: end it in about its own impedance (`feed_r`) or raise `max_steps`. With the cosine pulse the energy can also settle on static charge (41.1) |
| `openEMS - enabled the CPU engine (experimental)` | `engine='cpu'`: openEMS's new engine. On O01 it gave the default engine's numbers within 0.005 %, in less time and memory ([OpenEMS Implementation Hardware](OpenEMS-Implementation-Hardware.md)) |

## 41.4 The Preflight

The preflight stops a run before it starts. Each line it can fail on, and what to change:

| Failed line | Fix |
|---|---|
| `largest x cell in the dielectric under lambda/15` (or y, z) | raise `res_div`, or lower `f_max` if the band allows |
| `largest x cell in the air under lambda0/15` | the same; in z, the air's cells grow by `ratio` up to λ₀/`res_div` |
| `neighbouring x cells within 2:1` | lower `ratio`, or move a port's plane off a copper edge: a plane between the two thirds-rule lines makes two cells of 1:2 (2.00 passes) |
| `port N lies on copper of net ...` under 90 % | the port's `start` and `stop` are not on the strip: they are in model coordinates, y = −y_KiCad, and z at the strip's underside |
| `port N has its reference copper ... under it` under 99 % | `ref_net` names the wrong copper, or the reference plane has a gap under the port |
| `port N: at least 3 cells across its strip` | lower `h_edge` |

## 41.5 KESE And Python

| Symptom | Cause | Fix |
|---|---|---|
| `KESE not found` | neither `3D_Geometry/run_KESE.py` nor `KESE_PATH` points at KESE | copy KESE's `Generator/` into `3D_Geometry/` or set `KESE_PATH` ([OpenEMS Implementation Installation](OpenEMS-Implementation-Installation.md)) |
| `missing Python package(s): mapbox_earcut` | KESE runs in openEMS's Python and needs its own packages | `pip install -r <Generator>/requirements.txt` into openEMS's environment |
| trimesh asks for `networkx` while the parts load | trimesh's `section()` assembles paths with networkx | the bridge cuts the copper with `trimesh.intersections.mesh_plane` instead and needs no networkx |
| A board with no stack-up stops with `FINISH ERROR` under `--for viewer` | the viewer preset wants a copper finish that the board does not have | `--set Stackup.finish=False`; the `openems` preset leaves the finish out already |

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Hardware](OpenEMS-Implementation-Hardware.md) | [Elmer vs openEMS](Elmer-vs-OpenEMS.md) |
