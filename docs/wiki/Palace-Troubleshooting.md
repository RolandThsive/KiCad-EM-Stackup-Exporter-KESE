# 69. Palace Troubleshooting

What went wrong while the bridge was built, what it looked like, and what fixed it. The bridge already does what the
right-hand column says; this page is for reading a failed run of your own, or a case changed by hand.

## 69.1 Ports

| Symptom | Cause | Fix |
|---|---|---|
| Palace refuses a lumped port | Palace takes a lumped port only as a rectangle whose two ends lie on conductors, and checks the sheet's bounding box against its direction to a part in a million | Make the port's line straight, its ends on the mesher's 0.5 µm grid (`snap` in the coil board's `simulation.py`), and draw it into the mesh with `build_mesh(extra_lines=[line])`; nothing else may cross it |
| `ValueError: the copper of X borders the gap in 1 places, not 2` (or 3, ...) | The gap region does not cut the coil into one open conductor: it misses the copper, or crosses it twice | Draw `gap_box` (or the cut box) so that it holds the gap and touches each of the two ends once |
| `no copper faces of X border the gap` | The gap region lies away from the coil, or the height range given to `electrodes()` misses the copper's faces | Check the gap's position in model coordinates (y = −y_KiCad) and the z range |
| `no two copper vertices face each other across the gap` | `ports.facing_vertices` found no pair of outline vertices on opposite sides of the gap sharing their coordinate across `axis` | Check `gap_box` and `axis` (0 for a gap across x, 1 across y) |
| `X: no mesh faces on the port line` | The port's line is not in the triangle mesh | Pass it in `extra_lines`, with its ends on the grid |
| M about 13 % low at a left-out via (found on another coil board) | KESE exports a via with its drill hole through the pads, and a port sheet standing over the hole does not end on copper where it crosses it | Fill the left-out via's pads over the hole (`voids()` in the coil board's `simulation.py`): a via that is left out is not drilled |
| A receiver should be opened by a cut, as the real board is, without editing the board files | `new_coil.py` opens each receiver at a left-out via | Set `"rx_port": "cut"` and each receiver's `cut` in `test_spec.json`; `simulation.py` takes the copper in the cut box out as a `void` part and draws the box's outline into the mesh, so both cut faces are meshed exactly |

## 69.2 The Linear Solver

| Symptom | Cause | Fix |
|---|---|---|
| GMRES diverges at 10 kHz | At low frequency the field's gradients in the air cost almost nothing, and the operator AMS works on is all but singular there | Tell AMS so: `AMSSingularOperator: true` in the solver settings (E01 and E02 do). GMRES then converges, slowly, and on E01 and E02 it stops at its 3,000 iteration limit (next row) |
| Slow or stalled iterations on an otherwise good mesh | Slivers (tetrahedra with four nearly coplanar corners) in the air | `tet_fill` runs gmsh's optimiser and then Netgen's, which swap and smooth them away without touching the surface |
| GMRES runs to its 3,000 iteration limit at 10 kHz | The same near-singular operator: it converges slowly, to residuals of 3e-8 to 6e-5 on E01 and E02 | Harmless here: converged 100 kHz checks give the same L to 0.01 % and M to 0.002 % |
| A large mesh does not fit in memory with GMRES's 300 vectors (E02 with the coil board's air, 303,129 nodes) | GMRES keeps one vector per iteration until it restarts | Restart every 100 iterations (`--restart 100` on E02): 12.5 GB |
| At 10 kHz a graded, restarted solve does not converge (E02's RX stalled at a residual of 0.65, with plainly wrong numbers) | The short restart and the near-singular operator together | Solve the low frequency at 100 kHz, where AMS needs no singular-operator flag; on E02's default mesh M at 100 kHz and 10 kHz agree to 0.002 % |
| No direct solver to fall back on | The committed build has none: SuperLU_DIST and STRUMPACK need ParMETIS, and MUMPS's source could not be downloaded on the test machine | Check every solve ([Palace Accuracy](Palace-Accuracy.md#671-the-checks-on-every-solve)); `WITH_MUMPS=1` in `build_palace.sh` builds MUMPS without ParMETIS, untried |
| A solve reported as not readable | It did not converge, gave the TX a negative resistance, or its L from the port and from the field's energy (or M both ways) differ by more than 1 % | Its chart marks it with a ring and `SINCOS_Results.md` lists it under **Not readable**; its iterations and residual are in the gap's results table |

## 69.3 Running Palace

| Symptom | Cause | Fix |
|---|---|---|
| `Palace not found: see Solver_Palace/README.md, or set PALACE to its launcher` | The bridge looks for `$PALACE`, then `Solver_Palace/install/bin/palace`, then `palace` on the `PATH` | Use the committed build, or set `PALACE` |
| The committed program does not start | It needs 64-bit Linux with glibc 2.38 or newer and Open MPI 4.1, OpenBLAS, gfortran's runtime and zlib from the system | `bash bridge/setup_machine.sh` installs them, and builds Palace from source where the committed one still does not run |
| `mpirun` refuses to run as root, or to place more ranks than cores | Open MPI's defaults | The bridge sets `OMPI_ALLOW_RUN_AS_ROOT`, `OMPI_ALLOW_RUN_AS_ROOT_CONFIRM` and `OMPI_MCA_rmaps_base_oversubscribe` for each run |
| Palace cannot open the mesh with a relative `--out` folder | Palace runs inside the case folder, so a relative mesh path points elsewhere | The proof boards' scripts now make the folder absolute |
| `Palace failed in <folder> (exit N)` | Palace stopped; the bridge prints the end of its log | Read `palace.log` in that folder: it is written as Palace runs |
| The machine runs out of memory | The mesh is too large | See [Palace Hardware](Palace-Hardware.md) for the memory per node, and check a mesh's size with `--mesh-only` first |

## 69.4 Building Palace

| Symptom | Cause | Fix |
|---|---|---|
| The superbuild fails downloading patches for MFEM and hypre | It fetches them from github.com's commit and compare links, which some networks refuse (the test machine's did) | `LOCAL_PATCHES=1 bash Solver_Palace/build_palace.sh` makes the same diffs with git from MFEM's and hypre's own repositories |
| MFEM's first example fails to link in a build with no direct solver | In Palace's own build, BLAS and LAPACK reach MFEM's link line only through a direct solver | `no_parmetis.patch` gives MFEM hypre's BLAS and LAPACK (OpenBLAS) |
| A build with ParMETIS in it | Palace's release build links ParMETIS, whose licence is not open source | `no_parmetis.patch`; `build_palace.sh` refuses to install a program in which any ParMETIS symbol is found |

## 69.5 KESE And The Mesh

| Symptom | Cause | Fix |
|---|---|---|
| `KESE not found: copy main's Generator into 3D_Geometry (see its README) or set KESE_PATH to run_KESE.py` | A board with no committed export, and no KESE | Copy KESE's `Generator/` from `main` into `3D_Geometry/`, or set `KESE_PATH` |
| `KESE wrote no materials.json for <board>` | KESE ran but exported nothing for the solver preset | Read KESE's output printed with the error |
| The mesh is not 2.5D | A part tilted out of the board's plane | The mesh needs a layered stack, flat at a few heights, as every KiCad board is; a board over another works, a tilted part does not |

| Previous | Next |
|:---|---:|
| [Palace Hardware](Palace-Hardware.md) | [Solvers Comparison](Solvers-Comparison.md) |
