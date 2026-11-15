# Things to test in OpenEMS

This file is the brief for building and using the **KESE -> openEMS bridge**. It is written so it can be given as-is
to the project's AI or to a person who has not seen the rest of the pack. Everything needed is in this zip:
the boards, a machine-readable `test_spec.json` per board, and the expected numbers.

## 0. The short version

* The product: an inductive angle encoder on a PCB. A **stator** board carries one TX coil and two RX coils
  (SIN, COS) per coil set; single boards have one set, dual boards two (set 1 inner, set 2 outer). A **rotor** board
  with copper sectors sits 1.0 mm above it. The TX is driven at 3 ... 5 MHz; the rotor's eddy currents modulate the
  TX -> RX coupling, and the two RX voltages follow sin and cos of the rotor angle.
* KESE turns `Stator.kicad_pcb` and `Rotor.kicad_pcb` into an accurate 3-D model. The bridge turns that model into an
  openEMS simulation, runs it, and reads impedances and voltages.
* **openEMS's job in this project is the part Elmer cannot do: the coils' self resonance and stray capacitance
  (check C8).** Elmer (see "Things to test in ELMER.md") is the main solver for inductance, coupling and the rotor.
  openEMS *can* also do C1 ... C7 as a cross-check, but each run takes hours (section 6), so run them only on the small
  boards (S2, D2) unless the GPU engine makes it cheap.
* **KESE must build both boards with solder mask on: the stator AND the rotor** (section 2.3). In openEMS the mask is
  the one material that changes the answer of C8.

## 1. What is in the zip, and what the bridge reads

```
Things to test in OpenEMS.md          this file
Things to test in ELMER.md            the brief for the Elmer bridge
README.md                             index of the pack
boards/<board>/
  Stator.kicad_pcb, Rotor.kicad_pcb   the input to KESE (KiCad 7 format)
  test_spec.json                      what the bridge needs, machine readable (section 3)
  Parameters.txt                      the generator's full record (where test_spec.json got its numbers)
  expected_results.json               every predicted number, with the coupling curves vs rotor angle
  expected_coupling.png, *_stator_and_rotor.png, README.md (the board card)
tools/
  kicad_to_openems.py                 a working reference converter straight from KiCad (no KESE) - see section 5
  quasistatic_reference.py            the script that made expected_results.json
SOLVER_VALIDATION_GUIDE.md            the long background document (physics, method, sources)
```

The ten boards, smallest first is the best order to bring a bridge up:

| Board | Set(s) | OD / bore (mm) | Layers, board | Why it is in the pack |
|---|---|---|---|---|
| S2_4x_OD40_2L_small | 4x | 40 / 20 | 2, 1.6 mm | the cheapest model: **start here** |
| D2_1x8x_OD40_small | 1x + 8x | 40 / 10 | 4, 1.6 mm | the smallest dual board |
| S1_1x_OD54_2L_baseline | 1x | 54 / 30 | 2, 1.6 mm | the generator's default; simplest geometry |
| S3_8x_OD59_4L_series_wideband | 8x | 59 / 22 | 4, 1.6 mm | TX on inner layers, series TX |
| S4_16x_OD54_2L_fingers | 16x | 54 / 30 | 2, 1.6 mm | finest pitch, bridging fingers |
| S5_4x_OD98_cosine_r_2subcoils_spiralTX | 4x | 98 / 58 | 2, 1.6 mm | biggest board, spiral TX |
| D1_1x16x_OD54_Renesas_R145_size | 1x + 16x | 54 / 15 | 4, 3.2 mm | the dual default, thick board |
| D3_1x16x_OD59_fitted_bands | 1x + 16x | 59 / 17 | 4, 1.6 mm | typical dual |
| D4_2x8x_OD59_parallel_TX | 2x + 8x | 59 / 17 | 4, 1.6 mm | parallel TX wiring |
| D5_1x16x_OD74_ID40_large | 1x + 16x | 74 / 40 | 4, 1.6 mm | large thin ring |

## 2. What the KESE model must contain for openEMS

### 2.1 Coordinates and placement (same in both bridges)

