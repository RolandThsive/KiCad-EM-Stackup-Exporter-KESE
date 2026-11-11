#!/usr/bin/env python3
"""Run A Board: runs KESE on boards of your own choosing and writes, for each, the two files of its data folder in
Corpus Testing, board.json and runs.jsonl, ready to push to corpus-testing/data/ on the corpus-testing branch.

    The Main Program/   KESE: the KiCad-EM-Stackup-Exporter-KESE repository as downloaded or cloned (or its Generator
                        folder alone), wherever run_KESE.py is inside it
    Input_Boards/       the boards, each inside a folder named <owner>__<repo>, as the boards are in their repository:
                        Input_Boards/<owner>__<repo>/<path in the repo>/<board>.kicad_pcb (cloning the repository
                        into Input_Boards/<owner>__<repo> does just that, and its commit is noted)
    Output_Run/         a folder per board, named as its file: board.json and runs.jsonl

    python run_a_board.py                       every board in Input_Boards
    python run_a_board.py --help                the options (memory cap, time limit, source, KESE's commit)

Each board is run six times, one file format a run, as in Corpus Testing: simulation mode with GLB, STEP, STL and OBJ,
visual mode with GLB and OBJ, each with the Verifier, the solder mask and the silkscreen on. The runner only measures:
it counts the board's file (its layers, parts, tracks, vias and KESE features) and records each run. Everything else
(the board's score, level, rank, number and folder name, its tables, chart and pages) is worked out by the engine on
GitHub once the data folder is pushed. The license is yours to give: board.json leaves it blank, to fill in with the
day you looked it up, or to leave blank.

A board stopped part way (the machine restarted, Ctrl+C) carries on where it stopped: a run already in its
runs.jsonl is not run again. Needs Python 3.9 or newer with KESE's own requirements installed
(pip install -r "The Main Program/.../Generator/requirements.txt"); psutil (pip install psutil) to measure the
memory on Windows and macOS, where /proc is missing."""
import argparse
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAIN, INPUT, OUTPUT = HERE / "The Main Program", HERE / "Input_Boards", HERE / "Output_Run"
MAKER = HERE.parent / "corpus-testing" / "engine" / "maker"          # the board's counts, as the engine reads them
KINDS = [("simulation", "glb"), ("simulation", "step"), ("simulation", "stl"), ("simulation", "obj"),
         ("visual", "glb"), ("visual", "obj")]
SETS = ["--set", "SolderMask.SOLDER_MASK_ENABLED=True", "--set", "Silkscreen.SILKSCREEN_ENABLED=True"]
LINUX = sys.platform.startswith("linux")


def fail(msg):
    sys.exit(f"Run A Board: {msg}")


# ---- KESE, the counts and the machine
def find_kese():
    """The folder with run_KESE.py and the kese package, inside The Main Program."""
    found = sorted((p.parent for p in MAIN.rglob("run_KESE.py") if (p.parent / "kese" / "__init__.py").is_file()),
                   key=lambda p: len(p.parts))
    if not found:
        fail(f'no KESE in "{MAIN}": put the KiCad-EM-Stackup-Exporter-KESE repository (or its Generator folder) there')
    return found[0]


def git_commit(folder, within):
    """The commit of the git clone folder is in, or None: only a clone inside within counts (this runner sits in a
    clone of the corpus-testing branch itself, whose commit is not the board's nor KESE's)."""
    try:
        r = subprocess.run(["git", "-C", str(folder), "rev-parse", "--show-toplevel", "HEAD"], capture_output=True,
                           text=True, timeout=30)
        top, head = r.stdout.splitlines()[:2] if r.returncode == 0 else (None, None)   # a path may have spaces
        if top and Path(top).resolve().is_relative_to(Path(within).resolve()):
            return head
    except Exception:
        pass
    return None


def ram_bytes():
    if LINUX:
        return next(int(l.split()[1]) * 1024 for l in open("/proc/meminfo") if l.startswith("MemTotal"))
    try:
        import psutil
        return psutil.virtual_memory().total
    except ImportError:
        return 0


def cpu_name():
    try:
        if LINUX:
            return next(l for l in open("/proc/cpuinfo") if l.startswith("model name")).split(":", 1)[1].strip()
        if sys.platform == "darwin":
            return subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
    except Exception:
        pass
    return platform.processor() or platform.machine()


