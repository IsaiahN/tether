import sys
p = sys.argv[1]
src = open(p, encoding="utf-8").read()
def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (old[:60], src.count(old))
    src = src.replace(old, new)
rep('''        ag = _agent()
        ag.wants.pop(SLOT, None)
        ag._want_terms.pop(SLOT, None)
        if occupied:
            ag.wants[SLOT] = occupied''',
'''        ag = _agent()
        # BOTH spellings of the pick tie ("o0.col == o1.col" / "o1.col == o0.col": A1_TIES decides
        # the member), so both slots are cleared -- or both occupied -- and the subject is read
        # from the link (2026-10-20)
        for sl in PAIR:
            ag.wants.pop(sl, None)
            ag._want_terms.pop(sl, None)
            if occupied:
                ag.wants[sl] = occupied''')
rep('SLOT = "o0.col"\n', 'SLOT = "o0.col"     # the docstring\'s spelling; either of PAIR is the subject\nPAIR = ("o0.col", "o1.col")\n')
rep('''    link = row["link"]
    assert link["linked"] and link["slots"] == [SLOT] and ag.wants[SLOT] == link["want"][0], row''',
'''    link = row["link"]
    assert link["linked"] and len(link["slots"]) == 1 and link["slots"][0] in PAIR, row
    SLOT = link["slots"][0]
    P = next(sl for sl in PAIR if sl != SLOT)
    assert ag.wants[SLOT] == link["want"][0], row''')
rep('''    on = dict(state, **{"o0.col": state["o1.col"]})
    off_st = dict(state, **{"o0.col": (state["o1.col"] + 1) % 5})''',
'''    on = dict(state, **{SLOT: state[P]})
    off_st = dict(state, **{SLOT: (state[P] + 1) % 5})''')
rep('''    off_r = abs(off_st["o0.col"] - off_st["o1.col"]) / (ag.alphabet[SLOT] - 1)''',
'''    off_r = abs(off_st[SLOT] - off_st[P]) / (ag.alphabet[SLOT] - 1)''')
rep('''    expect = 1 - sum(1 for v in grp if v == state["o1.col"]) / len(grp)''',
'''    expect = 1 - sum(1 for v in grp if v == state[P]) / len(grp)''')
rep('''    assert occ.wants[SLOT] == "some . other<want>" and row["link"]["linked"] is False, row''',
'''    assert all(occ.wants[sl] == "some . other<want>" for sl in PAIR), row
    assert row["link"]["linked"] is False, row''')
rep('''        assert not occ._goal_conds and occ.wants[SLOT] == "some . other<want>"''',
'''        assert not occ._goal_conds and all(occ.wants[sl] == "some . other<want>" for sl in PAIR)''')
open(p, "w", encoding="utf-8", newline="").write(src)
print("ok")
