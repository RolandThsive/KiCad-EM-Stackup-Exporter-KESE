[Solvers comparison](../README.md) › OD23 Cut

# S0_1x_OD23_2L_tiny_TX3top_Cut: the solvers compared

**OD23 Cut**: the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by cuts.

| Solver | Gaps finished (of 5) | Solves | Passing their own checks |
|---|---|---|---|
| Elmer | 5 | 40 | 40 |
| PyPEEC | 5 | 40 | 40 |
| FastHenry | 5 | 40 | 40 |
| Palace | 5 | 40 | 40 |
| Theory | worked out from the copper by hand formulas, nothing to solve | — | — |

Against FastHenry, the yardstick (the closest to the reference on the proof boards):

- **Elmer** (FEM): the coupling (SIN's and COS's amplitude) is 3.7 % under FastHenry's on average over the 5 gaps both have finished (−4.0 to −3.0 %); L TX is 7.3 % under (−8.4 to −6.8 %); the rms angle error is within 0.09° of FastHenry's (electrical degrees).
- **PyPEEC** (PEEC): the coupling (SIN's and COS's amplitude) is 1.8 % under FastHenry's on average over the 5 gaps both have finished (−2.2 to −1.4 %); L TX is 1.1 % over (+0.8 to +1.5 %); the rms angle error is within 0.02° of FastHenry's (electrical degrees).
- **Palace** (FEM): the coupling (SIN's and COS's amplitude) is 0.7 % under FastHenry's on average over the 5 gaps both have finished (−0.9 to −0.3 %); L TX is 4.9 % under (−5.8 to −4.5 %); the rms angle error is within 0.07° of FastHenry's (electrical degrees).

