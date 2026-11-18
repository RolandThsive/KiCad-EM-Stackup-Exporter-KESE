# Solvers comparison: the KESE inductive-coil examples

KESE exports a KiCad board's copper and stackup for electromagnetic solvers. Four free, open-source solvers were run on the same six inductive position-sensor boards (a TX coil that drives the rotor, and SIN and COS receivers that read it), each on its own branch, with the same boards, the same air gaps (0.1, 0.5, 1, 1.5 and 2 mm), the same rotor angles and the same frequency (3.5 MHz, copper at 58 MS/m). This branch reads their results and compares them. It solves nothing itself.

| Solver | Method | Branch | Coil boards finished (of 6) | Solves | Passing their own checks |
|---|---|---|---|---|---|
| Elmer | FEM (finite elements, the A-V eddy-current formulation) | `Elmer_Integration` | 6 | 280 | 280 |
| PyPEEC | PEEC (partial elements on voxels, FFT-accelerated) | `PyPEEC_Integration` | 6 | 280 | 280 |
| FastHenry | PEEC (partial elements on filaments, direct solve) | `FastHenry_Integration` | 6 | 280 | 280 |
| Palace | FEM (finite elements, the frequency-domain Maxwell solver) | `Palace_Integration` | 6 | 280 | 280 |
| Theory | hand formulas: Neumann's integral over the TX copper, its DC resistance ([Formulas](#formulas)) | this one (`scripts/theory.py`) | 6 | — | — |

Each integration branch keeps its own solver's results, settings and checks, and knows nothing of the others. The numbers here are read from those branches unchanged by `scripts/collect.py`. The two FEM solvers mesh the air around the copper and close it at an outer boundary; the two PEEC solvers model only the copper, and the air's field comes from the free-space formulas, with no mesh and no boundary.

This page shows one board, S0d2_1x_OD23_2L_tiny_TX3top_Cut. Every board has its own page in [`Comparisons/`](Comparisons/), named as its folder in the integration branches:

| Board | What it is | SIN amplitude at 1 mm: Elmer, PyPEEC, FastHenry, Palace (nH) | L TX with the rotor away, Theory (nH) |
|---|---|---|---|
| [S0_1x_OD21_2L_tiny](Comparisons/S0_1x_OD21_2L_tiny.md) | S0: 21 mm across, one period per turn, the TX one turn on each layer, a half-ring rotor; SIN and COS opened at a left-out via | 2.81 / 2.94 / 2.99 / 2.93 | 131.4 to 135.7 |
| [S0_1x_OD21_2L_tiny_TXtop](Comparisons/S0_1x_OD21_2L_tiny_TXtop.md) | S0 TXtop: S0 with the TX two turns on the top layer (the generator narrows the RX band to fit them) | 2.35 / 2.43 / 2.48 / 2.42 | 129.1 to 133.0 |
| [S0_1x_OD22_2L_tiny_TXtop](Comparisons/S0_1x_OD22_2L_tiny_TXtop.md) | OD22 TXtop: the TX two turns on the top layer around S0's own RX coils, the board grown to 22.2 mm | 3.26 / 3.38 / 3.43 / 3.37 | 143.2 to 147.4 |
| [S0_1x_OD22_2L_tiny_TXtop_Cut](Comparisons/S0_1x_OD22_2L_tiny_TXtop_Cut.md) | OD22 Cut: the 22 mm board with SIN and COS opened by a 0.2 mm cut in a top trace instead of a left-out via | 3.26 / 3.34 / 3.40 / 3.37 | 143.2 to 147.4 |
| [S0_1x_OD23_2L_tiny_TX3top_Cut](Comparisons/S0_1x_OD23_2L_tiny_TX3top_Cut.md) | OD23 Cut: the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by cuts | 4.88 / 4.98 / 5.07 / 5.03 | 289.2 to 295.6 |
| [S0d2_1x_OD23_2L_tiny_TX3top_Cut](Comparisons/S0d2_1x_OD23_2L_tiny_TX3top_Cut.md) | S0d2: the three-turn 23 mm board with two electrical periods per turn and a rotor of two sectors, so the curves repeat every 180°; solved at 16 angles over the whole turn | 4.51 / 4.61 / 4.73 / 4.65 | 289.2 to 295.6 |

