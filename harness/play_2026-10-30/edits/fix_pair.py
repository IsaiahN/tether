import sys
p = sys.argv[1]
src = open(p, encoding="utf-8").read()
def rep(old, new):
    global src
    assert src.count(old) == 1, (old[:70], src.count(old))
    src = src.replace(old, new)
rep('''  must-pass: at its 6th completion (c89) the pair "o0.col == o3.col and o0.row < o3.row" is held;
     re-priced on every later step to c119 (L1), it still pays and stays held;''',
'''  must-pass: at its 6th completion (c89) a zero-error PAIR of the exact tie is the pick (A1_TIES
     decides the member; "o0.col == o3.col and o0.row < o3.row" is one of them, 2026-10-20); that
     named pair, re-priced on every later step to c119 (L1), still pays and stays held;''')
rep('''     wants -- on o0.col and o3.row (the "<" conjunct compiles by the reversed binding) -- whose''',
'''     wants -- on o0.col and o0.row (the "<" conjunct binds on o0.row through `below`; it bound
     reversed on o3.row before that atom existed) -- linked explicitly (the member is A1's), whose''')
rep('''    want = {"o0.col == o3.col", "o0.row < o3.row"}
    assert set(row["pick"].split(" and ")) == want, row''',
'''    assert " and " in row["pick"] and row["cheapest"][0]["if"] == row["pick"], row
    assert row["cheapest"][0]["errors"] == 0, row
    named = tether._Pair((_compiled(ag, "o0.col == o3.col"), _compiled(ag, "o0.row < o3.row")))
    ag._goal_conds = {"test_pair": named}
    ag._goal_text = {"test_pair": "o0.col == o3.col and o0.row < o3.row"}''')
rep('''        lk._reach_hist = ROWS[:C89 + 1]
        lk._goal_condition()
        link = [r["detail"] for r in lk.led.rows() if r["event"] == "goal_condition"][-1]["link"]
        # "o0.row < o3.row" compiles by the REVERSED binding (`above` run on o3.row with o0.row
        # as operand): no atom says "below" on o0's own row. So the conjuncts' subjects are
        # o0.col and o3.row -- recorded as found, for the reviewer's ruling.
        assert link["linked"] and link["slots"] == ["o0.col", "o3.row"], link''',
'''        lk._reach_hist = ROWS[:C89 + 1]
        named = tether._Pair((_compiled(lk, "o0.col == o3.col"), _compiled(lk, "o0.row < o3.row")))
        lk._goal_conds["test_pair"] = named
        link = lk._link_goal("test_pair", named)
        # "o0.row < o3.row" binds on o0.row through `below` (ORDERED -> PRED), so both conjuncts'
        # subjects are o0's own: o0.col and o0.row (2026-10-20; o3.row before `below` existed)
        assert link["linked"] and link["slots"] == ["o0.col", "o0.row"], link''')
rep('''        rr = lk.goal_residual("o3.row", away)
        assert 0 < rr <= 1 and lk.goal_residual("o3.row", home) == 0.0, rr
        tc = lk._goal_target("o0.col", away)
        tr = lk._goal_target("o3.row", away)''',
'''        rr = lk.goal_residual("o0.row", away)
        assert 0 < rr <= 1 and lk.goal_residual("o0.row", home) == 0.0, rr
        tc = lk._goal_target("o0.col", away)
        tr = lk._goal_target("o0.row", away)''')
rep('''        print(f"      objective targets: o0.col -> {tc} (o3's column); o3.row -> {tr} (a target "
              f"for o3's row, which the avatar does not control) -- FOR RULING")''',
'''        print(f"      objective targets: o0.col -> {tc} (o3's column); o0.row -> {tr} (above "
              f"o3's row, on the avatar's own row)")''')
rep('''        key = next(iter(lk._goal_conds))
        assert lk._release_link(key) and not ({"o0.col", "o3.row"} & set(lk.wants))''',
'''        key = "test_pair"
        assert lk._release_link(key) and not ({"o0.col", "o0.row"} & set(lk.wants))''')
rep('''        oc.wants.pop("o0.col", None)
        oc.wants["o3.row"] = "some . other<want>"
        oc._reach_hist = ROWS[:C89 + 1]
        oc._goal_condition()
        ol = [r["detail"] for r in oc.led.rows() if r["event"] == "goal_condition"][-1]["link"]
        assert ol["linked"] is False and "o0.col" not in oc.wants, ol
        assert oc.gamma.book.get("goal_link_refused_wants") == 1
        print("  (b) refusal: o3.row already wanted, so the WHOLE pair is refused (no half-link), "
              "counted once")''',
'''        oc.wants.pop("o0.col", None)
        oc.wants["o0.row"] = "some . other<want>"
        refused0 = oc.gamma.book.get("goal_link_refused_wants", 0)
        named_oc = tether._Pair((_compiled(oc, "o0.col == o3.col"),
                                 _compiled(oc, "o0.row < o3.row")))
        ol = oc._link_goal("test_pair", named_oc)
        assert ol["linked"] is False and "o0.col" not in oc.wants, ol
        assert oc.gamma.book.get("goal_link_refused_wants") == refused0 + 1
        print("  (b) refusal: o0.row already wanted, so the WHOLE pair is refused (no half-link), "
              "counted once")''')
open(p, "w", encoding="utf-8", newline="").write(src)
print("ok")
