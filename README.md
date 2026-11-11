# KESE Corpus Testing

This branch holds the Corpus Testing of [KiCad EM Stackup Exporter (KESE)](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE),
apart from the code: 3,138 KiCad boards from 819 open hardware projects, each exported six times by KESE, one file
format a run, with the Verifier on.

- [`docs/tables/`](docs/tables): a folder per board, `b<number>b_<repo>_<board>`, with its three tables and what the
  pages need to know about it.
- [`docs/images/`](docs/images): a folder per board, of the same name, with its chart.
- [`docs/wiki/Corpus-Testing.md`](docs/wiki/Corpus-Testing.md): the master page, how the boards were run and graded,
  and what did not pass.
- [`docs/wiki/CorpusTestingPages/`](docs/wiki/CorpusTestingPages): Corpus Page 1 to 30, 108 boards each, and every
  board on one page.
- [`docs/wiki/BoardPages/`](docs/wiki/BoardPages): a page per board.
- [`corpus-testing/engine/`](corpus-testing/engine): the engine that numbers the boards and builds every page from
  their folders, by itself on each push.
- [`corpus-testing/maker/`](corpus-testing/maker): makes a board's folders from its runs.
- [`corpus-testing/data/`](corpus-testing/data): the record of every run and the boards' complexity list.

To add a board, push its two folders named `<repo>_<board>`; to take one out, delete them. The engine does the rest.

No board, nor any part of one, is in this branch: the boards belong to their authors ([Credits](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/Credits)).
