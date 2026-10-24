"""The output folder of one run: <root>/<board>/<mode>_<FORMATS>, then <mode>_<FORMATS>__1, __2,
... so no run overwrites another."""
from pathlib import Path


def new_folder(root, board, mode, formats):
    base = Path(root) / board / (mode + "_" + "_".join(f.upper() for f in formats))
    out_dir, n = base, 0
    while out_dir.exists():
        n += 1
        out_dir = base.with_name(f"{base.name}__{n}")
    out_dir.mkdir(parents=True)
    return out_dir
