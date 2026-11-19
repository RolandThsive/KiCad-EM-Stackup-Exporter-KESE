# 28. Elmer FEM Troubleshooting

What went wrong while the bridge was built, what it looked like, and what fixed it. The bridge
already does what the right-hand column says; this page is for reading a failed run of your own, or
a case changed by hand.

## 28.1 Coils

| Symptom | Cause | Fix |
|---|---|---|
| A closed coil (a ring with no gap) as a massive coil gives NaN, runs out of memory, diverges, or MUMPS crashes | Elmer's 3D massive coils take their direction only from the gradient of the potential W, which needs two electrodes; a closed massive coil has none (`CircuitsAndDynamics.F90`, `Add_massive`). `Coil Use W Vector` serves stranded coils only | Open every coil at its port: two electrodes with W = 0 and W = 1 ([Elmer FEM Walkthrough 26.5](Elmer-FEM-Walkthrough.md#2412-open-each-coil-at-its-port)) |
| The coil's voltage is singular, or changes with the solver | The electrodes lie inside the domain, and V on the coil and the gradient part of A are not pinned | Fix the scalar potential on both electrodes (`A re = 0`, `A im = 0`) and put a port sheet with n × A = 0 across the gap |
| `ValueError: the copper of X borders the gap in 1 place, not 2` (or 3, ...) | The gap region does not cut the coil into one open conductor: it misses the copper, or crosses it twice | Draw `gap_box` (or the gap disc) so that it holds the gap and touches each of the two ends once |
| `no copper faces of X border the gap` | The gap region lies away from the coil, or the height range given to `electrodes()` misses the copper's faces | Check the gap's position in model coordinates (y = −y_KiCad) and the z range |
| `no triangle edges along the line: embed it in the mesh (extra_lines)` | A vertical port sheet's line is not in the triangle mesh | Pass the line to `build_mesh(..., extra_lines=[line])`, with its ends on the mesher's 0.5 µm grid |
| With `rx_port` `"cut"`: *rx_port 'cut' needs a 'cut' for SIN and COS in test_spec.json* | A receiver in `test_spec.json` has no `cut` | Give each receiver's terminal a `cut` with `xy_kicad`, `along_kicad`, `gap_mm` and `half_width_mm` ([Elmer FEM Simulating Your Own Board](Elmer-FEM-Simulating-Your-Own-Board.md#258-a-coil-set-from-the-generator)) |
| A coil's iterative solve stays at its first iterate (the coil board at 3.5 MHz) | `Activate Constraint = True` adds each coil's own scalar potential, whose rows swamp the residual after Elmer's diagonal scaling; a conductor that is not a coil (a rotor) gets such rows from Elmer as well | Leave `constraint=False` (the default) and `conductor_potential=False` (the rotor's potential fixed to 0); a direct solve gives the same L and M either way |

## 28.2 The Linear Solver

