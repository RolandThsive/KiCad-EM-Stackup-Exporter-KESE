# KESE Corpus Testing

This branch holds the Corpus Testing of [KiCad EM Stackup Exporter (KESE)](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE),
apart from the code: 3,101 KiCad boards from 801 open hardware projects, each exported six times by KESE, one file
format a run, with the Verifier on.

- [`corpus-testing/data/`](corpus-testing/data): a folder per board, `b<number>b_<repo>_<board>`, with its counts
  from its `.kicad_pcb`, its path and license (`board.json`) and the record of every run of it, each with its date
  (`runs.jsonl`). This is the board: everything else is made from it, its rank and score too.
- [`docs/tables/`](docs/tables): a folder per board, of the same name, with its three tables and what the pages need
  to know about it.
- [`docs/images/`](docs/images): a folder per board, of the same name, with its chart.
- [`docs/wiki/Corpus-Testing.md`](docs/wiki/Corpus-Testing.md): the master page, how the boards were run and graded,
  and what did not pass.
- [`docs/wiki/CorpusTestingPages/`](docs/wiki/CorpusTestingPages): Corpus Page 1 to 29, 108 boards each, and every
  board on one page.
- [`docs/wiki/BoardPages/`](docs/wiki/BoardPages): a page per board.
- [`docs/wiki/Credits.md`](docs/wiki/Credits.md) and [`credits.txt`](credits.txt): every board by its number, with
  its project and the project's license.
- [`corpus-testing/engine/`](corpus-testing/engine): the maker, which makes each board's tables and chart from its
  data folder, and the engine, which numbers the boards and builds every page; both run by themselves on each push.
- [`RunABoard/`](RunABoard): the runner, which you run on your own computer: give it KESE and boards, and it writes
  each board's data folder.

To add a board, make its data folder with [Run A Board](RunABoard), fill in its license (or leave it blank) and
push it; to take one out, delete it. The rest is made on GitHub: the folder's name, the board's score, rank and
number, its tables and chart, every page, the Credits and the counts. A folder without all six runs is rejected and
deleted. A second board of the same name gets `-2` after its folder's name. A board's chart is drawn once: to draw it
again after its runs change, take the board out in one push and add it back in another.

For how to add a board, see [pull request #56](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/pull/56),
which added Thermometer's main board this way: a branch made from corpus-testing with only the board's data folder,
`board.json` and `runs.jsonl`, merged into corpus-testing. The engine did the rest at the merge.

No board, nor any part of one, is in this branch: the boards belong to their authors ([Credits](docs/wiki/Credits.md)).
