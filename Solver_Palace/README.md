# Solver_Palace

[Palace](https://github.com/awslabs/palace) is the solver of this branch: AWS Labs' parallel finite element code for
electromagnetics, built on [MFEM](https://mfem.org) and [hypre](https://github.com/hypre-space/hypre), released under
the Apache 2.0 licence. In its frequency-domain (driven) mode it solves Maxwell's equations for the electric field
with Nédélec edge elements: the copper is a conducting region, the air round it is meshed out to a boundary, and
each coil is opened by a lumped port, a sheet across the cut with a resistance across it. `install/` holds the build
every simulation in this branch ran with, committed so a fresh copy of the branch runs without building anything,
and so every machine solves with the same program.

| | |
|---|---|
| Program | Palace 0.19.0 (it prints `Palace version: v0.19.0-dirty` in its log, `dirty` because the patch below is applied to the release's source), AWS Labs' release: [github.com/awslabs/palace](https://github.com/awslabs/palace), tag `v0.19.0`, commit `ca9a6a2` |
| Build | [`build_palace.sh`](build_palace.sh): Palace's own CMake superbuild, which builds MFEM, hypre, libCEED, METIS, ARPACK-NG and GSLIB at the versions Palace 0.19.0 pins, with [`no_parmetis.patch`](no_parmetis.patch) applied (below); GCC 13.3 and Open MPI 4.1.6 on Ubuntu 24.04, release build, double precision, no OpenMP and no GPU |
| Solvers in it | AMS (hypre's auxiliary-space Maxwell preconditioner) under GMRES, the iterative solve Palace recommends for its frequency-domain problems. No sparse direct solver: SuperLU_DIST and STRUMPACK need ParMETIS (below), and MUMPS's source is downloaded from mumps-solver.org, which the test machine's network refused (the patch builds MUMPS without ParMETIS, ordered by METIS: `WITH_MUMPS=1` in the build script, not tried here). Every solve is checked instead (see the bridge's README) |
| Files | `install/bin/palace` (Palace's launcher script: it starts the program under `mpirun`), `install/bin/palace-x86_64.bin` (the program, 36.5 MB, every library statically linked but those below) and `install/lib/libceed.so` (libCEED, which Palace loads beside it). SHA-256 in the table at the end |
| Runs on | 64-bit Linux with glibc 2.38 or newer (Ubuntu 24.04 and up) and, from the system, Open MPI 4.1 (`openmpi-bin`, `libopenmpi3t64`), OpenBLAS (`libopenblas0`), gfortran's runtime (`libgfortran5`) and zlib, all free. `bash bridge/setup_machine.sh` installs them. Elsewhere, build it with the script |
| Licence | Apache 2.0 for Palace; everything built into it is open source too, under the licences in [`licenses/`](licenses/) (BSD, MIT, Apache 2.0, MPL 2.0). See [Licences](#licences) |

## Using it

The bridge finds the program by itself: `$PALACE` if it is set, else `Solver_Palace/install/bin/palace`, else
`palace` on the PATH (`bridge/palace_case.py`, `palace_exe`). To check it:

```
Solver_Palace/install/bin/palace --version
```

Palace reads one JSON file per solve. `bridge/palace_case.py` writes it (`config.json`, kept under each board's
`case/`), runs `palace -np N config.json` on N MPI ranks, and reads back the CSV files Palace writes: each port's
voltage and current, and the field's energy.

To build it again from source (an hour on four cores, 3 GB of disk while it builds), from the branch's root:

```
sudo apt install git cmake build-essential gfortran openmpi-bin libopenmpi-dev libopenblas-dev zlib1g-dev \
                 pkg-config patchelf
bash Solver_Palace/build_palace.sh
```

It clones Palace at `v0.19.0`, applies the patch, runs Palace's superbuild (which clones each library at the version
Palace pins and builds it) and puts the program in `install/`, with its run path set so that it finds `libceed.so`
beside it wherever the folder is. `JOBS=...` sets the parallel jobs, `WORK=...` keeps the source and build in a
folder of your choosing. The superbuild downloads a few patches to MFEM and hypre from github.com's commit and compare
links; the test machine's network refused those, so the committed program was built with `LOCAL_PATCHES=1`, which
makes the same nine diffs with git from MFEM's and hypre's own repositories (the script's diffs and the ones the
committed build used are the same files, byte for byte).

## Why it is built without ParMETIS

Palace's release build links ParMETIS, the parallel graph partitioner, for the fill-reducing orderings of its direct
solvers, and prints its version. ParMETIS is not open source: its licence lets non-profit institutions use it for
research and education only, and forbids selling or redistributing it without the University of Minnesota's
approval (Debian ships it in `non-free`). A program with ParMETIS in it could not be committed here or used freely, so
[`no_parmetis.patch`](no_parmetis.patch) makes ParMETIS optional:

* ParMETIS is built and linked only with SuperLU_DIST or STRUMPACK, which are both left out;
* MUMPS, where it is built, is ordered by METIS alone (`MUMPS_parmetis=OFF`), METIS being Apache 2.0 since version
  5.0.2;
* Palace's version report leaves ParMETIS out when it is not linked;
* MFEM is given hypre's BLAS and LAPACK (OpenBLAS) to link with: in Palace's own build they reach MFEM's link line
  only through a direct solver, so a build with none fails to link MFEM's first example without it.

Nothing else changes: MFEM partitions the mesh between the MPI ranks with METIS, as it always does. `build_palace.sh`
refuses to install a program in which any ParMETIS symbol is found, and the committed program has none
(`nm install/bin/palace-x86_64.bin | grep -ci parmetis` gives 0; the word is left only as the name of a configuration
option, SuperLU_DIST's column ordering, in the schema the program checks its input against).

## What Palace is given

For every solve, `bridge/palace_case.py` writes:

* the mesh, in Gmsh's format 2.2, in millimetres (`L0 = 1e-3`): wedges through the copper and the air beside it, and
  tetrahedra out to the domain's boundary, each body a physical volume and each boundary a physical surface;
* the materials: air everywhere (relative permittivity and permeability 1), the copper with a conductivity of
  5.8e7 S/m;
* the outer boundary as a perfect conductor (tangential E = 0), far enough out (three board radii) not to matter;
* each coil's port as a `LumpedPort`: the driven one with a resistance of 50 Ω and an excitation, the receivers with
  1 MΩ, so that they are open to a few parts in a million;
* one frequency point (`Driven`, `Samples`), Nédélec elements of order 1, and the linear solver (GMRES with AMS).

Palace writes each port's voltage (`port-V.csv`) and the magnetic energy of the field (`domain-E.csv`), and the bridge
works out each coil's impedance, inductance, resistance and mutual inductance from them (see
[`bridge/README.md`](../bridge/README.md)).

## Licences

Palace is Apache 2.0 ([`LICENSE`](LICENSE), [`NOTICE`](NOTICE), and Palace's own third-party files
[`THIRD-PARTY-LICENSES`](THIRD-PARTY-LICENSES) and [`THIRD-PARTY-NOTICES`](THIRD-PARTY-NOTICES)). What the program
has built into it, each at the version Palace 0.19.0 pins, with its licence text in [`licenses/`](licenses/):

| Library | Version | What it does in Palace | Licence | Files in `licenses/` |
|---|---|---|---|---|
| [MFEM](https://github.com/mfem/mfem) | 4.10 | the finite element library Palace is built on (meshes, Nédélec spaces, assembly) | BSD 3-Clause | `MFEM-LICENSE`, `MFEM-NOTICE` |
| [hypre](https://github.com/hypre-space/hypre) | 3.2.0 | AMS, the preconditioner of every solve here, and its algebraic multigrid | MIT or Apache 2.0, at the user's choice | `hypre-COPYRIGHT`, `hypre-LICENSE-MIT`, `hypre-LICENSE-APACHE`, `hypre-NOTICE` |
| [libCEED](https://github.com/CEED/libCEED) | 1.0.1 | the operators' partial assembly (`install/lib/libceed.so`) | BSD 2-Clause | `libCEED-LICENSE`, `libCEED-NOTICE` |
| [METIS](https://bitbucket.org/petsc/pkg-metis) | 5.1.0 (PETSc's `v5.1.0-p13`) | partitions the mesh between the MPI ranks | Apache 2.0 | `METIS-LICENSE.txt` |
| [GSLIB](https://github.com/Nek5000/gslib) | 1.0.9 | interpolation of the fields at points | BSD 3-Clause | `GSLIB-LICENSE` |
| [ARPACK-NG](https://github.com/opencollab/arpack-ng) | 3.9.1 | eigenvalues (Palace's eigenmode solves, not used here) | BSD 3-Clause | `ARPACK-NG-COPYING` |
| [Eigen](https://gitlab.com/libeigen/eigen) | 5.0.1 | small dense linear algebra (headers) | MPL 2.0, a few files BSD or Apache 2.0 | `Eigen-LICENSE`, `Eigen-COPYING.*` |
| [{fmt}](https://github.com/fmtlib/fmt) | 12.2.0 | text formatting | MIT | `fmt-LICENSE` |
| [scnlib](https://github.com/eliaskosunen/scnlib) | 4.0.1 | text scanning | Apache 2.0 | `scnlib-LICENSE` |
| [nlohmann/json](https://github.com/nlohmann/json) | 3.12.0 | reading the configuration file | MIT | `nlohmann-json-LICENSE.MIT` |
| [json-schema-validator](https://github.com/pboettch/json-schema-validator) | 2.4.1 | checking the configuration file against Palace's schema | MIT | `json-schema-validator-LICENSE` |

The system libraries it loads (Open MPI, OpenBLAS, gfortran's runtime, zlib) come with the operating system under
their own free licences (BSD, BSD, GPL with the GCC runtime library exception, zlib). Every source is public at the
version named, which is how the MPL 2.0 asks for Eigen's to be offered; none of these libraries was changed (the
patches Palace's build applies to MFEM and hypre are their own upstream commits).

## Checksums

| File | SHA-256 |
|---|---|
| `install/bin/palace` | `7a397eab85d1bc714b78ff501783a9e771f69eba3e9ea3e08607f05edc95781a` |
| `install/bin/palace-x86_64.bin` | `bdba472c742da7b00cc449802b378bc9f6c14ad5bdbd48929c46ed9fc9804945` |
| `install/lib/libceed.so` | `351c62184d2998d6e900ce9ed7fa82f7cc1480fbe9780f99731dd519989cd2ef` |
