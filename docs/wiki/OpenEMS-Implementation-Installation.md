# 34. OpenEMS Implementation Installation

The bridge needs openEMS with its Python modules (`openEMS` and `CSXCAD`), a few more Python
packages in the same environment, and a copy of KESE. The branch never carries openEMS or KESE
itself: `Solver_OpenEMS/` and `3D_Geometry/` are empty on purpose and are filled by hand.

## 34.1 Linux (Ubuntu 24.04)

This is the route the test boards ran on, at openEMS-Project master, commit `e4cd015`
(13 November 2026).

**openEMS**, built with its Python modules into `Solver_OpenEMS/install`:

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake git libhdf5-dev libtinyxml-dev libboost-all-dev zlib1g-dev \
    python3-dev python3-venv cython3 python3-numpy python3-h5py python3-matplotlib python3-setuptools-scm
cd Solver_OpenEMS
git clone --recursive https://github.com/thliebig/openEMS-Project.git
cd openEMS-Project && git checkout e4cd015 && git submodule update --init --recursive
./update_openEMS.sh --python --disable-GUI --njobs="$(nproc)" "$PWD/../install"
```

This leaves the solver in `Solver_OpenEMS/install/bin/openEMS` and a Python environment with the
`openEMS` and `CSXCAD` modules in `Solver_OpenEMS/install/venv`. The bridge's own packages and
KESE's go into that same environment:

```bash
Solver_OpenEMS/install/venv/bin/pip install trimesh shapely scipy matplotlib
Solver_OpenEMS/install/venv/bin/pip install -r <your KESE>/Generator/requirements.txt
```

**KESE**, copied from `main` so that `run_KESE.py` sits directly in `3D_Geometry/`:

```bash
git -C <your KESE clone> archive main Generator | tar -x --strip-components=1 -C 3D_Geometry
```

or point the bridge at any KESE with `export KESE_PATH=<path to Generator>`.

**Check the whole chain** with the first proof board (a few minutes on 4 cores):

```bash
cd Examples/O01_microstrip
../../Solver_OpenEMS/install/venv/bin/python simulation.py
```

The simulations use openEMS's new CPU engine (`engine='cpu'`, marked experimental by openEMS), which
ran about 1.6 times faster than the default engine on the test machine, in about 60 % of its memory.

## 34.2 Windows

openEMS publishes a ready-made Windows package with its releases
([openEMS-Project releases](https://github.com/thliebig/openEMS-Project/releases)): a ZIP with the
solver's DLLs and pre-compiled wheels of the `openEMS` and `CSXCAD` modules, each for one Python
version (`cp313` in a wheel's name means CPython 3.13). openEMS's own documentation calls it a quick
start that may lag behind the source and recommends Linux for production runs. Two routes:

| Route | Steps | Notes |
|---|---|---|
| **WSL 2 (recommended)** | Install Ubuntu 24.04 from the Microsoft Store, then follow [34.1](#341-linux-ubuntu-2404) inside it | Everything runs as on Linux. Keep the repository inside the WSL file system (not under `/mnt/c`) |
| **Native** | Unzip the package (say to `C:\openEMS`); `python -m pip install numpy h5py matplotlib`; `python -m pip install --no-index --find-links C:\openEMS\python openEMS`; set `CSXCAD_INSTALL_PATH` to the folder with the DLLs and open a new prompt; then `pip install trimesh shapely scipy` and KESE's requirements into the same Python | The bridge only needs `import openEMS, CSXCAD` to work in the Python that runs `simulation.py`. A package older than the CPU engine does not know `engine='cpu'`: leave the engine out ([OpenEMS Implementation Troubleshooting](OpenEMS-Implementation-Troubleshooting.md)). Not yet run on the test boards |

## 34.3 What The Test Machine Had

| Item | Version |
|---|---|
| OS | Ubuntu 24.04, 4 cores, 15 GB of memory |
| openEMS | openEMS-Project master `e4cd015` (openEMS `fc00235`, CSXCAD `fdff4b5`) |
| Python | 3.13, with numpy 2.5.4 in openEMS's environment |
| trimesh, shapely, scipy | 5.2.1, 2.2.0, 1.18.1 |

Each example writes the versions and the hashes of the code it ran with into its `results.json`.

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Introduction](OpenEMS-Implementation-Introduction.md) | [OpenEMS Implementation Workflow](OpenEMS-Implementation-Workflow.md) |
