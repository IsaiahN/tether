"""BUILD 2 7d, THE PIPELINE LOG (TETHER_PIPELINE_LOG; the reviewer r895 4, r992 3), and r992's
rider (TETHER_CLOSURE_VERDICT). About a minute.

MF-P1  a gridworld agent with a ledger path writes pipeline.log: one line per stage scope exit,
       "c<cycle> <STAGE> <ms>ms rows=... slots=<n> stop=...", every STAGE one of ledger.STEPS, on
       the cycles the agent ran; RED on HEAD (no pipeline.log)
MF-P2  the ledger is the same ON and OFF (identity_mod_rows: only the arms row differs)
MF-P3  deep mode over one cycle (TETHER_PIPELINE_DEEP=c1-c1) writes function lines, and only
       under that cycle's stage lines; each with its self time (r999: the inclusive list names
       the wrapper), self <= ms, the largest self first
MF-P4  rotation at a tiny segment and cap: closed segments are gzipped, the oldest unpinned is
       dropped past the cap (a "rotation: dropped" line), a segment covering a planted game_win
       ending is pinned and survives
MF-P5  OFF: no pipeline.log
MF-V   the rider, split by Fig 8 (r994): candidates priced and none at pays reads "not found
       within budget" when a budget stopped it (budget_spent) and "closure cannot cover R" when it
       enumerated to its depth (depth_exhausted), each with stopped_by and the best candidate; with
       a pays call, or the arm OFF, the verdict is the old one

    python tests/test_pipelog.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402
import pipelog  # noqa: E402

HERE = Path(__file__).resolve()
LINE = re.compile(r"^c(\d+) ([A-Z]+) [\d.]+ms rows=\S+ slots=\d+ stop=\S+$")
FN = re.compile(r"^  fn \S+ calls=\d+ ms=([\d.]+) self=([\d.]+)$")


def child(out: str, env_extra: dict, steps: int = 4) -> None:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
           "TETHER_AGENT_SEED": "0", **env_extra}
    r = subprocess.run([sys.executable, "-B", str(HERE), "--run", out, str(steps)], env=env,
                       capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stderr[-2000:]


def run(out: str, steps: int) -> None:
    import gamma
    import gridworld
    import tether
    import world
    env = world.bind(gridworld.family("default", 0))
    os.makedirs(out, exist_ok=True)      # narrate and the pipeline log write beside the ledger
    led = ledger.Ledger(path=os.path.join(out, "run.jsonl"))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    for _ in range(steps):
        ag.step()
    ag.end_run("cap")


def rows(p: Path) -> list:
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def main():
    if "--run" in sys.argv:
        i = sys.argv.index("--run")
        run(sys.argv[i + 1], int(sys.argv[i + 2]))
        return
    sys.path.insert(0, str(HERE.parent.parent / "conform"))
    import identity_mod_rows
    with tempfile.TemporaryDirectory() as td:
        on, off, deep = (Path(td) / n for n in ("on", "off", "deep"))
        child(str(on), {})
        child(str(off), {"TETHER_PIPELINE_LOG": "0"})
        child(str(deep), {"TETHER_PIPELINE_DEEP": "c1-c1"})
        log = (on / "pipeline.log").read_text(encoding="utf-8").splitlines()
        bad = [x for x in log if not LINE.match(x)]
        stages = {LINE.match(x).group(2) for x in log if LINE.match(x)}
        cycles = sorted({int(LINE.match(x).group(1)) for x in log if LINE.match(x)})
        assert log and not bad and stages <= set(ledger.STEPS) and cycles == [0, 1, 2, 3, 4], (
            "MF-P1", bad[:3], stages, cycles)
        diff = identity_mod_rows.compare(rows(off / "run.jsonl"), rows(on / "run.jsonl"), set())
        assert all(d.startswith("seq 0 (arms)") for d in diff), ("MF-P2", diff[:3])
        dl = (deep / "pipeline.log").read_text(encoding="utf-8").splitlines()
        cyc, fn_cycles, blocks = None, set(), []
        for x in dl:
            m = LINE.match(x)
            if m:
                cyc = int(m.group(1))
                blocks.append([])
            elif x.startswith("  fn "):
                fn_cycles.add(cyc)
                f = FN.match(x)
                if f:
                    blocks[-1].append((float(f.group(1)), float(f.group(2))))
        selfs = [s for b in blocks for s in b]
        assert fn_cycles == {1}, ("MF-P3", fn_cycles)
        assert selfs and all(own <= inc + 0.05 for inc, own in selfs) and all(
            [own for _i, own in b] == sorted((own for _i, own in b), reverse=True)
            for b in blocks), ("MF-P3 self", [b[:4] for b in blocks if b][:3])
        assert not (off / "pipeline.log").exists(), "MF-P5"
        n_lines = len(log)
    with tempfile.TemporaryDirectory() as td:
        was = (pipelog.SEG_BYTES, pipelog.CAP_BYTES)
        try:
            pipelog.SEG_BYTES, pipelog.CAP_BYTES = 300, 400
            pl = pipelog.PipeLog(Path(td) / "run.jsonl", (ledger.WIN, ledger.ADVANCE))
            for c in range(40):
                pl.enter("MINT", c)
                if c == 3:
                    pl.see(c, "IMPORT", "@loop", "ending", {"how": ledger.WIN})
                pl.see(c, "MINT", "o1.row", "park", {"verdict": "budget_spent"})
                pl.exit("MINT", c, False)
        finally:
            pipelog.SEG_BYTES, pipelog.CAP_BYTES = was
        segs = sorted(p.name for p in Path(td).glob("pipeline.*.log.gz"))
        cur = (Path(td) / "pipeline.log").read_text(encoding="utf-8")
        pinned = [s for s in segs if ".pin." in s]
        assert pinned == ["pipeline.00000.pin.log.gz"] and "rotation: dropped" in cur + "".join(
            __import__("gzip").open(Path(td) / s, "rt").read() for s in segs) \
            and not (Path(td) / "pipeline.00001.log.gz").exists(), ("MF-P4", segs, cur[:200])
    import tether
    ag = tether.Agent.__new__(tether.Agent)
    ag._priced, ag._cp_best = 12, {"term": "inc . dec", "rows_read": 3, "of_rows": 9,
                                   "cost_bits": 12.8, "misses_allowed": 0}
    d = {"verdict": "budget_spent", "slot": "o1.row"}
    v1 = ag._closure_verdict(d, 0, {0: {"pays_called": 0}})
    v4 = ag._closure_verdict({**d, "verdict": "depth_exhausted"}, 0, {0: {"pays_called": 0}})
    v2 = ag._closure_verdict(d, 0, {0: {"pays_called": 1}})
    was = tether._CLOSURE_VERDICT
    try:
        tether._CLOSURE_VERDICT = False
        v3 = ag._closure_verdict(d, 0, {0: {"pays_called": 0}})
    finally:
        tether._CLOSURE_VERDICT = was
    assert v1["verdict"] == "not found within budget" and v1["stopped_by"] == "budget_spent" \
        and v4["verdict"] == "closure cannot cover R" and v4["stopped_by"] == "depth_exhausted" \
        and v1["best_candidate"]["rows_read"] == 3 and v2 is d and v3 is d \
        and d["verdict"] == "budget_spent", ("MF-V", v1, v2, v3)
    print(f"  MF-P1 {n_lines} stage lines, stages {sorted(stages)}, cycles {cycles}")
    print(f"  MF-P2 the ledger ON vs OFF: {len(diff)} difference(s), the arms row only")
    print(f"  MF-P3 deep mode c1-c1: function lines under cycles {sorted(fn_cycles)}, "
          f"{len(selfs)} with self <= ms, largest self first")
    print(f"  MF-P4 rotation: {segs}; the pinned segment kept")
    print("  MF-P5 OFF: no pipeline.log")
    print(f"  MF-V budget_spent -> {v1['verdict']!r}; depth_exhausted -> {v4['verdict']!r}; "
          f"with a pays call or OFF: "
          f"{v2['verdict']!r} / {v3['verdict']!r}")
    print("test_pipelog OK")


if __name__ == "__main__":
    main()
