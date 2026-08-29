"""§18.3's four members, TRANSCRIBED. The rules are Redux's; the numbers are not.

§18.3 records why one detector was not enough: *the forward model looked for ONE thing -- a
rigid object that translates -- and that world's self does not translate.* The fix is a family
whose **failure modes are independent**, and the four are a lookup with a source rather than
four rules designed from the members' glosses. **Designing them here would be the
resemblance-into-class move**, and the working set exists.

**THE COLOUR MEMBERS ARE RE-SCOPED, NOT REPAIRED.** Redux calls `background_colour()`, which
names a stable fact that is not one -- colours permute when a game refreshes. `arc_percept`
refuses that concept as a DOMAIN PRIMITIVE and is right to; **it never refused reading a
colour's role WITHIN an episode.** So the reading is *the most common colour, this episode*:
bound on first sight, dropped at the boundary, with the same lifetime the map and the bindings
have. **Vocabulary permanent, instances transient.**

**EVERY CONSTANT IN THE SOURCE IS ACCOUNTED FOR HERE.** Thirteen distinct numbers, not the
seven I first counted -- the seven were constructor defaults and the bodies carried six more:

    window=2 (x2), bucket=8    DROPPED BY SCOPE. Used only by `self_frame`, Redux's
                               state-abstraction key for a policy. Nothing here consumes it,
                               so transcribing the parameter would import a knob for a
                               mechanism that is not present
    K=8                        DROPPED BY SCOPING. The history IS the episode and clears with
                               it, so a recency cap has nothing left to buy
    alpha=0.3                  RUNNING MEAN, in `self_family`
    res < 0.5 (x2)             `explained > unexplained` -- two observed counts compared
    mono < 0.8                 EXISTENTIAL: every nonzero step shares a sign. Monotone means
                               monotone, which is a basis; 0.8 was a cut
    streak >= 2, _n < 4,       COLLAPSED into `MIN_REPEAT`, one number with its basis stated
    len < 4, len(nz) < 3       at the site
    db[bg] = -10**9            REMOVED. The episode colour is skipped rather than sentinelled
    net >= len(nz)             TRANSCRIBED UNCHANGED -- already a comparison between two
                               quantities the world produced, with no free parameter

**AND IF ONE COULD NOT BE CONVERTED IT WOULD SAY SO.** A basis invented to satisfy the rule is
worse than a stated GUESSED, so nothing here carries a plausible sentence in place of a reason.
"""
from __future__ import annotations

import sys
from collections import Counter

import arc_percept as P
from self_family import MIN_REPEAT, SelfHypothesis, SelfModelFamily

sys.dont_write_bytecode = True


def _rows(board) -> list[list[int]]:
    """Duck-typed. A board arrives as a list of lists or an ndarray and both index the same."""
    return [[int(v) for v in row] for row in board]


def _counts(g: list[list[int]]) -> Counter:
    return Counter(v for row in g for v in row)


def _changed(a: list[list[int]], b: list[list[int]]) -> set[tuple[int, int]]:
    """Cells that differ. An empty set on a shape change: nothing is comparable cell-wise."""
    if len(a) != len(b) or (a and len(a[0]) != len(b[0])):
        return set()
    return {(r, c) for r, row in enumerate(a) for c, v in enumerate(row) if b[r][c] != v}


class Episode:
    """The per-episode binding, and the ONLY thing here with an episode's lifetime.

    *In this episode, the frame's colour is 4.* A fact about instances, so it clears at the
    boundary with `bound`, `trace` and the map. The variable-keyed READING -- *the colour
    nothing else sits on* -- is permanent and lives in the rule that asks for it.
    """

    def __init__(self) -> None:
        self.common: int | None = None

    def see(self, g: list[list[int]]) -> None:
        if self.common is None and g:
            self.common = _counts(g).most_common(1)[0][0]

    def clear(self) -> None:
        self.common = None


class TranslationSelf(SelfHypothesis):
    """A rigid object that moves. Explained = **vacated + arrived**, over what changed."""

    name = "translation"

    def __init__(self) -> None:
        super().__init__()
        self._streak = 0

    def observe(self, before, action, after) -> float:
        a, b = _rows(before), _rows(after)
        ch = _changed(a, b)
        if not ch:
            self._streak = 0
            return 1.0
        old = {P.shape_of(o): o for o in P.components(a)}
        explained: set[tuple[int, int]] = set()
        for o in P.components(b):
            prev = old.get(P.shape_of(o))
            if prev is not None and prev["cells"] != o["cells"]:
                explained |= (prev["cells"] | o["cells"]) & ch
        res = max(0.0, 1.0 - len(explained) / len(ch))
        self._attribute(action, 1.0 - res)
        self._streak = self._streak + 1 if (1.0 - res) > res else 0
        return res

    def has_self(self) -> bool:
        return self._streak >= MIN_REPEAT

    def boundary(self) -> None:
        super().boundary()
        self._streak = 0


