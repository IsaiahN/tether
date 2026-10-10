"""7a(5) A + B, the ruin record (ARC_AGENT 19.3-19.4; the reviewer 2026-10-10 10:41Z), on hand
snaps worlds that die (AVOID: s0 must never read 3). Record only; arm TETHER_RUIN_RECORD.

  1. a ladder: death; the deterministic RETRY of the same board dies the same way; a death at a
     DIFFERENT board; a level that survives; end_run("cap"). The FULL gate passes;
  2. A: Termination hears every ending once: death_possible latches (proven); must-fail, a cap
     alone never latches it; must-fail, a WIN retargeted then ended by the loop is ONE ending;
     must-fail, a death then the deadline with no step between is TWO (the reviewer 10:57Z);
  3. B: one veto per death, keyed (fingerprint, action, realised coordinate); the retry re-reads
     the same key (new False); must-fail, a death at another fingerprint is a second entry;
     must-fail, the same action at another coordinate on the same board is another key;
     the fingerprint reads board() where the world gives one -- two boards that observe() alike
     get two fingerprints -- else observe(), and the row says which;
  4. OFF: the same ladder writes the same rows less the termination/veto rows (the run's arms
     row aside, which states the arm), and no vetoes.

    python test_ruin_record.py
"""
from __future__ import annotations

import sys

import gamma
import gate
import ledger
import snaps
import tether
from world import bind

sys.dont_write_bytecode = True


def _spec(s0: int) -> snaps.WorldSpec:
    return snaps.WorldSpec(slots=["s0", "s1"],
                           rules={"s0": snaps.SlotSpec("action", k=1),
                                  "s1": snaps.SlotSpec("identity")},
                           obj="AVOID", tgt=3, who="s0", start={"s0": s0, "s1": 0})


class Boarded(snaps.Snap):
    """A world whose board holds a cell observe() does not publish."""

    def __init__(self, spec: snaps.WorldSpec, hidden: int) -> None:
        super().__init__(spec)
        self.hidden = hidden

    def board(self) -> list:
        return [[self.state["s0"], self.state["s1"], self.hidden]]


class Positioned(snaps.Snap):
    """A world that takes a positioned press (the coordinate does not change what it does)."""

    def step(self, action: str, _x: int | None = None, _y: int | None = None) -> None:
        super().step(action)


def _agent(snap: snaps.Snap) -> tether.Agent:
    return tether.Agent(bind(snap), gamma.Gamma(snaps._atoms(), game="ruin_fixture"),
                        tether.Config(), ledger.Ledger())


def _play(ag: tether.Agent, snap: snaps.Snap, actions: str) -> str | None:
    for a in actions:
        ag.step(a)
        if snap.terminal():
            return snap.terminal()
    return None


def _ladder(on: bool) -> tether.Agent:
    """(start of s0, actions): A from 2 dies; the retry of the same board dies the same way;
    B from 1 dies on another board; B then A from 2 survives (s0 4, 5)."""
    was, tether._RUIN_RECORD = tether._RUIN_RECORD, on
    plan = [(2, "A"), (2, "A"), (1, "B"), (2, "BA")]
    snap = snaps.Snap(_spec(plan[0][0]))
    ag, last = _agent(snap), "run_end"
    for lv, (s0, acts) in enumerate(plan):
        if lv:
            snap = snaps.Snap(_spec(s0))
            ag.retarget(bind(snap), lv, last)
        last = _play(ag, snap, acts) or "run_end"
    ag.end_run("cap")
    tether._RUIN_RECORD = was
    return ag


def _ev(ag: tether.Agent, event: str) -> list[dict]:
    return [r["detail"] for r in ag.led.rows() if r["event"] == event]


def _bare(rows: list[dict]) -> list[tuple]:
    """Every row but the run's `arms` row, which states the arm and so must differ."""
    return [(r["cycle"], r["step"], r["slot"], r["event"], repr(r["detail"])) for r in rows
            if r["event"] != "arms"]


