import sys
tree = sys.argv[1]


def edit(path, old, new):
    s = open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (path, s.count(old))
    assert new not in s
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


edit(tree + "/frontier.py",
     '    return pool[int.from_bytes(h, "big") % len(pool)], "draw", front\n',
     '    return pool[int.from_bytes(h, "big") % len(pool)], "draw", front\n'
     '\n\n'
     'def draw_order(names: list, key: str, seed: str | None = None) -> list:\n'
     '    """S0 (the reviewer 2026-10-20 18:18): the recorded draw, one hash PER NAME, lowest first.\n'
     '    The first of these that qualifies is a uniform draw over the qualifying pool -- the same\n'
     '    distribution as frontier_pick\'s hash of the pool -- so a caller can stop at the first that\n'
     '    qualifies and read the same pick as checking all. Never a name, a text or a position."""\n'
     '    s = SEED if seed is None else seed\n'
     '    return sorted(names, key=lambda n: (hashlib.blake2b(f"{s}:{key}:{n!r}".encode(),\n'
     '                                                        digest_size=8).digest(), repr(n)))\n')
edit(tree + "/conform/arms.py",
     '    "TETHER_G1_SUFFIX": ',
     '    "TETHER_HYP_DRAW": "S0 (the reviewer 2026-10-20 18:18): at the goal-hypothesis site only, '
     'an exact tie\'s draw is one hash per candidate (frontier.draw_order) and routes are checked "\n'
     '                       "in that order, stopping at the first routable -- the same pick as checking "\n'
     '                       "all under that draw; the proposal row carries its wall time and its checks. "\n'
     '                       "OFF: every tied member route-checked, the draw a hash of the routable pool "\n'
     '                       "(6fe24e2). default ON",\n'
     '    "TETHER_G1_SUFFIX": ')
print("ok")
