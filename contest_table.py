"""The four-arm table: ?ACTED x CONTEST, one script, separate processes, flag-stamped rows.

**WHY THIS EXISTS, AND IT IS NOT A CONVENIENCE.** Three reversals in one morning on a single
slot, every one of them from comparing a number taken on one build against a number taken on
another: a sixty-cycle total answering a question about post-bind cycles, a CONTEST=1 mint
count read against CONTEST=0 route bins, and a correct alarm withdrawn because the evidence
behind it had been gathered carelessly. `F413`'s lesson one level up -- the population was the
BUILD.

    AN A/B IS ONE SCRIPT WITH ONE FLAG, AND A FOUR-WAY IS ONE SCRIPT WITH TWO.

Each arm runs in its OWN PROCESS because the flags are read at import time, so two arms in one
interpreter are the same arm twice. Each arm ASSERTS ITS OWN FLAGS before stepping, and an arm
whose build cannot supply a flag reports UNAVAILABLE rather than running as its opposite --
which is the treatment-absent failure that makes a null unreadable.

    .venv/Scripts/python.exe contest_table.py                      the table
    .venv/Scripts/python.exe contest_table.py --patched <root>     include the CONTEST arms
    .venv/Scripts/python.exe contest_table.py --child ...          one arm (used by the parent)

REPRODUCE, in full, from a clean tree -- the CONTEST arms need a tree that HAS the flag, and
building it from `git archive` rather than `cp -r` is deliberate: a copy of the working
directory drags `.venv` and takes minutes.

    S=<scratch>
    mkdir -p $S/patched && git archive HEAD | tar -x -C $S/patched
    cp contest_table.py $S/patched/
    (cd $S/patched && git apply $S/contest.patch)
    .venv/Scripts/python.exe contest_table.py --patched $S/patched --panel click_only:5

Without `--patched`, both CONTEST arms print `UNAVAILABLE -- this build has no TETHER_CONTEST`.
THAT IS THE POINT: an arm whose build cannot supply its flag must refuse, never run as its
opposite, or a null from an absent treatment reads exactly like a null from a real one.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

SLOT = "o0.colour"
ARMS = [(0, 0), (1, 0), (0, 1), (1, 1)]     # (acted, contest)


def _rows(world: str, seed: int, cycles: int, acted: int, contest: int) -> list[dict]:
    """One arm, in this process, with the flags already set in the environment."""
    import gamma as G
    import gridworld
    import ledger
    import tether
    import world as _w

    # THE SELF-CHECK. An arm that cannot take its flag must say so, not run as its opposite.
    assert bool(acted) == tether._ACTED_GUARD, f"ACTED flag did not take: want {acted}"
    has = hasattr(tether, "_CONTEST")
    if contest and not has:
        return [{"unavailable": "this build has no TETHER_CONTEST"}]
    if has:
        assert bool(contest) == tether._CONTEST, f"CONTEST flag did not take: want {contest}"

    out: list[dict] = []
    # THE ROUTE BIN, because the first table recorded mint CALLS and not the decision that
    # precedes them -- so a zero could not say whether the slot was refused or never asked.
    bins: dict[int, str] = {}
    real_route = tether.Agent.route

    def route(self, res):
        got = real_route(self, res)
        for slot, b, _fit, _why in got:
            if slot == SLOT:
                bins[self.cycle] = b
        return got

    tether.Agent.route = route
    real_mint = tether.Agent.mint

    def mint(self, slot):
        if slot == SLOT:
            ref = (self._price_ref(slot) if hasattr(self, "_price_ref")
                   else self.gamma.library[self.bound.get(slot, tether.IDN)])
            base = self._accumulated(slot, ref)
            floor = tether.term_bits(1, self.gamma.alphabet)
            inc = self.bound.get(slot)
            out.append({"cycle": self.cycle, "mint": True, "incumbent": inc,
                        "settled": bool(inc) and self.gamma.is_settled(inc),
                        "ref": ref.name, "base": round(base, 3), "floor": round(floor, 3),
                        "enumerates": base > floor})
        return real_mint(self, slot)

    tether.Agent.mint = mint
    try:
        env = _w.bind(gridworld.family(world, seed, cycles))
        gam = G.Gamma(env.atoms(), game="ct")
        ag = tether.Agent(env, gam, tether.Config(max_depth=2), ledger.Ledger())
        for _ in range(cycles):
            ag.step()
    finally:
        tether.Agent.mint = real_mint
        tether.Agent.route = real_route
    for r in out:
        r["bin"] = bins.get(r["cycle"], "-")
    # every cycle's bin, not only the minting ones: the question is what the slot was ASKED
    return [{"bins": bins}, *out]


def _child() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--child", action="store_true")
    p.add_argument("--world", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--cycles", type=int, default=60)
    p.add_argument("--acted", type=int, required=True)
    p.add_argument("--contest", type=int, required=True)
    a = p.parse_args()
    rows = _rows(a.world, a.seed, a.cycles, a.acted, a.contest)
    print(json.dumps({"acted": a.acted, "contest": a.contest, "world": a.world,
                      "seed": a.seed, "rows": rows}))


def _run(root: str, world: str, seed: int, cycles: int, acted: int, contest: int) -> dict:
    env = dict(os.environ, TETHER_ACTED_GUARD=str(acted), TETHER_CONTEST=str(contest),
               PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, os.path.join(root, "contest_table.py"), "--child",
                        "--world", world, "--seed", str(seed), "--cycles", str(cycles),
                        "--acted", str(acted), "--contest", str(contest)],
                       cwd=root, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        return {"acted": acted, "contest": contest, "world": world, "seed": seed,
                "rows": [{"unavailable": (r.stderr.strip().splitlines() or ["?"])[-1][:120]}]}
    return json.loads(r.stdout.strip().splitlines()[-1])


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--patched", default=None, help="a tree with the contest change applied")
    p.add_argument("--cycles", type=int, default=60)
    p.add_argument("--panel", default="click_only:5,click_only:3,buttons:5,buttons:3")
    a, _ = p.parse_known_args()
    here = os.path.dirname(os.path.abspath(__file__))
    fail = 0
    for spec in a.panel.split(","):
        world, seed = spec.split(":")
        for acted, contest in ARMS:
            root = a.patched if (contest and a.patched) else here
            res = _run(root, world, int(seed), a.cycles, acted, contest)
            rows = res["rows"]
            tag = f"acted={acted} contest={contest}"
            head = f"{world}:{seed}  {tag}"
            if rows and "unavailable" in rows[0]:
                print(f"  {head:34s} UNAVAILABLE -- {rows[0]['unavailable']}")
                fail += 1
                continue
            allbins = rows[0].get("bins", {}) if rows and "bins" in rows[0] else {}
            rows = [r for r in rows if "cycle" in r]
            bind = next((r["cycle"] for r in rows if r["incumbent"]), None)
            post = [r for r in rows if bind is not None and r["cycle"] > bind]
            print(f"  {head:34s} mint {len(rows):>3}  bind@{str(bind):>4}  "
                  f"post-bind mint {len(post):>3}  "
                  f"post-bind enumerates {sum(1 for r in post if r['enumerates']):>3}")
            for r in rows:
                if bind is not None and bind - 1 <= r["cycle"] <= bind + 3:
                    print(f"       cyc {r['cycle']:>3} bin {r.get('bin', '-'):>9}"
                          f" base {r['base']:>7} floor {r['floor']:>6}"
                          f" enum {str(r['enumerates']):>5} settled {str(r['settled']):>5}"
                          f"  ref {r['ref'][:28]}")
            # THE BINS FOR THE CYCLES WITH NO MINT ROW -- a slot that is never asked and a
            # slot that is asked and refuses look identical in a mint count, and that
            # ambiguity is what sent five explanations the wrong way.
            if bind is not None and allbins:
                after = {int(c): v for c, v in allbins.items() if int(c) > bind}
                import collections as _c
                print(f"       post-bind route bins: {dict(_c.Counter(after.values()))}")
    return 1 if fail == len(ARMS) * len(a.panel.split(",")) else 0


if __name__ == "__main__":
    if "--child" in sys.argv:
        _child()
    else:
        sys.exit(main())
