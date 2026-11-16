# 29. Elmer FEM Test Board Results

What Elmer gave on each board of [Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md), against numbers
known without any solver. Every chart and picture here is drawn from Elmer's own output by
`Examples/E01_circular_loop/make_pictures.py`; nothing is drawn by hand. The numbers are in each
example's `results*.json` on the `Elmer_Integration` branch, with the settings, the versions, the
mesh's size, the time, the memory and the solver's last residual of every solve, and each example's
`results.md` has the full tables.

## 29.1 E01 Circular Loop

One circular trace, 10 mm in radius to its centre line, 0.5 mm wide and 35 µm thick, opened by a
0.2 mm gap where the bridge puts its two electrodes. Elmer's circuit drives 1 A through it.

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

## 29.3 The Ten Inductive Encoder Boards

**YET TO BE RUN.** Every coil board needs more memory than the 15 GB test machine has: S2, the
smallest, about 59 GB for its measured mesh, the largest about 240 GB
([Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md#283-the-ten-inductive-encoder-boards),
[Elmer FEM Hardware](Elmer-FEM-Hardware.md#315-the-coil-boards)). They wait for a bigger machine.

| Previous | Next |
|:---|---:|
| [Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md) | [Elmer FEM Accuracy](Elmer-FEM-Accuracy.md) |
