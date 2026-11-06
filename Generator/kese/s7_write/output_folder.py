"""The output folder of one run: <root>/<board>/<mode>_<FORMATS>, then <mode>_<FORMATS>__1, __2,
... so no run overwrites another."""
from itertools import count
from pathlib import Path


def new_folder(root, board, mode, formats):
    """The first of those names free, made.  Taken by making it: two runs started together (a batch
    of boards in parallel) each get a folder of their own, where looking first and making after
    let both pick the same name and the second stop on it."""
    base = Path(root) / board / (mode + "_" + "_".join(f.upper() for f in formats))
    for n in count():
        out_dir = base.with_name(f"{base.name}__{n}") if n else base
        try:
            out_dir.mkdir(parents=True)
        except FileExistsError:
            continue
        return out_dir
