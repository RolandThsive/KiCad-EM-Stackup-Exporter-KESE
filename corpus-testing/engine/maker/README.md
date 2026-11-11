# Corpus Board Maker

Makes each board's files from its runs in `corpus-testing/data/`, for the engine to build the pages from:

    docs/tables/<repo>_<board>/board.json    name, project, path, license, complexity, features, status ...
    docs/tables/<repo>_<board>/stages.md     seconds per stage, one row per mode and format
    docs/tables/<repo>_<board>/facts.md      repo, folder, complexity, layers, format, the Verifier's result ...
    docs/tables/<repo>_<board>/files.md      the file each run wrote and its peak memory
    docs/images/<repo>_<board>/stages.webp   the chart

A board the engine has numbered already keeps its folders (`b0057b_<repo>_<board>`) and they are written in place;
a new board's folders have no number, and the engine numbers and renames them. From the top of this branch:

    python3 corpus-testing/engine/maker/make.py            every board
    python3 corpus-testing/engine/maker/make.py 2 13 57    the boards of these ranks only
    python3 corpus-testing/engine/assemble.py       then the pages (a push does this by itself)

Needs Python 3.11 or newer with matplotlib and Pillow.

Each board's runs are in its folder in `corpus-testing/data/`, named as its tables folder: `board.json` (its counts
from the `.kicad_pcb`, its KESE features, its path, its project's license, and what makes it a bad design, if it is
one) and `runs.jsonl` (every run of it in order, each with its date and source).

- **Add a board:** add its folder to `data/`, `<repo>_<board>/`, with its `board.json` (a rank no other board has)
  and `runs.jsonl`, then make it. Or add its two folders by hand, named `<repo>_<board>`.
- **Take a board out:** delete its folders in `docs/tables/`, `docs/images/` and `data/`.
- **Name a bad design:** set `bad_design` in the board's `data/.../board.json`, with what the file has there.
- **A run that passes when run again:** add it to the board's `runs.jsonl` with its source: `"fixed"` (with fixes to
  KESE), `"cap"` (with a bigger memory cap) or `"nocap"` (with no memory cap). It takes the place of a failed run; a
  run that fails again keeps its first result. A `"corpus"` run takes the place of an earlier `"corpus"` run.
- **Charts:** one is drawn only when its `stages.webp` is missing; delete it to draw it again.

The boards themselves belong to their authors and are not here: only the numbers of the runs.
