"""(C), THE TIERS INDEX (TETHER_TIERS_INDEX; the reviewer 2026-10-21 03:05). gridworld_arc_s1, 15
steps, the agent and hash seeds pinned, four processes: ON, CHECK (ON + TETHER_TIERS_INDEX_CHECK:
every _tiers call also scans and compares the rung sums and the recency map; the scan's are used),
OFF and PLANT (CHECK + existing landed counts raised past the writer once the index is built).

  PRECONDITION: the CHECK run compares (tiers_index_agree > 0), or the rest is vacuous.
  (1) CHECK: every call's index sums equal the scan's (0 disagree); ON's rows are CHECK's once the
      tiers_index_* book counters are masked -- the same lists in the same order, no decision moves.
  (2) PLANT: counts changed past the writers (no key added, so the index's signature does not move)
      make the CHECK disagree, so the check can see a stale index.
  OFF: no tiers_index counter moves.
  (3), OFF identity against 41fa451, is run apart (the ledgers through ident_mask).

    python tests/test_tiers_index.py
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
tree, plant = sys.argv[1], sys.argv[2] == "1"
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world

state = {"planted": 0}
if plant:
    _tiers = tether.Agent._tiers

    def tiers(self, *a, **k):
        got = _tiers(self, *a, **k)
        # once the index is built and current, raise every landed count past the writer: no key
        # is added, so its signature stands and it goes stale
        if (not state["planted"] and self._kix is not None and self._kind_landed_dk
                and self._kix["sig"] == self._kix_sig()):
            for e in list(self._kind_landed_dk):
                dict.__setitem__(self._kind_landed_dk, e, self._kind_landed_dk[e] + 5)
            state["planted"] = len(self._kind_landed_dk)
        return got

    tether.Agent._tiers = tiers
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="tiers"), tether.Config(), ledger.Ledger())
for _ in range(15):
    ag.step()
b = ag.gamma.book
print(json.dumps({"on": tether._TIERS_INDEX, "check": tether._TIERS_INDEX_CHECK,
                  "agree": b.get("tiers_index_agree", 0),
                  "disagree": b.get("tiers_index_disagree", 0),
                  "fallback": b.get("tiers_index_fallback", 0), "planted": state["planted"],
                  "rows": ag.led.rows()}, default=str))
'''


def _run(on: str, check: str, plant: str = "0") -> dict:
    here = _repo.ROOT
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_TIERS_INDEX=on, TETHER_TIERS_INDEX_CHECK=check)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here, plant], env=env,
                         capture_output=True, text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    here = _repo.ROOT
    sys.path.insert(0, os.path.join(here, "conform"))
    from identity_mod_rows import compare
    on, chk, off, pl = _run("1", "0"), _run("1", "1"), _run("0", "0"), _run("1", "1", "1")
    assert on["on"] is True and chk["check"] is True and off["on"] is False
    assert chk["agree"] > 0, f"PRECONDITION: no call compared: {chk['agree']}"
    assert chk["disagree"] == 0 and chk["fallback"] == 0, (chk["disagree"], chk["fallback"])   # (1)
    keys = ("tiers_index_agree", "tiers_index_disagree", "tiers_index_fallback")
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
    assert off["agree"] == off["disagree"] == off["fallback"] == 0, off["agree"]
    print(f"test_tiers_index: pass ((1) CHECK {chk['agree']} calls' index sums equal the scan's, "
          f"0 disagree, and ON's {len(on['rows'])} rows are CHECK's; (2) {pl['planted']} landed "
          f"counts raised past the writer: {pl['disagree']} disagree; OFF moves no counter)")


if __name__ == "__main__":
    main()
