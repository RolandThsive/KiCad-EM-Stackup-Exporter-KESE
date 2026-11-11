# The Main Program

Put KESE here: the [KiCad-EM-Stackup-Exporter-KESE](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE)
repository, cloned or downloaded, or its `Generator` folder alone. The runner finds `run_KESE.py` wherever it is
inside this folder.

    git clone --depth 1 https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE "The Main Program/KESE"

A clone lets the runner note KESE's commit in every run. For a download, give the commit with
`--kese-commit <commit>`, or the runs say "unknown". Install KESE's requirements once:

    pip install -r "The Main Program/KESE/Generator/requirements.txt"

Nothing put here is committed: only this README is.
