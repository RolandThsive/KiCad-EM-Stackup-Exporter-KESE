# 30. Elmer FEM Accuracy

Where the Elmer bridge's errors come from, how big each one measured on E01 and E02, and what the
bridge leaves out of the physics. Every number here is from the runs on the `Elmer_Integration`
branch (`Examples/E01_circular_loop/results*.json`, `Examples/E02_coaxial_loops/results*.json`).

## 30.1 The Error Budget On E01

Each line changes one thing and keeps the rest; all are L at 10 kHz.

| Source | Test | Effect on L |
|---|---|---|
| The copper's mesh | level 0.75 → 1 → 1.3 (59,782, 85,712, 125,043 nodes) | +0.54 %, then +0.12 % |
| The iterative solve | level 1 at 1500 and at 3000 iterations | +0.17 % with the doubled cap |
| The air's mesh | level 0.75 with the air graded twice as finely (`grade` 0.25, `tet_grade` 0.35; 88,760 nodes against 59,782), then four times (0.125 and 0.175; 166,471 nodes) | **+2.3 %, then +1.1 %** |
| The air domain | level 0.75 in a domain twice as big (120 mm in radius and half height instead of 60) | +0.26 %: the 60 mm domain holds L down by about 0.3 %, since the bigger one keeps about an eighth of that |
| The reference's open-loop share | with the sheet across the gap, the coil's voltage is the flux through the whole circle, so L is the closed ring's L times the share of the circle the current runs in; the reference ends that share at the round ends' centres, but the current runs on into the half-discs | the reference is a lower bound: up to 0.8 % higher (56.44 nH) with the current taken on to the gap's faces |
| **Elmer against the reference** | Grover's ring formula with the trace's GMD | **−3.1 % at level 1.3; −0.46 % at level 0.75 with the air four times as fine** |

The ladder in the first line refines only the copper's mesh: a level divides `h_edge`, `h_in` and
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
([Elmer FEM Workflow](Elmer-FEM-Workflow.md#262-section-the-parts-into-slabs)), so the air's grading
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

## 30.2 The Iterative Solve

At 10 kHz the BiCGStab(l) solve reaches a relative residual of about 1e-6 within 1500 iterations and
stalls there: the conduction term jωσ is too small, next to the curl-curl term, to steady the system
without a gauge. At 3.5 MHz the same case converges to 1e-7 in under 1200 iterations. The bridge
caps the iterations (`max_iter`) and lets the run go on (`Linear System Abort Not Converged =
False`), so a 10 kHz answer carries an iteration error:

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

## 30.3 What The Bridge Leaves Out

| What | In the bridge | What it does to the numbers |
|---|---|---|
| Displacement current | none: the magneto-quasi-static A-V formulation | no capacitance between turns and no self resonance; the answer holds only well below the coil's self resonance, which openEMS finds ([Elmer vs openEMS](Elmer-vs-OpenEMS.md#423-which-one-for-what)) |
| The insulators | FR-4, solder mask and air are all μr 1, σ 0 | right for the magnetic field; εr plays no part without displacement current |
| The copper's conductivity | 5.8 × 10⁷ S/m, one value for all copper | copper at 20 °C; R rises about 0.4 % per kelvin above that, which the bridge does not follow |
| The copper's shape | KESE's solids, extruded straight through the board: a 2.5D mesh | the etched trapezoid and the copper's roughness are not in the mesh |
| The terminals | two electrodes on the gap's faces and a sheet across the gap | the gap's own short piece of current path is not counted; E01's reference accounts for it with the open-loop share |

## 30.4 What To Trust

| Quantity | On boards like E01 and E02 |
|---|---|
| L and M at 10 kHz | 3 to 4 % low with the examples' air grading; 0.46 % low on E01 with the air graded four times as finely, of the size of the reference's own uncertainty; rising with every refinement: a lower bound |
| L and M at 3.5 MHz | the same mesh error; the iterative solve converges, so no iteration error on top |
| R at 10 kHz | within 0.5 % |
| R at 3.5 MHz, skin and proximity effect | no exact reference, and not yet settled with the mesh: it fell 1.2 % from level 0.75 to level 1; the change against 10 kHz (+29 %) and the RX's share on E02 (+1.5 mΩ) behave as they should |
| L from the circuit against L from the energy | within 0.05 %: a check on every run, at no cost |

The coil boards' most important number, C2, is a ratio: how much the rotor lowers the TX's L. Errors
that lower L and M alike may largely cancel in such a ratio, but that is not shown yet; the first coil
board to run should be run with two air gradings as well as two mesh levels to show it.

| Previous | Next |
|:---|---:|
| [Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md) | [Elmer FEM Hardware](Elmer-FEM-Hardware.md) |
