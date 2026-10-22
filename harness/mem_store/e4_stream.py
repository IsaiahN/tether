"""E4 (c), THE STREAM (Isaiah 2026-10-18 11:39 via the reviewer 11:40: "alltogether at once if possible so the agent
reads it all as one big game"). ONE process, ONE agent, ONE life: the 25 public games in a random order from a
recorded seed, back to back, each a slice of wall time (or until a WIN). HARNESS ONLY: the agent is never told a
game changed -- no retarget, no restarted, no game_start, no game id, nothing passed at a switch.

THE SWAP: ArcWorld touches its wrapper only at construction (observation_space / reset) and in step(); the driver
builds ONE ArcWorld (through arc_holdout.wire) over a proxy that delegates to the CURRENT game. At a switch the next
game is made, and the agent's next step() gets that game's fresh frame back as its outcome (its action is not
forwarded). In-game events keep play()'s own handling: a GAME_OVER is that game's death, a clear its level edge.

The order, the seed and each switch (wall time, the agent's cycle) go to the HARNESS's switch.tsv, never to the
agent's ledger. --mf plants ag.restarted(env) at every switch, so e4_stream_check.py can be shown to catch it.

argv: repo out [--seed HEX] [--slice-s S] [--lineage DIR] [--mf]"""
import argparse
import collections
import json
import os
import random
import secrets
import sys
import time

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("out")
ap.add_argument("--seed", default=None)
ap.add_argument("--slice-s", type=float, default=600.0)
ap.add_argument("--lineage", default=None)
ap.add_argument("--mf", action="store_true")
ap.add_argument("--n-games", type=int, default=25)   # the MF test plays the first 2 of the order
ap.add_argument("--slice-steps", default=None)       # per position, e.g. "3,1": a slice ends after N agent steps
ap.add_argument("--census", action="store_true")     # census_heap.point between steps (the reviewer 2026-10-19 03:00)
A = ap.parse_args()
STEPS = [int(x) for x in A.slice_steps.split(",")] if A.slice_steps else None
CH = None
if A.census:                                         # loaded by path: scratchpad dirs are stripped from sys.path below
    import importlib.util
    _spec = importlib.util.spec_from_file_location(
        "census_heap", os.path.join(os.path.dirname(os.path.abspath(__file__)), "census_heap.py"))
    CH = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(CH)
os.makedirs(A.out, exist_ok=True)


def _record_traceback(kind, value, tb):
    """ANY uncaught exception in the one life: its full traceback to <out>/stream.traceback.txt, then the
    default hook (the reviewer 19:36: if the error comes in the one life, we must at least get the LINE)."""
    import traceback
    with open(os.path.join(A.out, "stream.traceback.txt"), "w", encoding="utf-8") as fh:
        fh.write("".join(traceback.format_exception(kind, value, tb)))
    sys.__excepthook__(kind, value, tb)


sys.excepthook = _record_traceback
sys.path = [p for p in sys.path if "scratchpad" not in p]     # as game_one: no stray module shadows
sys.path.insert(0, A.repo)
os.chdir(A.repo)

import arc_holdout  # noqa: E402, I001   (the import order is the run's; not reordered)
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
from arc_agi import Arcade  # noqa: E402

games = sorted(os.listdir(os.path.join(A.repo, "environment_files")))
assert len(games) == 25, games
seed = A.seed or secrets.token_hex(4)
order = random.Random(seed).sample(games, len(games))
order = order[:A.n_games]
SW = os.path.join(A.out, "switch.tsv")


