# E01 Results

Run on the 4-core, 15 GB test machine (Ubuntu 24.04) with Elmer 26.2 (`a19504a`), gmsh 4.15.2 and
KESE 3.4.0, on 15 and 16 November 2026. Every number below is in `results.json` (the mesh ladder)
and the `results_*.json` beside it (the iteration check and the diagnostic runs), with the settings,
the versions, the mesh's size, the time, the memory and the solver's last residual of every solve.

## Expected Against What Came Out

| Quantity | Reference | Level 0.75 | Level 1 | Level 1.3 |
|---|---|---|---|---|
| Nodes | | 59,782 | 85,712 | 125,043 |
| L at 10 kHz | 55.99 nH | 53.91 nH (−3.7 %) | 54.20 nH (−3.2 %) | 54.27 nH (−3.1 %) |
| L from the field's energy at 10 kHz | 55.99 nH | 53.91 nH | 54.18 nH | 54.29 nH |
| R at 10 kHz | 61.20 mΩ | 61.53 mΩ (+0.5 %) | 61.53 mΩ (+0.5 %) | 61.52 mΩ (+0.5 %) |
| R_dc, Elmer's DC solve | 61.20 mΩ | 61.34 mΩ (+0.2 %) | 61.36 mΩ (+0.3 %) | 61.36 mΩ (+0.3 %) |
| L at 3.5 MHz | about 55.44 nH (an estimate) | | 53.26 nH (−3.9 %) | L13_HF |
| R at 3.5 MHz | | | 79.25 mΩ (1.29 × R_dc) | R13_HF |
| Solve at 10 kHz | | 25 min, 3.39 GB, 3000 iterations, residual 5.9e-7 | 17 min, 3000 iterations, residual 1.3e-6 | 45 min, 7.09 GB, 3000 iterations, residual 2.7e-6 |
| Solve at 3.5 MHz | | | 6 min, 864 iterations, converged (1e-7) | T13_HF |

| Quantity | The reference's own accuracy | Elmer against it |
|---|---|---|
| L at 10 kHz | Grover's formula is exact for a thin ring (here R / g = 84); the open loop's share of the closed ring is a first-order estimate, good to a fraction of the gap's 1.1 % of the circle | −3.1 % at the finest mesh, rising with the mesh |
| L from the energy | the same | within 0.05 % of the circuit's L at every level |
| R at 10 kHz | exact for the annular sector; the two round ends past the sector's ends are left out | +0.5 % |
| L at 3.5 MHz | none exact: the skin depth equals the copper's thickness, so the current is neither uniform nor crowded to the surface | −3.9 % against the thin strip's estimate |

What came out:

* **L is 3 % low and rises with the mesh**: 53.91, 54.20, 54.27 nH. First-order edge elements with
  the current imposed give a lower bound on the field's energy, so a low L that rises as the mesh is
  refined is what they should give. The rise from level 1 to 1.3 (0.12 %) is far smaller than the
  3 % that is left, so refining the copper alone does not close the gap; see the diagnostic runs.
* **The circuit and the field's energy agree** within 0.05 % at every level: the electrodes, the
  sheet and Elmer's circuit read back the same inductance the field holds.
* **R is 0.5 % high**, as it should be: the annular sector of the reference stops at the round ends'
  centres, and the current also runs through the two half-discs past them to the electrodes.
* **At 3.5 MHz** L falls by 1.7 % and R rises by 29 % against 10 kHz: the current leaves the
  copper's middle for its surface as the skin depth falls to the copper's thickness.

## The Iterative Solve

At 10 kHz the linear solve stops at its cap of 3000 iterations at every level, with the residual
stalled between 6e-7 and 3e-6 instead of reaching 1e-7. At 3.5 MHz it converges in 864 iterations.

| Level 1 at 10 kHz | Iterations | Residual | L | R |
|---|---|---|---|---|
| `results_iter1500.json` | 1500 | 1.5e-6 | 54.11 nH | 61.52 mΩ |
| `results.json` | 3000 | 1.3e-6 | 54.20 nH | 61.53 mΩ |

Doubling the iterations moved L by 0.17 % and R by 0.01 %, with the residual barely lower. The
iteration error of L at 10 kHz is therefore of the same size as the change from level 1 to 1.3, and
the three levels cannot be extrapolated to a zero mesh size with any confidence; the level 1.3 value
is a lower bound, not a limit.

## Diagnostic Runs

DIAGNOSTICS

## Problems Met

What stopped a run or gave a wrong number while the bridge was built, and what fixed
it, is on the wiki's *Elmer FEM Troubleshooting* page: the coil that must be opened at its port, the
tree gauge that a direct solver turns on, the stalling residual at 10 kHz, and the mesh's sliver
tetrahedra.
