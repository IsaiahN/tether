"""RDL PIECE 3, THE AGENT'S WIRING (TETHER_RDL, default ON; docs/03-DESIGN/
RDL_BUILD_SPEC_2026-11-16.md "Piece 3"). Released preloads set SEARCH PRIORITY ONLY: an entry
attached to one sorts ahead of an otherwise-equal entry in the described lookup's rank
(Agent._topk); nothing added, removed, made reachable or given standing. Feedback rows
rdl_offer / rdl_settle / rdl_refuse carry the C6 stamp; their counts ride the lineage as rdl_n
(the obg_n pattern).

  A1  a fixture preload file (tether.RDL_PRELOAD pointed at a temp file): an attached entry is
      ranked ahead of an equal unattached one, and an rdl_offer row is written once
  A2  the same candidate set ON and OFF, a different order
  A3  an attached entry's term settles -> rdl_settle with the stamp; refused -> rdl_refuse
  A4  rdl_n round-trips through lineage save / load (the store and the archive chain): loaded
      equal, a save with nothing new adds nothing, one more settle grows it by one
  MF-A1 TETHER_RDL off -> order unchanged, no rdl rows -> RED as required
  A5  gridworld 12 steps ON (the real library/rdl_preload.json when present, else the fixture)
      and OFF: both pass gate.check
  A6  no preload file -> inert, exactly one rdl_inert row saying why

rdl_store / rdl_release (pieces 1 and 2) are used when importable; where they are absent the
test stands in for them with a minimal module implementing the spec's interface (the fixture is the
spec's names, not their behaviour). Seconds.

    python tests/test_rdl_agent.py
"""
from __future__ import annotations

import dataclasses
import json
import os
import sys
import tempfile
import types
from pathlib import Path

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

SLOT = "o1.col"
PID: dict = {}      # fixture name -> the pid rdl_store.make computed


def _stand_ins() -> str:
    """The real pieces when present; else a minimal module per piece, to the spec's names."""
    try:
        import rdl_release  # noqa: F401
        import rdl_store  # noqa: F401
        return "real rdl_store / rdl_release"
    except ImportError:
        pass

    @dataclasses.dataclass(frozen=True)
    class Preload:
        pid: str
        tier: int
        stage: str
        source: dict
        kind: str
        text: str
        bonds: tuple
        refusal: tuple
        attaches: tuple
        parents: tuple

    def load(path):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        return [Preload(**{**p, "bonds": tuple(tuple(b) for b in p["bonds"]),
                           "refusal": tuple(p["refusal"]), "attaches": tuple(p["attaches"]),
                           "parents": tuple(p["parents"])}) for p in d["preloads"]]

    def dump(preloads, path, header):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"header": header, "preloads": [dataclasses.asdict(p) for p in preloads]},
                      fh, sort_keys=True)

    def usable(p):
        return bool(p.bonds) and bool(p.attaches)

    st = types.ModuleType("rdl_store")
    st.STAGES = ("instance", "regularity", "abstraction", "core_rule")
    st.Preload, st.load, st.dump, st.usable = Preload, load, dump, usable

    def make(tier, source, kind, text, bonds=(), refusal=(), attaches=(), parents=()):
        return Preload(pid=f"pid-{tier}-{kind}", tier=tier, stage=st.STAGES[tier - 1],
                       source=dict(source), kind=kind, text=text,
                       bonds=tuple(tuple(b) for b in bonds), refusal=tuple(refusal),
                       attaches=tuple(attaches), parents=tuple(parents))
    st.make = make

    def stats_from_rows(rows):
        out: dict = {}
        f = {"rdl_offer": "offered", "rdl_settle": "settled", "rdl_refuse": "refused"}
        for r in rows:
            if r.get("event") in f:
                d = r["detail"]
                c = out.setdefault((d["corpus"], d["tier"]), {})
                c[f[r["event"]]] = c.get(f[r["event"]], 0) + 1
        return out

    def merge_stats(a, b):
        out = {k: dict(v) for k, v in a.items()}
        for k, v in b.items():
            into = out.setdefault(k, {})
            for e, n in v.items():
                into[e] = into.get(e, 0) + n
        return out

    def released(preloads, stats, inherited_settled=True, usable=None):
        ok = usable or st.usable
        settled: dict = {}
        for (_c, t), v in stats.items():
            settled[t] = settled.get(t, 0) + v.get("settled", 0)
        return {p.pid for p in preloads if ok(p)
                and (p.tier == 1 and inherited_settled or settled.get(p.tier - 1, 0) >= 2)}

    rl = types.ModuleType("rdl_release")
    rl.MIN_SETTLED = 2
    rl.stats_from_rows, rl.merge_stats, rl.released = stats_from_rows, merge_stats, released
    rl.reach_policy = lambda _rows: []
    rl.priority = lambda p, _policy, age: (0, p.tier, -age, p.pid)
    sys.modules["rdl_store"], sys.modules["rdl_release"] = st, rl
    return "stand-in modules (pieces 1/2 not on this branch)"


