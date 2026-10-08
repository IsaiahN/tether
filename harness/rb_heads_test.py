"""Must-fail fixture for rb_heads.one_commit: a mixed-commit table, and a table with a row naming no
commit, are refused; a one-commit table passes. Run: python rb_heads_test.py"""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rb_heads


def table(rows):
    d = tempfile.mkdtemp()
    for g, c in rows.items():
        open(os.path.join(d, g + ".jsonl"), "w").close()
        if c:
            json.dump({"commit": c, "source": "recorded"}, open(os.path.join(d, g + ".head"), "w"))
    return d


def refused(d):
    try:
        rb_heads.one_commit(d)
    except SystemExit as e:
        return "REFUSED" in str(e)
    return False


assert rb_heads.one_commit(table({"ar25": "a" * 40, "vc33": "a" * 40})) == "a" * 40, "one commit refused"
assert refused(table({"ar25": "a" * 40, "vc33": "b" * 40})), "a two-commit table was read"
assert refused(table({"ar25": "a" * 40, "vc33": None})), "a row with no commit was read"
print("rb_heads: 3 checks pass")
