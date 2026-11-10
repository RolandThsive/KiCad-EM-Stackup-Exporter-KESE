"""Builds docs/wiki/Corpus-Testing.md and its charts from the workers' results (results/W*.jsonl).
    python3 build.py <results dir> <repo>
The prose that depends on the results is written from the numbers; read the page through after each build."""
import collections, json, math, re, statistics, sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image

RES = Path(sys.argv[1]); REPO = Path(sys.argv[2]); IMG = REPO / "docs/images"; WIKI = REPO / "docs/wiki"
RAW = "https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/corpus-testing/docs/images"
DATA = Path(HERE).parent / "data"
SCORES = DATA / "kicad_board_complexity_scores.txt"
N = 23  # the page's number in the wiki's order
for f in fm.findSystemFonts():
    if "/inter/Inter-" in f: fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Inter"
BG, INK, SOFT, GRID = "#fcfcfb", "#1a1a1a", "#5f5e5b", "#e4e3df"
BARS = [("1–2 read", ("read", "collect"), "#2a78d6"), ("3 resolve", ("resolve",), "#eb6834"),
        ("4 geometry", ("geometry",), "#1baf7a"), ("5 materials", ("materials",), "#eda100"),
        ("6 assemble", ("assemble",), "#e87ba4"), ("7 write", ("write",), "#008300"),
        ("8 verify", ("verify",), "#6250d6"), ("start-up and exit", None, "#e34948")]
KEYS = [b[0] for b in BARS]
WHITE = {"#2a78d6", "#6250d6", "#008300", "#e34948"}
MODES = [("simulation/glb", "Simulation, GLB"), ("simulation/step", "Simulation, STEP"),
         ("simulation/stl", "Simulation, STL"), ("simulation/obj", "Simulation, OBJ"),
         ("visual/glb", "Visual, GLB"), ("visual/obj", "Visual, OBJ")]
KINDS = [k for k, _ in MODES]
SHORT = {"simulation": "simulation, all four", "visual": "visual, GLB + OBJ"}
LEVELS = ["EXTREME", "VERY HIGH", "HIGH", "MEDIUM", "LOW", "SIMPLE"]
LEVEL_RANGE = {"EXTREME": "20,000 and over", "VERY HIGH": "8,000 to 19,999", "HIGH": "3,000 to 7,999",
               "MEDIUM": "1,000 to 2,999", "LOW": "250 to 999", "SIMPLE": "under 250"}


def fmt(v):
    if v < 0.001: return f"{v*1000:.1f} ms"
    if v < 0.0995: return f"{v*1000:.0f} ms"
    return f"{v:.1f}"


def secs(v):
    if v >= 3600: return f"{v/3600:.1f} h"
    if v >= 99.5: return f"{v/60:.0f} min"
    if v >= 9.95: return f"{v:.0f} s"
    return f"{v:.1f} s"


def size(b):
    for u, d in (("GB", 1e9), ("MB", 1e6), ("kB", 1e3)):
        if b >= d: return f"{b/d:.1f} {u}" if b < 10 * d else f"{b/d:.0f} {u}"
    return f"{b} B"


def anchor(title):
    return "#" + re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


# ---- the corpus: every board's numbers from the complexity list
lines = open(SCORES).read().splitlines()
hdr = next(l for l in lines if l.startswith("RANK"))
cN, cP = hdr.index("NOTES"), hdr.index("PATH INSIDE ZIP")
BOARDS = {}
for l in lines:
    m = re.match(r"\s*(\d+)\s+(\d+)\s+(EXTREME|VERY HIGH|HIGH|MEDIUM|LOW|SIMPLE)\s", l)
    if not m or len(l) <= cP: continue
    num = l[:cN].split()
    path = l[cP:].strip()
    BOARDS[int(m.group(1))] = dict(rank=int(m.group(1)), score=int(m.group(2)), level=m.group(3), layers=int(num[-10]),
                                   parts=int(num[-9]), big=int(num[-8]), bga=int(num[-7]), tracks=int(num[-6]), vias=int(num[-5]), size_mb=float(num[-3]),
                                   kicad=int(num[-2]), notes=l[cN:cP].strip(), path=path,
                                   project=path.split("/")[0].replace("__", "/", 1), name=Path(path).stem)
