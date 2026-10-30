import sys

P = sys.argv[1]
s = open(P, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
t = s.replace("\r\n", "\n")


def sub(old, new, count=1):
    global t
    assert t.count(old) == count, (t.count(old), old[:60])
    t = t.replace(old, new)


sub("import sys\n\nimport _repo", "import contextlib\nimport sys\n\nimport _repo")
sub('''def _evidence(ag: tether.Agent, rows: list) -> dict[int, bool]:''',
    '''@contextlib.contextmanager
def _prev_offer(on: bool):
    """The window's own order is checked with PREV_OFFER OFF, where the window also owns ~1; with
    it ON, ~1 is PREV_OFFER's and the window offers j >= 2 (the reviewer 2026-10-26 09:43)."""
    keep = tether._PREV_OFFER
    tether._PREV_OFFER = on
    try:
        yield
    finally:
        tether._PREV_OFFER = keep


def _evidence(ag: tether.Agent, rows: list) -> dict[int, bool]:''')
sub('''    got = [int(b.rsplit("~", 1)[1]) for b in ag._window_lags(SLOT, rows)]
    assert sorted(got) == [j for j in sorted(ev) if ev[j]], (got, ev)''',
    '''    with _prev_offer(False):
        got = [int(b.rsplit("~", 1)[1]) for b in ag._window_lags(SLOT, rows)]
    assert sorted(got) == [j for j in sorted(ev) if ev[j]], (got, ev)''')
sub('''    _given_evidence(ag, set(range(1, 10)))
    got = ag._window_lags(SLOT, rows)
    assert got == [f"{SLOT}~1"], got
    ag.trace = []
    ag._trace_pos = None
    assert ag._window_lags(SLOT, []) == []''',
    '''    _given_evidence(ag, set(range(1, 10)))
    with _prev_offer(False):
        got = ag._window_lags(SLOT, rows)
        assert got == [f"{SLOT}~1"], got
        ag.trace = []
        ag._trace_pos = None
        assert ag._window_lags(SLOT, []) == []''')
sub('''    _given_evidence(ag, {1, 2, 3})
    got = [int(b.rsplit("~", 1)[1]) for b in ag._window_lags(SLOT, rows)]
    assert got == [j, 1, 2], got''',
    '''    _given_evidence(ag, {1, 2, 3})
    with _prev_offer(False):
        got = [int(b.rsplit("~", 1)[1]) for b in ag._window_lags(SLOT, rows)]
    assert got == [j, 1, 2], got
    with _prev_offer(True):                    # ~1 is PREV_OFFER's: the window never offers it
        got = [int(b.rsplit("~", 1)[1]) for b in ag._window_lags(SLOT, rows)]
    assert got == [j, 2], got''')
sub('''    _given_evidence(ag, {1, 2, 3, 4})
    got = [int(b.rsplit("~", 1)[1]) for b in ag._window_lags(SLOT, rows)]
    assert got == [4, 2, 1, 3], got''',
    '''    _given_evidence(ag, {1, 2, 3, 4})
    with _prev_offer(False):
        got = [int(b.rsplit("~", 1)[1]) for b in ag._window_lags(SLOT, rows)]
    assert got == [4, 2, 1, 3], got''')
sub('''def _mint_window(seq: list[int], budget: int) -> tuple[dict, str]:''',
    '''def check_prev_offer_keeps_its_1_under_the_window() -> None:
    """The reviewer 2026-10-26 09:43: turning the window ON must not cut PREV_OFFER's ~1. On a
    stepped agent, every slot's binding list with the window ON is the OFF list (which holds the
    slot's ~1 once, in its own place) with only lags j >= 2 after it."""
    ag = _agent()
    for _ in range(12):
        ag.step()
    keep = tether._WINDOW
    try:
        with _prev_offer(True):
            seen = 0
            for slot in ag.slots:
                robs = ag._residual_obs(slot, ag.gamma.library[ag.bound.get(slot, tether.IDN)],
                                        ag.history(slot))
                tether._WINDOW = False
                off = ag._bindings(slot, robs)
                tether._WINDOW = True
                on = ag._bindings(slot, robs)
                assert on[:len(off)] == off, (slot, off, on)
                assert on.count(slot + tether.PREV) == 1, (slot, on)
                assert all((tether.lag_of(b) or ("", 0))[1] >= 2 for b in on[len(off):]), on
                seen += (slot + tether.PREV) in off
            assert seen, "no slot held its ~1: the guard checked nothing"
    finally:
        tether._WINDOW = keep


def _mint_window(seq: list[int], budget: int) -> tuple[dict, str]:''')
open(P, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
print("ok", repr(nl))
