[Solvers comparison](../README.md) › OD22 Cut

# S0_1x_OD22_2L_tiny_TXtop_Cut: the solvers compared

**OD22 Cut**: the 22 mm board with SIN and COS opened by a 0.2 mm cut in a top trace instead of a left-out via.

| Solver | Gaps finished (of 5) | Solves | Passing their own checks |
|---|---|---|---|
| Elmer | 5 | 40 | 40 |
| PyPEEC | 5 | 40 | 40 |
| FastHenry | 5 | 40 | 40 |
| Palace | 5 | 40 | 40 |

Against FastHenry, the yardstick (the closest to the reference on the proof boards):

- **Elmer** (FEM): the coupling (SIN's and COS's amplitude) is 4.0 % under FastHenry's on average over the 5 gaps both have finished (−4.3 to −3.3 %); L TX is 8.7 % under (−9.8 to −8.3 %); the rms angle error is within 0.09° of FastHenry's (electrical degrees).
- **PyPEEC** (PEEC): the coupling (SIN's and COS's amplitude) is 1.9 % under FastHenry's on average over the 5 gaps both have finished (−2.3 to −1.4 %); L TX is 1.3 % over (+0.9 to +1.9 %); the rms angle error is within 0.02° of FastHenry's (electrical degrees).
- **Palace** (FEM): the coupling (SIN's and COS's amplitude) is 0.8 % under FastHenry's on average over the 5 gaps both have finished (−1.1 to −0.5 %); L TX is 6.0 % under (−7.0 to −5.6 %); the rms angle error is within 0.06° of FastHenry's (electrical degrees).

![OD22 Cut against the air gap](../charts/S0_1x_OD22_2L_tiny_TXtop_Cut.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

## At 1 mm

![The curves at 1 mm](../charts/S0_1x_OD22_2L_tiny_TXtop_Cut_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| Elmer | 3.257 | 3.267 | 122.7 | 134.6 | 286 | 0.207 | 0.304 | 8 |
| PyPEEC | 3.340 | 3.342 | 135.6 | 148.2 | 313 | 0.179 | 0.333 | 8 |
| FastHenry | 3.403 | 3.410 | 134.1 | 146.9 | 274 | 0.155 | 0.237 | 8 |
| Palace | 3.368 | 3.374 | 126.2 | 138.9 | 292 | 0.195 | 0.276 | 8 |

## Every air gap

**SIN's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 6.466 | 6.600 | 6.695 | 6.661 |
| 0.5 mm | 4.912 | 5.040 | 5.117 | 5.069 |
| 1 mm | 3.257 | 3.340 | 3.403 | 3.368 |
| 1.5 mm | 2.149 | 2.198 | 2.246 | 2.226 |
| 2 mm | 1.441 | 1.473 | 1.504 | 1.495 |

**COS's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 6.476 | 6.600 | 6.700 | 6.665 |
| 0.5 mm | 4.923 | 5.042 | 5.124 | 5.075 |
| 1 mm | 3.267 | 3.342 | 3.410 | 3.374 |
| 1.5 mm | 2.156 | 2.200 | 2.252 | 2.231 |
| 2 mm | 1.447 | 1.475 | 1.509 | 1.499 |

**L TX, mean over the turn (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 100.9 | 113.9 | 111.8 | 104.0 |
| 0.5 mm | 115.2 | 127.4 | 126.2 | 118.5 |
| 1 mm | 122.7 | 135.6 | 134.1 | 126.2 |
| 1.5 mm | 126.7 | 140.2 | 138.3 | 130.5 |
| 2 mm | 129.1 | 142.2 | 140.8 | 132.9 |

**R TX, mean over the turn (mΩ)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 313 | 337 | 298 | 318 |
| 0.5 mm | 293 | 318 | 280 | 298 |
| 1 mm | 286 | 313 | 274 | 292 |
| 1.5 mm | 283 | 310 | 271 | 289 |
| 2 mm | 281 | 308 | 270 | 287 |

**Angle error, rms (electrical °)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 1.093 | 1.033 | 1.016 | 1.079 |
| 0.5 mm | 0.376 | 0.341 | 0.319 | 0.374 |
| 1 mm | 0.207 | 0.179 | 0.155 | 0.195 |
| 1.5 mm | 0.213 | 0.168 | 0.148 | 0.179 |
| 2 mm | 0.253 | 0.180 | 0.164 | 0.186 |

## Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX.

| Air gap | Elmer | PyPEEC | Palace |
|---|---|---|---|
| 0.1 mm | 0.966 (0.902) | 0.986 (1.019) | 0.995 (0.930) |
| 0.5 mm | 0.960 (0.913) | 0.985 (1.009) | 0.991 (0.939) |
| 1 mm | 0.957 (0.915) | 0.981 (1.011) | 0.990 (0.941) |
| 1.5 mm | 0.957 (0.916) | 0.979 (1.014) | 0.991 (0.944) |
| 2 mm | 0.958 (0.917) | 0.979 (1.010) | 0.993 (0.944) |

## The generator's estimates

The generator's own figures from `Parameters.txt`, formulas rather than field solves: L TX 144 nH with the rotor away and 116 nH with it (which it calls an upper estimate of the drop), and R TX 250 mΩ at DC.

| Solver | L TX, rotor away (nH) | Over the estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) |
|---|---|---|---|---|
| Elmer | 134.6 | −6.5 % | 100.9 | 122.7 |
| PyPEEC | 148.2 | +2.9 % | 113.9 | 135.6 |
| FastHenry | 146.9 | +2.0 % | 111.8 | 134.1 |
| Palace | 138.9 | −3.6 % | 104.0 | 126.2 |

## Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on the same machine (4 cores, 15 GB), often while another solver shared it, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 174 | 121 to 360 | 13.3 |
| PyPEEC | 246 | 155 to 471 | 1.5 to 3.0 |
| FastHenry | 194 | 178 to 279 | 0.7 |
| Palace | 163 | 122 to 213 | 6.2 to 9.9 |

A receiver whose plus terminal sits on the other side in one branch comes out turned over; here Elmer COS, Palace COS, Palace SIN, PyPEEC COS is turned back to match FastHenry. Amplitudes and angle errors are the same either way.

---

The proof boards, why the solvers differ, the data files and how to run it again are in the [branch's README](../README.md). The boards are the Sinusoidal Coil Generator's, for non-commercial use: see [LICENSE.md](../LICENSE.md).