assert len(BOARDS) == 3146
# the boards taken out of the corpus, and those that are a bad design according to KESE: corpus_boards.json
_CFG = json.loads((Path(HERE) / "corpus_boards.json").read_text())
CUT_SHORT = {int(r) for r in _CFG["left_out"]}
BAD_DESIGN = {int(r): why for r, why in _CFG["bad_design"].items()}
for _r in CUT_SHORT: BOARDS.pop(_r, None)

def _clean(t): return re.sub(r"-+", "-", re.sub(r"[^A-Za-z0-9-]+", "-", t)).strip("-")
_base = {r: _clean(b["project"].split("/")[1]) + "_" + _clean(b["name"]) for r, b in BOARDS.items()}
_cnt = collections.Counter(_base.values())
SLUG = {}
for r, b in BOARDS.items():
    if _cnt[_base[r]] == 1: SLUG[r] = _base[r]
    else:
        mid = _clean("-".join(b["path"].split("/")[1:-1]))
        SLUG[r] = _base[r].split("_", 1)[0] + ("_" + mid if mid else "") + "_" + _clean(b["name"])
_c2 = collections.Counter(SLUG.values())
for r in SLUG:
    if _c2[SLUG[r]] > 1: SLUG[r] += f"_{r}"
assert len(set(SLUG.values())) == len(SLUG)

# ---- the runs
R = {}
import datetime as _dt, bisect as _bs
_SNAP = collections.defaultdict(list)          # file -> [(line count, UTC date)], from the line-count log taken every 2 minutes
for _l in open(DATA / "linecounts.log"):
    _t, _f, _n = _l.split()
    _SNAP[_f].append((int(_n), _t[:10]))
_FIRST = "2026-11-09"                          # results4 was started on 9 November 2026, before the log began
def _run_date(fname, i):
    for n, day in _SNAP.get(fname, []):
        if n >= i: return day
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")
for f in sorted(RES.glob("W*.jsonl")) + sorted(RES.glob("RERUN*.jsonl")):   # a rerun replaces a run whose runner was stopped
    for i, l in enumerate(open(f), 1):
        try: d = json.loads(l)
        except Exception: continue
        if d.get("runner_died") and d["tag"] in R: continue
        d["date"] = _run_date(f.name, i) if _SNAP.get(f.name) else _FIRST
        R[d["tag"]] = d
# a run that failed and passes when run again, with the corpus fixes (FIXED*.jsonl) or under the raised
# 14.5 GB memory cap (C*.jsonl), takes the new run's place; a run that fails again keeps its first record
FIXES = RES.parent / "fixes"
for f, why in [(p, "fixed") for p in sorted(FIXES.glob("FIXED[23]*.jsonl"))] + [(p, "cap") for p in sorted(FIXES.glob("C[0-9]*.jsonl"))]:
    for l in open(f):
        try: d = json.loads(l)
        except Exception: continue
        old = R.get(d["tag"])
        if old is None or (old["rc"] == 0 and "PASS" in old["verifier"]): continue
        if not (d["rc"] == 0 and "PASS" in (d.get("verifier") or "")): continue
        d["date"], d["rerun"] = "2026-11-10", why
        R[d["tag"]] = d
R = {t: d for t, d in R.items() if d["rank"] not in CUT_SHORT}
for d in R.values():
    d["wall"] = d.get("wall") or 0
    st = {}
    for k, v in d["stages"]: st[k] = st.get(k, 0) + v
    d["bars"] = {name: sum(st.get(k, 0) for k in keys) for name, keys, _ in BARS if keys}
    d["bars"]["start-up and exit"] = max(d["wall"] - sum(st.values()), 0) if st else 0
    d["ok"] = d["rc"] == 0 and "PASS" in d["verifier"]
    d["board"] = BOARDS[d["rank"]]
    d["kind"] = f"{d['mode']}/{d['format']}"
runs = {m: [d for d in R.values() if d["kind"] == m] for m, _ in MODES}
run_of = lambda rank, kind: R.get(f"{rank:04d}/{kind}")
done_ranks = {d["rank"] for d in R.values()}
both = [r for r in BOARDS if all(run_of(r, k) for k in KINDS)]
ok_both = [r for r in both if all(run_of(r, k)["ok"] for k in KINDS)]
machines = collections.Counter(d["machine"]["cpu"] for d in R.values())
versions = collections.Counter((d["machine"]["shapely"], d["machine"]["geos"], d["machine"]["python"]) for d in R.values())
kese = {d["machine"]["kese"] for d in R.values()}


