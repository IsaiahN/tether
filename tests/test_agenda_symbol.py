"""The agenda card's residual symbol must bind under either spelling.

The 'Describe before you look' card writes `describe(R_s) ...`; the bound symbol in
symbols.BOUND is `R⁺_s`. Before this fix the reader looked only for the canonical spelling, so
every such row carried `sym: null` -- a false record (Fig 1). This locks the truthfulness of that
row. It does NOT claim contact: the `sym` field is written to the ledger and read by nothing in
the decision path; this is a record fix, not a capability change.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.dont_write_bytecode = True

import agenda  # noqa: E402
import symbols  # noqa: E402

_SYM = "R\u207a_s"   # the canonical bound symbol, built without a literal for console safety


class _FakeLed:
    def __init__(self):
        self.rows = []

    def record(self, *_a, **kw):  # noqa: ARG002
        self.rows.append(kw)


class _FakeAg:
    def __init__(self):
        self.cycle = 0
        self._running_step = "PLAN"
        self.led = _FakeLed()


def _row_with(do_sym, value):
    ag = _FakeAg()
    r = agenda.Reader()
    cards = agenda.cards()
    original = cards.get("_test_card")
    cards["_test_card"] = {"asks": ["q"], "do_sym": do_sym}
    res = {"focal": "o0.col", "live_mass": 1.0, "shrinking": False, "slots": ["o0.col"]}
    orig = symbols.evaluate
    symbols.evaluate = lambda *_a, **_kw: value  # noqa: ARG005
    try:
        return r._row(ag, "_test_card", "q", "a", "board", res, "why")
    finally:
        symbols.evaluate = orig
        if original is None:
            cards.pop("_test_card", None)
        else:
            cards["_test_card"] = original


def test_card_spelling_binds():
    """A card do_sym using the card's own `R_s` spelling yields a non-null sym key."""
    row = _row_with("describe(R_s) by effect", 0.75)
    assert row["sym"] is not None, "card spelling R_s was not bound -- silent null record"
    assert _SYM in row["sym"], row["sym"]
    print("card spelling binds: OK")


def test_canonical_spelling_still_binds():
    """The canonical spelling still binds (no regression)."""
    row = _row_with(f"describe({_SYM}) by effect", 0.5)
    assert row["sym"] is not None and _SYM in row["sym"]
    print("canonical spelling binds: OK")


def test_no_symbol_unchanged():
    """A card without any residual symbol yields sym None (unchanged behaviour)."""
    row = _row_with("plain text, no symbol", 0.5)
    assert row["sym"] is None
    print("no-symbol unchanged: OK")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn) and name != "test_gate":
            fn()
            print(f"{name}: OK")
    print("agenda_symbol: OK")
