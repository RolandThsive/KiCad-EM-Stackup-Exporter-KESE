# 40. OpenEMS Implementation Hardware

What openEMS needed on the test machine, how to estimate a board of your own before you run it, and
which boards wait for a bigger machine.

## 40.1 The Test Machine

| Item | Value |
|---|---|
| Processor | 4 cores |
| Memory | 15 GB |
| System | Ubuntu 24.04 |
| openEMS | built from source, openEMS-Project master `e4cd015` ([OpenEMS Implementation Installation](OpenEMS-Implementation-Installation.md)) |
| Graphics card | none, so openEMS's GPU engine is untested here (40.5) |

## 40.2 Memory And Speed, Measured

openEMS's memory grows with the number of cells, and its speed is counted in cell updates a second:
one time step over a million cells is a million updates.

| Engine | Bytes per cell | Speed on a 13.5 million cell model, the machine to itself | O01 (411,424 cells), sharing the machine |
|---|---|---|---|
| CPU engine (`engine='cpu'`, marked experimental) | 60 | 701 million updates a second | 88 s for 23,048 steps, 113 million a second, 0.15 GB |
| default engine (`--engine default`) | 103 | 434 million updates a second | 97 s for 23,316 steps, 104 million a second, 0.17 GB |

* The O01 runs shared the machine with an Elmer solve that held two of its four cores, so their
  speed is far under the benchmark's. Their times are what a run took, not what the machine can do.
* O01's peak memory is the whole Python process: KESE's parts, the mesh, trimesh and
  openEMS. openEMS's own share at 60 bytes a cell is 25 MB.
* openEMS's log counts mesh lines, not cells: O01's 104 × 86 × 46 cells are its *105x87x47 --> 429345
  FDTD cells*, and the speeds above are the ones openEMS printed for those. The bridge's preflight
  counts cells.
* Both engines give the same O01 numbers within 0.005 % ([OpenEMS Implementation Test Board Results](OpenEMS-Implementation-Test-Board-Results.md#381-o01-microstrip)).

openEMS's own changelog gives the CPU engine 3 to 6 times the default engine's speed on an 8-core
Ryzen 7 5800X and about a third less memory at the peak of the setup. On the 4-core test machine it
was 1.6 times as fast with 42 % less memory.

## 40.3 Estimating A Run

| Quantity | How to get it | O01 |
|---|---|---|
| Cells | the preflight prints them before anything runs | 411,424 |
| Time step | set by the smallest cells: one 35 µm cell through each copper layer makes it small, and openEMS warns *the timestep seems to be very small* | 93 fs |
| Time steps | the pulse's length, plus the time the field takes to die away to `end_criteria` | the pulse 15,401 steps (1.43 ns), the run 23,048 |
| Memory | cells × 60 bytes (CPU engine) or × 103 (default engine), plus the Python process | 0.15 GB |
| Time | cells × time steps ÷ speed | 88 s, with half the machine |

A board that rings needs far more time steps than a line ended in its own impedance: a resonance of
high Q holds the field for a long time after the pulse has gone. A coil's self-resonance run needs
about 540,000 time steps, 23 times O01's run.

## 40.4 What Fits Where

The tables leave a third or more of a machine's memory to the system and to Python.

| Machine | Boards that fit, CPU engine | Example |
|---|---|---|
| 8 GB | up to about 75 million cells | O01 |
| 16 GB | up to about 120 million cells | |
| 32 GB | up to about 250 million cells | |

Time is the harder limit: at 701 million cell updates a second, a self-resonance run of 540,000 time
steps on 34 million cells takes about 7 hours on 4 cores, and longer in proportion to the cells.

## 40.5 The GPU Engine

openEMS's master branch, which the bridge is built against, adds a GPU engine (`engine='gpu'`) for
AMD and NVIDIA cards (HIP and CUDA) and for macOS (Metal), as its changelog lists under *Unreleased*.
The test machine has no graphics card, so the bridge has not been run on it; a build for it needs
the HIP, CUDA or Metal compiler when openEMS is compiled, and the backend is left out with a warning
when that compiler is missing.

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Accuracy](OpenEMS-Implementation-Accuracy.md) | [OpenEMS Implementation Troubleshooting](OpenEMS-Implementation-Troubleshooting.md) |
