# Solvers comparison: the KESE inductive-coil examples

KESE exports a KiCad board's copper and stackup for electromagnetic solvers. Four free, open-source solvers were run on the same six inductive position-sensor boards (a TX coil that drives the rotor, and SIN and COS receivers that read it), each on its own branch, with the same boards, the same air gaps (0.1, 0.5, 1, 1.5 and 2 mm), the same rotor angles and the same frequency (3.5 MHz, copper at 58 MS/m). This branch reads their results and compares them. It solves nothing itself.

| Solver | Method | Branch | Coil boards finished (of 6) | Solves | Passing their own checks |
|---|---|---|---|---|---|
| Elmer | FEM (finite elements, the A-V eddy-current formulation) | `Elmer_Integration` | 6 | 280 | 280 |
| PyPEEC | PEEC (partial elements on voxels, FFT-accelerated) | `PyPEEC_Integration` | 6 | 280 | 280 |
| FastHenry | PEEC (partial elements on filaments, direct solve) | `FastHenry_Integration` | 6 | 280 | 280 |
| Palace | FEM (finite elements, the frequency-domain Maxwell solver) | `Palace_Integration` | 4 (still solving; 20 of 30 gaps) | 160 | 160 |

Each integration branch keeps its own solver's results, settings and checks, and knows nothing of the others. The numbers here are read from those branches unchanged by `scripts/collect.py`. The two FEM solvers mesh the air around the copper and close it at an outer boundary; the two PEEC solvers model only the copper, and the air's field comes from the free-space formulas, with no mesh and no boundary.

This page shows one board, S0d2_1x_OD23_2L_tiny_TX3top_Cut. Every board has its own page in [`Comparisons/`](Comparisons/), named as its folder in the integration branches:

| Board | What it is | SIN amplitude at 1 mm: Elmer, PyPEEC, FastHenry, Palace (nH) |
|---|---|---|
| [S0_1x_OD21_2L_tiny](Comparisons/S0_1x_OD21_2L_tiny.md) | S0: 21 mm across, one period per turn, the TX one turn on each layer, a half-ring rotor; SIN and COS opened at a left-out via | 2.81 / 2.94 / 2.99 / 2.93 |
| [S0_1x_OD21_2L_tiny_TXtop](Comparisons/S0_1x_OD21_2L_tiny_TXtop.md) | S0 TXtop: S0 with the TX two turns on the top layer (the generator narrows the RX band to fit them) | 2.35 / 2.43 / 2.48 / 2.42 |
| [S0_1x_OD22_2L_tiny_TXtop](Comparisons/S0_1x_OD22_2L_tiny_TXtop.md) | OD22 TXtop: the TX two turns on the top layer around S0's own RX coils, the board grown to 22.2 mm | 3.26 / 3.38 / 3.43 / 3.37 |
| [S0_1x_OD22_2L_tiny_TXtop_Cut](Comparisons/S0_1x_OD22_2L_tiny_TXtop_Cut.md) | OD22 Cut: the 22 mm board with SIN and COS opened by a 0.2 mm cut in a top trace instead of a left-out via | 3.26 / 3.34 / 3.40 / 3.37 |
| [S0_1x_OD23_2L_tiny_TX3top_Cut](Comparisons/S0_1x_OD23_2L_tiny_TX3top_Cut.md) | OD23 Cut: the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by cuts | 4.88 / 4.98 / 5.07 / — |
| [S0d2_1x_OD23_2L_tiny_TX3top_Cut](Comparisons/S0d2_1x_OD23_2L_tiny_TX3top_Cut.md) | S0d2: the three-turn 23 mm board with two electrical periods per turn and a rotor of two sectors, so the curves repeat every 180°; solved at 16 angles over the whole turn | 4.51 / 4.61 / 4.73 / — |

## S0d2_1x_OD23_2L_tiny_TX3top_Cut