* Origin on the rotation axis = KiCad point (100, 100). **KiCad's y axis points down**: a model with y up uses
  y_model = -(y_kicad - 100). That flips every rotation sense; say in the bridge which convention it uses.
* z up, from the stator towards the rotor. **The top face of the stator's F.Cu copper is z = 0**; the stator
  is below (negative z). Layer z values per board are in `test_spec.json` -> `stator.layer_z_mm`.
* The rotor: `Rotor.kicad_pcb` **as drawn, not mirrored**, copper side facing down towards the stator, its copper face
  at z = +air gap (1.0 mm), its 1.6 mm FR-4 above. The air gap is measured copper to copper.
* Rotor angle theta: turn the rotor about the axis by (x, y) -> (x cos t - y sin t, x sin t + y cos t) in KiCad
  coordinates. theta = 0 is the rotor exactly as drawn. The expected curves use the same convention.

### 2.2 Copper and FR-4

* Copper 35 um thick on every layer, as real solids. openEMS options: (a) perfect conductor (fastest, fine for
  C1 ... C7 and the resonance frequency); (b) a conducting sheet of 35 um and 5.8e7 S/m (adds the loss, which sets the
  Q of the resonance). Use (b) for C8.
* FR-4: eps_r 4.4, loss tangent 0.02 (stator and rotor). It only moves the self resonance, but that is exactly C8.
* Vias: copper cylinders (or the plated barrel) between the layers they join.

### 2.3 Solder mask on both boards (required)

* KESE must build the solder mask on **both faces of the stator and both faces of the rotor**, over all copper and
  the bare FR-4, with no openings (vias tented). No mask is set in these KiCad stackups, so use the typical LPI values
  in `test_spec.json` -> `solder_mask`: **20 um thick, eps_r 3.8, loss tangent 0.02**. If KESE's own stackup gives
  other values, use those and write them into the results.
* The mask lies inside the 1.0 mm gap: between the stator's mask and the rotor's mask there is 1.0 - 2 x 0.020 =
  0.96 mm of air (over copper).
* Why it matters here: the mask fills the space between neighbouring traces on the outer layers, where the fringing
  field of the turn-to-turn capacitance is strongest. It lowers the self resonance by a few percent. It has no effect on
  L, M or the eddy currents (it is a non-magnetic insulator).
* openEMS mesh: the mask needs z mesh lines at its two faces (copper top + 0.020 mm, and the FR-4 surface + 0.020 mm).
  A 20 um layer on a staircase mesh is the thinnest feature in the model; if it makes the time step too small, model
  it as a flat 20 um slab from z = 0 to +0.020 (and the same on the rotor and the stator bottom) and say so. The slab
  version misses only the mask in the gaps between traces below the copper top. For C8, run both once on S2 and report the difference.

### 2.4 Terminals (ports)

The generator's coils are closed or open loops without connectors. Ports go where the real board gets its leads.
`test_spec.json` -> `terminals` gives each one:

* **TX** ("TX ends"): the two coil ends lie stacked at one (x, y) on two layers (e.g. Top and Bottom). Put a
  z-directed lumped port between the two ends.
* **RX** ("RX cut"): cut the F.Cu trace at the given point with a gap of about 0.2 mm; the port spans the gap.
* **RX on S2 and S4** ("RX via (fallback)"): the generator found no cut spot. Leave the named via out and put a
  z-directed port between its two pads.
* Port resistances: TX 500 ohm (excited), every RX 1000 ohm (load, nearly open). See section 4 for why.

### 2.5 Boundary and air

* Air around everything to about 2.5 ... 3 x the board radius (`test_spec.json` -> `air_box`), MUR or PML outside.
  At 400 MHz the wavelength is 750 mm, so the box is still far smaller than a wavelength: the boundary mainly has to be
  far enough not to load the coils' near field.

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
| `terminals` | where each coil's port goes (section 2.4), in KiCad and in axis coordinates, with the layers and z |
| `expected` | L (generator and reference, rotor away and with rotor), DC resistance, M0, amplitude, h3, phase, angle error per set |
| `tx_wiring` | D4 only: parallel TX (drive both layers from one port) |

