# E02 Results

Run on the 4-core, 15 GB test machine (Ubuntu 24.04, Python 3.13) with FastHenry 3.0.1 (the build in
`../../Solver_FastHenry`), on KESE 3.4.0's stack-up of the board, on 17 November 2026. Every number below is in
`results.json`, with the settings, the versions, the reference, the model's size, and the time and peak memory of
every solve.

## Expected Against What Came Out

| Filaments (across × through, each loop) | 1 × 1 | 3 × 1 | 5 × 1 | 9 × 1 | 9 × 3 |
|---|---|---|---|---|---|
| Filaments in the model | 252 | 756 | 1,260 | 2,268 | 6,804 |
| M at 10 kHz (reference 23.886 nH) | 23.891 nH (+0.022 %) | 23.892 nH (+0.024 %) | 23.892 nH (+0.024 %) | 23.892 nH (+0.024 %) | 23.892 nH (+0.024 %) |
| M back from the RX to the TX at 10 kHz | the same to the last digit | the same | the same | the same | the same |
| M at 3.5 MHz | 23.891 nH | 23.865 nH | 23.859 nH | 23.857 nH | 23.856 nH |
| TX's L at 10 kHz (E01's at the same filaments) | 55.343 nH (55.343) | 55.474 nH (55.474) | 55.516 nH (55.516) | 55.538 nH (55.538) | 55.578 nH (55.579) |
| TX's R at 10 kHz (E01's) | 61.207 mΩ (61.207) | 61.207 mΩ (61.208) | 61.208 mΩ (61.208) | 61.208 mΩ (61.208) | 61.208 mΩ (61.208) |
| TX's L at 3.5 MHz (E01's) | 55.343 nH (55.343) | 54.898 nH (54.899) | 54.782 nH (54.783) | 54.770 nH (54.771) | 54.800 nH (54.801) |
| TX's R at 3.5 MHz (E01's) | 61.207 mΩ (61.207) | 69.955 mΩ (69.946) | 74.361 mΩ (74.351) | 75.110 mΩ (75.099) | 75.423 mΩ (75.375) |
| Solve (each frequency) | 0.04 s | 0.2 s | 0.7 s | 7 s, 0.12 GB | 5 min, 1.1 GB |

| Quantity | The reference's own accuracy | FastHenry against it |
|---|---|---|
| M at 10 kHz | Neumann's integral is exact for two coaxial filament arcs; the 21 × 21 radii across the two traces average it with the current uniform across each, which leaves out the trace's thickness and the current's slight lean to the inside of a ring | +0.024 %, the same from 1 × 1 on |
| Reciprocity | exact for any exact solve of a passive linear model | the same to the last digit at every rung and both frequencies |
| The TX beside the open RX | an open loop carries no net current, so at 10 kHz the TX is E01's | E01's to the last digit at 10 kHz |

What came out:

* **M is 0.024 % over Neumann's integral, and the filaments do not move it.** With one filament per segment
  FastHenry already reads 23.891 nH, because it works out the mutual inductance of two bars from their whole
  cross-sections, not only from their centre lines (one filament on each centre line would give 23.997 nH, 0.5 %
  more). From 3 × 1 to 9 × 3 the uniform current is split ever finer and M stays at 23.892 nH to five digits.
* **Reciprocity holds to the last digit**: Z[TX][RX] and Z[RX][TX] are the same number at every rung and both
  frequencies, as FastHenry's direct solve of a symmetric system gives.
* **The open RX leaves the TX alone at 10 kHz**: L and R are E01's at the same filaments, to the last digit.
* **At 3.5 MHz the RX takes a little from the TX**: the TX's R rises by 0.01 to 0.06 % over E01's and its L falls by
  0.002 %, while M falls 0.15 % from its 10 kHz value. The RX carries no net current round it, but the TX's field
  drives eddy currents across its trace, filament against filament, whose loss shows in the TX's R. One filament
  across cannot carry any of that, so at 1 × 1 nothing changes with frequency.
