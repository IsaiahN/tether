"""§18.3's non-simulable detector family — the SEAM and the SELECTION, domain-agnostic.

The members live elsewhere and are injected, on `arc_atoms.three_spaces(predict)`'s pattern:
**this file must not know what a self can look like**, or the family's membership becomes a
decision taken here instead of by whatever reads the world.

**THE DISCIPLINE IS THE BASE CLASS AND IT IS THE WHOLE POINT.** §18.3: *four correlated
detectors are one detector wearing four names, which is collapse 2 inside the perception
layer.* So members are compared **only** by a ground-facing residual and **never by judging
each other** — no member sees another's score, and the family holds no cross-member state.

**THE COMPLETENESS CRITIC IS THE OTHER HALF.** `unmodeled()` fires when no member has a self
OR the best one still leaves more unexplained than it explains — *the whole family failed
together, which flags a shared smuggled presupposition to surface.*

> **AND IT INSTRUMENTS ONLY THE FAILURE SIDE, WHICH IS RECORDED RATHER THAN HIDDEN.** §18.3's
> requirement is that members *not share a failure mode*. Four members **failing** together is
> visible in the residuals; four **agreeing and all being right by common cause** is invisible
> without the ground. **Non-simulability is still asserted from the shape of the four
> descriptions, and asserting a panel property is the thing the panel law forbids.** The
> measurement is owed; this file does not pretend to supply it.

**PER-MEMBER CONTINGENCY (RULED).** *What responds to me* is not separated from *what kind of
thing I am*: **each member attributes its OWN signal to actions**, the way Redux's
`ValueLatentSelf` carries `act_delta`. Neither a fifth member nor a substrate under the four.

**ONE NUMBER SURVIVES IN THIS FILE AND IT IS `MIN_REPEAT`.** Every other constant in the
transcribed source was dropped by scope or converted to a comparison between two quantities the
world produced. `0.5` is not among them: *explained vs unexplained* are the two halves of one
quantity, so their meeting point is not a cut anyone chose — and the code says it that way so
it cannot be read as a threshold.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

# anchor: one observation is a coincidence -- over a single step every direction is monotone,
# every change is a first change, and no repeat has happened. Two is the smallest count that is
# not one observation. Not tuned, and nothing above it was tried: if it needs to be 3 that is a
# finding rather than a knob. It replaces `streak >= 2`, `_n < 4`, `len(series) < 4` and
# `len(nz) < 3` in the source, none of which carried a basis.
MIN_REPEAT = 2


class SelfHypothesis:
    """A candidate answer to *what do I control here?*

    `observe()` returns a residual in [0, 1]: **0 explained this step perfectly, 1 explained
    nothing.** It is the only quantity the family compares, and it faces the ground rather than
    another member.
    """

    name = "base"

    def __init__(self) -> None:
        self._by_action: dict[str, list[float]] = {}
        self._order: tuple[str, ...] = ()   # its own ranking of the actions, last seen
        self._held = 0                      # how long that ranking has been unchanged

    def observe(self, _before, _action, _after) -> float:
        return 1.0

    def has_self(self) -> bool:
        return False

    def boundary(self) -> None:
        """Drop what was bound to THIS episode. Vocabulary permanent, instances transient."""
        self._by_action = {}
        self._order, self._held = (), 0

    def _attribute(self, action: str, signal: float) -> None:
        """This member's OWN signal, under this action. Per-member contingency."""
        self._by_action.setdefault(str(action), []).append(float(signal))
        c = self.contingency()
        now = tuple(sorted(c, key=lambda a: c[a]))
        self._held = self._held + 1 if now == self._order else 0
        self._order = now

    def stable(self) -> bool:
        """**ORDINAL, BECAUSE A THRESHOLD HERE WOULD MEASURE THE SAMPLE COUNT.**

        A running mean changes by `(x - mean) / n`, which shrinks as `1/n` **whatever the data
        does** -- so *change below epsilon* would report how many observations there are, not
        whether the estimate settled. That is `EPS`'s own failure, and it is why this is a
        RANKING rather than a magnitude: **has this member stopped reordering the actions.**

        `MIN_REPEAT` is reused rather than a second constant invented -- *one observation is a
        coincidence* is the same claim about a ranking as about a streak.
        """
        return self._held >= MIN_REPEAT

    def contingency(self) -> dict[str, float]:
        return {a: sum(v) / len(v) for a, v in sorted(self._by_action.items()) if v}


class SelfModelFamily:
    """The members, priced by their own residuals and selected on them. Nothing else."""

    def __init__(self, members: list[SelfHypothesis], on_boundary=None) -> None:
        # `on_boundary` is whatever else this family bound to the episode. Agnostic on purpose:
        # this file must not learn what a domain's per-episode binding IS.
        self.members = list(members)
        self._on_boundary = on_boundary
        self._sum = {m.name: 0.0 for m in self.members}
        self._n = 0

    def observe(self, before, action, after) -> None:
        self._n += 1
        for m in self.members:
            self._sum[m.name] += float(m.observe(before, action, after))

    def mean(self, name: str) -> float:
        """A RUNNING MEAN, because every observation counts once and nothing weights recency.

        Redux used an EWMA at `alpha = 0.3`. The smoothing had no basis at the site and a mean
        needs no parameter, so the number went rather than acquiring a sentence.
        """
        return self._sum[name] / self._n if self._n else 1.0

    def selected(self) -> SelfHypothesis | None:
        """The best-PREDICTING member that has a self. Ties are not broken -- `min` is stable
        over the injected order, and inventing a tie-break would be a preference nobody asked
        for."""
        live = [m for m in self.members if m.has_self()]
        return min(live, key=lambda m: self.mean(m.name)) if live else None

    def unmodeled(self) -> bool:
        """The completeness critic. **The whole family failing together is the signal.**"""
        m = self.selected()
        if m is None:
            return True
        unexplained = self.mean(m.name)
        return (1.0 - unexplained) < unexplained      # explained < unexplained

    def boundary(self) -> None:
        for m in self.members:
            m.boundary()
        if self._on_boundary is not None:
            self._on_boundary()

    def report(self) -> dict:
        sel = self.selected()
        return {
            "steps": self._n,
            "residuals": {m.name: round(self.mean(m.name), 4) for m in self.members},
            "has_self": sorted(m.name for m in self.members if m.has_self()),
            "selected": sel.name if sel else None,
            "unmodeled": self.unmodeled(),
            "contingency": {m.name: {a: round(v, 3) for a, v in m.contingency().items()}
                            for m in self.members},
            "reads": ("members are compared ONLY by their ground-facing residual, never by "
                      "judging each other. `unmodeled` is the family failing TOGETHER, which "
                      "instruments the failure side of independence and not the agreement side"),
        }
