# 3D_Geometry

This folder is empty on purpose.  KESE is developed on `main`, and this branch never carries a copy
of it, so the bridge always runs the KESE you choose.

To fill it, copy what is inside the `Generator/` folder of `main` (or of a KESE release) in here
by hand, so that `run_KESE.py` sits directly in this folder:

```
git -C <your KESE clone> archive main Generator | tar -x --strip-components=1 -C 3D_Geometry
```

Then check that it runs:

```
python 3D_Geometry/run_KESE.py --help
```

The bridge writes KESE's version into every example's Results section, so each result names the
geometry it came from.
