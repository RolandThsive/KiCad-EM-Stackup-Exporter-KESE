# KESE Corpus Testing

This branch holds the Corpus Testing of [KiCad EM Stackup Exporter (KESE)](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE),
apart from the code: 3,138 KiCad boards from 819 open hardware projects, each exported six times by KESE, one file
format a run, with the Verifier on.

- [`docs/wiki/Corpus-Testing.md`](docs/wiki/Corpus-Testing.md): the index, how the boards were run and graded,
  and what did not pass.
- [`docs/wiki/CorpusTesting/`](docs/wiki/CorpusTesting): Corpus Page 1 to 29, a section for every board.
- [`docs/images/Corpus-Testing/`](docs/images/Corpus-Testing): the charts.
- [`corpus-testing/builder/`](corpus-testing/builder): the script that builds the pages, and how to add or take out
  a board.
- [`corpus-testing/data/`](corpus-testing/data): the record of every run and the boards' complexity list.

No board, nor any part of one, is in this branch: the boards belong to their authors ([Credits](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/Credits)).
