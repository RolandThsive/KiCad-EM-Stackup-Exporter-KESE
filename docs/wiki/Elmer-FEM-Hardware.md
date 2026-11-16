# 31. Elmer FEM Hardware

What Elmer needed on the test machine, how to estimate a board of your own before you run it, and
why every coil board waits for a bigger machine.

## 31.1 The Test Machine

| Item | Value |
|---|---|
| Processor | 4 cores |
| Memory | 15 GB |
| System | Ubuntu 24.04 |
| Elmer | 26.2 (`a19504a`), built from source with MUMPS ([Elmer FEM Installation](Elmer-FEM-Installation.md)) |
| Linear solver | Elmer's iterative BiCGStab(l) with its circuit preconditioner, 4 threads |

## 31.2 Memory, Measured

Elmer's memory grows with the mesh's nodes. The bridge reads ElmerSolver's peak resident memory from
Linux while it runs and writes it into `results.json`.

| Run | Nodes | Peak memory | Per node |
|---|---|---|---|
| E01, level 0.75 | 59,782 | 3.39 GB | 59 kB |
| E01, level 1 | 85,712 | 4.86 GB | 59 kB |
| E02, level 1 | 119,559 | 6.74 GB | 59 kB |
| E01, level 1.3 | 125,043 | 7.09 GB | 59 kB |

Four meshes from 60,000 to 125,000 nodes cost the same 59 kB per node, at both frequencies (Linux
counts in kibibytes, so a GB here is 1,073,741,824 bytes). The memory does not depend on the
frequency or on the number of iterations: BiCGStab(l) keeps a fixed number of vectors.

## 31.3 Time, Measured

| Run | Mesh | Solve at 10 kHz | Solve at 3.5 MHz |
|---|---|---|---|
| E01, level 0.75 | 9 s | 25 min, 3000 iterations (the cap) | |
| E01, level 1 | 11 s | 17 min, 3000 iterations (the cap); 13 min for 1500 | 6 min, 864 iterations |
| E02, level 1 | 11 s | 22 min, 1500 iterations (the cap) | 10 min, 1147 iterations |
| E01, level 1.3 | 16 s | 45 min, 3000 iterations (the cap) | |

The runs shared the machine with openEMS runs and with each other's meshing, so their times are what
they took, not what the machine can do. Two things are certain from them: meshing takes seconds and
the solve takes minutes, and a 10 kHz solve runs to its iteration cap while a 3.5 MHz one stops on
its own ([Elmer FEM Accuracy](Elmer-FEM-Accuracy.md#302-the-iterative-solve)). The time of one solve
grows with the nodes times the iterations.

## 31.4 Estimating A Board

| Quantity | How to get it | E01, level 1 |
|---|---|---|
| Nodes | build the mesh alone: the S2 script has `--mesh-only`, and E01 too; the log prints the nodes | 85,712 |
| Memory | nodes × 59 kB, plus a few GB for the system | 4.9 GB |
| Solves | one per frequency, and one per rotor angle on the coil boards | 2 |
| Time | minutes per 100,000 nodes and 1000 iterations, from 31.3 | 23 min for both |

The nodes come mostly from the copper: the mesh is finest at the copper's edges and through its
thickness (18 µm wedge layers at level 1, half the skin depth at 3.5 MHz) and coarse in the air.
S2's mesh at level 1, built and counted, has 979,420 nodes for 0.96 m of stator copper, about one
million nodes per metre.

## 31.5 The Coil Boards

| Board | Stator copper | Memory at level 1 | A machine with |
|---|---|---|---|
| S2, the smallest | 0.96 m | about 59 GB (its mesh measured) | 64 GB |
| S1 | 0.92 m | about 55 GB | 64 GB |
| S4 | 1.30 m | about 80 GB | 128 GB |
| D2 | 1.56 m | about 95 GB | 128 GB |
| S3 | 1.91 m | about 115 GB | 128 GB |
| D4, D3, D1 | 2.74 to 3.14 m | about 170 to 190 GB | 256 GB |
| S5, D5 | 3.41 and 3.96 m | about 210 and 240 GB | 256 GB |

S2's memory is its measured mesh at 59 kB per node: 55 GB in the units of 31.2, about 59 GB in the
decimal gigabytes of this table and of machines' specifications. The others scale S2 by their
stator's length of copper, about 61 GB per metre. Every one needs more than the 15 GB test machine, so all ten are held
([Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md#283-the-ten-inductive-encoder-boards)).

Three ways would bring them closer, none of them tried yet:

| Way | What it gives | What it costs |
|---|---|---|
| A coarser mesh (level 0.75) | about two thirds of the nodes (E01: 59,782 against 85,712) | E01's L was 0.5 % lower at level 0.75 than at level 1 |
| One coil set of a dual board at a time | half the copper | the crosstalk between the sets (C7) needs both |
| A direct solver (MUMPS) on a machine with much more memory | no iteration cap | far more memory per node than the iterative solver; not measured here |

| Previous | Next |
|:---|---:|
| [Elmer FEM Accuracy](Elmer-FEM-Accuracy.md) | [Elmer FEM Troubleshooting](Elmer-FEM-Troubleshooting.md) |
