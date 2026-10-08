"""ONE COMMIT PER TABLE (the reviewer 2026-10-08 10:31Z). A run's tree is pinned to one commit; each
game's commit sits beside its ledger as <game>.head; a table whose rows name more than one commit,
or a row naming none, is refused -- never read."""
import json
import os
import subprocess


def tree_head(tree: str) -> str:
    return subprocess.run(["git", "-C", tree, "rev-parse", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()


def tree_dirty(tree: str) -> str:
    return subprocess.run(["git", "-C", tree, "status", "--porcelain", "--untracked-files=no"],
                          capture_output=True, text=True, check=True).stdout.strip()


def refuse_unless_pinned(tree: str, commit: str) -> None:
    head, dirty = tree_head(tree), tree_dirty(tree)
    if head != commit or dirty:
        raise SystemExit(f"REFUSED: tree {tree} is at {head[:7]}"
                         f"{' with uncommitted changes' if dirty else ''}, pinned {commit[:7]}")


def one_commit(outdir: str) -> str:
    """The table's single commit, or SystemExit naming every disagreeing row."""
    games = sorted(f[:-6] for f in os.listdir(outdir) if f.endswith(".jsonl"))
    by = {}
    for g in games:
        p = os.path.join(outdir, g + ".head")
        by[g] = None
        if os.path.exists(p):
            with open(p) as fh:
                by[g] = json.load(fh)["commit"]
    missing = [g for g, c in by.items() if c is None]
    commits = sorted({c for c in by.values() if c})
    if missing or len(commits) != 1:
        raise SystemExit(f"REFUSED: {outdir} -- {len(commits)} commits "
                         f"{[c[:7] for c in commits]}, rows with no commit {missing}")
    return commits[0]
