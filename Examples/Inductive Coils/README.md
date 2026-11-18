# Inductive Coils

Inductive angle-encoder boards from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator), one folder each. A **stator** board carries one TX coil and two RX coils (SIN and COS). A **rotor** board with copper sectors sits 1.0 mm above it by default. The TX is driven at 3 to 5 MHz, the rotor's eddy currents change how much of the TX's field reaches each RX coil, and the two RX voltages follow the sine and cosine of the rotor's angle.

## What this branch checks

At 3 to 5 MHz the boards are about 1/2000 of a wavelength across, so the physics is magneto-quasi-static, which is what FastHenry solves. Per board it gives the TX's inductance and resistance with the rotor away and over the stator, the coupling from the TX to SIN and COS against the rotor's angle at each air gap, and what follows from it: how well SIN and COS match and the angle error. Each solve is FastHenry's dense direct solve, so its impedance matrix is the exact answer of the filament model and symmetric to the last digit: M from each receiver back to the TX equals M from the TX to it, which every solve is checked for. FastHenry's own default, GMRES with its multipole speed-up, left the two 2.7 % apart on these boards, and is not used.

How fine the filaments need to be was measured on [S0_1x_OD22_2L_tiny_TXtop](S0_1x_OD22_2L_tiny_TXtop/) at 1 mm and 0°, each track split into more filaments across its width and through its thickness, the rotor's grid kept:

| Filaments in each track | Filaments in the model | L TX | R TX | M SIN | M COS | Memory | Time on one core |
|---|---|---|---|---|---|---|---|
| 1 across, 1 through | 4,781 | 133.935 nH | 258.73 mΩ | −2.32104 nH | 2.52151 nH | 0.34 GB | 30 s |
| **3 across, 1 through (as solved)** | **7,117** | **133.988 nH** | **274.50 mΩ** | **−2.31623 nH** | **2.51557 nH** | **0.73 GB** | **136 s** |
| 5 across, 1 through | 9,453 | 133.998 nH | 278.55 mΩ | −2.31569 nH | 2.51485 nH | 1.54 GB | 485 s |
| 3 across, 2 through | 10,621 | 134.119 nH | 274.73 mΩ | −2.31610 nH | 2.51531 nH | 2.0 GB | 663 s |

From three filaments across to five, M SIN and M COS move by 0.03 % and L TX by 0.01 %; two through the copper instead of one move M by 0.01 % and L TX by 0.1 %. A finer rotor grid (bars 0.025 to 0.2 mm wide instead of 0.05 to 0.3 mm) moves M by 0.04 %, and a finer one still (0.02 to 0.15 mm) by 0.005 % more. So M and L TX are settled to a few hundredths of a percent. R TX is the number that still moves, 1.5 % from three filaments across to five, because at 3.5 MHz the skin depth (35 µm) is the copper's thickness and the current crowds to each track's edges more finely than three filaments follow.

## The boards here

All of them are S0 and boards made from it. A solve takes 0.7 to 1.1 GB and 1.2 to 5.9 min on one core, so a small machine runs several at once:

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

Every board is solved at 0.1, 0.5, 1, 1.5 and 2 mm, at 8 angles over the turn (S0d2 at 16), with the rotor taken away once at 1 mm: 286 solves, every one readable. SIN's amplitude, the best sine through each gap's solves (1 nH is 22 mV of EMF with 1 A at 3.5 MHz in the TX):

