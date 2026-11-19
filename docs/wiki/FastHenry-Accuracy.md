# 37. FastHenry Accuracy

Where the FastHenry bridge's errors come from, how big each one measured on E01, E02 and the coil board, and what
the bridge leaves out of the physics. Every number here is from the runs on the `FastHenry_Integration` branch
(`Examples/E01_circular_loop/results.json`, `Examples/E02_coaxial_loops/results.json`, the coil board's `Results/`),
and from the filament study in the branch's `Examples/Inductive Coils/README.md`.

## 37.1 No Mesh In The Air, No Iteration

Two of the usual sources of a field solver's error are not there:

| Source | In FastHenry | What it means |
|---|---|---|
| The air's mesh and its outer boundary | none: every filament couples to every other through its partial inductance, worked out exactly, and the space round the copper is not discretised | no air grading to refine and no domain size to choose |
| The iterative solve | none: the dense direct solve (`-s ludecomp -m direct`) factorises the whole system | the answer is the exact answer of the filament model; the impedance matrix comes out symmetric to the last digit, which is checked on every solve (reciprocity) |

What is left is how well the filaments draw the copper and its current: the split of each track's section, the
chords of an arc, and the rotor's grid of bars.

> [!NOTE]
> FastHenry's own default, GMRES with its multipole speed-up, left M from the TX to a receiver and M back 2.7 % apart
> on the coil boards, and is not used. The multipole refinement is also off (`-a off`): at the 1 mm gap, where both
> ways ran, they gave the same numbers to 3 parts in 10⁸.

## 37.2 The Error Budget On E01

Each line changes one thing and keeps the rest.

| Source | Test | Effect |
|---|---|---|
| Filaments across the trace, at 10 kHz | 1 → 3 → 5 → 9 across, 1 through | L +0.24 %, +0.08 %, +0.04 % (55.343, 55.474, 55.516, 55.538 nH) |
| Filaments through the copper, at 10 kHz | 9 × 1 → 9 × 3 | L +0.07 % (55.579 nH) |
| Finer still, at 10 kHz | 9 × 3 → 15 × 3 | L +0.002 % (55.580 nH): settled |
| The chords | 126 straight strips, 0.5 mm wide, in place of the ring | R at 10 kHz 0.011 % over the annular sector (61.208 against 61.201 mΩ), the chords' own value worked by hand (61.207 mΩ) |
| The reference's own approximations | Neumann's integral with the GMD of a straight bar used on a ring of R / g = 84 | of order (g / R)², 1e-4 |
| **FastHenry against the reference** | Neumann's double integral over the open arc | **L −0.02 % from 9 × 3 on, settling from below; R +0.011 %** |

At 3.5 MHz, where the skin depth equals the copper's thickness and no formula is exact, the ladder shows how many
filaments the crowding of the current needs:

| E01 at 3.5 MHz | 1 × 1 | 3 × 1 | 9 × 1 | 15 × 3 |
|---|---|---|---|---|
| L | 55.343 nH | 54.899 nH | 54.771 nH | 54.797 nH |
| R | 61.207 mΩ | 69.946 mΩ | 75.099 mΩ | 75.433 mΩ |

One filament holds the current uniform, so it misses the rise of R altogether. With 3 × 1, the coil board's setting,
E01 reads L at 3.5 MHz 0.2 % high and R 7 % low on its 0.5 mm trace. From 9 × 3 on, L and R move by 0.01 % and 0.08 %.

## 37.3 Mutual Inductance On E02

M is the number the coil board's signal rests on.

| E02, M at 10 kHz | 1 × 1 | 3 × 1 | 9 × 3 |
|---|---|---|---|
| FastHenry | 23.891 nH | 23.892 nH | 23.892 nH |
| Against Neumann's integral (23.886 nH) | +0.022 % | +0.024 % | +0.024 % |

M hardly depends on the filaments: FastHenry works out the coupling of two bars from their whole cross-sections, so
even one filament per segment is within 0.004 % of the finest. The 0.024 % left is of the size of the reference's own
approximations: it averages Neumann's integral over 21 × 21 radii across the two traces' widths with the current
uniform across each, leaving out the traces' thickness and the current's slight lean to the inside of a ring.

## 37.4 The Coil Board

The coil board runs at 3 filaments across each track and 1 through, the edge ones twice as narrow, and a rotor grid
of bars 0.05 mm wide at its edges growing to 0.3 mm. What that setting costs was measured on a sibling board of the
same family at 1 mm and 0° (the branch's `Examples/Inductive Coils/README.md`):

| Change from the setting used | M SIN and M COS | L TX | R TX |
|---|---|---|---|
| 1 filament across instead of 3 | 0.2 % | 0.04 % | |
| 5 filaments across instead of 3 | 0.03 % | 0.01 % | **+1.5 %** |
| 2 filaments through instead of 1 | 0.01 % | 0.1 % | |
| A finer rotor grid (0.025 to 0.2 mm bars) | 0.04 % | | |
| Finer still (0.02 to 0.15 mm) | 0.005 % more | | |

So M and L TX are settled to a few hundredths of a percent. R TX is the number that still moves, because at 3.5 MHz
the skin depth (35 µm) is the copper's thickness and the current crowds to each track's edges more finely than three
filaments follow; on the coil boards' 0.2 to 0.3 mm traces 3 × 1 reads R about 2 % low.

On `S0d2_1x_OD23_2L_tiny_TX3top_Cut` itself, every one of its 81 solves was reciprocal to the last digit, and the
best sine through each gap's 16 solves leaves 0.018 to 0.019 nH rms at 1 mm, against an amplitude of 4.73 nH. The
solves at θ and θ + 180° came out as the same numbers, as the two-sector rotor's symmetry asks: turning the rotor
moves only its grid, never the stator's filaments, so there is no meshing noise between angles.

## 37.5 What The Bridge Leaves Out

| What | In the bridge | What it does to the numbers |
|---|---|---|
| Displacement current | none: FastHenry's magneto-quasi-static formulation | no capacitance between turns and no self-resonance; the answer holds only well below the coil's self-resonance |
| The insulators | FR-4, solder mask and air are not in the model | right for the magnetic field, since they are μr 1 and σ 0 |
| The copper's conductivity | 5.8 × 10⁷ S/m, one value for all copper | copper at 20 °C; temperature is not followed |
| The current inside a filament | uniform along it and across it | the current's spread across a track is drawn only as finely as its filaments (37.2) |
| The copper's shape | each track a straight bar along its centre line, its width and its layer's thickness; arcs as chords | a track's round ends and a via's pads are not modelled, only its centre line, width and barrel; on the coil board they are a small part of the copper. The etched trapezoid and the copper's roughness are not in the model |
| Boards, not arbitrary 3D | copper flat at its layers' heights | a board over another (a rotor over a stator) works; a part tilted out of the board's plane does not |
| The terminals | a port between two nodes; at a cut, the copper inside the 0.2 mm cut taken out | the leads to the IC are not modelled |

## 37.6 What To Trust

| Quantity | On boards like E01, E02 and the coil board |
|---|---|
| L at 10 kHz | within 0.02 % of Neumann's integral from 9 × 3 on; 0.2 % low at 3 × 1 |
| M | within 0.024 % of Neumann's integral at any filaments; on the coil board settled to a few hundredths of a percent |
| R at 10 kHz | the chords' DC resistance, 0.011 % over the ring's |
| R at 3.5 MHz, skin and proximity effect | no exact reference; it needs filaments across: settled from 9 across on E01, about 2 % low at the coil board's 3 × 1 |
| Reciprocity | to the last digit on every solve: a check on every run, at no cost |
| SIN and COS, the angle error | from M, so as good as M; every solve's M is read only once its reciprocity check passes |

How FastHenry's numbers compare with the other solvers' on the same boards is on
[Solvers Comparison](Solvers-Comparison.md).

| Previous | Next |
|:---|---:|
| [FastHenry Test Boards And Results](FastHenry-Test-Boards-And-Results.md) | [FastHenry Troubleshooting](FastHenry-Troubleshooting.md) |
