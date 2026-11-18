# E01 Results

Solved on 18 Nov 2026 with Palace 0.19.0, on 4 MPI ranks (4 cores, 15 GB). The mesh ladder is in `results.json`; the run with the coil boards' air grading is in `results_grade.json`.

## Expected Against What Came Out

| Mesh level | 0.25 | 0.5 | 0.75 | 1 | 0.75, the coil boards' air |
|---|---|---|---|---|---|
| Nodes | 18,677 | 29,946 | 53,299 | 68,808 | 151,251 |
| L at 10 kHz (reference 55.590 to 56.293 nH) | 51.946 nH (−6.55 %) | 53.184 nH (−4.33 %) | 53.993 nH (−2.87 %) | 54.199 nH (−2.50 %) | 55.857 nH (+0.48 %) |
| L from the energy at 10 kHz | 51.946 nH | 53.183 nH | 53.993 nH | 54.197 nH | 55.856 nH |
| R at 10 kHz (sector 61.201 mΩ) | 62.193 mΩ | 62.263 mΩ | 62.270 mΩ | 62.524 mΩ | 62.304 mΩ |
| L at 3.5 MHz (at most its DC value) | 50.670 nH | 52.038 nH | 53.013 nH | 53.295 nH | 54.878 nH |
| R at 3.5 MHz | 81.303 mΩ | 82.174 mΩ | 81.105 mΩ | 80.370 mΩ | 81.329 mΩ |
| R at 3.5 MHz over R at 10 kHz | 1.31 | 1.32 | 1.30 | 1.29 | 1.31 |
| Solve at 10 kHz | 219 s, 1.0 GB, 3,000 iterations, residual 4e-08 | 357 s, 1.6 GB, 3,000 iterations, residual 1e-06 | 688 s, 2.6 GB, 3,000 iterations, residual 9e-06 | 918 s, 3.3 GB, 3,000 iterations, residual 4e-05 | 2258 s, 8.0 GB, 3,000 iterations, residual 7e-06 |
| Solve at 3.5 MHz | 10 s, 0.8 GB, 95 iterations | 15 s, 1.1 GB, 83 iterations | 35 s, 1.9 GB, 113 iterations | 45 s, 2.5 GB, 111 iterations | 112 s, 5.8 GB, 102 iterations |

Each solve ran on 4 MPI ranks. "Iterations" are GMRES's; at 10 kHz it stops at its limit, and the residual is the one it reached, ‖Ax − b‖ / ‖b‖.

What came out:

* **L is low and rises with the mesh**: 51.95, 53.18, 53.99 and 54.20 nH from level 0.25 to 1, 2.5 % under the lower reference at level 1. First-order edge elements driven at a port store too little magnetic energy on a coarse mesh, so a low L that rises as the mesh is refined is what they should give. The rise slows from 2.4 % (0.25 to 0.5) to 0.4 % (0.75 to 1) while 2.5 % is still left, so refining the copper alone does not close the gap.
* **With the air graded as the coil boards' is, L lands between the references**: 55.857 nH at level 0.75, 0.48 % above the arc between the round ends' centres and under the arc to the gap's faces, against 53.993 nH with the default air at the same level. Grading the air four times as finely (`grade` 0.125 against 0.5, `tet_grade` 0.175 against 0.7) and making its wedge layers half as thick moved L by 3.5 %, nine times what refining the copper from level 0.75 to 1 did: the air's mesh held the gap.
* **The port and the field's energy agree** within 0.01 % at every level and in the graded run: the lumped port reads back the inductance the field holds.
* **R is 1.6 to 2.2 % above the sector's 61.201 mΩ.** The half-discs past the round ends' centres add a little. The port's sheet also meets each round end only along a line through its tip, so the current crowds into that line; that crowding's resistance grows slowly as the mesh resolves it, which is the likely reason R rises from level 0.75 to 1.
* **At 3.5 MHz** L falls by 1.7 % and R rises by 29 % against 10 kHz at level 1: the current leaves the copper's middle for its surface as the skin depth falls to the copper's thickness. In the graded run L at 3.5 MHz is 54.878 nH, 1.8 % under its 10 kHz value and 0.3 % under the thin strip's high-frequency estimate of 55.039 nH. That estimate leaves out the copper's 35 µm thickness, which spreads the edge current over the edges' height and lowers the true limit a little, so it is not a firm floor.
* **At 10 kHz GMRES stops at its 3,000 iteration limit in every run**, with the residual at 4e-8 to 4e-5 of where it started rather than 1e-8. A check at 100 kHz on level 0.5, where GMRES converged to 1e-8 in 79 iterations, gave L = 53.181 nH and R = 62.308 mΩ, against 53.184 nH and 62.263 mΩ at 10 kHz: the 10 kHz L is right to 0.01 % despite the limit.

## Problems Met

What stopped a run or gave a wrong number while the board was solved, and what fixed it:

* **GMRES diverged at 10 kHz** with AMS as on the coil boards: in the air the electric field's gradients cost almost nothing at low frequency, so the operator AMS works on is all but singular. Telling AMS so (`AMSSingularOperator`, below 100 kHz) makes it converge, slowly.
* **A relative `--out` folder** gave Palace a mesh path it could not open from the folder it runs in; the script now makes the folder absolute.
