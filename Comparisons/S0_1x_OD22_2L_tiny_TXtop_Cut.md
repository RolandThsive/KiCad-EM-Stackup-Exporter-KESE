[Solvers comparison](../README.md) › OD22 Cut

# S0_1x_OD22_2L_tiny_TXtop_Cut: the solvers compared

**OD22 Cut**: the 22 mm board with SIN and COS opened by a 0.2 mm cut in a top trace instead of a left-out via.

| Solver | Gaps finished (of 5) | Solves | Passing their own checks |
|---|---|---|---|
| Elmer | 5 | 40 | 40 |
| PyPEEC | 5 | 40 | 40 |
| FastHenry | 5 | 40 | 40 |
| Palace | 5 | 40 | 40 |
| Theory | worked out from the copper by hand formulas, nothing to solve | — | — |

Against FastHenry, the yardstick (the closest to the reference on the proof boards):

- **Elmer** (FEM): the coupling (SIN's and COS's amplitude) is 4.0 % under FastHenry's on average over the 5 gaps both have finished (−4.3 to −3.3 %); L TX is 8.7 % under (−9.8 to −8.3 %); the rms angle error is within 0.09° of FastHenry's (electrical degrees).
- **PyPEEC** (PEEC): the coupling (SIN's and COS's amplitude) is 1.9 % under FastHenry's on average over the 5 gaps both have finished (−2.3 to −1.4 %); L TX is 1.3 % over (+0.9 to +1.9 %); the rms angle error is within 0.02° of FastHenry's (electrical degrees).
- **Palace** (FEM): the coupling (SIN's and COS's amplitude) is 0.8 % under FastHenry's on average over the 5 gaps both have finished (−1.1 to −0.5 %); L TX is 6.0 % under (−7.0 to −5.6 %); the rms angle error is within 0.06° of FastHenry's (electrical degrees).

