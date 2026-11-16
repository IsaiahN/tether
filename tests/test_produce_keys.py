"""O1 follow-on, PRODUCTIONS AS ⇒ KEYS (TETHER_PRODUCE_KEYS, default ON). A SETTLED production of
the step-10 ledger (can_ledger.ProductionBook: press A, item kind K; settled = predicted at least
once, hits outnumber misses) is mapped onto two record-backed truth readings -- @press:A (the press
the trace records just before the state) and @kind:K (the can ledger's reading of the state had an
item of kind K on the CAN list) -- and routed through _route_junction as ⇒:@press:A|@kind:K onto the
guard offer of every slot of kind K. MECHANICS ONLY, modelled on test_implies_bond.py: a gridworld
agent whose trace and history are set by hand. Seconds.

  P1  a settled production is routed as an ⇒ key on the consequent's slots, reads (not A) or K on
      record-backed states, and is offered where it separates R (the normal junction offer)
  P2  an unsettled one (predicted and missed; or learned and never predicted) is not routed; one
      that tips back to unsettled is taken off the offer
  P3  keyed by kind: every slot of kind K shares the one key; no object name in it
  MF-P1 tether._PRODUCE_KEYS = False -> no key routed or read -> RED as required
  P5  gridworld 12 steps ON: the live path runs and the gate passes

    python tests/test_produce_keys.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import can_ledger  # noqa: E402
import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

S, S2, V = "o0.col", "o1.col", "o0.colour"


def agent():
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())


def book_for(ag):
    """up => K settled (1 predicted, 1 hit); down => KV unsettled (1 predicted, 0 hit); left => KV
    only learned (never predicted)."""
    k, kv = ag._can_kind_key(S), ag._can_kind_key(V)
    b = can_ledger.ProductionBook()
    b.learn("up", {k})
    b.learn("down", {kv})
    b.learn("left", {kv})
    b.settle("up", b.predict("up"), {k})
    b.settle("down", b.predict("down"), set())
    return b, k, kv


def main() -> int:
    assert tether._PRODUCE_KEYS is True, "the arm defaults ON"
    ag = agent()
    book, k, kv = book_for(ag)
    assert book.settled() == [("up", k)], ("settled", book.settled(), book.score)
    ag._produce_keys(book)
    key = f"⇒:@press:up|@kind:{k!r}"

    # P1: routed as an ⇒ key on the consequent's slot, through the existing route
    assert key in ag._junction_of.get(S, ()), ("P1 routed", sorted(ag._junction_of.get(S, ())))
    assert ag._junction_conds[key] == ("⇒", "@press:up", f"@kind:{k!r}"), ag._junction_conds[key]
    # the readings, record-backed: rows 0..3 pressed down, up, up, down; the ledger read K on the
    # CAN list after row 0 and row 2, not after row 1
    st = [{S: i, V: 0} for i in range(5)]
    ag.trace = [(st[0], "down", st[1], None, None), (st[1], "up", st[2], None, None),
                (st[2], "up", st[3], None, None), (st[3], "down", st[4], None, None)]
    # st[1..3] are row i's before-state AND row i-1's after-state here; the agent's own trace has
    # fresh dicts per observe, and _pk_at reads the before-state by row
    ag._pk_can = (ag.trace, {0: {k}, 1: set(), 2: {k}})
    got = [ag._jc_value(key, s) for s in st]
    # st0: no press before it -> None; st1: after down -> True; st2: after up, K not CAN -> False;
    # st3: after up, K CAN -> True; st4: after down (last row) -> no ledger reading -> None
    assert got == [None, True, False, True, None], ("P1 reads (not A) or K", got)
    hist = [(st[i], ag.trace[i][1], i, None, None) for i in range(4)]
    robs = [hist[1], hist[3]]
    ag.history = lambda slot: hist if slot in (S, S2) else []
    off = ag._guards_once(robs, S, [])
    assert off[6] == [key] and off[1][-1] == gamma.JUNCTION_GUARD, ("P1 offered", off)
    off_r0 = ag._guards_once([hist[1], hist[2]], S, [])     # True and False on R: no separation
    assert key not in off_r0[6], ("P1 not offered where it does not separate R", off_r0)
    print(f"P1 settled up=>K routed to {S} as {key}; reads {got}; offered where it separates R, "
          f"not elsewhere: GREEN")

    # P2: unsettled productions are not routed
    bad = f"⇒:@press:down|@kind:{kv!r}"
    bad2 = f"⇒:@press:left|@kind:{kv!r}"
    assert not any(bad in ks or bad2 in ks for ks in ag._junction_of.values()), \
        ("P2", ag._junction_of.get(V))
    assert bad not in ag._junction_conds and bad2 not in ag._junction_conds
    # ...and a settled one that tips back (two more misses: 1 hit of 3) is taken off the offer
    book.settle("up", book.predict("up"), set())
    book.settle("up", book.predict("up"), set())
    ag._produce_keys(book)
    assert not any(key in ks for ks in ag._junction_of.values()), ("P2 tip back", ag._junction_of)
    print(f"P2 down=>KV (missed) and left=>KV (never predicted) not routed; up=>K at "
          f"{book.score[('up', k)]} [predicted, hit] taken off the offer: GREEN")

    # P3: keyed by kind -- every slot of kind K shares the one key, and no object name is in it
    ag3 = agent()
    b3, k3, _kv3 = book_for(ag3)
    ag3._produce_keys(b3)
    same = sorted(s for s in ag3.slots if "." in s and "~" not in s and "@" not in s
                  and ag3._can_kind_key(s) == k3)
    assert len(same) >= 2 and S in same and S2 in same, ("P3 kind members", same)
    assert all(key in ag3._junction_of.get(s, ()) for s in same), ("P3 shared", same)
    assert sum(1 for c in ag3._junction_conds if c.startswith("⇒:@press:up")) == 1
    owners = {s.split(".")[0] for s in same}
    assert not any(f"{o}." in key for o in owners), ("P3 no object name in the key", key)
    print(f"P3 one key on all {len(same)} slots of kind {k3} ({', '.join(same[:3])}...): GREEN")

    # MF-P1: the arm OFF -> no production key routed, and the operand reads nothing
    tether._PRODUCE_KEYS = False
    try:
        ag4 = agent()
        b4, k4, _ = book_for(ag4)
        ag4._produce_keys(b4)
        none_routed = not any(k.startswith("⇒:@press") for k in ag4._junction_conds)
        ag4._pk_ops["@press:up"] = ("press", "up")
        read_off = ag4._jc_read("@press:up", {S: 1})
    finally:
        tether._PRODUCE_KEYS = True
    assert none_routed and read_off is None, ("MF-P1", none_routed, read_off)
    print("MF-P1 the arm OFF: no production key routed, the operand unread -> RED as required")

    # P5: the live path -- gridworld 12 steps ON, the gate passes
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag5 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    for _ in range(12):
        ag5.step()
    ag5.end_run("cap")
    v = gate.check(led.rows())["verdict"]
    assert v == "pass", ("P5: the gate refused", v)
    n_pk = sum(1 for r in led.rows() if r.get("event") in ("produce_key", "produce_key_off"))
    n_cp = sum(1 for r in led.rows() if r.get("event") == "can_produce")
    held = len(ag5.__dict__.get("_pk_can", (None, {}))[1])
    print(f"P5 gridworld 12 steps ON: gate pass; {held} CAN readings kept, {n_cp} can_produce "
          f"rows, {n_pk} produce_key rows: GREEN")
    print("test_produce_keys OK")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
