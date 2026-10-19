"""E4 (the reviewer 2026-10-18 11:19, the plan of 11:17 with its six amendments). ONE lane, sequential, each run
under harness/supervise.py. Harness side only; the agent never reads any of this.

  practice  the panel's 7 members (gridworld_s0-2, fake, gridworld_arc_s0-2), 5 min each, seed drawn at birth
  public    the 25 games of environment_files/, sorted, 10 min each through harness/game_one.py
  scrambled the same 25 in a random order drawn from a recorded seed; the lineage carries on from public

Stops (posted, the running game never killed): a game whose result carries an error that is not the cap, a
child rc other than 0, a peak at 90% of the ceiling. A game whose ledger is not written for 5 min before its
cap is HUNG: py-spy dumps it to <game>.pyspy.txt and the batch stops after it ends.

argv: repo out [--part practice|games|all] [--scramble-seed HEX]"""
import argparse
import json
import os
import random
import secrets
import subprocess
import sys
import threading
import time

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("out")
ap.add_argument("--part", default="all")
ap.add_argument("--scramble-seed", default=None)
ap.add_argument("--start", type=int, default=0)   # resume the sorted public list at this index (the reviewer 17:55)
A = ap.parse_args()
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
SUP = os.path.join(A.repo, "harness", "supervise.py")
PYSPY = ("C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/"
         "2043231f-437e-4548-ac19-702f1efcfb71/scratchpad/spyenv/Scripts/py-spy.exe")
LINEAGE, SAVES = os.path.join(A.out, "lineage"), "C:/Users/Admin/tether_saves"
os.makedirs(A.out, exist_ok=True)
RES = os.path.join(A.out, "results.tsv")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
MEMBERS = ("gridworld_s0", "gridworld_s1", "gridworld_s2", "fake",
           "gridworld_arc_s0", "gridworld_arc_s1", "gridworld_arc_s2")
games = sorted(os.listdir(os.path.join(A.repo, "environment_files")))
assert len(games) == 25, games
scr_seed = A.scramble_seed or secrets.token_hex(4)
scrambled = random.Random(scr_seed).sample(games, len(games))
head = subprocess.run(["git", "-C", A.repo, "rev-parse", "HEAD"], capture_output=True,
                            text=True).stdout.strip()
with open(os.path.join(A.repo, "harness", "game_one.py"), encoding="utf-8") as _fh:
    DL_AFTER_LOAD = "deadline_after_load" in _fh.read()   # the tree's own game_one


def note(line: str) -> None:
    with open(RES, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


def seed_of(ledger: str):
    try:
        with open(ledger, encoding="utf-8") as fh:
            for i, ln in enumerate(fh):
                d = json.loads(ln).get("detail") or {}
                if "seed" in d:
                    return d.get("seed"), d.get("generation")
                if i > 200:
                    break
    except OSError:
        pass
    return None, None


def children(pid: int) -> list:
    """The processes whose parent is pid (Windows, via CIM)."""
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
                          f"(Get-CimInstance Win32_Process -Filter 'ParentProcessId={pid}').ProcessId"],
                         capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout
    return [int(x) for x in out.split() if x.isdigit()]


