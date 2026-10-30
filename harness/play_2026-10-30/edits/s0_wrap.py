import sys
tree = sys.argv[1]


def edit(path, old, new):
    s = open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (path, s.count(old))
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


edit(tree + "/tether.py",
     "# S0 (the reviewer 2026-10-20 18:18): at the goal-hypothesis site only, a tie group is drawn one hash\n"
     "# per candidate (frontier.draw_order) and route-checked in that order, stopping at the first\n",
     "# S0 (the reviewer 2026-10-20 18:18): at the goal-hypothesis site only, a tie group is drawn one\n"
     "# hash per candidate (frontier.draw_order) and route-checked in that order, stopping at the first\n")
s = open(tree + "/conform/arms.py", encoding="utf-8", newline="").read()
i = s.index('    "TETHER_HYP_DRAW": ')
j = s.index('    "TETHER_G1_SUFFIX": ')
nl = "\r\n" if "\r\n" in s else "\n"
row = nl.join([
    '    "TETHER_HYP_DRAW": "S0 (the reviewer 2026-10-20 18:18): at the goal-hypothesis site only, "',
    '                       "an exact tie\'s draw is one hash per candidate (frontier.draw_order) "',
    '                       "and routes are checked in that order, stopping at the first "',
    '                       "routable -- the same pick as checking all under that draw; the "',
    '                       "proposal row carries its wall time and its checks. OFF: every tied "',
    '                       "member route-checked, the draw a hash of the routable pool "',
    '                       "(6fe24e2). default ON",']) + nl
open(tree + "/conform/arms.py", "w", encoding="utf-8", newline="").write(s[:i] + row + s[j:])
print("ok")
