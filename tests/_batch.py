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
    ("TETHER_NAMED_REMAINDER", "a228a09"),        # 1e
    ("TETHER_PLAN_NARROW", "e4c3be3"),       # 4
    ("TETHER_CONTACT_FIRST", "82308d8"),     # wip/finish 1 (r392, r393)
    ("TETHER_ROUTE_NAMED", "af6f0cd"),       # wip/finish 2
    ("TETHER_PROGRESS_SHELF", "5cb5e78"),    # wip/finish 3
    ("TETHER_UNTESTED_KEEP", "10cbfae"),     # wip/finish 4
    ("TETHER_CARRY_W", "afe1a82"),           # wip/finish 5
    ("TETHER_INDIST_ON_CHANGE", "2de7df7"),  # wip/finish 6 (r400)
    ("TETHER_VIEW_HOLD_SAME", "c1075e4"),    # wip/finish2 7 (r414, r415)
    ("TETHER_VIEW_HOLD_SAME_ROLE", "e7a1c8e"),   # wip/finish2 8 (r417)
    ("TETHER_CONTINGENT_ONE_PASS", "b0489bf"),   # wip/finish3 9 (B3, r427)
    ("TETHER_ARRIVAL_ALIAS", "eadee1a"),     # wip/arrival-alias 10 (r428, r431)
    ("TETHER_ASK_ON_BOARD", "3736340"),      # wip/ask-on-board 11 (r452 A)
    ("TETHER_HARNESS_LEVEL_RESET", "713c73e"),   # wip/harness-level-reset 13 (r464 2); base cba1dd5
    ("TETHER_STOP_READ_STEP", "9eb4012"),    # wip/stop-read-step 12 (r462, r463)
    ("TETHER_RETIRE_HOLDER", "f0b53e8"),     # wip/retire-holder 15 (r466 1(c), r470); base 9eb4012
    ("TETHER_REMAINDER_VERDICT_KEY", "22319e0"),   # wip/remainder-verdict-key 14 (r466 1(b))
    ("TETHER_CONTACT_LIGHT", "wip"),         # wip/contact-light 16 (r481, r482 B, r483)
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
