# Things to test in ELMER

This file is the brief for building and using the **KESE -> Elmer bridge**. It is written so it can be given as-is
to the project's AI or to a person who has not seen the rest of the pack. Everything needed is in this zip:
the boards, a machine-readable `test_spec.json` per board, and the expected numbers.

## 0. The short version

* The product: an inductive angle encoder on a PCB. A **stator** board carries one TX coil and two RX coils
  (SIN, COS) per coil set; single boards have one set, dual boards two (set 1 inner, set 2 outer). A **rotor** board
  with copper sectors sits 1.0 mm above it. The TX is driven at 3 ... 5 MHz; the rotor's eddy currents modulate the
  TX -> RX coupling, and the two RX voltages follow sin and cos of the rotor angle.
* At 3 ... 5 MHz the boards are about 1/2000 of a wavelength across: the physics is **magneto-quasi-static**.
  Elmer's time-harmonic A-V solver with edge elements (WhitneyAVHarmonicSolver) is the right tool and is the
  **main solver** of the project: TX inductance and resistance, the rotor's effect, the TX -> RX coupling vs angle,
  dual-set crosstalk, and the rotor loss.
* KESE turns `Stator.kicad_pcb` and `Rotor.kicad_pcb` into an accurate 3-D model. The bridge turns it into a Gmsh mesh
  with named bodies and boundaries and an Elmer `.sif` per run, runs ElmerSolver, and reads L, R and M.
* **KESE must build both boards with solder mask on: the stator AND the rotor** (section 2.3).
* The most important single result: **how much the rotor lowers the TX inductance** (C2). Two models disagree by a
  factor of 3 (2 ... 7 % vs 12 ... 21 %). Elmer settles it.
* What Elmer does not give: the coils' self resonance and stray capacitance (an eddy-current solve has no displacement
  current). That is openEMS's job ("Things to test in OpenEMS.md", C8).

## 1. What is in the zip, and what the bridge reads

```
Things to test in ELMER.md            this file
Things to test in OpenEMS.md          the brief for the openEMS bridge
README.md                             index of the pack
boards/<board>/
  Stator.kicad_pcb, Rotor.kicad_pcb   the input to KESE (KiCad 7 format)
  test_spec.json                      what the bridge needs, machine readable (section 3)
  Parameters.txt                      the generator's full record (where test_spec.json got its numbers)
  expected_results.json               every predicted number, with the coupling curves vs rotor angle
  expected_coupling.png, *_stator_and_rotor.png, README.md (the board card)
tools/
  quasistatic_reference.py            the script that made expected_results.json (an independent method:
                                      Neumann integrals + a thin-sheet eddy-current solver for the rotor)
  kicad_to_openems.py                 the openEMS converter (its geometry parser is reusable)
SOLVER_VALIDATION_GUIDE.md            the long background document (physics, method, sources)
```

The ten boards, in the order to bring the bridge up (smallest mesh first):

| Board | Set(s) | OD / bore (mm) | Layers, board | Why it is in the pack |
|---|---|---|---|---|
| S2_4x_OD40_2L_small | 4x | 40 / 20 | 2, 1.6 mm | the smallest single board: **start here** |
| S1_1x_OD54_2L_baseline | 1x | 54 / 30 | 2, 1.6 mm | the generator's default; simplest geometry; used for the mesh study |
| D2_1x8x_OD40_small | 1x + 8x | 40 / 10 | 4, 1.6 mm | the smallest dual board |
| S3_8x_OD59_4L_series_wideband | 8x | 59 / 22 | 4, 1.6 mm | TX on inner layers, series TX |
| S4_16x_OD54_2L_fingers | 16x | 54 / 30 | 2, 1.6 mm | finest pitch, bridging fingers |
| S5_4x_OD98_cosine_r_2subcoils_spiralTX | 4x | 98 / 58 | 2, 1.6 mm | biggest board, spiral TX |
| D1_1x16x_OD54_Renesas_R145_size | 1x + 16x | 54 / 15 | 4, 3.2 mm | the dual default, thick board |
| D3_1x16x_OD59_fitted_bands | 1x + 16x | 59 / 17 | 4, 1.6 mm | typical dual |
| D4_2x8x_OD59_parallel_TX | 2x + 8x | 59 / 17 | 4, 1.6 mm | parallel TX wiring |
| D5_1x16x_OD74_ID40_large | 1x + 16x | 74 / 40 | 4, 1.6 mm | large thin ring |