class GrowthEdgeSelf(SelfHypothesis):
    """A growing / advancing trail: the colour that GAINED most, skipping the episode's own."""

    name = "growth"

    def __init__(self, ep: Episode) -> None:
        super().__init__()
        self.ep = ep
        self._streak = 0
        self.colour: int | None = None
        self.frontier: set[tuple[int, int]] = set()

    def observe(self, before, action, after) -> float:
        a, b = _rows(before), _rows(after)
        ch = _changed(a, b)
        if not ch:
            self._streak = 0
            return 1.0
        self.ep.see(a)
        ca, cb = _counts(a), _counts(b)
        gained = [(cb[k] - ca[k], k) for k in set(ca) | set(cb) if k != self.ep.common]
        gained = [g for g in gained if g[0] > 0]
        if not gained:
            self._streak = 0
            return 1.0
        col = max(gained)[1]
        fresh = {(r, c) for (r, c) in ch if b[r][c] == col}
        res = max(0.0, 1.0 - len(fresh) / len(ch))
        self._attribute(action, 1.0 - res)
        if (1.0 - res) > res:
            self._streak += 1
            self.colour, self.frontier = col, fresh
        else:
            self._streak = 0
        return res

    def has_self(self) -> bool:
        return self._streak >= MIN_REPEAT and bool(self.frontier)

    def boundary(self) -> None:
        super().boundary()
        self._streak, self.colour, self.frontier = 0, None, set()


class ValueLatentSelf(SelfHypothesis):
    """A NON-SPATIAL self: the controllable thing is a scalar that moves consistently.

    **There is no self-cell to point at -- the self IS the value.** This is the member whose
    absence made a translation-shaped family fail together, and it is why the family is not
    four flavours of one idea.
    """

    name = "value"

    def __init__(self, ep: Episode) -> None:
        super().__init__()
        self.ep = ep
        self.hist: dict[int, list[int]] = {}
        self.colour: int | None = None

    @staticmethod
    def _nz(series: list[int]) -> list[int]:
        return [d for d in (series[i + 1] - series[i] for i in range(len(series) - 1)) if d]

    def observe(self, before, action, after) -> float:
        b = _rows(after)
        if not b:
            return 1.0
        self.ep.see(_rows(before))
        cts = _counts(b)
        prev = self.hist.get(self.colour, [])
        was = prev[-1] if prev else None
        for k in set(cts) | set(self.hist):
            self.hist.setdefault(k, []).append(int(cts[k]))
        if self.colour is not None and was is not None:
            # the resource's signed motion under THIS action -- Redux's `act_delta`, and the
            # per-member half of the Agency ruling.
            self._attribute(action, float(cts[self.colour]) - float(was))
        best, best_mono = None, 0.0
        for col, series in self.hist.items():
            if col == self.ep.common:
                continue
            nz = self._nz(series)
            if not nz:
                continue
            mono = abs(sum(1 if d > 0 else -1 for d in nz)) / len(nz)
            if mono > best_mono:
                best, best_mono = col, mono
        if best is not None:
            self.colour = best
        return max(0.0, 1.0 - best_mono)

    def has_self(self) -> bool:
        """Consistent AND meaningful: every nonzero step one way, and net travel of at least
        one unit per nonzero step -- which count jitter does not sustain."""
        if self.colour is None:
            return False
        series = self.hist.get(self.colour, [])
        nz = self._nz(series)
        if len(nz) < MIN_REPEAT:
            return False
        if abs(sum(1 if d > 0 else -1 for d in nz)) != len(nz):
            return False
        return abs(series[-1] - series[0]) >= len(nz)

    def boundary(self) -> None:
        super().boundary()
        self.hist, self.colour = {}, None


class RegionToggleSelf(SelfHypothesis):
    """A bounded region that ALTERNATES -- true toggling, not mere repeated change.

    A cell toggles iff its value returns to what it was two steps ago. **The rule carries its
    own falsifier**: random repaint changes cells every step and never brings them back.
    """

    name = "toggle"

    def __init__(self) -> None:
        super().__init__()
        self._g1: list[list[int]] | None = None
        self._g2: list[list[int]] | None = None
        self._streak = 0
        self.region: set[tuple[int, int]] = set()

    def observe(self, _before, action, after) -> float:
        # `_before` is unused: this member keeps its OWN two-step history, because the rule
        # is g[t] == g[t-2], which one before/after pair cannot see.
        b = _rows(after)
        res = 1.0
        if self._g1 is not None and self._g2 is not None:
            ch = _changed(self._g1, b)
            back = {(r, c) for (r, c) in ch
                    if len(self._g2) == len(b) and b[r][c] == self._g2[r][c]}
            if ch:
                res = max(0.0, 1.0 - len(back) / len(ch))
                self._attribute(action, 1.0 - res)
                if (1.0 - res) > res and back:
                    self._streak += 1
                    self.region = back
                else:
                    self._streak = 0
        self._g2, self._g1 = self._g1, b
        return res

    def has_self(self) -> bool:
        return self._streak >= MIN_REPEAT and bool(self.region)

    def boundary(self) -> None:
        super().boundary()
        self._g1 = self._g2 = None
        self._streak, self.region = 0, set()


def family() -> SelfModelFamily:
    """The four, sharing one episode binding. **The order is §18.3's table order.**"""
    ep = Episode()
    fam = SelfModelFamily([TranslationSelf(), GrowthEdgeSelf(ep),
                           ValueLatentSelf(ep), RegionToggleSelf()],
                          on_boundary=ep.clear)
    fam.episode = ep
    return fam
