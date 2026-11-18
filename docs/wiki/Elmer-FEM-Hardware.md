# 31. Elmer FEM Hardware

What Elmer needed on the test machines, measured, and how to estimate a board of your own before you
run it. The two linear solves cost very different memory: the iterative one about 60 kB per node, the
direct one (MUMPS) far more.

## 31.1 The Test Machines

| Item | E01 and E02 | The coil board |
|---|---|---|
| Processor | 4 cores | 4 OpenMP threads |
| Memory | 15 GB | 16 GB, with a swap file of 8 GB (0.1 mm gap) to about 24 GB (0.5 mm and wider) |
| System | Ubuntu 24.04 | Ubuntu 24.04 |
| Elmer | 26.2 (`a19504a`), the build in `Solver_Elmer/install/` ([Elmer FEM Installation](Elmer-FEM-Installation.md)) | the same |
| Linear solver | Elmer's iterative BiCGStab(l) with its circuit preconditioner, 4 threads | the direct solver MUMPS (serial) |

## 31.2 Memory And Time On E01 And E02

With the iterative solve, Elmer's memory grows with the mesh's nodes. The bridge reads ElmerSolver's peak resident memory from
Linux while it runs and writes it into `results.json`.

| Run | Nodes | Peak memory | Per node |
|---|---|---|---|
| E01, level 0.75 | 59,782 | 3.39 GB | 59 kB |
| E01, level 1 | 85,712 | 4.86 GB | 59 kB |
| E02, level 0.75 | 92,120 | 5.19 GB | 59 kB |
| E02, level 1 | 119,559 | 6.74 GB | 59 kB |
| E01, level 1.3 | 125,043 | 7.09 GB | 59 kB |
| E01, level 0.75 with the air graded twice as finely | 88,760 | 5.11 GB | 60 kB |
| E01, level 0.75 with the air graded four times as finely | 166,471 | 9.73 GB | 61 kB |
| E02, level 0.75 with the air graded twice as finely | 134,840 | 7.66 GB | 60 kB |
| E01, level 0.75 in an air domain twice as big | 86,518 | 4.91 GB | 60 kB |

Nine meshes from 60,000 to 166,000 nodes cost 59 to 61 kB per node, at both frequencies (Linux
counts in kibibytes, so a GB here is 1,073,741,824 bytes). The memory does not depend on the
frequency or on the number of iterations: BiCGStab(l) keeps a fixed number of vectors.

### Time

| Run | Mesh | Solve at 10 kHz | Solve at 3.5 MHz |
|---|---|---|---|
| E01, level 0.75 | 9 s | 25 min, 3000 iterations (the cap) | 3 min, 579 iterations |
| E01, level 1 | 11 s | 17 min, 3000 iterations (the cap); 13 min for 1500 | 6 min, 864 iterations |
| E02, level 0.75 | 9 s | 9 min, 1500 iterations (the cap), the machine to itself | |
| E02, level 1 | 12 s | 22 min, 1500 iterations (the cap) | 10 min, 1147 iterations |
| E01, level 1.3 | 16 s | 45 min, 3000 iterations (the cap) | |
| E01, level 0.75 with the air graded twice as finely | 15 s | 18 min, 3000 iterations (the cap) | |
| E01, level 0.75 with the air graded four times as finely | 44 s | 36 min, 3000 iterations (the cap) | |
| E02, level 0.75 with the air graded twice as finely | 17 s | 15 min, 1500 iterations (the cap) | |
| E01, level 0.75 in an air domain twice as big | 20 s | 18 min, 3000 iterations (the cap) | |

Most runs shared the machine with other runs or with each other's meshing, so their times are what
they took, not what the machine can do: E02 at level 0.75, with the machine to itself, needed 3.9 µs
per node and iteration, the shared E02 at level 1 7.3 µs. Two things are certain from them: meshing takes seconds and
the solve takes minutes, and a 10 kHz solve runs to its iteration cap while a 3.5 MHz one stops on
its own ([Elmer FEM Accuracy](Elmer-FEM-Accuracy.md#302-the-iterative-solve)). The time of one solve
grows with the nodes times the iterations.


## 31.3 The Coil Board

Every solve of S0d2_1x_OD23_2L_tiny_TX3top_Cut is direct, at mesh level 0.25, one mesh and one solve
per rotor angle:

| Air gap | Nodes | Layers through the gap | Time a solve |
|---|---|---|---|
| 0.1 mm | 118,416 to 119,266 | 10 | 3 to 4 min |
| 0.5 mm | 128,812 to 129,731 | 11 | 4 to 6 min |
| 1 mm | 139,208 to 140,196 | 12 | 6 to 7 min |
| 1.5 mm | 149,604 to 150,661 | 13 | 7 to 9 min |
| 2 mm | 160,000 to 161,126 | 14 | 8 to 15 min |

A wider gap means more wedge layers through the air between the boards, and so more nodes. Meshing
takes 10 to 18 s. The 16 solves of a gap took about an hour in all at 0.1 mm and about two and a
half hours at 2 mm; the 1 mm gap, with the rotor away as well, 17 solves in 108 minutes.

**Memory.** Each direct solve needs more than 13 GB: every one held 13.3 GB in memory and put the rest
in swap. At 0.1 mm an 8 GB swap file was enough; from 0.5 mm on it
was not, and the solve was stopped for want of memory, so those gaps ran with about 24 GB of swap,
40 GB of memory and swap together ([Elmer FEM Installation](Elmer-FEM-Installation.md#251-linux-ubuntu-2404)
has the command that adds one). With 118,000 to 161,000 nodes that is more than 100 kB per node, against about 60 kB for the iterative solve on E01 and E02. `new_coil.py` estimates a direct
solve at roughly 200 kB a node, and notes that the memory grows faster than the nodes.

The iterative solve (`--solver iterative`, GCR) needs far less, about 57 kB a node, but on this board
at 3.5 MHz it converges too slowly to read M, so the direct solve is the one that gives answers here.

## 31.4 Estimating A Board

| Quantity | How to get it | E01, level 1 |
|---|---|---|
| Nodes | build the mesh alone (`--mesh-only`); the log prints the nodes | 85,712 |
| Memory | iterative: nodes × 60 kB, plus a few GB for the system; direct: far more, see 31.3 | 4.9 GB |
| Solves | one per frequency, and one per rotor angle on a coil board | 2 |
| Time | iterative: about 4 µs per node and iteration with the machine to itself, from 31.2 | 17 min at 10 kHz (3000 iterations), 5 min at 3.5 MHz (864) |

The nodes come mostly from the copper: the mesh is finest at the copper's edges and through its
thickness (18 µm wedge layers on E01 at level 1, half the skin depth at 3.5 MHz) and coarse in the
air. A finer air grading, as E01's accuracy calls for
([Elmer FEM Accuracy](Elmer-FEM-Accuracy.md#301-the-error-budget-on-e01)), grew E01's mesh by half,
and 2.8 times at four times as fine; on the coil board that growth has not been measured.

| Previous | Next |
|:---|---:|
| [Elmer FEM Accuracy](Elmer-FEM-Accuracy.md) | [Elmer FEM Troubleshooting](Elmer-FEM-Troubleshooting.md) |
