p = "test_hyp_trend.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"


def rep(old, new):
    global s
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (old[:60], s.count(old))
    s = s.replace(old, new)


rep('''    acts = list(ag.actions)
    for a in acts:
        e = ag.iface.table.setdefault(a, {"by_ctx": {}, "n": 0, "delta": {}})
        e["n"] = e["n"] or 4
        for k in [k for k in e["delta"] if k[1] in ("o0.col", "o0.row")]:
            del e["delta"][k]
        e["delta"][((), "o0.col", "x")] = (e["n"], -2 * e["n"])
        if a == acts[-1]:
            e["delta"][((), "o0.row", "x")] = (e["n"], e["n"])
''', '''    acts = list(ag.actions)
    planted = []                       # the agent's own transitions: one press of each action
    for a in acts:
        b, af = dict(before), dict(before)
        af["o0.col"] = b["o0.col"] - 2
        af["o0.row"] = b["o0.row"] + (1 if a == acts[-1] else 0)
        planted.append((b, a, af, None, None))
    ag.trace = planted
''')
rep('''print(json.dumps({''', '''def click():
    # a one-action click board (19:54 (c)): ACTION6 and the platform's RESET, never pressed
    ag = fresh()
    ag.actions = ["ACTION6", "RESET"]
    ag.env.provenance = lambda a: "platform-universal" if a == "RESET" else "declared"
    b0 = ag.env.observe()

    def press(land, drow):
        b, af = dict(b0), dict(b0)
        af["o0.col"] = b["o0.col"] + 1          # +1 on every click, wherever it lands
        af["o0.row"] = b["o0.row"] + drow       # moved only where the click lands on o1
        return (b, "ACTION6", af, None, land)
    ag.trace = [press("o1", 1)]
    one = ag._self_moving("o0.col")
    ag.trace = [press("o1", 1), press("o2", 0), press("o1", 1)]
    return {"one_place": one, "two_places": ag._self_moving("o0.col"),
            "mover_at_one_place": ag._self_moving("o0.row")}


print(json.dumps({''')
rep('''    "t4_on": clock(True), "t4_off": clock(False)}''', '''    "t4_on": clock(True), "t4_off": clock(False), "t5": click()}''')
rep('''    assert r["t4_off"]["open"] > r["t4_on"]["open"], (r["t4_on"], r["t4_off"])
''', '''    assert r["t4_off"]["open"] > r["t4_on"]["open"], (r["t4_on"], r["t4_off"])
    assert r["t5"] == {"one_place": False, "two_places": True, "mover_at_one_place": False}, r["t5"]
''')
rep('''          f"T4 ON {r['t4_on']}, OFF {r['t4_off']})")''', '''          f"T4 ON {r['t4_on']}, OFF {r['t4_off']}; T5 click board {r['t5']})")''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
