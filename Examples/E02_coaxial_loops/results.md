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
covers (0.989). The two filaments alone, at the traces' centre lines, give 24.51 nH.

| Quantity | The reference's own accuracy | Elmer against it |
|---|---|---|
| M at 10 kHz | Maxwell's formula is exact for filaments; the average over the widths assumes uniform current, right at 10 kHz; the open loop's share is a first-order estimate | −3.1 % at level 1, rising with the mesh |
| M at 3.5 MHz | the current crowds to each trace's edges, which moves M little: the loops are 1.565 mm apart, three times a trace's width | −3.4 % |

What came out:

* **M is 3.1 % low and rises with the mesh**, as E01's L does, and by about the same amount at the
  same mesh size: whatever holds E01's L down holds M down alike (see E01's results.md for the
  diagnostic runs).
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

## Problems Met

See E01's results.md and the wiki's *Elmer FEM Troubleshooting* page.
