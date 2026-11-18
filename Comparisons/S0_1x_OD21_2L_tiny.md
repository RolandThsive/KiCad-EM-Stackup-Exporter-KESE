[Solvers comparison](../README.md) › S0

# S0_1x_OD21_2L_tiny: the solvers compared

**S0**: 21 mm across, one period per turn, the TX one turn on each layer, a half-ring rotor; SIN and COS opened at a left-out via.

| Solver | Gaps finished (of 5) | Solves | Passing their own checks |
|---|---|---|---|
| Elmer | 5 | 40 | 40 |
| PyPEEC | 5 | 40 | 40 |
| FastHenry | 5 | 40 | 40 |
| Palace | 5 | 40 | 40 |

Against FastHenry, the yardstick (the closest to the reference on the proof boards):

- **Elmer** (FEM): the coupling (SIN's and COS's amplitude) is 5.7 % under FastHenry's on average over the 5 gaps both have finished (−6.1 to −5.1 %); L TX is 9.7 % under (−10.5 to −9.4 %); the rms angle error is within 0.17° of FastHenry's (electrical degrees).
- **PyPEEC** (PEEC): the coupling (SIN's and COS's amplitude) is 1.7 % under FastHenry's on average over the 5 gaps both have finished (−2.0 to −1.2 %); L TX is 1.2 % over (+0.9 to +1.9 %); the rms angle error is within 0.01° of FastHenry's (electrical degrees).
- **Palace** (FEM): the coupling (SIN's and COS's amplitude) is 2.0 % under FastHenry's on average over the 5 gaps both have finished (−2.2 to −1.7 %); L TX is 6.5 % under (−7.1 to −6.1 %); the rms angle error is within 0.06° of FastHenry's (electrical degrees).

![S0 against the air gap](../charts/S0_1x_OD21_2L_tiny.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

## At 1 mm

![The curves at 1 mm](../charts/S0_1x_OD21_2L_tiny_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| Elmer | 2.812 | 2.820 | 114.3 | 122.6 | 271 | 0.141 | 0.289 | 8 |
| PyPEEC | 2.937 | 2.944 | 127.8 | 136.5 | 294 | 0.062 | 0.107 | 8 |
| FastHenry | 2.989 | 2.995 | 126.4 | 135.3 | 257 | 0.050 | 0.105 | 8 |
| Palace | 2.926 | 2.930 | 118.3 | 127.1 | 276 | 0.069 | 0.098 | 8 |

## Every air gap

**SIN's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 6.225 | 6.478 | 6.561 | 6.437 |
| 0.5 mm | 4.452 | 4.657 | 4.720 | 4.618 |
| 1 mm | 2.812 | 2.937 | 2.989 | 2.926 |
| 1.5 mm | 1.798 | 1.874 | 1.913 | 1.875 |
| 2 mm | 1.178 | 1.230 | 1.255 | 1.233 |

**COS's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 6.232 | 6.486 | 6.567 | 6.440 |
| 0.5 mm | 4.462 | 4.666 | 4.728 | 4.624 |
| 1 mm | 2.820 | 2.944 | 2.995 | 2.930 |
| 1.5 mm | 1.804 | 1.879 | 1.918 | 1.878 |
| 2 mm | 1.184 | 1.233 | 1.258 | 1.234 |

**L TX, mean over the turn (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 99.4 | 113.1 | 111.0 | 103.1 |
| 0.5 mm | 109.2 | 122.1 | 121.0 | 113.1 |
| 1 mm | 114.3 | 127.8 | 126.4 | 118.3 |
| 1.5 mm | 117.1 | 131.1 | 129.3 | 121.3 |
| 2 mm | 118.8 | 132.3 | 131.0 | 123.0 |

**R TX, mean over the turn (mΩ)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 290 | 311 | 275 | 294 |
| 0.5 mm | 276 | 298 | 262 | 280 |
| 1 mm | 271 | 294 | 257 | 276 |
| 1.5 mm | 268 | 292 | 255 | 274 |
| 2 mm | 267 | 291 | 253 | 272 |

**Angle error, rms (electrical °)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 0.465 | 0.532 | 0.520 | 0.517 |
| 0.5 mm | 0.088 | 0.088 | 0.077 | 0.092 |
| 1 mm | 0.141 | 0.062 | 0.050 | 0.069 |
| 1.5 mm | 0.185 | 0.080 | 0.066 | 0.108 |
| 2 mm | 0.271 | 0.110 | 0.098 | 0.161 |

## Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX.

| Air gap | Elmer | PyPEEC | Palace |
|---|---|---|---|
| 0.1 mm | 0.949 (0.895) | 0.987 (1.019) | 0.981 (0.929) |
| 0.5 mm | 0.943 (0.902) | 0.987 (1.009) | 0.979 (0.934) |
| 1 mm | 0.941 (0.904) | 0.983 (1.011) | 0.979 (0.936) |
| 1.5 mm | 0.940 (0.906) | 0.980 (1.014) | 0.981 (0.938) |
| 2 mm | 0.939 (0.906) | 0.980 (1.010) | 0.983 (0.939) |

## The generator's estimates

The generator's own figures from `Parameters.txt`, formulas rather than field solves: L TX 132 nH with the rotor away and 109 nH with it (which it calls an upper estimate of the drop), and R TX 230 mΩ at DC.

| Solver | L TX, rotor away (nH) | Over the estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) |
|---|---|---|---|---|
| Elmer | 122.6 | −7.1 % | 99.4 | 114.3 |
| PyPEEC | 136.5 | +3.4 % | 113.1 | 127.8 |
| FastHenry | 135.3 | +2.5 % | 111.0 | 126.4 |
| Palace | 127.1 | −3.7 % | 103.1 | 118.3 |

## Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on the same machine (4 cores, 15 GB), often while another solver shared it, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 158 | 115 to 249 | 13.1 to 13.3 |
| PyPEEC | 219 | 138 to 419 | 1.3 to 2.7 |
| FastHenry | 86 | 78 to 106 | 0.7 |
| Palace | 210 | 121 to 305 | 5.9 to 9.3 |

---

The proof boards, why the solvers differ, the data files and how to run it again are in the [branch's README](../README.md). The boards are the Sinusoidal Coil Generator's, for non-commercial use: see [LICENSE.md](../LICENSE.md).
