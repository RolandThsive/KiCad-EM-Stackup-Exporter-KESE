# 32. Elmer FEM Troubleshooting

What went wrong while the bridge was built, what it looked like, and what fixed it. The bridge
already does what the right-hand column says; this page is for reading a failed run of your own, or
a case changed by hand.

## 32.1 Coils

| Symptom | Cause | Fix |
|---|---|---|
| A closed coil (a ring with no gap) as a massive coil gives NaN, runs out of memory, diverges, or MUMPS crashes | Elmer's 3D massive coils take their direction only from the gradient of the potential W, which needs two electrodes; a closed massive coil has none (`CircuitsAndDynamics.F90`, `Add_massive`). `Coil Use W Vector` serves stranded coils only | Open every coil at its port: two electrodes with W = 0 and W = 1 ([Elmer FEM Workflow 26.5](Elmer-FEM-Workflow.md#265-open-each-coil-at-its-port)) |
| The coil's voltage is singular, or changes with the solver | The electrodes lie inside the domain, and V on the coil and the gradient part of A are not pinned | Fix the scalar potential on both electrodes (`A re = 0`, `A im = 0`), give the component `Activate Constraint = True`, and put a port sheet with n × A = 0 across the gap |
| `ValueError: the copper of X borders the gap in 1 place, not 2` (or 3, ...) | The gap region does not cut the coil into one open conductor: it misses the copper, or crosses it twice | Draw `gap_box` (or the gap disc) so that it holds the gap and touches each of the two ends once |
| `no copper faces of X border the gap` | The gap region lies away from the coil, or the height range given to `electrodes()` misses the copper's faces | Check the gap's position in model coordinates (y = −y_KiCad) and the z range |
| `no triangle edges along the line: embed it in the mesh (extra_lines)` | A vertical port sheet's line is not in the triangle mesh | Pass the line to `build_mesh(..., extra_lines=[line])`, with its ends on the mesher's 0.5 µm grid |

## 32.2 The Linear Solver

| Symptom | Cause | Fix |
|---|---|---|
| With a direct solver (MUMPS): V ≈ 0 and a huge field energy, or a segfault | Elmer turns on the tree gauge by default with a direct solver; with Dirichlet conditions inside the domain (electrodes, sheets) the tree gauge gives a wrong answer, or crashes with the iterative solver | The bridge uses the iterative solver and no tree gauge |
| The residual falls to about 10⁻⁶ and stalls at 10 kHz, while the same case converges to 10⁻⁷ in under 900 iterations at 3.5 MHz | Without a gauge the curl-curl operator is singular: in the air at every frequency, and nearly so in the copper when the conduction term jωσ is small, as at 10 kHz | Harmless for L and R (they settle well before the residual does); the run stops at `max_iter` and continues (`Linear System Abort Not Converged = False`). Measured on E01: halving the iterations from 3000 to 1500 moves L by 0.17 % (from the voltage) and 0.05 % (from the energy) |
| ILU1 diverges | The A-V system with the circuit rows is not suited to more fill-in | Keep ILU0 inside the `Circuit` preconditioner |
| `Preconditioner "circuit" needs either Umfpack or MUMPS!` | Elmer was built without a direct solver | Rebuild with MUMPS ([Elmer FEM Installation](Elmer-FEM-Installation.md)) |
| `Linear System Robust` has no effect | It exists only in Elmer's real BiCGStabL and IDR(s), not in the complex methods the bridge uses | Use `max_iter` |

## 32.3 The Mesh

| Symptom | Cause | Fix |
|---|---|---|
| Very slow convergence, many sliver tetrahedra | The disc's rim was much finer than the far-field size, and the tetrahedra were not optimised | The rim is sized to `h_max` (`disc(..., h=h_max)`) and gmsh's Netgen optimiser runs after the 3D mesh; together they cut the tetrahedra four-fold |
| L or M a few percent low, while the mesh ladder's last step is small | The ladder divides only the copper's sizes; the air's grading (`grade`, `tet_grade`) stays as it is, and the elements round the copper grow too fast | Run one level again with both halved (`--mesh grade=0.25 --mesh tet_grade=0.35` for the examples) and its own `--results`: on E01 L rose 2.3 %, from 3.7 % to 1.55 % under the reference, and to 0.46 % with both quartered; E02's M rose 2.3 % alike ([Elmer FEM Accuracy](Elmer-FEM-Accuracy.md#301-the-error-budget-on-e01)) |
| A board with vias gets dozens of wedge layers through the board | The dielectric slab held copper (the via barrels), so it was given the copper's thin layers | Only slabs up to `foil_max` (0.15 mm) count as copper foils; S2 went from 96 layers to 17 |
| `the new layout has other slabs: its parts moved in z` | `relabel()` was given a layout whose parts start or end at other heights | Only move parts in the plane (a rotor turned about the axis) between relabelled runs |

## 32.4 Reading Elmer's Log

| Log line | Meaning |
|---|---|
| `CheckKeyword: Unlisted keyword: [w] ...`, `[a re {e}]`, `[activate constraint]` | Harmless: these keywords are read by solvers that do not list them for the keyword checker |
| `ReadTargetNames: Mapped 4 body names and 3 bc names` when there are 3 bodies and 4 boundaries | Elmer's message swaps its two counters; the mapping itself is right |
| `Eddy current power` far from I²R | Do not use it for the coils' loss; R from the circuit's V / I is the bridge's number |
| The run ends with `ERROR` | The bridge stops with the last three ERROR or Fatal lines of the log in the message; the full log is `case/.../<freq>.log` |

## 32.5 KESE And Python

| Symptom | Cause | Fix |
|---|---|---|
| `missing Python package(s): mapbox_earcut` | KESE runs in the bridge's Python and needs its own packages | `pip install -r <Generator>/requirements.txt` into the same environment |
| `KESE not found` | Neither `3D_Geometry/run_KESE.py` nor `KESE_PATH` points at KESE | Copy KESE in ([Elmer FEM Installation](Elmer-FEM-Installation.md)) or set `KESE_PATH` |
| `FINISH ERROR: Finish.FINISH_TYPE = "file" but no finish was found` (with `--for viewer`) | A board with no stack-up has no copper finish for the viewer preset | `--set Stackup.finish=False`. The `elmer` preset leaves the finish out already |
| The machine runs out of memory during the solve | The mesh is too large for the machine | See [Elmer FEM Hardware](Elmer-FEM-Hardware.md) for the measured memory per node, and check a mesh's size with `--mesh-only` first |

| Previous | Next |
|:---|---:|
| [Elmer FEM Hardware](Elmer-FEM-Hardware.md) | [OpenEMS Implementation Introduction](OpenEMS-Implementation-Introduction.md) |
