"""(B), IN-GAME RECOVERY AFTER AN AGENT FAULT (TETHER_FAULT_RECOVER; the design post 2026-10-22
15:13, approved 15:17 with (C3), (C4)). arc_holdout.play's real loop on the fake game (FakeWrapper
through a stub Arcade), over a two-game fake lineage, with planted faults in Agent.step.

  a     one fault at step K: the game goes on to its last cycle (play returns), one agent_fault
        row, one fault_recovered row naming the fault's generation ("ended": "agent_fault") as the
        fresh agent's parent, the traceback beside the ledger; gate REFUSES the ledger (faults)
  b     the same fault twice (one raise site): the second is recorded repeat and ends the game;
        b2 a DIFFERENT fault recovers again; C4 two MemoryErrors from two sites: repeat by type
  c     TETHER_FAULT_RECOVER off: the game ends at the first fault, as item 4 alone
  e     a fault raised in a frame under arc_agi/: re-raised, never recorded or recovered
  r1    two fresh agents built from copies of the checked save on deep copies of the board take
        the same next action and write the same rows (identity_mod_rows.compare)
  r2    the fresh agent's state digest (state_digest's structures) equals a cold process's load
        of a copy of the same folder
  r3    a marker planted in the faulted agent's bindings is absent from the fresh agent; with the
        discard step disabled (keep_faulted) it SURVIVES (the check can fire)
  r4    the ledger's bytes before the recovery are its prefix after the game; the old wire() path
        (which opens a new Ledger and truncates) FAILS it
  (f), the gate's own defect, is in test_gate; (d), the identity replay, is the measurement's.

    python tests/test_fault_recover.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
sys.path.insert(0, os.path.join(HERE, "conform"))
from identity_mod_rows import compare  # noqa: E402  the one identity reader

K = 3
CYCLES = 12

SEED = r'''
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import arc_holdout, lineage, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
d = sys.argv[2]
for _g in range(2):
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
    for _ in range(4):
        env.observe()
        ag.step()
    ag.end_run("cap")
    lineage.write(d, ag, "fake")
print("seeded")
'''

DIGEST = r'''
import hashlib, json


def canon(x):
    if isinstance(x, dict):
        return ["D", sorted(([canon(k), canon(v)] for k, v in x.items()), key=repr)]
    if isinstance(x, (set, frozenset)):
        return ["S", sorted((canon(v) for v in x), key=repr)]
    if isinstance(x, (list, tuple)):
        return ["T" if isinstance(x, tuple) else "L", [canon(v) for v in x]]
    if isinstance(x, (int, float, str, bool)) or x is None:
        return x
    return ["R", repr(x)]


def digest(ag):
    """harness/mem_store/state_digest.py's structures, read off one agent after its load."""
    import lineage, tether
    S = {
        "lineage_parent": ag.lineage_parent, "gamma_blob": ag.gamma.blob(with_names=True),
        "kind_known": ag._kind_known, "kind_known_n": dict(ag._kind_known_n),
        "kind_last": ag._kind_last, "kdk_last": ag._kdk_last,
        "kind_known_dk": dict(ag._kind_known_dk), "kind_known_off": dict(ag._kind_known_off),
        "kind_pairs": ag._kind_pairs, "kind_seq": ag._kind_seq,
        "line_grade_in": ag._line_grade_in, "root_grade_in": ag._root_grade_in,
        "kind_carried_in": ag._kind_carried_in, "cause_kind_in": ag._cause_kind_in,
        "entry_use_in": ag._entry_use_in, "3a_in": ag._3a_in, "3a_written": ag._3a_written,
        "carried_used": ag.gamma.carried_used,
        "pending_index": {k[1:]: (v["gen"], [(i, ch, lineage._enc_c(c), lineage._enc_c(t))
                                             for i, ch, c, t in v["items"]])
                          for k, v in lineage._PENDING.items()},
        "index_store": len(tether._INDEX_STORE),
    }
    out = {k: hashlib.sha256(json.dumps(canon(v), sort_keys=True, default=repr).encode())
           .hexdigest()[:16] for k, v in S.items()}
    out["_index_store_n"] = len(tether._INDEX_STORE)
    return out


