# Inductive Coils

Ten inductive angle-encoder boards from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator), one folder each. A **stator** board carries one TX coil and two RX coils (SIN and COS) per coil set; the single boards (S) have one set, the dual boards (D) two, set 1 inside and set 2 outside. A **rotor** board with copper sectors sits 1.0 mm above it. The TX is driven at 3 to 5 MHz, the rotor's eddy currents change how much of the TX's field reaches each RX coil, and the two RX voltages follow the sine and cosine of the rotor's angle.

## What this branch checks

openEMS's job on these boards is what Elmer cannot do: the coils' self resonance and stray capacitance (C8). Each TX must resonate at least five times above its operating frequency, or the 3 to 5 MHz results do not hold. C1 to C7 (inductance and coupling) are Elmer's; openEMS repeats them as a cross-check only on S2 and D2, where a run is affordable. The brief that sets it all out is [`Things to test in OpenEMS.md`](Things%20to%20test%20in%20OpenEMS.md).

## The ten boards, in the order they run

| # | Board | What it tests | Cells at 0.05 mm | Memory | One run, 4-core test machine | Runs on | Status |
|---|---|---|---|---|---|---|---|
| 1 | [S2_4x_OD40_2L_small](S2_4x_OD40_2L_small/) | the smallest single board, the cheapest model: first | 34 M | about 2.0 GB | about 7 h | 8 GB | not run yet |
| 2 | [D2_1x8x_OD40_small](D2_1x8x_OD40_small/) | the smallest dual board, tight spacing between the sets | 34 M | about 2.0 GB | about 7 h | 8 GB | not run yet |
| 3 | [S1_1x_OD54_2L_baseline](S1_1x_OD54_2L_baseline/) | the generator's default, the simplest geometry; Elmer's mesh study C0 | 63 M | about 3.8 GB | about 13 h | 8 GB | not run yet |
| 4 | [S3_8x_OD59_4L_series_wideband](S3_8x_OD59_4L_series_wideband/) | TX on the inner layers, far from the rotor; a wide band | 75 M | about 4.5 GB | about 16 h | 8 GB | not run yet |
| 5 | [S4_16x_OD54_2L_fingers](S4_16x_OD54_2L_fingers/) | the finest single pitch, and the bridging fingers | 63 M | about 3.8 GB | about 13 h | 8 GB | not run yet |
| 6 | [S5_4x_OD98_cosine_r_2subcoils_spiralTX](S5_4x_OD98_cosine_r_2subcoils_spiralTX/) | the other RX profile, sub-coils, a spiral TX, the biggest board | 212 M | about 12.7 GB | about 45 h | 32 GB | not run yet |
| 7 | [D1_1x16x_OD54_Renesas_R145_size](D1_1x16x_OD54_Renesas_R145_size/) | the dual default, a 3.2 mm board | 71 M | about 4.3 GB | about 15 h | 8 GB | not run yet |
| 8 | [D3_1x16x_OD59_fitted_bands](D3_1x16x_OD59_fitted_bands/) | a typical dual board | 74 M | about 4.4 GB | about 16 h | 8 GB | not run yet |
| 9 | [D4_2x8x_OD59_parallel_TX](D4_2x8x_OD59_parallel_TX/) | parallel TX wiring, a 2-period set | 74 M | about 4.4 GB | about 16 h | 8 GB | not run yet |
| 10 | [D5_1x16x_OD74_ID40_large](D5_1x16x_OD74_ID40_large/) | a large thin ring | 119 M | about 7.1 GB | about 25 h | 16 GB | not run yet |

Cells and the 540,000 time steps per run are the pack's dry run; memory and time use openEMS's new CPU engine as measured on the 4-core, 15 GB test machine (60 bytes a cell, 701 million cell updates a second). Each C8 run takes hours, so these runs are held until a machine can run them unattended.

## Pass marks, as reviewed on 16 November

The brief's marks stand, except five that as written either cannot fail or cannot be resolved by a solver. Where this table and the brief differ, this table holds.

| Check | In the brief | Now |
|---|---|---|
| C2, angle independence | L at 0° and a second angle within 0.5 % | L at all eight C4 angles within 0.5 % of their mean (the second angle was already one of the eight, so its solve is dropped) |
| C4, period | exactly 360/N | dropped: the rotor repeats itself after 360/N, so the period is exact by construction in any solver; instead the even harmonic h2 stays below 1 % of the amplitude A |
| C4, h3 | within 2× | within 2×, or within 0.3 % of A, whichever is looser, with the stator's mesh the same at every angle |
| C3, sign pattern | the same sign pattern | M0 / A below 3 % stays; the sign is judged only where M0 is at least 3 times its change between the two finest meshes |
| C6 | the same order of magnitude | within 3 times the prediction, or below 0.5 electrical degree, whichever is looser |

These marks apply to openEMS's cross-check of C1 to C7 as well; its C1 mark stays at 5 %.

## Placement and terminals, in short

* The rotation axis is KiCad's point (100, 100), z points up from the stator towards the rotor, and the top face of the stator's F.Cu copper is z = 0. KiCad's y axis points down, which flips every rotation sense in a y-up model; each results file says which convention the run used.
* The rotor is `Rotor.kicad_pcb` as drawn, not mirrored, copper side down, its copper face at z = +1.0 mm. Rotor angle θ turns it about the axis by (x, y) → (x cos θ − y sin θ, x sin θ + y cos θ) in KiCad's coordinates.
* Both boards get solder mask on both faces: 20 µm, εr 3.8, tan δ 0.02, vias tented.
* Each coil is opened where the real board gets its leads (`test_spec.json` → `terminals`): the TX at its two stacked ends, an RX at its cut point, or, on S2, S4 and some dual sets, by leaving one via out.

## What is not here

The generator pack's tools (`quasistatic_reference.py`, `kicad_to_openems.py` and the rest), which the brief mentions, stay with the generator. The expected numbers they made are in each board's `test_spec.json` and `expected_results.json`.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [LICENSE.md](LICENSE.md); this branch's GPL-3.0 does not cover this folder.
