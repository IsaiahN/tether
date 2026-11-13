#!/usr/bin/env python3
"""general-agent after-grep (reviewer r1639, for D2). Usage, from the repo root:

    SCRUB_USERNAME=<username> python3 -I conform/scrub_check.py <candidate-ref> [<baseline-ref>]

<candidate-ref> is the tree about to be pushed to general-agent; <baseline-ref> defaults to
origin/general-agent. Exit 0 = clean. Exit 1 = a HARD finding (listed). Exit 2 = it could not run
(no candidate, or SCRUB_USERNAME unset: the username is read from the environment so it is never
written into the tree this check guards). The REVIEW list (new files that say "kaggle" in prose,
beyond the baseline's) is printed for a human read and does not fail the check.

HARD (Isaiah 10-21, 10-22, 10-30, 10-31): no Kaggle material (kaggle/, docs/kaggle_export/,
docs/kaggle/, a notebook), no Kaggle username, nothing the agent learned or minted while playing
ARC (lineage or save data, store dumps), no CLAUDE.md or .claude/ tracked, no hardcoded machine
path.
"""
import os
import re
import subprocess
import sys

HARD_PATHS = [
    (re.compile(r"^kaggle/"), "Kaggle material (kaggle/)"),
    (re.compile(r"^docs/kaggle_export/"), "Kaggle material (docs/kaggle_export/)"),
    (re.compile(r"^docs/kaggle/"), "Kaggle material (docs/kaggle/)"),
    (re.compile(r"\.ipynb$"), "a notebook"),
    (re.compile(r"(^|/)CLAUDE\.md$", re.I), "CLAUDE.md tracked"),
    (re.compile(r"(^|/)\.claude/"), ".claude/ tracked"),
    # ARC learning: lineage / save / store DATA (code that implements them is general and stays)
    (re.compile(r"(lineage|saves?|store|kind_store|ak_)[^/]*\.(json|jsonl|pkl|pickle|db|sqlite|npz|gz)$",
                re.I), "ARC learning data (lineage / save / store file)"),
    (re.compile(r"(^|/)(lineage|saves|stores?)/"), "ARC learning data directory"),
]
MACHINE = re.compile(r"C:[/\\]+Users[/\\]+Admin", re.I)


def git(*a: str) -> str:
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


def files(ref: str) -> list[str]:
    return [f for f in git("ls-tree", "-r", "--name-only", ref).splitlines() if f]


def grep_files(ref: str, pattern: str, ci: bool = True) -> set[str]:
    args = ["grep", "-l"] + (["-i"] if ci else []) + ["-E", pattern, ref, "--", "."]
    p = subprocess.run(["git", *args], capture_output=True, text=True)
    return {line.split(":", 1)[1] for line in p.stdout.splitlines() if ":" in line}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    username = os.environ.get("SCRUB_USERNAME", "").strip()
    if not username:
        print("SCRUB_USERNAME is not set: the username check cannot run, so nothing is cleared")
        return 2
    cand = sys.argv[1]
    base = sys.argv[2] if len(sys.argv) > 2 else "origin/general-agent"
    hard: list[str] = []
    for f in files(cand):
        for rx, why in HARD_PATHS:
            if rx.search(f):
                hard.append(f"{why}: {f}")
    for f in sorted(grep_files(cand, re.escape(username))):
        hard.append(f"Kaggle username: {f}")
    for f in sorted(grep_files(cand, MACHINE.pattern)):
        hard.append(f"machine path: {f}")
    gi = subprocess.run(["git", "show", f"{cand}:.gitignore"], capture_output=True,
                        text=True).stdout
    if not re.search(r"^CLAUDE\.md\s*$", gi, re.M):
        hard.append(".gitignore does not list CLAUDE.md")
    review = sorted(grep_files(cand, r"kaggle") - grep_files(base, r"kaggle"))
    print(f"candidate {cand} vs baseline {base}")
    print(f"HARD findings: {len(hard)}")
    for h in hard:
        print("  " + h)
    print(f"REVIEW (new files mentioning 'kaggle' in prose, read before the push): {len(review)}")
    for r in review:
        print("  " + r)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
