# E02 Results

Solved on 18 Nov 2026 with Palace 0.19.0, on 4 MPI ranks (4 cores, 15 GB). The mesh ladder is in `results.json`, the run with the coil boards' air grading in `results_grade.json`, and M at 100 kHz on the default mesh in `results_100k.json`.

## Expected Against What Came Out

| Mesh level | 0.25 | 0.5 | 0.75 | 1 | 0.75, the coil boards' air |
|---|---|---|---|---|---|
| Nodes | 30,042 | 49,643 | 92,136 | 119,637 | 303,129 |
| M at 10 kHz (open arcs 23.886 nH, closed rings 24.400 nH) | 23.123 nH (−3.20 %) | 23.273 nH (−2.57 %) | 23.326 nH (−2.35 %) | 23.355 nH (−2.22 %) | 24.166 nH (+1.17 %) (100 kHz) |
| M back, RX to TX, at 10 kHz | 23.123 nH | 23.281 nH | 23.326 nH | 23.355 nH | 24.166 nH (100 kHz) |
| L TX at 10 kHz (E01's at the same level) | 52.597 nH (51.946) | 53.518 nH (53.184) | 54.187 nH (53.993) | 54.329 nH (54.199) | 55.880 nH (100 kHz) |
| R TX at 10 kHz | 62.193 mΩ | 62.263 mΩ | 62.269 mΩ | 62.523 mΩ | 62.344 mΩ (100 kHz) |
| M at 3.5 MHz | 23.047 nH (−3.51 %) | 23.203 nH (−2.86 %) | 23.266 nH (−2.60 %) | 23.299 nH (−2.46 %) | 24.104 nH (+0.91 %) |
| M back at 3.5 MHz | 23.047 nH | 23.203 nH | 23.266 nH | 23.299 nH | 24.104 nH |
| Solve at 10 kHz (both ports) | 677 s, 1.7 GB, 3,000 iterations, residual 3e-08 | 1149 s, 2.8 GB, 3,000 iterations, residual 2e-05 | 2374 s, 4.9 GB, 3,000 iterations, residual 1e-05 | 3078 s, 6.3 GB, 3,000 iterations, residual 5e-05 | 608 s, 12.5 GB, 191 iterations (100 kHz) |
| Solve at 3.5 MHz (both ports) | 26 s, 1.3 GB, 89 iterations | 47 s, 2.1 GB, 91 iterations | 122 s, 3.9 GB, 131 iterations | 160 s, 5.1 GB, 133 iterations | 447 s, 12.5 GB, 135 iterations |

Each solve ran on 4 MPI ranks and drove both ports in turn. "Iterations" are GMRES's for each port; at 10 kHz it stops at its limit, and the residual is the one it reached. The graded run restarted GMRES every 100 iterations (the ladder every 300), and its low frequency is 100 kHz (marked).

On level 0.75's default mesh, 100 kHz against 10 kHz (`results_100k.json`): M 23.3257 nH against 23.3261 nH (−0.002 %), M back 23.3257 nH against 23.3260 nH, L TX 54.1847 nH against 54.1867 nH (−0.004 %); at 100 kHz GMRES converged in 134 and 126 iterations.

What came out:

* **M is low and settles with the mesh**: 23.12, 23.27, 23.33 and 23.36 nH from level 0.25 to 1, 2.2 % under the open arcs at level 1, as the loop's L in E01. The rise slows from 0.7 % (0.25 to 0.5) to 0.1 % (0.75 to 1), so refining the copper alone does not close the gap.
* **With the air graded as the coil boards' is, M is 24.166 nH** at level 0.75: 1.17 % above the open arcs and 1.0 % under the closed rings, against 23.326 nH with the default air at the same level. Grading the air moved M by 3.6 %, as it moved E01's L by 3.5 %. M is above the open arcs, as it should be with the ports' sheets closing both loops.
* **The TX beside the open RX matches E01's loop once both have the graded air**: 55.880 nH against 55.857 nH (+0.04 %). On the default ladder the TX reads 0.2 to 1.3 % more than E01's loop at the same level, because E02's fine wedges run through the board to the RX, so the air under the TX is meshed finer than in E01, where tetrahedra start just under the copper. R at 10 kHz is E01's to 0.01 %.
* **Reciprocity holds**: the M from the TX to the RX and back agree to 0.03 % at every level, and to the fourth decimal in the graded run and at 100 kHz, where GMRES converged.
* **At 3.5 MHz** M is 0.2 to 0.3 % under its low-frequency value at every mesh, and the TX's R is 1 to 3 % above E01's: the current moves within each trace, and eddy currents in the RX's copper take a little from the TX.
* **At 10 kHz GMRES stops at its 3,000 iteration limit** for both ports at every level of the ladder, with residuals of 3e-8 to 6e-5. On level 0.75 at 100 kHz, where it converged in 134 and 126 iterations, M is 23.3257 nH against 23.3261 nH at 10 kHz (−0.002 %): the M read at the limit is right.

## Problems Met

What stopped a run or gave a wrong number while the board was solved, and what fixed it:

* **The graded mesh would not fit GMRES's 300 vectors in 15 GB.** E01's graded run peaked at 8.0 GB on 151,251 nodes; E02's carries the fine wedges through the board to the RX, 303,129 nodes (1.37 million unknowns). The first attempt was stopped before it ran out of memory, and the graded run restarts GMRES every 100 iterations (`--restart 100`), peaking at 12.5 GB.
* **At 10 kHz the graded run did not converge.** With the restart at 100, after 3,000 iterations (6,943 s) the TX's solve had reached a residual of 1.4e-3 and the RX's had stalled at 0.65, and the RX's numbers were plainly wrong (M back 51.0 nH, the RX's L 29.1 nH). The graded run's low frequency is therefore 100 kHz, where AMS needs no singular-operator flag and GMRES converged in 191 and 183 iterations; on level 0.75's default mesh M at 100 kHz and at 10 kHz agree to 0.002 %.
