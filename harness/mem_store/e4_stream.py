"""E4 (c), THE STREAM (Isaiah 2026-10-18 11:39 via the reviewer 11:40: "alltogether at once if possible so the agent
reads it all as one big game"). ONE process, ONE agent, ONE life: the 25 public games in a random order from a
recorded seed, back to back, each a slice of wall time (or until a WIN). HARNESS ONLY: the agent is never told a
game changed -- no retarget, no restarted, no game_start, no game id, nothing passed at a switch.

THE SWAP: ArcWorld touches its wrapper only at construction (observation_space / reset) and in step(); the driver
builds ONE ArcWorld (through arc_holdout.wire) over a proxy that delegates to the CURRENT game. At a switch the next
game is made current and its first frame handed to the world BETWEEN steps (ArcWorld.arrive, no action paired with
it), so the agent's next step decides on that game's own first frame and its action reaches that game (--switch
between, the default; the reviewer 2026-10-25 10:47, 11:03). --switch step keeps the old swap: the agent's next
step() got the new frame back as its action's outcome and the action was not forwarded. In-game events keep play()'s
own handling: a GAME_OVER is that game's death, a clear its level edge.

The order, the seed and each switch (wall time, the agent's cycle) go to the HARNESS's switch.tsv, never to the
agent's ledger. --mf plants ag.restarted(env) at every switch, so e4_stream_check.py can be shown to catch it.

argv: repo out [--seed HEX] [--slice-s S] [--lineage DIR] [--mf] [--games files|arcade]"""
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
ap.add_argument("--switch", choices=("between", "step"), default="between")   # see THE SWAP above
ap.add_argument("--n-games", type=int, default=None)   # the MF test plays the first 2 of the order; None: all
# where the games come from: "files" (environment_files, the 25, a seeded order) or "arcade" (the Arcade's own list, in
# its order and count, as a competition gateway serves it; the reviewer 2026-10-30 r464 3)
ap.add_argument("--games", choices=("files", "arcade"), default="files")
ap.add_argument("--slice-steps", default=None)       # per position, e.g. "3,1": a slice ends after N agent steps
ap.add_argument("--census", action="store_true")     # census_heap.point between steps (the reviewer 2026-10-19 03:00)
# E4b's slice rule (A) (Isaiah 2026-10-23 "i like c and then a"; the reviewer 06:29 B1, 06:54 (a)): a slice ends at
# the first step boundary at or after max(MIN, its first completed action), and no step starts past MAX. A step under
# way finishes (a cut would end the one life's thinking, tether.Agent.step's _cut), so a slice can overrun MAX.
ap.add_argument("--slice-min-s", type=float, default=None)
ap.add_argument("--slice-max-s", type=float, default=None)
# (b), THE ONE WHOLE-RUN NET (the reviewer 2026-10-23 06:54, 07:08 (i), superseding 2026-10-22 15:24 for this only): an
# epoch the launcher computes (its clock before the supervisor starts + the supervisor's wall - a chosen margin), set
# ONCE on the agent before the first game and never at a switch. Past it the agent's own cut ends thinking for the rest
# of the life; the end path still writes, and the games not started are "unreached at this budget".
ap.add_argument("--deadline-at", type=float, default=None)
A = ap.parse_args()
assert (A.slice_min_s is None) == (A.slice_max_s is None), "--slice-min-s and --slice-max-s go together"
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

arc = Arcade(operation_mode=arc_holdout._mode())
if A.games == "arcade":
    seed = A.seed
    order = [e.game_id for e in arc.get_environments()]
    assert order, "the Arcade lists no games"
else:
    games = sorted(os.listdir(os.path.join(A.repo, "environment_files")))
    assert len(games) == 25, games
    seed = A.seed or secrets.token_hex(4)
    order = random.Random(seed).sample(games, len(games))
order = order[:A.n_games]
SW = os.path.join(A.out, "switch.tsv")


def commit_mb() -> int:
    """This process's private commit, MB (the reviewer 23:13: the stream logs commit at every switch); off Windows the
    resident set, as the agent reads its own body (tether._commit_bytes), -1 if unreadable."""
    if os.name != "nt":
        b = tether._commit_bytes()
        return -1 if b is None else b // 2**20
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
        if A.switch == "between":         # current at once; the driver hands its frame over (arrive)
            self.cur = self.arc.make(game)
        else:                             # "step": today's swap at the next step, its action lost
            self.pending = self.arc.make(game)


proxy = Stream(arc, order[0])
led_path = os.path.join(A.out, "stream.jsonl")
env, ag, led, _board, _pal, _loaded = arc_holdout.wire(proxy, "stream", led_path=led_path,
                                                         lineage_dir=A.lineage)