The 16x boards have 9,000 ... 15,000 trace segments; their meshes are the big ones.

## 2. What the KESE model must contain for Elmer

### 2.1 Coordinates and placement (same in both bridges)

* Origin on the rotation axis = KiCad point (100, 100). **KiCad's y axis points down**: a model with y up uses
  y_model = -(y_kicad - 100). That flips every rotation sense; say in the bridge which convention it uses.
* z up, from the stator towards the rotor. **The top face of the stator's F.Cu copper is z = 0**; the stator
  is below (negative z). Layer z values per board: `test_spec.json` -> `stator.layer_z_mm`.
* The rotor: `Rotor.kicad_pcb` **as drawn, not mirrored**, copper side facing down towards the stator, its copper face
  at z = +air gap (1.0 mm), its 1.6 mm FR-4 above. The air gap is measured copper to copper.
* Rotor angle theta: turn the rotor about the axis by (x, y) -> (x cos t - y sin t, x sin t + y cos t) in KiCad
  coordinates. theta = 0 is the rotor exactly as drawn. One model (one mesh) per angle; the expected curves use the same convention.

### 2.2 Named solids -> Gmsh physical groups -> Elmer bodies

| Solid | Material | Notes |
|---|---|---|
| `TX` (single) or `TX_1`, `TX_2` (dual) | copper, sigma 5.8e7 S/m, mu_r 1 | each TX net with its vias as one connected solid, cut open at its terminals (2.4) |
| `SIN`, `COS` (single: nets `2`, `1`) or `SIN_1`, `COS_1`, `SIN_2`, `COS_2` | copper | each RX net with its vias as one solid, cut open at its terminal |
| `ROTOR` (all rotor copper), or `ROTOR_1`, `ROTOR_2` per ring | copper | 35 um thick sectors |
| `FR4_STATOR`, `FR4_ROTOR` | sigma 0, mu_r 1 (eps_r 4.4 unused here) | may be merged into the air: non-magnetic, no effect on L or M |
| `MASK_STATOR`, `MASK_ROTOR` | sigma 0, mu_r 1 (eps_r 3.8 unused here) | see 2.3 |
| `AIR` | sigma 0, mu_r 1 | a box or cylinder about 3 x the board radius around everything (`test_spec.json` -> `air_box`) |

Boundaries (physical surface groups): `<NET>_START` and `<NET>_END` for each coil's two terminal faces, and `OUTER`
for the outside of the air box.

### 2.3 Solder mask on both boards (required)

* KESE must build the solder mask on **both faces of the stator and both faces of the rotor**, over all copper and the
  bare FR-4, with no openings (vias tented). No mask is set in these KiCad stackups, so use the typical LPI values in
  `test_spec.json` -> `solder_mask`: **20 um thick, eps_r 3.8, loss tangent 0.02**. If KESE's own stackup gives other
  values, use those and write them into the results.
* The mask lies inside the 1.0 mm gap: air between the two mask faces = 1.0 - 2 x 0.020 = 0.96 mm (over copper).
* In Elmer the mask is a non-conducting, non-magnetic body, so it gives the same L, M and eddy currents as air.
  Keep it in the model anyway: the Elmer model and the openEMS model then come from one and the same KESE export, and
  the geometry is the real board's. Mesh it coarsely; it needs no skin-depth refinement. If it causes meshing trouble
  (thin slivers between traces), it may be merged into the air body in Elmer only, and that must be stated in the results.

### 2.4 Terminals: where each coil is cut

Each coil must be an open conductor with two terminal faces, at the place where the real board gets its leads, so the
model and the board measure the same loop. `test_spec.json` -> `terminals`:

* **TX** ("TX ends"): the two coil ends lie stacked at one (x, y) on two layers (e.g. Top and Bottom, or Top and In2).
  The end faces of the two traces are `TX_START` and `TX_END`.
* **RX** ("RX cut"): cut the F.Cu trace at the given point with a gap of about 0.2 mm. The two cut faces are
  `SIN_START` / `SIN_END` (or COS...).
* **RX on S2 and S4** ("RX via (fallback)"): the generator found no cut spot. Leave the named via out; the two pad faces
  where it was are the terminals.
* D4 (parallel TX): both TX layers start and end at the same terminal pair; the two parallel paths are one solid.

### 2.5 Mesh (Gmsh)

* Skin depth in copper: delta = sqrt(2 / (w mu0 sigma)) = **38 um at 3.0 MHz, 35 um at 3.5 MHz, 32 um at 4.3 MHz**,
  about the copper thickness (35 um). So the current is not uniform across a trace and the rotor sectors are not
  thick compared with delta: the rotor must be meshed as a conducting volume (2.6), with at least 3 elements through
  its 35 um thickness, and about delta / 3 (~12 um) at its surfaces.
* Traces: 2 ... 3 elements across the thickness, element size 0.05 ... 0.1 mm along. Air: size by distance, growing to
  a few mm at the air box.
* Convert: `ElmerGrid 14 2 model.msh -autoclean` (format 14 = Gmsh, 2 = ElmerSolver mesh; `-autoclean` removes
  lower-dimensional leftovers and renumbers bodies and boundaries). Keep the mesh in mm and set `Coordinate Scaling = 1.0e-3`.
* Element order: first-order Whitney elements first; second order (`Element = "n:1 e:2 -quad_face b:2"` style, *to
  check*) only if the mesh study (C0) does not converge.

### 2.6 Rotor model: two options

* **A. Conducting volume (reference)**: the rotor sectors as copper bodies, meshed through the thickness. This is exact
  for a 35 um sheet at these frequencies and is the one to trust.
* **B. Surface impedance (cheaper)**: the rotor copper left out of the mesh and its surface given the impedance
  boundary condition (Models Manual eq. 18.62, E x n = Z_S (H x n) x n, Z_S = (1 + i) / (sigma delta)), keywords
  `Layer Electric Conductivity = 5.8e7` and `Layer Relative Permeability = 1` on the rotor boundaries (*confirmed*,
  Models Manual chapter 18). It assumes the copper is thick compared with delta, which it is not (35 um vs 32 ... 38 um).
  Run it once on S2 against option A and report the difference before using it anywhere else.

## 3. `test_spec.json`: the fields a bridge uses

| Field | Meaning |
|---|---|
| `coordinates` | the axis in KiCad coordinates, the y-down note, the z convention |
| `stator.layers`, `stator.layer_z_mm`, `board_thickness_mm`, `copper_thickness_mm` | the stackup |
| `rotor.rings` | each copper ring of the rotor: r_in, r_out, number of sectors, metal fraction, start angle (rad) |
| `rotor.placement`, `rotor.rotation` | how to place and turn the rotor |
| `air_gap_mm`, `air_gap_definition` | 1.0 mm, copper to copper |
| `solder_mask` | 0.020 mm, eps_r 3.8, tan d 0.02, on both faces of both boards |
| `air_box` | suggested air region |
| `nets` | net name -> role (TX / SIN / COS). Single boards: net `2` = SIN, net `1` = COS |
| `sets` | per coil set: TX, SIN and COS net names, frequency, loop count N, the 8 rotor angles for C4, the second angle for C2 |
| `terminals` | where each coil is cut (2.4), in KiCad and in axis coordinates, with the layers and z |
| `expected` | L (generator and reference, rotor away and with rotor), DC resistance, M0, amplitude, h3, phase, angle error per set |
| `tx_wiring` | D4 only: parallel TX |

## 4. The Elmer setup

