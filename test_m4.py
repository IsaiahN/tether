"""M4's fixture (the reviewer 2026-10-09 10:25Z): the reach wire end to end, through the ARC
wiring and the real agent, in a world where the library's description has something to reach.

o1 shuttles toward o2 and back; on each contact o2 takes a new colour. One recolour is a residual
under the floor (the bargain refuses it before any description matters), so the contact RECURS
until the mint searches o2.colour. Asserted: the compiled CAUSE pair
touches<o2> => other<o2.colour~1> is supported, offered with its provenance, and yielded to
the mint with its OWN operand.
Must-fails: with the library emptied the old path is byte-identical; with the ~1 arm OFF the pair
is withheld by the gate and its operand never reaches the mint.

    python test_m4.py
"""
from __future__ import annotations

import contextlib
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
from arcengine import FrameDataRaw, GameState

import test_entry
import tether
import tether_agent

sys.dont_write_bytecode = True

# anchor: measured on this world -- the mint first searches o2.colour at cycle 18 (under the
# floor before), so 20 actions is the shortest run that reaches the candidate stream
ACTIONS = 20
SLOT, PAIR_IF, PAIR_THEN, OPERAND = "o2.colour", "touches<o2>", "other<o2.colour~1>", "o2.colour~1"


class Contagion(test_entry.FakeWrapper):
    """o1 (colour 3) steps toward o2 and back; the frame after each contact o2 recolours."""
    COLOURS = (9, 11, 12, 13, 14, 2, 4, 6)

    def reset(self):
        self.calls.append("RESET")
        self.c1, self.col2, self.touched, self.dir, self.k = 10, 7, False, 4, 0
        return self._frame(GameState.NOT_FINISHED)

    def _frame(self, state):
        g = np.zeros((64, 64), dtype=int)
        g[30:34, self.c1:self.c1 + 4] = 3
        g[30:34, 30:34] = self.col2
        f = FrameDataRaw(game_id="cont-0001", state=state, levels_completed=0, win_levels=2,
                         guid="g", available_actions=list(self.actions))
        f.frame = [g]
        self._last = f
        return f

    def step(self, action, data=None, reasoning=None):  # noqa: ARG002 -- the wrapper's signature
        self.calls.append(action.name)
        if action.name == "RESET":
            return self.reset()
        if self.touched:
            self.col2 = self.COLOURS[self.k % len(self.COLOURS)]
            self.k, self.touched, self.dir = self.k + 1, False, -4
        self.c1 += self.dir
        if self.c1 <= 10:
            self.c1, self.dir = 10, 4
        if self.c1 + 4 >= 30:
            self.c1, self.touched = 26, True
        return self._frame(GameState.NOT_FINISHED)


@contextlib.contextmanager
def _arms(prev: bool, first: bool, library: bool = True):
    was = (tether._PREV_OFFER, tether._LIBRARY_FIRST, tether._library)
    tether._PREV_OFFER, tether._LIBRARY_FIRST = prev, first
    if not library:
        tether._library = lambda: None
    try:
        yield
    finally:
        tether._PREV_OFFER, tether._LIBRARY_FIRST, tether._library = was


def _run(**arms) -> tuple[list, list]:
    """The ledger rows and every (cycle, chain, offered operands) yielded on SLOT."""
    yielded, orig = [], tether.Agent._library_chains

    def spy(self, slot, in_t, out_t, stats, ops, *a, **k):     # fbe9f41: and evidence
        got = orig(self, slot, in_t, out_t, stats, ops, *a, **k)
        if slot == SLOT:
            yielded.extend((self.cycle, c.name, list(ops.get(c.name, ()))) for c in got)
        return got
    tether.Agent._library_chains = spy
    try:
        with _arms(**arms), tempfile.TemporaryDirectory() as d:
            led = Path(d) / "m4.jsonl"
            tether_agent.run(Contagion(), "cont", max_actions=ACTIONS, led_path=str(led))
            rows = [json.loads(x) for x in led.read_text(encoding="utf-8").splitlines() if x]
    finally:
        tether.Agent._library_chains = orig
    return [r for r in rows if isinstance(r, dict)], yielded