## 4. How openEMS measures at 3 ... 5 MHz (the method)

openEMS is FDTD: the time step is set by the smallest cell, not by the frequency. The openEMS documentation says that
below about 100 MHz the number of steps becomes impractically large. Three things make it workable here:

1. The wanted quantities (L, M) are flat in frequency well below the self resonance, so they can be read anywhere
   between a few MHz and about a fifth of the resonance.
2. The run does not need to resolve a 3 MHz period. It needs the energy to die out; then the DFT is exact at every
   frequency in the pulse. The decay time is L / R of the coil on its port resistance, so a 500 ohm TX port (few-uH
   coil: about 5 ns) keeps the run to a few hundred thousand steps. R does not change Z = V / I.
3. The RX ports are nearly open (1 kohm), so one run per TX gives the whole column of the coupling matrix:
   V_RX / I_TX = Z21 within Z22 / R (under 3 % at 5 MHz). For an exact matrix, excite each port once and convert S to Z.

Excitation: Gaussian, f0 = 0, bandwidth fmax (100 MHz for C1 ... C7, 400 MHz for C8). End criterion: energy down 50 dB.

Reading: w = 2 pi f, L_TX = Im(Z11) / w, R_TX = Re(Z11), M = Im(V_RX / I_TX) / w,
capacitive coupling = Re(V_RX / I_TX) growing with f.

## 5. The reference converter (without KESE)

`tools/kicad_to_openems.py` builds the same model directly from the KiCad files with flat strips (no copper
thickness, **no solder mask**). It is the baseline the KESE bridge should agree with on C1 ... C7, and the
difference on C8 shows what the real copper and the mask add. It was written against the openEMS 0.37 Python API;
its parsing, ports and mesh estimate were run on all ten boards, but **the openEMS part was never run** (openEMS was not
installed where it was written). Use `--dry-run` first and look at `model.xml` in AppCSXCAD.

## 6. The tests

Per board, every test uses the same run type; only the rotor (none, or turned to an angle) and the driven TX change.
Frequencies: single boards 3.5 MHz; dual boards set 1 at 3.0 MHz, set 2 at 4.3 MHz (`sets[].f_Hz`).

### C8 Self resonance and stray capacitance (openEMS's main job)

* Runs per board: each TX driven, rotor away; then the same with the rotor at theta = 0. fmax 400 MHz, copper as
  35 um conducting sheets, FR-4 and solder mask with loss.
* Read:
  * f_SRF of each TX: the first frequency where Im(Z11) crosses zero (Z11 peaks; the coil looks like an open).
  * The TX's own capacitance: C_self = 1 / ((2 pi f_SRF)^2 x L_TX), with L_TX from the flat low-frequency part.
  * Each RX coil's self resonance: one extra run per RX coil, that coil driven, the others loaded.
  * Capacitive TX -> RX coupling: Re(V_RX / I_TX) and the deviation of |V_RX / I_TX| from w x M between 5 and 50 MHz.
    Pure inductive coupling grows exactly as f; capacitive coupling adds a part growing as f^2 with a 90 deg different phase.
  * Dual boards: also TX_1 -> TX_2 (open TX_2) above 20 MHz.
