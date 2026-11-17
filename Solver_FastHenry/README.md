# Solver_FastHenry

[FastHenry](https://github.com/ediloren/FastHenry2) is the solver of this branch: the magneto-quasi-static inductance
and resistance extractor written at M.I.T. by Mattan Kamon, Lou Silveira and others (1994 to 1996), kept up by
FastFieldSolvers as release 3.0.1. It works on conductors cut into straight filaments, each carrying a uniform
current, and couples every filament to every other through its partial inductance; only the copper is
discretised, and the space round it is handled exactly. `install/bin/fasthenry` is the build every simulation in this
branch ran with. It is one small program (460 kB) that needs nothing but the C library, committed so a fresh copy of
the branch runs without building anything, and so every machine solves with the same program.

| | |
|---|---|
| Program | FastHenry 3.0.1 (it prints `FastHenry Version 3.0.1 (28May12)`), from FastFieldSolvers' Linux/Unix release: [github.com/ediloren/FastHenry2](https://github.com/ediloren/FastHenry2), branch `master`, commit `363e43e` |
| Build | [`build_fasthenry.sh`](build_fasthenry.sh): its `x64` configuration, GCC 13.3 with `-O3 -DFOUR -m64 -fcommon`, on Ubuntu 24.04; the script makes the very same file again, byte for byte |
| Runs on | 64-bit Linux with glibc 2.34 or newer (Ubuntu 22.04 and up); it needs only `libc` and `libm`. Elsewhere, build it from source with the script (any Unix with a C compiler), or use FastFieldSolvers' FastHenry2 on Windows |
| Solve used | `-s ludecomp -m direct -a off`: the dense direct solve, LU of the full mesh matrix, with the multipole refinement off (it splits filaments that come close, which the direct solve does not need and which ended in an exit at 0.1 mm air gaps). It gives the exact answer of the filament model (the impedance matrix comes out symmetric to the last digit), with no iteration to converge and nothing paid or proprietary under it |
| Licence | M.I.T.'s, as M.I.T. re-released FastHenry in 2003: use, copy, modify, sell and distribute for any purpose, without royalty, keeping the notice. See [`LICENSE.md`](LICENSE.md), which also says why the source files still carry an older notice |

## Using it

The bridge finds the program by itself: `$FASTHENRY` if it is set, else `Solver_FastHenry/install/bin/fasthenry`,
else `fasthenry` on the PATH (`bridge/fasthenry_case.py`, `fasthenry_exe`). To check it:

```
Solver_FastHenry/install/bin/fasthenry -h | head -3        # FastHenry Version 3.0.1 (28May12)
```

To build it again from source (git, make and a C compiler; about ten seconds), from the branch's root:

```
bash Solver_FastHenry/build_fasthenry.sh
```

It clones FastFieldSolvers' repository at commit `363e43e` into a temporary folder, configures it for x64, compiles
it with the flags above and puts the program in `install/bin`. `SRC=...` keeps the source in a folder of your
choosing. `-fcommon` is needed with GCC 10 and newer, which otherwise refuse the program's shared global variables.
`-O3` in place of the release's `-O` makes it a few per cent faster and changes no result (checked on a full S0
model: the same `Zc.mat`, digit for digit).

## Why this release

Whiteley Research's FastHenry 3.0wr (in [XicTools](https://github.com/wrcad/xictools)) carries M.I.T.'s 2003 licence
text in every source file, but it lacks two of FastFieldSolvers' fixes to the mutual inductance of filaments that
meet or nearly touch (in `mutual.c`: the formula for filaments meeting at a point, and a negative distance clipped to
zero). A rotor grid of collinear bars trips exactly those cases: 3.0wr (release 031424) prints thousands of
"mutual inductance = infinity" warnings on an S0 model and returns a matrix of NaN, where 3.0.1 solves it cleanly
(the same model with the rotor away gives the same matrix in both, to 1e-20). So this branch runs 3.0.1.

## What FastHenry is given

`bridge/fasthenry_case.py` writes one input file per solve (`model.inp`, kept under each board's `case/`): units of
millimetres, copper at 5.8e7 S/m, every track a segment split into filaments across its width, every via a bar,
the rotor a grid of bars, and the three ports (`.external`) between the nodes where each coil is opened. FastHenry
writes `Zc.mat`, the open-circuit impedance matrix between the ports at the frequency asked for, which the bridge
reads back. The board READMEs and `bridge/README.md` say how each part is modelled.
