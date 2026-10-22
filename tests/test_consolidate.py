"""CONSOLIDATION (TETHER_CONSOLIDATE; Isaiah 2026-10-18 04:20, 04:26; the reviewer 04:21, 04:43,
04:55). The fake ARC game, C-seed-X.

  CON-1  after a level end (retarget), the instance-keyed bound stores hold 0 entries; the
         @consolidate row shows them before and after
  CON-2  the fold leaves the asked record (ak_'s source) and the episodes unchanged. MF: a fold
         that does not keep the asked keys drops them; a fold that appends episodes adds them
  CON-3  50 sampled slot answers asked again after the clear equal their values before it; the
         rebuild time reported
  CON-5  the size trigger fires with the ceiling lowered by env (TETHER_CONSOLIDATE_CEILING); a
         second size fold is held back while commit has not grown (counted). MF: the arm OFF,
         no fold
  CON-6  two games in one lineage: a 7l key that landed in both is loaded with n_landed = the
         sum, and every game's episodes are present. MF: an overwrite instead of an add differs

    python tests/test_consolidate.py
"""
from __future__ import annotations

import os
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
sys.path.insert(0, HERE)


def agent(lineage_dir=None):
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=lineage_dir)
    return tether, env, ag


def rows_of(ag) -> list:
    out = []
    real = ag.led.record

    def spy(cycle, step, slot, event, **d):
        out.append((event, slot, d))
        return real(cycle, step, slot, event, **d)
    ag.led.record = spy
    return out


def steps(env, ag, n):
    for _ in range(n):
        env.observe()
        ag.step()


