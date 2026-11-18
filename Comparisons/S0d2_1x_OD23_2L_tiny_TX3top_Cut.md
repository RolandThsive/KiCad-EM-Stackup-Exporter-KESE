[Solvers comparison](../README.md) › S0d2

# S0d2_1x_OD23_2L_tiny_TX3top_Cut: the solvers compared

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

![S0d2 against the air gap](../charts/S0d2_1x_OD23_2L_tiny_TX3top_Cut.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

## At 1 mm

![The curves at 1 mm](../charts/S0d2_1x_OD23_2L_tiny_TX3top_Cut_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| **Theory** | no hand formula | no hand formula | ≤ 295.6 | 289.2 to 295.6 | ≥ 379.4 | 0 (ideal) | 0 (ideal) | — |
| Elmer | 4.511 | 4.514 | 250.3 | 274.2 | 460 | 0.212 | 0.440 | 16 |
| PyPEEC | 4.613 | 4.627 | 271.8 | 296.4 | 496 | 0.216 | 0.434 | 16 |
| FastHenry | 4.730 | 4.736 | 269.6 | 294.6 | 436 | 0.181 | 0.331 | 16 |
| Palace | 4.652 | 4.657 | 256.5 | 281.0 | 468 | 0.198 | 0.355 | 16 |

## Every air gap

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

## Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX. In the Theory column, in brackets, the most L TX can be (its DC value) over FastHenry's L TX; there is no hand value for the amplitude.

| Air gap | Elmer | PyPEEC | Palace | Theory |
|---|---|---|---|---|
| 0.1 mm | 0.967 (0.916) | 0.984 (1.013) | 0.994 (0.941) | — (≤ 1.268) |
| 0.5 mm | 0.958 (0.925) | 0.981 (1.006) | 0.987 (0.949) | — (≤ 1.156) |
| 1 mm | 0.954 (0.928) | 0.975 (1.008) | 0.983 (0.951) | — (≤ 1.096) |
| 1.5 mm | 0.953 (0.930) | 0.972 (1.011) | 0.983 (0.953) | — (≤ 1.066) |
| 2 mm | 0.953 (0.931) | 0.972 (1.007) | 0.984 (0.954) | — (≤ 1.048) |

## The hand values and the generator's estimates

The Theory row is worked out from the TX copper alone (see [Formulas](#formulas)). The generator's figures come from `Parameters.txt`, formulas rather than field solves: L TX 292 nH with the rotor away and 226 nH with it at 1 mm (which it calls an upper estimate of the drop, so the true value should be above it), and R TX 380 mΩ at DC.

| | L TX, rotor away (nH) | Against the hand values | Over the generator's estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) | R TX, rotor away (mΩ) |
|---|---|---|---|---|---|---|
| **Theory** | 289.2 to 295.6 | — | +1.2 % (DC value) | ≤ 295.6 | ≤ 295.6 | ≥ 379.4 |
| Generator | 292 | — | — | — | ≥ 226 | 380 (DC) |
| Elmer | 274.2 | 5.2 % under the high-frequency limit | −6.1 % | 213.6 | 250.3 | 438 |
| PyPEEC | 296.4 | 0.3 % over the DC value, the most it can be | +1.5 % | 236.1 | 271.8 | 475 |
| FastHenry | 294.6 | inside the hand values | +0.9 % | 233.2 | 269.6 | 413 |
| Palace | 281.0 | 2.8 % under the high-frequency limit | −3.8 % | 219.5 | 256.5 | 445 |

## Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on the same machine (4 cores, 15 GB), often while another solver shared it, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 382 | 217 to 583 | 13.3 |
| PyPEEC | 305 | 184 to 678 | 1.7 to 3.5 |
| FastHenry | 245 | 212 to 269 | 1.1 |
| Palace | 214 | 141 to 253 | 8.0 to 12.9 |
| Theory | 44 (once for the board: both of Neumann's sums) | — | 2.0 |

A receiver whose plus terminal sits on the other side in one branch comes out turned over; here Elmer COS, Palace COS, Palace SIN, PyPEEC COS is turned back to match FastHenry. Amplitudes and angle errors are the same either way.

## Formulas

How each Theory value is worked out, with this board's numbers. `scripts/theory.py` does the sums; its inputs are the TX copper in the board's `Boards/Stator.kicad_pcb` and the stack-up KESE exported with it (`3D_Geometry/Stator/materials.json`), read from the FastHenry branch (every branch has the same boards).

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

---

The proof boards, why the solvers differ, the data files and how to run it again are in the [branch's README](../README.md). The boards are the Sinusoidal Coil Generator's, for non-commercial use: see [LICENSE.md](../LICENSE.md).