| Symptom | Cause | Fix |
|---|---|---|
| With a direct solver: V ≈ 0 and a huge field energy, a circuit voltage of 0, or a segfault | Elmer turns on the tree gauge by default with a direct solver; its tree runs through the conductors, which is wrong where a conductor has no potential of its own, and with the port sheets it gave a circuit voltage of 0 | `solver='mumps'` writes `Use Tree Gauge = False` and `Mumps Solve Singular = True`: A stays ungauged and MUMPS handles the null pivots |
| Serial MUMPS (`mumpslocal`) segfaults at once | The usual 8 MB stack is too small for it | The bridge lifts the stack limit before it starts ElmerSolver; by hand, run `ulimit -s unlimited` first |
| A direct solve is stopped for want of memory | The coil board's direct solves need more than 13 GB, and up to about 40 GB with swap from a 0.5 mm gap on | Add a swap file ([Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md#245-linux-ubuntu-2404)), or a machine with more memory ([Elmer FEM Simulating Your Own Board](Elmer-FEM-Simulating-Your-Own-Board.md#257-before-a-large-board)) |
| On the coil board at 3.5 MHz the iterative solve falls too slowly to read M | The iterative solve with the circuit preconditioner converges slowly on these boards; BiCGStab(l) wanders, GCR(50) falls slowly but steadily | Use the direct solve (`--solver mumps`, the coil board's default) |
| The W potential's solve stalls near 1e-4 | CG with ILU0 stalls on some coarse meshes (it did on the three-turn coil board at level 0.25) | The bridge solves W directly with UMFPACK |
| An ILU of the field's block breaks down on tiny pivots | The air's curl-curl block is singular | A shifted ILU: `ilu_factor=0.1` factors the matrix with its diagonal times 1.1 |
| The residual falls to about 10⁻⁶ and stalls at 10 kHz on E01, while the same case converges to 10⁻⁷ in under 900 iterations at 3.5 MHz | Without a gauge the curl-curl operator is singular: in the air at every frequency, and nearly so in the copper when the conduction term jωσ is small, as at 10 kHz | Harmless for L and R (they settle well before the residual does); the run stops at `max_iter` and continues (`Linear System Abort Not Converged = False`). Measured on E01: halving the iterations from 3000 to 1500 moves L by 0.17 % (from the voltage) and 0.05 % (from the energy) |
| `Preconditioner "circuit" needs either Umfpack or MUMPS!` | Elmer was built without a direct solver | Rebuild with MUMPS ([Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md#245-linux-ubuntu-2404)) |
| `Linear System Robust` has no effect | It exists only in Elmer's real BiCGStabL and IDR(s), not in the complex methods the bridge uses | Use `max_iter` |

## 28.3 The Mesh

| Symptom | Cause | Fix |
|---|---|---|
| Very slow convergence, many sliver tetrahedra | The disc's rim was much finer than the far-field size, and the tetrahedra were not optimised | The rim is sized to `h_max` (`disc(..., h=h_max)`) and gmsh's Netgen optimiser runs after the 3D mesh; together they cut the tetrahedra four-fold |
| L or M a few percent low, while the mesh ladder's last step is small | The ladder divides only the copper's sizes; the air's grading (`grade`, `tet_grade`) stays as it is, and the elements round the copper grow too fast | Run one level again with both halved (`--mesh grade=0.25 --mesh tet_grade=0.35` for the examples) and its own `--results`: on E01 L rose 2.3 %, from 3.7 % to 1.55 % under the reference, and to 0.46 % with both quartered; E02's M rose 2.3 % alike ([Elmer FEM Accuracy](Elmer-FEM-Accuracy.md#271-the-error-budget-on-e01)) |
| A board with vias gets dozens of wedge layers through the board | The dielectric slab held copper (the via barrels), so it was given the copper's thin layers | Only slabs up to `foil_max` (0.15 mm) count as copper foils |
| `the new layout has other slabs: its parts moved in z` | `relabel()` was given a layout whose parts start or end at other heights | Only move parts in the plane (a rotor turned about the axis) between relabelled runs |

## 28.4 Reading Elmer's Log

| Log line | Meaning |
|---|---|
| `CheckKeyword: Unlisted keyword: [w] ...`, `[a re {e}]`, `[activate constraint]` | Harmless: these keywords are read by solvers that do not list them for the keyword checker |
| `ReadTargetNames: Mapped 4 body names and 3 bc names` when there are 3 bodies and 4 boundaries | Elmer's message swaps its two counters; the mapping itself is right |
| `Eddy current power` far from I²R | With `Activate Constraint` on, `MagnetoDynamicsCalcFields` leaves the coil's grad v out of E, so the eddy power is wrong; with it off (the default) it gives R a second way, and on the coil board it agreed with R from V / I within 0.004 % |
| The run ends with `ERROR` | The bridge stops with the last three ERROR or Fatal lines of the log in the message; the full log is `case/.../<freq>.log` |

## 28.5 KESE And Python

| Symptom | Cause | Fix |
|---|---|---|
| `missing Python package(s): mapbox_earcut` | KESE runs in the bridge's Python and needs its own packages | `pip install -r <Generator>/requirements.txt` into the same environment |
| `KESE not found` | Neither `3D_Geometry/run_KESE.py` nor `KESE_PATH` points at KESE | Copy KESE in ([Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md#245-linux-ubuntu-2404)) or set `KESE_PATH` |
| `FINISH ERROR: Finish.FINISH_TYPE = "file" but no finish was found` (with `--for viewer`) | A board with no stack-up has no copper finish for the viewer preset | `--set Stackup.finish=False`. The `elmer` preset leaves the finish out already |
| The machine runs out of memory during the solve | The mesh is too large for the machine | See [Elmer FEM Simulating Your Own Board](Elmer-FEM-Simulating-Your-Own-Board.md#257-before-a-large-board) for the measured memory per node, and check a mesh's size with `--mesh-only` first |
| *elements.def not found* when ElmerSolver is run by hand | Elmer does not know its home folder | `export ELMER_HOME=<branch>/Solver_Elmer/install`; the bridge sets it itself |
| `ldd ... libelmersolver.so` prints *not found* | The committed build's libraries are missing | `sudo apt-get install -y libgfortran5 libgomp1 libopenblas0 libopenmpi3t64 libmumps-5.6t64`, or `bash bridge/setup_machine.sh` |

| Previous | Next |
|:---|---:|
| [Elmer FEM Accuracy](Elmer-FEM-Accuracy.md) | [PyPEEC Walkthrough](PyPEEC-Walkthrough.md) |
