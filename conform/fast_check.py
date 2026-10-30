"""fast_check: every seat, full green, in a fraction of the time -- and nothing skipped silently.

    python conform/fast_check.py            the pre-commit gate (exit 1 on any non-ok seat)
    python conform/fast_check.py --all      ignore the cache; run every seat (parallel)
    python conform/fast_check.py --explain  print each seat's inputs and fingerprint, run nothing

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
2. WHAT RUNS, RUNS IN PARALLEL across the machine's cores instead of 23 in a row.

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
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import check  # noqa: E402  -- the STAGES table and run_stage are the single source; nothing is copied

CACHE = ROOT / ".git" / "fast_check_cache.json"

# --- what each seat reads (data; conservative) -------------------------------------------------
CODE = ["*.py", "conform/*.py", "conform/*.json", "conform/ITEM", "harness/*.py", "pyproject.toml", "library/*"]
# Read 2026-10-08 at seat-act e50406d: only conform/figures.py opens docs/INDEX.md; composer, condition,
# mapping, self_graded, detectors read docs/library-closure; kaggle_bundle reads docs/example.
DOCS_READ_BY_CODE = ["docs/library-closure/*", "docs/example/*"]
LEDGERS = ["runs/*", "runs/**/*"]
INPUTS = {
    "ruff": CODE, "lint": CODE, "recshape": CODE, "layers": CODE, "arms": CODE, "evalctx": CODE,
    "aim": CODE, "landed": CODE, "census": CODE + DOCS_READ_BY_CODE,
    "figures": ["conform/figures.py", "docs/INDEX.md", "docs/figures/*"],
    "kernel": CODE + DOCS_READ_BY_CODE, "stateful": CODE + DOCS_READ_BY_CODE,
    "shipped": CODE + DOCS_READ_BY_CODE, "fixture": CODE + DOCS_READ_BY_CODE,
    "condition": CODE + DOCS_READ_BY_CODE, "demo": CODE + DOCS_READ_BY_CODE,
    "gate": CODE + DOCS_READ_BY_CODE, "tests": CODE + DOCS_READ_BY_CODE, "m2": CODE + DOCS_READ_BY_CODE,
    "entry": CODE + DOCS_READ_BY_CODE, "percept": CODE + DOCS_READ_BY_CODE,
    "panel": CODE + DOCS_READ_BY_CODE + LEDGERS, "wiring": CODE + DOCS_READ_BY_CODE + LEDGERS,
}
DEFAULT = CODE + DOCS_READ_BY_CODE + LEDGERS   # a seat not listed above reads everything that matters
ALWAYS = ["conform/fast_check.py", "conform/check.py"]
# Seats whose result depends on the WORKING TREE rather than on file contents (aim reads
# `git status --porcelain`): never reused, always run.
NEVER_CACHE = {"aim"}


def index_blobs() -> dict[str, str]:
    """path -> blob id, for every file STAGED in the index (what the commit will contain)."""
    out = subprocess.run(["git", "ls-files", "-s"], cwd=ROOT, capture_output=True, text=True,
                         check=True).stdout
    blobs = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        blobs[path] = meta.split()[1]
    return blobs


def fingerprint(stage: str, blobs: dict[str, str]) -> str:
    pats = INPUTS.get(stage, DEFAULT) + ALWAYS
    h = hashlib.sha256()
    for path in sorted(blobs):
        if any(fnmatch.fnmatch(path, p) for p in pats):
            h.update(f"{path}\0{blobs[path]}\n".encode())
    return h.hexdigest()[:16]


def head() -> str:
    p = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    return p.stdout.strip() or "(none)"


def main(argv: list[str]) -> int:
    blobs = index_blobs()
    stages = list(check.STAGES)
    fps = {name: fingerprint(name, blobs) for name, *_ in stages}
    if "--explain" in argv:
        for name, *_ in stages:
            print(f"  {name:<9} {fps[name]}  reads {INPUTS.get(name, DEFAULT)}")
        return 0
    cache = {} if "--all" in argv or not CACHE.exists() else json.loads(CACHE.read_text())
    todo, results = [], {}
    for name, cmd, why, needs in stages:
        hit = cache.get(name)
        if hit and name not in NEVER_CACHE and hit["fp"] == fps[name] and hit["status"] == "ok":
            results[name] = ("ok", f"REUSED -- inputs byte-identical to {hit['at']} ({hit['fp']})", why, True)
        else:
            todo.append((name, cmd, why, needs))
    t0 = time.time()
    workers = max(1, (os.cpu_count() or 2))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {name: ex.submit(check.run_stage, cmd, needs) for name, cmd, _why, needs in todo}
        for name, cmd, why, needs in todo:
            status, detail = futs[name].result()
            results[name] = (status, detail, why, False)
            if status == "ok":
                cache[name] = {"fp": fps[name], "status": "ok", "at": head()}
            else:
                cache.pop(name, None)
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
    print(f"\n  {len(stages) - bad}/{len(stages)} seats clean -- {len(todo)} ran in {time.time() - t0:.0f}s "
          f"on {workers} workers, {n_reused} reused on byte-identical inputs")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
