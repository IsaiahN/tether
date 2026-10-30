p = "test_fit_tier0.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
old = '''    b0, store = tether.STEP_BUDGET, {}
    try:
        for tag, budget in (("owed", ag._spent), ("walk", ag._spent + 1)):
            tether.STEP_BUDGET = budget
            ag._fit_none.pop(s, None)
            ag._fit_tier0(s, ag.bound.get(s))
            store[tag] = s in ag._fit_none
    finally:
        tether.STEP_BUDGET = b0
'''.replace("\n", nl)
new = '''    b0, store = tether.STEP_BUDGET, {}
    try:
        tether.STEP_BUDGET = ag._spent                    # spent before the call: not asked
        ag._fit_none.pop(s, None)
        ag._fit_tier0(s, ag.bound.get(s))
        store["owed"] = s in ag._fit_none
    finally:
        tether.STEP_BUDGET = b0
    ag._spent = 0
    ag._lookup = lambda _s, _h: setattr(ag, "_spent", ag._spent + tether.STEP_BUDGET)
    ag._fit_none.pop(s, None)
    ag._fit_tier0(s, ag.bound.get(s))                     # asked, and its walk ran to the budget
    store["walk"] = s in ag._fit_none
    del ag._lookup
'''.replace("\n", nl)
assert s.count(old) == 1
s = s.replace(old, new)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