def fixture(td: str, attach: tuple) -> str:
    """One usable tier-1 preload attached to `attach`, one tier-2 (not released at start), one
    unusable (no bonds): written with rdl_store.dump."""
    import rdl_store
    src = {"corpus": "fixture", "corpus_sha": "0" * 8, "parser": "test", "parser_version": "0"}
    p1 = rdl_store.make(1, src, "wn:n0", "a thing that moves", bonds=(("+", "a", "b"),),
                        attaches=attach)
    p2 = rdl_store.make(2, src, "wn-group:g", "things", bonds=(("+", "a", "b"),),
                        attaches=attach, parents=(p1.pid,))
    p3 = rdl_store.make(1, src, "wn:n1", "no bond", attaches=attach)
    ps = [p1, p2, p3]
    PID.update({"p1": p1.pid, "p2": p2.pid, "p3": p3.pid})
    path = os.path.join(td, "rdl_preload.json")
    rdl_store.dump(ps, path, {"standing": "none (C3)"})
    return path


def agent(led=None):
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        led if led is not None else ledger.Ledger())


def rdl_rows(led, n0=0):
    return [r for r in led.rows()[n0:] if str(r.get("event", "")).startswith("rdl_")]


def rank(ag):
    """The described lookup's rank over two entries every other field leaves equal."""
    lit = [("eA", 1.0), ("eB", 1.0)]
    win, _nxt = ag._topk(lit, lit, {"T1a": 2}, {}, (SLOT,), (SLOT, None, (), (), (SLOT,)))
    ag._tk_off.clear()
    return [k for k, _w in win]


