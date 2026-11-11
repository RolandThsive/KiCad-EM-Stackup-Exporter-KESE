"""The Corpus Testing engine: builds every Corpus Testing page from the boards' files.

A board is its data folder, corpus-testing/data/<repo>_<board>/ (board.json: its counts, path and license;
runs.jsonl: its runs). The maker (maker/make.py) makes from it the board's tables, docs/tables/<same name>/
(board.json, stages.md, facts.md, files.md), and its chart, docs/images/<same name>/stages.webp; from those this
writes:

    docs/wiki/Corpus-Testing.md                                  the master page
    docs/wiki/CorpusTestingPages/Corpus-Testing-NN.md            Corpus Page NN, 108 boards each
    docs/wiki/CorpusTestingPages/CombinedCorpusTesting.md        every board on one page (not linked)
    docs/wiki/BoardPages/b<number>b_<repo>_<board>.md            one page per board
    docs/wiki/Credits.md, credits.txt                            every board by number, with its project and license

The boards are numbered 1 to n in order of project and then path, at every run. A board added comes as a data folder
named <repo>_<board>, with no number: it goes into its place, and every board after it moves up by one. The engine
renames each folder whose number is no longer right, in corpus-testing/data, docs/tables and docs/images, and writes
every page again. A board whose data folder is deleted is gone: its tables, chart and board page with it, and any page
past the last.

    python3 corpus-testing/engine/maker/make.py && python3 corpus-testing/engine/assemble.py

Needs only Python 3.9 or newer (the maker needs matplotlib and Pillow, for the charts)."""
import collections
import json
import math
import re
import shutil
import textwrap
import sys
from pathlib import Path

TOP = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[2])
TABLES, IMAGES, WIKI = TOP / "docs" / "tables", TOP / "docs" / "images", TOP / "docs" / "wiki"
DATA = TOP / "corpus-testing" / "data"
PAGES, BOARDPAGES = WIKI / "CorpusTestingPages", WIKI / "BoardPages"
PER_PAGE = 108
RAW = "https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images"
WIKI_URL = "https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/"
FEATURES = [tuple(f) for f in json.loads((Path(__file__).resolve().parent / "features.json").read_text())]


def charts():
    """The folders under docs/images that hold a chart."""
    return {p.parent.name for p in IMAGES.glob("*/stages.webp")}


