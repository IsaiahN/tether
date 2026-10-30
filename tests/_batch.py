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
    ("TETHER_ASK", "2a8045c"),               # 1b
    ("TETHER_OWED_REJUDGE", "20cc52a"),      # 1d
    ("TETHER_S1_REPRICE", "2855932"),        # 1b's re-price (r350)
    ("TETHER_STOP_RULES", "d148097"),        # 1c
    ("TETHER_NAMED_REMAINDER", None),        # 1e; its sha comes with the next arm
)
# A batch arm whose TREE DEFAULT was flipped after later arms landed (r359): (the arm, the last
# batch arm before the flip, its value before, the flip's commit). An arm under test that landed
# after the flipped arm and up to the flip was gated against bases holding the old value, so
# off_env pins it.
FLIPS = (
    ("TETHER_DIVIDE_CREDIT", "TETHER_STOP_RULES", "1", "2dea904"),   # (a2), Isaiah 2026-10-29 15:50
)


def off_env(arm: str) -> dict:
    """The arm and every later batch arm OFF, for an OFF identity against the arm's base; a flipped
    arm that landed before it is pinned to its value before the flip (FLIPS)."""
    names = [a for a, _c in ARMS]
    assert arm in names, ("not a batch arm", arm)
    i = names.index(arm)
    env = dict.fromkeys(names[i:], "0")
    for flipped, last, before, _c in FLIPS:
        if flipped not in env and i <= names.index(last):
            env[flipped] = before
    return env


def flip_env(flipped: str) -> dict:
    """A flip's own identity against the tree before it (r369): the flipped arm at its value
    before the flip, and every batch arm that landed after the flip OFF."""
    names = [a for a, _c in ARMS]
    (_f, last, before, _c), = [f for f in FLIPS if f[0] == flipped]
    return {flipped: before, **dict.fromkeys(names[names.index(last) + 1:], "0")}
