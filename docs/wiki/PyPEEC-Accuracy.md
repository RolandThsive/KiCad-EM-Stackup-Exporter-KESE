# 49. PyPEEC Accuracy

Where the PyPEEC bridge's errors come from, how big each one measured on E01, E02 and the coil board,
and what the bridge leaves out of the physics. Every number here is from the runs on the
`PyPEEC_Integration` branch (`Examples/E01_circular_loop/results*.json`,
`Examples/E02_coaxial_loops/results.json`, and the coil board's `Results/`).

## 49.1 The Error Budget On E01

Each line changes one thing and keeps the rest.

| Source | Test | Effect |
|---|---|---|
| The voxels in the plane | 100 → 50 → 25 → 12.5 µm | L at 10 kHz: 57.00, 56.59, 56.24, 56.09 nH, each step about half the one before. R at 10 kHz: 69.25, 65.23, 63.20, 62.30 mΩ, its excess over the reference halving with each step: first order |
| The voxels through the copper | 25 µm with two voxel layers of 17.5 µm instead of one of 35 µm (`--n-cu 2`) | nothing moves: L 56.236 against 56.234 nH, R 63.200 mΩ both, at both frequencies |
| The iterative solve | one GMRES iteration, residual 1e-10 at 10 kHz and below 1e-8 at 3.5 MHz | none measurable |
| The terminals and the read-back | L and R from the terminals' voltage, against the stored energy and the losses | the same to the last digit at every voxel size |
| The air | none: PyPEEC needs no air box and no outer boundary | none |
| The reference's open-loop share | the reference ends the current at the round ends' centres (55.99 nH); taken on to the gap's faces it gives 56.44 nH | the reference is a band, 0.8 % wide |
| **PyPEEC against the reference** | L inside the band from 25 µm on; R 1.8 % over the annular sector at 12.5 µm | **L's limit about 55.9 to 56.0 nH, the band's lower end; R's limit 61.4 mΩ, 0.3 % over the sector, which the two half-discs past the sector's ends add** |

Almost all of the error is the voxels in the plane. A voxel is copper when its centre is in the trace,
so the trace's round edges are drawn as steps and its width is right only on average; R follows the
width directly, which is why it settles more slowly than L. Two layers through the copper change
nothing on a lone trace: it is the same above and below its middle, so its two halves carry the same
current whatever the frequency, and the current's drift towards the surfaces would take three layers
or more to show.

## 49.2 E02: The Mutual Inductance

| Quantity | 100 µm | 50 µm | Reference |
|---|---|---|---|
| M at 10 kHz | 24.01 nH (−0.51 %) | 24.09 nH (−0.17 %) | 24.13 nH |
| TX's L beside the open RX, 10 kHz | 57.00 nH | 56.60 nH (+0.01 % on E01's) | E01's at the same voxels |

M's error fell by two thirds when the voxels halved, so its limit is at or a little over 24.13 nH.
The reference carries the same open-loop share as E01's, uncertain by up to 0.8 %, so this board
cannot tell PyPEEC's M from it more finely than that. The open RX leaves the TX's L and R alone at
10 kHz to 0.01 %, as an open loop must. At 3.5 MHz the RX's eddy currents add 0.8 % to the TX's R:
the proximity effect, which the voxels across the RX's trace resolve.

## 49.3 The Coil Board

S0d2_1x_OD23_2L_tiny_TX3top_Cut has no exact reference, so its accuracy is read from its own checks
and symmetries:

| Check | What it shows | Measured |
|---|---|---|
| L and R from the TX's voltage, against the stored energy and the losses | the terminals and the read-back, on every solve | within 0.001 % on all 81 solves (1 % is allowed) |
| The second half turn against the first | the rotor's two sectors, turned by 180°, fall on the very same voxels | the same M, to the last digit, at every angle |
| SIN against COS | equal swings a quarter period apart, as the board is drawn | within 0.4 % in amplitude, 89.9° to 90.1° apart |
| The voxel size | the branch's voxel study on a coil board of the same size ([`Examples/Inductive Coils/README.md`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/PyPEEC_Integration/Examples/Inductive%20Coils/README.md)) | 50 µm reads M and L TX to about half a percent; R TX reads at least 5 % high, still falling at 25 µm |
| The generator's estimate | the TX's L with the rotor away, by a separate method | 296.4 nH against 292 nH, +1.5 % |
| The iterative solve | GMRES on each solve | 2 to 4 iterations, residuals 4e-8 to 3e-7, PyPEEC's own checks passed |

Every angle gets its own voxels: the rotor's copper at that angle is drawn onto the grid, which stays
where the stator is. The rotor's edges then fall on the voxels a little differently at each angle,
which shows as small noise on the curves; each gap's best sine fit says how much (at 1 mm, 0.025 nH rms
left on SIN, 0.018 nH on COS, against swings of 4.6 nH).

## 49.4 What The Bridge Leaves Out

| What | In the bridge | What it does to the numbers |
|---|---|---|
| Capacitance | none: PyPEEC has no charges on the surfaces | no capacitance between turns and no self-resonance; the answer holds only well below the coil's self-resonance |
| The insulators | FR-4, solder mask and air are all μr 1 and carry no voxels | right for the magnetic field of a magneto-quasi-static solve |
| The copper's conductivity | 5.8 × 10⁷ S/m, one value for all copper | copper at 20 °C; no temperature |
| The current through the copper's thickness | one voxel layer (`n_cu` 1): uniform through each sheet | the skin effect through the 35 µm copper, whose skin depth at 3.5 MHz is about the same, is not resolved; the crowding to the traces' edges is, as far as the voxels across a trace allow. Two layers changed nothing on E01 |
| The copper's shape | KESE's solids on a uniform grid; a trace's edges drawn as steps, a via's barrel as a solid column of its outer diameter | a 0.2 mm trace is 4 voxels across at 50 µm; the etched trapezoid and the copper's roughness are not drawn |
| The board's shape | layered, flat at a few heights | a board over another works (the rotor over the stator); a part tilted out of the board's plane does not |
| The terminals | the coil's voxels on the two faces of its gap, held as one potential each | the gap's own short piece of current path is not counted; E01's reference accounts for it with the open-loop share |

## 49.5 What To Trust

| Quantity | On boards like these |
|---|---|
| L at 10 kHz | inside the reference's band from 25 µm voxels on (E01); +1.1 % at 50 µm, settling from above |
| M | 0.17 % under Maxwell's formula at 50 µm (E02), rising towards it |
| R at 10 kHz | high by about the voxels' step error: +6.6 % at 50 µm, +1.8 % at 12.5 µm (E01); first order, so a ladder of two sizes gives the limit |
| R at 3.5 MHz | edge crowding resolved across the width only; no exact reference |
| SIN, COS and the angle error on the coil board | M to about half a percent at 50 µm; SIN and COS match within 0.4 % and sit 90° apart; the angle error is the board's own, measured against the solves' best sine |
| L from the terminals against L from the energy | the same to the last digit, or within 0.001 %: a check on every run, at no cost |

| Previous | Next |
|:---|---:|
| [PyPEEC Test Board Results](PyPEEC-Test-Board-Results.md) | [PyPEEC Hardware](PyPEEC-Hardware.md) |
