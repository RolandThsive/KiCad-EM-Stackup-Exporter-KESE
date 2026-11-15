# S3_8x_OD59_4L_series_wideband

Coil board 4 of 10 in this branch's order. Single coil set board. 8x, wide RX band 12 ... 24 mm, 4 layers (RX Top + Inner 1, TX Inner 2 + Bottom, series).

## The board

Outline 59.2 mm, bore 21.6 mm, 4 copper layers, board 1.6 mm, air gap 1.0 mm. Stator copper: 1.91 m of trace in all. One coil set: a TX coil and two RX coils, SIN and COS. The rotor, a second board with copper sectors, sits 1.0 mm above the stator, copper to copper, and its eddy currents make the TX to RX coupling follow the sine and cosine of its angle.

![stator and rotor](S3_8x_OD59_4L_series_wideband_stator_and_rotor.png)

| Coil set | TX | SIN | COS | Frequency | Periods per revolution (N) | Electrical period |
|---|---|---|---|---|---|---|
| 1 | TX | SIN (net `2`) | COS (net `1`) | 3.5 MHz | 8 | 45° mechanical |

| Rotor copper ring | Sectors | Metal fraction |
|---|---|---|
| 11.33 to 26.9 mm | 8 | 0.50 |

Where each coil is opened for its terminals (KiCad coordinates, mm; the rotation axis is at (100, 100)):

| Net | Kind | Where | Terminals |
|---|---|---|---|
| `TX` (TX) | TX ends | (128.9, 100), In2.Cu and B.Cu | the two coil ends, stacked at one point on two layers: their end faces are the terminals |
| `2` (SIN) | RX cut | (117.061, 100.992), F.Cu | the trace is cut there with a 0.2 mm gap: the two cut faces are the terminals |
| `1` (COS) | RX cut | (121.359, 99.1434), F.Cu | the trace is cut there with a 0.2 mm gap: the two cut faces are the terminals |

Both boards are built by KESE with solder mask on both faces, stator and rotor: 20 µm, εr 3.8, tan δ 0.02, vias tented (`test_spec.json` → `solder_mask`). These KiCad stack-ups set no mask, so the bridge sets it.

## Why it is here

TX on the inner layers far from the rotor (depth 1.4 ... 1.6 mm), a wide band, 8 periods.

openEMS's job on these boards is the part Elmer cannot do: the coils' self resonance and stray capacitance (C8). An eddy-current solve has no displacement current, so only a full-wave solver sees them.

## What the solver checks

openEMS, FDTD, excited by a Gaussian pulse up to 400 MHz: each TX driven through a 500 Ω lumped port between its two ends, every RX loaded with 1 kΩ (nearly open). Copper as 35 µm conducting solids (5.8e7 S/m), FR-4 at εr 4.4 and tan δ 0.02, solder mask at εr 3.8 and tan δ 0.02. The run ends when the energy has fallen by 50 dB. Then f_SRF is the first frequency where Im(Z11) crosses zero, and C_self = 1 / ((2π f_SRF)² L_TX).

The checks are the openEMS brief's (`../Things to test in OpenEMS.md`, section 6): C8 on every board; C1 to C7 as a cross-check with Elmer only on S2 and D2, where a run is affordable.

Size: about 75 million cells at 0.05 mm (the pack's dry run), so about 4.5 GB with openEMS's new CPU engine, and about 16 hours a run on the 4-core test machine (701 million cell updates a second, measured). It fits an 8 GB PC (such as an i9-14900K with 8 GB) and the 16 GB test machine; runs of this length are held until a machine can run them unattended.

## Results

Not run yet. When it runs, `results.md` in this folder gets every number, the runs' CSV and the plots, and this table gets the Got and Pass columns.

| Check | Quantity | Expected | Got | Pass |
|---|---|---|---|---|
| C8 | TX: self resonance f_SRF, rotor away | none from the pack (the generator models no capacitance) | | at least 17.5 MHz (5 × 3.5 MHz) |
| C8 | TX: its own capacitance C_self = 1 / ((2π f_SRF)² L) | none | | reported |
| C8 | TX: f_SRF shift with the rotor at 0° | lower, by the rotor's capacitance | | reported |
| C8 | TX: capacitive coupling to SIN / COS, 5 to 50 MHz | small against ωM | | reported |
| C8 | Each RX coil's self resonance (one run per RX coil) | far above the operating frequency | | reported |

Expected numbers: the generator pack's quasi-static reference (`tools/quasistatic_reference.py` of the generator pack: Neumann integrals and a thin-sheet eddy-current model of the rotor) and the generator's own estimates, from `test_spec.json` → `expected` and `expected_results.json`. The sign of the phase difference depends on the rotation sense; either is right if consistent.

## How to run

```
python run_simulation.py "Examples/Inductive Coils/S3_8x_OD59_4L_series_wideband"
```

## Files

| File | What it is |
|---|---|
| `Stator.kicad_pcb`, `Rotor.kicad_pcb` (and their `.kicad_pro`) | the two boards, KiCad 7 format, as the generator wrote them |
| `test_spec.json` | what the bridge reads: stack-up, rotor placement and angles, solder mask, terminals, expected values |
| `expected_results.json`, `expected_results.txt`, `expected_coupling.png` | every predicted number, with the coupling curves against the rotor angle |
| `Parameters.txt`, `parameter_files/`, `run_log.txt` | the generator's full record of this board |
| `S3_8x_OD59_4L_series_wideband_stator_and_rotor.png`, `*_Actual.svg`, `*_Representative.svg` | pictures of the board and its coils |

## Licence

This board is output of the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator), for non-commercial use only; see `../LICENSE.md`. It is not covered by this branch's GPL-3.0.