def run(label: str, d: str, cmd: list, ledger: str, cap_s: float) -> dict:
    os.makedirs(d, exist_ok=True)
    t0, hung = time.time(), {"hit": False}
    p = subprocess.Popen([PY, "-B", SUP, "--out", d, "--watch-pid", str(os.getpid()),
                          "--max-s", str(cap_s + 900), "--", PY, "-B", *cmd], env=ENV,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def watch():
        while p.poll() is None:
            time.sleep(30)
            age = time.time() - (os.path.getmtime(ledger) if os.path.exists(ledger) else t0)
            if not hung["hit"] and age > 300 and time.time() - t0 < cap_s:
                hung["hit"] = True
                # the supervisor logs its child as "start pid N" (sup.json comes only at the end)
                try:
                    first = open(os.path.join(d, "sup.log"), encoding="utf-8").readline()
                    pids = [int(first.split("start pid ")[1].split()[0])]
                except (OSError, IndexError, ValueError):
                    pids = []
                with open(os.path.join(d, "pyspy.txt"), "w") as fh:
                    # the logged pid is the venv's launcher python.exe; the interpreter is its child
                    # (the reviewer 18:50), so dump the launcher's children too
                    for q in list(pids) + [c for p_ in pids for c in children(p_)]:
                        fh.write(f"--- py-spy dump --pid {q}\n")
                        fh.flush()
                        subprocess.run([PYSPY, "dump", "--pid", str(q)], stdout=fh, stderr=fh)
                    fh.write(f"ledger silent {age:.0f} s at {time.time() - t0:.0f} s\n")
    threading.Thread(target=watch, daemon=True).start()
    p.wait()
    try:
        sup = json.load(open(os.path.join(d, "sup.json"), encoding="utf-8"))
    except (OSError, ValueError) as e:
        sup = {"rc": None, "ending": f"no sup.json: {e!r}"}
    ws = 0     # peak working set (RSS) of any process in the job, from the supervisor's mem.tsv
    try:
        for ln in open(os.path.join(d, "mem.tsv"), encoding="utf-8"):
            f = ln.split("\t")
            if len(f) == 4 and f[3].strip().isdigit():
                ws = max(ws, int(f[3]))
    except OSError:
        pass
    return {"label": label, "sup": sup, "hung": hung["hit"], "wall": round(time.time() - t0),
            "ws_gib": round(ws / 1024, 2)}


note(f"# E4 start {time.strftime('%Y-%m-%d %H:%M:%S')} head {head} deadline_after_load {DL_AFTER_LOAD} start_index {A.start} scramble_seed {scr_seed} "
     f"scrambled {','.join(scrambled)}")
note("# part\tidx\tname\tchild_rc\tending\twall_s\tpeak_commit_gib\tpeak_rss_gib\tseed\tgeneration\terror\t"
     "actions\tlevel_changes\twon\thung")
stop = None
if A.part in ("practice", "all"):
    for i, m in enumerate(MEMBERS):
        d = os.path.join(A.out, "practice", m)
        led = os.path.join(d, f"{m}.jsonl")
        r = run(m, d, [os.path.join(os.path.dirname(os.path.abspath(__file__)), "e4_practice.py"),
                       A.repo, m, led, "300"], led, 300)
        s, gen = seed_of(led)
        note(f"practice\t{i}\t{m}\t{r['sup'].get('rc')}\t{r['sup'].get('ending')}\t{r['wall']}\t"
             f"{r['sup'].get('peak_process_commit_gib')}\t{r['ws_gib']}\t{s}\t{gen}\t-\t-\t-\t-\t"
             f"{r['hung']}")
        if r["sup"].get("rc") != 0 or r["hung"]:
            stop = f"practice {m}: rc {r['sup'].get('rc')} hung {r['hung']}"
            break
if stop is None and A.part in ("games", "all"):
    # the scrambled 25 run as ONE stream (e4_stream.py; Isaiah 11:39), never here as separate games
    for part, order in (("public", games),):
        for i, g in enumerate(order):
            if i < A.start:
                continue
            d = os.path.join(A.out, part, f"{i:02d}_{g}")
            led = os.path.join(d, f"{g}.jsonl")
            r = run(g, d, [os.path.join(A.repo, "harness", "game_one.py"), "--repo", A.repo,
                           "--game", g, "--cap-s", "600", "--out", d, "--lineage", LINEAGE,
                           "--saves", SAVES], led, 600)
            try:
                res = json.load(open(os.path.join(d, f"{g}.result.json"), encoding="utf-8"))
            except (OSError, ValueError):
                res = {}
            s, gen = seed_of(led)
            err = res.get("error")
            note(f"{part}\t{i}\t{g}\t{r['sup'].get('rc')}\t{r['sup'].get('ending')}\t{r['wall']}\t"
                 f"{r['sup'].get('peak_process_commit_gib')}\t{r['ws_gib']}\t{s}\t{gen}\t"
                 f"{str(err)[:120]}\t{res.get('actions')}\t{len(res.get('level_changes') or [])}\t"
                 f"{res.get('won')}\t{r['hung']}")
            ceil = r["sup"].get("ceiling_gib") or 0
            if (r["sup"].get("rc") != 0 or err or r["hung"]
                    or (ceil and (r["sup"].get("peak_process_commit_gib") or 0) >= 0.9 * ceil)):
                stop = f"{part} {g}: rc {r['sup'].get('rc')} error {err} hung {r['hung']}"
                break
        if stop:
            break
note(f"# E4 end {time.strftime('%Y-%m-%d %H:%M:%S')} stop {stop}")