Status: keywords marked *confirmed* were read in the Elmer Models Manual (chapters 18 "Computation of Magnetic Fields in
3D", 19 "Circuits and Dynamics", 27 "Coil Solver") or in Elmer's test case `mgdyn_harmonic_wire`. The exact matrix
entries of a circuit definition are not spelled out in the manual: take them from **Elmer CircuitBuilder**
(github.com/ElmerCSC/elmer_circuitbuilder), which writes them, or the examples in github.com/ElmerCSC/elmer-elmag.

### 4.1 Recommended method: every coil a massive circuit component

All coils (TX and RX) are **massive** coil components of the circuit module. The driven TX gets a 1 A current source;
every other coil is left open (its component current fixed at 0). The solve then gives, directly:
* the TX voltage V_TX, so Z_TX = V_TX / I_TX: **L_TX = Im(Z_TX) / w and R_TX = Re(Z_TX)** (with skin and proximity effect and the rotor loss);
* every open coil's voltage V_k = j w M_k I_TX: **M_k = Im(V_k / I_TX) / w** (and Re(V_k / I_TX) should be about 0).

This is the same quantity the real IC measures (open-circuit RX voltage), it needs no field post-processing, and
it handles the cut-open coils naturally through their terminal faces.

```
Header
  Mesh DB "." "mesh"
End

Simulation
  Coordinate System = Cartesian
  Coordinate Scaling = 1.0e-3                ! mesh in mm  (confirmed)
  Simulation Type = Steady
  Steady State Max Iterations = 1
  Angular Frequency = Real 2.199115e7        ! 2 pi x 3.5 MHz single; 1.884956e7 (3.0 MHz) set 1; 2.701770e7 (4.3 MHz) set 2
  Max Output Level = 8                       ! level 8 prints the component results (confirmed, ch. 19)
End

Material 1  ! copper: coils and rotor
  Electric Conductivity = 5.8e7
  Relative Permeability = 1.0
End
Material 2  ! air, FR-4, solder mask
  Electric Conductivity = 0.0
  Relative Permeability = 1.0
End

Component 1                                  ! the driven TX  (confirmed keywords, ch. 19)
  Name = "TX"
  Master Bodies(1) = <TX body id>
  Coil Type = "massive"
End
Component 2                                  ! SIN, open
  Name = "SIN"
  Master Bodies(1) = <SIN body id>
  Coil Type = "massive"
End
Component 3                                  ! COS, open
  ...
End

Boundary Condition 1                         ! TX terminal faces (confirmed in the Coil Solver chapter and the
  Target Boundaries(1) = <TX_START id>       ! Elmer forum example of two coupled coils)
  Coil Start = Logical True
End
Boundary Condition 2
  Target Boundaries(1) = <TX_END id>
  Coil End = Logical True
End
! ... the same pair for every RX coil
Boundary Condition n                         ! outside of the air box
  Target Boundaries(1) = <OUTER id>
  AV re {e} = Real 0                         ! zero tangential A (to check the exact form in mgdyn_harmonic_wire)
  AV im {e} = Real 0
End

Body Force 1
  I_TX_Source re = Real 1.0                  ! 1 A on the driven TX (source name as defined in the circuit)
  I_TX_Source im = Real 0.0
End

Solver 1
  Equation = "Circuits"
  Procedure = "CircuitsAndDynamics" "CircuitsAndDynamicsHarmonic"   ! confirmed, ch. 19
  No Matrix = Logical True
End
Solver 2
  Equation = "MGDynamics"
  Variable = "AV[AV re:1 AV im:1]"
  Procedure = "MagnetoDynamics" "WhitneyAVHarmonicSolver"            ! confirmed
  Export Lagrange Multiplier = Logical True                          ! needed with circuits (confirmed)
  Linear System Symmetric = True
  Linear System Solver = Iterative                                   ! or Direct (MUMPS) for the small boards
  Linear System Iterative Method = BiCGStabl
  Linear System Max Iterations = 3000
  Linear System Convergence Tolerance = 1.0e-8
End
Solver 3
  Equation = "MGDynamicsCalc"
  Procedure = "MagnetoDynamics" "MagnetoDynamicsCalcFields"
  Potential Variable = String "AV"
  Calculate Current Density = Logical True
  Calculate Joule Heating = Logical True     ! rotor loss
  Calculate Magnetic Field Strength = Logical True
End
Solver 4
  Equation = "Circuits Output"
  Procedure = "CircuitsAndDynamics" "CircuitsOutput"                 ! confirmed
End
Solver 5
  Procedure = "SaveData" "SaveScalars"
  Filename = "results.dat"                   ! component voltages and currents, Eddy current power, Magnetic Field Energy
End
```

The circuit (MATC, at the top of the .sif; *confirmed* structure, ch. 19): one circuit with, per component k,
the unknowns `i_component(k)` and `v_component(k)`, plus the source current. The equations to put in:
* TX: i_component(1) = I_TX_Source (a current source in series with the coil). CircuitBuilder's sample of a current
  source in series with one coil writes exactly this as a KCL row in `C.1.B` with `C.1.source.<row> = "I_TX_Source"`.
* each open RX coil k: i_component(k) = 0 (one row each, no source).
* then v_component(1) is the TX voltage and v_component(k) the open-circuit voltage of RX coil k.

Write the MATC block with CircuitBuilder (define the components as massive, the source as a complex current
source, and the RX components unconnected / open) and check the generated rows against these three equations.

Dual boards: all six coils are components; drive TX_1 (at 3.0 MHz) in one solve and TX_2 (at 4.3 MHz) in another.
The open TX of the other set is also a component, so TX_1 -> TX_2 coupling comes for free.

### 4.2 Simpler first step: TX as a source current from the Coil Solver

To get the first numbers before the circuit is working: solve the TX current distribution with the Coil Solver and
impose it as a source (no eddy currents in the TX itself).
* *Confirmed* (ch. 27, and the `CoilSolver2` test): `Procedure = "CoilSolver" "CoilSolver"`, `Desired Coil Current =
  Real 1.0`, `Normalize Coil Current = Logical True`, `Coil Start` / `Coil End` on the terminal faces (an open coil),
  and `Impose Body Force Current = Logical True` in the field solver section (ch. 18).
* Then L_TX = 2 W_m / I^2 from the "Magnetic Field Energy" that the solver saves (I = 1 A peak; check whether Elmer's
  energy is the peak or the time-averaged value for harmonic runs: for time-averaged, L = 4 W_m / I^2).
* M to an RX coil = the line integral of A along the RX coil's centre line (the KiCad segments in order; see
  `chain()` in `tools/quasistatic_reference.py`), divided by I_TX. Close the path across the cut so the integral is
  gauge independent. This needs A as a nodal field (*to check*: the CalcFields option that writes the vector potential);
  otherwise integrate B over a surface spanning the RX coil.
