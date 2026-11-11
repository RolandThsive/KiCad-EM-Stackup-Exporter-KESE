# Corpus Board Maker

Makes each board's files from the run results in `corpus-testing/data/`, for the engine to build the pages from:

    docs/tables/<repo>_<board>/board.json    name, project, path, complexity, features, status, bad design ...
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

- **Add a board:** add its line to `data/kicad_board_complexity_scores.txt` and its runs to `data/results/`, then
  make it. Or add its two folders by hand, named `<repo>_<board>`.
- **Take a board out:** delete its folders in `docs/tables/` and `docs/images/`, and add its rank to `left_out` in
  `corpus_boards.json`, with why, so that it is not made again.
- **Name a bad design:** add its rank to `bad_design` in `corpus_boards.json`, with what the file has there.
- **A run that passes when run again:** `data/fixes/FIXED[23]*.jsonl` (with fixes to KESE), `data/fixes/C*.jsonl`
  (with a bigger memory cap) and `data/fixes/M*.jsonl` (with no memory cap) take the place of a failed run; a run
  that fails again keeps its first result.
- **Charts:** one is drawn only when its `stages.webp` is missing; delete it to draw it again.

The boards themselves belong to their authors and are not here: only the numbers of the runs.
