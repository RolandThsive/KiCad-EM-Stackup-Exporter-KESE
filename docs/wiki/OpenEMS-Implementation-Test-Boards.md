# 37. OpenEMS Implementation Test Boards

The boards the openEMS bridge is proved on, each rendered by KESE's static renderer from its own
export, top and bottom. A board that has run links to its results; a board that has not is marked
**YET TO BE RUN**. Every board is a folder under `Examples/` on the `OpenEMS_Integration` branch,
with its KiCad files, its `simulation.py` and its `README.md`.

## 37.1 O01 Microstrip

| Top | Bottom |
|:---:|:---:|
| ![O01 from above: the 30 mm by 50 mm FR-4 board with the 2.9 mm trace of net RF running along its whole length, its round ends touching the board's left and right edges](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/OpenEMS-Implementation-Test-Boards/O01_microstrip/oemsboards_1_top.webp) | ![O01 from below: B.Cu, one copper polygon with no net over the whole board](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/OpenEMS-Implementation-Test-Boards/O01_microstrip/oemsboards_2_bottom.webp) |

| Item | Value |
|---|---|
| Board | 50 mm × 30 mm, two copper layers, a 1.53 mm FR-4 core (εr 4.4, tan δ 0.02 at 1 GHz), 1.6 mm finished |
| Copper | F.Cu: one trace of net `RF`, 2.9 mm wide and 35 µm thick, along the whole board. B.Cu: one filled polygon with no net |
| What openEMS checks | Z0 and εeff from the ports' own probes, εeff again from S21's phase, S21 against the dielectric's loss, S11 |
| References | Hammerstad and Jensen (Z0 with the strip's thickness, static εeff), Kirschning and Jansen (εeff's dispersion), Pozar (the dielectric's loss) |
| Run | 88 s on 4 cores, 411,424 cells |
| Status | **run**: [OpenEMS Implementation Test Board Results](OpenEMS-Implementation-Test-Board-Results.md#381-o01-microstrip) |

## 37.2 The Ten Inductive Encoder Boards

Ten angle-encoder boards from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator),
in `Examples/Inductive Coils/` (non-commercial licence, see that folder's `LICENSE.md`). A stator
carries one TX and two RX coils (SIN and COS) per coil set, the single boards (S) one set and the dual
boards (D) two; a rotor with copper sectors sits 1.0 mm above it. The TX runs at 3 to 5 MHz.

openEMS's job on these boards is what Elmer's quasi-static solve cannot do: each TX coil's self
resonance and stray capacitance (check C8). The TX must resonate at least five times above its
operating frequency, or the 3 to 5 MHz results of the Elmer checks do not hold. openEMS repeats the
inductance and coupling checks (C1 to C7) as a cross-check on S2 and D2 only, where a run is
affordable.

A C8 run rings the coil down for about 540,000 time steps, which takes many hours on the 4-core test
machine, so every one waits for a machine that can run unattended:

| # | Board | What it tests | Cells at 0.05 mm | Memory | One run, 4 cores | Runs on | Status |
|---|---|---|---|---|---|---|---|
| 1 | `S2_4x_OD40_2L_small` | the smallest single board, the cheapest model | 34 M | about 2.0 GB | about 7 h | 8 GB | **YET TO BE RUN** |
| 2 | `D2_1x8x_OD40_small` | the smallest dual board, tight spacing between the sets | 34 M | about 2.0 GB | about 7 h | 8 GB | **YET TO BE RUN** |
| 3 | `S1_1x_OD54_2L_baseline` | the generator's default, the simplest geometry | 63 M | about 3.8 GB | about 13 h | 8 GB | **YET TO BE RUN** |
| 4 | `S3_8x_OD59_4L_series_wideband` | TX on the inner layers, far from the rotor; a wide band | 75 M | about 4.5 GB | about 16 h | 8 GB | **YET TO BE RUN** |
| 5 | `S4_16x_OD54_2L_fingers` | the finest single pitch, and the bridging fingers | 63 M | about 3.8 GB | about 13 h | 8 GB | **YET TO BE RUN** |
| 6 | `S5_4x_OD98_cosine_r_2subcoils_spiralTX` | the other RX profile, sub-coils, a spiral TX, the biggest board | 212 M | about 12.7 GB | about 45 h | 32 GB | **YET TO BE RUN** |
| 7 | `D1_1x16x_OD54_Renesas_R145_size` | the dual default, a 3.2 mm board | 71 M | about 4.3 GB | about 15 h | 8 GB | **YET TO BE RUN** |
| 8 | `D3_1x16x_OD59_fitted_bands` | a typical dual board | 74 M | about 4.4 GB | about 16 h | 8 GB | **YET TO BE RUN** |
| 9 | `D4_2x8x_OD59_parallel_TX` | parallel TX wiring, a 2-period set | 74 M | about 4.4 GB | about 16 h | 8 GB | **YET TO BE RUN** |
| 10 | `D5_1x16x_OD74_ID40_large` | a large thin ring | 119 M | about 7.1 GB | about 25 h | 16 GB | **YET TO BE RUN** |

Cells and time steps are the generator pack's dry run; memory and time use openEMS's CPU engine at
60 bytes a cell and 701 million cell updates a second, as measured on the test machine for the pack
([OpenEMS Implementation Hardware](OpenEMS-Implementation-Hardware.md)).

The boards, stator and rotor, from above and from below:

| Board | Stator, top | Stator, bottom | Rotor, top | Rotor, bottom |
|---|:---:|:---:|:---:|:---:|
| `S2_4x_OD40_2L_small` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S2_4x_OD40_2L_small/elmerboards_1_stator_top.webp" width="160" alt="S2_4x_OD40_2L_small, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S2_4x_OD40_2L_small/elmerboards_2_stator_bottom.webp" width="160" alt="S2_4x_OD40_2L_small, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S2_4x_OD40_2L_small/elmerboards_3_rotor_top.webp" width="160" alt="S2_4x_OD40_2L_small, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S2_4x_OD40_2L_small/elmerboards_4_rotor_bottom.webp" width="160" alt="S2_4x_OD40_2L_small, rotor bottom"> |
| `D2_1x8x_OD40_small` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D2_1x8x_OD40_small/elmerboards_1_stator_top.webp" width="160" alt="D2_1x8x_OD40_small, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D2_1x8x_OD40_small/elmerboards_2_stator_bottom.webp" width="160" alt="D2_1x8x_OD40_small, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D2_1x8x_OD40_small/elmerboards_3_rotor_top.webp" width="160" alt="D2_1x8x_OD40_small, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D2_1x8x_OD40_small/elmerboards_4_rotor_bottom.webp" width="160" alt="D2_1x8x_OD40_small, rotor bottom"> |
| `S1_1x_OD54_2L_baseline` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S1_1x_OD54_2L_baseline/elmerboards_1_stator_top.webp" width="160" alt="S1_1x_OD54_2L_baseline, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S1_1x_OD54_2L_baseline/elmerboards_2_stator_bottom.webp" width="160" alt="S1_1x_OD54_2L_baseline, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S1_1x_OD54_2L_baseline/elmerboards_3_rotor_top.webp" width="160" alt="S1_1x_OD54_2L_baseline, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S1_1x_OD54_2L_baseline/elmerboards_4_rotor_bottom.webp" width="160" alt="S1_1x_OD54_2L_baseline, rotor bottom"> |
| `S3_8x_OD59_4L_series_wideband` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S3_8x_OD59_4L_series_wideband/elmerboards_1_stator_top.webp" width="160" alt="S3_8x_OD59_4L_series_wideband, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S3_8x_OD59_4L_series_wideband/elmerboards_2_stator_bottom.webp" width="160" alt="S3_8x_OD59_4L_series_wideband, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S3_8x_OD59_4L_series_wideband/elmerboards_3_rotor_top.webp" width="160" alt="S3_8x_OD59_4L_series_wideband, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S3_8x_OD59_4L_series_wideband/elmerboards_4_rotor_bottom.webp" width="160" alt="S3_8x_OD59_4L_series_wideband, rotor bottom"> |
| `S4_16x_OD54_2L_fingers` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S4_16x_OD54_2L_fingers/elmerboards_1_stator_top.webp" width="160" alt="S4_16x_OD54_2L_fingers, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S4_16x_OD54_2L_fingers/elmerboards_2_stator_bottom.webp" width="160" alt="S4_16x_OD54_2L_fingers, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S4_16x_OD54_2L_fingers/elmerboards_3_rotor_top.webp" width="160" alt="S4_16x_OD54_2L_fingers, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S4_16x_OD54_2L_fingers/elmerboards_4_rotor_bottom.webp" width="160" alt="S4_16x_OD54_2L_fingers, rotor bottom"> |
| `S5_4x_OD98_cosine_r_2subcoils_spiralTX` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S5_4x_OD98_cosine_r_2subcoils_spiralTX/elmerboards_1_stator_top.webp" width="160" alt="S5_4x_OD98_cosine_r_2subcoils_spiralTX, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S5_4x_OD98_cosine_r_2subcoils_spiralTX/elmerboards_2_stator_bottom.webp" width="160" alt="S5_4x_OD98_cosine_r_2subcoils_spiralTX, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S5_4x_OD98_cosine_r_2subcoils_spiralTX/elmerboards_3_rotor_top.webp" width="160" alt="S5_4x_OD98_cosine_r_2subcoils_spiralTX, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S5_4x_OD98_cosine_r_2subcoils_spiralTX/elmerboards_4_rotor_bottom.webp" width="160" alt="S5_4x_OD98_cosine_r_2subcoils_spiralTX, rotor bottom"> |
| `D1_1x16x_OD54_Renesas_R145_size` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D1_1x16x_OD54_Renesas_R145_size/elmerboards_1_stator_top.webp" width="160" alt="D1_1x16x_OD54_Renesas_R145_size, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D1_1x16x_OD54_Renesas_R145_size/elmerboards_2_stator_bottom.webp" width="160" alt="D1_1x16x_OD54_Renesas_R145_size, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D1_1x16x_OD54_Renesas_R145_size/elmerboards_3_rotor_top.webp" width="160" alt="D1_1x16x_OD54_Renesas_R145_size, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D1_1x16x_OD54_Renesas_R145_size/elmerboards_4_rotor_bottom.webp" width="160" alt="D1_1x16x_OD54_Renesas_R145_size, rotor bottom"> |
| `D3_1x16x_OD59_fitted_bands` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D3_1x16x_OD59_fitted_bands/elmerboards_1_stator_top.webp" width="160" alt="D3_1x16x_OD59_fitted_bands, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D3_1x16x_OD59_fitted_bands/elmerboards_2_stator_bottom.webp" width="160" alt="D3_1x16x_OD59_fitted_bands, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D3_1x16x_OD59_fitted_bands/elmerboards_3_rotor_top.webp" width="160" alt="D3_1x16x_OD59_fitted_bands, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D3_1x16x_OD59_fitted_bands/elmerboards_4_rotor_bottom.webp" width="160" alt="D3_1x16x_OD59_fitted_bands, rotor bottom"> |
| `D4_2x8x_OD59_parallel_TX` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D4_2x8x_OD59_parallel_TX/elmerboards_1_stator_top.webp" width="160" alt="D4_2x8x_OD59_parallel_TX, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D4_2x8x_OD59_parallel_TX/elmerboards_2_stator_bottom.webp" width="160" alt="D4_2x8x_OD59_parallel_TX, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D4_2x8x_OD59_parallel_TX/elmerboards_3_rotor_top.webp" width="160" alt="D4_2x8x_OD59_parallel_TX, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D4_2x8x_OD59_parallel_TX/elmerboards_4_rotor_bottom.webp" width="160" alt="D4_2x8x_OD59_parallel_TX, rotor bottom"> |
| `D5_1x16x_OD74_ID40_large` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D5_1x16x_OD74_ID40_large/elmerboards_1_stator_top.webp" width="160" alt="D5_1x16x_OD74_ID40_large, stator top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D5_1x16x_OD74_ID40_large/elmerboards_2_stator_bottom.webp" width="160" alt="D5_1x16x_OD74_ID40_large, stator bottom"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D5_1x16x_OD74_ID40_large/elmerboards_3_rotor_top.webp" width="160" alt="D5_1x16x_OD74_ID40_large, rotor top"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/D5_1x16x_OD74_ID40_large/elmerboards_4_rotor_bottom.webp" width="160" alt="D5_1x16x_OD74_ID40_large, rotor bottom"> |

The renders leave out the solder mask, so that the copper shows; the simulations keep it (20 µm,
εr 3.8, tan δ 0.02 on both faces of both boards, as each board's `test_spec.json` sets).

## 37.3 What Comes Next

The examples beyond O01 (crosstalk between two lines, a TDR of a line with a step in it, a cavity's
resonances, a filter) follow the same pattern: a board made by `make_board.py`, a `simulation.py`
with every setting in `SETTINGS`, and a `results.md` with what was expected against what came out.

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Simulating Your Own Board](OpenEMS-Implementation-Simulating-Your-Own-Board.md) | [OpenEMS Implementation Test Board Results](OpenEMS-Implementation-Test-Board-Results.md) |
