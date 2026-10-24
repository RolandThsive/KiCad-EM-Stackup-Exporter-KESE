#!/usr/bin/env python3
"""KiCad EM Stackup Exporter (KESE), run from the project folder without installing it:

    python run_KESE.py [boards] [options]        python run_KESE.py --help lists the options

After `pip install .` the same command is `kese`.  The code is in kese/cli.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kese.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
