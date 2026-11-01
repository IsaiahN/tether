"""RUN B'S WORKER (the reviewer 2026-10-31 r541 3, r542; Isaiah 10:26 "tether B parallelized"): ONE process, ONE agent,
ONE life, as harness/mem_store/e4_stream.py, whose loop this keeps line for line -- the switch between steps,
arrive, the edges, step_or_recover. HARNESS ONLY: nothing in the agent; the agent is never told a game's name or
that its slice ends. What differs, and only this:
  - the games: taken one at a time from run_b.py's queue (a claim file made with O_CREAT|O_EXCL, so no two workers
    take one game), never a fixed order;
  - the card: every game is made on the ONE scorecard run_b.py opened (a competition server refuses a second open,
    arc_agi api.py new_scorecard); run_b.py closes it;
  - the slice: each game's share, derived when its slice starts -- (deadline_at - now - this worker's longest step)
    x N / the games not yet finished, this one among them; min = max = the share under rule A. B_SHARE=0: run A's
    300/400 (B_ and never TETHER_: that namespace is the agent's arms, as harness/supervise.py says);
  - nothing is written to the lineage: the end write is not called, the boundary writes are off
    (TETHER_LINEAGE_BOUNDARY=0) and a fault is recovered without end_path's write (TETHER_FAULT_RECOVER=0; recover);
  - a None from the wrapper (r563) is never handed to the agent: the game ends "no_answer" with no retry, the agent
    cut inside its step is replaced from the unchanged lineage, and a make with no frame on a gone card (the
    gateway's 404) ends this worker's claims, exit 0.
THE ONE KNOWN DUPLICATION (the reviewer 2026-10-31 r543): the per-step loop below is e4_stream's text; when e4_stream's
loop changes, this one must follow.
B_TEST_FAULT="worker,step" (the local test only, r543's must-hold; never set by the notebook): that worker's agent
raises once at that step of its life, through step_or_recover, so the recovery below can be seen to run.
argv: code out lineage card queue_dir n_workers deadline_at worker"""
import collections
import gc
import glob
import json
import os
import sys
import time
import weakref

sys.dont_write_bytecode = True
CODE, OUT, LIN, CARD, QDIR, N, DL, WID = sys.argv[1:9]
N, DL = int(N), float(DL)
SHARE = os.environ.get("B_SHARE", "1") != "0"
FAULT_AT = os.environ.get("B_TEST_FAULT", "")
FAULT_AT = int(FAULT_AT.split(",")[1]) if FAULT_AT and FAULT_AT.split(",")[0] == WID else None
MEM_GUARD = os.environ.get("B_MEM_GUARD", "1") != "0"   # r554 3; B_TEST_SHARE_MB forces a share (the must-fail only)
SHARE_MB = int(os.environ.get("B_TEST_SHARE_MB") or os.environ.get("B_SHARE_MB") or 0)
# B_MEM_GROWTH_MARGIN, a declared convention (Fig 10; Isaiah 2026-11-01 06:47, r669 2): the guard
# reckons the next game may grow by this multiple of the largest one-game growth seen so far in
# this worker (rehearsal 2's bp35 grew ~1.7x its estimate). 1 is the guard as before.
GROWTH_MARGIN = float(os.environ.get("B_MEM_GROWTH_MARGIN", "2"))
FIXED_MIN_S, FIXED_MAX_S = 300.0, 400.0      # run A's slice (Isaiah 2026-10-30 21:28); only under B_SHARE=0
assert os.environ.get("PYTHONHASHSEED") == "0", "the hash seed must be pinned by the launcher"
os.environ["TETHER_AGENT_SEED"] = "0"
os.makedirs(OUT, exist_ok=True)


def _record_traceback(kind, value, tb):
    import traceback
    with open(os.path.join(OUT, "stream.traceback.txt"), "w", encoding="utf-8") as fh:
        fh.write("".join(traceback.format_exception(kind, value, tb)))
    sys.__excepthook__(kind, value, tb)


sys.excepthook = _record_traceback
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, CODE)
os.chdir(CODE)