def machine(gen, commit):
    try:
        import numpy
        import shapely
    except ImportError as e:
        fail(f"KESE's requirements are not installed ({e}): pip install -r \"{gen / 'requirements.txt'}\"")
    version = re.search(r'__version__ = "([^"]+)"', (gen / "kese" / "__init__.py").read_text())
    # the engine reads the cores and the GB from the cpu entry: "<model>, 4 cores, 15 GB"
    return dict(cpu=f"{cpu_name()}, {os.cpu_count()} cores, {ram_bytes() // 1073741824} GB",
                python=platform.python_version(), shapely=shapely.__version__, geos=shapely.geos_version_string,
                numpy=numpy.__version__, kese=commit or "unknown", kese_version=version.group(1) if version else "unknown")


# ---- the memory of a run: its whole process tree, sampled every 0.05 s
def _tree_pss_linux(root):
    """Proportional set size (PSS) of a process and all its descendants, in bytes: shared pages are split between the
    processes that share them, so the sum is the memory the run really holds; with swap, what is swapped out too."""
    kids = {}
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            with open(f"/proc/{d}/stat") as f:
                st = f.read()
            kids.setdefault(int(st[st.rindex(")") + 2:].split()[1]), []).append(int(d))
        except Exception:
            continue
    total, todo = 0, [root]
    while todo:
        p = todo.pop()
        todo += kids.get(p, [])
        try:
            with open(f"/proc/{p}/smaps_rollup") as f:
                total += sum(int(l.split()[1]) for l in f if l.startswith(("Pss:", "SwapPss:"))) * 1024
        except Exception:
            pass
    return total


def _tree_uss_psutil(root):
    import psutil
    try:
        ps = [psutil.Process(root)]
        ps += ps[0].children(recursive=True)
    except psutil.Error:
        return 0
    total = 0
    for p in ps:
        try:
            total += p.memory_full_info().uss
        except psutil.Error:
            pass
    return total


def memory_probe():
    if LINUX and os.path.exists("/proc/self/smaps_rollup"):
        return _tree_pss_linux, "PSS of the process tree, sampled every 0.05 s"
    try:
        import psutil  # noqa: F401
        return _tree_uss_psutil, "USS of the process tree, sampled every 0.05 s"
    except ImportError:
        return None, "not measured (install psutil)"


def kill_tree(p):
    if os.name == "posix":
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except Exception:
            pass
    else:
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)