* Use 4.2 only to bring the bridge up; the reported numbers come from 4.1.

### 4.3 Reading the results

| Quantity | From the solve (TX driven with I_TX = 1 A) |
|---|---|
| L_TX | Im(v_component(TX) / I_TX) / w |
| R_TX (AC, with the rotor loss) | Re(v_component(TX) / I_TX) |
| M to RX coil k | Im(v_component(k) / I_TX) / w |
| capacitive / loss part | Re(v_component(k) / I_TX): should be near 0 |
| rotor loss | the Joule heat over the rotor bodies (Calculate Joule Heating), or "Eddy current power"; as a series resistance R_rotor = 2 P / I^2 (peak I) |
| V_RX / V_TX (what the IC sees) | M_k / L_TX(rotor) |
| drop | 1 - L_TX(rotor) / L_TX(away) at the same mesh |

## 5. The tests

Frequencies: single boards 3.5 MHz; dual boards set 1 at 3.0 MHz, set 2 at 4.3 MHz (`sets[].f_Hz`). w = 2 pi f.

### Runs per board

| Run | Rotor | TX driven | Gives |
|---|---|---|---|
| 1 | away (no rotor bodies) | each TX in turn | C1, C3 (C7 offsets on dual boards) |
| 2 ... 9 | at the 8 angles of `sets[].c4_angles_mech_deg` | the set's TX | C2, C4, C5, C6, C10 |
| 10 | at `sets[].c2_second_angle_mech_deg` | the set's TX | C2 angle independence |
| dual | the same for set 2 with its own angles | TX_2 | as above; the TX_1 runs also give C7 |

