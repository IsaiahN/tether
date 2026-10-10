"""7a(5b), the contact instrument (Isaiah 2026-10-10 06:46 CDT; the reviewer 11:46Z, 12:27Z). With
TETHER_CONTACT on, `gamma_read["fed"]` on each REPEAT row names, by seq, the library terms read by
the exit whose action was RETURNED, each with a role (goal / route / body). Record only.

On a panel member (default gridworld s0), 20 cycles, ON (with TETHER_MC_SIGNAL, for MC2's pointer):
  must-pass: every discriminate:goal step's fed names the term the split read (role goal, with its
     stamp seq or the reason it has none); every routine step's fed has its body (the plan, with
     its mint row's seq or why not) and the objective its guards read;
  1. probe, system0, distinguish and draw steps: fed [] and entered False;
  2. a step whose routine mint formed an intent and whose exit was NOT the goal split: fed does
     not name that split's term (counted on the member's own run, where it can be vacuous, and
     on a forced run where the bored probe takes such steps: 2b);
  3. OFF, the per-step reset: no routine or probe step carries a gamma_read value, while the
     committed panel (before the reset) shows such steps carrying the previous cycle's;
  4. MC2: every resolution row's fed is a list (REPEAT seqs after the bet), never None, ON.

    python test_contact.py [panel member, default gridworld_s0]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import gamma
import gate
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True

CYCLES = 20     # anchor: a declared convention, not measured; long enough on gridworld s0 for the
                #   mint to fire (counted, asserted >= 1); movable


MEMBER = sys.argv[1] if len(sys.argv) > 1 else "gridworld_s0"   # a panel member's name


def _world():
    """The panel member's board, built as conform/panel.py builds it."""
    g = gridworld.family("default", int(MEMBER.rsplit("s", 1)[1]), CYCLES)
    if "_arc_" in MEMBER:
        import arc_atoms
        import arc_predict
        g.atom_set = arc_atoms.three_spaces(arc_predict.predict())
        g.attribute_types = dict(arc_atoms.ATTRIBUTE_TYPE)
    return g


def _run(on: bool) -> tuple[list[dict], list]:
    was = (tether._FED, tether._MC_SIGNAL)
    tether._FED = tether._MC_SIGNAL = on
    env = world.bind(_world())
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="contact_fixture"), tether.Config(),
                      ledger.Ledger())
    inner, formed = ag._goal_split, []

    def split(before, commit=True):
        act = inner(before, commit=commit)
        if not commit and act is not None:
            formed.append((ag.cycle, ag._term_of(ag._goal_want.subject)))
        return act
    ag._goal_split = split
    for _ in range(CYCLES):
        ag.step()
    ag.end_run("cap")
    tether._FED, tether._MC_SIGNAL = was
    return ag.led.rows(), formed


def _steps(rows: list[dict]) -> list[dict]:
    return [r["detail"] for r in rows if r["event"] == "repeat" and r["detail"].get("by")
            and r["detail"]["by"] != "given"]


