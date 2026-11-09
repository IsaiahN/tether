"""R1 (the reviewer 2026-11-06 r1294): a goal hypothesis held at a level boundary is closed by
retarget's GQ2 block; its goal_hypothesis_end row joins the boundary's own chain on "@boundary"
(the object in hyp_slot), so the next step's PERCEIVE on the object's slot in the same cycle no
longer runs that slot's chain backwards and the gate passes the ledger. gridworld_arc_s1, the agent
seed pinned, stepped until a hypothesis is held; the boundary planted as play() makes it (retarget
between steps, the cycle already advanced). Each check in its own process; a tree may be named.

  R1a GAME LOSS: a held hypothesis at a planted game loss, then one step: the gate's step order
      holds and
      the whole gate passes; the end row is on "@boundary" with the object in hyp_slot.
      Red at 4a1cc5d: "<slot>: PERCEIVE after IMPORT".
  R1b WIN: the same boundary on a win still credits the hypothesis's shelf record (won), ends it
      "level_cleared", on "@boundary".

    python tests/test_r1_boundary_end.py [tree] [check ...]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import collections, json, sys
sys.dont_write_bytecode = True
tree, which = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, gate, ledger, panel, tether, world
tether._AGENT_SEED = False
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="r1"), tether.Config(), ledger.Ledger())
for _ in range(40):
    ag.step()
    if ag._hyp is not None:
        break
else:
    raise SystemExit("no hypothesis held in 40 steps")
slot = ag._hyp["slots"][0]
out = {"slot": slot}
if which == "game_loss":
    ag.retarget(ag.env, ag.level, how=ledger.GAME_LOSS)
    ag.step()
    rows = ag.led.rows()
    out["steps"] = gate._steps(rows)
    out["verdict"] = gate.check(rows)
else:
    ag._hyp["shelf"] = "r1-shelf"
    ag._goal_shelf["r1-shelf"] = {"record": collections.Counter()}
    ag.retarget(ag.env, ag.level + 1, how=ledger.WIN)
    out["record"] = dict(ag._goal_shelf["r1-shelf"]["record"])
end = [r for r in ag.led.rows() if r["event"] == "goal_hypothesis_end"][-1]
out["end"] = {"slot": end["slot"], "step": end["step"], "why": end["detail"].get("why"),
              "ended_by": end["detail"].get("ended_by"), "hyp_slot": end["detail"].get("hyp_slot")}
print(json.dumps(out, default=str))
'''


def _probe(tree: str, which: str) -> dict:
    p = subprocess.run([sys.executable, "-B", "-c", PROBE, tree, which], capture_output=True,
                       text=True, cwd=tree, stdin=subprocess.DEVNULL,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    assert p.returncode == 0, p.stderr[-1500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def check_r1a_game_loss(tree: str) -> None:
    o = _probe(tree, "game_loss")
    assert o["steps"] is None, ("the step order refused", o["steps"])
    assert o["verdict"]["verdict"] == "pass", o["verdict"]
    e = o["end"]
    # an untested hold keeps its boundary as ended_by (UNTESTED_KEEP)
    assert e["slot"] == "@boundary" and e["hyp_slot"] == o["slot"], e
    assert "closed_game_loss" in (e["why"], e["ended_by"]), e
    print(f"  game loss with {o['slot']} held, then a step: the gate passes; the end on @boundary, "
          f"hyp_slot {e['hyp_slot']}")


def check_r1b_win(tree: str) -> None:
    o = _probe(tree, "win_probe")
    assert o["record"].get("won") == 1, o["record"]
    e = o["end"]
    assert e["slot"] == "@boundary" and e["why"] == "level_cleared", e
    print(f"  win with {o['slot']} held: shelf record {o['record']}, ended level_cleared on "
          f"@boundary")


def main() -> int:
    args = sys.argv[1:]
    tree = args.pop(0) if args and os.path.isdir(args[0]) else str(_repo.ROOT)
    names = [k for k in globals() if k.startswith("check_") and (not args or k in args)]
    if len(names) == 1:
        globals()[names[0]](tree)
        print("ok  ", names[0])
        return 0
    bad = [n for n in names if subprocess.run([sys.executable, "-B", __file__, tree, n],
                                              cwd=str(_repo.ROOT),
                                              stdin=subprocess.DEVNULL).returncode]
    assert not bad, bad
    print(f"r1_boundary_end: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
