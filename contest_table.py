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

THE OUTCOME IS THE SLOT'S FINAL STATE -- standing, the reviewer 2026-10-02. The final bound
term, whether it SETTLED, and how it predicted after the bind. **A MINT COUNT AND A FITTED
`left` ARE MECHANISM READINGS AND NEVER OUTCOMES.** Both misled this seat inside one morning:
`post-bind mint 0` was read as a slot wrongly CLOSED when it was a slot SOLVED, and
`left = 0.000` was read as a good term when it is the signature of a fitted one.

SLOTS ARE CHOSEN PER WORLD-SEED FROM THE DATA, never hardcoded. A hardcoded `o0.colour` made
four of sixteen rows read `mint 0` on buttons seed 5 -- UNINFORMATIVE rows that look exactly
like four arms where nothing happened. A row counts only if something was minted on that slot
in AT LEAST ONE ARM; the rest are reported and counted, never read as negatives.

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


def _rows(world: str, seed: int, cycles: int, acted: int, contest: int) -> dict:
    """One arm, in this process, with the flags already set in the environment.

    PER SLOT, not per hardcoded slot: `minted` is how many terms this arm minted there,
    and the OUTCOME is the final bound term, whether it settled, and how it predicted
    after the bind.
    """
    import collections

    import gamma as G
    import gridworld
    import ledger
    import tether
    import world as _w

    # THE SELF-CHECK. An arm that cannot take its flag must say so, not run as its opposite.
    assert bool(acted) == tether._ACTED_GUARD, f"ACTED flag did not take: want {acted}"
    has = hasattr(tether, "_CONTEST")
    if contest and not has:
        return {"unavailable": "this build has no TETHER_CONTEST"}
    if has:
        assert bool(contest) == tether._CONTEST, f"CONTEST flag did not take: want {contest}"

    minted = collections.Counter()          # slot -> terms minted there
    bound_at: dict[str, int] = {}           # slot -> first cycle it held anything
    correct = collections.Counter()         # slot -> post-bind cycles predicted right
    total = collections.Counter()           # slot -> post-bind cycles seen
    real_mint, real_route = tether.Agent.mint, tether.Agent.route
    before: dict[str, int] = {}

    def mint(self, slot):
        before[slot] = len(self.gamma.library)
        try:
            return real_mint(self, slot)
        finally:
            minted[slot] += len(self.gamma.library) - before[slot]

    def route(self, res):
        got = real_route(self, res)
        for slot, _b, _fit, _why in got:
            if slot in self.bound and slot not in bound_at:
                bound_at[slot] = self.cycle
            if slot in bound_at and self.cycle > bound_at[slot]:
                r = res.get(slot)
                total[slot] += 1
                if r is not None and r.mass == 0.0:
                    correct[slot] += 1
        return got

    tether.Agent.mint, tether.Agent.route = mint, route
    env = _w.bind(gridworld.family(world, seed, cycles))
    gam = G.Gamma(env.atoms(), game="ct")
    ag = tether.Agent(env, gam, tether.Config(max_depth=2), ledger.Ledger())
    try:
        for _ in range(cycles):
            ag.step()
    finally:
        tether.Agent.mint, tether.Agent.route = real_mint, real_route

    out = {}
    for slot in set(minted) | set(bound_at):
        nm = ag.bound.get(slot)
        tot = total[slot]
        out[slot] = {"minted": minted[slot], "bound": nm,
                     "settled": bool(nm) and gam.is_settled(nm),
                     "correct": correct[slot], "total": tot,
                     # SETTLED-AND-CORRECT, fixed before the run: the slot ends on a term
                     # the ground SETTLED -- its own held-out test -- and that term
                     # predicted on every post-bind cycle. A denominator of 0 cannot pass.
                     "win": bool(nm) and gam.is_settled(nm) and tot > 0 and correct[slot] == tot}
    return {"slots": out}


