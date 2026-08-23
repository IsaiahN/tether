"""The loop. Steps 1 to 5.

One track: an action is proposed by an utterance that type-checks and passes the gate, or
there is no action. There is no fast path, because a fast path is what makes the framework
optional.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from typing import Any

import grammar as G
from gamma import Ctx, Gamma, Term
from ledger import SPECIFIED, Ledger
from probe import Drive
from world import ACTIONS, M

sys.dont_write_bytecode = True

IDN = "idn"

# THE CODE, declared. Both halves of the bargain are lengths under it.
#   a correction on one slot-transition: log2(M) bits, a uniform code over the M values
#   a term of k atoms:                   (k+1) * log2(|atoms|+1), the atoms plus a stop
CODE = "uniform(M) per correction; (k+1)*log2(|atoms|+1) per term"

HELD, NOVEL, REBIND, MECHANISM = "held", "novel", "rebinding", "mechanism"

# why not the neighbouring bin. A bin without its discriminator is a label, not a diagnosis.
WHY_NOT = {
    HELD: "not novel: the slot is bound and the bound term predicted it",
    NOVEL: "not mechanism: too little history to distinguish a wrong model from a new one",
    REBIND: "not mechanism: a term already in the library explains the whole history",
    MECHANISM: "not rebinding: no library term explains the history, so the model is wrong",
}

TRANSITION, REWARD, BRACKET = "transition", "reward", "bracket"


def correction_bits(a: int, b: int) -> float:
    return 0.0 if a % M == b % M else math.log2(M)


def term_bits(k: int, alphabet: int) -> float:
    return (k + 1) * math.log2(alphabet + 1)


@dataclass
class Config:
    max_depth: int = 3
    budget: int = 4000
    mode: str = SPECIFIED


@dataclass
class SlotResidual:
    slot: str
    channel: str
    predicted: Any
    actual: Any
    bits: float

    @property
    def mass(self) -> float:
        return self.bits


@dataclass
class Report:
    cycles: int = 0
    bound: dict[str, str] = field(default_factory=dict)
    minted: list[str] = field(default_factory=list)
    settled: list[str] = field(default_factory=list)
    owed_import: set[str] = field(default_factory=set)
    abstained: dict[str, dict] = field(default_factory=dict)
    refusals: list[str] = field(default_factory=list)
    stopped_at_link: str = "1 - perception"


class Agent:
    def __init__(self, env: Any, gam: Gamma, cfg: Config | None = None,
                 led: Ledger | None = None) -> None:
        self.env, self.gamma = env, gam
        self.cfg = cfg if cfg is not None else Config()
        # not `led or ...`: an empty Ledger has len 0 and is therefore falsy
        self.led = led if led is not None else Ledger(mode=self.cfg.mode)
        self.slots = env.slots()
        self.bound: dict[str, str] = {}
        self.history: dict[str, list[tuple[int, str, int]]] = {s: [] for s in self.slots}
        self.owed_import: set[str] = set()
        self.abstained: dict[str, dict] = {}
        self.candidates: dict[str, int] = {}     # term -> cycle accepted, awaiting the ground
        self.settled: set[str] = set()
        self.drive = Drive()
        self.cycle = 0
        self._prev_bet: str | None = None
        self._prev_pred: dict[str, int] | None = None
        self.refusals: list[str] = []

    # -- step 1 -----------------------------------------------------------------------

    def _predict(self, slot: str, before: int, action: str) -> int:
        term = self.gamma.library[self.bound.get(slot, IDN)]
        return term.apply(before, Ctx(action=action)) % M

    def perceive(self, action: str) -> dict[str, SlotResidual]:
        before = self.env.observe()
        pred = {s: self._predict(s, before[s], action) for s in self.slots}
        _, deg_before = self.env.objective()
        self.env.step(action)
        after = self.env.observe()
        name, deg_after = self.env.objective()

        res: dict[str, SlotResidual] = {}
        for s in self.slots:
            r = SlotResidual(s, TRANSITION, pred[s], after[s], correction_bits(pred[s], after[s]))
            res[s] = r
            self.history[s].append((before[s], action, after[s]))
            self.led.record(self.cycle, "PERCEIVE", s, "bet", channel=TRANSITION,
                            predicted=pred[s], actual=after[s], mass=r.bits,
                            bound=self.bound.get(s, IDN))
            self.drive.note(action, r.bits > 0)

        # the reward channel: on the figures, and reported here. Its remedy is the
        # composition of actions, which is not built -- so it is recorded, not actioned.
        self.led.record(self.cycle, "PERCEIVE", "@objective", "bet", channel=REWARD,
                        objective=name, degree=round(deg_after, 4),
                        mass=round(1.0 - deg_after, 4), moved=round(deg_after - deg_before, 4))
        self._route_reward(deg_after, deg_after - deg_before)
        # the bracket channel: this env defines no coarse view, so it is inert. Stated.
        self.led.record(self.cycle, "PERCEIVE", "@bracket", "bet", channel=BRACKET,
                        mass=0.0, inert="env.transform() is None; no coarse view defined")
        self._prev_pred = pred
        return res

    def _route_reward(self, degree: float, moved: float) -> None:
        """The reward channel is a channel of R, so the boundary diff sorts it too.

        It is routed and diagnosed here; its remedy -- composing actions that advance the
        objective -- is not built, and the entry says so rather than going silent.
        """
        self.drive.note_score(moved > 0)
        if degree >= 1.0:
            b, why = HELD, "not novel: the objective is satisfied, nothing owed"
        elif self.cycle < 2:
            b, why = NOVEL, "not mechanism: too little history on the objective"
        elif moved > 0:
            b, why = REBIND, "not mechanism: the current approach advanced the degree"
        else:
            b, why = MECHANISM, "not rebinding: nothing in the library advances the degree"
        self.led.record(self.cycle, "ROUTE", "@objective", "route", bin=b, why_not=why,
                        channel=REWARD, degree=round(degree, 4),
                        remedy="deferred: composition of actions is not built at agent scale")

    # -- step 2 -----------------------------------------------------------------------

    def _library_fit(self, slot: str, exclude: str | None) -> str | None:
        hist = self.history[slot]
        fits = [(len(t), n) for n, t in self.gamma.library.items()
                if n != exclude and self._explains(t, hist)]
        return min(fits)[1] if fits else None

    @staticmethod
    def _explains(term: Term, hist: list[tuple[int, str, int]]) -> bool:
        return bool(hist) and all(term.apply(b, Ctx(action=a)) % M == c % M for b, a, c in hist)

    def route(self, res: dict[str, SlotResidual]) -> list[tuple[str, str, str | None]]:
        out = []
        for slot, r in res.items():
            if r.mass == 0.0:
                b, fit = HELD, None
            elif len(self.history[slot]) < 2:
                b, fit = NOVEL, None
            else:
                fit = self._library_fit(slot, self.bound.get(slot))
                b = REBIND if fit else MECHANISM
            out.append((slot, b, fit))
            self.led.record(self.cycle, "ROUTE", slot, "route", bin=b,
                            why_not=WHY_NOT[b], support=len(self.history[slot]))
        return out

    # -- steps 3 to 5 -------------------------------------------------------------------

    def _accumulated(self, slot: str, term: Term) -> float:
        """|R| over the slot's whole history. Accumulated, because the model cost is paid
        once and the savings scale with n -- which is what makes the bargain discriminate.
        No min_support: the arithmetic is its own support gate."""
        return sum(correction_bits(term.apply(b, Ctx(action=a)), c)
                   for b, a, c in self.history[slot])

    def mint(self, slot: str) -> None:
        hist = self.history[slot]
        base = self._accumulated(slot, self.gamma.library[self.bound.get(slot, IDN)])
        guards = {"support": base > 0.0, "reachability": False, "novelty": False}
        cuts: list[dict] = []
        best: tuple[float, float, Term] | None = None
        seen = 0

        if guards["support"]:
            for cand in self.gamma.enumerate_closure("val", "val", self.cfg.max_depth,
                                                     self.cfg.budget):
                seen += 1
                if self.gamma.is_atom(cand) or cand.name in self.gamma.library:
                    cuts.append({"name": cand.name, "rank": seen, "reversible": True,
                                 "reason": "not-novel"})
                    continue
                guards["novelty"] = True
                left = self._accumulated_with(hist, cand)
                cost = term_bits(len(cand), self.gamma.alphabet)
                if not cost + left < base:
                    cuts.append({"name": cand.name, "rank": seen, "reversible": True,
                                 "reason": "does-not-pay"})
                    continue
                guards["reachability"] = True
                if best is None or left < best[0]:
                    best = (left, cost, cand)
                if left == 0.0:
                    break

        exhausted = seen >= self.cfg.budget
        detail = {"guards": guards, "candidates_seen": seen, "code": CODE,
                  "base_bits": round(base, 3), "cuts": cuts[:12],
                  "budget_exhausted": exhausted, "depth": self.cfg.max_depth}

        if best is None:
            # nothing in closure(Gamma) CLOSES R, and nothing even PAYS. Only IMPORT moves
            # the wall, and this build has no second frame -- so the debt is recorded.
            detail["verdict"] = "unreached"
            detail["note"] = "unreached at this budget; not a proof of unreachable"
            self.owed_import.add(slot)
            self.abstained[slot] = {"depth": self.cfg.max_depth, "candidates": seen,
                                    "base_bits": round(base, 3)}
            self.led.record(self.cycle, "MINT", slot, "park", **detail)
            return

        left, cost, term = best
        self.gamma.accept(term, seq=len(self.led), residual=f"{slot}@{self.cycle}")
        self.bound[slot] = term.name
        closes = left == 0.0
        # only a term that CLOSED R is eligible to settle. A partial term was already
        # observed to fail on the history it was fitted to, so a later lucky hit is not
        # the ground settling it -- it stays a candidate until something closes.
        if closes:
            self.candidates[term.name] = self.cycle
        if not closes:
            self.owed_import.add(slot)
        else:
            self.owed_import.discard(slot)
            self.abstained.pop(slot, None)
        self.led.record(self.cycle, "MINT", slot, "mint", verdict="pays", closes=closes,
                        term=term.name, term_bits=round(cost, 3), left_bits=round(left, 3),
                        **detail)
        self.led.record(self.cycle, "ACCEPT", slot, "accept", term=term.name,
                        origin=term.origin, seq=len(self.led),
                        status="candidate", cited="no: candidate may be held, not cited")

    def _accumulated_with(self, hist: list[tuple[int, str, int]], term: Term) -> float:
        return sum(correction_bits(term.apply(b, Ctx(action=a)), c) for b, a, c in hist)

    def settle(self, res: dict[str, SlotResidual]) -> None:
        """The ground settles it, by held-out payment: a term predicts a transition it was
        never fitted to. A gate passing is not the ground."""
        for slot, r in res.items():
            name = self.bound.get(slot)
            if not name or name in self.settled:
                continue
            born = self.candidates.get(name)
            if born is None or born >= self.cycle or r.mass > 0.0:
                continue
            self.settled.add(name)
            self.led.record(self.cycle, "SETTLE", slot, "settle", term=name,
                            status="accepted", verdict="held on a transition it was not fitted to",
                            held_out_cycle=self.cycle, fitted_through=born)

    # -- the utterance: the only way an action is proposed --------------------------------

    def _utter(self, action: str, before: dict[str, int], focal: str) -> tuple[str, list]:
        see = [G.compose(G.SEE, G.Leaf(G.T.OBJECT, s), G.Leaf(G.T.REGION, s),
                         G.Leaf(G.T.ATTR, before[s])) for s in self.slots]
        per = G.compose(G.PERCEIVE, *see)
        pid = f"p{self.cycle}"

        name, deg = self.env.objective()
        want = G.compose(G.WANT, G.compose("ALL", G.compose(
            "BECOME", G.Leaf(G.T.OBJECT, "slot"), G.Leaf(G.T.ATTR, 0))))

        bound = self.bound.get(focal)
        refs = [G.ref(pid, "perceive")] + ([G.ref(bound, "term")] if bound else [])
        ground = G.compose(G.GROUND, *refs)

        if bound:
            pred = self._predict(focal, before[focal], action)
            bet = G.compose("BECOME", G.Leaf(G.T.OBJECT, focal), G.Leaf(G.T.ATTR, pred))
            der = G.compose(G.DERIVE, ground, G.ref(bound, "term"), bet)
            pay = G.compose(G.PAY, G.price(float(len(self.history[focal])),
                                           len(self.history[focal])))
        else:
            der = G.compose(G.DERIVE, ground, G.T.PRED)       # the typed hole: a probe
            pay = G.compose(G.PAY, G.price(None, None, "explicit-null: nothing bound"))

        bet_t = G.compose(G.BET, want, ground, der, pay)
        bid = f"b{self.cycle}"
        act = G.compose(G.ACT, G.compose(G.NEED, G.ref(bid, "bet"),
                                         G.Leaf(G.T.ATTR, action)))
        return bid, [("PERCEIVE", pid, per), ("BET", bid, bet_t), ("ACT", f"a{self.cycle}", act)]

    # -- driving ---------------------------------------------------------------------------

    def step(self, action: str | None = None) -> bool:
        """One turn. Returns False if no action was proposed -- which is a legal outcome."""
        before = self.env.observe()
        focal = max(self.slots, key=lambda s: len(self.history[s]) and 1 or 0)
        focal = next((s for s in self.slots if s in self.owed_import), focal)
        action = action or self.drive.choose(ACTIONS, self.cycle)

        try:
            bid, utts = self._utter(action, before, focal)
        except G.Ill as exc:
            self.refusals.append(str(exc))
            self.led.record(self.cycle, "PERCEIVE", focal, "refused", reason=str(exc))
            return False

        for kind, uid, term in utts:
            # all three belong to step 1 -- "bet, act, observe" is one step
            self.led.record(self.cycle, "PERCEIVE", focal, "utterance", kind=kind,
                            id=uid, text=repr(term),
                            heads=[a.head for a in term.args if hasattr(a, "head")])

        res = self.perceive(action)
        for slot, b, fit in self.route(res):
            if b == REBIND and fit:
                self.bound[slot] = fit
                self.owed_import.discard(slot)
                self.abstained.pop(slot, None)
                self.led.record(self.cycle, "ACCEPT", slot, "rebind", term=fit,
                                status="candidate", note="refit; the library did not change")
            elif b == MECHANISM:
                self.mint(slot)
        if self.drive.bored():
            self.led.record(self.cycle, "MINT", "@probe", "probe",
                            **self.drive.report(), guards={"support": False,
                                                           "reachability": False,
                                                           "novelty": False},
                            note="density(R) at zero on the transition channel; perturbing")
        self.settle(res)
        self.cycle += 1
        self.led.record(self.cycle - 1, "REPEAT", "@loop", "repeat",
                        gamma_size=len(self.gamma.library), owed=sorted(self.owed_import))
        return True

    def run(self, cycles: int) -> Report:
        for _ in range(cycles):
            self.step()
        rep = Report(cycles=self.cycle, bound=dict(self.bound),
                     minted=[e.detail["term"] for e in self.led.by_event("mint")],
                     settled=sorted(self.settled), owed_import=set(self.owed_import),
                     abstained=dict(self.abstained), refusals=list(self.refusals))
        rep.stopped_at_link = self._link()
        return rep

    def _link(self) -> str:
        """Figure 3's diagnostic: which link did it stop at, and was that measured?"""
        if not any(self.history.values()):
            return "1 - perception (measured: no observations)"
        if not self.gamma.library:
            return "2 - vocabulary (measured: empty library)"
        if not self.settled:
            return "5 - learn and carry (measured: nothing settled against the ground)"
        if self.owed_import:
            return (f"2 - vocabulary (measured: {len(self.owed_import)} "
                "slot(s) unreached at budget)")
        return "3 - the objective (measured: prediction closed, no goal composition built)"
