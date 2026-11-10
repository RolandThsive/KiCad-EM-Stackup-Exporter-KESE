"""Builds the Corpus Testing page (an index) and its sub-pages of per-board sections, about 100 boards each.
    python3 final.py <results dir> <repo>"""
import sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "build2_lib.py")).read())
PAGEDIR = None
(WIKI / "CorpusTesting").mkdir(parents=True, exist_ok=True)
def save(fig, name):
    png = Path("/tmp") / f"{name}.png"; fig.savefig(png, facecolor=BG); plt.close(fig)
    Image.open(png).convert("RGB").save(IMG / "Corpus-Testing" / PAGEDIR / f"{name}.webp", quality=82, method=6)
# Every board stays on the page it was first put on (PAGE_OF, saved): a board taken out of BOARDS leaves only its own
# page changed, and a board added goes to the page of its project, or else to the last page, or a new one once the
# last holds PER boards.  Within a page the boards are in order of project and path.
PER = 100
PAGE_OF_FILE = Path(HERE) / "page_of_rank.json"
PAGE_OF = {int(r): k for r, k in json.loads(PAGE_OF_FILE.read_text()).items()} if PAGE_OF_FILE.exists() else {}
page_of_project = {BOARDS[r]["project"]: k for r, k in PAGE_OF.items() if r in BOARDS}
for b in sorted(BOARDS.values(), key=lambda b: (b["project"].lower(), b["path"].lower())):
    if b["rank"] in PAGE_OF: continue
    last = max(PAGE_OF.values(), default=1)
    k = page_of_project.get(b["project"]) or (last if sum(1 for v in PAGE_OF.values() if v == last) < PER else last + 1)
    PAGE_OF[b["rank"]] = page_of_project[b["project"]] = k
PAGE_OF_FILE.write_text(json.dumps({str(r): k for r, k in sorted(PAGE_OF.items())}))
groups = collections.defaultdict(list)
for b in sorted(BOARDS.values(), key=lambda b: (b["project"].lower(), b["path"].lower())):
    groups[PAGE_OF[b["rank"]]].append(b)
pages = [(f"Corpus-Testing-{k:02d}", groups[k]) for k in sorted(groups)]
title = lambda k, g: f"Corpus Page {k}"
done = {d["rank"] for d in R.values()}
ver = ", ".join(f"shapely {s} (GEOS {g})" for (s, g, _), _ in versions.most_common(1)) or "shapely 2.2.0 (GEOS 3.14.1)"
cpu = machines.most_common(1)[0][0].split(",")[0] if machines else "an Intel Xeon"
ok6 = len(ok_both)

gr = [grade(b)[0] for b in BOARDS.values()]
idx = [f"# {N}. Corpus Testing\n",
       f"Every board in [Credits](Credits.md), {len(BOARDS):,} KiCad boards from 819 open hardware projects, exported by the "
       "current KESE once for every file format each mode writes, board by board, in the style of the "
       "[Feature Test Collection](Feature-Test-Collection.md):\n",
       "- Each board was run six times, **one file format a run**: in simulation mode with GLB, with STEP, with STL "
       "and with OBJ, and in visual mode with GLB and with OBJ (visual mode is a surface, not solids, so KESE does "
       "not write STEP or STL in it). One format a run gives each format its own time, file size and peak memory.",
       "- Every run had the Verifier, the solder mask and the silkscreen on. Each bar of a board's chart is one "
       "stage's seconds in that run, from the `timing` block of "
       "[`report.txt`](Project-Output-Organization.md#2022-reporttxt).",
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
       f"**The runs used KESE version 2.4.0 (`main` at {', '.join(sorted({k[:7] for k in kese})) or '22fd70c'}) with the "
       f"default parameters otherwise and {ver}, spread over several Linux machines with 4 cores each ({cpu}) and "
       "16 GB of RAM, so `Parallel.WORKERS = 0` gave four workers ([Work Done In "
       "Parallel](Working-Principle.md#74-work-done-in-parallel)). A run was stopped after 90 minutes, or once its "
       "memory passed 11 GB: that cap is a limit of the measurement on these 15 GB machines, not of KESE, and a board "
       "stopped there needs a machine with more memory. On another machine the seconds differ.**\n",
       "**A run that failed was run again on 10 November 2026, with the same settings: one that KESE had got wrong, "
       "with the fixes to KESE made for it, and one stopped at the 11 GB "
       "cap, with the cap raised to 14.5 GB. A run that passed then shows the new run, and its board says so in a "
       "Run again row; a run that failed again keeps its first result.**\n",
       (f"{ok6:,} of the {len(BOARDS):,} boards passed the Verifier in all six runs. The "
        f"{len(BOARDS) - ok6} others are listed by why under [What Did Not Pass](#what-did-not-pass).\n" if len(both) == len(BOARDS) else
        f"The runs are under way: {len(both):,} of the {len(BOARDS):,} boards are done so far. A sub-page is added once all its boards are done.\n"),
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
       *[f"| {name.capitalize()} | {what} | {w} | {sum(1 for r in BOARDS if FEAT.get(r, {}).get(k, 0) > 0):,} |" for k, name, what, w in FEATURES],
       "| **All** | | **500** | |",
       f"\nIn this corpus the grades run from {min(gr)} to {max(gr)}, half the boards below {sorted(gr)[len(gr)//2]}: the "
       "top of the scale is left for boards larger and richer in features than any here. Each board's section gives its "
       "grade as size plus features, and names its features.\n",
       "## The Boards, By Project\n",
       "| Page | Projects | Boards | Boards run | Passed all six runs |", "|---|---|---:|---:|---:|"]
