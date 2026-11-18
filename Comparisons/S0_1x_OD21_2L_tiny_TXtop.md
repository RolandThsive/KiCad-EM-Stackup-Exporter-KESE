[Solvers comparison](../README.md) › S0 TXtop

# S0_1x_OD21_2L_tiny_TXtop: the solvers compared

**S0 TXtop**: S0 with the TX two turns on the top layer (the generator narrows the RX band to fit them).

| Solver | Gaps finished (of 5) | Solves | Passing their own checks |
|---|---|---|---|
| Elmer | 5 | 40 | 40 |
| PyPEEC | 5 | 40 | 40 |
| FastHenry | 5 | 40 | 40 |
| Palace | 5 | 40 | 40 |

Against FastHenry, the yardstick (the closest to the reference on the proof boards):

- **Elmer** (FEM): the coupling (SIN's and COS's amplitude) is 5.3 % under FastHenry's on average over the 5 gaps both have finished (−5.7 to −4.8 %); L TX is 8.8 % under (−9.8 to −8.4 %); the rms angle error is within 0.04° of FastHenry's (electrical degrees).
- **PyPEEC** (PEEC): the coupling (SIN's and COS's amplitude) is 2.0 % under FastHenry's on average over the 5 gaps both have finished (−2.4 to −1.6 %); L TX is 1.3 % over (+1.0 to +1.9 %); the rms angle error is within 0.04° of FastHenry's (electrical degrees).
- **Palace** (FEM): the coupling (SIN's and COS's amplitude) is 2.3 % under FastHenry's on average over the 5 gaps both have finished (−2.5 to −2.0 %); L TX is 6.1 % under (−7.1 to −5.7 %); the rms angle error is within 0.03° of FastHenry's (electrical degrees).

![S0 TXtop against the air gap](../charts/S0_1x_OD21_2L_tiny_TXtop.webp)

*SIN's amplitude, L TX (its mean over the turn, and on the right with the rotor taken away) and the rms angle error against the air gap, one line per solver.*

## At 1 mm

![The curves at 1 mm](../charts/S0_1x_OD21_2L_tiny_TXtop_1mm.webp)

| Solver | SIN amplitude (nH) | COS amplitude (nH) | L TX (nH) | L TX, rotor away (nH) | R TX (mΩ) | Angle error, rms (°) | Angle error, peak (°) | Solves |
|---|---|---|---|---|---|---|---|---|
| Elmer | 2.346 | 2.346 | 111.6 | 121.2 | 265 | 0.423 | 0.579 | 8 |
| PyPEEC | 2.429 | 2.435 | 123.4 | 133.7 | 290 | 0.445 | 0.562 | 8 |
| FastHenry | 2.481 | 2.486 | 122.1 | 132.5 | 254 | 0.413 | 0.517 | 8 |
| Palace | 2.420 | 2.424 | 114.8 | 125.1 | 270 | 0.440 | 0.576 | 8 |

## Every air gap

**SIN's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 5.060 | 5.229 | 5.314 | 5.202 |
| 0.5 mm | 3.708 | 3.848 | 3.915 | 3.818 |
| 1 mm | 2.346 | 2.429 | 2.481 | 2.420 |
| 1.5 mm | 1.486 | 1.533 | 1.570 | 1.534 |
| 2 mm | 0.965 | 0.993 | 1.016 | 0.995 |

**COS's amplitude (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 5.060 | 5.236 | 5.319 | 5.204 |
| 0.5 mm | 3.709 | 3.856 | 3.921 | 3.823 |
| 1 mm | 2.346 | 2.435 | 2.486 | 2.424 |
| 1.5 mm | 1.485 | 1.537 | 1.574 | 1.537 |
| 2 mm | 0.963 | 0.996 | 1.019 | 0.998 |

**L TX, mean over the turn (nH)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 92.1 | 104.2 | 102.2 | 95.0 |
| 0.5 mm | 105.0 | 116.2 | 115.1 | 108.0 |
| 1 mm | 111.6 | 123.4 | 122.1 | 114.8 |
| 1.5 mm | 115.0 | 127.5 | 125.6 | 118.5 |
| 2 mm | 117.1 | 129.1 | 127.8 | 120.5 |

**R TX, mean over the turn (mΩ)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 291 | 312 | 276 | 295 |
| 0.5 mm | 271 | 295 | 259 | 276 |
| 1 mm | 265 | 290 | 254 | 270 |
| 1.5 mm | 262 | 287 | 251 | 268 |
| 2 mm | 261 | 286 | 249 | 266 |

**Angle error, rms (electrical °)**

| Air gap | Elmer | PyPEEC | FastHenry | Palace |
|---|---|---|---|---|
| 0.1 mm | 1.519 | 1.538 | 1.494 | 1.507 |
| 0.5 mm | 0.673 | 0.701 | 0.660 | 0.685 |
| 1 mm | 0.423 | 0.445 | 0.413 | 0.440 |
| 1.5 mm | 0.388 | 0.399 | 0.372 | 0.393 |
| 2 mm | 0.409 | 0.395 | 0.372 | 0.381 |

## Against FastHenry, gap by gap

Each solver's value over FastHenry's at the same gap: SIN's amplitude, and in brackets L TX.

| Air gap | Elmer | PyPEEC | Palace |
|---|---|---|---|
| 0.1 mm | 0.952 (0.902) | 0.984 (1.019) | 0.979 (0.929) |
| 0.5 mm | 0.947 (0.912) | 0.983 (1.010) | 0.975 (0.938) |
| 1 mm | 0.946 (0.914) | 0.979 (1.011) | 0.975 (0.941) |
| 1.5 mm | 0.947 (0.916) | 0.976 (1.015) | 0.977 (0.943) |
| 2 mm | 0.950 (0.916) | 0.977 (1.010) | 0.980 (0.943) |

## The generator's estimates

The generator's own figures from `Parameters.txt`, formulas rather than field solves: L TX 130 nH with the rotor away and 106 nH with it (which it calls an upper estimate of the drop), and R TX 230 mΩ at DC.

| Solver | L TX, rotor away (nH) | Over the estimate | L TX at 0.1 mm (nH) | L TX at 1 mm (nH) |
|---|---|---|---|---|
| Elmer | 121.2 | −6.8 % | 92.1 | 111.6 |
| PyPEEC | 133.7 | +2.9 % | 104.2 | 123.4 |
| FastHenry | 132.5 | +1.9 % | 102.2 | 122.1 |
| Palace | 125.1 | −3.8 % | 95.0 | 114.8 |

## Time and memory

Each branch records the wall time and the peak memory of every solve. They all ran on the same machine (4 cores, 15 GB), often while another solver shared it, and each with its own process layout (FastHenry runs several single-threaded solves at once; Palace runs two or four MPI processes per solve). Read these as rough.

| Solver | Seconds per solve (median over the gaps) | Range | Peak memory of a solve, as the branch measured it (GB) |
|---|---|---|---|
| Elmer | 178 | 134 to 249 | 13.3 |
| PyPEEC | 281 | 146 to 382 | 1.3 to 2.6 |
| FastHenry | 183 | 86 to 204 | 0.7 |
| Palace | 147 | 117 to 208 | 6.1 to 9.7 |

---

The proof boards, why the solvers differ, the data files and how to run it again are in the [branch's README](../README.md). The boards are the Sinusoidal Coil Generator's, for non-commercial use: see [LICENSE.md](../LICENSE.md).
