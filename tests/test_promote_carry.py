"""ROW 13, A PROMOTION ACROSS A GAME SERIES -- the record of the ruling (the reviewer 2026-11-01
r704 (b)). 
Two game series on the carry fixture's gridworld, through lineage.write / lineage.load. Game series
1 steps, plants one accepted 2-atom chain and promotes it (the feed rarely fires on a short fixture,
so the promotion is seeded; the natural count is printed), then writes. Game series 2 loads.

  MUST-HOLD (by design, ruled (b)): the store keeps the promotion -- the row is written and
  reaches game series 2's load_blob as admitted=promoted -- and load_blob enters it as IMPORTED
  (gamma: "A TERM FROM ANOTHER GAME ENTERS AS IMPORTED, NEVER AS promoted"; Sec 11 clause two,
  "across games there is no first"). So in game series 2 the stamp and is_primitive agree: neither
  says promoted. r702's "storage break" was refuted by this check and withdrawn. Occasions: the
  planted term crossed (asserted > 0).

    python tests/test_promote_carry.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def _life(d, seed):
    import gamma
    import gridworld
    import ledger
    import lineage
    import tether
    import world
    env = world.bind(gridworld.family("default", seed))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(),
                      ledger.Ledger())
    return ag, lineage.load(d, ag)


def _key(t):
    return json.dumps([[a.name for a in t.atoms], t.guard])


def child(d):
    import gamma
    import lineage
    d = Path(d)
    ag1, _ = _life(d, 0)
    for _ in range(20):
        ag1.step()
    natural = len(ag1.gamma.primitives)
    plant = next((t for t in ag1.gamma.enumerate_closure("val", "val", 2, 4000, {})
                  if len(t.atoms) == 2 and t.name not in ag1.gamma.library), None)
    assert plant is not None, "fixture: no new 2-atom chain to plant"
    ag1.gamma.accept(plant, seq=len(ag1.led), residual=f"o1.x@{ag1.cycle}")
    ag1.gamma.promote(plant.name, {"seeded": True}, {"slot": "o1.x", "closed": True})
    assert ag1.gamma.is_primitive(plant.name)
    assert ag1.gamma.stamps[plant.name]["admitted"] == gamma.PROMOTED
    ag1.end_run("cap")
    atoms = [a.name for a in plant.atoms]
    written = [r.get("admitted") for r in ag1.gamma.blob()["terms"] if r.get("atoms") == atoms]
    lineage.write(d, ag1, "default")
    loaded = []
    real = gamma.Gamma.load_blob

    def spy(self, blob, parent=None, hold_unbound=False):
        loaded.extend(r.get("admitted") for r in blob.get("terms", ()) if r.get("atoms") == atoms)
        return real(self, blob, parent=parent, hold_unbound=hold_unbound)
    gamma.Gamma.load_blob = spy
    try:
        ag2, _ = _life(d, 1)
    finally:
        gamma.Gamma.load_blob = real
    got = [n for n, t in ag2.gamma.library.items() if _key(t) == _key(plant)]
    print(json.dumps({"natural_life1": natural, "written": written, "loaded": loaded,
                      "crossed": len(got),
                      "primitive": [ag2.gamma.is_primitive(n) for n in got],
                      "admitted": [ag2.gamma.stamps.get(n, {}).get("admitted") for n in got]}))


def main():
    d = tempfile.mkdtemp(prefix="promote_carry_")
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONDONTWRITEBYTECODE": "1"}
    p = subprocess.run([sys.executable, "-B", __file__, "child", d], env=env,
                       capture_output=True, text=True, timeout=540)
    assert p.returncode == 0, p.stderr[-2000:]
    out = json.loads(p.stdout.strip().splitlines()[-1])
    print(out)
    assert out["crossed"] > 0, ("occasions: the plant did not cross", out)
    assert out["written"] == ["promoted"] and set(out["loaded"]) == {"promoted"}, out
    assert set(out["admitted"]) == {"imported"}, ("load enters it as IMPORTED (Sec 11)", out)
    assert not any(out["primitive"]), ("the stamp and is_primitive agree", out)
    print("test_promote_carry: the store keeps the promotion; load enters it IMPORTED; the stamp "
          "and is_primitive agree (r704 (b), by design)")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "child":
        child(sys.argv[2])
    else:
        main()
