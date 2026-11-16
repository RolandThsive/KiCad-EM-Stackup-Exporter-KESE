# E01 Results

Run on the 4-core, 15 GB test machine (Ubuntu 24.04) with Elmer 26.2 (`a19504a`), gmsh 4.15.2 and
KESE 3.4.0, on 15 and 16 November 2026. Every number below is in `results.json` (the mesh ladder)
and the `results_*.json` beside it (the iteration check, the diagnostic runs, and `results_fields.json`,
the run that also wrote the fields and gave level 0.75 at 3.5 MHz), with the settings, the versions,
the mesh's size, the time, the memory and the solver's last residual of every solve.

## Expected Against What Came Out

| Quantity | Reference | Level 0.75 | Level 1 | Level 1.3 |
|---|---|---|---|---|
| Nodes | | 59,782 | 85,712 | 125,043 |
| L at 10 kHz | 55.99 nH | 53.91 nH (−3.7 %) | 54.20 nH (−3.2 %) | 54.27 nH (−3.1 %) |
| L from the field's energy at 10 kHz | 55.99 nH | 53.91 nH | 54.18 nH | 54.29 nH |
| R at 10 kHz | 61.20 mΩ | 61.53 mΩ (+0.5 %) | 61.53 mΩ (+0.5 %) | 61.52 mΩ (+0.5 %) |
| R_dc, Elmer's DC solve | 61.20 mΩ | 61.34 mΩ (+0.2 %) | 61.36 mΩ (+0.3 %) | 61.36 mΩ (+0.3 %) |
| L at 3.5 MHz | about 55.44 nH (an estimate) | 52.93 nH (−4.5 %) | 53.26 nH (−3.9 %) | |
| R at 3.5 MHz | | 80.19 mΩ (1.31 × R_dc) | 79.25 mΩ (1.29 × R_dc) | |
| Solve at 10 kHz | | 25 min, 3.39 GB, 3000 iterations, residual 5.9e-7 | 17 min, 3000 iterations, residual 1.3e-6 | 45 min, 7.09 GB, 3000 iterations, residual 2.7e-6 |
| Solve at 3.5 MHz | | 3 min, 579 iterations, converged (1e-7) | 6 min, 864 iterations, converged (1e-7) | |

| Quantity | The reference's own accuracy | Elmer against it |
|---|---|---|
| L at 10 kHz | Grover's formula is exact for a thin ring (here R / g = 84). The open loop's share is a lower bound: it stops the current at the round ends' centres, but the current runs on into the half-discs, and taken to the gap's faces the share gives 56.44 nH, 0.8 % more | −3.1 % at the ladder's finest mesh; −0.46 % with the air graded four times as finely |
| L from the energy | the same | within 0.05 % of the circuit's L at every level |
| R at 10 kHz | exact for the annular sector; the two round ends past the sector's ends are left out | +0.5 % |
| L at 3.5 MHz | none exact: the skin depth equals the copper's thickness, so the current is neither uniform nor crowded to the surface | −3.9 % against the thin strip's estimate |

What came out:

* **L is 3 % low and rises with the mesh**: 53.91, 54.20, 54.27 nH. First-order edge elements with
  the current imposed give a lower bound on the field's energy, so a low L that rises as the mesh is
  refined is what they should give. The rise from level 1 to 1.3 (0.12 %) is far smaller than the
  3 % that is left, so refining the copper alone does not close the gap: the air's mesh holds
  most of it (see the diagnostic runs).
* **The circuit and the field's energy agree** within 0.05 % at every level: the electrodes, the
  sheet and Elmer's circuit read back the same inductance the field holds.
* **R is 0.5 % high**, as it should be: the annular sector of the reference stops at the round ends'
  centres, and the current also runs through the two half-discs past them to the electrodes.
* **At 3.5 MHz** L falls by 1.7 % and R rises by 29 % against 10 kHz at level 1: the current leaves
  the copper's middle for its surface as the skin depth falls to the copper's thickness.
* **R at 3.5 MHz falls by 1.2 % from level 0.75 to level 1**, while R at 10 kHz does not move. Both
  levels put two wedge layers through the copper; level 1 has finer triangles at the copper's edges,
  where the current crowds at 3.5 MHz. No level 1.3 solve at 3.5 MHz was run, so whether R at
  3.5 MHz has settled is not known.