def write(path, text):
    """Writes only what changed, so that a run that changes nothing leaves the files as they were."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file() or path.read_text() != text:
        path.write_text(text)


# ---- a board whose data folder is gone is taken out: its tables and chart go with it
data_boards = {p.name for p in DATA.iterdir() if (p / "board.json").is_file()} if DATA.is_dir() else set()
taken_out = []
if data_boards:                                       # (no data at all is a checkout without it: nothing is taken out)
    for root in (TABLES, IMAGES):
        for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name not in data_boards):
            shutil.rmtree(d)
            if root == TABLES:
                taken_out.append(d.name)
waiting = sorted(n for n in data_boards if not (TABLES / n / "board.json").is_file())   # the maker says why

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
        for root in (TABLES, IMAGES, DATA):
            if (root / m["folder"]).is_dir():
                (root / m["folder"]).rename(root / m["slug"])
        renamed += 1
    m["chart"] = m["folder"] in have_chart
    for part in ("stages", "facts", "files"):
        f = TABLES / m["slug"] / f"{part}.md"
        m[part] = f.read_text().strip() if f.is_file() else ""
NPAGES = max(1, math.ceil(len(B) / PER_PAGE))
page_file = lambda k: f"Corpus-Testing-{k:02d}"
page_title = lambda k: f"Corpus Page {k}"
heading = lambda m: f"{m['number']}. {m['name']}"
anchor = lambda title: "#" + re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")   # as GitHub makes it


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
versions = sorted({v for m in B for v in m.get("kese_version", [])})
mach = collections.Counter(json.dumps(m["machine"], sort_keys=True) for m in B).most_common(1)
mach = json.loads(mach[0][0]) if mach else {}
ver = f"shapely {mach.get('shapely', '2.2.0')} (GEOS {mach.get('geos', '3.14.1')})"
join = lambda xs: ", ".join(xs[:-1]) + (" and " if len(xs) > 1 else "") + (xs[-1] if xs else "")
WORDS = "zero one two three four five six seven eight nine ten eleven twelve".split()
word = lambda n: WORDS[n] if n < len(WORDS) else f"{n:,}"
gb = lambda v: f"{v / 1e9:g} GB"
day = lambda iso: f"{int(iso[8:]):d} {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][int(iso[5:7]) - 1]} {iso[:4]}"


def days(ds, on="on "):
    """A day, or the first and last of several: 10 November 2026; 9 to 10 November 2026."""
    ds = sorted(set(ds))
    if not ds: return ""
    a, z = ds[0], ds[-1]
    if a == z: return on + day(a)
    if a[:7] == z[:7]: return f"{'between ' if on else ''}{int(a[8:])} {'and' if on else 'to'} {day(z)}"
    return f"{'between ' if on else ''}{day(a)} {'and' if on else 'to'} {day(z)}"


def spec(cpu):
    """(cores, GB of RAM) from a machine's cpu entry, "..., 4 cores, 15 GB": the system reports a little under the RAM
    fitted, so it is rounded up to the next 4 GB."""
    c, g = re.search(r"(\d+) cores", cpu), re.search(r"(\d+) GB", cpu)
    return (int(c.group(1)) if c else None, 4 * math.ceil(int(g.group(1)) / 4) if g else None)


specs = collections.Counter(spec(m["machine"].get("cpu", "")) for m in B if m.get("machine"))
on_machine = lambda s: (f"a {s[0]}-core CPU" if s[0] else "a CPU") + (f" with {s[1]} GB of RAM" if s[1] else "")
if len(specs) <= 1:
    s0 = next(iter(specs), (4, 16))
    machine_text = (f"on {on_machine(s0)}, so `Parallel.WORKERS = 0` gave {word(s0[0] or 4)} workers")
else:
    machine_text = ("on " + " or ".join(f"{on_machine(s)} ({n:,} boards)" for s, n in specs.most_common())
                    + ", and `Parallel.WORKERS = 0` gave as many workers as the CPU has cores")
ram_text = lambda: (f"a {specs.most_common(1)[0][0][1]} GB machine" if specs and specs.most_common(1)[0][0][1] else "the test machine")
# the limits each run had, from the runs: [source, date, cap, time limit] of every run of every board
RUNREC = [(m["number"], *x) for m in B for x in m.get("runs", [])]
first = collections.Counter((cap, tl) for _, src, _, cap, tl in RUNREC if src == "corpus")


def limit_words(cap, tl):
    w = ([f"after {tl / 60:g} minutes"] if tl else []) + ([f"once its memory passed {gb(cap)}"] if cap else [])
    return ", or ".join(w)


if first:
    (cap0, tl0), _ = first.most_common(1)[0]
    others = [limit_words(c, t) or "with no limit" for (c, t), _ in first.most_common()[1:]]
    stop_text = ((f"A run was stopped {limit_words(cap0, tl0)}" if limit_words(cap0, tl0) else "A run had no memory cap and no time limit")
                 + (f" (some, {'; '.join(others)})" if others else "")
                 + (": that cap is a limit of the measurement, not of KESE, and a board stopped there "
                    "needs a machine with more memory" if cap0 else "") + ". ")
else:
    cap0, stop_text = None, ""
again = {src: [x for x in RUNREC if x[1] == src] for src in ("fixed", "cap", "nocap")}
how = []
if again["fixed"]: how.append("one that KESE had got wrong, with the fixes to KESE made for it")
if again["cap"]:
    caps = sorted({x[3] for x in again["cap"] if x[3]})
    how.append(f"one stopped at the {gb(cap0) if cap0 else 'memory'} cap, with the cap raised to {' or '.join(gb(c) for c in caps)}")
first_again = days([x[2] for src in ("fixed", "cap") for x in again[src]])
rerun_text = ""
if how or again["nocap"]:
    rerun_text = ("**A run that failed was run again " + first_again + ", with the same settings: " + ", and ".join(how)
                  if how else "**A run that failed was run again")
    if again["nocap"]:
        nc = again["nocap"]
        lim = ("no memory cap" if not any(x[3] for x in nc) else "a higher memory cap") + \
              (" and no time limit" if not any(x[4] for x in nc) else "")
        rerun_text += ((", and, where that was not enough, " if how else " ") + days([x[2] for x in nc]) + f", with {lim} on "
                       f"{ram_text()} with swap added (its seconds then include waiting on the swap)")
    rerun_text += (". A run that passed then shows the new run, and its board says so in a Run again row; a run that failed "
                   "again keeps its first result.**\n")
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
       f"**The runs used KESE version {join(versions) or '2.4.0'} (`main` at {join(kese) or '22fd70c'}) "
       f"with the default parameters otherwise and {ver}, {machine_text} "
       "([Work Done In Parallel](Working-Principle.md#74-work-done-in-parallel)). "
       f"{stop_text}On another machine the seconds differ.**\n",
       rerun_text,
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
text = re.sub(r"\]\(((?!CorpusTestingPages/|BoardPages/|Credits\.md)[A-Za-z0-9-]+)\.md(#[^)]*)?\)",
              lambda m: f"]({WIKI_URL}{m.group(1)}{m.group(2) or ''})", "\n".join(idx))
write(WIKI / "Corpus-Testing.md", text + "\n")

# ---- the Credits page and credits.txt: every board by its number, with its project and the project's license
NOT_YET = "Not looked up yet"
known = {}
for m in B:
    if m.get("license"):
        known.setdefault(m["project"], m["license"])
lic = lambda m: m.get("license") or known.get(m["project"], NOT_YET)      # a board added by hand takes its project's
LOOKED_UP = days([m["license_checked"] for m in B if m.get("license_checked")])
esc = lambda s: re.sub(r"([\\`*_\[\]<>|&])", r"\\\1", s)
gh = lambda p: f"https://github.com/{p}"
CREDITS_TXT = "https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/corpus-testing/credits.txt"
thanks = (f"KESE was checked on {len(B):,} KiCad boards from {len(projects):,} open hardware projects on GitHub. "
          "Thank you to the authors and contributors of every one of them.")
owners = ("Every board belongs to its authors, and so does its license: the rights in each design, and the terms it may "
          "be used under, are theirs alone. Their boards were used only for checking KESE and verifying its determinism "
          "(that the same board and settings give the same files, byte for byte). No board, nor any part of one, is "
          "included in KESE or distributed with it.")
how = ("The license is the one GitHub identifies in the repository (an SPDX identifier); where GitHub names none, it is "
       "what the project's own license files or README say, with the file it is in. \"No license found\" means that "
       "neither the repository's root, the folders of its boards nor its README names one, and the boards remain under "
       "their authors' copyright. Each repository is the authority on its own terms. "
       + (f"The licenses were looked up {LOOKED_UP}" if LOOKED_UP else "The licenses are still to be looked up")
       + (f"; \"{NOT_YET}\" marks a board added since, whose project's license is still to be looked "
                         "up" if any(lic(m) == NOT_YET for m in B) else "") + ".")
cr = ["# Credits\n", thanks + "\n", owners + "\n", "## The Licenses\n", how + "\n",
      f"The repository's [`credits.txt`]({CREDITS_TXT}) holds the same list by project, with the path of each board in "
      "its repository.\n",
      "## The Boards\n",
      f"The {len(B):,} boards by their number in [Corpus Testing](Corpus-Testing.md), in order of project and then path, "
      "each with its project, the project's license and the days its runs were made. A board's name links to its "
      "section on its Corpus Page.\n",
      "| No. | Board | Project | License | Tested |", "|---:|:---|:---|:---|:---|"]
tested = lambda m: days(m["tested"], on="") if m.get("tested") else ""
for m in B:
    cr.append(f"| {m['number']:,} | [{esc(m['name'])}](CorpusTestingPages/{page_file(m['page'])}.md{anchor(heading(m))}) "
              f"| [{esc(m['project'])}]({gh(m['project'])}) | {esc(lic(m))} | {tested(m)} |")
cr.append("\n| Previous | Next |\n|:---|---:|\n| [Corpus Testing](Corpus-Testing.md) | |")
write(WIKI / "Credits.md", "\n".join(cr) + "\n")

fill = lambda s, **k: textwrap.fill(s, 96, break_long_words=False, break_on_hyphens=False, **k)
by_project = {}
for m in B:
    by_project.setdefault(m["project"], []).append(m)
tx = ["Credits: the KiCad boards KESE was checked against", "=" * 51, "", fill(thanks), "", fill(owners), "",
      fill("Below, for each project in the order of Corpus Testing: its repository, its license, and the boards used, "
           "by their number in Corpus Testing, their name, their path in the repository and the days their runs were made. " + how), "", ""]
for p, ms in by_project.items():
    tx += [p, f"  {gh(p)}", fill(lic(ms[0]), initial_indent="  License: ", subsequent_indent=" " * 11),
           f"  {'Board' if len(ms) == 1 else 'Boards'} ({len(ms)}):"]
    tx += [f"    {m['number']}. {m['name']}  ({m['path'].split('/', 1)[-1]})" + (f", tested {tested(m)}" if tested(m) else "")
           for m in ms]
    tx.append("")
write(TOP / "credits.txt", "\n".join(tx))

# ---- the counts in this branch's README
readme = TOP / "README.md"
if readme.is_file():
    t = re.sub(r"[\d,]+ KiCad boards from [\d,]+ open hardware projects",
               f"{len(B):,} KiCad boards from {len(projects):,} open hardware projects", readme.read_text())
    write(readme, re.sub(r"Corpus Page 1 to \d+", f"Corpus Page 1 to {NPAGES}", t))
if taken_out:
    print(f"{len(taken_out)} boards taken out (their data folder is gone): " + ", ".join(taken_out))
if waiting:
    print(f"{len(waiting)} data folders with no board made from them (the maker says why): " + ", ".join(waiting))
print(f"{renamed} folders renamed; {len(B):,} boards on {NPAGES} pages; {len(ok):,} pass all six runs; {len(bad)} bad design, {len(mem)} memory, "
      f"{len(other)} failed")