Against the hand values (the Theory rows, worked out in [Formulas](#formulas)): with the rotor away, L TX has to lie between about 289.2 nH (all the current at the copper's surface) and 295.6 nH (its DC value, the most it can be at any frequency), and R TX can be no less than its DC resistance, 379.4 mΩ.

- **Elmer**: L TX with the rotor away 273.3 nH, 5.5 % under the high-frequency limit; R TX 438 mΩ, 15.6 % over its DC value.
- **PyPEEC**: L TX with the rotor away 296.7 nH, 0.4 % over the DC value, the most it can be; R TX 472 mΩ, 24.5 % over its DC value.
- **FastHenry**: L TX with the rotor away 294.6 nH, inside the hand values; R TX 413 mΩ, 8.9 % over its DC value.
- **Palace**: L TX with the rotor away 281.4 nH, 2.7 % under the high-frequency limit; R TX 441 mΩ, 16.3 % over its DC value.

![OD23 Cut against the air gap](../charts/S0_1x_OD23_2L_tiny_TX3top_Cut.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

## At 1 mm

![The curves at 1 mm](../charts/S0_1x_OD23_2L_tiny_TX3top_Cut_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| **Theory** | no hand formula | no hand formula | ≤ 295.6 | 289.2 to 295.6 | ≥ 379.4 | 0 (ideal) | 0 (ideal) | — |
| Elmer | 4.879 | 4.882 | 245.1 | 273.3 | 455 | 0.344 | 0.560 | 8 |
| PyPEEC | 4.984 | 4.986 | 266.4 | 296.7 | 493 | 0.318 | 0.489 | 8 |
| FastHenry | 5.074 | 5.081 | 263.8 | 294.6 | 436 | 0.300 | 0.418 | 8 |
| Palace | 5.031 | 5.037 | 251.2 | 281.4 | 463 | 0.350 | 0.450 | 8 |

## Every air gap

In the Theory column: L TX can be no more than its DC value and R TX no less than its DC resistance, at any gap; an ideal sensor's angle error is 0; and no hand formula gives the amplitudes (see [Formulas](#formulas)).

**SIN's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 9.123 | 9.276 | 9.407 | 9.381 | — |
| 0.5 mm | 7.099 | 7.255 | 7.361 | 7.309 | — |
| 1 mm | 4.879 | 4.984 | 5.074 | 5.031 | — |
| 1.5 mm | 3.321 | 3.386 | 3.457 | 3.427 | — |
| 2 mm | 2.286 | 2.329 | 2.377 | 2.360 | — |

**COS's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 9.125 | 9.276 | 9.410 | 9.385 | — |
| 0.5 mm | 7.101 | 7.256 | 7.367 | 7.315 | — |
| 1 mm | 4.882 | 4.986 | 5.081 | 5.037 | — |
| 1.5 mm | 3.324 | 3.387 | 3.462 | 3.434 | — |
| 2 mm | 2.287 | 2.330 | 2.382 | 2.365 | — |

**L TX, mean over the turn (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 203.1 | 224.9 | 221.6 | 208.8 | ≤ 295.6 |
| 0.5 mm | 229.0 | 249.4 | 247.4 | 234.9 | ≤ 295.6 |
| 1 mm | 245.1 | 266.4 | 263.8 | 251.2 | ≤ 295.6 |
| 1.5 mm | 254.3 | 276.5 | 273.2 | 260.7 | ≤ 295.6 |
| 2 mm | 260.1 | 281.5 | 279.1 | 266.5 | ≤ 295.6 |

**R TX, mean over the turn (mΩ)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 498 | 532 | 472 | 505 | ≥ 379.4 |
| 0.5 mm | 467 | 504 | 446 | 474 | ≥ 379.4 |
| 1 mm | 455 | 493 | 436 | 463 | ≥ 379.4 |
| 1.5 mm | 449 | 487 | 430 | 458 | ≥ 379.4 |
| 2 mm | 446 | 483 | 426 | 454 | ≥ 379.4 |

**Angle error, rms (electrical °)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 1.236 | 1.175 | 1.151 | 1.226 | 0 |
| 0.5 mm | 0.569 | 0.533 | 0.512 | 0.575 | 0 |
| 1 mm | 0.344 | 0.318 | 0.300 | 0.350 | 0 |
| 1.5 mm | 0.304 | 0.274 | 0.260 | 0.299 | 0 |
| 2 mm | 0.311 | 0.269 | 0.257 | 0.286 | 0 |

## Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX. In the Theory column, in brackets, the most L TX can be (its DC value) over FastHenry's L TX; there is no hand value for the amplitude.

| Air gap | Elmer | PyPEEC | Palace | Theory |
|---|---|---|---|---|
| 0.1 mm | 0.970 (0.916) | 0.986 (1.015) | 0.997 (0.942) | — (≤ 1.334) |
| 0.5 mm | 0.964 (0.926) | 0.986 (1.008) | 0.993 (0.949) | — (≤ 1.195) |
| 1 mm | 0.962 (0.929) | 0.982 (1.010) | 0.991 (0.952) | — (≤ 1.121) |
| 1.5 mm | 0.961 (0.931) | 0.980 (1.012) | 0.992 (0.954) | — (≤ 1.082) |
| 2 mm | 0.962 (0.932) | 0.980 (1.009) | 0.993 (0.955) | — (≤ 1.059) |

## The hand values and the generator's estimates

The Theory row is worked out from the TX copper alone (see [Formulas](#formulas)). The generator's figures come from `Parameters.txt`, formulas rather than field solves: L TX 292 nH with the rotor away and 226 nH with it at 1 mm (which it calls an upper estimate of the drop, so the true value should be above it), and R TX 380 mΩ at DC.

| | L TX, rotor away (nH) | Against the hand values | Over the generator's estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) | R TX, rotor away (mΩ) |
|---|---|---|---|---|---|---|
| **Theory** | 289.2 to 295.6 | — | +1.2 % (DC value) | ≤ 295.6 | ≤ 295.6 | ≥ 379.4 |
| Generator | 292 | — | — | — | ≥ 226 | 380 (DC) |
| Elmer | 273.3 | 5.5 % under the high-frequency limit | −6.4 % | 203.1 | 245.1 | 438 |
| PyPEEC | 296.7 | 0.4 % over the DC value, the most it can be | +1.6 % | 224.9 | 266.4 | 472 |
| FastHenry | 294.6 | inside the hand values | +0.9 % | 221.6 | 263.8 | 413 |
| Palace | 281.4 | 2.7 % under the high-frequency limit | −3.6 % | 208.8 | 251.2 | 441 |

## Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on machines of the same size (4 cores, 15 GB), often while another solver shared the machine, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve, and solved S0d2's five gaps on five such machines at once). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 279 | 160 to 392 | 13.3 |
| PyPEEC | 384 | 212 to 639 | 1.6 to 3.4 |
| FastHenry | 143 | 142 to 145 | 0.9 |
| Palace | 188 | 134 to 306 | 6.9 to 11.4 |
| Theory | 45 (once for the board: both of Neumann's sums) | — | 2.0 |

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

**5. No hand value for the amplitudes.** How much of the TX field reaches SIN and COS depends on the eddy currents in the rotor's copper, and no closed formula gives those: only a field solve does. The generator's note that the signal falls about as exp(−2π gap / period), with a period of 29.2 mm here, would keep SIN's amplitude at 2 mm at 66 % of its value at 0.1 mm; FastHenry finds 25 %. It is a rule of thumb, and is not used here.

**6. The generator's estimates.** L TX 292 nH with the rotor away, from its own formula (the DC value above is 1.2 % over it); 226 nH with the rotor at 1 mm, which it calls an upper estimate of the drop, so the true value should be above it (every solver's is); and R TX 380 mΩ at DC, rounded (the copper's 154.0 mm give 379.4 mΩ).

---

The proof boards, why the solvers differ, the data files and how to run it again are in the [branch's README](../README.md). The boards are the Sinusoidal Coil Generator's, for non-commercial use: see [LICENSE.md](../LICENSE.md).
