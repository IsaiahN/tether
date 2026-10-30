"""r348: every batch arm's OFF identity through tests/_batch.off_env. argv: worktree root."""
import sys
sys.dont_write_bytecode = True
W = sys.argv[1].rstrip("/") + "/tests/"
edits = {
 "test_arrival_gap.py": [('        cur = norm(child(root, kind, k, {"TETHER_ARRIVAL_GAP": "0"})["rows"])\n',
                          '        cur = norm(child(root, kind, k, off_env("TETHER_ARRIVAL_GAP"))["rows"])\n')],
 "test_settle_pred.py": [('    cur = norm(child(root, w, {"TETHER_SETTLE_PRED": "0"}))\n',
                          '    cur = norm(child(root, w, off_env("TETHER_SETTLE_PRED")))\n')],
 "test_kind_save.py": [('    cur = child(root, {"TETHER_KIND_SAVE": "0"})\n',
                        '    cur = child(root, off_env("TETHER_KIND_SAVE"))\n')],
 "test_instance_retire.py": [('            cur = norm(child(root, mode, {"TETHER_INSTANCE_RETIRE": "0"})["rows"])\n',
                              '            cur = norm(child(root, mode, off_env("TETHER_INSTANCE_RETIRE"))["rows"])\n')],
 "test_divide.py": [('    cur = norm(_child(root, w, {arm: "0"}))\n',
                     '    cur = norm(_child(root, w, off_env(arm)))\n')],
 "test_ask.py": [('    # the batch\'s later arms off too (1d), so the tree reads as it stood before this arm\n'
                  '    cur = _norm(_child(root, w, {"TETHER_ASK": "0", "TETHER_OWED_REJUDGE": "0"}))\n',
                  '    cur = _norm(_child(root, w, off_env("TETHER_ASK")))      # and every later batch arm\n')],
 "test_owed_rejudge.py": [('    cur = _norm(_child(root, w, {"TETHER_OWED_REJUDGE": "0"}))\n',
                           '    cur = _norm(_child(root, w, off_env("TETHER_OWED_REJUDGE")))\n')],
}
for f, pairs in edits.items():
    p = W + f
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (f, a[:70], s.count(a))
        s = s.replace(a, b)
    imp = "import _repo  # noqa: F401"
    i = s.index(imp)
    j = s.index(nl, i) + len(nl)
    s = s[:j] + "from _batch import off_env  # noqa: E402  the batch's arms (r348)" + nl + s[j:]
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
