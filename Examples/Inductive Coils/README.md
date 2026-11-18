# Inductive Coils

Inductive angle-encoder boards from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator), one folder each. A **stator** board carries one TX coil and two RX coils (SIN and COS). A **rotor** board with copper sectors sits 1.0 mm above it by default. The TX is driven at 3 to 5 MHz, the rotor's eddy currents change how much of the TX's field reaches each RX coil, and the two RX voltages follow the sine and cosine of the rotor's angle.

## What this branch checks

At 3 to 5 MHz the boards are about 1/2000 of a wavelength across, so the fields are magneto-quasi-static; Palace solves Maxwell's equations in full in the frequency domain, which at this size gives the same. Per board it gives the TX's inductance and resistance with the rotor away and over the stator, the coupling from the TX to SIN and COS against the rotor's angle at each air gap, and what follows from it: how well SIN and COS match and the angle error. Every solve is checked: its linear solve converged, the TX's L from its port's voltage equals the L from the magnetic energy of the whole field within 1 %, and at the first angle of each gap, where SIN and COS are driven in turn too, M is reciprocal within 1 %.

The mesh and the ports were settled on S0 at 1 mm and 0° ([its README](S0_1x_OD21_2L_tiny/README.md#what-the-solver-does) has the table). Grading the air round the thin tracks four times as finely as the bridge's default raised M by 3 to 4 % and L TX by 2 %, and wedge layers half as thick raised L TX by 1.4 % more; with both, as solved, M is within 0.5 % of the finest mesh that fits in 16 GB, and L TX, which first-order edge elements give from below, reads about 5 % low. Each left-out via's pads are filled over the drill hole, since a via that is left out is not drilled: a port sheet over the hole does not end on copper, and read M 13 % low when the mesh resolved it.

## The boards here

All of them are S0 and boards made from it. A solve takes 4.4 to 11.4 GB and 1 to 12 min on 2 or 4 MPI ranks, so a 16 GB machine runs one at a time, on all its cores:

| Board | What it is |
|---|---|
| [S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) | S0: 21 mm across, one period per turn, the TX one turn on each layer, a half-ring rotor |
| [S0_1x_OD21_2L_tiny_TXtop](S0_1x_OD21_2L_tiny_TXtop/) | the same board with the TX two turns on the top layer (the generator narrows the RX band to fit them) |
| [S0_1x_OD22_2L_tiny_TXtop](S0_1x_OD22_2L_tiny_TXtop/) | the TX two turns on the top layer around S0's own RX coils, the board grown to 22.2 mm |
| [S0_1x_OD22_2L_tiny_TXtop_Cut](S0_1x_OD22_2L_tiny_TXtop_Cut/) | the 22 mm board with SIN and COS opened by a cut in a top trace instead of a left-out via |
| [S0_1x_OD23_2L_tiny_TX3top_Cut](S0_1x_OD23_2L_tiny_TX3top_Cut/) | the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by cuts |
| [S0d2_1x_OD23_2L_tiny_TX3top_Cut](S0d2_1x_OD23_2L_tiny_TX3top_Cut/) | the three-turn board with two electrical periods per turn and a rotor of two sectors, so the curves repeat every 180°; solved at 16 angles over the whole turn |

Every board folder holds the same files and stands on its own: its README has the board, its results at each air gap and how to run it. [`Comparisons/`](Comparisons/) sets the boards side by side, with the scripts that print those tables and draw the charts.

## Results in short

Every board is solved at 0.1, 0.5, 1, 1.5 and 2 mm, at 8 angles over the turn (S0d2 at 16), with the rotor taken away once at 1 mm: 205 solves so far, every one readable. SIN's amplitude, the best sine through each gap's solves (1 nH is 22 mV of EMF with 1 A at 3.5 MHz in the TX):

| Board | 0.1 mm | 0.5 mm | 1 mm | 1.5 mm | 2 mm |
|---|---|---|---|---|---|
| [S0](S0_1x_OD21_2L_tiny/) | 6.44 nH | 4.62 nH | 2.93 nH | 1.88 nH | 1.23 nH |
| [21 mm, 2 TX turns on top](S0_1x_OD21_2L_tiny_TXtop/) | 5.20 nH | 3.82 nH | 2.42 nH | 1.53 nH | 1.00 nH |
| [22 mm, 2 TX turns on top](S0_1x_OD22_2L_tiny_TXtop/) | 6.66 nH | 5.07 nH | 3.37 nH | 2.23 nH | 1.49 nH |
| [22 mm, 2 TX turns on top, opened by cuts](S0_1x_OD22_2L_tiny_TXtop_Cut/) | 6.66 nH | 5.07 nH | 3.37 nH | 2.23 nH | 1.49 nH |
| [23 mm, 3 TX turns on top, opened by cuts](S0_1x_OD23_2L_tiny_TX3top_Cut/) | 9.38 nH | 7.31 nH | 5.03 nH | 3.43 nH | 2.36 nH |
| [23 mm, 3 TX turns on top, opened by cuts, 2 periods per turn](S0d2_1x_OD23_2L_tiny_TX3top_Cut/) | — | — | — | — | — |

SIN and COS match within 0.3 % on every board. The angle error is 0.1° to 0.7° rms from 0.5 to 2 mm and up to 1.5° at 0.1 mm, where the fourth-harmonic ripple that two-coil sensors typically have shows. On S0, L TX with the rotor away is 127.1 nH, 4.1 % under a hand calculation that leaves out the leads to the terminal (two coaxial rings of 7.2 mm radius 0.765 mm apart, in series, 132.5 nH by Grover's and Maxwell's formulas). [`Comparisons/`](Comparisons/README.md) sets the boards side by side.

## A small board for the SIN and COS curves

[S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) is the smallest coil set the generator makes that is still a whole sensor (OD 21 mm, one period per turn, a TX of one turn per layer, a half-ring rotor). Its README says how it was made and how to run it.

Any other single coil set from the generator is set up the same way, in one command: [`new_coil.py`](new_coil.py) turns the generator's output folder into a folder here laid out as S0's (`Boards/` straight from the generator, `Palace Simulation/` with S0's `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`, which run it as they are, `Results/`, and `3D_Geometry/` with KESE's export of the boards once the first run makes it), and prints the mesh, memory and time a solve needs. The steps are in [S0's README](S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

## Placement and terminals, in short

* The rotation axis is KiCad's point (100, 100), z points up from the stator towards the rotor, and the top face of the stator's F.Cu copper is z = 0. KiCad's y axis points down, which flips every rotation sense in a y-up model; each results file says which convention the run used.
* The rotor is `Rotor.kicad_pcb` as drawn, not mirrored, copper side down, its copper face at z = +1.0 mm. Rotor angle θ turns it about the axis by (x, y) → (x cos θ − y sin θ, x sin θ + y cos θ) in KiCad's coordinates.
* KESE exports both boards with solder mask on both faces; FR-4 and mask are insulators with μr 1, which to these fields are air, so only the copper is a material of its own; the air round it is meshed out to a cylinder whose radius is three board radii and whose outside is a perfect conductor.
* Each coil is opened where the real board gets its leads (`test_spec.json` → `terminals`): the TX at its two stacked ends, an RX by leaving one layer-change via out, or, in the `_Cut` folders, by a 0.2 mm cut across a top trace. Each opening holds a lumped port, a sheet with a resistance across it: between the TX's two ends and between a left-out via's two pads it stands across the board from one copper face to the other, and at a cut it spans the gap through the copper's thickness. The TX's port has 50 Ω and the drive; SIN's and COS's have 1 MΩ, which leaves them open to a few parts in a million, so the voltage across each is its open-circuit EMF.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [LICENSE.md](LICENSE.md); this branch's GPL-3.0 covers only the scripts here (`new_coil.py`, each board's `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`, and those in `Comparisons/`).