def main() -> int:
    import lineage
    tether, env, ag = agent()
    calls: list = []
    real_c = tether.Agent._compiled

    def spy(self, lib, key, role, o, x, comp, atoms, sig, slot=None, tally=None):
        got = real_c(self, lib, key, role, o, x, comp, atoms, sig, slot=slot, tally=tally)
        got = list(got)
        if slot is not None and got and len(calls) < 50 and self._atoms_token:
            calls.append(((lib, key, role, o, x, comp, atoms, sig), slot, tally is not None,
                          repr(got)))
        return got
    tether.Agent._compiled = spy
    try:
        steps(env, ag, 6)
    finally:
        tether.Agent._compiled = real_c
    rows = rows_of(ag)
    stores = ag._bound_stores()
    before = {n: len(m) for n, m in stores.items()}
    assert sum(before.values()), "precondition: the bound stores are empty after 6 steps"
    ak_before = len(lineage._ak_source(ag))
    ep_before = len(ag._kind_episodes)
    ag.retarget(env, 1, how=tether.ADVANCE)
    after = {n: len(m) for n, m in ag._bound_stores().items()}
    con = [d for e, s, d in rows if e == "consolidate"]
    assert not sum(after.values()) and con and con[-1]["before"] == before, (after, con)  # CON-1
    print(f"CON-1 the level end cleared {sum(before.values())} entries "
          f"({ {k: v for k, v in before.items() if v} }) to 0; the @consolidate row: trigger "
          f"{con[-1]['trigger']}, fold {con[-1]['fold']}, {ag._body_rows[-1]['ms']} ms (@body), "
          f"landed cleared {con[-1]['landed_cleared']}")
    assert not {"commit_before", "commit_after", "ms"} & set(con[-1]), con[-1]   # the row: shared
    assert ag._body_rows[-1]["fold"] == con[-1]["fold"], "@body: not joined by the fold"
    ak_after = len(lineage._ak_source(ag))
    assert ak_after == ak_before and len(ag._kind_episodes) == ep_before, (
        ak_before, ak_after, ep_before, len(ag._kind_episodes))                          # CON-2
    print(f"CON-2 the asked record {ak_before} -> {ak_after} questions, episodes {ep_before} -> "
          f"{len(ag._kind_episodes)}: unchanged by the fold")
    # MF-CON-2: a fold that forgets the kept keys, and one that appends an episode
    kept, ag._ak_kept = ag._ak_kept, set()
    mf_drop = len(lineage._ak_source(ag))
    ag._ak_kept = kept
    assert mf_drop < ak_before, ("MF-CON-2: without the kept keys nothing was dropped", mf_drop)
    ag._kind_episodes.append({"mf": 1})
    assert len(ag._kind_episodes) != ep_before, "MF-CON-2: an appended episode went unseen"
    ag._kind_episodes.pop()
    print(f"MF-CON-2 without the kept keys the record falls to {mf_drop} of {ak_before}; an "
          "appended episode is seen")

    assert len(calls) >= 10, ("precondition: too few slot answers sampled", len(calls))
    t0 = time.perf_counter()
    # the agent passes a tally (SPEED-2: the slot memo then holds landing rows only), so the
    # replay passes one too
    same = sum(repr(list(real_c(ag, *a, slot=s, tally=Counter() if t else None))) == v
               for a, s, t, v in calls)
    ms = 1000 * (time.perf_counter() - t0)
    assert same == len(calls), (same, len(calls))                                       # CON-3
    print(f"CON-3 {same} of {len(calls)} sampled slot answers rebuilt after the clear equal their "
          f"values before it; the rebuild took {ms:.0f} ms")

    os.environ["TETHER_CONSOLIDATE_CEILING"] = "2"
    w_was, tether._W_BUDGET = tether._W_BUDGET, False   # the ceiling path is W-1 OFF (ON: test_w12)
    try:
        rows = rows_of(ag)
        steps(env, ag, 2)
        size = [d for e, s, d in rows if e == "consolidate" and d["trigger"] == "size"]
        assert size, "CON-5: no size fold with the ceiling lowered"                       # CON-5
        print(f"CON-5 the size trigger fired {len(size)} time(s) in 2 steps with the ceiling "
              f"lowered; held back by the hysteresis: {ag._fold_suppressed}")
        was = tether._CONSOLIDATE
        tether._CONSOLIDATE = False
        try:
            rows = rows_of(ag)
            steps(env, ag, 1)
            assert not [1 for e, _s, _d in rows if e == "consolidate"], (
                "MF-CON-5: folded with the arm OFF")
        finally:
            tether._CONSOLIDATE = was
        print("MF-CON-5 the arm OFF: no fold")
    finally:
        del os.environ["TETHER_CONSOLIDATE_CEILING"]
        tether._W_BUDGET = w_was

    d = tempfile.mkdtemp()
    ns, dks, prs, eps = [], [], [], 0
    for _g in range(2):
        tether, env, ag = agent(lineage_dir=d)
        steps(env, ag, 6)
        ag.end_run("cap")
        ns.append(Counter(ag._kind_landed_n))
        dks.append(Counter(ag._kind_landed_dk))
        prs.append(Counter())
        for e, n in ag._kind_landed_n.items():
            prs[-1][(e[2], e[3])] += n
        eps += len(ag._kind_episodes)
        lineage.write(d, ag, "fake")
    tether, env, ag = agent(lineage_dir=d)
    both = [k for k in ns[0] if k in ns[1]]
    bd = [e for e in dks[0] if e in dks[1]]
    assert both and bd, "precondition: no 7l key / dk row landed in both games"
    # the sum WHERE THE RANKING READS IT (the reviewer 2026-10-21 00:27): the dk rows (_tiers'
    # T1a-d) in both loads; under the memory store the 7l trio stays empty by design, so T2's
    # t2 rows and _pair_counts' pairs, else the trio's _kind_known_n
    def known(e):   # the carried count: the in-RAM copy, or under W-4 the load-time snapshot
        return ag._dk_snap.rows(e[0]).get(e, 0) if ag._dk_snap is not None else ag._kind_known_dk[e]
    bad = [e for e in bd if known(e) != dks[0][e] + dks[1][e]]
    if ag._kind_store is not None:
        t2, pr = ag._kind_store["t2"], ag._kind_store["pairs"]
        bad += [k for k in both if k in t2 and t2[k][0] != ns[0][k] + ns[1][k]]
        bad += [p for p in prs[0] if p in prs[1] and pr.get(p, (None,))[0] != prs[0][p] + prs[1][p]]
    else:
        bad += [k for k in both if ag._kind_known_n[k] != ns[0][k] + ns[1][k]]
    chain_eps = sum(len(g.get("episodes", ())) for _h, g in lineage._chain(Path(d))) if hasattr(
        lineage, "_chain") else None
    assert not bad, bad[:3]                                                               # CON-6
    over = [e for e in bd if dks[1][e] != dks[0][e] + dks[1][e]]
    assert over, "MF-CON-6: an overwrite would read the same as the sum"
    print(f"CON-6 {len(bd)} dk rows and {len(both)} 7l keys landed in both games; each dk row "
          f"loads n = the sum (e.g. {dks[0][bd[0]]} + {dks[1][bd[0]]} = "
          f"{known(bd[0])}), "
          f"and {'the store pairs / t2' if ag._kind_store is not None else '_kind_known_n'} too; "
          f"episodes written {eps}, in the chain {chain_eps}; MF an overwrite differs on "
          f"{len(over)}")
    print("consolidate: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