if __name__ == "__main__":
    tether._RUIN_RECORD = True      # the arm ON for every check below but the OFF ladder
    ag = _ladder(True)
    rows = ag.led.rows()
    out = gate.check(rows)
    assert out["verdict"] == gate.PASS, out
    vetoes, terms = _ev(ag, "veto"), _ev(ag, "termination")
    print(f"  ladder: {len(rows)} rows, full gate passes; termination rows "
          f"{[(t['was'], t['class']) for t in terms]}")
    # A
    rep = ag.term.report()
    assert rep["death_possible"] and "death_possible" in rep["proven"], rep
    assert rep["endings"] == 4 and rep["capped_seen"], rep          # 3 deaths + the run's cap
    print(f"  A: {rep['endings']} endings, class {rep['class']}, proven {rep['proven']}")
    cap = _agent(snaps.Snap(_spec(4)))
    _play(cap, cap.env, "AA")
    cap.end_run("cap")
    rc = cap.term.report()
    assert not rc["death_possible"] and rc["capped_seen"] and rc["class"] == "open", rc
    print(f"  must-fail, a cap alone: death_possible {rc['death_possible']}, class {rc['class']}, "
          f"assumed {rc['assumed']}")
    win = _agent(snaps.Snap(_spec(4)))
    _play(win, win.env, "A")
    win.retarget(win.env, 1, "advance")
    win.end_run("advance")
    one = win.term.report()["endings"]
    _play(win, win.env, "A")
    win.end_run("cap")
    assert one == 1 and win.term.report()["endings"] == 2, (one, win.term.report())
    print(f"  must-fail, WIN + end_run: {one} ending; a step then a cap: 2")
    dd = _agent(snaps.Snap(_spec(2)))
    _play(dd, dd.env, "A")
    dd.retarget(bind(snaps.Snap(_spec(2))), 1, "death")
    dd.end_run("time")
    rd = dd.term.report()
    assert rd["endings"] == 2 and rd["death_possible"] and rd["capped_seen"], rd
    print(f"  must-fail, a death then the deadline with no step between: {rd['endings']} endings, "
          f"death_possible {rd['death_possible']}, capped_seen {rd['capped_seen']}")
    # B
    keys = [(v["fingerprint"], v["action"], v["coord"], v["new"]) for v in vetoes]
    assert len(vetoes) == 3 and len(ag._vetoes) == 2, keys
    assert keys[0][:3] == keys[1][:3] and keys[0][3] and not keys[1][3], keys
    assert keys[2][0] != keys[0][0] and keys[2][3], keys
    assert all(v["fingerprint_of"] == "state" and v["coord"] is None for v in vetoes), vetoes
    print(f"  B: {len(vetoes)} veto rows, {len(ag._vetoes)} entries; the retry re-read its key "
          f"(new {keys[1][3]}); the other board is a second entry")
    aimed = _agent(Positioned(_spec(2)))
    for coord in ((1, 2), (5, 6)):

        def _choose(_before, _c=coord, _ag=aimed):
            _ag._aimed = _c
            return "A", "probe"
        aimed.choose = _choose
        aimed.step()
        assert aimed.env.terminal() == "death"
        aimed.retarget(bind(Positioned(_spec(2))), aimed.level + 1, "death")
    av = _ev(aimed, "veto")
    assert [v["coord"] for v in av] == [[1, 2], [5, 6]], av
    assert av[0]["fingerprint"] == av[1]["fingerprint"] and len(aimed._vetoes) == 2, av
    print("  must-fail, same board and action at another coordinate: two keys "
          f"{[v['coord'] for v in av]}")
    fps = []
    for hidden in (0, 1):
        b = Boarded(_spec(2), hidden)
        bag = _agent(b)
        _play(bag, b, "A")
        bag.retarget(bind(Boarded(_spec(2), hidden)), 1, "death")
        fps.append((_ev(bag, "veto")[0], bag._fingerprint({"s0": 2, "s1": 0})))
    (v0, _), (v1, _) = fps
    assert v0["fingerprint_of"] == v1["fingerprint_of"] == "board", fps
    assert v0["fingerprint"] != v1["fingerprint"], fps
    print("  board(): two boards that observe() alike get two fingerprints "
          f"({v0['fingerprint']} vs {v1['fingerprint']}), fingerprint_of 'board'")
    # OFF
    off = _ladder(False)
    assert not off._vetoes and not _ev(off, "veto") and not _ev(off, "termination")
    on_rows = [r for r in rows if r["event"] not in ("veto", "termination")]
    assert _bare(on_rows) == _bare(off.led.rows()), "the OFF arm's rows differ"
    arms = [r["detail"]["on"] for r in (rows[0], off.led.rows()[0])]
    assert ("tether._RUIN_RECORD" in arms[0]) and ("tether._RUIN_RECORD" not in arms[1]), arms
    print(f"  OFF: {len(off.led.rows())} rows, identical to ON (the arms row aside) less its "
          f"{len(rows) - len(on_rows)} termination/veto rows; no vetoes")
    print("ok")
