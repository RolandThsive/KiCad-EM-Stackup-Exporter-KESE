# 67. Palace Accuracy

Where the Palace bridge's errors come from, how big each one measured, and what the bridge leaves out of the physics.
Every number here is from the runs on the `Palace_Integration` branch.

> [!NOTE]
> The error budget against textbook references comes from E01 and E02, whose solves are being finished; their
> section below is filled in from their results when they are on the branch. The coil board has no closed-form
> reference for M, so its accuracy rests on the checks and the mesh study here.

## 67.1 The Checks On Every Solve

The committed Palace has no direct solver ([Palace Installation](Palace-Installation.md#624-why-it-is-built-without-parmetis)),
so every iterative solve is checked before it is read. A solve on the coil board is **readable** when all of these
hold (`readable()` in its `make_charts.py`):

| Check | What it catches | Allowed | `S0d2_1x_OD23_2L_tiny_TX3top_Cut`, worst of 81 solves |
|---|---|---|---|
| GMRES converged | a solve stopped short | to 1e-8 of the starting residual | all converged, 115 to 195 iterations |
| R TX positive | a broken port or drive | | 444.67 to 518.85 mΩ |
| L TX from its port's voltage against L from the field's magnetic energy, 2W / \|I\|² | the port and the field inside disagreeing | 1 % | 0.005 % |
| M from the TX to SIN and COS against M back, with each receiver driven (the first angle of each gap) | an unconverged or unsymmetric solve | 1 % | 0.00026 % |

These say the solve reached the answer of its own mesh. They do not say how far that mesh is from the true answer,
which is what the rest of this page is about.

## 67.2 The Linear Solve's Tolerance

The tolerance was chosen on S0, the smallest coil board on the branch, at 1 mm and 0°: a residual of 1e-10 instead of
1e-8 moved L, R and M by under 3e-7 of themselves, and 1e-6 by under 4e-5. At 1e-8 the solve's own error is far below
the mesh's.

## 67.3 The Mesh

The coil board's mesh settings were settled on S0 at 1 mm and 0°, one setting changed at a time from the bridge's
defaults. The air close round the thin tracks holds most of what a coarse mesh misses: grading it four times as
finely (`grade` 0.5 → 0.125, `tet_grade` 0.7 → 0.175) raised M by 3 to 4 % and L TX by 2 %, while the copper's own
mesh, twice as fine, moved M by under 1 %. With the air graded four times as finely and wedge layers half as thick
(`dz_max` 0.4 → 0.2 mm), which is how `S0d2_1x_OD23_2L_tiny_TX3top_Cut` is solved:

| Quantity | Error of the mesh as solved |
|---|---|
| M of SIN and COS | within 0.5 % of the finest mesh that fits in 16 GB |
| L TX | still rising with the copper's mesh (+1.5 % with it twice as fine); first-order edge elements give the field's energy from below, so L TX reads low, by about 5 % if each refinement keeps adding half as much as the one before |
| R TX | not studied apart |

## 67.4 The Mesh At Each Angle

Every rotor angle gets its own mesh, the rotor's outline at that angle drawn into it, so the stator's mesh differs a
little between angles. That shows as small noise on the curves, and the best sine fit measures it: the rms of what the
fit leaves, as a share of the amplitude.

| Air gap | SIN | COS |
|---|---|---|
| 2 mm | 0.25 % | 0.17 % |
| 1.5 mm | 0.31 % | 0.25 % |
| 1 mm | 0.40 % | 0.36 % |
| 0.5 mm | 0.58 % | 0.57 % |
| 0.1 mm | 1.2 % | 1.21 % |

The residual grows as the gap closes, as the harmonics the rotor adds at a small gap do
([Palace Test Board Results](Palace-Test-Board-Results.md#at-the-01-mm-air-gap)); the fit cannot tell mesh noise from
a real harmonic, so these are upper bounds on the noise.

## 67.5 The Ports

| Item | Effect |
|---|---|
| Receivers' ports at 1 MΩ | the receivers are open to within \|Z\| / 1 MΩ, a few parts in a million |
| A port sheet over a via's drill hole | measured on S0: a sheet standing over the hole of a left-out via does not end on copper where it crosses the hole, and read M 13 % low when the mesh resolved it. The bridge fills a left-out via's pads over the hole; the sheet then reads the same M in pieces as drawn whole, within 0.5 %. `S0d2_1x_OD23_2L_tiny_TX3top_Cut` is opened by cuts and keeps its vias, so this does not arise on it |
| Where the coil is opened | the cut sits 0.86 mm from the via, where the real board is opened; the voltage across it is the coil's EMF round the whole loop |

## 67.6 What The Model Leaves Out

| Item | In the model | What it does to the answer |
|---|---|---|
| FR-4 and solder mask | air (εr 1) | at 3.5 MHz their permittivity changes nothing the examples read |
| The outer boundary | a perfect conductor three board radii out (35.1 mm) | far enough out not to matter, by the branch's choice; not measured apart on the coil board |
| Mesh order | first order | see 67.3: L TX reads low |

## 67.7 Against The References

E01 and E02 set the bridge against textbook values: Neumann's integral over the open arc and an annular sector's
resistance for E01, Maxwell's formula for coaxial rings for E02. Their numbers go here when their solves are on the
branch. On the coil board, the only outside number is the generator's estimate of L TX with the rotor away, 292 nH,
against Palace's 281.0 nH (−3.8 %); the generator's figure is an estimate, not a reference.

| Previous | Next |
|:---|---:|
| [Palace Test Board Results](Palace-Test-Board-Results.md) | [Palace Hardware](Palace-Hardware.md) |
