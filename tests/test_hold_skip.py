"""E, THE GROUP HOLD SKIP (the reviewer 2026-11-07 r1419, r1424, r1427): a group none of whose
member subjects (as spelled, plus the 16c mirror) can route is not linked or route-read; its
displaced wants are restored as a failed hold restores them. The fake ARC game, 12 steps, three
children: ON (as built), OFF (_hyp_hold called without `routable`, as before E), MF (the skip
widened to every candidate: a planted wrong skip).

  H1  the skip fires ON (HOLD_SKIP_N["skipped"] > 0, the precondition)
  H2  ON vs OFF: the picks, the holds checked, the refused-by-reason counts and the order of
      self.wants after every step are equal
  MF  the widened skip changes the picks -- so H2's comparison can see a wrong skip

    python tests/test_hold_skip.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT


def child(mode: str) -> dict:
    sys.path.insert(0, HERE)
    sys.path.insert(1, os.path.join(HERE, "tests"))
    os.chdir(HERE)
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    real = tether.Agent._hyp_hold

    def hold(self, key, c, before, routable=None):
        if mode == "off":
            routable = None
        elif mode == "mf" and routable is not None:
            return None, "no route"     # the planted wrong skip: every ranked candidate
        return real(self, key, c, before, routable)
    tether.Agent._hyp_hold = hold
    _env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    wants = []
    for _ in range(12):
        ag.step()
        wants.append(list(ag.wants))
    gh = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_hypotheses"]
    return {"skip": dict(tether.HOLD_SKIP_N), "picks": [d.get("pick") for d in gh],
            "checked": [d.get("checked") for d in gh], "refused": [d.get("refused") for d in gh],
            "wants": wants}


def run(mode: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--child", mode],
                       capture_output=True, text=True, env=env, cwd=HERE,
                       stdin=subprocess.DEVNULL, timeout=900)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def main() -> int:
    if len(sys.argv) > 2 and sys.argv[1] == "--child":
        print(json.dumps(child(sys.argv[2]), sort_keys=True))
        return 0
    on, off, mf = run("on"), run("off"), run("mf")
    assert on["skip"].get("skipped", 0) > 0, ("H1 precondition: the skip never fired", on["skip"])
    assert not off["skip"], ("OFF must not skip", off["skip"])
    for k in ("picks", "checked", "refused", "wants"):
        assert on[k] == off[k], (f"H2: {k} differs ON vs OFF", on[k], off[k])
    assert mf["picks"] != off["picks"], ("MF: a skip widened to every candidate kept the picks",
                                         mf["picks"])
    print(f"H1  skipped {on['skip']['skipped']} groups (with a mirror: "
          f"{on['skip'].get('skipped_with_mirror', 0)})")
    print(f"H2  ON = OFF: picks {off['picks']}, holds checked, refused counts, wants order "
          f"per step")
    print(f"MF  the widened skip changes the picks: {mf['picks']}")
    print("hold_skip: 3 of 3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
