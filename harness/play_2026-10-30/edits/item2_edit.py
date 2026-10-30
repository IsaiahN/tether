def rep(p, old, new):
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (p, old[:70], s.count(old))
    open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))


T = "tether.py"
# one shrink definition, beside arrival()
rep(T, '''    return TOUCHED if series and series[-1] <= 0 else OPEN
''', '''    return TOUCHED if series and series[-1] <= 0 else OPEN


def shrinking(series) -> bool:
    """THE selector's test (M2 item 3, Sec 13.4's *confidently shrinking*): the last MIN_REPEAT + 1
    readings never rise and fall at least once. One definition, read by the selector, the
    goal_series row and -- with the opposite sign -- a held hypothesis's stall (18:40, 19:11)."""
    w = series[-(MIN_REPEAT + 1):] if series else []
    d = [b - a for a, b in zip(w, w[1:], strict=False)]
    return len(w) == MIN_REPEAT + 1 and all(x <= 0 for x in d) and any(x < 0 for x in d)
''')
rep(T, '''            if all(d <= 0 for d in deltas) and any(d < 0 for d in deltas):
''', '''            if shrinking(window):
''')
rep(T, '''                                 if len(ser) >= w and all(d <= 0 for d in _deltas(ser))
                                 and any(d < 0 for d in _deltas(ser))
                                 and (not _ARRIVAL or arrival(ser) == OPEN)),
''', '''                                 if shrinking(ser)
                                 and (not _ARRIVAL or arrival(ser) == OPEN)),
''')
rep(T, '''            # THE TREND (the reviewer 2026-10-20 17:34): the selector's shrink test with the
            # opposite sign -- MIN_REPEAT + 1 consecutive readings with no new low, on every
            # subject -- ends it; the gap budget is only the ceiling
            w = MIN_REPEAT + 1

            def stuck(sl: str) -> bool:
                r = h["reads"].get(sl, [])
                return len(r) >= w and min(r[-w:]) >= min([h["r0s"].get(sl, 1.0)] + r[:-w])
''', '''            # THE TREND (the reviewer 2026-10-20 17:34, 19:11): the selector's own shrinking(),
            # with the opposite sign, over the readings since the hold or the last touch-loss
            # (a touch-loss starts a new approach); shorter than MIN_REPEAT + 1 is not yet
            # judgeable; on every subject; the gap budget is only the ceiling
            def stuck(sl: str) -> bool:
                seg = h["reads"].get(sl, [])[h["seg"].get(sl, 0):]
                return len(seg) >= MIN_REPEAT + 1 and not shrinking(seg)
''')
rep(T, '''                     "r0s": {s: (v if v is not None else 1.0) for s in link["slots"]
                             for v in (self.goal_residual(s, before),)},
                     "reads": {}, "held_unreadable": 0, "acted": Counter()}
''', '''                     "reads": {}, "seg": {}, "touches": 0, "losses": 0,
                     "held_unreadable": 0, "acted": Counter()}
''')
# note_goals: the hypothesis's readings, touches, and the segment a touch-loss starts
rep(T, '''                elif sl in counts:
                    h["reads"].setdefault(sl, []).append(self._res[sl][-1])
''', '''                elif sl in counts:
                    r = h["reads"].setdefault(sl, [])
                    r.append(self._res[sl][-1])
                    if r[-1] <= 0:
                        h["touches"] += 1
                    if any(t[0] == sl for t in touch_lost):
                        h["losses"] += 1
                        h["seg"][sl] = len(r) - 1      # the losing reading opens the approach
''')
rep(T, '''                        held_unreadable=h["held_unreadable"],
''', '''                        held_unreadable=h["held_unreadable"], touches=h["touches"],
                        losses=h["losses"],
''')
rep("test_hyp_trend.py", '''    h.update(steps=0, budget=99, reads={s: list(reads) for s in h["slots"]},
             r0s={s: reads[0] for s in h["slots"]})
''', '''    h.update(steps=0, budget=99, reads={s: list(reads) for s in h["slots"]}, seg={})
''')
print("ok")
