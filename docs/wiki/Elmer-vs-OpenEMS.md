# 42. Elmer vs openEMS

The two bridges turn the same KESE export into two very different simulations. This page sets them
side by side, with the numbers measured on their proof boards, so that you can pick the one a
question needs.

## 42.1 The Two Solvers

| | Elmer FEM | openEMS |
|---|---|---|
| Method | finite elements, in the frequency domain | finite differences in time (FDTD) |
| Physics | magneto-quasi-static: the A-V formulation with eddy currents, no displacement current | the full Maxwell equations, with waves |
| Branch and bridge | `Elmer_Integration`, `bridge/` (five modules) | `OpenEMS_Integration`, `bridge/fdtd.py` |
| KESE preset | `--for elmer` | `--for openems` |
| Copper | a conductor with its σ, current inside it, skin effect included | PEC: no loss, no skin depth |
| Insulators | air (μr 1, and εr plays no part without displacement current) | each dielectric with its εr, and tan δ as a conductivity |
| Mesh | 2.5D: one triangle mesh of the footprint, wedges through the board, tetrahedra in the air | a rectilinear grid: lines at every copper edge by the thirds rule, smoothed and graded |
| Ports | each coil opened at its terminals: two electrodes and a sheet across the gap | microstrip ports with their own probes and an end resistor |
| Results | L, R, M, the field's energy, at each frequency asked for | S-parameters (one column per run), Z0, εeff, time signals |
| Frequency range | DC up to where the board is still small against the wavelength | from where a pulse fits the run (hundreds of MHz on a small board) up to the mesh's f_max |

## 42.2 Measured On The Proof Boards

| | E01, one loop (Elmer) | O01, a microstrip (openEMS) |
|---|---|---|
| Model size | 85,712 nodes (level 1) | 411,424 cells |
| Run | 17 minutes at 10 kHz (3000 iterations), 6 minutes at 3.5 MHz | under 2 minutes for 1 to 5 GHz at once |
| Memory | 4.9 GB | 0.15 GB |
| Against the reference | L 3 % under Grover's open ring at level 1, 0.46 % with the air graded four times as finely; rising with the mesh (a lower bound) | εeff within 1.5 % of Kirschning–Jansen, Z0 within 2 % of Hammerstad–Jensen |

Elmer pays for its unstructured mesh and its iterative solve with about 59 kB per node; openEMS
needs only 60 to 103 bytes per cell (its CPU and default engines), but its cells must resolve the copper's edges and its run
must last until the field has died away. Elmer's run time grows with the number of frequencies,
openEMS's with the length of the ring-down: a resonance of high Q takes openEMS hundreds of thousands
of time steps.

## 42.3 Which One For What

| Question | Solver | Why |
|---|---|---|
| Inductance, resistance, mutual inductance of coils at kHz to a few MHz | Elmer | quasi-static is exact there, and it has the copper's conductivity and skin depth |
| How a rotor or a shield of copper changes a coil (eddy currents) | Elmer | the A-V formulation with σ |
| A line's impedance, εeff, loss in the dielectric | openEMS | it needs waves and εr |
| S-parameters, crosstalk, TDR, filters | openEMS | the same |
| A coil's self resonance and stray capacitance | openEMS | Elmer's quasi-static solve has no capacitance between turns |
| Conductor loss at GHz | neither yet | openEMS's copper is PEC; Elmer has no waves |

## 42.4 Where They Meet: The Coil Boards

The ten inductive encoder boards are the one place both solvers work on the same boards. Elmer
answers the inductance and coupling checks (C1 to C7, C10) at 3 to 5 MHz; openEMS answers the self
resonance (C8), which tells whether those MHz answers hold at all, and repeats C1 to C7 on S2 and D2
as a cross-check of Elmer. Neither has run them yet: S2's Elmer mesh needs about 59 GB and an openEMS
C8 run on S2 about 7 hours, so both wait for a bigger, unattended machine
([Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md#283-the-ten-inductive-encoder-boards),
[OpenEMS Implementation Test Boards](OpenEMS-Implementation-Test-Boards.md#372-the-ten-inductive-encoder-boards)).

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Troubleshooting](OpenEMS-Implementation-Troubleshooting.md) | [Glossary](Glossary.md) |