def _child() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--child", action="store_true")
    p.add_argument("--world", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--cycles", type=int, default=60)
    p.add_argument("--acted", type=int, required=True)
    p.add_argument("--contest", type=int, required=True)
    a = p.parse_args()
    # MERGED, NOT NESTED. The parent reads `slots` and `unavailable` at the top level;
    # wrapping them under `rows` made every arm look empty and the whole table read 0/0.
    print(json.dumps({"acted": a.acted, "contest": a.contest, "world": a.world,
                      "seed": a.seed, **_rows(a.world, a.seed, a.cycles,
                                              a.acted, a.contest)}))


def _pinned(root: str) -> str:
    """REFUSE A ROOT THAT IS THE MAIN WORKING TREE, and return the commit it is pinned at.

    **A PANEL IMPORTS ONLY FROM A PINNED SNAPSHOT -- the reviewer, 2026-10-02, after this
    seat contaminated a live panel.** The `buttons` run took its `contest=0` arms from the
    main tree while `gridworld.py` was edited at 15:30:51, so a row finishing after that
    would take `contest=0` from the NEW generator and `contest=1` from the OLD one and print
    the four cells side by side AS ONE WORLD. Two builds inside a single row, invisible in
    the output.

    THE ASYMMETRY IS WHAT MADE IT POSSIBLE: the patched tree WAS pinned and the main tree was
    not, so only half the arms were protected. So this refuses per ARM, not per panel.

    **IT CHECKS WHAT ACTUALLY WENT WRONG -- the resolved path of the modules the agent runs
    on -- not whether the caller passed something that looks like a worktree.** A check that
    merely asks for a path would pass while importing from anywhere.
    """
    main = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(root) == main:
        raise AssertionError(
            f"panel refused: arm would import from the MAIN WORKING TREE ({main}). "
            f"A panel imports only from a pinned worktree -- the tree can move under a "
            f"running arm, and two builds inside one row are invisible in the output.")
    for mod in ("gridworld.py", "tether.py"):
        if not os.path.exists(os.path.join(root, mod)):
            raise AssertionError(f"panel refused: {root} has no {mod} -- it is not a snapshot")
    r = subprocess.run(["git", "-C", root, "rev-parse", "--short", "HEAD"],
                       capture_output=True, text=True)
    pin = r.stdout.strip()
    # **AND AN UNPINNED SNAPSHOT IS REFUSED TOO, which the first version of this guard did
    # not do.** A `git archive` extract cannot move under a run -- nothing writes to it --
    # so it satisfies half the rule and fails the other half: IT HAS NO COMMIT TO RECORD,
    # and a row stamped "unpinned" is exactly the untraceable table the rule exists to
    # prevent. Caught by the guard's own accept-path control returning 'unpinned' instead
    # of a hash.
    if not pin:
        raise AssertionError(
            f"panel refused: {root} is not a git worktree, so no commit can be recorded "
            f"for its rows. Create it with `git worktree add <path> <commit>`.")
    # **AND A DIRTY WORKTREE IS REFUSED, WHICH IS THE SAME FAILURE ONE STEP SUBTLER.** It
    # reports a commit and runs something else, so the row carries A HASH THAT IS A LIE --
    # worse than "unpinned", which at least announces itself. Found while setting up the
    # re-takes: applying the contest patch to a worktree is the obvious way to get a
    # contest arm, and it would have stamped every row with the base commit.
    dirty = subprocess.run(["git", "-C", root, "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        first = "; ".join(dirty.splitlines()[:4])
        raise AssertionError(
            f"panel refused: worktree {root} is DIRTY at {pin}, so its rows would record "
            f"a commit that does not describe the code that ran -- {first}. Commit the "
            f"variant to its own branch and pin a worktree at THAT commit.")
    return pin


def _fits(seeds: int, arms: int, per_arm_s: float, cap_s: float) -> None:
    """REFUSE TO START A JOB WHOSE OWN ESTIMATE EXCEEDS ITS OWN CAP.

    **Twice in one day this seat wrote both numbers itself, minutes apart, and never
    subtracted:** a panel estimated at FOUR TO FIVE HOURS against a cap it had set to TWO,
    and a `P3` run estimated to land at 16:40-17:00 against a cap expiring at 16:40. Both
    were killed mid-run. The arithmetic is one subtraction and being careful is not the fix.
    """
    est = seeds * arms * per_arm_s
    if est > cap_s:
        raise AssertionError(
            f"panel refused: estimate {est / 60:.0f} min ({seeds} seeds x {arms} arms x "
            f"{per_arm_s / 60:.1f} min, MEASURED) exceeds the cap {cap_s / 60:.0f} min. "
            f"Split it into chunks of at most {max(1, int(cap_s // (arms * per_arm_s)))} "
            f"seeds -- do not raise the cap to match a guess.")


def _run(root: str, world: str, seed: int, cycles: int, acted: int, contest: int) -> dict:
    pin = _pinned(root)          # refuses the main working tree, per ARM
    env = dict(os.environ, TETHER_ACTED_GUARD=str(acted), TETHER_CONTEST=str(contest),
               PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, os.path.join(root, "contest_table.py"), "--child",
                        "--world", world, "--seed", str(seed), "--cycles", str(cycles),
                        "--acted", str(acted), "--contest", str(contest)],
                       cwd=root, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        return {"acted": acted, "contest": contest, "world": world, "seed": seed,
                "unavailable": (r.stderr.strip().splitlines() or ["?"])[-1][:120]}
    out = json.loads(r.stdout.strip().splitlines()[-1])
    # EVERY ROW CARRIES THE COMMIT IT RAN ON, so a contaminated table is visible in its own
    # output instead of reconstructible from file mtimes -- which is how the last one was
    # caught, and only because the seat happened to look.
    out["commit"] = pin
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--patched", default=None, help="a tree with the contest change applied")
    p.add_argument("--cycles", type=int, default=60)
    p.add_argument("--worlds", default="click_only,buttons")
    p.add_argument("--seeds", default="0,1,2,3,4,5,6,7,8,9")
    p.add_argument("--per-arm-sec", type=float, default=120.0,
                   help="MEASURED seconds per arm; the launcher refuses if the estimate "
                        "exceeds --cap-sec")
    p.add_argument("--cap-sec", type=float, default=7200.0)
    a, _ = p.parse_known_args()
    here = os.path.dirname(os.path.abspath(__file__))
    seeds = [int(x) for x in a.seeds.split(",")]
    # BOTH REFUSALS FIRE BEFORE A SINGLE ARM RUNS.
    _fits(len(seeds) * len(a.worlds.split(",")), len(ARMS), a.per_arm_sec, a.cap_sec)

    # THE PRE-REGISTERED READING, fixed here in the source before any run.
    # The contest plan proceeds ONLY IF, on informative slot-rows, contest ON ends with
    # MORE slots settled-and-correct than contest OFF in BOTH ?ACTED arms, and never
    # fewer in either. Anything else, it does not proceed.
    tally = dict.fromkeys(ARMS, 0)
    rows_seen = dict.fromkeys(ARMS, 0)
    informative = uninformative = 0
    unavailable = 0

    for world in a.worlds.split(","):
        for seed in seeds:
            per = {}
            for acted, contest in ARMS:
                root = a.patched if (contest and a.patched) else here
                res = _run(root, world, seed, a.cycles, acted, contest)
                per[(acted, contest)] = res
                if "unavailable" in res:
                    unavailable += 1
            if any("unavailable" in r for r in per.values()):
                print(f"  {world}:{seed}  ARM UNAVAILABLE -- world-seed skipped")
                continue
            # SLOTS FROM THE DATA: the union over arms of slots anything was minted on.
            union = set()
            for r in per.values():
                union |= set(r.get("slots", {}))
            for slot in sorted(union):
                # THE INFORMATIVE-ROW CRITERION, written before running: a slot-row
                # counts only if SOMETHING WAS MINTED on it in at least one arm.
                if not any(per[k].get("slots", {}).get(slot, {}).get("minted", 0)
                           for k in ARMS):
                    uninformative += 1
                    continue
                informative += 1
                cells = []
                for k in ARMS:
                    d = per[k].get("slots", {}).get(slot, {})
                    rows_seen[k] += 1
                    if d.get("win"):
                        tally[k] += 1
                    cells.append(f"{'W' if d.get('win') else '.'}"
                                 f"{d.get('correct', 0)}/{d.get('total', 0)}")
                shown = "  ".join(f"{k[0]}{k[1]}:{c:>9s}"
                                  for k, c in zip(ARMS, cells, strict=True))
                print(f"  {world}:{seed:<2} {slot:16s} {shown}")

    print("")
    print(f"  informative slot-rows {informative}   uninformative {uninformative}"
          f"   unavailable arms {unavailable}")
    print("  SETTLED-AND-CORRECT, by arm (acted,contest):")
    for k in ARMS:
        print(f"    acted={k[0]} contest={k[1]}   {tally[k]}/{rows_seen[k]}")
    on0, off0 = tally[(0, 1)], tally[(0, 0)]
    on1, off1 = tally[(1, 1)], tally[(1, 0)]
    proceeds = on0 > off0 and on1 > off1
    print("  PRE-REGISTERED: contest proceeds only if ON > OFF in BOTH ?ACTED arms.")
    print(f"    acted=0  ON {on0} vs OFF {off0}      acted=1  ON {on1} vs OFF {off1}")
    print(f"    -> {'PROCEEDS' if proceeds else 'DOES NOT PROCEED'}")
    return 0


if __name__ == "__main__":
    if "--child" in sys.argv:
        _child()
    else:
        sys.exit(main())
