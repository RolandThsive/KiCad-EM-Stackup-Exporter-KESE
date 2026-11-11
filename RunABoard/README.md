# Run A Board

Runs KESE on boards of your choosing, on your own computer, and writes for each board the two files of its data
folder in Corpus Testing: `board.json` and `runs.jsonl`. Push that folder to `corpus-testing/data/` and the engine
on GitHub does the rest. The runner is not run on GitHub: you run it yourself.

    The Main Program/   put KESE here (the latest from GitHub)
    Input_Boards/       put the boards here, each in a folder named <owner>__<repo>
    Output_Run/         a folder per board comes out here: board.json and runs.jsonl

## Getting it

The runner uses the engine's own code to count a board's file, so get this folder together with
`corpus-testing/engine`. You don't need the rest of the branch:

    git clone --depth 1 --branch corpus-testing --filter=blob:none --sparse \
        https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE KESE-corpus
    cd KESE-corpus
    git sparse-checkout set RunABoard corpus-testing/engine
    cd RunABoard

Then put KESE in [`The Main Program`](The%20Main%20Program) and install its requirements, and put the boards in
[`Input_Boards`](Input_Boards):

    git clone --depth 1 https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE "The Main Program/KESE"
    pip install -r "The Main Program/KESE/Generator/requirements.txt"
    git clone https://github.com/<owner>/<repo> Input_Boards/<owner>__<repo>

Needs Python 3.9 or newer. On Windows and macOS, also `pip install psutil`, to measure the memory.

## Running it

    python run_a_board.py                          every board in Input_Boards
    python run_a_board.py TheMainBoard             only the boards whose path has this in it

Each board is run six times, one file format a run, as in Corpus Testing: simulation mode with GLB, STEP, STL and
OBJ, and visual mode with GLB and OBJ. Every run has the Verifier, the solder mask and the silkscreen on, and each
run's peak memory is measured. A run is stopped after 90 minutes, or once its memory passes 11 GB (or 72% of the RAM,
if that is less), as in the corpus run. Stopped part way, it carries on where it stopped when you run it again.

| Option | What it does |
|---|---|
| `--cap GB` | stop a run whose memory passes this (0: no cap) |
| `--time-limit MIN` | stop a run after this many minutes (0: no limit) |
| `--runs simulation/obj,visual/obj` | only these modes and formats, to run failed runs again |
| `--source fixed`, `cap` or `nocap` | marks runs made again: with fixes to KESE, a higher memory cap, or no cap |
| `--kese-commit <commit>` | KESE's commit, when The Main Program is a download, not a clone |

## What it writes, and what it leaves to others

For each board, `Output_Run/<board>/` holds:

- **`board.json`:** the board's project (`owner/repo`), its path (`<owner>__<repo>/<path in the repo>`) and name,
  the commit it was taken at, its counts from its file (copper layers, parts, big chips, BGAs, tracks, vias, the
  KiCad version that wrote it, notes), the KESE features it uses, and a blank license.
- **`runs.jsonl`:** one line per run: its seconds per stage, its file sizes, its peak memory, the Verifier's result,
  the machine and KESE version it ran on, its memory cap and time limit, and the day.

The runner only measures. It never works out a board's score, level, rank, number or folder name, nor makes its
tables, chart or pages: the engine does all of that once the folder is pushed.

**The license is yours to give.** Look up the board's license in its repository, and write it in `license`, with the
day you looked it up in `license_checked` (`YYYY-MM-DD`), or leave both blank. A board with no license given shows
"Not given" in the Credits, unless another board of its project already has one.

**Bad design:** if a run fails the Verifier because the board itself puts copper of two nets on top of each other,
add `bad_design` to its `board.json`, saying where.

Then copy each folder into `corpus-testing/data/` on the corpus-testing branch and push it. A folder without all
six runs is rejected by the engine and deleted.

Nothing put into the three folders is ever committed: KESE, the boards (which belong to their authors) and the
outputs stay on your computer.
