# Corpus Testing Engine

A board is its data folder, `corpus-testing/data/<repo>_<board>/`, given by hand. It holds `board.json` (its counts
from the `.kicad_pcb`, its KESE features, its path and its project's license) and `runs.jsonl` (its six runs, and any
run again, each with its date). Its rank, score and number are never given: they are worked out at every push. Everything
else is made from it. On every push to this branch the Corpus Engine workflow runs the maker, then the engine, commits
what changed and starts the wiki sync:

    python3 corpus-testing/engine/maker/make.py && python3 corpus-testing/engine/assemble.py

1. The **maker** ([`maker/make.py`](maker)) names a new board's data folder `<repo>_<board>` (`-2`, `-3` ... after
   it when that name is taken). It works out every
   board's score, level and rank (1 the most complex) from the counts in its `board.json`. It then makes each
   board's tables, `docs/tables/<name>/` (`board.json`, `stages.md`, `facts.md`, `files.md`), and its chart,
   `docs/images/<name>/stages.webp`, named as its data folder. A board is made once its `runs.jsonl` has a run of
   each of the six modes and formats: one without them is rejected, its data folder and anything made from it
   deleted. A chart is drawn only when it is missing: taking a board out and adding it back draws it again. A data
   folder that can't be read is left out. Either way the run fails, naming the folder and why.
2. The **engine** (`assemble.py`) takes out a board whose data folder is gone, with its tables and chart, and numbers
   the boards 1 to n in order of project and then path.
3. It names every board's folders `b<number>b_<repo>_<board>`, in `corpus-testing/data/`, `docs/tables/` and
   `docs/images/`: a new board, pushed as `<repo>_<board>` with no number, gets its number, and every board after it
   is renamed with its new one.
4. It writes `docs/wiki/CorpusTestingPages/Corpus-Testing-NN.md`, 108 boards a page, each board's section headed with
   its number and name; `CombinedCorpusTesting.md`, every board on one page; and
   `docs/wiki/BoardPages/b<number>b_<repo>_<board>.md`, one page per board.
5. It writes the master page, `docs/wiki/Corpus-Testing.md`: the counts, the pages, the grades and what did not pass.
   How the boards were run is worked out from the runs too: the KESE version and commit, the machine (its cores and
   RAM), the memory cap and time limit, and the days a failed run was run again and how.
6. It writes the Credits, `docs/wiki/Credits.md` (every board by its number, with its project, the project's
   license and the days its runs were made) and `credits.txt` (the same by project, with each board's path), with the
   days the licenses were looked up from each board's `license_checked`, and the counts of boards and projects
   in this branch's README. A board of a project already here that comes with no license takes its project's; a
   board of a new project with none shows "Not looked up yet".

The engine needs nothing but Python 3.9 or newer; the maker needs Python 3.11 or newer with matplotlib and Pillow,
whose own font, DejaVu Sans, the charts are drawn in. `features.json` holds the features and weights of the
complexity grade, which the master page lists.