complete = {pg for pg, g in pages if all(b["rank"] in both for b in g)}
for k, (pg, g) in enumerate(pages, 1):
    projs = sorted({b["project"] for b in g}, key=str.lower)
    link = f"[{title(k, g)}](CorpusTesting/{pg}.md)" if pg in complete else f"{title(k, g)} (running)"
    idx.append(f"| {link} | {len(projs)} | {len(g)} | {sum(1 for b in g if b['rank'] in both)} | {sum(1 for b in g if b['rank'] in ok_both)} |")
sect = lambda k, bi, b: "#" + re.sub(r"[^a-z0-9 _-]", "", f"{N}.{k}.{bi} {b['name']}".lower()).replace(" ", "-")   # as GitHub makes it
where = {b["rank"]: f"[{b['name']}](CorpusTesting/{pg}.md{sect(k, bi, b)})" for k, (pg, g) in enumerate(pages, 1) for bi, b in enumerate(g, 1)}
not_ok = [r for r in both if r not in ok_both]
memory = [r for r in not_ok if r not in BAD_DESIGN]
idx += ["\n## What Did Not Pass\n",
        f"Of the {len(BOARDS):,} boards, {len(not_ok)} did not pass in all six runs, none of them for a fault of KESE "
        "(each board's section says what stopped it):\n",
        f"- **Bad design according to KESE ({sum(1 for r in not_ok if r in BAD_DESIGN)} boards):** the file puts copper of two "
        "nets on top of each other, a short KiCad's DRC reports. KESE models what the file says, so the Verifier rightly "
        "finds the two nets' solids overlapping: " + ", ".join(where[r] for r in sorted(not_ok) if r in BAD_DESIGN) + ".",
        f"- **Stopped for memory ({len(memory)} boards):** a run passed the 11 GB cap of the test machines, and again "
        "the 14.3 GB the 16 GB machines allow when run again; they will be run again on a machine with more memory: "
        + ", ".join(where[r] for r in sorted(memory)) + ".",
        f"- **Left out:** {len(CUT_SHORT)} more files of the collection, snapshots in Wren6991 Snowflake-FPGA's `timelapse` "
        "folder, are cut off before their end (each at an exact multiple of 4 KB: copied while KiCad was saving it). KESE "
        "stops on each, as it should (\"the file ends with N parentheses still open: it is cut short\"), and they are not "
        "part of this corpus.\n"]
idx.append("\n| Previous | Next |\n|:---|---:|\n| [Feature Test Collection](Feature-Test-Collection.md) | [openEMS Workflow](OpenEMS-Workflow.md) |")
# the pages of KESE's wiki live on the main branch, not beside this one: linked there
WIKI_URL = "https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/"
text = re.sub(r"\]\(((?!CorpusTesting/)[A-Za-z0-9-]+)\.md(#[^)]*)?\)", lambda m: f"]({WIKI_URL}{m.group(1)}{m.group(2) or ''})", "\n".join(idx))
(WIKI / "Corpus-Testing.md").write_text(text + "\n")

for k, (pg, g) in enumerate(pages, 1):
    PAGEDIR = pg; (IMG / "Corpus-Testing" / pg).mkdir(parents=True, exist_ok=True)
    P = [f"# {N}.{k} {title(k, g)}\n",
         f"Part {k} of {len(pages)} of [Corpus Testing](../Corpus-Testing.md): every board of these projects, six runs "
         "each, one file format a run, as [Corpus Testing](../Corpus-Testing.md) describes.\n"]
    for bi, b in enumerate(g, 1):
        P.append(board_section(b, f"{N}.{k}.{bi}"))
    prev = f"[{title(k - 1, pages[k - 2][1])}]({pages[k - 2][0]}.md)" if k > 1 and pages[k - 2][0] in complete else "[Corpus Testing](../Corpus-Testing.md)"
    nxt = f"[{title(k + 1, pages[k][1])}]({pages[k][0]}.md)" if k < len(pages) and pages[k][0] in complete else "[Corpus Testing](../Corpus-Testing.md)"
    P.append(f"| Previous | Next |\n|:---|---:|\n| {prev} | {nxt} |")
    (WIKI / "CorpusTesting" / f"{pg}.md").write_text("\n".join(P) + "\n")
sizes = [len((WIKI / "CorpusTesting" / f"{pg}.md").read_text()) for pg, _ in pages]
print(len(pages), "pages;", min(sizes), "to", max(sizes), "bytes;", len(R), "runs;", ok6, "boards pass all six")

# one page with every board, kept beside the sub-pages (not linked from the wiki's order)
C = [f"# Combined Corpus Testing\n",
     "Every board of [Corpus Testing](../Corpus-Testing.md) on one page: the same sections as its sub-pages, together.\n"]
for k, (pg, g) in enumerate(pages, 1):
    body = (WIKI / "CorpusTesting" / f"{pg}.md").read_text()
    C.append(body[:body.rindex("| Previous | Next |")].rstrip() + "\n")
(WIKI / "CorpusTesting" / "CombinedCorpusTesting.md").write_text("\n".join(C))
print("combined", len("\n".join(C)), "bytes")

status = [(k, pg, sum(1 for b in g if b["rank"] in both), len(g)) for k, (pg, g) in enumerate(pages, 1)]
json.dump(status, open(Path(HERE) / "status.json", "w"))
print("complete:", [pg for k, pg, d, n in status if d == n])