There is no hand formula for the SIN amplitude; the Theory column gives the range L TX must lie in with the rotor away (see [Formulas](#formulas)).

## S0d2_1x_OD23_2L_tiny_TX3top_Cut

**S0d2**: the three-turn 23 mm board with two electrical periods per turn and a rotor of two sectors, so the curves repeat every 180°; solved at 16 angles over the whole turn.

| Solver | Gaps finished (of 5) | Solves | Passing their own checks |
|---|---|---|---|
| Elmer | 5 | 80 | 80 |
| PyPEEC | 5 | 80 | 80 |
| FastHenry | 5 | 80 | 80 |
| Palace | 5 | 80 | 80 |
| Theory | worked out from the copper by hand formulas, nothing to solve | — | — |

Against FastHenry, the yardstick (the closest to the reference on the proof boards):

- **Elmer** (FEM): the coupling (SIN's and COS's amplitude) is 4.3 % under FastHenry's on average over the 5 gaps both have finished (−4.8 to −3.3 %); L TX is 7.4 % under (−8.4 to −6.9 %); the rms angle error is within 0.08° of FastHenry's (electrical degrees).
- **PyPEEC** (PEEC): the coupling (SIN's and COS's amplitude) is 2.2 % under FastHenry's on average over the 5 gaps both have finished (−2.8 to −1.4 %); L TX is 0.9 % over (+0.6 to +1.3 %); the rms angle error is within 0.04° of FastHenry's (electrical degrees).
- **Palace** (FEM): the coupling (SIN's and COS's amplitude) is 1.4 % under FastHenry's on average over the 5 gaps both have finished (−1.7 to −0.6 %); L TX is 5.0 % under (−5.9 to −4.6 %); the rms angle error is within 0.04° of FastHenry's (electrical degrees).

Against the hand values (the Theory rows, worked out in [Formulas](#formulas)): with the rotor away, L TX has to lie between about 289.2 nH (all the current at the copper's surface) and 295.6 nH (its DC value, the most it can be at any frequency), and R TX can be no less than its DC resistance, 379.4 mΩ.

- **Elmer**: L TX with the rotor away 274.2 nH, 5.2 % under the high-frequency limit; R TX 438 mΩ, 15.3 % over its DC value.
- **PyPEEC**: L TX with the rotor away 296.4 nH, 0.3 % over the DC value, the most it can be; R TX 475 mΩ, 25.2 % over its DC value.
- **FastHenry**: L TX with the rotor away 294.6 nH, inside the hand values; R TX 413 mΩ, 8.9 % over its DC value.
- **Palace**: L TX with the rotor away 281.0 nH, 2.8 % under the high-frequency limit; R TX 445 mΩ, 17.2 % over its DC value.

![S0d2 against the air gap](charts/S0d2_1x_OD23_2L_tiny_TX3top_Cut.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

### At 1 mm

![The curves at 1 mm](charts/S0d2_1x_OD23_2L_tiny_TX3top_Cut_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| **Theory** | no hand formula | no hand formula | ≤ 295.6 | 289.2 to 295.6 | ≥ 379.4 | 0 (ideal) | 0 (ideal) | — |
| Elmer | 4.511 | 4.514 | 250.3 | 274.2 | 460 | 0.212 | 0.440 | 16 |
| PyPEEC | 4.613 | 4.627 | 271.8 | 296.4 | 496 | 0.216 | 0.434 | 16 |
| FastHenry | 4.730 | 4.736 | 269.6 | 294.6 | 436 | 0.181 | 0.331 | 16 |
| Palace | 4.652 | 4.657 | 256.5 | 281.0 | 468 | 0.198 | 0.355 | 16 |

### Every air gap

In the Theory column: L TX can be no more than its DC value and R TX no less than its DC resistance, at any gap; an ideal sensor's angle error is 0; and no hand formula gives the amplitudes (see [Formulas](#formulas)).

**SIN's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 9.436 | 9.604 | 9.762 | 9.706 | — |
| 0.5 mm | 6.974 | 7.137 | 7.279 | 7.183 | — |
| 1 mm | 4.511 | 4.613 | 4.730 | 4.652 | — |
| 1.5 mm | 2.882 | 2.940 | 3.026 | 2.973 | — |
| 2 mm | 1.856 | 1.891 | 1.946 | 1.915 | — |

**COS's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 9.437 | 9.625 | 9.766 | 9.706 | — |
| 0.5 mm | 6.976 | 7.157 | 7.285 | 7.188 | — |
| 1 mm | 4.514 | 4.627 | 4.736 | 4.657 | — |
| 1.5 mm | 2.884 | 2.950 | 3.030 | 2.978 | — |
| 2 mm | 1.857 | 1.898 | 1.950 | 1.918 | — |

**L TX, mean over the turn (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 213.6 | 236.1 | 233.2 | 219.5 | ≤ 295.6 |
| 0.5 mm | 236.6 | 257.4 | 255.8 | 242.7 | ≤ 295.6 |
| 1 mm | 250.3 | 271.8 | 269.6 | 256.5 | ≤ 295.6 |
| 1.5 mm | 257.9 | 280.3 | 277.4 | 264.4 | ≤ 295.6 |
| 2 mm | 262.6 | 284.2 | 282.2 | 269.1 | ≤ 295.6 |

**R TX, mean over the turn (mΩ)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 509 | 540 | 475 | 517 | ≥ 379.4 |
| 0.5 mm | 473 | 508 | 447 | 481 | ≥ 379.4 |
| 1 mm | 460 | 496 | 436 | 468 | ≥ 379.4 |
| 1.5 mm | 453 | 490 | 430 | 462 | ≥ 379.4 |
| 2 mm | 449 | 486 | 426 | 457 | ≥ 379.4 |

**Angle error, rms (electrical °)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 0.917 | 0.892 | 0.862 | 0.906 | 0 |
| 0.5 mm | 0.386 | 0.384 | 0.349 | 0.381 | 0 |
| 1 mm | 0.212 | 0.216 | 0.181 | 0.198 | 0 |
| 1.5 mm | 0.181 | 0.173 | 0.139 | 0.143 | 0 |
| 2 mm | 0.197 | 0.157 | 0.122 | 0.115 | 0 |

### Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX. In the Theory column, in brackets, the most L TX can be (its DC value) over FastHenry's L TX; there is no hand value for the amplitude.

| Air gap | Elmer | PyPEEC | Palace | Theory |
|---|---|---|---|---|
| 0.1 mm | 0.967 (0.916) | 0.984 (1.013) | 0.994 (0.941) | — (≤ 1.268) |
| 0.5 mm | 0.958 (0.925) | 0.981 (1.006) | 0.987 (0.949) | — (≤ 1.156) |
| 1 mm | 0.954 (0.928) | 0.975 (1.008) | 0.983 (0.951) | — (≤ 1.096) |
| 1.5 mm | 0.953 (0.930) | 0.972 (1.011) | 0.983 (0.953) | — (≤ 1.066) |
| 2 mm | 0.953 (0.931) | 0.972 (1.007) | 0.984 (0.954) | — (≤ 1.048) |

### The hand values and the generator's estimates

The Theory row is worked out from the TX copper alone (see [Formulas](#formulas)). The generator's figures come from `Parameters.txt`, formulas rather than field solves: L TX 292 nH with the rotor away and 226 nH with it at 1 mm (which it calls an upper estimate of the drop, so the true value should be above it), and R TX 380 mΩ at DC.

| | L TX, rotor away (nH) | Against the hand values | Over the generator's estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) | R TX, rotor away (mΩ) |
|---|---|---|---|---|---|---|
| **Theory** | 289.2 to 295.6 | — | +1.2 % (DC value) | ≤ 295.6 | ≤ 295.6 | ≥ 379.4 |
| Generator | 292 | — | — | — | ≥ 226 | 380 (DC) |
| Elmer | 274.2 | 5.2 % under the high-frequency limit | −6.1 % | 213.6 | 250.3 | 438 |
| PyPEEC | 296.4 | 0.3 % over the DC value, the most it can be | +1.5 % | 236.1 | 271.8 | 475 |
| FastHenry | 294.6 | inside the hand values | +0.9 % | 233.2 | 269.6 | 413 |
| Palace | 281.0 | 2.8 % under the high-frequency limit | −3.8 % | 219.5 | 256.5 | 445 |

### Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on machines of the same size (4 cores, 15 GB), often while another solver shared the machine, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve, and solved S0d2's five gaps on five such machines at once). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 382 | 217 to 583 | 13.3 |
| PyPEEC | 305 | 184 to 678 | 1.7 to 3.5 |
| FastHenry | 245 | 212 to 269 | 1.1 |
| Palace | 214 | 141 to 253 | 8.0 to 12.9 |
| Theory | 44 (once for the board: both of Neumann's sums) | — | 2.0 |

A receiver whose plus terminal sits on the other side in one branch comes out turned over; here Elmer COS, Palace COS, Palace SIN, PyPEEC COS is turned back to match FastHenry. Amplitudes and angle errors are the same either way.

## The proof boards

![The proof boards](charts/proof.webp)

Two boards whose answer is known from a formula, solved by every branch: E01, one open circular loop (its L), and E02, two coaxial open loops (their M). The references are the same for every solver: Neumann's double integral over the open arcs, averaged across the traces' widths. E01's at 3.5 MHz is an estimate, since the skin depth there equals the copper's thickness. Each branch's own README compares with its own choice of formula; here they all meet one.

| Solver | E01, L, 10 kHz | E01, L, 3.5 MHz | E02, M, 10 kHz | E02, M, 3.5 MHz | Run |
|---|---|---|---|---|---|
| Elmer | 54.267 nH (−2.38 %) | — | 23.383 nH (−2.11 %) | 23.315 nH (−2.39 %) | as each branch solves it |
| Elmer | — | — | 23.866 nH (−0.08 %) | — | `results_grade.json` (a finer mesh, kept by the branch) |
| Elmer | 55.731 nH (+0.25 %) | — | — | — | `results_grade2.json` (a finer mesh, kept by the branch) |
| PyPEEC | 56.089 nH (+0.90 %) | 54.990 nH (−0.09 %) | 24.091 nH (+0.86 %) | 23.841 nH (−0.19 %) | as each branch solves it |
| FastHenry | 55.580 nH (−0.02 %) | 54.797 nH (−0.44 %) | 23.892 nH (+0.03 %) | 23.856 nH (−0.12 %) | as each branch solves it |
| Palace | 54.199 nH (−2.50 %) | 53.295 nH (−3.17 %) | 23.355 nH (−2.22 %) | 23.299 nH (−2.46 %) | as each branch solves it |
| Palace | 55.857 nH (+0.48 %) | 54.878 nH (−0.29 %) | 24.166 nH (+1.17 %) at 100 kHz | 24.104 nH (+0.91 %) | `results_grade.json` (a finer mesh, kept by the branch) |
| **Theory** | 55.590 nH | 53.37 to 55.59 nH (the branches use 55.039) | 23.886 nH | 23.886 nH | the references, by Neumann's integral ([Formulas](#the-proof-boards-references)) |

- **Palace's values sit above the open arcs.** Its lumped port is a sheet across each gap: the TX's current crosses it and the RX's EMF is taken across it, so Palace's loops are closed across their gaps, and once its mesh is fine enough its L and M should lie above the open arcs and near the closed rings. With the coil boards' air its E01 L is 0.48 % above the open arc and 1.4 % under the closed ring (56.622 nH), and its E02 M is 1.17 % above the open arcs and 1.0 % under the closed rings (24.400 nH). FastHenry's port closes its loop at no length, which is what the open arcs describe.
- **Palace's graded E02 is solved at 100 kHz** in place of 10 kHz: on its 303,129 node mesh GMRES does not converge at 10 kHz within 15 GB, and on the default mesh M at the two frequencies agrees to 0.002 %.

## Why they differ

**FEM against PEEC.** A FEM solver has to mesh the air, and on a coarse air mesh it stores too little magnetic energy, so L and M come out low and rise as the mesh is refined. Palace's mesh study on S0 at 1 mm shows it: at the bridges' default mesh L TX is 114.3 nH, with the air graded four times as finely and thinner layers 118.3 nH, and with the copper refined too 120.0 nH, against FastHenry's 126.3 nH at the same angle. The coupling moves less, 3 to 4 %, and had settled to 0.5 % at the mesh Palace's results use. The outer boundary also lowers L a little.

**Elmer and Palace agree on the same mesh.** On S0 at 1 mm and rotor angle 0, with the bridges' default mesh, Elmer gives L TX 114.27 nH and M 2.004 and 1.880 nH; Palace, two unrelated codes, gives 114.31 nH and 2.015 and 1.881 nH. So Elmer's 9 % deficit in L is its mesh, not its physics, and its branch's mesh ladder (which refines only the copper) cannot show it. Its proof board E01 says the same: −2.4 % at its default mesh, +0.25 % with the air graded finely. So does Palace's: −2.5 % at the finest level of its default mesh, +0.48 % with the coil boards' air.

**PyPEEC against FastHenry.** Both are PEEC, so the difference is how they cut up the copper. PyPEEC draws the tracks onto a grid of 50 µm voxels, which turns every arc into a staircase; FastHenry follows each track's centreline with straight filaments (3 across the width, 5° per segment at most). PyPEEC's coupling is about 2 % under FastHenry's and its L TX about 1 % over; on the proof boards PyPEEC is 0.9 % high at 10 kHz and settles towards the reference as its voxels shrink, while FastHenry is within 0.03 %.

**R TX is the least settled number.** At 3.5 MHz the skin depth in copper is 35 µm, the copper's own thickness, so R depends on how finely a solver resolves the current inside each track: FastHenry has one filament through the thickness, PyPEEC one voxel layer, the FEM meshes two element layers. FastHenry's R is the lowest, Elmer's about 5 % higher, PyPEEC's about 14 % higher. R does not enter M or the angle error.

**Palace's receiver port.** While setting Palace up, its receivers read M 11 to 13.5 % low whenever the mesh put a point inside the drill hole of the via that closes each receiver (KESE draws a via's pads with the hole, and Palace's port sheet stands across it). A via that a design leaves out is not drilled, so the Palace bridge now fills those pads over the hole, as PyPEEC's already did. Every Palace result compared here is solved with the fill. Elmer reads the pads' potentials, so it never saw this.

**The signs.** Where a receiver's plus terminal is on the other side in one branch than in another, its curve comes out turned over. The comparison turns it back (see "The data"); the amplitudes and the angle errors are the same either way.

## The data

| File | One row per | Columns |
|---|---|---|
| [data/solves.csv](data/solves.csv) | solve | solver, board, gap, rotor angle, M SIN and M COS (nH), L TX (nH), R TX (mΩ), whether it passed its branch's checks, seconds, peak memory |
| [data/summary.csv](data/summary.csv) | solver, board and gap | the best sine through SIN and COS (amplitude, offset, phase), the angle error (rms and peak, electrical degrees), L TX over the turn (mean, lowest, highest), R TX, L and R with the rotor away, seconds per solve, peak memory |
| [data/proof.csv](data/proof.csv) | proof-board value | solver, board, results file, frequency, value, reference, error (%), the run's settings |
| [data/generator.csv](data/generator.csv) | board | the generator's estimates of L TX (rotor away, with the rotor) and of R TX at DC |
| [data/theory.csv](data/theory.csv) | board | the hand values: L TX at DC and in the high-frequency limit, R TX at DC, and their inputs (the copper's length, width and thickness, the GMDs, the layers' spacing, the skin depth) |
| [data/theory_e01.csv](data/theory_e01.csv) | — | the same code on E01's loop, against its reference |

A port's plus side is each branch's own convention, so a receiver can come out with the opposite sign. Where a solver's curve is more than 90° from FastHenry's, its sign is turned (the `sign_turned_SIN` and `sign_turned_COS` columns say so); amplitudes and angle errors do not depend on it.

## Formulas

How each Theory value is worked out, with S0d2's numbers. `scripts/theory.py` does the sums; its inputs are the TX copper in the board's `Boards/Stator.kicad_pcb` and the stack-up KESE exported with it (`3D_Geometry/Stator/materials.json`), read from the FastHenry branch (every branch has the same boards).

**1. L TX with the rotor away: Neumann's formula, with the geometric mean distance.**

```math
L = \frac{\mu_0}{4\pi} \oint \oint \frac{d\mathbf{l} \cdot d\mathbf{l}'}{r}
```

over the TX copper's centre line, 154.0 mm of 0.2 mm × 35 µm trace from one terminal end to the other, with the via that joins the layers (the two ends sit stacked at the terminal, and the port closes the loop there at no length, as in E01). Along one stretch of trace (points less than 2 mm apart along the copper), r becomes √(r² + g²), where g is the geometric mean distance (GMD) of the trace's cross-section: a conductor's self-inductance is the mutual inductance of two thin filaments g apart (Rosa; Grover, *Inductance Calculations*). Between separate stretches of copper (neighbouring turns, and the two layers 0.725 mm apart), 1/r is averaged over both cross-sections, to second order. The sum runs over pieces of 0.05 mm with four Gauss points each.

- **DC**, the current spread evenly: g = 0.2235 (w + t) = 0.0525 mm (Grover), so **L = 295.6 nH**.
- **High-frequency limit**, the current all at the copper's surface: g is then the rectangle's logarithmic capacity, 0.0653 mm (from a boundary-element solve of the cross-section, which gives the known 0.25 w for a thin strip and 0.590 a for a square of side a), so **L = 289.2 nH**.

The same code on E01's loop gives 55.571 nH against the textbook 55.590 nH (−0.03 %).

**2. Why these bound the solvers.** With no magnetic material near, a coil's inductance can only fall, and its resistance only rise, as the frequency goes up; and copper brought near it (the rotor) only lowers L and adds loss. So at 3.5 MHz and at every air gap, L TX ≤ 295.6 nH and R TX ≥ 379.4 mΩ; with the rotor away, L TX lies between about 289.2 and 295.6 nH. The skin depth at 3.5 MHz,

```math
\delta = \frac{1}{\sqrt{\pi f \mu_0 \sigma}} = 35.3\ \mu\mathrm{m},
```

is the copper's own thickness, so the true value lies inside that range, not at either end. The lower end counts each trace on its own; the turns pushing each other's current about at high frequency would lower it by well under 1 %.

**3. R TX at DC.**

```math
R = \frac{\ell}{\sigma w t} = \frac{154.0\ \mathrm{mm}}{58\ \mathrm{MS/m} \times 0.2\ \mathrm{mm} \times 35\ \mu\mathrm{m}} = 379.4\ \mathrm{m}\Omega
```

The via adds well under 1 mΩ.

**4. Angle error 0.** The receivers are drawn so that SIN and COS follow the sine and cosine of the rotor angle exactly, and an ideal sensor's angle error is zero. It is the design's target, not a bound: a solver's error is the real board's departure from it plus the solver's own.

**5. No hand value for the amplitudes.** How much of the TX field reaches SIN and COS depends on the eddy currents in the rotor's copper, and no closed formula gives those: only a field solve does. The generator's note that the signal falls about as exp(−2π gap / period), with a period of 14.6 mm here, would keep SIN's amplitude at 2 mm at 44 % of its value at 0.1 mm; FastHenry finds 20 %. It is a rule of thumb, and is not used here.

**6. The generator's estimates.** L TX 292 nH with the rotor away, from its own formula (the DC value above is 1.2 % over it); 226 nH with the rotor at 1 mm, which it calls an upper estimate of the drop, so the true value should be above it (every solver's is); and R TX 380 mΩ at DC, rounded (the copper's 154.0 mm give 379.4 mΩ).

### The proof boards' references

E01 is one open circular loop, its trace 0.5 mm wide on a 10 mm radius, open by 0.2 mm; E02 is two such loops, one on each side of a board, 1.565 mm apart (copper centre to copper centre). Both references are Neumann's double integral over the open arcs, each over θ = 356.0°, between its round ends' centres:

```math
M_{12} = \frac{\mu_0 r_1 r_2}{4\pi} \int_0^{\theta}\!\int_0^{\theta} \frac{\cos(\varphi_1 - \varphi_2)\, d\varphi_1\, d\varphi_2}{\sqrt{r_1^2 + r_2^2 - 2 r_1 r_2 \cos(\varphi_1 - \varphi_2) + d^2}}
```

- E01's L is the loop's M with itself at d = g, the trace's GMD (the same method as the coils' L): g = 0.2235 (w + t) at DC gives 55.590 nH. At 3.5 MHz the branches use g = w / 4 = 0.125 mm, the GMD of a strip of no thickness with its current crowded to the edges, which gives 55.039 nH. With the copper's 35 µm thickness counted, the high-frequency limit's GMD is 0.1426 mm and L 53.37 nH; since the skin depth at 3.5 MHz equals the thickness, the true value lies between that and the DC value, 53.37 to 55.59 nH, and 55.039 nH is one point inside that range rather than an exact answer.
- E02's M is the two loops' M at d = 1.565 mm, averaged over both traces' widths with the current spread evenly (21 × 21 radii): 23.886 nH, used at both frequencies.

## Running it again

```
git fetch origin Elmer_Integration PyPEEC_Integration FastHenry_Integration Palace_Integration
python scripts/collect.py          # reads every branch into data/
python scripts/theory.py --check   # works out the hand values into data/ (a few minutes)
python scripts/charts.py           # draws charts/
python scripts/report.py           # writes this README and Comparisons/
```

It needs Python 3 with numpy and matplotlib (and Pillow for WebP). `collect.py --dir SOLVER=FOLDER` reads one solver from a checkout instead of git.

## Licence

The scripts are GPL-3.0 ([LICENSE](LICENSE)). The boards are the Sinusoidal Coil Generator's, and the data, charts and these pages describe them, so they keep its non-commercial terms: see [LICENSE.md](LICENSE.md).
