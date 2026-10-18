"""C-7i-1, 7i THE SETTLED CORE (Isaiah 2026-10-14 07:08, 07:14; the reviewer 2026-10-15 19:04).

  I1  an INNATE term (the library's one-atom description) is settled with admitted INHERITED; a
      refute leaves it settled and writes a contradiction row; a PRIOR atom likewise
  MF  the same refutes on a term that earned its standing in play demote it
  I3  a mint not from the library stays a candidate until it earns
  I4  inheritance settles no slot (innate is umwelt, never a slot preference)
  Q1  a per-slot refute on an innate term clears that slot; the global standing stays
  I5  a LEARNED library recipe starts settled with admitted LEARNED; an ordinary refute demotes it
  I2  after a real lineage write and load, a term that earned its standing is settled again (the
      evidence replayed); control: with the arm OFF it arrives a candidate
  I6  after the reload an innate name stays innate and a learned name stays learned
  I2b / I6b  (R7i, the reviewer 2026-10-17 19:50) the same for BOUND terms, which reload under
      another name: an earned bound term arrives settled with its paid; a learned bound recipe
      that was demoted arrives learned, not innate, and demoted. MF-R: with TETHER_REPLAY_UNIT=0
      (by name, as before) the earned bound term arrives a candidate
  I7  after the reload no term is settled on any slot (A1: the replay is global)
  A2  the hook's predicate (_core_kind): one atom inherit, multi-atom learn, an extension and
      another operand candidate
  N   the fake game's described mints, one-atom vs multi-atom (a count, not a target)

    python test_settled_core.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

CHILD = r"""
import json, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode = True
import gamma, gridworld, ledger, lineage, tether, world
from gamma import Term, MINTED

def agent(d, seed):
    env = world.bind(gridworld.family("default", seed))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(),
                      ledger.Ledger())
    return ag, lineage.load(d, ag)

d = Path(tempfile.mkdtemp(prefix="core_")) / "g"
ag, _ = agent(d, 0)
g = ag.gamma
a0, a1 = g.atoms[0], g.atoms[1]
T = {"inn": Term((a0,), origin=MINTED, operand="o0.row"),
     "lrn": Term((a0, a1), origin=MINTED), "lrn2": Term((a1, a0, a1), origin=MINTED),
     "new": Term((a1, a0), origin=MINTED), "cand": Term((a1,), origin=MINTED, operand="o0.col"),
     "bnd": Term((a1, a0, a0), origin=MINTED, operand="o0.row"),
     "bdm": Term((a0, a0, a1), origin=MINTED, operand="o0.col")}
for t in T.values():
    g.accept(t, seq=0, residual="fixture")
n = {k: t.name for k, t in T.items()}
if gamma._SETTLED_CORE:
    g.inherit(n["inn"]); g.learn(n["lrn"]); g.learn(n["lrn2"]); g.learn(n["bdm"])
out = {"born": {k: g.is_settled(v) for k, v in n.items()},
       "admitted": {k: g.stamps[v].get("admitted") for k, v in n.items()},
       "innate_slot": g.is_settled(n["inn"], "o0.row")}
g.settle(n["new"]); g.settle(n["cand"]); g.settle(n["bnd"], "default:L0")
g.settle(n["new"], slot="s2")
out["slot_pre"] = g.is_settled(n["new"], "s2")
for _ in range(2):
    g.refute(n["inn"]); g.refute(n["cand"]); g.refute(n["lrn"]); g.refute(a0.name)
    g.refute(n["bdm"])
g.settle(n["inn"], slot="s1")
out["slot_before"] = g.is_settled(n["inn"], "s1")
for _ in range(2):
    g.refute(n["inn"], slot="s1")
out.update(after={k: g.is_settled(v) for k, v in n.items()},
           slot_after=g.is_settled(n["inn"], "s1"),
           prior_innate=a0.name in g.innate,
           contradictions=g.book.get("contradictions", 0),
           rows=sorted({r[0] for r in g.evidence}))
ag.end_run("cap")
lineage.write(d, ag, "default")
ag2, rep = agent(d, 1)
g2 = ag2.gamma
out.update(reload={k: g2.is_settled(v) for k, v in n.items()},
           reload_admitted={k: (g2.stamps.get(v) or {}).get("admitted") for k, v in n.items()},
           reload_innate={k: v in g2.innate for k, v in n.items()},
           replayed=rep.get("replayed"),
           reload_bound={k: [g2.renamed.get(n[k]),
                             g2.is_settled(g2.renamed.get(n[k], n[k])),
                             (g2.stamps.get(g2.renamed.get(n[k], n[k])) or {}).get("admitted"),
                             g2.renamed.get(n[k], n[k]) in g2.innate,
                             dict((g2.standing.get(g2.renamed.get(n[k], n[k])) or
                                   gamma.Standing()).paid)]
                         for k in ("bnd", "bdm")},
           reload_slots=sorted(nm for nm, st in g2.standing.items() if st.settled_on),
           # a one-atom term's operand binding does not cross, so it reloads under its unbound
           # form (gamma load_blob); found by its INHERITED stamp, not by its old name
           reload_inherited=[[nm, nm in g2.innate, g2.is_settled(nm)]
                             for nm, st in g2.stamps.items()
                             if st.get("admitted") == "inherited"])
