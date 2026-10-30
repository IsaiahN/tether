"""4d-x's must-fail (the reviewer 2026-10-22 08:47, 08:54, 09:03): the stream's slice ends at a WIN.

harness/mem_store/e4_stream.py compared terminal() to "win", a word F1b (29d3f59) renamed to ledger.WIN, so a won game
never ended its slice. This drives e4_stream's REAL loop (as tiers_timer.py does: the class patched, then the file
run) in two children, one game, N agent steps, seed 00000000, with arc_world.ArcWorld.terminal answering ledger.WIN
from the agent's K-th step on (so which game the seed puts first does not matter; switch.tsv names it):
  NEW   the file as committed: switch.tsv's row reads steps == K, ending == ledger.WIN
  OLD   the same source with the end check put back to "win" IN MEMORY (the file is not touched): steps == N,
        ending "slice" -- so the test proves the line it guards, and fails if OLD also ends at K
Guards: (a) the OLD patch's target occurs exactly once in the source, or the test is broken, not passed; (b) the
children write only into their throwaway folders: each folder (out, and a fresh empty lineage through the stream's
own --lineage, the cold-start path) received a write, the repo's git status is identical before and after, and the
stream's DEFAULT lineage (read from its argparse) is untouched. The status listing cannot see an EXISTING untracked or
ignored file changed in place (a new file anywhere, or a tracked file changed, does show). The games are not
shipped: on a machine without them the test fails with arc_holdout.missing_game()'s message, as the tests that play
through arc_holdout do.

    python tests/test_stream_win.py
"""
import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import ast
import os
import subprocess
import sys
import tempfile
import time

import arc_holdout
import ledger

sys.dont_write_bytecode = True
STREAM = os.path.join(_repo.ROOT, "harness", "mem_store", "e4_stream.py")
GAMES = os.path.join(_repo.ROOT, "environment_files")
SEED, K, N = "00000000", 2, 4
NEW_LINE = "if end == ledger.WIN:"
OLD_LINE = 'if end == "win":'

CHILD = r"""
import os, sys
repo, out, lin, seed, k, n, mode, stream, new_line, old_line = sys.argv[1:11]
k, n = int(k), int(n)
sys.path.insert(0, repo)
os.chdir(repo)
import arc_world, ledger, tether
seen = {"steps": 0}
_step, _term = tether.Agent.step, arc_world.ArcWorld.terminal
def step(self, *a, **kw):
    r = _step(self, *a, **kw)
    seen["steps"] += 1
    return r
tether.Agent.step = step
arc_world.ArcWorld.terminal = lambda self: ledger.WIN if seen["steps"] >= k else _term(self)
with open(stream, encoding="utf-8") as fh:
    src = fh.read()
if mode == "old":
    hits = src.count(new_line)
    assert hits == 1, f"BROKEN TEST: the end check {new_line!r} occurs {hits} times in e4_stream.py, not once"
    src = src.replace(new_line, old_line)
sys.argv = [stream, repo, out, "--n-games", "1", "--slice-steps", str(n), "--seed", seed, "--lineage", lin]
exec(compile(src, stream, "exec"), {"__name__": "__main__", "__file__": stream})
print("AGENT_STEPS", seen["steps"])
"""


def _default_lineage() -> str | None:
    """e4_stream's own --lineage default, read from its add_argument call (the file runs on import)."""
    with open(STREAM, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    for n in ast.walk(tree):
        if (isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "add_argument" and n.args
                and isinstance(n.args[0], ast.Constant) and n.args[0].value == "--lineage"):
            return next(ast.literal_eval(k.value) for k in n.keywords if k.arg == "default")
    raise AssertionError("e4_stream has no --lineage argument: the guard cannot read its default")


def _snap(d: str) -> dict:
    return {os.path.relpath(os.path.join(r, f), d): (os.stat(os.path.join(r, f)).st_size,
                                                      os.stat(os.path.join(r, f)).st_mtime_ns)
            for r, _, fs in os.walk(d) for f in fs}


def _git_status() -> str:
    return subprocess.run(["git", "-C", _repo.ROOT, "status", "--porcelain", "--untracked-files=all", "--ignored"],
                          capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL).stdout


def _row(out: str) -> dict:
    with open(os.path.join(out, "switch.tsv"), encoding="utf-8") as fh:
        rows = [ln.rstrip("\n").split("\t") for ln in fh if ln.strip() and not ln.startswith("#")]
    assert len(rows) == 1, rows
    r = rows[0]
    return {"game": r[1], "steps": int(r[5]), "ending": r[7]}


def _run(mode: str, tmp: str) -> dict:
    out, lin = os.path.join(tmp, mode, "out"), os.path.join(tmp, mode, "lineage")
    os.makedirs(lin)
    t0 = time.time()
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, _repo.ROOT, out, lin, SEED, str(K), str(N), mode, STREAM,
                        NEW_LINE, OLD_LINE], capture_output=True, text=True, timeout=280,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "OPERATION_MODE": "offline"},
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, (mode, p.returncode, p.stdout[-1500:], p.stderr[-3000:])
    r = _row(out)
    r["agent_steps"] = int(next(x for x in p.stdout.splitlines() if x.startswith("AGENT_STEPS")).split()[1])
    r["lineage_files"] = len(_snap(lin))
    r["wall_s"] = round(time.time() - t0, 1)
    return r


def main() -> None:
    assert os.path.isfile(STREAM), STREAM
    have = sorted(os.listdir(GAMES)) if os.path.isdir(GAMES) else []
    assert len(have) == 25, ("e4_stream plays from the 25 public games; environment_files/ holds "
                             f"{len(have)}", arc_holdout.missing_game("<game>"))
    default = _default_lineage()
    before = (_snap(default) if os.path.isdir(default) else None) if default else None
    status = _git_status()
    with tempfile.TemporaryDirectory() as tmp:
        new, old = _run("new", tmp), _run("old", tmp)
    print(f"  seed {SEED}, K {K}, N {N}, the game that ran: {new['game']}")
    print(f"  NEW {new}")
    print(f"  OLD {old}")
    assert new["game"] == old["game"], (new, old)
    assert new["steps"] == new["agent_steps"] == K and new["ending"] == ledger.WIN, ("NEW did not end at K", new)
    assert old["steps"] == old["agent_steps"] == N and old["ending"] == "slice", (
        "OLD ended early: the test cannot tell the two lines apart", old)
    assert new["lineage_files"] and old["lineage_files"], ("a throwaway lineage got no write", new, old)
    assert _git_status() == status, "the children wrote into the repo"
    if default:
        assert (_snap(default) if os.path.isdir(default) else None) == before, f"the default lineage {default} changed"
    print(f"stream_win: OK (the slice ends at a WIN; the old line does not; the repo unchanged; the stream's "
          f"default lineage is {default!r}{'' if default else ', so none to touch'})")


if __name__ == "__main__":
    main()
