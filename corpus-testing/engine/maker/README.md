# Corpus Board Maker

Makes each board's files from its data folder, `corpus-testing/data/<name>/`, for the engine to build the pages from:

    docs/tables/<name>/board.json    name, project, path, license, complexity, features, status ...
    docs/tables/<name>/stages.md     seconds per stage, one row per mode and format
    docs/tables/<name>/facts.md      repo, folder, complexity, layers, format, the Verifier's result ...
    docs/tables/<name>/files.md      the file each run wrote and its peak memory
    docs/images/<name>/stages.webp   the chart

`<name>` is the data folder's: `<repo>_<board>` for a new board, which the engine then numbers and renames, and
`b0057b_<repo>_<board>` once it has. The Corpus Engine workflow runs the maker and then the engine on every push;
from the top of this branch, by hand:

    python3 corpus-testing/engine/maker/make.py                           every board
    python3 corpus-testing/engine/maker/make.py Thermometer_TheMainBoard  the boards of these data folders only
    python3 corpus-testing/engine/assemble.py                             then the pages

Needs Python 3.11 or newer with matplotlib and Pillow.

A board's data folder is given by hand. It holds `board.json`, with the board's `project` (`owner/repo`), its `path`
(`<owner>__<repo>/<path in the repo>`), its `name` (if left out, its file's name), its project's `license` and the
day it was looked up (`license_checked`, `YYYY-MM-DD`), its counts from the `.kicad_pcb` (`layers`, `parts`, `big`,
`bga`, `tracks`, `vias`, `kicad`, `notes`), its KESE `features`, and `bad_design` if KESE finds it one. It also holds
`runs.jsonl`, every run of the board in order, each with its `date`, its `source`, its memory `cap` and `time_limit`
(in bytes and seconds, `null` for none) and the `machine` it ran on, with the KESE `kese_version` and commit (`kese`).
[`score.py`](score.py) prints a board's counts and features from its file:

    python3 corpus-testing/engine/maker/score.py <board.kicad_pcb>

The maker works out the rest, and never takes it as given:
- **Folder name:** a new board's folder is renamed `<repo>_<board>`. If another board has that name already, it
  gets `-2` after it (`<repo>_<board>-2`), a third `-3`, and so on.
- **Score and level:** worked out from the counts, as `score.py` describes.
- **Rank:** 1 is the most complex, by score.

These go into the board's tables (`docs/tables/<name>/board.json`), with the days of its runs, the KESE version,
the machine and the limits they ran with, which the master page and the Credits are written from. The engine then
gives the board its number.

A data folder that can't be read is not added, and the workflow run fails with a line saying why, never a crash: a
`board.json` or a line of `runs.jsonl` that isn't valid JSON, a field missing, a count that isn't a whole number.

- **Add a board:** push its data folder under any name, with its `board.json` and its six runs in `runs.jsonl`. A
  board already in the corpus (the same project and path) is not added twice, and the workflow's log says so.
- **Take a board out:** delete its data folder; its tables, chart and board page go at the next run.
- **Name a bad design:** set `bad_design` in the board's `data/.../board.json`, with what the file has there.
- **A run that passes when run again:** add it to the board's `runs.jsonl` with its source: `"fixed"` (with fixes to
  KESE), `"cap"` (with a bigger memory cap) or `"nocap"` (with no memory cap). It takes the place of a failed run; a
  run that fails again keeps its first result. A `"corpus"` run takes the place of an earlier `"corpus"` run.
- **Charts:** one is drawn only when its `stages.webp` is missing, so a run added later changes the board's tables
  but not its chart. To draw it again, take the board out (push the deletion of its data folder) and add it back
  (push the folder again): its chart is drawn from the runs it then has. Deleting its `stages.webp` does the same.
  A chart is drawn in DejaVu Sans, which comes with matplotlib, so nothing else needs installing (the charts drawn
  before 11 November 2026 are in Inter).

The boards themselves belong to their authors and are not here: only the numbers of the runs.
