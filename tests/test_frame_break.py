"""B, THE FRAME BREAK (TETHER_FRAME_BREAK, default ON; the reviewer 2026-10-23 12:35, 13:04, 13:12;
design posted 13:00). Each case asserts its occasion before its failure.
  TRACKER (arc_percept.Objects; the arm is read at call time):
  MF1  a switch (a new board over the old cells in other colours): a break is recorded and every
       claim is issued as a birth; OFF: the old names are claimed
  MF2  (a) a toggle at claim score 1.0 (one piece recoloured, cells unchanged), alternated A, A',
       A, A': no break on any call; (b, AGENT) the cascade: each action answered with two equal
       toggled frames, so the first claim of each new frame is made inside _walk_cascade (:279):
       no break. Both occasions are counted separately
  MF3  a mover (three pieces shifted, colours kept): median under the bar, colour share 0: no
       break (the one-reading route)
  MF4  small frames through _break: 0 claims -> no test, recorded; 1 claim both ways ((0.2,
       recoloured) breaks; (0.2, same colour) and (0.9, recoloured) do not)
  REC  a break, then a call on the same frame (the lf52 k1 self-match): the call log still
       holds the break call while the last matches show the self-match
  AGENT (arc_holdout.wire on a fake game whose board swaps to a striped board after K steps):
  SEAM ON: a frame_break row at the swap's cycle; every object bet suspended (seam); no
       Agency.note, _route_reward or _note_goal_choice call there; no trace row appended; no
       mint-type row; the gate passes. OFF: no frame_break; the swap cycle's bets scored,
       Agency.note called, the trace row appended
  OFF  identity: the arm OFF on this tree writes the same ledger as the last commit without B
       (git archive) on the fake game, arms rows aside and wall timings masked
    python tests/test_frame_break.py
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

import numpy as np

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_percept  # noqa: E402


def board_a():
    g = np.zeros((12, 12), dtype=int)
    g[2:5, 2:5] = 3
    g[7:10, 6:9] = 7
    g[1:3, 8:11] = 4
    return g


def stripes(n=12):
    g = np.zeros((n, n), dtype=int)
    for k, col in enumerate((1, 2, 5, 6)):
        g[:, k * n // 4:(k + 1) * n // 4] = col
    return g


def tracker_cases() -> None:
    a, b = board_a(), stripes()
    arc_percept._FRAME_BREAK = True
    o = arc_percept.Objects()
    o(a)
    old = set(o.tracked)
    o(b)
    assert old, "MF1 precondition: the first board tracked nothing"
    assert len(o.breaks) == 1 and o.breaks[0]["broke"], ("MF1: no break on the switch", o.call_log)
    assert all(r == "birth" for r, _s in o.matches.values()), ("MF1: a claim survived", o.matches)
    assert not (set(o.matches) & old), ("MF1: an old name was reissued", o.matches)
    print(f"  MF1 switch: break (median {o.breaks[0]['median']}, colour "
          f"{o.breaks[0]['colour_share']}, {o.breaks[0]['claimed']} claims), all "
          f"{len(o.matches)} pieces born")
    arc_percept._FRAME_BREAK = False
    o = arc_percept.Objects()
    o(a)
    o(b)
    assert any(r != "birth" for r, _s in o.matches.values()) and not o.breaks, ("MF1 OFF",
                                                                               o.matches)
    print("  MF1 OFF: the old names are claimed, no break recorded")
    arc_percept._FRAME_BREAK = True

    a2 = board_a()
    a2[2:5, 2:5] = 5
    o = arc_percept.Objects()
    for g in (a, a2, a, a2, a):
        o(g)
    tog = [r for r in o.call_log if r["tested"] and r["median"] == 1.0 and r["colour_share"] > 0]
    assert tog, ("MF2 occasion (a): no toggle at claim score 1.0", o.call_log)
    assert not o.breaks, ("MF2: a toggle broke", o.call_log)
    print(f"  MF2 toggle, alternated 5 times: {len(o.call_log)} tested calls, colour share "
          f"{o.call_log[0]['colour_share']}, median {o.call_log[0]['median']}, no break")

    m = np.zeros((12, 12), dtype=int)
    m[2:5, 4:7] = 3
    m[7:10, 8:11] = 7
    m[1:3, 10:12] = 4
    o = arc_percept.Objects()
    o(a)
    o(m)
    t = o.call_log[-1]
    assert t["tested"] and t["median"] < arc_percept.BREAK_MEDIAN, ("MF3 precondition", t)
    assert t["colour_share"] == 0 and not o.breaks, ("MF3: a mover broke", t)
    print(f"  MF3 mover: median {t['median']} under the bar, colour share 0, no break")

    o = arc_percept.Objects()
    o(a)
    found = arc_percept.components(b)
    assign = dict.fromkeys(range(len(found)), (None, 0.0))
    o._break(b, found, assign)
    assert o.call_log[-1] == {"found": len(found), "claimed": 0, "tested": False}, o.call_log
    o = arc_percept.Objects()
    o(a)
    name = sorted(o.tracked)[0]
    found = [{**o.tracked[name], "colour": (o.tracked[name]["colour"] + 1) % 10}]
    assign = {0: (name, 0.2)}
    o._break(b, found, assign)
    assert o.breaks and o.breaks[-1]["claimed"] == 1 and assign[0] == (None, 0.0), (o.breaks,
                                                                                    assign)
    for score, recolour in ((0.2, False), (0.9, True)):     # 1 claim, the two no-break directions
        o = arc_percept.Objects()
        o(a)
        c0 = o.tracked[name]["colour"]
        f1 = [{**o.tracked[name], "colour": (c0 + 1) % 10 if recolour else c0}]
        a1 = {0: (name, score)}
        o._break(b, f1, a1)
        assert o.call_log[-1]["tested"] and not o.breaks and a1[0] == (name, score), (
            score, o.call_log)
    print("  MF4 small frames: 0 claims -> no test, recorded; 1 claim (0.2, recoloured) -> break, "
          "retired; 1 claim (0.2, same colour) and (0.9, recoloured) -> no break")

    o = arc_percept.Objects()
    o(a)
    o(b)
    o(b)
    assert len(o.call_log) == 1 and o.call_log[0]["broke"], ("REC", o.call_log)
    assert all(r == "overlap" and s == 1.0 for r, s in o.matches.values()), ("REC precondition",
                                                                             o.matches)
    print("  REC: after the break, a same-frame call self-matches at 1.0; the log still holds the "
          "break call")


PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, mode = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import numpy as np
import arc_holdout, arc_percept, arc_world, gate, instruments, tether
from test_entry import FakeWrapper

class Swap(FakeWrapper):
    def __init__(self, k):
        self.k, self.swapped = k, False
        super().__init__()

    def _frame(self, state):
        f = super()._frame(state)
        if self.n >= self.k:
            g = np.zeros((64, 64), dtype=int)
            for i, col in enumerate((1, 2, 5, 6)):
                g[:, i * 16:(i + 1) * 16] = col
            g[5:9, 5:9] = 7     # one piece identical across the swap: B keeps it (C's case)
            f.frame = [g]
            self.swapped = True
        return f

class Cascade(FakeWrapper):
    """Each action is answered with TWO equal frames (an intermediate equal to the settled one,
    the lf52 shape), the 5:9 block's colour toggled 7 <-> 8 each step (the ft09 toggle)."""
    def _frame(self, state):
        f = super()._frame(state)
        g = f.frame[0].copy()
        if self.n:
            g[5:9, 5:9] = 8 if self.n % 2 else 7
        f.frame = [g, g.copy()]
        return f