def main() -> int:
    assert tether._RDL is True, "the arm defaults ON"
    print("pieces:", _stand_ins())
    td = tempfile.mkdtemp(prefix="rdl3_")
    keep = tether.RDL_PRELOAD
    tether.RDL_PRELOAD = fixture(td, ("eB",))

    led = ledger.Ledger()
    ag = agent(led)
    assert ag._rdl is not None and ag._rdl["released"] == {PID["p1"]}, \
        ag._rdl and ag._rdl["released"]
    assert ag._rdl["by_entry"] == {"eB": [PID["p1"], PID["p2"]]}, ag._rdl["by_entry"]
    on = rank(ag)
    offers = [r for r in rdl_rows(led) if r["event"] == "rdl_offer"]
    again = rank(ag)
    offers2 = [r for r in rdl_rows(led) if r["event"] == "rdl_offer"]
    ok1 = on == ["eB", "eA"] and again == on and len(offers) == 1 and len(offers2) == 1 \
        and offers[0]["detail"]["entry"] == "eB"
    print(f"A1 attached eB ranked ahead of equal eA: {on}; rdl_offer rows {len(offers)} then "
          f"{len(offers2)}: {'GREEN' if ok1 else 'RED'}")

    rd = ag._rdl
    ag._rdl = None
    off = rank(ag)
    ag._rdl = rd
    ok2 = set(on) == set(off) and on != off and len(on) == len(off)
    print(f"A2 the same set ON {on} / OFF {off}, a different order: {'GREEN' if ok2 else 'RED'}")

    n0 = len(led.rows())
    name = next(iter(ag.gamma.library))
    rd["term_entry"][name] = ("eB", [PID["p1"]])
    ag._rdl_feedback(name, SLOT, "rdl_settle", "SETTLE")
    ag.refuse_term(name, SLOT)
    got = rdl_rows(led, n0)
    st = [r for r in got if r["event"] == "rdl_settle"]
    rf = [r for r in got if r["event"] == "rdl_refuse"]
    stamp = {"pid", "stage", "tier", "corpus", "parser", "cluster"}
    bc, _why = tether.inherited.by_cluster()
    c0 = min((c for c in (bc or {}) if bc[c]), default=None)   # a filed entry -> its first cluster
    ok3 = (len(st) == 1 and len(rf) == 1
           and all(stamp <= set(r["detail"]) for r in got)
           and all(isinstance(r["detail"]["cluster"], str) for r in got)
           and (c0 is None or rd["cluster_of"][bc[c0][0]] <= c0)
           and st[0]["detail"]["pid"] == PID["p1"] and st[0]["detail"]["corpus"] == "fixture"
           and st[0]["detail"]["tier"] == 1 and st[0]["detail"]["term"] == name)
    print(f"A3 settle -> rdl_settle, refuse_term -> rdl_refuse, stamped {sorted(stamp)}: "
          f"{'GREEN' if ok3 else 'RED'}")
    n_now = {f"{c}|{t}": dict(d) for (c, t), d in rd["stats_n"].items()}
    assert n_now == {"fixture|1": {"offered": 1, "settled": 1, "refused": 1}}, n_now

    oks4 = []
    keep_store = lineage._MEMORY_STORE
    for label, store in (("store", True), ("archive", False)):
        lineage._MEMORY_STORE = store
        d = Path(tempfile.mkdtemp(prefix=f"rdl3_{label}_"))
        a = agent()
        a._rdl["stats_n"] = {("fixture", 1): {"settled": 2, "refused": 1}}
        lineage.write(d, a, "default")
        b = agent()
        lineage.load(d, b)
        first = {f"{c}|{t}": dict(v) for (c, t), v in b._rdl["carried"].items()}
        lineage.write(d, a, "default")           # nothing new since a's last save
        c = agent()
        lineage.load(d, c)
        again = {f"{c_}|{t}": dict(v) for (c_, t), v in c._rdl["carried"].items()}
        c._rdl["stats_n"] = {("fixture", 1): {"settled": 1}}
        lineage.write(d, c, "default")
        e = agent()
        lineage.load(d, e)
        grown = {f"{c_}|{t}": dict(v) for (c_, t), v in e._rdl["carried"].items()}
        want0 = {"fixture|1": {"settled": 2, "refused": 1}}
        want1 = {"fixture|1": {"settled": 3, "refused": 1}}
        ok = first == want0 and again == want0 and grown == want1
        # carried settled 3 at tier 1 >= MIN_SETTLED: the tier-2 preload is now released
        ok = ok and PID["p2"] in e._rdl["released"]
        print(f"  A4 ({label}): loaded {first}; after a save with nothing new {again}; "
              f"after one more settle {grown}; released {sorted(e._rdl['released'])}")
        oks4.append(ok)
    lineage._MEMORY_STORE = keep_store
    ok4 = all(oks4)
    print(f"A4 rdl_n round-trips through lineage save / load: {'GREEN' if ok4 else 'RED'}")

    tether._RDL = False
    led_off = ledger.Ledger()
    ag_off = agent(led_off)
    off2 = rank(ag_off)
    tether._RDL = True
    red = ag_off._rdl is None and off2 == ["eA", "eB"] and not rdl_rows(led_off)
    print(f"MF-A1 TETHER_RDL off: order {off2}, rdl rows {len(rdl_rows(led_off))} -> "
          f"{'RED as required' if red else 'GREEN (the arm did not switch off)'}")

    ok5 = True
    if os.path.exists(keep):
        tether.RDL_PRELOAD = keep               # the real preload file (Pieces 1/2 landed)
    for arm in (True, False):
        tether._RDL = arm
        led5 = ledger.Ledger()
        ag5 = agent(led5)
        for _ in range(12):
            ag5.step()
        ag5.end_run("cap")
        v = gate.check(led5.rows())["verdict"]
        from collections import Counter
        evs = dict(Counter(r["event"] for r in rdl_rows(led5)))
        rel = (f", released {len(ag5._rdl['released'])} of {len(ag5._rdl['preloads'])}"
               if ag5._rdl is not None else "")
        print(f"  A5 gw12 RDL {'ON' if arm else 'OFF'} ({os.path.basename(tether.RDL_PRELOAD)}):"
              f" gate {v}, rdl rows {evs}{rel}")
        ok5 = ok5 and v == "pass"
    tether._RDL = True
    print(f"A5 gridworld 12 steps ON and OFF both pass the gate: {'GREEN' if ok5 else 'RED'}")

    tether.RDL_PRELOAD = os.path.join(td, "absent.json")
    led6 = ledger.Ledger()
    ag6 = agent(led6)
    inert = rdl_rows(led6)
    ok6 = ag6._rdl is None and len(inert) == 1 and inert[0]["event"] == "rdl_inert" \
        and "no preload file" in inert[0]["detail"]["why"]
    print(f"A6 no preload file: inert, {len(inert)} rdl_inert row: {'GREEN' if ok6 else 'RED'}")
    tether.RDL_PRELOAD = keep

    assert ok1 and ok2 and ok3 and ok4 and red and ok5 and ok6
    print("rdl_agent: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
