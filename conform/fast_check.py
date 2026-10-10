"""fast_check: every seat, full green, in a fraction of the time -- and nothing skipped silently.

    python conform/fast_check.py            the pre-commit gate (exit 1 on any non-ok seat)
    python conform/fast_check.py --all      ignore the cache; run every seat (parallel)
    python conform/fast_check.py --explain  print each seat's inputs and fingerprint, run nothing
    python conform/fast_check.py --index-only  certify the INDEX even where the working copy differs

WHY (Isaiah, 2026-10-08): the 23-seat hook took ~20 minutes, so the seat routed around it with
worktrees, branches and an unreviewed backlog. The 2026-09-30 rule stands -- a commit needs
every seat green -- and this keeps it, two ways:

1. A SEAT'S RESULT IS A FUNCTION OF ITS INPUTS. Each seat declares the files it reads (INPUTS,
   data below, conservative: when unsure, more files). Its fingerprint is the git BLOB ids of
   those files IN THE INDEX -- the exact tree being committed, not the working copy. If a seat
   passed before on a byte-identical fingerprint, that pass is reused and SAID SO, with the
   fingerprint and the commit it was earned on. Anything else runs. A records-only commit
   (docs/*.md) re-runs only the seats that read docs. Figure 12: "where the arrangement is
   recorded, re-deriving it is a lookup"; Figure 6: "What is reachable is derived".
2. WHAT RUNS, RUNS IN PARALLEL across the machine's cores instead of 23 in a row -- EXCEPT where
   one seat writes a file another reads (v5 correction; the seat found it, 2026-10-08 12:39 CDT:
   `demo` writes runs/demo.jsonl and `gate` reads it). Those pairs keep check.py's sequence:
   RUN_WRITES / RUN_READS below are data, every overlap becomes an ordering edge in the order
   check.STAGES lists the two seats, and a reader that reads what an EARLIER seat writes in the
   same run is cached and run AS ONE UNIT with that writer (if either misses, both run).
3. FILES THE INDEX CANNOT SEE ARE HASHED FROM DISK (v5 correction, the reviewer's own defect):
   runs/ is git-ignored, so a ledger pattern in INPUTS never matched a blob and `wiring`/`panel`
   could reuse a pass over ledgers that had changed. Run files are now fingerprinted by content,
   read at the start of the check, before any seat rewrites them.

Only an `ok` is ever reused. FAIL, INCOMPLETE and DID-NOT-RUN are never cached, so a seat that
did not pass is asked again every time. `--all` and a changed `fast_check.py`/`check.py`
invalidate everything.

Whether a reused pass counts as "full green" under the 2026-09-30 rule is ISAIAH'S RULING; this
file states the case and prints every reuse so the answer can be checked commit by commit.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import check  # noqa: E402  -- the STAGES table and run_stage are the single source; nothing is copied
import throttle  # noqa: E402

# THE GIT DIR IS ASKED, NOT ASSUMED: in a worktree `.git` is a file and the dir is
# .git/worktrees/<name>/, so each tree keeps its own fingerprints (their blobs differ).
_GIT_DIR = subprocess.run(["git", "rev-parse", "--absolute-git-dir"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
CACHE = Path(_GIT_DIR) / "fast_check_cache.json"

# --- what each seat reads (data; conservative) -------------------------------------------------
CODE = [
    "*.py",
    "conform/*.py",
    "conform/*.json",
    "conform/ITEM",
    "harness/*.py",
    "pyproject.toml",
    "library/*",
]
# Read 2026-10-08 at seat-act e50406d: only conform/figures.py opens docs/INDEX.md; composer,
# condition, mapping, self_graded, detectors read docs/library-closure; kaggle_bundle reads
# docs/example.
DOCS_READ_BY_CODE = ["docs/library-closure/*", "docs/example/*"]
LEDGERS = ["runs/*", "runs/**/*"]
INPUTS = {
    "ruff": CODE,
    "lint": CODE,
    "recshape": CODE,
    "layers": CODE,
    "arms": CODE,
    "evalctx": CODE,
    "aim": CODE,
    "landed": CODE,
    "census": CODE + DOCS_READ_BY_CODE,
    "figures": ["conform/figures.py", "docs/INDEX.md", "docs/figures/*"],
    "kernel": CODE + DOCS_READ_BY_CODE,
    "stateful": CODE + DOCS_READ_BY_CODE,
    "shipped": CODE + DOCS_READ_BY_CODE,
    "fixture": CODE + DOCS_READ_BY_CODE,
    "condition": CODE + DOCS_READ_BY_CODE,
    "demo": CODE + DOCS_READ_BY_CODE,
    "gate": CODE + DOCS_READ_BY_CODE,
    "tests": CODE + DOCS_READ_BY_CODE,
    "m2": CODE + DOCS_READ_BY_CODE,
    "entry": CODE + DOCS_READ_BY_CODE,
    "percept": CODE + DOCS_READ_BY_CODE,
    # the run files these two read are declared in RUN_READS below (exact), not as all of runs/
    "panel": CODE + DOCS_READ_BY_CODE,
    "wiring": CODE + DOCS_READ_BY_CODE,
}
DEFAULT = (
    CODE + DOCS_READ_BY_CODE + LEDGERS
)  # a seat not listed above reads everything that matters
ALWAYS = ["conform/fast_check.py", "conform/check.py"]
# WHO WRITES AND WHO READS A RUN FILE IN THE SAME CHECK (read 2026-10-08 at arc-agent 8783717 by
# grep; THE SEAT CONFIRMS by reading every seat's writes before this table is called complete).
# An overlap is an ordering edge in check.STAGES order; nothing else is serialised.
RUN_WRITES = {"demo": ["runs/demo.jsonl"], "fixture": ["runs/fixture-*.jsonl"]}
RUN_READS = {"gate": ["runs/demo.jsonl"], "wiring": ["runs/*.jsonl"], "panel": ["runs/panel/*"]}
# Seats whose result depends on the WORKING TREE rather than on file contents (aim reads
# `git status --porcelain`): never reused, always run.
NEVER_CACHE = {"aim"}


def index_blobs() -> dict[str, str]:
    """path -> blob id, for every file STAGED in the index (what the commit will contain)."""
    out = subprocess.run(
        ["git", "ls-files", "-s"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    blobs = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        blobs[path] = meta.split()[1]
    return blobs


def disk_blobs() -> dict[str, str]:
    """path -> content hash for the git-IGNORED run files (the index cannot see them). Read once,
    at the start, before any seat rewrites them -- the state a reader-before-writer seat reads."""
    out = {}
    runs = ROOT / "runs"
    if runs.exists():
        for f in sorted(runs.rglob("*")):
            if f.is_file():
                out[f.relative_to(ROOT).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()[
                    :16
                ]
    return out


def drift() -> list[str]:
    """Files a seat fingerprints whose WORKING COPY is not what the index holds: tracked files with
    unstaged edits, and untracked files a seat's patterns match. The fingerprint is the INDEX, so
    with any of these a reused pass certifies a tree that is not the one in front of the seats
    (the reviewer 2026-10-09 11:58Z: 17 seats "reused" from HEAD while M4 sat unstaged)."""
    pats = set(ALWAYS) | set(DEFAULT) | {p for v in INPUTS.values() for p in v}

    def git(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True,
                              check=True).stdout.splitlines()
    paths = git("diff", "--name-only") + git("ls-files", "--others", "--exclude-standard")
    return sorted({p for p in paths if any(fnmatch.fnmatch(p, q) for q in pats)})


def own_reads(stage: str, names: list[str]) -> list[str]:
    """The run files a seat reads AS FOUND ON DISK. A file an EARLIER seat writes in this same check
    is not one of them: it is that writer's output, already covered by the writer's fingerprint
    (the two are one unit), and hashing the stale copy would only stop the pair ever caching."""
    pos = {n: i for i, n in enumerate(names)}
    earlier = [w for w in RUN_WRITES if w in pos and stage in pos and pos[w] < pos[stage]]
    return [
        r
        for r in RUN_READS.get(stage, [])
        if not any(_overlap(RUN_WRITES[w], [r]) for w in earlier)
    ]


def fingerprint(stage: str, blobs: dict[str, str], names: list[str] | None = None) -> str:
    pats = INPUTS.get(stage, DEFAULT) + ALWAYS + own_reads(stage, names or [])
    h = hashlib.sha256()
    for path in sorted(blobs):
        if any(fnmatch.fnmatch(path, p) for p in pats):
            h.update(f"{path}\0{blobs[path]}\n".encode())
    return h.hexdigest()[:16]


def _overlap(writes: list[str], reads: list[str]) -> bool:
    return any(fnmatch.fnmatch(w, r) or fnmatch.fnmatch(r, w) for w in writes for r in reads)


def ordering(names: list[str]) -> tuple[dict[str, set[str]], list[set[str]]]:
    """(after, units). `after[b]` = seats b must wait for; a UNIT = a writer and every later seat
    that reads what it writes in this run (cached and run together)."""
    pos = {n: i for i, n in enumerate(names)}
    after: dict[str, set[str]] = {n: set() for n in names}
    unit_of: dict[str, set[str]] = {n: {n} for n in names}
    for w, wp in RUN_WRITES.items():
        for r, rp in RUN_READS.items():
            if w == r or w not in pos or r not in pos or not _overlap(wp, rp):
                continue
            first, second = (w, r) if pos[w] < pos[r] else (r, w)
            after[second].add(first)
            if first == w:  # the reader reads THIS run's write: one unit
                merged = unit_of[w] | unit_of[r]
                for n in merged:
                    unit_of[n] = merged
    units = []
    for u in unit_of.values():
        if u not in units:
            units.append(u)
    return after, units


def head() -> str:
    p = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True
    )
    return p.stdout.strip() or "(none)"


def main(argv: list[str]) -> int:
    index_only = "--index-only" in argv
    if not index_only and "--explain" not in argv:
        moved = drift()
        if moved:
            print("  REFUSED -- the working copy differs from the index on files seats read, so")
            print("  a reused pass would certify the index, not this tree. Stage them, or run")
            print("  --index-only to certify the index on purpose:")
            for f in moved:
                print(f"    {f}")
            return 1
    blobs = {**index_blobs(), **disk_blobs()}
    stages = list(check.STAGES)
    names = [name for name, *_ in stages]
    fps = {name: fingerprint(name, blobs, names) for name in names}
    after, units = ordering(names)
    if "--explain" in argv:
        for name in names:
            print(
                f"  {name:<9} {fps[name]}  reads "
                f"{INPUTS.get(name, DEFAULT) + own_reads(name, names)}"
                + (f"  after {sorted(after[name])}" if after[name] else "")
            )
        return 0
    cache = {} if "--all" in argv or not CACHE.exists() else json.loads(CACHE.read_text())

    def hit(name):
        h = cache.get(name)
        return bool(h) and name not in NEVER_CACHE and h["fp"] == fps[name] and h["status"] == "ok"

    run_set = set()
    for u in units:  # a unit is reused only if EVERY member is
        if not all(hit(n) for n in u):
            run_set |= u
    results = {}
    for name in names:
        if name not in run_set:
            h = cache[name]
            results[name] = (
                "ok",
                f"REUSED -- inputs byte-identical to {h['at']} ({h['fp']})",
                None,
                True,
            )
    spec = {name: (cmd, why, needs) for name, cmd, why, needs in stages}
    t0 = time.time()
    workers = throttle.CAP          # Isaiah 2026-10-09 21:16 CDT: never peg his machine
    pending, running = [n for n in names if n in run_set], {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        while pending or running:
            for n in list(pending):  # submit every seat whose predecessors are done
                if all(d in results or d not in run_set for d in after[n]):
                    if not throttle.may_start(len(running)):
                        break
                    cmd, _why, needs = spec[n]
                    running[ex.submit(check.run_stage, cmd, needs)] = n
                    pending.remove(n)
            if not running:
                time.sleep(throttle.POLL_S)
                continue
            done, _ = wait(running, return_when=FIRST_COMPLETED)
            for f in done:
                n = running.pop(f)
                status, detail = f.result()
                results[n] = (status, detail, spec[n][1], False)
                if status == "ok":
                    cache[n] = {"fp": fps[n], "status": "ok", "at": head()}
                else:
                    cache.pop(n, None)
    todo = run_set
    CACHE.write_text(json.dumps(cache, indent=1))
    bad = 0
    for name, *_ in stages:
        status, detail, why, reused = results[name]
        print(f"  {name:<9} {status}{'  (reused)' if reused else ''}")
        if status == "FAIL":
            print(f"            {why}")
        if detail:
            print(f"            {detail}")
        bad += status != "ok"
    n_reused = sum(1 for r in results.values() if r[3])
    print(
        f"\n  {len(stages) - bad}/{len(stages)} seats clean -- {len(todo)} ran in "
        f"{time.time() - t0:.0f}s "
        f"on {workers} workers, {n_reused} reused on byte-identical inputs"
        + ("  -- INDEX ONLY" if index_only else "")
    )
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