Single boards: 10 solves. Dual boards: 20. The rotor bodies move between runs; the stator part of the mesh can be kept
identical if the air around the rotor is a separate region meshed per angle (this keeps C2 free of mesh noise).

### The checks

| # | Check | Read | Expected | Pass | If it fails |
|---|---|---|---|---|---|
| C0 | **Mesh study first** (once, S1, run 1 and one rotor angle, three mesh levels) | L_TX, Amp | converged | L and Amp change < 1 % between the two finest | refine the copper surfaces and the rotor first |
| C1 | TX inductance, rotor away | L_TX | `expected.tx.*.L_away_ref_H` (generator agrees within 0.5 %) | within 3 % | look at the terminals and the via solids; an open or shorted turn shows as a large error |
| C2 | TX inductance with the rotor, and the drop | L(rotor) at theta = 0 and the second angle, drop % | **the open question**: reference 2 ... 7 %, generator 12 ... 21 % (the table in section 6) | report the number; the two angles within 0.5 % | the drop decides which rotor model the generator's tank-capacitor and frequency estimates should use |
| C3 | Direct coupling (offset) | M0 per RX coil, rotor away | `expected.coupling.*.M0_no_rotor_H` | M0 / Amp < 3 %, the same sign pattern | an offset larger than predicted, stable under mesh refinement, points at the TX tail / lead area or the RX layer changes |
| C4 | Coupling vs rotor angle | M_SIN(theta), M_COS(theta) at the 8 angles; fit mean + A cos(N theta + phi) + A3 cos(3 N theta + phi3) (a DFT of the 8 values) | `amplitude_H`, `h3_rel`; curves in `expected_results.json` (`coupling` -> `M_total_H` vs `theta_mech_deg`) | A within 15 %, period exactly 360/N, h3 within 2x | an amplitude far off with C1 fine points at the rotor model |
| C5 | SIN / COS match | phi_SIN - phi_COS, A_SIN / A_COS | +/-90.0 deg, 1.000 | 90 +/- 1 deg, 1.00 +/- 0.02 | an asymmetry in the coils (a generator bug) or in the model (ports, rotor placement) |
| C6 | Angle error | atan2(SIN - mean, COS - mean) minus N theta, peak; also without removing the means (raw) | `pairs.*.angle_error_pk_elec_deg` (and `_raw`) | same order of magnitude | follows from C3 ... C5 |
| C7 | Dual crosstalk | TX_1 -> SIN_2 / COS_2, TX_2 -> SIN_1 / COS_1, TX_1 -> TX_2 | crosstalk amplitudes, section 6 | report | a crosstalk far above the prediction is a dual-board design issue |
| C10 | TX AC resistance and rotor loss | R_TX (rotor away and with rotor), rotor Joule loss | R_DC in `expected.tx.*.R_dc_ohm`; the generator says "up to about 2x that" at the operating frequency | report | sets the Q of the TX tank and the drive current the IC needs |

### Optional

* **C9 air gap sweep**: runs 1 ... 9 at gaps of 0.5 and 1.5 mm. Predictions: copy the board folder, change
  `AIR_GAP_MM` in Parameters.txt, run `python tools/quasistatic_reference.py <copy>`. The amplitude falls roughly
  exponentially with gap / pole pitch: steep for 16x, gentle for 1x.
* **C11 tolerances** (S1 and D3): the rotor 0.2 mm off-centre, and tilted 0.3 deg. Report the change of the angle error
  (C6) against the centred case. These are the mounting errors the real product sees.
* **C12 rotor model check**: option B (surface impedance) against option A (meshed copper) on S2 (2.6).

### Calibrate the workflow once (before the boards)

