# 68. Palace Hardware

What Palace needed on the test machine, and how to estimate a board of your own before you run it. Every number is
from the results files of `S0d2_1x_OD23_2L_tiny_TX3top_Cut`, E01 and E02 on the `Palace_Integration` branch.

## 68.1 The Test Machine

| Item | Value |
|---|---|
| Processor | 4 cores |
| Memory | 15 GB |
| System | Ubuntu 24.04 |
| Palace | 0.19.0, the committed build ([Palace Installation](Palace-Installation.md)) |
| Linear solver | GMRES with hypre's AMS, 4 MPI ranks |

## 68.2 Memory, Measured

The bridge reads Palace's own estimate of its peak memory, all ranks together, from Palace's log (`Estimated peak
per-node memory usage`) and writes it into the results.

| Air gap | Nodes | Element layers | Memory, TX driven alone | Memory, three coils driven in turn | Per node |
|---|---|---|---|---|---|
| 0.1 mm | 177,568 to 179,385 | 12 | 6.0 to 6.2 GB | 8.0 GB | 33 to 35 kB; 45 kB driven in turn |
| 0.5 mm | 202,416 to 204,487 | 14 | 6.8 to 6.9 GB | 9.0 GB | 33 to 34 kB; 44 kB |
| 1 mm | 227,264 to 229,589 | 16 | 7.5 to 8.0 GB | 10.5 GB | 33 to 35 kB; 46 kB |
| 1.5 mm | 264,536 to 267,242 | 19 | 8.7 to 8.9 GB | 11.7 GB | 33 kB; 44 kB |
| 2 mm | 289,384 to 292,344 | 21 | 9.4 to 9.7 GB | 12.9 GB | 32 to 33 kB; 44 kB |

A solve needs about **33 kB per mesh node** with the TX driven alone, and about **44 kB** at the first angle of each
gap, where the three coils are driven in turn (three solves in one), on 2 MPI ranks or 4 alike. A larger gap means
more air between the boards, so more element layers and more nodes.

On the proof boards, all on 4 MPI ranks (E02 drives both ports in turn):

| Run | Nodes | Solve at 10 kHz | Solve at 3.5 MHz |
|---|---|---|---|
| E01, level 0.25 | 18,677 | 219 s, 1.0 GB | 10 s, 0.8 GB |
| E01, level 1 | 68,808 | 918 s, 3.3 GB | 45 s, 2.5 GB |
| E01, level 0.75 with the coil board's air | 151,251 | 2258 s, 8.0 GB | 112 s, 5.8 GB |
| E02, level 0.25 | 30,042 | 677 s, 1.7 GB | 26 s, 1.3 GB |
| E02, level 1 | 119,637 | 3078 s, 6.3 GB | 160 s, 5.1 GB |
| E02, level 0.75 with the coil board's air, GMRES restarted every 100 | 303,129 | 608 s, 12.5 GB (at 100 kHz) | 447 s, 12.5 GB |

The 10 kHz solves are slow because GMRES runs to its 3,000 iteration limit there
([Palace Troubleshooting](Palace-Troubleshooting.md#692-the-linear-solver)). GMRES keeps its restart's worth of
vectors, so a smaller restart (`--restart 100` on E02) is what fitted 303,129 nodes in 15 GB.

## 68.3 Time, Measured

| Air gap | Mesh | Solve, TX driven alone | Solve, three coils driven in turn |
|---|---|---|---|
| 0.1 mm | 18 to 22 s | 115 to 154 s | 370 s |
| 0.5 mm | 23 to 27 s | 172 to 208 s | 573 s |
| 1 mm | 20 to 22 s | 168 to 221 s | 635 s |
| 1.5 mm | 20 to 22 s | 212 to 231 s | 668 s |
| 2 mm | 17 to 20 s | 200 to 253 s | 735 s |

Each solve converged in 115 to 195 iterations. The whole board, 81 solves, took 4.8 hours of solving and 28 minutes of meshing on
the 4-core machine, each solve on 4 MPI ranks.

## 68.4 Estimating A Board Of Your Own

1. Build its mesh alone: `python simulation.py --angles 0 --mesh-only` on a coil board, or `--mesh-only` on a proof
   board's script, and read the node count. `new_coil.py` does this by itself for a new coil board and prints the
   memory a solve needs.
2. Multiply by 33 kB per node (44 kB where several ports are driven in turn).
3. Keep the result under the machine's memory. A 16 GB machine runs one coil-board solve at a time on all its cores,
   or two at once (`--jobs 2 --ranks 2`) where a solve stays under 7 GB.

If the estimate is too big, make the coil smaller (fewer loops, fewer TX turns, a smaller or thinner board each
shrink the mesh) or use a lower `--level`; a coarser mesh moves the answer, by the amounts on
[Palace Accuracy](Palace-Accuracy.md#673-the-mesh).

| Previous | Next |
|:---|---:|
| [Palace Accuracy](Palace-Accuracy.md) | [Palace Troubleshooting](Palace-Troubleshooting.md) |