def outcome(d):
    if d is None: return "not run"
    if d["timeout"]: return "time-out (90 minutes)"
    if d.get("capped"): return (f"exceeded {size(d.get('cap') or 11e9)} on a 15 GB machine (stopped there, not a KESE failure); "
                                "it will be run again on a machine with more memory")
    if d.get("runner_died"): return "interrupted: the test machine restarted during the run (not a KESE result)"
    if d["rc"] == -9: return "ran out of memory on a 15 GB machine; it will be run again on a machine with more memory"
    if d["rc"] != 0:
        err = next((l for l in reversed(d["log"].splitlines()) if l.strip()), "")
        return "error: " + re.sub(r"^\w+Error: ", "", err).strip()
    if "PASS" in d["verifier"] and d.get("rerun") == "fixed": return "PASS (run again with the corpus fixes)"
    if "PASS" in d["verifier"] and d.get("rerun") == "cap": return "PASS (run again with a 14.5 GB memory cap)"
    if "PASS" in d["verifier"]: return "PASS"
    return d["verifier"].replace("Verifier: ", "Verifier ") or "no Verifier line"


def medians(ds):
    """The median of each stage over the runs, the total the sum of the bars (as the Feature Test Collection)."""
    med = {k: statistics.median([d["bars"][k] for d in ds]) for k in KEYS}
    return {"stages": med, "total": sum(med.values())}


# ---- charts
def stacked(rows, head, sub, png_name, label_w=0.25):
    """rows: [(label, {stage: seconds})], FTC-style stacked bars, thin stages marked with a line and a label."""
    tmax = max(sum(s.values()) for _, s in rows)
    h = 1.6 + 0.62 * len(rows)
    fig = plt.figure(figsize=(10, h), dpi=200, facecolor=BG)
    top = 1 - 1.15 / h
    ax = fig.add_axes([label_w, 0.36 / h * 1.4, 0.93 - label_w, top - 0.36 / h * 1.4 - 0.32 / h], facecolor=BG)
    fig.text(0.024, 1 - 0.32 / h, head, fontsize=15.5, fontweight="semibold", color=INK, va="center")
    fig.text(0.024, 1 - 0.6 / h, sub, fontsize=11, color=SOFT, va="center")
    x = 0.024
    for name, _, col in BARS:
        fig.patches.append(matplotlib.patches.Rectangle((x, 1 - 0.94 / h), 0.012, 0.115 / h, transform=fig.transFigure, color=col))
        t = fig.text(x + 0.019, 1 - 0.885 / h, name, fontsize=11, color=INK, va="center")
        fig.canvas.draw(); bb = t.get_window_extent().transformed(fig.transFigure.inverted()); x = bb.x1 + 0.026
    xmax = tmax * 1.15
    fig.canvas.draw()
    px_per_s = ax.get_window_extent().width / xmax
    n = len(rows)
    for i, (label, st) in enumerate(rows):
        y = n - 1 - i; left = 0; thin = []
        for name, _, col in BARS:
            v = st[name]; wpx = v * px_per_s
            if wpx < 12: thin.append((left + v / 2, name, v, col))
            ax.barh(y, v, left=left, height=0.56, color=col, edgecolor=BG, linewidth=1.2 if wpx >= 12 else 0)
            if wpx > (75 if "ms" in fmt(v) else 46):
                ax.text(left + v / 2, y, fmt(v), ha="center", va="center", fontsize=10.5, color="white" if col in WHITE else INK)
            left += v
        nextfree = -1e9
        for xc, name, v, col in thin:
            if v < 0.0005 and name != "5 materials": continue
            ax.plot([xc, xc], [y - 0.28, y + 0.28], color=col, linewidth=2.2, solid_capstyle="butt", zorder=5)
            t = ax.text(max(xc, nextfree), y + 0.34, f"{name}: {fmt(v) if v < 0.0995 else fmt(v) + ' s'}",
                        ha="left", va="bottom", fontsize=9.5, color=SOFT)
            fig.canvas.draw()
            nextfree = max(t.get_window_extent(renderer=fig.canvas.get_renderer()).transformed(ax.transData.inverted()).x1,
                           max(xc, nextfree) + len(t.get_text()) * xmax * 0.0115) + xmax * 0.02
        ax.text(left + tmax * 0.012, y, secs(left), va="center", fontsize=11.5, color=INK)
    ax.set_yticks(list(range(n - 1, -1, -1)), [r[0] for r in rows], fontsize=11, color=INK)
    ax.set_xlim(0, xmax); ax.set_ylim(-0.5, n - 0.25)
    ax.tick_params(axis="y", length=0, pad=10); ax.tick_params(axis="x", length=0, colors=SOFT, labelsize=10.5, pad=6)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g} s"))
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    ax.grid(axis="x", color=GRID, linewidth=1); ax.set_axisbelow(True)
    for s_ in ax.spines.values(): s_.set_visible(False)
    save(fig, png_name)


