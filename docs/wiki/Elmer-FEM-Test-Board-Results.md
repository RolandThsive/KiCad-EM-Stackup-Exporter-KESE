# 29. Elmer FEM Test Board Results

What Elmer gave on each board of [Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md), against numbers
known without any solver. Every chart and picture here is drawn from Elmer's own output, E01's and
E02's by `Examples/E01_circular_loop/make_pictures.py` and the coil board's by its own
`make_charts.py`; nothing is drawn by hand. The numbers are in each example's results files on the
`Elmer_Integration` branch, with the settings, the versions, the mesh's size, the time and the memory
of every solve; each example's `results.md` (E01, E02) or `Results/SINCOS_Results.md` (the coil
board) has the full tables.

> [!NOTE]
> E01 and E02 ran on 15 and 16 November with the iterative solve (BiCGStab(l)) and `Activate
> Constraint` on, the bridge's settings then. The coil board ran on 17 November with the direct solve
> (MUMPS) and the constraint off, today's default ([Elmer FEM Workflow](Elmer-FEM-Workflow.md#266-write-the-elmer-case)).

## 29.1 E01 Circular Loop

One circular trace, 10 mm in radius to its centre line, 0.5 mm wide and 35 µm thick, opened by a
0.2 mm gap where the bridge puts its two electrodes. Elmer's circuit drives 1 A through it.

### In Short

E01 is one copper loop on a board, the simplest coil there is. Its inductance L (how much magnetic
field 1 A makes, which sets the voltage a changing current induces) and its resistance R have textbook
formulas. Elmer drives 1 A through the loop and reads both back:

| What | What it means | The formula | Elmer |
|---|---|---|---|
| L at 10 kHz | the loop's inductance | 55.99 nH | 54.27 nH on the finest mesh, −3.1 %; −0.46 % with a finer mesh in the air round the copper |
| R at 10 kHz | its resistance, the current spread evenly through the copper | 61.20 mΩ | 61.52 mΩ, +0.5 % |
| R at 3.5 MHz | the current crowds to the trace's edges, so R rises | no exact formula | 79.25 mΩ, 29 % above the 10 kHz value |
| L, two ways | from the circuit's voltage and from the energy of the whole field | the two must agree | within 0.05 % |

The 3 % is the mesh in the air round the copper, not the bridge: a finer air mesh takes L to within
0.5 % of the formula, and the two ways of reading L agree, so the electrodes and Elmer's circuit
measure what the field holds.

| Item | Value |
|---|---|
| Run | 15 and 16 November 2026, Elmer 26.2 (`a19504a`), gmsh 4.15.2, KESE 3.4.0 |
| Solver | `WhitneyAVHarmonicSolver`, first-order edge elements, BiCGStab(l) with the circuit preconditioner, tolerance 1e-7, at most 3000 iterations |
| Mesh | three levels, 59,782 to 125,043 nodes: a level divides the copper's mesh sizes by itself |
| Air | a cylinder 60 mm in radius and 120 mm high round the loop, n × A = 0 on its outside |

### Expected Against What Came Out

| Quantity | Reference | Level 0.75 | Level 1 | Level 1.3 |
|---|---|---|---|---|
| Nodes | | 59,782 | 85,712 | 125,043 |
| L at 10 kHz | 55.99 nH | 53.91 nH (−3.7 %) | 54.20 nH (−3.2 %) | 54.27 nH (−3.1 %) |
| L from the field's energy, 10 kHz | 55.99 nH | 53.91 nH | 54.18 nH | 54.29 nH |
| R at 10 kHz | 61.20 mΩ | 61.53 mΩ (+0.5 %) | 61.53 mΩ (+0.5 %) | 61.52 mΩ (+0.5 %) |
| L at 3.5 MHz | about 55.44 nH (an estimate) | 52.93 nH (−4.5 %) | 53.26 nH (−3.9 %) | |
| R at 3.5 MHz | | 80.19 mΩ | 79.25 mΩ | |

The reference L is Grover's ring formula μ0 R (ln(8R / g) − 2), with the rectangle's geometric mean
distance g = 0.2235 (w + t), times the share of the circle the copper covers (0.989) up to the round
ends' centres; since the current runs on into the half-discs, it is a lower bound, by up to 0.8 %.
The reference R is the annular sector's DC resistance. At 3.5 MHz the skin depth (35 µm) equals the copper's
thickness, and no formula is exact there.

