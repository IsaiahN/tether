"""C-7h-1, 7h (the reviewer 2026-10-15 17:32, 19:59): the tried count, the shown frequency, root.

  R1  a root row at birth, and after a death's restart, none while dead; its fields answer what is
      shown, expected, open, owed, and name no action, button or coordinate
  R2  every choice row after a root carries that root's id
  R3  a root written before a death gets a verdict row with ending "death" at that boundary
  T1  site 8: two operands equal in everything but this level's tries go fewer-tries-first; MF with
      no tried count the draw decides (the order today)
  S1  site 9: a value shown 3 times reads 3, one shown once reads 1; MF OFF reads 1 and 1
  Runs under the old seed constant (C-seed-X): R1-R3 need a birth that restarts after its death.

    python test_7h.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

RUN = r"""
import json, sys, tempfile, os
sys.dont_write_bytecode = True
import tether_agent
from arcengine import GameState
from test_entry import FakeWrapper
led = os.path.join(tempfile.mkdtemp(prefix="t7h_"), "led.jsonl")
w = FakeWrapper(script={2: GameState.GAME_OVER})
out = tether_agent.run(w, "fake", max_actions=8, led_path=led)
rows = [json.loads(x) for x in open(led, encoding="utf-8")]
keep = [[r["seq"], r["event"], r["detail"]] for r in rows
        if r["event"] in ("intent_root", "intent_verdict", "choice")]
print("OUT " + json.dumps({"rows": keep, "end": out["end"], "resets": out["agent_resets"],
                           "calls": w.calls}))
"""

SHOWN = r"""
import json, sys
sys.dont_write_bytecode = True
import gamma, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
bs, as_ = [3, 3, 3, 5], [3, 3, 5, 7]
ag.trace = [({"x": b}, None, {"x": a}, None, None) for b, a in zip(bs, as_)]
ag.alphabet["x"] = 10
d = ag._domain("x", {"x": 7, "_fresh": 1}, gamma.Ctx())
print("OUT " + json.dumps({str(k): v for k, v in sorted(d.counts.items())}))
"""


def _run(code: str, arms: dict) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"TETHER_AGENT_SEED": "0"}, **arms)
    r = subprocess.run([sys.executable, "-B", "-c", code], env=env, capture_output=True,
                       text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads([ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")][-1][4:])


def main() -> None:
    run = _run(RUN, {})
    roots = [(s, d) for s, e, d in run["rows"] if e == "intent_root"]
    verdicts = [(s, d) for s, e, d in run["rows"] if e == "intent_verdict"]
    assert run["end"] != "death" and run["resets"] >= 1, ("precondition: no restart", run)
    assert len(roots) >= 2 and all(d["alive"] for _s, d in roots), ("R1", roots)
    first = roots[0][1]
    for k in ("shown", "expected", "open", "owed"):
        assert k in first, ("R1 field", k)
    blob = json.dumps([d for _s, d in roots])
    assert not any(x in blob for x in ("ACTION", "RESET", "coord")), ("R1 A3", blob[:300])
    print(f"  R1 {len(roots)} roots, all alive; shown {first['shown']}, expected"
          f" {first['expected']}; no action, button or coordinate")
    by_seq = sorted(roots)
    bad = []
    for s, e, d in run["rows"]:
        if e == "choice":
            live = [r for r in by_seq if r[0] < s]
            want = live[-1][1]["root"] if live else None
            # a root graded by a verdict (the death) before this choice is closed: while dead there
            # is no root (R1), so a choice made then -- 7h (f)'s exit row -- carries none
            if live and any(live[-1][0] < v < s for v, _vd in verdicts):
                want = None
            if d.get("root") != want:
                bad.append([s, d.get("root"), want])
    n_choice = sum(e == "choice" for _s, e, _d in run["rows"])
    assert n_choice and not bad, ("R2", n_choice, bad[:3])
    print(f"  R2 {n_choice} choice rows each carry the root before them")
    assert verdicts and verdicts[0][1]["root"] == first["root"] \
        and verdicts[0][1]["ending"] == "death", ("R3", verdicts)
    print(f"  R3 the birth root {first['root']} graded at the death: {verdicts[0][1]}")

    import frontier as FR
    from tether import _lookup_order
    draw = sorted(["a", "b"], key=lambda s: FR.draw_key("k", s, "0"))
    # the operand the draw puts LAST is given fewer tries, so the count and the draw disagree
    few, many = draw[1], draw[0]
    comp = {few: (0, False, 0, 1, 1), many: (0, False, 0, 1, 3)}
    assert _lookup_order(["a", "b"], comp, "k", seed="0") == [few, many], "T1"
    plain = {k: v[:4] for k, v in comp.items()}
    assert _lookup_order(["a", "b"], plain, "k", seed="0") == draw != [few, many], "T1 MF"
    print(f"  T1 fewer tries first ({few} before {many}); MF without the count the draw decides"
          f" ({draw})")

    on, off = _run(SHOWN, {}), _run(SHOWN, {"TETHER_7H_SHOWN": "0"})
    assert on.get("3") == 3 and on.get("5") == 1 and on.get("7") == 1, ("S1", on)
    assert off.get("3") == 1 and off.get("5") == 1, ("S1 MF", off)
    print(f"  S1 shown counts ON {on}; MF OFF {off}")
    print("7h: OK")


if __name__ == "__main__":
    main()
