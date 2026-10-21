"""(2a), ONE DEFINITION ONCE PER FIT (TETHER_FIT_DEDUP; the reviewer 2026-10-21 04:40).
gridworld_arc_s1, the agent and hash seeds pinned, each run its own process.

  PRECONDITION: the CHECK run reuses a definition (fit_dedup_agree > 0), or (1) is vacuous.
  (1) 15 steps ON, CHECK (ON + TETHER_FIT_DEDUP_CHECK: every reuse also computed fresh and
      compared; the fresh values used) and OFF: 0 disagree; ON's rows are CHECK's and OFF's once
      the fit_dedup_* book counters and the arms row's on/off lists are masked.
  (2) THE CARRY PLANT (TETHER_CARRY_PRICE=1), 8 steps, then one fit: two names, "pa" and "pb",
      hold ONE definition (equal Terms, two objects) and the carry credits only one of them (and
      the reference price is planted low, so a credited payer wins). OFF picks the credited name;
      ON picks the same name with the same carry, crediting "pa" and crediting "pb". BROKEN (the
      carry cached per definition, the defect the per-name rule forbids) crediting "pb" does not
      pick "pb" -- the plant can see a carry shared across names.
  (3), OFF identity against 920dfc7, is run apart (the ledgers through ident_mask).

    python test_fit_dedup.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

PROBE = r'''
import dataclasses, json, sys
sys.dont_write_bytecode = True
tree, mode, credit, broken = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] == "1"
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world

env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="dedup"), tether.Config(), ledger.Ledger())
b = ag.gamma.book
if mode == "game":
    for _ in range(15):
        ag.step()
    print(json.dumps({"on": tether._FIT_DEDUP, "check": tether._FIT_DEDUP_CHECK,
                      "agree": b.get("fit_dedup_agree", 0),
                      "disagree": b.get("fit_dedup_disagree", 0), "rows": ag.led.rows()},
                     default=str))
    raise SystemExit
assert tether._CARRY_PRICE and tether._BARGAIN_FIT
for _ in range(8):
    ag.step()
lib = ag.gamma.library
slot = t = None
for s in sorted(ag.slots):
    if not ag.history(s):
        continue
    t = next((x for x in lib.values() if not x.reads_operand
              and tether._may_bind(x, ag.slot_types.get(s))), None)
    if t is not None:
        slot = s
        break
assert slot is not None, "PRECONDITION: no slot with history and a bindable term"
lib["pa"], lib["pb"] = dataclasses.replace(t), dataclasses.replace(t)
assert lib["pa"] == lib["pb"] == t and lib["pa"] is not lib["pb"]
ag._carry_ref = lambda: (len(lib), -1e9)
memo = {}


def carry(name, cand, *a):
    if not broken:
        return name == credit
    if cand not in memo:                  # the defect: one carry per definition
        memo[cand] = name == credit
    return memo[cand]


ag._carry_credit = carry
n0 = len(ag.led.rows())
ag._library_fit(slot, None)
pulls = [r for r in ag.led.rows()[n0:] if r["event"] == "pull"]
d = pulls[-1]["detail"] if pulls else {}
print(json.dumps({"on": tether._FIT_DEDUP, "slot": slot, "def": t.name, "held": d.get("held"),
                  "carry": d.get("carry"), "pulls": len(pulls)}, default=str))
'''


def _run(on: str, check: str, mode: str = "game", credit: str = "", broken: str = "0") -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_FIT_DEDUP=on, TETHER_FIT_DEDUP_CHECK=check)
    if mode == "plant":
        env["TETHER_CARRY_PRICE"] = "1"
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, HERE, mode, credit or "-", broken],
                         env=env, capture_output=True, text=True, timeout=1200, cwd=HERE)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _mask(rows: list) -> list:
    for r in rows:
        if r["event"] == "books":
            for k in ("fit_dedup_agree", "fit_dedup_disagree"):
                r["detail"].pop(k, None)
        elif r["event"] == "arms" and r["slot"] == "@run":
            r["detail"].pop("on", None)
            r["detail"].pop("off", None)
        elif r["event"] == "goal_hypotheses":
            r["detail"].pop("wall_s", None)
    return rows


def main() -> None:
    sys.path.insert(0, os.path.join(HERE, "conform"))
    from identity_mod_rows import compare
    on, chk, off = _run("1", "0"), _run("1", "1"), _run("0", "0")
    assert on["on"] is True and chk["check"] is True and off["on"] is False
    assert chk["agree"] > 0, f"PRECONDITION: no reuse checked: {chk['agree']}"
    assert chk["disagree"] == 0, chk["disagree"]                                          # (1)
    assert off["agree"] == off["disagree"] == on["agree"] == on["disagree"] == 0
    for a, b_ in ((chk, on), (off, on)):
        bad = compare(_mask(a["rows"]), _mask(b_["rows"]), set())
        assert not bad, bad[:3]
    got = {}
    for credit in ("pa", "pb"):
        for o in ("0", "1"):
            got[(credit, o)] = _run(o, "0", "plant", credit)
        x, y = got[(credit, "0")], got[(credit, "1")]
        assert x["held"] == credit and (x["carry"] or {}).get("credited") is True, x       # (2)
        assert (y["held"], y["carry"]) == (x["held"], x["carry"]), (x, y)
    bk = _run("1", "0", "plant", "pb", "1")
    assert bk["held"] != "pb", f"the plant cannot see a carry shared per definition: {bk}"
    print(f"test_fit_dedup: pass ((1) CHECK {chk['agree']} reuses equal fresh, 0 disagree; ON's "
          f"{len(on['rows'])} rows are CHECK's and OFF's; (2) one definition "
          f"{got[('pa', '0')]['def']!r} under 'pa' and 'pb' on {got[('pa', '0')]['slot']}: the "
          f"credited name is picked ON as OFF, both ways; the carry shared per definition picks "
          f"{bk['held']!r}, not 'pb')")


if __name__ == "__main__":
    main()