class SwapCascade(Swap):
    """The swap's new board answered as TWO equal frames: the switch arrives through :279 (k0)
    and is then decomposed again at :198 (k1), the lf52 shape."""
    def _frame(self, state):
        f = super()._frame(state)
        if self.swapped:
            f.frame = [f.frame[0], f.frame[0].copy()]
        return f

w = {"plain": FakeWrapper, "cascade": Cascade,
     "swapcascade": lambda: SwapCascade(3)}.get(mode, lambda: Swap(3))()
if mode == "off":
    arc_percept._FRAME_BREAK = False
IN = [False]
real_walk = arc_world.ArcWorld._walk_cascade
def walk(self, *a, **k):
    IN[0] = True
    try:
        return real_walk(self, *a, **k)
    finally:
        IN[0] = False
arc_world.ArcWorld._walk_cascade = walk
tested = []
real_break = getattr(arc_percept.Objects, "_break", None)      # absent on the tree before B
def brk(self, *a, **k):
    n0 = len(self.call_log)
    out = real_break(self, *a, **k)
    if len(self.call_log) > n0:
        tested.append([IN[0], self.call_log[-1]])
    return out
if real_break is not None:
    arc_percept.Objects._break = brk
calls = {"note": [], "reward": [], "goal": []}
for key, (cls, attr) in {"note": (instruments.Agency, "note"),
                         "reward": (tether.Agent, "_route_reward"),
                         "goal": (tether.Agent, "_note_goal_choice")}.items():
    real = getattr(cls, attr)
    def spy(self, *a, _real=real, _key=key, **k):
        if AG[0] is not None:
            calls[_key].append(AG[0].cycle)
        return _real(self, *a, **k)
    setattr(cls, attr, spy)