def save(fig, name):
    png = Path("/tmp") / f"{name}.png"
    fig.savefig(png, facecolor=BG); plt.close(fig)
    Image.open(png).convert("RGB").save(IMG / f"{name}.webp", quality=82, method=6)



def brk(v, n=34):
    """A value over n characters breaks at the comma that evens the two lines."""
    if len(v) <= n or ", " not in v: return v
    cuts = [i for i in range(len(v)) if v.startswith(", ", i)]
    i = min(cuts, key=lambda i: abs(len(v) - 2 * i))
    return v[:i + 1] + "<br>" + v[i + 2:]



# ---- per-board sections
SUB = "Seconds per stage, one run per format, 4 cores, the Verifier, mask and silkscreen on"
FNAME = {"glb": "GLB", "step": "STEP", "stl": "STL", "obj": "OBJ"}


FEATURES = [  # (key in features.json, name on the page, what is counted in the .kicad_pcb file, weight)
    ("through_vias", "through vias", "`(via (at ...` with no type", 15),
    ("blind_buried_vias", "blind and buried vias", "`(via blind ...`, `(via buried ...`", 40),
    ("microvias", "microvias", "`(via micro ...`", 40),
    ("backdrills", "backdrills", "`(backdrill ...`, `(tertiary_drill ...`", 40),
    ("counterbores_countersinks", "counterbores and countersinks", "`(front_post_machining counterbore ...`, and `countersink`, front or back", 25),
    ("via_protection", "covered, plugged, capped or filled vias", "`(covering ...)` or `(plugging ...)` with a `yes`, `(capping yes)`, `(filling yes)`", 30),
    ("padstacks", "padstacks", "`(padstack ...`", 30),
    ("slotted_holes", "slotted holes", "`(drill oval ...`", 10),
    ("custom_pads", "custom pads", "a pad of shape `custom`", 15),
    ("shaped_pads", "rounded, trapezoid or chamfered pads", "a pad of shape `roundrect` or `trapezoid`, or `(chamfer ...`", 10),
    ("drill_offsets", "drill offsets", "`(drill ... (offset ...))`", 10),
    ("arc_tracks", "arc tracks", "`(arc (start ...` (KiCad 6 and later)", 15),
    ("filled_zones", "filled zones", "`(filled_polygon ...` or `(fill_segments ...`", 20),
    ("copper_graphics", "copper drawings", "a `gr_line`, `gr_arc`, `gr_circle`, `gr_rect`, `gr_poly` or `gr_curve` on a copper layer", 10),
    ("copper_text", "copper text", "a `gr_text` on a copper layer", 10),
    ("curved_outline", "curved board outline", "an arc, circle or curve on `Edge.Cuts`", 10),
    ("knockout_text", "knockout text", "`knockout`", 15),
    ("truetype_text", "TrueType text", "`(face \"...\")` other than `\"KiCad Font\"`", 15),
    ("hatched_fills", "hatched fills", "`(fill hatch)`", 25),
    ("bare_copper_tracks", "tracks bare of mask", "a `segment` with `(layers \"F.Cu\" \"F.Mask\")` or the back's", 15),
    ("stackup", "stack-up", "`(stackup ...`", 20),
    ("dielectric_properties", "dielectric εr and tanδ", "`(epsilon_r ...`", 10),
    ("copper_finish", "copper finish", "`(copper_finish ...)` other than `None`", 15),
    ("mask_silk_colours", "mask and silkscreen colours", "a `(color ...)` on a mask or silkscreen layer of the stack-up", 5),
    ("castellated_pads", "castellated pads", "`pad_prop_castellated` or `(castellated_pads yes)`", 25),
    ("edge_plating", "plated board edge", "`(edge_plating yes)`", 25),
]
assert sum(w for *_, w in FEATURES) == 500
FEAT = {int(k): v for k, v in json.load(open(DATA / "features.json")).items()}


