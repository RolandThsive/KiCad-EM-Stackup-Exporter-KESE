# 53. FastHenry Installation

The bridge needs three things: FastHenry, a Python environment with the bridge's packages, and, only to export a
board whose `3D_Geometry/` is not committed, a copy of KESE. Unlike the other solvers' branches, this one carries its
solver: `Solver_FastHenry/install/bin/fasthenry` is the build every simulation on the branch ran with, one small
program (460 kB) that needs nothing but the C library.

## 53.1 Linux (Ubuntu 24.04)

This is the route the test boards ran on. One script sets up a fresh machine:

```bash
bash bridge/setup_machine.sh
```

It makes `.venv` at the branch's root with the packages of `requirements.txt`, at the versions the examples ran
with, and builds FastHenry from source only if the committed program does not run. It needs Python 3.12 or newer
(numpy 2.5 and scipy 1.18 need it) and is safe to run again.

**FastHenry**, committed and ready:

```bash
Solver_FastHenry/install/bin/fasthenry -h | head -3        # FastHenry Version 3.0.1 (28May12)
```

The bridge finds the program by itself: `$FASTHENRY` if it is set, else `Solver_FastHenry/install/bin/fasthenry`,
else `fasthenry` on the PATH (`fasthenry_exe` in `bridge/fasthenry_case.py`).

| Item | Value |
|---|---|
| Program | FastHenry 3.0.1, from FastFieldSolvers' Linux/Unix release: [github.com/ediloren/FastHenry2](https://github.com/ediloren/FastHenry2), branch `master`, commit `363e43e` |
| Build | `Solver_FastHenry/build_fasthenry.sh`: its `x64` configuration, GCC 13.3 with `-O3 -DFOUR -m64 -fcommon`, on Ubuntu 24.04; the script makes the very same file again, byte for byte |
| Runs on | 64-bit Linux with glibc 2.34 or newer (Ubuntu 22.04 and up); it needs only `libc` and `libm` |
| Licence | M.I.T.'s, as M.I.T. re-released FastHenry in 2003: use, copy, modify, sell and distribute for any purpose, without royalty, keeping the notice (`Solver_FastHenry/LICENSE.md`) |

**To build FastHenry again from source** (git, make and a C compiler; about ten seconds), from the branch's root:

```bash
bash Solver_FastHenry/build_fasthenry.sh
```

It clones FastFieldSolvers' repository at commit `363e43e` into a temporary folder, configures it for x64, compiles
it and puts the program in `install/bin`. `SRC=...` keeps the source in a folder of your choosing.

> [!IMPORTANT]
> Keep `-fcommon` in the flags. GCC 10 and newer otherwise refuse the program's shared global variables. `-O3` in
> place of the release's `-O` makes it a few per cent faster and changes no result: on a full coil model it gave the
> same `Zc.mat`, digit for digit.

**Python**, if you set it up by hand instead of with the script:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt       # numpy, scipy, shapely, matplotlib, pillow
```

numpy and shapely are the bridge's; matplotlib and pillow draw the coil examples' charts and pictures.

**KESE**, only to export a board whose `3D_Geometry/` is not committed (the three boards of this category have
theirs committed). Copy it from `main` so that `run_KESE.py` sits directly in `3D_Geometry/`:

```bash
git -C <your KESE clone> archive main Generator | tar -x --strip-components=1 -C 3D_Geometry
.venv/bin/python 3D_Geometry/run_KESE.py --help
```

or leave `3D_Geometry/` empty and point the bridge at any KESE with `export KESE_PATH=<path to Generator>`. KESE
runs inside the bridge's Python, so its own packages (`requirements.txt` in `Generator/`) must be in the same
environment.

**Check the whole chain** with the first proof board, at nine filaments across its trace:

```bash
cd Examples/E01_circular_loop
../../.venv/bin/python simulation.py --nwinc 9
```

Each solve takes under a second. It should print L about 55.538 nH and R about 61.208 mOhm at 10 kHz, the 9 × 1
values of [FastHenry Test Board Results](FastHenry-Test-Board-Results.md#571-e01-circular-loop). A rerun replaces
that rung in the committed `results.json`, with the same numbers.

## 53.2 Windows

The committed program is a Linux build. Two routes:

| Route | Steps | Notes |
|---|---|---|
| **WSL 2 (recommended)** | Install Ubuntu 24.04 from the Microsoft Store, then follow [53.1](#531-linux-ubuntu-2404) inside it | The bridge, KESE and the committed FastHenry all run as on Linux. Keep the repository inside the WSL file system (not under `/mnt/c`) |
| **Native** | Use FastFieldSolvers' FastHenry2 for Windows, set `FASTHENRY` to its program, and set up Python with `py -m venv .venv` and `.venv\Scripts\pip install -r requirements.txt` | Not run on the test boards. The bridge passes `-s ludecomp -m direct -a off` and reads `Zc.mat`; check that the Windows build takes those options and writes that file |

## 53.3 What The Test Machine Had

| Item | Version |
|---|---|
| OS | Ubuntu 24.04, 4 cores, 15 GB of memory |
| FastHenry | 3.0.1 (the committed build) |
| Python | 3.13 (3.13.18) |
| numpy, scipy, shapely | 2.5.5, 1.18.1, 2.2.0 |
| matplotlib, pillow | 3.11.2, 13.0.0 |
| KESE | 3.4.0, for the stack-up exports committed with each board |

Each example writes the versions it ran with into its results file, so every number on
[FastHenry Test Board Results](FastHenry-Test-Board-Results.md) names the software that made it.

| Previous | Next |
|:---|---:|
| [FastHenry Introduction](FastHenry-Introduction.md) | [FastHenry Workflow](FastHenry-Workflow.md) |