| Board | 0.1 mm | 0.5 mm | 1 mm | 1.5 mm | 2 mm |
|---|---|---|---|---|---|
| [S0](S0_1x_OD21_2L_tiny/) | 6.56 nH | 4.72 nH | 2.99 nH | 1.91 nH | 1.25 nH |
| [21 mm, 2 TX turns on top](S0_1x_OD21_2L_tiny_TXtop/) | 5.31 nH | 3.91 nH | 2.48 nH | 1.57 nH | 1.02 nH |
| [22 mm, 2 TX turns on top](S0_1x_OD22_2L_tiny_TXtop/) | 6.76 nH | 5.16 nH | 3.43 nH | 2.27 nH | 1.52 nH |
| [22 mm, 2 TX turns on top, opened by cuts](S0_1x_OD22_2L_tiny_TXtop_Cut/) | 6.70 nH | 5.12 nH | 3.40 nH | 2.25 nH | 1.50 nH |
| [23 mm, 3 TX turns on top, opened by cuts](S0_1x_OD23_2L_tiny_TX3top_Cut/) | 9.41 nH | 7.36 nH | 5.07 nH | 3.46 nH | 2.38 nH |
| [23 mm, 3 TX turns on top, opened by cuts, 2 periods per turn](S0d2_1x_OD23_2L_tiny_TX3top_Cut/) | 9.76 nH | 7.28 nH | 4.73 nH | 3.03 nH | 1.95 nH |

SIN and COS match within 0.3 % on every board. The angle error is 0.1° to 0.7° rms from 0.5 to 2 mm and up to 1.5° at 0.1 mm, where the fourth-harmonic ripple that two-coil sensors typically have shows. On S0, L TX with the rotor away is 135.3 nH, 2.1 % over a hand calculation that leaves out the leads to the terminal (two coaxial rings of 7.2 mm radius 0.765 mm apart, in series, 132.5 nH by Grover's and Maxwell's formulas). The first four boards (S0 to the 22 mm board opened by cuts) were solved before the bridge wrote the model about its middle and merged straight pieces of a trace; with the bridge as it is now their models are the same nodes, segments and filaments to the last one, and S0 solved again at 1 mm moves L TX by under 1e-5 and M by under 1e-4 (0.0003 nH), so they were not solved again. [`Comparisons/`](Comparisons/README.md) sets the boards side by side.

## A small board for the SIN and COS curves

[S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) is the smallest coil set the generator makes that is still a whole sensor (OD 21 mm, one period per turn, a TX of one turn per layer, a half-ring rotor). Its README says how it was made and how to run it.

Any other single coil set from the generator is set up the same way, in one command: [`new_coil.py`](new_coil.py) turns the generator's output folder into a folder here laid out as S0's (`Boards/` straight from the generator, `FastHenry Simulation/` with S0's `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`, which run it as they are, `Results/`, and `3D_Geometry/` with KESE's export of the boards once the first run makes it), and prints the filaments, memory and time a solve needs. The steps are in [S0's README](S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

## Placement and terminals, in short

* The rotation axis is KiCad's point (100, 100), z points up from the stator towards the rotor, and the top face of the stator's F.Cu copper is z = 0. KiCad's y axis points down, which flips every rotation sense in a y-up model; each results file says which convention the run used.
* The rotor is `Rotor.kicad_pcb` as drawn, not mirrored, copper side down, its copper face at z = +1.0 mm. Rotor angle θ turns it about the axis by (x, y) → (x cos θ − y sin θ, x sin θ + y cos θ) in KiCad's coordinates.
* KESE exports both boards with solder mask on both faces; FR-4 and mask are insulators with μr 1, which to these fields are air, so only the copper is drawn, and the air takes nothing.
* Each coil is opened where the real board gets its leads (`test_spec.json` → `terminals`): the TX at its two stacked ends, an RX by leaving one layer-change via out, or, in the `_Cut` folders, by a 0.2 mm cut across a top trace. A port is a pair of nodes: the TX's two end nodes, a left-out via's node on each layer (its bar is left out), or the nodes of a cut's two faces (the trace's copper inside the cut is left out). FastHenry gives the open-circuit impedances between the three ports, so a receiver's voltage is its open-circuit EMF.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [LICENSE.md](LICENSE.md); this branch's GPL-3.0 covers only the scripts here (`new_coil.py`, each board's `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`, and those in `Comparisons/`).
