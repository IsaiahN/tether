"""10a+: WHAT I CAN DO, WHAT I CAN'T, AND WHEN AN ITEM SWITCHES SIDES (TETHER_CAN_LEDGER; the
reviewer 2026-11-12; Isaiah 15:01-15:08; WATSON what_i_can_and_cant_and_when_it_switches;
Fig 6 :42-47, Fig 8 :39, Fig 11 :40-53, Fig 9 :60).

Every subject slot sits in one of four lists, read off the board each planning episode, never
authored:
  CAN        movable, routable, not on the agent's own clock
  BLOCKED    a precondition missing: not a movable slot, on the own clock, or no route although
             every action has been tried on this board
  NOT_FOUND  no route YET, while some action is still untried on this board (a search that found
             nothing is never a proof of absence, Fig 8 :39)
  GIVEN_UP   would be CAN, but every goal held on it this level ended refuted (Fig 6 :46: never-held
             and held-and-given-up are different facts)
An item that crosses between lists is a CUE (Isaiah 15:01): its row carries the old and new list and
reason (the pretext), what changed just before it (the cue), the steps since the last reading (the
lag) and, from step 8's source order, who it reads as moved by (src; a filter, never a verdict,
Fig 9 :60). An item new to the lists is an APPEARANCE. GIVEN_UP -> CAN with nothing new learned is
flagged "world or scope changed" (Fig 6 :47).

Pure functions here; the agent hands in what it read. Record-only: nothing here changes a choice.
"""
from __future__ import annotations

CAN, BLOCKED, NOT_FOUND, GIVEN_UP = "CAN", "BLOCKED", "NOT_FOUND", "GIVEN_UP"
REFUTED_ENDS = frozenset({"arrived_no_clear", "stalled", "lost", "left_rate"})


def classify(slots, movable, routable, clock, untried_actions, given_up) -> dict:
    """slot -> (list, reason) for every subject slot. `movable` / `routable` / `clock` /
    `given_up` are sets of slots; `untried_actions` is how many actions this board has not yet
    tried (0: every action tried)."""
    out = {}
    for s in slots:
        if s not in movable:
            out[s] = (BLOCKED, "not a movable slot")
        elif s in clock:
            out[s] = (BLOCKED, "the own clock moves it")
        elif s not in routable:
            out[s] = ((NOT_FOUND, f"no route yet; {untried_actions} action(s) untried")
                      if untried_actions else (BLOCKED, "no route; every action tried"))
        elif s in given_up:
            out[s] = (GIVEN_UP, "every goal held on it this level ended refuted")
        else:
            out[s] = (CAN, "movable and routable")
    return out


def crossings(prev: dict, now: dict, learned_since: bool) -> tuple[list, list]:
    """(crossings, appearances) between two readings. A crossing is an item whose list changed;
    an appearance is an item absent from `prev`. `learned_since`: something new was learned
    between the readings (a new effect, a new term) -- without it, GIVEN_UP -> CAN is flagged."""
    cross, appear = [], []
    for s, (side, why) in now.items():
        if s not in prev:
            appear.append({"item": s, "list": side, "reason": why})
            continue
        old_side, old_why = prev[s]
        if old_side == side:
            continue
        kind = ("opened" if side == CAN and old_side == BLOCKED else
                "discovered" if side == CAN and old_side == NOT_FOUND else
                "returned" if side == CAN and old_side == GIVEN_UP else
                "closed" if old_side == CAN else "moved")
        row = {"item": s, "from": [old_side, old_why], "to": [side, why], "kind": kind}
        if kind == "returned" and not learned_since:
            row["flag"] = "world or scope changed (Fig 6 :47): re-test before trusting either"
        cross.append(row)
    return cross, appear


def counts(now: dict) -> dict:
    c = {CAN: 0, BLOCKED: 0, NOT_FOUND: 0, GIVEN_UP: 0}
    for side, _why in now.values():
        c[side] += 1
    return c
