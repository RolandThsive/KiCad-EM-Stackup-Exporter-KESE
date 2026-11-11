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
DATA = Path(HERE).parents[1] / "data"
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
# ---- the boards and their runs: one folder per board in data/, b<number>b_<repo>_<board> (named as its tables folder)
#   board.json  the board's counts from its .kicad_pcb (tracks, vias, parts, chips, layers ...), its KESE features,
#               its path and zip, and what makes it a bad design according to KESE, if it is one
#   runs.jsonl  every run of the board in order, each with its date and source: "corpus" (the first runs; a later
#               one replaces an earlier one), or "fixed", "cap" or "nocap" (run again with the fixes to KESE, with
#               the memory cap raised to 14.5 GB, or with no memory cap: it takes the place of a run that failed,
#               when it passes; a run that fails again keeps the first result)
BOARDS, FEAT, BAD_DESIGN, SLUG, RUNS = {}, {}, {}, {}, {}
for _d in sorted(p for p in DATA.iterdir() if (p / "board.json").is_file()):
    _b = json.loads((_d / "board.json").read_text())
    _r = _b["rank"]
    BOARDS[_r] = _b
    FEAT[_r] = _b.get("features") or {}
    if _b.get("bad_design"): BAD_DESIGN[_r] = _b["bad_design"]
    _m = re.fullmatch(r"b\d+b_(.+)", _d.name)
    SLUG[_r] = _m.group(1) if _m else _d.name
    _f = _d / "runs.jsonl"
    RUNS[_r] = [json.loads(l) for l in open(_f) if l.strip()] if _f.is_file() else []
assert len(set(SLUG.values())) == len(SLUG)

R = {}
import datetime as _dt
for _r in sorted(RUNS):
    for d in RUNS[_r]:
        if d["source"] == "corpus":
            if d.get("runner_died") and d["tag"] in R: continue      # a rerun replaces a run whose runner was stopped
            R[d["tag"]] = d
            continue
        old = R.get(d["tag"])
        if old is None or (old["rc"] == 0 and "PASS" in old["verifier"]): continue
        if not (d["rc"] == 0 and "PASS" in (d.get("verifier") or "")): continue
        d["rerun"] = d["source"]
        R[d["tag"]] = d
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
    if "PASS" in d["verifier"] and d.get("rerun") == "nocap": return "PASS (run again with no memory cap)"
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
    png = Path("/tmp") / f"{name.replace('/', '_')}.png"
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


FEATURES = [tuple(f) for f in json.load(open(Path(HERE).parent / "features.json"))]  # (key in features.json, name on the page, what is counted in the .kicad_pcb file, weight)
assert sum(w for *_, w in FEATURES) == 500


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


def board_parts(b):
    """One board's pieces, as the Feature Test Collection shows a board: its chart (drawn into
    docs/images/<repo>_<board>/stages.webp when missing) and its three tables, and the chart's alt text."""
    rs = {k: run_of(b["rank"], k) for k in KINDS}
    alt = ""
    okrs = [(lab, rs[k]) for k, lab in MODES if rs[k] and rs[k]["rc"] == 0]
    if okrs:
        sh = lambda d, ks: sum(d["bars"][k] for k in ks) / max(sum(d["bars"].values()), 1e-9) * 100
        fixed = [sh(d, ("1–2 read", "start-up and exit")) for _, d in okrs]
        work = [sh(d, ("4 geometry", "6 assemble")) for _, d in okrs]
        a, what = (fixed, "reading, start-up and exit take") if max(fixed) > 45 else (work, "stages 4 and 6 take")
        lo, hi = round(min(a)), round(max(a))
        head = f"{b['name']}: {what} {lo}% to {hi}% of a run" if lo != hi else f"{b['name']}: {what} {lo}% of a run"
        if len(head) > 70: head = head.split(": ", 1)[1].capitalize()
        cdir = IMG / board_dir(REPO / "docs" / "tables", slug(b)).name   # named as its tables folder
        if not (cdir / "stages.webp").exists():   # a board's chart is drawn once
            cdir.mkdir(parents=True, exist_ok=True)
            stacked([(lab, d["bars"]) for lab, d in okrs], head, SUB, f"{cdir.name}/stages", label_w=0.24)
        alt = head + ". " + ". ".join(f"{lab} takes {secs(sum(d['bars'].values()))}" for lab, d in okrs)
    out = []
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
    stages = "\n".join(out)
    out = []
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
    for why in ("fixed", "cap", "nocap"):
        labs = [lab for lab, w in again if w == why]
        if labs:
            how = {"fixed": "with fixes to KESE made after the corpus run, and passed",
                   "cap": "with the memory cap raised from 11 GB to 14.5 GB, and passed",
                   "nocap": "with no memory cap and no time limit (swap added to the 15 GB machine), and passed"}[why]
            out.append(f"| Run&nbsp;again | {'; '.join(labs)}: failed in the corpus run, run again {how} |")
    return dict(stages=stages, facts="\n".join(out), files=board_files_table(b), alt=alt, ok=not bad,
                done=all(rs.values()), rerun={w: [lab for lab, x in again if x == w] for w in ("fixed", "cap", "nocap")})