def mask_fold(rows):
    """the game-start fold's counts of what an EARLIER agent in the process left, which it clears
    (tether._consolidate); "after" stays"""
    kept = []
    for x in rows:
        if x["event"] == "consolidate" and x["detail"].get("trigger") == "game_start":
            kept.append({f: x["detail"].pop(f, None)
                         for f in ("before", "landed_cleared", "slot_rows_before")})
            kept[-1]["after"] = x["detail"].get("after")
    return kept
'''

CHILD = r'''
import copy, glob, json, os, pathlib, shutil, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
sys.path.insert(2, os.path.join(sys.argv[1], "conform"))
import arc_holdout, gate, ledger, lineage, tether
from identity_mod_rows import compare
from test_entry import FakeWrapper
tether._AGENT_SEED = False
d, led, k, mode = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
''' + DIGEST + r'''


class Arc:
    def make(self, _game):
        return FakeWrapper(script={})


def boom_key():
    raise KeyError("planted fault")


def boom_val():
    raise ValueError("another planted fault")


def boom_mem_a():
    raise MemoryError("planted memory fault a")


def boom_mem_b():
    raise MemoryError("planted memory fault b")


_ns = {}
exec(compile("def boom():\n    raise KeyError('in the game')\n",
             os.path.join(os.sep, "x", "arc_agi", "fake_game.py"), "exec"), _ns)
PLAN = {"once": {k: boom_key}, "r3keep": {k: boom_key}, "r4bad": {k: boom_key},
        "twice": {k: boom_key, k + 2: boom_key}, "two_kinds": {k: boom_key, k + 2: boom_val},
        "mem": {k: boom_mem_a, k + 2: boom_mem_b}, "off": {k: boom_key},
        "game": {k: _ns["boom"]}}[mode]
real = tether.Agent.step
calls = [0]
hook = {}
MARK = "MARKER_o9.x"


def step(self, *a, **kw):
    calls[0] += 1
    f = PLAN.get(calls[0])
    if f is not None:
        self.bound[MARK] = "marker_term"     # (r3): the faulted agent's episode state
        f()
    return real(self, *a, **kw)


tether.Agent.step = step
real_wa = arc_holdout.wire_agent


def wa(env, game, cfg, led_obj, library, lineage_dir, clock=None):
    if clock is None or "prefix" in hook:
        return real_wa(env, game, cfg, led_obj, library, lineage_dir, clock=clock)
    with open(led, "rb") as fh:
        hook["prefix"] = fh.read()                  # (r4): the ledger before the recovery
    hook["snap"] = d + "_snap"
    shutil.copytree(d, hook["snap"])                # (r2): the folder the fresh agent loads
    if mode == "once":                              # (r1): two fresh agents, same save, same board
        import pickle
        hook["board"], hook["clock"], hook["palette"] = d + "_board.pkl", list(clock), env._palette
        with open(hook["board"], "wb") as fh:       # (r2b): the board at the fault, for a cold step
            pickle.dump(copy.deepcopy(env.w.w), fh)
        outs = []
        for i in range(2):
            di = f"{d}_r1_{i}"
            shutil.copytree(d, di)
            wi = arc_holdout.ResetGuard(copy.deepcopy(env.w.w))   # a guard does not deep-copy
            ei = arc_holdout.world_on(wi, game, env._palette, None)
            li = ledger.Ledger(None)
            ai, _l = real_wa(ei, game, cfg, li, library, di, clock=clock)
            ei.observe()
            real(ai)
            outs.append((li.rows(), list(wi.w.calls)))     # wi: the ResetGuard; .w the board
        # the game-start fold counts what the agent BEFORE left in the process's bound stores and
        # clears it: those three counts differ by construction (r1_0 follows the faulted agent,
        # r1_1 follows r1_0), so they are masked and kept; "after" is not
        cleared = [c for rows_i, _c in outs for c in mask_fold(rows_i)]
        hook["r1"] = {"diff": compare(outs[0][0], outs[1][0], set()), "cleared": cleared,
                      "calls": [o[1] for o in outs], "rows": len(outs[0][0]),
                      "rows0": outs[0][0]}
    if mode == "r4bad":                             # the old path: a new Ledger on the same file
        _e, a2, *_ = arc_holdout.wire(env.w, game, led_path=led, lineage_dir=lineage_dir)
        a2.cycle, a2.deadline = clock
        return a2, None
    ag2, loaded = real_wa(env, game, cfg, led_obj, library, lineage_dir, clock=clock)
    hook["digest"] = digest(ag2)
    return ag2, loaded


