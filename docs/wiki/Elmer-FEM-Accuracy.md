# 22.1 Elmer FEM Accuracy

Where the Elmer bridge's errors come from, how big each one measured on E01 and E02, what that means
for the coil board, and what the bridge leaves out of the physics. Every number here is from the runs
on the `Elmer_Integration` branch (`Examples/E01_circular_loop/results*.json`,
`Examples/E02_coaxial_loops/results*.json` and the coil board's
`Examples/Inductive Coils/S0d2_1x_OD23_2L_tiny_TX3top_Cut/Results/`).

## 22.1.1 The Error Budget On E01

Each line changes one thing and keeps the rest; all are L at 10 kHz.

| Source | Test | Effect on L |
|---|---|---|
| The copper's mesh | level 0.75 → 1 → 1.3 (59,782, 85,712, 125,043 nodes) | +0.54 %, then +0.12 % |
| The iterative solve | level 1 at 1500 and at 3000 iterations | +0.17 % with the doubled cap |
| The air's mesh | level 0.75 with the air graded twice as finely (`grade` 0.25, `tet_grade` 0.35; 88,760 nodes against 59,782), then four times (0.125 and 0.175; 166,471 nodes) | **+2.3 %, then +1.1 %** |
| The air domain | level 0.75 in a domain twice as big (120 mm in radius and half height instead of 60) | +0.26 %: the 60 mm domain holds L down by about 0.3 %, since the bigger one keeps about an eighth of that |
| The reference's open-loop share | with the sheet across the gap, the coil's voltage is the flux through the whole circle, so L is the closed ring's L times the share of the circle the current runs in; the reference ends that share at the round ends' centres, but the current runs on into the half-discs | the reference is a lower bound: up to 0.8 % higher (56.44 nH) with the current taken on to the gap's faces |
| **Elmer against the reference** | Grover's ring formula with the trace's GMD | **−3.1 % at level 1.3; −0.46 % at level 0.75 with the air four times as fine** |