if __name__ == "__main__":
    rows, formed = _run(True)
    steps = _steps(rows)
    out = gate.check(rows)
    assert out["verdict"] == gate.PASS, out
    by = {}
    for d in steps:
        by.setdefault(d["by"], []).append(d)
    goal, rout = by.get("discriminate:goal", []), by.get("routine", [])
    assert goal or rout, f"precondition: no goal or routine exit in {CYCLES} cycles: {list(by)}"
    for d in goal:
        fed = d["gamma_read"]["fed"]
        assert fed and all(e["role"] == "goal" for e in fed), d["gamma_read"]
        assert all(e["seq"] is not None or e.get("why") for e in fed), fed
    for d in rout:
        fed = d["gamma_read"]["fed"]
        assert fed and fed[0]["role"] == "body" and fed[0]["kind"] == "routine", fed
        assert fed[0]["seq"] is not None or fed[0].get("why"), fed
    print(f"  {MEMBER}: must-pass: {len(goal)} goal steps and {len(rout)} routine steps, each "
          f"fed naming its term(s) with seq or the reason; full gate passes ({len(rows)} rows)")
    others = [d for d in steps if d["by"] not in ("discriminate:goal", "routine")]
    assert others and all(d["gamma_read"].get("fed") == [] and not d["gamma_read"]["entered"]
                          for d in others), [d["gamma_read"] for d in others][:3]
    print(f"  1: {len(others)} probe/system0/distinguish/draw steps: fed [] and entered False")
    cyc = {r["cycle"]: r["detail"] for r in rows if r["event"] == "repeat"}
    hits = 0
    for c, term in formed:
        d = cyc.get(c)
        if d and d["by"] != "discriminate:goal" and term is not None:
            hits += 1
            names = [e["name"] for e in d["gamma_read"]["fed"] if e["role"] != "body"]
            assert d["by"] == "routine" or term["name"] not in names, (c, d)
    print(f"  2: {len(formed)} mints formed an intent; on the {hits} whose exit was not the goal "
          f"split, fed does not name the split's term outside a taken routine")
    # 2b, FORCED: on the panel the goal exit takes nearly every step a mint forms on, so the case
    # can be vacuous. The bored probe is forced on odd cycles from 12 (gridworld s0, 30 cycles),
    # so a step whose mint formed an intent is taken by ANOTHER exit; fed must not name its term.
    tether._FED = tether._MC_SIGNAL = True
    env2 = world.bind(gridworld.family("default", 0, 30))
    ag2 = tether.Agent(env2, gamma.Gamma(env2.atoms(), game="contact_mf2"), tether.Config(),
                       ledger.Ledger())
    _bored = ag2.drive.bored
    ag2.drive.bored = lambda: (ag2.cycle >= 12 and ag2.cycle % 2 == 1) or _bored()
    _inner, formed2 = ag2._goal_split, []

    def _split2(before, commit=True):
        act = _inner(before, commit=commit)
        if not commit and act is not None:
            formed2.append((ag2.cycle, ag2._term_of(ag2._goal_want.subject)))
        return act
    ag2._goal_split = _split2
    for _ in range(30):
        ag2.step()
    tether._FED = tether._MC_SIGNAL = False
    cyc2 = {r["cycle"]: r["detail"] for r in ag2.led.rows() if r["event"] == "repeat"}
    q = [(c, t, cyc2[c]) for c, t in formed2 if c in cyc2 and t is not None
         and cyc2[c]["by"] not in ("discriminate:goal", "routine")]
    assert q, "2b: the forced run produced no qualifying step"
    assert all(t["name"] not in [e["name"] for e in d["gamma_read"]["fed"]] for _c, t, d in q), q
    exits = sorted({d["by"] for _c, _t, d in q})
    print(f"  2b (forced bored probe): {len(formed2)} mints formed an intent; on the {len(q)} "
          f"taken by another exit ({exits}), fed never names the split's term")
    off, _f = _run(False)
    stale = [d for d in _steps(off) if d["by"] in ("routine", "probe") and d["gamma_read"]]
    assert not stale, stale[:2]
    panel = Path(f"runs/panel/{MEMBER}.jsonl")
    before = [json.loads(x)["detail"] for x in panel.read_text(encoding="utf-8").splitlines()
              if '"repeat"' in x] if panel.exists() else []
    carried = [d for d in before if d.get("by") in ("routine", "probe") and d.get("gamma_read")]
    print(f"  3: OFF, 0 routine/probe steps carry a gamma_read value; the committed panel's "
          f"{MEMBER} (before the reset) has {len(carried)} that did")
    res = [r["detail"] for r in rows if r["event"] == "resolution"]
    assert res and all(isinstance(d["fed"], list) for d in res), res[:2]
    n_fed = sum(bool(d["fed"]) for d in res)
    roles = sorted({r for d in res for _s, r in d["fed"]})
    assert all(len(x) == 2 for d in res for x in d["fed"]), "fed entries are [seq, role]"
    print(f"  4: {len(res)} MC2 resolution rows, fed a list of [seq, role] on every one "
          f"({n_fed} non-empty; roles {roles})")
    print("ok")
