# S0_1x_OD21_2L_tiny

The smallest coil set that is still a whole angle sensor, made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) for one job: the SIN and COS curves over a full turn of the rotor, at any air gap, on a machine with 16 GB. It is not one of the ten boards of the brief, and it is not meant to be built: its TX is too small for the IPS2550's tank (the generator warns about it, see below).

## The board

Outline 21.0 mm, bore 4.0 mm, 2 copper layers, board 0.8 mm, air gap 1.0 mm by default (any other with `--gap`). One coil set: a TX of one turn on each layer in series, and two RX coils, SIN and COS, of one period per turn. The rotor is a half ring of copper, so a full turn of it gives one period of each curve: SIN follows the sine of the rotor's angle and COS its cosine.

![stator and rotor](S0_1x_OD21_2L_tiny_stator_and_rotor.png)

*Drawn by the generator (`Coil_2_10.5_1_1_1_Series_SteppedDiagonal_Representative.svg`; the `_Actual.svg` beside it is the copper at its true size).*

| Coil set | TX | SIN | COS | Frequency | Periods per revolution (N) | Electrical period |
|---|---|---|---|---|---|---|
| 1 | TX, 1 + 1 turns, r = 7.2 mm | SIN (net `2`) | COS (net `1`) | 3.5 MHz | 1 | 360° mechanical |

| RX band | Rotor copper ring | Sectors | Metal fraction |
|---|---|---|---|
| 3.2 to 6.1 mm | 2.52 to 7.8 mm | 1 | 0.50 |

Where each coil is opened for its terminals (KiCad coordinates, mm; the rotation axis is at (100, 100)):

| Net | Kind | Where | Terminals |
|---|---|---|---|
| `TX` (TX) | TX ends | (109.8, 100), F.Cu and B.Cu | the two coil ends, stacked at one point on two layers |
| `2` (SIN) | RX via (fallback) | via at (97.737, 102.263) | the generator found no cut spot: the via is left out, and its two pads are the terminals |
| `1` (COS) | RX via (fallback) | via at (97.737, 97.737) | as for SIN |

The fallback via of each RX coil is its layer-change via farthest from the TX copper (4.0 mm, on the inner edge of the band), of the two such on the side away from the TX terminal.

## How it was made

The generator at commit `32bf9cb`, S2's parameter files with five values changed (the files used are in [`parameter_files`](parameter_files/), and [`Parameters.txt`](Parameters.txt) is the generator's record of the run):

| Parameter | S2 | S0 | Why |
|---|---|---|---|
| `LOOPS` | 4 | 1 | one period per turn: the curves over a full turn are one sine and one cosine |
| `TX_TURNS` | 3 | 1 | less copper; the TX's turns add little to the coupling's shape |
| `INNER_EDGE_RADIUS_MM` | 10.0 | 2.0 | a small board |
| `OUTER_EDGE_RADIUS_MM` | 20.0 | 10.5 | 10.0 left a via 0.11 mm from other copper; 10.5 gives 0.274 mm (at least 0.2) |
| `PCB_THICKNESS_MM` | 1.6 | 0.8 | two fewer wedge layers through the board |

The generator's two warnings, both expected: the TX tank's parallel resistance would be about 12 Ω where the IPS2550 needs 250 Ω (more TX turns would fix it, at more mesh), and it found no spot with room for the two lead vias of each RX coil (so each RX coil is opened at a via instead).

## What the solver does

Elmer, magnetic (WhitneyAVHarmonicSolver with edge elements), every coil a massive coil of the circuit module, the same case as S2: the TX carries 1 A at 3.5 MHz, SIN and COS are open, and their voltages over the TX's current give their mutual inductances M. The EMF is 2πfM × 1 A: 1 nH is 22 mV at 3.5 MHz.

One solve per rotor angle, 0 to 330° in 30° steps by default (`--step 10` for every 10°), and one with the rotor away. The rotor is a half ring, so its outline turns with it and every angle gets its own mesh; the stator's mesh therefore differs a little between angles, which shows as small noise on the curves. The best sine fit and the rms of what it leaves are written with the results, so that noise is measured, not guessed.

| Mesh level | Nodes | Memory a solve | Fits |
|---|---|---|---|
| 0.75 (the default here) | 203,669 | 11.4 GB seen while solving the first angle (57 kB a node, as E01 and E02) | the 15 GB test machine |
| 1.0 (S2's) | about 280,000 | about 16 GB | a 32 GB machine |

## Running it

    python simulation.py                   # the rotor away, then 0 to 330 degrees every 30, at a 1 mm gap
    python simulation.py --gap 0.5         # the same at 0.5 mm
    python simulation.py --step 10         # every 10 degrees
    python simulation.py --plot            # redraw the table and the curves from the results

Each gap writes `results_gap<gap>mm.json` (every solve, the fit), `results_gap<gap>mm.csv` (angle, M of SIN and COS in nH, the TX's L, and the EMFs in mV) and `results_gap<gap>mm.png` (the two curves against the rotor's angle). An angle already in the results is skipped, so a stopped sweep picks up where it was.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [../LICENSE.md](../LICENSE.md); this branch's GPL-3.0 covers `simulation.py` only.
