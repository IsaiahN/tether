"""N1 / N2, THE LIVE NARRATOR (the reviewer 2026-11-02 14:38 plan, r822; Isaiah 14:22, question 4):
the ledger's key rows said aloud as they are written, one line each, in the agent's own words, and
copied to narrate.log beside the ledger. It reads rows and writes nothing back: the ledger is the
same with it ON or OFF (Fig 13: "That record is not documentation of the term. It is the term.").

  N1  c<cycle> <EVENT> <slot>: <what the row says>, for MINT, SETTLE, REFUTE, LEAVE (no_entry),
      LEVEL / WIN, PLAN (a plan episode, a newly selected want), ROUTINE_REFUSED (its reason),
      CLOSER (progress on an aim) and NOT_YET (a window under the cut offered nothing).
      THE CAP is the loop's own shape: one line per event kind per cycle, so a step prints at most
      one line per kind it produced; every further row of a kind is COUNTED and said at the next
      cycle as "+n more", never dropped silently.
  N2  per game, "stopped at link <perception | vocabulary | objective | plan | carry> because
      <counts>": the first link of the chain whose output this game was empty (Fig 3 :18 "Where a
      given chain stops is a reading, never a property"; :20 "Each link consumes what the one above
      produces").
  GUARD (the reviewer r825, r828 a): say / see / end_game never raise into play. The first error
      turns the narrator off for the run and is counted (faults, fault); the ledger is untouched.
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

import armflag

_NARRATE = armflag.arm("TETHER_NARRATE", default=True)
WIDTH = 200                 # one console line; a longer row is cut, its full form is the ledger


def _short(v) -> str:
    s = v if isinstance(v, str) else repr(v)
    return s if len(s) <= 80 else s[:77] + "..."


def say_row(step: str, event: str, d: dict, ends: tuple) -> tuple[str, str] | None:
    """(EVENT, text) for a key row, or None. `ends` is (WIN, ADVANCE) from the ledger."""
    win, advance = ends
    if d.get("status") == "refuted":
        what = _short(d.get("term") or d.get("asked"))
        return "REFUTE", f"{what} -- {_short(d.get('verdict', ''))}"
    if step == "MINT" and event == "mint":
        return "MINT", f"{_short(d.get('term'))} reads={_short(d.get('reads', ''))}"
    if step == "SETTLE" and event == "settle":
        return "SETTLE", f"{_short(d.get('term'))} {d.get('status')}"
    if step == "SETTLE" and event == "demote":
        return "REFUTE", f"{_short(d.get('term'))} demoted"
    if step == "ROUTE" and event == "no_entry":
        return "LEAVE", f"no entry under {_short(d.get('key'))}"
    if step == "IMPORT" and event == "ending" and d.get("how") in (win, advance):
        return ("WIN" if d["how"] == win else "LEVEL"), f"cleared, to level {d.get('to_level')}"
    if step == "MINT" and event == "plan_episode":
        return "PLAN", _short({k: v for k, v in d.items() if k != "reads"})
    if step == "PLAN" and event == "routine_refused":
        return "ROUTINE_REFUSED", _short(d.get("reason"))
    if step == "PERCEIVE" and event == "progress":
        on = _short(list(d.get("closer") or ()))
        return "CLOSER", f"on {on} selected={d.get('selected_want')}"
    return None


class Narrator:
    def __init__(self, path: Path | None, ends: tuple) -> None:
        self.on = _NARRATE and path is not None
        self._log = path.with_name("narrate.log") if self.on else None
        if self._log is not None:
            self._log.write_text("", encoding="utf-8")
        self._ends = ends
        self._cyc = None
        self._said: set = set()
        self._over: collections.Counter = collections.Counter()
        self._want = None
        self.game: collections.Counter = collections.Counter()
        self.refused: collections.Counter = collections.Counter()
        self._games = 0                  # N2 lines said; an empty game after one is not said
        self.faults = 0
        self.fault: str | None = None

    def _guard(self, fn, *a) -> None:
        if not self.on:
            return
        try:
            fn(*a)
        except Exception as e:           # a console or log error must never reach play
            self.on = False
            self.faults += 1
            self.fault = repr(e)[:200]

    def say(self, cycle: int, kind: str, slot: str, text: str) -> None:
        self._guard(self._say, cycle, kind, slot, text)

    def see(self, cycle: int, step: str, slot: str, event: str, d: dict) -> None:
        self._guard(self._see, cycle, step, slot, event, d)

    def end_game(self, cycle: int, label: str) -> None:
        self._guard(self._end_game, cycle, label)

    def _emit(self, line: str) -> None:
        line = line if len(line) <= WIDTH else line[:WIDTH - 3] + "..."
        print(line, file=sys.stdout, flush=True)
        with self._log.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def _flush(self) -> None:
        if self._over:
            self._emit(f"c{self._cyc} +{sum(self._over.values())} more: "
                       + ", ".join(f"{k} {n}" for k, n in sorted(self._over.items())))
        self._said, self._over = set(), collections.Counter()

    def _turn(self, cycle: int) -> None:
        if cycle != self._cyc:
            self._flush()
            self._cyc = cycle

    def _say(self, cycle: int, kind: str, slot: str, text: str) -> None:
        self._turn(cycle)
        self.game[kind] += 1
        if kind in self._said:
            self._over[kind] += 1
            return
        self._said.add(kind)
        self._emit(f"c{cycle} {kind} {slot}: {text}")

    def _see(self, cycle: int, step: str, slot: str, event: str, d: dict) -> None:
        if step == "PERCEIVE" and event == "bet":
            self.game["bet"] += 1
        if step == "PLAN" and event == "routine_refused":
            self.refused[str(d.get("reason"))[:60]] += 1
        if step == "PERCEIVE" and event == "goal_choice":
            sel = d.get("selected")
            if sel is not None and sel != self._want:
                self._want = sel
                self._say(cycle, "PLAN", slot, f"want selected {_short(sel)}")
            return
        got = say_row(step, event, d, self._ends)
        if got is not None:
            self._say(cycle, got[0], slot, got[1])

    def stopped_at(self) -> tuple[str, str]:
        """N2: the first link whose output was empty this game, and the counts it read."""
        g = self.game
        reads = (f"bets {g['bet']}, minted {g['MINT']}, settled {g['SETTLE']}, refuted "
                 f"{g['REFUTE']}, closer {g['CLOSER']}, plans {g['PLAN']}, levels {g['LEVEL']}, "
                 f"won {g['WIN']}")
        if self.refused:
            reads += f", routine refused {sum(self.refused.values())} (most: " \
                     f"{self.refused.most_common(1)[0][0]})"
        if g["WIN"]:
            return "none (won)", reads
        if not g["bet"]:
            return "perception", reads
        if not (g["MINT"] or g["SETTLE"]):
            return "vocabulary", reads
        if not (g["CLOSER"] or g["PLAN"]):
            return "objective", reads
        if not g["LEVEL"]:
            return "plan", reads
        return "carry", reads

    def _end_game(self, cycle: int, label: str) -> None:
        self._flush()
        if self._games and not self.game:
            return                       # nothing since the last game's line: no second line
        self._games += 1
        link, reads = self.stopped_at()
        self._emit(f"c{cycle} GAME {label}: stopped at link {link} because {reads}")
        self.game, self.refused, self._want = collections.Counter(), collections.Counter(), None
