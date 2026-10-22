"""C-seed-1, HOLD_SEED: THE SEED MADE THE AGENT'S (the reviewer 2026-10-15 14:56, 15:04). WRITTEN,
NOT RUN: it runs in the end-of-step-7 checklist. Each agent runs in a child process, because the
arms resolve at import.

  S1  BIRTH: two agents born with nothing set draw different seeds, each "birth", generation 0,
      draw seed "<seed>:0", and the run header records it.
  S2  REPLAY: an agent pointed at S1's first ledger (TETHER_SEED_FROM) carries that seed and
      generation, labelled "replay:<sha16>"; it chose nothing.
  S3  A SEEDLESS RECORD IS REFUSED BY NAME: a ledger written with the arm OFF carries no seed of
      the agent's, and an agent pointed at it does not start.
  S4  OFF: TETHER_AGENT_SEED=0 gives seed "0", draw seed "0", "constant" (the old draws exactly).
  S5  RETIRED: TETHER_HOLD_SEED set refuses the agent's birth by name.
  S6  LINEAGE (Q1): an agent loading a one-generation lineage carries its writer's seed, as
      "lineage:<tip>", at generation 1, so its draw seed is "<seed>:1". MF-S6: the writer's draw
      seed ("<seed>:0") differs, so the continued life does not replay its day. F-a: gamma's draw
      seed when load_blob runs is already the lineage's ("<seed>:1"), so a handle the load mints
      is minted under the seed a replay reads; with the old order it was the birth seed.
  S7  HANDLES (Q4): under a seed a composition's handle is the same twice and differs under another
      seed; the old random suffix is kept for None.

    python tests/test_agent_seed.py
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

CHILD = """
import json, sys
sys.dont_write_bytecode = True
import arc_holdout, gamma, lineage
from test_entry import FakeWrapper
at_load, real = [], gamma.Gamma.load_blob
def spy(self, *a, **k):
    at_load.append(self.draw_seed)
    return real(self, *a, **k)
gamma.Gamma.load_blob = spy
led, lin, write = sys.argv[1], sys.argv[2] or None, sys.argv[3] == "1"
env, ag, _led, *_ = arc_holdout.wire(FakeWrapper(), "fake", led_path=led, lineage_dir=lin)
[ag.step() for _ in range(5)]
if write:
    lineage.write(lin, ag, "fake")
print("OUT " + json.dumps({"seed": ag.seed, "gen": ag.generation, "src": ag.seed_source,
                           "draw": ag.draw_seed, "at_load": at_load}))
"""


def child(led: Path, lin: Path | None = None, write: bool = False, **env_set) -> tuple:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(env_set)
    r = subprocess.run([sys.executable, "-B", "-c", CHILD, str(led), str(lin or ""),
                        "1" if write else "0"], env=env, capture_output=True, text=True,
                       check=False, stdin=subprocess.DEVNULL)
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return r.returncode, (json.loads(out[-1][4:]) if out else None), r.stderr[-2000:]


def header(led: Path) -> dict:
    rows = [json.loads(ln) for ln in led.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return next(r["detail"] for r in rows if r["slot"] == "@run" and r["event"] == "arms")


def main() -> None:
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        rc, a, err = child(t / "a.jsonl")
        assert rc == 0, err
        rc, b, err = child(t / "b.jsonl")
        assert rc == 0, err
        assert a["seed"] != b["seed"] and a["src"] == b["src"] == "birth", (a, b)
        assert a["gen"] == 0 and a["draw"] == f"{a['seed']}:0", a
        assert header(t / "a.jsonl")["seed"] == a["seed"], "S1: the header does not record it"
        print(f"  S1 two births, two seeds; header records {a['seed']}")

        rc, r, err = child(t / "r.jsonl", TETHER_SEED_FROM=str(t / "a.jsonl"))
        assert rc == 0, err
        assert (r["seed"], r["gen"]) == (a["seed"], 0) and r["src"].startswith("replay:"), r
        print(f"  S2 the replay carries the recorded seed ({r['src']})")

        rc, o, err = child(t / "off.jsonl", TETHER_AGENT_SEED="0")
        assert rc == 0, err
        assert (o["seed"], o["draw"], o["src"]) == ("0", "0", "constant"), o
        print("  S4 OFF: seed 0, draw seed 0, constant")

        rc, _, err = child(t / "x.jsonl", TETHER_SEED_FROM=str(t / "off.jsonl"))
        assert rc != 0 and "carries no seed" in err, (rc, err)
        print("  S3 a seedless record is refused by name")

        rc, _, err = child(t / "h.jsonl", TETHER_HOLD_SEED="5")
        assert rc != 0 and "TETHER_HOLD_SEED is retired" in err, (rc, err)
        print("  S5 TETHER_HOLD_SEED refused by name")

        lin = t / "lin"
        lin.mkdir()
        rc, w, err = child(t / "w.jsonl", lin, write=True)
        assert rc == 0, err
        rc, c, err = child(t / "c.jsonl", lin)
        assert rc == 0, err
        assert c["seed"] == w["seed"] and c["gen"] == 1 and c["src"].startswith("lineage:"), c
        assert c["draw"] == f"{w['seed']}:1", c
        assert c["draw"] != w["draw"], "MF-S6: the continued life replays its day"
        assert c["at_load"] == [c["draw"]], ("F-a: the load ran under another seed", c)
        print(f"  S6 the lineage carries the seed at generation 1 ({c['draw']})")

    import arc_holdout
    from test_entry import FakeWrapper
    term = next(iter(arc_holdout.wire(FakeWrapper(), "fake")[1].gamma.library.values()))
    h1, h2 = term.handle("g", "s:0"), term.handle("g", "s:0")
    assert h1 == h2 and h1 != term.handle("g", "t:0"), (h1, h2)
    assert len(term.handle("g").rsplit("_", 1)[1]) == 8
    print(f"  S7 a handle under a seed is stable ({h1}) and differs under another")
    print("agent seed: OK")


if __name__ == "__main__":
    main()
