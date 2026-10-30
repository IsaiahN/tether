import sys
for p, old, new in (
    ("test_goal_distance.py",
     '    want = 1.0 - tether.objective_degree(_sat, ag._group("o2.col", st))',
     '    # GQ2b (TETHER_GROUP_MEMBER): the subject is a member of its own scope\n'
     '    scope = ((st["o2.col"],) if tether._GROUP_MEMBER else ()) + ag._group("o2.col", st)\n'
     '    want = 1.0 - tether.objective_degree(_sat, scope)'),
    ("test_goal_link.py",
     '    grp = ag._group(view, state)',
     '    grp = ag._group(view, state)\n'
     '    if tether._GROUP_MEMBER:       # GQ2b: the subject is a member of its own scope\n'
     '        grp = (state[view],) + grp'),
):
    src = open(p, encoding="utf-8").read()
    assert src.count(old) == 1, (p, src.count(old))
    open(p, "w", encoding="utf-8", newline="").write(src.replace(old, new))
print("ok")