def commit_mb() -> int:
    """This process's private commit, MB (the reviewer 23:13: the stream logs commit at every switch)."""
    import ctypes
    import ctypes.wintypes as wt

    class PMC(ctypes.Structure):
        _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD)] + [
            (n, ctypes.c_size_t) for n in (
                "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
                "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage",
                "PeakPagefileUsage", "PrivateUsage")]
    c = PMC()
    c.cb = ctypes.sizeof(c)
    k32 = ctypes.windll.kernel32
    k32.GetCurrentProcess.restype = wt.HANDLE
    gpmi = ctypes.windll.psapi.GetProcessMemoryInfo
    gpmi.argtypes = [wt.HANDLE, ctypes.POINTER(PMC), wt.DWORD]
    gpmi(k32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return int(c.PrivateUsage) // 2**20


def log(line: str) -> None:
    with open(SW, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


class Stream:
    """The proxy wrapper: the current game's wrapper, swapped by the harness between steps."""

    def __init__(self, arc, first: str):
        self.arc, self.cur, self.pending = arc, arc.make(first), None

    @property
    def observation_space(self):
        return getattr(self.cur, "observation_space", None)

    def reset(self):
        return self.cur.reset()

    def step(self, act, data=None):
        if self.pending is not None:      # the switch lands here: the new board is the outcome
            self.cur, self.pending = self.pending, None
            return getattr(self.cur, "observation_space", None) or self.cur.reset()
        return self.cur.step(act, data=data) if data is not None else self.cur.step(act)

    def switch_to(self, game: str) -> None:
        self.pending = self.arc.make(game)


arc = Arcade(operation_mode=arc_holdout._mode())
proxy = Stream(arc, order[0])
led_path = os.path.join(A.out, "stream.jsonl")
env, ag, led, _board, _pal, _loaded = arc_holdout.wire(proxy, "stream", led_path=led_path,
                                                         lineage_dir=A.lineage)
log(f"# stream start {time.strftime('%Y-%m-%d %H:%M:%S')} seed {seed} slice_s {A.slice_s} mf {A.mf} "
    f"order {','.join(order)}")
log("# idx\tgame\twall_start_s\tcycle_start\twall_s\tsteps\tlevels_in_slice\tending\tendings\tcommit_mb_end\t"
    "seq0\tseqP\tseq1")
T0 = time.time()
if CH:
    CH.point("after_load", ag, A.out)
endings_all = collections.Counter()
for i, g in enumerate(order):
    seq0 = len(ag.led)           # the check's window opens before the switch (and the plant) ...
    if i:
        proxy.switch_to(g)
        if A.mf:
            ag.restarted(env)      # THE PLANT: a boundary hook at the switch, for the check to catch
    seqP = len(ag.led)           # rows in [seq0, seqP) were written AT the switch: by design none
    t_start, c_start, steps, seq1 = time.time(), ag.cycle, 0, None
    was_terminal = ""            # harness state: a switch is no restart of the old game
    lv_seen = 0
    lv_start, ending, endings = None, "slice", collections.Counter()
    n_steps = STEPS[min(i, len(STEPS) - 1)] if STEPS else None
    while (steps < n_steps) if n_steps else (time.time() - t_start < A.slice_s):
        ag.step()
        steps += 1
        seq1 = len(ag.led) if seq1 is None else seq1     # ... and closes after the first step
        lv = env.levels()[0]
        lv_start = lv if lv_start is None else lv_start
        end = env.terminal()
        if end and end != was_terminal:
            endings[end] += 1
            ag.retarget(env, lv, how=end)
        if tether._LINEAGE_HOLD and was_terminal == "death" and not end:
            ag.restarted(env)
        term_edge = bool(end) and end != was_terminal
        lvl_edge = not term_edge and lv > lv_seen
        if lvl_edge and tether._LEVEL_EDGE:
            ag.retarget(env, lv, how=ledger.ADVANCE)
        if lineage._BOUNDARY and A.lineage and (term_edge or lvl_edge):      # as play()
            lineage.boundary(A.lineage, ag, "stream", end if term_edge else "level")
        lv_seen, was_terminal = lv, end
        if end == ledger.WIN:
            ending = ledger.WIN
            break
        if CH and n_steps and steps < n_steps:       # between steps; the last step's point is the switch below
            CH.point(f"after_step{steps}", ag, A.out)
    endings_all.update(endings)
    wall_end, commit_end = round(time.time() - t_start, 1), commit_mb()   # read BEFORE the switch's census
    if CH:
        CH.point("switch", ag, A.out)
    log(f"{i}\t{g}\t{round(t_start - T0, 1)}\t{c_start}\t{wall_end}\t{steps}\t"
        f"{(lv_seen - (lv_start or 0))}\t{ending}\t{dict(endings)}\t{commit_end}\t{seq0}\t{seqP}\t{seq1}")
ag.end_run("cap")
gen = lineage.write(A.lineage, ag, "stream") if lineage._CARRY and A.lineage else None
close = getattr(ag.led, "close", None)
if close:
    close()
out = {"seed": seed, "order": order, "cycles": ag.cycle, "wall_s": round(time.time() - T0, 1),
       "endings": dict(endings_all), "lineage": str(gen)[:300], "mf": A.mf}
with open(os.path.join(A.out, "stream.result.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, default=str)
log(f"# stream end {time.strftime('%Y-%m-%d %H:%M:%S')} {json.dumps(out, default=str)[:400]}")