Run Elmer's own `mgdyn_harmonic_wire` test, then the TEAM Problem 7 benchmark (an aluminium plate with an off-centre
hole under a racetrack coil, with published measured fields and eddy currents) with the same mesh rules and solver
settings as the boards. Agreement there makes the board results trustworthy before any hardware exists.

## 6. Expected numbers (quasi-static reference)

L gen = the generator's estimate, L ref = the reference's (rotor away / with rotor); M0 = direct coupling with no rotor;
Amp = rotor-dependent coupling amplitude; V_RX/V_TX = Amp / L ref(rotor); h3 = 3rd harmonic; err = angle error, electrical
degrees, offsets removed (raw). All numbers per board, in H, are in `test_spec.json` -> `expected` and `expected_results.json`.

| Board | Set | L gen away / rotor (uH) | L ref away / rotor (uH) | M0 SIN / COS (nH) | Amp SIN / COS (nH) | V_RX/V_TX (x1e-3) | dphi (deg) | SIN/COS | h3 | err el.deg (raw) |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | TX (1x) | 1.146 / 1.004 (-12.4 %) | 1.149 / 1.101 (-4.1 %) | +0.271 / +0.276 | 16.64 / 16.64 | 15.12 | +90.0 | 1.000 | 1.09 % | 0.66 (1.78) |
| S2 | TX (4x) | 2.311 / 1.883 (-18.5 %) | 2.311 / 2.184 (-5.5 %) | -0.055 / -0.060 | 17.63 / 17.63 | 8.07 | +90.0 | 1.000 | 0.49 % | 0.32 (0.73) |
| S3 | TX (8x) | 4.952 / 3.963 (-20.0 %) | 4.935 / 4.724 (-4.3 %) | +0.004 / -0.004 | 89.25 / 89.25 | 18.89 | +90.0 | 1.000 | 0.46 % | 0.27 (0.28) |
| S4 | TX (16x) | 1.146 / 1.004 (-12.4 %) | 1.149 / 1.129 (-1.7 %) | -0.029 / +0.102 | 10.62 / 10.62 | 9.40 | +90.0 | 1.000 | 0.24 % | 0.23 (0.65) |
| S5 | TX (4x) | 6.197 / 5.032 (-18.8 %) | 6.192 / 5.786 (-6.6 %) | +0.427 / +2.191 | 206.33 / 206.33 | 35.66 | +90.0 | 1.000 | 0.18 % | 0.10 (0.68) |
| D1 | TX_1 (1x) | 2.872 / 2.463 (-14.2 %) | 2.873 / 2.782 (-3.2 %) | +0.096 / +0.054 | 15.83 / 15.83 | 5.69 | +90.0 | 1.000 | 1.86 % | 1.09 (1.67) |
| D1 | TX_2 (16x) | 6.881 / 5.593 (-18.7 %) | 6.878 / 6.647 (-3.4 %) | +0.071 / -0.030 | 60.35 / 60.35 | 9.08 | +90.0 | 1.000 | 0.14 % | 0.09 (0.15) |
| D2 | TX_1 (1x) | 1.463 / 1.214 (-17.0 %) | 1.461 / 1.388 (-5.0 %) | +0.004 / -0.010 | 13.42 / 13.42 | 9.67 | +90.0 | 1.000 | 1.85 % | 1.09 (1.27) |
| D2 | TX_2 (8x) | 1.358 / 1.130 (-16.7 %) | 1.355 / 1.294 (-4.5 %) | +0.029 / -0.005 | 19.04 / 19.04 | 14.72 | +90.0 | 1.000 | 0.29 % | 0.17 (0.24) |
| D3 | TX_1 (1x) | 2.612 / 2.077 (-20.5 %) | 2.609 / 2.426 (-7.0 %) | -0.031 / -0.042 | 37.04 / 37.04 | 15.27 | +90.0 | 1.000 | 2.21 % | 1.33 (1.36) |
| D3 | TX_2 (16x) | 4.702 / 3.721 (-20.9 %) | 4.695 / 4.477 (-4.6 %) | +0.026 / -0.009 | 59.86 / 59.86 | 13.37 | +90.0 | 1.000 | 0.12 % | 0.08 (0.10) |
| D4 | TX_1 (2x) | 0.653 / 0.519 (-20.5 %) | - (parallel TX) | -1.754 / -1.769 | 18.45 / 18.45 | - | +90.0 | 1.000 | 1.85 % | 1.11 (8.22) |
| D4 | TX_2 (8x) | 1.175 / 0.930 (-20.9 %) | - (parallel TX) | -0.864 / -0.885 | 35.13 / 35.13 | - | +90.0 | 1.000 | 0.35 % | 0.21 (2.12) |
| D5 | TX_1 (1x) | 4.284 / 3.774 (-11.9 %) | 4.278 / 4.131 (-3.4 %) | +0.107 / +0.104 | 23.62 / 23.62 | 5.72 | +90.0 | 1.000 | 2.09 % | 1.22 (1.77) |
| D5 | TX_2 (16x) | 6.360 / 5.203 (-18.2 %) | 6.351 / 6.087 (-4.2 %) | +0.027 / -0.012 | 76.52 / 76.52 | 12.57 | +90.0 | 1.000 | 0.22 % | 0.13 (0.15) |

