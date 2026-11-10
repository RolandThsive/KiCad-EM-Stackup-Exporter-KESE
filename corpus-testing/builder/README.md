# Corpus Pages Builder

Builds `docs/wiki/Corpus-Testing.md` and `docs/wiki/CorpusTesting/*.md` (and the charts in
`docs/images/Corpus-Testing/`) from the run results in `corpus-testing/data/`. From the top of this branch:

    python3 corpus-testing/builder/final.py corpus-testing/data/results .

Needs Python 3.11 or newer with matplotlib and Pillow.

- **Take a board out:** add its rank to `left_out` in `corpus_boards.json`, with why.
- **Name a bad design:** add its rank to `bad_design`, with what the file has there.
- **Add a board:** add its line to `data/kicad_board_complexity_scores.txt` and its runs to `data/results/`. It
  goes on the page of its project, else on the last page (a new page once that holds 100 boards).
  `page_of_rank.json` pins every board to its page, so no other page changes.
- **A run that passes when run again:** `data/fixes/FIXED[23]*.jsonl` (with fixes to KESE) and `data/fixes/C*.jsonl`
  (with a bigger memory cap) take the place of a failed run; a run that fails again keeps its first result.
- **Charts:** one is drawn only when its `.webp` is missing; delete a board's `.webp` to draw it again.

The boards themselves belong to their authors and are not here: only the numbers of the runs.