AG = [None]
swap_cycle = [None]
grew = {}
real_perceive = tether.Agent.perceive
def perceive(self, *a, **k):
    was, n0 = getattr(w, "swapped", False), len(self.trace)
    out = real_perceive(self, *a, **k)
    grew[self.cycle] = len(self.trace) - n0
    if not was and getattr(w, "swapped", False) and swap_cycle[0] is None:
        swap_cycle[0] = self.cycle
    return out
tether.Agent.perceive = perceive
env, ag, led, *_ = arc_holdout.wire(w, "fake")
AG[0] = ag
for _ in range(8):
    ag.step()
rows = ag.led.rows()
v = gate.check(rows)
wa = getattr(ag, "_window_at", 0)
cross = {}
if ag.trace and wa:
    last = ag.trace[-1]
    for s in [s for s in last[0] if s in last[2]]:
        pre = sum(1 for x in ag.trace[:wa] if s in x[0] and s in x[2])
        post = sum(1 for x in ag.trace[wa:] if s in x[0] and s in x[2])
        if pre and post:
            cross[s] = [len(ag.history(s)), pre, post]
print(json.dumps({"swap_cycle": swap_cycle[0], "grew": grew, "calls": calls, "tested": tested,
                  "window_at": wa, "cross": cross,
                  "gate": [v["verdict"], v.get("check"), v.get("token")],
                  "rows": rows}, default=str))
