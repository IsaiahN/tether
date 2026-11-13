"""8c: HOW OFTEN A SETTLED IDEA IS REUSED, PER CONTEXT, AND WHAT STAYS READY (TETHER_REUSE_BOOK; the
reviewer 2026-11-12 r1835/r1838, DESIGN_STEP8 P6; Isaiah 11-11 07:20-07:30, 11-12 10:06).

Isaiah's rules, kept as they were given:
- 07:20 a settled idea's reuse count decides what is loaded at game start and what is kept ready:
  the initially loaded first, new items that keep getting reused as a second tier, one-offs put
  back first; before a game exits, new items are stored with their usage updated.
- 07:20 the count must not outweigh other actions or reflexes and can't be relied on forever, so it
  stops after an "age" window that is the same length for every item;
- 07:22 that window is counted in CHANCES (occasions the item could have been used), not time;
- 07:24-07:30 second nature is per task, and the task is the sense cluster the cues pick out, so
  every count here is kept per CONTEXT (DESIGN_STEP8 B3's context_key), never pooled;
- 11-11 (the roadmap): a unit joins the GENERAL tier only after paying in at least 2 independent
  contexts; a failure in a new context splits it rather than demoting it (that is 8b-1's split);
- 11-12 (item 7): a musing re-test that PAYS on a parked gap counts as a payment in that context.

What it decides is only what is KEPT READY (an order and a residency list) and a TIEBREAK for the
idea walk (authority). Never which action wins, never standing (Fig 9 :60 "Use filters for the
budget and witnesses for the verdict"; Fig 2 :40 agreement is not evidence: authority orders, the
board's endings give standing).

PERSISTENCE: one summed field in the store's counts blob, "reuse_n", in the {key: {sub: n}} shape
lineage_store._counts_apply already sums: {json(ctx): {"C|head": chances, "U|head": uses,
"P|head": paid, "S|head": chances at its second use (written once), "M|head": payments
from musing}}. `drain()` returns only what changed since the last drain, so each save carries
its own increment and the root-to-tip sum is the lifetime count (the same rule as unit_used).
"""
from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Callable, Iterable
from typing import Any

import armflag

_ON = armflag.arm("TETHER_REUSE_BOOK", default=True)
ON = _ON          # the call sites read reuse.ON (arms are _UPPER: test_arm_modules)
FIELD = "reuse_n"


def _ck(ctx: Any) -> str:
    return json.dumps(ctx, sort_keys=True, default=str)


