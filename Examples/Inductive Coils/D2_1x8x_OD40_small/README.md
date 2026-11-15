# D2_1x8x_OD40_small

Coil board 3 of 10 in this branch's order. Dual coil set board. 1x + 8x, small (OD 40, bore 10), 1.6 mm board, TX 3 / 2 turns.

## The board

Outline 40.0 mm, bore 10.0 mm, 4 copper layers, board 1.6 mm, air gap 1.0 mm. Stator copper: 1.56 m of trace in all. Two coil sets: set 1 inside, set 2 outside, each a TX coil and two RX coils, SIN and COS. The rotor, a second board with copper sectors, sits 1.0 mm above the stator, copper to copper, and its eddy currents make the TX to RX coupling follow the sine and cosine of its angle.

![stator and rotor](D2_1x8x_OD40_small_stator_and_rotor.png)

| Coil set | TX | SIN | COS | Frequency | Periods per revolution (N) | Electrical period |
|---|---|---|---|---|---|---|
| 1 | TX_1 | SIN_1 | COS_1 | 3 MHz | 1 | 360° mechanical |
| 2 | TX_2 | SIN_2 | COS_2 | 4.3 MHz | 8 | 45° mechanical |

| Rotor copper ring | Sectors | Metal fraction |
|---|---|---|
| 5.53 to 9.85 mm | 1 | 0.50 |
| 12.85 to 19.3 mm | 8 | 0.50 |

Where each coil is opened for its terminals (KiCad coordinates, mm; the rotation axis is at (100, 100)):

| Net | Kind | Where | Terminals |
|---|---|---|---|
| `TX_1` (TX_1) | TX ends | (87.55, 100), F.Cu and In2.Cu | the two coil ends, stacked at one point on two layers: their end faces are the terminals |
| `TX_2` (TX_2) | TX ends | (119.3, 100), F.Cu and In2.Cu | the two coil ends, stacked at one point on two layers: their end faces are the terminals |
| `SIN_1` (SIN_1) | RX cut | (94.1945, 102.585), F.Cu | the trace is cut there with a 0.2 mm gap: the two cut faces are the terminals |
| `COS_1` (COS_1) | RX cut | (91.0632, 96.1141), F.Cu | the trace is cut there with a 0.2 mm gap: the two cut faces are the terminals |
| `SIN_2` (SIN_2) | RX via (fallback) | via at (115.166, 95.8939) | no cut spot on this board: the via is left out, and its two pads are the terminals |
| `COS_2` (COS_2) | RX via (fallback) | via at (84.4175, 102.013) | no cut spot on this board: the via is left out, and its two pads are the terminals |

Both boards are built by KESE with solder mask on both faces, stator and rotor: 20 µm, εr 3.8, tan δ 0.02, vias tented (`test_spec.json` → `solder_mask`). These KiCad stack-ups set no mask, so the bridge sets it.

## Why it is here

The smallest dual: tight spacing between the sets.

Elmer is the main solver of these encoder boards: at 3 to 5 MHz the boards are about 1/2000 of a wavelength across, so the physics is magneto-quasi-static, which is exactly what Elmer's time-harmonic A-V solver does.

## What the solver checks

Elmer, magnetic (WhitneyAVHarmonicSolver with edge elements), every coil a massive coil of the circuit module: the driven TX carries 1 A, every other coil is open. One solve gives the TX's impedance (L and R, with skin, proximity and the rotor's loss) and each open coil's voltage, so its mutual inductance M. The rotor's 35 µm copper is meshed through its thickness (the skin depth at these frequencies is 32 to 38 µm).

Solves: 20. Per coil set, the rotor away (C1, C3), the rotor at the eight angles of C4 (set 1: 0, 45, 90, 135, 180, 225, 270, 315° mechanical) (set 2: 0, 5.625, 11.25, 16.875, 22.5, 28.125, 33.75, 39.375° mechanical) and one more: the rotor at one electrical period (360/N) for C4's period check, where N > 1. The stator's mesh is the same in every solve; only the air around the rotor is meshed again for each angle.

The checks are the Elmer brief's (`../Things to test in ELMER.md`, section 5), with the five pass marks reviewed on 16 November (see `../README.md`): C0 (the mesh study, on S1), C1 to C6, C7 on the dual boards, and C10. C9 (air gap sweep), C11 (rotor off-centre and tilted) and C12 (surface-impedance rotor) are optional.

Size: about 17 GB of memory, a first guess from its 1.56 m of copper; it runs on a PC with 32 GB. The S2 mesh study measures the real figure and this line is corrected then.

## Results

