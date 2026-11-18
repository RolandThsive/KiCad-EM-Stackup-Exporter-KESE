[Solvers comparison](../README.md) › S0

# S0_1x_OD21_2L_tiny: the solvers compared

**S0**: 21 mm across, one period per turn, the TX one turn on each layer, a half-ring rotor; SIN and COS opened at a left-out via.

| Solver | Gaps finished (of 5) | Solves | Passing their own checks |
|---|---|---|---|
| Elmer | 5 | 40 | 40 |
| PyPEEC | 5 | 40 | 40 |
| FastHenry | 5 | 40 | 40 |
| Palace | 5 | 40 | 40 |
| Theory | worked out from the copper by hand formulas, nothing to solve | — | — |

Against FastHenry, the yardstick (the closest to the reference on the proof boards):

- **Elmer** (FEM): the coupling (SIN's and COS's amplitude) is 5.7 % under FastHenry's on average over the 5 gaps both have finished (−6.1 to −5.1 %); L TX is 9.7 % under (−10.5 to −9.4 %); the rms angle error is within 0.17° of FastHenry's (electrical degrees).
- **PyPEEC** (PEEC): the coupling (SIN's and COS's amplitude) is 1.7 % under FastHenry's on average over the 5 gaps both have finished (−2.0 to −1.2 %); L TX is 1.2 % over (+0.9 to +1.9 %); the rms angle error is within 0.01° of FastHenry's (electrical degrees).
- **Palace** (FEM): the coupling (SIN's and COS's amplitude) is 2.0 % under FastHenry's on average over the 5 gaps both have finished (−2.2 to −1.7 %); L TX is 6.5 % under (−7.1 to −6.1 %); the rms angle error is within 0.06° of FastHenry's (electrical degrees).

