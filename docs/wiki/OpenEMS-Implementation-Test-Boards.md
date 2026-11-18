# 37. OpenEMS Implementation Test Boards

The boards the openEMS bridge is proved on. O01 is drawn from above and in section, and links to its
results. Every board is a folder under `Examples/` on the `OpenEMS_Integration` branch, with its KiCad
files, its `simulation.py` and its `README.md`.

## 37.1 O01 Microstrip

![O01 drawn from above and in section: a 50 by 30 mm FR-4 board with a 2.9 mm red strip on Top running its whole length over a ground plane on Bottom; dashed boxes mark the 10 mm ports at each end and lines their measurement planes, 38 mm apart; the section across the strip shows the strip on top of the 1.53 mm core and the ground under the whole board](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/OpenEMS-Implementation-Test-Boards/O01_microstrip/oemsboards_1_board.webp)

| Item | Value |
|---|---|
| Board | 50 mm × 30 mm, two copper layers, a 1.53 mm FR-4 core (εr 4.4, tan δ 0.02 at 1 GHz), 1.6 mm finished |
| Copper | F.Cu: one trace of net `RF`, 2.9 mm wide and 35 µm thick, along the whole board. B.Cu: one filled polygon with no net |
| What openEMS checks | Z0 and εeff from the ports' own probes, εeff again from S21's phase, S21 against the dielectric's loss, S11 |
| References | Hammerstad and Jensen (Z0 with the strip's thickness, static εeff), Kirschning and Jansen (εeff's dispersion), Pozar (the dielectric's loss) |
| Run | 88 s on 4 cores, 411,424 cells |
| Status | **run**: [OpenEMS Implementation Test Board Results](OpenEMS-Implementation-Test-Board-Results.md#381-o01-microstrip) |

## 37.2 What Comes Next

The examples beyond O01 (crosstalk between two lines, a TDR of a line with a step in it, a cavity's
resonances, a filter) follow the same pattern: a board made by `make_board.py`, a `simulation.py`
with every setting in `SETTINGS`, and a `results.md` with what was expected against what came out.

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Simulating Your Own Board](OpenEMS-Implementation-Simulating-Your-Own-Board.md) | [OpenEMS Implementation Test Board Results](OpenEMS-Implementation-Test-Board-Results.md) |
