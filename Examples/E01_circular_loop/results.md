# E01 Results

Run on the 4-core, 15 GB test machine (Ubuntu 24.04, Python 3.13) with PyPEEC 5.8.0 (SciPy 1.18.1, NumPy 2.5.5),
on KESE 3.4.0's export of the board, on 17 November 2026. Every number below is in `results.json` (the voxel
ladder) and `results_cu2.json` (two voxel layers through the copper), with the settings, the versions, the grid, the
time, the memory, the iterative solver's iterations and residual, and PyPEEC's own checks of every solve.

## Expected Against What Came Out

| Quantity | Reference | 100 µm | 50 µm | 25 µm | 12.5 µm |
|---|---|---|---|---|---|
| Grid (one voxel layer, 35 µm) | | 208 × 208 | 412 × 412 | 822 × 822 | 1642 × 1642 |
| Copper voxels | | 3,102 | 12,467 | 49,979 | 199,997 |
| L at 10 kHz | 55.99 to 56.44 nH | 57.00 nH (+1.8 %) | 56.59 nH (+1.1 %) | 56.24 nH (+0.44 %) | 56.09 nH (+0.18 %) |
| L from the stored energy at 10 kHz | the same | 57.00 nH | 56.59 nH | 56.24 nH | 56.09 nH |
| R at 10 kHz | 61.20 mΩ | 69.25 mΩ (+13 %) | 65.23 mΩ (+6.6 %) | 63.20 mΩ (+3.3 %) | 62.30 mΩ (+1.8 %) |
| R from the losses at 10 kHz | the same | 69.25 mΩ | 65.23 mΩ | 63.20 mΩ | 62.30 mΩ |
| L at 3.5 MHz | about 55.44 nH (an estimate) | 56.14 nH | 55.61 nH | 55.16 nH | 54.99 nH (−0.8 %) |
| R at 3.5 MHz | | 83.37 mΩ | 81.93 mΩ | 80.53 mΩ | 79.79 mΩ |
| R at 3.5 MHz over R at 10 kHz | | 1.20 | 1.26 | 1.27 | 1.28 |
| Solve at 10 kHz | | 1 s | 3 s, 0.17 GB | 9 s, 0.37 GB | 24 s, 1.29 GB |
| Solve at 3.5 MHz | | 1 s, 0.11 GB | 8 s, 0.17 GB | 24 s, 0.41 GB | 58 s, 1.39 GB |

The percentages of L are against 55.99 nH, the lower end of the reference's band. Every solve took one GMRES
iteration (PyPEEC's preconditioner is all but exact for a single loop), with a residual of 1e-10 at 10 kHz and below
1e-8 at 3.5 MHz, and passed PyPEEC's own checks.

| Quantity | The reference's own accuracy | PyPEEC against it |
|---|---|---|
| L at 10 kHz | Grover's formula is exact for a thin ring (here R / g = 84). The open loop's share is uncertain by 0.8 %: it stops the current at the round ends' centres (55.99 nH), but the current runs on into the half-discs, and taken to the gap's faces it gives 56.44 nH | inside the band from 25 µm on, and falling towards its lower end as the voxels shrink |
| L from the energy | the same | the same as the terminals' L to the last digit at every size |
| R at 10 kHz | exact for the annular sector; the two round ends past the sector's ends are left out, so the board's own R is a little higher | +1.8 % at 12.5 µm, the excess halving with each halving of the voxels |
| L at 3.5 MHz | none exact: the skin depth equals the copper's thickness, so the current is neither uniform nor crowded to the surface | −0.8 % against the thin strip's estimate |

What came out:

* **L settles from above, into the reference's band.** 57.00, 56.59, 56.24, 56.09 nH as the voxels go from 100 to
  12.5 µm. A voxel is copper when its centre is in the trace, so the trace's round edges are drawn as steps, and its
  width is right only on average; the steps' error in L falls as the voxels shrink. The last step (−0.15 nH, half the
  one before) puts the limit at about 55.9 to 56.0 nH, the band's lower end, where Grover's formula with the current
  stopped at the round ends' centres sits.
* **The terminals and the stored energy agree** to the last digit, for L and for R, at every voxel size and both
  frequencies: the two terminals, PyPEEC's sources and the read-back give the inductance and the resistance that the
  field and the losses hold.
* **R converges at first order**: its excess over the annular sector is 8.05, 4.03, 2.00 and 1.10 mΩ, halving with
  each halving of the voxels. Taken to zero voxel size, the last two give 61.4 mΩ, 0.3 % over the sector, which is
  what the two half-discs past the sector's ends add (the Elmer branch's E01 has its R 0.5 % over the sector for the
  same reason).
* **At 3.5 MHz** L falls by 2 % and R rises by 28 % against 10 kHz at 12.5 µm: the current crowds to the trace's
  edges. With one voxel layer through the copper the current is uniform through its thickness, so only the crowding
  across the width is drawn, and the finer the voxels across the trace, the more of it shows (R rises from 1.20 to
  1.28 times its 10 kHz value along the ladder). The Elmer branch, which resolves the copper's thickness with two
  wedge layers, gives 1.29.

## Two Voxel Layers Through the Copper

`results_cu2.json`: the 25 µm ladder step again with two voxel layers of 17.5 µm through the copper
(`--n-cu 2`):

| 25 µm | L at 10 kHz | R at 10 kHz | L at 3.5 MHz | R at 3.5 MHz | Solve at 3.5 MHz |
|---|---|---|---|---|---|
| one layer (`results.json`) | 56.236 nH | 63.200 mΩ | 55.160 nH | 80.530 mΩ | 24 s, 0.41 GB |
| two layers (`results_cu2.json`) | 56.234 nH | 63.200 mΩ | 55.159 nH | 80.530 mΩ | 37 s, 0.81 GB |

Nothing moves. A lone trace is the same above and below its middle, so its two halves carry the same current
whatever the frequency; the current's drift towards the surfaces would take three layers or more to show, and on
this board it is small beside the crowding to the edges. On the coil boards, where a rotor or another coil sits on
one side of a trace, the two halves can differ; one layer is what they are solved with.

## Problems Met

What stopped a run or gave a wrong number while the bridge was built, and what fixed it:

* **PyPEEC's solution file wraps its answer** in a `data` block beside `meta`; the bridge reads `data`.
* **PyPEEC's integrity check fails on groups of unequal size**: its rule that no two conductors touch pairs the
  domains of the groups it is given one to one. The bridge gives it one domain per conductor (the coil's first
  terminal, or a rotor's grounded voxel).
* **A terminal's voxels split into many groups** when they were taken as the voxels inside the gap's outline; they
  are now the coil's voxels that share a face with the gap, grouped with their edge and corner neighbours, which
  gives exactly two, one on each side.
* **The grid's z step chose extreme values** on the coil boards (45 µm at small gaps, 28 µm at 2 mm) when it looked
  only for the least misfit of the copper sheets; it now takes the step nearest the copper's 35 µm among those that
  put every sheet within a micron of a voxel layer.
