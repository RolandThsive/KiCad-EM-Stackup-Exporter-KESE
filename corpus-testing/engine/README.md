# Corpus Testing Engine

`assemble.py` builds every Corpus Testing page from the boards' files alone, in about a second, with nothing but
Python 3.9 or newer. The Corpus Engine workflow runs it on every push that changes `docs/tables/` or `docs/images/`,
commits what it changed and starts the wiki sync.

A board is two folders with the same name: `docs/tables/<name>/` (`board.json`, `stages.md`, `facts.md`,
`files.md`) and `docs/images/<name>/` (`stages.webp`, when the board has a chart). At every run the engine:

1. Numbers the boards 1 to n in order of project and then path (from `board.json`).
2. Names every board's folders `b<number>b_<repo>_<board>`, its data folder in `corpus-testing/data/` too: a new
   board, added as `<repo>_<board>` with no number, gets its number, and every board after it is renamed with its new
   one. A board added by hand with no data folder is given one, with what its `board.json` says and no runs.
3. Writes `docs/wiki/CorpusTestingPages/Corpus-Testing-NN.md`, 108 boards a page, each board's section headed with
   its number and name; `CombinedCorpusTesting.md`, every board on one page; and
   `docs/wiki/BoardPages/b<number>b_<repo>_<board>.md`, one page per board.
4. Writes the master page, `docs/wiki/Corpus-Testing.md`: the counts, the pages, the grades and what did not pass.

A board whose folders are deleted is gone at the next run, with its board page (delete its data folder too).
`features.json` holds the features and weights of the complexity grade, which the master page lists.

    python3 corpus-testing/engine/assemble.py

The boards' files are made from their runs by [`maker/`](maker), which lives here too.