'''


def child(mode: str, tree: str | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree or str(_repo.ROOT), mode],
                         env=env, capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def obj_bets(rows: list, c: int) -> list:
    return [r for r in rows if r["cycle"] == c and r["event"] == "bet" and r["step"] == "PERCEIVE"
            and not r["slot"].startswith("@")]


def agent_cases() -> None:
    on = child("on")
    c = on["swap_cycle"]
    brk = [r for r in on["rows"] if r["event"] == "frame_break"]
    assert c is not None and brk and brk[0]["cycle"] == c, ("SEAM precondition", c, brk[:1])
    bets = obj_bets(on["rows"], c)
    assert bets and all(r["detail"].get("seam") and r["detail"].get("suspended") for r in bets), (
        "SEAM: a bet of the seam step was scored", bets[:3])
    for k in ("note", "reward", "goal"):
        assert c not in on["calls"][k], (f"SEAM: {k} was called at the seam cycle", on["calls"][k])
    assert on["grew"][str(c)] == 0, ("SEAM: the trace grew at the seam step", on["grew"])
    mint = [r["event"] for r in on["rows"] if r["cycle"] == c and r["event"] in (
        "mint", "accept", "park", "pull", "reuse_install", "derived_asked", "g1_want", "stream")]
    assert not mint, ("SEAM: a mint-type row at the seam cycle", mint)
    assert on["gate"][0] == "pass", ("SEAM: the gate refused", on["gate"])
    site = [flag for flag, r in on["tested"] if r.get("broke")]
    print(f"  SEAM ON: frame_break at cycle {c} ({brk[0]['detail'].get('claimed')} claims, "
          f"median {brk[0]['detail'].get('median')}) via "
          f"{':279 (cascade)' if site and site[0] else ':198 (settled read)'}; {len(bets)} of "
          f"{len(bets)} bets of that step suspended (seam), 0 scored; no Agency.note, "
          f"_route_reward or _note_goal_choice at {c}; no trace row; no mint-type row; gate pass")
    # C: after the break, a slot present on both sides reads only the rows after it
    assert on["window_at"] and on["cross"], ("C occasion: no slot on both sides of the break",
                                             on["window_at"], on["cross"])
    assert all(h == post for h, _pre, post in on["cross"].values()), ("C: history crossed the "
                                                                       "break", on["cross"])
    coff = child_env("on", {"TETHER_BREAK_WINDOW": "0"})
    assert coff["window_at"] and coff["cross"], ("C OFF occasion", coff["window_at"])
    assert all(h == pre + post for h, pre, post in coff["cross"].values()), ("C OFF: history "
                                                                              "was windowed",
                                                                              coff["cross"])
    k = sorted(on["cross"])[0]
    print(f"  C: window at trace row {on['window_at']}; {len(on['cross'])} slots on both sides "
          f"(e.g. {k}: history {on['cross'][k][0]} = the {on['cross'][k][2]} rows after the "
          f"break, not {on['cross'][k][1]} + {on['cross'][k][2]}). C OFF: history = all rows")
    sc = child("swapcascade")
    cs = sc["swap_cycle"]
    via = [r for flag, r in sc["tested"] if flag and r.get("broke")]
    assert via, ("CASCADE SWITCH occasion: no break through :279", sc["tested"])
    after = [r for flag, r in sc["tested"] if not flag]
    sbrk = [r for r in sc["rows"] if r["event"] == "frame_break"]
    sbets = obj_bets(sc["rows"], cs)
    assert sbrk and sbrk[0]["cycle"] == cs and len(sbrk) == 1, ("CASCADE SWITCH: frame_break",
                                                                sbrk, cs)
    assert sbets and all(r["detail"].get("seam") for r in sbets), ("CASCADE SWITCH: seam",
                                                                   sbets[:2])
    assert sc["grew"][str(cs)] == 0, ("CASCADE SWITCH: trace grew", sc["grew"])
    print(f"  CASCADE SWITCH: the break is read at :279 (median {via[0]['median']}, colour "
          f"{via[0]['colour_share']}); the settled :198 call on the same frame is untested "
          f"({len(after)} later :198 tests, none undoing it); one frame_break row at cycle {cs}; "
          f"{len(sbets)} of {len(sbets)} bets suspended (seam); no trace row")
    off = child("off")
    co = off["swap_cycle"]
    assert co is not None and not any(r["event"] == "frame_break" for r in off["rows"]), "SEAM OFF"
    bo = obj_bets(off["rows"], co)
    assert any((r["detail"].get("mass") or 0) > 0 and not r["detail"].get("suspended")
               for r in bo), ("SEAM OFF: the swap's bets were not scored", bo[:3])
    assert co in off["calls"]["note"], ("SEAM OFF: Agency.note not called", off["calls"])
    assert off["grew"][str(co)] == 1, ("SEAM OFF: the swap row was not appended", off["grew"])
    print(f"  SEAM OFF: no frame_break; the swap cycle {co}'s bets are scored, Agency.note is "
          "called there, and its trace row is appended")
    cas = child("cascade")
    inner = [r for flag, r in cas["tested"] if flag and r["tested"]]
    # a recolour at a HIGH score (the fake's block also moves, so the median is just under 1.0;
    # the exact-1.0 toggle is the tracker case above)
    toggles = [r for _f, r in cas["tested"] if r["tested"] and r["colour_share"] > 0
               and r["median"] >= arc_percept.BREAK_MEDIAN]
    assert inner, ("MF2 occasion (b): no claim through the cascade path (:279)", cas["tested"])
    assert toggles, ("MF2 occasion (a) in the agent: no high-score recolour", cas["tested"])
    assert not any(r.get("broke") for _f, r in cas["tested"]), ("MF2: the cascade broke",
                                                               cas["tested"])
    assert not any(r["event"] == "frame_break" for r in cas["rows"]), "MF2: a frame_break row"
    print(f"  MF2 cascade: {len(inner)} tested calls inside _walk_cascade (an intermediate frame "
          f"equal to the settled one), {len(toggles)} high-score recolours (median "
          f"{toggles[0]['median']}, colour {toggles[0]['colour_share']}), no break")


def off_identity() -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        # the tree before B: the last commit without arc_percept.BREAK_MEDIAN, archived whole
        rev = next(h for h in subprocess.run(
            ["git", "-C", root, "log", "--first-parent", "--format=%H"], capture_output=True,
            text=True, check=True).stdout.split()
            if "BREAK_MEDIAN" not in subprocess.run(
                ["git", "-C", root, "show", f"{h}:arc_percept.py"], capture_output=True,
                text=True, check=True).stdout)
        tar = subprocess.run(["git", "-C", root, "archive", rev], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = child("plain", d)
    os.environ["TETHER_FRAME_BREAK"] = "0"
    try:
        # the R4 record arm OFF too: its rows postdate the base tree (the reviewer 18:43); and
        # TETHER_KIND_CARRY, an arm downstream of B, so "before B, B off" includes its OFF
        # (the reviewer 2026-10-25 09:01); and TETHER_ROUTE_REFUSE (R-C, 429f36e 2026-10-24),
        # which postdates this test's base and changes hypothesis_test rows; it stays ON in every
        # run of the agent (Isaiah 2026-10-24 14:16), OFF only here (the reviewer 2026-10-25 09:31);
        # and TETHER_HYP_ROUTE_FIRST (P1, 2026-10-25), which postdates the base: ON it leaves the
        # picks unchanged and moves the search rows' counts (3 rows: checked, refused, open,
        # ranked); and TETHER_OWN_CLOCK_SUBJECT (D2, 2026-10-25), likewise later than the base:
        # ON it refuses 42 clock-naming candidates here, the pick unchanged (2 rows' counts move)
        cur = child_env("plain", {"TETHER_FRAME_BREAK": "0", "TETHER_R4_RECORD": "0",
                                  "TETHER_KIND_CARRY": "0", "TETHER_ROUTE_REFUSE": "0",
                                  "TETHER_HYP_ROUTE_FIRST": "0",
                                  "TETHER_OWN_CLOCK_SUBJECT": "0"})
    finally:
        os.environ.pop("TETHER_FRAME_BREAK", None)

    # the one shared timing list, imported (the reviewer 2026-10-25 21:52)
    sys.path.insert(0, os.path.join(_repo.ROOT, "conform"))
    from identity_mod_rows import mask_timings

    def norm(rows):
        out = []
        for r in mask_timings(json.loads(json.dumps(rows))):
            d = dict(r["detail"])
            if r["event"] == "arms":
                continue
            out.append((r["cycle"], r["step"], r["slot"], r["event"], json.dumps(d, sort_keys=True,
                                                                                  default=str)))
        return out
    nb, nc = norm(base["rows"]), norm(cur["rows"])
    diff = sum(1 for x, y in zip(nb, nc, strict=False) if x != y) + abs(len(nb) - len(nc))
    assert len(nb) > 50 and diff == 0, ("OFF identity", len(nb), len(nc),
                                       next((i for i, (x, y) in enumerate(zip(nb, nc, strict=False))
                                             if x != y), None))
    assert not any("calls" in r["detail"] for r in cur["rows"] if r["event"] == "matches"), (
        "OFF identity: a matches row carries calls")
    assert not any(r["event"] == "frame_break" for r in cur["rows"]), "OFF: a frame_break row"
    assert cur["calls"] == base["calls"] and cur["grew"] == base["grew"], (
        "OFF identity: the agent's outputs differ", cur["calls"], base["calls"])
    print(f"  OFF identity: {len(nb)} rows compared, {diff} differences (the arms row excluded: it "
          "lists the new arm and the tree's own file shas; wall timings masked); no calls field, "
          "no frame_break row; the spied credit calls and the trace growth per step equal")


def child_env(mode: str, extra: dict) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0", **extra)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, str(_repo.ROOT), mode], env=env,
                         capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    tracker_cases()
    agent_cases()
    off_identity()
    print("frame_break: OK")


if __name__ == "__main__":
    main()