def _pair(rows: list) -> list:
    return [s for r in rows if r.get("event") == "library" and r.get("slot") == SLOT
            for s in r["detail"]["supported"] if s["if"] == PAIR_IF and s["then"] == PAIR_THEN]


def _old_path(rows: list) -> list:
    """The ledger with the library's rows and fields removed, every seq reference renumbered."""
    keep = [r for r in rows if r.get("event") != "library"]
    seq = {r["seq"]: i for i, r in enumerate(keep)}

    def tr(o):
        if isinstance(o, dict):
            return {k: (seq.get(v, ("UNMAPPED", v)) if k in ("seq", "recorded_before")
                        and isinstance(v, int) else tr(v))
                    for k, v in o.items() if k not in ("library_first", "library")}
        return [tr(v) for v in o] if isinstance(o, list) else o
    return [tr(r) for r in keep]


def test_the_contagion_pair_reaches_the_mint_with_its_operand():
    rows, yielded = _run(prev=True, first=True)
    pair = [s for s in _pair(rows) if s["offered"]]
    assert pair, "the pair was never supported and offered on o2.colour"
    assert all(s["library"] and s["entries"] >= 1 for s in pair), pair[0]
    assert any(OPERAND in ops for _c, _n, ops in yielded), \
        f"the pair's own operand never reached the mint: {yielded[:3]}"
    return rows, len(pair), pair[0]["library"], pair[0]["entries"], yielded


def test_an_emptied_library_leaves_the_old_path_identical(full: list):
    rows, yielded = _run(prev=True, first=True, library=False)
    assert not yielded and not any(r.get("event") == "library" for r in rows)
    # RESTATED (the reviewer 2026-10-18 11:03): the library has consumers past the reach wire
    # since E1 / K1 / A1's summons, so its lookup and choice rows are library-fed and differ by
    # design. The old path is the DECISIONS: bet, settle, mint and act rows, equal in content
    def _decisions(rs):
        return [(r["cycle"], r["slot"], r["event"], json.dumps(r.get("detail"), sort_keys=True,
                                                               default=str))
                for r in rs if r.get("event") in ("bet", "settle", "mint", "act")]
    assert _decisions(rows) == _decisions(full), "the library changed the old path's decisions"
    ca = [r for r in full if r.get("event") == "choice"]
    cb = [r for r in rows if r.get("event") == "choice"]
    d = next(((x, y) for x, y in zip(ca, cb, strict=False)
              if x.get("detail") != y.get("detail")), None)
    print(f"  (information) choice rows {len(ca)} / {len(cb)}; first library-fed difference: "
          f"{None if d is None else (d[0]['cycle'], d[0]['slot'])}")


def test_the_prev_gate_withholds_the_pair():
    rows, yielded = _run(prev=False, first=True)
    pair = _pair(rows)
    assert pair and not any(s["offered"] for s in pair), pair[:1]
    assert any("TETHER_PREV_OFFER off" in s["why"] for s in pair), [s["why"] for s in pair]
    assert not any(OPERAND in ops for _c, _n, ops in yielded)


if __name__ == "__main__":
    full, n, prov, entries, ylds = test_the_contagion_pair_reaches_the_mint_with_its_operand()
    test_an_emptied_library_leaves_the_old_path_identical(full)
    test_the_prev_gate_withholds_the_pair()
    print(f"m4: {PAIR_IF} => {PAIR_THEN} supported and offered on {n} lookup(s), provenance "
          f"{prov!r} (+{entries - 1} more entries), yielded to the mint with {OPERAND} on "
          f"{sum(OPERAND in o for _c, _n, o in ylds)} of {len(ylds)} chains; the library emptied "
          f"leaves the old path's decisions identical; the ~1 gate withholds it with the arm OFF")
