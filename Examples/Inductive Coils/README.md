# Inductive Coils

Inductive angle-encoder boards from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator), one folder each. A **stator** board carries one TX coil and two RX coils (SIN and COS). A **rotor** board with copper sectors sits 1.0 mm above it by default. The TX is driven at 3 to 5 MHz, the rotor's eddy currents change how much of the TX's field reaches each RX coil, and the two RX voltages follow the sine and cosine of the rotor's angle.

## What this branch checks

At 3 to 5 MHz the boards are about 1/2000 of a wavelength across, so the physics is magneto-quasi-static. Elmer's time-harmonic A-V solver is the main solver of these boards. Per board it gives the TX's inductance and resistance with the rotor away and present (C1, C2, C10), the direct TX to RX coupling (C3), the coupling against the rotor's angle (C4) and what follows from it: the SIN and COS match (C5) and the angle error (C6), the crosstalk between the two sets of a dual board (C7), and the rotor's loss (C10). The brief that sets it all out is [`Things to test in ELMER.md`](Things%20to%20test%20in%20ELMER.md).

The most important single number is C2: how much the rotor lowers the TX's inductance. The generator says 12 to 21 %, the quasi-static reference 2 to 7 %. Elmer settles it, after it has proved itself on eddy-current cases with known answers (TEAM Problem 7, and a coil above a copper plate against the exact Dodd and Deeds solution).

## The boards here

All of them are S0 and boards made from it, small enough that a solve runs on a 15 GB machine (the 1.5 and 2 mm gaps and the three-turn board with a swapfile):

| Board | What it is |
|---|---|
| [S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) | S0: 21 mm across, one period per turn, the TX one turn on each layer, a half-ring rotor |
| [S0_1x_OD21_2L_tiny_TXtop](S0_1x_OD21_2L_tiny_TXtop/) | the same board with the TX two turns on the top layer (the generator narrows the RX band to fit them) |
| [S0_1x_OD22_2L_tiny_TXtop](S0_1x_OD22_2L_tiny_TXtop/) | the TX two turns on the top layer around S0's own RX coils, the board grown to 22.2 mm |
| [S0_1x_OD22_2L_tiny_TXtop_Cut](S0_1x_OD22_2L_tiny_TXtop_Cut/) | the 22 mm board with SIN and COS opened by a cut in a top trace instead of a left-out via |
| [S0_1x_OD23_2L_tiny_TX3top_Cut](S0_1x_OD23_2L_tiny_TX3top_Cut/) | the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by cuts |

Every board folder holds the same files and stands on its own: its README has the board, its results at each air gap and how to run it. [`Comparisons/`](Comparisons/) sets the boards side by side (the TX on top against S0, the cut against the via, three TX turns against two, and every board's signal), with the scripts that print those tables and draw the charts.

The ten larger generator boards (S1 to S5 and D1 to D5) were taken out on 16 November and will be added back later. Measured before that: S2's mesh at level 1 had 979,420 nodes, about 59 GB a solve, and the others scaled at about 61 GB per metre of stator copper, so every one of them needs a bigger PC than the test machine.

## A small board for the SIN and COS curves

[S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) is the smallest coil set the generator makes that is still a whole sensor (OD 21 mm, one period per turn, a TX of one turn per layer, a half-ring rotor), made so that the SIN and COS curves over a full turn of the rotor, at any air gap, run on the 15 GB test machine (about 12 GB a solve). Its README says how it was made and how to run it.

Any other single coil set from the generator is set up the same way, in one command: [`new_coil.py`](new_coil.py) turns the generator's output folder into a folder here laid out as S0's (`Boards/` straight from the generator, `Elmer Simulation/` with S0's `simulation.py`, `angle_error.py`, `make_charts.py` and `rig_picture.py`, which run it as they are, `Results/`, and `3D_Geometry/` with KESE's export of the boards once the first run makes it), and prints the memory a solve needs. The steps are in [S0's README](S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

## Pass marks, as reviewed on 16 November

The brief's marks stand, except five that as written either cannot fail or cannot be resolved by a solver. Where this table and the brief differ, this table holds.

| Check | In the brief | Now |
|---|---|---|
| C2, angle independence | L at 0° and a second angle within 0.5 % | L at all eight C4 angles within 0.5 % of their mean (the second angle was already one of the eight, so its solve is dropped) |
| C4, period | exactly 360/N | dropped: the rotor repeats itself after 360/N, so the period is exact by construction in any solver; instead the even harmonic h2 stays below 1 % of the amplitude A |
| C4, h3 | within 2× | within 2×, or within 0.3 % of A, whichever is looser, with the stator's mesh the same at every angle |
| C3, sign pattern | the same sign pattern | M0 / A below 3 % stays; the sign is judged only where M0 is at least 3 times its change between the two finest meshes |
| C6 | the same order of magnitude | within 3 times the prediction, or below 0.5 electrical degree, whichever is looser |

## Placement and terminals, in short

* The rotation axis is KiCad's point (100, 100), z points up from the stator towards the rotor, and the top face of the stator's F.Cu copper is z = 0. KiCad's y axis points down, which flips every rotation sense in a y-up model; each results file says which convention the run used.
* The rotor is `Rotor.kicad_pcb` as drawn, not mirrored, copper side down, its copper face at z = +1.0 mm. Rotor angle θ turns it about the axis by (x, y) → (x cos θ − y sin θ, x sin θ + y cos θ) in KiCad's coordinates.
* Both boards get solder mask on both faces: 20 µm, εr 3.8, tan δ 0.02, vias tented.
* Each coil is opened where the real board gets its leads (`test_spec.json` → `terminals`): the TX at its two stacked ends, an RX by leaving one layer-change via out, or, in the `_Cut` folders, by a 0.2 mm cut across a top trace.

## What is not here

The generator pack's tools (`quasistatic_reference.py`, `kicad_to_openems.py` and the rest), which the brief mentions, stay with the generator. The expected numbers they made are in each board's `test_spec.json` and `expected_results.json`.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [LICENSE.md](LICENSE.md); this branch's GPL-3.0 covers only the scripts here (`new_coil.py`, each board's `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`, and the three in `Comparisons/`).
