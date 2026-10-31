"""SHAPE B (the reviewer 2026-10-31 r541 3, r542; Isaiah 10:26 "tether B parallelized version"): N processes, each ONE
agent and ONE life (kaggle/b_worker.py), taking the games the Arcade lists from one queue until none is left. ONE MIND,
N COPIES: every worker loads the same lineage and none writes to it, so the copies never merge (r465 3). Harness only:
nothing in the agent. Seeds as run A's: PYTHONHASHSEED 0 from the launcher, TETHER_AGENT_SEED 0 in each worker.
N = min(the cores this process may run on, the memory it may use // one worker's peak), read here at run time.
ONE scorecard: opened here before any worker starts (a competition server refuses a second open, arc_agi api.py
new_scorecard), its id handed to every worker, closed here once every worker has ended -- the close scores every game.
Writes <out>/kaggle_b.json: N and what it was read from, the card and what its close returned, each worker's rc, and
whether the lineage folder is unchanged (names, sizes and modification times, before and after).
argv: code out lineage deadline_at [n_games]"""
import json
import os
import subprocess
import sys
import time
import traceback

sys.dont_write_bytecode = True
CODE, OUT, LIN, DL, *rest = sys.argv[1:]
assert os.environ.get("PYTHONHASHSEED") == "0", "the hash seed must be pinned by the launcher"
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, CODE)
# ONE WORKER'S PEAK, MB, a measurement: PLAY25 round_01 switch.tsv row 24 (tn36), commit_mb_end 7086, the highest of the
# round's 25 games, read at the switch after the game (the reviewer 2026-10-31 r541 3(a)). B writes no lineage, so the
# end path's write (its 9.88 GiB) never runs in a worker.
PEAK_MB = 7086
SIDE = ("-shm", "-wal", "-journal")      # SQLite's side files: an open reader makes them; they hold no lineage


def cores() -> tuple[int, str]:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0)), "os.sched_getaffinity"
    return os.cpu_count() or 1, "os.cpu_count"


