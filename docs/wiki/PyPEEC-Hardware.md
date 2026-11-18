# 50. PyPEEC Hardware

What PyPEEC needed on the test machines, and how to estimate a board of your own before you run it.
The bridge runs each PyPEEC solve in a process of its own, reads its peak resident memory from Linux
while it runs, and writes it with the time into the results files.

## 50.1 The Test Machine

| Item | Value |
|---|---|
| Processor | 4 cores |
| Memory | 15 GB |
| System | Ubuntu 24.04, Python 3.13 |
| PyPEEC | 5.8.0 from the committed wheels ([PyPEEC Installation](PyPEEC-Installation.md)) |
| Numerics | SciPy's FFT and SuperLU, GMRES with PyPEEC's own preconditioner, 4 threads; no FFTW, PARDISO, MKL or CUDA |

The coil board's solves of each gap were shared over several machines of this size and merged into one
results file (`simulation.py --merge`).

## 50.2 Memory And Time, The Proof Boards

| Run | Grid | Solve at 10 kHz | Solve at 3.5 MHz |
|---|---|---|---|
| E01, 100 µm | 208 × 208 × 1 | 1 s | 1 s, 0.11 GB |
| E01, 50 µm | 412 × 412 × 1 | 3 s, 0.17 GB | 8 s, 0.17 GB |
| E01, 25 µm | 822 × 822 × 1 | 9 s, 0.37 GB | 24 s, 0.41 GB |
| E01, 12.5 µm | 1642 × 1642 × 1 | 24 s, 1.29 GB | 58 s, 1.39 GB |
| E01, 25 µm, two layers through the copper | 822 × 822 × 2 | | 37 s, 0.81 GB |
| E02, 100 µm | 208 × 208 × 46 | 12 s, 0.64 GB | 29 s, 0.64 GB |
| E02, 50 µm | 412 × 412 × 46 | 62 s, 2.16 GB | 145 s, 2.17 GB |

Every proof-board solve took one GMRES iteration. E02's grid is 46 voxel layers tall, for the 1.565 mm
between its two loops, though only the first and the last hold copper: the layers between add no
unknowns, but they are grid to the FFTs, and its 50 µm solve needs 13 times E01's memory. A 25 µm
solve of E02 would take a grid of 30 million voxels and about 9 GB.

## 50.3 Memory And Time, The Coil Board

S0d2_1x_OD23_2L_tiny_TX3top_Cut, with 50 µm voxels, one solve per rotor angle:

| Air gap | Grid (up to) | dz | Memory a solve | Time a solve |
|---|---|---|---|---|
| 0.1 mm | 405 × 364 × 33 = 4.9 million | 26.9 µm | 1.6 to 1.7 GB | 2 to 4 min |
| 0.5 mm | 405 × 364 × 34 = 5.0 million | 38.2 µm | 1.6 to 1.7 GB | 2 to 4 min |
| 1 mm | 405 × 364 × 52 = 7.7 million | 34.5 µm | 2.2 to 2.4 GB | 4 to 7 min |
| 1.5 mm | 405 × 364 × 79 = 11.6 million | 29.0 µm | 3.2 to 3.4 GB | 8 to 16 min |
| 2 mm | 405 × 364 × 81 = 11.9 million | 34.5 µm | 3.3 to 3.5 GB | 5 to 11 min |
| rotor away | 394 × 343 × 22 = 3.0 million | 34.6 µm | 1.0 GB | 1 min |

The grid's footprint changes a little with the rotor's angle (from 394 × 343 to 405 × 364), since it
covers whatever copper is there. Its height is set by the copper: it runs from the stator's B.Cu to the
rotor's copper in steps of about 35 µm, chosen so that every sheet lands on a voxel layer, so it grows
with the air gap, and the memory and time with it. The 1.5 mm gap needed 79 layers of 29.0 µm where the
2 mm gap needed 81 of 34.5 µm: the step that fits every sheet within a micron is not always near
35 µm. The 81 solves add up to about 8 hours of solving (0.8 hours at 0.1 mm, 3.0 hours at 1.5 mm),
shared over the machines; a machine with 8 GB runs every gap.

## 50.4 What The Cost Follows

| Quantity | What it follows | On these boards |
|---|---|---|
| Memory | the whole grid, copper or not: the FFTs run over every voxel | 0.29 to 0.35 GB a million voxels over all 81 coil-board solves |
| Time | the grid, times GMRES's iterations (1 on the proof boards, 2 to 4 on the coil board) | 0.36 to 1.41 minutes a million voxels on 4 cores over the 81 coil-board solves, on machines that were not always to themselves |
| The grid's footprint | the copper's extent in the plane, over d² | halving d makes four times the voxels: E01 from 0.17 to 0.41 GB at 3.5 MHz, from 50 to 25 µm |
| The grid's height | the distance from the lowest copper to the highest, over dz | the air gap and the board's thickness |

There is no air mesh and no outer boundary, so nothing round the board adds to the cost: the voxel
size `d` and the copper's extent set it.

## 50.5 Estimating A Board

| Quantity | How to get it | The coil board at 1 mm |
|---|---|---|
| Grid | `simulation.py --voxels-only` (with `--angles 0` on the coil board) draws the voxels and prints the grid; `new_coil.py` does it for a new coil board | 405 × 364 × 52 = 7.7 million |
| Memory | about 0.31 GB a million voxels, `new_coil.py`'s rule, plus a few GB for the system | 2.4 GB |
| Time | about 0.9 minute a million voxels on 4 cores, `new_coil.py`'s rule | 7 minutes (measured: 4 to 7) |
| Solves | one per frequency, and on a coil board one per rotor angle and gap, plus the rotor away | 16 angles × 5 gaps + 1 = 81 |

If the estimate is too big, a larger voxel size (`--voxel`) or a smaller board shrinks it; what a
larger voxel costs in accuracy is on [PyPEEC Accuracy](PyPEEC-Accuracy.md).

| Previous | Next |
|:---|---:|
| [PyPEEC Accuracy](PyPEEC-Accuracy.md) | [PyPEEC Troubleshooting](PyPEEC-Troubleshooting.md) |