* Expected: no number from the pack (the generator does not model capacitance). Requirement: **f_SRF at least 5 x the
  operating frequency** (> 17.5 MHz single, > 21.5 MHz for a dual board's set 2). Then the 3 ... 5 MHz results of
  C1 ... C7 hold. My guess, not a calculation: some tens to a few hundred MHz, lowest for the TX with the most turns
  (S5, D1 set 2).
* Also report: the shift of f_SRF with the rotor on (the rotor copper adds capacitance), and with the solder mask
  on vs off (S2 only, once). The mask should lower f_SRF by a few percent.
* Why it matters: the tank capacitor on the TX is chosen from L; the stray capacitance adds to it, and an RX
  self resonance near the operating frequency would distort the RX voltages.

### C1 ... C7 (optional cross-check, the same tests Elmer runs)

| # | Run | Read | Expected (from `test_spec.json` / section 7) | Pass |
|---|---|---|---|---|
| C1 TX L, rotor away | TX driven, no rotor | L_TX = Im(Z11)/w, flat from 1 MHz to past 5 MHz | `expected.tx.*.L_away_ref_H` (agrees with the generator within 0.5 %) | within 5 % |
| C2 TX L with rotor | rotor at theta = 0, then at `c2_second_angle_mech_deg` | L(rotor), drop = 1 - L(rotor)/L(away) | **the open question**: the reference says 2 ... 7 %, the generator 12 ... 21 % | report the number |
| C3 offset | the C1 run | M0 = Im(V_RX/I_TX)/w per RX coil | `expected.coupling.*.M0_no_rotor_H`, a few % of the amplitude or less | M0/Amp < 3 % |
| C4 coupling vs angle | rotor at the 8 angles in `sets[].c4_angles_mech_deg` | M_SIN(theta), M_COS(theta); fit mean + A cos(N theta + phi) + A3 cos(3 N theta + phi3) | `amplitude_H`, `h3_rel`; curves in `expected_results.json` | A within 15 %, period exact, h3 within 2x |
| C5 SIN/COS match | from C4 | phi_SIN - phi_COS, A_SIN / A_COS | +/-90.0 deg, 1.000 | 90 +/- 1 deg, 1.00 +/- 0.02 |
| C6 angle error | from C4 | atan2 of SIN/COS minus N theta, peak | `pairs.*.angle_error_pk_elec_deg` | same order |
| C7 dual crosstalk | TX_1 runs read SIN_2/COS_2; then TX_2 driven | amplitude of the other set's coupling | crosstalk table, section 7 | report |

Run-time of one openEMS run at 0.05 mm cells (estimates from the dry run, not measurements; GPU at 2 G cell updates/s):

| Board | Cells | Steps | One run, GPU | One run, CPU (200 M/s) |
|---|---|---|---|---|
| S2 | 34 M | 540 k | 2.5 h | 25 h |
| D2 | 34 M | 540 k | 2.5 h | 25 h |
| S1, S4 | 63 M | 540 k | 4.7 h | 47 h |
| S3, D3, D4 | 74 ... 75 M | 540 k | 5.6 h | 56 h |
| D1 | 71 M | 540 k | 5.3 h | 53 h |
| D5 | 119 M | 540 k | 9.0 h | 90 h |
| S5 | 212 M | 540 k | 15.9 h | 159 h |

A solder mask meshed at 20 um in z adds z lines but not x/y lines, so it costs little; a finer x/y mesh is what costs
(half the cell = 4x the cells and 2x the steps). Never use x/y cells larger than half the narrowest trace (0.15 ... 0.2 mm),
or a strip can break into pieces on the staircase mesh and open the coil.

## 7. Expected numbers (quasi-static reference)

L gen = the generator's estimate, L ref = the reference's (rotor away / with rotor); M0 = direct coupling with no rotor;
Amp = rotor-dependent coupling amplitude; V_RX/V_TX = Amp / L ref(rotor); h3 = 3rd harmonic; err = angle error, electrical degrees,
offsets removed (raw).

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

Dual crosstalk (C7), amplitude of each TX into the other set's RX coils: D1 TX_1->set 2 9.51 nH, TX_2->set 1 6.45 nH;
D2 8.42 / 4.39 nH; D3 20.87 / 16.29 nH; D4 12.15 / 8.25 nH; D5 34.11 / 9.54 nH.

The sign of dphi (+90 or -90) depends on the rotation sense and the y convention; either is right if it is consistent.

## 8. What to report

One CSV per board, one line per run:

```
board,set,tx,rotor,angle_mech_deg,f_Hz,L_tx_H,R_tx_ohm,M_sin_H,M_cos_H,re_sin_over_itx,re_cos_over_itx,f_srf_Hz,C_self_F,cell_mm,mask,copper_model,end_db,runtime_s,notes
```

plus Z11(f) and V_RX/I_TX(f) from 1 to 400 MHz for the C8 runs, and the KESE version and the mask values used.
