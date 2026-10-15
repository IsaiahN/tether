"""THE STOP-LOSS (the reviewer 2026-10-14 11:32, 11:39): a run WRITES what its Gamma holds to a
save-only path and never reads it back.

  (a) OFF identity: the ledger of a run with the save-only path is the ledger of one without it,
      row for row;
  (b) one file per run, named by the run header, marked lossy in its own header;
  (c) a second run with the same save-only path never loads anything (Gamma.load is not called)
      and writes a second, distinct file;
  (d) an existing file is never overwritten (a stand-in holding a real Gamma, so removing the
      refusal trips a NAMED assertion, not a crash);
  (e) two runs whose ledgers share a stem in different folders both save.

    python test_save_only.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import arc_holdout
import gamma
import gridworld
import tether_agent
import world
from test_entry import FakeWrapper

sys.dont_write_bytecode = True
N = 2


def _run(tmp: Path, name: str, save_only_dir: str | None = None) -> tuple[dict, list]:
    led = tmp / f"{name}.jsonl"
    led.parent.mkdir(parents=True, exist_ok=True)
    rep = tether_agent.run(FakeWrapper(), "fake", N, led_path=str(led), save_only_dir=save_only_dir)
    return rep, [json.loads(x) for x in led.read_text(encoding="utf-8").splitlines() if x.strip()]


def main() -> None:
    import tether
    # C-seed-X (the reviewer 2026-10-15 15:27): two separately born agents compared, so one
    # temperament: the old constant seed, a replay-style constant inside a test
    tether._AGENT_SEED = False
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        so = tmp / "saves"
        # A WARM-UP RUN FIRST: the run header hashes the modules LOADED so far (files_sha,
        # n_files), and the first run in a process loads some lazily, so run 1 and run 2 differ
        # in that one row whatever is saved (measured: plain vs plain, row 0 only).
        _run(tmp, "warm")
        _, plain = _run(tmp, "plain")
        rep, saving = _run(tmp, "saving", str(so))
        assert plain == saving, "the save-only path changed the ledger"
        print(f"  (a) ledger identical with and without the save-only path ({len(plain)} rows)")
        files = sorted(so.glob("*.json"))
        assert len(files) == 1 and rep["saved_only"]["path"] == str(files[0]), (files, rep)
        hdr = json.loads(files[0].read_text(encoding="utf-8"))["header"]
        assert hdr["lossy"] == arc_holdout.LOSSY and hdr["game"] == "fake", hdr
        assert "_saving" in files[0].name and hdr["ledger"].endswith("saving.jsonl")
        print(f"  (b) one file, {files[0].name}, marked lossy")
        loads = []
        real = gamma.Gamma.load
        gamma.Gamma.load = lambda self, path: loads.append(path) or real(self, path)
        try:
            rep2, _ = _run(tmp, "second", str(so))
        finally:
            gamma.Gamma.load = real
        assert not loads, f"a run read a save: {loads}"
        assert len(sorted(so.glob("*.json"))) == 2 and rep2["saved_only"]["path"] != str(files[0])
        print("  (c) a second run loads nothing and writes its own file")
        before = files[0].read_bytes()
        again = arc_holdout.save_only(type("A", (), {"led": _Led(plain), "env": ArcWorld(),
                                                       "gamma": _gamma()})(),
                                      str(so), "fake", str(tmp / "saving.jsonl"))
        assert files[0].read_bytes() == before, "an existing save was overwritten"
        assert "refused" in again and "exists" in again["refused"], again
        print("  (d) an existing file is never overwritten")
        _run(tmp, "x/same", str(so))
        _run(tmp, "y/same", str(so))
        same = sorted(so.glob("*_same*.json"))
        assert len(same) == 2, f"a same-stem run's save was lost: {same}"
        print(f"  (e) two ledgers named same.jsonl in different folders: {len(same)} saves")
    print("save only: OK")


def _gamma() -> gamma.Gamma:
    """A real Gamma over a real world's atoms (as test_probe_flush builds one), so a save from it
    writes a file whose bytes differ from the run's."""
    return gamma.Gamma(world.bind(gridworld.family("default", 0, 4)).atoms(), game="other")


class ArcWorld:
    """Named as the real world is, so (d) rebuilds the real run's file name."""


class _Led:
    """Just the header lookup save_only makes, over a real run's rows."""

    def __init__(self, rows):
        self._hdr = next(r for r in rows if r["slot"] == "@run" and r["event"] == "arms")

    def by_event(self, event):
        return [type("E", (), {"slot": "@run", "detail": self._hdr["detail"]})()] \
            if event == "arms" else []


if __name__ == "__main__":
    main()