def grade(b):
    """The complexity grade, 0 to 1000: the size (0 to 500), four parts each on a log scale with a fixed top, plus
    the features KESE models that the board uses (0 to 500), each with its weight. Fixed, so a board added later is
    graded on the same scale. Returns (total, size, features, [names of the features present])."""
    L = lambda x, top: min(1.0, math.log10(1 + x) / math.log10(1 + top))
    size = round(200 * L(b["tracks"] + 3 * b["vias"], 200_000) + 100 * L(b["parts"], 10_000)
                 + 100 * L(60 * b["big"] + 150 * b["bga"], 30_000) + 100 * min(1.0, math.log2(max(b["layers"], 1)) / 6))
    f = FEAT.get(b["rank"], {})
    have = [(name, w) for k, name, _, w in FEATURES if f.get(k, 0) > 0]
    feats = sum(w for _, w in have)
    return size + feats, size, feats, [n for n, _ in have]


def wrap(v, n=34):
    """Breaks a comma list into lines of about n characters."""
    out, line = [], ""
    for w in v.split(", "):
        if line and len(line) + 2 + len(w) > n: out.append(line + ","); line = w
        else: line = f"{line}, {w}" if line else w
    return "<br>".join(out + [line])


def nice_date(iso):
    y, m, d = map(int, iso.split("-"))
    suf = "th" if 11 <= d % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")
    return f"{d}{suf} {_dt.date(y, m, d).strftime('%B')} {y}"


def slug(b):
    return SLUG[b["rank"]]


def board_files_table(b):
    h = ["<table>", "<tr><th>File<br>type</th><th>File<br>size</th><th>Peak memory<br>used</th></tr>"]
    for mode in ("simulation", "visual"):
        h.append(f'<tr><th colspan="3" align="left">{mode.capitalize()}</th></tr>')
        for k in [k for k in KINDS if k.startswith(mode)]:
            d = run_of(b["rank"], k); f = k.split("/")[1]
            if d is None:
                h.append(f"<tr><td>{FNAME[f]}</td><td align=\"right\">not run</td><td align=\"right\">–</td></tr>")
                continue
            sz = d["files"].get(f, [0, 0])[1] + (d["files"].get("mtl", [0, 0])[1] if f == "obj" else 0)
            szt = size(sz) if (d["ok"] and sz) else ("–" if not sz else size(sz))
            pk = size(d["peak_memory"]) if d.get("peak_memory") else "–"
            h.append(f'<tr><td>{FNAME[f]}</td><td align="right">{szt.replace(" ", "&nbsp;")}</td><td align="right">{pk.replace(" ", "&nbsp;")}</td></tr>')
    h.append("</table>")
    return "\n".join(h)


