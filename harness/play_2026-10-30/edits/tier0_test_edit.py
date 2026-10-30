p = "test_fit_tier0.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
i = s.index("if tether._FIT_TIER0 and not tether._FIT_TIER0_CHECK and ag._fit_none:")
j = s.index("print(json.dumps(out, default=str))")
new = '''if tether._FIT_TIER0 and not tether._FIT_TIER0_CHECK and ag._fit_none:
    s = sorted(ag._fit_none)[0]
    ag.owed_import.add(s)
    key0 = ag._fit_none[s][0]
    same = ag._fit_key(s, ag.bound.get(s)) == key0
    # (d) a planted term moves every stored slot's key; removed, they stand again
    keys = {sl: ag._fit_key(sl, ag.bound.get(sl)) for sl in ag._fit_none}
    lib = ag.gamma.library
    lib["zz_planted"] = next(iter(lib.values()))
    moved = [sl for sl in keys if ag._fit_key(sl, ag.bound.get(sl)) != keys[sl]]
    del lib["zz_planted"]
    back = all(ag._fit_key(sl, ag.bound.get(sl)) == keys[sl] for sl in keys)
    # (a) route: a held bet skips the fit, a missed one runs it and drops the verdict
    del calls[:]
    ag.route({s: tether.SlotResidual(s, "x", 0, 0, 0.0)})
    held = [c for c in calls if c[1] == s]
    del calls[:]
    ag.route({s: tether.SlotResidual(s, "x", 0, 1, 3.0)})
    missed = [c for c in calls if c[1] == s]
    dropped = s not in ag._fit_none
    # (e) the budget (the reviewer 20:15): a call at an exhausted budget (_lookup not asked) and a
    # call that ends at it (its walk cut) store nothing; a full call stores
    b0, store = tether.STEP_BUDGET, {}
    try:
        for tag, budget in (("owed", ag._spent), ("walk", ag._spent + 1)):
            tether.STEP_BUDGET = budget
            ag._fit_none.pop(s, None)
            ag._fit_tier0(s, ag.bound.get(s))
            store[tag] = s in ag._fit_none
    finally:
        tether.STEP_BUDGET = b0
    ag._spent = 0
    ag._fit_tier0(s, ag.bound.get(s))
    store["full"] = s in ag._fit_none
    out.update(key_same=same, held_calls=len(held), missed_calls=len(missed), dropped=dropped,
               woke=len(moved), of=len(keys), back=back, store=store)
'''
s = s[:i] + new.replace("\n", nl) + s[j:]
s = s.replace('''    assert on["woke"] == on["of"] > 0, on''',
              '''    assert on["woke"] == on["of"] > 0 and on["back"], on
    assert on["store"] == {"owed": False, "walk": False, "full": True}, on["store"]''')
s = s.replace('''f"term woke {on['woke']} of {on['of']})")''',
              '''f"term woke {on['woke']} of {on['of']}; (e) budget-capped calls stored nothing, a "
          f"full call stored)")''')
s = s.replace("  OFF: no tier0 row, and a call per owed slot per step.",
              "  (e) a call at an exhausted step budget, and one whose walk ends at it, store nothing;" + nl
              + "     a full call stores (the reviewer 20:15)." + nl
              + "  OFF: no tier0 row, and a call per owed slot per step.")
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
