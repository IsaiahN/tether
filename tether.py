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
import instruments as I
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


def pays(cost: float, left: float, base: float) -> bool:
    """The bargain. Strict: a tie does not license a new term."""
    return cost + left < base


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
    demoted: list[str] = field(default_factory=list)
    chain: dict = field(default_factory=dict)
    phases: dict = field(default_factory=dict)
    clocks: dict = field(default_factory=dict)
    retro: list = field(default_factory=list)
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
        # the whole before-state is kept, because an operand is another slot's past value
        self.trace: list[tuple[dict[str, int], str, dict[str, int]]] = []
        self.owed_import: set[str] = set()
        self.abstained: dict[str, dict] = {}
        self.candidates: dict[str, int] = {}     # term -> cycle accepted, awaiting the ground
        self.settled: set[str] = set()
        self.demoted: list[str] = []
        self.chain = I.Chain()
        self.phases = I.Phases()
        self.clocks = I.Clocks()
        self.retro: list[dict] = []
        self.drive = Drive()
        self.cycle = 0
        self._prev_bet: str | None = None
        self._prev_pred: dict[str, int] | None = None
        self.refusals: list[str] = []

    # -- step 1 -----------------------------------------------------------------------

    def history(self, slot: str) -> list[tuple[dict[str, int], str, int]]:
        """(before-state, action, this slot's after-value) for every recorded step."""
        return [(b, a, af[slot]) for b, a, af in self.trace]

    @staticmethod
    def _ops(term: Term, state: dict[str, int]) -> tuple:
        return (state[term.operand],) if term.operand else ()

    def _predict(self, slot: str, state: dict[str, int], action: str) -> int:
        term = self.gamma.library[self.bound.get(slot, IDN)]
        return term.apply(state[slot], Ctx(action=action, operands=self._ops(term, state))) % M

    def perceive(self, action: str) -> dict[str, SlotResidual]:
        before = self.env.observe()
        pred = {s: self._predict(s, before, action) for s in self.slots}
        _, deg_before = self.env.objective()
        self.env.step(action)
        after = self.env.observe()
        name, deg_after = self.env.objective()

        res: dict[str, SlotResidual] = {}
        for s in self.slots:
            r = SlotResidual(s, TRANSITION, pred[s], after[s], correction_bits(pred[s], after[s]))
            res[s] = r
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
        self.chain.note_diff(any(r.mass > 0 for r in res.values()))
        self.trace.append((before, action, after))
        self.gamma.tick = len(self.trace)
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
        hist = self.history(slot)
        fits = [(len(t), n) for n, t in self.gamma.library.items()
                if n != exclude and self._explains(t, slot, hist)]
        return min(fits)[1] if fits else None

    def _explains(self, term: Term, slot: str, hist) -> bool:
        return bool(hist) and self._left(term, slot, hist) == 0.0

    def _left(self, term: Term, slot: str, hist) -> float:
        """What the term leaves unexplained across the slot's history, in bits."""
        total = 0.0
        for state, action, actual in hist:
            got = term.apply(state[slot], Ctx(action=action, operands=self._ops(term, state)))
            total += correction_bits(got, actual)
        return total

    def route(self, res: dict[str, SlotResidual]) -> list[tuple[str, str, str | None]]:
        out = []
        for slot, r in res.items():
            if r.mass == 0.0:
                b, fit = HELD, None
            elif len(self.trace) < 2:
                b, fit = NOVEL, None
            else:
                fit = self._library_fit(slot, self.bound.get(slot))
                b = REBIND if fit else MECHANISM
            out.append((slot, b, fit))
            self.led.record(self.cycle, "ROUTE", slot, "route", bin=b,
                            why_not=WHY_NOT[b], support=len(self.trace))
        return out

    # -- steps 3 to 5 -------------------------------------------------------------------

    def _accumulated(self, slot: str, term: Term) -> float:
        """|R| over the slot's whole history. Accumulated, because the model cost is paid
        once and the savings scale with n -- which is what makes the bargain discriminate.
        No min_support: the arithmetic is its own support gate."""
        return self._left(term, slot, self.history(slot))

    def _bindings(self, slot: str) -> list[str | None]:
        """Which slots may fill operand 0. None first -- a unary term is cheaper, so it
        wins when both fit, which is Occam priced rather than preferred."""
        return [None] + [s for s in self.slots if s != slot]

    def mint(self, slot: str) -> None:
        hist = self.history(slot)
        base = self._accumulated(slot, self.gamma.library[self.bound.get(slot, IDN)])
        guards = {"support": base > 0.0, "reachability": False, "novelty": False}
        cuts: list[dict] = []
        best: tuple[float, float, Term] | None = None
        stats: dict = {"seen": 0, "budget_spent": False, "depth_exhausted": True,
                       "units": self.gamma.alphabet, "estimate": 0}
        rank = 0

        if guards["support"]:
            for cand in self.gamma.enumerate_closure("val", "val", self.cfg.max_depth,
                                                     self.cfg.budget, stats):
                for bind in (self._bindings(slot) if cand.reads_operand else [None]):
                    rank += 1
                    term = Term(cand.atoms, operand=bind)
                    if self.gamma.is_atom(term) or term.name in self.gamma.library:
                        cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                     "reason": "not-novel"})
                        continue
                    guards["novelty"] = True
                    left = self._left(term, slot, hist)
                    cost = term_bits(len(term), self.gamma.alphabet)
                    if not pays(cost, left, base):
                        cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                     "reason": "does-not-pay"})
                        continue
                    guards["reachability"] = True
                    if best is None or left < best[0]:
                        best = (left, cost, term)
                if best is not None and best[0] == 0.0:
                    break

        seen = stats["seen"]
        est = max(stats["estimate"], seen)
        detail = {"guards": guards, "candidates_seen": seen, "candidates_tried": rank,
                  "code": CODE, "base_bits": round(base, 3), "cuts": cuts[:12],
                  "budget_exhausted": bool(stats["budget_spent"]),
                  "depth": self.cfg.max_depth, "units": stats["units"],
                  "space_estimate": est,
                  "coverage": round(seen / est, 6) if est else 0.0}

        if best is None:
            # THE VERDICT IS NOT ONE WORD. "I stopped early" and "the whole space at this
            # depth does not contain one" are different claims and only one is strong.
            if not guards["support"]:
                detail["verdict"] = "no_support"
            elif stats["budget_spent"]:
                detail["verdict"] = "budget_spent"
                detail["note"] = (f"stopped early; coverage {detail['coverage']:.4f}. "
                                  "Says nothing about whether a term exists")
            elif not guards["novelty"]:
                detail["verdict"] = "not_novel"
                detail["note"] = "the machinery worked; the answer was already known"
            else:
                detail["verdict"] = "depth_exhausted"
                detail["note"] = ("the whole space at this depth was seen and none paid; "
                                  "not at this depth, NOT unreachable")
            if detail["verdict"] in ("budget_spent", "depth_exhausted"):
                self.owed_import.add(slot)
                self.abstained[slot] = {"depth": self.cfg.max_depth, "candidates": seen,
                                        "coverage": detail["coverage"],
                                        "verdict": detail["verdict"],
                                        "units_then": stats.get("units", 0),
                                        "base_bits": round(base, 3)}
            self.led.record(self.cycle, "MINT", slot, "park", **detail)
            return

        left, cost, term = best
        self.gamma.accept(term, seq=len(self.led), residual=f"{slot}@{self.cycle}")
        self.bound[slot] = term.name
        closes = left == 0.0
        if closes:
            self.candidates[term.name] = self.cycle
            self.owed_import.discard(slot)
            self.abstained.pop(slot, None)
        else:
            # it pays and it is not the mechanism. Accepting is correct; settling for it
            # is not -- the slot keeps owing until something closes R.
            self.owed_import.add(slot)
        detail["verdict"] = "pays"
        detail["closes"] = closes
        if not closes:
            detail["note"] = "pays but does not close R; the slot still owes"
        detail.update(term=term.name, term_depth=len(term), operand=term.operand,
                      term_bits=round(cost, 3), left_bits=round(left, 3))
        self.led.record(self.cycle, "MINT", slot, "mint", **detail)
        self.led.record(self.cycle, "ACCEPT", slot, "accept", term=term.name,
                        origin=term.origin, seq=len(self.led),
                        status="candidate", cited="no: candidate may be held, not cited")
        self.chain.note_mint()
        self.sweep(term, slot)

    def _reach(self, slot: str, hist: list) -> tuple[float, Term] | None:
        """Re-run the search for a parked slot because the UNIT SET grew.

        This is the chunking claim made falsifiable: closure(Gamma) is unchanged and no
        atom was added, but a settled term now counts as one unit, so a composition that
        was past max_depth in atoms can be within it in units. No actions are spent -- it
        re-reads evidence already on the trace -- so it is search cost, never budget.
        """
        best = None
        for cand in self.gamma.enumerate_closure("val", "val", self.cfg.max_depth,
                                                 self.cfg.budget):
            for bind in self._bindings(slot):
                t = Term(cand.atoms, operand=bind)
                left = self._left(t, slot, hist)
                if best is None or left < best[0]:
                    best = (left, t)
                if left == 0.0:
                    return best
        return best

    def sweep(self, term: Term, origin_slot: str) -> None:
        """Re-run a newly accepted term against every outstanding parked residual.

        Costs no actions -- it re-reads evidence already paid for. And a term minted for
        one slot that explains another slot's old residual is an operator REUSED on a task
        it was not minted for, which is the stated bar for the whole loop firing once.
        """
        outstanding = sorted(self.owed_import - {origin_slot})
        units_now = len(self.gamma.units())

        def stale(rec: dict) -> bool:
            """`depth_exhausted` is not permanent. It means 'the whole space AT THIS UNIT
            SET', so a settled chunk that adds a unit retracts it -- the reachable set
            genuinely grew. Until then it is a depth verdict, already recorded, and
            charging it to the reuse funnel would let a missing second task read as
            MINTED_UNUSED, an architecture verdict."""
            return (rec.get("verdict") != "depth_exhausted"
                    or units_now > rec.get("units_then", 0))

        eligible = [s for s in outstanding if stale(self.abstained.get(s, {}))]
        if not eligible:
            self.chain.reuse_branch["no-eligible-target"] += 1
            return
        for slot in eligible:
            how = "direct"
            hist = self.history(slot)
            base = self._accumulated(slot, self.gamma.library[self.bound.get(slot, IDN)])
            best = None
            for bind in self._bindings(slot):
                cand = Term(term.atoms, operand=bind)
                left = self._left(cand, slot, hist)
                if best is None or left < best[0]:
                    best = (left, cand)
            left, cand = best
            rec = self.abstained.get(slot, {})
            if left > 0.0 and units_now > rec.get("units_then", units_now):
                # counted so its inertness is a measured zero, not hidden dead code
                self.chain.reuse_branch["rescan"] += 1
                found = self._reach(slot, hist)
                if found is not None and found[0] < left:
                    left, cand = found
                    how = "chunk"
            if left == 0.0:
                self.chain.note_reuse_attempt(f"closed:{how}")
                self.chain.note_reused()
                self.chain.note_cleared()
                self.bound[slot] = (cand.name if cand.name in self.gamma.library
                                    else self._install_reuse(cand, slot))
                self.owed_import.discard(slot)
                born = self.abstained.pop(slot, {})
                rec = {"term": cand.name, "slot": slot, "cycle": self.cycle,
                       "was": born.get("verdict"), "via": how}
                self.retro.append(rec)
                self.led.record(self.cycle, "MINT", slot, "retro", term=cand.name,
                                verdict="retroactive resolution", reused_from=origin_slot,
                                guards={"support": True, "reachability": True,
                                        "novelty": False},
                                note="minted elsewhere; it explains this slot's parked residual",
                                was=rec["was"], via=rec["via"])
            elif left < base:
                self.chain.note_reuse_attempt("did-not-pay")
            else:
                self.chain.note_reuse_attempt("no-split")

    def _install_reuse(self, cand: Term, slot: str) -> str:
        self.gamma.accept(cand, seq=len(self.led), residual=f"reuse:{slot}@{self.cycle}")
        return cand.name

    def settle(self, res: dict[str, SlotResidual]) -> None:
        """The ground settles it, by held-out payment: a term predicts a transition it was
        never fitted to. And it un-settles the same way -- a settled term that mispredicts
        on fresh evidence is DEMOTED, defeasibly, never deleted."""
        for slot, r in res.items():
            name = self.bound.get(slot)
            if not name:
                continue
            if r.mass > 0.0:
                # express-before-judge: this term actually predicted, and was wrong
                if self.gamma.refute(name):
                    self.demoted.append(name)
                    self.led.record(self.cycle, "SETTLE", slot, "demote", term=name,
                                    status="candidate",
                                    verdict="mispredicted on fresh evidence",
                                    rejections=round(self.gamma.rejection_of(name), 3),
                                    note="defeasible: the rejection decays and it may settle again")
                continue
            born = self.candidates.get(name)
            if born is None or born >= self.cycle or self.gamma.is_settled(name):
                continue
            self.gamma.settle(name)
            self.settled.add(name)
            self.led.record(self.cycle, "SETTLE", slot, "settle", term=name,
                            status="accepted",
                            verdict="held on a transition it was not fitted to",
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
            pred = self._predict(focal, before, action)
            bet = G.compose("BECOME", G.Leaf(G.T.OBJECT, focal), G.Leaf(G.T.ATTR, pred))
            der = G.compose(G.DERIVE, ground, G.ref(bound, "term"), bet)
            pay = G.compose(G.PAY, G.price(float(len(self.trace)), len(self.trace)))
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
        focal = self.slots[0]
        focal = next((s for s in self.slots if s in self.owed_import), focal)
        action = action or self.drive.choose(ACTIONS, self.cycle)
        # PROBE when nothing is bound to look at, DIRECTED when a term is driving the bet.
        # STRATEGY arrives with routines and is 0 until then -- an honest zero, not a gap.
        phase = I.DIRECTED if self.bound.get(focal) else I.PROBE
        self.phases.note(phase)

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
        _, degree = self.env.objective()
        self.clocks.note(self.drive.err, 1 if degree >= 1.0 else 0)
        self.cycle += 1
        self.led.record(self.cycle - 1, "REPEAT", "@loop", "repeat",
                        phase=phase, stage=self.chain.seg.stage(),
                        gamma_size=len(self.gamma.library), owed=sorted(self.owed_import))
        return True

    def run(self, cycles: int) -> Report:
        for _ in range(cycles):
            self.step()
        rep = Report(cycles=self.cycle, bound=dict(self.bound),
                     minted=[e.detail["term"] for e in self.led.by_event("mint")],
                     demoted=list(self.demoted),
                     settled=sorted(self.settled), owed_import=set(self.owed_import),
                     abstained=dict(self.abstained), refusals=list(self.refusals))
        self.chain.close("run_end")
        rep.chain = self.chain.report()
        rep.phases = self.phases.report()
        rep.clocks = self.clocks.report()
        rep.retro = list(self.retro)
        rep.stopped_at_link = self._link()
        return rep

    def _link(self) -> str:
        """Figure 3's diagnostic: which link did it stop at, and was that measured?"""
        if not self.trace:
            return "1 - perception (measured: no observations)"
        if not self.gamma.library:
            return "2 - vocabulary (measured: empty library)"
        if not self.settled:
            return "5 - learn and carry (measured: nothing settled against the ground)"
        if self.owed_import:
            return (f"2 - vocabulary (measured: {len(self.owed_import)} "
                "slot(s) unreached at budget)")
        return "3 - the objective (measured: prediction closed, no goal composition built)"
