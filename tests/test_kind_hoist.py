"""(D), THE KIND HOIST (TETHER_KIND_HOIST; the S2E box, 2026-10-20 23:08).
gridworld_arc_s1, 15 steps, the agent and hash seeds pinned, three processes: ON, OFF, and PLANT (ON
with every owner's _kind perturbed).

  PRECONDITION: the walk lands kinds (the ON run's _kind_landed is not empty), or the rest is
      vacuous.
  (1) ON and OFF: every row identical (the arms row's on/off lists masked) and the kind stores the
      landings write -- _kind_landed, _kind_pairs, _kind_landed_dk, _kdk_last, _kind_last -- equal.
  (2) the hoist ran: ON calls _kind fewer times than OFF.
  MF: PLANT's kind stores differ from OFF's, so (1)'s comparison sees a changed kind.

    python tests/test_kind_hoist.py
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

calls = [0]
real = tether.Agent._kind


def _kind(self, owner):
    calls[0] += 1
    k = real(self, owner)
    return (*k, "planted") if plant else k


tether.Agent._kind = _kind
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="hoist"), tether.Config(), ledger.Ledger())
for _ in range(15):
    ag.step()
st = {n: sorted(map(repr, getattr(ag, n).items() if hasattr(getattr(ag, n), "items")
                    else getattr(ag, n)))
      for n in ("_kind_landed", "_kind_pairs", "_kind_landed_dk", "_kdk_last", "_kind_last")}
print(json.dumps({"hoist": tether._KIND_HOIST, "calls": calls[0], "stores": st,
                  "rows": ag.led.rows()}, default=str))
'''


def _run(hoist: str, plant: str = "0") -> dict:
    here = _repo.ROOT
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    # the hash seed too: _kind_seq orders landings within a cycle by set iteration, so two ON
    # runs differ in _kdk_last / _kind_last without it
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_KIND_HOIST=hoist)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here, plant], env=env,
                         capture_output=True, text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    here = _repo.ROOT
    sys.path.insert(0, os.path.join(here, "conform"))
    from identity_mod_rows import compare
    on, off, pl = _run("1"), _run("0"), _run("1", "1")
    assert on["hoist"] is True and off["hoist"] is False
    assert on["stores"]["_kind_landed"], "PRECONDITION: the walk landed no kind"
    for rs in (on["rows"], off["rows"]):
        for r in rs:
            if r["event"] == "arms" and r["slot"] == "@run":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
    bad = compare(off["rows"], on["rows"], set())
    assert not bad, bad[:3]
    assert on["stores"] == off["stores"], [n for n in on["stores"]
                                           if on["stores"][n] != off["stores"][n]]
    assert on["calls"] < off["calls"], (on["calls"], off["calls"])
    moved = [n for n in off["stores"] if pl["stores"][n] != off["stores"][n]]
    assert moved, "MF: a planted kind left every kind store unchanged"
    print(f"test_kind_hoist: pass ((1) ON's {len(on['rows'])} rows are OFF's and the five kind "
          f"stores equal ({len(on['stores']['_kind_landed'])} landed kinds); (2) _kind calls "
          f"{on['calls']} ON vs {off['calls']} OFF; MF a planted kind moves {moved})")


if __name__ == "__main__":
    main()
