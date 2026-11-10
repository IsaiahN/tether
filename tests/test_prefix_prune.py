"""TETHER_PREFIX_PRUNE (the reviewer 2026-11-04 r1010 3, r1012 4, r1019 4; Fig 8 :41-42 "more
search, not another atom"). pays needs cost + left < base with left >= 0, so a chain whose cost
alone with the cheapest guard reaches base can never pay, nor can an extension of it; the walk
neither yields nor extends it nor counts it against its budget. The demo world (world.Transitions,
which mints).

MF-P1  MUST-STAY at an ample budget (work budget 15000): the minted terms are identical ON and OFF,
       and there are some
MF-P2  EXACTNESS by brute force: every chain the predicate pruned (the first 60 per mint), extended
       by every unit to the walk's max depth, is pruned too -- 0 counterexamples
MF-P4  (r1029) at an AMPLE budget the park VERDICT per slot is the same ON and OFF, on the demo
       world and gridworld: a pruned chain still reads novelty, so a mint whose novel terms were
       all too dear parks "priced_out_at_depth" ON as OFF does, never "not_novel"; RED on 21726d3
MF-P3  at a small walk budget, ON prices strictly more candidates than OFF in the same work budget,
       and the park rows count "pruned at the prefix: not generated"; RED on HEAD (no arm: equal)

    python tests/test_prefix_prune.py
"""
from __future__ import annotations

import collections
import json
import os
import subprocess
import sys
from pathlib import Path

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

HERE = Path(__file__).resolve()


def run(work: int, walk: int | None, spy: bool, which: str = "demo") -> dict:
    import gridworld
    env = world.bind(world.Transitions() if which == "demo" else gridworld.family("default", 0))
    led = ledger.Ledger()
    cfg = tether.Config(work_budget=work, **({"budget": walk} if walk else {}))
    g = gamma.Gamma(env.atoms()) if which == "demo" else gamma.Gamma(env.atoms(),
                                                                       game="fam_default_0")
    pruned: list = []
    seen_args: list = []          # the (depth, closed) each pruned chain was walked at
    if spy:
        real = gamma.Gamma.enumerate_closure

        def wrapped(self, *a, prune=None, **k):
            if prune is None:
                return real(self, *a, **k)

            def p(chain, *rest, _p=prune):
                hit = _p(chain, *rest)
                if hit:
                    seen_args.append(rest)
                if hit and len(pruned) < 60 * 40:
                    pruned.append((chain, _p, a[2]))
                return hit
            return real(self, *a, prune=p, **k)
        gamma.Gamma.enumerate_closure = wrapped
    try:
        ag = tether.Agent(env, g, cfg, led)
        if which == "demo":
            ag.run(16)
        else:
            for _ in range(12):
                ag.step()
    finally:
        if spy:
            gamma.Gamma.enumerate_closure = real
    rows = led.rows()
    minted = sorted((r.get("slot"), r["detail"].get("term")) for r in rows if r["event"] == "mint")
    priced = sum(r["detail"].get("candidates_priced") or 0 for r in rows if r["event"] == "park")
    cut = sum((r["detail"].get("cut_counts") or {}).get("pruned at the prefix: not generated", 0)
              for r in rows if r["event"] == "park")
    bad = checked = 0
    if spy:
        units = g.units()
        for chain, p, depth in pruned[:600]:
            frontier = [chain]
            while frontier:
                nxt = []
                for ch in frontier:
                    if len(ch) >= depth:
                        continue
                    for u in units:
                        ext = ch + u.atoms
                        if len(ext) > depth:
                            continue
                        checked += 1
                        try:                    # the cost test alone: beyond max depth, open
                            ok = p(ext, 10 ** 9, False)
                        except TypeError:       # a one-argument predicate (before r1030)
                            ok = p(ext)
                        if not ok:
                            bad += 1
                        nxt.append(ext)
                frontier = nxt[:200]
    parks = [(r["cycle"], r.get("slot"), r["detail"].get("verdict")) for r in rows
             if r["event"] == "park"]
    unclosed = sum(1 for r in seen_args if len(r) == 2 and r[0] == cfg.max_depth and not r[1])
    return {"minted": minted, "priced": priced, "cut": cut, "pruned": len(pruned),
            "checked": checked, "bad": bad, "parks": parks, "unclosed_at_max": unclosed,
            "pruned_all": len(seen_args)}


def child(extra: dict, *args) -> dict:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
           "TETHER_AGENT_SEED": "0", **extra}
    r = subprocess.run([sys.executable, "-B", str(HERE), "--run", *map(str, args)], env=env,
                       capture_output=True, text=True, timeout=1200)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def main():
    if "--run" in sys.argv:
        i = sys.argv.index("--run")
        work, walk, spy = int(sys.argv[i + 1]), int(sys.argv[i + 2]), sys.argv[i + 3] == "1"
        which = sys.argv[i + 4] if len(sys.argv) > i + 4 else "demo"
        print(json.dumps(run(work, walk or None, spy, which)))
        return
    on1, off1 = child({}, 15000, 0, 0), child({"TETHER_PREFIX_PRUNE": "0"}, 15000, 0, 0)
    assert on1["minted"] and on1["minted"] == off1["minted"], ("MF-P1", on1["minted"],
                                                               off1["minted"])
    p2 = child({}, 15000, 0, 1)
    assert p2["pruned"] and p2["checked"] and not p2["bad"], ("MF-P2", p2)
    on3, off3 = child({}, 400, 40, 0), child({"TETHER_PREFIX_PRUNE": "0"}, 400, 40, 0)
    assert on3["priced"] > off3["priced"] and on3["cut"] > 0 and off3["cut"] == 0, (
        "MF-P3", on3, off3)
    p4 = {}
    for which in ("demo", "grid"):
        on4 = child({}, 10 ** 6, 10 ** 6, 0, which)
        off4 = child({"TETHER_PREFIX_PRUNE": "0"}, 10 ** 6, 10 ** 6, 0, which)
        assert on4["parks"] == off4["parks"], ("MF-P4", which, [
            (x, y) for x, y in zip(off4["parks"], on4["parks"], strict=False) if x != y][:3],
            len(on4["parks"]), len(off4["parks"]))
        p4[which] = collections.Counter(v for _c, _s, v in off4["parks"])
    assert any(c.get("priced_out_at_depth") for c in p4.values()), ("MF-P4 has no occasion", p4)
    print(f"  MF-P1 budget 15000: minted identical ON and OFF, {on1['minted']}")
    print(f"  MF-P4 ample budget 10^6: park verdicts identical ON and OFF per slot: "
          f"{ {k: dict(v) for k, v in p4.items()} }")
    print(f"  MF-P2 {p2['pruned']} pruned chains seen, {p2['checked']} extensions checked, "
          f"{p2['bad']} affordable; of {p2['pruned_all']} pruned, {p2['unclosed_at_max']} were "
          f"unclosed at max_depth (r1030: they read no novelty)")
    print(f"  MF-P3 walk budget 40, work 400: priced ON {on3['priced']} vs OFF {off3['priced']}; "
          f"pruned at the prefix ON {on3['cut']}")
    print("test_prefix_prune OK")


if __name__ == "__main__":
    main()
