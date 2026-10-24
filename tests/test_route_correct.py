"""R-C, COURSE CORRECTION -- the must-fails, PRE-REGISTERED before the build (Isaiah 2026-10-24
09:29: "can the agent gauge that it overshot? switch them back on and fix that - thats what course
correction is ... unless the agent is specific like "5 pixels" or something it will be general";
the reviewer 09:30 RC1-RC5, 09:37 alpha). Run with TETHER_ROUTE_REFUSE ON. They FAIL on 4fde7d6
(R-B as built), each with its occasion counted, so none can pass by not happening.
  THE SEAMS the build adds, named here first: Agent._intent_aim(slot, target) -> "general" |
  "specific" (today's agent always "general": its ordered intent states a sign only; a stub
  returns "specific"); the ledger events route_corrected and route_uncorrected ("no correction
  known"); the route_refused reason "overshoots_without_closing".
  THE ACTION RECORD is the agent's own: iface.table in the shape audit writes it, seeded here for
  the two offered actions -- the real iface.realise picks from it; nothing in the probe picks.
  RC1  a SPECIFIC target, a press that passes it: graded "overshot", never "farther"; not refused
  RC2  then the next goal exit issues the CORRECTION: the same target, the reversed sign, its
       action from the record, a route_corrected row; with no reverse action recorded, a
       route_uncorrected row ("no correction known"), nothing pressed -- ONCE per overshoot (the
       correction is cleared), and each counts one non-closing outcome on the overshooting
       route, so the second refuses it "no_shrink" (the reviewer 09:46, no deadlock)
  RC3  a GENERAL intent ("+"), a right-way move of 3: "reached" (the pre-registered overshoot
       must-fail of 496dadc, under alpha)
  RC4  a GENERAL intent, the wrong way: "farther", refused at once -- a PRESERVATION check: it
       passes on 4fde7d6 too, by design
  RC5  a SPECIFIC target, alternating overshoots with |gap| not shrinking: refused after
       MIN_REPEAT non-closing pairs, why "overshoots_without_closing"
    python tests/test_route_correct.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, case = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout, tether
import interface as IFace
from test_entry import FakeWrapper
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
for _ in range(12):
    ag.step()
sl = sorted(s for s, t in ag.slot_types.items() if t in tether.ORDERED_TYPES)[0]
ag.slot_types[sl] = "POSITION"
ag._hyp = None
ag._goal_choice = lambda why=None, book=False: sl
CTX = (("probe", 1),)
IFace.Interface.context = staticmethod(lambda env, actor=None: CTX)
UP, DN = [a for a in ag.actions if a != "RESET"][:2]
ag.actions = [UP, DN]
rec = {UP: {"n": 1, "delta": {(CTX, sl, "self"): (1, 42)}},
       DN: {"n": 1, "delta": {(CTX, sl, "self"): (1, -42)}}}
if case == "RC2b":
    rec.pop(DN)                      # no action is recorded moving it the other way
ag.iface.table = rec
SPECIFIC = case in ("RC1", "RC2a", "RC2b", "RC5")
if SPECIFIC:
    ag._intent_aim = lambda slot, tgt: "specific"
    ag._goal_target = lambda s, bf: 44                 # a named place: does not move with the slot
else:
    ag._goal_target = lambda s, bf: bf[s] + 1          # today's nominal target: before + 1
ag._route_refused, ag._route_run, ag._test = {}, {}, None
k0 = len(ag.led.rows())
MOVES = {"RC1": [(43, 85)], "RC2a": [(43, 85), (85, 40)],
         "RC2b": [(43, 85), (85, 85), (43, 85), (85, 85)],
         "RC3": [(43, 46)], "RC4": [(43, 38)], "RC5": [(43, 50), (50, 38), (38, 50), (50, 38)]}
presses = []
for value, after in MOVES[case]:
    before = {sl: value}
    n = len(ag.led.rows())
    act = ag._goal_split(before)
    t = ag._test
    ag.trace.append((act, before, {sl: after}))
    ag._audit_at = ag.cycle
    if ag._test is not None:
        ag._test_row()
    rows = ag.led.rows(n)
    presses.append({"cycle": ag.cycle, "action": act, "before": value, "after": after,
                    "target": t["target"] if t else None, "intent": t["intent"] if t else None,
                    "outcome": next((r["detail"]["outcome"] for r in rows
                                     if r["event"] == "hypothesis_test"), None),
                    "events": [r["event"] for r in rows]})
    ag.cycle += 1
ev = [r for r in ag.led.rows()[k0:]
      if r["event"] in ("route_refused", "route_corrected", "route_uncorrected", "route_exhausted")]
print(json.dumps({"arm": tether._ROUTE_REFUSE, "up": UP, "dn": DN, "presses": presses,
                  "rows": [{"event": r["event"], **r["detail"]} for r in ev]}, default=str))
'''


def child(case: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_ROUTE_REFUSE="1")
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, str(_repo.ROOT), case], env=env,
                         capture_output=True, text=True, timeout=1800, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def passed(target, before, after) -> bool:
    return (before - target) * (after - target) < 0


def check(case: str, r: dict) -> list[str]:
    """The case's failures (empty is a pass); the occasion is asserted first."""
    p, rows = r["presses"], r["rows"]
    why = [x.get("why") for x in rows if x["event"] == "route_refused"]
    bad = []
    if case == "RC1":
        assert passed(44, p[0]["before"], p[0]["after"]), "occasion: the press did not pass 44"
        if p[0]["outcome"] != "overshot":
            bad.append(f"graded {p[0]['outcome']!r}, not 'overshot'")
        if why:
            bad.append(f"refused: {why}")
    elif case in ("RC2a", "RC2b"):
        assert passed(44, p[0]["before"], p[0]["after"]), "occasion: press 1 did not pass 44"
        corr = [x for x in rows if x["event"] == "route_corrected"]
        unk = [x for x in rows if x["event"] == "route_uncorrected"]
        if case == "RC2a":
            if not corr:
                bad.append("no route_corrected row")
            elif not (corr[0].get("target") == 44 and corr[0].get("direction") == "-"
                      and corr[0].get("before") == 43 and corr[0].get("after") == 85):
                bad.append(f"route_corrected row wrong: {corr[0]}")
            if p[1]["action"] != r["dn"]:
                bad.append(f"the correction pressed {p[1]['action']!r}, not the recorded "
                           f"reverse {r['dn']!r}")
            if not str(p[1]["intent"]).startswith("BECOME") or " - " not in f" {p[1]['intent']} ":
                bad.append(f"the correction intent is {p[1]['intent']!r}, not the reversed sign")
        else:
            assert passed(44, p[2]["before"], p[2]["after"]), "occasion: press 3 did not pass 44"
            if [x.get("why") for x in unk] != ["no correction known"] * 2:
                bad.append(f"not one route_uncorrected 'no correction known' per overshoot: {unk}")
            if p[1]["action"] is not None or p[3]["action"] is not None:
                bad.append(f"something was pressed with no correction known: "
                           f"{p[1]['action']!r}, {p[3]['action']!r}")
            # the reviewer 09:46 (no deadlock): each abstains ONCE -- the pending correction is
            # cleared, so the overshoot press between them is no abstention for it -- and each
            # counts one non-closing outcome on the overshooting route: MIN_REPEAT of them refuse
            # it the existing way, "no_shrink"
            if "route_uncorrected" in p[2]["events"]:
                bad.append(f"the pending correction was not cleared: press 3 {p[2]['events']}")
            if why != ["no_shrink"]:
                bad.append(f"the uncorrected exits were not counted non-closing: refusals {why}")
    elif case == "RC3":
        assert p[0]["after"] - p[0]["before"] == 3 and p[0]["intent"], "occasion: no +3 press"
        if p[0]["outcome"] != "reached":
            bad.append(f"a general right-way move of 3 graded {p[0]['outcome']!r}, not 'reached'")
        if why:
            bad.append(f"refused: {why}")
    elif case == "RC4":
        assert p[0]["after"] < p[0]["before"] and p[0]["intent"], "occasion: no wrong-way press"
        if p[0]["outcome"] != "farther":
            bad.append(f"the wrong way graded {p[0]['outcome']!r}, not 'farther'")
        if "farther" not in why:
            bad.append(f"the wrong way was not refused at once: {why}")
    elif case == "RC5":
        n_pass = sum(passed(44, x["before"], x["after"]) for x in p)
        assert n_pass >= 3, f"occasion: only {n_pass} presses passed the target"
        if "overshoots_without_closing" not in why:
            bad.append(f"no 'overshoots_without_closing' refusal: {why}")
        if "farther" in why:
            bad.append("an overshoot was refused as 'farther'")
    return bad


def main() -> None:
    fails = {}
    for case in ("RC1", "RC2a", "RC2b", "RC3", "RC4", "RC5"):
        r = child(case)
        assert r["arm"] is True, "the switch did not reach the module"
        bad = check(case, r)
        seen = [(x["before"], x["after"], x["outcome"], x["action"]) for x in r["presses"]]
        print(f"  {case}: {'PASS' if not bad else 'FAIL'}  presses " + json.dumps(seen)
              + f"  rows {[(x['event'], x.get('why')) for x in r['rows']]}"
              + "".join(f"\n      {b}" for b in bad))
        if bad:
            fails[case] = bad
    assert not fails, f"route_correct: {sorted(fails)} failed"
    print("route_correct: OK")


if __name__ == "__main__":
    main()