arc_holdout.wire_agent = wa
real_sor = arc_holdout.step_or_recover


def sor(env, ag, ctx):
    if mode == "r3keep":
        ctx["keep_faulted"] = lambda a: a           # the discard step disabled
    before = len(ctx.get("faults", []))
    out = real_sor(env, ag, ctx)
    if len(ctx.get("faults", [])) > before and out[3] is None and "marker_after" not in hook:
        hook["marker_after"] = MARK in out[1].bound
    return out


arc_holdout.step_or_recover = sor
before = set(os.listdir(d))
raised = None
try:
    arc_holdout.play("fake", int(sys.argv[6]), arc=Arc(), led_path=led, lineage_dir=d)
except Exception as e:
    raised = f"{type(e).__name__}: {e}"
new = sorted(set(os.listdir(d)) - before)
with open(led, encoding="utf-8") as fh:
    rows = [json.loads(x) for x in fh if x.strip()]
with open(led, "rb") as fh:
    whole = fh.read()
ended = {}
for n in (x for x in new if x.startswith("gen_")):
    import lineage_store as ls
    ended[n[4:20]] = json.loads(ls.file_bytes(pathlib.Path(d, n))).get("ended")
out = {"raised": raised, "calls": calls[0], "ended": ended,
       "faults": [r["detail"] for r in rows if r["event"] == "agent_fault"],
       "recovered": [r["detail"] for r in rows if r["event"] == "fault_recovered"],
       "tb": sorted(os.path.basename(p) for p in glob.glob(led + ".fault*.txt")),
       "gate": gate.check(rows), "marker_after": hook.get("marker_after"), "r1": hook.get("r1"),
       "digest": hook.get("digest"), "snap": hook.get("snap"), "board": hook.get("board"),
       "clock": hook.get("clock"), "palette": hook.get("palette"),
       "prefix_ok": whole.startswith(hook["prefix"]) if "prefix" in hook else None,
       "prefix_len": len(hook.get("prefix", b""))}
print(json.dumps(out, default=str))
'''

COLD = r'''
import os, shutil, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import json, pickle, arc_holdout, ledger, tether
tether._AGENT_SEED = False
''' + DIGEST + r'''
d = sys.argv[2] + "_cold"
shutil.copytree(sys.argv[2], d)
with open(sys.argv[3], "rb") as fh:
    board = pickle.load(fh)
env = arc_holdout.world_on(arc_holdout.ResetGuard(board), "fake", int(sys.argv[4]), None)
led = ledger.Ledger(None)
ag, _l = arc_holdout.wire_agent(env, "fake", None, led, None, d,
                                clock=(int(sys.argv[5]), json.loads(sys.argv[6])))
