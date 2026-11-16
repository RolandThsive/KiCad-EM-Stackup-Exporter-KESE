# Inductive Coils

Ten inductive angle-encoder boards from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator), one folder each. A **stator** board carries one TX coil and two RX coils (SIN and COS) per coil set; the single boards (S) have one set, the dual boards (D) two, set 1 inside and set 2 outside. A **rotor** board with copper sectors sits 1.0 mm above it. The TX is driven at 3 to 5 MHz, the rotor's eddy currents change how much of the TX's field reaches each RX coil, and the two RX voltages follow the sine and cosine of the rotor's angle.

## What this branch checks

At 3 to 5 MHz the boards are about 1/2000 of a wavelength across, so the physics is magneto-quasi-static. Elmer's time-harmonic A-V solver is the main solver of these boards. Per board it gives the TX's inductance and resistance with the rotor away and present (C1, C2, C10), the direct TX to RX coupling (C3), the coupling against the rotor's angle (C4) and what follows from it: the SIN and COS match (C5) and the angle error (C6), the crosstalk between the two sets of a dual board (C7), and the rotor's loss (C10). The brief that sets it all out is [`Things to test in ELMER.md`](Things%20to%20test%20in%20ELMER.md).

The most important single number is C2: how much the rotor lowers the TX's inductance. The generator says 12 to 21 %, the quasi-static reference 2 to 7 %. Elmer settles it, after it has proved itself on eddy-current cases with known answers (TEAM Problem 7, and a coil above a copper plate against the exact Dodd and Deeds solution).

## The ten boards, in the order they run

| # | Board | What it tests | Stator copper | Solves | Memory | Runs on | Status |
|---|---|---|---|---|---|---|---|
| 1 | [S2_4x_OD40_2L_small](S2_4x_OD40_2L_small/) | the smallest single board, the cheapest model: first | 0.96 m | 9 | about 59 GB (measured mesh) | 64 GB | held for a bigger PC |
| 2 | [S1_1x_OD54_2L_baseline](S1_1x_OD54_2L_baseline/) | the generator's default, the simplest geometry; Elmer's mesh study C0 | 0.92 m | 9 | about 55 GB | 64 GB | held for a bigger PC |
| 3 | [D2_1x8x_OD40_small](D2_1x8x_OD40_small/) | the smallest dual board, tight spacing between the sets | 1.56 m | 18 | about 95 GB | 128 GB | held for a bigger PC |
| 4 | [S3_8x_OD59_4L_series_wideband](S3_8x_OD59_4L_series_wideband/) | TX on the inner layers, far from the rotor; a wide band | 1.91 m | 9 | about 115 GB | 128 GB | held for a bigger PC |
| 5 | [S4_16x_OD54_2L_fingers](S4_16x_OD54_2L_fingers/) | the finest single pitch, and the bridging fingers | 1.30 m | 9 | about 80 GB | 128 GB | held for a bigger PC |
| 6 | [S5_4x_OD98_cosine_r_2subcoils_spiralTX](S5_4x_OD98_cosine_r_2subcoils_spiralTX/) | the other RX profile, sub-coils, a spiral TX, the biggest board | 3.41 m | 9 | about 210 GB | 256 GB | held for a bigger PC |
| 7 | [D1_1x16x_OD54_Renesas_R145_size](D1_1x16x_OD54_Renesas_R145_size/) | the dual default, a 3.2 mm board | 3.14 m | 18 | about 190 GB | 256 GB | held for a bigger PC |
| 8 | [D3_1x16x_OD59_fitted_bands](D3_1x16x_OD59_fitted_bands/) | a typical dual board | 3.07 m | 18 | about 190 GB | 256 GB | held for a bigger PC |
| 9 | [D4_2x8x_OD59_parallel_TX](D4_2x8x_OD59_parallel_TX/) | parallel TX wiring, a 2-period set | 2.74 m | 18 | about 170 GB | 256 GB | held for a bigger PC |
| 10 | [D5_1x16x_OD74_ID40_large](D5_1x16x_OD74_ID40_large/) | a large thin ring | 3.96 m | 18 | about 240 GB | 256 GB | held for a bigger PC |

The memory rests on measurements: S2's mesh at level 1 has 979,420 nodes, and the proof boards E01 and E02 measured about 59 kB per node with the iterative solver, so S2 needs about 59 GB. The other boards scale S2 by their length of copper, about 61 GB per metre. Every board needs more than the 4-core, 15 GB test machine and is held for a bigger PC.

## A small board for the SIN and COS curves

[S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) is not one of the ten: it is the smallest coil set the generator makes that is still a whole sensor (OD 21 mm, one period per turn, a TX of one turn per layer, a half-ring rotor), made so that the SIN and COS curves over a full turn of the rotor, at any air gap, run on the 15 GB test machine (about 12 GB a solve). Its README says how it was made and how to run it.

Any other single coil set from the generator is set up the same way, in one command: [`new_coil.py`](new_coil.py) turns the generator's output folder into a folder here that S0's `simulation.py` runs as it is, and prints the memory a solve needs. The steps are in [S0's README](S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

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
* Each coil is opened where the real board gets its leads (`test_spec.json` → `terminals`): the TX at its two stacked ends, an RX at its cut point, or, on S2, S4 and some dual sets, by leaving one via out.

## What is not here

The generator pack's tools (`quasistatic_reference.py`, `kicad_to_openems.py` and the rest), which the brief mentions, stay with the generator. The expected numbers they made are in each board's `test_spec.json` and `expected_results.json`.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [LICENSE.md](LICENSE.md); this branch's GPL-3.0 covers only the scripts here (`new_coil.py` and each board's `simulation.py`).