def board_section(b, num):
    """One board, as the Feature Test Collection shows one: chart, stage table, facts beside files and memory."""
    rs = {k: run_of(b["rank"], k) for k in KINDS}
    out = [f"## {num} {b['name']}\n"]
    okrs = [(lab, rs[k]) for k, lab in MODES if rs[k] and rs[k]["rc"] == 0]
    if okrs:
        sh = lambda d, ks: sum(d["bars"][k] for k in ks) / max(sum(d["bars"].values()), 1e-9) * 100
        fixed = [sh(d, ("1–2 read", "start-up and exit")) for _, d in okrs]
        work = [sh(d, ("4 geometry", "6 assemble")) for _, d in okrs]
        a, what = (fixed, "reading, start-up and exit take") if max(fixed) > 45 else (work, "stages 4 and 6 take")
        lo, hi = round(min(a)), round(max(a))
        head = f"{b['name']}: {what} {lo}% to {hi}% of a run" if lo != hi else f"{b['name']}: {what} {lo}% of a run"
        if len(head) > 70: head = head.split(": ", 1)[1].capitalize()
        if not (IMG / "Corpus-Testing" / PAGEDIR / f"{slug(b)}.webp").exists():   # a finished board is drawn once
            stacked([(lab, d["bars"]) for lab, d in okrs], head, SUB, slug(b), label_w=0.24)
        alt = head + ". " + ". ".join(f"{lab} takes {secs(sum(d['bars'].values()))}" for lab, d in okrs)
        out.append(f"![{alt}]({RAW}/Corpus-Testing/{PAGEDIR}/{slug(b)}.webp)\n")
    out.append("| Mode and format | 1–2 read | 3 resolve | 4 geometry | 5 materials | 6 assemble | 7 write | 8 verify | start-up and exit | Total |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for k, lab in MODES:
        d = rs[k]
        if d and d["rc"] == 0:
            out.append(f"| {lab} | " + " | ".join(fmt(d["bars"][x]).replace(" ", "&nbsp;") for x in KEYS) + f" | {sum(d['bars'].values()):.1f} |")
        else:
            out.append(f"| {lab} | " + " | ".join([""] * 8) + f" | {outcome(d)} |")
    bad = [(lab, rs[k]) for k, lab in MODES if not (rs[k] and rs[k]["ok"])]
    res = "PASS in all six runs" if not bad else "<br>".join(f"{lab}: {outcome(d)}" for lab, d in bad)
    d0 = next((d for d in rs.values() if d and d.get("kicad_format")), None)
    kfmt = re.sub(r"^KiCad format (\d+) \((KiCad \d+)\).*", r"\2 (\1)", d0["kicad_format"]) if d0 else f"KiCad {b['kicad']}"
    proj, fname = b["path"].split("/", 1)
    folder, _, leaf = fname.rpartition("/")
    out.append('\n<table align="center"><tr><td valign="top">\n')
    out.append(f"| Board | Repo: [{b['project']}](https://github.com/{b['project']})<br>Board: `{leaf}` |")
    out.append("|---|---|")
    if folder: out.append(f"| Folder | {brk(folder.replace('/', ' / '))} |")
    g = grade(b)
    out.append(f"| Complexity | {g[0]}&nbsp;/&nbsp;1000 (size&nbsp;{g[1]}, features&nbsp;{g[2]}) |")
    if g[3]: out.append(f"| KESE&nbsp;features | {wrap(', '.join(g[3]))} |")
    days = sorted({d["date"] for d in rs.values() if d})
    if days: out.append(f"| Tested | {nice_date(days[0])}" + (f" to {nice_date(days[-1])}" if len(days) > 1 else "") + " |")
    out.append(f"| Copper&nbsp;layers | {b['layers']} |")
    out.append(f"| File&nbsp;format | {kfmt} |")
    out.append(f"| Parts,&nbsp;tracks,&nbsp;vias | {b['parts']:,}, {b['tracks']:,}, {b['vias']:,} |")
    if d0: out.append(f"| Triangles,&nbsp;simulation | {d0['triangles']:,} in {d0['parts']} parts |")
    if b["notes"]: out.append(f"| Note | {b['notes'].replace(',', ', ')} |")
    out.append(f"| Verifier | {res} |")
    if b["rank"] in BAD_DESIGN:
        out.append(f"| Bad&nbsp;design | Bad design according to KESE: copper of two nets on top of each other in the file, "
                   f"a short KiCad's DRC reports; {BAD_DESIGN[b['rank']]}. KESE models what the file says, so the Verifier "
                   f"rightly finds the two nets' solids overlapping |")
    again = [(lab, rs[k]["rerun"]) for k, lab in MODES if rs[k] and rs[k].get("rerun")]
    for why in ("fixed", "cap"):
        labs = [lab for lab, w in again if w == why]
        if labs:
            how = ("with fixes to KESE made after the corpus run, and passed" if why == "fixed"
                   else "with the memory cap raised from 11 GB to 14.5 GB, and passed")
            out.append(f"| Run&nbsp;again | {'; '.join(labs)}: failed in the corpus run, run again {how} |")
    out.append('\n</td><td valign="top">\n')
    out.append(board_files_table(b))
    out.append("\n</td></tr></table>\n")
    return "\n".join(out)