Not run yet. When it runs, `results.md` in this folder gets every number, the runs' CSV and the plots, and this table gets the Got and Pass columns.

| Check | Quantity | Expected | Got | Pass |
|---|---|---|---|---|
| C1 | TX_1: L, rotor away | 1.461 µH (reference; generator 1.463 µH) | | within 3 % |
| C2 | TX_1: L with the rotor at 0°, and the drop | 1.388 µH, -5.0 % (reference); 1.214 µH, -17.0 % (generator) | | reported: the open question |
| C2 | TX_1: spread of L over the eight C4 angles | none, by symmetry | | within 0.5 % of their mean |
| C3 | TX_1: M0 to SIN / COS, rotor away | +0.004 nH / -0.010 nH | | M0 / A below 3 %; the sign judged only where resolved |
| C4 | TX_1: amplitude A to SIN / COS | 13.42 / 13.42 nH | | within 15 % |
| C4 | TX_1: even harmonic h2 | below 1 % of A | | below 1 % of A |
| C4 | TX_1: third harmonic h3 (SIN / COS) | 1.85 % / 1.85 % | | within 2×, or within 0.3 % of A |
| C5 | TX_1: phase difference SIN − COS | +90.0° (either sign) | | 90 ± 1° |
| C5 | TX_1: amplitude ratio SIN / COS | 1.000 | | 1.00 ± 0.02 |
| C6 | TX_1: peak angle error, offsets removed (raw) | 1.09 (1.27) electrical degrees | | within 3×, or below 0.5° |
| C10 | TX_1: resistance, DC / at 3 MHz rotor away / with the rotor; rotor loss | 1.05 Ω DC; the generator says up to about 2× at 3 MHz | | reported |
| C1 | TX_2: L, rotor away | 1.355 µH (reference; generator 1.358 µH) | | within 3 % |
| C2 | TX_2: L with the rotor at 0°, and the drop | 1.294 µH, -4.5 % (reference); 1.130 µH, -16.8 % (generator) | | reported: the open question |
| C2 | TX_2: spread of L over the eight C4 angles | none, by symmetry | | within 0.5 % of their mean |
| C3 | TX_2: M0 to SIN / COS, rotor away | +0.029 nH / -0.005 nH | | M0 / A below 3 %; the sign judged only where resolved |
| C4 | TX_2: amplitude A to SIN / COS | 19.04 / 19.04 nH | | within 15 % |
| C4 | TX_2: period, M at 45° against M at 0° | equal (period 45°) | | within 1 % of A; h2 below 1 % of A |
| C4 | TX_2: third harmonic h3 (SIN / COS) | 0.29 % / 0.29 % | | within 2×, or within 0.3 % of A |
| C5 | TX_2: phase difference SIN − COS | +90.0° (either sign) | | 90 ± 1° |
| C5 | TX_2: amplitude ratio SIN / COS | 1.000 | | 1.00 ± 0.02 |
| C6 | TX_2: peak angle error, offsets removed (raw) | 0.17 (0.24) electrical degrees | | within 3×, or below 0.5° |
| C10 | TX_2: resistance, DC / at 4.3 MHz rotor away / with the rotor; rotor loss | 1.14 Ω DC; the generator says up to about 2× at 4.3 MHz | | reported |
| C7 | Crosstalk: TX_1 into set 2's RX / TX_2 into set 1's RX | 8.42 / 4.39 nH | | reported |

Expected numbers: the generator pack's quasi-static reference (`tools/quasistatic_reference.py` of the generator pack: Neumann integrals and a thin-sheet eddy-current model of the rotor) and the generator's own estimates, from `test_spec.json` → `expected` and `expected_results.json`. The sign of the phase difference depends on the rotation sense; either is right if consistent.

## How to run

```
python run_simulation.py "Examples/Inductive Coils/D2_1x8x_OD40_small"
```

## Files

| File | What it is |
|---|---|
| `Stator.kicad_pcb`, `Rotor.kicad_pcb` (and their `.kicad_pro`) | the two boards, KiCad 7 format, as the generator wrote them |
| `test_spec.json` | what the bridge reads: stack-up, rotor placement and angles, solder mask, terminals, expected values |
| `expected_results.json`, `expected_results.txt`, `expected_coupling.png` | every predicted number, with the coupling curves against the rotor angle |
| `Parameters.txt`, `parameter_files/`, `run_log.txt` | the generator's full record of this board |
| `D2_1x8x_OD40_small_stator_and_rotor.png`, `*_Actual.svg`, `*_Representative.svg` | pictures of the board and its coils |

## Licence

This board is output of the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator), for non-commercial use only; see `../LICENSE.md`. It is not covered by this branch's GPL-3.0.
