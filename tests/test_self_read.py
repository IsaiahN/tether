"""M3 SELF_READ (the reviewer 2026-11-02 r844 3): the narrator's N2 link counted per game, carried by
the lineage, read at the next game's start.
  SR-a  a game with a bet and nothing minted ends "vocabulary", one with no bet "perception": the
        narrator counts each (links).
  SR-b  game 1 writes those counts (stopped_at); game 2, a new agent loading the lineage, starts
        with a self_read row naming them; a second write with no new game carries nothing again.
  MUST-FAIL: OFF writes no stopped_at and loads no self_read row.

    python tests/test_self_read.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import lineage  # noqa: E402
import narrate  # noqa: E402
import tether  # noqa: E402
from test_consolidate import agent  # noqa: E402


def links() -> dict:
    n = narrate.Narrator(Path(tempfile.mkdtemp()) / "run.jsonl", ("WIN", "ADVANCE"))
    n.see(0, "PERCEIVE", "o1.x", "bet", {})
    n.end_game(0, "g1")
    n.say(1, "PLAN", "o1.x", "a plan with no bet")
    n.end_game(1, "g2")
    return dict(n.links)


def carry(got: dict, on: bool = True):
    tether._SELF_READ = on
    try:
        d = tempfile.mkdtemp()
        _t, _env, g1 = agent(lineage_dir=d)
        g1.led.narrator.links.update(got)
        lineage.write(d, g1, "fake")
        again = lineage.write(d, g1, "fake")
        _t, _env, g2 = agent(lineage_dir=d)
        rows = [r["detail"] for r in g2.led.rows() if r["event"] == "self_read"]
        gens = [g.get("stopped_at") for _h, g in lineage._chain(Path(d))]
        return g2._stopped_in, rows, gens, again
    finally:
        tether._SELF_READ = True


def main():
    assert tether._SELF_READ, "ON by default"
    got = links()
    assert got == {"vocabulary": 1, "perception": 1}, ("SR-a: one link per game", got)
    into, rows, gens, _a = carry(got)
    assert into == got and rows and rows[0]["stopped_at"] == got and rows[0]["games"] == 2, (
        "SR-b: carried and read at the start", into, rows)
    assert gens == [got, {}], ("SR-b: the second write carries nothing again", gens)
    off_in, off_rows, off_gens, _a = carry(got, on=False)
    assert not off_in and not off_rows and off_gens == [None, None], (
        "MUST-FAIL: OFF records and reads nothing", off_in, off_rows, off_gens)
    print(f"test_self_read: links {got}; game 2 starts with self_read {rows[0]['stopped_at']} "
          f"({rows[0]['games']} games); generations {gens}; OFF none")


if __name__ == "__main__":
    main()