import arc_holdout  # noqa: E402, I001   (the import order is e4_stream's)
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
from arc_agi import Arcade  # noqa: E402

assert not lineage._BOUNDARY and not tether._FAULT_RECOVER and lineage._CARRY, (
    "the arms B runs under, read through armflag: run_b sets TETHER_LINEAGE_BOUNDARY=0 and TETHER_FAULT_RECOVER=0")
with open(os.path.join(QDIR, "games.json"), encoding="utf-8") as fh:
    GAMES = json.load(fh)


def take():
    """The next game no worker has taken, claimed atomically; None when every game is taken."""
    for i, g in enumerate(GAMES):
        try:
            fd = os.open(os.path.join(QDIR, f"take_{i}"), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            continue
        os.write(fd, f"{WID} {time.time()}".encode())
        os.close(fd)
        return i, g
    return None


def finished(i: int) -> None:
    with open(os.path.join(QDIR, f"done_{i}"), "w", encoding="utf-8") as fh:
        fh.write(f"{WID} {time.time()}")


def commit_mb() -> tuple[int, int]:
    """(this process's private commit, its peak), MB; off Windows (the resident set, its high-water mark)."""
    if os.name != "nt":
        import resource
        b = tether._commit_bytes()
        return (-1 if b is None else b // 2**20), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024
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
    return int(c.PrivateUsage) // 2**20, int(c.PeakPagefileUsage) // 2**20


MEMOS = ("_HELD_COMPILE", "_INDEX_STORE", "_BOUND_MEMO")   # process-wide, never cleared (r551 3)


def memo(event: str, i: int, g: str) -> None:
    """RECORD ONLY (r551 3): at each claim and each game's end, the sizes of tether's process-wide memos and this
    process's commit, to memo.tsv; the driver writes it and the agent never reads it. A memo absent here is -1."""
    sizes = [len(getattr(tether, n)) if hasattr(tether, n) else -1 for n in MEMOS]
    c, pk = commit_mb()
    with open(os.path.join(OUT, "memo.tsv"), "a", encoding="utf-8") as fh:
        fh.write("\t".join(map(str, (round(time.time(), 1), event, i, g, *sizes, c, pk))) + "\n")


SW = os.path.join(OUT, "switch.tsv")


def log(line: str) -> None:
    with open(SW, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


class NoAnswer(BaseException):
    """r563: the wrapper answered None (arc_agi's client logs any HTTP error or timeout and returns None). Raised in
    place of handing the None to the agent; a BaseException, so step_or_recover never reads it as an agent fault."""


class Stream:
    """The proxy wrapper: the current game's wrapper, swapped by the harness between steps (e4_stream's, the switch
    'between'), every game made on the one card. switch_to says whether the made game holds a frame."""

    def __init__(self, arc):
        self.arc, self.cur = arc, None

    @property
    def observation_space(self):
        return getattr(self.cur, "observation_space", None)

    def reset(self):
        return self._answer(self.cur.reset())

    def step(self, act, data=None):
        return self._answer(self.cur.step(act, data=data) if data is not None else self.cur.step(act))

    @staticmethod
    def _answer(frame):
        if frame is None:
            raise NoAnswer
        return frame

    def switch_to(self, game: str) -> bool:
        self.cur = self.arc.make(game, scorecard_id=CARD)
        return self.observation_space is not None


def card_gone(arc) -> bool:
    """r563: after a make with no frame, whether the card itself is gone -- the gateway's own 404 for it (a competition
    card that is still open answers 403, api.py get_scorecard). Anything else reads as not gone."""
    try:
        arc.get_scorecard(CARD)
    except Exception as e:   # noqa: BLE001
        return getattr(getattr(e, "response", None), "status_code", None) == 404
    return False


def recover(env, ag, ctx):
    """(A), the reviewer 2026-10-31 r542: step_or_recover's recovery (arc_holdout.py, after end_path) with end_path's
    writes left out -- the faulted agent's end_run, guarded; a fresh world on the SAME wrapper; a fresh agent on the
    SAME ledger loading the UNCHANGED lineage, with the harness's clock (the cycle after the faulted one, the
    deadline). The faulted agent is dropped, and with it what this life learned since its load."""
    arc_holdout.guarded(ag, ag.end_run, ledger.AGENT_FAULT)
    cycle, deadline, led = ag._fault_cycle + 1, ag.deadline, ag.led
    fresh_env = arc_holdout.world_on(env.w, ctx["game"], ctx["palette"], env.on_frame)
    fresh, _loaded = arc_holdout.wire_agent(fresh_env, ctx["game"], None, led, None, LIN, clock=(cycle, deadline))
    led.record(cycle, "SETTLE", "@run", "fault_recovered", fault=len(ctx["faults"]),
               parent=getattr(fresh, "lineage_parent", None),
               reads="run B (A): a fresh agent loaded from the unchanged lineage goes on in the same game, on the "
                     "board as the game holds it; nothing was written and nothing of the faulted agent crossed")
    return fresh_env, fresh


def rewire(env, ag, ctx, why: dict, no_answer: bool = False):
    """B_MEM_GUARD (the reviewer 2026-10-31 r554 3), BETWEEN games only: recover()'s path with no fault -- this life's
    end_run, a fresh world on the SAME wrapper, a fresh agent on the SAME ledger from the UNCHANGED lineage, the clock
    carried -- because this worker's commit and its own largest one-game growth would pass its share of the machine.
    What this life built in memory is dropped; nothing is written.
    no_answer (r563): the same path after a step the wrapper never answered, whose agent was cut inside its step, so
    its end_run is guarded as recover()'s is."""
    if no_answer:
        arc_holdout.guarded(ag, ag.end_run, "cap")
    else:
        ag.end_run("cap")
    cycle, deadline, led = ag.cycle, ag.deadline, ag.led
    fresh_env = arc_holdout.world_on(env.w, ctx["game"], ctx["palette"], env.on_frame)
    fresh, _loaded = arc_holdout.wire_agent(fresh_env, ctx["game"], None, led, None, LIN, clock=(cycle, deadline))
    if no_answer:
        led.record(cycle, "SETTLE", "@run", "no_answer", what="rewire", **why,
                   parent=getattr(fresh, "lineage_parent", None),
                   reads="run B: the wrapper answered None to a step, so that game ended with no retry and the "
                         "agent cut inside its step was dropped; a fresh agent from the unchanged lineage goes on to "
                         "the next game; nothing was written")
        return fresh_env, fresh
    led.record(cycle, "SETTLE", "@run", "b_mem_guard", what="rewire", **why,
               parent=getattr(fresh, "lineage_parent", None),
               reads="run B B_MEM_GUARD: between games, a fresh agent from the unchanged lineage, because this "
                     "worker's commit plus its largest one-game growth would pass its share; nothing was written")
    return fresh_env, fresh


def inject(ag) -> None:
    """B_TEST_FAULT: this agent's next step() raises, once; the instance's own step is restored by the raise."""
    real = ag.step

    def once(*_a, **_k):
        ag.step = real
        raise RuntimeError("B_TEST_FAULT: a fault injected by the local test's driver")
    ag.step = once


steps_life = 0
arc = Arcade(operation_mode=arc_holdout._mode())
proxy = Stream(arc)
no_answer = []                            # r563: games ended because the wrapper answered None
first = take()
while first is not None and not proxy.switch_to(first[1]):
    no_answer.append(first[1])
    finished(first[0])
    gone = card_gone(arc)
    log(f"# {first[0]}\t{first[1]}\tno_answer: the make held no frame; no retry; card gone {gone}")
    first = None if gone else take()
if first is None:
    log(f"# worker {WID}: no game left to take (no_answer {no_answer})")
    sys.exit(0)
led_path = os.path.join(OUT, "stream.jsonl")
env, ag, led, _board, _pal, _loaded = arc_holdout.wire(proxy, "stream", led_path=led_path, lineage_dir=LIN)
_today = tether.arms_today()     # r690 3, STAYS ON: every arm built 2026-11-01 must read ON here
led.record(0, "SETTLE", "@run", "arms_today", arms=_today, off=sorted(k for k, v in _today.items() if not v))
# r694 row 22: the lineage load reserves the last save's end-path wall; B writes nothing, so it is spent
led.record(0, "SETTLE", "@run", "end_reserve_zeroed", was=getattr(ag, "_end_reserve", None),
           sleep_was=getattr(ag, "_end_sleep_s", None))
ag._end_reserve, ag._end_sleep_s = 0.0, 0.0
if not all(_today.values()):
    log(f"# worker {WID}: arms OFF {sorted(k for k, v in _today.items() if not v)} -- the run is refused (r690 3)")
    sys.exit(3)
ctx = {"game": "stream", "cfg": None, "library": None, "lineage_dir": LIN,
       "led_path": led_path, "save_only_dir": None, "palette": _pal}
LOAD_S = round(time.time() - float(os.environ.get("B_T0", time.time())), 1)
log(f"# worker {WID} start {time.strftime('%Y-%m-%d %H:%M:%S')} card {CARD} n_workers {N} share {SHARE} "
    f"deadline_at {DL} load_s_since_launch {LOAD_S} games_listed {len(GAMES)}")
log("# idx\tgame\twall_start_s\tcycle_start\twall_s\tsteps\tlevels_in_slice\tending\tendings\tcommit_mb_end\t"
    "seq0\tseqP\tseq1\tacts\tfirst_act_s\textended\tunreached\toverrun_s\tshare_s\tleft\tlongest_step_s\tpeak_mb")


def going(t_start: float, acts: int, mn: float, mx: float) -> bool:
    """e4_stream's rule (A): a slice ends at the first step boundary at or after max(MIN, its first completed action),
    and no step starts past MAX."""
    el = time.time() - t_start
    return el < mx and (el < mn or acts == 0)


ag.deadline = DL
T0 = time.time()
endings_all = collections.Counter()
budget_unreached, taken, longest = [], [], 0.0
grow_max = None                           # B_MEM_GUARD: this worker's largest one-game commit growth, MB
nxt = first
while nxt is not None:
    i, g = nxt
    taken.append(g)
    memo("claim", i, g)
    if getattr(ag, "_cut", False):        # the net fired: thinking has ended for the life
        budget_unreached.append(g)
        finished(i)
        log(f"# {i}\t{g}\tunreached at this budget (the whole-run deadline passed; no switch)")
        nxt = take()
        continue
    if MEM_GUARD and SHARE_MB and grow_max is not None:
        c_now = commit_mb()[0]
        if c_now + GROWTH_MARGIN * grow_max > SHARE_MB:
            old = (weakref.ref(ag), weakref.ref(env)) if os.environ.get("B_TEST_SHARE_MB") else None
            env, ag = rewire(env, ag, ctx, {"commit_mb": c_now, "largest_game_growth_mb": grow_max,
                                            "growth_margin": GROWTH_MARGIN,
                                            "share_mb": SHARE_MB, "games_played": len(taken) - 1})
            gc.collect()      # the old life is cyclic garbage until collected, and freeing it is the guard's point
            if old is not None:   # r557, the test only: nothing may still hold the old agent or its world
                held = [r() for r in old]
                ag.led.record(ag.cycle, "SETTLE", "@run", "b_mem_guard_test",
                              old_agent_dead=held[0] is None, old_env_dead=held[1] is None,
                              holders=[sorted({type(x).__name__ for x in gc.get_referrers(h)}) for h in held
                                       if h is not None])
                del held
            memo("rewire", i, g)
    c_game0 = commit_mb()[0] if MEM_GUARD else None
    seq0 = len(ag.led)
    if len(taken) > 1:
        if not proxy.switch_to(g):        # r563: no frame at the make; a gone card stops this worker's claims
            no_answer.append(g)
            finished(i)
            gone = card_gone(arc)
            log(f"# {i}\t{g}\tno_answer: the make held no frame; nothing taken, no retry; card gone {gone}")
            nxt = None if gone else take()
            continue
        if not env.arrive():
            log(f"# {i}\t{g}\tarrive: the wrapper held no frame; nothing taken, no reset issued")
    seqP = len(ag.led)
    left = len(GAMES) - len(glob.glob(os.path.join(QDIR, "done_*")))   # not finished, this one among them
    if SHARE:
        mn = mx = max(0.0, (DL - time.time() - longest) * N / left)
    else:
        mn, mx = FIXED_MIN_S, FIXED_MAX_S
    t_start, c_start, steps, seq1 = time.time(), ag.cycle, 0, None
    was_terminal = ""
    lv_seen = 0
    lv_start, ending, endings = None, "slice", collections.Counter()
    acts, first_act_s = 0, None
    while going(t_start, acts, mn, mx):
        t_step = time.time()
        if FAULT_AT is not None and steps_life == FAULT_AT:
            inject(ag)
        steps_life += 1
        try:
            env, ag, acted, fault = arc_holdout.step_or_recover(env, ag, ctx)
        except NoAnswer:                  # r563: the game ends here, no retry; the cut agent is replaced
            steps += 1
            ending = "no_answer"
            no_answer.append(g)
            env, ag = rewire(env, ag, ctx, {"game_steps": steps}, no_answer=True)
            break
        if fault is not None:
            if ctx["faults"].count(arc_holdout.fault_key(fault)) > 1:
                raise fault                # a repeat ends the life, as e4_stream's
            env, ag = recover(env, ag, ctx)
        longest = max(longest, time.time() - t_step)
        steps += 1
        if acted:
            acts += 1
            first_act_s = first_act_s if first_act_s is not None else round(time.time() - t_start, 1)
        seq1 = len(ag.led) if seq1 is None else seq1
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
        if lineage._BOUNDARY and LIN and (term_edge or lvl_edge):      # as e4_stream; off in B (asserted above)
            lineage.boundary(LIN, ag, "stream", end if term_edge else "level")
        lv_seen, was_terminal = lv, end
        if end == ledger.WIN:
            ending = ledger.WIN
            break
        if getattr(ag, "_cut", False):
            ending = "cut"
            break
    endings_all.update(endings)
    wall_end, (commit_end, peak) = round(time.time() - t_start, 1), commit_mb()
    if c_game0 is not None:
        grow_max = max(grow_max or 0, commit_end - c_game0)
    extended = first_act_s is None or first_act_s > mn
    unreached = acts == 0
    overrun = round(max(0.0, wall_end - mx), 1)
    log(f"{i}\t{g}\t{round(t_start - T0, 1)}\t{c_start}\t{wall_end}\t{steps}\t"
        f"{(lv_seen - (lv_start or 0))}\t{ending}\t{dict(endings)}\t{commit_end}\t{seq0}\t{seqP}\t{seq1}\t"
        f"{acts}\t{first_act_s}\t{extended}\t{unreached}\t{overrun}\t{round(mx, 1)}\t{left}\t{round(longest, 1)}\t"
        f"{peak}")
    memo("end", i, g)
    finished(i)
    nxt = take()
ag.end_run("cap")                         # no lineage.write: B keeps nothing (r541 3(d))
close = getattr(ag.led, "close", None)
if close:
    close()
out = {"worker": WID, "taken": taken, "cycles": ag.cycle, "wall_s": round(time.time() - T0, 1),
       "endings": dict(endings_all), "deadline_at": DL, "deadline_fired": bool(getattr(ag, "_cut", False)),
       "budget_unreached": budget_unreached, "faults": len(ctx.get("faults", [])), "peak_mb": commit_mb()[1],
       "longest_step_s": round(longest, 1), "no_answer": no_answer}
with open(os.path.join(OUT, "stream.result.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, default=str)
log(f"# worker {WID} end {time.strftime('%Y-%m-%d %H:%M:%S')} {json.dumps(out, default=str)[:400]}")
