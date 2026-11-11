"""Makes each board's files from its data folder, corpus-testing/data/<name>/ (board.json, runs.jsonl):

    docs/tables/<name>/board.json   what the engine needs: name, project, path, license, complexity ...
    docs/tables/<name>/stages.md    seconds per stage, one row per mode and format
    docs/tables/<name>/facts.md     repo, folder, complexity, layers, format, the Verifier's result ...
    docs/tables/<name>/files.md     the file each run wrote and its peak memory
    docs/images/<name>/stages.webp  the chart, drawn only when it is missing

<name> is the data folder's: <repo>_<board> for a new board, b<number>b_<repo>_<board> once the engine has numbered it.
A board needs a run of each of the six modes and formats in its runs.jsonl: one without is rejected, and its data
folder and every file made from it are deleted. Its rank, score and level are worked out here, from the counts in
its board.json, and written into its tables' board.json.

    python3 corpus-testing/engine/maker/make.py                          every board
    python3 corpus-testing/engine/maker/make.py Thermometer_TheMainBoard  only the boards of these data folders

Then corpus-testing/engine/assemble.py builds the pages. The Corpus Engine workflow runs both on every push.
Needs Python 3.11 or newer with matplotlib and Pillow."""
import collections
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
only = sys.argv[1:]                                         # data folder names, with or without the number
sys.argv = [sys.argv[0], os.path.join(TOP, "corpus-testing", "data", "results"), TOP]
exec(open(os.path.join(HERE, "lib.py")).read())

TABLES = REPO / "docs" / "tables"


def status(b, parts):
    if parts["ok"]: return "pass"
    if b["rank"] in BAD_DESIGN: return "bad_design"
    runs = [run_of(b["rank"], k) for k in KINDS]
    if any(d and not d["ok"] and (d.get("capped") or d["rc"] == -9) for d in runs): return "memory"
    if any(d and not d["ok"] and d["timeout"] for d in runs): return "timeout"
    return "failed"                                   # a fault of KESE: neither the file nor a limit of the measurement


def limits(x):
    """A run's memory cap and time limit: None for none."""
    cap = x.get("cap")
    return [cap if isinstance(cap, (int, float)) and cap != float("inf") else None, x.get("time_limit")]


for s in SKIPPED:
    print("not made:", s)
# a board without all six runs is rejected: its data folder, tables and chart are deleted, so nothing of it stays
for d, why in UNFINISHED:
    for root in (d.parent, TABLES, IMG):
        if (root / d.name).is_dir():
            shutil.rmtree(root / d.name)
    print(f"rejected: {d.name}: {why}; its data folder and every file made from it are deleted")
made = 0
want = [r for r in BOARDS if FOLDER[r] in only or SLUG[r] in only] if only else sorted(BOARDS)
for r in want:
    try:
        b = BOARDS[r]
        parts = board_parts(b)
        runs = [run_of(r, k) for k in KINDS]
        g = grade(b)
        days = sorted({d["date"] for d in runs})
        meta = dict(name=b["name"], project=b["project"], path=b["path"], license=b.get("license"),
                    license_checked=b.get("license_checked"), rank=r, score=b["score"], level=b["level"],
                    complexity=dict(grade=g[0], size=g[1], features=g[2]),
                    features=[k for k, *_ in FEATURES if FEAT.get(r, {}).get(k, 0) > 0],
                    layers=b["layers"], status=status(b, parts), bad_design=BAD_DESIGN.get(r),
                    chart_alt=parts["alt"], rerun={w: v for w, v in parts["rerun"].items() if v},
                    tested=[days[0], days[-1]],
                    kese=sorted({d["machine"]["kese"][:7] for d in runs}),
                    kese_version=sorted({d["machine"]["kese_version"] for d in runs if d["machine"].get("kese_version")}),
                    # every run of the board (one the test machine's restart cut short aside): its source, date, cap, time limit
                    runs=sorted({json.dumps([x["source"], x["date"], *limits(x)]) for x in RUNS[r] if not x.get("runner_died")}),
                    machine=collections.Counter(json.dumps({k: d["machine"][k] for k in ("cpu", "python", "shapely", "geos")},
                                                           sort_keys=True) for d in runs).most_common(1)[0][0])
        meta["machine"] = json.loads(meta["machine"])
        meta["runs"] = [json.loads(x) for x in meta["runs"]]
        text = json.dumps(meta, indent=1, ensure_ascii=False) + "\n"
    except Exception as e:                                  # never a traceback: the board is named, with what went wrong
        print(f"not made: {FOLDER[r]}: {type(e).__name__}: {e}")
        continue
    d = TABLES / FOLDER[r]                                  # named as its data folder
    d.mkdir(parents=True, exist_ok=True)
    (d / "board.json").write_text(text)
    (d / "stages.md").write_text(parts["stages"] + "\n")
    (d / "facts.md").write_text(parts["facts"] + "\n")
    (d / "files.md").write_text(parts["files"] + "\n")
    made += 1
print(made, "boards made")
