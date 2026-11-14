"""THE AGENDA READER (item 2a, TETHER_AGENDA; the reviewer r1948/r1949 on Isaiah's overnight word,
2026-11-13 23:28-23:29; design docs/04-PLANS_AHEAD/02-BUILD_SEQUENCE_FUTURE_STATE.md 2a). It runs a
Tether card the way the hand test did, as the agent's own thinking step, and writes what it asked.

A card is never lit by a word in a reading: it is chosen by the SHAPE of what is unexplained. Each
card's shape is a predicate over readings the agent already holds (SHAPES below); a card with no
predicate yet is never lit, and shapes() says so. Ties go to the card's `order` (Fig 3: upstream
first).

Per call (once per PLAN step, beside the goal path, never replacing it):
  1. describe the residual in effect terms ("Describe before you look", order 0) -- a row only when
     it is new;
  2. look the card up by shape, lowest order first, skipping a card refuted on this board;
  3. run its asks: for "Which link first", the first unmet link of SEE -> WORDS -> GOAL -> ROUTE ->
     KEEP, each read from the board or the record; the question is that link's ask, and its answer
     says where it will come from;
  4. check refuted_by: the first unmet link unchanged while the goal's gap shrinks anyway -- the
     card did not bear here; it is dropped for this board and the next card by order is used;
  5. write one decision row: residual | card | question | answer | from | why, and the card's
     do_sym evaluated through symbols (a symbol with no reading is written "unbound", never
     substituted).
Budget: no new clock; a question asked twice on one board without a new residual is not asked a
third time.
"""
from __future__ import annotations

import json
import os
from typing import Any

import symbols

_HERE = os.path.dirname(os.path.abspath(__file__))
LINKS = ("SEE", "WORDS", "GOAL", "ROUTE", "KEEP")
_CARDS: dict | None = None
_ANSWER = {"SEE": "read the board again", "WORDS": "press-and-watch: the next unpressed action",
           "GOAL": "the goal path proposes one", "ROUTE": "the goal split names one",
           "KEEP": "name, verify, carry"}


def cards() -> dict[str, dict]:
    """The Tether cards from library/tether_rules.json, by short name (without "TETHER|")."""
    global _CARDS
    if _CARDS is None:
        with open(os.path.join(_HERE, "library", "tether_rules.json"), encoding="utf-8") as fh:
            ent = json.load(fh)["entries"]
        _CARDS = {k.split("|", 1)[-1]: v for k, v in ent.items()}
    return _CARDS


def _shrinking(ag: Any) -> bool:
    """Some slot's goal gap fell on its last reading (the selector's own record, agent._res)."""
    return any(len(v) >= 2 and v[-1] < v[-2] for v in getattr(ag, "_res", {}).values())


def links(ag: Any) -> dict[str, tuple[Any, str]]:
    """Which link first's five links, each (met, where read); met None = no reading (never the
    first unmet)."""
    hold = getattr(ag, "_try_first_hold", None)
    held = getattr(ag, "_hyp", None) is not None
    return {
        "SEE": (bool(getattr(ag, "slot_types", None)), "board: objects perceived and told apart"),
        "WORDS": (not (hold() if hold is not None else False),
                  "record: every offered action pressed on this board (TRY_FIRST)"),
        "GOAL": (held, "record: a goal held"),
        "ROUTE": (held and getattr(ag, "_split_why", None) is None,
                  "record: the last goal split named a route"),
        "KEEP": (None, "no reading yet: what worked named and carried"),
    }


def _first_unmet(lk: dict) -> str | None:
    return next((k for k in LINKS if lk[k][0] is False), None)


SHAPES = {
    "Which link first": lambda _ag, res: res["live"] and not res["shrinking"],
    "Instrument the middle": lambda ag, _res: getattr(ag, "_hyp", None) is None,
}


def shapes() -> dict[str, bool]:
    """Every card and whether it has a shape predicate yet."""
    return {name: name in SHAPES for name in cards()}


