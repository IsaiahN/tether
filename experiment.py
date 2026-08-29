"""§21.1 / 4e — the controlled experiment, and it is the only one the loop can run.

§21.1: *everywhere else the agent gets **observational** data, and correlation is cheap;
causation is not, because **you can never re-run the same moment.** A level-resetting loss
breaks that **because the games are deterministic**: same starting board, vary exactly one
action, observe the difference.*

**ITS PRECONDITION IS A PROPERTY OF THE DOMAIN, NOT OF THE DESIGN**, and it was confirmed
before this was written rather than after: `ls20` returns `GAME_OVER` on 172 of 300 blind
steps, so a level-resetting loss exists to be exploited. **A mechanism built on a panel that
cannot supply its precondition is the fourth defect this project has recorded that way.**

WHAT MAKES IT CONTROLLED. Two visits to the SAME state signature, differing in EXACTLY ONE
action, with both outcomes read. Anything else is two observations that happen to look alike.
So the signature is the full slot reading -- not a summary, not a hash of a summary -- because
**two boards agreeing on a digest is Figure 2's collapse at the level of the key.**

**THE OUTCOME IS THE WORLD'S RESPONSE, NOT THE MODEL'S RESIDUAL, AND THE FIRST VERSION HAD IT
WRONG.** §21.1 asks *did the world do something different* -- it is *disambiguating
intervention* (Schulz & Bonawitz) and *causal structure learning from intervention* (Gopnik),
**both about the world's causal structure and neither about calibrating a predictor.** The
residual measures the MODEL. **Both are per-slot quantities available at the same instant, so
the substitution is invisible** -- the same shape as `_rtype` taking a plausible neighbour when
the right quantity was one layer down.

**AND IT DISSOLVES A CONFOUND RATHER THAN MANAGING ONE.** With the residual as the outcome, two
visits whose slots were all `IDN`-bound produce an identical reading and the model state is a
term in the measurement. **With the world's response, the model is not in the comparison at
all**, so two identical model states are simply irrelevant.

**AND THE READING IS EXISTENTIAL, NEVER A SUM.** `any slot differing` rather than a total: an
aggregate can be flat while every slot underneath it moved, which is the construction the hard
rules refuse and which the first version shipped.

**IT RECORDS, IT DOES NOT DECIDE.** A pair is evidence about one action's effect; what that
means for a bet is the loop's, and what it means for a diagnosis is a seat's. The rung
reports; the layer above judges.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field

sys.dont_write_bytecode = True


@dataclass
class Controlled:
    """Visits keyed by exact state, so a repeat is a re-run rather than a resemblance."""

    seen: dict[tuple, dict[str, dict]] = field(default_factory=dict)
    pairs: list[dict] = field(default_factory=list)

    @staticmethod
    def signature(state: dict[str, int]) -> tuple:
        """The whole reading, ordered. **Not a hash and not a summary.**

        A digest would let two different boards collide into one key, and the mechanism's
        entire claim is *the same moment, re-run* -- which a collision silently falsifies.
        """
        return tuple(sorted(state.items()))

    def visit(self, state: dict[str, int], action: str,
              outcome: dict[str, int]) -> list[dict]:
        """One (state, action, outcome). Returns EVERY pair this completes.

        A pair is the same signature under a DIFFERENT action. The same action twice is a
        determinism check, not an experiment, and is kept separately rather than counted --
        it says the domain held still, which is the precondition rather than the result.

        **AGAINST EVERY PRIOR ACTION, NOT THE FIRST, AND THE FIRST VERSION DID THE LATTER.**
        It paired on `sorted(prior)[0]`, giving `n-1` pairs where the check needs
        `n(n-1)/2` -- so `ls20`'s *3 of 3 discriminating* said **ACTION1 differs from each of
        the others** and said **nothing about whether 2, 3 and 4 differ from each other.**
        That is exactly §2622 §5's third required property, ***two actuators that are
        indistinguishable, so `I cannot tell these apart` is reachable*** -- **untestable
        under a reading that sounded complete.**
        """
        sig = self.signature(state)
        prior = self.seen.setdefault(sig, {})
        # DID THIS ACTION CHANGE ANYTHING AT ALL? Not a comparison -- §5's *an actuator that
        # does nothing* needs one action's before against its after, and a PAIR can never
        # say it: two actions that both do nothing are indistinguishable AND inert, and the
        # pair reports only the first.
        moved_self = sorted(k for k in set(state) | set(outcome)
                            if state.get(k) != outcome.get(k))
        if action in prior:
            prior[action]["repeats"] += 1
            prior[action]["stable"] = prior[action]["stable"] and (
                prior[action]["outcome"] == outcome)
            return []
        made = []
        for other in sorted(prior):
            a_out = prior[other]["outcome"]
            moved = sorted(k for k in set(a_out) | set(outcome)
                           if a_out.get(k) != outcome.get(k))
            pair = {"varied": (other, action), "slots": len(state),
                    "slots_differing": moved, "n_differing": len(moved),
                    "discriminates": bool(moved),
                    "reads": ("same state, exactly one action varied, and the WORLD's "
                              "per-slot response compared. ANY slot differing is the "
                              "reading -- an existential, never a sum")}
            self.pairs.append(pair)
            made.append(pair)
        prior[action] = {"outcome": outcome, "repeats": 0, "stable": True,
                         "moved": moved_self, "inert": not moved_self}
        return made

    def determinism(self) -> dict:
        """What the repeats say about the DOMAIN, reported apart from the experiments.

        §21.1's precondition is determinism, and it is a property of the world rather than a
        design choice -- so it is MEASURED here and never assumed, and an unstable repeat
        invalidates every pair drawn from that state rather than merely being noted.
        """
        reps = [v for a in self.seen.values() for v in a.values() if v["repeats"]]
        return {"states_revisited": sum(1 for a in self.seen.values() if any(
                    v["repeats"] for v in a.values())),
                "repeated_readings": len(reps),
                "unstable": sum(1 for v in reps if not v["stable"])}

    def vacuity(self) -> dict:
        """§2622 §5, stated in advance and answerable only with all pairs.

        > *If motor learning does not fire, that has two readings and they must be separable
        > BEFORE the run: **the mechanism does not work** vs **this world could not have
        > shown it**. This world can show it only if all three are present and reachable.*

        **Each of the three is a reachability claim about the PANEL, not a result** -- and
        `absent` here means a null on motor learning would be **vacuous rather than a
        finding.**
        """
        acts = {a: v for byact in self.seen.values() for a, v in byact.items()}
        inert = sorted(a for a, v in acts.items() if v.get("inert"))
        same = [p["varied"] for p in self.pairs if not p["discriminates"]]
        return {
            "discoverable_effect": sorted(a for a, v in acts.items() if v.get("moved")),
            "does_nothing": inert,
            "indistinguishable": same,
            "all_three_present": bool(acts) and bool(inert) and bool(same)
                                 and any(v.get("moved") for v in acts.values()),
            "reads": ("all three must be REACHABLE or a motor-learning null is vacuous "
                      "rather than a result. `does_nothing` needs one action's before "
                      "against its after; `indistinguishable` needs every pair, not n-1"),
        }

    def report(self) -> dict:
        d = self.determinism()
        return {"states_seen": len(self.seen), "controlled_pairs": len(self.pairs),
                "discriminating": sum(1 for p in self.pairs if p["discriminates"]),
                **d, "vacuity": self.vacuity(),
                "reads": ("a pair is the same state with exactly one action varied; "
                          "`unstable` above zero means the domain did not hold still and "
                          "the pairs from that state are not controls")}