![E01's L and E02's M at 10 kHz, as a percentage off their references, against the mesh's nodes in thousands: E01 rises from −3.7 % at 60,000 nodes to −3.2 % at 86,000 and −3.1 % at 125,000; E02 rises from −3.3 % at 92,000 nodes to −3.1 % at 120,000; E01 with the air graded twice and four times as finely rises from −1.55 % at 89,000 nodes to −0.46 % at 166,000, and E02's M with the air graded twice as finely sits at −1.1 % with 135,000 nodes; E01 in an air domain twice as big sits at −3.5 % with 87,000 nodes; a grey band from 0 to +0.8 % shows the reference's own uncertainty](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Board-Results/elmerresults_1_against_reference.webp)

L rises as the mesh is refined, as it should with first-order edge elements, but along the ladder it
levels off about 3 % under the reference. The ladder refines only the copper's mesh. Grading the air
twice and four times as finely at level 0.75 (the diamonds) brings L to 1.55 % and then 0.46 % under
the reference: the air's mesh round the copper holds most of the gap. The grey band is the
reference's own uncertainty: it ends the current at the round ends' centres, and with the current
taken on to the gap's faces it is 0.8 % higher
([Elmer FEM Accuracy](Elmer-FEM-Accuracy.md#301-the-error-budget-on-e01)). The circuit's L and the
field energy's agree within 0.05 % at every level, so the electrodes, the sheet across the gap and
Elmer's circuit read back the inductance the field holds. R is 0.5 % high, as it should be: the
reference stops at the round ends' centres, and the current also runs through the two half-discs
past them.

![The linear solver's relative residual against its iterations, on a log scale: at 10 kHz all three levels fall to between 5e-7 and 3e-6 within about 1500 iterations and stall there until the cap of 3000; at 3.5 MHz level 1 falls below the 1e-7 tolerance at 864 iterations](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Board-Results/E01_circular_loop/elmerresults_2_residual.webp)

At 10 kHz the conduction term jωσ is too small, next to the curl-curl term, to steady the system,
and the iterative solve stalls; at 3.5 MHz, 350 times higher, it converges. Doubling the cap from 1500 to 3000 iterations moved
level 1's L by 0.17 %, about as much as going from level 1 to 1.3.

![Left: the magnitude of B at 3.5 MHz for 1 A, on a log colour scale from 10 to 1000 µT, in the plane through the loop's axis, with field lines circling the trace's two crossings at y = −110 and −90 mm and threading the loop; 66 µT at the centre. Right: the magnitude of the current density across the trace's 0.5 mm width, halfway through the copper: about 57 A/mm² everywhere at 10 kHz, slightly more at the inner edge; at 3.5 MHz about 153 A/mm² at the inner edge, about 45 in the middle and 87 at the outer edge](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Board-Results/E01_circular_loop/elmerresults_3_fields.webp)

The fields themselves, at level 0.75, read from the VTU files that `simulation.py --fields` writes.
The field circles each crossing of the trace and threads the loop. At the loop's centre it is 66 µT
for 1 A, against μ0 I / 2R = 63 µT for a closed ring: a value at one point, in elements several
millimetres across, where first-order elements hold B constant in each element, so it is a rough
check only; L, from the energy of the whole field, is the bridge's number. Across the trace, the
current at 10 kHz is nearly even and a little denser at the inner edge, as the 1/r of a ring's DC
current gives. At 3.5 MHz it crowds to both edges, most to the inner one, and the middle carries less
than an even share: the edge effect behind R's rise at 3.5 MHz (+29 % at level 1, +30 % at level
0.75). The line follows the level 0.75 triangles, only a few across the width, so its shape is
coarse.

## 29.2 E02 Coaxial Loops

E01's loop twice, TX on F.Cu and RX on B.Cu, 1.565 mm apart. TX carries 1 A, RX is open, so the
voltage across RX's gap gives M. E02 runs at most 1500 iterations.

### In Short

E02 puts a second loop right under the first. A current in the top loop (TX) induces a voltage in
the bottom one (RX), and the ratio is their mutual inductance M: the same coupling that carries the
coil boards' signal from the TX to SIN and COS.

| What | What it means | The formula | Elmer |
|---|---|---|---|
| M at 10 kHz | how strongly the two loops couple | 24.13 nH (Maxwell) | 23.38 nH, −3.1 %; −1.1 % with a finer mesh in the air |
| TX's L beside the open RX | an open loop carries no current, so it must leave L alone | E01's 54.20 nH | 54.18 nH |
| TX's R at 3.5 MHz | eddy currents in the RX trace take a little power from the TX | a little above E01's 79.25 mΩ | 80.75 mΩ |

### Expected Against What Came Out

| Quantity | Reference | Level 0.75 | Level 1 |
|---|---|---|---|
| Nodes | | 92,120 | 119,559 |
| M at 10 kHz | 24.13 nH | 23.33 nH (−3.3 %) | 23.38 nH (−3.1 %) |
| M at 3.5 MHz | 24.13 nH (an estimate) | | 23.32 nH (−3.4 %) |
| TX's L at 10 kHz | E01's L at the same level | 54.06 nH (E01: 53.91 nH) | 54.18 nH (E01: 54.20 nH) |
| TX's R at 3.5 MHz | E01's R at the same level | | 80.75 mΩ (E01: 79.25 mΩ) |

The reference M is Maxwell's formula for two coaxial circular filaments, averaged over 41 × 41
filaments across both traces' widths, times the share of the circle the TX's copper covers: like
E01's, a lower bound by up to 0.8 %.

* **M is 3.1 % low and rises with the mesh** (−3.3 % at level 0.75), the same as E01's L at this mesh
  size, and for the same reason: with the air graded twice as finely, M rose 2.3 % to 1.1 % under the
  reference (the orange diamond), as much as E01's L did.
* **The open RX leaves the TX's L alone** at 10 kHz (54.18 against 54.20 nH): a loop with no current
  in it adds no field.
* **At 3.5 MHz the RX adds 1.5 mΩ to the TX's R.** RX carries no net current, but eddy currents
  circulate across its width and dissipate power that the TX has to supply: the proximity effect. It
  shows also as a real part of the RX's transfer impedance, 0.91 mΩ.

## 29.3 S0d2_1x_OD23_2L_tiny_TX3top_Cut

The whole encoder: the TX carries 1 A at 3.5 MHz, SIN and COS carry none, and the voltage across each
receiver's cut is its open-circuit EMF, given as the mutual inductance M = V / (jωI) (1 nH is 22 mV
of EMF). The rotor is solved at 16 angles over the whole turn, every 22.5° from 0 to 337.5° (two of
its 180° periods), at each of 5 air gaps, and once with the rotor away: 81 solves, each direct
(MUMPS) on its own mesh at level 0.25.

### In Short

The coil board is a real sensor: as the rotor turns, SIN and COS should trace a sine and a cosine,
equal in size and a quarter period apart, and an IC reads the angle from the pair. Elmer turns the
rotor in 22.5° steps and solves each position:

| What | What it means | Elmer |
|---|---|---|
| SIN and COS amplitude | the signal the IC gets | 9.44 nH (208 mV) at a 0.1 mm gap, 4.51 nH (99 mV) at 1 mm, 1.86 nH (41 mV) at 2 mm |
| SIN against COS | must be equal and 90° apart | equal within 0.06 %, 90.06 to 90.18° apart at every gap |
| Angle error | how far the angle read from SIN and COS is from the true one | 0.2° rms (electrical) from 1 to 2 mm, 0.4° at 0.5 mm, 0.9° at 0.1 mm; half that in mechanical degrees |
| TX's L | lowered by the rotor's eddy currents | 274.2 nH with the rotor away; 250.0 to 250.6 nH at 1 mm |
| The two checks | the TX's L and R read two ways must agree | within 0.004 % on every solve, where 1 % is allowed: 81 of 81 pass |

### SIN And COS Against The Rotor Angle

![SIN (blue) and COS (orange) against the rotor angle at a 1 mm air gap, 0 to 360 degrees, mesh level 0.25: the mutual inductance from the TX, one dot per Elmer solve joined by a solid line, with each channel's best sine fit dotted. Both swing between about -4.5 and +4.5 nH with two full periods over the turn, COS leading SIN by a quarter period; the dots sit on the dotted curves](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Board-Results/S0d2_1x_OD23_2L_tiny_TX3top_Cut/elmerresults_1_gap1mm.webp)

At 1 mm, the default gap, SIN and COS are close to a sine and a cosine: best sine fits of 4.511 and
4.514 nH, with offsets of 0.100 and 0.020 nH, 90.09° apart. The second half turn repeats the first:
at six of its eight angles each solve gives the same M, to the last digit, as the one 180° before it,
and at 225° and 315°, where the 2D mesh comes out a few triangles different, it is within 0.03 nH.

| Air gap | Amplitude SIN / COS | Angle error (electrical) | Solves passing both checks | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 1.86 / 1.86 nH (41 / 41 mV) | 0.2° rms, 0.4° peak | 16 of 16 | 262.4 to 262.8 nH |
| 1.5 mm | 2.88 / 2.88 nH (63 / 63 mV) | 0.2° rms, 0.4° peak | 16 of 16 | 257.6 to 258.1 nH |
| 1 mm | 4.51 / 4.51 nH (99 / 99 mV) | 0.2° rms, 0.4° peak | 16 of 16 | 250.0 to 250.6 nH |
| 0.5 mm | 6.97 / 6.98 nH (153 / 153 mV) | 0.4° rms, 0.6° peak | 16 of 16 | 236.3 to 237.0 nH |
| 0.1 mm | 9.44 / 9.44 nH (208 / 208 mV) | 0.9° rms, 1.2° peak | 16 of 16 | 213.1 to 214.2 nH |

### Every Air Gap

![SIN at each air gap, 0.1, 0.5, 1, 1.5 and 2 mm, against the rotor angle from 0 to 360 degrees, one colour per gap: each a two-period sine, its amplitude falling from about 9.4 nH at 0.1 mm to about 1.9 nH at 2 mm, the solves joined by solid lines and each gap's best sine fit dotted. Below, the solves minus the fit: within about 0.03 nH at 1 to 2 mm, within about 0.07 nH at 0.5 mm, and at 0.1 mm a ripple of about ±0.1 to 0.2 nH that changes sign from one angle to the next](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Board-Results/S0d2_1x_OD23_2L_tiny_TX3top_Cut/elmerresults_2_gaps_SIN.webp)

The signal grows 5.08 times from a 2 mm to a 0.1 mm gap. The lower panel shows what the angle error
is made of: at 0.1 mm the solves alternate about the fit from one angle to the next, a ripple at four
periods per electrical period, the fastest that eight angles a period can show, which fades with the
gap faster than the sine. [COS at each gap](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Board-Results/S0d2_1x_OD23_2L_tiny_TX3top_Cut/elmerresults_3_gaps_COS.webp) is the same picture a
quarter period on.

### How The Angle Error Is Worked Out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase).
Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and
+1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS);
the error at each angle is that reading less the true angle, less the average of all of them, since a
fixed offset only moves where zero is. The rms and the worst of them are the angle error, in
electrical degrees; with two periods per turn, a mechanical degree is two electrical ones.

### The TX And The Rotor

| Quantity | Generator's estimate | Elmer |
|---|---|---|
| L TX, rotor away | 292 nH | 274.2 nH |
| L TX, rotor at 1 mm | 226 nH (its drop with the rotor is an upper estimate) | 250.0 to 250.6 nH |
| L TX, rotor at 0.1 mm | | 213.1 to 214.2 nH |
| R TX at DC | 0.38 Ω | 0.377 Ω (Elmer's DC solve of the current's direction) |
| R TX at 3.5 MHz, rotor away | | 437.6 mΩ |
| R TX at 3.5 MHz, rotor at 2 mm and at 0.1 mm | | 449 to 450 mΩ, and 507 to 512 mΩ |

The rotor lowers the TX's L by about 4.2 % at 2 mm, 8.7 % at 1 mm and 22 % at 0.1 mm against the rotor
away (worked out from the table), and L TX moves by 1.1 nH at most over a turn. The TX's R rises as
the rotor comes closer: the power the rotor's eddy currents take shows as resistance in the TX.

> [!NOTE]
> These are on the coarse mesh, level 0.25, on which a direct solve runs on a 16 GB machine with a swap file,
> and the level was not refined on this board. On the proof boards the air's mesh held L and M about
> 3 % low with the examples' grading ([Elmer FEM Accuracy](Elmer-FEM-Accuracy.md#301-the-error-budget-on-e01)),
> so the coil board's L TX and M are best read as lower bounds. The angle error is worked out after
> each channel's gain is calibrated out, so an error that scales SIN and COS alike leaves it as it is.

| Previous | Next |
|:---|---:|
| [Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md) | [Elmer FEM Accuracy](Elmer-FEM-Accuracy.md) |