Against the hand values (the Theory rows, worked out in [Formulas](#formulas)): with the rotor away, L TX has to lie between about 143.2 nH (all the current at the copper's surface) and 147.4 nH (its DC value, the most it can be at any frequency), and R TX can be no less than its DC resistance, 247.3 mΩ.

- **Elmer**: L TX with the rotor away 134.6 nH, 6.0 % under the high-frequency limit; R TX 280 mΩ, 13.3 % over its DC value.
- **PyPEEC**: L TX with the rotor away 148.2 nH, 0.5 % over the DC value, the most it can be; R TX 303 mΩ, 22.7 % over its DC value.
- **FastHenry**: L TX with the rotor away 146.9 nH, inside the hand values; R TX 264 mΩ, 6.8 % over its DC value.
- **Palace**: L TX with the rotor away 138.9 nH, 3.0 % under the high-frequency limit; R TX 282 mΩ, 13.9 % over its DC value.

![OD22 Cut against the air gap](../charts/S0_1x_OD22_2L_tiny_TXtop_Cut.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

## At 1 mm

![The curves at 1 mm](../charts/S0_1x_OD22_2L_tiny_TXtop_Cut_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| **Theory** | no hand formula | no hand formula | ≤ 147.4 | 143.2 to 147.4 | ≥ 247.3 | 0 (ideal) | 0 (ideal) | — |
| Elmer | 3.257 | 3.267 | 122.7 | 134.6 | 286 | 0.207 | 0.304 | 8 |
| PyPEEC | 3.340 | 3.342 | 135.6 | 148.2 | 313 | 0.179 | 0.333 | 8 |
| FastHenry | 3.403 | 3.410 | 134.1 | 146.9 | 274 | 0.155 | 0.237 | 8 |
| Palace | 3.368 | 3.374 | 126.2 | 138.9 | 292 | 0.195 | 0.276 | 8 |

## Every air gap

In the Theory column: L TX can be no more than its DC value and R TX no less than its DC resistance, at any gap; an ideal sensor's angle error is 0; and no hand formula gives the amplitudes (see [Formulas](#formulas)).

**SIN's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 6.466 | 6.600 | 6.695 | 6.661 | — |
| 0.5 mm | 4.912 | 5.040 | 5.117 | 5.069 | — |
| 1 mm | 3.257 | 3.340 | 3.403 | 3.368 | — |
| 1.5 mm | 2.149 | 2.198 | 2.246 | 2.226 | — |
| 2 mm | 1.441 | 1.473 | 1.504 | 1.495 | — |

**COS's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 6.476 | 6.600 | 6.700 | 6.665 | — |
| 0.5 mm | 4.923 | 5.042 | 5.124 | 5.075 | — |
| 1 mm | 3.267 | 3.342 | 3.410 | 3.374 | — |
| 1.5 mm | 2.156 | 2.200 | 2.252 | 2.231 | — |
| 2 mm | 1.447 | 1.475 | 1.509 | 1.499 | — |

**L TX, mean over the turn (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 100.9 | 113.9 | 111.8 | 104.0 | ≤ 147.4 |
| 0.5 mm | 115.2 | 127.4 | 126.2 | 118.5 | ≤ 147.4 |
| 1 mm | 122.7 | 135.6 | 134.1 | 126.2 | ≤ 147.4 |
| 1.5 mm | 126.7 | 140.2 | 138.3 | 130.5 | ≤ 147.4 |
| 2 mm | 129.1 | 142.2 | 140.8 | 132.9 | ≤ 147.4 |

**R TX, mean over the turn (mΩ)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 313 | 337 | 298 | 318 | ≥ 247.3 |
| 0.5 mm | 293 | 318 | 280 | 298 | ≥ 247.3 |
| 1 mm | 286 | 313 | 274 | 292 | ≥ 247.3 |
| 1.5 mm | 283 | 310 | 271 | 289 | ≥ 247.3 |
| 2 mm | 281 | 308 | 270 | 287 | ≥ 247.3 |

**Angle error, rms (electrical °)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 1.093 | 1.033 | 1.016 | 1.079 | 0 |
| 0.5 mm | 0.376 | 0.341 | 0.319 | 0.374 | 0 |
| 1 mm | 0.207 | 0.179 | 0.155 | 0.195 | 0 |
| 1.5 mm | 0.213 | 0.168 | 0.148 | 0.179 | 0 |
| 2 mm | 0.253 | 0.180 | 0.164 | 0.186 | 0 |

## Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX. In the Theory column, in brackets, the most L TX can be (its DC value) over FastHenry's L TX; there is no hand value for the amplitude.

| Air gap | Elmer | PyPEEC | Palace | Theory |
|---|---|---|---|---|
| 0.1 mm | 0.966 (0.902) | 0.986 (1.019) | 0.995 (0.930) | — (≤ 1.319) |
| 0.5 mm | 0.960 (0.913) | 0.985 (1.009) | 0.991 (0.939) | — (≤ 1.168) |
| 1 mm | 0.957 (0.915) | 0.981 (1.011) | 0.990 (0.941) | — (≤ 1.100) |
| 1.5 mm | 0.957 (0.916) | 0.979 (1.014) | 0.991 (0.944) | — (≤ 1.066) |
| 2 mm | 0.958 (0.917) | 0.979 (1.010) | 0.993 (0.944) | — (≤ 1.047) |

## The hand values and the generator's estimates

The Theory row is worked out from the TX copper alone (see [Formulas](#formulas)). The generator's figures come from `Parameters.txt`, formulas rather than field solves: L TX 144 nH with the rotor away and 116 nH with it at 1 mm (which it calls an upper estimate of the drop, so the true value should be above it), and R TX 250 mΩ at DC.

| | L TX, rotor away (nH) | Against the hand values | Over the generator's estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) | R TX, rotor away (mΩ) |
|---|---|---|---|---|---|---|
| **Theory** | 143.2 to 147.4 | — | +2.4 % (DC value) | ≤ 147.4 | ≤ 147.4 | ≥ 247.3 |
| Generator | 144 | — | — | — | ≥ 116 | 250 (DC) |
| Elmer | 134.6 | 6.0 % under the high-frequency limit | −6.5 % | 100.9 | 122.7 | 280 |
| PyPEEC | 148.2 | 0.5 % over the DC value, the most it can be | +2.9 % | 113.9 | 135.6 | 303 |
| FastHenry | 146.9 | inside the hand values | +2.0 % | 111.8 | 134.1 | 264 |
| Palace | 138.9 | 3.0 % under the high-frequency limit | −3.6 % | 104.0 | 126.2 | 282 |

## Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on the same machine (4 cores, 15 GB), often while another solver shared it, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 174 | 121 to 360 | 13.3 |
| PyPEEC | 246 | 155 to 471 | 1.5 to 3.0 |
| FastHenry | 194 | 178 to 279 | 0.7 |
| Palace | 163 | 122 to 213 | 6.2 to 9.9 |
| Theory | 18 (once for the board: both of Neumann's sums) | — | 1.2 |

A receiver whose plus terminal sits on the other side in one branch comes out turned over; here Elmer COS, Palace COS, Palace SIN, PyPEEC COS is turned back to match FastHenry. Amplitudes and angle errors are the same either way.

## Formulas

How each Theory value is worked out, with this board's numbers. `scripts/theory.py` does the sums; its inputs are the TX copper in the board's `Boards/Stator.kicad_pcb` and the stack-up KESE exported with it (`3D_Geometry/Stator/materials.json`), read from the FastHenry branch (every branch has the same boards).

**1. L TX with the rotor away: Neumann's formula, with the geometric mean distance.**

```math
L = \frac{\mu_0}{4\pi} \oint \oint \frac{d\mathbf{l} \cdot d\mathbf{l}'}{r}
```

over the TX copper's centre line, 100.4 mm of 0.2 mm × 35 µm trace from one terminal end to the other, with the via that joins the layers (the two ends sit stacked at the terminal, and the port closes the loop there at no length, as in E01). Along one stretch of trace (points less than 2 mm apart along the copper), r becomes √(r² + g²), where g is the geometric mean distance (GMD) of the trace's cross-section: a conductor's self-inductance is the mutual inductance of two thin filaments g apart (Rosa; Grover, *Inductance Calculations*). Between separate stretches of copper (neighbouring turns, and the two layers 0.725 mm apart), 1/r is averaged over both cross-sections, to second order. The sum runs over pieces of 0.05 mm with four Gauss points each.

- **DC**, the current spread evenly: g = 0.2235 (w + t) = 0.0525 mm (Grover), so **L = 147.4 nH**.
- **High-frequency limit**, the current all at the copper's surface: g is then the rectangle's logarithmic capacity, 0.0653 mm (from a boundary-element solve of the cross-section, which gives the known 0.25 w for a thin strip and 0.590 a for a square of side a), so **L = 143.2 nH**.

The same code on E01's loop gives 55.571 nH against the textbook 55.590 nH (−0.03 %).

**2. Why these bound the solvers.** With no magnetic material near, a coil's inductance can only fall, and its resistance only rise, as the frequency goes up; and copper brought near it (the rotor) only lowers L and adds loss. So at 3.5 MHz and at every air gap, L TX ≤ 147.4 nH and R TX ≥ 247.3 mΩ; with the rotor away, L TX lies between about 143.2 and 147.4 nH. The skin depth at 3.5 MHz,

```math
\delta = \frac{1}{\sqrt{\pi f \mu_0 \sigma}} = 35.3\ \mu\mathrm{m},
```

is the copper's own thickness, so the true value lies inside that range, not at either end. The lower end counts each trace on its own; the turns pushing each other's current about at high frequency would lower it by well under 1 %.

**3. R TX at DC.**

```math
R = \frac{\ell}{\sigma w t} = \frac{100.4\ \mathrm{mm}}{58\ \mathrm{MS/m} \times 0.2\ \mathrm{mm} \times 35\ \mu\mathrm{m}} = 247.3\ \mathrm{m}\Omega
```

The via adds well under 1 mΩ.

**4. Angle error 0.** The receivers are drawn so that SIN and COS follow the sine and cosine of the rotor angle exactly, and an ideal sensor's angle error is zero. It is the design's target, not a bound: a solver's error is the real board's departure from it plus the solver's own.

**5. No hand value for the amplitudes.** How much of the TX field reaches SIN and COS depends on the eddy currents in the rotor's copper, and no closed formula gives those: only a field solve does. The generator's note that the signal falls about as exp(−2π gap / period), with a period of 29.2 mm here, would keep SIN's amplitude at 2 mm at 66 % of its value at 0.1 mm; FastHenry finds 22 %. It is a rule of thumb, and is not used here.

**6. The generator's estimates.** L TX 144 nH with the rotor away, from its own formula (the DC value above is 2.4 % over it); 116 nH with the rotor at 1 mm, which it calls an upper estimate of the drop, so the true value should be above it (every solver's is); and R TX 250 mΩ at DC, rounded (the copper's 100.4 mm give 247.3 mΩ).

---

The proof boards, why the solvers differ, the data files and how to run it again are in the [branch's README](../README.md). The boards are the Sinusoidal Coil Generator's, for non-commercial use: see [LICENSE.md](../LICENSE.md).
