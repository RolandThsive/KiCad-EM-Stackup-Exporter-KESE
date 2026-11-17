# E02 Results

Run on the 4-core, 15 GB test machine (Ubuntu 24.04, Python 3.13) with PyPEEC 5.8.0 (SciPy 1.18.1, NumPy 2.5.5),
on KESE 3.4.0's export of the board, on 17 November 2026. Every number below is in `results.json`, with the
settings, the versions, the grid, the time, the memory, the iterative solver's iterations and residual, and PyPEEC's
own checks of every solve.

## Expected Against What Came Out

| Quantity | Reference | 100 µm | 50 µm |
|---|---|---|---|
| Grid | | 208 × 208 × 46 | 412 × 412 × 46 |
| M at 10 kHz | 24.13 nH | 24.01 nH (−0.51 %) | 24.09 nH (−0.17 %) |
| M at 3.5 MHz | about 24.13 nH | 23.78 nH | 23.84 nH |
| TX's L at 10 kHz | E01's at the same voxels: 57.00 and 56.59 nH | 57.00 nH | 56.60 nH (+0.01 %) |
| TX's L from the stored energy at 10 kHz | the same | 57.00 nH | 56.60 nH |
| TX's R at 10 kHz | E01's: 69.25 and 65.23 mΩ | 69.25 mΩ | 65.23 mΩ |
| TX's L at 3.5 MHz | E01's: 56.14 and 55.61 nH | 56.09 nH (−0.08 %) | 55.55 nH (−0.09 %) |
| TX's R at 3.5 MHz | E01's: 83.37 and 81.93 mΩ | 83.88 mΩ (+0.6 %) | 82.56 mΩ (+0.8 %) |
| Solve at 10 kHz | | 12 s, 0.64 GB | 62 s, 2.16 GB |
| Solve at 3.5 MHz | | 29 s, 0.64 GB | 145 s, 2.17 GB |

Every solve took one GMRES iteration, with a residual of 1e-10 at 10 kHz and below 1e-8 at 3.5 MHz, and passed
PyPEEC's own checks; the TX's L and R from its voltage and from the stored energy and the losses agree to the last
digit.

What came out:

* **M is 0.17 % under Maxwell's formula at 50 µm**, and rises towards it as the voxels shrink: the error went from
  0.51 % to 0.17 % when the voxels halved, so the limit is at or a little over 24.13 nH. The reference carries the
  open loop's share of the circle, uncertain by up to 0.8 % in the same way as E01's L (it stops the current at the
  round ends' centres), so this board cannot tell PyPEEC's M from it more finely than that.
* **The open RX leaves the TX alone at 10 kHz**: the TX's L and R are E01's at the same voxels to 0.01 %. An open
  loop carries no current round it.
* **At 3.5 MHz the RX takes a little from the TX**: the TX's L falls by 0.09 % and its R rises by 0.8 % against
  E01's, and M by 1 % against 10 kHz. The RX carries no net current, but eddy currents circulate across its trace,
  driven by the TX's field; their loss shows in the TX's R and in the real part of the mutual impedance (3.2 mΩ at
  50 µm).
* **The z step fits the board**: the two copper sheets' middles are 1.565 mm apart, and with 45 steps of 34.8 µm the
  sheets land within 1 µm of where they are; each sheet's resistivity is scaled by 0.994 so that its 34.8 µm of voxels
  keep the 35 µm copper's sheet resistance.