![E01's L and E02's M at 10 kHz, as a percentage off their references, against the mesh's nodes in thousands: E01 rises from −3.7 % at 60,000 nodes to −3.2 % at 86,000 and −3.1 % at 125,000; E02 rises from −3.3 % at 92,000 nodes to −3.1 % at 120,000; E01 with the air graded twice and four times as finely rises from −1.55 % at 89,000 nodes to −0.46 % at 166,000, and E02's M with the air graded twice as finely sits at −1.1 % with 135,000 nodes; E01 in an air domain twice as big sits at −3.5 % with 87,000 nodes; a grey band from 0 to +0.8 % shows the reference's own uncertainty](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Board-Results/elmerresults_1_against_reference.webp)

E01's L and E02's M against the mesh's size, from the runs in the table. The ladder in the first line refines only the copper's mesh: a level divides `h_edge`, `h_in` and
`dz_copper` and leaves the air's grading as it is. Its small last step made the answer look
converged, but it measured the copper alone. Grading the air twice as finely, at the coarsest copper
mesh, moved L three and a half times as far as the whole ladder did, with about as many nodes as
level 1. Most of a thin trace's inductance is in the field close round it, and with `grade` 0.5 the
elements there
grow from 0.12 mm at the copper's edge to 0.62 mm a millimetre away (the size is `h_edge` +
`grade` × distance); the tetrahedra above and below grow by `tet_grade` per mm of height in the same way. R did
not move, since it depends on the copper's mesh alone, and the circuit's L and the field energy's
still agreed. The board under the copper is not meshed apart from the air: a board or mask part that
lies wholly outside the copper's heights is merged into it
([Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md#1919-section-the-parts-into-slabs)), so the air's grading
covers it too.

![E01's mesh at level 0.75, cut through the loop's axis, 4 mm by 4 mm round one crossing of the trace. Left, the examples' grading (grade 0.5, tet_grade 0.7; 59,782 nodes, L 3.7 % low): the tetrahedra above and below the thin band of wedges grow to about a millimetre within a millimetre of the copper. Right, twice as fine (grade 0.25, tet_grade 0.35; 88,760 nodes, L 1.55 % low): the elements stay smaller round the trace](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Accuracy/E01_circular_loop/elmeraccuracy_1_air_mesh.webp)

On E02 the same change raised M by 2.3 % as well, from 3.3 % to 1.1 % under Maxwell's formula: the
air holds L and M down alike. Graded four times as finely, the air brings E01's L to 0.46 % under the
reference, with 166,471 nodes. Each halving of the grading halved the change, so the air's mesh is
converging but not done, and the copper's ladder showed another +0.7 % from level 0.75 to 1.3; the
domain holds L down by about 0.3 % more. Against that stands the reference's own band, from 0 to
+0.8 %: what is left is of the same size, and E01 cannot measure it. A ladder that refines the air
with the copper is the fix this points to; it is not yet in the bridge
([Future Upgrades And Planning](Future-Upgrades-And-Planning.md)).

## 22.1.2 The Iterative Solve

At 10 kHz the BiCGStab(l) solve reaches a relative residual of about 1e-6 within 1500 iterations and
stalls there: the conduction term jωσ is too small, next to the curl-curl term, to steady the system
without a gauge. At 3.5 MHz the same case converges to 1e-7 in under 1200 iterations. The bridge
caps the iterations (`max_iter`) and lets the run go on (`Linear System Abort Not Converged =
False`), so a 10 kHz answer carries an iteration error:

![The linear solver's relative residual against its iterations, on a log scale: at 10 kHz all three levels fall to between 5e-7 and 3e-6 within about 1500 iterations and stall there until the cap of 3000; at 3.5 MHz level 1 falls below the 1e-7 tolerance at 864 iterations](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Board-Results/E01_circular_loop/elmerresults_2_residual.webp)

The linear solver's residual on E01, 15 and 16 November.

| E01, level 1, 10 kHz | 1500 iterations | 3000 iterations | Change |
|---|---|---|---|
| L from the circuit | 54.11 nH | 54.20 nH | +0.17 % |
| L from the field's energy | 54.15 nH | 54.18 nH | +0.05 % |
| R | 61.52 mΩ | 61.53 mΩ | +0.01 % |
| The residual at the end | 1.5e-6 | 1.3e-6 | |

The iteration error is of the same size as the change from level 1 to 1.3, so the three levels do
not follow one power of the mesh size, and no value extrapolated to a zero mesh size is quoted.
R settles first, the field's energy next, the circuit's voltage last. At 3.5 MHz, where the solve
converges, none of this applies.

The bridge has moved on since these runs. Its README says that with the coils' scalar potentials
left out (the default today) and GCR with the shifted ILU(1), E01 converges to 1e-10 in 400
iterations; E01's committed results are still those of the older solve above. On the coil board at
3.5 MHz the iterative solve no longer stalls but converges too slowly to read M, so the coil board
uses the direct solve, which has no iteration error at all.

## 22.1.3 What The Bridge Leaves Out

| What | In the bridge | What it does to the numbers |
|---|---|---|
| Displacement current | none: the magneto-quasi-static A-V formulation | no capacitance between turns and no self resonance; the answer holds only well below the coil's self resonance, which another solver has to find ([Solvers Comparison](Solvers-Comparison.md)) |
| The insulators | FR-4, solder mask and air are all μr 1, σ 0 | right for the magnetic field; εr plays no part without displacement current |
| The copper's conductivity | 5.8 × 10⁷ S/m, one value for all copper | copper at 20 °C; R rises about 0.4 % per kelvin above that, which the bridge does not follow |
| The copper's shape | KESE's solids, extruded straight through the board: a 2.5D mesh | the etched trapezoid and the copper's roughness are not in the mesh |
| The terminals | two electrodes on the gap's faces and a sheet across the gap | the gap's own short piece of current path is not counted; E01's reference accounts for it with the open-loop share. On the coil board each receiver's 0.2 mm cut is made in the model only: the real board's leads to the IC are not in it |

## 22.1.4 The Coil Board

S0d2_1x_OD23_2L_tiny_TX3top_Cut has no textbook answer, so its accuracy rests on what E01 and E02
measured and on checks inside its own runs:

| Source | On the coil board | What it does to the numbers |
|---|---|---|
| The linear solve | direct (MUMPS) on every solve | no iteration error |
| The two readings of the TX | L from its voltage against L from the field energy, R from its voltage against R from the eddy power | within 0.004 % on all 81 solves, where 1 % is allowed: the ports and the circuit read back what the field holds |
| The copper's mesh | level 0.25 only, on every gap; not refined on this board | not measured here |
| The air's mesh | the examples' grading (`grade` 0.5, `tet_grade` 0.7) | on E01 and E02 it held L and M about 3 % low; the same is likely here, so L TX and M are lower bounds |
| A mesh per angle | every angle gets its own mesh, so the stator's mesh differs a little from angle to angle | the second half turn repeats the first: at six of eight angles M is the same to the last digit, at 225° and 315° within 0.03 nH, against a 4.51 nH amplitude at 1 mm |
| The angle error | SIN and COS each fitted with a sine, offset and gain calibrated out | an error that scales SIN and COS alike leaves it as it is; mesh noise between angles adds to it |

## 22.1.5 What To Trust

| Quantity | On boards like E01 and E02 |
|---|---|
| L and M at 10 kHz | 3 to 4 % low with the examples' air grading; 0.46 % low on E01 with the air graded four times as finely, of the size of the reference's own uncertainty; rising with every refinement: a lower bound |
| L and M at 3.5 MHz | the same mesh error; the iterative solve converges, so no iteration error on top |
| R at 10 kHz | within 0.5 % |
| R at 3.5 MHz, skin and proximity effect | no exact reference, and not yet settled with the mesh: it fell 1.2 % from level 0.75 to level 1; the change against 10 kHz (+29 %) and the RX's share on E02 (+1.5 mΩ) behave as they should |
| L from the circuit against L from the energy | within 0.05 %: a check on every run, at no cost |

| Quantity | On the coil board |
|---|---|
| The shape of SIN and COS, their match and their phase | equal within 0.06 %, 90.06 to 90.18° apart; the angle error of 0.2 to 0.9° rms (electrical) includes the mesh's noise between angles |
| M and L TX | lower bounds, probably by a few percent, from the air's mesh as on E01 and E02 |
| How much the rotor lowers L TX | a ratio of two L values on like meshes; errors that lower both alike may largely cancel, but that is not shown yet |
| R TX | the DC value, 0.377 Ω, against the generator's 0.38 Ω; at 3.5 MHz level 0.25 allows wedge layers up to 72 µm, so each 35 µm foil gets a single layer, where E01 at level 1 has two, and the skin effect is only coarsely resolved |

A ladder that refines the air with the copper, run on the coil board with two air gradings, is the
next check these numbers need ([Future Upgrades And Planning](Future-Upgrades-And-Planning.md)).

| Previous | Next |
|:---|---:|
| [Accuracy](Accuracy.md) | [PyPEEC Accuracy](PyPEEC-Accuracy.md) |
