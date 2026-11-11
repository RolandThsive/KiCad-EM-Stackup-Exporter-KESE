"""Makes each board's files from the run results in corpus-testing/data/:

    docs/tables/<repo>_<board>/board.json   what the engine needs: name, project, path, license, complexity ...
    docs/tables/<repo>_<board>/stages.md    seconds per stage, one row per mode and format
    docs/tables/<repo>_<board>/facts.md     repo, folder, complexity, layers, format, the Verifier's result ...
    docs/tables/<repo>_<board>/files.md     the file each run wrote and its peak memory
    docs/images/<repo>_<board>/stages.webp  the chart, drawn only when it is missing

    python3 corpus-testing/engine/maker/make.py            every board
    python3 corpus-testing/engine/maker/make.py 2 13 57    only the boards of these ranks

Then corpus-testing/engine/assemble.py (or the Corpus Engine workflow, on a push) builds the pages from them.
Needs Python 3.11 or newer with matplotlib and Pillow."""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
only = [int(a) for a in sys.argv[1:]]
sys.argv = [sys.argv[0], os.path.join(TOP, "corpus-testing", "data", "results"), TOP]
exec(open(os.path.join(HERE, "lib.py")).read())

TABLES = REPO / "docs" / "tables"


def board_dir(root, name):
    """The board's folder under root: b<number>b_<repo>_<board> once the engine has numbered it, else <repo>_<board>
    (a new board, which the engine numbers and renames at its next run)."""
    old = sorted(root.glob(f"b[0-9]*b_{name}"))
    old = [p for p in old if re.fullmatch(r"b\d+b_" + re.escape(name), p.name)]
    return old[0] if old else root / name


def status(b, parts):
    if parts["ok"]: return "pass"
    if b["rank"] in BAD_DESIGN: return "bad_design"
    runs = [run_of(b["rank"], k) for k in KINDS]
    if any(d and not d["ok"] and (d.get("capped") or d["rc"] == -9) for d in runs): return "memory"
    return "failed"


made = 0
for r in (only or sorted(BOARDS)):
    if r not in BOARDS or not all(run_of(r, k) for k in KINDS):
        continue                                            # left out, or not every run done yet
    b = BOARDS[r]
    parts = board_parts(b)
    runs = [run_of(r, k) for k in KINDS]
    g = grade(b)
    meta = dict(name=b["name"], project=b["project"], path=b["path"], license=b.get("license"), rank=r,
                complexity=dict(grade=g[0], size=g[1], features=g[2]),
                features=[k for k, *_ in FEATURES if FEAT.get(r, {}).get(k, 0) > 0],
                layers=b["layers"], status=status(b, parts), bad_design=BAD_DESIGN.get(r),
                chart_alt=parts["alt"], rerun={w: v for w, v in parts["rerun"].items() if v},
                kese=sorted({d["machine"]["kese"][:7] for d in runs}),
                machine=collections.Counter(json.dumps({k: d["machine"][k] for k in ("cpu", "python", "shapely", "geos")},
                                                       sort_keys=True) for d in runs).most_common(1)[0][0])
    meta["machine"] = json.loads(meta["machine"])
    d = board_dir(TABLES, slug(b))
    d.mkdir(parents=True, exist_ok=True)
    (d / "board.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")
    (d / "stages.md").write_text(parts["stages"] + "\n")
    (d / "facts.md").write_text(parts["facts"] + "\n")
    (d / "files.md").write_text(parts["files"] + "\n")
    made += 1
print(made, "boards made")
