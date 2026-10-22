"""(B), THE UNITS ONCE PER FIT (TETHER_FIT_UNITS; the reviewer 2026-10-21 02:02). gridworld_arc_s1,
15 steps, the agent and hash seeds pinned, four processes: ON, CHECK (ON + TETHER_FIT_UNITS_CHECK:
every reuse also takes _units_for fresh and compares; the fresh units are used), OFF and PLANT
(CHECK + a refusal appended INSIDE the candidate loop).

  PRECONDITION: the CHECK run reuses the units (fit_units_agree > 0), or the rest is vacuous.
  (1) CHECK: every reuse equals the fresh units (0 disagree); ON's rows are CHECK's once the two
      fit_units_* book counters are masked -- no decision moves.
  (2) PLANT: one settled two-atom term held before the game (a cold gridworld settles no
      composite, and _units_for filters only composites), then refused INSIDE the loop under the
      slot's key, as tether.py's one writer of _not does: the CHECK disagrees, so the check can see
      a stale reuse.
  OFF: no fit_units counter moves.
  (3), OFF identity against 35c283a, is run apart (the ledgers through ident_mask).

    python test_fit_units.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, plant = sys.argv[1], sys.argv[2] == "1"
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world

state = {"slot": None, "planted": None, "bits_in_fit": 0}
if plant:
    _fit, _bits = tether.Agent._library_fit, tether.Agent._bits

    def fit(self, slot, exclude):
        state["slot"], state["bits_in_fit"] = slot, 0
        try:
            return _fit(self, slot, exclude)
        finally:
            state["slot"] = None

    def bits(self, x):
        # inside a fit, after its units were taken: refuse the planted composite under the
        # slot's key, as tether's one writer of _not does
        if state["slot"] is not None and state["planted"] is None and isinstance(x, tuple):
            state["bits_in_fit"] += 1
            if state["bits_in_fit"] == 1 and any(u.atoms == PAIR for u in x[1]):
                gk = self._term_gkey(state["slot"])
                self._not.setdefault(("planted_pair", gk), []).append(self._refusal_scope())
                state["planted"] = "planted_pair"
        return _bits(self, x)

    tether.Agent._library_fit = fit
    tether.Agent._bits = bits
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="units"), tether.Config(), ledger.Ledger())
if plant:
    # a cold gridworld settles no composite in 15 steps, and _units_for filters only composites,
    # so the plant first holds ONE settled two-atom term (a composite unit) for the refusal to hit
    PAIR = tuple(ag.gamma.atoms[:2])
    ag.gamma.library["planted_pair"] = gamma.Term(PAIR)
    _settled = ag.gamma.is_settled
    ag.gamma.is_settled = lambda name, slot=None: name == "planted_pair" or _settled(name, slot)
    assert any(u.atoms == PAIR for u in ag.gamma.units_held()), "the planted pair is not a unit"
for _ in range(15):
    ag.step()
b = ag.gamma.book
print(json.dumps({"on": tether._FIT_UNITS, "check": tether._FIT_UNITS_CHECK,
                  "agree": b.get("fit_units_agree", 0), "disagree": b.get("fit_units_disagree", 0),
                  "planted": state["planted"], "rows": ag.led.rows()}, default=str))
'''


def _run(on: str, check: str, plant: str = "0") -> dict:
    here = os.path.dirname(os.path.abspath(__file__))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_FIT_UNITS=on, TETHER_FIT_UNITS_CHECK=check)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here, plant], env=env,
                         capture_output=True, text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "conform"))
    from identity_mod_rows import compare
    on, chk, off, pl = _run("1", "0"), _run("1", "1"), _run("0", "0"), _run("1", "1", "1")
    assert on["on"] is True and chk["check"] is True and off["on"] is False
    assert chk["agree"] > 0, f"PRECONDITION: no reuse checked: {chk['agree']}"
    assert chk["disagree"] == 0, chk["disagree"]                                          # (1)
    keys = ("fit_units_agree", "fit_units_disagree")
    for rs in (on["rows"], chk["rows"]):
        for r in rs:
            if r["event"] == "books":
                for k in keys:
                    r["detail"].pop(k, None)
            elif r["event"] == "arms" and r["slot"] == "@run":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
    bad = compare(chk["rows"], on["rows"], set())
    assert not bad, bad[:3]
    assert pl["planted"] and pl["disagree"] > 0, (pl["planted"], pl["disagree"])          # (2)
    assert off["agree"] == off["disagree"] == 0, (off["agree"], off["disagree"])
    print(f"test_fit_units: pass ((1) CHECK {chk['agree']} reuses equal their fresh units, 0 "
          f"disagree, and ON's {len(on['rows'])} rows are CHECK's; (2) a refusal of "
          f"{pl['planted']!r} planted inside the loop: {pl['disagree']} disagree; OFF moves no "
          f"counter)")


if __name__ == "__main__":
    main()
