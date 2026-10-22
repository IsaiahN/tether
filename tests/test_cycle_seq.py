"""ONE SEQ PER CYCLE (TETHER_CYCLE_SEQ; the reviewer 2026-10-20 23:33). gridworld_arc_s1, 15 steps,
the agent seed pinned.

  (1) two ON runs under DIFFERENT hash seeds (1, 2): _kdk_last and _kind_last identical, and every
      row identical (masked: the arms row's pythonhashseed, which records the seed, and
      goal_hypotheses' wall_s, a timing). CONTROL: two OFF runs under the same two hash seeds DIFFER
      in those stores, so (1) can see the hash dependence it removes.
  (3) a planted two-landing cycle: ON both landings carry one seq; OFF consecutive seqs.
  (2), OFF identity against 582a223, is run apart (the ledgers through ident_mask).

    python tests/test_cycle_seq.py
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
import gamma, ledger, panel, tether, world

env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="cseq"), tether.Config(), ledger.Ledger())
for _ in range(15):
    ag.step()
st = {n: sorted(map(repr, getattr(ag, n).items())) for n in ("_kdk_last", "_kind_last")}
print(json.dumps({"cycle_seq": tether._CYCLE_SEQ, "stores": st, "rows": ag.led.rows()},
                 default=str))
'''


def _run(cseq: str, hseed: str) -> dict:
    here = _repo.ROOT
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED=hseed, TETHER_AGENT_SEED="0",
               TETHER_CYCLE_SEQ=cseq)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here], env=env,
                         capture_output=True, text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def planted() -> None:
    here = _repo.ROOT
    sys.path[:0] = [here, os.path.join(here, "conform")]
    import panel

    import gamma
    import ledger
    import tether
    import world
    env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="cseq"), tether.Config(), ledger.Ledger())
    assert tether._CONSOLIDATE, "the seq is written under CONSOLIDATE only"
    ko = ("COLOUR",)
    seqs = {}
    was = tether._CYCLE_SEQ
    try:
        for on in (True, False):
            tether._CYCLE_SEQ = on
            ag.cycle += 1
            ag._dk_this = set()
            e1, e2 = ("planted_a", "STATE", ko, ko), ("planted_b", "STATE", ko, ko)
            ag._land_kind(e1, slot="s")
            ag._land_kind(e2, slot="s")
            seqs[on] = (ag._kind_last[e1][3], ag._kind_last[e2][3])
    finally:
        tether._CYCLE_SEQ = was
    assert seqs[True][0] == seqs[True][1], seqs
    assert seqs[False][1] == seqs[False][0] + 1, seqs
    print(f"(3) a planted two-landing cycle: ON seqs {seqs[True]}, OFF {seqs[False]}")


def main() -> None:
    here = _repo.ROOT
    sys.path.insert(0, os.path.join(here, "conform"))
    from identity_mod_rows import compare
    a, b = _run("1", "1"), _run("1", "2")
    c, d = _run("0", "1"), _run("0", "2")
    assert a["cycle_seq"] is True and c["cycle_seq"] is False
    assert c["stores"] != d["stores"], "CONTROL: OFF under two hash seeds did not differ"
    assert a["stores"] == b["stores"], [n for n in a["stores"] if a["stores"][n] != b["stores"][n]]
    for rs in (a["rows"], b["rows"]):
        for r in rs:
            if r["event"] == "arms" and r["slot"] == "@run":
                r["detail"].pop("pythonhashseed", None)
    bad = compare(a["rows"], b["rows"], set())
    assert not bad, bad[:3]
    print(f"(1) ON under hash seeds 1 and 2: _kdk_last ({len(a['stores']['_kdk_last'])}) and "
          f"_kind_last ({len(a['stores']['_kind_last'])}) identical, {len(a['rows'])} rows "
          f"identical; CONTROL OFF under the same seeds differs")
    planted()
    print("test_cycle_seq: pass")


if __name__ == "__main__":
    main()