dg = digest(ag)
env.observe()
ag.step()
rows = led.rows()
cleared = mask_fold(rows)
print(json.dumps({"digest": dg, "rows": rows, "cleared": cleared}, default=str))
'''


def run(code: str, *args: str, **arms) -> object:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0", **arms)
    p = subprocess.run([sys.executable, "-B", "-c", code, HERE, *args], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL, timeout=900)
    assert p.returncode == 0, p.stderr[-3000:]
    return p.stdout.strip().splitlines()[-1]


def game(mode: str, **arms) -> dict:
    d = tempfile.mkdtemp(prefix="recover_")
    assert run(SEED, d) == "seeded"
    led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
    return json.loads(run(CHILD, d, led, str(K), mode, str(CYCLES), **arms))


def main() -> int:
    r = game("once")
    assert r["raised"] is None and r["calls"] == CYCLES, ("a: the game must go on", r)
    assert len(r["faults"]) == 1 and r["faults"][0]["repeat"] is False, ("a: one row", r)
    assert len(r["recovered"]) == 1 and r["tb"] == ["r.jsonl.fault1.txt"], ("a", r)
    fault_gen = [h for h, e in r["ended"].items() if e == "agent_fault"]
    assert fault_gen == [r["recovered"][0]["parent"]], ("a: the fresh agent loads the fault's", r)
    assert r["gate"]["verdict"] == "refuse" and r["gate"]["check"] == "faults", ("a: gate", r)
    print(f"  a  one fault at step {K}: the game went on to cycle {r['calls']}; agent_fault 1 "
          f"(repeat False); fault_recovered 1, parent {fault_gen[0]} (ended agent_fault); "
          f"traceback {r['tb']}; gate {r['gate']['verdict']} at {r['gate']['check']}")
    r1 = r["r1"]
    assert r1 and not r1["diff"] and r1["calls"][0] == r1["calls"][1] and r1["rows"], ("r1", r1)
    cl = r1["cleared"]
    assert len(cl) == 2 and cl[0]["after"] == cl[1]["after"], ("r1: the fold's after", cl)
    assert all(not any(v for v in c["after"].values()) for c in cl), ("r1: left after", cl)
    print(f"  r1 two fresh agents from copies of the save on copies of the board: "
          f"{r1['rows']} rows equal, last calls {r1['calls'][0][-1:]} equal; the game-start fold "
          f"cleared an earlier agent's leftovers, every store empty after: {cl}")
    c = json.loads(run(COLD, r["snap"], r["board"], str(r["palette"]), str(r["clock"][0]),
                       json.dumps(r["clock"][1])))
    cold, fresh = c["digest"], r["digest"]
    proc = ("index_store", "_index_store_n")    # the process's compile cache, read separately
    diff = sorted(k for k in set(cold) | set(fresh)
                  if k not in proc and cold.get(k) != fresh.get(k))
    assert not diff, ("r2: the fresh agent's load differs from a cold load of the save", diff)
    print(f"  r2 the fresh agent's load equals a cold process's load of the same save on "
          f"{len([k for k in cold if k not in proc])} structures; the process's compile cache "
          f"tether._INDEX_STORE: fresh {fresh['_index_store_n']} entries, cold "
          f"{cold['_index_store_n']} (READ, NOT ASSERTED: for the reviewer's ruling)")
    d2 = compare(r1["rows0"], c["rows"], set())
    assert not d2, ("r2b: the fresh agent's step differs from a cold process's", d2)
    print(f"  r2b the fresh agent's next step and a cold process's on the same board from the same "
          f"save: {len(c['rows'])} rows equal (the cold fold cleared {c['cleared']})")
    assert r["marker_after"] is False, ("r3: the faulted agent's binding crossed", r)
    rk = game("r3keep")
    assert rk["marker_after"] is True, ("r3 MF: with the discard disabled the marker must survive",
                                        rk)
    print("  r3 the faulted agent's planted binding is absent from the fresh agent; with the "
          "discard disabled it survives (the check fires)")
    assert r["prefix_ok"] is True and r["prefix_len"] > 0, ("r4", r)
    rb = game("r4bad")
    assert rb["prefix_ok"] is False, ("r4 MF: the truncating old path must fail the check", rb)
    print(f"  r4 the {r['prefix_len']} ledger bytes before the recovery are its prefix after the "
          f"game; through the old wire() path they are not (the check fires)")
    r = game("twice")
    assert r["raised"] and r["raised"].startswith("KeyError"), ("b: a repeat ends the game", r)
    assert [f["repeat"] for f in r["faults"]] == [False, True] and len(r["recovered"]) == 1, r
    assert "agent_fault" in r["ended"].values(), ("b: the end path's generation", r)
    print(f"  b  the same fault twice: recovered once, the second recorded repeat, the game "
          f"ended ({r['raised']})")
    r = game("two_kinds")
    assert r["raised"] is None and len(r["recovered"]) == 2, ("b2: a different fault recovers", r)
    assert r["tb"] == ["r.jsonl.fault1.txt", "r.jsonl.fault2.txt"], ("b2", r)
    print("  b2 two different faults: both recovered, two traceback files")
    r = game("mem")
    assert r["raised"] and r["raised"].startswith("MemoryError"), ("C4", r)
    assert [f["repeat"] for f in r["faults"]] == [False, True], ("C4: repeat by type", r)
    print(f"  C4 two MemoryErrors from two sites: the second is a repeat by type ({r['raised']})")
    r = game("off", TETHER_FAULT_RECOVER="0")
    assert r["raised"] and not r["recovered"] and len(r["faults"]) == 1, ("c", r)
    print(f"  c  TETHER_FAULT_RECOVER off: the game ended at the first fault ({r['raised']})")
    r = game("game")
    assert r["raised"] and not r["faults"] and not r["recovered"], ("e", r)
    print(f"  e  a fault raised under arc_agi/: re-raised, never recorded or recovered "
          f"({r['raised']})")
    print("fault recover: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
