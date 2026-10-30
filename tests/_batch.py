"""THE BATCH'S ARMS IN COMMIT ORDER (the reviewer 2026-10-29 r348): one list, so each arm's OFF
identity turns off its own arm AND every arm that landed after it. The tree then reads as it stood
before the arm, at any tip. Landing an arm appends it here; no older test is touched. Each with the
commit it landed in."""
from __future__ import annotations

ARMS = (
    ("TETHER_ARRIVAL_GAP", "0588f3a"),       # decision 5
    ("TETHER_INSTANCE_RETIRE", "26caa41"),   # decisions 2+3
    ("TETHER_KIND_SAVE", "27e574c"),
    ("TETHER_SETTLE_PRED", "658d5fb"),
    ("TETHER_DIVIDE", "2e4601b"),            # 1a
    ("TETHER_DIVIDE_CREDIT", "78d42b4"),
    ("TETHER_ASK", "2a8045c"),               # 1b, and its S1 re-price on read (same arm)
    ("TETHER_OWED_REJUDGE", "20cc52a"),      # 1d
)


def off_env(arm: str) -> dict:
    """The arm and every later batch arm OFF, for an OFF identity against the arm's base."""
    names = [a for a, _c in ARMS]
    assert arm in names, ("not a batch arm", arm)
    return dict.fromkeys(names[names.index(arm):], "0")