ctx = {"game": "stream", "cfg": None, "library": None, "lineage_dir": A.lineage,
       "led_path": led_path, "save_only_dir": None, "palette": _pal}   # (B)
log(f"# stream start {time.strftime('%Y-%m-%d %H:%M:%S')} seed {seed} slice_s {A.slice_s} mf {A.mf} switch {A.switch} "
    f"slice_min_s {A.slice_min_s} slice_max_s {A.slice_max_s} order {','.join(order)}")
log("# idx\tgame\twall_start_s\tcycle_start\twall_s\tsteps\tlevels_in_slice\tending\tendings\tcommit_mb_end\t"
    "seq0\tseqP\tseq1\tacts\tfirst_act_s\textended\tunreached\toverrun_s")


def going(steps: int, n_steps, t_start: float, acts: int) -> bool:
    """Whether the slice takes another step: N steps (--slice-steps), else the rule (A), else --slice-s."""
    if n_steps:
        return steps < n_steps
    el = time.time() - t_start
    if A.slice_min_s is None:
        return el < A.slice_s
    return el < A.slice_max_s and (el < A.slice_min_s or acts == 0)


if A.deadline_at is not None:
    ag.deadline = A.deadline_at
T0 = time.time()
if CH:
    CH.point("after_load", ag, A.out)
endings_all = collections.Counter()
budget_unreached = []
for i, g in enumerate(order):
    if getattr(ag, "_cut", False):        # the net fired: thinking has ended for the life
        budget_unreached.append(g)
        log(f"# {i}\t{g}\tunreached at this budget (the whole-run deadline passed; no switch)")
        continue
    seq0 = len(ag.led)           # the check's window opens before the switch (and the plant) ...
    if i:
        proxy.switch_to(g)
        if A.switch == "between" and not env.arrive():   # the new game's first frame, before the next step
            log(f"# {i}\t{g}\tarrive: the wrapper held no frame; nothing taken, no reset issued")
        if A.mf:
            ag.restarted(env)      # THE PLANT: a boundary hook at the switch, for the check to catch
    seqP = len(ag.led)           # rows in [seq0, seqP) were written AT the switch: by design none
    t_start, c_start, steps, seq1 = time.time(), ag.cycle, 0, None
    was_terminal = ""            # harness state: a switch is no restart of the old game
    lv_seen = 0
    lv_start, ending, endings = None, "slice", collections.Counter()
    n_steps = STEPS[min(i, len(STEPS) - 1)] if STEPS else None
    acts, first_act_s = 0, None
    while going(steps, n_steps, t_start, acts):
        env, ag, acted, fault = arc_holdout.step_or_recover(env, ag, ctx)   # (B)
        if fault is not None:
            raise fault
        steps += 1
        if acted:
            acts += 1
            first_act_s = first_act_s if first_act_s is not None else round(time.time() - t_start, 1)
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
        if getattr(ag, "_cut", False):
            ending = "cut"
            break
        if CH and n_steps and steps < n_steps:       # between steps; the last step's point is the switch below
            CH.point(f"after_step{steps}", ag, A.out)
    endings_all.update(endings)
    wall_end, commit_end = round(time.time() - t_start, 1), commit_mb()   # read BEFORE the switch's census
    if CH:
        CH.point("switch", ag, A.out)
    mn, mx = A.slice_min_s, A.slice_max_s
    extended = mn is not None and (first_act_s is None or first_act_s > mn)
    unreached = mx is not None and acts == 0
    overrun = round(max(0.0, wall_end - mx), 1) if mx is not None else None
    log(f"{i}\t{g}\t{round(t_start - T0, 1)}\t{c_start}\t{wall_end}\t{steps}\t"
        f"{(lv_seen - (lv_start or 0))}\t{ending}\t{dict(endings)}\t{commit_end}\t{seq0}\t{seqP}\t{seq1}\t"
        f"{acts}\t{first_act_s}\t{extended}\t{unreached}\t{overrun}")
t_end = time.time()
ag.end_run("cap")
gen = lineage.write(A.lineage, ag, "stream") if lineage._CARRY and A.lineage else None
end_path_s = round(time.time() - t_end, 1)
close = getattr(ag.led, "close", None)
if close:
    close()
out = {"seed": seed, "order": order, "cycles": ag.cycle, "wall_s": round(time.time() - T0, 1),
       "endings": dict(endings_all), "lineage": str(gen)[:300], "mf": A.mf, "deadline_at": A.deadline_at,
       "deadline_fired": bool(getattr(ag, "_cut", False)), "budget_unreached": budget_unreached,
       "end_path_s": end_path_s}
with open(os.path.join(A.out, "stream.result.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, default=str)
log(f"# stream end {time.strftime('%Y-%m-%d %H:%M:%S')} {json.dumps(out, default=str)[:400]}")
