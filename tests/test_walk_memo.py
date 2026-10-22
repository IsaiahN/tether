"""(A), THE WALK MEMO (TETHER_WALK_MEMO; the reviewer 2026-10-20 21:18, 21:28 CDT).
gridworld_arc_s1, 15 steps, the agent seed pinned, three processes: ON, CHECK (ON +
TETHER_WALK_MEMO_CHECK: every hit is also walked fresh and compared, the fresh walk used) and OFF.

  PRECONDITION: the ON run hits the memo (walk_memo_hit > 0), or the rest is vacuous.
  (1) the CHECK run: every kept entry walk equals its fresh walk -- views, causes, refusals, _spent
      charges, landings and the asked tally (agree == ON's hits, disagree 0); and ON's rows are the
      CHECK run's rows (a hit charges the budget and lands its kinds as the walk would, so no
      decision moves): identical once the books row's walk_memo_* counters are masked.
  (2) the held index is a pure function of (compile signature, entry, role) inside a process, so a
      planted signature change (the atoms' compile signature) makes the next step's walks all
      misses: no hit after the plant.
  OFF: no walk_memo counter moves.

    python tests/test_walk_memo.py
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
tree = sys.argv[1]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import compile_term, gamma, ledger, panel, tether, world

env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="walk"), tether.Config(), ledger.Ledger())
for _ in range(15):
    ag.step()
b = ag.gamma.book
out = {"memo": tether._WALK_MEMO, "check": tether._WALK_MEMO_CHECK,
       **{k: b.get(k, 0) for k in ("walk_memo_hit", "walk_memo_miss", "walk_memo_agree",
                                   "walk_memo_disagree")},
       "rows": ag.led.rows()}
if tether._WALK_MEMO and not tether._WALK_MEMO_CHECK:
    real = compile_term.signature
    compile_term.signature = lambda atoms: ("planted", real(atoms))
    h0, m0 = b.get("walk_memo_hit", 0), b.get("walk_memo_miss", 0)
    ag.step()
    compile_term.signature = real
    out.update(plant_hits=b.get("walk_memo_hit", 0) - h0,
               plant_misses=b.get("walk_memo_miss", 0) - m0)
print(json.dumps(out, default=str))
'''


def _run(memo: str, check: str) -> dict:
    here = _repo.ROOT
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_AGENT_SEED="0", TETHER_WALK_MEMO=memo,
               TETHER_WALK_MEMO_CHECK=check)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    here = _repo.ROOT
    sys.path.insert(0, os.path.join(here, "conform"))
    from identity_mod_rows import compare
    on, chk, off = _run("1", "0"), _run("1", "1"), _run("0", "0")
    assert on["memo"] is True and chk["check"] is True and off["memo"] is False
    assert on["walk_memo_hit"] > 0, f"PRECONDITION: no hit: {on['walk_memo_hit']}"
    assert chk["walk_memo_disagree"] == 0 and chk["walk_memo_agree"] == on["walk_memo_hit"], \
        (chk["walk_memo_agree"], chk["walk_memo_disagree"], on["walk_memo_hit"])
    keys = ("walk_memo_hit", "walk_memo_miss", "walk_memo_agree", "walk_memo_disagree")
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
    assert on["plant_hits"] == 0 and on["plant_misses"] > 0, (on["plant_hits"], on["plant_misses"])
    assert all(off[k] == 0 for k in keys), {k: off[k] for k in keys}
    print(f"test_walk_memo: pass (ON {on['walk_memo_hit']} hits / {on['walk_memo_miss']} misses; "
          f"(1) CHECK {chk['walk_memo_agree']} kept walks equal their fresh walks, 0 disagree, "
          f"and ON's {len(on['rows'])} rows are CHECK's; (2) a planted signature: "
          f"{on['plant_hits']} hits, {on['plant_misses']} misses on the next step; OFF moves no "
          f"counter)")


if __name__ == "__main__":
    main()