## The Iterative Solve

At 10 kHz the linear solve stops at its cap of 3000 iterations at every level, with the residual
stalled between 6e-7 and 3e-6 instead of reaching 1e-7. At 3.5 MHz it converges, in 579 iterations
at level 0.75 and 864 at level 1.

| Level 1 at 10 kHz | Iterations | Residual | L | R |
|---|---|---|---|---|
| `results_iter1500.json` | 1500 | 1.5e-6 | 54.11 nH | 61.52 mΩ |
| `results.json` | 3000 | 1.3e-6 | 54.20 nH | 61.53 mΩ |

| Level 0.75 at 10 kHz | Iterations | Residual | L | R |
|---|---|---|---|---|
| `results_fields.json` | 1500 | 1.1e-6 | 53.89 nH | 61.53 mΩ |
| `results.json` | 3000 | 5.9e-7 | 53.91 nH | 61.53 mΩ |

Doubling the iterations moved L by 0.17 % at level 1 and by 0.03 % at level 0.75, and R by 0.01 %
at most, while the residual fell by half at most. The iteration error of L at 10 kHz is therefore of
the same size as the change from level 1 to 1.3, and the three levels cannot be extrapolated to a
zero mesh size with any confidence; the level 1.3 value is a lower bound, not a limit.

## Diagnostic Runs

The ladder refines only the copper: a level divides `h_edge`, `h_in` and `dz_copper` and leaves the
air's grading (`grade` 0.5, `tet_grade` 0.7) as it is. Its small last step (+0.12 %) therefore says
that the copper's mesh has converged, not that the answer has. The runs below change one thing at
level 0.75, at 10 kHz and 3000 iterations:

| Run | File | Nodes | L | Against the reference | Solve |
|---|---|---|---|---|---|
| The ladder's level 0.75 | `results.json` | 59,782 | 53.91 nH | −3.7 % | 25 min, 3.39 GB, residual 5.9e-7 |
| The air graded twice as finely: `grade` 0.25, `tet_grade` 0.35 | `results_grade.json` | 88,760 | 55.12 nH | −1.55 % | 18 min, 5.11 GB, residual 2.2e-7 |
| Four times as finely: `grade` 0.125, `tet_grade` 0.175 | `results_grade2.json` | 166,471 | 55.73 nH | −0.46 % | 36 min, 9.73 GB, residual 1.5e-6 |

* **The air's mesh holds most of the gap.** Grading the air twice as finely raised L by 2.3 %, with
  about as many nodes as level 1 (85,712), whose L is 3.2 % low. Most of a thin trace's inductance is
  in the field close round it, and the default grading lets the elements there grow too fast.
* **Each halving of the grading halves the change**: +2.3 %, then +1.1 %. The air's mesh is
  converging, but at four times as fine it is not done: if the pattern holds, the next halving adds
  about 0.5 %. The copper's ladder adds its own +0.7 % from level 0.75 to 1.3.
* **The reference can no longer tell the rest apart.** Its open loop's share stops the current at the
  round ends' centres; the current runs on into the half-discs, so the open loop's L lies between
  55.99 nH and 56.44 nH (the current taken to the gap's faces). At −0.46 % Elmer's L is just under
  that band, with the air and the copper both still rising: what is left is of the size of the
  reference's own uncertainty, so this board cannot measure it.
* **R did not move** (61.53 to 61.54 mΩ on all three meshes): the resistance depends on the
  copper's mesh alone.
* **The circuit and the field's energy still agree**, within 0.01 % on both finer meshes.

The ladder's settings stay as they are, so that `results.json` can be run again as published; the
coil boards' estimates in the wiki's *Elmer FEM Hardware* page are for those settings too.

## Problems Met

What stopped a run or gave a wrong number while the bridge was built, and what fixed
it, is on the wiki's *Elmer FEM Troubleshooting* page: the coil that must be opened at its port, the
tree gauge that a direct solver turns on, the stalling residual at 10 kHz, and the mesh's sliver
tetrahedra.
