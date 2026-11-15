# Solver_OpenEMS

This folder is empty on purpose: openEMS is built here from its own source, on the machine that runs
the simulations.  Checked on Ubuntu 24.04 on 15 November 2026 at openEMS-Project master, commit
e4cd015 (13 November 2026).

## Ubuntu 24.04

```
sudo apt-get update
sudo apt-get install -y build-essential cmake git libhdf5-dev libtinyxml-dev libboost-all-dev zlib1g-dev \
    python3-dev python3-venv cython3 python3-numpy python3-h5py python3-matplotlib python3-setuptools-scm
cd Solver_OpenEMS
git clone --recursive https://github.com/thliebig/openEMS-Project.git
cd openEMS-Project && git checkout e4cd015 && git submodule update --init --recursive
./update_openEMS.sh --python --disable-GUI --njobs="$(nproc)" "$PWD/../install"
```

The bridge looks for `Solver_OpenEMS/install/bin/openEMS` and the Python modules in
`Solver_OpenEMS/install/venv`.  Simulations use openEMS's new CPU engine (`engine='cpu'`), which ran
about 1.6 times faster than the default engine here, in about 60% of its memory.