class ReuseBook:
    """Per (context, head): chances, uses inside the age window, and payments.

    `window` is the age window in chances, the same for every head (Isaiah 11-11 07:20-07:22).
    None = no window yet: the count runs until `derive_window` has enough history to set one
    (no number is picked here; DESIGN_STEP8: N is read from the agent's own reuse curves)."""

    def __init__(self, window: int | None = None, kernel: Iterable[str] = ()) -> None:
        self.window = window
        self.kernel = set(kernel)            # loaded first, always (reflexes and the kernel)
        self.chances: dict = defaultdict(int)  # (ckey, head) -> n
        self.uses: dict = defaultdict(int)     # (ckey, head) -> n inside the window
        self.paid: dict = defaultdict(int)     # (ckey, head) -> n
        self._delta: dict = defaultdict(lambda: defaultdict(int))
        self.second_use_at: dict = {}          # (ckey, head) -> chances at its SECOND use

    # -- the hooks the agent calls -------------------------------------------------------------
    def note_chance(self, ctx: Any, head: str) -> None:
        """`head` was offered (reachable) under `ctx`: one chance, whether used or not."""
        k = (_ck(ctx), head)
        self.chances[k] += 1
        self._delta[k[0]]["C|" + head] += 1

    def note_use(self, ctx: Any, head: str, paid: bool, source: str = "settle") -> bool:
        """`head` was used as a building block under `ctx` (a settle bound it, or musing re-tested
        it: source="muse"). Counted only inside the window; a payment is always recorded (it is
        what GENERAL reads). Returns whether the use was counted."""
        k = (_ck(ctx), head)
        if paid:
            self.paid[k] += 1
            self._delta[k[0]]["P|" + head] += 1
            if source == "muse":                 # 8d reads how often musing installed a head
                self._delta[k[0]]["M|" + head] += 1
        if self.window is not None and self.chances[k] > self.window:
            return False                         # the age window has closed for this head here
        self.uses[k] += 1
        self._delta[k[0]]["U|" + head] += 1
        if self.uses[k] == 2 and k not in self.second_use_at:
            self.second_use_at[k] = self.chances[k]
            self._delta[k[0]]["S|" + head] += self.chances[k]     # written once: its sum is it
        return True

    # -- what the counts decide ------------------------------------------------------------------
    def contexts_paid(self, head: str) -> int:
        return sum(1 for (c, h), n in self.paid.items() if h == head and n > 0)

    def tier(self, head: str) -> str:
        """kernel | general (paid in >= 2 contexts) | reused (used more than once in a context) |
        one_off (used once) | unused."""
        if head in self.kernel:
            return "kernel"
        if self.contexts_paid(head) >= 2:
            return "general"
        used = [n for (c, h), n in self.uses.items() if h == head]
        if any(n > 1 for n in used):
            return "reused"
        return "one_off" if used else "unused"

    def residency(self, heads: Iterable[str]) -> list[str]:
        """The order to load / keep ready: kernel, general, reused, one-offs, unused -- inside a
        tier by total uses (more first), then by the order given. One-offs are the first put back
        (Isaiah 11-11 07:20); nothing is deleted."""
        rank = {"kernel": 0, "general": 1, "reused": 2, "one_off": 3, "unused": 4}
        total: dict = defaultdict(int)
        for (_c, h), n in self.uses.items():
            total[h] += n
        hs = list(dict.fromkeys(heads))
        return sorted(hs, key=lambda h: (rank[self.tier(h)], -total[h], hs.index(h)))

    def authority(self, names: Callable[[tuple], Iterable[str]] | None = None
                  ) -> Callable[[tuple], float]:
        """8c's tiebreak for the idea walk (shape_order.make_order_key(authority=...)): a chain's
        authority is the summed paid-contexts of the heads it is built from -- a part used by ideas
        that paid in many contexts rises in ORDER only (PageRank's shape, Isaiah 11-03 "if thats
        useful lets do it"; Fig 2 :40: never standing). `names(chain)` gives the head names a chain
        contains (default: each atom's name)."""
        def default(chain: tuple) -> Iterable[str]:
            return (a.name for a in chain)
        nm = names or default
        cache: dict = {}

        def score(chain: tuple) -> float:
            s = 0.0
            for h in nm(chain):
                if h not in cache:
                    cache[h] = float(self.contexts_paid(h))
                s += cache[h]
            return s
        return score

    # -- persistence -----------------------------------------------------------------------------
    def drain(self) -> dict:
        """{json(ctx): {"C|", "U|", "P|", "S|", "M|" + head: n}} changed since the last drain."""
        out = {c: dict(d) for c, d in self._delta.items() if d}
        self._delta = defaultdict(lambda: defaultdict(int))
        return out

    def load(self, summed: dict) -> None:
        """Read the store's root-to-tip sum of FIELD back into the book (before play)."""
        for ck, d in (summed or {}).items():
            for sub, n in d.items():
                kind, head = sub.split("|", 1)
                if kind == "S":
                    self.second_use_at[(ck, head)] = n
                    continue
                tgt = {"C": self.chances, "U": self.uses, "P": self.paid}.get(kind)
                if tgt is not None:
                    tgt[(ck, head)] += n


def derive_window(book: ReuseBook) -> int | None:
    """THE AGE WINDOW FROM THE AGENT'S OWN HISTORY, not a picked number: the median number of
    chances a head took to be used a SECOND time -- how long this agent takes to make an idea
    "reused" (the toddler's run of praise until the act is routine, Isaiah 11-11 06:56). None until
    some head has been reused, so the count runs unwindowed until there is a curve to read."""
    seconds = sorted(book.second_use_at.values())
    if not seconds:
        return None
    return max(1, seconds[len(seconds) // 2])