Against the hand values (the Theory rows, worked out in [Formulas](#formulas)): with the rotor away, L TX has to lie between about 131.4 nH (all the current at the copper's surface) and 135.7 nH (its DC value, the most it can be at any frequency), and R TX can be no less than its DC resistance, 234.5 mΩ.

- **Elmer**: L TX with the rotor away 122.6 nH, 6.7 % under the high-frequency limit; R TX 264 mΩ, 12.4 % over its DC value.
- **PyPEEC**: L TX with the rotor away 136.5 nH, 0.6 % over the DC value, the most it can be; R TX 287 mΩ, 22.4 % over its DC value.
- **FastHenry**: L TX with the rotor away 135.3 nH, inside the hand values; R TX 249 mΩ, 6.1 % over its DC value.
- **Palace**: L TX with the rotor away 127.1 nH, 3.3 % under the high-frequency limit; R TX 267 mΩ, 14.0 % over its DC value.

![S0 against the air gap](../charts/S0_1x_OD21_2L_tiny.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

## At 1 mm

![The curves at 1 mm](../charts/S0_1x_OD21_2L_tiny_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| **Theory** | no hand formula | no hand formula | ≤ 135.7 | 131.4 to 135.7 | ≥ 234.5 | 0 (ideal) | 0 (ideal) | — |
| Elmer | 2.812 | 2.820 | 114.3 | 122.6 | 271 | 0.141 | 0.289 | 8 |
| PyPEEC | 2.937 | 2.944 | 127.8 | 136.5 | 294 | 0.062 | 0.107 | 8 |
| FastHenry | 2.989 | 2.995 | 126.4 | 135.3 | 257 | 0.050 | 0.105 | 8 |
| Palace | 2.926 | 2.930 | 118.3 | 127.1 | 276 | 0.069 | 0.098 | 8 |

## Every air gap

In the Theory column: L TX can be no more than its DC value and R TX no less than its DC resistance, at any gap; an ideal sensor's angle error is 0; and no hand formula gives the amplitudes (see [Formulas](#formulas)).

**SIN's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 6.225 | 6.478 | 6.561 | 6.437 | — |
| 0.5 mm | 4.452 | 4.657 | 4.720 | 4.618 | — |
| 1 mm | 2.812 | 2.937 | 2.989 | 2.926 | — |
| 1.5 mm | 1.798 | 1.874 | 1.913 | 1.875 | — |
| 2 mm | 1.178 | 1.230 | 1.255 | 1.233 | — |

**COS's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 6.232 | 6.486 | 6.567 | 6.440 | — |
| 0.5 mm | 4.462 | 4.666 | 4.728 | 4.624 | — |
| 1 mm | 2.820 | 2.944 | 2.995 | 2.930 | — |
| 1.5 mm | 1.804 | 1.879 | 1.918 | 1.878 | — |
| 2 mm | 1.184 | 1.233 | 1.258 | 1.234 | — |

**L TX, mean over the turn (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 99.4 | 113.1 | 111.0 | 103.1 | ≤ 135.7 |
| 0.5 mm | 109.2 | 122.1 | 121.0 | 113.1 | ≤ 135.7 |
| 1 mm | 114.3 | 127.8 | 126.4 | 118.3 | ≤ 135.7 |
| 1.5 mm | 117.1 | 131.1 | 129.3 | 121.3 | ≤ 135.7 |
| 2 mm | 118.8 | 132.3 | 131.0 | 123.0 | ≤ 135.7 |

**R TX, mean over the turn (mΩ)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 290 | 311 | 275 | 294 | ≥ 234.5 |
| 0.5 mm | 276 | 298 | 262 | 280 | ≥ 234.5 |
| 1 mm | 271 | 294 | 257 | 276 | ≥ 234.5 |
| 1.5 mm | 268 | 292 | 255 | 274 | ≥ 234.5 |
| 2 mm | 267 | 291 | 253 | 272 | ≥ 234.5 |

**Angle error, rms (electrical °)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace | Theory |
|---|---|---|---|---|---|
| 0.1 mm | 0.465 | 0.532 | 0.520 | 0.517 | 0 |
| 0.5 mm | 0.088 | 0.088 | 0.077 | 0.092 | 0 |
| 1 mm | 0.141 | 0.062 | 0.050 | 0.069 | 0 |
| 1.5 mm | 0.185 | 0.080 | 0.066 | 0.108 | 0 |
| 2 mm | 0.271 | 0.110 | 0.098 | 0.161 | 0 |

## Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX. In the Theory column, in brackets, the most L TX can be (its DC value) over FastHenry's L TX; there is no hand value for the amplitude.

| Air gap | Elmer | PyPEEC | Palace | Theory |
|---|---|---|---|---|
| 0.1 mm | 0.949 (0.895) | 0.987 (1.019) | 0.981 (0.929) | — (≤ 1.222) |
| 0.5 mm | 0.943 (0.902) | 0.987 (1.009) | 0.979 (0.934) | — (≤ 1.121) |
| 1 mm | 0.941 (0.904) | 0.983 (1.011) | 0.979 (0.936) | — (≤ 1.073) |
| 1.5 mm | 0.940 (0.906) | 0.980 (1.014) | 0.981 (0.938) | — (≤ 1.049) |
| 2 mm | 0.939 (0.906) | 0.980 (1.010) | 0.983 (0.939) | — (≤ 1.035) |

## The hand values and the generator's estimates

The Theory row is worked out from the TX copper alone (see [Formulas](#formulas)). The generator's figures come from `Parameters.txt`, formulas rather than field solves: L TX 132 nH with the rotor away and 109 nH with it at 1 mm (which it calls an upper estimate of the drop, so the true value should be above it), and R TX 230 mΩ at DC.

| | L TX, rotor away (nH) | Against the hand values | Over the generator's estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) | R TX, rotor away (mΩ) |
|---|---|---|---|---|---|---|
| **Theory** | 131.4 to 135.7 | — | +2.8 % (DC value) | ≤ 135.7 | ≤ 135.7 | ≥ 234.5 |
| Generator | 132 | — | — | — | ≥ 109 | 230 (DC) |
| Elmer | 122.6 | 6.7 % under the high-frequency limit | −7.1 % | 99.4 | 114.3 | 264 |
| PyPEEC | 136.5 | 0.6 % over the DC value, the most it can be | +3.4 % | 113.1 | 127.8 | 287 |
| FastHenry | 135.3 | inside the hand values | +2.5 % | 111.0 | 126.4 | 249 |
| Palace | 127.1 | 3.3 % under the high-frequency limit | −3.7 % | 103.1 | 118.3 | 267 |

## Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on the same machine (4 cores, 15 GB), often while another solver shared it, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 158 | 115 to 249 | 13.1 to 13.3 |
| PyPEEC | 219 | 138 to 419 | 1.3 to 2.7 |
| FastHenry | 86 | 78 to 106 | 0.7 |
| Palace | 210 | 121 to 305 | 5.9 to 9.3 |
| Theory | 16 (once for the board: both of Neumann's sums) | — | 1.2 |

## Formulas

How each Theory value is worked out, with this board's numbers. `scripts/theory.py` does the sums; its inputs are the TX copper in the board's `Boards/Stator.kicad_pcb` and the stack-up KESE exported with it (`3D_Geometry/Stator/materials.json`), read from the FastHenry branch (every branch has the same boards).

**1. L TX with the rotor away: Neumann's formula, with the geometric mean distance.**

```math
L = \frac{\mu_0}{4\pi} \oint \oint \frac{d\mathbf{l} \cdot d\mathbf{l}'}{r}
```

over the TX copper's centre line, 95.2 mm of 0.2 mm × 35 µm trace from one terminal end to the other, with the via that joins the layers (the two ends sit stacked at the terminal, and the port closes the loop there at no length, as in E01). Along one stretch of trace (points less than 2 mm apart along the copper), r becomes √(r² + g²), where g is the geometric mean distance (GMD) of the trace's cross-section: a conductor's self-inductance is the mutual inductance of two thin filaments g apart (Rosa; Grover, *Inductance Calculations*). Between separate stretches of copper (neighbouring turns, and the two layers 0.725 mm apart), 1/r is averaged over both cross-sections, to second order. The sum runs over pieces of 0.05 mm with four Gauss points each.

- **DC**, the current spread evenly: g = 0.2235 (w + t) = 0.0525 mm (Grover), so **L = 135.7 nH**.
- **High-frequency limit**, the current all at the copper's surface: g is then the rectangle's logarithmic capacity, 0.0653 mm (from a boundary-element solve of the cross-section, which gives the known 0.25 w for a thin strip and 0.590 a for a square of side a), so **L = 131.4 nH**.

The same code on E01's loop gives 55.571 nH against the textbook 55.590 nH (−0.03 %).

**2. Why these bound the solvers.** With no magnetic material near, a coil's inductance can only fall, and its resistance only rise, as the frequency goes up; and copper brought near it (the rotor) only lowers L and adds loss. So at 3.5 MHz and at every air gap, L TX ≤ 135.7 nH and R TX ≥ 234.5 mΩ; with the rotor away, L TX lies between about 131.4 and 135.7 nH. The skin depth at 3.5 MHz,

```math
\delta = \frac{1}{\sqrt{\pi f \mu_0 \sigma}} = 35.3\ \mu\mathrm{m},
```

is the copper's own thickness, so the true value lies inside that range, not at either end. The lower end counts each trace on its own; the turns pushing each other's current about at high frequency would lower it by well under 1 %.

**3. R TX at DC.**

```math
R = \frac{\ell}{\sigma w t} = \frac{95.2\ \mathrm{mm}}{58\ \mathrm{MS/m} \times 0.2\ \mathrm{mm} \times 35\ \mu\mathrm{m}} = 234.5\ \mathrm{m}\Omega
```

The via adds well under 1 mΩ.

**4. Angle error 0.** The receivers are drawn so that SIN and COS follow the sine and cosine of the rotor angle exactly, and an ideal sensor's angle error is zero. It is the design's target, not a bound: a solver's error is the real board's departure from it plus the solver's own.

**5. No hand value for the amplitudes.** How much of the TX field reaches SIN and COS depends on the eddy currents in the rotor's copper, and no closed formula gives those: only a field solve does. The generator's note that the signal falls about as exp(−2π gap / period), with a period of 29.2 mm here, would keep SIN's amplitude at 2 mm at 66 % of its value at 0.1 mm; FastHenry finds 19 %. It is a rule of thumb, and is not used here.

**6. The generator's estimates.** L TX 132 nH with the rotor away, from its own formula (the DC value above is 2.8 % over it); 109 nH with the rotor at 1 mm, which it calls an upper estimate of the drop, so the true value should be above it (every solver's is); and R TX 230 mΩ at DC, rounded (the copper's 95.2 mm give 234.5 mΩ).

---

The proof boards, why the solvers differ, the data files and how to run it again are in the [branch's README](../README.md). The boards are the Sinusoidal Coil Generator's, for non-commercial use: see [LICENSE.md](../LICENSE.md).