class Reader:
    def __init__(self) -> None:
        self.asked: dict = {}          # (board, card, question, residual key) -> times asked
        self.refuted: set = set()      # (board, card)
        self.last: tuple | None = None
        self.history: list = []        # (board, first unmet link, shrinking) per call

    def residual(self, ag: Any) -> dict:
        h = getattr(ag, "_hyp", None)
        focal = h["slots"][0] if h and h.get("slots") else None
        live = symbols.evaluate("R⁺_s", ag, slot=focal) if focal else symbols.UNBOUND
        return {"focal": focal, "live": True if live is symbols.UNBOUND else live > 0,
                "live_mass": None if live is symbols.UNBOUND else round(float(live), 3),
                "shrinking": _shrinking(ag),
                "slots": len(getattr(ag, "slot_types", {}) or {})}

    def step(self, ag: Any) -> dict | None:
        board = getattr(getattr(ag, "iface", None), "board_n", None)
        res = self.residual(ag)
        key = (res["focal"], res["live"], res["shrinking"])
        if key != self.last:
            self.last = key
            gap = "shrinking" if res["shrinking"] else "not shrinking"
            self._row(ag, "Describe before you look",
                      cards()["Describe before you look"]["asks"][0],
                      f"{res['slots']} slots; focal {res['focal']}; live mass "
                      f"{res['live_mass']}; gap {gap}", "board", res,
                      "a new residual is described before any lookup (order 0)")
        lk = links(ag)
        first = _first_unmet(lk)
        self.history.append((board, first, res["shrinking"]))
        for name in sorted(SHAPES, key=lambda n: (cards()[n].get("order", 9), n)):
            if (board, name) in self.refuted or not SHAPES[name](ag, res):
                continue
            if name == "Which link first":
                if self._refuted_link(board, first):
                    self.refuted.add((board, name))
                    self._row(ag, name, "refuted_by", cards()[name]["refuted_by"], "record", res,
                              "the first unmet link held while the gap shrank anyway: dropped")
                    continue
                if first is None:
                    continue
                q = cards()[name]["asks"][LINKS.index(first)]
                src = "press" if first == "WORDS" else lk[first][1].split(":", 1)[0]
                return self._ask(ag, board, name, q, f"{first} unmet -> {_ANSWER[first]}", src,
                                 res, key, f"first unmet link {first} ({lk[first][1]})")
            q = cards()[name]["asks"][0]
            return self._ask(ag, board, name, q, "no goal held: the goal path proposes one",
                             "record", res, key,
                             "the agent has percepts and actions but no stated goal")
        return None

    def refused(self, ag: Any, slot: str, why: str, pushed: bool) -> dict:
        """REPAIR AT THE REFUSAL (r1957): a goal refused at its own test is "Three texts before
        acting"'s residual ("whenever an action did not do what it was for"). The goal was held
        and acted on, so the thin text is CONTEXT: the condition the board showed becomes a
        subgoal (cards v4 (b), on_refuted). One row, whatever the push found."""
        card = "Three texts before acting"
        c = cards()[card]
        on = c.get("on_refuted", {})
        res = {"focal": slot, "live_mass": None, "shrinking": _shrinking(ag),
               "slots": len(getattr(ag, "slot_types", {}) or {})}
        ans = (f"CONTEXT thin ({why}): the missing condition is pursued first as a subgoal"
               if pushed else
               f"CONTEXT thin ({why}): no open condition found to pursue first; narrow what is "
               "missing")
        return self._row(ag, card, on.get("first", c["asks"][1]), ans, "board", res,
                         on.get("context", "the goal was refused at its own test"))

    def _refuted_link(self, board: Any, first: str | None) -> bool:
        tail = [h for h in self.history if h[0] == board][-4:]
        return (first is not None and len(tail) >= 4 and all(h[1] == first for h in tail)
                and sum(h[2] for h in tail) >= 2)

    def _ask(self, ag, board, card, q, answer, src, res, key, why) -> dict | None:
        k = (board, card, q, key)
        self.asked[k] = self.asked.get(k, 0) + 1
        if self.asked[k] > 2:
            return None
        return self._row(ag, card, q, answer, src, res, why)

    def _row(self, ag, card, q, answer, src, res, why) -> dict:
        do_sym = cards()[card].get("do_sym")
        sym = None
        if do_sym and "R⁺_s" in do_sym:
            v = (symbols.evaluate("R⁺_s", ag, slot=res["focal"]) if res["focal"]
                 else symbols.UNBOUND)
            sym = {"R⁺_s": "unbound" if v is symbols.UNBOUND else round(float(v), 3)}
        row = {"card": card, "question": q, "answer": answer, "from": src, "why": why,
               "residual": {k: res[k] for k in ("focal", "live_mass", "shrinking", "slots")},
               "do_sym": do_sym, "sym": sym}
        ag.led.record(ag.cycle, ag._running_step, "@agenda", "agenda", **row,
                      reads="the agent's own card step: residual | card | question | answer | "
                            "from | why")
        return row
