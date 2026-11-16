# 30. Elmer FEM Accuracy

Where the Elmer bridge's errors come from, how big each one measured on E01 and E02, and what the
bridge leaves out of the physics. Every number here is from the runs on the `Elmer_Integration`
branch (`Examples/E01_circular_loop/results*.json`, `Examples/E02_coaxial_loops/results.json`).

## 30.1 The Error Budget On E01

Each line changes one thing and keeps the rest; all are L at 10 kHz.

| Source | Test | Effect on L |
|---|---|---|
| The copper's mesh | level 0.75 → 1 → 1.3 (59,782, 85,712, 125,043 nodes) | +0.54 %, then +0.12 % |
| The iterative solve | level 1 at 1500 and at 3000 iterations | +0.17 % with the doubled cap |
| The air's mesh | level 0.75 with the air graded twice as finely (`grade` 0.25, `tet_grade` 0.35) | GRADE_EFFECT |
| The air domain | level 0.75 in a domain twice as big (120 mm instead of 60) | DOMAIN_EFFECT |
| The reference's open-loop share | the gap is 1.1 % of the circle; the share is a first-order estimate | a small part of the 1.1 %, either way |
| **Elmer against the reference** | Grover's ring formula with the trace's GMD | **−3.1 % at level 1.3** |

ACCURACY_READING

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
| L and M at 10 kHz | 3 to 4 % low at the meshes this machine can hold, rising with the mesh: a lower bound |
| L and M at 3.5 MHz | the same mesh error; the iterative solve converges, so no iteration error on top |
| R at 10 kHz | within 0.5 % |
| R at 3.5 MHz, skin and proximity effect | no exact reference; the change against 10 kHz (+29 %) and the RX's share on E02 (+1.5 mΩ) behave as they should |
| L from the circuit against L from the energy | within 0.05 %: a check on every run, at no cost |

The coil boards' most important number, C2, is a ratio: how much the rotor lowers the TX's L. Errors
that lower L and M alike may largely cancel in such a ratio, but that is not shown yet; the first coil
board to run should be run at two mesh levels to show it.

| Previous | Next |
|:---|---:|
| [Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md) | [Elmer FEM Hardware](Elmer-FEM-Hardware.md) |
