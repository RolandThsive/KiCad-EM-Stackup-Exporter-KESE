[Solvers comparison](../README.md) › S0d2

# S0d2_1x_OD23_2L_tiny_TX3top_Cut: the solvers compared

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

![S0d2 against the air gap](../charts/S0d2_1x_OD23_2L_tiny_TX3top_Cut.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

## At 1 mm

![The curves at 1 mm](../charts/S0d2_1x_OD23_2L_tiny_TX3top_Cut_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| Elmer | 4.511 | 4.514 | 250.3 | 274.2 | 460 | 0.212 | 0.440 | 16 |
| PyPEEC | 4.613 | 4.627 | 271.8 | 296.4 | 496 | 0.216 | 0.434 | 16 |
| FastHenry | 4.730 | 4.736 | 269.6 | 294.6 | 436 | 0.181 | 0.331 | 16 |

## Every air gap

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

## Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX.

| Air gap | Elmer | PyPEEC |
|---|---|---|
| 0.1 mm | 0.967 (0.916) | 0.984 (1.013) |
| 0.5 mm | 0.958 (0.925) | 0.981 (1.006) |
| 1 mm | 0.954 (0.928) | 0.975 (1.008) |
| 1.5 mm | 0.953 (0.930) | 0.972 (1.011) |
| 2 mm | 0.953 (0.931) | 0.972 (1.007) |

## The generator's estimates

The generator's own figures from `Parameters.txt`, formulas rather than field solves: L TX 292 nH with the rotor away and 226 nH with it (which it calls an upper estimate of the drop), and R TX 380 mΩ at DC.

| Solver | L TX, rotor away (nH) | Over the estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) |
|---|---|---|---|---|
| Elmer | 274.2 | −6.1 % | 213.6 | 250.3 |
| PyPEEC | 296.4 | +1.5 % | 236.1 | 271.8 |
| FastHenry | 294.6 | +0.9 % | 233.2 | 269.6 |

## Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on the same machine (4 cores, 15 GB), often while another solver shared it, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 382 | 217 to 583 | 13.3 |
| PyPEEC | 305 | 184 to 678 | 1.7 to 3.5 |
| FastHenry | 245 | 212 to 269 | 1.1 |

A receiver whose plus terminal sits on the other side in one branch comes out turned over; here Elmer COS, PyPEEC COS is turned back to match FastHenry. Amplitudes and angle errors are the same either way.

---

The proof boards, why the solvers differ, the data files and how to run it again are in the [branch's README](../README.md). The boards are the Sinusoidal Coil Generator's, for non-commercial use: see [LICENSE.md](../LICENSE.md).
