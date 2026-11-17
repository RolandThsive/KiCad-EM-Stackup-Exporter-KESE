# E01 Results

Run on the 4-core, 15 GB test machine (Ubuntu 24.04, Python 3.13) with FastHenry 3.0.1 (the build in
`../../Solver_FastHenry`), on KESE 3.4.0's stack-up of the board, on 17 November 2026. Every number below is in
`results.json`, with the settings, the versions, the model's size, and the time and peak memory of every solve.

## Expected Against What Came Out

| Filaments (across × through) | 1 × 1 | 3 × 1 | 5 × 1 | 9 × 1 | 9 × 3 | 15 × 3 |
|---|---|---|---|---|---|---|
| Filaments in the model | 126 | 378 | 630 | 1,134 | 3,402 | 5,670 |
| L at 10 kHz (reference 55.590 nH) | 55.343 nH (−0.44 %) | 55.474 nH (−0.21 %) | 55.516 nH (−0.13 %) | 55.538 nH (−0.09 %) | 55.579 nH (−0.02 %) | 55.580 nH (−0.02 %) |
| R at 10 kHz (reference 61.201 mΩ) | 61.207 mΩ | 61.208 mΩ | 61.208 mΩ | 61.208 mΩ | 61.208 mΩ | 61.208 mΩ |
| L at 3.5 MHz (estimate about 55.04 nH) | 55.343 nH | 54.899 nH | 54.783 nH | 54.771 nH | 54.801 nH | 54.797 nH |
| R at 3.5 MHz | 61.207 mΩ | 69.946 mΩ | 74.351 mΩ | 75.099 mΩ | 75.375 mΩ | 75.433 mΩ |
| R at 3.5 MHz over R at 10 kHz | 1.00 | 1.14 | 1.21 | 1.23 | 1.23 | 1.23 |
| Solve (each frequency) | 0.01 s | 0.03 s | 0.1 s | 0.6 s | 29 s, 0.31 GB | 3 min, 0.82 GB |

| Quantity | The reference's own accuracy | FastHenry against it |
|---|---|---|
| L at 10 kHz | Neumann's integral is exact for two filaments; the GMD makes it exact for a straight conductor of the trace's section, and on a ring of R / g = 84 the curvature's correction is of order (g / R)², 1e-4. The arc stops at the round ends' centres, where FastHenry's segments stop too | −0.02 % from 9 × 3 on, settling from below |
| R at 10 kHz | exact for the annular sector; the model's 126 chords are straight strips 0.5 mm wide, whose resistance is 0.011 % above the sector's (61.207 mΩ worked by hand for the chords) | +0.011 %, the chords' own value to the last digit |
| L at 3.5 MHz | none exact: the skin depth equals the copper's thickness, and in a ring the current also shifts towards the inside edge, which the straight strip's GMD leaves out | −0.4 % against the estimate, settled to 0.01 % from 9 × 3 on |

What came out:

* **L settles from below onto the reference.** 55.343, 55.474, 55.516, 55.538 nH as the filaments across go from 1
  to 9; then 3 through the copper adds 0.04 nH (55.579 nH) and 15 across adds nothing more (55.580 nH). Each
  filament carries a uniform current along its length, so a segment of one filament is a bar whose self term
  FastHenry works out exactly; it is the split of the section into filaments that sets how well the current's spread
  over the section, and so its geometric mean distance, is drawn. The limit, 55.58 nH, is 0.02 % under Neumann's
  integral over the arc: the size of the integral's own approximations (the GMD of a straight bar used on a ring,
  and the chords). Grover's ring formula scaled by the arc's share of the circle would read 0.7 % above it.
* **R is the chords' DC resistance at 10 kHz** whatever the filaments: 61.208 mΩ, the 126 straight strips' own
  value, 0.011 % over the annular sector, which is what straight strips 0.5 mm wide give against a ring.
* **At 3.5 MHz the current crowds to the edges**, and only the filaments across can show it: one filament holds the
  current uniform (R stays at 61.21 mΩ, L at its DC value), 3 across give 69.95 mΩ, and from 9 across R settles at
  75.4 mΩ, 1.23 times its DC value, while L falls 1.4 % from its DC value to 54.80 nH. Three filaments through the
  copper move R by 0.4 % and L by 0.05 %: the skin depth equals the copper's thickness, so the current is spread
  through it nearly as at DC. The coil boards use 3 × 1, which here reads L at 3.5 MHz 0.2 % high and R 7 % low
  (their traces are 0.2 to 0.3 mm wide, not 0.5, and there 3 × 1 reads R about 2 % low: see the coil boards'
  README).

## Problems Met

What stopped a run or gave a wrong number while the bridge was built, and what fixed it:

* **The first reference was Grover's ring formula times the share of the circle the arc covers** (55.99 nH): it
  puts the open arc 0.7 % over what FastHenry settled to. The share is not how an open loop's inductance scales:
  each part of the ring loses its coupling to the missing part, which the share leaves out. Neumann's double integral
  over the arc itself, with the same GMD, gives 55.590 nH and is what FastHenry is checked against now.
* **FastHenry's multipole refinement splits filaments** where they come close, and on the coil boards' 0.1 mm
  gaps that split ended in an exit ("filament not expected length"); the dense direct solve needs none of it, so
  every run here has the refinement off (`-a off`). At the coil boards' 1 mm gap, where both ways run, they gave the
  same numbers to 3 parts in 10⁸.