**S0d2**: the three-turn 23 mm board with two electrical periods per turn and a rotor of two sectors, so the curves repeat every 180°; solved at 16 angles over the whole turn.

| Solver | Gaps finished (of 5) | Solves | Passing their own checks |
|---|---|---|---|
| Elmer | 5 | 80 | 80 |
| PyPEEC | 5 | 80 | 80 |
| FastHenry | 5 | 80 | 80 |
| Palace | 0 (still solving) | 0 | 0 |

Against FastHenry, the yardstick (the closest to the reference on the proof boards):

- **Elmer** (FEM): the coupling (SIN's and COS's amplitude) is 4.3 % under FastHenry's on average over the 5 gaps both have finished (−4.8 to −3.3 %); L TX is 7.4 % under (−8.4 to −6.9 %); the rms angle error is within 0.08° of FastHenry's (electrical degrees).
- **PyPEEC** (PEEC): the coupling (SIN's and COS's amplitude) is 2.2 % under FastHenry's on average over the 5 gaps both have finished (−2.8 to −1.4 %); L TX is 0.9 % over (+0.6 to +1.3 %); the rms angle error is within 0.04° of FastHenry's (electrical degrees).
- **Palace** has not finished a gap of this board yet; it is still solving.

![S0d2 against the air gap](charts/S0d2_1x_OD23_2L_tiny_TX3top_Cut.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

### At 1 mm

![The curves at 1 mm](charts/S0d2_1x_OD23_2L_tiny_TX3top_Cut_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| Elmer | 4.511 | 4.514 | 250.3 | 274.2 | 460 | 0.212 | 0.440 | 16 |
| PyPEEC | 4.613 | 4.627 | 271.8 | 296.4 | 496 | 0.216 | 0.434 | 16 |
| FastHenry | 4.730 | 4.736 | 269.6 | 294.6 | 436 | 0.181 | 0.331 | 16 |

### Every air gap

**SIN's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry |
|---|---|---|---|
| 0.1 mm | 9.436 | 9.604 | 9.762 |
| 0.5 mm | 6.974 | 7.137 | 7.279 |
| 1 mm | 4.511 | 4.613 | 4.730 |
| 1.5 mm | 2.882 | 2.940 | 3.026 |
| 2 mm | 1.856 | 1.891 | 1.946 |

**COS's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry |
|---|---|---|---|
| 0.1 mm | 9.437 | 9.625 | 9.766 |
| 0.5 mm | 6.976 | 7.157 | 7.285 |
| 1 mm | 4.514 | 4.627 | 4.736 |
| 1.5 mm | 2.884 | 2.950 | 3.030 |
| 2 mm | 1.857 | 1.898 | 1.950 |

**L TX, mean over the turn (nH)**

| Air gap | Elmer | PyPEEC | FastHenry |
|---|---|---|---|
| 0.1 mm | 213.6 | 236.1 | 233.2 |
| 0.5 mm | 236.6 | 257.4 | 255.8 |
| 1 mm | 250.3 | 271.8 | 269.6 |
| 1.5 mm | 257.9 | 280.3 | 277.4 |
| 2 mm | 262.6 | 284.2 | 282.2 |

**R TX, mean over the turn (mΩ)**

| Air gap | Elmer | PyPEEC | FastHenry |
|---|---|---|---|
| 0.1 mm | 509 | 540 | 475 |
| 0.5 mm | 473 | 508 | 447 |
| 1 mm | 460 | 496 | 436 |
| 1.5 mm | 453 | 490 | 430 |
| 2 mm | 449 | 486 | 426 |

**Angle error, rms (electrical °)**

| Air gap | Elmer | PyPEEC | FastHenry |
|---|---|---|---|
| 0.1 mm | 0.917 | 0.892 | 0.862 |
| 0.5 mm | 0.386 | 0.384 | 0.349 |
| 1 mm | 0.212 | 0.216 | 0.181 |
| 1.5 mm | 0.181 | 0.173 | 0.139 |
| 2 mm | 0.197 | 0.157 | 0.122 |

### Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX.

| Air gap | Elmer | PyPEEC |
|---|---|---|
| 0.1 mm | 0.967 (0.916) | 0.984 (1.013) |
| 0.5 mm | 0.958 (0.925) | 0.981 (1.006) |
| 1 mm | 0.954 (0.928) | 0.975 (1.008) |
| 1.5 mm | 0.953 (0.930) | 0.972 (1.011) |
| 2 mm | 0.953 (0.931) | 0.972 (1.007) |

### The generator's estimates

The generator's own figures from `Parameters.txt`, formulas rather than field solves: L TX 292 nH with the rotor away and 226 nH with it (which it calls an upper estimate of the drop), and R TX 380 mΩ at DC.

| Solver | L TX, rotor away (nH) | Over the estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) |
|---|---|---|---|---|
| Elmer | 274.2 | −6.1 % | 213.6 | 250.3 |
| PyPEEC | 296.4 | +1.5 % | 236.1 | 271.8 |
| FastHenry | 294.6 | +0.9 % | 233.2 | 269.6 |

### Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on the same machine (4 cores, 15 GB), often while another solver shared it, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 382 | 217 to 583 | 13.3 |
| PyPEEC | 305 | 184 to 678 | 1.7 to 3.5 |
| FastHenry | 245 | 212 to 269 | 1.1 |

A receiver whose plus terminal sits on the other side in one branch comes out turned over; here Elmer COS, PyPEEC COS is turned back to match FastHenry. Amplitudes and angle errors are the same either way.

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
| Palace | still to solve | | | | |

The references: E01 at 10 kHz 55.590 nH; E01 at 3.5 MHz 55.039 nH; E02 at 10 kHz 23.886 nH; E02 at 3.5 MHz 23.886 nH.

## Why they differ

**FEM against PEEC.** A FEM solver has to mesh the air, and on a coarse air mesh it stores too little magnetic energy, so L and M come out low and rise as the mesh is refined. Palace's mesh study on S0 at 1 mm shows it: at the bridges' default mesh L TX is 114.3 nH, with the air graded four times as finely and thinner layers 118.3 nH, and with the copper refined too 120.0 nH, against FastHenry's 126.3 nH at the same angle. The coupling moves less, 3 to 4 %, and had settled to 0.5 % at the mesh Palace's results use. The outer boundary also lowers L a little.

**Elmer and Palace agree on the same mesh.** On S0 at 1 mm and rotor angle 0, with the bridges' default mesh, Elmer gives L TX 114.27 nH and M 2.004 and 1.880 nH; Palace, two unrelated codes, gives 114.31 nH and 2.015 and 1.881 nH. So Elmer's 9 % deficit in L is its mesh, not its physics, and its branch's mesh ladder (which refines only the copper) cannot show it. Its proof board E01 says the same: −2.4 % at its default mesh, +0.25 % with the air graded finely.

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

A port's plus side is each branch's own convention, so a receiver can come out with the opposite sign. Where a solver's curve is more than 90° from FastHenry's, its sign is turned (the `sign_turned_SIN` and `sign_turned_COS` columns say so); amplitudes and angle errors do not depend on it.

## Running it again

```
git fetch origin Elmer_Integration PyPEEC_Integration FastHenry_Integration Palace_Integration
python scripts/collect.py          # reads every branch into data/
python scripts/charts.py           # draws charts/
python scripts/report.py           # writes this README and Comparisons/
```

It needs Python 3 with numpy and matplotlib (and Pillow for WebP). `collect.py --dir SOLVER=FOLDER` reads one solver from a checkout instead of git.

## Licence

The scripts are GPL-3.0 ([LICENSE](LICENSE)). The boards are the Sinusoidal Coil Generator's, and the data, charts and these pages describe them, so they keep its non-commercial terms: see [LICENSE.md](LICENSE.md).
