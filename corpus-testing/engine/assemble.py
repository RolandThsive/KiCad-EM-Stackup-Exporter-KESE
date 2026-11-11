"""The Corpus Testing engine: builds every Corpus Testing page from the boards' files alone.

A board is a folder docs/tables/b<number>b_<repo>_<board>/ (board.json, stages.md, facts.md, files.md), with its
chart in docs/images/b<number>b_<repo>_<board>/stages.webp when it has one. From those this writes:

    docs/wiki/Corpus-Testing.md                                  the master page
    docs/wiki/CorpusTestingPages/Corpus-Testing-NN.md            Corpus Page NN, 108 boards each
    docs/wiki/CorpusTestingPages/CombinedCorpusTesting.md        every board on one page (not linked)
    docs/wiki/BoardPages/b<number>b_<repo>_<board>.md            one page per board

The boards are numbered 1 to n in order of project and then path, at every run. A board added comes as folders
named <repo>_<board>, with no number: it goes into its place, and every board after it moves up by one. The engine
renames each folder whose number is no longer right, in both docs/tables and docs/images, and writes every page
again. A board whose folders are deleted is gone, and so are its board page and any page past the last.

    python3 corpus-testing/engine/assemble.py [<top of the corpus-testing branch>]

Needs only Python 3.9 or newer: no run results, no drawing."""
import collections
import json
import math
import re
import sys
from pathlib import Path

TOP = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[2])
TABLES, IMAGES, WIKI = TOP / "docs" / "tables", TOP / "docs" / "images", TOP / "docs" / "wiki"
PAGES, BOARDPAGES = WIKI / "CorpusTestingPages", WIKI / "BoardPages"
PER_PAGE = 108
RAW = "https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images"
WIKI_URL = "https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/"
FEATURES = [tuple(f) for f in json.loads((Path(__file__).resolve().parent / "features.json").read_text())]


def charts():
    """The folders under docs/images that hold a chart."""
    return {p.parent.name for p in IMAGES.glob("*/stages.webp")}


# ---- the boards, numbered in order of project and path; each folder named b<number>b_<repo>_<board>
PREFIX = re.compile(r"b(\d+)b_(.+)")
B = []
for d in sorted(p for p in TABLES.iterdir() if (p / "board.json").is_file()):
    m = json.loads((d / "board.json").read_text())
    pm = PREFIX.fullmatch(d.name)
    m["key"], m["folder"] = (pm.group(2) if pm else d.name), d.name     # a folder with no prefix is a new board
    B.append(m)
B.sort(key=lambda m: (m["project"].lower(), m["path"].lower()))
WIDTH = max(4, len(str(len(B))))
have_chart = charts()
renamed = 0
for i, m in enumerate(B, 1):
    m["number"] = i
    m["page"] = (i - 1) // PER_PAGE + 1
    m["slug"] = f"b{i:0{WIDTH}d}b_{m['key']}"
    if m["folder"] != m["slug"]:                                       # a new board, or one whose number moved
        (TABLES / m["folder"]).rename(TABLES / m["slug"])
        if (IMAGES / m["folder"]).is_dir():
            (IMAGES / m["folder"]).rename(IMAGES / m["slug"])
        renamed += 1
    m["chart"] = m["folder"] in have_chart
    for part in ("stages", "facts", "files"):
        f = TABLES / m["slug"] / f"{part}.md"
        m[part] = f.read_text().strip() if f.is_file() else ""
NPAGES = max(1, math.ceil(len(B) / PER_PAGE))
page_file = lambda k: f"Corpus-Testing-{k:02d}"
page_title = lambda k: f"Corpus Page {k}"
heading = lambda m: f"{m['number']} {m['name']}"
anchor = lambda title: "#" + re.sub(r"[^a-z0-9 _-]", "", title.lower()).replace(" ", "-")   # as GitHub makes it


def body(m):
    """A board's chart and its three tables, as the Feature Test Collection shows a board."""
    out = []
    if m["chart"]:
        out.append(f"![{m['chart_alt']}]({RAW}/{m['slug']}/stages.webp)\n")
    out.append(m["stages"])
    out.append('\n<table align="center"><tr><td valign="top">\n')
    out.append(m["facts"])
    out.append('\n</td><td valign="top">\n')
    out.append(m["files"])
    out.append("\n</td></tr></table>\n")
    return "\n".join(out)