Dual crosstalk (C7), amplitude of each TX into the other set's RX coils (rotor-modulated at the RX coil's own period):
D1 TX_1->set 2 9.51 nH, TX_2->set 1 6.45 nH; D2 8.42 / 4.39 nH; D3 20.87 / 16.29 nH; D4 12.15 / 8.25 nH; D5 34.11 / 9.54 nH.

How exact are these? The TX inductance is a first-principles integral (within 0.5 % of the generator). The rotor model
was checked against exact thin-disc and strip results (1 ... 3 %) but never against a 3-D solver or hardware: that is
why C2 and the C4 amplitudes are the numbers to look at first. The D4 offsets (M0) are the least certain prediction.
The sign of dphi (+90 or -90) depends on the rotation sense and the y convention; either is right if consistent.

## 7. What to report

One CSV per board, one line per solve:

```
board,set,tx,rotor,angle_mech_deg,f_Hz,L_tx_H,R_tx_ohm,M_sin_H,M_cos_H,re_sin_over_itx,re_cos_over_itx,M_other_tx_H,P_rotor_W,mesh_level,n_elements,rotor_model,mask,runtime_s,notes
```

Then per board the C0 ... C7 and C10 results against section 6 with pass / fail, and the KESE version, Elmer version and
mask values used.

## 8. Sources used for the Elmer part

* Elmer Models Manual (CSC): chapter 18 (3-D magnetic fields: WhitneyAVHarmonicSolver, Angular Frequency, surface
  impedance BC 18.62 with Layer Electric Conductivity / Layer Relative Permeability, MagnetoDynamicsCalcFields options,
  Component with Master Bodies, the saved Eddy current power and Magnetic Field Energy), chapter 19 (Circuits and
  Dynamics: massive / stranded / foil coils, CircuitsAndDynamicsHarmonic, No Matrix, Export Lagrange Multiplier,
  Coil Type, the MATC circuit definition, CircuitsOutput), chapter 27 (Coil Solver: Coil Start / Coil End, Desired Coil
  Current, Normalize Coil Current).
* ElmerGrid manual (format 14 -> 2, `-autoclean`, `-scale`).
* Elmer test cases `mgdyn_harmonic_wire`, `CoilSolver1`, `CoilSolver2` (github.com/ElmerCSC/elmerfem, fem/tests).
* Elmer CircuitBuilder README (github.com/ElmerCSC/elmer_circuitbuilder): current source in series with a coil,
  complex sources for harmonic runs, Coil Start / Coil End on the terminals of an open coil.
* Elmer forum, "Model induction between two coils" (elmerfem.org/forum/viewtopic.php?p=30446): Coil Start / Coil End
  boundary conditions for open coils; the Coil Solver is optional.
* Not read: the elmer-elmag example repository (github.com/ElmerCSC/elmer-elmag); check its circuit examples for the
  exact MATC rows of a massive coil before the first run.