def run(cmd, env, cap, time_limit, probe):
    """Runs cmd as its own process group; returns (rc, log, timed out, capped, peak bytes of the process tree)."""
    kw = dict(start_new_session=True) if os.name == "posix" else dict(creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    with tempfile.TemporaryFile("w+", encoding="utf-8", errors="replace") as out:
        p = subprocess.Popen(cmd, env=env, stdout=out, stderr=subprocess.STDOUT, text=True, **kw)
        peak, capped, stop = [0], [False], threading.Event()

        def watch():
            while not stop.is_set():
                m = probe(p.pid) if probe else 0
                peak[0] = max(peak[0], m)
                if cap and m > cap and not capped[0]:
                    capped[0] = True
                    kill_tree(p)
                stop.wait(0.05)
        th = threading.Thread(target=watch, daemon=True)
        th.start()
        timed_out = False
        try:
            p.wait(timeout=time_limit)
        except subprocess.TimeoutExpired:
            timed_out = True
            kill_tree(p)
            p.wait()
        except KeyboardInterrupt:
            kill_tree(p)
            raise
        kill_tree(p)                                        # a worker left behind
        stop.set()
        th.join()
        out.seek(0)
        return (None if timed_out else p.returncode), out.read(), timed_out, capped[0], (peak[0] or None)


# ---- the boards
def boards():
    """(project, path, file) of every board in Input_Boards: path is <owner>__<repo>/<path in the repo>."""
    out, loose = [], []
    for f in sorted(INPUT.rglob("*.kicad_pcb")):
        rel = f.relative_to(INPUT)
        if any(part.endswith("-backups") or part.startswith((".", "#")) for part in rel.parts[:-1]) \
                or f.name.startswith(("_autosave", "~")):
            continue                                        # KiCad's backups and autosaves
        top = rel.parts[0]
        if len(rel.parts) < 2 or "__" not in top:
            loose.append(str(rel))
            continue
        owner, repo = top.split("__", 1)
        out.append((f"{owner}/{repo}", rel.as_posix(), f))
    for r in loose:
        print(f'left out: Input_Boards/{r} is not in a folder named <owner>__<repo> (where its repository is on GitHub)')
    return out


def outcome_line(d):
    if d["timeout"]: return "time limit"
    if d["capped"]: return "memory cap"
    return d["verifier"] or f"rc={d['rc']}"


def main():
    ap = argparse.ArgumentParser(description="Runs KESE six times on each board in Input_Boards and writes its "
                                             "board.json and runs.jsonl to Output_Run.")
    ap.add_argument("--cap", type=float, default=None,
                    help="stop a run whose memory passes this many GB (default: 11, or 72%% of the RAM if less; 0: no cap)")
    ap.add_argument("--time-limit", type=float, default=90, help="stop a run after this many minutes (default 90; 0: none)")
    ap.add_argument("--source", default="corpus", choices=("corpus", "fixed", "cap", "nocap"),
                    help='what the runs are: "corpus" (first runs, the default), or a failed run run again with fixes '
                         'to KESE ("fixed"), with a higher memory cap ("cap") or with no cap ("nocap")')
    ap.add_argument("--kese-commit", help="the KESE commit, when The Main Program is not a git clone")
    ap.add_argument("--runs", help='only these modes and formats, as "simulation/obj,visual/obj" (to run failed runs '
                                   'again); all six by default')
    ap.add_argument("only", nargs="*", help="only the boards whose path in Input_Boards contains one of these")
    a = ap.parse_args()

    kinds = KINDS
    if a.runs:
        kinds = [tuple(k.strip().split("/")) for k in a.runs.split(",")]
        bad = [("/".join(k)) for k in kinds if k not in KINDS]
        if bad:
            fail(f"--runs: {', '.join(bad)} is not one of " + ", ".join("/".join(k) for k in KINDS))
    for d in (MAIN, INPUT, OUTPUT):
        d.mkdir(exist_ok=True)
    gen = find_kese()
    commit = a.kese_commit or git_commit(gen, MAIN)
    if not commit:
        print('note: The Main Program is not a git clone, so the runs say KESE commit "unknown"; give it with --kese-commit')
    mach = machine(gen, commit)
    ram = ram_bytes()
    cap = (min(11e9, ram * 0.72) if ram else 11e9) if a.cap is None else (a.cap * 1e9 or None)
    time_limit = a.time_limit * 60 or None
    probe, probe_kind = memory_probe()
    if cap and not probe:
        print("note: memory is not measured here (pip install psutil), so the memory cap does nothing")
    sys.path.insert(0, str(MAKER))
    try:
        import score
        import features
    except ImportError:
        fail(f"the engine's counting code is not in {MAKER}: run this from a checkout of the corpus-testing branch")

    todo = [b for b in boards() if not a.only or any(s in b[1] for s in a.only)]
    if not todo:
        fail("no boards in Input_Boards: put each in Input_Boards/<owner>__<repo>/<path in the repo>/")
    names = {}
    for project, path, f in todo:
        names.setdefault(f.stem, []).append(path)
    print(f"KESE {mach['kese_version']} ({mach['kese'][:7]}) from {gen}; {len(todo)} boards; memory cap "
          f"{f'{cap / 1e9:g} GB' if cap else 'none'}, time limit {f'{a.time_limit:g} min' if time_limit else 'none'}")

    work = Path(tempfile.mkdtemp(prefix="runaboard_"))
    env = dict(os.environ, KESE_GENERATOR=str(gen), PYTHONIOENCODING="utf-8")
    try:
        for project, path, f in todo:
            n = names[f.stem]
            folder = OUTPUT / (f.stem if len(n) == 1 else f"{f.stem} ({n.index(path) + 1})")
            folder.mkdir(parents=True, exist_ok=True)
            data = f.read_bytes()
            b = score.count(data)                           # its counts and notes, as the engine reads them
            b.update(path=path, project=project, name=f.stem, license="", license_checked="")
            c = git_commit(f.parent, INPUT / path.split('/')[0])
            if c:
                b["commit"] = c[:7]
            b["features"] = features.scan(data.decode("utf-8", "replace"))
            bj = folder / "board.json"
            if bj.is_file():                               # a license given there already is kept
                old = json.loads(bj.read_text(encoding="utf-8"))
                for k in ("license", "license_checked", "bad_design"):
                    if old.get(k): b[k] = old[k]
            bj.write_text(json.dumps(b, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            rj = folder / "runs.jsonl"
            have = set()
            if rj.is_file():
                for l in rj.read_text(encoding="utf-8").splitlines():
                    if l.strip():
                        x = json.loads(l)
                        if x.get("source", "corpus") == a.source and not x.get("runner_died"):
                            have.add((x["mode"], x["format"]))
            print(f"\n{path}\n  -> {folder.relative_to(HERE)}")
            board = work / "board" / f.name
            shutil.rmtree(board.parent, ignore_errors=True)
            board.parent.mkdir(parents=True)
            shutil.copy2(f, board)
            for mode, fmt in kinds:
                if (mode, fmt) in have:
                    print(f"  {mode + '/' + fmt + ':':17}already run")
                    continue
                out, times = work / "out", work / "times.json"
                shutil.rmtree(out, ignore_errors=True)
                if times.exists():
                    times.unlink()
                env["KESE_TIMES"] = str(times)
                cmd = [sys.executable, "-I", str(HERE / "timed_kese.py"), str(board), "--mode", mode, "--format", fmt,
                       "--verify", "--out", str(out), *SETS]
                t = time.perf_counter()
                rc, log, timed_out, capped, peak = run(cmd, env, cap, time_limit, probe)
                wall = time.perf_counter() - t
                try:
                    stages = json.loads(times.read_text())
                except Exception:
                    stages = []
                files, report = {}, ""
                for g in (out.rglob("*") if out.exists() else []):
                    if not g.is_file():
                        continue
                    k = files.setdefault(g.suffix.lstrip(".").lower(), [0, 0])
                    k[0] += 1
                    k[1] += g.stat().st_size
                    if g.name == "report.txt":
                        report = g.read_text(errors="replace")
                parts = re.findall(r"^\s{2}(\S.*?)\s+(\d+) triangles", report, re.M)
                rep = report.splitlines()
                ver = next((l.strip() for l in log.splitlines() if "Verifier:" in l), "")
                ok = rc == 0 and "PASS" in ver
                rec = dict(path=path, mode=mode, format=fmt, rc=rc, timeout=timed_out, killed=(rc == -9), capped=capped,
                           cap=cap, time_limit=time_limit, peak_memory=peak,
                           peak_memory_kind=probe_kind, wall=round(wall, 3), stages=stages, verifier=ver,
                           rays=next((l.strip() for l in rep if "per vertical ray" in l), ""),
                           kicad_format=next((l.strip() for l in rep if l.startswith("KiCad format")), ""),
                           copper_layers=next((l.split(":", 1)[1].strip() for l in rep if l.strip().startswith("copper layers:")), ""),
                           parts=len(parts), triangles=sum(int(x) for _, x in parts), files=files,
                           messages=[l.strip() for l in log.splitlines() if re.match(r"\s+(note|warning|error)", l)][:40],
                           log=(log[-3000:] + (f"\n[stopped by the runner: memory passed {cap / 1e9:.1f} GB]" if capped else ""))
                           if not ok else "",
                           machine=mach, date=time.strftime("%Y-%m-%d", time.gmtime()), source=a.source)
                with open(rj, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                shutil.rmtree(out, ignore_errors=True)      # only the record is kept: every file KESE wrote goes
                print(f"  {mode + '/' + fmt + ':':17}{wall:8.1f} s, peak {(peak or 0) / 1e9:5.2f} GB, {outcome_line(rec)}", flush=True)
    except KeyboardInterrupt:
        print("\nstopped: run it again to carry on where it stopped")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"\nDone. Fill in each board's license in Output_Run/<board>/board.json (or leave it blank), then push the "
          f"folder to corpus-testing/data/ on the corpus-testing branch.")


if __name__ == "__main__":
    main()