def write(path, text):
    """Writes only what changed, so that a run that changes nothing leaves the files as they were."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file() or path.read_text() != text:
        path.write_text(text)


# ---- the corpus pages, 108 boards each, and the combined page
for k in range(1, NPAGES + 1):
    g = [m for m in B if m["page"] == k]
    P = [f"# {page_title(k)}\n",
         f"Part {k} of {NPAGES} of [Corpus Testing](../Corpus-Testing.md): boards {g[0]['number']:,} to "
         f"{g[-1]['number']:,}, six runs each, one file format a run, as [Corpus Testing](../Corpus-Testing.md) "
         "describes.\n" if g else ""]
    for m in g:
        P.append(f"## {heading(m)}\n")
        P.append(body(m))
    prev = f"[{page_title(k - 1)}]({page_file(k - 1)}.md)" if k > 1 else "[Corpus Testing](../Corpus-Testing.md)"
    nxt = f"[{page_title(k + 1)}]({page_file(k + 1)}.md)" if k < NPAGES else "[Corpus Testing](../Corpus-Testing.md)"
    P.append(f"| Previous | Next |\n|:---|---:|\n| {prev} | {nxt} |")
    write(PAGES / f"{page_file(k)}.md", "\n".join(P) + "\n")
for f in PAGES.glob("Corpus-Testing-*.md"):
    n = re.fullmatch(r"Corpus-Testing-(\d+)\.md", f.name)
    if n and int(n.group(1)) > NPAGES:
        f.unlink()
C = ["# Combined Corpus Testing\n",
     "Every board of [Corpus Testing](../Corpus-Testing.md) on one page: the same sections as its Corpus Pages, together.\n"]
for m in B:
    C += [f"## {heading(m)}\n", body(m)]
write(PAGES / "CombinedCorpusTesting.md", "\n".join(C))

# ---- one page per board
for i, m in enumerate(B):
    k = m["page"]
    P = [f"# {heading(m)}\n",
         f"Board {m['number']:,} of the {len(B):,} of [Corpus Testing](../Corpus-Testing.md), on "
         f"[{page_title(k)}](../CorpusTestingPages/{page_file(k)}.md{anchor(heading(m))}).\n",
         body(m)]
    prev = f"[{heading(B[i - 1])}]({B[i - 1]['slug']}.md)" if i > 0 else "[Corpus Testing](../Corpus-Testing.md)"
    nxt = f"[{heading(B[i + 1])}]({B[i + 1]['slug']}.md)" if i + 1 < len(B) else "[Corpus Testing](../Corpus-Testing.md)"
    P.append(f"| Previous | Next |\n|:---|---:|\n| {prev} | {nxt} |")
    write(BOARDPAGES / f"{m['slug']}.md", "\n".join(P) + "\n")
keep = {f"{m['slug']}.md" for m in B}
for f in BOARDPAGES.glob("*.md"):
    if f.name not in keep:
        f.unlink()

# ---- the master page
where = lambda m: f"[{m['name']}](CorpusTestingPages/{page_file(m['page'])}.md{anchor(heading(m))})"
ok = [m for m in B if m["status"] == "pass"]
gr = sorted(m["complexity"]["grade"] for m in B)
projects = {m["project"] for m in B}
kese = sorted({c for m in B for c in m["kese"]})
mach = collections.Counter(json.dumps(m["machine"], sort_keys=True) for m in B).most_common(1)
mach = json.loads(mach[0][0]) if mach else {}
ver = f"shapely {mach.get('shapely', '2.2.0')} (GEOS {mach.get('geos', '3.14.1')})"
cpu = mach.get("cpu", "an Intel Xeon").split(",")[0]
rerun_any = {w for m in B for w in m.get("rerun", {})}
idx = ["# Corpus Testing\n",
       f"Every board in [Credits](Credits.md), {len(B):,} KiCad boards from {len(projects):,} open hardware projects, "
       "exported by the current KESE once for every file format each mode writes, board by board, in the style of the "
       "[Feature Test Collection](Feature-Test-Collection.md):\n",
       "- Each board was run six times, **one file format a run**: in simulation mode with GLB, with STEP, with STL "
       "and with OBJ, and in visual mode with GLB and with OBJ (visual mode is a surface, not solids, so KESE does "
       "not write STEP or STL in it). One format a run gives each format its own time, file size and peak memory.",
       "- Every run had the Verifier, the solder mask and the silkscreen on. Each bar of a board's chart is one "
       "stage's seconds in that run, from the `timing` block of "
       "[`report.txt`](Project-Output-Organization.md#1122-reporttxt).",
       "- Beside each board's facts, the file each run wrote (STL: all the part files of the run together) and the "
       "run's peak memory: the proportional set size (PSS) of KESE and its four workers summed, so shared memory is "
       "counted once, sampled every 0.05 s.",
       "- No picture of any board is shown: the boards belong to their authors ([Credits](Credits.md)), and none of "
       "them, nor any part of one, is included in KESE.",
       "- The commands, for a board B and a format F (glb, step, stl or obj in simulation mode; glb or obj in visual "
       "mode):\n",
       "```text\npython run_KESE.py B --mode simulation --format F --verify \\\n"
       "    --set SolderMask.SOLDER_MASK_ENABLED=True --set Silkscreen.SILKSCREEN_ENABLED=True\n"
       "python run_KESE.py B --mode visual --format F --verify \\\n"
       "    --set SolderMask.SOLDER_MASK_ENABLED=True --set Silkscreen.SILKSCREEN_ENABLED=True\n```\n",
       f"**The runs used KESE version 2.4.0 (`main` at {', '.join(kese) or '22fd70c'}) with the default parameters "
       f"otherwise and {ver}, spread over several Linux machines with 4 cores each ({cpu}) and 16 GB of RAM, so "
       "`Parallel.WORKERS = 0` gave four workers ([Work Done In Parallel](Working-Principle.md#74-work-done-in-parallel)). "
       "A run was stopped after 90 minutes, or once its memory passed 11 GB: that cap is a limit of the measurement on "
       "these 15 GB machines, not of KESE, and a board stopped there needs a machine with more memory. On another "
       "machine the seconds differ.**\n",
       "**A run that failed was run again on 10 November 2026, with the same settings: one that KESE had got wrong, with the fixes to KESE "
       "made for it, and one stopped at the 11 GB cap, with the cap raised to 14.5 GB"
       + (", and, where that was not enough, with no memory cap and no time limit on a 15 GB machine with swap added "
          "(its seconds then include waiting on the swap)" if "nocap" in rerun_any else "")
       + ". A run that passed then shows the new run, and its board says so in a Run again row; a run that failed "
       "again keeps its first result.**\n",
       f"{len(ok):,} of the {len(B):,} boards passed the Verifier in all six runs. The {len(B) - len(ok)} others are "
       "listed by why under [What Did Not Pass](#what-did-not-pass).\n",
       "## Grading A Board's Complexity\n",
       "Each board's Complexity is a grade from 0 to 1000: its **size**, from 0 to 500, plus the **features** of it "
       "that KESE models, from 0 to 500. Both are counted from the `.kicad_pcb` file alone, with fixed tops and weights, "
       "so any KiCad board can be graded the same way and a board added to the corpus later is graded on this scale.\n",
       "```text\ngrade = size + features\n```\n",
       "### The Size\n",
       "Four counts, each on a log scale with a fixed top:\n",
       "```text\nsize = 200 × log10(1 + tracks + 3 × vias) / log10(1 + 200,000)\n"
       "     + 100 × log10(1 + parts) / log10(1 + 10,000)\n"
       "     + 100 × log10(1 + 60 × big chips + 150 × BGAs) / log10(1 + 30,000)\n"
       "     + 100 × log2(copper layers) / 6\n```\n",
       "Each of the four terms is at most its top (200, 100, 100, 100), and the sum is rounded.\n",
       "- **tracks**: routed copper track segments and arcs. **vias**: vias of every kind.\n"
       "- **parts**: footprints with two or more pads (mounting holes, fiducials, logos and stitching vias are not counted).\n"
       "- **big chips**: chips of 32 pads or more in QFP, QFN, BGA, LGA or DIMM-style packages.\n"
       "- **BGAs**: BGA, LGA or CSP chips of 25 pads or more, counted again on top of the big chips.\n"
       "- **copper layers**: points as in the table below.\n",
       "| Copper layers | 1 | 2 | 4 | 6 | 8 | 10 | 12 | 16 | 32 | 64 |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
       "| Points | 0 | 17 | 33 | 43 | 50 | 55 | 60 | 67 | 83 | 100 |\n",
       "Ten times the routing adds about 38 to the size, ten times the parts about 25 and ten times the chips about 22.\n",
       "### The Features\n",
       "Each feature KESE models that the board uses adds its weight once, however many times it is used. The weights "
       "add up to 500: the rarer and harder a feature is to model (vias between inner layers, backdrills, plated edges), "
       "the more it weighs.\n",
       "```text\nfeatures = the sum of the weights of the features present\n```\n",
       "| Feature | Present when the file has | Weight | Boards in this corpus |", "|---|---|---:|---:|",
       *[f"| {name.capitalize()} | {what} | {w} | {sum(1 for m in B if k in m['features']):,} |"
         for k, name, what, w in FEATURES],
       "| **All** | | **500** | |",
       (f"\nIn this corpus the grades run from {gr[0]} to {gr[-1]}, half the boards below {gr[len(gr) // 2]}: the "
        "top of the scale is left for boards larger and richer in features than any here. Each board's section gives "
        "its grade as size plus features, and names its features.\n" if gr else ""),
       "## The Boards, By Project\n",
       f"The boards are numbered in order of project and then path, {PER_PAGE} to a page.\n",
       "| Page | Boards | Projects | Passed all six runs |", "|---|---|---:|---:|"]
for k in range(1, NPAGES + 1):
    g = [m for m in B if m["page"] == k]
    if g:
        idx.append(f"| [{page_title(k)}](CorpusTestingPages/{page_file(k)}.md) | {g[0]['number']:,} to {g[-1]['number']:,} "
                   f"| {len({m['project'] for m in g})} | {sum(1 for m in g if m['status'] == 'pass')} |")
bad = [m for m in B if m["status"] == "bad_design"]
mem = [m for m in B if m["status"] == "memory"]
other = [m for m in B if m["status"] == "failed"]
idx += ["\n## What Did Not Pass\n",
        f"Of the {len(B):,} boards, {len(B) - len(ok)} did not pass in all six runs"
        + (", none of them for a fault of KESE" if not other else "") + " (each board's section says what stopped it):\n"]
if bad:
    idx.append(f"- **Bad design according to KESE ({len(bad)} boards):** the file puts copper of two nets on top of each "
               "other, a short KiCad's DRC reports. KESE models what the file says, so the Verifier rightly finds the "
               "two nets' solids overlapping: " + ", ".join(where(m) for m in sorted(bad, key=lambda m: m["rank"])) + ".")
if mem:
    idx.append(f"- **Stopped for memory ({len(mem)} boards):** a run passed the memory the test machines allow, and again "
               "when run again; they will be run again on a machine with more memory: "
               + ", ".join(where(m) for m in sorted(mem, key=lambda m: m["rank"])) + ".")
if other:
    idx.append(f"- **Failed ({len(other)} boards):** " + ", ".join(where(m) for m in sorted(other, key=lambda m: m["rank"])) + ".")
idx.append("\n| Previous | Next |\n|:---|---:|\n| [Feature Test Collection](Feature-Test-Collection.md) "
           "| [Parameter Reference](Parameter-Reference.md) |")
# the pages of KESE's wiki live on the main branch, not beside this one: linked there
text = re.sub(r"\]\(((?!CorpusTestingPages/|BoardPages/)[A-Za-z0-9-]+)\.md(#[^)]*)?\)",
              lambda m: f"]({WIKI_URL}{m.group(1)}{m.group(2) or ''})", "\n".join(idx))
write(WIKI / "Corpus-Testing.md", text + "\n")
print(f"{renamed} folders renamed; {len(B):,} boards on {NPAGES} pages; {len(ok):,} pass all six runs; {len(bad)} bad design, {len(mem)} memory, "
      f"{len(other)} failed")
