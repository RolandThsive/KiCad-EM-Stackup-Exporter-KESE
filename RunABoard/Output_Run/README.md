# Output Run

The runner writes a folder here for each board, named as its file, with the board's data folder for Corpus
Testing:

- `board.json`: the board's project, path and name, its counts from its file (layers, parts, big chips, BGAs,
  tracks, vias, the KiCad version, notes), its KESE features, the commit it was taken at, and a blank license
- `runs.jsonl`: its six runs, one line each

Fill in the license and the day you looked it up (`license_checked`, as `YYYY-MM-DD`), or leave them blank. Then
copy the folder into `corpus-testing/data/` and push it: the engine names it, works out its score and rank, and
makes its tables, chart and pages.

Nothing written here is committed: only this README is.
