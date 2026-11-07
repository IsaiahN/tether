"""THE SELF-MOVING MEMO (the reviewer 2026-11-07 r1416): _admit asks _self_moving once per subject
per proposal pass, never across passes (the trace grows between them). The fake ARC game (the
library's grammar is loaded there; gridworld has none), a few steps, then two proposal passes on
the same agent, each in a PLAN scope. The subject S is the first one the filter read in pass 1.

  F1  pass 2, S planted self-moving (a constant +1 under every action, one planted press more):
      "self-moving subject" refuses it, and the R4 record reads verdict True, deltas [1]
  F2  pass 1 on the real trace: S is not self-moving (verdict False); pass 2 refuses it -- a memo
      kept across passes would carry pass 1's False
  MF  a memo kept across passes (a scratch copy of tether.py) fails F2 -- run by hand, named in
      the commit; "--child <tree>" prints both passes for a tree, so a base tree's counts can be
      compared to this one's (r1416 (b): "the count equals today's")

    python tests/test_self_moving_memo.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT


def passes(tree: str) -> list[dict]:
    sys.path.insert(0, tree)
    sys.path.insert(1, os.path.join(tree, "tests"))
    os.chdir(tree)
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    _env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    for _ in range(int(os.environ.get("SMM_STEPS", "3"))):
        ag.step()
    out, s = [], None
    for n in (1, 2):
        if n == 2:      # S moves +1 under every action, and one press more is planted
            rows = []
            for k, (b, a, af, i, land) in enumerate(ag.trace):
                b, af = dict(b), dict(af)
                b[s], af[s] = k, k + 1
                rows.append((b, a, af, i, land))
            last = rows[-1]
            for a in ag.actions:     # a positioned action needs two landings (_self_moving)
                for land in ((0, 0), (1, 1)) if a in tether.IFace.POSITIONED else (None,):
                    b, af = dict(rows[-1][2]), dict(rows[-1][2])
                    af[s] = b[s] + 1
                    rows.append((b, a, af, last[3], land))
            ag.trace = rows
        before = ag.trace[-1][2]
        with ag._step_scope("PLAN"):
            ag._hyp_propose(before)
        row = [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]["detail"]
        rec = row.get("self_moving") or {}
        if s is None:
            s = sorted(rec)[0] if rec else None
            if s is None:
                return [{"pass": 1, "record": None, "refused": row["refused"]}]
        out.append({"pass": n, "subject": s,
                    "refused_self_moving": row["refused"].get("self-moving subject", 0),
                    "record": rec.get(s), "refused": row["refused"], "open": row.get("open"),
                    "pick": row.get("pick")})
    return out


def main() -> int:
    if len(sys.argv) > 2 and sys.argv[1] == "--child":
        print(json.dumps(passes(sys.argv[2]), sort_keys=True))
        return 0
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--child", HERE],
                       capture_output=True, text=True, env=env, cwd=HERE,
                       stdin=subprocess.DEVNULL, timeout=600)
    assert p.returncode == 0, p.stderr[-2000:]
    got = json.loads(p.stdout.strip().splitlines()[-1])
    assert got[0]["record"] is not None and len(got) == 2, \
        ("precondition: no subject reached the self-moving filter", got[0]["refused"])
    p1, p2 = got
    s = p1["subject"]
    assert p1["record"]["verdict"] is False, ("F2 pass 1", p1)
    assert p2["record"] is not None and p2["record"]["verdict"] is True, ("F1 record", p2)
    assert p2["record"]["deltas"] == [1], ("F1 deltas", p2["record"])
    assert p2["refused_self_moving"] > 0, ("F1/F2: pass 2 did not refuse the subject", p2)
    print(f"F2  pass 1: {s} read, verdict False, {p1['refused_self_moving']} refused "
          f"(open {p1['open']})")
    print(f"F1  pass 2: {s} verdict True, deltas [1], refused \"self-moving subject\" "
          f"{p2['refused_self_moving']} (open {p2['open']})")
    print("self_moving_memo: 2 of 2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