print("OUT " + json.dumps(out, default=repr))
"""

COUNT = r"""
import json, sys
sys.dont_write_bytecode = True
import arc_holdout
from test_entry import FakeWrapper
def count(led):
    c = {}
    for r in led.rows():
        if r["event"] == "accept":
            s = r["detail"].get("status")
            c[s] = c.get(s, 0) + 1
    return c
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), 'fake')
[ag.step() for _ in range(8)]
print("OUT " + json.dumps({"fake_8": count(led)}))
"""


def _run(code: str, arms: dict) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(arms)
    r = subprocess.run([sys.executable, "-B", "-c", code], env=env, capture_output=True,
                       text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads([ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")][-1][4:])


def main() -> None:
    on, off = _run(CHILD, {}), _run(CHILD, {"TETHER_SETTLED_CORE": "0"})
    by_name = _run(CHILD, {"TETHER_REPLAY_UNIT": "0"})
    assert on["born"]["inn"] and on["admitted"]["inn"] == "inherited", ("I1", on["born"])
    assert on["after"]["inn"] and on["contradictions"] >= 4 and "contradiction" in on["rows"], (
        "I1: an innate term was demoted, or its contradiction not recorded", on)
    assert on["prior_innate"], "I1: a PRIOR atom is not innate"
    print(f"  I1 innate settled at birth (inherited); 2 refutes leave it settled;"
          f" {on['contradictions']} contradictions recorded (a PRIOR atom's included)")
    assert on["born"]["cand"] is False and on["after"]["cand"] is False, ("MF", on)
    print("  MF a term that earned its standing in play, refuted twice, is demoted")
    assert on["born"]["new"] is False, "I3: a mint not from the library was born settled"
    print("  I3 a mint not from the library is born a candidate")
    assert on["innate_slot"] is False, "I4: inheritance settled a slot"
    print("  I4 inheritance settles no slot")
    assert on["slot_before"] and not on["slot_after"] and on["after"]["inn"], ("Q1", on)
    print("  Q1 a per-slot refute clears that slot; the global standing stays")
    assert on["born"]["lrn"] and on["admitted"]["lrn"] == "learned" and not on["after"]["lrn"], (
        "I5", on)
    print("  I5 a learned recipe is born settled (learned); an ordinary refute demotes it")
    assert on["reload"]["new"] and not off["reload"]["new"], ("I2", on["reload"], off["reload"])
    print(f"  I2 the earned standing survives the reload (replayed {on['replayed']});"
          " OFF it arrives a candidate")
    inh = on["reload_inherited"]
    assert inh and all(i and s for _nm, i, s in inh), ("I6 innate", inh)
    assert (on["reload"]["lrn2"] and on["reload_admitted"]["lrn2"] == "learned"
            and not on["reload_innate"]["lrn2"]), ("I6 learned", on)
    assert not on["reload"]["lrn"], "I6: a demoted learned recipe came back settled"
    print("  I6 innate stays innate, learned stays learned (a demoted one stays demoted)")
    bnd, bdm = on["reload_bound"]["bnd"], on["reload_bound"]["bdm"]
    assert bnd[0] and bnd[1] and bnd[4] == {"default:L0": 1} and not bnd[3], ("I2b", bnd)
    print(f"  I2b a bound earned term reloads as {bnd[0]!r}, settled, paid {bnd[4]}")
    assert bdm[0] and bdm[2] == "learned" and not bdm[3] and not bdm[1], ("I6b", bdm)
    print(f"  I6b a demoted learned bound recipe reloads as {bdm[0]!r}: learned, not innate, "
          "demoted")
    nb = by_name["reload_bound"]["bnd"]
    assert not nb[1] and not nb[4], ("MF-R: by name the bound term still arrived settled", nb)
    print(f"  MF-R by name only (TETHER_REPLAY_UNIT=0): the bound term arrives a candidate, paid "
          f"{nb[4]} (replayed {by_name['replayed']})")
    assert on["slot_pre"] and not on["reload_slots"], ("I7", on["slot_pre"], on["reload_slots"])
    print("  I7 a term settled on a slot before the boundary is settled on no slot after it")
    from types import SimpleNamespace as NS

    from tether import _core_kind

    def t(names, operand=None):
        return NS(atoms=tuple(NS(name=x) for x in names), operand=operand)

    offers = [{"operand": "o1", "term": t("a")}, {"operand": None, "term": t("ab")}]
    cases = {"one atom": (t("a", "o1"), "inherit"), "multi": (t("ab"), "learn"),
             "extension": (t("abc"), None), "other operand": (t("a", "o2"), None)}
    for k, (term, want) in cases.items():
        assert _core_kind(offers, term) == want, ("A2", k, _core_kind(offers, term), want)
    print("  A2 the hook's predicate: one atom inherit, multi learn, extension and another"
          " operand candidate")
    n = _run(COUNT, {})
    print(f"  N fake game, 8 steps, accepts by status: {n}")
    print("settled core: OK")


if __name__ == "__main__":
    main()
