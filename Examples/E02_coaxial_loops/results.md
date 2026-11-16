# E02 Results

Run on the 4-core, 15 GB test machine (Ubuntu 24.04) with Elmer 26.2 (`a19504a`), gmsh 4.15.2 and
KESE 3.4.0, on 15 and 16 November 2026. Every number below is in `results.json`, with the settings,
the versions, the mesh's size, the time, the memory and the solver's last residual of every solve.

## Expected Against What Came Out

| Quantity | Reference | Level 0.75 | Level 1 |
|---|---|---|---|
| Nodes | | 92,120 | 119,559 |
| M at 10 kHz | 24.13 nH | 23.33 nH (−3.3 %) | 23.38 nH (−3.1 %) |
| M at 3.5 MHz | 24.13 nH (an estimate) | | 23.32 nH (−3.4 %) |
| TX's L at 10 kHz | E01's L at the same level: 53.91 and 54.20 nH | 54.06 nH | 54.18 nH |
| TX's L from the field's energy, 10 kHz | the same | 54.06 nH | 54.23 nH |
| TX's R at 10 kHz | E01's: 61.53 mΩ | 61.53 mΩ | 61.53 mΩ |
| TX's R at 3.5 MHz | E01's at level 1: 79.25 mΩ | | 80.75 mΩ |
| The RX's transfer resistance at 3.5 MHz | none | | 0.91 mΩ |
| Solve at 10 kHz | | 9 min, 5.19 GB, 1500 iterations (the cap), residual 1.6e-6 | 22 min, 6.74 GB, 1500 iterations (the cap), residual 2.9e-6 |
| Solve at 3.5 MHz | | | 10 min, 6.74 GB, 1147 iterations, converged (1e-7) |

The reference is Maxwell's formula for two coaxial circular filaments,
μ0 √(ab) ((2/k − k) K(k) − (2/k) E(k)) with k² = 4ab / ((a + b)² + d²), averaged over 41 × 41
filaments across both traces' widths (24.40 nH), times the share of the circle the TX's copper
covers (0.989) up to the round ends' centres. The current runs on into the half-discs past them,
so this share is a lower bound: taken on to the gap's faces it gives 24.32 nH, 0.8 % more (see E01's
results.md). The two filaments alone, at the traces' centre lines, give 24.51 nH.

| Quantity | The reference's own accuracy | Elmer against it |
|---|---|---|
| M at 10 kHz | Maxwell's formula is exact for filaments; the average over the widths assumes uniform current, right at 10 kHz; the open loop's share is a lower bound, by up to 0.8 % | −3.1 % at level 1, rising with the mesh |
| M at 3.5 MHz | the current crowds to each trace's edges, which moves M little: the loops are 1.565 mm apart, three times a trace's width | −3.4 % |

What came out:

* **M is 3.1 % low and rises with the mesh**, as E01's L does, and by about the same amount at the
  same mesh size, for the same reason: the air's mesh round the copper, which the ladder does not
  refine (see the diagnostic run below and E01's results.md).
* **The open RX leaves the TX's L alone**: 54.18 nH against E01's 54.20 nH at level 1. A loop with no
  current in it adds no field. At level 0.75 the TX's L is 0.3 % above E01's. The two meshes are not
  the same at the same level (E02 has wedge layers through its second copper as well, and more nodes)
  and E02 stops at 1500 iterations, E01 at 3000; differences of a few tenths of a percent are of the
  size those make.
* **At 3.5 MHz the RX adds 1.5 mΩ to the TX's R.** RX carries no net current, but eddy currents
  circulate across its width and dissipate power that the TX supplies: the proximity effect. It
  shows also as the real part of the RX's transfer impedance, 0.91 mΩ.
* **M falls 0.3 % from 10 kHz to 3.5 MHz**, while the TX's L falls 1.6 %: the internal inductance
  that the skin effect removes belongs to each trace's own field, not to the field that links the
  other loop.

## Diagnostic Run

As on E01, level 0.75 again with the air graded twice as finely (`grade` 0.25, `tet_grade` 0.35), at
10 kHz and 1500 iterations:

| Run | File | Nodes | M | Against the reference | TX's L | Solve |
|---|---|---|---|---|---|---|
| The ladder's level 0.75 | `results.json` | 92,120 | 23.33 nH | −3.3 % | 54.06 nH | 9 min, 5.19 GB, residual 1.6e-6 |
| The air graded twice as finely | `results_grade.json` | 134,840 | 23.87 nH | −1.1 % | 54.94 nH | 15 min, 7.66 GB, residual 2.1e-6 |

M rose 2.3 %, as much as E01's L did with the same change (from 3.7 % to 1.55 % under its
reference): the air's coarse mesh round the copper held E01's L and E02's M down alike. The TX's L
rose 1.6 %, and its L from the field's energy agrees with the circuit's within 0.04 %.

## Problems Met

See E01's results.md and the wiki's *Elmer FEM Troubleshooting* page.