def memory() -> tuple[int, str]:
    """The bytes this run may use: the cgroup's limit (v2, then v1), else MemTotal; on Windows, which has neither, what
    other processes leave at launch."""
    for p in ("/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        if os.path.isfile(p):
            with open(p) as fh:
                v = fh.read().strip()
            if v.isdigit() and int(v) < 2**60:
                return int(v), p
    if os.path.isfile("/proc/meminfo"):
        with open("/proc/meminfo") as fh:
            kb = next(int(ln.split()[1]) for ln in fh if ln.startswith("MemTotal:"))
        return kb * 1024, "/proc/meminfo MemTotal"
    import ctypes

    class MS(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [
            (n, ctypes.c_ulonglong) for n in ("ullTotalPhys", "ullAvailPhys", "ullTotalPageFile", "ullAvailPageFile",
                                              "ullTotalVirtual", "ullAvailVirtual", "ullAvailExtendedVirtual")]
    m = MS()
    m.dwLength = ctypes.sizeof(m)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    # the smaller of the physical memory and the commit still available: commit is what ran out on 2026-10-31 (r539)
    return min(int(m.ullAvailPhys), int(m.ullAvailPageFile)), "GlobalMemoryStatusEx min(ullAvailPhys, ullAvailPageFile)"


def listing(d: str) -> dict:
    out = {}
    for root, _dirs, files in os.walk(d):
        for f in files:
            if f.endswith(SIDE):
                continue
            p = os.path.join(root, f)
            st = os.stat(p)
            out[os.path.relpath(p, d)] = (st.st_size, st.st_mtime_ns)
    return out


import arc_holdout  # noqa: E402, I001   (for _mode, the one reading of OPERATION_MODE)
from arc_agi import Arcade  # noqa: E402

rec = {"argv": sys.argv, "t_start": time.time(), "error": None}
rc = 0
arc = card = None
try:
    arc = Arcade(operation_mode=arc_holdout._mode())
    games = [e.game_id for e in arc.get_environments()]
    assert games, "the Arcade lists no games"
    games = games[:int(rest[0])] if rest else games
    (nproc, nproc_from), (mem, mem_from) = cores(), memory()
    n = max(1, min(nproc, mem // (PEAK_MB * 2**20), len(games)))
    # B_MEM_GUARD's share (r554 3): the memory read above, less this parent's own commit now, split over the N workers
    parent_mb = (arc_holdout.tether._commit_bytes() or 0) // 2**20
    share_mb = (mem // 2**20 - parent_mb) // n
    rec.update(games=games, n_workers=n, nproc=nproc, nproc_from=nproc_from, mem_bytes=mem, mem_from=mem_from,
               peak_mb=PEAK_MB, parent_commit_mb=parent_mb, share_mb=share_mb)
    card = arc.create_scorecard()
    rec["card"] = card
    qdir = os.path.join(OUT, "queue")
    os.makedirs(qdir)
    with open(os.path.join(qdir, "games.json"), "w", encoding="utf-8") as fh:
        json.dump(games, fh)
    before = listing(LIN)
    env = {**os.environ, "TETHER_LINEAGE_BOUNDARY": "0", "TETHER_FAULT_RECOVER": "0",
           "B_T0": repr(time.time()), "B_SHARE_MB": str(share_mb), "PYTHONDONTWRITEBYTECODE": "1"}
    print(f"run_b: {len(games)} games, N {n} (cores {nproc} by {nproc_from}; memory {mem // 2**20} MB by {mem_from} "
          f"// peak {PEAK_MB} MB), card {card}, each worker's share {share_mb} MB (parent {parent_mb} MB)",
          flush=True)
    procs = []
    for k in range(n):                     # spawned, never forked: each loads its own copy, on Windows as on Linux
        wout = os.path.join(OUT, f"worker_{k}")
        os.makedirs(wout)
        with open(os.path.join(wout, "worker.log"), "w", encoding="utf-8") as fh:   # the child holds its own handle
            procs.append(subprocess.Popen([sys.executable, "-B", os.path.join(CODE, "kaggle", "b_worker.py"), CODE,
                                           wout, LIN, card, qdir, str(n), DL, str(k)],
                                          env=env, cwd=CODE, stdin=subprocess.DEVNULL, stdout=fh,
                                          stderr=subprocess.STDOUT))
    rec["workers"] = [{"worker": k, "rc": p.wait()} for k, p in enumerate(procs)]
    rc = int(any(w["rc"] for w in rec["workers"]))
    after = listing(LIN)
    rec["lineage_unchanged"] = before == after
    rec["lineage_changed"] = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))[:40]
    rec["untaken"] = [g for i, g in enumerate(games) if not os.path.exists(os.path.join(qdir, f"take_{i}"))]
except BaseException as e:   # noqa: BLE001 -- every ending, SystemExit included, still closes the card
    rc = 1
    rec["error"] = "".join(traceback.format_exception(type(e), e, e.__traceback__))
finally:
    if arc is not None and card is not None:
        try:
            sc = arc.close_scorecard(card)
            rec["closed"] = sc.model_dump(mode="json") if hasattr(sc, "model_dump") else repr(sc)
        except Exception as e:   # noqa: BLE001
            rec["close_error"] = repr(e)
            # r563: a 404 on our own close is the gateway's auto-close (STALE_MINUTES) having closed it first
            rec["closed_by_gateway"] = getattr(getattr(e, "response", None), "status_code", None) == 404
            rc = rc if rec["closed_by_gateway"] else 1
    rec["t_end"] = time.time()
    with open(os.path.join(OUT, "kaggle_b.json"), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, default=repr)
print(f"kaggle_b rc {rc}; workers {[w['rc'] for w in rec.get('workers', [])]}; lineage unchanged "
      f"{rec.get('lineage_unchanged')}; error {'yes' if rec['error'] else 'no'}", flush=True)
sys.exit(rc)
